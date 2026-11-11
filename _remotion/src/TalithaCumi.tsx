// Talitha Cumi (Swirls ep6, vector POC) - Remotion "elevate" overlay.
// Design: poc_living_water_ink_style_test/swirls_episode_06_talitha_cumi/style_poc_vector/remotion_design/DESIGN.md
// Base video + audio untouched; text pills + the "Overruled Word" strike on top.
// Frame times re-checked against short_g5/narration.mp3 pauses (silencedetect).
import React, { useEffect, useState } from "react";
import {
  AbsoluteFill, OffthreadVideo, Sequence, staticFile, useCurrentFrame,
  interpolate, Easing, delayRender, continueRender,
} from "remotion";

export const TC_FPS = 30;
export const TC_FRAMES = 1614;

export const C = {
  cream: "#F6E9CA", teal: "#0E434D", navy: "#15253C", turq: "#2DAFB1",
  orange: "#EE8D44", burnt: "#BE6829", gold: "#F2B63C", ink: "#101418",
};
const OUT = Easing.out(Easing.cubic);
const clamp = { extrapolateLeft: "clamp", extrapolateRight: "clamp" } as const;

export const useFonts = () => {
  const [h] = useState(() => delayRender("talitha-fonts"));
  useEffect(() => {
    Promise.all([
      new FontFace("Kalam", `url(${staticFile("Kalam-Bold.ttf")})`, { weight: "700" }).load(),
      new FontFace("Kalam", `url(${staticFile("Kalam-Regular.ttf")})`, { weight: "400" }).load(),
    ]).then((ff) => { ff.forEach((f) => (document as any).fonts.add(f)); continueRender(h); })
      .catch(() => continueRender(h));
  }, [h]);
};

type Line = { text: string; at: number }; // at = frame (relative to Sequence) the line appears
type PillProps = {
  lines: Line[]; size: number; y: number; end: number; // end = relative frame fade-out finishes
  fadeOut?: number; fill?: string; tab?: string; jesus?: boolean; tabSize?: number;
  chip?: string; chipAt?: number; lineRise?: number; lineFade?: number; settle?: boolean;
  extraOpacity?: number; extraScale?: number;
};

export const Pill: React.FC<PillProps> = ({
  lines, size, y, end, fadeOut = 8, fill = "rgba(14,67,77,0.66)", tab, jesus, tabSize = 40,
  chip, chipAt = 0, lineRise = 18, lineFade = 8, settle, extraOpacity = 1, extraScale = 1,
}) => {
  const f = useCurrentFrame();
  const start = lines[0].at;
  const boxIn = settle ? 1 : interpolate(f, [start, start + lineFade], [0, 1], { ...clamp, easing: OUT });
  const boxOut = interpolate(f, [end - fadeOut, end], [1, 0], clamp);
  const rise = settle ? 0 : interpolate(f, [start, start + lineFade], [lineRise, 0], { ...clamp, easing: OUT });
  const sc = settle ? interpolate(f, [0, 6], [1.06, 1], { ...clamp, easing: OUT }) : 1;
  const tabH = tabSize * 1.25 + 8;
  return (
    <div style={{
      position: "absolute", top: y, left: 0, width: 1080, display: "flex", justifyContent: "center",
      opacity: boxIn * boxOut * extraOpacity, transform: `translateY(${rise}px) scale(${sc * extraScale})`,
    }}>
      <div style={{
        position: "relative", maxWidth: 920, background: fill, borderRadius: 44,
        border: `4px solid rgba(246,233,202,0.9)`, padding: "26px 44px",
        fontFamily: "Kalam", fontWeight: 700, fontSize: size, lineHeight: 1.15, color: C.cream,
        textShadow: "0 3px 0 rgba(16,20,24,.55)", textAlign: "center", whiteSpace: "nowrap",
      }}>
        {tab && (
          <div style={{
            position: "absolute", top: -tabH / 2, left: 40, borderRadius: 20, padding: "4px 22px",
            background: jesus ? C.turq : C.burnt, color: jesus ? C.ink : C.cream,
            fontSize: tabSize, lineHeight: 1.25, textShadow: "none",
          }}>{tab}</div>
        )}
        {lines.map((l, i) => {
          const o = i === 0 || (settle && l.at === start) ? 1 : interpolate(f, [l.at, l.at + lineFade], [0, 1], { ...clamp, easing: OUT });
          const r = i === 0 ? 0 : interpolate(f, [l.at, l.at + lineFade], [lineRise * 0.67, 0], { ...clamp, easing: OUT });
          return <div key={i} style={{ opacity: o, transform: `translateY(${r}px)` }}>{l.text}</div>;
        })}
        {chip && (
          <div style={{
            position: "absolute", bottom: -26, right: 40, borderRadius: 999, padding: "2px 24px",
            background: C.gold, color: C.ink, fontSize: 38, lineHeight: 1.25, textShadow: "none",
            opacity: interpolate(f, [chipAt, chipAt + 8], [0, 1], clamp),
          }}>{chip}</div>
        )}
      </div>
    </div>
  );
};

