// POC (2026-07-23): kinetic SCRIPTURE ink-type composited over a LIVING
// PAINTED-COMIC plate — the one genuinely-new beat for the EW01 painted-comic
// rebuild. Method borrowed from the ArkAIology VOX skill (§10: never bake text
// into the AI still; composite real animated type over a text-free, negative-
// space-reserved plate) but rendered in OUR ink idiom, NOT Vox highlighter:
//   - a hand-inked scripture chip that springs in with a drawn-on ink underline
//   - the KJV phrase revealing TOP-TO-BOTTOM, mirroring the veil tearing
// Background = pc_20_veil_clip.mp4 (painted-comic plate of Matt 27:51, animated
// on Kling), whose lower-left was rendered as reserved in-scene dead space.
import React, { useEffect, useState } from "react";
import {
  AbsoluteFill, OffthreadVideo, staticFile, useCurrentFrame, useVideoConfig,
  interpolate, spring, delayRender, continueRender,
} from "remotion";

export const POC_KT_FPS = 30;
export const POC_KT_FRAMES = 150; // 5s @ 30fps

const FILL = { width: "100%", height: "100%", objectFit: "cover" as const };
const clip = staticFile("poc/pc_20_veil_clip.mp4");

const useInkFont = () => {
  const [h] = useState(() => delayRender("pocktfont"));
  useEffect(() => {
    const pm = new FontFace("PermanentMarker", `url(${staticFile("PermanentMarker.ttf")})`);
    pm.load().then((ff) => { (document as any).fonts.add(ff); continueRender(h); })
      .catch(() => continueRender(h));
  }, [h]);
};

// a short rough ink underline that draws on (dark edge under a gold core)
const InkUnderline: React.FC<{ start: number; dur: number }> = ({ start, dur }) => {
  const f = useCurrentFrame();
  const len = 360;
  const p = interpolate(f, [start, start + dur], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  const off = len * (1 - p);
  const common = { fill: "none" as const, strokeDasharray: len, strokeDashoffset: off, strokeLinecap: "round" as const, filter: "url(#pockt-rough)" };
  return (
    <svg width="420" height="34" style={{ display: "block", marginTop: 4 }}>
      <defs>
        <filter id="pockt-rough" x="-20%" y="-20%" width="140%" height="140%">
          <feTurbulence type="fractalNoise" baseFrequency="0.02" numOctaves="2" seed="5" result="n" />
          <feDisplacementMap in="SourceGraphic" in2="n" scale="6" />
        </filter>
      </defs>
      <path d="M6,18 C120,10 250,24 372,14" stroke="#141009" strokeWidth={10} {...common} />
      <path d="M6,18 C120,10 250,24 372,14" stroke="#e9c877" strokeWidth={5} {...common} />
    </svg>
  );
};

export const PocKineticType: React.FC = () => {
  useInkFont();
  const f = useCurrentFrame();
  const { fps } = useVideoConfig();

  // scripture chip springs in
  const chipS = spring({ frame: f - 16, fps, config: { damping: 14, stiffness: 200, mass: 0.6 } });
  const chipScale = interpolate(chipS, [0, 1], [0.72, 1]);
  const chipO = interpolate(f, [16, 22], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });

  // KJV phrase reveals top -> bottom (mirrors "rent in twain from the top to the bottom")
  const reveal = interpolate(f, [42, 92], [100, 0], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  const phraseO = interpolate(f, [42, 54], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });

  return (
    <AbsoluteFill style={{ backgroundColor: "black" }}>
      {/* living painted-comic plate */}
      <OffthreadVideo src={clip} muted style={FILL} />

      {/* legibility scrim over the reserved lower-left dead zone (SPEC §6) */}
      <AbsoluteFill style={{
        pointerEvents: "none",
        background: "linear-gradient(102deg, rgba(6,4,2,0.74) 0%, rgba(6,4,2,0.42) 32%, rgba(0,0,0,0) 54%)",
      }} />

      {/* kinetic ink-type, seated in the reserved dead zone (screen-space, plate moves behind) */}
      <div style={{ position: "absolute", left: 104, top: 372, width: 960 }}>
        {/* scripture chip */}
        <div style={{
          opacity: chipO, transform: `scale(${chipScale})`, transformOrigin: "left center",
          fontFamily: "PermanentMarker", fontSize: 42, letterSpacing: 3, color: "#e9c877",
          textShadow: "0 3px 14px rgba(0,0,0,0.85)",
        }}>MATTHEW 27:51</div>
        <InkUnderline start={22} dur={14} />

        {/* the KJV phrase, revealed top -> bottom */}
        <div style={{
          marginTop: 22, opacity: phraseO, clipPath: `inset(0 0 ${reveal}% 0)`,
          fontFamily: "PermanentMarker", fontSize: 64, lineHeight: 1.12, color: "#f7f2e6",
          WebkitTextStroke: "1.5px #0d0b07", paintOrder: "stroke fill",
          textShadow: "0 4px 16px rgba(0,0,0,0.85)",
        }}>
          The veil of the temple<br />was rent in twain —<br />from the top to the bottom
        </div>
      </div>
    </AbsoluteFill>
  );
};
