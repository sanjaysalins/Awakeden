// The Second Fire (Folk Print) - motion layer v1. Spec: poc_folk_print_style/motion_v1/MOTION_DESIGN.md (binding).
// 17 clips at 1.0x laid as overlapping Sequences (transition = mask on the incoming clip + a printed edge on top).
// All frames ABSOLUTE comp frames (30 fps). No Math.random, no boil: every mark is deterministic.
// Positions are in STILL coordinates (clip time 0); each shot's doodle layer follows the clip's slow camera (CAM, tracked with SIFT).
// Spec changes + position adjustments: see motion_v1/BUILD_NOTES (report). Audio is muxed later from SECOND_FIRE_SCORED_v2.mp4.
import React from "react";
import { AbsoluteFill, Easing, OffthreadVideo, Sequence, interpolate, interpolateColors, staticFile, useCurrentFrame } from "remotion";

export const SF_FPS = 30;
export const SF_FRAMES = 2637;
export type SFProps = { DENSITY: number };

// ---------- knobs ----------
let DENS = 1;
/** DENSITY < 0.8 drops every 2nd flower / gull / wave row / star spot. */
const keep = (i: number) => DENS >= 0.8 || i % 2 === 0;
const COAL_K = 1.4; // spec 1.0; raised after first QC (coals read as stones at 1.0)

// ---------- palette (starts from the spec; eyedropped from the clip frames) ----------
const C = {
  ink: "#1E2A2E", night: "#0D363D", mid: "#376168", sea: "#388586", star: "#86C2B6",
  orange: "#F7600A", coral: "#EF594D", mustard: "#F2AE3D", flameMid: "#FFCF63", cream: "#F9DCAE", core: "#FEE8A0",
  rust: "#B5522B", coal: "#2A2320", fish: "#7FA3A1", steam: "#C59F84", spike: "#1C3B40", moon: "#FEFEE5",
};
const FLC: [string, string, string] = [C.orange, C.flameMid, C.core];
const FLC_DULL: [string, string, string] = [C.rust, C.mustard, C.cream];

// ---------- math ----------
type Pt = [number, number];
type Box = { x1: number; y1: number; x2: number; y2: number };
const clampO = { extrapolateLeft: "clamp", extrapolateRight: "clamp" } as const;
const lerp = (f: number, a: number, b: number, from: number, to: number, easing?: (t: number) => number) =>
  interpolate(f, [a, b], [from, to], { ...clampO, easing });
const OUT = Easing.out(Easing.cubic);
const INOUT = Easing.inOut(Easing.cubic);
const SINE = Easing.inOut(Easing.sin);
const BACK = Easing.out(Easing.back(1.8));
const pop = (f: number, at: number) => interpolate(f, [at, at + 9], [0, 1], { ...clampO, easing: BACK });
const sway = (f: number, x: number, amp: number) => amp * Math.sin((2 * Math.PI * f) / 80 + x * 0.013);
const rad = (d: number) => (d * Math.PI) / 180;
const mixc = (w: number, c0: string, c1: string) => interpolateColors(Math.min(1, Math.max(0, w)), [0, 1], [c0, c1]);
const FULL: React.CSSProperties = { position: "absolute", left: 0, top: 0, width: 1080, height: 1920, overflow: "visible" };

/** Catmull-Rom position along control points P, u 0..1. */
const posOn = (P: Pt[], u: number): Pt => {
  const n = P.length - 1;
  if (u >= 1) return P[n];
  const t = Math.max(0, u) * n, i = Math.floor(t), k = t - i;
  const p0 = P[Math.max(0, i - 1)], p1 = P[i], p2 = P[i + 1], p3 = P[Math.min(n, i + 2)];
  const c = (a: number, b: number, c2: number, d: number) =>
    0.5 * (2 * b + (-a + c2) * k + (2 * a - 5 * b + 4 * c2 - d) * k * k + (-a + 3 * b - 3 * c2 + d) * k * k * k);
  return [c(p0[0], p1[0], p2[0], p3[0]), c(p0[1], p1[1], p2[1], p3[1])];
};
const sPath = (a: Pt, b: Pt, amp: number, sg = 1): Pt[] => {
  const dx = b[0] - a[0], dy = b[1] - a[1], L = Math.hypot(dx, dy) || 1, nx = -dy / L, ny = dx / L;
  return [a, [a[0] + dx / 3 + nx * amp * sg, a[1] + dy / 3 + ny * amp * sg], [a[0] + (2 * dx) / 3 - nx * amp * sg, a[1] + (2 * dy) / 3 - ny * amp * sg], b];
};
const smoothD = (p: Pt[]) => {
  let d = `M ${p[0][0].toFixed(1)} ${p[0][1].toFixed(1)}`;
  for (let i = 0; i < p.length - 1; i++) {
    const p0 = p[Math.max(0, i - 1)], p1 = p[i], p2 = p[i + 1], p3 = p[Math.min(p.length - 1, i + 2)];
    d += ` C ${(p1[0] + (p2[0] - p0[0]) / 6).toFixed(1)} ${(p1[1] + (p2[1] - p0[1]) / 6).toFixed(1)} ${(p2[0] - (p3[0] - p1[0]) / 6).toFixed(1)} ${(p2[1] - (p3[1] - p1[1]) / 6).toFixed(1)} ${p2[0].toFixed(1)} ${p2[1].toFixed(1)}`;
  }
  return d;
};

// ---------- camera follow (SIFT-tracked per clip; positions are still coordinates) ----------
const CAM: Record<number, number[][]> = {
  0: [[0.0, 1.0, 0.0, 0.0], [0.8, 1.0082, -4.9, -5.5], [1.6, 1.0165, -9.8, -11.2], [2.4, 1.025, -14.8, -17.1], [3.2, 1.0335, -19.9, -23.2], [4.0, 1.0422, -25.0, -29.4]],
  1: [[0.0, 1.0, 0.0, 0.0], [1.2, 0.9999, -5.7, 0.2], [2.4, 0.9999, -12.7, 0.3], [3.6, 0.9998, -20.9, 0.4], [4.8, 0.9997, -30.3, 0.4], [6.0, 0.9996, -41.0, 0.4]],
  2: [[0.0, 1.0, 0.0, 0.0], [1.2, 1.0139, -7.7, -13.3], [2.4, 1.0291, -16.3, -28.0], [3.6, 1.0454, -25.6, -43.9], [4.8, 1.063, -35.7, -61.3], [6.0, 1.0819, -46.7, -80.0]],
  4: [[0.0, 1.0, 0.0, 0.0], [0.8, 0.9991, 0.5, 1.1], [1.6, 1.0006, -0.4, -0.5], [2.4, 1.0045, -2.7, -4.6], [3.2, 1.0108, -6.3, -11.4], [4.0, 1.0196, -11.4, -20.7]],
  6: [[0.0, 1.0, 0.0, 0.0], [1.2, 1.0222, -12.0, -7.3], [2.4, 1.0441, -23.9, -14.8], [3.6, 1.0656, -35.7, -22.3], [4.8, 1.0867, -47.4, -29.9], [6.0, 1.1075, -58.9, -37.7]],
  9: [[0.0, 1.0, 0.0, 0.0], [0.8, 1.0109, -5.8, -11.1], [1.6, 1.0251, -13.8, -25.2], [2.4, 1.0424, -23.9, -42.3], [3.2, 1.0631, -36.2, -62.4], [4.0, 1.0869, -50.7, -85.6]],
  11: [[0.0, 1.0, 0.0, 0.0], [1.2, 1.0156, -8.6, -15.3], [2.4, 1.0309, -17.1, -30.4], [3.6, 1.046, -25.7, -45.3], [4.8, 1.0608, -34.2, -60.1], [6.0, 1.0754, -42.8, -74.7]],
  12: [[0.0, 1.0, 0.0, 0.0], [1.6, 1.0204, -11.7, -19.6], [3.2, 1.0407, -23.3, -39.0], [4.8, 1.0607, -34.8, -58.5], [6.4, 1.0805, -46.3, -77.8], [8.0, 1.1001, -57.6, -97.1]],
  13: [[0.0, 1.0, 0.0, 0.0], [1.6, 1.0211, -12.9, -5.1], [3.2, 1.0431, -25.8, -11.0], [4.8, 1.0661, -38.7, -17.6], [6.4, 1.09, -51.6, -24.8], [8.0, 1.1149, -64.5, -32.8]],
  14: [[0.0, 1.0, 0.0, 0.0], [1.6, 1.0003, -0.1, 44.9], [3.2, 1.0006, -0.3, 99.1], [4.8, 1.0008, -0.5, 162.7], [6.4, 1.0009, -0.8, 235.7], [8.0, 1.001, -1.0, 318.1]],
  15: [[0.0, 1.0, 0.0, 0.0], [1.2, 1.0012, -0.6, -1.1], [2.4, 1.0025, -1.3, -2.4], [3.6, 1.004, -2.1, -3.9], [4.8, 1.0057, -3.0, -5.6], [6.0, 1.0076, -4.0, -7.6]],
  16: [[0.0, 1.0, 0.0, 0.0], [1.8, 1.0217, -12.0, -6.9], [3.6, 1.0434, -24.2, -14.0], [5.4, 1.065, -36.5, -21.3], [7.2, 1.0866, -48.9, -28.9], [9.0, 1.1081, -61.4, -36.6]],
};

