/**
 * md3e-studio.js — Hidden Layer 4 Personal Studio Engine & Human-AI Co-Tuning Protocol
 *
 * Strictly dormant opt-in runtime for `:root[data-studio-profile="personal-studio"]`.
 * Integrates with `md3e-spring.js` (`createSpringAnimator`, `synthesizeSpringLinearCss`)
 * so horizontal drag scrubbers, live CSS tokens, telemetry JSON, pointer spotlights,
 * scroll-edge fades, status capsules, and spring counters stay synchronized.
 */

import { createSpringAnimator, synthesizeSpringLinearCss } from './md3e-spring.js';

export const STUDIO_PARAM_SCHEMA = Object.freeze({
  blurPx: Object.freeze({
    key: 'blurPx',
    group: 'glass',
    label: 'Backdrop Blur',
    min: 8,
    max: 48,
    step: 1,
    decimals: 0,
    default: 28,
    cssVar: '--md-studio-blur-px',
    unit: 'px',
  }),
  glassAlpha: Object.freeze({
    key: 'glassAlpha',
    group: 'glass',
    label: 'Glass Opacity',
    min: 32,
    max: 88,
    step: 1,
    decimals: 0,
    default: 56,
    cssVar: '--md-studio-glass-alpha',
    unit: '%',
  }),
  glassSaturate: Object.freeze({
    key: 'glassSaturate',
    group: 'glass',
    label: 'Optical Saturate',
    min: 100,
    max: 240,
    step: 1,
    decimals: 0,
    default: 190,
    cssVar: '--md-studio-glass-saturate',
    unit: '%',
  }),
  specularAlpha: Object.freeze({
    key: 'specularAlpha',
    group: 'glass',
    label: 'Specular Rim',
    min: 0,
    max: 36,
    step: 1,
    decimals: 0,
    default: 18,
    cssVar: '--md-studio-specular-alpha',
    unit: '%',
  }),
  hdrBoost: Object.freeze({
    key: 'hdrBoost',
    group: 'glass',
    label: 'HDR Headroom',
    min: 0,
    max: 100,
    step: 1,
    decimals: 0,
    default: 35,
    cssVar: '--md-studio-hdr-boost',
    unit: '%',
  }),
  springStiffness: Object.freeze({
    key: 'springStiffness',
    group: 'physics',
    label: 'Spring Stiffness',
    min: 180,
    max: 900,
    step: 1,
    decimals: 0,
    default: 340,
    cssVar: '--md-studio-spring-stiffness',
    unit: '',
  }),
  springDamping: Object.freeze({
    key: 'springDamping',
    group: 'physics',
    label: 'Damping Ratio',
    min: 0.58,
    max: 1.0,
    step: 0.01,
    decimals: 2,
    default: 0.76,
    cssVar: '--md-studio-spring-damping',
    unit: '',
  }),
  staggerMs: Object.freeze({
    key: 'staggerMs',
    group: 'physics',
    label: 'Stagger Step',
    min: 12,
    max: 60,
    step: 1,
    decimals: 0,
    default: 32,
    cssVar: '--md-studio-stagger-ms',
    unit: 'ms',
  }),
  spotlightPx: Object.freeze({
    key: 'spotlightPx',
    group: 'desktop',
    label: 'Spotlight Radius',
    min: 120,
    max: 420,
    step: 1,
    decimals: 0,
    default: 260,
    cssVar: '--md-studio-spotlight-px',
    unit: 'px',
  }),
  spotlightAlpha: Object.freeze({
    key: 'spotlightAlpha',
    group: 'desktop',
    label: 'Spotlight Glow',
    min: 0,
    max: 24,
    step: 1,
    decimals: 0,
    default: 12,
    cssVar: '--md-studio-spotlight-alpha',
    unit: '%',
  }),
  splitRatio: Object.freeze({
    key: 'splitRatio',
    group: 'desktop',
    label: 'Bento Split Ratio',
    min: 32,
    max: 68,
    step: 1,
    decimals: 0,
    default: 58,
    cssVar: '--md-studio-split-ratio',
    unit: '%',
  }),
});

const PARAM_KEYS = Object.freeze(Object.keys(STUDIO_PARAM_SCHEMA));
const STORAGE_KEY = 'md3e-personal-studio-v1';

function clamp(lo, hi, v) {
  return v < lo ? lo : v > hi ? hi : v;
}

function quantizeParam(key, raw) {
  const spec = STUDIO_PARAM_SCHEMA[key];
  if (!spec) return raw;
  const num = Number(raw);
  if (!Number.isFinite(num)) return spec.default;
  const clamped = clamp(spec.min, spec.max, num);
  const steps = Math.round((clamped - spec.min) / spec.step);
  const snapped = clamp(spec.min, spec.max, spec.min + steps * spec.step);
  return Number(snapped.toFixed(spec.decimals));
}

function formatParamValue(key, val) {
  const spec = STUDIO_PARAM_SCHEMA[key];
  if (!spec) return String(val);
  const num = quantizeParam(key, val);
  const text = spec.decimals > 0 ? num.toFixed(spec.decimals) : String(num);
  return `${text}${spec.unit}`;
}

function defaultValues() {
  const out = {};
  for (const key of PARAM_KEYS) {
    out[key] = STUDIO_PARAM_SCHEMA[key].default;
  }
  return out;
}

function defaultSources() {
  const out = {};
  for (const key of PARAM_KEYS) {
    out[key] = 'default';
  }
  return out;
}

function normalizeState(input = {}) {
  const values = defaultValues();
  const sources = defaultSources();
  const srcObj = input && typeof input === 'object' ? input : {};
  const hasExplicitValues = srcObj.values && typeof srcObj.values === 'object';
  const hasExplicitSources = srcObj.sources && typeof srcObj.sources === 'object';

  for (const key of PARAM_KEYS) {
    const spec = STUDIO_PARAM_SCHEMA[key];
    let rawVal = spec.default;
    let rawSrc = 'default';

    if (hasExplicitValues && Object.prototype.hasOwnProperty.call(srcObj.values, key)) {
      rawVal = srcObj.values[key];
      if (hasExplicitSources && typeof srcObj.sources[key] === 'string') {
        rawSrc = srcObj.sources[key];
      } else if (quantizeParam(key, rawVal) !== spec.default) {
        rawSrc = 'human';
      }
    } else if (srcObj[key] && typeof srcObj[key] === 'object' && 'value' in srcObj[key]) {
      rawVal = srcObj[key].value;
      rawSrc = typeof srcObj[key].source === 'string'
        ? srcObj[key].source
        : (quantizeParam(key, rawVal) !== spec.default ? 'human' : 'default');
    } else if (typeof srcObj[key] === 'number') {
      rawVal = srcObj[key];
      if (hasExplicitSources && typeof srcObj.sources[key] === 'string') {
        rawSrc = srcObj.sources[key];
      } else if (quantizeParam(key, rawVal) !== spec.default) {
        rawSrc = 'human';
      }
    }

    values[key] = quantizeParam(key, rawVal);
    sources[key] = rawSrc === 'human' || rawSrc === 'ai' ? rawSrc : 'default';
  }

  return { values, sources };
}

