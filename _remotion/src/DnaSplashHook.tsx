// DNA HOOK v2 (2026-07-23) — COMIC-NATIVE alternative to the B&W-to-colour move.
// The cinematic noir reveal read flat on the retro-comic style (it's a MOVIE trick,
// not a COMIC trick). This version stays inside the medium: bold slammed panels with
// hand-drawn ink borders, a jagged ink impact-burst at each cut, a torn-gutter 2-panel
// beat, then the panel border PEELS AWAY to reveal the full-bleed wide landing shot.
// Colour stays on throughout — no grading trick needed. Same 4 existing clips, $0.
import React, { useEffect, useState } from "react";
import {
  AbsoluteFill, Img, OffthreadVideo, Audio, Sequence, staticFile, useCurrentFrame,
  useVideoConfig, interpolate, spring, delayRender, continueRender,
} from "remotion";

export const SPLASH_FPS = 30;
export const SPLASH_FRAMES = 360; // 12s — extended to let the gold Scripture beat breathe
const clip = (id: string) => staticFile(`dnapoc/${id}.mp4`);
const stillClip = (id: string) => staticFile(`dnapoc/${id}.png`);
const RED = new Set(["DIED", "TORE", "VEIL", "FREE", "TWO"]);
// DNA canonical palette (v2/AWAKEDEN_COMIC_DNA.md §2) — never pure black/white
const INK = "#231F20";
const NEWSPRINT = "#E8D9B5";
const GOLD = "#E9C877";
const CAPTION_YELLOW = "#FFE100";
const PROCESS_CYAN = "#00AEEF";
const PROCESS_MAGENTA = "#EC008C";

const useFonts = () => {
  const [h] = useState(() => delayRender("splashfonts"));
  useEffect(() => {
    Promise.all([
      new FontFace("Bangers", `url(${staticFile("Bangers.ttf")})`).load(),
      new FontFace("PermanentMarker", `url(${staticFile("PermanentMarker.ttf")})`).load(),
      new FontFace("Kalam", `url(${staticFile("Kalam-Bold.ttf")})`).load(),
    ]).then((ff) => { ff.forEach((f) => (document as any).fonts.add(f)); continueRender(h); })
      .catch(() => continueRender(h));
  }, [h]);
};

// hand-drawn roughen filter, referenced by border/panel elements
const RoughFilter: React.FC = () => (
  <svg width="0" height="0" style={{ position: "absolute" }}>
    <filter id="rough"><feTurbulence type="fractalNoise" baseFrequency="0.045" numOctaves="2" seed={7} result="n" />
      <feDisplacementMap in="SourceGraphic" in2="n" scale="7" /></filter>
  </svg>
);

// jagged ink-star impact burst, fires at a beat's opening frames
const ImpactBurst: React.FC<{ start: number; x: number; y: number; size?: number }> = ({ start, x, y, size = 420 }) => {
  const f = useCurrentFrame();
  const t = f - start;
  if (t < 0 || t > 14) return null;
  const progress = t / 14;
  const grow = Math.min(1, progress / 0.35);
  const scale = 0.3 + 0.7 * (1 - (1 - grow) ** 2);
  const alpha = progress < 0.4 ? 1 : Math.max(0, 1 - (progress - 0.4) / 0.6);
  const n = 14;
  const pts: string[] = [];
  for (let i = 0; i < n * 2; i++) {
    const ang = (i / (n * 2)) * Math.PI * 2;
    const long = i % 2 === 0;
    const r = (long ? size * 0.5 : size * 0.19) * scale * (1 + 0.08 * Math.sin(i * 3.1));
    pts.push(`${x + r * Math.cos(ang)},${y + r * Math.sin(ang)}`);
  }
  return (
    <svg width="100%" height="100%" style={{ position: "absolute", inset: 0, pointerEvents: "none" }}>
      <polygon points={pts.join(" ")} fill={INK} opacity={alpha * 0.92} filter="url(#rough)" />
    </svg>
  );
};

