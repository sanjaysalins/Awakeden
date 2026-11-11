// Zacchaeus scratchy-ink — motion-layer PREVIEW (~20 s): hook + reversal + landing.
// Design: poc_scratchy_ink/zacchaeus/_work/MOTION_DESIGN_FABLE.md (Fable seat, 2026-11-11).
// Base = untouched clips + mix (public/zacc/preview_base.mp4: film 0-5.70 + 70.95-85.22).
// Rules: no zoom/freeze/boomerang; nothing over faces/hands; 100% or 0% opacity; red only for Jesus's line.
import React, { useEffect, useState } from "react";
import {
  AbsoluteFill, OffthreadVideo, staticFile, useCurrentFrame, delayRender, continueRender, interpolate, Easing,
} from "remotion";

export const ZP_FPS = 30;
export const ZP_FRAMES = 600;
const INK = "#14110d", CREAM = "#f1e6c8", RED = "#a3261c";
const f = (s: number) => Math.round(s * ZP_FPS);
const clamp = { extrapolateLeft: "clamp", extrapolateRight: "clamp" } as const;
const OUT = Easing.out(Easing.cubic);
const prog = (fr: number, a: number, b: number) => interpolate(fr, [f(a), f(b)], [0, 1], { ...clamp, easing: OUT });

const useFonts = () => {
  const [h] = useState(() => delayRender("zacc-fonts"));
  useEffect(() => {
    Promise.all([
      new FontFace("Kalam", `url(${staticFile("Kalam-Bold.ttf")})`, { weight: "700" }).load(),
      new FontFace("PMarker", `url(${staticFile("PermanentMarker.ttf")})`).load(),
    ]).then((ff) => { ff.forEach((x) => (document as any).fonts.add(x)); continueRender(h); })
      .catch(() => continueRender(h));
  }, [h]);
};

// deterministic pseudo-random
const rnd = (n: number) => { const x = Math.sin(n * 12.9898) * 43758.5453; return x - Math.floor(x); };

// Boil: rough edges, new seed every 3 frames (moves "on threes" like hand-drawn art)
const Boil: React.FC<{ id: string; scale?: number }> = ({ id, scale = 3.5 }) => {
  const fr = useCurrentFrame();
  return (
    <filter id={id} x="-5%" y="-5%" width="110%" height="110%">
      <feTurbulence type="fractalNoise" baseFrequency="0.045" numOctaves={2} seed={Math.floor(fr / 3) % 97} />
      <feDisplacementMap in="SourceGraphic" scale={scale} />
    </filter>
  );
};

// ---------- SIGHT-LINE ----------
type LineP = { d: string; a: number; b: number; red?: boolean; out?: [number, number]; arrow?: { x: number; y: number; ang: number };
  clipId?: string; width?: number };
// a..b = draw-on seconds; out = [start,end] seconds the line retracts from its START (tail follows the head)
const SightLine: React.FC<LineP> = ({ d, a, b, red, out, arrow, clipId, width }) => {
  const fr = useCurrentFrame();
  const p = prog(fr, a, b);
  if (p <= 0) return null;
  const tail = out ? prog(fr, out[0], out[1]) : 0;
  if (tail >= 1) return null;
  const w = width ?? (red ? 16 : 6);
  const seg = (stroke: string, sw: number, dash?: string) => (
    <path d={d} pathLength={1} fill="none" stroke={stroke} strokeWidth={sw} strokeLinecap="round"
      strokeDasharray={dash ?? `0 ${tail} ${p - tail} 2`} />
  );
  const showArrow = arrow && p >= 0.999 && tail === 0;
  const head = arrow && (
    <g transform={`translate(${arrow.x},${arrow.y}) rotate(${arrow.ang})`}>
      <path d="M -34 -22 L 4 0 L -34 22 Z" fill={CREAM} stroke={CREAM} strokeWidth={10} strokeLinejoin="round" />
      <path d="M -34 -22 L 4 0 L -34 22 Z" fill={red ? RED : INK} />
    </g>
  );
  const maskId = `m${d.length}${a}`;
  return (
    <g filter="url(#boil)" clipPath={clipId ? `url(#${clipId})` : undefined}>
      {red ? (
        <>{seg(CREAM, w + 8)}{seg(RED, w)}</>
      ) : (
        <>
          <mask id={maskId}>{seg("white", w + 12)}</mask>
          <g mask={`url(#${maskId})`}>
            <path d={d} pathLength={1} fill="none" stroke={CREAM} strokeWidth={w + 6} strokeDasharray="0.025 0.018" strokeLinecap="round" />
            <path d={d} pathLength={1} fill="none" stroke={INK} strokeWidth={w} strokeDasharray="0.025 0.018" strokeLinecap="round" />
          </g>
        </>
      )}
      {showArrow && head}
    </g>
  );
};

