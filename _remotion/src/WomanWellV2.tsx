// Woman at the well (Pop Halftone) - motion layer v2 "LIVING WATER TAKES THE PAGE".
// Spec: poc_pop_halftone/woman_at_well/motion_v2/MOTION_DESIGN_v2.md  ($0, pure code)
// Layer stack: Base video / BACK (sky graphics, face-guarded) / InkTop (same video, SVG ink-key: only grey pixels) /
// FRONT (stickers, type) / TRANS / FRAME. All frames ABSOLUTE at 30 fps. No Math.random.
import React from "react";
import { AbsoluteFill, Easing, OffthreadVideo, Sequence, delayRender, continueRender, interpolate, staticFile, useCurrentFrame } from "remotion";

export const W2_FPS = 30;
export const W2_FRAMES = 2636;

// ---------- palette ----------
const K = "#111111", W = "#FFFFFF", PAPER = "#F4EFE4", TEAL = "#14B8C4", DEEP = "#0A7C8C", AQUA = "#7FE3E8";
const YEL = "#FFD60A", ORG = "#F55700", RED = "#EE0C00", GOLD = "#FFE89A";

// ---------- math ----------
type Pt = [number, number];
const clampO = { extrapolateLeft: "clamp", extrapolateRight: "clamp" } as const;
const lerp = (f: number, a: number, b: number, from: number, to: number, easing?: (t: number) => number) =>
  interpolate(f, [a, b], [from, to], { ...clampO, easing });
const OUT = Easing.out(Easing.cubic);
const INOUT = Easing.inOut(Easing.cubic);
const SINE = Easing.inOut(Easing.sin);
const BACKE = Easing.out(Easing.back(1.8));
const pop = (f: number, at: number) => interpolate(f, [at, at + 8], [0, 1], { ...clampO, easing: BACKE });
const well = (f: number, at: number, d = 40) => lerp(f, at, at + d, 0, 1, SINE);
const rad = (d: number) => (d * Math.PI) / 180;
const clamp01 = (v: number) => Math.max(0, Math.min(1, v));
const hash = (i: number) => { const x = Math.sin(i * 127.1 + 311.7) * 43758.5453; return x - Math.floor(x); };
const FULL: React.CSSProperties = { position: "absolute", left: 0, top: 0, width: 1080, height: 1920, overflow: "visible" };
const dataUri = (svg: string) => `url("data:image/svg+xml,${encodeURIComponent(svg)}")`;

const posOn = (P: Pt[], u: number): Pt => {
  const n = P.length - 1;
  if (u >= 1) return P[n];
  const t = Math.max(0, u) * n, i = Math.floor(t), k = t - i;
  const p0 = P[Math.max(0, i - 1)], p1 = P[i], p2 = P[i + 1], p3 = P[Math.min(n, i + 2)];
  const c = (a: number, b: number, c2: number, d: number) =>
    0.5 * (2 * b + (-a + c2) * k + (2 * a - 5 * b + 4 * c2 - d) * k * k + (-a + 3 * b - 3 * c2 + d) * k * k * k);
  return [c(p0[0], p1[0], p2[0], p3[0]), c(p0[1], p1[1], p2[1], p3[1])];
};

// ---------- timeline ----------
const CUT = [0, 132, 240, 348, 434, 568, 683, 801, 981, 1125, 1341, 1463, 1569, 1654, 1738, 1978, 2128, 2264, 2445, 2636];
const shotOf = (f: number) => Math.max(0, CUT.findIndex((c, k) => f >= c && f < CUT[k + 1]));

// face guards: [cx, cy, rx, ry] ellipses, or [x, y, w, h, "r"] rects
type G = [number, number, number, number] | [number, number, number, number, "r"];
const GUARD: G[][] = [
  [], // c01
  [[535, 810, 105, 120]],
  [[390, 810, 130, 150]],
  [[205, 800, 135, 150], [850, 775, 120, 135]],
  [[620, 715, 190, 235]],
  [[325, 1040, 90, 100], [880, 945, 90, 100]],
  [[355, 760, 165, 190]],
  [], // c08
  [[665, 975, 235, 325]],
  [[195, 895, 135, 150], [765, 935, 140, 160]],
  [[285, 1010, 115, 125]],
  [[540, 640, 210, 310]],
  [[510, 1080, 190, 250]],
  [[540, 790, 90, 125]],
  [[580, 945, 100, 105], [95, 1065, 80, 90], [285, 960, 80, 90], [930, 1065, 80, 90]],
  [[0, 1130, 1080, 330, "r"]],
  [], // c17
  [[370, 935, 130, 145], [80, 970, 80, 90], [650, 1080, 80, 90], [810, 1080, 85, 95], [1010, 945, 80, 90]],
  [], // c19
];

// ---------- text measure ----------
let _ctx: CanvasRenderingContext2D | null = null;
const tw = (t: string, size: number) => {
  if (!_ctx) _ctx = document.createElement("canvas").getContext("2d");
  _ctx!.font = `${size}px Bangers`;
  return _ctx!.measureText(t).width + 4 * t.length;
};

// ---------- hex dot helper ----------
const hexDots = (p: number, fn: (x: number, y: number, key: string) => React.ReactNode, pad = 1, yOff = 0, y0 = 0, y1 = 1920) => {
  const out: React.ReactNode[] = [];
  const rh = p * 0.866;
  for (let iy = Math.floor((y0 - yOff) / rh) - pad; iy * rh + yOff < y1 + pad * rh; iy++) {
    for (let ix = -pad; ix * p < 1080 + p * pad; ix++) {
      const x = ix * p + (((iy % 2) + 2) % 2 ? p / 2 : 0), y = iy * rh + yOff;
      const n = fn(x, y, `${ix}_${iy}`);
      if (n) out.push(n);
    }
  }
  return out;
};

// ---------- parts ----------
const DROP_U = "M 0 -1 C 0.2 -0.6 0.7 -0.2 0.7 0.3 A 0.7 0.7 0 0 1 -0.7 0.3 C -0.7 -0.2 -0.2 -0.6 0 -1 Z";
const dropD = (cx: number, cy: number, s: number) => {
  const X = (v: number) => (cx + v * s).toFixed(1), Y = (v: number) => (cy + v * s).toFixed(1), R = (v: number) => (v * s).toFixed(1);
  return `M ${X(0)} ${Y(-1)} C ${X(0.2)} ${Y(-0.6)} ${X(0.7)} ${Y(-0.2)} ${X(0.7)} ${Y(0.3)} A ${R(0.7)} ${R(0.7)} 0 0 1 ${X(-0.7)} ${Y(0.3)} C ${X(-0.7)} ${Y(-0.2)} ${X(-0.2)} ${Y(-0.6)} ${X(0)} ${Y(-1)} Z`;
};

type DropP = { f: number; at: number; x: number; y: number; h?: number; mode?: "pop" | "well" | "on"; bob?: boolean; rot?: number; lv?: number; col?: string; out?: number; outD?: number; wd?: number; grow?: [number, number]; draw?: [number, number] };
const Drop: React.FC<DropP> = ({ f, at, x, y, h = 150, mode = "pop", bob = true, rot = 0, lv = 0, col = TEAL, out, outD = 6, wd = 40, grow, draw }) => {
  const OL = h > 250 ? 12 : 9, EDGE = h > 250 ? 6 : 4;
  if (draw) {
    if (f < draw[0]) return null;
    if (f < draw[1]) {
      const p = lerp(f, draw[0], draw[1], 0, 1, OUT), half = h / 2;
      const d = dropD(0, 0, half);
      return (
        <g transform={`translate(${x} ${y}) rotate(${rot})`} fill="none" strokeLinejoin="round">
          <path d={d} pathLength={1} strokeDasharray="1 1" strokeDashoffset={1 - p} stroke={W} strokeWidth={OL + 2 * EDGE} />
          <path d={d} pathLength={1} strokeDasharray="1 1" strokeDashoffset={1 - p} stroke={K} strokeWidth={OL} />
        </g>
      );
    }
    mode = "on";
  }
  if (f < at && mode !== "on") return null;
  let s = mode === "pop" ? pop(f, at) : mode === "well" ? well(f, at, wd) : 1;
  const dy = mode === "well" ? (1 - s) * 26 : 0;
  if (out !== undefined) s *= lerp(f, out, out + outD, 1, 0);
  if (s <= 0.01) return null;
  let bs = 1, by = 0;
  if (bob) { const ph = (2 * Math.PI * f) / 80 + x * 0.013; bs = 1 + 0.03 * Math.sin(ph); by = 6 * Math.sin(ph + 1.3); }
  const hh = (grow ? lerp(f, grow[0], grow[1], 0.12, 1, OUT) : 1) * h;
  const half = hh / 2;
  return (
    <g transform={`translate(${x.toFixed(1)} ${(y + dy + by).toFixed(1)}) rotate(${rot.toFixed(1)}) scale(${(s * bs).toFixed(3)})`}>
      <g transform={`scale(${half})`}>
        <path d={DROP_U} fill="none" stroke={W} strokeWidth={OL + 2 * EDGE} strokeLinejoin="round" vectorEffect="non-scaling-stroke" />
      </g>
      {lv > 0.001 && (
        <g transform={`translate(5 5) scale(${half})`}>
          <g clipPath="url(#dropClip)"><rect x={-1} y={1 - 2 * lv} width={2} height={2 * lv + 0.02} fill={col} /></g>
        </g>
      )}
      <g transform={`scale(${half})`}>
        <path d={DROP_U} fill="none" stroke={K} strokeWidth={OL} strokeLinejoin="round" vectorEffect="non-scaling-stroke" />
      </g>
    </g>
  );
};

