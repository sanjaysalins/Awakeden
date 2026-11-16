// Prophecy 01 "Born in Bethlehem" - film v2 on the v2 words (words/FINAL_WORDS_v2.md, audio_v2/narration_v2.mp3).
// Same PixVerse clips, hard cuts at 1.0x (trim only); lettering reused from the animatic. Data: public/bethlehem/film_v2_data.json.
import React from "react";
import { AbsoluteFill, Audio, OffthreadVideo, Sequence, continueRender, delayRender, staticFile, useCurrentFrame } from "remotion";
// @ts-ignore
import D from "../public/bethlehem/film_v2_data.json";
import { Pill, ScrollCard, Slab } from "./BethlehemAnimatic";

export const BTH2_FPS = 30;
export const BTH2_FRAMES = D.frames as number;
const F = (s: number) => Math.round(s * 30);

export const BethlehemV2: React.FC<{ hud?: boolean }> = ({ hud = false }) => {
  const f = useCurrentFrame();
  const [h] = React.useState(() => delayRender("bv2fonts"));
  const [ready, setReady] = React.useState(false);
  React.useEffect(() => {
    Promise.all([
      new FontFace("KalamB", `url(${staticFile("Kalam-Bold.ttf")})`).load(),
      new FontFace("BangersB", `url(${staticFile("Bangers.ttf")})`).load(),
    ]).then((fs) => { fs.forEach((ff) => (document as any).fonts.add(ff)); setReady(true); continueRender(h); }).catch(() => continueRender(h));
  }, []);
  const items = D.items as any[];
  return (
    <AbsoluteFill style={{ background: "#000", overflow: "hidden" }}>
      <Audio src={staticFile("bethlehem/narration_v2.mp3")} />
      {(D.edl as [string, number, number, number][]).map(([c, a, b, inPt], i) => (
        <Sequence key={i} from={F(a)} durationInFrames={F(b) - F(a)}>
          <OffthreadVideo src={staticFile(`bethlehem/clips/${c}.mp4`)} startFrom={F(inPt)} muted style={{ width: 1080, height: 1920, objectFit: "cover" }} />
        </Sequence>
      ))}
      {ready && (
        <>
          {items.filter((it) => it.kind === "slab").map((it) => <Slab key={it.id} it={it} f={f} />)}
          {items.filter((it) => it.kind === "pill" || it.kind === "speech").map((it) => <Pill key={it.id} it={it} f={f} cy={1440} sacred={!!it.sacred} />)}
          <ScrollCard strips={items.filter((it) => it.kind === "scroll")} openAt={15.5} closeAt={17.8} f={f} />
        </>
      )}
      {hud && <div style={{ position: "absolute", left: 18, top: 1862, padding: "4px 14px", background: "rgba(0,0,0,0.7)", color: "#fff", fontFamily: "KalamB", fontSize: 26, borderRadius: 10 }}>{(f / 30).toFixed(2)} s · f{f}</div>}
    </AbsoluteFill>
  );
};
