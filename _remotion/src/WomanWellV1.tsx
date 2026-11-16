// Woman at the well (Pop Halftone) - motion layer v1. Spec: poc_pop_halftone/woman_at_well/motion_v1/MOTION_DESIGN.md
// Base = WOMAN_AT_WELL_POC.mp4 (public/waw_base_v2.mp4), 1.0x, never re-cut. Doodles are SVG layers over it.
// Transitions T1/T3 need the outgoing clip's tail: that comes from public/waw_c07.mp4 / waw_c17.mp4 (same clip the film was cut from).
// All frames are ABSOLUTE comp frames at 30 fps. No Math.random, no wobble: every mark is deterministic.
// Cut frames were measured from the real base film (scene detect), they differ by +1 from the design from c11 on.
// Audio is muxed from the base film after the render.
import React from "react";
import { AbsoluteFill, Easing, OffthreadVideo, Sequence, delayRender, continueRender, interpolate, staticFile, useCurrentFrame } from "remotion";

export const WW_FPS = 30;
export const WW_FRAMES = 2636;

// ---------- palette ----------
const K = "#111111", W = "#FFFFFF", TEAL = "#14B8C4", YEL = "#FFD60A";
const OL = 9, EDGE = 4; // black outline, white edge outside it

// ---------- math ----------
type Pt = [number, number];
const clampO = { extrapolateLeft: "clamp", extrapolateRight: "clamp" } as const;
const lerp = (f: number, a: number, b: number, from: number, to: number, easing?: (t: number) => number) =>
  interpolate(f, [a, b], [from, to], { ...clampO, easing });
const OUT = Easing.out(Easing.cubic);
const INOUT = Easing.inOut(Easing.cubic);
const SINE = Easing.inOut(Easing.sin);
const BACK = Easing.out(Easing.back(1.8));
const pop = (f: number, at: number) => interpolate(f, [at, at + 8], [0, 1], { ...clampO, easing: BACK });
const well = (f: number, at: number, d = 40) => lerp(f, at, at + d, 0, 1, SINE);
const rad = (d: number) => (d * Math.PI) / 180;
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

// ---------- timeline (measured from the real base film) ----------
const CUT = [0, 132, 240, 348, 434, 568, 683, 801, 981, 1125, 1341, 1463, 1569, 1654, 1738, 1978, 2128, 2264, 2445, 2636];

// ---------- parts ----------
// Drop: unit path, tip (0,-1), bottom (0,1). Outline is non-scaling (always 9 px).
const DROP_U = "M 0 -1 C 0.2 -0.6 0.7 -0.2 0.7 0.3 A 0.7 0.7 0 0 1 -0.7 0.3 C -0.7 -0.2 -0.2 -0.6 0 -1 Z";
/** Same drop at real size (for masks): centre cx,cy, half-height s. */
const dropD = (cx: number, cy: number, s: number) => {
  const X = (v: number) => (cx + v * s).toFixed(1), Y = (v: number) => (cy + v * s).toFixed(1), R = (v: number) => (v * s).toFixed(1);
  return `M ${X(0)} ${Y(-1)} C ${X(0.2)} ${Y(-0.6)} ${X(0.7)} ${Y(-0.2)} ${X(0.7)} ${Y(0.3)} A ${R(0.7)} ${R(0.7)} 0 0 1 ${X(-0.7)} ${Y(0.3)} C ${X(-0.7)} ${Y(-0.2)} ${X(-0.2)} ${Y(-0.6)} ${X(0)} ${Y(-1)} Z`;
};