/** sticker tick: W 46 / K 36 / colour 20, boils (length +-6% every 3 frames) */
const Tick: React.FC<{ f: number; at: number; x: number; y: number; ang: number; len: number; col?: string; out?: number }> = ({ f, at, x, y, ang, len, col = YEL, out }) => {
  let p = pop(f, at);
  if (out !== undefined) p *= lerp(f, out, out + 6, 1, 0);
  if (p <= 0.02) return null;
  const boil = 1 + 0.06 * (Math.floor(f / 3) % 2 ? 1 : -1);
  const L = len * p * boil;
  const x2 = x + Math.cos(rad(ang)) * L, y2 = y + Math.sin(rad(ang)) * L;
  return (
    <g strokeLinecap="round">
      <line x1={x} y1={y} x2={x2} y2={y2} stroke={W} strokeWidth={46} />
      <line x1={x} y1={y} x2={x2} y2={y2} stroke={K} strokeWidth={36} />
      <line x1={x} y1={y} x2={x2} y2={y2} stroke={col} strokeWidth={20} />
    </g>
  );
};
const JarTicks: React.FC<{ f: number; at: number; cx: number; cy: number; angles?: number[]; lens?: number[]; out?: number; rin?: number }> = ({
  f, at, cx, cy, angles = [-165, -140, -115, -90, -65, -40, -15], lens = [200, 230, 240, 220, 240, 230, 200], out, rin = 80,
}) => (
  <>
    {angles.map((a, i) => (
      <Tick key={i} f={f} at={at + i * 2} x={cx + Math.cos(rad(a)) * rin} y={cy + Math.sin(rad(a)) * rin} ang={a} len={lens[i % lens.length]} out={out} />
    ))}
  </>
);

const Puff: React.FC<{ f: number; at: number; x: number; y: number; r: number }> = ({ f, at, x, y, r }) => {
  const s = pop(f, at) * lerp(f, at + 12, at + 22, 1, 0);
  if (s <= 0.02) return null;
  const C: [number, number, number][] = [[0, 0, r], [-0.7 * r, 0.2 * r, 0.7 * r], [0.7 * r, 0.15 * r, 0.75 * r], [0.05 * r, -0.55 * r, 0.7 * r]];
  return (
    <g transform={`translate(${x} ${y}) scale(${s})`}>
      {C.map((c, i) => <circle key={`a${i}`} cx={c[0]} cy={c[1]} r={c[2]} fill={W} stroke={W} strokeWidth={17} />)}
      {C.map((c, i) => <circle key={`b${i}`} cx={c[0]} cy={c[1]} r={c[2]} fill={W} stroke={K} strokeWidth={9} />)}
      {C.map((c, i) => <circle key={`c${i}`} cx={c[0]} cy={c[1]} r={c[2] - 4} fill={W} />)}
    </g>
  );
};

const Rays: React.FC<{ f: number; o: Pt; angles: number[]; r0: number; r1: number; a: number; b: number; sk?: number; sw?: number }> = ({ f, o, angles, r0, r1, a, b, sk = 30, sw = 19 }) => {
  if (f < a) return null;
  const n = angles.length, dur = Math.max(10, (b - a) / 2);
  return (
    <>
      {angles.map((ang, k) => {
        const s = a + ((b - a - dur) * k) / Math.max(1, n - 1);
        const p = lerp(f, s, s + dur, 0, 1, OUT);
        if (p <= 0) return null;
        const cs = Math.cos(rad(ang)), sn = Math.sin(rad(ang)), rr = r0 + (r1 - r0) * p;
        const common = { x1: o[0] + r0 * cs, y1: o[1] + r0 * sn, x2: o[0] + rr * cs, y2: o[1] + rr * sn, strokeLinecap: "round" as const, strokeDasharray: "0.01 44", strokeDashoffset: -Math.max(0, f - b) * 0.4 };
        return (
          <g key={k}>
            <line {...common} stroke={K} strokeWidth={sk} />
            <line {...common} stroke={W} strokeWidth={sw} />
          </g>
        );
      })}
    </>
  );
};

const starPts = (cx: number, cy: number, R: number, r: number, n = 14, rot = 0) => {
  const p: string[] = [];
  for (let i = 0; i < n * 2; i++) {
    const a = rad(rot - 90 + (i * 180) / n), rr = i % 2 ? r : R;
    p.push(`${(cx + rr * Math.cos(a)).toFixed(1)},${(cy + rr * Math.sin(a)).toFixed(1)}`);
  }
  return p.join(" ");
};
const WhyStar: React.FC<{ f: number; at: number; cx: number; cy: number; swell: [number, number] }> = ({ f, at, cx, cy, swell }) => {
  const pp = pop(f, at);
  if (pp <= 0.01) return null;
  const rock = 2 * Math.sin(Math.PI * lerp(f, at + 8, at + 20, 0, 1));
  const sw = Math.exp(lerp(f, swell[0], swell[1], 0, Math.log(13), Easing.in(Easing.quad)));
  const k = pp * sw;
  return (
    <g transform={`translate(${cx} ${cy}) rotate(${rock}) scale(${k}) translate(${-cx} ${-cy})`}>
      <polygon points={starPts(cx, cy, 330, 210)} fill="none" stroke={W} strokeWidth={21} strokeLinejoin="round" vectorEffect="non-scaling-stroke" />
      <polygon points={starPts(cx + 6, cy + 6, 330, 210)} fill={K} />
      <polygon points={starPts(cx, cy, 330, 210)} fill={YEL} stroke={K} strokeWidth={12} strokeLinejoin="round" vectorEffect="non-scaling-stroke" />
      <text x={cx} y={cy + 82} textAnchor="middle" fontFamily="Bangers" fontSize={230} fill={K} stroke={W} strokeWidth={10} paintOrder="stroke" letterSpacing={4}>WHY?</text>
    </g>
  );
};

const Flower: React.FC<{ f: number; at: number; x: number; y: number; r: number; i: number }> = ({ f, at, x, y, r, i }) => {
  const g = lerp(f, at, at + 36, 0, 1, SINE);
  if (g <= 0.01) return null;
  const sway = 2.5 * Math.sin((2 * Math.PI * f) / 90 + i);
  const stem = 70 * g;
  return (
    <g>
      <path d={`M ${x} ${y + stem + 10} L ${x} ${y}`} stroke={W} strokeWidth={17} strokeLinecap="round" />
      <path d={`M ${x} ${y + stem + 10} L ${x} ${y}`} stroke={K} strokeWidth={9} strokeLinecap="round" />
      <g transform={`translate(${x} ${y}) rotate(${sway}) scale(${g})`}>
        {[0, 1, 2, 3, 4].map((k) => <ellipse key={`a${k}`} cx={0} cy={-r * 0.62} rx={r * 0.36} ry={r * 0.52} transform={`rotate(${k * 72})`} fill={W} stroke={W} strokeWidth={17} />)}
        {[0, 1, 2, 3, 4].map((k) => <ellipse key={`b${k}`} cx={0} cy={-r * 0.62} rx={r * 0.36} ry={r * 0.52} transform={`rotate(${k * 72})`} fill={W} stroke={K} strokeWidth={7} />)}
        {[0, 1, 2, 3, 4].map((k) => <ellipse key={`c${k}`} cx={0} cy={-r * 0.62} rx={r * 0.36 - 4} ry={r * 0.52 - 4} transform={`rotate(${k * 72})`} fill={W} />)}
        <circle r={r * 0.28} fill={YEL} stroke={K} strokeWidth={7} />
      </g>
    </g>
  );
};

const Rise: React.FC<{ f: number; P: Pt[]; L: number; D: number; h?: number }> = ({ f, P, L, D, h = 190 }) => {
  if (f < L) return null;
  const end = P[P.length - 1];
  if (f >= L + D) return <Drop f={f} at={0} x={end[0]} y={end[1]} h={h} mode="on" lv={1} col={TEAL} />;
  const u = lerp(f, L, L + D, 0, 1, Easing.out(Easing.quad));
  const [x, y] = posOn(P, u);
  const [xa, ya] = posOn(P, Math.min(1, u + 0.03)), [xb, yb] = posOn(P, Math.max(0, u - 0.03));
  const rot = Math.max(-14, Math.min(14, (Math.atan2(xa - xb, -(ya - yb)) * 180) / Math.PI));
  return <Drop f={f} at={0} x={x} y={y} h={h} rot={rot} mode="on" bob={false} lv={1} col={TEAL} />;
};

