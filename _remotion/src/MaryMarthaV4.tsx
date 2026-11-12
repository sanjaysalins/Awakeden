// Mary and Martha (Warm Storybook POC) - motion layer v4 = v3 retimed to words H2 (voice_v4, Luke 10:42 line fix, 2026-11-12, owner "yes").
// Shots 1-10 unchanged; later cuts/doodles moved to the new word times. Audio muxed from MARY_MARTHA_SCORED_v4.mp4.
// (v2 header below kept for the design history.)
// Mary and Martha (Warm Storybook POC) - motion layer v2 ("the illustrator keeps drawing").
// Design: poc_warm_storybook_style/motion_v2/MOTION_DESIGN.md (Fable, 2026-11-12). Owner said v1 doodles felt forced.
// Cut + 6 transitions = v1. Doodles come from the owner refs' own vocabulary: pencil lamp, gold flame, gold olive sprig.
// Pencil = Martha's side, terracotta (His mantle) = His words / "one thing" / the last line.
// Thread: a small pencil knot (her worry) -> lasso of "many things" -> one calm line -> named "worry" -> unties under "And He loved her."
// The 15 Kling clips are laid as separate layers (6 cuts overlap). Audio is muxed afterwards from MARY_MARTHA_SCORED_v2.mp4.
// All frames are ABSOLUTE comp frames (30 fps).
import React from "react";
import { AbsoluteFill, Easing, OffthreadVideo, Sequence, interpolate, staticFile, useCurrentFrame } from "remotion";
import { useFonts } from "./TalithaCumi";

import { MM_FPS } from "./MaryMarthaV1";
export const MM4_FRAMES = 2189; // 69.97 s voice + 3.0 s hold
const MM_FRAMES = MM4_FRAMES;
export { MM_FPS };

const clamp = { extrapolateLeft: "clamp", extrapolateRight: "clamp" } as const;
const OUT = Easing.out(Easing.cubic);
const INOUT = Easing.inOut(Easing.cubic);
const SINE = Easing.inOut(Easing.sin);
const boilSeed = (f: number) => [3, 11, 27][Math.floor(f / 5) % 3];
const lerp = (f: number, a: number, b: number, from: number, to: number, easing?: (t: number) => number) =>
  interpolate(f, [a, b], [from, to], { ...clamp, easing });

const C = { paper: "#F8EFDD", shade: "#E8D6B4", graphite: "#3A322B", sepia: "#6B4A32", terra: "#A84A24" };
type Box = { x1: number; y1: number; x2: number; y2: number };
type Pt = [number, number];
const FULL: React.CSSProperties = { position: "absolute", left: 0, top: 0, width: 1080, height: 1920, overflow: "visible" };
const FR = { x: "-15%", y: "-15%", width: "130%", height: "130%", colorInterpolationFilters: "sRGB" as const };
const HOLES = "0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  -2.2 0 0 0 1.85";

// ---------- clips + transitions ----------
// [clip, startFrame, endFrame]; cut frames from the spec (round(s*30)).
const CUTS = [0, 179, 261, 329, 464, 668, 837, 954, 1059, 1208, 1283, 1523, 1658, 1886, 1969, MM_FRAMES];
const CLIPS = ["s01", "s02", "s03", "s04", "s05", "s06", "s07", "s08", "s09", "s10", "s11", "s13", "s14", "s12", "s15"];
type TKind = "curtain" | "slideL" | "slideR" | "bloom";
// transition INTO shot index i (keyed by incoming index)
const TRANS: Record<number, { kind: TKind; n: number; ease: (t: number) => number; ox?: number; oy?: number }> = {
  2: { kind: "curtain", n: 12, ease: OUT },
  7: { kind: "slideL", n: 9, ease: INOUT },          // C7: outgoing exits left, incoming from right
  8: { kind: "bloom", n: 16, ease: OUT, ox: 320, oy: 372 },
  10: { kind: "slideR", n: 9, ease: INOUT },         // C10: mirror
  12: { kind: "bloom", n: 20, ease: SINE, ox: 540, oy: 800 },
  14: { kind: "bloom", n: 16, ease: OUT, ox: 600, oy: 420 },
};

const bloomMask = (p: number, ox: number, oy: number) => {
  const rx = Math.max(0.01, p * 1500), ry = Math.max(0.01, p * 2300);
  const svg = `<svg xmlns='http://www.w3.org/2000/svg' width='1080' height='1920'><filter id='w' x='-50%' y='-50%' width='200%' height='200%'>` +
    `<feTurbulence type='fractalNoise' baseFrequency='0.009 0.016' numOctaves='3' seed='4' result='n'/>` +
    `<feDisplacementMap in='SourceGraphic' in2='n' scale='34' xChannelSelector='R' yChannelSelector='G' result='d'/>` +
    `<feGaussianBlur in='d' stdDeviation='28'/></filter>` +
    `<ellipse cx='${ox}' cy='${oy}' rx='${rx}' ry='${ry}' fill='white' filter='url(#w)'/></svg>`;
  return `url("data:image/svg+xml,${encodeURIComponent(svg)}")`;
};
const curtainFront = (X: number) => {
  const pts: string[] = [];
  for (let y = -40; y <= 1960; y += 40) pts.push(`${(X + 26 * Math.sin((2 * Math.PI * y) / 640)).toFixed(1)},${y}`);
  return pts;
};
const curtainMask = (X: number) => {
  const front = curtainFront(X);
  const svg = `<svg xmlns='http://www.w3.org/2000/svg' width='1080' height='1920'><filter id='d' x='-20%' y='-20%' width='140%' height='140%'>` +
    `<feTurbulence type='fractalNoise' baseFrequency='0.022' numOctaves='3' seed='7' result='n'/>` +
    `<feDisplacementMap in='SourceGraphic' in2='n' scale='16' xChannelSelector='R' yChannelSelector='G'/></filter>` +
    `<polygon points='${front.join(" ")} 1200,1960 1200,-40' fill='white' filter='url(#d)'/></svg>`;
  return `url("data:image/svg+xml,${encodeURIComponent(svg)}")`;
};

const Clip: React.FC<{ name: string }> = ({ name }) => (
  <OffthreadVideo src={staticFile(`mm/${name}.mp4`)} muted style={{ width: 1080, height: 1920, objectFit: "cover" }} />
);

