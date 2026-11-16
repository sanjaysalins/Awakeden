// ThiefComic - "Jesus Promised Paradise to a Criminal" (38 s) as a full graphic-comic motion film. TEST COPY of the shipped short.
// Data: poc_comic_page/_ELEVATE/formula/build/thief_episode.json (written by build_thief.py). Render:
//   npx remotion render src/index.ts ThiefComic out.mp4 --muted --concurrency=2   (add --props=<other episode.json> for a new episode)
import React from "react";
import { ComicFilm } from "./comic_kit/ComicFilm";
import type { Episode } from "./comic_kit/core";
// @ts-ignore - JSON outside src
import thiefEpisode from "../../poc_comic_page/_ELEVATE/formula/build/thief_episode.json";

export const THIEF_FPS = 30;
export const THIEF_FRAMES = 1140;
export const thiefDefaults = { episode: thiefEpisode as unknown as Episode, marks: false };
export const ThiefComic: React.FC<{ episode: Episode; marks?: boolean; hideKinds?: string[] }> = ({ episode, marks, hideKinds }) => <ComicFilm episode={episode} marks={marks} hideKinds={hideKinds} />;
