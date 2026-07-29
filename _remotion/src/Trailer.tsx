import React, { useEffect, useState } from "react";
import {
  AbsoluteFill, Audio, OffthreadVideo, staticFile, Sequence,
  useCurrentFrame, useVideoConfig, interpolate, spring, delayRender, continueRender,
} from "remotion";

export const TRAILER_FPS = 30;
export const TRAILER_FRAMES = 1140; // 38s

const clip = (id: number) => staticFile(`clips/${String(id).padStart(2, "0")}.mp4`); // full colour
const noir = (id: number) => staticFile(`noir/${String(id).padStart(2, "0")}.mp4`);  // baked noir + spot red

const useFonts = () => {
  const [h] = useState(() => delayRender("fonts"));
  useEffect(() => {
    const b = new FontFace("Bangers", `url(${staticFile("Bangers.ttf")})`);
    b.load().then((f) => { (document as any).fonts.add(f); continueRender(h); })
      .catch(() => continueRender(h));
  }, [h]);
};

// noir -> colour bloom at the veil tear; drives the per-cell crossfade
const bloomAt = (gf: number) => interpolate(gf, [762, 800], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
type Mode = "noir" | "color" | "bloom";
const cellMode = (from: number, dur: number): Mode => {
  const end = from + dur;
  if (end <= 762) return "noir";
  if (from >= 800) return "color";
  return "bloom";
};
const FILL = { width: "100%", height: "100%", objectFit: "cover" } as const;

const Clip: React.FC<{ id: number; dur: number; from: number; mode: Mode; push?: boolean }> = ({ id, dur, from, mode, push }) => {
  const lf = useCurrentFrame();
  const s = push ? interpolate(lf, [0, dur], [1.02, 1.11]) : interpolate(lf, [0, dur], [1.07, 1.02]);
  const b = mode === "bloom" ? bloomAt(from + lf) : mode === "color" ? 1 : 0;
  const st = { ...FILL, transform: `scale(${s})` };
  return (
    <AbsoluteFill style={{ overflow: "hidden" }}>
      {mode !== "color" && <OffthreadVideo src={noir(id)} muted style={st} />}
      {mode !== "noir" && <AbsoluteFill style={{ opacity: b }}><OffthreadVideo src={clip(id)} muted style={st} /></AbsoluteFill>}
    </AbsoluteFill>
  );
};

const Grid: React.FC<{ ids: number[]; from: number; dur: number; mode: Mode }> = ({ ids, from, dur, mode }) => {
  const lf = useCurrentFrame();
  const b = mode === "bloom" ? bloomAt(from + lf) : mode === "color" ? 1 : 0;
  return (
    <AbsoluteFill style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gridTemplateRows: "1fr 1fr", gap: 6, background: "#0a0806" }}>
      {ids.slice(0, 4).map((id, i) => (
        <div key={i} style={{ overflow: "hidden", position: "relative" }}>
          {mode !== "color" && <OffthreadVideo src={noir(id)} muted style={FILL} />}
          {mode !== "noir" && <div style={{ position: "absolute", inset: 0, opacity: b }}><OffthreadVideo src={clip(id)} muted style={FILL} /></div>}
        </div>
      ))}
    </AbsoluteFill>
  );
};

// blood-theme words bleed red in the noir — the breadcrumb the eye tracks
const RED_WORDS = new Set(["KILLED", "BLOOD", "TORE", "VEIL", "DIED", "PRICE"]);