const Shots: React.FC<{ f: number; extras: (i: number) => React.ReactNode }> = ({ f, extras }) => (
  <>
    {CLIPS.map((name, i) => {
      const s = CUTS[i], e = CUTS[i + 1];
      const outT = TRANS[i + 1];
      const end = e + (outT ? outT.n : 0);
      const inT = TRANS[i];
      let style: React.CSSProperties = {};
      if (inT && f < s + inT.n) {
        const p = inT.ease(Math.min(1, Math.max(0, (f - s) / inT.n)));
        if (inT.kind === "bloom") {
          const m = bloomMask(p, inT.ox!, inT.oy!);
          style = { WebkitMaskImage: m, maskImage: m, WebkitMaskSize: "1080px 1920px", maskSize: "1080px 1920px" } as React.CSSProperties;
        } else if (inT.kind === "curtain") {
          const m = curtainMask(1100 + (-80 - 1100) * p);
          style = { WebkitMaskImage: m, maskImage: m, WebkitMaskSize: "1080px 1920px", maskSize: "1080px 1920px" } as React.CSSProperties;
        } else if (inT.kind === "slideL") style = { transform: `translateX(${1080 * (1 - p)}px)` };
        else if (inT.kind === "slideR") style = { transform: `translateX(${-1080 * (1 - p)}px)` };
      }
      if (outT && f >= e && (outT.kind === "slideL" || outT.kind === "slideR")) {
        const p = outT.ease(Math.min(1, (f - e) / outT.n));
        style = { transform: `translateX(${(outT.kind === "slideL" ? -1080 : 1080) * p}px)` };
      }
      return (
        <Sequence key={name} from={s} durationInFrames={end - s} layout="none">
          <AbsoluteFill style={style}><Clip name={name} />{extras(i)}</AbsoluteFill>
        </Sequence>
      );
    })}
  </>
);

/** Paper edges / cloth fold drawn on top of the clips during curtain + slide transitions. */
const TransitionEdges: React.FC<{ f: number }> = ({ f }) => {
  for (const [k, t] of Object.entries(TRANS)) {
    const i = Number(k), s = CUTS[i];
    if (f < s || f >= s + t.n) continue;
    const p = t.ease((f - s) / t.n);
    if (t.kind === "curtain") {
      const X = 1100 + (-80 - 1100) * p;
      const front = curtainFront(X).map((q) => q.split(",").map(Number) as Pt);
      const band = (dx: number) => front.map(([x, y]) => `${(x - dx).toFixed(1)},${y}`).join(" ");
      return (
        <svg style={FULL} width={1080} height={1920}>
          <polygon points={`${band(0)} ${front.slice().reverse().map(([x, y]) => `${(x - 16).toFixed(1)},${y}`).join(" ")}`} fill={C.paper} filter="url(#deckle)" />
          <polygon points={`${band(16)} ${front.slice().reverse().map(([x, y]) => `${(x - 56).toFixed(1)},${y}`).join(" ")}`} fill={C.shade} fillOpacity={0.5} filter="url(#deckle)" />
        </svg>
      );
    }
    if (t.kind === "slideL" || t.kind === "slideR") {
      const x = t.kind === "slideL" ? 1080 * (1 - p) : 1080 * p;
      return (
        <svg style={FULL} width={1080} height={1920}>
          <rect x={x - 7} y={-10} width={14} height={1940} fill={C.paper} />
          <line x1={x} y1={-10} x2={x} y2={1930} stroke={C.sepia} strokeWidth={2} strokeOpacity={0.5} />
        </svg>
      );
    }
  }
  return null;
};

// ---------- shared marks ----------
const Defs: React.FC<{ f: number }> = ({ f }) => (
  <svg width={0} height={0} style={{ position: "absolute" }}>
    <defs>
      <filter id="deckle" {...FR}>
        <feTurbulence type="fractalNoise" baseFrequency="0.022" numOctaves={3} seed={7} result="n" />
        <feDisplacementMap in="SourceGraphic" in2="n" scale={16} xChannelSelector="R" yChannelSelector="G" />
      </filter>
      <filter id="graphite" {...FR}>
        <feTurbulence type="fractalNoise" baseFrequency="1.1" numOctaves={1} seed={9} result="g" />
        <feColorMatrix in="g" type="matrix" values={HOLES} result="holes" />
        <feComposite in="SourceGraphic" in2="holes" operator="in" />
      </filter>
      <filter id="pencil" {...FR}>
        <feTurbulence type="fractalNoise" baseFrequency="0.035" numOctaves={2} seed={boilSeed(f)} result="w" />
        <feDisplacementMap in="SourceGraphic" in2="w" scale={4} xChannelSelector="R" yChannelSelector="G" result="d" />
        <feTurbulence type="fractalNoise" baseFrequency="1.1" numOctaves={1} seed={9} result="g" />
        <feColorMatrix in="g" type="matrix" values={HOLES} result="holes" />
        <feComposite in="d" in2="holes" operator="in" />
      </filter>
      <filter id="pencilStill" {...FR}>
        <feTurbulence type="fractalNoise" baseFrequency="0.035" numOctaves={2} seed={3} result="w" />
        <feDisplacementMap in="SourceGraphic" in2="w" scale={4} xChannelSelector="R" yChannelSelector="G" result="d" />
        <feTurbulence type="fractalNoise" baseFrequency="1.1" numOctaves={1} seed={9} result="g" />
        <feColorMatrix in="g" type="matrix" values={HOLES} result="holes" />
        <feComposite in="d" in2="holes" operator="in" />
      </filter>
    </defs>
  </svg>
);


/** Catmull-Rom -> cubic bezier path. */
const smooth = (p: Pt[]) => {
  if (p.length < 2) return "";
  let d = `M ${p[0][0].toFixed(1)} ${p[0][1].toFixed(1)}`;
  for (let i = 0; i < p.length - 1; i++) {
    const p0 = p[Math.max(0, i - 1)], p1 = p[i], p2 = p[i + 1], p3 = p[Math.min(p.length - 1, i + 2)];
    const c1: Pt = [p1[0] + (p2[0] - p0[0]) / 6, p1[1] + (p2[1] - p0[1]) / 6];
    const c2: Pt = [p2[0] - (p3[0] - p1[0]) / 6, p2[1] - (p3[1] - p1[1]) / 6];
    d += ` C ${c1[0].toFixed(1)} ${c1[1].toFixed(1)} ${c2[0].toFixed(1)} ${c2[1].toFixed(1)} ${p2[0].toFixed(1)} ${p2[1].toFixed(1)}`;
  }
  return d;
};