const camAt = (i: number, tSec: number) => {
  const k = CAM[i];
  if (!k) return { s: 1, tx: 0, ty: 0 };
  const t = Math.max(0, tSec);
  let j = 0;
  while (j < k.length - 2 && t > k[j + 1][0]) j++;
  const a = k[j], b = k[j + 1], w = Math.min(1, Math.max(0, (t - a[0]) / (b[0] - a[0] || 1)));
  return { s: a[1] + (b[1] - a[1]) * w, tx: a[2] + (b[2] - a[2]) * w, ty: a[3] + (b[3] - a[3]) * w };
};

// ---------- timeline + transitions ----------
const CUT = [0, 99, 240, 396, 471, 567, 711, 867, 1023, 1101, 1206, 1434, 1596, 1806, 2034, 2256, 2409, 2637];
const CLIPS = Array.from({ length: 17 }, (_, i) => `sf/s${String(i + 1).padStart(2, "0")}.mp4`);
type TK = "iris" | "ray" | "wave";
type Tr = { k: TK; a: number; b: number; o?: Pt; night?: boolean; low?: boolean };
// keyed by INCOMING shot index (0-based). Window = [cut-a, cut+b]. 8->9 changed to a=3 (clip s09 is only 3.04 s).
const TR: Record<number, Tr> = {
  1: { k: "iris", a: 6, b: 8, o: [537, 1318] },
  // v2 (owner yes 2026-11-13): ray wipe kept ONLY at sunrise (into s07); 4->5 and 11->12 are hard cuts now.
  5: { k: "wave", a: 7, b: 7, night: true },
  6: { k: "ray", a: 8, b: 6, o: [542, 408] },
  8: { k: "wave", a: 3, b: 7 },
  9: { k: "iris", a: 6, b: 8, o: [542, 1125] },
  16: { k: "iris", a: 8, b: 6, o: [542, 1640], low: true },
};
const shotStart = (i: number) => CUT[i] - (TR[i]?.a ?? 0);
const shotEnd = (i: number) => CUT[i + 1] + (TR[i + 1]?.b ?? 0);
const trP = (i: number, f: number) => {
  const t = TR[i];
  if (!t) return -1;
  const w0 = CUT[i] - t.a, w1 = CUT[i] + t.b;
  if (f < w0 || f >= w1) return -1;
  return (f - w0) / (t.a + t.b);
};

const dataUri = (svg: string) => `url("data:image/svg+xml,${encodeURIComponent(svg)}")`;
const irisR = (p: number) => 2100 * OUT(p);
const irisPts = (o: Pt, R: number, rot: number) => {
  const pts: string[] = [];
  for (let d = 0; d < 360; d += 3) {
    const th = rad(d), r = R * (1 + 0.07 * Math.sin(16 * th + rot));
    pts.push(`${(o[0] + r * Math.cos(th)).toFixed(1)},${(o[1] + r * Math.sin(th)).toFixed(1)}`);
  }
  return pts.join(" ");
};
const WROT = (f: number, w0: number) => rad(0.5 * (f - w0));

const rayWedges = (o: Pt, p: number, from: number, to: number) => {
  const R = 2400, rot = 6 * p;
  const out: { d: string; k: number }[] = [];
  for (let k = 0; k < 16; k++) {
    const a0 = k * 22.5 + rot + from * 22.5, a1 = k * 22.5 + rot + to * 22.5;
    if (a1 - a0 < 0.01) continue;
    const x0 = o[0] + R * Math.cos(rad(a0)), y0 = o[1] + R * Math.sin(rad(a0));
    const x1 = o[0] + R * Math.cos(rad(a1)), y1 = o[1] + R * Math.sin(rad(a1));
    out.push({ d: `M ${o[0]} ${o[1]} L ${x0.toFixed(1)} ${y0.toFixed(1)} A ${R} ${R} 0 0 1 ${x1.toFixed(1)} ${y1.toFixed(1)} Z`, k });
  }
  return out;
};
const rayMask = (o: Pt, p: number) => {
  const e = SINE(p);
  const w = rayWedges(o, e, 0, e);
  return dataUri(`<svg xmlns='http://www.w3.org/2000/svg' width='1080' height='1920'>${w.map((q) => `<path d='${q.d}' fill='white'/>`).join("")}</svg>`);
};

const waveY = (x: number, Y: number, ph: number) => Y + 28 * Math.sin((2 * Math.PI * x) / 270 + ph);
const waveGeo = (p: number, f: number, w0: number) => {
  const Y = lerp(p, 0, 1, 1980, -170, INOUT);
  const sl = (2 * Math.PI * 8 * (f - w0)) / 270;
  return { Y, ph1: 0.6 + sl, ph2: 2.1 - sl };
};
const waveMask = (p: number, f: number, w0: number) => {
  const { Y, ph2 } = waveGeo(p, f, w0);
  const pts: string[] = [];
  for (let x = -20; x <= 1100; x += 20) pts.push(`${x},${(waveY(x, Y + 120, ph2)).toFixed(1)}`);
  return dataUri(`<svg xmlns='http://www.w3.org/2000/svg' width='1080' height='1920'><polygon points='${pts.join(" ")} 1100,2100 -20,2100' fill='white'/></svg>`);
};

// ---------- motifs (all inside an <svg>) ----------
const FLAME = "M 0 0 C -44 -22 -36 -62 3 -100 C 34 -64 46 -26 0 0 Z";
const Flame1: React.FC<{ x: number; y: number; h: number; rot?: number; c?: [string, string, string]; o?: number }> = ({ x, y, h, rot = 0, c = FLC, o = 1 }) =>
  h <= 0.5 ? null : (
    <g transform={`translate(${x.toFixed(1)} ${y.toFixed(1)}) rotate(${rot.toFixed(1)}) scale(${(h / 100).toFixed(3)})`} opacity={o}>
      <path d={FLAME} fill={c[0]} />
      <g transform="scale(0.66)"><path d={FLAME} fill={c[1]} /></g>
      <g transform="scale(0.34)"><path d={FLAME} fill={c[2]} /></g>
    </g>
  );
const STAR = "M 0 -1 Q 0.16 -0.16 1 0 Q 0.16 0.16 0 1 Q -0.16 0.16 -1 0 Q -0.16 -0.16 0 -1 Z";
const Star: React.FC<{ x: number; y: number; r: number; f: number; col?: string; at?: number; o?: number; still?: boolean }> = ({ x, y, r, f, col = C.star, at, o = 1, still }) => {
  const pp = at === undefined ? 1 : pop(f, at);
  if (pp <= 0.01 || r <= 0.5) return null;
  const tw = still ? 1 : 0.925 + 0.075 * Math.sin((2 * Math.PI * f) / 60 + x * 0.05);
  return <g transform={`translate(${x} ${y}) scale(${(r * pp * tw).toFixed(2)})`} opacity={o}><path d={STAR} fill={col} /></g>;
};

