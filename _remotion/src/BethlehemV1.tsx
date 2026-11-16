// Prophecy 01 "Born in Bethlehem" - film v1. Real PixVerse V6 clips (prophecy/01_bethlehem/clips/) as full-frame base,
// hard cuts at 1.0x (trim only), lettering on top reused from the animatic (same words/times: public/bethlehem/animatic_data.json).
// 1080x1920 @30, 1548 frames (48.5 s narration + 3.1 s landing hold).
import React from "react";
import { AbsoluteFill, Audio, OffthreadVideo, Sequence, continueRender, delayRender, staticFile, useCurrentFrame } from "remotion";
// @ts-ignore
import D from "../public/bethlehem/animatic_data.json";
import { GoldWord, Pill, ScrollCard, Slab } from "./BethlehemAnimatic";

export const BV1_FPS = 30;
export const BV1_FRAMES = 1548;
const F = (s: number) => Math.round(s * 30);

// [clip, film start s, film end s, clip in-point s]. Every slot is shorter than what its clip has left after the in-point.
export const EDL: [string, number, number, number][] = [
  ["P1", 0.0, 7.15, 0.0],    // experts -> finger -> empty road ("never went to look")
  ["P2", 7.15, 12.25, 0.0],  // Micah page alive (page holds 0-5.1 s)
  ["M1", 12.25, 17.25, 0.0], // Micah points at the town: "named one small town" / "But thou, Bethlehem"
  ["P2", 17.25, 21.94, 5.3], // the dive: Micah at the lamp, his face, while his words scroll
  ["P3", 21.94, 26.98, 0.0], // manger -> camels ("newborn King")
  ["P4", 26.98, 35.3, 0.0],  // Herod points, scribe answers, Herod's cold face ("They knew the town.")
  ["M2", 35.3, 39.3, 0.0],   // "And Jesus was already there." (calm)
  ["P5", 39.3, 47.5, 0.0],   // everlasting stars -> crosses ("died for our sins") -> open tomb ("rose")
  ["M3", 47.5, 51.6, 0.0],   // risen; landing hold
];
const PILL_CY = 1440;

export const BethlehemV1: React.FC<{ hud?: boolean }> = ({ hud = false }) => {
  const f = useCurrentFrame();
  const [h] = React.useState(() => delayRender("bv1fonts"));
  const [ready, setReady] = React.useState(false);
  React.useEffect(() => {
    Promise.all([
      new FontFace("KalamB", `url(${staticFile("Kalam-Bold.ttf")})`).load(),
      new FontFace("BangersB", `url(${staticFile("Bangers.ttf")})`).load(),
    ]).then((fs) => { fs.forEach((ff) => (document as any).fonts.add(ff)); setReady(true); continueRender(h); }).catch(() => continueRender(h));
  }, []);
  const items = D.items as any[];
  const pills = items.filter((it) => it.kind === "pill" || it.kind === "speech");
  const sacredPage = (pg: number) => !!(D.pages as any[]).find((p) => p.n === pg)?.sacred;
  return (
    <AbsoluteFill style={{ background: "#000", overflow: "hidden" }}>
      <Audio src={staticFile("bethlehem/narration.mp3")} />
      {EDL.map(([c, a, b, inPt], i) => (
        <Sequence key={i} from={F(a)} durationInFrames={F(b) - F(a)}>
          <OffthreadVideo src={staticFile(`bethlehem/clips/${c}.mp4`)} startFrom={F(inPt)} muted
            style={{ width: 1080, height: 1920, objectFit: "cover" }} />
        </Sequence>
      ))}
      {ready && (
        <>
          {items.filter((it) => it.kind === "slab").map((it) => <Slab key={it.id} it={it} f={f} />)}
          {pills.map((it) => <Pill key={it.id} it={it} f={f} cy={PILL_CY} sacred={sacredPage(it.page)} />)}
          <ScrollCard strips={items.filter((it) => it.id.startsWith("c3"))} openAt={14.40} closeAt={21.74} f={f} />
          <ScrollCard strips={items.filter((it) => it.id === "c8")} openAt={39.30} closeAt={41.54} f={f} />
          <GoldWord f={f} />
        </>
      )}
      {hud && (
        <div style={{ position: "absolute", left: 18, top: 1862, padding: "4px 14px", background: "rgba(0,0,0,0.7)", color: "#fff", fontFamily: "KalamB", fontSize: 26, borderRadius: 10 }}>
          {(f / 30).toFixed(2)} s · f{f}
        </div>
      )}
    </AbsoluteFill>
  );
};