const Slam: React.FC<{ text: string; size: number; y: number; variant: number }> = ({ text, size, y, variant }) => {
  const f = useCurrentFrame();
  const { fps } = useVideoConfig();
  const s = spring({ frame: f, fps, config: { damping: 12, stiffness: 210, mass: 0.6 } });
  const lines = text.split("\n");
  let transform = "";
  if (variant === 0) {
    const sc = interpolate(s, [0, 1], [2.3, 1]); const r = interpolate(s, [0, 1], [-7, 0]);
    transform = `scale(${sc}) rotate(${r}deg)`;
  } else {
    const x = interpolate(s, [0, 1], [-520, 0]); const sk = interpolate(s, [0, 1], [-14, 0]);
    transform = `translateX(${x}px) skewX(${sk}deg)`;
  }
  const opacity = interpolate(f, [0, 2], [0, 1], { extrapolateRight: "clamp" });
  return (
    <AbsoluteFill>
      <div style={{ position: "absolute", top: y, width: "100%", textAlign: "center", transform, opacity }}>
        {lines.map((ln, i) => (
          <div key={i} style={{ fontFamily: "Bangers", fontSize: size, lineHeight: 1.0, letterSpacing: 3, paintOrder: "stroke fill" }}>
            {ln.split(" ").map((w, j, arr) => {
              const red = RED_WORDS.has(w.replace(/[^A-Z]/g, ""));
              return (
                <span key={j} style={{
                  color: red ? "#e01414" : "#f7f2e6",
                  WebkitTextStroke: red ? "9px #240202" : "9px #0d0b07",
                  textShadow: red
                    ? "0 8px 0 rgba(0,0,0,0.42), 0 0 34px rgba(224,20,20,0.7)"
                    : "0 8px 0 rgba(0,0,0,0.42), 0 0 26px rgba(0,0,0,0.5)",
                }}>{w}{j < arr.length - 1 ? " " : ""}</span>
              );
            })}
          </div>
        ))}
      </div>
    </AbsoluteFill>
  );
};

const Grain: React.FC = () => {
  const f = useCurrentFrame();
  return (
    <AbsoluteFill style={{ opacity: 0.07, mixBlendMode: "overlay", pointerEvents: "none" }}>
      <svg width="1920" height="1080">
        <filter id="n"><feTurbulence type="fractalNoise" baseFrequency="0.9" numOctaves="2" seed={f % 40} /></filter>
        <rect width="100%" height="100%" filter="url(#n)" />
      </svg>
    </AbsoluteFill>
  );
};
const Vignette: React.FC = () => (
  <AbsoluteFill style={{ background: "radial-gradient(ellipse at center, rgba(0,0,0,0) 52%, rgba(0,0,0,0.55) 100%)", pointerEvents: "none" }} />
);
const FLASHES = [123, 418, 609, 771];
const Flash: React.FC = () => {
  const f = useCurrentFrame();
  let o = 0;
  for (const ff of FLASHES) { const d = f - ff; if (d >= 0 && d < 8) o = Math.max(o, interpolate(d, [0, 8], [0.55, 0])); }
  return <AbsoluteFill style={{ background: "white", opacity: o, pointerEvents: "none" }} />;
};

const RAW: [number, "clip" | "grid", number[], boolean?][] = [
  [44, "clip", [4]], [40, "clip", [1], true], [39, "clip", [3]], [41, "clip", [4]],
  [33, "clip", [5], true], [32, "grid", [1, 3, 4, 5]], [30, "clip", [2]], [29, "grid", [2, 4, 3, 5]],
  [22, "grid", [7, 8, 9, 10]], [22, "clip", [7]], [24, "clip", [8]], [24, "clip", [11]],
  [19, "clip", [10]], [19, "clip", [9]], [21, "clip", [7], true], [21, "grid", [7, 10, 8, 11]],
  [21, "clip", [6]], [22, "clip", [14]], [30, "grid", [6, 14, 15, 12]], [30, "clip", [13]],
  [23, "clip", [15]], [23, "grid", [15, 6, 14, 13]], [34, "clip", [15], true], [33, "clip", [16]],
  [22, "clip", [17], true], [21, "clip", [20]], [52, "clip", [20], true],
  [40, "clip", [23]], [35, "clip", [23], true], [35, "clip", [20]], [46, "clip", [24]],
  [28, "grid", [11, 10, 25, 23]], [28, "clip", [11]], [35, "clip", [10]], [52, "clip", [25], true],
];
let acc = 0;
const CELLS = RAW.map(([d, type, ids, push]) => { const from = acc; acc += d; return { from, dur: d, type, ids, push, mode: cellMode(from, d) }; });