/** One spark flying a Catmull-Rom path. cool: orange -> star teal in the last 20 frames, becomes a twinkling star. */
const Flight: React.FC<{ f: number; P: Pt[]; L: number; D: number; s0: number; s1: number; cool?: boolean; star?: number; c?: [string, string, string]; starCol?: string; hold?: boolean }> =
  ({ f, P, L, D, s0, s1, cool, star = 44, c = FLC, starCol = C.star, hold = true }) => {
    if (f < L) return null;
    const end = P[P.length - 1];
    if (f >= L + D) {
      if (cool) return <Star x={end[0]} y={end[1]} r={star / 2} f={f} col={starCol} />;
      return hold ? <Flame1 x={end[0]} y={end[1]} h={s1} rot={sway(f, end[0], 4)} c={c} /> : null;
    }
    const u = lerp(f, L, L + D, 0, 1, Easing.out(Easing.quad));
    const [x, y] = posOn(P, u);
    const [xa, ya] = posOn(P, Math.min(1, u + 0.03)), [xb, yb] = posOn(P, Math.max(0, u - 0.03));
    const rot = Math.max(-8, Math.min(8, (Math.atan2(xa - xb, -(ya - yb)) * 180) / Math.PI));
    const size = s0 + (s1 - s0) * u;
    const w = cool ? lerp(f, L + D - 20, L + D, 0, 1) : 0;
    const cc: [string, string, string] = cool ? [mixc(w, c[0], starCol), mixc(w, c[1], starCol), mixc(w, c[2], C.cream)] : c;
    return (
      <>
        {w < 1 && <Flame1 x={x} y={y} h={size} rot={rot} c={cc} o={1 - w * 0.6} />}
        {w > 0 && <Star x={x} y={y} r={(star / 2) * w} f={f} col={starCol} still />}
      </>
    );
  };

/** Low sparks: n small flames looping in a box, life 30 frames, staggered, deterministic. */
const LowSparks: React.FC<{ f: number; box: Box; from: number; to?: number; n?: number; size?: number; life?: number; c?: [string, string, string] }> =
  ({ f, box, from, to = 99999, n = 6, size = 22, life = 30, c = FLC }) => {
    if (f < from || f >= to) return null;
    return (
      <>
        {Array.from({ length: n }, (_, i) => {
          const g = (f - from) / life + i / n, k = Math.floor(g), t = g - k;
          const x = box.x1 + ((i * 0.381966 + k * 0.2718) % 1) * (box.x2 - box.x1) + 6 * Math.sin(t * 6.28 + i);
          const y = box.y2 - (box.y2 - box.y1) * t;
          return <Flame1 key={i} x={x} y={y} h={size * Math.sin(Math.PI * Math.min(1, t * 1.1 + 0.05))} c={c} />;
        })}
      </>
    );
  };

const TONGUE_SZ = [1.0, 0, 0.62, 0, 0.88, 0.5, 0, 0.78, 0, 0.58, 0.95, 0];
const TONGUE_DA = [0, 0, 6, 0, -8, 5, 0, -4, 0, 9, -6, 0];
/** Tongue ring: 12 flames around a fire rim; pulse(s) 1 -> 1.15 -> 1 over 12 frames at pulseAt. warm 0..1 blends dull -> bright. */
const TongueRing: React.FC<{ f: number; cx: number; cy: number; rx: number; ry: number; size: number; at: number; pulses?: number[]; warm?: number; sweep?: [number, number]; yieldAt?: number; yieldK?: number[] }> =
  ({ f, cx, cy, rx, ry, size, at, pulses = [], warm = 1, sweep, yieldAt, yieldK = [] }) => {
    const c: [string, string, string] = [mixc(warm, C.rust, C.orange), mixc(warm, C.mustard, C.flameMid), mixc(warm, C.cream, C.core)];
    return (
      <>
        {Array.from({ length: 12 }, (_, k) => {
          // v2: 7 of the 12 slots, mixed sizes + a little angle offset, so the ring reads hand-printed, not stickered.
          const vs = TONGUE_SZ[k];
          if (vs === 0) return null;
          const th = rad(-90 + k * 30 + TONGUE_DA[k]);
          const x = cx + rx * Math.cos(th), y = cy + ry * Math.sin(th);
          let s = pop(f, at + (k % 3));
          for (const pf of pulses) s *= 1 + 0.15 * Math.sin(Math.PI * lerp(f, pf, pf + 12, 0, 1));
          if (sweep) s *= 1 + 0.3 * Math.sin(Math.PI * lerp(f, sweep[0] + k * 5, sweep[0] + k * 5 + 5, 0, 1));
          if (yieldAt !== undefined && yieldK.includes(k)) s *= lerp(f, yieldAt, yieldAt + 9, 1, 0);
          return <Flame1 key={k} x={x} y={y + size * vs * 0.15} h={size * vs * s} rot={((x - cx) / rx) * 22 + sway(f, x, 2)} c={c} />;
        })}
      </>
    );
  };

// -- count coals (M2). state: 'lit' | 'cold' | 'out'. events in absolute frames.
const smokeD = (h: number) => {
  const pts: Pt[] = [];
  for (let k = 0; k <= 12; k++) { const t = k / 12; pts.push([10 * Math.sin(t * 5), -h * t]); }
  const [lx, ly] = pts[pts.length - 1];
  for (let k = 1; k <= 7; k++) { const a = Math.PI + (k / 7) * 1.5 * Math.PI; pts.push([lx + 9 + 9 * Math.cos(a), ly - 8 + 8 * Math.sin(a)]); }
  return smoothD(pts);
};
const Coal: React.FC<{ f: number; x: number; y: number; at: number; s0: "lit" | "cold" | "out"; lightAt?: number; outAt?: number; swellAt?: number; k?: number }> =
  ({ f, x, y, at, s0, lightAt, outAt, swellAt, k = COAL_K }) => {
    const pp = pop(f, at);
    if (pp <= 0.01) return null;
    let flame = 0;
    if (s0 === "lit") flame = lerp(f, at + 2, at + 10, 0, 90, BACK);
    if (lightAt !== undefined) flame = lerp(f, lightAt, lightAt + 8, 0, 90, BACK);
    if (outAt !== undefined && f >= outAt) flame = lerp(f, outAt, outAt + 6, 90, 0);
    const isOut = s0 === "out" || (outAt !== undefined && f >= outAt);
    const swell = swellAt !== undefined ? 1 + 0.25 * Math.sin(Math.PI * lerp(f, swellAt, swellAt + 10, 0, 1)) : 1;
    const lit = flame > 5 && !isOut;
    const crack = lit || (lightAt !== undefined && f >= lightAt) ? C.orange : "#6DBDB3";
    const sm = outAt !== undefined ? f - outAt - 6 : -1;
    const smokeDraw = lerp(sm, 0, 12, 0, 1), drift = Math.max(0, sm - 12) * 0.4;
    const smokeO = sm < 0 ? 0 : sm > 36 ? 0 : sm > 28 ? lerp(sm, 28, 36, 1, 0) : 1;
    const sw = swellAt !== undefined || lit ? 1 : 1;
    return (
      <g transform={`translate(${x} ${y}) scale(${(k * pp * swell * sw).toFixed(3)})`}>
        <ellipse cx={2} cy={-2} rx={35} ry={17} fill="none" stroke={C.ink} strokeWidth={3} />
        <ellipse cx={0} cy={0} rx={35} ry={17} fill={C.coal} />
        <path d="M -16 -2 L -6 3 L 2 -3 L 12 4 M -4 -9 L 4 -4" stroke={crack} strokeWidth={2.5} fill="none" strokeLinecap="round" />
        {isOut && <circle cx={4} cy={-4} r={10} fill={C.mid} />}
        {flame > 0.5 && <Flame1 x={0} y={-6} h={flame} rot={sway(f, x, 3)} />}
        {outAt !== undefined && smokeO > 0 && smokeDraw > 0 && (
          <g transform={`translate(4 ${-14 - drift})`} opacity={smokeO}>
            <path d={smokeD(60)} pathLength={1} strokeDasharray={1} strokeDashoffset={1 - smokeDraw} fill="none" stroke={C.steam} strokeWidth={4.5} strokeLinecap="round" />
          </g>
        )}
      </g>
    );
  };