// ink tap / spat: a few blots at a point for ~6 frames then stays as a small mark
const Spat: React.FC<{ x: number; y: number; at: number; n?: number; r?: number; red?: boolean; keep?: boolean; until?: number }> = ({ x, y, at, n = 6, r = 9, red, keep = true, until }) => {
  const fr = useCurrentFrame();
  const t = fr - f(at);
  if (t < 0 || (!keep && t > 8) || (until !== undefined && fr >= f(until))) return null;
  const s = Math.min(1, t / 2);
  return (
    <g filter="url(#boil)">
      {Array.from({ length: n }).map((_, i) => {
        const ang = rnd(i + x) * Math.PI * 2, dist = (i === 0 ? 0 : 10 + rnd(i * 7 + y) * 34) * s;
        return <circle key={i} cx={x + Math.cos(ang) * dist} cy={y + Math.sin(ang) * dist} r={(i === 0 ? r * 1.4 : r * (0.3 + rnd(i * 3) * 0.6))}
          fill={red && i === 0 ? RED : INK} />;
      })}
    </g>
  );
};

// ---------- CAPTION: narrator black brush slab, words stamp on the voice ----------
type W = { w: string; t: number; red?: boolean };
const Slab: React.FC<{ words: W[]; a: number; b: number; y: number; size?: number; underline?: string }> = ({ words, a, b, y, size = 60, underline }) => {
  const fr = useCurrentFrame();
  if (fr < f(a) || fr >= f(b)) return null;
  const seed = Math.floor(fr / 3);
  // torn-end slab shape
  const pts: string[] = [];
  const L = 6, R = 94;
  for (let i = 0; i <= 8; i++) pts.push(`${L + i * (R - L) / 8 + (rnd(i + a) - 0.5) * 1.2}% ${(rnd(i * 5 + a) * 5).toFixed(1)}%`);
  for (let i = 0; i <= 5; i++) pts.push(`${R + (rnd(i * 9 + a + seed * 0.0) - 0.5) * 3}% ${i * 20}%`);
  for (let i = 8; i >= 0; i--) pts.push(`${L + i * (R - L) / 8 + (rnd(i + a + 30) - 0.5) * 1.2}% ${(95 + rnd(i * 3 + a) * 5).toFixed(1)}%`);
  for (let i = 5; i >= 0; i--) pts.push(`${L + (rnd(i * 11 + a) - 0.5) * 3}% ${i * 20}%`);
  return (
    <div style={{ position: "absolute", left: 0, right: 0, top: y, display: "flex", justifyContent: "center" }}>
      <div style={{ position: "relative", maxWidth: 860, padding: "26px 64px 30px", background: INK, clipPath: `polygon(${pts.join(",")})`,
        filter: "url(#boilSoft)" }}>
        <div style={{ fontFamily: "Kalam", fontWeight: 700, fontSize: size, lineHeight: 1.12, color: CREAM, textAlign: "center",
          textTransform: "uppercase", letterSpacing: 1 }}>
          {words.map((wd, i) => {
            const on = fr >= f(wd.t) - 2;
            const k = fr - (f(wd.t) - 2);
            const sc = on ? interpolate(k, [0, 2], [1.25, 1], clamp) : 1;
            const rot = (rnd(i * 13 + a) - 0.5) * 3;
            const dy = (rnd(i * 17 + a) - 0.5) * 5;
            const isU = underline && wd.w.replace(/[^A-Za-z]/g, "").toUpperCase() === underline;
            return (
              <span key={i} style={{ display: "inline-block", opacity: on ? 1 : 0, transform: `translateY(${dy}px) rotate(${rot}deg) scale(${sc})`,
                marginRight: "0.28em", color: wd.red ? "#ffcfc4" : CREAM, position: "relative" }}>
                {wd.w}
                {isU && on && (
                  <svg style={{ position: "absolute", left: -6, bottom: -6, overflow: "visible" }} width="110%" height="16">
                    <path d="M 0 8 Q 40 2 80 9 T 170 6" pathLength={1} fill="none" stroke={RED} strokeWidth={9} strokeLinecap="round"
                      strokeDasharray={`${interpolate(k, [2, 8], [0, 1], clamp)} 2`} />
                  </svg>
                )}
              </span>
            );
          })}
        </div>
      </div>
    </div>
  );
};

