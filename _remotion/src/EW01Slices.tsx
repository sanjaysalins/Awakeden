// EW01 painted-comic REBUILD — e2e POC slice films (2026-07-23).
// Three representative slices assembled in Remotion over the real narration +
// epic score (sliced from the finished audio). Painted-comic living plates
// (public/pc/NN.mp4), stretched to fill each scene's narration window; kinetic
// SCRIPTURE ink-type beats (our idiom, per PocKineticType) land on the quote
// beats; light film grain + vignette. Brightness arc is baked into the stills.
//   EW01Open   — sc 1-5   (dark law era)          99.0s
//   EW01Climax — sc 16-20 (pivot -> Christ -> veil) 113.0s
//   EW01Range  — sc 1-2 + 19-20 (tonal range)      84.2s
import React, { useEffect, useState } from "react";
import {
  AbsoluteFill, OffthreadVideo, Audio, Sequence, staticFile, useCurrentFrame,
  useVideoConfig, interpolate, spring, delayRender, continueRender,
} from "remotion";

export const FPS = 30;
const FILL = { width: "100%", height: "100%", objectFit: "cover" as const };
const CLIP_DUR = 5.0; // assumed source clip length; playbackRate stretches it to the window
const pc = (id: number) => staticFile(`pc/${String(id).padStart(2, "0")}.mp4`);
const aud = (name: string) => staticFile(`audio/${name}`);

// scene narration windows [start, end] in the full episode timeline (from scene_plan.json)
const WIN: Record<number, [number, number]> = {
  1: [0, 19.5], 2: [19.5, 39], 3: [39, 58.5], 4: [58.5, 78], 5: [78, 99],
  16: [338, 360.6], 17: [360.6, 383.2], 18: [383.2, 405.8], 19: [405.8, 428.4], 20: [428.4, 451],
};
const len = (id: number) => WIN[id][1] - WIN[id][0];

const useInkFonts = () => {
  const [h] = useState(() => delayRender("ew01fonts"));
  useEffect(() => {
    Promise.all([
      new FontFace("PermanentMarker", `url(${staticFile("PermanentMarker.ttf")})`).load(),
      new FontFace("Bangers", `url(${staticFile("Bangers.ttf")})`).load(),
    ]).then((ff) => { ff.forEach((f) => (document as any).fonts.add(f)); continueRender(h); })
      .catch(() => continueRender(h));
  }, [h]);
};

// ---- kinetic scripture beat (local frames within a scene Sequence) ----
type Beat = { chip: string; lines: string[]; start: number; topDown?: boolean };