// -- ray stitches (M4): dotted rays from the sun, drawn outward then crawling.
const Rays: React.FC<{ f: number; o: Pt; angles: number[]; r0: number; r1: number; a: number; b: number; col?: string; dot?: number }> =
  ({ f, o, angles, r0, r1, a, b, col = C.cream, dot = 16 }) => {
    if (f < a) return null;
    const n = angles.length, dur = Math.max(10, (b - a) / 2);
    return (
      <>
        {angles.map((ang, k) => {
          const s = a + ((b - a - dur) * k) / Math.max(1, n - 1);
          const p = lerp(f, s, s + dur, 0, 1, OUT);
          if (p <= 0) return null;
          const cs = Math.cos(rad(ang)), sn = Math.sin(rad(ang)), rr = r0 + (r1 - r0) * p;
          return <line key={k} x1={o[0] + r0 * cs} y1={o[1] + r0 * sn} x2={o[0] + rr * cs} y2={o[1] + rr * sn}
            stroke={col} strokeWidth={dot} strokeLinecap="round" strokeDasharray="0.01 34" strokeDashoffset={-Math.max(0, f - b) * 0.4} />;
        })}
      </>
    );
  };

// -- wave scallops (M5): row of joined arcs, scrolls sideways, clipped to its box.
const Waves: React.FC<{ f: number; x1: number; x2: number; y: number; at: number; col?: string; dir?: number; sw?: number; id: string }> =
  ({ f, x1, x2, y, at, col = C.cream, dir = 1, sw = 6.5, id }) => {
    if (f < at) return null;
    const off = (((f - at) * 0.667 * dir) % 60 + 60) % 60;
    let d = `M ${x1 - 60 + off - 60} ${y}`;
    for (let x = x1 - 120; x < x2 + 60; x += 60) d += ` a 30 30 0 0 1 60 0`;
    const w = (x2 - x1) * lerp(f, at, at + 14, 0, 1, OUT);
    return (
      <g>
        <clipPath id={`wc${id}`}><rect x={x1} y={y - 40} width={Math.max(0.1, w)} height={50} /></clipPath>
        <g clipPath={`url(#wc${id})`}><path d={d} fill="none" stroke={col} strokeWidth={sw} strokeLinecap="round" /></g>
      </g>
    );
  };

// -- woven band (M6)
const Woven: React.FC<{ f: number; a: number; b: number; y: number }> = ({ f, a, b, y }) => {
  const p = lerp(f, a, b, 0, 1, SINE);
  if (p <= 0) return null;
  let zz = "", dots: React.ReactNode[] = [];
  for (let x = -22, k = 0; x < 1120; x += 44, k++) {
    zz += `${k === 0 ? "M" : "L"} ${x} ${y + 14} L ${x + 22} ${y - 14} `;
    dots.push(<circle key={k} cx={x + 44} cy={y + 8} r={5.5} fill={C.coral} />);
  }
  return (
    <g>
      <clipPath id="wvc"><rect x={0} y={y - 30} width={1080 * p} height={60} /></clipPath>
      <g clipPath="url(#wvc)">
        <rect x={0} y={y - 22} width={1080} height={44} fill={C.mid} />
        <path d={zz + `L 1200 ${y + 14}`} fill="none" stroke={C.mustard} strokeWidth={7} strokeLinejoin="round" />
        {dots}
        <line x1={0} y1={y - 22} x2={1080} y2={y - 22} stroke={C.ink} strokeWidth={3} />
        <line x1={0} y1={y + 22} x2={1080} y2={y + 22} stroke={C.ink} strokeWidth={3} />
      </g>
    </g>
  );
};

// -- folk flower + stem (M7) and spiky agave
const PET = ["coral", "mustard", "cream"] as const;
const Daisy: React.FC<{ f: number; x: number; y: number; r: number; at: number; i: number; stem?: number }> = ({ f, x, y, r, at, i, stem = 120 }) => {
  const sp = lerp(f, at - 8, at, 0, 1);
  if (sp <= 0) return null;
  const hp = pop(f, at);
  const col = C[PET[i % 3]];
  const rot = sway(f, x, 4);
  const sd = `M ${x} ${y + stem} Q ${x - 10} ${y + stem * 0.5} ${x} ${y}`;
  return (
    <g>
      <path d={sd} pathLength={1} strokeDasharray={1} strokeDashoffset={1 - sp} stroke={C.mid} strokeWidth={5} fill="none" strokeLinecap="round" />
      {sp > 0.5 && <path d={`M ${x - 4} ${y + stem * 0.55} q -26 -14 -34 -2 q 22 12 34 2 z M ${x - 2} ${y + stem * 0.8} q 26 -14 34 -2 q -22 12 -34 2 z`} fill={C.mid} stroke={C.ink} strokeWidth={2} />}
      {hp > 0.01 && (
        <g transform={`translate(${x} ${y}) rotate(${rot}) scale(${hp})`}>
          {[0, 1, 2, 3, 4, 5].map((k) => (<ellipse key={`o${k}`} cx={2} cy={-r * 0.6 - 2} rx={r * 0.34} ry={r * 0.5} transform={`rotate(${k * 60})`} fill="none" stroke={C.ink} strokeWidth={3} />))}
          {[0, 1, 2, 3, 4, 5].map((k) => (<ellipse key={k} cx={0} cy={-r * 0.6} rx={r * 0.34} ry={r * 0.5} transform={`rotate(${k * 60})`} fill={col} />))}
          <circle r={r * 0.3} fill={C.mid} /><circle cx={-r * 0.08} cy={-r * 0.08} r={r * 0.09} fill={C.cream} />
        </g>
      )}
    </g>
  );
};
const Agave: React.FC<{ f: number; x: number; y: number; len: number; at: number; col: string; n?: number; spread?: number }> = ({ f, x, y, len, at, col, n = 6, spread = 110 }) => {
  const g = lerp(f, at, at + 12, 0, 1, BACK);
  if (g <= 0.01) return null;
  const rot = sway(f, x, 2.5);
  return (
    <g transform={`translate(${x} ${y}) rotate(${rot}) scale(${g})`}>
      {Array.from({ length: n }, (_, k) => {
        const a = -spread / 2 + (spread * k) / (n - 1), L = len * (1 - 0.22 * Math.abs(k - (n - 1) / 2) / ((n - 1) / 2));
        return <path key={k} d={`M -14 0 Q -9 ${-L * 0.55} 0 ${-L} Q 9 ${-L * 0.55} 14 0 Z`} transform={`rotate(${a})`} fill={col} />;
      })}
    </g>
  );
};

// -- gull (M8): follows pos(f); wings flap.
const Gull: React.FC<{ f: number; pos: (f: number) => Pt | null; kind: "tick" | "white"; s?: number }> = ({ f, pos, kind, s = 1 }) => {
  const p = pos(f);
  if (!p) return null;
  const p2 = pos(f + 3) ?? p;
  const flap = 0.4 + 0.6 * Math.abs(Math.sin((Math.PI * f) / 10));
  const bob = 6 * Math.sin((2 * Math.PI * f) / 40);
  const sx = p2[0] >= p[0] ? 1 : -1;
  return (
    <g transform={`translate(${p[0].toFixed(1)} ${(p[1] + bob).toFixed(1)}) scale(${sx * s * 1.3} ${s * 1.3})`}>
      {kind === "tick" ? (
        <g transform={`scale(1 ${flap})`}><path d="M -17 0 Q -8 -14 0 0 Q 8 -14 17 0" fill="none" stroke={C.ink} strokeWidth={4} strokeLinecap="round" strokeLinejoin="round" /></g>
      ) : (
        <g>
          <g transform={`scale(1 ${flap})`}>
            <path d="M 3 0 Q 16 -24 38 -15 Q 24 -6 3 6 Z" fill={C.cream} stroke={C.ink} strokeWidth={3} strokeLinejoin="round" />
            <path d="M -3 0 Q -16 -24 -38 -15 Q -24 -6 -3 6 Z" fill={C.cream} stroke={C.ink} strokeWidth={3} strokeLinejoin="round" />
            <path d="M 32 -17 L 40 -15 L 36 -9 Z M -32 -17 L -40 -15 L -36 -9 Z" fill={C.ink} />
          </g>
          <ellipse cx={0} cy={3} rx={12} ry={7} fill={C.cream} stroke={C.ink} strokeWidth={2.5} />
          <circle cx={11} cy={0} r={3} fill={C.ink} />
        </g>
      )}
    </g>
  );
};
const arc3 = (a: Pt, c: Pt, b: Pt, u: number): Pt => [(1 - u) * (1 - u) * a[0] + 2 * (1 - u) * u * c[0] + u * u * b[0], (1 - u) * (1 - u) * a[1] + 2 * (1 - u) * u * c[1] + u * u * b[1]];
const gullArc = (a: Pt, c: Pt, b: Pt, f0: number, f1: number) => (f: number): Pt | null => (f < f0 || f > f1 ? null : arc3(a, c, b, lerp(f, f0, f1, 0, 1, SINE)));

