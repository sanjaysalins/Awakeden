"""swirls_assemble.py -- shared assembly module for Swirls of Life episodes.

Replaces the per-episode assemble_book_v2.py / assemble_ashes.py fork
(function-for-function near-identical, 2 real ffmpeg bugs independently
discovered and fixed in both copies -- see the BUG FIX comments below) with
one parameterized module: fix a bug once, every episode gets it. Delegates
the final narration+score mix tail to pipeline.score_mix.mix_tail() (INV-26)
instead of a 3rd/4th hand-rolled copy of that filter fragment, while keeping
each episode's own empirically-required duck tuning in its own manifest (a
duck does not transfer between score generations -- see
SCORE_STYLE_BANK.md).
"""
from __future__ import annotations

import subprocess
from dataclasses import dataclass, field
from pathlib import Path
from typing import Literal

import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from pipeline import score_mix  # noqa: E402


@dataclass
class Unit:
    tag: str
    src: Path
    words: int
    mode: Literal["freeze", "boomerang"]
    tail_loop_seconds: float | None = None
    # freeze units only: when set, the slot-filling extension ping-pongs the clip's
    # own last `tail_loop_seconds` (see make_freeze_tail_loop) instead of a static
    # frame clone -- a $0 alternative to a longer native render for cutting a
    # freeze page's static ratio. None (default) = plain make_freeze, unchanged.


@dataclass
class DuckProfile:
    gain_db: float
    threshold: float
    ratio: float
    release_ms: int

    def sidechain(self) -> str:
        return f"threshold={self.threshold}:ratio={self.ratio}:attack=20:release={self.release_ms}"


@dataclass
class ScoreVariant:
    score: Path
    duck: DuckProfile
    out: Path


@dataclass
class EpisodeManifest:
    episode_dir: Path
    narration: Path
    units: list[Unit]
    scores: dict[str, ScoreVariant]
    panel_style: Literal["ink_wash", "woodcut_hybrid"]
    outro_hold: float = 3.0
    w: int = 720
    h: int = 1280
    fps: int = 30


def dur(p: Path) -> float:
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "default=nw=1:nk=1", str(p)],
        capture_output=True, text=True, check=True).stdout.strip()
    return float(out)


def run(cmd: list[str]) -> None:
    subprocess.run(cmd, check=True)


def encode(cmd_tail: list[str], out: Path, manifest: EpisodeManifest, prefilter: str = "") -> None:
    # BUG FIX (2026-08-22, independently rediscovered in BOTH assemble_book_v2.py
    # and assemble_ashes.py before being unified here): a caller-supplied
    # "-vf tpad=..." followed by this function's own "-vf scale=..." -- ffmpeg
    # silently honors only the LAST -vf flag, so the tpad extension was dropped
    # every time and freeze-mode clips never actually extended past their native
    # length (shipped unnoticed in Jacob's Ladder's original locked cut: F03
    # stayed at 5.03s instead of its intended 7.46s slot). Fix: chain any
    # prefilter into ONE -vf argument, permanently, in this one shared place.
    vf = f"{prefilter + ',' if prefilter else ''}scale={manifest.w}:{manifest.h}:flags=lanczos,setsar=1"
    run(["ffmpeg", "-y", "-v", "error"] + cmd_tail +
        ["-vf", vf, "-r", str(manifest.fps),
         "-c:v", "libx264", "-crf", "18", "-preset", "medium",
         "-pix_fmt", "yuv420p", "-an", str(out)])