// ---------- TRANSITIONS ----------
// Hatch wipe: cross-hatch strokes scribble over the frame (5 frames) then lift (5 frames), centred on the cut
const HatchWipe: React.FC<{ cut: number }> = ({ cut }) => {
  const fr = useCurrentFrame();
  const c = f(cut), t = fr - c;
  if (t < -6 || t > 6) return null;
  const strokes = 46;
  return (
    <svg width={1080} height={1920} style={{ position: "absolute", inset: 0 }}>
      <g filter="url(#boil)">
        {Array.from({ length: strokes }).map((_, i) => {
          const dir = i % 2 ? 1 : -1;
          const y0 = -300 + i * 52 + rnd(i) * 30;
          const order = rnd(i * 3.3);
          const on = interpolate(t, [-6 + order * 3, -2 + order * 3], [0, 1], clamp);
          const off = interpolate(t, [1 + order * 3, 5 + order * 3], [0, 1], clamp);
          const d = dir > 0 ? `M -80 ${y0} L 1160 ${y0 + 700}` : `M 1160 ${y0} L -80 ${y0 + 700}`;
          return <path key={i} d={d} pathLength={1} stroke={INK} strokeWidth={70 + rnd(i * 5) * 40} strokeLinecap="round" fill="none"
            strokeDasharray={`0 ${off} ${Math.max(0, on - off)} 2`} />;
        })}
      </g>
    </svg>
  );
};

// Opening hatch: frame starts covered in black scribble that lifts off in 6 frames
const OpenHatch: React.FC = () => {
  const fr = useCurrentFrame();
  if (fr > 8) return null;
  return (
    <svg width={1080} height={1920} style={{ position: "absolute", inset: 0 }}>
      <rect width={1080} height={1920} fill={INK} opacity={fr < 1 ? 1 : 0} />
      <g filter="url(#boil)">
        {Array.from({ length: 40 }).map((_, i) => {
          const y0 = -300 + i * 60;
          const off = interpolate(fr, [rnd(i) * 3, 3 + rnd(i) * 4], [0, 1], clamp);
          return <path key={i} d={`M -80 ${y0} L 1160 ${y0 + 600}`} pathLength={1} stroke={INK} strokeWidth={110} fill="none"
            strokeDasharray={`0 ${off} ${1 - off} 2`} />;
        })}
      </g>
    </svg>
  );
};

// Splat cut: 2-frame ink spatter in a corner on the cut frame
const SplatCut: React.FC<{ cut: number; x: number; y: number }> = ({ cut, x, y }) => {
  const fr = useCurrentFrame();
  const t = fr - f(cut);
  if (t < 0 || t > 2) return null;
  return (
    <svg width={1080} height={1920} style={{ position: "absolute", inset: 0 }}>
      <g filter="url(#boil)">
        {Array.from({ length: 14 }).map((_, i) => (
          <circle key={i} cx={x + (rnd(i) - 0.5) * 260} cy={y + (rnd(i * 2) - 0.5) * 260} r={4 + rnd(i * 4) * (i < 3 ? 46 : 16)} fill={INK} />
        ))}
      </g>
    </svg>
  );
};