function computeHumanDeltas(values, sources) {
  const deltas = {};
  for (const key of PARAM_KEYS) {
    if (sources[key] === 'human') {
      const diff = Number((values[key] - STUDIO_PARAM_SCHEMA[key].default).toFixed(STUDIO_PARAM_SCHEMA[key].decimals));
      deltas[key] = Object.is(diff, -0) ? 0 : diff;
    }
  }
  return deltas;
}

function computeOpticalLayerVars(values) {
  const dAlpha = values.glassAlpha - STUDIO_PARAM_SCHEMA.glassAlpha.default;
  const dBlur = values.blurPx - STUDIO_PARAM_SCHEMA.blurPx.default;
  const dSat = values.glassSaturate - STUDIO_PARAM_SCHEMA.glassSaturate.default;

  const brightness = clamp(1.02, 1.22, Number((1.10 - dAlpha * 0.0025 + dBlur * 0.002).toFixed(3)));
  const contrast = clamp(1.0, 1.12, Number((1.05 + Math.abs(dAlpha) * 0.0008 + dSat * 0.0003).toFixed(3)));
  return { brightness, contrast };
}

/**
 * Classify human-driven scrubber adjustments into an expressive design intent label.
 *
 * @param {object} state
 * @returns {'frosted-crystal'|'silk-cinematic'|'crisp-utility'|'tactile-focus'|'balanced-studio'}
 */
export function inferHumanIntent(state) {
  const { values, sources } = normalizeState(state);
  const humanKeys = PARAM_KEYS.filter((k) => sources[k] === 'human');
  if (humanKeys.length === 0) {
    return 'balanced-studio';
  }

  const nd = (key) => {
    if (sources[key] !== 'human') return 0;
    const spec = STUDIO_PARAM_SCHEMA[key];
    return (values[key] - spec.default) / (spec.max - spec.min);
  };

  const scores = {
    'frosted-crystal':
      Math.max(0, -nd('glassAlpha')) * 1.4
      + Math.max(0, nd('blurPx')) * 1.2
      + Math.max(0, nd('glassSaturate')) * 0.85
      + Math.max(0, nd('specularAlpha')) * 0.9
      + Math.max(0, nd('hdrBoost')) * 0.45,
    'silk-cinematic':
      Math.max(0, -nd('springStiffness')) * 1.45
      + Math.max(0, -nd('springDamping')) * 1.15
      + Math.max(0, nd('staggerMs')) * 1.0,
    'crisp-utility':
      Math.max(0, nd('springStiffness')) * 1.35
      + Math.max(0, nd('glassAlpha')) * 1.25
      + Math.max(0, nd('springDamping')) * 0.95
      + Math.max(0, -nd('staggerMs')) * 0.85
      + Math.max(0, -nd('blurPx')) * 0.65,
    'tactile-focus':
      Math.max(0, nd('spotlightAlpha')) * 1.3
      + Math.max(0, nd('spotlightPx')) * 1.0
      + Math.abs(nd('splitRatio')) * 1.15,
  };

  let bestIntent = 'balanced-studio';
  let bestScore = 0.08;
  for (const [label, score] of Object.entries(scores)) {
    if (score > bestScore) {
      bestScore = score;
      bestIntent = label;
    }
  }
  return bestIntent;
}

/**
 * Compute coupled complementary parameter recommendations across untouched (`source !== 'human'`)
 * controls while keeping every human-pinned parameter strictly unchanged.
 *
 * @param {object} state
 * @returns {{
 *   values: Record<string, number>,
 *   sources: Record<string, 'default'|'human'|'ai'>,
 *   humanModifiedKeys: string[],
 *   aiHarmonizedKeys: string[],
 *   intent: string,
 *   rationale: string[],
 * }}
 */
export function computeHarmonizedParams(state) {
  const { values: inputValues, sources: inputSources } = normalizeState(state);
  const humanModifiedKeys = PARAM_KEYS.filter((k) => inputSources[k] === 'human');
  const intent = inferHumanIntent({ values: inputValues, sources: inputSources });

  if (humanModifiedKeys.length === 0) {
    return {
      values: defaultValues(),
      sources: defaultSources(),
      humanModifiedKeys: [],
      aiHarmonizedKeys: [],
      intent,
      rationale: ['All 11 studio tokens are at calibrated Personal Studio defaults.'],
    };
  }

  const nextValues = defaultValues();
  const nextSources = defaultSources();
  for (const k of humanModifiedKeys) {
    nextValues[k] = inputValues[k];
    nextSources[k] = 'human';
  }

  // Only derive coupling deltas from human-pinned anchors so repeated runs are idempotent.
  const hd = (key) => (
    inputSources[key] === 'human'
      ? inputValues[key] - STUDIO_PARAM_SCHEMA[key].default
      : 0
  );

  const dBlur = hd('blurPx');
  const dAlpha = hd('glassAlpha');
  const dSat = hd('glassSaturate');
  const dSpec = hd('specularAlpha');
  const dHdr = hd('hdrBoost');
  const dStiffness = hd('springStiffness');
  const dDamping = hd('springDamping');
  const dStagger = hd('staggerMs');
  const dSpotPx = hd('spotlightPx');
  const dSpotAlpha = hd('spotlightAlpha');
  const dSplit = hd('splitRatio');

  const proposals = {};
  const rationale = [];

  const glassHumanTouched = dBlur !== 0 || dAlpha !== 0 || dSat !== 0 || dSpec !== 0 || dHdr !== 0;
  if (glassHumanTouched) {
    proposals.blurPx = STUDIO_PARAM_SCHEMA.blurPx.default - dAlpha * 0.45 + dSpec * 0.35;
    proposals.glassAlpha = STUDIO_PARAM_SCHEMA.glassAlpha.default - dBlur * 0.45 + dSat * 0.08;
    proposals.glassSaturate = STUDIO_PARAM_SCHEMA.glassSaturate.default - dAlpha * 1.15 + dBlur * 0.9 + dHdr * 0.25;
    proposals.specularAlpha = STUDIO_PARAM_SCHEMA.specularAlpha.default - dAlpha * 0.35 + dBlur * 0.22 + dSat * 0.06 + dHdr * 0.08;
    proposals.hdrBoost = STUDIO_PARAM_SCHEMA.hdrBoost.default - dAlpha * 0.55 + dSpec * 0.65 + dBlur * 0.25;
    proposals.spotlightAlpha = STUDIO_PARAM_SCHEMA.spotlightAlpha.default - dAlpha * 0.16 + dBlur * 0.10 + dHdr * 0.05;
    proposals.spotlightPx = STUDIO_PARAM_SCHEMA.spotlightPx.default + dBlur * 1.6 - dAlpha * 0.8;
    rationale.push('Coupled optical saturation, HDR specular headroom, rim, and spotlight glow to balance glass translucency.');
  }

  const physicsHumanTouched = dStiffness !== 0 || dDamping !== 0 || dStagger !== 0;
  if (physicsHumanTouched) {
    const kSignal = dStiffness !== 0
      ? dStiffness
      : (-dStagger * 9 + dDamping * 420);
    proposals.springStiffness = STUDIO_PARAM_SCHEMA.springStiffness.default + kSignal;
    proposals.springDamping = STUDIO_PARAM_SCHEMA.springDamping.default + (kSignal / 720) * 0.18;
    proposals.staggerMs = STUDIO_PARAM_SCHEMA.staggerMs.default - (kSignal / 720) * 24 + dDamping * 14;
    rationale.push('Aligned damping ratio and choreography stagger step with spring settling cadence.');
  }

  const desktopHumanTouched = dSpotPx !== 0 || dSpotAlpha !== 0 || dSplit !== 0;
  if (desktopHumanTouched) {
    const baseSpotPx = proposals.spotlightPx ?? STUDIO_PARAM_SCHEMA.spotlightPx.default;
    const baseSpotAlpha = proposals.spotlightAlpha ?? STUDIO_PARAM_SCHEMA.spotlightAlpha.default;
    proposals.spotlightPx = baseSpotPx + dSpotAlpha * 6 - Math.abs(dSplit) * 1.5;
    proposals.spotlightAlpha = baseSpotAlpha + dSpotPx * 0.03;
    if (dSpec === 0 && inputSources.specularAlpha !== 'human') {
      proposals.specularAlpha = (proposals.specularAlpha ?? STUDIO_PARAM_SCHEMA.specularAlpha.default) + dSpotAlpha * 0.25;
    }
    if (dHdr === 0 && inputSources.hdrBoost !== 'human') {
      proposals.hdrBoost = (proposals.hdrBoost ?? STUDIO_PARAM_SCHEMA.hdrBoost.default) + dSpotAlpha * 1.1;
    }
    rationale.push('Balanced pointer spotlight envelope with panel proportions, HDR boost, and specular highlight.');
  }

  const aiHarmonizedKeys = [];
  for (const [key, rawTarget] of Object.entries(proposals)) {
    if (inputSources[key] === 'human') {
      continue;
    }
    const quantized = quantizeParam(key, rawTarget);
    if (quantized !== STUDIO_PARAM_SCHEMA[key].default) {
      nextValues[key] = quantized;
      nextSources[key] = 'ai';
      aiHarmonizedKeys.push(key);
    }
  }

  return {
    values: nextValues,
    sources: nextSources,
    humanModifiedKeys,
    aiHarmonizedKeys,
    intent,
    rationale,
  };
}

