// Episode 16 "Let the Little Children" - motion layer v2 ("the storyteller's desk").
// Design: poc_living_water_ink_style_test/swirls_episode_16_let_the_little_children/motion_v2/MOTION_DESIGN.md (Fable).
// Grey pencil on paper = the world's "no"; Jesus-blue watercolour = His "yes".
// Thread: the "not now" slip (hook -> rebuked -> washed over at "Look"). Spine: small "a touch" -> big blue "His arms."
// All frames are ABSOLUTE comp frames (30 fps). Base video/audio untouched.
import React from "react";
import { AbsoluteFill, Easing, OffthreadVideo, interpolate, staticFile, useCurrentFrame } from "remotion";
import { useFonts } from "./TalithaCumi";
import { EP16_FPS, EP16_FRAMES } from "./Ep16Children";

export { EP16_FPS, EP16_FRAMES };

const clamp = { extrapolateLeft: "clamp", extrapolateRight: "clamp" } as const;
const OUT = Easing.out(Easing.cubic);
const IN = Easing.in(Easing.cubic);
const BACK = Easing.out(Easing.back(1.6));
const boilSeed = (f: number) => [3, 11, 27][Math.floor(f / 5) % 3];
const lerp = (f: number, a: number, b: number, from: number, to: number, easing?: (t: number) => number) =>
  interpolate(f, [a, b], [from, to], { ...clamp, easing });
/** opacity: 0->1 over [inA,inB], 1->0 over [outA,outB] */
const fade = (f: number, inA: number, inB: number, outA = 1e9, outB = 1e9 + 1) =>
  Math.min(lerp(f, inA, inB, 0, 1), lerp(f, outA, outB, 1, 0));

const C = {
  paper: "#F6EEDC", shade: "#E6D8BC", graphite: "#2E2A27", slip: "#E4DFD3", slipText: "#3A3A3C",
  sienna: "#9A4A2B", blue: "#3D6497", blueEdge: "#2B4A75", mottle: "#6E93C4", cream: "#FBF4E4",
};
type Box = { x1: number; y1: number; x2: number; y2: number };
const FULL: React.CSSProperties = { position: "absolute", left: 0, top: 0, width: 1080, height: 1920, overflow: "visible" };
const FR = { x: "-15%", y: "-15%", width: "130%", height: "130%", colorInterpolationFilters: "sRGB" as const };
const HOLES = "0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  -2.2 0 0 0 1.85";

const Defs: React.FC<{ f: number }> = ({ f }) => (
  <svg width={0} height={0} style={{ position: "absolute" }}>
    <defs>
      <filter id="deckle" {...FR}>
        <feTurbulence type="fractalNoise" baseFrequency="0.022" numOctaves={3} seed={7} result="n" />
        <feDisplacementMap in="SourceGraphic" in2="n" scale={16} xChannelSelector="R" yChannelSelector="G" />
      </filter>
      <filter id="tear" {...FR}>
        <feTurbulence type="fractalNoise" baseFrequency="0.022" numOctaves={3} seed={7} result="n" />
        <feDisplacementMap in="SourceGraphic" in2="n" scale={9} xChannelSelector="R" yChannelSelector="G" />
      </filter>
      <filter id="wash" {...FR}>
        <feTurbulence type="fractalNoise" baseFrequency="0.009 0.016" numOctaves={3} seed={4} result="n" />
        <feDisplacementMap in="SourceGraphic" in2="n" scale={34} xChannelSelector="R" yChannelSelector="G" />
      </filter>
      <filter id="mottle" {...FR}>
        <feTurbulence type="fractalNoise" baseFrequency="0.035" numOctaves={2} seed={21} result="t" />
        <feColorMatrix in="t" type="matrix" values="0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  1.6 0 0 0 -0.5" result="a" />
        <feComposite in="SourceGraphic" in2="a" operator="in" />
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
      <filter id="slipShadow" {...FR}><feGaussianBlur stdDeviation={7} /></filter>
    </defs>
  </svg>
);

/** Cream paint/paper carrier. paint=[a,b] -> left-to-right ragged wipe. */
const Swatch: React.FC<{ id: string; b: Box; f: number; paint?: [number, number]; tail?: boolean }> = ({ id, b, f, paint, tail = true }) => {
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
        <rect x={x} y={y + 5} width={w} height={h} rx={18} fill={C.shade} fillOpacity={0.18} />
        <rect x={x} y={y} width={w} height={h} rx={18} fill={C.paper} fillOpacity={0.6} />
        {tail && tw > 0 && <rect x={tx} y={ty} width={tw} height={th} rx={12} fill={C.paper} fillOpacity={0.32} />}
      </g>
    </svg>
  );
};

