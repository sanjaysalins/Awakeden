// Mary and Martha (Warm Storybook POC) - motion layer v1 ("one pencil line").
// Design: poc_warm_storybook_style/motion_v1/MOTION_DESIGN.md (Fable, 2026-11-12).
// Pencil = Martha's side, terracotta (His mantle) = His words / "one thing" / the last line.
// Thread: a small pencil knot (her worry) -> lasso of "many things" -> one calm line -> named "worry" -> unties under "And He loved her."
// The 15 Kling clips are laid as separate layers (6 cuts overlap). Audio is muxed afterwards from MARY_MARTHA_SCORED_v2.mp4.
// All frames are ABSOLUTE comp frames (30 fps).
import React from "react";
import { AbsoluteFill, Easing, OffthreadVideo, Sequence, interpolate, staticFile, useCurrentFrame } from "remotion";
import { useFonts } from "./TalithaCumi";

export const MM_FPS = 30;
export const MM_FRAMES = 2148;

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
const SWATCH_OPACITY = 0.8; // ep16 owner asked for see-through carriers; spec said .94

// ---------- clips + transitions ----------
// [clip, startFrame, endFrame]; cut frames from the spec (round(s*30)).
const CUTS = [0, 179, 261, 329, 464, 668, 837, 954, 1059, 1208, 1313, 1512, 1616, 1844, 1920, MM_FRAMES];
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

