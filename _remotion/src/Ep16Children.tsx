// Episode 16 "Let the Little Children" (Mark 10:13-16) - v2 high-production cut, Remotion text layer.
// Base: public/ep16/base.mp4 (75.7 s, voice + 17 pro clips). Video/audio untouched.
// Same pill system as Talitha Cumi / Ep12 (Kalam, see-through pills, Jesus tab, gold verse chips).
// Times = whisperx word times of the X5 voice (narration.alignment.json), 30 fps.
// The Jesus-line pill is the plain meaning ("Let the children come to Me.") because 4 blind seats
// misread KJV "Suffer" as pain (guardrail r2); the KJV words stay spoken.
import React from "react";
import { AbsoluteFill, OffthreadVideo, Sequence, staticFile } from "remotion";
import { Pill, useFonts } from "./TalithaCumi";

export const EP16_FPS = 30;
export const EP16_FRAMES = 2271; // 75.7 s

const S: React.FC<{ from: number; to: number; children: React.ReactNode }> = ({ from, to, children }) => (
  <Sequence from={from} durationInFrames={to - from} layout="none">{children}</Sequence>
);

export const Ep16Children: React.FC = () => {
  useFonts();
  return (
    <AbsoluteFill style={{ background: "#000" }}>
      <OffthreadVideo src={staticFile("ep16/base.mp4")} />
      <AbsoluteFill>
        {/* HOOK 0-5.4 s, on screen from frame 0; 2nd line on "Told" (2.76 s) */}
        <S from={0} to={162}>
          <Pill settle lines={[{ text: "Pushed away?", at: 0 }, { text: "Told “not now”?", at: 83 }]}
            size={84} y={140} end={162} />
        </S>
        {/* "Angry." 26.47 s, low band on the tunic (Jesus close-up) */}
        <S from={794} to={866}>
          <Pill lines={[{ text: "Angry.", at: 0 }]} size={120} y={1460} end={72} />
        </S>
        {/* JESUS 32.64-38.4 s: plain meaning of "Suffer the little children", top band above His head */}
        <S from={979} to={1155}>
          <Pill lines={[{ text: "Let the children", at: 0 }, { text: "come to Me.", at: 0 }]}
            size={84} y={110} end={176} tab="Jesus" jesus chip="Mark 10:14" chipAt={6} />
        </S>
        {/* "He took them up in his arms" 56.46 s */}
        <S from={1694} to={1784}>
          <Pill lines={[{ text: "He took them up", at: 0 }, { text: "in His arms.", at: 0 }]}
            size={78} y={1500} end={90} chip="Mark 10:16" chipAt={6} />
        </S>
        {/* LANDING 71.24 s to the end, low band on the robe (girl's head is up top) */}
        <S from={2137} to={EP16_FRAMES}>
          <Pill lines={[{ text: "Look at who", at: 0 }, { text: "Jesus picked up.", at: 10 }]}
            size={96} y={1560} end={9999} lineFade={12} />
        </S>
      </AbsoluteFill>
    </AbsoluteFill>
  );
};
