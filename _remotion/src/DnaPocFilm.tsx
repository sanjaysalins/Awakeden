// DNA-LOCK POC (2026-07-23) — proves the moderate retro-comic DNA works MOVING:
// 4 Seedream 4.5 beats (dots baked into the plate = no crawl), animated, with the
// Remotion lettering system (comic-yellow caption + gold kinetic Scripture + a
// subtle SFX) + grain, over a reverent audio bed. If this reads clean, the DNA locks.
import React, { useEffect, useState } from "react";
import {
  AbsoluteFill, OffthreadVideo, Audio, Sequence, staticFile, useCurrentFrame,
  useVideoConfig, interpolate, spring, delayRender, continueRender,
} from "remotion";

export const POC_FPS = 30;
export const BEAT = 180;            // 6s per beat
export const POC_FRAMES = BEAT * 4; // 24s
const FILL = { width: "100%", height: "100%", objectFit: "cover" as const };
const clip = (id: string) => staticFile(`dnapoc/${id}.mp4`);

const useFonts = () => {
  const [h] = useState(() => delayRender("dnapocfonts"));
  useEffect(() => {
    Promise.all([
      new FontFace("Bangers", `url(${staticFile("Bangers.ttf")})`).load(),
      new FontFace("Kalam", `url(${staticFile("Kalam-Bold.ttf")})`).load(),
      new FontFace("PermanentMarker", `url(${staticFile("PermanentMarker.ttf")})`).load(),
    ]).then((ff) => { ff.forEach((f) => (document as any).fonts.add(f)); continueRender(h); })
      .catch(() => continueRender(h));
  }, [h]);
};

// clip stretched to fill the beat (0.8x so a ~5s clip covers 6s — no black tail)
const Plate: React.FC<{ id: string }> = ({ id }) => (
  <OffthreadVideo src={clip(id)} muted playbackRate={0.8} style={FILL} />
);

// comic-yellow narrator caption, top-left, springs in
const Caption: React.FC<{ text: string; start?: number }> = ({ text, start = 8 }) => {
  const f = useCurrentFrame(); const { fps } = useVideoConfig();
  const s = spring({ frame: f - start, fps, config: { damping: 16, stiffness: 180 } });
  const o = interpolate(f, [start, start + 8], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  return (
    <div style={{
      position: "absolute", top: 46, left: 54, maxWidth: 620, opacity: o,
      transform: `translateX(${interpolate(s, [0, 1], [-30, 0])}px)`,
      background: "#ffe100", border: "3px solid #000", boxShadow: "5px 5px 0 rgba(0,0,0,.45)",
      padding: "12px 16px", fontFamily: "Kalam", fontWeight: 700, fontStyle: "italic",
      textTransform: "uppercase", color: "#1a140a", fontSize: 30, lineHeight: 1.12,
    }}>{text}</div>
  );
};

// gold kinetic Scripture (distinct), reveal + a scripture chip
const Scripture: React.FC<{ lines: string[]; cite?: string; start?: number }> = ({ lines, cite, start = 20 }) => {
  const f = useCurrentFrame();
  const chipO = interpolate(f, [start, start + 8], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  const ps = start + 18;
  const reveal = interpolate(f, [ps, ps + 40], [100, 0], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  const o = interpolate(f, [ps, ps + 12], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  return (
    <>
      <AbsoluteFill style={{ pointerEvents: "none", background: "linear-gradient(0deg, rgba(6,4,2,0.7) 0%, rgba(0,0,0,0) 42%)" }} />
      <div style={{ position: "absolute", left: 70, bottom: 70, width: 1000 }}>
        {cite && <div style={{ opacity: chipO, fontFamily: "PermanentMarker", fontSize: 34, letterSpacing: 2, color: "#e9c877", textShadow: "0 3px 12px rgba(0,0,0,.85)" }}>{cite}</div>}
        <div style={{
          marginTop: 8, opacity: o, clipPath: `inset(0 0 ${reveal}% 0)`,
          fontFamily: "PermanentMarker", fontSize: 74, lineHeight: 1.08, color: "#f4e3ad",
          WebkitTextStroke: "1.5px #0d0b07", paintOrder: "stroke fill", textShadow: "0 4px 16px rgba(0,0,0,.85)",
        }}>{lines.map((l, i) => <React.Fragment key={i}>{l}{i < lines.length - 1 && <br />}</React.Fragment>)}</div>
      </div>
    </>
  );
};

// subtle SFX (Bangers, angled) — atmospheric, never on the sacred figure
const Sfx: React.FC<{ text: string; start?: number }> = ({ text, start = 30 }) => {
  const f = useCurrentFrame(); const { fps } = useVideoConfig();
  const s = spring({ frame: f - start, fps, config: { damping: 11, stiffness: 200 } });
  const o = interpolate(f, [start, start + 4, start + 70, start + 85], [0, 1, 1, 0], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  return (
    <div style={{
      position: "absolute", right: 90, top: 120, opacity: o,
      transform: `scale(${interpolate(s, [0, 1], [0.6, 1])}) rotate(-8deg) skewX(-6deg)`,
      fontFamily: "Bangers", fontSize: 76, color: "#e9c877",
      WebkitTextStroke: "5px #000", paintOrder: "stroke fill", textShadow: "4px 4px 0 #2e3a52",
    }}>{text}</div>
  );
};

const Grain: React.FC = () => {
  const f = useCurrentFrame();
  return (
    <AbsoluteFill style={{ mixBlendMode: "overlay", opacity: 0.05, pointerEvents: "none" }}>
      <svg width="1920" height="1080"><filter id="dpg"><feTurbulence type="fractalNoise" baseFrequency="0.9" numOctaves="2" seed={f % 40} /></filter>
        <rect width="100%" height="100%" filter="url(#dpg)" /></svg>
    </AbsoluteFill>
  );
};

export const DnaPocFilm: React.FC = () => {
  useFonts();
  return (
    <AbsoluteFill style={{ backgroundColor: "black" }}>
      <Audio src={staticFile("audio/dnapoc_bed.mp3")} />

      <Sequence from={0} durationInFrames={BEAT}>
        <AbsoluteFill><Plate id="01_establish" />
          <Caption text="Once a year — one man carried blood behind the veil." />
          <Sfx text="RUMBLE" start={38} /></AbsoluteFill>
      </Sequence>

      <Sequence from={BEAT} durationInFrames={BEAT}>
        <AbsoluteFill><Plate id="02_event" />
          <Caption text="Outside the gate, the price was paid." /></AbsoluteFill>
      </Sequence>

      <Sequence from={BEAT * 2} durationInFrames={BEAT}>
        <AbsoluteFill><Plate id="03_reaction" />
          <Caption text="And the people trembled." /></AbsoluteFill>
      </Sequence>

      <Sequence from={BEAT * 3} durationInFrames={BEAT}>
        <AbsoluteFill><Plate id="04_welcome" />
          <Scripture cite="MATTHEW 11:28" lines={["Come unto me,", "and I will give you rest."]} start={16} /></AbsoluteFill>
      </Sequence>

      <Grain />
    </AbsoluteFill>
  );
};