const Shots: React.FC<{ f: number }> = ({ f }) => (
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
          <AbsoluteFill style={style}><Clip name={name} /></AbsoluteFill>
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

/** Cream gouache dab. paint=[a,b] -> left-to-right ragged wipe. */
const Swatch: React.FC<{ id: string; b: Box; f: number; paint?: [number, number]; opacity?: number }> = ({ id, b, f, paint, opacity = SWATCH_OPACITY }) => {
  const x = b.x1 + 14, y = b.y1 + 14, w = b.x2 - b.x1 - 28, h = b.y2 - b.y1 - 28;
  const tx = x + 0.7 * w, tw = Math.min(x + w + 40, 950) - tx, th = 0.55 * h, ty = y + (h - th) / 2;
  const p = paint ? lerp(f, paint[0], paint[1], 0, 1) : 1;
  return (
    <svg style={FULL} width={1080} height={1920}>
      {paint && (
        <mask id={id} maskUnits="userSpaceOnUse" x={0} y={0} width={1080} height={1920}>
          <rect x={b.x1 - 30} y={b.y1 - 40} width={Math.max(0.01, p * (b.x2 - b.x1 + 60))} height={b.y2 - b.y1 + 80} fill="white" filter="url(#deckle)" />
        </mask>
      )}
      <g mask={paint ? `url(#${id})` : undefined} filter="url(#deckle)">
        <rect x={x} y={y + 5} width={w} height={h} rx={18} fill={C.shade} fillOpacity={0.25} />
        <rect x={x} y={y} width={w} height={h} rx={18} fill={C.paper} fillOpacity={opacity} />
        {tw > 0 && <rect x={tx} y={ty} width={tw} height={th} rx={12} fill={C.paper} fillOpacity={opacity * 0.4} />}
      </g>
    </svg>
  );
};

/** Hand-speed linear write-on (left-to-right clip). terra = His colour, solid gouache (no grain). */
const Write: React.FC<{ cx: number; cy: number; size: number; f: number; on?: [number, number]; terra?: boolean;
  weight?: number; rot?: number; children: React.ReactNode; left?: boolean }> = ({ cx, cy, size, f, on, terra, weight = 700, rot = 0, children, left }) => {
  const r = on ? lerp(f, on[0], on[1], 100, 0) : 0;
  return (
    <div style={{
      position: "absolute", left: cx, top: cy, transform: `translate(${left ? "0" : "-50%"},-50%) rotate(${rot}deg)`,
      fontFamily: "Kalam", fontWeight: weight, fontSize: size, lineHeight: 1.1, whiteSpace: "nowrap",
      padding: "0.18em 0.12em", color: terra ? C.terra : C.graphite,
      filter: terra ? undefined : "url(#graphite)",
      textShadow: terra ? "0 2px 0 rgba(120,50,20,.25)" : "0 0 12px rgba(248,239,221,.85)",
      clipPath: `inset(0 ${r}% 0 0)`,
    }}>{children}</div>
  );
};
const T: React.FC<{ children: React.ReactNode }> = ({ children }) => <span style={{ color: C.terra, filter: "none" }}>{children}</span>;

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

/** The knot: 120 loop points + 12 tail points (spec 5.2). */
const knotPts = (cx: number, cy: number, s: number): Pt[] => {
  const pts: Pt[] = [];
  for (let i = 0; i < 120; i++) {
    const t = i / 119;
    const th = 2 * Math.PI * 5.5 * t;
    const r = 26 + 46 * Math.abs(Math.sin(2 * Math.PI * 1.7 * t + 0.6));
    pts.push([cx + s * (1.15 * r * Math.cos(th) + 10 * Math.sin(2 * Math.PI * 3.1 * t)),
      cy + s * (0.9 * r * Math.sin(th) + 8 * Math.cos(2 * Math.PI * 2.3 * t))]);
  }
  const [lx, ly] = pts[119];
  for (let j = 1; j <= 12; j++) {
    const u = j / 12;
    pts.push([lx + s * (60 * u + 12 * Math.sin(Math.PI * u)), ly + s * (60 * u * u + 10 * u)]);
  }
  return pts;
};

/** Path draw-on with a boiling pencil edge. p = 0..1 drawn. */
const Line: React.FC<{ d: string; p: number; color: string; width: number; opacity?: number; still?: boolean }> = ({ d, p, color, width, opacity = 1, still }) =>
  p <= 0 ? null : (
    <svg style={FULL} width={1080} height={1920}>
      <path d={d} pathLength={1} strokeDasharray={1} strokeDashoffset={1 - p} fill="none" stroke={color} strokeWidth={width}
        strokeLinecap="round" strokeLinejoin="round" filter={still ? "url(#pencilStill)" : "url(#pencil)"} opacity={opacity} />
    </svg>
  );
const under = (x1: number, y1: number, x2: number, y2: number) => `M ${x1} ${y1} Q ${(x1 + x2) / 2} ${(y1 + y2) / 2 + 6} ${x2} ${y2}`;

/** The lasso: 5 loose ~1.15-turn loops round the "many things", then a tail (spec 5.4). */
const lassoPts = (): Pt[] => {
  const things: [number, number, number, number][] = [[200, 1050, 170, 125], [600, 930, 140, 225], [841, 915, 135, 105], [870, 1185, 115, 92], [627, 1238, 150, 125]];
  const pts: Pt[] = [];
  things.forEach(([cx, cy, rx, ry], k) => {
    const a0 = (5 * Math.PI) / 4;
    const n = 44;
    for (let i = 0; i <= n; i++) {
      const a = a0 + (i / n) * 1.15 * 2 * Math.PI;
      const wob = 1 + 0.06 * Math.sin(3 * a + k);
      pts.push([cx + rx * wob * Math.cos(a), cy + ry * wob * Math.sin(a)]);
    }
  });
  const [lx, ly] = pts[pts.length - 1];
  for (let j = 1; j <= 6; j++) { const u = j / 6; pts.push([lx + (400 - lx) * u, ly + (1400 - ly) * u - 30 * Math.sin(Math.PI * u)]); }
  return pts;
};
const LASSO = smooth(lassoPts());
const KNOT1 = smooth(knotPts(160, 440, 1.0));
const KNOT6 = knotPts(858, 522, 0.8);
const KNOT9 = knotPts(745, 1290, 0.6);
// beat 6: underline runs into the knot = one stroke
const KNOT6_D = smooth([[772, 434], [850, 436], [925, 428], ...KNOT6]);
// calm line target for the untie: 132 points along M 150 1456 Q 520 1470 890 1448
const CALM: Pt[] = Array.from({ length: 132 }, (_, i) => {
  const t = i / 131;
  return [(1 - t) * (1 - t) * 150 + 2 * (1 - t) * t * 520 + t * t * 890, (1 - t) * (1 - t) * 1456 + 2 * (1 - t) * t * 1470 + t * t * 1448];
});
const hexLerp = (a: string, b: string, t: number) => {
  const pa = [1, 3, 5].map((i) => parseInt(a.slice(i, i + 2), 16)), pb = [1, 3, 5].map((i) => parseInt(b.slice(i, i + 2), 16));
  return `rgb(${pa.map((v, i) => Math.round(v + (pb[i] - v) * t)).join(",")})`;
};

const grainSvg = encodeURIComponent(
  "<svg xmlns='http://www.w3.org/2000/svg' width='540' height='960'><filter id='n'><feTurbulence type='fractalNoise' baseFrequency='0.8' numOctaves='2' seed='5'/><feColorMatrix type='saturate' values='0'/></filter><rect width='100%' height='100%' filter='url(#n)'/></svg>");
const PaperGrain: React.FC = () => (
  <AbsoluteFill style={{ backgroundImage: `url("data:image/svg+xml,${grainSvg}")`, backgroundSize: "1080px 1920px", mixBlendMode: "multiply", opacity: 0.05 }} />
);
const Beat: React.FC<{ f: number; from: number; to: number; o?: number; style?: React.CSSProperties; children: React.ReactNode }> = ({ f, from, to, o = 1, style, children }) =>
  f >= from && f < to ? <AbsoluteFill style={{ opacity: o, ...style }}>{children}</AbsoluteFill> : null;

export const MaryMarthaV1: React.FC = () => {
  useFonts();
  const f = useCurrentFrame();
  // untie (9b)
  const knot9 = KNOT9.map((q, i) => {
    const p = INOUT(Math.min(1, Math.max(0, (f - 2030 - 6 * (1 - i / 131)) / 18)));
    return [q[0] + (CALM[i][0] - q[0]) * p, q[1] + (CALM[i][1] - q[1]) * p] as Pt;
  });
  const u9 = lerp(f, 2030, 2054, 0, 1, INOUT);
  return (
    <AbsoluteFill style={{ background: C.paper }}>
      <Defs f={f} />
      <Shots f={f} />
      <TransitionEdges f={f} />

      {/* 1a HOOK - fully there on frame 0, leaves on the hard cut */}
      <Beat f={f} from={0} to={179} style={{ transform: `scale(${lerp(f, 0, 6, 1.05, 1, OUT)})`, transformOrigin: "400px 240px" }}>
        <Swatch id="m1a" b={{ x1: 70, y1: 170, x2: 730, y2: 310 }} f={f} />
        <Write cx={400} cy={240} size={76} f={f}>Does anyone care?</Write>
      </Beat>
      {/* 1b the knot is born */}
      <Beat f={f} from={20} to={179}>
        <Line d={KNOT1} p={f < 98 ? lerp(f, 20, 58, 0, 0.6) : lerp(f, 98, 122, 0.6, 1)} color={C.sepia} width={5} />
      </Beat>

      {/* 2 "Martha" label */}
      <Beat f={f} from={186} to={261}>
        <Swatch id="m2" b={{ x1: 600, y1: 1340, x2: 950, y2: 1470 }} f={f} paint={[186, 191]} />
        <Write cx={775} cy={1405} size={92} f={f} on={[190, 200]}>Martha</Write>
      </Beat>

      {/* 3 "Mary" label + tiny arrow */}
      <Beat f={f} from={380} to={452} o={lerp(f, 440, 452, 1, 0)}>
        <Swatch id="m3" b={{ x1: 270, y1: 375, x2: 540, y2: 492 }} f={f} paint={[380, 385]} />
        <Write cx={405} cy={432} size={96} f={f} on={[384, 392]}>Mary</Write>
        <Line d="M 405 496 Q 392 522 384 544" p={lerp(f, 393, 400, 0, 1, OUT)} color={C.sepia} width={4} />
        <Line d="M 372 532 L 384 546 L 394 530" p={lerp(f, 399, 402, 0, 1)} color={C.sepia} width={4} />
      </Beat>

      {/* 4 "Martha, Martha," (KJV) in His colour, following His voice */}
      <Beat f={f} from={841} to={952} o={lerp(f, 940, 952, 1, 0)}>
        <Swatch id="m4" b={{ x1: 130, y1: 190, x2: 900, y2: 390 }} f={f} paint={[841, 846]} />
        <div style={{ position: "absolute", left: 515, top: 290, transform: "translate(-50%,-50%)", display: "flex", gap: 24 }}>
          <div style={{ position: "relative", fontFamily: "Kalam", fontWeight: 700, fontSize: 104, color: C.terra, textShadow: "0 2px 0 rgba(120,50,20,.25)",
            clipPath: `inset(0 ${lerp(f, 843, 857, 100, 0)}% 0 0)`, whiteSpace: "nowrap" }}>Martha,</div>
          <div style={{ position: "relative", fontFamily: "Kalam", fontWeight: 700, fontSize: 104, color: C.terra, textShadow: "0 2px 0 rgba(120,50,20,.25)",
            clipPath: `inset(0 ${lerp(f, 868, 882, 100, 0)}% 0 0)`, whiteSpace: "nowrap" }}>Martha,</div>
        </div>
      </Beat>

      {/* 5a "many things" + the lasso */}
      <Beat f={f} from={963} to={1008} o={lerp(f, 998, 1008, 1, 0)}>
        <Line d={LASSO} p={lerp(f, 964, 994, 0, 1)} color={C.sepia} width={8} />
      </Beat>
      <Beat f={f} from={963} to={1120} o={Math.min(lerp(f, 1108, 1120, 1, 0), f < 1009 ? 1 : 1)}>
        <AbsoluteFill style={{ opacity: f < 1006 ? 1 : lerp(f, 1006, 1010, 0.7, 1) }}>
          <Swatch id="m5" b={{ x1: 70, y1: 220, x2: 570, y2: 390 }} f={f} paint={[963, 967]} />
        </AbsoluteFill>
        <AbsoluteFill style={{ opacity: lerp(f, 998, 1008, 1, 0) }}>
          <Write cx={320} cy={300} size={84} f={f} on={[964, 977]}>many things</Write>
        </AbsoluteFill>
        {/* 5b "one thing" + the first calm line; holds across the C8 bloom */}
        <Beat f={f} from={1009} to={1120}>
          <Write cx={320} cy={295} size={104} f={f} on={[1009, 1022]} terra>one thing</Write>
          <Line d="M 112 372 Q 320 380 530 364" p={lerp(f, 1024, 1034, 0, 1, OUT)} color={C.terra} width={7} />
        </Beat>
      </Beat>

      {/* 6 "careful" means full of worry -> underline ties the knot */}
      <Beat f={f} from={1208} to={1310} o={lerp(f, 1298, 1310, 1, 0)}>
        <Swatch id="m6" b={{ x1: 440, y1: 185, x2: 950, y2: 455 }} f={f} paint={[1208, 1213]} />
        <Write cx={695} cy={250} size={88} f={f} on={[1210, 1226]}>“careful”</Write>
        <AbsoluteFill style={{ opacity: lerp(f, 1236, 1242, 0, 1) }}>
          <Write cx={695} cy={320} size={42} weight={400} f={f}>means</Write>
        </AbsoluteFill>
        <Write cx={695} cy={392} size={74} f={f} on={[1245, 1266]}>full of worry</Write>
        <Line d={KNOT6_D} p={lerp(f, 1262, 1288, 0, 1)} color={C.sepia} width={4} />
      </Beat>

      {/* 7 "Did He care?" - same hand and place as the hook */}
      <Beat f={f} from={1545} to={1612} o={lerp(f, 1600, 1612, 1, 0)}>
        <Swatch id="m7" b={{ x1: 90, y1: 170, x2: 700, y2: 310 }} f={f} paint={[1545, 1550]} />
        <Write cx={395} cy={240} size={92} f={f} on={[1549, 1569]}>Did <T>He</T> care?</Write>
      </Beat>

      {/* 8 small John 11:5 tag */}
      <Beat f={f} from={1665} to={1832} o={Math.min(lerp(f, 1665, 1677, 0, 1), lerp(f, 1820, 1832, 1, 0))}
        style={{ transform: "rotate(-1.5deg)", transformOrigin: "200px 206px" }}>
        <Swatch id="m8" b={{ x1: 70, y1: 172, x2: 330, y2: 240 }} f={f} />
        <Write cx={200} cy={206} size={40} weight={400} f={f}>John 11:5</Write>
      </Beat>

      {/* 9a "He saw her worry." + underline into a small knot ; 9b the knot unties under "And He loved her." */}
      <Beat f={f} from={1968} to={MM_FRAMES}>
        <Swatch id="m9" b={{ x1: 110, y1: 1235, x2: 930, y2: 1485 }} f={f} paint={[1968, 1974]} />
        <Write cx={160} cy={1292} size={64} f={f} on={[1974, 2002]} left>He saw her worry.</Write>
        <Line d={under(540, 1327, 690, 1323)} p={lerp(f, 1996, 2002, 0, 1)} color={C.sepia} width={4} opacity={lerp(f, 2030, 2040, 1, 0)} />
        {f < 2030
          ? <Line d={smooth(KNOT9)} p={lerp(f, 2002, 2016, 0, 1)} color={C.sepia} width={4} />
          : <Line d={smooth(knot9)} p={1} color={hexLerp(C.sepia, C.terra, u9)} width={3 + 4 * u9} still={f >= 2054} />}
        <Write cx={520} cy={1392} size={100} f={f} on={[2034, 2057]} terra>And He loved her.</Write>
      </Beat>

      <PaperGrain />
    </AbsoluteFill>
  );
};