/**
 * Detect hardware & CSS HDR / wide-gamut Display-P3 capabilities safely.
 * Guards all browser globals so Node unit tests can invoke this directly.
 *
 * @returns {{
 *   dynamicRangeHigh: boolean,
 *   colorGamutP3: boolean,
 *   cssDisplayP3: boolean,
 *   cssDynamicRangeLimit: boolean,
 *   effectiveHdr: boolean,
 * }}
 */
export function detectHdrCapabilities() {
  const win = typeof window !== 'undefined' ? window : null;
  const mm = typeof win?.matchMedia === 'function'
    ? win.matchMedia.bind(win)
    : (typeof matchMedia === 'function' ? matchMedia : null);
  const cssObj = typeof CSS !== 'undefined' ? CSS : win?.CSS;

  const safeMatchMedia = (query) => {
    if (!mm) return false;
    try {
      return Boolean(mm(query)?.matches);
    } catch {
      return false;
    }
  };

  const safeCssSupports = (prop, val) => {
    if (!cssObj || typeof cssObj.supports !== 'function') return false;
    try {
      return Boolean(cssObj.supports(prop, val));
    } catch {
      return false;
    }
  };

  const dynamicRangeHigh = safeMatchMedia('(dynamic-range: high)');
  const colorGamutP3 = safeMatchMedia('(color-gamut: p3)');
  const cssDisplayP3 = safeCssSupports('color', 'color(display-p3 1 1 1)');
  const cssDynamicRangeLimit = safeCssSupports('dynamic-range-limit', 'constrained-high');
  const effectiveHdr = Boolean(dynamicRangeHigh && (cssDisplayP3 || cssDynamicRangeLimit));

  return {
    dynamicRangeHigh,
    colorGamutP3,
    cssDisplayP3,
    cssDynamicRangeLimit,
    effectiveHdr,
  };
}

function getHdrCapableTier(caps) {
  if (caps.effectiveHdr) return 'hdr';
  if (caps.colorGamutP3 && caps.cssDisplayP3) return 'p3';
  return 'sdr';
}

function getHdrA11yBlockReason(rootEl) {
  if (rootEl?.dataset?.reducedTransparency === 'true') return 'reduced-transparency';
  if (rootEl?.dataset?.contrast === 'high') return 'high-contrast';
  const win = typeof window !== 'undefined' ? window : null;
  const mm = typeof win?.matchMedia === 'function'
    ? win.matchMedia.bind(win)
    : (typeof matchMedia === 'function' ? matchMedia : null);
  if (mm) {
    try {
      if (mm('(prefers-reduced-transparency: reduce)')?.matches) return 'reduced-transparency';
      if (mm('(prefers-contrast: more)')?.matches) return 'high-contrast';
      if (mm('(forced-colors: active)')?.matches) return 'forced-colors';
    } catch {
      // Ignore matchMedia evaluation errors in headless mocks.
    }
  }
  return null;
}

/**
 * Format live Layer 4 CSS variables + synthesized M3E `linear()` spatial motion token
 * as a copyable stylesheet patch.
 *
 * @param {object} valuesOrState
 * @param {{ hdrEnabled?: boolean }} [opts]
 * @returns {string}
 */
export function formatStudioCssPatch(valuesOrState, { hdrEnabled } = {}) {
  const { values } = normalizeState(valuesOrState);
  const { brightness, contrast } = computeOpticalLayerVars(values);
  const spring = synthesizeSpringLinearCss(values.springStiffness, values.springDamping, 36);
  const resolvedHdrEnabled = typeof hdrEnabled === 'boolean'
    ? hdrEnabled
    : (typeof valuesOrState?.hdr?.enabled === 'boolean' ? valuesOrState.hdr.enabled : true);

  const lines = [
    ':root[data-studio-profile="personal-studio"] {',
  ];
  for (const key of PARAM_KEYS) {
    lines.push(`  ${STUDIO_PARAM_SCHEMA[key].cssVar}: ${formatParamValue(key, values[key])};`);
  }
  lines.push(`  --md-studio-glass-brightness: ${brightness};`);
  lines.push(`  --md-studio-glass-contrast: ${contrast};`);
  lines.push(`  --md-bento-motion-default-spatial-duration: ${spring.durationMs}ms;`);
  lines.push(`  --md-bento-motion-default-spatial-easing: ${spring.linearEasing};`);
  lines.push(`  --md-bento-motion-default-spatial: ${spring.cssShorthand};`);
  lines.push('}');
  lines.push(`:root[data-studio-profile="personal-studio"][data-studio-hdr="${resolvedHdrEnabled ? 'on' : 'off'}"] {`);
  lines.push(`  --md-studio-hdr-boost: ${resolvedHdrEnabled ? formatParamValue('hdrBoost', values.hdrBoost) : '0%'};`);
  lines.push('}');
  return lines.join('\n');
}