type DropP = { f: number; at: number; x: number; y: number; h?: number; mode?: "pop" | "well" | "on"; bob?: boolean; rot?: number; lv?: number; col?: string; out?: number; wd?: number; grow?: [number, number] };
/** lv = fill level 0..1 from the bottom, col = fill colour. out = frame it shrinks to nothing (6 frames). */
const Drop: React.FC<DropP> = ({ f, at, x, y, h = 150, mode = "pop", bob = true, rot = 0, lv = 0, col = TEAL, out, wd = 40, grow }) => {
  if (f < at && mode !== "on") return null;
  let s = mode === "pop" ? pop(f, at) : mode === "well" ? well(f, at, wd) : 1;
  let dy = mode === "well" ? (1 - s) * 26 : 0;
  if (out !== undefined) s *= lerp(f, out, out + 6, 1, 0);
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

/** One thick sticker stroke (white edge, black outline, colour core). grows from (x,y) along ang over len. */
const Tick: React.FC<{ f: number; at: number; x: number; y: number; ang: number; len: number; col?: string; out?: number }> = ({ f, at, x, y, ang, len, col = YEL, out }) => {
  let p = pop(f, at);
  if (out !== undefined) p *= lerp(f, out, out + 6, 1, 0);
  if (p <= 0.02) return null;
  const x2 = x + Math.cos(rad(ang)) * len * p, y2 = y + Math.sin(rad(ang)) * len * p;
  return (
    <g strokeLinecap="round">
      <line x1={x} y1={y} x2={x2} y2={y2} stroke={W} strokeWidth={34} />
      <line x1={x} y1={y} x2={x2} y2={y2} stroke={K} strokeWidth={26} />
      <line x1={x} y1={y} x2={x2} y2={y2} stroke={col} strokeWidth={14} />
    </g>
  );
};
/** five jar ticks in a fan around (cx,cy) */
const JarTicks: React.FC<{ f: number; at: number; cx: number; cy: number; angles?: number[]; out?: number }> = ({ f, at, cx, cy, angles = [-150, -120, -90, -60, -30], out }) => {
  const lens = [120, 150, 165, 150, 120];
  return (
    <>
      {angles.map((a, i) => (
        <Tick key={i} f={f} at={at + i * 2} x={cx + Math.cos(rad(a)) * 62} y={cy + Math.sin(rad(a)) * 62} ang={a} len={lens[i % 5]} out={out} />
      ))}
    </>
  );
};

const Splash: React.FC<{ f: number; at: number; x: number; y: number }> = ({ f, at, x, y }) => {
  const u = (f - at) / 10;
  if (u < 0 || u >= 1) return null;
  const s = Math.sin(Math.PI * u);
  return (
    <>
      {[-50, 0, 50].map((a, i) => (
        <Drop key={i} f={f} at={at} x={x + Math.sin(rad(a)) * 55 * Math.min(1, u * 2.5)} y={y - Math.cos(rad(a)) * 55 * Math.min(1, u * 2.5) - 12} h={54 * s} rot={a} lv={1} col={W} mode="on" bob={false} />
      ))}
    </>
  );
};

const Puff: React.FC<{ f: number; at: number; x: number; y: number; r: number }> = ({ f, at, x, y, r }) => {
  const s = pop(f, at) * lerp(f, at + 12, at + 22, 1, 0);
  if (s <= 0.02) return null;
  const C: [number, number, number][] = [[0, 0, r], [-0.7 * r, 0.2 * r, 0.7 * r], [0.7 * r, 0.15 * r, 0.75 * r], [0.05 * r, -0.55 * r, 0.7 * r]];
  return (
    <g transform={`translate(${x} ${y}) scale(${s})`}>
      {C.map((c, i) => <circle key={`a${i}`} cx={c[0]} cy={c[1]} r={c[2]} fill={W} stroke={W} strokeWidth={OL + 2 * EDGE} />)}
      {C.map((c, i) => <circle key={`b${i}`} cx={c[0]} cy={c[1]} r={c[2]} fill={W} stroke={K} strokeWidth={OL} />)}
      {C.map((c, i) => <circle key={`c${i}`} cx={c[0]} cy={c[1]} r={c[2] - 4} fill={W} />)}
    </g>
  );
};

/** Dot rays running out from a sun (white dots with a black ring), drawn outward then crawling slowly. */
const Rays: React.FC<{ f: number; o: Pt; angles: number[]; r0: number; r1: number; a: number; b: number }> = ({ f, o, angles, r0, r1, a, b }) => {
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
            <line {...common} stroke={K} strokeWidth={30} />
            <line {...common} stroke={W} strokeWidth={19} />
          </g>
        );
      })}
    </>
  );
};

