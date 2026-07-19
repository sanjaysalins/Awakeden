"""ONE shared ambient/SFX cue-bed engine for the long-form episodes.

Before 2026-07-20 there were SEVEN per-episode copies of the same ~55-line
ffmpeg engine (render each cue -> sum a bed -> mix it UNDER the scored film),
differing only in paths / TOTAL / the cue sheet — the same fork pattern that
let the score-mix pad bugs live in shipped files (see pipeline/score_mix.py).
Each episode keeps its own CUES list (the actual sound design, genuinely
per-piece); this module owns the engine.

Cue tuple: (slug, start_s, end_s, gain_db) — slug resolves to
sound_library/clips/<slug>.mp3. Ambient/accents only: NO choir, NO score_*
clips (feedback-no-choir-pad-under-score). The bed is summed with
amix normalize=0 so narration+score stay full and the SFX only adds, low.
Layer stack (feedback-audio-layer-stack): narration (base) -> orchestral
SCORE -> SFX (quietest, this).

The shorts keep their own engine (sfx_pilots/sfxlib.py) — measured-gain
sidechain-ducked layers, a genuinely different design, not a fork of this.
"""
from __future__ import annotations

import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_LIB = ROOT / "sound_library" / "clips"


def cue_af(gain: float, dur: float, start: float) -> str:
    """The per-cue filter chain: gain, 1.0s fade-in, 1.5s fade-out pinned to
    the cue's end (floored at 0 for very short cues), then delay to `start`."""
    delay = int(start * 1000)
    return (f"volume={gain}dB,afade=t=in:d=1.0,"
            f"afade=t=out:st={max(0, dur - 1.5):.2f}:d=1.5,"
            f"adelay={delay}|{delay}")


def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        raise SystemExit(f"ffmpeg failed:\n{' '.join(str(c) for c in cmd[:8])}...\n{r.stderr[-1000:]}")


def build(scored, out, cues, total: float, *, lib=None, work=None) -> Path:
    """Render each cue, sum them into one bed, mix the bed UNDER the scored
    film's audio (video stream copied untouched). Returns `out`."""
    scored = Path(scored)
    out = Path(out)
    lib = Path(lib) if lib else DEFAULT_LIB
    work = Path(work) if work else scored.parent / "_sfx_work"
    if not scored.exists():
        raise SystemExit(f"missing scored film: {scored}")
    work.mkdir(exist_ok=True)

    cue_files = []
    for i, (slug, start, end, gain) in enumerate(cues):
        src = lib / f"{slug}.mp3"
        if not src.exists():
            raise SystemExit(f"missing sound: {src}")
        d = end - start
        cue_out = work / f"cue_{i:02d}.wav"
        run(["ffmpeg", "-y", "-stream_loop", "-1", "-i", str(src), "-t", f"{d:.3f}",
             "-af", cue_af(gain, d, start), "-ar", "44100", "-ac", "2", str(cue_out)])
        cue_files.append(cue_out)
        print(f"  cue {i:02d} {slug:22s} [{start:6.1f}-{end:6.1f}] {gain}dB")

    bed = work / "sfx_bed.wav"
    inputs = []
    for f in cue_files:
        inputs += ["-i", str(f)]
    amix = f"amix=inputs={len(cue_files)}:normalize=0:duration=longest[b]"
    run(["ffmpeg", "-y", *inputs, "-filter_complex", amix, "-map", "[b]",
         "-t", f"{total:.3f}", "-ar", "44100", "-ac", "2", str(bed)])
    print(f"[bed] {len(cue_files)} cues -> {bed.name}")

    run(["ffmpeg", "-y", "-i", str(scored), "-i", str(bed),
         "-filter_complex", "[0:a][1:a]amix=inputs=2:normalize=0:duration=first[a]",
         "-map", "0:v", "-map", "[a]", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k",
         str(out)])
    print(f"[done] {out}")
    return out