// ---------- D5 water kit ----------
const Crown: React.FC<{ f: number; at: number; x: number; y: number; w?: number; col?: string }> = ({ f, at, x, y, w = 300, col = W }) => {
  const age = f - at, u = age / 12;
  if (u < 0 || u >= 1) return null;
  const e = OUT(u);
  return (
    <g>
      {age < 6 && (
        <ellipse cx={x} cy={y} rx={0.5 * w * Math.min(1, (age + 1) / 3)} ry={0.12 * w * Math.min(1, (age + 1) / 3)} fill={W} stroke={K} strokeWidth={10} />
      )}
      {[-60, -30, 0, 30, 60].map((a, i) => (
        <Drop key={i} f={f} at={0} x={x + Math.sin(rad(a)) * 0.5 * w * e} y={y - Math.cos(rad(a)) * 0.5 * w * e * 0.9} h={0.42 * w * (1 - 0.7 * u)} rot={a} mode="on" bob={false} lv={1} col={col} />
      ))}
    </g>
  );
};
const Ripple: React.FC<{ f: number; at: number; C: Pt; r0: number; r1: number; col?: string; d?: number }> = ({ f, at, C, r0, r1, col = W, d = 24 }) => {
  if (f < at || f >= at + d) return null;
  const r = lerp(f, at, at + d, r0, r1, OUT);
  const k = f < at + d - 6 ? 1 : lerp(f, at + d - 6, at + d, 1, 0);
  if (k <= 0.02) return null;
  return (
    <g fill="none">
      <circle cx={C[0]} cy={C[1]} r={r} stroke={K} strokeWidth={28 * k} />
      <circle cx={C[0]} cy={C[1]} r={r} stroke={col} strokeWidth={16 * k} />
    </g>
  );
};
const TealDots: React.FC<{ maxDist?: number; C?: Pt }> = ({ maxDist, C = [540, 1080] }) => (
  <>
    {hexDots(46, (x, y, k) => {
      if (maxDist !== undefined && Math.hypot(x - C[0], y - C[1]) > maxDist) return null;
      return <circle key={k} cx={x} cy={y} r={9} fill={DEEP} />;
    })}
  </>
);
const Flood: React.FC<{ f: number; C: Pt; a: number; b: number }> = ({ f, C, a, b }) => {
  if (f < a) return null;
  const r = lerp(f, a, b, 330, 2300, Easing.in(Easing.quad));
  const pts: string[] = [];
  for (let i = 0; i < 144; i++) {
    const th = (i / 144) * 2 * Math.PI, rr = r * (1 + 0.045 * Math.sin(18 * th + f * 0.5));
    pts.push(`${(C[0] + rr * Math.cos(th)).toFixed(1)} ${(C[1] + rr * Math.sin(th)).toFixed(1)}`);
  }
  const d = "M " + pts.join(" L ") + " Z";
  return (
    <g>
      <clipPath id="floodClip"><path d={d} /></clipPath>
      <path d={d} fill={TEAL} />
      <g clipPath="url(#floodClip)">
        <circle cx={C[0]} cy={C[1]} r={0.9 * r} fill="none" stroke={AQUA} strokeWidth={22} />
        <TealDots maxDist={0.7 * r} C={C} />
      </g>
      <path d={d} fill="none" stroke={K} strokeWidth={14} strokeLinejoin="round" />
    </g>
  );
};
const waveY = (f: number, x: number, yTop: number, sa: number, sb: number) => yTop + 34 * Math.sin(x / 170 + f * sa) + 16 * Math.sin(x / 61 - f * sb);
const WaveBody: React.FC<{ f: number; yTop: number; col?: string; op?: number; sa?: number; sb?: number; bare?: boolean }> = ({ f, yTop, col = TEAL, op = 1, sa = 0.16, sb = 0.23, bare = false }) => {
  const xs: number[] = [];
  for (let x = -30; x <= 1110; x += 30) xs.push(x);
  const top = xs.map((x) => [x, waveY(f, x, yTop, sa, sb)] as Pt);
  const body = `M -30 2000 L ` + top.map((p) => `${p[0]} ${p[1].toFixed(1)}`).join(" L ") + ` L 1110 2000 Z`;
  const edge = "M " + top.map((p) => `${p[0]} ${p[1].toFixed(1)}`).join(" L ");
  const low = "M " + top.map((p) => `${p[0]} ${(p[1] + 30).toFixed(1)}`).join(" L ");
  const thr = yTop + 0.6 * (1960 - yTop);
  if (bare) return <g opacity={op}><path d={body} fill={col} /></g>;
  return (
    <g opacity={op}>
      <clipPath id={`wbc${Math.round(yTop)}`}><path d={body} /></clipPath>
      <path d={body} fill={col} />
      <path d={low} fill="none" stroke={W} strokeWidth={8} strokeLinejoin="round" />
      <g clipPath={`url(#wbc${Math.round(yTop)})`}>
        {hexDots(46, (x, y, k) => (y > thr && y > waveY(f, x, yTop, sa, sb) + 45 ? <circle key={k} cx={x} cy={y} r={8} fill={DEEP} /> : null), 1, 0, Math.max(0, thr - 50), 1960)}
      </g>
      <path d={edge} fill="none" stroke={K} strokeWidth={12} strokeLinejoin="round" />
    </g>
  );
};
const Stream: React.FC<{ f: number; lane: number; a: number }> = ({ f, lane, a }) => {
  const out: React.ReactNode[] = [];
  const k1 = Math.floor((f - a) / 12), k0 = Math.max(0, Math.floor((f - a - 170) / 12));
  for (let k = k0; k <= k1; k++) {
    const age = f - (a + 12 * k), y = 2040 - 13 * age;
    if (y < -140 || age < 0) continue;
    out.push(<Drop key={k} f={f} at={0} x={lane + 22 * Math.sin(y / 140 + k)} y={y} h={190} mode="on" bob={false} lv={1} col={TEAL} />);
  }
  return <>{out}</>;
};

// ---------- D6 speed lines ----------
const SpeedLines: React.FC<{ f: number; F: Pt; n?: number; r0: number; boil?: boolean }> = ({ f, F, n = 46, r0, boil = true }) => {
  const sOff = boil ? (Math.floor(f / 3) % 2) * 1000 : 0;
  const out: React.ReactNode[] = [];
  for (let i = 0; i < n; i++) {
    const ang = rad((360 * i) / n + (hash(i + sOff) - 0.5) * 8);
    const bw = 10 + hash(i + 50 + sOff) * 30, tipR = r0 + hash(i + 20 + sOff) * 160;
    const c = Math.cos(ang), s = Math.sin(ang);
    const tip: Pt = [F[0] + tipR * c, F[1] + tipR * s];
    const bx = F[0] + 2400 * c, by = F[1] + 2400 * s;
    out.push(<polygon key={i} points={`${tip[0].toFixed(1)},${tip[1].toFixed(1)} ${(bx - s * bw / 2).toFixed(1)},${(by + c * bw / 2).toFixed(1)} ${(bx + s * bw / 2).toFixed(1)},${(by - c * bw / 2).toFixed(1)}`} fill={K} />);
  }
  return <>{out}</>;
};