/** Burst star + text. */
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
      <polygon points={starPts(cx, cy, 262, 168)} fill="none" stroke={W} strokeWidth={OL + 2 * EDGE} strokeLinejoin="round" vectorEffect="non-scaling-stroke" />
      <polygon points={starPts(cx + 5, cy + 5, 262, 168)} fill={YEL} />
      <polygon points={starPts(cx, cy, 262, 168)} fill="none" stroke={K} strokeWidth={OL} strokeLinejoin="round" vectorEffect="non-scaling-stroke" />
      <text x={cx} y={cy + 68} textAnchor="middle" fontFamily="Bangers" fontSize={190} fill={K} stroke={W} strokeWidth={10} paintOrder="stroke" letterSpacing={4}>WHY?</text>
    </g>
  );
};

const Caption: React.FC<{ f: number; at: number }> = ({ f, at }) => {
  if (f < at) return null;
  const w = lerp(f, at, at + 8, 0, 760);
  return (
    <g>
      <clipPath id="capClip"><rect x={160} y={170} width={Math.max(0.1, w + 10)} height={330} /></clipPath>
      <g clipPath="url(#capClip)">
        <rect x={170} y={190} width={740} height={290} rx={22} fill={W} stroke={K} strokeWidth={OL} />
        <text x={540} y={316} textAnchor="middle" fontFamily="Bangers" fontSize={112} fill={K} letterSpacing={3}>THE SAVIOUR</text>
        <text x={540} y={438} textAnchor="middle" fontFamily="Bangers" fontSize={112} fill={K} letterSpacing={3}>OF THE WORLD</text>
      </g>
    </g>
  );
};

/** Tomb flower: the art's own 5-petal outline flower, grown slowly, no bounce. */
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
        {[0, 1, 2, 3, 4].map((k) => <ellipse key={`a${k}`} cx={0} cy={-r * 0.62} rx={r * 0.36} ry={r * 0.52} transform={`rotate(${k * 72})`} fill={W} stroke={W} strokeWidth={OL + 2 * EDGE} />)}
        {[0, 1, 2, 3, 4].map((k) => <ellipse key={`b${k}`} cx={0} cy={-r * 0.62} rx={r * 0.36} ry={r * 0.52} transform={`rotate(${k * 72})`} fill={W} stroke={K} strokeWidth={OL - 2} />)}
        {[0, 1, 2, 3, 4].map((k) => <ellipse key={`c${k}`} cx={0} cy={-r * 0.62} rx={r * 0.36 - 4} ry={r * 0.52 - 4} transform={`rotate(${k * 72})`} fill={W} />)}
        <circle r={r * 0.28} fill={YEL} stroke={K} strokeWidth={OL - 2} />
      </g>
    </g>
  );
};

// ---------- rising drops (c09) ----------
const Rise: React.FC<{ f: number; P: Pt[]; L: number; D: number; h?: number; hold?: boolean; bobAfter?: boolean }> = ({ f, P, L, D, h = 150, hold = true }) => {
  if (f < L) return null;
  const end = P[P.length - 1];
  if (f >= L + D) return hold ? <Drop f={f} at={0} x={end[0]} y={end[1]} h={h} mode="on" lv={1} col={TEAL} /> : null;
  const u = lerp(f, L, L + D, 0, 1, Easing.out(Easing.quad));
  const [x, y] = posOn(P, u);
  const [xa, ya] = posOn(P, Math.min(1, u + 0.03)), [xb, yb] = posOn(P, Math.max(0, u - 0.03));
  const rot = Math.max(-14, Math.min(14, (Math.atan2(xa - xb, -(ya - yb)) * 180) / Math.PI));
  return <Drop f={f} at={0} x={x} y={y} h={h} rot={rot} mode="on" bob={false} lv={1} col={TEAL} />;
};

