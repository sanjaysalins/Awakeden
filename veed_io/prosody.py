"""Acoustic emphasis from the narration audio — offline, no API.

Measures how *stressed* each spoken word is, so the caption renderer can move
the enlarged key word to wherever the voice actually lands the emphasis (rather
than a text heuristic that always picks a mid-phrase content word).

Per word we read the audio inside its [start, end] window and measure:
    * RMS loudness   — louder = stressed
    * peak loudness  — a hard hit on a single syllable
(duration is already on the Word, the renderer folds it in.)

These are RAW magnitudes; the renderer turns them into a *relative* z-score
inside each phrase, because emphasis is local contrast (a loud word among quiet
neighbours), not absolute volume.

Pure stdlib ``wave`` + numpy — no scipy, no librosa, no extra install.
"""

from __future__ import annotations

import wave
from pathlib import Path

import numpy as np


def _read_wav_mono(wav_path: str | Path) -> tuple[np.ndarray, int]:
    """Read a PCM wav as a float32 mono signal in [-1, 1] and its sample rate."""
    with wave.open(str(wav_path), "rb") as wf:
        n_ch = wf.getnchannels()
        sampwidth = wf.getsampwidth()
        sr = wf.getframerate()
        raw = wf.readframes(wf.getnframes())

    if sampwidth == 2:
        data = np.frombuffer(raw, dtype=np.int16).astype(np.float32) / 32768.0
    elif sampwidth == 4:
        data = np.frombuffer(raw, dtype=np.int32).astype(np.float32) / 2147483648.0
    elif sampwidth == 1:                          # 8-bit PCM is unsigned
        data = (np.frombuffer(raw, dtype=np.uint8).astype(np.float32) - 128) / 128.0
    else:                                         # pragma: no cover
        raise ValueError(f"unsupported sample width: {sampwidth} bytes")

    if n_ch > 1:
        data = data.reshape(-1, n_ch).mean(axis=1)
    return data, sr


def word_loudness(
    wav_path: str | Path,
    words: list[dict],
) -> list[dict]:
    """Stamp ``rms`` and ``peak`` (raw loudness) onto each word dict, in place.

    ``words`` items need ``start``/``end`` (seconds). Returns the same list.
    A word whose window is empty/out-of-range gets the signal-wide mean so it
    never reads as artificially silent.
    """
    if not words:
        return words

    signal, sr = _read_wav_mono(wav_path)
    n = signal.shape[0]
    if n == 0:
        for wd in words:
            wd["rms"] = 0.0
            wd["peak"] = 0.0
        return words

    sq = signal * signal
    global_rms = float(np.sqrt(sq.mean())) or 1e-6

    for wd in words:
        a = int(max(0.0, float(wd["start"])) * sr)
        b = int(max(0.0, float(wd["end"])) * sr)
        b = min(max(b, a + 1), n)                 # at least 1 sample, in range
        a = min(a, n - 1)
        seg = sq[a:b]
        if seg.size == 0:
            wd["rms"] = global_rms
            wd["peak"] = global_rms
        else:
            wd["rms"] = float(np.sqrt(seg.mean()))
            wd["peak"] = float(np.sqrt(seg.max()))
    return words
