// NazarethComicV6 - words v7 + new voice (59.85 s). Data: prophecy/02_nazareth/build/nazareth_episode_v6.json
import React from "react";
import { ComicFilm } from "./comic_kit/ComicFilm";
import type { Episode } from "./comic_kit/core";
// @ts-ignore - JSON outside src
import nazarethEpisodeV6 from "../../prophecy/02_nazareth/build/nazareth_episode_v6.json";

export const NAZARETH6_FPS = 30;
export const NAZARETH6_FRAMES = 1796;
export const nazareth6Defaults = { episode: nazarethEpisodeV6 as unknown as Episode, marks: false };
export const NazarethComicV6: React.FC<{ episode: Episode; marks?: boolean; hideKinds?: string[] }> = ({ episode, marks, hideKinds }) => <ComicFilm episode={episode} marks={marks} hideKinds={hideKinds} />;
