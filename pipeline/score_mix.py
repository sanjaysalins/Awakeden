"""ONE shared score-mix tail for every scorer in the repo (INV-26 hardening).

Before 2026-07-19 there were THREE independent copies of the final
narration+music mix filter graph (`run_piece.py::score_cmd` for shorts,
`longform/_add_score_lf.py` for long-form, and Bronze Serpent's path-only fork
`longform/04_The_Bronze_Serpent/_add_score_inked.py`) — and they grew two
DIFFERENT audio-padding bugs in two different places (shorts: no `apad` at all;
long-form: relative `apad=pad_dur` preserving a pre-existing short-audio gap).
Both surfaced as real desyncs in shipped files. This module is the single
source of truth for the fragment where those bugs lived; the three scorers
keep their own music-preparation chains (2-track crossfade vs N-segment
chain + de-tail + atempo — genuinely different designs) and delegate the tail.

The contract of `mix_tail`:
- narration audio is padded to the ABSOLUTE target (`apad=whole_dur`), never
  by a relative amount (`pad_dur`) — a source whose audio is already shorter
  than its video gets corrected, not preserved (INV-26).
- the caller's music chain must have produced a `[mus]` label already.
- video holds its last frame for the outro (`tpad=stop_mode=clone`).
- music ducks under the narration (sidechain), one limiter, 44.1k out.
"""
from __future__ import annotations

from pathlib import Path

AFMT = "aformat=sample_fmts=fltp:channel_layouts=stereo:sample_rates=44100"
SIDECHAIN = "threshold=0.12:ratio=2.5:attack=20:release=250"


def mix_tail(total: float, outro: float | str, *, fmt_narration: bool = False,
             sidechain: str = SIDECHAIN) -> str:
    """The shared narration-pad + duck + mix + video-hold filter fragment.
    Append after the caller's music chain (which must end in `[mus]`).
    `total` = narration + outro (the absolute final duration); `outro` = the
    last-frame hold. `fmt_narration` inserts the aformat normalizer before the
    narration pad (the long-form scorers always did; shorts never needed to).
    `sidechain` overrides the default duck tuning -- added 2026-08-23 for
    swirls_assemble.py, whose rhythmic/sparse scores need a much looser duck
    than this module's ambient-pad-tuned default (see SCORE_STYLE_BANK.md);
    every existing caller keeps the default and is unaffected."""
    fmt = (AFMT + ",") if fmt_narration else ""
    return (
        f"[0:a]{fmt}apad=whole_dur={total},asplit=2[main][key];"
        f"[mus][key]sidechaincompress={sidechain}[musd];"
        f"[main][musd]amix=inputs=2:normalize=0,alimiter=limit=0.97,aresample=44100[mix];"
        f"[0:v]tpad=stop_mode=clone:stop_duration={outro}[vout]"
    )


def output_args(out: Path | str, *, preset: str, total: float | None = None) -> list[str]:
    """The shared output arg block (maps + codecs). `total` bounds the output
    duration when given (the long-form scorers always pass it; shorts' graph is
    self-bounding so they don't)."""
    args = ["-map", "[vout]", "-map", "[mix]",
            "-c:v", "libx264", "-crf", "18", "-preset", preset, "-pix_fmt", "yuv420p",
            "-movflags", "+faststart", "-c:a", "aac", "-b:a", "192k"]
    if total is not None:
        args += ["-t", f"{total:.3f}"]
    return args + [str(out)]