// One wobbly brush stroke, x 150 -> 1100 (off the right edge), drawn by dashoffset.
const Strike: React.FC<{ cy: number; from: number; dur?: number; opacity?: number }> = ({ cy, from, dur = 24, opacity = 1 }) => {
  const f = useCurrentFrame();
  const p = interpolate(f, [from, from + dur], [0, 1], { ...clamp, easing: OUT });
  const d = `M150 ${cy + 10} C 330 ${cy - 6}, 520 ${cy + 8}, 700 ${cy - 4} S 960 ${cy - 14}, 1110 ${cy - 22}`;
  const dry = `M170 ${cy + 26} C 340 ${cy + 12}, 540 ${cy + 22}, 720 ${cy + 12} S 960 ${cy}, 1110 ${cy - 6}`;
  if (p <= 0) return null;
  return (
    <svg width={1080} height={1920} style={{ position: "absolute", left: 0, top: 0, opacity }}>
      <path d={d} pathLength={1} fill="none" stroke={C.orange} strokeWidth={26} strokeLinecap="round"
        strokeDasharray={1} strokeDashoffset={1 - p} />
      <path d={dry} pathLength={1} fill="none" stroke={C.orange} strokeOpacity={0.6} strokeWidth={6}
        strokeLinecap="round" strokeDasharray={1} strokeDashoffset={1 - p} />
    </svg>
  );
};

// Beats 3+4: "Too late." lands (f372), struck on "and did not turn back" (f450). Crosses the p2->p3 cut.
const TooLateFirst: React.FC = () => {
  const f = useCurrentFrame(); // 0 = f372
  const drop = interpolate(f, [0, 5], [-40, 0], { ...clamp, easing: OUT });
  const dim = interpolate(f, [90, 100], [1, 0.45], clamp);
  const shrink = interpolate(f, [90, 100], [1, 0.9], clamp);
  const out = interpolate(f, [126, 138], [1, 0], clamp);
  return (
    <AbsoluteFill style={{ transform: `translateY(${drop}px)` }}>
      <Pill lines={[{ text: "Too late.", at: 0 }]} size={150} y={1300} end={140} fadeOut={1}
        fill="rgba(21,37,60,0.80)" lineFade={5} lineRise={0} extraOpacity={dim} extraScale={shrink} />
      <Strike cy={1412} from={78} opacity={out} />
    </AbsoluteFill>
  );
};

// Beat 8: small "Too late." (f1330), struck on "hear Him instead" (f1362), then pushed up and aside.
const TooLateClose: React.FC = () => {
  const f = useCurrentFrame(); // 0 = f1330
  const up = interpolate(f, [56, 74], [0, -250], { ...clamp, easing: Easing.inOut(Easing.cubic) });
  const dim = interpolate(f, [56, 74], [1, 0.45], clamp);
  const shrink = interpolate(f, [56, 74], [1, 0.7], { ...clamp, easing: Easing.inOut(Easing.cubic) });
  const out = interpolate(f, [100, 116], [1, 0], clamp); // gone before His words land (f1446)
  return (
    <AbsoluteFill style={{ transform: `translateY(${up}px)`, opacity: out }}>
      <Pill lines={[{ text: "Too late.", at: 0 }]} size={96} y={1260} end={9999}
        fill="rgba(21,37,60,0.80)" lineFade={5} extraOpacity={dim} extraScale={shrink} />
      <Strike cy={1342} from={32} opacity={dim} />
    </AbsoluteFill>
  );
};

