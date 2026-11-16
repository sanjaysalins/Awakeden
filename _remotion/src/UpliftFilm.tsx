// UpliftFilm - the comic uplift layer: a pre-joined silent base video (the livingpage beats, back to back)
// + page turns between beats + hand-drawn marks on top. Data driven; no film-specific code.
// Spec: _quality_uplift_20261116/design_comic/COMIC_UPLIFT_SPEC.md (T5).
//   npx remotion render src/index.ts UpliftFilm out.mp4 --props=<film.json> --muted --crf=12
//   marks-only render for the gates: add  "marksOnly": true  to the props file.
// Page turns never move a beat edge: the OLD beat's last frame is held for <= 10 frames over the NEW beat's first frames.
import React from "react";
import { AbsoluteFill, Freeze, OffthreadVideo, Sequence, staticFile, useCurrentFrame } from "remotion";
import { Doodle, FH, FW, INK, clamp, glide, prog } from "./comic_kit/core";
import { halftoneMask, svgMask } from "./comic_kit/transitions";
import { HandMark } from "./comic_kit/hand";

export interface UpliftTurn { kind: "page_flip_up" | "halftone_dissolve"; at: number; frames: number; mode?: string }
export interface UpliftFilmSpec {
  src: string;            // path under public/
  frames: number;
  turns: UpliftTurn[];
  marks: Doodle[];
}
export interface UpliftProps { film: UpliftFilmSpec; marksOnly?: boolean }

const Base: React.FC<{ src: string; style?: React.CSSProperties }> = ({ src, style }) => (
  <div style={{ position: "absolute", left: 0, top: 0, width: FW, height: FH, ...style }}>
    <OffthreadVideo src={staticFile(src)} muted style={{ width: FW, height: FH }} />
  </div>
);

/** the old beat's last frame (source frame at-1), frozen. */
const OldFrame: React.FC<{ src: string; at: number; frames: number; style?: React.CSSProperties }> = ({ src, at, frames, style }) => (
  <Sequence from={at} durationInFrames={frames} layout="none">
    <div style={{ position: "absolute", left: 0, top: 0, width: FW, height: FH, ...style }}>
      <Freeze frame={0}>
        <OffthreadVideo src={staticFile(src)} muted startFrom={at - 1} style={{ width: FW, height: FH }} />
      </Freeze>
    </div>
  </Sequence>
);

export const UpliftFilm: React.FC<UpliftProps> = ({ film, marksOnly = false }) => {
  const f = useCurrentFrame();
  const turn = film.turns.find((t) => f >= t.at && f < t.at + t.frames);
  let layers: React.ReactNode;
  if (!turn) {
    layers = <Base src={film.src} />;
  } else {
    const p = prog(f, turn.at, turn.frames);
    if (turn.kind === "page_flip_up") {
      // old page hinged at the top: tips up and away, darkening, revealing the new beat beneath
      const e = glide(p), ang = 104 * e;
      layers = (
        <>
          <Base src={film.src} />
          <OldFrame
            src={film.src}
            at={turn.at}
            frames={turn.frames}
            style={{ transformOrigin: "50% 0%", transform: `perspective(2200px) rotateX(${ang}deg)`, filter: `brightness(${1 - 0.65 * e})` }}
          />
        </>
      );
    } else {
      // halftone dissolve (rise): the new beat climbs in through ink dots over the old frame
      layers = (
        <>
          <OldFrame src={film.src} at={turn.at} frames={turn.frames} />
          <Base src={film.src} style={p >= 1 ? {} : svgMask(halftoneMask(turn.mode || "rise", p, [FW / 2, FH / 2]))} />
        </>
      );
    }
  }
  const live = film.marks.filter((d) => f >= d.at && (d.until == null || f < d.until + 1));
  return (
    <AbsoluteFill style={{ background: marksOnly ? "#000" : INK }}>
      {!marksOnly && layers}
      <div style={marksOnly ? { position: "absolute", left: 0, top: 0, width: FW, height: FH, filter: "brightness(0) invert(1)" } : undefined}>
        <svg width={FW} height={FH} style={{ position: "absolute", left: 0, top: 0, overflow: "visible" }}>
          {live.map((d, i) => <HandMark key={`${d.kind}${i}`} d={d} f={f} />)}
        </svg>
      </div>
    </AbsoluteFill>
  );
};
void clamp;