/** Path draw-on with a boiling pencil edge. p = 0..1 drawn. */
const Line: React.FC<{ d: string; p: number; color: string; width: number; opacity?: number; still?: boolean }> = ({ d, p, color, width, opacity = 1, still }) =>
  p <= 0 ? null : (
    <svg style={FULL} width={1080} height={1920}>
      <path d={d} pathLength={1} strokeDasharray={1} strokeDashoffset={1 - p} fill="none" stroke={color} strokeWidth={width}
        strokeLinecap="round" strokeLinejoin="round" filter={still ? "url(#pencilStill)" : "url(#pencil)"} opacity={opacity} />
    </svg>
  );

const grainSvg = encodeURIComponent(
  "<svg xmlns='http://www.w3.org/2000/svg' width='540' height='960'><filter id='n'><feTurbulence type='fractalNoise' baseFrequency='0.8' numOctaves='2' seed='5'/><feColorMatrix type='saturate' values='0'/></filter><rect width='100%' height='100%' filter='url(#n)'/></svg>");
const PaperGrain: React.FC = () => (
  <AbsoluteFill style={{ backgroundImage: `url("data:image/svg+xml,${grainSvg}")`, backgroundSize: "1080px 1920px", mixBlendMode: "multiply", opacity: 0.05 }} />
);
const Beat: React.FC<{ f: number; from: number; to: number; o?: number; style?: React.CSSProperties; children: React.ReactNode }> = ({ f, from, to, o = 1, style, children }) =>
  f >= from && f < to ? <AbsoluteFill style={{ opacity: o, ...style }}>{children}</AbsoluteFill> : null;


// ---------- v2 marks ----------
const P = { paper: "#F8EFDD", graphite: "#3A322B", sketch: "#8C6B4F", body: "#EAD9BF", fOut: "#F2B544", fIn: "#FBE3A0", fBase: "#E58A2B",
  fWash: "#F6DFA6", stem13: "#D8BF88", leaf13: "#EAD7A6", stem15: "#C9A65E", leaf15: "#E6CC8E", terra: "#A84A24" };

/** Words straight on the paper. No card, no shadow. */
const Write: React.FC<{ cx: number; cy: number; size: number; f: number; on?: [number, number]; terra?: boolean; weight?: number;
  children: React.ReactNode }> = ({ cx, cy, size, f, on, terra, weight = 700, children }) => {
  const r = on ? lerp(f, on[0], on[1], 100, 0) : 0;
  return (
    <div style={{ position: "absolute", left: cx, top: cy, transform: "translate(-50%,-50%)", fontFamily: "Kalam", fontWeight: weight,
      fontSize: size, lineHeight: 1.1, whiteSpace: "nowrap", padding: "0.18em 0.12em", color: terra ? P.terra : P.graphite,
      filter: terra ? undefined : "url(#graphite)", clipPath: `inset(0 ${r}% 0 0)` }}>{children}</div>
  );
};

/** 4.1 lift: paint thinned back to paper. */
const Lift: React.FC<{ id: string; cx: number; cy: number; rx: number; ry: number; o?: number }> = ({ id, cx, cy, rx, ry, o = 1 }) => (
  <svg style={{ ...FULL, opacity: o }} width={1080} height={1920}>
    <defs><radialGradient id={id}><stop offset="0" stopColor={P.paper} stopOpacity={0.62} /><stop offset="0.6" stopColor={P.paper} stopOpacity={0.45} />
      <stop offset="1" stopColor={P.paper} stopOpacity={0} /></radialGradient></defs>
    <ellipse cx={cx} cy={cy} rx={rx} ry={ry} fill={`url(#${id})`} />
  </svg>
);

const flamePath = (bx: number, by: number, h: number, w: number) => {
  const a = w / 2;
  return `M ${bx} ${by} C ${bx - a} ${by - 0.25 * h}, ${bx - 0.6 * a} ${by - 0.62 * h}, ${bx + 2} ${by - h} C ${bx + a} ${by - 0.62 * h}, ${bx + 1.3 * a} ${by - 0.25 * h}, ${bx} ${by} Z`;
};
/** 4.3 flame: flat gouache, painted bottom->top over [a,b], gentle sway. */
const Flame: React.FC<{ id: string; bx: number; by: number; h: number; w: number; f: number; paint: [number, number]; o?: number; wash?: boolean; dx?: number; dy?: number }> =
  ({ id, bx, by, h, w, f, paint, o = 0.9, wash = true, dx = 0, dy = 0 }) => {
  const p = lerp(f, paint[0], paint[1], 0, 1, OUT);
  if (p <= 0) return null;
  const rot = 3 * Math.sin((2 * Math.PI * f) / 46) + 1.5 * Math.sin((2 * Math.PI * f) / 17);
  const sy = 1 + 0.05 * Math.sin((2 * Math.PI * f) / 23);
  const top = by - (h + 6) * p;
  return (
    <svg style={{ ...FULL, transform: `translate(${dx}px, ${dy}px)` }} width={1080} height={1920}>
      <defs>
        <clipPath id={id}><rect x={bx - w * 2} y={top} width={w * 4} height={by - top + 4} /></clipPath>
        <filter id={`${id}d`} {...FR}><feTurbulence type="fractalNoise" baseFrequency="0.08" numOctaves={2} seed={5} result="n" />
          <feDisplacementMap in="SourceGraphic" in2="n" scale={3} xChannelSelector="R" yChannelSelector="G" /></filter>
      </defs>
      {wash && <ellipse cx={bx} cy={by - h / 2} rx={1.5 * w} ry={0.75 * h} fill={P.fWash} fillOpacity={0.22 * p} filter="url(#deckle)" />}
      <g clipPath={`url(#${id})`}>
        <g opacity={o * Math.min(1, p * 1.5)} filter={`url(#${id}d)`}
          transform={`translate(${bx} ${by}) rotate(${rot}) scale(1 ${sy}) translate(${-bx} ${-by})`}>
          <path d={flamePath(bx, by, h, w)} fill={P.fOut} />
          <path d={flamePath(bx, by, h * 0.2, w * 0.9)} fill={P.fBase} fillOpacity={0.6} />
          <path d={flamePath(bx, by, h * 0.55, w * 0.55)} fill={P.fIn} />
        </g>
      </g>
    </svg>
  );
};