// ---------- D2 ray swap ----------
const WEDGE_W = [26, 18, 30, 20, 14, 28, 22, 24, 16, 30, 20, 26, 18, 22, 28, 18];
const PALS: Record<string, string[]> = {
  NOON: [YEL, W, YEL, "#FFF3A0"], DRY: [PAPER, W], WATER: [TEAL, DEEP, TEAL, AQUA, TEAL, W], LEFT: [YEL, ORG, W], RIGHT: [RED, K, ORG], DAWN: [GOLD, W, YEL], WHITE: [W],
};
const wedgePath = (o: Pt, a0: number, a1: number, R = 2600) => {
  a1 += 0.5;
  const x0 = o[0] + R * Math.cos(rad(a0)), y0 = o[1] + R * Math.sin(rad(a0)), x1 = o[0] + R * Math.cos(rad(a1)), y1 = o[1] + R * Math.sin(rad(a1));
  return `M ${o[0]} ${o[1]} L ${x0.toFixed(1)} ${y0.toFixed(1)} A ${R} ${R} 0 0 1 ${x1.toFixed(1)} ${y1.toFixed(1)} Z`;
};
type Rev = { t: "snap"; a: number } | { t: "sweep"; a: number; b: number } | { t: "iris"; a: number; b: number; R: number } | { t: "front"; a: number; b: number; dir: "down" | "up" } | { t: "pulse"; at: number };
const RaySwap: React.FC<{ f: number; id: string; O: Pt; pal: string; spin?: number; t0?: number; rev: Rev; op?: number; clip?: React.ReactNode }> = ({ f, id, O, pal, spin = 0, t0 = 0, rev, op = 1, clip }) => {
  let revClip: React.ReactNode = null;
  let extra: React.ReactNode = null;
  if (rev.t === "snap" && f < rev.a) return null;
  if (rev.t === "pulse" && !(f >= rev.at && f < rev.at + 4)) return null;
  if (rev.t === "sweep") {
    if (f < rev.a) return null;
    const p = lerp(f, rev.a, rev.b, 0, 1, OUT);
    if (p < 0.999) {
      const sw = 360 * p, R = 3200;
      const ea = rad(180 + sw);
      revClip = <path d={`M ${O[0]} ${O[1]} L ${O[0] - R} ${O[1]} A ${R} ${R} 0 ${sw > 180 ? 1 : 0} 1 ${(O[0] + R * Math.cos(ea)).toFixed(1)} ${(O[1] + R * Math.sin(ea)).toFixed(1)} Z`} />;
    }
  }
  if (rev.t === "iris") {
    if (f < rev.a) return null;
    const r = rev.R * SINE(lerp(f, rev.a, rev.b, 0, 1));
    if (r < 1) return null;
    revClip = <circle cx={O[0]} cy={O[1]} r={r} />;
  }
  if (rev.t === "front") {
    if (f < rev.a) return null;
    const p = lerp(f, rev.a, rev.b, 0, 1), ye = p * (1920 + 80) - 20;
    if (rev.dir === "down") {
      revClip = <rect x={0} y={0} width={1080} height={Math.max(0.1, ye)} />;
      if (p < 1) extra = (
        <g fill={K}>
          {hexDots(34, (x, y, k) => (Math.abs(y - (ye + 10)) < 20 ? <circle key={k} cx={x} cy={y} r={y < ye + 10 ? 9 : 6} /> : null), 1, 0, ye - 40, ye + 60)}
        </g>
      );
    } else revClip = <rect x={0} y={1920 - ye} width={1080} height={Math.max(0.1, ye)} />;
  }
  const ang0 = spin * (f - t0);
  const cols = PALS[pal];
  const wedges: React.ReactNode[] = [];
  const paperWedges: React.ReactNode[] = [];
  let a = ang0;
  WEDGE_W.forEach((w, i) => {
    const c = cols[i % cols.length];
    const d = wedgePath(O, a, a + w);
    wedges.push(<path key={i} d={d} fill={c} />);
    if (pal === "DRY" && c === PAPER) paperWedges.push(<path key={`p${i}`} d={d} fill="url(#dryDots)" />);
    a += w;
  });
  const body = (
    <g>
      {wedges}
      {paperWedges}
    </g>
  );
  const withRev = revClip ? <g clipPath={`url(#${id}r)`}>{body}</g> : body;
  const withClip = clip ? <g clipPath={`url(#${id}c)`}>{withRev}</g> : withRev;
  return (
    <g opacity={op}>
      <defs>
        {revClip && <clipPath id={`${id}r`}>{revClip}</clipPath>}
        {clip && <clipPath id={`${id}c`}>{clip}</clipPath>}
      </defs>
      {withClip}
      {extra}
    </g>
  );
};

// ---------- D3 dot fields ----------
const projRange = (ang: number): [number, number] => {
  const c = Math.cos(rad(ang)), s = Math.sin(rad(ang));
  const v = [0, 1080 * c, 1920 * s, 1080 * c + 1920 * s];
  return [Math.min(...v), Math.max(...v)];
};
/** cut wipe. cover: dots grow behind the front; reveal: dots shrink behind the front. */
const dotWipe = (f: number, a: number, b: number, ang: number, col: string, mode: "cover" | "reveal", p = 54) => {
  const front = lerp(f, a, b, -0.25, 1.25);
  const [mn, mx] = projRange(ang);
  const c = Math.cos(rad(ang)), s = Math.sin(rad(ang));
  const out: React.ReactNode[] = [];
  if (mode === "cover" && front > 1.0) out.push(<rect key="solid" x={0} y={0} width={1080} height={1920} fill={col} />);
  if (mode === "reveal" && front < -0.1) out.push(<rect key="solid" x={0} y={0} width={1080} height={1920} fill={col} />);
  out.push(...hexDots(p, (x, y, k) => {
    const d = (x * c + y * s - mn) / (mx - mn);
    const r = mode === "cover" ? 40 * clamp01((front - d) / 0.22) : 40 * clamp01((d - front) / 0.22);
    return r > 0.5 ? <circle key={k} cx={x} cy={y} r={r} fill={col} /> : null;
  }, 2));
  return <g>{out}</g>;
};
const crawl = (f: number, col: string, r: number, speedY: number, op: number, clipY: number, id: string) => {
  const rh = 64 * 0.866, off = (((speedY * f) % (2 * rh)) + 2 * rh) % (2 * rh);
  return (
    <g opacity={op}>
      <defs><clipPath id={id}><rect x={0} y={0} width={1080} height={clipY} /></clipPath></defs>
      <g clipPath={`url(#${id})`} fill={col}>
        {hexDots(64, (x, y, k) => <circle key={k} cx={x} cy={y} r={r} />, 2, off - 2 * rh, -2 * rh, clipY + 2 * rh)}
      </g>
    </g>
  );
};
const sunDots = (f: number, O: Pt, R: number, col: string) => (
  <g fill={col}>
    {hexDots(54, (x, y, k) => {
      const d = Math.hypot(x - O[0], y - O[1]);
      if (d >= R) return null;
      const r = 22 * (1 - d / R) * (0.8 + 0.2 * Math.sin((2 * Math.PI * f) / 40));
      return r > 0.5 ? <circle key={k} cx={x} cy={y} r={r} /> : null;
    })}
  </g>
);

// ---------- D4 gutter / shutters / bars ----------
const GutterBar: React.FC<{ x: number; y0: number; y1: number }> = ({ x, y0, y1 }) => (
  <g>
    <rect x={x - 32} y={y0} width={10} height={y1 - y0} fill={K} />
    <rect x={x + 22} y={y0} width={10} height={y1 - y0} fill={K} />
    <rect x={x - 22} y={y0} width={44} height={y1 - y0} fill={W} />
  </g>
);
const Shutters = (f: number, a: number, cut: number, b: number, x: number) => {
  if (f < a || f >= b) return null;
  const p = f < cut ? lerp(f, a, cut, 0, 1, Easing.in(Easing.cubic)) : lerp(f, cut, b, 1, 0, OUT);
  const lr = x * p, rl = 1080 - (1080 - x) * p;
  return (
    <g>
      <rect x={-100} y={0} width={lr + 100} height={1920} fill={K} />
      <rect x={lr - 12} y={0} width={12} height={1920} fill={W} />
      <rect x={rl} y={0} width={1180 - rl} height={1920} fill={K} />
      <rect x={rl} y={0} width={12} height={1920} fill={W} />
    </g>
  );
};
const Bars = (f: number, a: number, cut: number, b: number, cols: string[]) => {
  if (f < a || f >= b) return null;
  return (
    <g>
      {[0, 1, 2, 3, 4].map((k) => {
        const R = f < cut ? lerp(f, Math.min(a + 2 * k, cut - 1), cut, -100, 1180) : 1180;
        const L = f < cut ? -100 : lerp(f, cut, cut + 4 + 2 * k, -100, 1180);
        if (R <= L) return null;
        const y = 384 * k;
        return (
          <g key={k}>
            <rect x={L} y={y} width={R - L} height={384} fill={cols[k % cols.length]} />
            <rect x={L} y={y} width={R - L} height={8} fill={K} />
            <rect x={L} y={y + 376} width={R - L} height={8} fill={K} />
          </g>
        );
      })}
    </g>
  );
};