// ---------- per-shot layers (absolute frames) ----------
const S01 = (f: number) => {
  const F: [number, number, number][] = [[612, 8, 0], [628, 20, 1], [598, 32, 2]];
  const yl = 1372;
  return (
    <>
      {F.map(([x, tl], i) => f < tl && <Drop key={i} f={f} at={0} x={x} y={yl - 40 * (tl - f)} h={130} mode="on" bob={false} lv={1} col={W} />)}
      {F.map(([x, tl], i) => <Splash key={`s${i}`} f={f} at={tl} x={x} y={yl} />)}
      <JarTicks f={f} at={69} cx={205} cy={1140} out={104} />
      <WhyStar f={f} at={112} cx={600} cy={420} swell={[126, 132]} />
    </>
  );
};
const S02 = (f: number) => (
  <Rays f={f} o={[510, 560]} angles={[205, 222, 240, 255, 270, 285, 300, 318, 335]} r0={270} r1={820} a={139} b={165} />
);
const S03 = (_f: number) => null;
const S04 = (f: number) => <Drop f={f} at={376} x={555} y={830} h={150} />;
const S05 = (f: number) => (
  <>
    <Tick f={f} at={436} x={150} y={330} ang={-132} len={130} />
    <Tick f={f} at={440} x={260} y={205} ang={-112} len={130} />
    <Tick f={f} at={444} x={420} y={135} ang={-92} len={130} />
    <Drop f={f} at={538} x={880} y={330} rot={-12 * Math.sin(Math.PI * lerp(f, 548, 566, 0, 1) * 2) * (f > 548 ? 1 : 0)} />
  </>
);
const CRACK: Pt[] = [[540, 0], [498, 70], [578, 140], [514, 215], [582, 290], [530, 360], [572, 430], [548, 470]];
const S06 = (f: number) => {
  const d = "M " + CRACK.map((p) => p.join(" ")).join(" L ");
  const p = lerp(f, 602, 614, 0, 1, OUT);
  const u = lerp(f, 658, 674, 0, 1, INOUT);
  const hx = 300 + 490 * u, hy = 430 - 920 * lerp(f, 658, 674, 0, 1) * (1 - lerp(f, 658, 674, 0, 1));
  return (
    <>
      {p > 0 && (
        <g fill="none" strokeLinejoin="round" strokeLinecap="round">
          <path d={d} pathLength={1} strokeDasharray={1} strokeDashoffset={1 - p} stroke={W} strokeWidth={26} />
          <path d={d} pathLength={1} strokeDasharray={1} strokeDashoffset={1 - p} stroke={K} strokeWidth={15} />
        </g>
      )}
      {f < 658 ? <Drop f={f} at={640} x={300} y={430} /> : <Drop f={f} at={0} x={hx} y={hy} mode="on" rot={(u - 0.5) * 30} bob={f > 674} />}
      <Tick f={f} at={674} x={720} y={520} ang={-150} len={70} />
      <Tick f={f} at={676} x={790} y={510} ang={-90} len={70} />
      <Tick f={f} at={678} x={860} y={520} ang={-30} len={70} />
    </>
  );
};
const S07 = (f: number) => {
  const T: Pt[] = [[800, 180], [900, 330], [1000, 250]];
  return (
    <>
      {T.map((t, i) => {
        const L = 730 + 8 * i, E = 771 + 7 * i;
        const fall = lerp(f, L, L + 12, 0, 1, OUT);
        const y = t[1] - 520 * (1 - fall);
        const lv = f < E ? 1 : lerp(f, E, E + 7, 1, 0);
        return f >= L && <Drop key={i} f={f} at={0} x={t[0]} y={y} h={150} mode="on" bob={f > L + 12} lv={lv} col={W} />;
      })}
    </>
  );
};
const DISC: Pt = [540, 1080];
const SPRING: Pt[] = [0, 315, 45, 90, 270, 135, 225, 180].map((a) => [540 + 430 * Math.sin(rad(a)), 1080 - 640 * Math.cos(rad(a))] as Pt);
const SPRING_AT = [866, 872, 878, 920, 925, 930, 935, 940];
const ringR = (f: number, at: number, to: number) => lerp(f, at, at + 24, 240, to, OUT);
const S08 = (f: number) => (
  <>
    {([[836, 430], [846, 530]] as [number, number][]).map(([at, to], i) => {
      const r = ringR(f, at, to), k = f < at ? 0 : lerp(f, at + 24, at + 30, 1, 0);
      return f >= at && k > 0 && (
        <g key={i} fill="none">
          <circle cx={DISC[0]} cy={DISC[1]} r={r} stroke={W} strokeWidth={(OL + 2 * EDGE) * k} />
          <circle cx={DISC[0]} cy={DISC[1]} r={r} stroke={K} strokeWidth={OL * k} />
        </g>
      );
    })}
    {SPRING.map((p, i) => {
      const at = SPRING_AT[i];
      if (f < at) return null;
      const u = lerp(f, at, at + 16, 0, 1, OUT);
      const x = DISC[0] + (p[0] - DISC[0]) * u, y = DISC[1] + (p[1] - DISC[1]) * u;
      const rot = (Math.atan2(DISC[0] - p[0], -(DISC[1] - p[1])) * 180) / Math.PI;
      return <Drop key={i} f={f} at={0} x={x} y={y} h={170} rot={rot} mode="on" bob={f > at + 16} lv={1} col={TEAL} grow={[at, at + 16]} />;
    })}
  </>
);
const S09 = (f: number) => {
  const T: Pt[] = [[1012, 640], [962, 400], [820, 205], [600, 135], [300, 150], [120, 300], [70, 450]];
  const via: Pt[] = [[1015, 1300], [1015, 900]];
  return (
    <>
      {T.map((t, i) => {
        const up: Pt = i < 2 ? [1015, 700] : [1010, 380];
        const P: Pt[] = i === 0 ? [[1015, 2080], ...via, t] : [[1015, 2080], ...via, up, t];
        return <Rise key={i} f={f} P={P} L={1001 + 9 * i} D={40} h={130} />;
      })}
      {[0, 1, 2].map((i) => (
        <Rise key={`r${i}`} f={f} P={[[1010 + 6 * i, 2080], [1022 - 8 * i, 1500], [1012, 900], [1018, 300], [1010, -120]]} L={1090 + 9 * i} D={70} h={130} hold={false} />
      ))}
    </>
  );
};
const S10 = (f: number) => (
  <>
    <Drop f={f} at={0} x={180} y={260} mode="on" />
    <Drop f={f} at={0} x={560} y={140} mode="on" />
    <Drop f={f} at={0} x={900} y={300} mode="on" />
  </>
);
const S11 = (f: number) => <Rays f={f} o={[560, 655]} angles={[215, 235, 250, 265, 280, 295, 315]} r0={210} r1={760} a={1428} b={1458} />;
const S12 = (_f: number) => null;
const S13 = (_f: number) => null;
const S14 = (f: number) => (
  <>
    <JarTicks f={f} at={1668} cx={335} cy={1290} angles={[-200, -175, -150, -125]} />
    <Puff f={f} at={1668} x={250} y={1215} r={42} />
    <Puff f={f} at={1680} x={330} y={1150} r={32} />
  </>
);
const S15 = (f: number) => (
  <>
    {([[120, 170], [380, 110], [700, 140], [960, 230]] as Pt[]).map((p, i) => <Drop key={i} f={f} at={1748 + 20 * i} x={p[0]} y={p[1]} mode="well" lv={1} />)}
  </>
);
const S16 = (f: number) => {
  const T: Pt[] = [[90, 230], [100, 450], [210, 650], [430, 560], [660, 540], [870, 560], [960, 430], [990, 220]];
  return (
    <>
      {T.map((p, i) => <Drop key={i} f={f} at={2004 + 6 * i} x={p[0]} y={p[1]} mode="well" wd={24} lv={1} />)}
      <Caption f={f} at={2076} />
    </>
  );
};
const S17 = (f: number) => {
  const lv = lerp(f, 2248, 2256, 0, 1);
  return (
    <>
      <JarTicks f={f} at={2140} cx={215} cy={1130} out={2186} />
      <Drop f={f} at={2196} x={220} y={940} h={170} lv={lv} col={TEAL} />
    </>
  );
};
const S18 = (f: number) => (
  <>
    {([[140, 260], [330, 470], [620, 180], [850, 420], [960, 150]] as Pt[]).map((p, i) => <Drop key={i} f={f} at={0} x={p[0]} y={p[1]} mode="on" lv={1} />)}
  </>
);
const S19 = (f: number) => (
  <>
    {([[190, 1830], [370, 1850], [545, 1840], [730, 1860], [860, 1820]] as Pt[]).map((p, i) => <Flower key={i} f={f} at={2510 + 6 * i} x={p[0]} y={p[1]} r={46} i={i} />)}
    <Rays f={f} o={[550, 860]} angles={[215, 232, 249, 266, 283, 300, 318]} r0={250} r1={760} a={2522} b={2545} />
  </>
);

