/**
 * md3e-spring.js — Velocity-preserving damped harmonic oscillator for M3 Expressive.
 *
 * CSS `linear()` springs handle declarative hover/toggle transitions cleanly,
 * but they always start from v0 = 0 and restart on interruption. Use this helper
 * for pointer drag releases, mid-flight retargeting, physics continuity, and
 * closed-form CSS `linear()` synthesis so CSS and JS springs settle identically.
 */

export const SPRING_PRESETS = Object.freeze({
  expressive: Object.freeze({
    'fast-spatial': Object.freeze({ damping: 0.6, stiffness: 800 }),
    'default-spatial': Object.freeze({ damping: 0.8, stiffness: 380 }),
    'slow-spatial': Object.freeze({ damping: 0.8, stiffness: 200 }),
    'fast-effects': Object.freeze({ damping: 1.0, stiffness: 3800 }),
    'default-effects': Object.freeze({ damping: 1.0, stiffness: 1600 }),
    'slow-effects': Object.freeze({ damping: 1.0, stiffness: 800 }),
  }),
  standard: Object.freeze({
    'fast-spatial': Object.freeze({ damping: 0.9, stiffness: 1400 }),
    'default-spatial': Object.freeze({ damping: 0.9, stiffness: 700 }),
    'slow-spatial': Object.freeze({ damping: 0.9, stiffness: 300 }),
    'fast-effects': Object.freeze({ damping: 1.0, stiffness: 3800 }),
    'default-effects': Object.freeze({ damping: 1.0, stiffness: 1600 }),
    'slow-effects': Object.freeze({ damping: 1.0, stiffness: 800 }),
  }),
});

const DEFAULT_STIFFNESS = 380;
const DEFAULT_DAMPING = 0.8;
const DEFAULT_PRECISION = 0.005;
const FRAME_1_DT = 1 / 60;
const MIN_DT = 0.0005;
const MAX_DT = 0.05;

function isPositiveFinite(n) {
  return typeof n === 'number' && Number.isFinite(n) && n > 0;
}

function nowMs() {
  return typeof performance !== 'undefined' && typeof performance.now === 'function'
    ? performance.now()
    : Date.now();
}

function isDocumentHidden() {
  return typeof document !== 'undefined' && document.hidden === true;
}

function isReducedMotionPreferred() {
  return typeof window !== 'undefined'
    && Boolean(window.matchMedia?.('(prefers-reduced-motion: reduce)').matches);
}

function scheduleFrame(cb) {
  if (typeof requestAnimationFrame === 'function') {
    return { id: requestAnimationFrame(cb), isTimeout: false };
  }
  return { id: setTimeout(() => cb(nowMs()), 16), isTimeout: true };
}

function cancelFrame(handle) {
  if (!handle) return;
  if (handle.isTimeout) {
    clearTimeout(handle.id);
  } else if (typeof cancelAnimationFrame === 'function') {
    cancelAnimationFrame(handle.id);
  }
}

// Shared visibilitychange registry so springs pause ONLY when document.hidden === true
// and seamlessly rebase timestamps on foreground return without stalling behind modals/blur.
const visibilitySubscribers = new Set();
let boundDocument = null;

function handleDocumentVisibilityChange() {
  const hidden = isDocumentHidden();
  for (const subscriber of Array.from(visibilitySubscribers)) {
    subscriber(hidden);
  }
}

function ensureVisibilitySubscription() {
  if (typeof document === 'undefined' || typeof document.addEventListener !== 'function') {
    return;
  }
  if (boundDocument !== document) {
    if (boundDocument && typeof boundDocument.removeEventListener === 'function') {
      boundDocument.removeEventListener('visibilitychange', handleDocumentVisibilityChange);
    }
    document.addEventListener('visibilitychange', handleDocumentVisibilityChange);
    boundDocument = document;
  }
}