const SLAMS = [
  { f: 44, t: "ONCE A YEAR", size: 150, y: 430, v: 0 },
  { f: 84, t: "ONE MAN", size: 190, y: 420, v: 1 },
  { f: 123, t: "ONE DOOR", size: 190, y: 420, v: 0 },
  { f: 164, t: "A HOLINESS\nTHAT COULD KILL", size: 108, y: 340, v: 1 },
  { f: 288, t: "TWO GOATS", size: 220, y: 400, v: 0 },
  { f: 332, t: "ONE KILLED", size: 155, y: 130, v: 1 },
  { f: 380, t: "ONE SET FREE", size: 145, y: 770, v: 1 },
  { f: 418, t: "WHY TWO?", size: 230, y: 400, v: 0 },
  { f: 460, t: "SAME BLOOD", size: 155, y: 430, v: 1 },
  { f: 503, t: "SAME DOOR", size: 155, y: 130, v: 0 },
  { f: 563, t: "EVERY YEAR", size: 170, y: 430, v: 1 },
  { f: 609, t: "NEVER ENOUGH", size: 160, y: 770, v: 0 },
  { f: 676, t: "UNTIL ONE\nPRIEST SAT DOWN", size: 112, y: 340, v: 1 },
  { f: 771, t: "THE VEIL TORE", size: 190, y: 410, v: 0 },
  { f: 881, t: "THE DOOR NEVER\nCLOSED AGAIN", size: 108, y: 340, v: 1 },
  { f: 927, t: "ONE GOAT DIED", size: 145, y: 130, v: 0 },
  { f: 983, t: "ONE GOAT WENT FREE", size: 125, y: 770, v: 1 },
  { f: 1018, t: "BOTH WERE\nPOINTING AT HIM", size: 116, y: 360, v: 0 },
];
const SLAM_SEQ = SLAMS.map((s, i) => { const next = i < SLAMS.length - 1 ? SLAMS[i + 1].f : 1140; return { ...s, dur: Math.min(next - s.f, 52) }; });

const Title: React.FC = () => {
  const f = useCurrentFrame(); const { fps } = useVideoConfig();
  const s = spring({ frame: f, fps, config: { damping: 13, stiffness: 120 } });
  const sc = interpolate(s, [0, 1], [1.4, 1]);
  const subO = interpolate(f, [14, 28], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  return (
    <AbsoluteFill>
      <OffthreadVideo src={clip(25)} muted style={{ ...FILL, filter: "brightness(0.5)" }} />
      <AbsoluteFill style={{ justifyContent: "center", alignItems: "center", flexDirection: "column" }}>
        <div style={{ fontFamily: "Bangers", fontSize: 230, color: "#f7f2e6", WebkitTextStroke: "9px #0d0b07", paintOrder: "stroke fill", letterSpacing: 5, transform: `scale(${sc})` }}>TWO GOATS</div>
        <div style={{ fontFamily: "Bangers", fontSize: 64, color: "#e9c877", letterSpacing: 4, opacity: subO, marginTop: 10 }}>THE DAY THE VEIL TORE</div>
      </AbsoluteFill>
    </AbsoluteFill>
  );
};

export const Trailer: React.FC = () => {
  useFonts();
  return (
    <AbsoluteFill style={{ backgroundColor: "black" }}>
      <Audio src={staticFile("trailer_audio.mp3")} />
      <AbsoluteFill>
        {CELLS.map((c, i) => (
          <Sequence key={i} from={c.from} durationInFrames={c.dur}>
            {c.type === "grid"
              ? <Grid ids={c.ids} from={c.from} dur={c.dur} mode={c.mode} />
              : <Clip id={c.ids[0]} dur={c.dur} from={c.from} mode={c.mode} push={c.push} />}
          </Sequence>
        ))}
        <Sequence from={1070} durationInFrames={70}><Title /></Sequence>
        <Grain />
      </AbsoluteFill>
      <Vignette />
      <Flash />
      <AbsoluteFill>
        {SLAM_SEQ.filter((s) => s.f < 1070).map((s, i) => (
          <Sequence key={i} from={Math.max(0, s.f - 4)} durationInFrames={s.dur + 4}>
            <Slam text={s.t} size={s.size} y={s.y} variant={s.v} />
          </Sequence>
        ))}
      </AbsoluteFill>
    </AbsoluteFill>
  );
};