const LAYERS: ((f: number) => React.ReactNode)[] = [S01, S02, S03, S04, S05, S06, S07, S08, S09, S10, S11, S12, S13, S14, S15, S16, S17, S18, S19];

// ---------- transitions ----------
// T1 well iris c07 -> c08 : window [801,813)
const T1_O: Pt = [1000, 1590];
const T3_O: Pt = [220, 940];
const holeMask = (d: string) =>
  dataUri(`<svg xmlns='http://www.w3.org/2000/svg' width='1080' height='1920'><path fill-rule='evenodd' d='M 0 0 H 1080 V 1920 H 0 Z ${d}' fill='white'/></svg>`);
const circD = (cx: number, cy: number, R: number) => `M ${cx - R} ${cy} a ${R} ${R} 0 1 0 ${2 * R} 0 a ${R} ${R} 0 1 0 ${-2 * R} 0 Z`;
const maskStyle = (m: string): React.CSSProperties =>
  ({ WebkitMaskImage: m, maskImage: m, WebkitMaskSize: "1080px 1920px", maskSize: "1080px 1920px" } as React.CSSProperties);

const T1_R = (f: number) => 2100 * Easing.inOut(Easing.quad)(lerp(f, 801, 813, 0, 1));
const T3_S = (f: number) => 85 * Math.pow(2300 / 85, lerp(f, 2264, 2276, 0, 1, INOUT));