/** Real typed text, hand-speed linear write-on (left-to-right clip). */
const Write: React.FC<{ text: string; cx: number; cy: number; size: number; f: number; on?: [number, number];
  onBlue?: boolean; weight?: number; rot?: number; color?: string }> = ({ text, cx, cy, size, f, on, onBlue, weight = 700, rot = 0, color }) => {
  const r = on ? lerp(f, on[0], on[1], 100, 0) : 0;
  return (
    <div style={{
      position: "absolute", left: cx, top: cy, transform: `translate(-50%,-50%) rotate(${rot}deg)`,
      fontFamily: "Kalam", fontWeight: weight, fontSize: size, lineHeight: 1.1, whiteSpace: "nowrap",
      padding: "0.18em 0.12em", color: color ?? (onBlue ? C.cream : C.graphite),
      filter: onBlue ? undefined : "url(#graphite)",
      textShadow: onBlue ? "0 2px 0 rgba(30,50,85,.55), 0 0 14px rgba(30,50,85,.55)" : "0 0 12px rgba(246,238,220,.85)",
      clipPath: `inset(0 ${r}% 0 0)`,
    }}>{text}</div>
  );
};

/** Jesus-blue watercolour wash, blooming from its left end. */
const Wash: React.FC<{ id: string; b: Box; f: number; bloom: [number, number] }> = ({ id, b, f, bloom }) => {
  const x = b.x1 + 24, y = b.y1 + 24, w = b.x2 - b.x1 - 48, h = b.y2 - b.y1 - 48;
  const W = b.x2 - b.x1, H = b.y2 - b.y1;
  const p = lerp(f, bloom[0], bloom[1], 0, 1, OUT);
  const o = lerp(f, bloom[0], bloom[0] + 5, 0, 1);
  const cxr = x + w / 2, cyr = y + h / 2;
  return (
    <svg style={{ ...FULL, opacity: o }} width={1080} height={1920}>
      <mask id={id} maskUnits="userSpaceOnUse" x={0} y={0} width={1080} height={1920}>
        <ellipse cx={b.x1 + 90} cy={(b.y1 + b.y2) / 2} rx={Math.max(0.01, p * W * 1.15)} ry={Math.max(0.01, p * H * 1.3)} fill="white" filter="url(#wash)" />
      </mask>
      <g mask={`url(#${id})`}>
        <rect x={x} y={y} width={w} height={h} rx={60} fill={C.blue} fillOpacity={0.12} filter="url(#wash)"
          transform={`translate(${cxr} ${cyr}) scale(1.05) translate(${-cxr} ${-cyr})`} style={{ mixBlendMode: "multiply" }} />
        <rect x={x} y={y} width={w} height={h} rx={60} fill={C.blue} fillOpacity={0.6} filter="url(#wash)" />
        <rect x={x} y={y} width={w} height={h} rx={60} fill="none" stroke={C.blueEdge} strokeWidth={7} strokeOpacity={0.55} filter="url(#wash)" />
        <g filter="url(#wash)"><rect x={x} y={y} width={w} height={h} rx={60} fill={C.mottle} fillOpacity={0.16} filter="url(#mottle)" /></g>
      </g>
    </svg>
  );
};

/** The "not now" torn slip - one object, three uses. */
const Slip: React.FC<{ f: number; at: number; cx: number; cy: number; scale?: number; rotFrom: number; rotTo: number;
  dy?: number; textOpacity?: number }> = ({ f, at, cx, cy, scale = 1, rotFrom, rotTo, dy = 0, textOpacity = 1 }) => {
  const s = lerp(f, at, at + 6, 1.25, 1, BACK) * scale;
  const r = lerp(f, at, at + 6, rotFrom, rotTo, BACK);
  const o = lerp(f, at, at + 4, 0, 1);
  const so = lerp(f, at, at + 6, 0, 1);
  const pts = "0,8 212,0 430,6 426,134 220,140 4,132";
  return (
    <svg style={{ ...FULL, opacity: o }} width={1080} height={1920}>
      <g transform={`translate(${cx} ${cy + dy}) rotate(${r}) scale(${s}) translate(-215 -70)`}>
        <polygon points={pts} fill="rgba(60,40,20,.28)" transform="translate(4 9)" filter="url(#slipShadow)" opacity={so} />
        <polygon points={pts} fill={C.slip} filter="url(#tear)" />
        <text x={215} y={74} textAnchor="middle" dominantBaseline="middle" fontFamily="Kalam" fontWeight={700} fontSize={92}
          fill={C.slipText} filter="url(#graphite)" opacity={textOpacity}>“not now”</text>
      </g>
    </svg>
  );
};

