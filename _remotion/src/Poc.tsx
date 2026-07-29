// POCs: elevating our ink-comic style with SUBTLE techniques borrowed from the
// ArkAIology VOX skills — NOT their flat-collage/paper-diorama look (that stays
// unique to that repo). Two ideas, reimagined in OUR inked-noir language:
//   PocInk   — hand-inked marginalia: a pen-stroke circle + arrow that DRAW ON
//              to point at a detail (their "hand-drawn circles/underlines", in ink)
//   PocPrint — a real printed-page finish: halftone + newsprint texture + grain
//              + darkened deckle edge (their "distressed letterpress print texture")
import React, { useEffect, useState } from "react";
import {
  AbsoluteFill, OffthreadVideo, staticFile, useCurrentFrame, interpolate,
  delayRender, continueRender,
} from "remotion";

const noir = (id: number) => staticFile(`noir/${String(id).padStart(2, "0")}.mp4`);

const useFonts = () => {
  const [h] = useState(() => delayRender("fonts"));
  useEffect(() => {
    const b = new FontFace("Bangers", `url(${staticFile("Bangers.ttf")})`);
    b.load().then((ff) => { (document as any).fonts.add(ff); continueRender(h); })
      .catch(() => continueRender(h));
  }, [h]);
};

// ---------- shared rough-ink SVG filter (hand-drawn wobble) ----------
const RoughDefs: React.FC = () => (
  <defs>
    <filter id="rough" x="-20%" y="-20%" width="140%" height="140%">
      <feTurbulence type="fractalNoise" baseFrequency="0.018" numOctaves="2" seed="7" result="n" />
      <feDisplacementMap in="SourceGraphic" in2="n" scale="9" />
    </filter>
  </defs>
);

// a stroke that draws on, with a dark edge behind a cream core so it reads on any tone
const InkStroke: React.FC<{ d?: string; ellipse?: [number, number, number, number]; len: number; start: number; dur: number }> =
  ({ d, ellipse, len, start, dur }) => {
    const f = useCurrentFrame();
    const p = interpolate(f, [start, start + dur], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
    const off = len * (1 - p);
    const common = { fill: "none" as const, strokeDasharray: len, strokeDashoffset: off, strokeLinecap: "round" as const, filter: "url(#rough)" };
    const Shape: React.FC<{ stroke: string; w: number }> = ({ stroke, w }) =>
      ellipse
        ? <ellipse cx={ellipse[0]} cy={ellipse[1]} rx={ellipse[2]} ry={ellipse[3]} stroke={stroke} strokeWidth={w} {...common} />
        : <path d={d} stroke={stroke} strokeWidth={w} {...common} />;
    return (<>
      <Shape stroke="#141009" w={16} />
      <Shape stroke="#f3e8cc" w={8} />
    </>);
  };

export const PocInk: React.FC = () => {
  useFonts();
  const f = useCurrentFrame();
  // scene 7 = the two lot-stones held over the vessel — circle the LOTS, arrow in
  const circLen = 2 * Math.PI * Math.sqrt((150 * 150 + 120 * 120) / 2);
  const labelO = interpolate(f, [46, 58], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  return (
    <AbsoluteFill style={{ backgroundColor: "black" }}>
      <OffthreadVideo src={noir(7)} muted style={{ width: "100%", height: "100%", objectFit: "cover" }} />
      {/* subtle darken so the ink reads */}
      <AbsoluteFill style={{ background: "radial-gradient(ellipse at 42% 46%, rgba(0,0,0,0) 30%, rgba(0,0,0,0.35) 80%)" }} />
      <svg width="1920" height="1080" style={{ position: "absolute", inset: 0 }}>
        <RoughDefs />
        {/* circle the lots (approx centre of the two held stones) */}
        <InkStroke ellipse={[820, 470, 150, 120]} len={circLen} start={6} dur={26} />
        {/* an ink arrow sweeping in from lower-left, drawing on after the circle */}
        <InkStroke d="M470,880 C560,760 640,650 700,540" len={430} start={30} dur={16} />
        <InkStroke d="M700,540 L664,585" len={70} start={44} dur={6} />
        <InkStroke d="M700,540 L724,592" len={70} start={44} dur={6} />
      </svg>
      {/* hand-lettered marginal note (Bangers), fades in as the arrow lands */}
      <div style={{
        position: "absolute", left: 300, top: 900, opacity: labelO,
        fontFamily: "Bangers", fontSize: 84, color: "#f3e8cc", letterSpacing: 2,
        WebkitTextStroke: "6px #141009", paintOrder: "stroke fill", transform: "rotate(-4deg)",
      }}>THE LOTS — LIFE OR DEATH</div>
    </AbsoluteFill>
  );
};

// ---------- print finish: halftone + newsprint + grain + deckle edge ----------
const PrintFinish: React.FC = () => {
  const f = useCurrentFrame();
  return (
    <>
      {/* halftone dot screen */}
      <AbsoluteFill style={{
        mixBlendMode: "multiply", opacity: 0.22, pointerEvents: "none",
        backgroundImage: "radial-gradient(circle, rgba(10,8,6,0.9) 32%, transparent 33%)",
        backgroundSize: "5px 5px",
      }} />
      {/* warm newsprint paper texture */}
      <AbsoluteFill style={{ mixBlendMode: "multiply", opacity: 0.16, pointerEvents: "none" }}>
        <svg width="1920" height="1080">
          <filter id="paper"><feTurbulence type="fractalNoise" baseFrequency="0.012 0.02" numOctaves="3" seed="4" /></filter>
          <rect width="100%" height="100%" filter="url(#paper)" />
          <rect width="100%" height="100%" fill="rgb(150,120,70)" opacity="0.35" />
        </svg>
      </AbsoluteFill>
      {/* moving film grain */}
      <AbsoluteFill style={{ mixBlendMode: "overlay", opacity: 0.09, pointerEvents: "none" }}>
        <svg width="1920" height="1080">
          <filter id="grain"><feTurbulence type="fractalNoise" baseFrequency="0.9" numOctaves="2" seed={f % 40} /></filter>
          <rect width="100%" height="100%" filter="url(#grain)" />
        </svg>
      </AbsoluteFill>
      {/* darkened rough deckle edge */}
      <AbsoluteFill style={{ boxShadow: "inset 0 0 120px 40px rgba(8,6,4,0.75)", pointerEvents: "none" }} />
    </>
  );
};

export const PocPrint: React.FC = () => (
  <AbsoluteFill style={{ backgroundColor: "#0a0806" }}>
    <AbsoluteFill style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gridTemplateRows: "1fr 1fr", gap: 6, background: "#0a0806" }}>
      {[7, 8, 11, 10].map((id, i) => (
        <div key={i} style={{ overflow: "hidden" }}>
          <OffthreadVideo src={noir(id)} muted style={{ width: "100%", height: "100%", objectFit: "cover" }} />
        </div>
      ))}
    </AbsoluteFill>
    <PrintFinish />
  </AbsoluteFill>
);