const ExtLayers: React.FC<{ f: number }> = ({ f }) => (
  <>
    {f >= 801 && f < 813 && (
      <Sequence from={801} durationInFrames={12} layout="none">
        <AbsoluteFill style={maskStyle(holeMask(circD(T1_O[0], T1_O[1], Math.max(2, T1_R(f)))))}>
          <OffthreadVideo src={staticFile("waw_c07.mp4")} startFrom={118} muted style={{ width: 1080, height: 1920, objectFit: "fill" }} />
          <svg style={FULL} width={1080} height={1920}>{S07(f)}</svg>
        </AbsoluteFill>
      </Sequence>
    )}
    {f >= 2264 && f < 2276 && (
      <Sequence from={2264} durationInFrames={12} layout="none">
        <AbsoluteFill style={maskStyle(holeMask(dropD(T3_O[0], T3_O[1], T3_S(f))))}>
          <OffthreadVideo src={staticFile("waw_c17.mp4")} startFrom={136} muted style={{ width: 1080, height: 1920, objectFit: "fill" }} />
          <svg style={FULL} width={1080} height={1920}>{S17(f)}</svg>
        </AbsoluteFill>
      </Sequence>
    )}
  </>
);

const WEDGE_COL = ["#0CA1A8", "#FFD60A", "#F55700", "#0CA1A8", "#EE0C00", "#FFD60A", "#F55700", "#0CA1A8", "#FFD60A", "#EE0C00", "#0CA1A8", "#F55700", "#FFD60A", "#0CA1A8", "#EE0C00", "#F55700"];
const wedgePath = (o: Pt, a0: number, a1: number, R = 2600) => {
  a1 += 0.5; // tiny overlap so no hairline gaps show the picture through
  const x0 = o[0] + R * Math.cos(rad(a0)), y0 = o[1] + R * Math.sin(rad(a0)), x1 = o[0] + R * Math.cos(rad(a1)), y1 = o[1] + R * Math.sin(rad(a1));
  return `M ${o[0]} ${o[1]} L ${x0.toFixed(1)} ${y0.toFixed(1)} A ${R} ${R} 0 0 1 ${x1.toFixed(1)} ${y1.toFixed(1)} Z`;
};