/** Hand-drawn stroke (underline / arc), path-draw with a boiling pencil edge. */
const Stroke: React.FC<{ d: string; f: number; a: number; b: number; color: string; width: number; linear?: boolean;
  opacity?: number; dx?: number; dy?: number }> = ({ d, f, a, b, color, width, linear, opacity = 1, dx = 0, dy = 0 }) => {
  const p = lerp(f, a, b, 0, 1, linear ? undefined : OUT);
  if (p <= 0) return null;
  return (
    <svg style={FULL} width={1080} height={1920}>
      <path d={d} pathLength={1} strokeDasharray={1} strokeDashoffset={1 - p} fill="none" stroke={color}
        strokeWidth={width} strokeLinecap="round" filter="url(#pencil)" opacity={opacity} transform={`translate(${dx} ${dy})`} />
    </svg>
  );
};
const under = (x1: number, y1: number, x2: number, y2: number) => `M ${x1} ${y1} Q ${(x1 + x2) / 2} ${(y1 + y2) / 2 + 6} ${x2} ${y2}`;

const grainSvg = encodeURIComponent(
  "<svg xmlns='http://www.w3.org/2000/svg' width='540' height='960'><filter id='n'><feTurbulence type='fractalNoise' baseFrequency='0.8' numOctaves='2' seed='5'/><feColorMatrix type='saturate' values='0'/></filter><rect width='100%' height='100%' filter='url(#n)'/></svg>");
const PaperGrain: React.FC = () => (
  <AbsoluteFill style={{ backgroundImage: `url("data:image/svg+xml,${grainSvg}")`, backgroundSize: "1080px 1920px", mixBlendMode: "multiply", opacity: 0.06 }} />
);

const Beat: React.FC<{ f: number; from: number; to: number; o?: number; style?: React.CSSProperties; children: React.ReactNode }> = ({ f, from, to, o = 1, style, children }) =>
  f >= from && f < to ? <AbsoluteFill style={{ opacity: o, ...style }}>{children}</AbsoluteFill> : null;