const InkUnderline: React.FC<{ start: number; dur: number }> = ({ start, dur }) => {
  const f = useCurrentFrame();
  const L = 360;
  const p = interpolate(f, [start, start + dur], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  const common = { fill: "none" as const, strokeDasharray: L, strokeDashoffset: L * (1 - p), strokeLinecap: "round" as const, filter: "url(#ew01-rough)" };
  return (
    <svg width="420" height="34" style={{ display: "block", marginTop: 4 }}>
      <defs><filter id="ew01-rough" x="-20%" y="-20%" width="140%" height="140%">
        <feTurbulence type="fractalNoise" baseFrequency="0.02" numOctaves="2" seed="5" result="n" />
        <feDisplacementMap in="SourceGraphic" in2="n" scale="6" />
      </filter></defs>
      <path d="M6,18 C120,10 250,24 372,14" stroke="#141009" strokeWidth={10} {...common} />
      <path d="M6,18 C120,10 250,24 372,14" stroke="#e9c877" strokeWidth={5} {...common} />
    </svg>
  );
};

const KineticBeat: React.FC<Beat> = ({ chip, lines, start, topDown }) => {
  const f = useCurrentFrame(); const { fps } = useVideoConfig();
  const chipS = spring({ frame: f - start, fps, config: { damping: 14, stiffness: 200, mass: 0.6 } });
  const chipScale = interpolate(chipS, [0, 1], [0.72, 1]);
  const chipO = interpolate(f, [start, start + 6], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  const ps = start + 26; // phrase begins after the chip
  const reveal = interpolate(f, [ps, ps + 50], [100, 0], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  const rise = interpolate(f, [ps, ps + 16], [26, 0], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  const phraseO = interpolate(f, [ps, ps + 12], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  return (
    <>
      <AbsoluteFill style={{ pointerEvents: "none", background: "linear-gradient(102deg, rgba(6,4,2,0.74) 0%, rgba(6,4,2,0.42) 32%, rgba(0,0,0,0) 54%)" }} />
      <div style={{ position: "absolute", left: 104, top: 372, width: 960 }}>
        <div style={{ opacity: chipO, transform: `scale(${chipScale})`, transformOrigin: "left center", fontFamily: "PermanentMarker", fontSize: 42, letterSpacing: 3, color: "#e9c877", textShadow: "0 3px 14px rgba(0,0,0,0.85)" }}>{chip}</div>
        <InkUnderline start={start + 6} dur={14} />
        <div style={{
          marginTop: 22, opacity: phraseO,
          clipPath: topDown ? `inset(0 0 ${reveal}% 0)` : undefined,
          transform: topDown ? undefined : `translateY(${rise}px)`,
          fontFamily: "PermanentMarker", fontSize: 64, lineHeight: 1.12, color: "#f7f2e6",
          WebkitTextStroke: "1.5px #0d0b07", paintOrder: "stroke fill", textShadow: "0 4px 16px rgba(0,0,0,0.85)",
        }}>
          {lines.map((l, i) => <React.Fragment key={i}>{l}{i < lines.length - 1 && <br />}</React.Fragment>)}
        </div>
      </div>
    </>
  );
};

// ---- one scene: living plate stretched to its narration window, + optional beat ----
const Scene: React.FC<{ id: number; durFrames: number; beat?: Beat }> = ({ id, durFrames, beat }) => {
  const rate = CLIP_DUR / (durFrames / FPS); // slow the 5s clip to fill the window
  return (
    <AbsoluteFill style={{ backgroundColor: "black" }}>
      <OffthreadVideo src={pc(id)} muted playbackRate={rate} style={FILL} />
      {beat && <KineticBeat {...beat} />}
    </AbsoluteFill>
  );
};

// ---- light film texture (reused from the trailer, dialed down) ----
const Grain: React.FC = () => {
  const f = useCurrentFrame();
  return (
    <AbsoluteFill style={{ mixBlendMode: "overlay", opacity: 0.06, pointerEvents: "none" }}>
      <svg width="1920" height="1080"><filter id="ew01-grain"><feTurbulence type="fractalNoise" baseFrequency="0.9" numOctaves="2" seed={f % 40} /></filter>
        <rect width="100%" height="100%" filter="url(#ew01-grain)" /></svg>
    </AbsoluteFill>
  );
};
const Vignette: React.FC = () => (
  <AbsoluteFill style={{ pointerEvents: "none", background: "radial-gradient(ellipse at 50% 46%, rgba(0,0,0,0) 52%, rgba(0,0,0,0.5) 100%)" }} />
);

// beat local-start = 40% into the scene window (approx; no forced alignment)
const beatStart = (id: number) => Math.round(0.4 * len(id) * FPS);

// build a run of contiguous scenes into laid-out Sequences given a slice start time
const Run: React.FC<{ ids: number[]; sliceStart: number; beats: Record<number, Beat> }> = ({ ids, sliceStart, beats }) => (
  <>
    {ids.map((id) => {
      const from = Math.round((WIN[id][0] - sliceStart) * FPS);
      const dur = Math.round(len(id) * FPS);
      return (
        <Sequence key={id} from={from} durationInFrames={dur}>
          <Scene id={id} durFrames={dur} beat={beats[id]} />
        </Sequence>
      );
    })}
  </>
);

// ================= slice compositions =================
const S5: Beat = { chip: "LEVITICUS 16:2", lines: ["I will appear in the cloud", "upon the mercy seat"], start: beatStart(5) };
const S17: Beat = { chip: "HEBREWS 9:12", lines: ["by his own blood", "he entered in once"], start: beatStart(17) };
const S18: Beat = { chip: "ISAIAH 53:6", lines: ["the LORD hath laid on him", "the iniquity of us all"], start: beatStart(18) };
const S20: Beat = { chip: "MATTHEW 27:51", lines: ["The veil of the temple", "was rent in twain —", "from the top to the bottom"], start: beatStart(20), topDown: true };

export const OPEN_FRAMES = Math.round(99 * FPS);
export const EW01Open: React.FC = () => {
  useInkFonts();
  return (
    <AbsoluteFill style={{ backgroundColor: "black" }}>
      <Audio src={aud("ew01_open_0_99.mp3")} />
      <Run ids={[1, 2, 3, 4, 5]} sliceStart={0} beats={{ 5: S5 }} />
      <Grain /><Vignette />
    </AbsoluteFill>
  );
};

export const CLIMAX_FRAMES = Math.round(113 * FPS);
export const EW01Climax: React.FC = () => {
  useInkFonts();
  return (
    <AbsoluteFill style={{ backgroundColor: "black" }}>
      <Audio src={aud("ew01_climax_338_451.mp3")} />
      <Run ids={[16, 17, 18, 19, 20]} sliceStart={338} beats={{ 17: S17, 18: S18, 20: S20 }} />
      <Grain /><Vignette />
    </AbsoluteFill>
  );
};

// Range: sc1-2 (dark) hard-cut to sc19-20 (warm). Two audio segments back to back.
const RANGE_A = Math.round(39 * FPS);        // sc1-2 = 0..39s
const RANGE_B = Math.round((451 - 405.8) * FPS); // sc19-20 = 45.2s
export const RANGE_FRAMES = RANGE_A + RANGE_B;
export const EW01Range: React.FC = () => {
  useInkFonts();
  return (
    <AbsoluteFill style={{ backgroundColor: "black" }}>
      {/* dark half */}
      <Sequence from={0} durationInFrames={RANGE_A}>
        <AbsoluteFill style={{ backgroundColor: "black" }}>
          <Audio src={aud("ew01_open_0_99.mp3")} endAt={RANGE_A} />
          <Run ids={[1, 2]} sliceStart={0} beats={{}} />
          <Grain /><Vignette />
        </AbsoluteFill>
      </Sequence>
      {/* warm half (sc19-20 lives at 67.8..113s inside the climax audio file) */}
      <Sequence from={RANGE_A} durationInFrames={RANGE_B}>
        <AbsoluteFill style={{ backgroundColor: "black" }}>
          <Audio src={aud("ew01_climax_338_451.mp3")} startFrom={Math.round((405.8 - 338) * FPS)} />
          <Run ids={[19, 20]} sliceStart={405.8} beats={{ 20: S20 }} />
          <Grain /><Vignette />
        </AbsoluteFill>
      </Sequence>
    </AbsoluteFill>
  );
};