def make_freeze(src: Path, out: Path, slot: float, cdur: float, work: Path, tag: str,
                 manifest: EpisodeManifest) -> None:
    extension = max(slot - cdur, 0)
    if extension <= 0:
        encode(["-i", str(src)], out, manifest)
        return
    # BUG FIX (2026-08-29, user: "several freeze frames across the clips, we must fix
    # that"): a plain tpad clone extends with a dead, motionless duplicated frame -- no
    # reversal artifact (unlike boomerang on continuous motion, see
    # project_swirls_boomerang_continuous_motion_unsafe), but reads as visibly frozen/
    # stiff on a long extension (several seconds on some units). Give the extension a
    # slow, continuous, subtle zoom instead -- consistent with this engine's own
    # "frozen tableau, only the camera moves" language (SKILL_locked.md) -- rather than
    # a flat static clone.
    #
    # This MUST be built as two separate passes, not one chained `tpad=...,zoompan=...`
    # filter: applying zoompan directly after tpad on the same stream silently drops
    # frames and shortens the output (confirmed by direct test -- with zoompan's own
    # `fps=` sub-param the output came in ~1.5s short of the requested duration; without
    # it, ~0.3-0.5s short; both leave the final mux's video track shorter than its audio
    # track, INV-26 territory). zoompan on a single looped still image (the classic
    # image-to-video idiom, `-loop 1 -i still.png ... d=<frames>`) is exact and reliable
    # by contrast -- so extract the clip's own last frame as a still, zoompan THAT for
    # exactly `extension` seconds, then concat it onto the untouched native clip (same
    # concat-filter pattern as make_boomerang/make_freeze_tail_loop). The native footage's
    # own motion is never touched, only the added hold gets the push.
    last_frame = work / f"{tag}__lastframe.png"
    run(["ffmpeg", "-y", "-v", "error", "-sseof", "-0.1", "-i", str(src),
         "-vsync", "0", "-frames:v", "1", str(last_frame)])
    ext_frames = max(int(round(extension * manifest.fps)), 1)
    zoompan = (f"zoompan=z='min(1+0.06*on/{ext_frames},1.06)':d={ext_frames}:"
               f"s={manifest.w}x{manifest.h}:fps={manifest.fps}")
    tail = work / f"{tag}__zoomtail.mp4"
    run(["ffmpeg", "-y", "-v", "error", "-loop", "1", "-i", str(last_frame), "-vf",
         f"{zoompan},scale={manifest.w}:{manifest.h}:flags=lanczos,setsar=1",
         "-t", f"{extension:.3f}", "-r", str(manifest.fps),
         "-c:v", "libx264", "-crf", "18", "-preset", "medium",
         "-pix_fmt", "yuv420p", str(tail)])
    parts = [src, tail]
    cmd = ["ffmpeg", "-y", "-v", "error"]
    for p in parts:
        cmd += ["-i", str(p)]
    scale_filters = [f"[{i}:v]scale={manifest.w}:{manifest.h}:flags=lanczos,setsar=1[s{i}]"
                      for i in range(len(parts))]
    scale_labels = [f"[s{i}]" for i in range(len(parts))]
    filt = ";".join(scale_filters) + ";" + "".join(scale_labels) + f"concat=n={len(parts)}:v=1:a=0[v]"
    cmd += ["-filter_complex", filt, "-map", "[v]", "-t", f"{slot:.3f}",
            "-r", str(manifest.fps), "-c:v", "libx264", "-crf", "18", "-preset", "medium",
            "-pix_fmt", "yuv420p", "-an", str(out)]
    run(cmd)