export const Ep16ChildrenV2: React.FC = () => {
  useFonts();
  const f = useCurrentFrame();
  return (
    <AbsoluteFill style={{ background: "#000" }}>
      <OffthreadVideo src={staticFile("ep16/base.mp4")} />
      <Defs f={f} />

      {/* 1a HOOK "Pushed away?" - on frame 0 */}
      <Beat f={f} from={0} to={162} o={lerp(f, 150, 162, 1, 0)}
        style={{ transform: `scale(${lerp(f, 0, 6, 1.05, 1, OUT)})`, transformOrigin: "625px 265px" }}>
        <Swatch id="m1a" b={{ x1: 305, y1: 190, x2: 945, y2: 340 }} f={f} tail={false} />
        <Write text="Pushed away?" cx={625} cy={265} size={104} f={f} />
      </Beat>
      {/* 1b slip "not now" lands on "not" */}
      <Beat f={f} from={95} to={162} o={lerp(f, 150, 162, 1, 0)}>
        <Slip f={f} at={95} cx={560} cy={440} rotFrom={-9} rotTo={-3} />
      </Beat>

      {/* 2 "a touch" (seed of the spine) */}
      <Beat f={f} from={393} to={450} o={lerp(f, 441, 450, 1, 0)}>
        <Swatch id="m2" b={{ x1: 410, y1: 180, x2: 790, y2: 315 }} f={f} paint={[393, 399]} />
        <Write text="a touch" cx={600} cy={248} size={96} f={f} on={[396, 406]} />
        <Stroke d={under(548, 296, 742, 290)} f={f} a={406} b={414} color={C.sienna} width={7} />
      </Beat>

      {/* 3 slip returns on "rebuked", slides off */}
      <Beat f={f} from={497} to={612} o={lerp(f, 600, 612, 1, 0, IN)}>
        <Slip f={f} at={497} cx={600} cy={380} rotFrom={7} rotTo={2} dy={lerp(f, 600, 612, 0, 24, IN)} />
      </Beat>

      {/* 4 "Angry." stamped, two hard underlines */}
      <Beat f={f} from={794} to={836} o={Math.min(lerp(f, 794, 797, 0, 1, OUT), lerp(f, 827, 836, 1, 0))}
        style={{ transform: `scale(${lerp(f, 794, 797, 1.12, 1, OUT)})`, transformOrigin: "540px 1345px" }}>
        <Swatch id="m4" b={{ x1: 280, y1: 1262, x2: 800, y2: 1462 }} f={f} />
        <Write text="Angry." cx={540} cy={1345} size={150} f={f} />
        <Stroke d={under(330, 1428, 752, 1418)} f={f} a={798} b={802} color={C.sienna} width={9} linear />
        <Stroke d={under(352, 1446, 736, 1440)} f={f} a={803} b={807} color={C.sienna} width={6} linear />
      </Beat>

      {/* 5 JESUS: plain meaning of "Suffer the little children", in His blue */}
      <Beat f={f} from={977} to={1158} o={lerp(f, 1146, 1158, 1, 0)}>
        <Wash id="m5" b={{ x1: 130, y1: 160, x2: 950, y2: 415 }} f={f} bloom={[977, 991]} />
        <Write text="Let the children" cx={540} cy={240} size={88} f={f} on={[983, 1001]} onBlue />
        <Write text="come to Me." cx={540} cy={338} size={88} f={f} on={[1017, 1031]} onBlue />
        <AbsoluteFill style={{ opacity: lerp(f, 1040, 1050, 0, 1), transform: "rotate(-1.5deg)", transformOrigin: "280px 434px" }}>
          <Swatch id="m5t" b={{ x1: 140, y1: 408, x2: 420, y2: 460 }} f={f} tail={false} />
          <Write text="Jesus · Mark 10:14" cx={280} cy={434} size={38} weight={400} f={f} />
        </AbsoluteFill>
      </Beat>

      {/* 6 "like a little child" */}
      <Beat f={f} from={1535} to={1612} o={lerp(f, 1602, 1612, 1, 0)}>
        <Swatch id="m6" b={{ x1: 190, y1: 205, x2: 890, y2: 345 }} f={f} paint={[1535, 1541]} />
        <Write text="like a little child" cx={540} cy={275} size={84} f={f} on={[1539, 1562]} />
      </Beat>

      {/* 7a "a touch" twin - hard cut with the shot at 1950 */}
      <Beat f={f} from={1900} to={1950}>
        <Swatch id="m7a" b={{ x1: 100, y1: 262, x2: 440, y2: 390 }} f={f} paint={[1900, 1905]} />
        <Write text="a touch" cx={270} cy={326} size={84} f={f} on={[1903, 1912]} />
        <Stroke d={under(232, 372, 402, 367)} f={f} a={1912} b={1919} color={C.sienna} width={6} />
      </Beat>

      {/* 7b "His arms." - the spine lands, big and blue */}
      <Beat f={f} from={1978} to={2040} o={lerp(f, 2030, 2040, 1, 0)}>
        <Wash id="m7b" b={{ x1: 160, y1: 180, x2: 920, y2: 400 }} f={f} bloom={[1978, 1990]} />
        <Write text="His arms." cx={540} cy={278} size={128} f={f} on={[1986, 1999]} onBlue />
        <Stroke d="M 318 352 Q 540 398 762 352" f={f} a={1999} b={2011} color={C.cream} width={10} />
        <Stroke d="M 318 352 Q 540 398 762 352" f={f} a={2002} b={2014} color={C.cream} width={3} opacity={0.5} dx={6} dy={9} />
      </Beat>

      {/* 8a last "not now" - Jesus's blue washes over it on "Look" */}
      <Beat f={f} from={2072} to={2176}>
        <AbsoluteFill style={{ opacity: lerp(f, 2158, 2176, 1, 0) }}>
          <Slip f={f} at={2072} cx={230} cy={240} scale={0.75} rotFrom={-10} rotTo={-4} textOpacity={lerp(f, 2139, 2152, 1, 0.15)} />
        </AbsoluteFill>
        <svg style={{ ...FULL, opacity: lerp(f, 2158, 2176, 1, 0), mixBlendMode: "multiply" }} width={1080} height={1920}>
          <circle cx={230} cy={240} r={Math.max(0.01, lerp(f, 2137, 2151, 0, 165, OUT))} fill={C.blue} fillOpacity={0.55}
            stroke={C.blueEdge} strokeWidth={5} strokeOpacity={0.55} filter="url(#wash)" />
        </svg>
      </Beat>

      {/* 8b LANDING - holds to the last frame */}
      <Beat f={f} from={2140} to={EP16_FRAMES}>
        <Wash id="m8b" b={{ x1: 120, y1: 1222, x2: 920, y2: 1478 }} f={f} bloom={[2140, 2154]} />
        <Write text="Look at who" cx={520} cy={1302} size={90} f={f} on={[2146, 2158]} onBlue />
        <Write text="Jesus picked up." cx={520} cy={1402} size={90} f={f} on={[2158, 2178]} onBlue />
      </Beat>

      <PaperGrain />
    </AbsoluteFill>
  );
};
