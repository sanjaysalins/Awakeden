// Episode 12 "Ye Are Not All Clean" (John 13) - v3 retro cut, Remotion text layer.
// Base: public/ep12/base.mp4 (79.7 s, voice + clips + owner's score). Video/audio untouched.
// Same pill system as Talitha Cumi (Kalam, see-through pills, Jesus tab, gold verse chips).
// Times = whisper word times of the v2 voice, +0.5 s after the Jesus line (build_v3.py).
import React from "react";
import { AbsoluteFill, OffthreadVideo, Sequence, staticFile, useCurrentFrame, interpolate } from "remotion";
import { C, Pill, useFonts } from "./TalithaCumi";

export const EP12_FPS = 30;
export const EP12_FRAMES = 2440; // 81.33 s (voice v2b)

const clamp = { extrapolateLeft: "clamp", extrapolateRight: "clamp" } as const;

const S: React.FC<{ from: number; to: number; children: React.ReactNode }> = ({ from, to, children }) => (
  <Sequence from={from} durationInFrames={to - from} layout="none">{children}</Sequence>
);

// Small name label over a face (helps a newcomer know who Judas and Peter are).
const NameTag: React.FC<{ text: string; x: number; y: number; end: number }> = ({ text, x, y, end }) => {
  const f = useCurrentFrame();
  const o = interpolate(f, [0, 8], [0, 1], clamp) * interpolate(f, [end - 8, end], [1, 0], clamp);
  const r = interpolate(f, [0, 8], [10, 0], clamp);
  return (
    <div style={{
      position: "absolute", left: x, top: y, transform: `translate(-50%, ${r}px)`, opacity: o,
      background: "rgba(14,67,77,0.72)", border: "3px solid rgba(246,233,202,0.9)", borderRadius: 999,
      padding: "4px 26px", fontFamily: "Kalam", fontWeight: 700, fontSize: 52, color: C.cream,
      textShadow: "0 3px 0 rgba(16,20,24,.55)", whiteSpace: "nowrap",
    }}>{text}</div>
  );
};

export const Ep12Towel: React.FC = () => {
  useFonts();
  return (
    <AbsoluteFill style={{ background: "#000" }}>
      <OffthreadVideo src={staticFile("ep12/base.mp4")} />
      <AbsoluteFill>
        {/* HOOK 0-5.6 s: on screen from frame 0 */}
        <S from={0} to={183}>
          <Pill settle lines={[{ text: "If people really knew me,", at: 0 }, { text: "would they leave?", at: 0 }]}
            size={74} y={150} end={183} />
        </S>
        {/* Names (picture 3): "Judas" ~12.2 s, "Peter" ~15.3 s */}
        <S from={399} to={648}><NameTag text="Judas" x={300} y={410} end={249} /></S>
        <S from={489} to={648}><NameTag text="Peter" x={790} y={300} end={159} /></S>
        {/* The question 19.7-21.6 s (picture 4, low band) */}
        <S from={660} to={746}>
          <Pill lines={[{ text: "So what does He do", at: 0 }, { text: "with friends like that?", at: 0 }]}
            size={80} y={1250} end={86} />
        </S>
        {/* Jesus 36.6-38.4 s (picture 6) */}
        <S from={1176} to={1230}>
          <Pill lines={[{ text: "“Know ye what I have", at: 0 }, { text: "done to you?”", at: 0 }]}
            size={72} y={1400} end={54} tab="Jesus" jesus chip="John 13:12" chipAt={4} />
        </S>
        {/* 41.6-46.5 s (picture 7, top band: low band covered the towel) */}
        <S from={1323} to={1473}>
          <Pill lines={[{ text: "“He loved them", at: 0 }, { text: "unto the end.”", at: 0 }]}
            size={88} y={150} end={150} chip="John 13:1" chipAt={6} />
        </S>
        {/* "and it was night" 54.3 s (picture 8, Judas gone) */}
        <S from={1743} to={1797}>
          <Pill lines={[{ text: "“and it was night.”", at: 0 }]} size={96} y={1180} end={54}
            fill="rgba(21,37,60,0.80)" chip="John 13:30" chipAt={4} />
        </S>
        {/* "Jesus knows. All of it." 63.4 s (picture 10, low band on the tunic) */}
        <S from={2007} to={2100}>
          <Pill lines={[{ text: "Jesus knows.", at: 0 }, { text: "All of it.", at: 44 }]} size={84} y={1400} end={93} />
        </S>
        {/* LANDING (picture 11, top band above His head) */}
        <S from={2166} to={2283}>
          <Pill lines={[{ text: "The one who knew the worst", at: 0 }, { text: "was not the one who left.", at: 0 }]}
            size={68} y={130} end={117} />
        </S>
        <S from={2286} to={EP12_FRAMES}>
          <Pill lines={[{ text: "He was the one", at: 0 }, { text: "holding the towel.", at: 14 }]}
            size={100} y={130} end={9999} lineFade={12} />
        </S>
      </AbsoluteFill>
    </AbsoluteFill>
  );
};
