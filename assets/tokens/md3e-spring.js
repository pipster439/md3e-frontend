/**
 * md3e-spring.js — Velocity-preserving damped harmonic oscillator for M3 Expressive.
 *
 * CSS `linear()` springs handle declarative hover/toggle transitions cleanly,
 * but they always start from v0 = 0 and restart on interruption. Use this helper
 * for pointer drag releases, mid-flight retargeting, and physics continuity.
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
const DEFAULT_PRECISION = 0.05;

function isPositiveFinite(n) {
  return typeof n === 'number' && Number.isFinite(n) && n > 0;
}

function isReducedMotionPreferred() {
  return typeof window !== 'undefined'
    && Boolean(window.matchMedia?.('(prefers-reduced-motion: reduce)').matches);
}

function scheduleFrame(cb) {
  if (typeof requestAnimationFrame === 'function') {
    return { id: requestAnimationFrame(cb), isTimeout: false };
  }
  const now = () => (typeof performance !== 'undefined' && typeof performance.now === 'function'
    ? performance.now()
    : Date.now());
  return { id: setTimeout(() => cb(now()), 16), isTimeout: true };
}

function cancelFrame(handle) {
  if (!handle) return;
  if (handle.isTimeout) {
    clearTimeout(handle.id);
  } else if (typeof cancelAnimationFrame === 'function') {
    cancelAnimationFrame(handle.id);
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

export function createSpringAnimator({
  initialValue = 0,
  stiffness = DEFAULT_STIFFNESS,
  damping = DEFAULT_DAMPING,
  precision = DEFAULT_PRECISION,
  onUpdate,
  onComplete,
} = {}) {
  let value = Number.isFinite(initialValue) ? initialValue : 0;
  let velocity = 0;
  let target = value;
  let k = isPositiveFinite(stiffness) ? stiffness : DEFAULT_STIFFNESS;
  let z = isPositiveFinite(damping) ? damping : DEFAULT_DAMPING;
  const eps = isPositiveFinite(precision) ? precision : DEFAULT_PRECISION;
  let frameHandle = null;
  let lastTs = null;

  function stop() {
    if (frameHandle) {
      cancelFrame(frameHandle);
      frameHandle = null;
      lastTs = null;
    }
  }

  function tick(ts) {
    const dt = lastTs !== null ? Math.min(0.05, Math.max(0.001, (ts - lastTs) / 1000)) : 0.016;
    lastTs = ts;
    [value, velocity] = stepAnalyticalSpring(value, velocity, target, z, k, dt);

    if (Math.abs(value - target) < eps && Math.abs(velocity) < eps) {
      value = target;
      velocity = 0;
      frameHandle = null;
      lastTs = null;
      onUpdate?.(value, 0);
      onComplete?.();
      return;
    }

    onUpdate?.(value, velocity);
    frameHandle = scheduleFrame(tick);
  }

  return {
    get value() { return value; },
    get velocity() { return velocity; },
    get target() { return target; },
    configure({ stiffness: nextK, damping: nextZ } = {}) {
      if (isPositiveFinite(nextK)) k = nextK;
      if (isPositiveFinite(nextZ)) z = nextZ;
    },
    setTarget(nextTarget, velocityOverride, { immediate = false } = {}) {
      if (typeof nextTarget !== 'number' || !Number.isFinite(nextTarget)) return;
      target = nextTarget;
      if (typeof velocityOverride === 'number' && Number.isFinite(velocityOverride)) {
        velocity = velocityOverride;
      }
      if (immediate || isReducedMotionPreferred()) {
        stop();
        value = target;
        velocity = 0;
        onUpdate?.(value, 0);
        onComplete?.();
        return;
      }
      if (!frameHandle) {
        lastTs = null;
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
    stop,
  };
}