// -- fish (M9): leaps one arc out of the sea; optional smaller repeats.
const FISH = "M 55 0 Q 10 -28 -40 -4 L -62 -22 Q -52 0 -62 22 L -40 4 Q 10 28 55 0 Z";
const Fish: React.FC<{ f: number; at: number; x: number; dx: number; y: number; H?: number; dur?: number; repeat?: boolean }> = ({ f, at, x, dx, y, H = 140, dur = 24, repeat }) => {
  if (f < at) return null;
  const k = Math.floor((f - at) / 45);
  if (k > 0 && !repeat) return null;
  const t = f - at - 45 * k;
  const d = k === 0 ? dur : 20, hh = k === 0 ? H : 70, ddx = k === 0 ? dx : (k % 2 ? -1 : 1) * 50;
  const xx = k === 0 ? x : x + dx * (k % 2 ? 1 : 0);
  const u = t / d;
  if (u < 0 || u > 1) return null;
  const px = xx + ddx * u, py = y - hh * 4 * u * (1 - u);
  const th = (Math.atan2(-4 * hh * (1 - 2 * u), Math.abs(ddx) || 1) * 180) / Math.PI;
  const sx = ddx < 0 ? -1 : 1;
  const sc = lerp(t, 0, 3, 0.4, 1) * lerp(t, d - 3, d, 1, 0.5);
  const dropT = t / 14;
  return (
    <g>
      <g transform={`translate(${px.toFixed(1)} ${py.toFixed(1)}) scale(${sx * sc * 1.45} ${sc * 1.45}) rotate(${th.toFixed(1)})`}>
        <path d={FISH} fill="none" stroke={C.ink} strokeWidth={3} transform="translate(2 -2)" />
        <path d={FISH} fill={C.fish} />
        <path d="M 38 7 Q 5 17 -30 5" fill="none" stroke={C.cream} strokeWidth={3} strokeLinecap="round" />
        <path d="M -8 -8 Q -2 -2 -8 4 M 6 -9 Q 12 -2 6 5 M 20 -8 Q 26 -1 20 5 M -22 -5 Q -17 0 -22 5" fill="none" stroke={C.ink} strokeWidth={2} strokeLinecap="round" />
        <circle cx={38} cy={-6} r={3.6} fill={C.ink} />
      </g>
      {k === 0 && dropT >= 0 && dropT <= 1 && [0, 1, 2].map((q) => (
        <circle key={q} cx={xx + (q - 1) * 26 * dropT} cy={y - 40 * Math.sin(Math.PI * dropT) * (1 - 0.2 * q) + 18 * dropT * dropT} r={6 - q} fill={C.cream} opacity={1 - dropT * 0.6} />
      ))}
    </g>
  );
};

// -- ripple ring + steam curl (M10)
const Ripple: React.FC<{ f: number; at: number; x: number; y: number; col?: string }> = ({ f, at, x, y, col = C.star }) => {
  const u = lerp(f, at, at + 24, 0, 1, OUT);
  if (f < at || u >= 1) return null;
  return <ellipse cx={x} cy={y} rx={30 + 120 * u} ry={10 + 40 * u} fill="none" stroke={col} strokeWidth={4} opacity={1 - u * u} />;
};
const steamD = (h: number, amp: number, ph: number) => {
  const pts: Pt[] = [];
  for (let k = 0; k <= 22; k++) { const t = k / 22; pts.push([amp * Math.sin(ph + t * 2.4 * Math.PI) * (0.4 + t), -h * t]); }
  const [lx, ly] = pts[pts.length - 1];
  for (let k = 1; k <= 9; k++) { const a = Math.PI + (k / 9) * 1.6 * Math.PI; pts.push([lx + 18 + 18 * Math.cos(a), ly - 16 + 16 * Math.sin(a)]); }
  return smoothD(pts);
};
const Steam: React.FC<{ f: number; at: number; x: number; y: number; h?: number; amp?: number; ph?: number }> = ({ f, at, x, y, h = 220, amp = 20, ph = 0 }) => {
  if (f < at) return null;
  const p = lerp(f, at, at + 20, 0, 1, OUT), drift = Math.max(0, f - at - 20) * 0.35;
  return (
    <g transform={`translate(${x} ${y - drift})`}>
      <path d={steamD(h, amp, ph)} pathLength={1} strokeDasharray={1} strokeDashoffset={1 - p} fill="none" stroke={C.steam} strokeWidth={7 - 3.5 * Math.min(1, drift / 60)} strokeLinecap="round" />
    </g>
  );
};

// -- splash crown (s09)
const Crown: React.FC<{ f: number; x: number; y: number; r: number; at: number }> = ({ f, x, y, r, at }) => {
  const s = pop(f, at);
  if (s <= 0.01) return null;
  const n = Math.max(5, Math.round((Math.PI * r) / 62));
  let d = "";
  for (let k = 0; k <= n; k++) {
    const th = rad(180 + (180 * k) / n), px = x + r * Math.cos(th), py = y + r * Math.sin(th);
    if (k === 0) d = `M ${px.toFixed(1)} ${py.toFixed(1)}`;
    else d += ` A ${(r * 0.17).toFixed(1)} ${(r * 0.17).toFixed(1)} 0 0 1 ${px.toFixed(1)} ${py.toFixed(1)}`;
  }
  return <g transform={`translate(${x} ${y}) scale(${s}) translate(${-x} ${-y})`}><path d={d} fill="none" stroke={C.cream} strokeWidth={8} strokeLinecap="round" /></g>;
};

// ---------- per-shot layers ----------
const rr = (f: number, a: number, b: number) => lerp(f, a, b, 0, 1);

const S01 = (f: number) => {
  const spots: Pt[] = [[130, 110], [420, 200], [610, 80], [950, 340], [300, 330], [700, 260], [60, 470], [1010, 520]];
  const launch = [-40, -28, -16, -4, 8, 20, 32, 44];
  const lanes = [[50, 150, 200], [1030, 940, 880], [60, 190, 240], [1020, 960, 900], [70, 120, 180], [1010, 980, 920], [40, 170, 220], [1040, 930, 860]];
  return (
    <>
      {launch.map((L, i) => {
        const [x0, x1, x2] = lanes[i];
        const P: Pt[] = [[x0, 1960], [x0, 1400], [x1, 1150], [x2, 700], spots[i]];
        return <Flight key={i} f={f} P={P} L={L} D={70} s0={40} s1={60} cool star={56} />;
      })}
      <Agave f={f} x={40} y={1925} len={200} at={-100} col={C.spike} n={5} spread={80} />
      <Agave f={f} x={1040} y={1925} len={200} at={-100} col={C.spike} n={5} spread={80} />
    </>
  );
};