/**
 * Debounced non-occluding titlebar status capsule controller.
 * Keeps `aria-live="polite"` announcements calm during continuous pointer scrubs.
 */
export function createStatusCapsule(pillEl, { debounceMs = 140, holdMs = 2600, defaultText = 'Personal Studio' } = {}) {
  let debounceTimer = null;
  let idleTimer = null;
  let destroyed = false;

  function applyNow(text, tone = 'active') {
    if (destroyed || !pillEl) return;
    pillEl.textContent = text;
    pillEl.dataset.tone = tone;
    clearTimeout(idleTimer);
    if (tone === 'active' && holdMs > 0) {
      idleTimer = setTimeout(() => {
        if (!destroyed && pillEl) {
          pillEl.dataset.tone = 'idle';
        }
      }, holdMs);
    }
  }

  return {
    notify(text, { tone = 'active', immediate = false } = {}) {
      if (destroyed || !pillEl) return;
      clearTimeout(debounceTimer);
      if (immediate || debounceMs <= 0) {
        applyNow(text, tone);
        return;
      }
      debounceTimer = setTimeout(() => applyNow(text, tone), debounceMs);
    },
    clear() {
      clearTimeout(debounceTimer);
      clearTimeout(idleTimer);
      if (destroyed) return;
      if (pillEl) {
        pillEl.textContent = defaultText;
        pillEl.dataset.tone = 'idle';
      }
    },
    destroy() {
      destroyed = true;
      clearTimeout(debounceTimer);
      clearTimeout(idleTimer);
      debounceTimer = null;
      idleTimer = null;
    },
  };
}

const counterAnimators = new WeakMap();
const activeStudioByRoot = new WeakMap();
let activeDetachedStudio = null;

/**
 * Animate numeric readouts smoothly using `md3e-spring.js` with `.tabular-nums` alignment
 * and exact final target snap on settle.
 */
export function animateTabularCounter(
  el,
  targetValue,
  {
    decimals = 0,
    prefix = '',
    suffix = '',
    stiffness = 380,
    damping = 0.82,
    immediate = false,
  } = {},
) {
  if (!el || !Number.isFinite(Number(targetValue))) return null;
  const target = Number(targetValue);
  el.classList?.add('tabular-nums');

  const fmt = (val) => {
    const fixed = decimals > 0 ? val.toFixed(decimals) : String(Math.round(val));
    return `${prefix}${fixed}${suffix}`;
  };

  let entry = counterAnimators.get(el);
  if (!entry) {
    const parsedInitial = Number.parseFloat(el.dataset?.studioCounterValue ?? el.textContent ?? '0');
    const initial = Number.isFinite(parsedInitial) ? parsedInitial : target;
    const precision = decimals > 0 ? Math.min(0.05, 10 ** -(decimals + 1)) : 0.25;
    entry = { animator: null, target, fmt };
    entry.animator = createSpringAnimator({
      initialValue: initial,
      stiffness,
      damping,
      precision,
      onUpdate(val, vel) {
        const displayVal = vel === 0 ? entry.target : val;
        if (el.dataset) el.dataset.studioCounterValue = String(displayVal);
        el.textContent = entry.fmt(displayVal);
      },
    });
    counterAnimators.set(el, entry);
  } else {
    const precision = decimals > 0 ? Math.min(0.05, 10 ** -(decimals + 1)) : 0.25;
    entry.target = target;
    entry.fmt = fmt;
    entry.animator.configure({ stiffness, damping, precision });
  }

  entry.target = target;
  entry.fmt = fmt;
  entry.animator.setTarget(target, undefined, { immediate });
  return entry.animator;
}

/**
 * Initialize Hidden Layer 4 Personal Studio bindings and expose
 * `window.__MD3E_TUNER__` (and identical alias `window.__MD3E_STUDIO__`).
 */