/** Pale pencil sketch stroke that stays still once drawn. */
const Sketch: React.FC<{ d: string; f: number; a: number; b: number; w?: number; o?: number }> = ({ d, f, a, b, w = 4.5, o = 1 }) =>
  <Line d={d} p={lerp(f, a, b, 0, 1)} color={P.sketch} width={w} opacity={o} still />;

/** 4.4 leaf, base at (x,y), opens along its length. */
const Leaf: React.FC<{ x: number; y: number; rot: number; s: number; open: number; fill: string; stem: string; fo: number; sway?: number }> =
  ({ x, y, rot, s, open, fill, stem, fo, sway = 0 }) => open <= 0 ? null : (
    <g transform={`translate(${x} ${y}) rotate(${rot + sway}) scale(${s * open} ${s})`}>
      <path d="M 0 0 Q 23 -14 46 0 Q 23 14 0 0 Z" fill={fill} fillOpacity={fo} stroke={stem} strokeWidth={1.5} />
      <path d="M 0 0 L 40 0" stroke={stem} strokeWidth={2} fill="none" />
    </g>
  );

/** Pencil steam curl: drawn upward, then drifts up slowly and thins. */
const steamPath = (x: number, y: number, h: number, amp: number, ph: number) => {
  const pts: Pt[] = [];
  for (let k = 0; k <= 24; k++) { const t = k / 24; pts.push([x + amp * Math.sin(ph + t * 2.6 * Math.PI) * (0.4 + t), y - h * t]); }
  const [lx, ly] = pts[pts.length - 1];
  for (let k = 1; k <= 8; k++) { const a = Math.PI + (k / 8) * 1.6 * Math.PI; pts.push([lx + 16 + 16 * Math.cos(a), ly - 14 + 14 * Math.sin(a)]); }
  return smooth(pts);
};
const Steam: React.FC<{ f: number; a: number; b: number; x: number; y: number; h: number; amp: number; ph: number; w?: number }> = ({ f, a, b, x, y, h, amp, ph, w = 7 }) => {
  const drift = Math.max(0, f - b) * 0.35;
  return (
    <AbsoluteFill style={{ transform: `translateY(${-drift}px)`, opacity: 1 - Math.min(0.5, drift / 80) }}>
      <Line d={steamPath(x, y, h, amp, ph)} p={lerp(f, a, b, 0, 1, OUT)} color={P.sketch} width={w} opacity={1} />
    </AbsoluteFill>
  );
};

// ---------- v3 "cuter": hand-drawn flowers + flowering vines (owner 2026-11-12: "go stronger ... flowers or motifs ... even cutier") ----------
const FL = { stem: "#B8954F", leaf: "#D9C27E", line: "#B07C4F", blush: "#F4C7B5", honey: "#F2C46A", cream: "#FFF4DE", heart: "#C0643A" };
const BACKP = Easing.out(Easing.back(1.8));
/** Catmull-Rom sampled polyline (n points) through control points. */
const sampleCR = (p: Pt[], n = 60): Pt[] => {
  const out: Pt[] = [];
  for (let k = 0; k < n; k++) {
    const u = (k / (n - 1)) * (p.length - 1), i = Math.min(p.length - 2, Math.floor(u)), t = u - i;
    const p0 = p[Math.max(0, i - 1)], p1 = p[i], p2 = p[i + 1], p3 = p[Math.min(p.length - 1, i + 2)];
    const c = (a: number, b: number, cc: number, d: number) => 0.5 * (2 * b + (-a + cc) * t + (2 * a - 5 * b + 4 * cc - d) * t * t + (-a + 3 * b - 3 * cc + d) * t * t * t);
    out.push([c(p0[0], p1[0], p2[0], p3[0]), c(p0[1], p1[1], p2[1], p3[1])]);
  }
  return out;
};
/** A 5-petal storybook blossom, popping open at frame `at`. */
const Blossom: React.FC<{ x: number; y: number; r: number; col: string; f: number; at: number; rot?: number }> = ({ x, y, r, col, f, at, rot = 0 }) => {
  const s = interpolate(f, [at, at + 9], [0, 1], { ...clamp, easing: BACKP });
  if (s <= 0) return null;
  const sway = 4 * Math.sin((2 * Math.PI * (f + x)) / 80);
  return (
    <g transform={`translate(${x} ${y}) rotate(${rot + sway + (1 - s) * -40}) scale(${s})`}>
      {[0, 1, 2, 3, 4].map((k) => (
        <ellipse key={k} cx={0} cy={-r * 0.55} rx={r * 0.36} ry={r * 0.52} transform={`rotate(${k * 72})`}
          fill={col} stroke={FL.line} strokeWidth={2} />
      ))}
      <circle r={r * 0.26} fill={FL.heart} stroke={FL.line} strokeWidth={1.5} />
      <circle cx={-r * 0.08} cy={-r * 0.08} r={r * 0.08} fill={FL.cream} opacity={0.8} />
    </g>
  );
};
const VLeaf: React.FC<{ x: number; y: number; ang: number; s: number; open: number }> = ({ x, y, ang, s, open }) => open <= 0 ? null : (
  <g transform={`translate(${x} ${y}) rotate(${ang}) scale(${s * open} ${s})`}>
    <path d="M 0 0 Q 20 -13 42 0 Q 20 13 0 0 Z" fill={FL.leaf} fillOpacity={0.9} stroke={FL.stem} strokeWidth={1.8} />
    <path d="M 2 0 L 36 0" stroke={FL.stem} strokeWidth={1.5} fill="none" />
  </g>
);
type VineSpec = { pts: Pt[]; a: number; b: number; w?: number; leaves?: [number, 1 | -1, number?][]; flowers?: [number, number, string, number?][] };
/** A vine that grows along pts over [a,b]; leaves open and blossoms pop as the tip passes them. */
const Vine: React.FC<{ v: VineSpec; f: number }> = ({ v, f }) => {
  const P2 = sampleCR(v.pts, 80);
  const p = lerp(f, v.a, v.b, 0, 1, Easing.inOut(Easing.sin));
  if (p <= 0) return null;
  const at = (t: number) => v.a + (v.b - v.a) * t;
  const pt = (t: number) => P2[Math.round(t * (P2.length - 1))];
  const ang = (t: number) => {
    const i = Math.round(t * (P2.length - 1)), j = Math.min(P2.length - 1, i + 1), h = Math.max(0, i - 1);
    return (Math.atan2(P2[j][1] - P2[h][1], P2[j][0] - P2[h][0]) * 180) / Math.PI;
  };
  return (
    <svg style={FULL} width={1080} height={1920}>
      <path d={smooth(v.pts)} pathLength={1} strokeDasharray={1} strokeDashoffset={1 - p} fill="none" stroke={FL.stem}
        strokeWidth={1.3 * (v.w ?? 5)} strokeLinecap="round" filter="url(#pencilStill)" />
      {(v.leaves ?? []).map(([t, side, s], k) => (
        <VLeaf key={`l${k}`} x={pt(t)[0]} y={pt(t)[1]} ang={ang(t) + side * 55} s={1.4 * (s ?? 1)}
          open={lerp(f, at(t), at(t) + 8, 0, 1, OUT)} />))}
      {(v.flowers ?? []).map(([t, r, col, d], k) => (
        <Blossom key={`f${k}`} x={pt(t)[0]} y={pt(t)[1]} r={1.5 * r} col={col} f={f} at={at(t) + (d ?? 2)} rot={k * 23} />))}
    </svg>
  );
};
const Bloom1: React.FC<{ f: number; x: number; y: number; r: number; col: string; at: number }> = (q) => (
  <svg style={FULL} width={1080} height={1920}><Blossom {...q} r={1.5 * q.r} /></svg>
);