const Edges: React.FC<{ f: number }> = ({ f }) => {
  const out: React.ReactNode[] = [];
  // T1 ring
  if (f >= 801 && f < 813) {
    const R = T1_R(f);
    if (R < 1500) out.push(
      <g key="t1" fill="none">
        <circle cx={T1_O[0]} cy={T1_O[1]} r={R} stroke={K} strokeWidth={14} />
        <circle cx={T1_O[0]} cy={T1_O[1]} r={Math.max(1, R - 12)} stroke={TEAL} strokeWidth={10} />
      </g>
    );
  }
  // T3 plain black line on the drop edge
  if (f >= 2264 && f < 2276) {
    const s = T3_S(f);
    if (s < 1500) out.push(<path key="t3" d={dropD(T3_O[0], T3_O[1], s)} fill="none" stroke={K} strokeWidth={12} strokeLinejoin="round" />);
  }
  // T2 burst fill c08 -> c09 (disc grows over the frame, then folds open like a pinwheel)
  if (f >= 965 && f < 989) {
    if (f < 981) {
      const p = lerp(f, 965, 981, 0, 1, INOUT);
      const R = 262 * Math.pow(2600 / 262, p);
      out.push(
        <g key="t2">
          <clipPath id="discClip"><circle cx={DISC[0]} cy={DISC[1]} r={R} /></clipPath>
          <g clipPath="url(#discClip)">
            {WEDGE_COL.map((c, k) => <path key={k} d={wedgePath(DISC, k * 22.5, (k + 1) * 22.5)} fill={c} />)}
          </g>
          {R < 1500 && <circle cx={DISC[0]} cy={DISC[1]} r={R} fill="none" stroke={K} strokeWidth={14} />}
        </g>
      );
    } else {
      const e = SINE(lerp(f, 981, 989, 0, 1)), rot = 8 * e;
      out.push(
        <g key="t2">
          {WEDGE_COL.map((c, k) => <path key={k} d={wedgePath(DISC, k * 22.5 + rot + e * 22.5, (k + 1) * 22.5 + rot)} fill={c} />)}
        </g>
      );
    }
  }
  // T4 question pop c01 -> c02: star floods yellow, then breaks into halftone dots that shrink away
  if (f >= 132 && f < 138) {
    const p = (f - 132) / 6;
    const dots: React.ReactNode[] = [];
    const P = 38;
    for (let iy = 0; iy * P < 1960; iy++) for (let ix = 0; ix * P < 1120; ix++) {
      const x = ix * P + (iy % 2 ? P / 2 : 0), y = iy * P;
      const k = Math.min(1, Math.max(0, p * 1.7 - (x + y) / 4200));
      const r = 30 * (1 - k);
      if (r > 0.6) dots.push(<circle key={`${ix}-${iy}`} cx={x} cy={y} r={r} fill={YEL} />);
    }
    out.push(<g key="t4">{dots}</g>);
  }
  if (f >= 130 && f < 132) out.push(<rect key="t4a" x={0} y={0} width={1080} height={1920} fill={YEL} opacity={lerp(f, 130, 132, 0.6, 1)} />);
  return <svg style={FULL} width={1080} height={1920}>{out}</svg>;
};

const Defs: React.FC = () => (
  <svg width={0} height={0} style={{ position: "absolute" }}>
    <defs>
      <clipPath id="dropClip"><path d={DROP_U} /></clipPath>
    </defs>
  </svg>
);

export const WomanWellV1: React.FC = () => {
  const f = useCurrentFrame();
  const [h] = React.useState(() => delayRender("wawfont"));
  React.useEffect(() => {
    new FontFace("Bangers", `url(${staticFile("Bangers.ttf")})`).load().then((ff) => { (document as any).fonts.add(ff); continueRender(h); }).catch(() => continueRender(h));
  }, [h]);
  const i = CUT.findIndex((c, k) => f >= c && f < CUT[k + 1]);
  return (
    <AbsoluteFill style={{ background: "#000" }}>
      <Defs />
      <OffthreadVideo src={staticFile("waw_base_v2.mp4")} muted style={{ width: 1080, height: 1920, objectFit: "cover" }} />
      {i >= 0 && <svg style={FULL} width={1080} height={1920}>{LAYERS[i](f)}</svg>}
      <ExtLayers f={f} />
      <Edges f={f} />
    </AbsoluteFill>
  );
};
