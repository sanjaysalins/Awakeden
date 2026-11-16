// NazarethComic - "He stopped mid-sentence" (Isaiah 61 -> Luke 4), comic-pages film, same kit as ThiefComic.
// Data: prophecy/02_nazareth/build/nazareth_episode.json (written by build_nazareth.py).
import React from "react";
import { ComicFilm } from "./comic_kit/ComicFilm";
import type { Episode } from "./comic_kit/core";
// @ts-ignore - JSON outside src
import nazarethEpisode from "../../prophecy/02_nazareth/build/nazareth_episode.json";

export const NAZARETH_FPS = 30;
export const NAZARETH_FRAMES = 1639;
export const nazarethDefaults = { episode: nazarethEpisode as unknown as Episode, marks: false };
export const NazarethComic: React.FC<{ episode: Episode; marks?: boolean; hideKinds?: string[] }> = ({ episode, marks, hideKinds }) => <ComicFilm episode={episode} marks={marks} hideKinds={hideKinds} />;