// a single hard-bordered comic panel showing a cropped/zoomed video, slams in
const Panel: React.FC<{
  id: string; from: number; left: number; top: number; width: number; height: number;
  zoom: number; panX: number; panY: number; slam?: boolean;
}> = ({ id, from, left, top, width, height, zoom, panX, panY, slam = true }) => {
  const f = useCurrentFrame(); const { fps } = useVideoConfig();
  const local = f - from;
  const s = spring({ frame: local, fps, config: { damping: 14, stiffness: 260, mass: 0.7 } });
  const sc = slam ? interpolate(s, [0, 1], [1.35, 1]) : 1;
  const rot = slam ? interpolate(s, [0, 1], [-3, 0]) : 0;
  const op = interpolate(local, [-2, 1], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  return (
    <div style={{
      position: "absolute", left: `${left}%`, top: `${top}%`, width: `${width}%`, height: `${height}%`,
      overflow: "hidden", opacity: op, transform: `scale(${sc}) rotate(${rot}deg)`,
      border: `10px solid ${INK}`, filter: "url(#rough)", boxShadow: "6px 6px 0 rgba(0,0,0,.5)",
      background: "#000",
    }}>
      <div style={{ width: "100%", height: "100%", transform: `scale(${zoom}) translate(${panX}%, ${panY}%)` }}>
        <OffthreadVideo src={clip(id)} muted style={{ width: "100%", height: "100%", objectFit: "cover" }} />
      </div>
    </div>
  );
};

// full-bleed landing plate — the panel border has dissolved away
const FullBleed: React.FC<{ id: string; from: number }> = ({ id, from }) => {
  const f = useCurrentFrame();
  const local = f - from;
  const sc = interpolate(local, [0, 24], [1.12, 1.0], { extrapolateRight: "clamp" });
  return (
    <AbsoluteFill style={{ overflow: "hidden" }}>
      <div style={{ width: "100%", height: "100%", transform: `scale(${sc})` }}>
        <OffthreadVideo src={clip(id)} muted style={{ width: "100%", height: "100%", objectFit: "cover" }} />
      </div>
    </AbsoluteFill>
  );
};

// the new purpose-built hero splash (Aaron + the two goats) — a still, not a clip
const StillFullBleed: React.FC<{ id: string; from: number; dur: number }> = ({ id, from, dur }) => {
  const f = useCurrentFrame();
  const local = f - from;
  const sc = interpolate(local, [0, dur], [1.14, 1.0], { extrapolateRight: "clamp" });
  return (
    <AbsoluteFill style={{ overflow: "hidden" }}>
      <div style={{ width: "100%", height: "100%", transform: `scale(${sc})` }}>
        <Img src={stillClip(id)} style={{ width: "100%", height: "100%", objectFit: "cover" }} />
      </div>
    </AbsoluteFill>
  );
};

// the narrator caption box (DNA §3: top-left, italic caps, comic-yellow — Kalam)
const CaptionBox: React.FC<{ text: string; start: number; dur: number }> = ({ text, start, dur }) => {
  const f = useCurrentFrame(); const { fps } = useVideoConfig();
  const local = f - start;
  const s = spring({ frame: local, fps, config: { damping: 16, stiffness: 180 } });
  const o = interpolate(local, [0, 8, dur - 10, dur], [0, 1, 1, 0], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  return (
    <div style={{
      position: "absolute", top: 56, left: 56, maxWidth: 640, opacity: o, zIndex: 20,
      transform: `translateX(${interpolate(s, [0, 1], [-30, 0])}px)`,
      background: CAPTION_YELLOW, border: `3px solid ${INK}`, boxShadow: "5px 5px 0 rgba(0,0,0,.45)",
      padding: "14px 18px", fontFamily: "Kalam", fontWeight: 700, fontStyle: "italic",
      textTransform: "uppercase", color: INK, fontSize: 27, lineHeight: 1.22, letterSpacing: 0.5,
    }}>{text}</div>
  );
};

// print texture: fine grain + a faint CMYK misregistration fringe (the DNA's own process inks)
const Grain: React.FC = () => {
  const f = useCurrentFrame();
  return (
    <AbsoluteFill style={{ mixBlendMode: "overlay", opacity: 0.055, pointerEvents: "none" }}>
      <svg width="1920" height="1080"><filter id="dsg"><feTurbulence type="fractalNoise" baseFrequency="0.85" numOctaves="2" seed={f % 40} /></filter>
        <rect width="100%" height="100%" filter="url(#dsg)" /></svg>
    </AbsoluteFill>
  );
};
const Misregister: React.FC = () => (
  <AbsoluteFill style={{ pointerEvents: "none" }}>
    <AbsoluteFill style={{ background: PROCESS_CYAN, mixBlendMode: "screen", opacity: 0.045, transform: "translateX(2px)" }} />
    <AbsoluteFill style={{ background: PROCESS_MAGENTA, mixBlendMode: "multiply", opacity: 0.045, transform: "translateX(-2px)" }} />
  </AbsoluteFill>
);

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
            WebkitTextStroke: `${Math.round(size * 0.05)}px ${INK}`, paintOrder: "stroke fill",
            textShadow: red ? "4px 4px 0 #3a0000, 0 0 24px rgba(224,20,20,.6)" : "4px 4px 0 #1a1a1a",
            margin: "0 .18em",
          }}>{w}</span>;
        })}
      </div>
    </AbsoluteFill>
  );
};