export function initPersonalStudio({
  rootEl = typeof document !== 'undefined' ? (document.documentElement ?? null) : null,
  telemetryEl = typeof document !== 'undefined' ? (document.getElementById?.('md3e-studio-telemetry') ?? null) : null,
  cssOutputEl = typeof document !== 'undefined' ? (document.getElementById?.('studio-css-output') ?? null) : null,
  intentBadgeEl = typeof document !== 'undefined' ? (document.getElementById?.('studio-intent-badge') ?? null) : null,
  statusPillEl = typeof document !== 'undefined' ? (document.getElementById?.('titlebar-status-pill') ?? null) : null,
  harmonizeBtnEl = typeof document !== 'undefined' ? (document.getElementById?.('btn-studio-harmonize') ?? null) : null,
  resetBtnEl = typeof document !== 'undefined' ? (document.getElementById?.('btn-studio-reset') ?? null) : null,
  hdrBadgeEl = typeof document !== 'undefined' ? (document.getElementById?.('studio-hdr-badge') ?? null) : null,
  hdrToggleBtnEl = typeof document !== 'undefined' ? (document.getElementById?.('btn-studio-hdr') ?? null) : null,
  scrubberSelector = '.studio-scrubber[data-scrubber-key]',
  spotlightSelector = '[data-studio-spotlight]',
  scrollFadeSelector = '.studio-scroll-fade, [data-studio-scroll-fade]',
  persistStorage = true,
  onChange = null,
} = {}) {
  const prevInstance = rootEl && typeof rootEl === 'object'
    ? activeStudioByRoot.get(rootEl)
    : activeDetachedStudio;
  if (prevInstance) {
    prevInstance.destroy();
  }

  let values = defaultValues();
  let sources = defaultSources();
  let hdrRequested = true;
  let lastRationale = ['All 11 studio tokens are at calibrated Personal Studio defaults.'];
  let destroyed = false;
  let wasPersonalProfile = !rootEl || rootEl.dataset?.studioProfile === 'personal-studio';
  const cleanups = [];
  const statusCapsule = createStatusCapsule(statusPillEl);

  function getSynthesizedSpring() {
    return synthesizeSpringLinearCss(values.springStiffness, values.springDamping, 36);
  }

  function resolveHdrState() {
    const caps = detectHdrCapabilities();
    const capable = getHdrCapableTier(caps);
    const blockReason = getHdrA11yBlockReason(rootEl);
    const isPersonal = !rootEl || rootEl.dataset?.studioProfile === 'personal-studio';
    const enabled = Boolean(isPersonal && hdrRequested && !blockReason);
    const effective = Boolean(enabled && caps.effectiveHdr);
    return {
      caps,
      capable,
      blockReason,
      enabled,
      effective,
      telemetryHdr: {
        ...caps,
        capable,
        enabled,
        effective,
        boostPct: values.hdrBoost,
      },
    };
  }

  function buildTelemetrySnapshot(hdrState = resolveHdrState()) {
    const humanModifiedKeys = PARAM_KEYS.filter((k) => sources[k] === 'human');
    const aiHarmonizedKeys = PARAM_KEYS.filter((k) => sources[k] === 'ai');
    const humanDeltas = computeHumanDeltas(values, sources);
    const inferredIntent = inferHumanIntent({ values, sources });
    const spring = getSynthesizedSpring();

    return {
      profile: rootEl?.dataset?.studioProfile || 'dormant',
      values: { ...values },
      sources: { ...sources },
      humanModifiedKeys,
      humanDeltas,
      aiHarmonizedKeys,
      inferredIntent,
      hdr: hdrState.telemetryHdr,
      rationale: [...lastRationale],
      synthesizedSpring: {
        stiffness: values.springStiffness,
        damping: values.springDamping,
        durationMs: spring.durationMs,
        peakOvershoot: spring.peakOvershoot,
        cssShorthand: spring.cssShorthand,
      },
      updatedAt: new Date().toISOString(),
    };
  }

  function syncCssVariables(spring, hdrState = resolveHdrState()) {
    if (rootEl?.dataset) {
      rootEl.dataset.studioHdr = hdrState.enabled ? 'on' : 'off';
      rootEl.dataset.studioHdrCapable = hdrState.capable;
    }
    if (!rootEl?.style) return;
    const isPersonal = rootEl.dataset?.studioProfile === 'personal-studio';
    if (!isPersonal) {
      const hadSplitRatio = Boolean(rootEl.style.getPropertyValue?.('--md-studio-split-ratio'));
      for (const key of PARAM_KEYS) {
        rootEl.style.removeProperty(STUDIO_PARAM_SCHEMA[key].cssVar);
      }
      rootEl.style.removeProperty('--md-studio-glass-brightness');
      rootEl.style.removeProperty('--md-studio-glass-contrast');
      rootEl.style.removeProperty('--md-bento-motion-default-spatial-duration');
      rootEl.style.removeProperty('--md-bento-motion-default-spatial-easing');
      rootEl.style.removeProperty('--md-bento-motion-default-spatial');
      if ((hadSplitRatio || wasPersonalProfile)
        && typeof CustomEvent === 'function'
        && typeof rootEl.dispatchEvent === 'function') {
        rootEl.dispatchEvent(new CustomEvent('md3e:studio-split-reset', {
          bubbles: true,
          detail: {
            splitRatio: STUDIO_PARAM_SCHEMA.splitRatio.default,
            profile: rootEl.dataset?.studioProfile || 'dormant',
          },
        }));
      }
      wasPersonalProfile = false;
      return;
    }

    wasPersonalProfile = true;
    for (const key of PARAM_KEYS) {
      const val = key === 'hdrBoost' && !hdrState.enabled
        ? '0%'
        : formatParamValue(key, values[key]);
      rootEl.style.setProperty(STUDIO_PARAM_SCHEMA[key].cssVar, val);
    }
    const { brightness, contrast } = computeOpticalLayerVars(values);
    rootEl.style.setProperty('--md-studio-glass-brightness', String(brightness));
    rootEl.style.setProperty('--md-studio-glass-contrast', String(contrast));

    rootEl.style.setProperty('--md-bento-motion-default-spatial-duration', `${spring.durationMs}ms`);
    rootEl.style.setProperty('--md-bento-motion-default-spatial-easing', spring.linearEasing);
    rootEl.style.setProperty('--md-bento-motion-default-spatial', spring.cssShorthand);
  }

  function syncHdrDom(hdrState = resolveHdrState()) {
    const badgeEl = hdrBadgeEl || (typeof document !== 'undefined' ? (document.getElementById?.('studio-hdr-badge') ?? null) : null);
    const toggleBtnEl = hdrToggleBtnEl || (typeof document !== 'undefined' ? (document.getElementById?.('btn-studio-hdr') ?? null) : null);

    if (badgeEl) {
      let badgeText = 'SDR Fallback';
      if (hdrState.blockReason === 'reduced-transparency') {
        badgeText = 'RT Fallback';
      } else if (hdrState.blockReason) {
        badgeText = 'HC Fallback';
      } else if (!hdrState.enabled) {
        badgeText = 'HDR Off';
      } else if (hdrState.effective) {
        badgeText = 'HDR Ready';
      } else if (hdrState.capable === 'p3') {
        badgeText = 'Display-P3';
      }
      badgeEl.textContent = badgeText;
      if (badgeEl.dataset) {
        badgeEl.dataset.hdrCapable = hdrState.capable;
        badgeEl.dataset.hdrActive = String(hdrState.enabled);
      }
    }

    if (toggleBtnEl) {
      toggleBtnEl.setAttribute('aria-checked', String(hdrState.enabled));
    }
  }

  function syncScrubbersDom() {
    if (typeof document === 'undefined') return;
    const scrubbers = document.querySelectorAll?.(scrubberSelector) || [];
    for (const el of scrubbers) {
      const key = el.dataset?.scrubberKey;
      const spec = STUDIO_PARAM_SCHEMA[key];
      if (!spec) continue;
      const val = values[key];
      const pct = ((val - spec.min) / (spec.max - spec.min)) * 100;
      const formatted = formatParamValue(key, val);
      el.setAttribute('aria-valuemin', String(spec.min));
      el.setAttribute('aria-valuemax', String(spec.max));
      el.setAttribute('aria-valuenow', String(val));
      el.setAttribute('aria-valuetext', formatted);
      el.dataset.scrubberSource = sources[key];
      el.style?.setProperty('--studio-scrubber-pct', `${pct.toFixed(2)}%`);
      const valNode = el.querySelector('.studio-scrubber__val');
      if (valNode) {
        valNode.textContent = formatted;
      }
    }
  }

  function syncSplitHandlesDom(isPersonal) {
    if (typeof document === 'undefined') return;
    const handles = document.querySelectorAll?.('.studio-split-handle') || [];
    const activeRatio = isPersonal ? values.splitRatio : STUDIO_PARAM_SCHEMA.splitRatio.default;
    const formatted = formatParamValue('splitRatio', activeRatio);
    for (const handle of handles) {
      handle.setAttribute?.('aria-valuenow', String(activeRatio));
      handle.setAttribute?.('aria-valuetext', formatted);
    }
  }

  function persistState() {
    if (!persistStorage || typeof localStorage === 'undefined') return;
    try {
      const hasCustom = PARAM_KEYS.some((k) => sources[k] !== 'default') || !hdrRequested;
      if (!hasCustom) {
        localStorage.removeItem(STORAGE_KEY);
      } else {
        localStorage.setItem(STORAGE_KEY, JSON.stringify({ values, sources, hdrEnabled: hdrRequested }));
      }
    } catch {
      // Ignore storage quota or private-browsing errors cleanly.
    }
  }

  function syncAll({ persist = true } = {}) {
    const hdrState = resolveHdrState();
    const snapshot = buildTelemetrySnapshot(hdrState);
    const spring = synthesizeSpringLinearCss(values.springStiffness, values.springDamping, 36);
    const isPersonal = !rootEl || rootEl.dataset?.studioProfile === 'personal-studio';
    syncCssVariables(spring, hdrState);
    syncHdrDom(hdrState);
    syncScrubbersDom();
    syncSplitHandlesDom(isPersonal);

    if (telemetryEl) {
      telemetryEl.textContent = JSON.stringify(snapshot, null, 2);
    }
    if (cssOutputEl) {
      cssOutputEl.textContent = formatStudioCssPatch(snapshot, { hdrEnabled: hdrState.enabled });
    }
    if (intentBadgeEl) {
      intentBadgeEl.textContent = snapshot.inferredIntent;
      if (intentBadgeEl.dataset) {
        intentBadgeEl.dataset.intent = snapshot.inferredIntent;
      }
    }
    if (persist) {
      persistState();
    }
    onChange?.(snapshot);
    syncSplitHandlesDom(isPersonal);
    return snapshot;
  }

  function setHdrEnabled(enabled, { announce = true } = {}) {
    hdrRequested = Boolean(enabled);
    const snap = syncAll();
    const isPersonal = !rootEl || rootEl.dataset?.studioProfile === 'personal-studio';
    if (announce && statusPillEl && isPersonal) {
      const label = snap.hdr.enabled
        ? `HDR Optics: ON (${snap.hdr.boostPct}%)`
        : (getHdrA11yBlockReason(rootEl) ? 'HDR Optics: Fallback active' : 'HDR Optics: OFF (SDR)');
      statusCapsule.notify(label, { immediate: true });
    }
    return snap;
  }

  function setParam(key, rawValue, { source = 'human', announce = true } = {}) {
    if (!Object.prototype.hasOwnProperty.call(STUDIO_PARAM_SCHEMA, key)) {
      return buildTelemetrySnapshot();
    }
    const nextVal = quantizeParam(key, rawValue);
    values[key] = nextVal;
    sources[key] = source === 'human' || source === 'ai' ? source : 'default';
    if (source === 'human') {
      lastRationale = [`User tuned ${STUDIO_PARAM_SCHEMA[key].label} to ${formatParamValue(key, nextVal)}.`];
    }
    const snap = syncAll();
    if (announce && statusPillEl) {
      statusCapsule.notify(
        `${STUDIO_PARAM_SCHEMA[key].label}: ${formatParamValue(key, nextVal)} · ${snap.inferredIntent}`,
      );
    }
    return snap;
  }

  function harmonize({ announce = true } = {}) {
    const result = computeHarmonizedParams({ values, sources });
    values = { ...result.values };
    sources = { ...result.sources };
    lastRationale = [...result.rationale];
    const snap = syncAll();
    if (announce && statusPillEl) {
      statusCapsule.notify(
        `Harmonized ${result.aiHarmonizedKeys.length} · ${snap.synthesizedSpring.durationMs}ms spring`,
        { immediate: true },
      );
    }
    return snap;
  }

  function reset({ announce = true } = {}) {
    values = defaultValues();
    sources = defaultSources();
    hdrRequested = true;
    lastRationale = ['All 11 studio tokens restored to Personal Studio defaults.'];
    const snap = syncAll();
    if (announce && statusPillEl) {
      statusCapsule.notify('Studio reset to 500ms expressive baseline', { immediate: true });
    }
    return snap;
  }

  function exportCss() {
    const hdrState = resolveHdrState();
    return formatStudioCssPatch(values, { hdrEnabled: hdrState.enabled });
  }

  function applyUrlOrStorage() {
    if (persistStorage && typeof localStorage !== 'undefined') {
      try {
        const raw = localStorage.getItem(STORAGE_KEY);
        if (raw) {
          const parsed = JSON.parse(raw);
          const norm = normalizeState(parsed);
          values = norm.values;
          sources = norm.sources;
          hdrRequested = typeof parsed?.hdrEnabled === 'boolean' ? parsed.hdrEnabled : true;
        } else {
          values = defaultValues();
          sources = defaultSources();
          hdrRequested = true;
        }
      } catch {
        // Ignore malformed storage JSON cleanly.
      }
    }

    if (typeof window !== 'undefined') {
      try {
        const searchParams = new URLSearchParams(window.location?.search || '');
        const hashRaw = (window.location?.hash || '').replace(/^#/, '');
        const hashParams = hashRaw.includes('=') ? new URLSearchParams(hashRaw) : null;
        const encoded = searchParams.get('studio') || hashParams?.get('studio');
        if (encoded) {
          const parsed = JSON.parse(decodeURIComponent(encoded));
          if (parsed && typeof parsed === 'object') {
            const hasExplicitValues = parsed.values && typeof parsed.values === 'object';
            const hasExplicitSources = parsed.sources && typeof parsed.sources === 'object';
            for (const key of PARAM_KEYS) {
              const spec = STUDIO_PARAM_SCHEMA[key];
              let hasKey = false;
              let rawVal;
              let rawSrc;
              if (hasExplicitValues && Object.prototype.hasOwnProperty.call(parsed.values, key)) {
                hasKey = true;
                rawVal = parsed.values[key];
                rawSrc = hasExplicitSources && typeof parsed.sources[key] === 'string'
                  ? parsed.sources[key]
                  : (quantizeParam(key, rawVal) !== spec.default ? 'human' : 'default');
              } else if (parsed[key] && typeof parsed[key] === 'object' && 'value' in parsed[key]) {
                hasKey = true;
                rawVal = parsed[key].value;
                rawSrc = typeof parsed[key].source === 'string'
                  ? parsed[key].source
                  : (quantizeParam(key, rawVal) !== spec.default ? 'human' : 'default');
              } else if (typeof parsed[key] === 'number') {
                hasKey = true;
                rawVal = parsed[key];
                rawSrc = hasExplicitSources && typeof parsed.sources[key] === 'string'
                  ? parsed.sources[key]
                  : (quantizeParam(key, rawVal) !== spec.default ? 'human' : 'default');
              }
              if (hasKey) {
                values[key] = quantizeParam(key, rawVal);
                sources[key] = rawSrc === 'human' || rawSrc === 'ai' ? rawSrc : 'default';
              }
            }
            if (typeof parsed.hdrEnabled === 'boolean') {
              hdrRequested = parsed.hdrEnabled;
            }
          }
        } else {
          for (const key of PARAM_KEYS) {
            const p = searchParams.get(key) ?? hashParams?.get(key);
            if (p !== null && p !== '') {
              const parsedNum = Number(p);
              if (Number.isFinite(parsedNum)) {
                values[key] = quantizeParam(key, parsedNum);
                sources[key] = values[key] !== STUDIO_PARAM_SCHEMA[key].default ? 'human' : 'default';
              }
            }
          }
          const hdrParam = searchParams.get('studioHdr') ?? searchParams.get('hdr') ?? hashParams?.get('studioHdr');
          if (hdrParam === 'off' || hdrParam === 'false' || hdrParam === '0') {
            hdrRequested = false;
          } else if (hdrParam === 'on' || hdrParam === 'true' || hdrParam === '1') {
            hdrRequested = true;
          }
        }
      } catch {
        // Ignore malformed URL parameters cleanly.
      }
    }

    return syncAll();
  }

  function bindScrubbers() {
    if (typeof document === 'undefined') return;
    const scrubbers = document.querySelectorAll?.(scrubberSelector) || [];
    for (const el of scrubbers) {
      if (el.dataset.studioScrubberBound === 'true') continue;
      el.dataset.studioScrubberBound = 'true';
      const key = el.dataset?.scrubberKey;
      const spec = STUDIO_PARAM_SCHEMA[key];
      if (!spec) continue;

      let dragState = null;

      const onPointerDown = (e) => {
        if (e.button !== undefined && e.button !== 0) return;
        e.preventDefault();
        el.focus?.();
        try {
          el.setPointerCapture?.(e.pointerId);
        } catch {
          // Ignore synthetic pointer capture in unit tests.
        }
        const rect = el.getBoundingClientRect?.() || { width: 220 };
        dragState = {
          pointerId: e.pointerId,
          startX: e.clientX,
          startVal: values[key],
          width: Math.max(80, rect.width || 220),
        };
        el.dataset.dragging = 'true';
      };

      const onPointerMove = (e) => {
        if (!dragState) return;
        const precision = e.shiftKey ? 0.25 : 1;
        const dx = e.clientX - dragState.startX;
        const span = spec.max - spec.min;
        const rawNext = dragState.startVal + (dx / dragState.width) * span * precision;
        setParam(key, rawNext, { source: 'human' });
      };

      const onPointerUp = () => {
        if (!dragState) return;
        dragState = null;
        delete el.dataset.dragging;
      };

      const onKeyDown = (e) => {
        let nextVal = null;
        const baseStep = spec.key === 'springStiffness' || spec.key === 'spotlightPx' ? 5 : spec.step;
        const stepAmt = e.shiftKey ? spec.step : baseStep;
        if (e.key === 'ArrowRight' || e.key === 'ArrowUp') {
          nextVal = values[key] + stepAmt;
        } else if (e.key === 'ArrowLeft' || e.key === 'ArrowDown') {
          nextVal = values[key] - stepAmt;
        } else if (e.key === 'PageUp') {
          nextVal = values[key] + baseStep * 5;
        } else if (e.key === 'PageDown') {
          nextVal = values[key] - baseStep * 5;
        } else if (e.key === 'Home') {
          nextVal = spec.min;
        } else if (e.key === 'End') {
          nextVal = spec.max;
        }
        if (nextVal !== null) {
          e.preventDefault();
          setParam(key, nextVal, { source: 'human' });
        }
      };

      const onWheel = (e) => {
        if (document.activeElement !== el && !e.shiftKey) return;
        e.preventDefault();
        const dir = e.deltaY < 0 || e.deltaX > 0 ? 1 : -1;
        const mult = e.shiftKey ? 1 : 2;
        setParam(key, values[key] + dir * spec.step * mult, { source: 'human' });
      };

      el.addEventListener('pointerdown', onPointerDown);
      el.addEventListener('pointermove', onPointerMove);
      el.addEventListener('pointerup', onPointerUp);
      el.addEventListener('pointercancel', onPointerUp);
      el.addEventListener('keydown', onKeyDown);
      el.addEventListener('wheel', onWheel, { passive: false });

      cleanups.push(() => {
        el.removeEventListener('pointerdown', onPointerDown);
        el.removeEventListener('pointermove', onPointerMove);
        el.removeEventListener('pointerup', onPointerUp);
        el.removeEventListener('pointercancel', onPointerUp);
        el.removeEventListener('keydown', onKeyDown);
        el.removeEventListener('wheel', onWheel);
        delete el.dataset.studioScrubberBound;
      });
    }
  }

  function bindSpotlights() {
    if (typeof document === 'undefined') return;
    let rafId = null;
    let pendingTarget = null;
    let pendingX = 0;
    let pendingY = 0;

    const flushSpotlight = () => {
      rafId = null;
      if (!pendingTarget || document.hidden === true) return;
      const rect = pendingTarget.getBoundingClientRect?.();
      if (!rect) return;
      const x = Math.round(pendingX - rect.left);
      const y = Math.round(pendingY - rect.top);
      pendingTarget.style?.setProperty('--studio-mx', `${x}px`);
      pendingTarget.style?.setProperty('--studio-my', `${y}px`);
      pendingTarget.dataset.spotlightActive = 'true';
    };

    const onPointerMove = (e) => {
      if (rootEl?.dataset?.studioProfile !== 'personal-studio') return;
      const card = e.target?.closest?.(spotlightSelector);
      if (!card) return;
      pendingTarget = card;
      pendingX = e.clientX;
      pendingY = e.clientY;
      if (!rafId && typeof requestAnimationFrame === 'function') {
        rafId = requestAnimationFrame(flushSpotlight);
      }
    };

    const onPointerOut = (e) => {
      const card = e.target?.closest?.(spotlightSelector);
      if (!card) return;
      if (!e.relatedTarget || !card.contains?.(e.relatedTarget)) {
        if (pendingTarget === card) {
          pendingTarget = null;
          if (rafId && typeof cancelAnimationFrame === 'function') {
            cancelAnimationFrame(rafId);
            rafId = null;
          }
        }
        delete card.dataset.spotlightActive;
      }
    };

    document.addEventListener?.('pointermove', onPointerMove, { passive: true });
    document.addEventListener?.('pointerout', onPointerOut, { passive: true });
    cleanups.push(() => {
      if (rafId && typeof cancelAnimationFrame === 'function') {
        cancelAnimationFrame(rafId);
      }
      document.removeEventListener?.('pointermove', onPointerMove);
      document.removeEventListener?.('pointerout', onPointerOut);
    });
  }

  const updateScrollEdge = (el) => {
    const topHidden = el.scrollTop > 4;
    const bottomHidden = el.scrollTop + el.clientHeight < el.scrollHeight - 4;
    el.dataset.scrollEdges = topHidden && bottomHidden
      ? 'both'
      : topHidden
        ? 'top'
        : bottomHidden
          ? 'bottom'
          : 'none';
  };

  const scrollFadeObserver = typeof ResizeObserver === 'function'
    ? new ResizeObserver((entries) => {
      for (const entry of entries) {
        updateScrollEdge(entry.target);
      }
    })
    : null;
  if (scrollFadeObserver) {
    cleanups.push(() => scrollFadeObserver.disconnect());
  }

  function bindScrollFades() {
    if (typeof document === 'undefined') return;
    const els = document.querySelectorAll?.(scrollFadeSelector) || [];

    for (const el of els) {
      if (el.dataset.studioScrollBound === 'true') {
        updateScrollEdge(el);
        continue;
      }
      el.dataset.studioScrollBound = 'true';
      const onScroll = () => updateScrollEdge(el);
      el.addEventListener('scroll', onScroll, { passive: true });
      scrollFadeObserver?.observe(el);
      updateScrollEdge(el);
      cleanups.push(() => {
        el.removeEventListener('scroll', onScroll);
        scrollFadeObserver?.unobserve(el);
        delete el.dataset.studioScrollBound;
      });
    }
  }

  function bindButtons() {
    if (harmonizeBtnEl && harmonizeBtnEl.dataset.studioBound !== 'true') {
      harmonizeBtnEl.dataset.studioBound = 'true';
      const onHarmonize = () => harmonize();
      harmonizeBtnEl.addEventListener('click', onHarmonize);
      cleanups.push(() => {
        harmonizeBtnEl.removeEventListener('click', onHarmonize);
        delete harmonizeBtnEl.dataset.studioBound;
      });
    }
    if (resetBtnEl && resetBtnEl.dataset.studioBound !== 'true') {
      resetBtnEl.dataset.studioBound = 'true';
      const onReset = () => reset();
      resetBtnEl.addEventListener('click', onReset);
      cleanups.push(() => {
        resetBtnEl.removeEventListener('click', onReset);
        delete resetBtnEl.dataset.studioBound;
      });
    }
    const toggleBtn = hdrToggleBtnEl || (typeof document !== 'undefined' ? (document.getElementById?.('btn-studio-hdr') ?? null) : null);
    if (toggleBtn && toggleBtn.dataset?.studioBound !== 'true' && toggleBtn.dataset?.studioHdrBound !== 'true') {
      if (toggleBtn.dataset) {
        toggleBtn.dataset.studioBound = 'true';
        toggleBtn.dataset.studioHdrBound = 'true';
      }
      const onToggleHdr = () => {
        const blockReason = getHdrA11yBlockReason(rootEl);
        if (blockReason) {
          if (statusPillEl) {
            statusCapsule.notify(`HDR disabled (${blockReason})`, { immediate: true });
          }
          syncAll();
          return;
        }
        setHdrEnabled(!hdrRequested);
      };
      toggleBtn.addEventListener('click', onToggleHdr);
      cleanups.push(() => {
        toggleBtn.removeEventListener('click', onToggleHdr);
        if (toggleBtn.dataset) {
          delete toggleBtn.dataset.studioBound;
          delete toggleBtn.dataset.studioHdrBound;
        }
      });
    }
  }

  function bindMediaWatchers() {
    const win = typeof window !== 'undefined' ? window : null;
    const mm = typeof win?.matchMedia === 'function' ? win.matchMedia.bind(win) : null;
    if (!mm) return;
    const queries = [
      '(dynamic-range: high)',
      '(color-gamut: p3)',
      '(prefers-reduced-transparency: reduce)',
      '(prefers-contrast: more)',
      '(forced-colors: active)',
    ];
    for (const q of queries) {
      try {
        const mql = mm(q);
        if (!mql) continue;
        const onMediaChange = () => syncAll();
        if (typeof mql.addEventListener === 'function') {
          mql.addEventListener('change', onMediaChange);
          cleanups.push(() => mql.removeEventListener('change', onMediaChange));
        } else if (typeof mql.addListener === 'function') {
          mql.addListener(onMediaChange);
          cleanups.push(() => mql.removeListener(onMediaChange));
        }
      } catch {
        // Ignore unsupported media queries cleanly.
      }
    }
  }

  function bindStorageWatcher() {
    const win = typeof window !== 'undefined' ? window : null;
    if (!persistStorage || !win || typeof win.addEventListener !== 'function') return;
    const onStorage = (e) => {
      if (e && e.key !== null && e.key !== undefined && e.key !== STORAGE_KEY) return;
      try {
        const raw = e && 'newValue' in e
          ? e.newValue
          : (typeof localStorage !== 'undefined' ? localStorage.getItem(STORAGE_KEY) : null);
        if (raw) {
          const parsed = JSON.parse(raw);
          const norm = normalizeState(parsed);
          values = norm.values;
          sources = norm.sources;
          hdrRequested = typeof parsed?.hdrEnabled === 'boolean' ? parsed.hdrEnabled : true;
        } else {
          values = defaultValues();
          sources = defaultSources();
          hdrRequested = true;
        }
        syncAll({ persist: false });
      } catch {
        // Ignore malformed storage payload cleanly.
      }
    };
    win.addEventListener('storage', onStorage);
    cleanups.push(() => win.removeEventListener?.('storage', onStorage));
  }

  bindScrubbers();
  bindSpotlights();
  bindScrollFades();
  bindButtons();
  bindMediaWatchers();
  bindStorageWatcher();

  if (rootEl && typeof MutationObserver === 'function') {
    const profileObserver = new MutationObserver(() => {
      syncAll();
    });
    profileObserver.observe(rootEl, {
      attributes: true,
      attributeFilter: ['data-studio-profile', 'data-reduced-transparency', 'data-contrast'],
    });
    cleanups.push(() => profileObserver.disconnect());
  }

  applyUrlOrStorage();

  const api = {
    getState: () => buildTelemetrySnapshot(),
    setParam,
    harmonize,
    reset,
    exportCss,
    applyUrlOrStorage,
    getHdrCapabilities: () => detectHdrCapabilities(),
    isHdrEnabled: () => resolveHdrState().enabled,
    setHdrEnabled,
    statusCapsule,
    animateTabularCounter,
    refreshBindings() {
      bindScrubbers();
      bindScrollFades();
      bindButtons();
      return syncAll();
    },
    destroy() {
      if (destroyed) return;
      destroyed = true;
      statusCapsule.destroy();
      while (cleanups.length) {
        cleanups.pop()();
      }
      if (rootEl && typeof rootEl === 'object') {
        if (activeStudioByRoot.get(rootEl) === api) {
          activeStudioByRoot.delete(rootEl);
        }
      } else if (activeDetachedStudio === api) {
        activeDetachedStudio = null;
      }
      if (typeof window !== 'undefined') {
        if (window.__MD3E_STUDIO__ === api) {
          delete window.__MD3E_STUDIO__;
        }
        if (window.__MD3E_TUNER__ === api) {
          delete window.__MD3E_TUNER__;
        }
      }
    },
  };

  if (rootEl && typeof rootEl === 'object') {
    activeStudioByRoot.set(rootEl, api);
  } else {
    activeDetachedStudio = api;
  }

  if (typeof window !== 'undefined') {
    window.__MD3E_TUNER__ = api;
    window.__MD3E_STUDIO__ = window.__MD3E_TUNER__;
  }
  return api;
}