// Tally stroke: a scratched mark drawn in 3 frames
const Tally: React.FC<{ x: number; y: number; at: number; red?: boolean }> = ({ x, y, at, red }) => {
  const fr = useCurrentFrame();
  const p = interpolate(fr, [f(at), f(at) + 3], [0, 1], clamp);
  if (p <= 0) return null;
  return (
    <g filter="url(#boil)">
      <path d={`M ${x} ${y} Q ${x + 8} ${y + 70} ${x - 4} ${y + 150}`} pathLength={1} stroke={CREAM} strokeWidth={26} fill="none" strokeLinecap="round" strokeDasharray={`${p} 2`} />
      <path d={`M ${x} ${y} Q ${x + 8} ${y + 70} ${x - 4} ${y + 150}`} pathLength={1} stroke={red ? RED : INK} strokeWidth={16} fill="none" strokeLinecap="round" strokeDasharray={`${p} 2`} />
    </g>
  );
};

// ---------- word lists (preview seconds) ----------
const w = (s: string, t0: number, t1: number, red: number[] = []): W[] => {
  const parts = s.split(" ");
  return parts.map((p, i) => ({ w: p, t: t0 + (t1 - t0) * (i / parts.length), red: red.includes(i) }));
};
// hook (film 0-5.70 = preview 0-5.70): exact word starts from alignment.json
const HOOK1: W[] = [["A", .12], ["MAN", .2], ["CLIMBED", .52], ["A", .84], ["TREE", .94], ["TO", 1.3], ["SEE", 1.42], ["JESUS.", 1.64]].map(([x, t]) => ({ w: x as string, t: t as number }));
const HOOK2: W[] = [["BUT", 3.48], ["JESUS", 3.68], ["WAS", 4.58], ["LOOKING", 4.76], ["FOR", 5.12], ["HIM.", 5.34]].map(([x, t]) => ({ w: x as string, t: t as number }));
// reversal + landing: preview = original narration time - 64.25
const R = (o: number) => o - 64.25;
const REV1: W[] = [["ZACCHAEUS", 70.04], ["CAME", 70.52], ["TO", 70.76], ["LOOK.", 70.88]].map(([x, t]) => ({ w: x as string, t: R(t as number) }));
const REV2: W[] = [["JESUS", 71.84], ["CAME", 72.44], ["TO", 72.64], ["FIND", 72.76], ["HIM.", 73.08]].map(([x, t]) => ({ w: x as string, t: R(t as number) }));
const REV3: W[] = [["HE", 74.4], ["STILL", 74.58], ["LOOKS", 74.8], ["FOR", 75.02], ["THE", 75.14], ["LOST.", 75.28]].map(([x, t]) => ({ w: x as string, t: R(t as number) }));
const LAND1: W[] = [["TO", 76.24], ["SAVE", 76.42], ["THEM,", 76.72], ["HE", 77.18], ["LATER", 77.34], ["DIED", 77.62], ["FOR", 77.88], ["OUR", 78.06], ["SINS,", 78.26]].map(([x, t]) => ({ w: x as string, t: R(t as number) }));
const LAND2: W[] = [["AND", 79.24], ["ROSE", 79.38], ["AGAIN", 79.62], ["ON", 80.42], ["THE", 80.52], ["THIRD", 80.66], ["DAY.", 80.94]].map(([x, t]) => ({ w: x as string, t: R(t as number) }));