const S02 = (f: number) => {
  const spots: Pt[] = [[120, 120], [420, 150], [610, 90], [760, 200], [480, 330], [930, 110], [140, 420], [680, 420]];
  return (
    <>
      <TongueRing f={f} cx={537} cy={1335} rx={150} ry={62} size={38} at={99} pulses={[99]} warm={0} />
      {spots.map((sp, i) => keep(i) && (
        <Flight key={i} f={f} P={[[537, 1235], [538, 1100], [538, 930], [(538 + sp[0]) / 2, (930 + sp[1]) / 2], sp]} L={112 + 12 * i} D={50} s0={22} s1={44} cool star={44} />
      ))}
      <LowSparks f={f} box={{ x1: 490, y1: 1150, x2: 590, y2: 1240 }} from={105} c={FLC_DULL} />
      {[0, 1, 2].map((i) => <Coal key={i} f={f} x={[420, 537, 654][i] - [20, 27, 34][i]} y={[1500, 1530, 1500][i] + [10, 10, 20][i]} at={198 + 7 * i} s0="lit" />)}
      <Agave f={f} x={60} y={1925} len={220} at={104} col={C.spike} n={5} spread={80} />
      <Agave f={f} x={230} y={1925} len={220} at={110} col={C.spike} n={5} spread={80} />
    </>
  );
};

const S03 = (f: number) => {
  const spots: Pt[] = [[200, 110], [470, 230], [660, 90], [380, 400]];
  return (
    <>
      <LowSparks f={f} box={{ x1: 480, y1: 1180, x2: 570, y2: 1280 }} from={240} />
      {spots.map((sp, i) => keep(i) && (
        <Flight key={i} f={f} P={[[525, 1250], [450, 1040], [440, 700], sp]} L={250 + 20 * i} D={60} s0={22} s1={42} cool star={40} />
      ))}
      <Coal f={f} x={420} y={1670} at={236} s0="lit" outAt={367} />
      <Coal f={f} x={510} y={1690} at={236} s0="lit" />
      <Coal f={f} x={600} y={1670} at={236} s0="lit" />
    </>
  );
};

const S04 = (f: number) => (
  <>
    <LowSparks f={f} box={{ x1: 490, y1: 1190, x2: 580, y2: 1290 }} from={396} to={443} />
    {([[150, 140], [520, 90], [640, 260]] as Pt[]).map((sp, i) => (
      <Flight key={i} f={f} P={[[533, 1260], [520, 900], sp]} L={412 + 8 * i} D={50} s0={22} s1={36} cool star={38} />
    ))}
    {([[700, 120], [760, 230], [820, 340]] as Pt[]).map((p, i) => <Star key={i} x={p[0]} y={p[1]} r={20} f={f} at={401 + 11 * i} col={C.cream} still />)}
    <Coal f={f} x={470} y={1720} at={396} s0="out" outAt={367} />
    <Coal f={f} x={560} y={1740} at={396} s0="lit" outAt={418} />
    <Coal f={f} x={650} y={1720} at={396} s0="lit" outAt={440} />
  </>
);

const S05 = (f: number) => (
  <>
    <Rays f={f} o={[520, 800]} angles={[190, 215, 238, 255, 270, 285, 302, 325, 350]} r0={240} r1={800} a={512} b={540} />
    <Gull f={f} pos={gullArc([600, 560], [800, 330], [1010, 190], 520, 567)} kind="tick" />
    {keep(1) && <Gull f={f} pos={gullArc([620, 580], [760, 420], [900, 260], 528, 567)} kind="tick" s={0.8} />}
    {([[160, 1700], [360, 1790], [560, 1740], [760, 1810], [930, 1720]] as Pt[]).map((p, i) => keep(i) && <Daisy key={i} f={f} x={p[0]} y={p[1]} r={34} at={526 + 5 * i} i={i} />)}
  </>
);

const S06 = (f: number) => {
  const stars: Pt[] = [[110, 90], [400, 250], [560, 110], [90, 420], [330, 470], [590, 330]];
  const rows: [number, number, number][] = [[0, 240, 860], [0, 240, 980], [0, 240, 1100], [0, 330, 1770], [0, 1080, 1850]];
  return (
    <>
      {stars.map((p, i) => keep(i) && <Star key={i} x={p[0]} y={p[1]} r={30 + (i % 3) * 6} f={f} at={570 + 3 * i} col={C.cream} />)}
      {rows.map((r, i) => keep(i) && <Waves key={i} id={`s6${i}`} f={f} x1={r[0]} x2={r[1]} y={r[2]} at={568 + 4 * i} col={C.star} dir={i % 2 ? -1 : 1} />)}
      <Ripple f={f} at={650} x={800} y={1830} />
      <Ripple f={f} at={662} x={800} y={1830} />
      <Ripple f={f} at={674} x={800} y={1830} />
    </>
  );
};

const S07 = (f: number) => (
  <>
    <Rays f={f} o={[542, 400]} angles={[200, 214, 228, 242, 256, 270, 284, 298, 312, 326, 340]} r0={230} r1={900} a={717} b={745} />
    <Gull f={f} pos={gullArc([-40, 560], [540, 300], [1120, 470], 730, 800)} kind="white" />
    {keep(1) && <Gull f={f} pos={gullArc([-40, 560], [540, 300], [1120, 470], 750, 820)} kind="white" s={0.9} />}
    <Gull f={f} pos={gullArc([-40, 560], [540, 300], [1120, 470], 775, 845)} kind="white" s={0.85} />
    {([[620, 900, 660], [640, 900, 880], [620, 940, 940]] as [number, number, number][]).map((r, i) => keep(i) && <Waves key={i} id={`s7${i}`} f={f} x1={r[0]} x2={r[1]} y={r[2]} at={724 + 4 * i} dir={i % 2 ? -1 : 1} />)}
    {([[170, 1760], [330, 1830], [520, 1790], [700, 1850], [880, 1770], [1010, 1840]] as Pt[]).map((p, i) => keep(i) && <Daisy key={i} f={f} x={p[0]} y={p[1]} r={36} at={722 + 6 * i} i={i} />)}
    <Ripple f={f} at={822} x={850} y={845} col={C.cream} />
    <Ripple f={f} at={832} x={850} y={845} col={C.cream} />
    <Ripple f={f} at={842} x={850} y={845} col={C.cream} />
  </>
);

const S08 = (f: number) => {
  const xs = [720, 980, 800, 1040, 880, 760, 940];
  return (
    <>
      {xs.map((x, i) => <Fish key={i} f={f} at={876 + 6 * i} x={x} dx={i % 2 ? -50 : 50} y={1700 + (i % 3) * 40} repeat />)}
      {([[940, 1060, 985], [950, 1060, 1075], [960, 1060, 1165]] as [number, number, number][]).map((r, i) => keep(i) && <Waves key={i} id={`s8${i}`} f={f} x1={r[0]} x2={r[1]} y={r[2]} at={880 + 5 * i} dir={i % 2 ? -1 : 1} />)}
      {[0, 1, 2, 3].map((i) => keep(i) && <Gull key={i} f={f} kind="white" s={0.9} pos={(ff) => { const t = ((ff - 867) / 90 + i * 0.25) * 2 * Math.PI; return [850 + 170 * Math.cos(t), 330 + 80 * Math.sin(t)]; }} />)}
      <Rays f={f} o={[576, 640]} angles={[190, 215, 235, 255, 270, 285, 305, 325, 350]} r0={200} r1={800} a={960} b={985} />
    </>
  );
};

const S09 = (f: number) => (
  <>
    <Crown f={f} x={440} y={1260} r={140} at={1040} />
    <Crown f={f} x={440} y={1260} r={220} at={1044} />
    <Crown f={f} x={440} y={1260} r={300} at={1048} />
    {Array.from({ length: 8 }, (_, i) => {
      const u = lerp(f, 1042, 1070, 0, 1), a = rad(200 + i * 20);
      if (f < 1042 || u >= 1) return null;
      return <circle key={i} cx={440 + 160 * Math.cos(a) * OUT(u)} cy={1260 + 160 * Math.sin(a) * OUT(u) + 220 * u * u} r={9} fill={C.cream} />;
    })}
    <Fish f={f} at={1046} x={120} dx={60} y={1480} />
    <Fish f={f} at={1056} x={330} dx={-60} y={1520} />
    {[1430, 1530].map((y, i) => <Waves key={y} id={`s9${i}`} f={f} x1={0} x2={1080} y={y} at={1050 + 6 * i} dir={i ? -1 : 1} />)}
    <g transform="translate(872 645)"><Flame1 x={0} y={0} h={22 * (0.95 + 0.15 * Math.sin((2 * Math.PI * f) / 14))} /></g>
  </>
);