/** A closed bud (teardrop) on a vine. */
const Bud: React.FC<{ x: number; y: number; ang: number; s: number; open: number }> = ({ x, y, ang, s, open }) => open <= 0 ? null : (
  <g transform={`translate(${x} ${y}) rotate(${ang - 90}) scale(${s * open})`}>
    <path d="M 0 0 L 0 -10" stroke={FL.stem} strokeWidth={2} />
    <path d="M 0 -10 Q -9 -20 0 -32 Q 9 -20 0 -10 Z" fill={FL.blush} stroke={FL.line} strokeWidth={1.8} />
  </g>
);
/** Three tiny pollen dots around a point. */
const Dots: React.FC<{ x: number; y: number; r: number; o: number }> = ({ x, y, r, o }) => o <= 0 ? null : (
  <g opacity={o}>
    <circle cx={x + r * 1.1} cy={y - r * 0.9} r={3.2} fill={FL.honey} stroke={FL.line} strokeWidth={1} />
    <circle cx={x + r * 1.45} cy={y - r * 0.2} r={2.4} fill={FL.blush} stroke={FL.line} strokeWidth={1} />
    <circle cx={x - r * 1.2} cy={y - r * 1.0} r={2.6} fill={FL.honey} stroke={FL.line} strokeWidth={1} />
  </g>
);
type Vine2Spec = VineSpec & { buds?: [number, 1 | -1][] };
/** Fuller vine: Vine + buds + pollen dots by each flower. */
const Vine2: React.FC<{ v: Vine2Spec; f: number }> = ({ v, f }) => {
  const P2 = sampleCR(v.pts, 80);
  const at = (t: number) => v.a + (v.b - v.a) * t;
  const pt = (t: number) => P2[Math.round(t * (P2.length - 1))];
  const ang = (t: number) => {
    const i = Math.round(t * (P2.length - 1)), j = Math.min(P2.length - 1, i + 1), h = Math.max(0, i - 1);
    return (Math.atan2(P2[j][1] - P2[h][1], P2[j][0] - P2[h][0]) * 180) / Math.PI;
  };
  if (f < v.a) return null;
  return (<>
    <Vine v={v} f={f} />
    <svg style={FULL} width={1080} height={1920}>
      {(v.buds ?? []).map(([t, side], k) => (
        <Bud key={`b${k}`} x={pt(t)[0]} y={pt(t)[1]} ang={ang(t) + side * 60} s={1.3} open={lerp(f, at(t), at(t) + 7, 0, 1, BACKP)} />))}
      {(v.flowers ?? []).map(([t, r], k) => (
        <Dots key={`d${k}`} x={pt(t)[0]} y={pt(t)[1]} r={1.5 * r} o={lerp(f, at(t) + 9, at(t) + 15, 0, 1)} />))}
    </svg>
  </>);
};
/** Doodle butterfly fluttering along a path between frames [a,b]; rests on the last point. */
const Butterfly: React.FC<{ f: number; pts: Pt[]; a: number; b: number; s?: number; col?: string }> = ({ f, pts, a, b, s = 1, col = FL.honey }) => {
  if (f < a) return null;
  const P2 = sampleCR(pts, 60);
  const u = lerp(f, a, b, 0, 1, Easing.inOut(Easing.sin));
  const i = Math.round(u * (P2.length - 1));
  const [x, y] = P2[i];
  const flying = f < b;
  const flap = flying ? 0.35 + 0.65 * Math.abs(Math.sin(f * 0.9)) : 0.75 + 0.2 * Math.sin(f * 0.15);
  const bob = flying ? 6 * Math.sin(f * 0.45) : 0;
  const j = Math.min(P2.length - 1, i + 1);
  const tilt = flying ? Math.max(-25, Math.min(25, (P2[j][0] - x) * 1.5)) : 0;
  const o = lerp(f, a, a + 6, 0, 1);
  return (
    <svg style={{ ...FULL, opacity: o }} width={1080} height={1920}>
      <g transform={`translate(${x} ${y + bob}) rotate(${tilt}) scale(${s})`}>
        <g transform={`scale(${flap} 1)`}>
          <path d="M 0 0 C -22 -30 -46 -18 -38 2 C -32 14 -12 10 0 0 Z" fill={col} stroke={FL.line} strokeWidth={2} />
          <path d="M 0 0 C -18 8 -30 26 -18 30 C -8 32 -2 16 0 0 Z" fill={FL.blush} stroke={FL.line} strokeWidth={2} />
          <path d="M 0 0 C 22 -30 46 -18 38 2 C 32 14 12 10 0 0 Z" fill={col} stroke={FL.line} strokeWidth={2} />
          <path d="M 0 0 C 18 8 30 26 18 30 C 8 32 2 16 0 0 Z" fill={FL.blush} stroke={FL.line} strokeWidth={2} />
          <circle cx={-24} cy={-8} r={3.5} fill={FL.cream} /><circle cx={24} cy={-8} r={3.5} fill={FL.cream} />
        </g>
        <path d="M 0 -12 L 0 20" stroke={FL.line} strokeWidth={4} strokeLinecap="round" />
        <path d="M 0 -12 Q -6 -26 -12 -30 M 0 -12 Q 6 -26 12 -30" stroke={FL.line} strokeWidth={2} fill="none" strokeLinecap="round" />
      </g>
    </svg>
  );
};

