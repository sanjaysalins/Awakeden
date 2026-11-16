// NazarethComicV5 - v4 + two panel fixes (pgI bottom = S10, pgJ crop = angry faces, pgC Q = S11). Data: prophecy/02_nazareth/build/nazareth_episode_v5.json
import React from "react";
import { ComicFilm } from "./comic_kit/ComicFilm";
import type { Episode } from "./comic_kit/core";
// @ts-ignore - JSON outside src
import nazarethEpisodeV5 from "../../prophecy/02_nazareth/build/nazareth_episode_v5.json";

export const NAZARETH5_FPS = 30;
export const NAZARETH5_FRAMES = 1773;
export const nazareth5Defaults = { episode: nazarethEpisodeV5 as unknown as Episode, marks: false };
export const NazarethComicV5: React.FC<{ episode: Episode; marks?: boolean; hideKinds?: string[] }> = ({ episode, marks, hideKinds }) => <ComicFilm episode={episode} marks={marks} hideKinds={hideKinds} />;