export const ZaccPreview: React.FC = () => {
  useFonts();
  void w;
  return (
    <AbsoluteFill style={{ backgroundColor: INK }}>
      <OffthreadVideo src={staticFile("zacc/preview_base.mp4")} />
      <svg width={1080} height={1920} style={{ position: "absolute", inset: 0 }}>
        <defs>
          <Boil id="boil" />
          <clipPath id="outsideDoor">
            {/* everything EXCEPT the tomb doorway (x585-725, y1070-1615) */}
            <path clipRule="evenodd" d="M0 0 H1080 V1920 H0 Z M585 1070 H725 V1615 H585 Z" />
          </clipPath>
        </defs>

        {/* ---- HOOK (c01) ---- */}
        {/* Zacchaeus looking: thin black dashed line from beside his head, up and out */}
        <SightLine d="M 640 330 Q 720 230 800 120" a={1.42} b={2.1} out={[5.6, 5.7]} />
        <Spat x={800} y={125} at={3.48} n={5} r={8} until={5.7} />
        {/* Jesus looking: thick red line from Jesus (small, bottom right) up to behind Zacchaeus */}
        <SightLine d="M 975 1545 C 1060 1250, 1000 900, 650 650" a={3.68} b={5.34} red arrow={{ x: 650, y: 650, ang: -150 }} out={[5.62, 5.7]} />

        {/* ---- REVERSAL (c13, empty tree at sunset) preview 5.70-11.65 ---- */}
        <SightLine d="M 760 1520 C 770 1300, 700 1050, 560 850" a={R(70.52)} b={R(71.14)} out={[11.55, 11.65]} />
        <Spat x={560} y={850} at={R(71.2)} n={4} r={7} until={11.65} />
        <SightLine d="M 410 1250 Q 470 1460 690 1560" a={R(71.84)} b={R(72.76)} red arrow={{ x: 690, y: 1560, ang: 25 }} out={[11.55, 11.65]} />
        <Spat x={700} y={1565} at={R(72.78)} n={6} r={10} red until={11.65} />
        <SightLine d="M 690 1560 C 700 1700, 640 1820, 610 1960" a={R(74.4)} b={R(75.66)} red out={[11.6, 11.65]} />

        {/* ---- LANDING (c14, empty tomb) preview 11.65-20 ---- */}
        {/* red line comes up the path, then on "died" runs INTO the doorway and is gone */}
        <SightLine d="M 655 1960 C 640 1820, 670 1700, 655 1560 L 655 1240" a={11.7} b={R(77.62)} red clipId="outsideDoor" out={[R(77.7), R(78.62)]} />
        {/* on "rose": thicker red line comes back OUT and runs down toward the viewer, holds */}
        <SightLine d="M 655 1420 L 655 1600 C 650 1700, 690 1780, 655 1860" a={R(79.38)} b={R(79.96)} red width={22} clipId="outsideDoor"
          arrow={{ x: 655, y: 1862, ang: 90 }} />
        <Tally x={440} y={520} at={R(80.42)} />
        <Tally x={500} y={512} at={R(80.52)} />
        <Tally x={562} y={522} at={R(80.66)} red />
      </svg>

      {/* captions (narrator slabs) */}
      <Slab words={HOOK1} a={0.1} b={3.42} y={1300} />
      <Slab words={HOOK2} a={3.46} b={5.70} y={1300} underline="HIM" />
      <Slab words={[...REV1]} a={R(70.0)} b={R(71.8)} y={220} />
      <Slab words={[...REV2]} a={R(71.8)} b={R(74.35)} y={220} underline="FIND" />
      <Slab words={REV3} a={R(74.36)} b={11.65} y={220} underline="LOST" />
      <Slab words={LAND1} a={R(76.2)} b={R(79.2)} y={330} size={56} />
      <Slab words={LAND2} a={R(79.22)} b={20.0} y={330} size={56} underline="ROSE" />

      <OpenHatch />
      <HatchWipe cut={5.70} />
      <SplatCut cut={11.65} x={980} y={180} />
      <svg width={0} height={0} style={{ position: "absolute" }}>
        <defs>
          <filter id="boilSoft"><feTurbulence type="fractalNoise" baseFrequency="0.03" numOctaves={2} seed={3} />
            <feDisplacementMap in="SourceGraphic" scale={6} /></filter>
        </defs>
      </svg>
    </AbsoluteFill>
  );
};