const flowersFor = (f: number) => (i: number): React.ReactNode => {
  const B = FL.blush, H = FL.honey, Cr = FL.cream;
  switch (i) {
    case 0: // shot 1 (hook): a vine curls in from the right edge by the window
      return <Vine2 f={f} v={{ pts: [[1090, 760], [1010, 700], [975, 610], [1000, 520], [1050, 480]], a: 30, b: 80,
        leaves: [[0.2, 1], [0.45, -1], [0.7, 1, 0.8]], flowers: [[0.35, 24, H], [0.62, 22, B], [1, 32, B]], buds: [[0.85, -1]] }} />;
    case 2: // shot 3 (doorway): blossoms climb the stone door jamb beside Him
      return <Vine2 f={f} v={{ pts: [[1090, 1500], [1060, 1400], [1060, 1290], [1030, 1200]], a: 262, b: 300, w: 4.5,
        leaves: [[0.25, -1], [0.55, 1], [0.8, -1, 0.8]], flowers: [[0.4, 24, B], [0.7, 22, H], [1, 30, Cr]] }} />;
    case 4: // shot 5 (her question): a quiet little vine along the top-left
      return <Vine2 f={f} v={{ pts: [[-10, 160], [80, 110], [180, 130], [270, 90]], a: 480, b: 530, w: 4.5,
        leaves: [[0.25, 1], [0.55, -1], [0.85, 1, 0.8]], flowers: [[0.4, 22, H], [1, 28, B]], buds: [[0.7, -1]] }} />;
    case 7: // shot 8 (kitchen): blossoms under the lamp on the bare plaster
      return <Vine2 f={f} v={{ pts: [[-10, 860], [80, 820], [170, 840], [260, 790]], a: 975, b: 1010, w: 4.5,
        leaves: [[0.25, -1], [0.55, 1], [0.85, -1, 0.8]], flowers: [[0.4, 22, B], [0.7, 20, Cr], [1, 28, H]] }} />;
    case 9: // shot 10 (careful): a vine along the top edge above the words
      return <Vine2 f={f} v={{ pts: [[1090, 70], [980, 110], [870, 80], [760, 120], [660, 90]], a: 1212, b: 1250, w: 4.5,
        leaves: [[0.2, 1], [0.45, -1], [0.7, 1, 0.8]], flowers: [[0.32, 22, B], [0.6, 20, H], [1, 28, Cr]], buds: [[0.85, 1]] }} />;
    case 13: // shot 14 (hand in His): blossoms along the top edge
      return <Vine2 f={f} v={{ pts: [[-10, 110], [110, 70], [230, 100], [350, 60], [450, 90]], a: 1888, b: 1922, w: 4.5,
        leaves: [[0.2, -1], [0.45, 1], [0.7, -1, 0.8]], flowers: [[0.32, 22, H], [0.6, 22, B], [1, 30, Cr]] }} />;
    case 1: // shot 2: fuller vine curls in from the right edge beside Martha, plus a little branch
      return (<>
        <Vine2 f={f} v={{ pts: [[1090, 900], [1010, 830], [955, 730], [975, 620], [1040, 570]], a: 186, b: 232,
          leaves: [[0.2, 1], [0.42, -1], [0.62, 1], [0.82, -1, 0.8]], flowers: [[0.32, 28, B], [0.55, 24, H], [0.75, 22, Cr], [1, 34, H]], buds: [[0.12, -1], [0.88, 1]] }} />
        <Vine2 f={f} v={{ pts: [[1090, 1060], [1030, 1030], [1000, 980]], a: 200, b: 236, w: 4, leaves: [[0.5, 1, 0.8]], flowers: [[1, 26, B]] }} />
      </>);
    case 3: // shot 4: blossoms grow up from the bottom-left corner while Mary listens + a butterfly
      return (<>
        <Vine2 f={f} v={{ pts: [[-10, 1880], [60, 1760], [70, 1640], [140, 1560], [210, 1540]], a: 345, b: 400,
          leaves: [[0.18, -1], [0.38, 1], [0.58, -1, 0.85], [0.8, 1, 0.8]], flowers: [[0.28, 26, H], [0.5, 24, B], [0.72, 22, Cr], [1, 34, B]], buds: [[0.1, 1], [0.64, 1]] }} />
        <Butterfly f={f} pts={[[-40, 900], [150, 780], [260, 880], [330, 1050], [250, 1300], [205, 1470]]} a={350} b={440} s={0.9} />
      </>);
    case 5: // shot 6: flowers pop beside Jesus on "Her name." and "Twice."
      return (<>
        <Vine2 f={f} v={{ pts: [[1090, 520], [1030, 430], [995, 330], [1015, 220], [1060, 160]], a: 712, b: 740, w: 4.5,
          leaves: [[0.25, 1], [0.5, -1], [0.75, 1, 0.8]], flowers: [[0.4, 24, H, 0], [0.7, 30, B, 0], [1, 26, Cr, 0]], buds: [[0.15, -1]] }} />
        <Bloom1 f={f} x={935} y={330} r={26} col={H} at={790} />
        <Bloom1 f={f} x={960} y={250} r={18} col={B} at={798} />
      </>);
    case 6: // shot 7: a small vine climbs the left edge while He says her name
      return <Vine2 f={f} v={{ pts: [[-10, 1360], [50, 1260], [40, 1140], [90, 1040], [80, 940]], a: 846, b: 890, w: 4.5,
        leaves: [[0.2, 1], [0.45, -1], [0.7, 1, 0.8]], flowers: [[0.35, 24, B], [0.62, 22, H], [1, 30, B]], buds: [[0.85, -1]] }} />;
    case 8: // shot 9: fuller vine across the top-left as the lamp over Mary lights
      return <Vine2 f={f} v={{ pts: [[-10, 330], [90, 280], [190, 300], [300, 240], [420, 210], [520, 150]], a: 1100, b: 1150,
        leaves: [[0.12, -1], [0.3, 1], [0.48, -1], [0.66, 1], [0.86, -1, 0.8]], flowers: [[0.2, 24, B], [0.4, 28, H], [0.6, 22, Cr], [0.8, 26, B], [1, 30, H]], buds: [[0.5, 1], [0.92, -1]] }} />;
    case 10: // shot 11: flowering vine from the top-left corner + a butterfly
      return (<>
        <Vine2 f={f} v={{ pts: [[-10, 120], [100, 160], [170, 260], [260, 300], [380, 280], [470, 330]], a: 1300, b: 1360,
          leaves: [[0.14, 1], [0.32, -1], [0.52, 1], [0.72, -1], [0.9, 1, 0.8]], flowers: [[0.24, 26, H], [0.44, 22, B], [0.64, 26, Cr], [0.84, 22, H], [1, 32, B]], buds: [[0.08, -1], [0.56, -1]] }} />
        <Butterfly f={f} pts={[[1120, 250], [940, 180], [820, 300], [700, 240], [600, 330], [505, 300]]} a={1350} b={1440} s={0.85} col={FL.blush} />
      </>);
    case 11: // shot 12: blossoms by the lamp + a vine from the left edge as the lamp over Martha lights
      return (<>
        <Bloom1 f={f} x={985} y={360} r={22} col={B} at={1597} />
        <Bloom1 f={f} x={1020} y={372} r={16} col={H} at={1601} />
        <Vine2 f={f} v={{ pts: [[-10, 980], [70, 880], [80, 760], [150, 680], [230, 660]], a: 1583, b: 1609, w: 4.5,
          leaves: [[0.25, 1], [0.5, -1], [0.75, 1, 0.8]], flowers: [[0.38, 24, H], [0.66, 22, B], [1, 30, Cr]] }} />
      </>);
    case 12: // family sprig blossoms (same local frame as the sprig)
      return f >= 1757 && f < 1884 ? (
        <AbsoluteFill style={{ opacity: lerp(f, 1872, 1884, 1, 0), transform: "translate(-175px, 25px) scale(1.3)", transformOrigin: "215px 235px" }}>
          <svg style={FULL} width={1080} height={1920}>
            <Blossom x={522} y={172} r={24} col={B} f={f} at={1852} />
            <Blossom x={384} y={168} r={18} col={H} f={f} at={1860} />
            <Blossom x={270} y={198} r={16} col={Cr} f={f} at={1866} />
            <Blossom x={470} y={192} r={14} col={B} f={f} at={1870} />
          </svg>
        </AbsoluteFill>) : null;
    case 14: // ending: fuller flower clusters from both bottom corners + a butterfly that settles on a flower
      return (<>
        <Vine2 f={f} v={{ pts: [[-10, 1930], [50, 1820], [60, 1700], [120, 1640]], a: 2102, b: 2138,
          leaves: [[0.25, 1], [0.5, -1], [0.75, 1, 0.8]], flowers: [[0.35, 26, H], [0.65, 24, Cr], [1, 36, B]], buds: [[0.12, -1]] }} />
        <Vine2 f={f} v={{ pts: [[90, 1930], [140, 1850], [210, 1800], [280, 1790]], a: 2112, b: 2142, w: 4, leaves: [[0.4, -1, 0.8], [0.75, 1, 0.8]], flowers: [[0.55, 22, B], [1, 30, Cr]] }} />
        <Vine2 f={f} v={{ pts: [[1090, 1930], [1030, 1830], [1020, 1720], [960, 1660]], a: 2108, b: 2144,
          leaves: [[0.25, -1], [0.5, 1], [0.75, -1, 0.8]], flowers: [[0.35, 24, B], [0.65, 22, Cr], [1, 36, H]], buds: [[0.12, 1]] }} />
        <Vine2 f={f} v={{ pts: [[990, 1930], [940, 1860], [870, 1820]], a: 2116, b: 2146, w: 4, leaves: [[0.5, 1, 0.8]], flowers: [[1, 28, B]] }} />
        <Butterfly f={f} pts={[[1120, 1250], [980, 1180], [1000, 1360], [1010, 1500], [972, 1612]]} a={2122} b={2177} s={0.9} />
      </>);
    default:
      return null;
  }
};