def make_freeze_tail_loop(src: Path, out: Path, slot: float, cdur: float, work: Path, tag: str,
                           manifest: EpisodeManifest, tail_seconds: float = 1.2) -> None:
    """User's own fix idea, 2026-08-23 ('do the boomerang play immediately at
    the end of a clip'), as a $0 alternative to paying for longer native
    renders to reduce a freeze page's static ratio: instead of statically
    cloning the last frame for the extension (plain make_freeze), ping-pong
    the clip's own TAIL (the last `tail_seconds` -- meant to already be a
    settled/holding moment per the page's own animation design, e.g. F04's
    'the motion completing early in the clip and then holding') back and
    forth to fill the remaining slot time. Gives continuous subtle motion
    (breath, fabric sway) instead of a dead frozen frame, WITHOUT ever
    visibly reversing the page's own completing gesture, which lives earlier
    in the clip and is never touched -- only re-verify this holds by eye
    per page before trusting it; a page whose gesture continues too close to
    its own last frame is not a safe candidate for this and should keep
    plain make_freeze or a longer native render instead."""
    extension = max(slot - cdur, 0)
    if extension <= 0:
        encode(["-i", str(src)], out, manifest)
        return
    tail_seconds = min(tail_seconds, cdur)
    tail_start = max(cdur - tail_seconds, 0)
    tail = work / f"{tag}__tail.mp4"
    run(["ffmpeg", "-y", "-v", "error", "-ss", f"{tail_start:.3f}", "-i", str(src),
         "-t", f"{tail_seconds:.3f}", "-vf",
         f"scale={manifest.w}:{manifest.h}:flags=lanczos,setsar=1",
         "-r", str(manifest.fps), "-c:v", "libx264", "-crf", "18", "-preset", "medium",
         "-pix_fmt", "yuv420p", str(tail)])
    tail_rev = work / f"{tag}__tail_rev.mp4"
    run(["ffmpeg", "-y", "-v", "error", "-i", str(tail), "-vf",
         f"reverse,scale={manifest.w}:{manifest.h}:flags=lanczos,setsar=1",
         "-r", str(manifest.fps), "-c:v", "libx264", "-crf", "18", "-preset", "medium",
         "-pix_fmt", "yuv420p", str(tail_rev)])
    reps = int(extension // tail_seconds) + 2
    # tail_rev first: continues seamlessly from native's own last frame (both at t=cdur),
    # then alternates back to tail (forward) which continues seamlessly from tail_rev's
    # own last frame (both at t=tail_start) -- no visible jump at any splice point.
    loop_parts = [tail_rev if i % 2 == 0 else tail for i in range(reps)]
    parts = [src] + loop_parts
    cmd = ["ffmpeg", "-y", "-v", "error"]
    for p in parts:
        cmd += ["-i", str(p)]
    scale_filters = [f"[{i}:v]scale={manifest.w}:{manifest.h}:flags=lanczos,setsar=1[s{i}]"
                      for i in range(len(parts))]
    scale_labels = [f"[s{i}]" for i in range(len(parts))]
    filt = ";".join(scale_filters) + ";" + "".join(scale_labels) + f"concat=n={len(parts)}:v=1:a=0[v]"
    cmd += ["-filter_complex", filt, "-map", "[v]", "-t", f"{slot:.3f}",
            "-r", str(manifest.fps), "-c:v", "libx264", "-crf", "18", "-preset", "medium",
            "-pix_fmt", "yuv420p", "-an", str(out)]
    run(cmd)


def make_boomerang(src: Path, out: Path, slot: float, cdur: float, work: Path, tag: str,
                    manifest: EpisodeManifest) -> None:
    if slot <= cdur:
        encode(["-i", str(src), "-t", f"{slot:.3f}"], out, manifest)
        return
    # BUG FIX (2026-08-22, same independent-rediscovery history as above): the
    # concat DEMUXER (-f concat, a text file list) combined with an output "-t"
    # trim silently truncates at whole-segment boundaries only, regardless of
    # where -t is placed. Switched to the concat FILTER (each segment its own
    # -i, joined via filter_complex) instead, which trims at the exact frame.
    rev = work / f"{tag}__rev.mp4"
    run(["ffmpeg", "-y", "-v", "error", "-i", str(src), "-vf",
         f"reverse,scale={manifest.w}:{manifest.h}:flags=lanczos,setsar=1",
         "-r", str(manifest.fps), "-c:v", "libx264", "-crf", "18", "-preset", "medium",
         "-pix_fmt", "yuv420p", str(rev)])
    reps = int(slot // cdur) + 2
    parts = [src if i % 2 == 0 else rev for i in range(reps)]
    cmd = ["ffmpeg", "-y", "-v", "error"]
    for p in parts:
        cmd += ["-i", str(p)]
    # BUG FIX (2026-08-23, found by actually RE-RUNNING this code for real during
    # validation, not just diffing it against the original -- neither
    # assemble_book_v2.py nor assemble_ashes.py ever had a per-source scale here,
    # only `rev` (scaled at generation time) and the CONCAT OUTPUT were ever scaled
    # to manifest.w x manifest.h. The raw `src` clip goes into concat at its own
    # native resolution -- fine when every clip in an episode happens to share one
    # resolution, but this project mixes kling3_0 (1076x1928) and veo3_1_lite
    # (720x1280) native output per-page, and ffmpeg's concat filter requires
    # matching input dimensions. Confirmed live on episode 1's real f02 unit
    # (kling-native 1076x1928 src concatenated with an already-720x1280 rev) --
    # exactly the silent-mismatch failure mode this project's own docstrings
    # claimed was already handled ("All held clips are explicitly scaled... before
    # concat") but the code never actually did. Fix: scale EVERY input individually
    # before concat, not just after.
    scale_labels = []
    scale_filters = []
    for i in range(len(parts)):
        scale_filters.append(f"[{i}:v]scale={manifest.w}:{manifest.h}:flags=lanczos,setsar=1[s{i}]")
        scale_labels.append(f"[s{i}]")
    filt = (";".join(scale_filters) + ";" +
            "".join(scale_labels) + f"concat=n={len(parts)}:v=1:a=0[v]")
    cmd += ["-filter_complex", filt, "-map", "[v]", "-t", f"{slot:.3f}",
            "-r", str(manifest.fps), "-c:v", "libx264", "-crf", "18", "-preset", "medium",
            "-pix_fmt", "yuv420p", "-an", str(out)]
    run(cmd)


def plan_units(manifest: EpisodeManifest) -> list[dict]:
    """$0 -- word-proportional slot + native duration per unit, no rendering.
    Used by `swirls_episode.py plan` and swirls_verify.py's freeze-hold gate."""
    narration_len = dur(manifest.narration)
    total_words = sum(u.words for u in manifest.units)
    stats = []
    for u in manifest.units:
        slot = narration_len * u.words / total_words
        native = dur(u.src) if u.src.exists() else None
        stats.append({"tag": u.tag, "mode": u.mode, "words": u.words, "slot": slot,
                       "native": native})
    return stats


def assemble(manifest: EpisodeManifest, score_name: str, *, work_dirname: str = "_assembly") -> dict:
    variant = manifest.scores[score_name]
    narration_len = dur(manifest.narration)
    total_words = sum(u.words for u in manifest.units)
    total = narration_len + manifest.outro_hold
    print(f"[plan] narration={narration_len:.2f}s total(+{manifest.outro_hold}s hold)={total:.2f}s")

    work = manifest.episode_dir / work_dirname
    work.mkdir(exist_ok=True)

    held = []
    unit_stats = []
    for u in manifest.units:
        slot = narration_len * u.words / total_words
        cdur = dur(u.src)
        out = work / f"{u.tag}__held.mp4"
        if u.mode == "boomerang":
            make_boomerang(u.src, out, slot, cdur, work, u.tag, manifest)
        elif u.tail_loop_seconds is not None:
            make_freeze_tail_loop(u.src, out, slot, cdur, work, u.tag, manifest,
                                   tail_seconds=u.tail_loop_seconds)
        else:
            make_freeze(u.src, out, slot, cdur, work, u.tag, manifest)
        held_duration = dur(out)
        mode_label = f"{u.mode}+tail_loop" if u.tail_loop_seconds is not None else u.mode
        print(f"  [{u.tag}] native={cdur:.2f}s -> slot={slot:.2f}s held={held_duration:.2f}s ({mode_label})")
        held.append(out)
        unit_stats.append({"tag": u.tag, "mode": u.mode, "native": cdur, "slot": slot,
                            "held_duration": held_duration})

    concat_list = work / "concat.txt"
    concat_list.write_text("\n".join(f"file '{p.resolve()}'" for p in held), encoding="utf-8")
    silent_video = work / "silent_concat.mp4"
    run(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0",
         "-i", str(concat_list), "-r", str(manifest.fps), "-c:v", "libx264", "-crf", "18",
         "-preset", "medium", "-pix_fmt", "yuv420p", str(silent_video)])
    print(f"[concat] {dur(silent_video):.2f}s silent video")

    with_narration = work / "with_narration.mp4"
    run(["ffmpeg", "-y", "-v", "error", "-i", str(silent_video), "-i", str(manifest.narration),
         "-map", "0:v", "-map", "1:a", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k",
         "-shortest", str(with_narration)])

    music_chain = f"[1:a]{score_mix.AFMT},volume={variant.duck.gain_db}dB[mus];"
    tail = score_mix.mix_tail(total, manifest.outro_hold, fmt_narration=True,
                               sidechain=variant.duck.sidechain())
    filt = music_chain + tail

    cmd = ["ffmpeg", "-y", "-v", "error",
           "-i", str(with_narration), "-i", str(variant.score),
           "-filter_complex", filt]
    cmd += score_mix.output_args(variant.out, preset="medium", total=total)
    run(cmd)
    final_dur = dur(variant.out)
    print(f"[done] {variant.out}  ({final_dur:.2f}s)")

    return {
        "out": variant.out, "total": total, "narration_len": narration_len,
        "units": unit_stats, "final_duration": final_dur,
    }