const EndFade: React.FC = () => {
  const f = useCurrentFrame();
  return <AbsoluteFill style={{ background: C.teal, opacity: interpolate(f, [TC_FRAMES - 8, TC_FRAMES - 1], [0, 1], clamp) }} />;
};

// <S from to> = Sequence covering absolute frames [from, to)
const S: React.FC<{ from: number; to: number; children: React.ReactNode }> = ({ from, to, children }) => (
  <Sequence from={from} durationInFrames={to - from} layout="none">{children}</Sequence>
);

export const TalithaCumi: React.FC = () => {
  useFonts();
  return (
    <AbsoluteFill style={{ background: "#000" }}>
      <OffthreadVideo src={staticFile("talitha/base.mp4")} />
      <AbsoluteFill>
        {/* 1 HOOK 0-5.3 s (voice: "my little girl is dying" 2.65-4.03 s) */}
        <S from={0} to={160}>
          <Pill settle lines={[{ text: "My little girl", at: 0 }, { text: "is dying.", at: 0 }]}
            size={96} y={180} end={159} tab="A father begs Jesus" tabSize={48} />
        </S>
        {/* 2 "Thy daughter is dead" 7.86 s */}
        <S from={237} to={358}>
          <Pill lines={[{ text: "Thy daughter", at: 0 }, { text: "is dead", at: 0 }]} size={96} y={1240}
            end={120} tab="News from his house" chip="Mark 5:35" chipAt={4} />
          {/* plain-English echo of "why troublest thou the Master any further?" (spoken 9.18 s); 4 of 5 blind seats */}
          <Pill lines={[{ text: "Why bother the Teacher now?", at: 38 }]} size={64} y={1050} end={120} />
        </S>
        {/* 3+4 THE OVERRULED WORD: lands 12.4 s, struck 15.0 s */}
        <S from={372} to={512}><TooLateFirst /></S>
        {/* 5 Jesus: "Be not afraid," 17.72 s / "only believe." 19.25 s */}
        <S from={530} to={613}>
          <Pill lines={[{ text: "Be not afraid,", at: 0 }, { text: "only believe.", at: 47 }]} size={96} y={210}
            end={82} fadeOut={12} tab="Jesus" jesus chip="Mark 5:36" chipAt={47} />
        </S>
        {/* p4 hand 20.2-25.3 s: nothing */}
        {/* 6 "Talitha cumi." 25.33 s, held through "Damsel, I say unto thee, arise." (27.5-31.0 s) */}
        <S from={759} to={970}>
          <Pill lines={[{ text: "Talitha cumi.", at: 0 }]} size={112} y={210} end={210} fadeOut={12}
            tab="Jesus" jesus chip="Mark 5:41" chipAt={18} lineFade={14} lineRise={12} />
          {/* meaning shown WITH the words (3 of 5 blind seats: no "magic word" on the miracle) */}
          <Pill lines={[{ text: "Little girl, get up.", at: 30 }]} size={76} y={470} end={210} fadeOut={12} />
        </S>
        {/* 7 "She got up" 34.91 s / "and walked." ~35.5 s */}
        <S from={1046} to={1124}>
          <Pill lines={[{ text: "She got up", at: 0 }, { text: "and walked.", at: 18 }]} size={84} y={210} end={78} />
        </S>
        {/* p6 family 37.6-43.1 s: nothing */}
        {/* 8 close: "too late" 44.3 s, struck on "hear Him instead" 45.4 s */}
        <S from={1330} to={1531}><TooLateClose /></S>
        {/* 9 ENDING: "Be not afraid," 48.2 s / "only believe." 49.88 s, holds to the end */}
        <S from={1446} to={TC_FRAMES}>
          <Pill lines={[{ text: "Be not afraid,", at: 0 }, { text: "only believe.", at: 50 }]} size={112} y={1150}
            end={9999} tab="Jesus" jesus chip="Mark 5:36" chipAt={66} lineFade={12} />
        </S>
      </AbsoluteFill>
      <EndFade />
    </AbsoluteFill>
  );
};