// ---------- D10 type ----------
type Wd = { t: string; at: number; out?: number };
const WordRow: React.FC<{
  f: number; words: Wd[]; size: number; y: number; x?: number; cx?: number; maxW: number; mode: "slam" | "step"; fill: string;
  stroke?: string; sw?: number; shadow?: string; rest?: number; seed?: number;
}> = ({ f, words, size, y, x, cx, maxW, mode, fill, stroke, sw = 14, shadow, rest = 0, seed = 0 }) => {
  let sz = size, gap = 0, widths: number[] = [], total = 0;
  for (let guard = 0; guard < 30; guard++) {
    gap = 0.26 * sz;
    widths = words.map((w) => tw(w.t, sz));
    total = widths.reduce((s, v) => s + v, 0) + gap * (words.length - 1);
    if (total <= maxW) break;
    sz -= 6;
  }
  const x0 = x !== undefined ? x : (cx as number) - total / 2;
  let cur = x0;
  return (
    <>
      {words.map((w, i) => {
        const wx = cur + widths[i] / 2;
        cur += widths[i] + gap;
        if (f < w.at || (w.out !== undefined && f >= w.out)) return null;
        const textProps = { fontFamily: "Bangers", fontSize: sz, textAnchor: "middle" as const, letterSpacing: 4 };
        if (mode === "step") return <text key={i} x={wx} y={y} {...textProps} fill={fill}>{w.t}</text>;
        const p = lerp(f, w.at, w.at + 5, 0, 1, Easing.out(Easing.back(1.6)));
        const sc = 1.7 - 0.7 * p, rot = rest + (hash(seed + i) - 0.5) * 10 * (1 - p);
        const py = y - sz * 0.35;
        return (
          <g key={i} transform={`translate(${wx} ${py}) rotate(${rot}) scale(${sc}) translate(${-wx} ${-py})`}>
            {shadow && <text x={wx + 8} y={y + 8} {...textProps} fill={shadow} stroke={shadow} strokeWidth={stroke ? sw : 0} strokeLinejoin="round">{w.t}</text>}
            <text x={wx} y={y} {...textProps} fill={fill} stroke={stroke} strokeWidth={stroke ? sw : 0} paintOrder="stroke" strokeLinejoin="round">{w.t}</text>
          </g>
        );
      })}
    </>
  );
};
const balloonD = (x0: number, y0: number, x1: number, y1: number, tip: Pt | null) => {
  const r = 60;
  if (!tip) return `M ${x0 + r} ${y0} H ${x1 - r} A ${r} ${r} 0 0 1 ${x1} ${y0 + r} V ${y1 - r} A ${r} ${r} 0 0 1 ${x1 - r} ${y1} H ${x0 + r} A ${r} ${r} 0 0 1 ${x0} ${y1 - r} V ${y0 + r} A ${r} ${r} 0 0 1 ${x0 + r} ${y0} Z`;
  const bx = Math.max(x0 + r + 45, Math.min(x1 - r - 45, tip[0]));
  return `M ${x0 + r} ${y0} H ${x1 - r} A ${r} ${r} 0 0 1 ${x1} ${y0 + r} V ${y1 - r} A ${r} ${r} 0 0 1 ${x1 - r} ${y1} H ${bx + 45} L ${tip[0]} ${tip[1]} L ${bx - 45} ${y1} H ${x0 + r} A ${r} ${r} 0 0 1 ${x0} ${y1 - r} V ${y0 + r} A ${r} ${r} 0 0 1 ${x0 + r} ${y0} Z`;
};
const Balloon: React.FC<{ x0: number; y0: number; x1: number; y1: number; tip: Pt | null; s: number; anchor: Pt }> = ({ x0, y0, x1, y1, tip, s, anchor }) => {
  if (s <= 0.01) return null;
  return (
    <g transform={`translate(${anchor[0]} ${anchor[1]}) scale(${s}) translate(${-anchor[0]} ${-anchor[1]})`}>
      <path d={balloonD(x0, y0, x1, y1, tip)} fill={W} stroke={K} strokeWidth={12} strokeLinejoin="round" />
    </g>
  );
};
const SlabRect: React.FC<{ x0: number; y0: number; x1: number; y1: number; fill: string }> = ({ x0, y0, x1, y1, fill }) => (
  <g>
    <rect x={x0 + 10} y={y0 + 10} width={x1 - x0} height={y1 - y0} rx={22} fill={K} />
    <rect x={x0} y={y0} width={x1 - x0} height={y1 - y0} rx={22} fill={fill} stroke={K} strokeWidth={10} />
  </g>
);

// ---------- shared cross-cut items ----------
const BAL15 = { x0: 110, y0: 210, x1: 970, y1: 450 };
const Balloon15 = (f: number) => {
  if (f < 1738 || f >= 2004) return null;
  let s = well(f, 1738, 12);
  if (f >= 1998) s *= lerp(f, 1998, 2004, 1, 0);
  const tip: Pt | null = f < 1978 ? [590, 800] : null;
  const mw = 860 - 60;
  return (
    <g>
      <Balloon {...BAL15} tip={tip} s={s} anchor={[540, 330]} />
      {s > 0.95 && (
        <>
          <WordRow f={f} size={120} y={375} cx={540} maxW={mw} mode="step" fill={K}
            words={[{ t: "COME,", at: 1739, out: 1905 }, { t: "SEE", at: 1772, out: 1905 }, { t: "A", at: 1789, out: 1905 }, { t: "MAN", at: 1793, out: 1905 }]} />
          <WordRow f={f} size={100} y={320} cx={540} maxW={mw} mode="step" fill={K}
            words={[{ t: "IS", at: 1915, out: 1998 }, { t: "NOT", at: 1951, out: 1998 }, { t: "THIS", at: 1958, out: 1998 }]} />
          <WordRow f={f} size={100} y={420} cx={540} maxW={mw} mode="step" fill={K}
            words={[{ t: "THE", at: 1977, out: 1998 }, { t: "CHRIST?", at: 1979, out: 1998 }]} />
        </>
      )}
    </g>
  );
};
const Ripples15 = (f: number) => (
  <>
    <Ripple f={f} at={1739} C={[580, 945]} r0={130} r1={900} col={TEAL} d={40} />
    <Ripple f={f} at={1749} C={[580, 945]} r0={130} r1={900} col={TEAL} d={40} />
    {[1964, 1970, 1976].map((a) => <Ripple key={a} f={f} at={a} C={[580, 945]} r0={130} r1={1500} col={TEAL} d={30} />)}
  </>
);
const Slab16 = (f: number) => {
  if (f < 2073 || f >= 2158) return null;
  const s = pop(f, 2073), dy = -700 * lerp(f, 2150, 2156, 0, 1, Easing.in(Easing.quad));
  const cx = 540, cy = 400;
  return (
    <g transform={`translate(0 ${dy})`}>
      <g transform={`translate(${cx} ${cy}) scale(${s}) translate(${-cx} ${-cy})`}>
        <SlabRect x0={80} y0={215} x1={1000} y1={585} fill={YEL} />
        <WordRow f={f} size={150} y={375} cx={540} maxW={860} mode="slam" fill={K} seed={30} words={[{ t: "THE", at: 2086 }, { t: "SAVIOUR", at: 2092 }]} />
        <WordRow f={f} size={150} y={530} cx={540} maxW={860} mode="slam" fill={K} seed={40} words={[{ t: "OF", at: 2102 }, { t: "THE", at: 2114 }, { t: "WORLD", at: 2119 }]} />
      </g>
    </g>
  );
};

// ---------- BACK layers (per shot, absolute frames) ----------
const pulses = (f: number, id: string, O: Pt, ats: number[]) =>
  ats.map((a, i) => <RaySwap key={i} f={f} id={`${id}${i}`} O={O} pal="NOON" rev={{ t: "pulse", at: a }} />);
const anyPulse = (f: number, ats: number[]) => ats.some((a) => f >= a && f < a + 4);