export function resolveSpringPreset(
  speed = 'default',
  type = 'spatial',
  rootEl = typeof document !== 'undefined' ? document.documentElement : null,
) {
  const reduced = isReducedMotionPreferred();
  const scheme = rootEl?.dataset?.motionScheme === 'standard' ? 'standard' : 'expressive';
  const preset = SPRING_PRESETS[scheme][`${speed}-${type}`] || SPRING_PRESETS.expressive['default-spatial'];
  return { ...preset, reduced };
}

function stepAnalyticalSpring(value, velocity, target, damping, stiffness, dt) {
  const safeTarget = Number.isFinite(target) ? target : 0;
  const safeValue = Number.isFinite(value) ? value : safeTarget;
  const safeVel = Number.isFinite(velocity) ? velocity : 0;

  if (!Number.isFinite(dt) || dt <= 0) {
    return [safeValue, safeVel];
  }
  if (!isPositiveFinite(stiffness)) {
    return [safeTarget, 0];
  }
  const z = isPositiveFinite(damping) ? damping : DEFAULT_DAMPING;

  const x0 = safeValue - safeTarget;
  const w = Math.sqrt(stiffness);
  let x;
  let v;

  if (Math.abs(z - 1) < 1e-6) {
    const e = Math.exp(-w * dt);
    const c1 = x0;
    const c2 = safeVel + w * x0;
    x = (c1 + c2 * dt) * e;
    v = (c2 - w * (c1 + c2 * dt)) * e;
  } else if (z < 1) {
    const wd = w * Math.sqrt(1 - z * z);
    const e = Math.exp(-z * w * dt);
    const b = (safeVel + z * w * x0) / wd;
    const cos = Math.cos(wd * dt);
    const sin = Math.sin(wd * dt);
    x = e * (x0 * cos + b * sin);
    v = e * ((b * wd - z * w * x0) * cos - (x0 * wd + z * w * b) * sin);
  } else {
    const r = w * Math.sqrt(z * z - 1);
    const r1 = -z * w + r;
    const r2 = -z * w - r;
    const c2 = (safeVel - r1 * x0) / (r2 - r1);
    const c1 = x0 - c2;
    const e1 = Math.exp(r1 * dt);
    const e2 = Math.exp(r2 * dt);
    x = c1 * e1 + c2 * e2;
    v = c1 * r1 * e1 + c2 * r2 * e2;
  }

  return [safeTarget + x, v];
}

/**
 * Synthesize a CSS `linear()` easing curve and settling duration from spring parameters
 * using the exact closed-form analytical harmonic oscillator.
 *
 * @param {number} stiffness
 * @param {number} damping
 * @param {number} [samples=36]
 * @returns {{ durationMs: number, linearEasing: string, cssShorthand: string, peakOvershoot: number }}
 */
export function synthesizeSpringLinearCss(
  stiffness = DEFAULT_STIFFNESS,
  damping = DEFAULT_DAMPING,
  samples = 36,
) {
  const safeK = isPositiveFinite(stiffness) ? stiffness : DEFAULT_STIFFNESS;
  const safeZ = isPositiveFinite(damping) ? damping : DEFAULT_DAMPING;
  const safeSamples = Number.isInteger(samples) && samples >= 8 ? Math.min(240, samples) : 36;

  const scanStep = 0.0005;
  const maxScanSec = 4.0;
  let lastOut = 0;
  let peak = 1;

  for (let t = 0; t <= maxScanSec + 1e-9; t += scanStep) {
    const [pos, vel] = stepAnalyticalSpring(0, 0, 1, safeZ, safeK, t);
    if (safeZ < 1 && t <= 3.0 && pos > peak) {
      peak = pos;
    }
    if (Math.abs(pos - 1) >= 0.001 || Math.abs(vel) >= 0.02) {
      lastOut = t;
    }
  }

  const durationMs = Math.max(80, Math.ceil((lastOut * 1000 + 20) / 10) * 10);
  const durationSec = durationMs / 1000;
  const points = [];

  for (let i = 0; i <= safeSamples; i++) {
    if (i === 0) {
      points.push(0);
      continue;
    }
    if (i === safeSamples) {
      points.push(1);
      continue;
    }
    const t = durationSec * (i / safeSamples);
    const [pos] = stepAnalyticalSpring(0, 0, 1, safeZ, safeK, t);
    const rounded = Math.round(pos * 10000) / 10000;
    points.push(Object.is(rounded, -0) ? 0 : rounded);
  }

  const linearEasing = `linear(${points.join(', ')})`;
  const cssShorthand = `${durationMs}ms ${linearEasing}`;
  const overshootPct = safeZ >= 1 ? 0 : Number(((peak - 1) * 100).toFixed(2));

  return {
    durationMs,
    linearEasing,
    cssShorthand,
    peakOvershoot: Object.is(overshootPct, -0) ? 0 : overshootPct,
  };
}

