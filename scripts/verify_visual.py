#!/usr/bin/env python3
"""Offline visual, font, CJK, and component parity verifier for MD3E starters.

Usage:
  python scripts/verify_visual.py
  python scripts/verify_visual.py --out-dir ./tmp/visual --baseline-dir ./tmp/baseline
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
import http.server
import json
from pathlib import Path
import sys
import tempfile
import threading
from typing import Any

from PIL import Image
import numpy as np
from playwright.sync_api import Browser, BrowserContext, Page, sync_playwright

ROOT_DIR = Path(__file__).resolve().parent.parent

SHARED_SELECTORS: dict[str, str] = {
    "btn-filled": ".md3e-btn--filled.md3e-btn--s",
    "btn-tonal": ".md3e-btn--tonal.md3e-btn--s",
    "btn-outlined": ".md3e-btn--outlined",
    "fab-medium": ".md3e-fab--medium",
    "switch": ".md3e-switch",
    "text-field": ".md3e-text-field",
    "toolbar-floating": ".toolbar-floating",
}

INDEX_SECTION_IDS = (
    "app-bar",
    "section-color",
    "section-shapes",
    "section-motion",
    "section-buttons",
    "section-expressive",
    "section-primitives",
    "floating-toolbar",
)

MINIMAL_SECTION_IDS = (
    "min-buttons",
    "min-fab",
    "min-switch",
    "min-text-field",
    "min-dialog",
    "min-toolbar",
)

PARITY_FIELDS: dict[str, tuple[str, ...]] = {
    "btn-filled": ("height", "borderRadius", "backgroundColor", "color"),
    "btn-tonal": ("height", "borderRadius", "backgroundColor", "color"),
    "btn-outlined": ("height", "borderRadius", "borderTopWidth", "color"),
    "fab-medium": ("width", "height", "borderRadius", "backgroundColor", "color"),
    "switch": ("width", "height", "borderRadius"),
    "text-field": ("height", "borderTopLeftRadius", "borderTopRightRadius"),
    "toolbar-floating": ("height", "borderRadius", "backgroundColor"),
    "dialog": ("borderRadius", "backgroundColor"),
}


@dataclass(frozen=True)
class CheckResult:
    """Single verification outcome."""

    name: str
    passed: bool
    detail: str


class _QuietHandler(http.server.SimpleHTTPRequestHandler):
    """Static file handler serving from the repository root without noisy logs."""

    def __init__(self, *args: Any, directory: str, **kwargs: Any) -> None:
        super().__init__(*args, directory=directory, **kwargs)

    def log_message(self, format: str, *args: Any) -> None:
        del format, args


def _start_server(repo_root: Path) -> tuple[http.server.ThreadingHTTPServer, int]:
    """Start an ephemeral localhost HTTP server serving repo_root."""

    class _BoundHandler(_QuietHandler):
        def __init__(self, *args: Any, **kwargs: Any) -> None:
            super().__init__(*args, directory=str(repo_root), **kwargs)

    httpd = http.server.ThreadingHTTPServer(("127.0.0.1", 0), _BoundHandler)
    httpd.daemon_threads = True
    port = int(httpd.server_address[1])

    def _serve() -> None:
        try:
            httpd.serve_forever()
        except OSError:
            pass

    thread = threading.Thread(target=_serve, daemon=True)
    thread.start()
    return httpd, port


def _launch_browser(playwright: Any) -> Browser:
    """Launch installed Chromium-family browser (Chrome, Edge, or Playwright default)."""
    last_exc: Exception | None = None
    for kwargs in (
        {"channel": "chrome", "headless": True},
        {"channel": "msedge", "headless": True},
        {"headless": True},
    ):
        try:
            return playwright.chromium.launch(**kwargs)
        except Exception as exc:  # noqa: BLE001 - try fallback browser channels
            last_exc = exc
    raise RuntimeError(f"Unable to launch any Chromium browser: {last_exc}")


def _open_offline_page(
    browser: Browser,
    url: str,
    viewport: dict[str, int],
    theme: str = "light",
    freeze_css: bool = True,
) -> tuple[BrowserContext, Page, dict[str, list[str]]]:
    """Open URL with external network blocked and collect runtime/network telemetry."""
    context = browser.new_context(viewport=viewport, device_scale_factor=1)
    telemetry: dict[str, list[str]] = {
        "console_errors": [],
        "page_errors": [],
        "failed_local": [],
        "blocked_external": [],
    }

    def _route_handler(route: Any) -> None:
        req_url = route.request.url
        if req_url.startswith(("http://127.0.0.1:", "http://localhost:", "data:", "blob:")):
            route.continue_()
        else:
            telemetry["blocked_external"].append(req_url)
            route.abort("blockedbyclient")

    context.route("**/*", _route_handler)
    page = context.new_page()
    page.on(
        "console",
        lambda msg: telemetry["console_errors"].append(msg.text)
        if msg.type == "error"
        else None,
    )
    page.on("pageerror", lambda err: telemetry["page_errors"].append(str(err)))
    page.on(
        "requestfailed",
        lambda req: telemetry["failed_local"].append(f"{req.url}: {req.failure}")
        if req.url.startswith(("http://127.0.0.1:", "http://localhost:"))
        else None,
    )

    page.goto(url, wait_until="load", timeout=30000)
    page.evaluate("(t) => document.documentElement.setAttribute('data-theme', t)", theme)
    page.evaluate(
        """async (freeze) => {
            await document.fonts.ready;
            if (freeze && !document.getElementById('__md3e_verify_freeze')) {
                const style = document.createElement('style');
                style.id = '__md3e_verify_freeze';
                style.textContent = `
                  *, *::before, *::after {
                    animation-play-state: paused !important;
                    transition: none !important;
                  }
                `;
                document.head.appendChild(style);
            }
            await new Promise((r) => requestAnimationFrame(() => requestAnimationFrame(r)));
        }""",
        freeze_css,
    )
    page.wait_for_timeout(120)
    return context, page, telemetry


def _audit_runtime_and_fonts(
    page: Page, telemetry: dict[str, list[str]], label: str
) -> list[CheckResult]:
    """Verify zero offline errors, loaded local fonts, icon ligatures, and CJK fallback."""
    results: list[CheckResult] = [
        CheckResult(
            f"{label}:offline-network",
            not telemetry["blocked_external"] and not telemetry["failed_local"],
            "blocked="
            f"{len(telemetry['blocked_external'])}, failed_local={len(telemetry['failed_local'])}"
            + (
                f" ({telemetry['blocked_external'][:3]})"
                if telemetry["blocked_external"]
                else ""
            ),
        ),
        CheckResult(
            f"{label}:runtime-errors",
            not telemetry["console_errors"] and not telemetry["page_errors"],
            f"console_errors={len(telemetry['console_errors'])}, page_errors={len(telemetry['page_errors'])}",
        ),
    ]

    probe = page.evaluate(
        """() => {
            const loadedFamilies = new Set();
            for (const f of document.fonts) {
                if (f.status === 'loaded') {
                    loadedFamilies.add(f.family.replace(/["']/g, ''));
                }
            }
            const sheetHrefs = [...document.styleSheets]
                .map((s) => s.href || '')
                .filter(Boolean);

            const badIcons = [];
            let checkedIcons = 0;
            for (const el of document.querySelectorAll('.material-symbols-outlined')) {
                const cs = getComputedStyle(el);
                if (cs.display === 'none' || cs.visibility === 'hidden') continue;
                const rect = el.getBoundingClientRect();
                if (rect.width === 0 || rect.height === 0) continue;
                checkedIcons += 1;
                const fs = parseFloat(cs.fontSize) || 24;
                const range = document.createRange();
                range.selectNodeContents(el);
                const textRect = range.getBoundingClientRect();
                const hasSymbolFamily = cs.fontFamily.toLowerCase().includes('material symbols');
                if (!hasSymbolFamily || textRect.width > fs * 1.45 || rect.width > fs * 1.45 || rect.height > fs * 1.6) {
                    badIcons.push({
                        text: (el.textContent || '').trim(),
                        family: cs.fontFamily,
                        rangeW: Math.round(textRect.width * 10) / 10,
                        boxW: Math.round(rect.width * 10) / 10,
                        fs: fs,
                    });
                }
            }

            let cjkEl = document.querySelector('[lang^="zh"]');
            let tempCjk = false;
            if (!cjkEl) {
                cjkEl = document.createElement('p');
                cjkEl.lang = 'zh-CN';
                cjkEl.textContent = '离线字体中文回退测试';
                cjkEl.style.cssText = 'position:fixed;left:0;top:0;opacity:0;pointer-events:none;font-family:var(--md-sys-typescale-plain-font);font-size:var(--md-sys-typescale-body-large-size, 16px);line-height:var(--md-sys-typescale-body-large-line-height, 26px);';
                document.body.appendChild(cjkEl);
                tempCjk = true;
            }
            const cjkCs = getComputedStyle(cjkEl);
            const cjkRect = cjkEl.getBoundingClientRect();
            const cjkFontFamily = cjkCs.fontFamily;
            const cjkFontSize = parseFloat(cjkCs.fontSize) || 16;
            const cjkLineHeight = parseFloat(cjkCs.lineHeight) || cjkFontSize;
            const canvas = document.createElement('canvas');
            canvas.width = 96;
            canvas.height = 36;
            const ctx = canvas.getContext('2d');
            let cjkInkPixels = 0;
            if (ctx) {
                ctx.font = `${cjkFontSize}px ${cjkFontFamily}`;
                ctx.fillStyle = '#000';
                ctx.fillText('中文设计', 2, 24);
                const data = ctx.getImageData(0, 0, 96, 36).data;
                for (let i = 3; i < data.length; i += 4) {
                    if (data[i] > 20) cjkInkPixels += 1;
                }
            }
            if (tempCjk) cjkEl.remove();

            return {
                loadedFamilies: [...loadedFamilies],
                hasLocalFontSheet: sheetHrefs.some((h) => h.includes('md3e-fonts.css')),
                checkedIcons,
                badIcons,
                cjkFontFamily,
                cjkWidth: Math.round(cjkRect.width * 10) / 10,
                cjkLineHeightRatio: Math.round((cjkLineHeight / cjkFontSize) * 100) / 100,
                cjkInkPixels,
                overflowX: document.documentElement.scrollWidth - window.innerWidth,
            };
        }"""
    )

    loaded = set(probe["loadedFamilies"])
    fonts_ok = (
        probe["hasLocalFontSheet"]
        and "Google Sans Flex" in loaded
        and "Material Symbols Outlined" in loaded
    )
    results.append(
        CheckResult(
            f"{label}:fonts-loaded",
            fonts_ok,
            f"localSheet={probe['hasLocalFontSheet']}, loaded={sorted(loaded)}",
        )
    )
    results.append(
        CheckResult(
            f"{label}:icon-ligatures",
            probe["checkedIcons"] > 0 and not probe["badIcons"],
            f"checked={probe['checkedIcons']}, oversized={probe['badIcons'][:3]}",
        )
    )
    cjk_has_fallback = any(
        fam in probe["cjkFontFamily"]
        for fam in ("PingFang SC", "Noto Sans SC", "Microsoft YaHei")
    )
    cjk_ok = (
        cjk_has_fallback
        and probe["cjkWidth"] > 0
        and probe["cjkLineHeightRatio"] >= 1.55
        and probe["cjkInkPixels"] > 20
    )
    results.append(
        CheckResult(
            f"{label}:cjk-fallback",
            cjk_ok,
            f"width={probe['cjkWidth']}, lhRatio={probe['cjkLineHeightRatio']}, "
            f"inkPx={probe['cjkInkPixels']}, stack={probe['cjkFontFamily']}",
        )
    )
    results.append(
        CheckResult(
            f"{label}:desktop-overflow",
            probe["overflowX"] <= 1,
            f"overflowX={probe['overflowX']}px",
        )
    )
    return results


def _collect_metrics(page: Page, selectors: dict[str, str]) -> dict[str, dict[str, Any]]:
    """Measure rendered box geometry and computed tokens for shared component selectors."""
    return page.evaluate(
        """(selMap) => {
            const out = {};
            for (const [key, sel] of Object.entries(selMap)) {
                const candidates = [...document.querySelectorAll(sel)];
                const el = candidates.find((c) => {
                    const cs = getComputedStyle(c);
                    if (cs.display === 'none' || cs.visibility === 'hidden') return false;
                    const r = c.getBoundingClientRect();
                    return r.width > 0 && r.height > 0;
                }) || candidates[0];
                if (!el) continue;
                const rect = el.getBoundingClientRect();
                const cs = getComputedStyle(el);
                out[key] = {
                    width: Math.round(rect.width),
                    height: Math.round(rect.height),
                    borderRadius: cs.borderRadius,
                    borderTopLeftRadius: cs.borderTopLeftRadius,
                    borderTopRightRadius: cs.borderTopRightRadius,
                    borderTopWidth: cs.borderTopWidth,
                    backgroundColor: cs.backgroundColor,
                    color: cs.color,
                };
            }
            return out;
        }""",
        selectors,
    )


def _measure_dialog_and_capture(
    page: Page,
    open_selector: str,
    dialog_selector: str,
    close_selector: str,
    screenshot_path: Path,
) -> tuple[dict[str, Any], bool, str]:
    """Open a native dialog via UI click, inspect geometry/capture, then dismiss it."""
    trigger = page.locator(open_selector)
    dlg = page.locator(dialog_selector)
    trigger.scroll_into_view_if_needed()
    trigger.click()
    page.wait_for_timeout(350)

    info = page.evaluate(
        """(sel) => {
            const el = document.querySelector(sel);
            if (!el) return { found: false, open: false };
            const rect = el.getBoundingClientRect();
            const cs = getComputedStyle(el);
            return {
                found: true,
                open: Boolean(el.open),
                width: Math.round(rect.width),
                height: Math.round(rect.height),
                borderRadius: cs.borderRadius,
                backgroundColor: cs.backgroundColor,
                color: cs.color,
            };
        }""",
        dialog_selector,
    )
    page.screenshot(path=str(screenshot_path), animations="disabled")

    close_btn = page.locator(close_selector)
    if close_btn.count() > 0:
        close_btn.click()
    else:
        page.keyboard.press("Escape")
    try:
        page.wait_for_function(
            "(sel) => !document.querySelector(sel)?.open",
            arg=dialog_selector,
            timeout=2500,
        )
        closed = True
    except Exception:  # noqa: BLE001
        closed = not bool(dlg.evaluate("el => el.open"))

    ok = bool(info.get("open")) and info.get("width", 0) >= 280 and closed
    detail = (
        f"open={info.get('open')}, w={info.get('width')}, "
        f"radius={info.get('borderRadius')}, closedAfter={closed}"
    )
    return info, ok, detail


def _verify_minimal_interactions(page: Page) -> list[CheckResult]:
    """Verify switch toggle and text-field clear interactions in minimal.html."""
    results: list[CheckResult] = []
    sw = page.locator("#min-switch-sync")
    before = bool(sw.is_checked())
    sw.click()
    after = bool(sw.is_checked())
    aria_after = sw.get_attribute("aria-checked")
    sw.click()
    results.append(
        CheckResult(
            "minimal:switch-interaction",
            after != before and aria_after == str(after).lower(),
            f"before={before}, after={after}, aria-checked={aria_after}",
        )
    )

    inp = page.locator("#min-outlined-input")
    clr = page.locator("#min-outlined-clear")
    cnt = page.locator("#min-field-counter")
    orig = inp.input_value()
    clr.click()
    cleared_val = inp.input_value()
    cleared_cnt = cnt.inner_text()
    inp.fill(orig)
    restored_cnt = cnt.inner_text()
    results.append(
        CheckResult(
            "minimal:text-field-clear",
            cleared_val == "" and cleared_cnt.startswith("0 /") and inp.input_value() == orig,
            f"cleared='{cleared_val}', counterAfterClear='{cleared_cnt}', restored='{restored_cnt}'",
        )
    )
    return results


def _compare_component_parity(
    min_metrics: dict[str, dict[str, Any]], idx_metrics: dict[str, dict[str, Any]]
) -> list[CheckResult]:
    """Verify minimal.html component geometries & colors match index.html."""
    results: list[CheckResult] = []
    for key, fields in PARITY_FIELDS.items():
        m = min_metrics.get(key)
        idx = idx_metrics.get(key)
        if not m or not idx:
            results.append(
                CheckResult(
                    f"parity:{key}",
                    False,
                    f"missing selector metric minimal={bool(m)}, index={bool(idx)}",
                )
            )
            continue
        diffs = [
            f"{f}: minimal={m.get(f)} vs index={idx.get(f)}"
            for f in fields
            if m.get(f) != idx.get(f)
        ]
        results.append(
            CheckResult(
                f"parity:{key}",
                not diffs,
                "exact match" if not diffs else "; ".join(diffs),
            )
        )
    return results


def _capture_sections(page: Page, section_ids: tuple[str, ...], out_dir: Path, prefix: str) -> None:
    """Capture section screenshots deterministically."""
    for sec_id in section_ids:
        loc = page.locator(f"#{sec_id}")
        if loc.count() > 0:
            loc.scroll_into_view_if_needed()
            page.wait_for_timeout(40)
            loc.screenshot(path=str(out_dir / f"{prefix}_{sec_id}.png"), animations="disabled")


def _compare_against_baseline(
    out_dir: Path, baseline_dir: Path, max_diff_pct: float
) -> list[CheckResult]:
    """Compare captured index screenshots against a reference baseline directory."""
    results: list[CheckResult] = []
    baseline_pngs = sorted(baseline_dir.glob("*.png"))
    if not baseline_pngs:
        return [
            CheckResult(
                "baseline:discover",
                False,
                f"No .png files found in baseline dir: {baseline_dir}",
            )
        ]

    for base_path in baseline_pngs:
        cur_path = out_dir / base_path.name
        if not cur_path.exists():
            results.append(
                CheckResult(f"baseline:{base_path.name}", False, "missing captured PNG")
            )
            continue
        a = np.asarray(Image.open(base_path).convert("RGBA"), dtype=np.int16)
        b = np.asarray(Image.open(cur_path).convert("RGBA"), dtype=np.int16)
        if a.shape != b.shape:
            results.append(
                CheckResult(
                    f"baseline:{base_path.name}",
                    False,
                    f"shape mismatch baseline={a.shape} vs current={b.shape}",
                )
            )
            continue
        diff = np.abs(a - b)
        changed_vis = int(np.any(diff > 4, axis=-1).sum())
        total = int(a.shape[0] * a.shape[1])
        pct = 100.0 * changed_vis / total
        results.append(
            CheckResult(
                f"baseline:{base_path.name}",
                pct <= max_diff_pct,
                f"changed_vis={changed_vis}/{total} ({pct:.4f}%), max_ch_diff={int(diff.max())}",
            )
        )
    return results


def run_verification(
    repo_root: Path,
    out_dir: Path,
    baseline_dir: Path | None = None,
    max_diff_pct: float = 0.75,
) -> tuple[bool, list[CheckResult]]:
    """Run full offline visual & parity verification and return (passed, checks)."""
    out_dir.mkdir(parents=True, exist_ok=True)
    httpd, port = _start_server(repo_root)
    results: list[CheckResult] = []
    base_url = f"http://127.0.0.1:{port}"

    try:
        with sync_playwright() as p:
            browser = _launch_browser(p)

            # 1. Verify minimal.html (light desktop + interactions + dialog)
            min_url = f"{base_url}/assets/starter/minimal.html"
            ctx, page, tel = _open_offline_page(
                browser, min_url, {"width": 1440, "height": 900}, theme="light"
            )
            results.extend(_audit_runtime_and_fonts(page, tel, "minimal-light"))
            min_metrics = _collect_metrics(page, SHARED_SELECTORS)
            results.extend(_verify_minimal_interactions(page))
            dlg_info, dlg_ok, dlg_detail = _measure_dialog_and_capture(
                page,
                "#min-dialog-open",
                "#minimal-dialog",
                "#min-dialog-cancel",
                out_dir / "minimal_light_dialog_open.png",
            )
            min_metrics["dialog"] = dlg_info
            results.append(CheckResult("minimal:dialog-modal", dlg_ok, dlg_detail))
            page.evaluate("window.scrollTo(0, 0)")
            page.wait_for_timeout(80)
            page.screenshot(
                path=str(out_dir / "minimal_light_full.png"),
                full_page=True,
                animations="disabled",
            )
            _capture_sections(page, MINIMAL_SECTION_IDS, out_dir, "minimal_light")
            ctx.close()

            # Minimal dark & mobile checks
            ctx_dark, page_dark, tel_dark = _open_offline_page(
                browser, min_url, {"width": 1440, "height": 900}, theme="dark"
            )
            results.extend(_audit_runtime_and_fonts(page_dark, tel_dark, "minimal-dark"))
            page_dark.screenshot(
                path=str(out_dir / "minimal_dark_full.png"),
                full_page=True,
                animations="disabled",
            )
            ctx_dark.close()

            ctx_mob, page_mob, _ = _open_offline_page(
                browser, min_url, {"width": 390, "height": 844}, theme="light"
            )
            mob_overflow = page_mob.evaluate(
                "() => document.documentElement.scrollWidth - window.innerWidth"
            )
            results.append(
                CheckResult(
                    "minimal:mobile-overflow",
                    mob_overflow <= 1,
                    f"overflowX={mob_overflow}px",
                )
            )
            page_mob.screenshot(
                path=str(out_dir / "minimal_mobile_top.png"), animations="disabled"
            )
            ctx_mob.close()

            # 2. Verify index.html (light & dark desktop + mobile + component parity)
            idx_url = f"{base_url}/assets/starter/index.html"
            idx_metrics: dict[str, dict[str, Any]] = {}
            for theme in ("light", "dark"):
                ictx, ipage, itel = _open_offline_page(
                    browser, idx_url, {"width": 1440, "height": 900}, theme=theme
                )
                results.extend(_audit_runtime_and_fonts(ipage, itel, f"index-{theme}"))
                ipage.evaluate("window.scrollTo(0, 0)")
                ipage.wait_for_timeout(80)
                ipage.screenshot(
                    path=str(out_dir / f"index_{theme}_full.png"),
                    full_page=True,
                    animations="disabled",
                )
                _capture_sections(ipage, INDEX_SECTION_IDS, out_dir, f"index_{theme}")
                if theme == "light":
                    idx_metrics = _collect_metrics(ipage, SHARED_SELECTORS)
                    idx_dlg_info, idx_dlg_ok, idx_dlg_detail = _measure_dialog_and_capture(
                        ipage,
                        "#prim-dialog-open",
                        "#prim-dialog",
                        "#prim-dialog-cancel",
                        out_dir / "index_light_dialog_open.png",
                    )
                    idx_metrics["dialog"] = idx_dlg_info
                    results.append(
                        CheckResult("index:dialog-modal", idx_dlg_ok, idx_dlg_detail)
                    )
                ictx.close()

            imob_ctx, imob_page, _ = _open_offline_page(
                browser, idx_url, {"width": 390, "height": 844}, theme="light"
            )
            idx_mob_overflow = imob_page.evaluate(
                "() => document.documentElement.scrollWidth - window.innerWidth"
            )
            results.append(
                CheckResult(
                    "index:mobile-overflow",
                    idx_mob_overflow <= 1,
                    f"overflowX={idx_mob_overflow}px",
                )
            )
            imob_page.screenshot(
                path=str(out_dir / "index_mobile_top.png"), animations="disabled"
            )
            imob_ctx.close()
            browser.close()
    finally:
        httpd.server_close()

    results.extend(_compare_component_parity(min_metrics, idx_metrics))
    if baseline_dir is not None:
        results.extend(_compare_against_baseline(out_dir, baseline_dir, max_diff_pct))

    return all(r.passed for r in results), results


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Verify MD3E offline rendering, self-hosted fonts, CJK fallback, and visual parity."
    )
    parser.add_argument(
        "--repo-root",
        type=Path,
        default=ROOT_DIR,
        help="Path to md3e-frontend repository root",
    )
    parser.add_argument(
        "--out-dir",
        type=Path,
        default=None,
        help="Optional directory to persist captured PNG screenshots",
    )
    parser.add_argument(
        "--baseline-dir",
        type=Path,
        default=None,
        help="Optional baseline PNG directory to diff against index.html screenshots",
    )
    parser.add_argument(
        "--threshold",
        type=float,
        default=0.75,
        help="Max allowed visible pixel change percent when comparing --baseline-dir (default: 0.75)",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Print structured JSON summary instead of text lines",
    )
    args = parser.parse_args(argv)

    if args.out_dir is not None:
        passed, results = run_verification(
            args.repo_root.resolve(),
            args.out_dir.resolve(),
            args.baseline_dir.resolve() if args.baseline_dir else None,
            args.threshold,
        )
    else:
        with tempfile.TemporaryDirectory(prefix="md3e-visual-") as tmp_dir:
            passed, results = run_verification(
                args.repo_root.resolve(),
                Path(tmp_dir),
                args.baseline_dir.resolve() if args.baseline_dir else None,
                args.threshold,
            )

    if args.json:
        print(
            json.dumps(
                {
                    "passed": passed,
                    "checks": [
                        {"name": r.name, "passed": r.passed, "detail": r.detail}
                        for r in results
                    ],
                },
                indent=2,
                ensure_ascii=False,
            )
        )
    else:
        for r in results:
            tag = "PASS" if r.passed else "FAIL"
            print(f"[{tag}] {r.name}: {r.detail}")
        total = len(results)
        ok_count = sum(1 for r in results if r.passed)
        print(f"Visual verification: {'PASS' if passed else 'FAIL'} ({ok_count}/{total} checks passed)")
    return 0 if passed else 1


if __name__ == "__main__":
    sys.exit(main())