const B01 = (f: number) => {
  const p = [10, 22, 34], sl = f >= 112 && f < 132;
  if (!anyPulse(f, p) && !sl) return null;
  return (<>{pulses(f, "b01", [540, 640], p)}{sl && <SpeedLines f={f} F={[600, 420]} n={46} r0={380} />}</>);
};
const B02 = (f: number) => (
  <>
    <RaySwap f={f} id="b02" O={[510, 560]} pal="NOON" spin={0.15} t0={157} rev={{ t: "sweep", a: 139, b: 157 }} />
    {f >= 150 && sunDots(f, [510, 560], 430, ORG)}
  </>
);
const B03 = (f: number) => crawl(f, W, 6, -0.6, 0.6, 260, "c03clip");
const B04 = (f: number) => (anyPulse(f, [351, 360, 376]) ? <>{pulses(f, "b04", [560, 700], [351, 360, 376])}</> : null);
const B05 = (f: number) => <SpeedLines f={f} F={[600, 720]} n={f < 470 ? 54 : 28} r0={560} boil={f < 470} />;
const B06 = (f: number) => {
  if (f < 607 || f >= 678) return null;
  const inner = (
    <>
      <RaySwap f={f} id="b06l" O={[540, 640]} pal="LEFT" rev={{ t: "snap", a: 607 }} clip={<rect x={0} y={0} width={578} height={1920} />} />
      <RaySwap f={f} id="b06r" O={[540, 640]} pal="RIGHT" rev={{ t: "snap", a: 607 }} clip={<rect x={622} y={0} width={458} height={1920} />} />
    </>
  );
  if (f < 665) return inner;
  const r = 2600 * (1 - lerp(f, 665, 678, 0, 1, Easing.inOut(Easing.sin)));
  return (
    <g clipPath="url(#b06iris)">
      <defs><clipPath id="b06iris"><circle cx={760} cy={380} r={Math.max(1, r)} /></clipPath></defs>
      {inner}
    </g>
  );
};
const B07 = (f: number) => (f >= 771 ? <RaySwap f={f} id="b07" O={[700, 900]} pal="DRY" rev={{ t: "front", a: 771, b: 797, dir: "down" }} /> : null);
const B09 = (f: number) => <RaySwap f={f} id="b09" O={[560, 760]} pal="WATER" spin={0.2} t0={981} rev={{ t: "snap", a: 981 }} />;
const B10 = (f: number) => crawl(f, W, 6, -0.5, 0.5, 620, "c10clip");
const B11 = (f: number) => (f >= 1432 ? <RaySwap f={f} id="b11" O={[560, 655]} pal="NOON" rev={{ t: "sweep", a: 1432, b: 1456 }} /> : null);
const B13 = (f: number) => {
  if (f < 1580) return null;
  const y = lerp(f, 1580, 1640, 1150, -80, SINE);
  return (<><WaveBody f={f} yTop={y} col={W} bare sa={0.08} sb={0.11} /><WaveBody f={f} yTop={y} op={0.55} sa={0.08} sb={0.11} /></>);
};
const B14 = (f: number) => (f >= 1700 ? <RaySwap f={f} id="b14" O={[540, 330]} pal="WATER" spin={0.1} t0={1700} rev={{ t: "sweep", a: 1700, b: 1725 }} /> : null);
const B15 = (f: number) => <RaySwap f={f} id="b15" O={[540, 330]} pal="WATER" spin={0.1} t0={1700} rev={{ t: "snap", a: 0 }} />;
const B16 = (f: number) => (
  <>
    <RaySwap f={f} id="b16" O={[540, 675]} pal="WATER" spin={0.15} t0={1978} rev={{ t: "snap", a: 0 }} />
    {f >= 2073 && <SpeedLines f={f} F={[540, 380]} n={40} r0={520} />}
  </>
);
const B17 = (f: number) => (f >= 2255 ? <SpeedLines f={f} F={[600, 380]} n={46} r0={300} /> : null);
const B18 = (f: number) => (
  <>
    {crawl(f, TEAL, 7, -0.6, 0.7, 620, "c18clip")}
    <WaveBody f={f} yTop={1790} op={1} sa={0.08} sb={0.11} />
  </>
);
const B19 = (f: number) => {
  if (f < 2510) return null;
  const rev: Rev = { t: "iris", a: 2510, b: 2570, R: 1500 };
  const clip = <rect x={0} y={0} width={1080} height={860} />;
  return (<><RaySwap f={f} id="b19w" O={[550, 860]} pal="WHITE" rev={rev} clip={clip} /><RaySwap f={f} id="b19" O={[550, 860]} pal="DAWN" spin={0.05} t0={2510} op={0.6} rev={rev} clip={clip} /></>);
};

const BACKS: ((f: number) => React.ReactNode)[] = [B01, B02, B03, B04, B05, B06, B07, () => null, B09, B10, B11, () => null, B13, B14, B15, B16, B17, B18, B19];

