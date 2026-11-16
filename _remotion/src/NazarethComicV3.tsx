// NazarethComicV3 - v3 of the Nazareth comic film (new 59.18 s audio, fewer repeats). Data: prophecy/02_nazareth/build/nazareth_episode_v3.json
import React from "react";
import { ComicFilm } from "./comic_kit/ComicFilm";
import type { Episode } from "./comic_kit/core";
// @ts-ignore - JSON outside src
import nazarethEpisodeV3 from "../../prophecy/02_nazareth/build/nazareth_episode_v3.json";

export const NAZARETH3_FPS = 30;
export const NAZARETH3_FRAMES = 1776;
export const nazareth3Defaults = { episode: nazarethEpisodeV3 as unknown as Episode, marks: false };
export const NazarethComicV3: React.FC<{ episode: Episode; marks?: boolean; hideKinds?: string[] }> = ({ episode, marks, hideKinds }) => <ComicFilm episode={episode} marks={marks} hideKinds={hideKinds} />;