export function createSpringAnimator({
  initialValue = 0,
  stiffness = DEFAULT_STIFFNESS,
  damping = DEFAULT_DAMPING,
  precision = DEFAULT_PRECISION,
  onUpdate,
  onComplete,
  onRest,
} = {}) {
  let value = Number.isFinite(initialValue) ? initialValue : 0;
  let velocity = 0;
  let target = value;
  let k = isPositiveFinite(stiffness) ? stiffness : DEFAULT_STIFFNESS;
  let z = isPositiveFinite(damping) ? damping : DEFAULT_DAMPING;
  let eps = isPositiveFinite(precision) ? precision : DEFAULT_PRECISION;
  const defaultOnRest = typeof onRest === 'function' ? onRest : undefined;

  let frameHandle = null;
  let running = false;
  let lastTs = null;
  let lastDt = FRAME_1_DT;
  let pausedByVisibility = false;
  let needsRebase = false;
  let targetEpoch = 0;
  let activeOnRest;

  function onVisibilityChange(hidden) {
    if (hidden) {
      if (frameHandle) {
        cancelFrame(frameHandle);
        frameHandle = null;
        pausedByVisibility = true;
        needsRebase = true;
      }
      return;
    }
    if (pausedByVisibility) {
      pausedByVisibility = false;
      needsRebase = true;
      if (running && !frameHandle) {
        frameHandle = scheduleFrame(tick);
      }
    }
  }

  function stop() {
    targetEpoch += 1;
    activeOnRest = undefined;
    running = false;
    if (frameHandle) {
      cancelFrame(frameHandle);
      frameHandle = null;
    }
    pausedByVisibility = false;
    needsRebase = false;
    lastTs = null;
    visibilitySubscribers.delete(onVisibilityChange);
  }

  function tick(ts) {
    frameHandle = null;
    if (!running) return;
    if (isDocumentHidden()) {
      pausedByVisibility = true;
      needsRebase = true;
      return;
    }

    const currentTs = typeof ts === 'number' && Number.isFinite(ts) ? ts : nowMs();
    let dt;
    if (needsRebase) {
      needsRebase = false;
      dt = lastDt;
      lastTs = currentTs;
    } else if (lastTs === null) {
      dt = FRAME_1_DT;
      lastTs = currentTs;
    } else {
      const rawDeltaSec = (currentTs - lastTs) / 1000;
      dt = Math.min(MAX_DT, Math.max(MIN_DT, rawDeltaSec));
      lastTs = currentTs;
    }
    lastDt = dt;

    [value, velocity] = stepAnalyticalSpring(value, velocity, target, z, k, dt);

    if (Math.abs(value - target) < eps && Math.abs(velocity) < eps) {
      value = target;
      velocity = 0;
      running = false;
      frameHandle = null;
      pausedByVisibility = false;
      needsRebase = false;
      lastTs = null;
      visibilitySubscribers.delete(onVisibilityChange);
      const settledEpoch = targetEpoch;
      const restCb = activeOnRest === undefined ? defaultOnRest : activeOnRest;
      activeOnRest = undefined;
      onUpdate?.(value, 0);
      if (targetEpoch === settledEpoch) {
        onComplete?.();
        restCb?.(value);
      }
      return;
    }

    onUpdate?.(value, velocity);
    if (running && !pausedByVisibility && !frameHandle) {
      frameHandle = scheduleFrame(tick);
    }
  }

  return {
    get value() { return value; },
    get velocity() { return velocity; },
    get target() { return target; },
    get paused() { return pausedByVisibility; },
    getValue() { return value; },
    getVelocity() { return velocity; },
    getTarget() { return target; },
    isAnimating() { return running || frameHandle !== null || pausedByVisibility; },
    configure({ stiffness: nextK, damping: nextZ, precision: nextEps } = {}) {
      if (isPositiveFinite(nextK)) k = nextK;
      if (isPositiveFinite(nextZ)) z = nextZ;
      if (isPositiveFinite(nextEps)) eps = nextEps;
    },
    setTarget(nextTarget, velocityOrOpts, maybeOpts) {
      if (typeof nextTarget !== 'number' || !Number.isFinite(nextTarget)) return;
      let velocityOverride;
      let opts = {};
      if (velocityOrOpts !== null && typeof velocityOrOpts === 'object') {
        opts = velocityOrOpts;
        velocityOverride = opts.velocity;
      } else {
        velocityOverride = velocityOrOpts;
        if (maybeOpts !== null && typeof maybeOpts === 'object') {
          opts = maybeOpts;
        }
      }

      if (isPositiveFinite(opts.stiffness)) k = opts.stiffness;
      if (isPositiveFinite(opts.damping)) z = opts.damping;
      if (isPositiveFinite(opts.precision)) eps = opts.precision;

      target = nextTarget;
      if (typeof velocityOverride === 'number' && Number.isFinite(velocityOverride)) {
        velocity = velocityOverride;
      }

      const hasPerTargetOnRest = Object.prototype.hasOwnProperty.call(opts, 'onRest');
      const nextOnRest = hasPerTargetOnRest
        ? (typeof opts.onRest === 'function' ? opts.onRest : null)
        : undefined;

      if (opts.immediate || isReducedMotionPreferred()) {
        stop();
        const settledEpoch = ++targetEpoch;
        const restCb = nextOnRest === undefined ? defaultOnRest : nextOnRest;
        value = target;
        velocity = 0;
        onUpdate?.(value, 0);
        if (targetEpoch === settledEpoch) {
          onComplete?.();
          restCb?.(value);
        }
        return;
      }

      targetEpoch += 1;
      activeOnRest = nextOnRest;
      running = true;

      ensureVisibilitySubscription();
      visibilitySubscribers.add(onVisibilityChange);
      if (isDocumentHidden()) {
        if (frameHandle) {
          cancelFrame(frameHandle);
          frameHandle = null;
        }
        pausedByVisibility = true;
        needsRebase = lastTs !== null;
        return;
      }
      if (!frameHandle) {
        pausedByVisibility = false;
        if (needsRebase) {
          // Keep needsRebase if resuming; otherwise start fresh with Frame-1 1/60 baseline.
        } else {
          lastTs = null;
          lastDt = FRAME_1_DT;
        }
        frameHandle = scheduleFrame(tick);
      }
    },
    snap(nextValue) {
      if (typeof nextValue !== 'number' || !Number.isFinite(nextValue)) return;
      stop();
      value = nextValue;
      target = nextValue;
      velocity = 0;
      onUpdate?.(value, 0);
    },
    jump(nextValue) {
      const resolved = nextValue === undefined ? target : nextValue;
      if (typeof resolved !== 'number' || !Number.isFinite(resolved)) return;
      stop();
      value = resolved;
      target = resolved;
      velocity = 0;
      onUpdate?.(value, 0);
    },
    stop,
  };
}