// ---------- FRONT layers ----------
const F01 = (f: number) => {
  const land = [10, 22, 34], xs = [612, 628, 598];
  return (
    <>
      {land.map((L, i) => f < L && <Drop key={i} f={f} at={0} x={xs[i]} y={1372 - 46 * (L - f)} h={300} mode="on" bob={false} lv={1} col={W} />)}
      {land.map((L, i) => <Crown key={`c${i}`} f={f} at={L} x={xs[i]} y={1372} w={300} col={W} />)}
      <Drop f={f} at={45} draw={[45, 57]} x={800} y={360} h={420} out={108} outD={4} />
      <JarTicks f={f} at={69} cx={205} cy={1140} out={104} />
      <WhyStar f={f} at={112} cx={600} cy={420} swell={[126, 132]} />
    </>
  );
};
const F04 = (f: number) => {
  const s = pop(f, 348);
  return (
    <>
      <Balloon x0={90} y0={205} x1={900} y1={600} tip={[300, 640]} s={s} anchor={[495, 402]} />
      <WordRow f={f} size={150} y={370} x={150} maxW={750} mode="slam" fill={K} seed={0} words={[{ t: "GIVE", at: 351 }, { t: "ME", at: 360 }]} />
      <WordRow f={f} size={150} y={530} x={150} maxW={750} mode="slam" fill={K} seed={10} words={[{ t: "TO", at: 369 }, { t: "DRINK.", at: 376 }]} />
      <Drop f={f} at={380} x={800} y={440} h={170} rot={f >= 392 && f < 410 ? 12 * Math.sin(2 * Math.PI * lerp(f, 392, 410, 0, 1)) : 0} />
    </>
  );
};
const F05 = (f: number) => (
  <>
    <Tick f={f} at={436} x={150} y={330} ang={-132} len={220} out={500} />
    <Tick f={f} at={440} x={260} y={205} ang={-112} len={220} out={500} />
    <Tick f={f} at={444} x={420} y={135} ang={-92} len={220} out={500} />
    <Drop f={f} at={540} x={910} y={330} h={300} rot={f >= 549 ? 12 * Math.sin(2 * Math.PI * 2 * lerp(f, 549, 566, 0, 1)) : 0} />
  </>
);
const F06 = (f: number) => {
  const gx = 600, land = 607;
  const slam = f < land ? -1920 * (1 - Easing.in(Easing.quad)(lerp(f, land - 5, land, 0, 1))) : 0;
  const sq = f >= land && f < land + 2 ? 0.985 : 1;
  const shatter = f >= 664;
  const age = f - 664;
  const slide = lerp(f, 665, 673, 0, 1, Easing.in(Easing.quad));
  const hopU = lerp(f, 658, 672, 0, 1, INOUT);
  const hx = 430 + 330 * hopU, hy = 380 - 4 * 100 * Math.sin(Math.PI * Math.min(1, hopU)) * 0.5 - 0;
  const hopY = 380 - 200 * Math.sin(Math.PI * hopU);
  return (
    <>
      {f >= land - 5 && f < 681 && (
        <g transform={`translate(0 ${slam}) translate(0 1920) scale(1 ${sq}) translate(0 -1920)`}>
          {!shatter ? <GutterBar x={gx} y0={0} y1={1920} /> : (
            <>
              <g transform={`translate(0 ${-300 * slide})`}><GutterBar x={gx} y0={0} y1={200} /></g>
              <g transform={`translate(0 ${1400 * slide})`}><GutterBar x={gx} y0={560} y1={1920} /></g>
            </>
          )}
        </g>
      )}
      {shatter && age < 14 && [0, 1, 2, 3, 4, 5].map((i) => {
        const vx = (hash(i) - 0.5) * 38, vy = -10 - hash(i + 9) * 14;
        const px = gx + vx * age, py = 230 + 60 * i + vy * age + 0.5 * 2.2 * age * age;
        return (
          <g key={i} transform={`translate(${px} ${py}) rotate(${(hash(i + 3) - 0.5) * 40 * age})`}>
            <rect x={-22} y={-30} width={44} height={60} fill={W} stroke={K} strokeWidth={6} />
          </g>
        );
      })}
      {[0, 1, 2, 3, 4, 5].map((k) => <Tick key={k} f={f} at={land} x={gx} y={1900} ang={-160 + 28 * k} len={150} out={land + 2} />)}
      {f < 658 ? <Drop f={f} at={640} x={430} y={380} h={200} /> : <Drop f={f} at={0} x={hx} y={hopY} h={200} mode="on" rot={-15 + 30 * hopU} bob={f > 672} />}
      <Tick f={f} at={672} x={690} y={520} ang={-150} len={110} />
      <Tick f={f} at={672} x={760} y={510} ang={-90} len={110} />
      <Tick f={f} at={672} x={830} y={520} ang={-30} len={110} />
    </>
  );
};
const F07 = (f: number) => {
  const T: Pt[] = [[640, 250], [815, 205], [975, 265]];
  return (
    <>
      {T.map((t, i) => {
        const L = 739 + 8 * i, E = 771 + 7 * i;
        if (f < L) return null;
        const fall = lerp(f, L, L + 12, 0, 1, OUT);
        const y = t[1] - 520 * (1 - fall);
        const lv = f < E ? 1 : lerp(f, E, E + 7, 1, 0);
        return <Drop key={i} f={f} at={0} x={t[0]} y={y} h={220} mode="on" bob={f > L + 12} lv={lv} col={W} />;
      })}
      <WordRow f={f} size={150} y={555} cx={765} maxW={420} mode="slam" fill={W} stroke={K} sw={14} shadow={K} rest={-4} seed={50} words={[{ t: "THIRST", at: 771 }]} />
      <WordRow f={f} size={150} y={715} cx={765} maxW={420} mode="slam" fill={W} stroke={K} sw={14} shadow={K} rest={-4} seed={60} words={[{ t: "AGAIN", at: 781 }]} />
    </>
  );
};
const DISC: Pt = [540, 1080];
const SPRING1: Pt[] = [0, 315, 45, 90, 270, 135, 225, 180].map((a) => [540 + 560 * Math.sin(rad(a)), 1080 - 700 * Math.cos(rad(a))] as Pt);
const SPRING2: Pt[] = Array.from({ length: 12 }, (_, i) => [540 + 380 * Math.sin(rad(15 + 30 * i)), 1080 - 480 * Math.cos(rad(15 + 30 * i))] as Pt);
const SpringDrop: React.FC<{ f: number; p: Pt; at: number; h: number }> = ({ f, p, at, h }) => {
  if (f < at) return null;
  const u = lerp(f, at, at + 16, 0, 1, OUT);
  const x = DISC[0] + (p[0] - DISC[0]) * u, y = DISC[1] + (p[1] - DISC[1]) * u;
  const rot = (Math.atan2(DISC[0] - p[0], -(DISC[1] - p[1])) * 180) / Math.PI;
  return <Drop f={f} at={0} x={x} y={y} h={h} rot={rot} mode="on" bob={f > at + 16} lv={1} col={TEAL} grow={[at, at + 16]} />;
};
const C08_TYPE = (f: number, ff?: number) => {
  const g = ff ?? f;
  return (
    <>
      <WordRow f={g} size={200} y={690} cx={540} maxW={900} mode="slam" fill={W} stroke={K} sw={16} shadow={DEEP} rest={-3} seed={70} words={[{ t: "SHALL", at: 952 }]} />
      <WordRow f={g} size={250} y={965} cx={540} maxW={900} mode="slam" fill={W} stroke={K} sw={16} shadow={DEEP} rest={2} seed={80} words={[{ t: "NEVER", at: 958 }]} />
      <WordRow f={g} size={250} y={1235} cx={540} maxW={900} mode="slam" fill={W} stroke={K} sw={16} shadow={DEEP} rest={-2} seed={90} words={[{ t: "THIRST", at: 967 }]} />
    </>
  );
};
const F08 = (f: number) => (
  <>
    {[829, 836, 843].map((a) => <Ripple key={a} f={f} at={a} C={DISC} r0={240} r1={700} col={W} />)}
    {[866, 874, 882].map((a) => <Ripple key={a} f={f} at={a} C={DISC} r0={240} r1={900} col={TEAL} />)}
    {SPRING1.map((p, i) => <SpringDrop key={i} f={f} p={p} at={866 + 4 * i} h={240} />)}
    {SPRING2.map((p, i) => <SpringDrop key={`s${i}`} f={f} p={p} at={920 + 2 * i} h={170} />)}
    <Flood f={f} C={DISC} a={940} b={956} />
    {f >= 956 && <rect x={0} y={0} width={1080} height={1920} fill={TEAL} />}
    {f >= 956 && <TealDots />}
    {C08_TYPE(f)}
  </>
);
const F09 = (f: number) => {
  const T: Pt[] = [[1005, 640], [960, 400], [820, 215], [600, 150], [300, 165], [120, 300], [75, 450]];
  const via: Pt[] = [[1015, 1300], [1015, 900]];
  return (
    <>
      <Stream f={f} lane={1010} a={1001} />
      {T.map((t, i) => {
        const up: Pt = i < 2 ? [1015, 700] : [1010, 380];
        const P: Pt[] = i === 0 ? [[1015, 2080], ...via, t] : [[1015, 2080], ...via, up, t];
        return <Rise key={i} f={f} P={P} L={1001 + 9 * i} D={40} h={190} />;
      })}
      <Crown f={f} at={1069} x={600} y={150} w={260} col={TEAL} />
      <Crown f={f} at={1069} x={300} y={165} w={260} col={TEAL} />
    </>
  );
};
const F10 = (f: number) => (
  <>
    {([[180, 270], [560, 215], [900, 300]] as Pt[]).map((p, i) => <Drop key={i} f={f} at={0} x={p[0]} y={p[1]} h={190} mode="on" lv={1} />)}
  </>
);
const F11 = (f: number) => <Rays f={f} o={[560, 655]} angles={[205, 221, 237, 253, 270, 287, 303, 319, 335]} r0={210} r1={900} a={1400} b={1432} sk={36} sw={24} />;
const F12 = (f: number) => {
  const w = lerp(f, 1466, 1478, 0, 900, SINE);
  if (w <= 0.5) return null;
  return (
    <g>
      <clipPath id="slab12"><rect x={80} y={1280} width={w + 20} height={250} /></clipPath>
      <g clipPath="url(#slab12)">
        <SlabRect x0={90} y0={1290} x1={990} y1={1510} fill={W} />
        <WordRow f={f} size={96} y={1385} cx={540} maxW={840} mode="step" fill={K}
          words={[{ t: "I", at: 1470 }, { t: "THAT", at: 1479 }, { t: "SPEAK", at: 1489 }, { t: "UNTO", at: 1499 }, { t: "THEE", at: 1511 }]} />
        <WordRow f={f} size={96} y={1480} cx={540} maxW={840} mode="step" fill={K} words={[{ t: "AM", at: 1540 }, { t: "HE.", at: 1544 }]} />
      </g>
    </g>
  );
};
const F14 = (f: number) => (
  <>
    <JarTicks f={f} at={1665} cx={335} cy={1290} angles={[-200, -178, -156, -134, -112]} lens={[200]} />
    <Puff f={f} at={1668} x={250} y={1215} r={70} />
    <Puff f={f} at={1680} x={330} y={1150} r={55} />
    <Puff f={f} at={1692} x={420} y={1080} r={40} />
  </>
);
const F15 = (f: number) => (<>{Balloon15(f)}{Ripples15(f)}</>);
const F16 = (f: number) => {
  const D: Pt[] = Array.from({ length: 14 }, (_, i) => [70 + 72 * i, 560 - 330 * Math.sin((Math.PI * i) / 13)] as Pt);
  return (
    <>
      {Ripples15(f)}
      {Balloon15(f)}
      {D.map((p, i) => <Drop key={i} f={f} at={2004 + 4 * i} wd={24} mode="well" x={p[0]} y={p[1]} h={170} lv={1} out={i >= 2 && i <= 11 ? 2068 : undefined} />)}
      {Slab16(f)}
    </>
  );
};
const F17 = (f: number) => (
  <>
    {Slab16(f)}
    <JarTicks f={f} at={2140} cx={215} cy={1130} out={2186} />
    <Drop f={f} at={2200} x={600} y={380} h={420} lv={lerp(f, 2255, 2263, 0, 1)} col={TEAL} />
  </>
);
const F18 = (f: number) => (
  <>
    {([[140, 260], [330, 470], [620, 200], [850, 420], [950, 215]] as Pt[]).map((p, i) => <Drop key={i} f={f} at={0} x={p[0]} y={p[1]} h={170} mode="on" lv={1} />)}
  </>
);
const F19 = (f: number) => {
  const X = [150, 290, 420, 560, 700, 830, 950];
  return (
    <>
      {X.map((x, i) => <Flower key={i} f={f} at={2510 + 6 * i} x={x} y={1840 + (hash(i + 5) - 0.5) * 40} r={60} i={i} />)}
      <Rays f={f} o={[550, 860]} angles={[215, 232, 249, 266, 283, 300, 318]} r0={250} r1={900} a={2522} b={2560} />
    </>
  );
};
const FRONTS: ((f: number) => React.ReactNode)[] = [F01, () => null, () => null, F04, F05, F06, F07, F08, F09, F10, F11, F12, () => null, F14, F15, F16, F17, F18, F19];

// ---------- transitions ----------
const T1_O: Pt = [1000, 1590];
const T3_O: Pt = [600, 380];
const holeMask = (d: string) =>
  dataUri(`<svg xmlns='http://www.w3.org/2000/svg' width='1080' height='1920'><path fill-rule='evenodd' d='M 0 0 H 1080 V 1920 H 0 Z ${d}' fill='white'/></svg>`);
const circD = (cx: number, cy: number, R: number) => `M ${cx - R} ${cy} a ${R} ${R} 0 1 0 ${2 * R} 0 a ${R} ${R} 0 1 0 ${-2 * R} 0 Z`;
const maskStyle = (m: string): React.CSSProperties =>
  ({ WebkitMaskImage: m, maskImage: m, WebkitMaskSize: "1080px 1920px", maskSize: "1080px 1920px" } as React.CSSProperties);
const T1_R = (f: number) => 2100 * Easing.inOut(Easing.quad)(lerp(f, 801, 813, 0, 1));
const T3_S = (f: number) => 210 * Math.pow(2600 / 210, lerp(f, 2264, 2278, 0, 1, INOUT));

const GuardMask: React.FC<{ id: string; shot: number; debug?: boolean }> = ({ id, shot, debug }) => (
  <mask id={id} maskUnits="userSpaceOnUse" x={0} y={0} width={1080} height={1920}>
    <rect x={0} y={0} width={1080} height={1920} fill="white" />
    {GUARD[shot].map((g, i) => (g.length === 5 ? <rect key={i} x={g[0]} y={g[1]} width={g[2]} height={g[3]} fill="black" /> : <ellipse key={i} cx={g[0]} cy={g[1]} rx={g[2]} ry={g[3]} fill="black" />))}
  </mask>
);