// torn ink gutter between the two split panels
const Gutter: React.FC = () => (
  <div style={{
    position: "absolute", left: "49%", top: 0, width: "2%", height: "100%",
    background: NEWSPRINT, filter: "url(#rough)", zIndex: 5,
  }} />
);

// the DNA's LOCKED gold kinetic Scripture treatment (ported from DnaPocFilm's
// Scripture component, §3: "Scripture must never look like ordinary speech") —
// the signature move this hook was missing.
const GoldScripture: React.FC<{ lines: string[]; cite: string; start: number }> = ({ lines, cite, start }) => {
  const f = useCurrentFrame();
  const chipO = interpolate(f, [start, start + 10], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  const ps = start + 16;
  const reveal = interpolate(f, [ps, ps + 46], [100, 0], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  const o = interpolate(f, [ps, ps + 14], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  return (
    <AbsoluteFill style={{ justifyContent: "center", alignItems: "center" }}>
      <AbsoluteFill style={{ pointerEvents: "none", background: "radial-gradient(ellipse at 50% 55%, rgba(0,0,0,.55) 0%, rgba(0,0,0,.18) 55%, rgba(0,0,0,0) 78%)" }} />
      <div style={{ textAlign: "center", maxWidth: 1500 }}>
        <div style={{
          opacity: chipO, fontFamily: "PermanentMarker", fontSize: 30, letterSpacing: 4,
          color: GOLD, textShadow: "0 3px 12px rgba(0,0,0,.85)", marginBottom: 14,
        }}>{cite}</div>
        <div style={{
          opacity: o, clipPath: `inset(0 0 ${reveal}% 0)`,
          fontFamily: "PermanentMarker", fontSize: 68, lineHeight: 1.22, color: GOLD,
          WebkitTextStroke: "1.5px #0d0b07", paintOrder: "stroke fill",
          textShadow: "0 4px 18px rgba(0,0,0,.9)",
        }}>{lines.map((l, i) => <React.Fragment key={i}>{l}{i < lines.length - 1 && <br />}</React.Fragment>)}</div>
      </div>
    </AbsoluteFill>
  );
};

const White: React.FC<{ at: number }> = ({ at }) => {
  const f = useCurrentFrame();
  const o = interpolate(f - at, [-1, 0, 5], [0, 0.85, 0], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  return <AbsoluteFill style={{ background: "#fff", opacity: o, pointerEvents: "none" }} />;
};

// beats: [clipId, from, dur, panelKind, zoom, panX, panY]
const BEATS: [string, number, number, "single" | "splitL" | "splitR", number, number, number][] = [
  ["02_event", 0, 40, "single", 1.08, 2, -1],
  ["01_establish", 40, 40, "splitL", 1.05, 0, 0],
  ["03_reaction", 40, 40, "splitR", 1.1, -2, 1],
  ["02_event", 80, 40, "single", 1.15, -3, 3],
  ["03_reaction", 120, 40, "single", 1.08, 1, -1],
];
const SLAMS: [number, string, number, number][] = [
  [4, "ONE DIED.", 148, 12], [46, "ONE WALKED FREE.", 108, 12], [86, "WHY TWO?", 148, 12],
  [126, "THE VEIL TORE.", 108, 12], [164, "TWO GOATS", 168, 40],
];
// DNA §5a: "NO SFX graphic on the crucifixion / veil-tear / resurrection — stillness
// only." Beats 0/40/80/120 are all passion content (02_event / 03_reaction) — the only
// beat that legitimately earns a punch is the title-card reveal at 162.
const BURSTS = [162];
const TWO_GOATS_START = 160;
const TWO_GOATS_DUR = 48; // its own beat now — not borrowed from the "welcome" landing shot
const WELCOME_START = TWO_GOATS_START + TWO_GOATS_DUR; // 208
const SCRIPTURE_START = WELCOME_START + 2; // after the title slam settles — sacred stillness before the gold reveal
const CTA_START = 322;

export const DnaSplashHook: React.FC = () => {
  useFonts();
  return (
    <AbsoluteFill style={{ backgroundColor: INK }}>
      <RoughFilter />
      <Audio src={staticFile("trailer_audio.mp3")} />

      {BEATS.map(([id, from, dur, kind, zoom, panX, panY], i) => {
        if (kind === "single") {
          return (
            <Sequence key={i} from={from} durationInFrames={dur}>
              <Panel id={id} from={0} left={4} top={4} width={92} height={92} zoom={zoom} panX={panX} panY={panY} />
            </Sequence>
          );
        }
        return (
          <Sequence key={i} from={from} durationInFrames={dur}>
            <Panel id={id} from={0} left={kind === "splitL" ? 2 : 51} top={4} width={47} height={92} zoom={zoom} panX={panX} panY={panY} />
          </Sequence>
        );
      })}
      <Sequence from={40} durationInFrames={40}><Gutter /></Sequence>

      <Sequence from={TWO_GOATS_START} durationInFrames={TWO_GOATS_DUR}>
        <StillFullBleed id="two_goats_splash" from={0} dur={TWO_GOATS_DUR} />
      </Sequence>

      <Sequence from={WELCOME_START} durationInFrames={SPLASH_FRAMES - WELCOME_START}>
        <FullBleed id="04_welcome" from={0} />
      </Sequence>

      {BURSTS.map((b, i) => <ImpactBurst key={i} start={b} x={960} y={540} />)}
      {BURSTS.map((b, i) => <White key={`w${i}`} at={b} />)}

      <Sequence from={0} durationInFrames={38}><CaptionBox text="Once a year, one man carried blood behind the veil." start={0} dur={38} /></Sequence>

      {SLAMS.map(([from, text, size, y], i) => {
        const next = SLAMS[i + 1]?.[0] ?? WELCOME_START;
        return <Sequence key={`s${i}`} from={from} durationInFrames={Math.min(next - from, 58)}><Slam text={text} size={size} y={y} /></Sequence>;
      })}

      <Sequence from={SCRIPTURE_START} durationInFrames={CTA_START - SCRIPTURE_START}>
        <GoldScripture cite="LEVITICUS 17:11" lines={["It is the blood", "that maketh atonement."]} start={0} />
      </Sequence>

      <Sequence from={CTA_START} durationInFrames={SPLASH_FRAMES - CTA_START}>
        <Slam text="come to Jesus." size={80} y={12} />
      </Sequence>

      <Grain />
      <Misregister />
    </AbsoluteFill>
  );
};