const S10 = (f: number) => (
  <>
    <TongueRing f={f} cx={542} cy={1120} rx={480} ry={250} size={96} at={1101} pulses={[1101]} sweep={[1121, 0]} />
    {Array.from({ length: 8 }, (_, i) => {
      const sx = [380, 450, 520, 590, 660, 410, 560, 620][i];
      return <Flight key={i} f={f} P={sPath([542, 1040], [sx, 560 + ((i * 37) % 200)], 60, i % 2 ? 1 : -1)} L={1110 + 10 * i} D={60} s0={34} s1={52} c={FLC} />;
    })}
    {([[430, 880, 0], [620, 860, 2], [540, 820, 4]] as [number, number, number][]).map((p, i) => <Steam key={i} f={f} at={1112 + 12 * i} x={p[0]} y={p[1]} ph={p[2]} />)}
    {([[370, 700, 130], [330, 560, 250]] as [number, number, number][]).map((r, i) => keep(i) && <Waves key={i} id={`s10${i}`} f={f} x1={r[0]} x2={r[1]} y={r[2]} at={1106 + 8 * i} dir={i ? -1 : 1} />)}
    {([[140, 1790], [400, 1850], [700, 1800], [940, 1860]] as Pt[]).map((p, i) => keep(i) && <Daisy key={i} f={f} x={p[0]} y={p[1]} r={36} at={1108 + 6 * i} i={i} />)}
  </>
);

const S11 = (f: number) => {
  const tops: Pt[] = [[150, 90], [420, 60], [640, 150], [880, 70], [300, 230]];
  const warm = f >= 1428 ? 1 : lerp(f, 1375, 1428, 0, 1);
  const link: Pt[] = [[542, 1420], [700, 1250], [400, 1050], [537, 800]];
  return (
    <>
      <Woven f={f} a={1212} b={1242} y={960} />
      <TongueRing f={f} cx={537} cy={760} rx={120} ry={52} size={34} at={1206} pulses={[1298, 1372]} warm={warm * 0.9} />
      <TongueRing f={f} cx={542} cy={1570} rx={290} ry={140} size={62} at={1206} pulses={[1312, 1342]} warm={1} />
      {tops.map((sp, i) => keep(i) && <Flight key={i} f={f} P={sPath([537, 790], sp, 50, i % 2 ? 1 : -1)} L={1215 + 14 * i} D={60} s0={20} s1={36} cool star={40} c={FLC_DULL} />)}
      <LowSparks f={f} box={{ x1: 440, y1: 1330, x2: 640, y2: 1430 }} from={1206} size={26} />
      {Array.from({ length: 9 }, (_, i) => <Flight key={i} f={f} P={link} L={1375 + 5 * i} D={30} s0={26} s1={26} hold={false} />)}
    </>
  );
};

const S12 = (f: number) => (
  <>
    <Rays f={f} o={[535, 500]} angles={[209, 218, 227, 243, 277, 289, 302, 331]} r0={180} r1={760} a={1441} b={1466} />
    <Gull f={f} pos={gullArc([-40, 330], [500, 250], [1120, 400], 1450, 1560)} kind="tick" />
    {keep(1) && <Gull f={f} pos={gullArc([-40, 410], [500, 330], [1120, 300], 1470, 1560)} kind="tick" s={0.8} />}
    {([[20, 300, 790], [180, 420, 870], [190, 300, 955]] as [number, number, number][]).map((r, i) => keep(i) && <Waves key={i} id={`s12${i}`} f={f} x1={r[0]} x2={r[1]} y={r[2]} at={1444 + 5 * i} dir={i % 2 ? -1 : 1} />)}
    {([[90, 1860], [250, 1890], [560, 1870], [900, 1830], [1010, 1890]] as Pt[]).map((p, i) => keep(i) && <Daisy key={i} f={f} x={p[0]} y={p[1]} r={36} at={1480 + 5 * i} i={i} />)}
    <LowSparks f={f} box={{ x1: 540, y1: 1500, x2: 630, y2: 1610 }} from={1434} size={24} />
  </>
);

const S13 = (f: number) => (
  <>
    {[0, 1, 2].map((i) => <Coal key={i} f={f} x={[400, 542, 684][i]} y={[1790, 1815, 1790][i]} at={1660 + 7 * i} s0="cold" />)}
    <Steam f={f} at={1712} x={470} y={1500} h={180} ph={1} />
    <Steam f={f} at={1759} x={600} y={1490} h={180} ph={3} />
    <Rays f={f} o={[211, 622]} angles={[250, 265, 280, 295, 310, 325, 340]} r0={200} r1={700} a={1602} b={1630} />
    {keep(0) && <Gull f={f} pos={gullArc([-40, 260], [400, 150], [1120, 300], 1620, 1800)} kind="tick" />}
    {keep(1) && <Gull f={f} pos={gullArc([-40, 140], [600, 240], [1120, 120], 1650, 1800)} kind="tick" s={0.8} />}
    {([[60, 380, 760], [160, 400, 900]] as [number, number, number][]).map((r, i) => keep(i) && <Waves key={i} id={`s13${i}`} f={f} x1={r[0]} x2={r[1]} y={r[2]} at={1604 + 6 * i} dir={i ? -1 : 1} />)}
  </>
);

const S14 = (f: number) => {
  const spots: Pt[] = [[120, 140], [400, 90], [640, 100], [940, 120], [130, 300], [950, 320], [60, 470], [1010, 380]];
  const lanes = [[50, 120, 160], [1030, 1000, 960], [60, 150, 190], [1020, 940, 900], [70, 100, 130], [1010, 970, 930], [40, 170, 200], [1040, 910, 880]];
  return (
    <>
      <Gull f={f} pos={gullArc([-40, 130], [300, 60], [700, 140], 1806, 1990)} kind="tick" s={0.9} />
      {keep(1) && <Gull f={f} pos={gullArc([1120, 200], [800, 90], [500, 170], 1830, 2000)} kind="tick" s={0.8} />}
      <Agave f={f} x={30} y={1925} len={170} at={-100} col={C.mustard} n={5} spread={70} />
      <Agave f={f} x={1050} y={1925} len={170} at={-100} col={C.coral} n={5} spread={70} />
      {spots.map((sp, i) => {
        const [x0, x1, x2] = lanes[i];
        return <Flight key={i} f={f} P={[[x0, 1960], [x0, 1400], [x1, 1150], [x2, 600], [x2, Math.max(sp[1] + 40, 140)], sp]} L={1974 + 8 * i} D={70} s0={40} s1={60} />;
      })}
    </>
  );
};

const S15 = (f: number) => (
  <>
    <Rays f={f} o={[410, 560]} angles={[200, 220, 236, 252, 270, 288, 304, 320, 340]} r0={190} r1={800} a={2040} b={2068} />
    {([[700, 1500], [760, 1470], [850, 1510], [940, 1480], [1010, 1520], [800, 1570], [960, 1575]] as Pt[]).map((p, i) => <Daisy key={i} f={f} x={p[0]} y={p[1]} r={32} at={2150 + 5 * i} i={i} stem={90} />)}
    {([[120, 1800], [330, 1860], [560, 1820], [790, 1870], [980, 1810]] as Pt[]).map((p, i) => keep(i) && <Daisy key={`b${i}`} f={f} x={p[0]} y={p[1]} r={36} at={2202 + 6 * i} i={i + 1} />)}
    <Gull f={f} pos={gullArc([-40, 180], [350, 70], [800, 150], 2060, 2250)} kind="tick" s={0.9} />
    {keep(1) && <Gull f={f} pos={gullArc([1120, 260], [800, 120], [450, 220], 2090, 2250)} kind="tick" s={0.8} />}
  </>
);

