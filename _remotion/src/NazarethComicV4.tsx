// NazarethComicV4 - v4 of the Nazareth comic film (words v6, new voice, 59.08 s). Data: prophecy/02_nazareth/build/nazareth_episode_v4.json
import React from "react";
import { ComicFilm } from "./comic_kit/ComicFilm";
import type { Episode } from "./comic_kit/core";
// @ts-ignore - JSON outside src
import nazarethEpisodeV4 from "../../prophecy/02_nazareth/build/nazareth_episode_v4.json";

export const NAZARETH4_FPS = 30;
export const NAZARETH4_FRAMES = 1773;
export const nazareth4Defaults = { episode: nazarethEpisodeV4 as unknown as Episode, marks: false };
export const NazarethComicV4: React.FC<{ episode: Episode; marks?: boolean; hideKinds?: string[] }> = ({ episode, marks, hideKinds }) => <ComicFilm episode={episode} marks={marks} hideKinds={hideKinds} />;