/** one full stack for a shot: [video] BACK, InkTop, FRONT. */
const Stack: React.FC<{ f: number; shot: number; maskId: string; src?: string; startFrom?: number; showVideo?: boolean; debug?: boolean }> = ({ f, shot, maskId, src = "waw_base_v2.mp4", startFrom, showVideo = false, debug }) => {
  const back = BACKS[shot](f);
  const front = FRONTS[shot](f);
  const video = <OffthreadVideo src={staticFile(src)} startFrom={startFrom} muted style={{ width: 1080, height: 1920, objectFit: "fill" }} />;
  return (
    <>
      {showVideo && video}
      {back && <svg style={FULL} width={1080} height={1920}><g>{back}</g></svg>}
      {back && <div style={{ position: "absolute", left: 0, top: 0, width: 1080, height: 1920, filter: "url(#inkKey)" }}>{video}</div>}
      <svg style={FULL} width={1080} height={1920}><g mask={`url(#${maskId})`}>{front}</g></svg>
      {debug && (
        <svg style={FULL} width={1080} height={1920}>
          {GUARD[shot].map((g, i) => (g.length === 5 ? <rect key={i} x={g[0]} y={g[1]} width={g[2]} height={g[3]} fill="none" stroke="red" strokeWidth={4} /> : <ellipse key={i} cx={g[0]} cy={g[1]} rx={g[2]} ry={g[3]} fill="none" stroke="red" strokeWidth={4} />))}
        </svg>
      )}
    </>
  );
};

const ExtLayers: React.FC<{ f: number; debug?: boolean }> = ({ f, debug }) => (
  <>
    {f >= 801 && f < 813 && (
      <Sequence from={801} durationInFrames={12} layout="none">
        <AbsoluteFill style={maskStyle(holeMask(circD(T1_O[0], T1_O[1], Math.max(2, T1_R(f)))))}>
          <Stack f={f} shot={6} maskId="gmOut" src="waw_c07.mp4" startFrom={118} showVideo debug={debug} />
        </AbsoluteFill>
      </Sequence>
    )}
    {f >= 2264 && f < 2278 && (
      <Sequence from={2264} durationInFrames={14} layout="none">
        <AbsoluteFill style={maskStyle(holeMask(dropD(T3_O[0], T3_O[1], T3_S(f))))}>
          <Stack f={f} shot={16} maskId="gmOut" src="waw_c17.mp4" startFrom={136} showVideo debug={debug} />
        </AbsoluteFill>
      </Sequence>
    )}
  </>
);

const Trans: React.FC<{ f: number }> = ({ f }) => {
  const out: React.ReactNode[] = [];
  if (f >= 132 && f < 142) out.push(<g key="t1">{dotWipe(f, 132, 142, 45, YEL, "reveal")}</g>);
  if (f >= 426 && f < 434) out.push(<g key="t4a">{dotWipe(f, 426, 434, 0, ORG, "cover")}</g>);
  if (f >= 434 && f < 442) out.push(<g key="t4b">{dotWipe(f, 434, 442, 0, ORG, "reveal")}</g>);
  out.push(<g key="t5">{Shutters(f, 562, 568, 574, 600)}</g>);
  if (f >= 677 && f < 683) out.push(<g key="t6a">{dotWipe(f, 677, 683, 180, YEL, "cover")}</g>);
  if (f >= 683 && f < 690) out.push(<g key="t6b">{dotWipe(f, 683, 690, 0, YEL, "reveal")}</g>);
  // T7 iris ring (clip tail is in ExtLayers)
  if (f >= 801 && f < 813) {
    const R = T1_R(f);
    if (R < 1500) out.push(
      <g key="t7" fill="none">
        <circle cx={T1_O[0]} cy={T1_O[1]} r={R} stroke={K} strokeWidth={14} />
        <circle cx={T1_O[0]} cy={T1_O[1]} r={Math.max(1, R - 12)} stroke={W} strokeWidth={10} />
      </g>
    );
  }
  // T8 flood radial hole
  if (f >= 981 && f < 995) {
    const hole = lerp(f, 981, 995, 0, 1500, OUT), C: Pt = [650, 1000];
    out.push(
      <g key="t8">
        <mask id="t8m" maskUnits="userSpaceOnUse" x={0} y={0} width={1080} height={1920}>
          <rect x={0} y={0} width={1080} height={1920} fill="white" />
          <circle cx={C[0]} cy={C[1]} r={hole + 120} fill="black" />
        </mask>
        <path fillRule="evenodd" d={`M 0 0 H 1080 V 1920 H 0 Z ${circD(C[0], C[1], hole + 240)}`} fill={TEAL} />
        {hexDots(54, (x, y, k) => {
          const d = Math.hypot(x - C[0], y - C[1]);
          const r = 40 * clamp01((d - hole) / 240);
          return d < hole + 260 && r > 0.5 ? <circle key={k} cx={x} cy={y} r={r} fill={TEAL} /> : null;
        }, 2)}
        <g mask="url(#t8m)"><TealDots />{C08_TYPE(f, 2000)}</g>
      </g>
    );
  }
  // T9 wave
  if (f >= 1109 && f < 1141) {
    const yTop = f < 1125 ? lerp(f, 1109, 1125, 1980, -80, Easing.in(Easing.quad)) : lerp(f, 1125, 1141, -80, 1990, Easing.out(Easing.quad));
    out.push(<WaveBody key="t9" f={f} yTop={yTop} />);
  }
  out.push(<g key="t14">{Bars(f, 1730, 1738, 1748, [TEAL, W, TEAL, W, TEAL])}</g>);
  if (f >= 2264 && f < 2278) {
    const s = T3_S(f);
    if (s < 1500) out.push(<path key="t17" d={dropD(T3_O[0], T3_O[1], s)} fill="none" stroke={K} strokeWidth={12} strokeLinejoin="round" />);
  }
  return <svg style={FULL} width={1080} height={1920}>{out}</svg>;
};

// ---------- page frame ----------
const THUMPS = [10, 22, 34, 112, 348, 436, 607, 771, 866, 952, 958, 967, 1341, 2092, 2119, 2128];
const Frame: React.FC<{ f: number }> = ({ f }) => {
  let sc = 1;
  for (const t of THUMPS) if (f >= t && f < t + 6) sc = 1 + 0.018 * (1 - OUT((f - t) / 6));
  return (
    <svg style={{ ...FULL, transform: `scale(${sc})`, transformOrigin: "540px 960px" }} width={1080} height={1920}>
      <rect x={10} y={10} width={1060} height={1900} fill="none" stroke={K} strokeWidth={20} />
      <rect x={26} y={26} width={1028} height={1868} fill="none" stroke={W} strokeWidth={6} />
    </svg>
  );
};

const Defs: React.FC<{ f: number; debug?: boolean }> = ({ f, debug }) => (
  <svg width={0} height={0} style={{ position: "absolute" }}>
    <defs>
      <clipPath id="dropClip"><path d={DROP_U} /></clipPath>
      <pattern id="dryDots" patternUnits="userSpaceOnUse" width={34} height={34}><circle cx={17} cy={17} r={7} fill={K} /></pattern>
      <filter id="inkKey" colorInterpolationFilters="sRGB" x="0" y="0" width="100%" height="100%">
        <feColorMatrix in="SourceGraphic" type="matrix" result="d" values="1 0 -1 0 0   -1 0 1 0 0   0 0 0 0 0   0 0 0 1 0" />
        <feColorMatrix in="d" type="matrix" result="m" values="0 0 0 0 0  0 0 0 0 0  0 0 0 0 0   -6 -6 0 0 1.5" />
        <feComposite in="SourceGraphic" in2="m" operator="in" />
      </filter>
      <GuardMask id="gmMain" shot={shotOf(f)} debug={debug} />
      <GuardMask id="gmOut" shot={f >= 2264 ? 16 : 6} debug={debug} />
    </defs>
  </svg>
);

export const WomanWellV2: React.FC<{ debug?: boolean }> = ({ debug = false }) => {
  const f = useCurrentFrame();
  const [h] = React.useState(() => delayRender("wawfont2"));
  React.useEffect(() => {
    new FontFace("Bangers", `url(${staticFile("Bangers.ttf")})`).load().then((ff) => { (document as any).fonts.add(ff); continueRender(h); }).catch(() => continueRender(h));
  }, [h]);
  const i = shotOf(f);
  return (
    <AbsoluteFill style={{ background: "#000" }}>
      <Defs f={f} debug={debug} />
      <OffthreadVideo src={staticFile("waw_base_v2.mp4")} muted style={{ width: 1080, height: 1920, objectFit: "cover" }} />
      <Stack f={f} shot={i} maskId="gmMain" debug={debug} />
      <ExtLayers f={f} debug={debug} />
      <Trans f={f} />
      <Frame f={f} />
    </AbsoluteFill>
  );
};
