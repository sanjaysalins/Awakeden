// DNA HOOK (2026-07-23, RESET to the origin approach) — like the noir trailer:
// a real BAKED black-&-white clip is the base, and the COLOUR clip fades in on
// top via OPACITY at the veil-tear reveal. No live grayscale filter (that was the
// dull-grey culprit). Red slam words stay red (spot colour).
import React, { useEffect, useState } from "react";
import {
  AbsoluteFill, OffthreadVideo, Audio, Sequence, staticFile, useCurrentFrame,
  useVideoConfig, interpolate, spring, delayRender, continueRender,
} from "remotion";

export const HOOK_FPS = 30;
export const HOOK_FRAMES = 300; // 10s
const BLOOM_A = 128, BLOOM_B = 168; // colour blooms in over the veil-tear beat
const FILL = { width: "100%", height: "100%", objectFit: "cover" as const };
const clip = (id: string) => staticFile(`dnapoc/${id}.mp4`);       // colour
const clipBw = (id: string) => staticFile(`dnapoc/${id}_bw.mp4`);   // baked stark B&W
const RED = new Set(["DIED", "TORE", "VEIL", "FREE"]);

const useFonts = () => {
  const [h] = useState(() => delayRender("hookfonts"));
  useEffect(() => {
    new FontFace("Bangers", `url(${staticFile("Bangers.ttf")})`).load()
      .then((f) => { (document as any).fonts.add(f); continueRender(h); }).catch(() => continueRender(h));
  }, [h]);
};

// baked B&W base + colour fading in on top (opacity ONLY — the origin move)
const Cut: React.FC<{ id: string; from: number; dur: number; zoom?: number }> = ({ id, from, dur, zoom = 1.08 }) => {
  const local = useCurrentFrame();
  const global = from + local;
  const col = interpolate(global, [BLOOM_A, BLOOM_B], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" }); // 0 = B&W, 1 = colour
  const sc = interpolate(local, [0, dur], [1.0, zoom]);
  const st = { ...FILL, transform: `scale(${sc})` };
  return (
    <AbsoluteFill style={{ overflow: "hidden" }}>
      <OffthreadVideo src={clipBw(id)} muted style={st} />
      <AbsoluteFill style={{ opacity: col }}><OffthreadVideo src={clip(id)} muted style={st} /></AbsoluteFill>
    </AbsoluteFill>
  );
};

const Slam: React.FC<{ text: string; size: number; y: number }> = ({ text, size, y }) => {
  const f = useCurrentFrame(); const { fps } = useVideoConfig();
  const s = spring({ frame: f, fps, config: { damping: 12, stiffness: 210, mass: 0.6 } });
  const sc = interpolate(s, [0, 1], [2.1, 1]); const rot = interpolate(s, [0, 1], [-6, 0]);
  const o = interpolate(f, [0, 2], [0, 1], { extrapolateRight: "clamp" });
  return (
    <AbsoluteFill style={{ justifyContent: "flex-end", alignItems: "center", paddingBottom: `${y}%` }}>
      <div style={{ transform: `scale(${sc}) rotate(${rot}deg)`, opacity: o, textAlign: "center", lineHeight: 1 }}>
        {text.split(" ").map((w, i) => {
          const red = RED.has(w.replace(/[.,—!?]/g, ""));
          return <span key={i} style={{
            fontFamily: "Bangers", fontSize: size, letterSpacing: 3, color: red ? "#e01414" : "#f4e9d0",
            WebkitTextStroke: `${Math.round(size * 0.05)}px #0d0b07`, paintOrder: "stroke fill",
            textShadow: red ? "4px 4px 0 #3a0000, 0 0 24px rgba(224,20,20,.6)" : "4px 4px 0 #1a1a1a",
            margin: "0 .18em",
          }}>{w}</span>;
        })}
      </div>
    </AbsoluteFill>
  );
};

const Flash: React.FC<{ at: number[]; bloom: number }> = ({ at, bloom }) => {
  const f = useCurrentFrame();
  const cuts = Math.max(0, ...at.map((a) => interpolate(f - a, [0, 6], [0.35, 0], { extrapolateLeft: "clamp", extrapolateRight: "clamp" })));
  const b = interpolate(f - bloom, [0, 8, 20], [0, 0.8, 0], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  return <AbsoluteFill style={{ background: "#fff", opacity: Math.max(cuts, b), pointerEvents: "none" }} />;
};
const Vignette: React.FC = () => <AbsoluteFill style={{ pointerEvents: "none", background: "radial-gradient(ellipse at 50% 48%, rgba(0,0,0,0) 70%, rgba(0,0,0,.18) 100%)" }} />;

const CUTS: [string, number, number, number][] = [
  ["02_event", 0, 42, 1.10], ["01_establish", 42, 42, 1.08], ["03_reaction", 84, 40, 1.12],
  ["02_event", 124, 40, 1.14], ["04_welcome", 164, 136, 1.07],
];
const SLAMS: [number, string, number, number][] = [
  [4, "ONE DIED.", 150, 12], [46, "ONE WALKED FREE.", 120, 12], [88, "WHY TWO?", 150, 12],
  [128, "THE VEIL TORE.", 120, 12], [186, "TWO GOATS", 168, 40], [236, "come to Jesus.", 82, 12],
];

export const DnaTrailerHook: React.FC = () => {
  useFonts();
  return (
    <AbsoluteFill style={{ backgroundColor: "black" }}>
      <Audio src={staticFile("trailer_audio.mp3")} />
      {CUTS.map(([id, from, dur, zoom], i) =>
        <Sequence key={i} from={from} durationInFrames={dur}><Cut id={id} from={from} dur={dur} zoom={zoom} /></Sequence>)}
      <Vignette />
      {SLAMS.map(([from, text, size, y], i) => {
        const next = SLAMS[i + 1]?.[0] ?? HOOK_FRAMES;
        return <Sequence key={`s${i}`} from={from} durationInFrames={Math.min(next - from, 56)}><Slam text={text} size={size} y={y} /></Sequence>;
      })}
      <Flash at={[0, 42, 84, 124]} bloom={BLOOM_A} />
    </AbsoluteFill>
  );
};
