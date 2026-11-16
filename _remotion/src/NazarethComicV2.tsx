// NazarethComicV2 - v2 of the Nazareth comic film (new 59.18 s audio, fewer repeats). Data: prophecy/02_nazareth/build/nazareth_episode_v2.json
import React from "react";
import { ComicFilm } from "./comic_kit/ComicFilm";
import type { Episode } from "./comic_kit/core";
// @ts-ignore - JSON outside src
import nazarethEpisodeV2 from "../../prophecy/02_nazareth/build/nazareth_episode_v2.json";

export const NAZARETH2_FPS = 30;
export const NAZARETH2_FRAMES = 1776;
export const nazareth2Defaults = { episode: nazarethEpisodeV2 as unknown as Episode, marks: false };
export const NazarethComicV2: React.FC<{ episode: Episode; marks?: boolean; hideKinds?: string[] }> = ({ episode, marks, hideKinds }) => <ComicFilm episode={episode} marks={marks} hideKinds={hideKinds} />;