const S16 = (f: number) => (
  <>
    <Rays f={f} o={[535, 500]} angles={[209, 218, 227, 243, 277, 289, 302, 331]} r0={180} r1={760} a={2230} b={2256} />
    <Gull f={f} pos={gullArc([-40, 330], [500, 250], [1120, 400], 2256, 2400)} kind="tick" />
    {keep(1) && <Gull f={f} pos={gullArc([1120, 410], [500, 330], [-40, 300], 2275, 2409)} kind="tick" s={0.8} />}
    <TongueRing f={f} cx={581} cy={1690} rx={135} ry={60} size={40} at={2366} pulses={[2366]} warm={1} />
    {[0, 1, 2].map((i) => <Coal key={i} f={f} x={[455, 581, 690][i]} y={[1810, 1830, 1822][i]} at={2262 + 10 * i} s0="cold" lightAt={[2330, 2344, 2358][i]} />)}
    <LowSparks f={f} box={{ x1: 540, y1: 1500, x2: 630, y2: 1610 }} from={2256} size={24} />
  </>
);

const S17 = (f: number) => {
  const xs = [416, 542, 697], ys = [1470, 1462, 1470];
  return (
    <>
      <TongueRing f={f} cx={542} cy={1640} rx={455} ry={215} size={92} at={2409} pulses={[2409]} yieldAt={2452} yieldK={[11, 0, 1]} />
      <LowSparks f={f} box={{ x1: 380, y1: 1470, x2: 700, y2: 1560 }} from={2409} size={28} />
      {[0, 1, 2].map((i) => <Coal key={i} f={f} x={xs[i]} y={ys[i]} at={2456 + 8 * i} s0="lit" swellAt={2502 + 14 * i} />)}
      <Gull f={f} pos={(ff) => [630 + 12 * Math.sin(ff / 40), 560 + 8 * Math.sin(ff / 31)]} kind="tick" s={0.9} />
      {keep(1) && <Gull f={f} pos={(ff) => [655 + 10 * Math.sin(ff / 35 + 1), 650 + 8 * Math.sin(ff / 27)]} kind="tick" s={0.8} />}
    </>
  );
};

const LAYERS: ((f: number) => React.ReactNode)[] = [S01, S02, S03, S04, S05, S06, S07, S08, S09, S10, S11, S12, S13, S14, S15, S16, S17];

// ---------- shell ----------
const Defs: React.FC = () => (
  <svg width={0} height={0} style={{ position: "absolute" }}>
    <defs>
      <filter id="riso" filterUnits="userSpaceOnUse" x={-200} y={-200} width={1480} height={2320} colorInterpolationFilters="sRGB">
        <feTurbulence type="fractalNoise" baseFrequency={0.9} numOctaves={1} seed={9} result="g" />
        <feColorMatrix in="g" type="matrix" values="0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  -16 0 0 0 11.4" result="holes" />
        <feComposite in="SourceGraphic" in2="holes" operator="in" />
      </filter>
    </defs>
  </svg>
);

const Shot: React.FC<{ i: number; f: number }> = ({ i, f }) => {
  const S = shotStart(i), E = shotEnd(i);
  const t = TR[i];
  let style: React.CSSProperties = {};
  const p = trP(i, f);
  if (t && p >= 0) {
    let m = "";
    if (t.k === "iris") {
      const R = irisR(p), w0 = CUT[i] - t.a;
      m = dataUri(`<svg xmlns='http://www.w3.org/2000/svg' width='1080' height='1920'><polygon points='${irisPts(t.o!, R, WROT(f, w0))}' fill='white'/></svg>`);
    } else if (t.k === "ray") m = rayMask(t.o!, p);
    else m = waveMask(p, f, CUT[i] - t.a);
    style = { WebkitMaskImage: m, maskImage: m, WebkitMaskSize: "1080px 1920px", maskSize: "1080px 1920px" } as React.CSSProperties;
  }
  const cam = camAt(i, (f - S) / 30);
  return (
    <Sequence from={S} durationInFrames={E - S} layout="none">
      <AbsoluteFill style={style}>
        <OffthreadVideo src={staticFile(CLIPS[i])} muted style={{ width: 1080, height: 1920, objectFit: "cover" }} />
        <div style={{ ...FULL, transformOrigin: "0 0", transform: `translate(${cam.tx}px, ${cam.ty}px) scale(${cam.s})` }}>
          <svg style={FULL} width={1080} height={1920}><g filter="url(#riso)">{LAYERS[i](f)}</g></svg>
        </div>
      </AbsoluteFill>
    </Sequence>
  );
};

const wedgeCol = [C.coral, C.mustard, C.mid];
const Edges: React.FC<{ f: number }> = ({ f }) => {
  for (const [ks, t] of Object.entries(TR)) {
    const i = Number(ks), p = trP(i, f);
    if (p < 0) continue;
    const w0 = CUT[i] - t.a;
    if (t.k === "ray") {
      const e = SINE(p);
      const w = rayWedges(t.o!, e, e, Math.min(1, e + 0.35));
      return <svg style={FULL} width={1080} height={1920}><g filter="url(#riso)">{w.map((q) => <path key={q.k} d={q.d} fill={wedgeCol[q.k % 3]} />)}</g></svg>;
    }
    if (t.k === "iris") {
      const R = irisR(p), rot = WROT(f, w0), o = t.o!;
      const op = Math.min(1, Math.max(0, (1500 - R) / 400));
      if (op <= 0) return null;
      return (
        <svg style={FULL} width={1080} height={1920}>
          {t.low && <clipPath id="lowhalf"><rect x={-200} y={t.o![1]} width={1480} height={1400} /></clipPath>}
          <g filter="url(#riso)" opacity={op} clipPath={t.low ? "url(#lowhalf)" : undefined}>
            <polygon points={irisPts(o, R, rot)} fill="none" stroke={C.orange} strokeWidth={26} strokeLinejoin="round" />
            <polygon points={irisPts(o, Math.max(1, R - 20), rot)} fill="none" stroke={C.mustard} strokeWidth={14} strokeLinejoin="round" />
            <polygon points={irisPts(o, Math.max(1, R - 34), rot)} fill="none" stroke={C.cream} strokeWidth={6} strokeLinejoin="round" />
            {Array.from({ length: 10 }, (_, k) => {
              const th = rad(k * 36) + rot * 0.6;
              return <Flame1 key={k} x={o[0] + (R + 44) * Math.cos(th)} y={o[1] + (R + 44) * Math.sin(th)} h={48} rot={(th * 180) / Math.PI + 90} />;
            })}
          </g>
        </svg>
      );
    }
    // wave
    const { Y, ph1, ph2 } = waveGeo(p, f, w0);
    const poly = (top: number, bot: number, ph: number, pb: number) => {
      const a: string[] = [], b: string[] = [];
      for (let x = -20; x <= 1100; x += 20) { a.push(`${x},${waveY(x, Y + top, ph).toFixed(1)}`); b.push(`${x},${waveY(x, Y + bot, pb).toFixed(1)}`); }
      return `${a.join(" ")} ${b.reverse().join(" ")}`;
    };
    const cols = t.night ? { b1: "#2E6F73", b2: "#173F45", foam: C.star } : { b1: "#3F8F8C", b2: "#2E6F73", foam: C.cream };
    let foam = "";
    for (let x = -60; x < 1140; x += 60) foam += `${x === -60 ? "M" : "L"} ${x} ${waveY(x, Y, ph1).toFixed(1)} Q ${x + 30} ${(waveY(x + 30, Y, ph1) - 46).toFixed(1)} ${x + 60} ${waveY(x + 60, Y, ph1).toFixed(1)} `;
    return (
      <svg style={FULL} width={1080} height={1920}>
        <g filter="url(#riso)">
          <polygon points={poly(50, 126, ph2, ph2)} fill={cols.b2} />
          <polygon points={poly(0, 70, ph1, ph1)} fill={cols.b1} />
          <path d={foam} fill="none" stroke={cols.foam} strokeWidth={10} strokeLinecap="round" strokeLinejoin="round" />
        </g>
      </svg>
    );
  }
  return null;
};

export const SecondFireV1: React.FC<SFProps> = ({ DENSITY }) => {
  DENS = DENSITY ?? 1;
  const f = useCurrentFrame();
  return (
    <AbsoluteFill style={{ background: C.night }}>
      <Defs />
      {Array.from({ length: 17 }, (_, i) => (
        <Shot key={i} i={i} f={f} />
      ))}
      <Edges f={f} />
    </AbsoluteFill>
  );
};