const LAMP = {
  shelf: "M 92 416 L 348 414 L 349 434 L 93 436 Z",
  br1: "M 132 436 Q 134 462 150 468 L 158 436", br2: "M 296 436 Q 298 462 284 468 L 276 436",
  body: "M 112 340 Q 150 348 182 344 Q 200 332 245 330 Q 290 332 304 352 Q 312 380 284 396 Q 235 410 190 400 Q 150 386 128 358 Q 116 352 112 340",
  rim: "M 200 336 Q 245 344 290 338", handle: "M 304 350 Q 340 336 344 362 Q 344 388 300 384", foot: "M 196 402 L 192 412 L 268 412 L 264 402",
};

const extrasFor = (f: number) => (i: number): React.ReactNode => {
  switch (i) {
    case 0: // T1 hook, fully there on frame 0
      return f < 179 ? (<>
        <AbsoluteFill style={{ transform: `scale(${lerp(f, 0, 6, 1.04, 1, OUT)})`, transformOrigin: "400px 240px" }}>
          <Lift id="l1" cx={400} cy={240} rx={370} ry={95} />
          <Write cx={400} cy={240} size={76} f={f}>Does anyone care?</Write>
        </AbsoluteFill>
        <Steam f={f} a={20} b={58} x={880} y={1060} h={330} amp={22} ph={0} />
        <Steam f={f} a={40} b={80} x={940} y={1050} h={260} amp={18} ph={2} w={5.5} />
        <Steam f={f} a={98} b={130} x={830} y={1070} h={220} amp={16} ph={4} w={5.5} />
        </>) : null;
    case 1: // T2 "Martha"
      return (<>
        <Steam f={f} a={182} b={222} x={960} y={1480} h={360} amp={24} ph={1} />
        <Steam f={f} a={205} b={245} x={1010} y={1440} h={260} amp={16} ph={3} w={5.5} />
        {f >= 190 && <Write cx={565} cy={208} size={72} f={f} on={[190, 200]}>Martha</Write>}
      </>);
    case 3: // T3 "Mary" (D1 sway dropped: the art's own lamp flames already move in this clip)
      return f >= 384 && f < 452 ? <AbsoluteFill style={{ opacity: lerp(f, 440, 452, 1, 0) }}><Write cx={420} cy={440} size={88} f={f} on={[384, 392]}>Mary</Write></AbsoluteFill> : null;
    case 6: // T4 "Martha, Martha," in His colour
      return f >= 843 && f < 952 ? (
        <AbsoluteFill style={{ opacity: lerp(f, 940, 952, 1, 0) }}>
          <div style={{ position: "absolute", left: 515, top: 290, transform: "translate(-50%,-50%)", display: "flex", gap: 24 }}>
            {[[843, 857], [868, 882]].map(([a, b], k) => (
              <div key={k} style={{ fontFamily: "Kalam", fontWeight: 700, fontSize: 104, color: P.terra, whiteSpace: "nowrap",
                clipPath: `inset(0 ${lerp(f, a, b, 100, 0)}% 0 0)` }}>Martha,</div>))}
          </div>
        </AbsoluteFill>) : null;
    case 7: // D2 kitchen lamp sketched, D3 lit + T5 "one thing" (leaves under the C8 bloom with the kitchen)
      return f >= 964 ? (
        <AbsoluteFill style={{ opacity: lerp(f, 1059, 1071, 1, 0) }}>
          <AbsoluteFill style={{ transform: "scale(1.5)", transformOrigin: "140px 300px" }}>
          <Sketch d={LAMP.shelf} f={f} a={964} b={972} />
          <Sketch d={LAMP.br1} f={f} a={966} b={972} w={2.5} />
          <Sketch d={LAMP.br2} f={f} a={968} b={974} w={2.5} />
          <svg style={{ ...FULL, opacity: lerp(f, 986, 996, 0, 0.35) }} width={1080} height={1920}><path d={LAMP.body} fill={P.body} /></svg>
          <Sketch d={LAMP.body} f={f} a={972} b={990} />
          <Sketch d={LAMP.rim} f={f} a={986} b={991} />
          <Sketch d={LAMP.handle} f={f} a={988} b={994} />
          <Sketch d={LAMP.foot} f={f} a={991} b={996} />
          <Sketch d={flamePath(118, 336, 74, 30)} f={f} a={994} b={1000} w={2} />
          <Flame id="fk" bx={118} by={336} h={74} w={30} f={f} paint={[1009, 1020]} />
          </AbsoluteFill>
          <Lift id="l5" cx={300} cy={600} rx={260} ry={85} o={lerp(f, 1004, 1010, 0, 1)} />
          {f >= 1009 && <Write cx={300} cy={600} size={96} f={f} on={[1009, 1022]} terra>one thing</Write>}
        </AbsoluteFill>) : null;
    case 8: // D4 Mary's flame coloured in on "good part"
      return <Flame id="fm" bx={654} by={180} h={100} w={28} f={f} paint={[1110, 1124]} dx={lerp(f, 1083, 1207, -10, 4)} dy={lerp(f, 1083, 1207, 46, 0)} />;
    case 9: // T6 "careful" means full of worry
      return f >= 1210 && f < 1283 ? (
        <AbsoluteFill style={{ opacity: lerp(f, 1271, 1283, 1, 0) }}>
          <Write cx={755} cy={235} size={84} f={f} on={[1210, 1226]}>“careful”</Write>
          <AbsoluteFill style={{ opacity: lerp(f, 1236, 1242, 0, 1) }}><Write cx={755} cy={305} size={40} weight={400} f={f}>means</Write></AbsoluteFill>
          <Write cx={755} cy={375} size={64} f={f} on={[1245, 1266]}>full of worry</Write>
        </AbsoluteFill>) : null;
    case 11: // D5 Martha's flame, a silent yes after "did He care?"
      return <Flame id="fmm" bx={750} by={298} h={104} w={35} f={f} paint={[1578, 1592]} dx={interpolate(f, [1595, 1626], [0, 8])} dy={interpolate(f, [1595, 1626], [0, -16])} />;
    case 12: { // D6 gold sprig, a leaf per name
      if (f < 1757 || f >= 1884) return null;
      const sw = (k: number) => 2 * Math.sin((2 * Math.PI * (f + 23 * k)) / 70);
      return (
        <AbsoluteFill style={{ opacity: lerp(f, 1872, 1884, 1, 0) }}>
          <AbsoluteFill style={{ transform: "translate(-175px, 25px) scale(1.3)", transformOrigin: "215px 235px" }}>
          <Line d="M 215 235 C 280 180 360 165 430 185 C 470 200 500 195 522 176" p={lerp(f, 1757, 1781, 0, 1, SINE)} color={P.stem15} width={3.5} still />
          <svg style={FULL} width={1080} height={1920}>
            <Leaf x={321} y={182} rot={-65} s={1} open={lerp(f, 1782, 1792, 0, 1, OUT)} fill={P.leaf15} stem={P.stem15} fo={0.9} sway={f > 1792 ? sw(0) : 0} />
            <Leaf x={430} y={185} rot={50} s={1} open={lerp(f, 1812, 1822, 0, 1, OUT)} fill={P.leaf15} stem={P.stem15} fo={0.9} sway={f > 1822 ? sw(1) : 0} />
            <Leaf x={522} y={176} rot={-25} s={1} open={lerp(f, 1839, 1849, 0, 1, OUT)} fill={P.leaf15} stem={P.stem15} fo={0.9} sway={f > 1849 ? sw(2) : 0} />
          </svg>
          </AbsoluteFill>
        </AbsoluteFill>);
    }
    case 14: // T7 last words in the doorway light + D7 one leaf
      return f >= 2076 ? (<>
        <Write cx={628} cy={256} size={60} f={f} on={[2076, 2084]} terra>And He</Write>
        <Write cx={628} cy={318} size={60} f={f} on={[2085, 2099]} terra>loved her.</Write>
        {/* D7 sprig dropped (2026-11-12): no clean room between the words and His head; the family shot carries the gold leaves */}
      </>) : null;
    default:
      return null;
  }
};

export const MaryMarthaV4: React.FC = () => {
  useFonts();
  const f = useCurrentFrame();
  return (
    <AbsoluteFill style={{ background: P.paper }}>
      <Defs f={f} />
      <Shots f={f} extras={(i) => <>{extrasFor(f)(i)}{flowersFor(f)(i)}</>} />
      <TransitionEdges f={f} />
      <PaperGrain />
    </AbsoluteFill>
  );
};
