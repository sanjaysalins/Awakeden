#!/usr/bin/env python
"""_finish_long.py -- the ONE shared score+sfx+captions+watermark runner for
a living-sketchbook LONG episode. Born from the Day of Atonement retrospective:
by the time DoA's `_s8_score.py`/`_s9_sfx.py`/`_s10_captions.py` were written,
they were the THIRD ~85%-identical copy of the same three scripts (bronze
short -> bronze long -> DoA), each hand-adapted for nothing but a recipe dict,
a cue table, a skip-window list, and filenames (memory
`day-of-atonement-retro-learnings` fix #6). This module owns the plumbing;
each episode keeps only its own genuinely-per-piece content in a small
`finish_config.py` sitting next to its other episode scripts.

finish_config.py schema (all fields required unless noted):
    STEM = "EPISODE_living_sketchbook"          # base filename stem
    SCORE = {"segments": [...], "xfade_s": 6.0, "gain_db": -11.0, "outro_s": 2.5}
    SFX_CUES = [(slug, spec, gain_db), ...]     # spec is one of:
        "ALL"                        -> whole film, (0.0, TOTAL)
        "some_spread_name"           -> that spread's own (start, end) window
        ("spread_a", "spread_b")     -> span from a.start to b.end
        (12.3, 14.9)                 -> literal absolute seconds (float pair)
    CAPTIONS = {"skip_spreads": [...], "segment_seconds": 60.0}   # spread
        names whose window already carries baked-in lettering
    WATERMARK = True                            # whether `--stage all` runs it

Engines reused, not reimplemented: pipeline/score_mix.py (INV-26 narration-pad
+ duck + mix tail), pipeline/sfx_bed.py (cue-render + bed-mix), the repo-root
add_watermark.py (idempotent in-place burn).

Usage:
    python poc_living_sketchbook/_finish_long.py --episode-dir <dir> [--stage score|sfx|captions|watermark|all]
        [--yes] [--dry-run] [--rebuild] [--out-suffix <sfx>]

`--dry-run` (score/captions only) prints the resolved plan with no rendering.
`--out-suffix` writes to `<STEM>_<stage>{suffix}.mp4` instead of the real
filename -- used by the DoA regression test so it never touches shipped files.
"""
from __future__ import annotations
import argparse
import importlib.util
import json
import random
import subprocess
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, ImageFilter

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from pipeline import score_mix, sfx_bed  # noqa: E402

MUSIC_LIB = ROOT / "music_library" / "clips"
AFMT = "aformat=sample_fmts=fltp:channel_layouts=stereo:sample_rates=44100"

W, H = 1920, 1080
F_KEEPER = "C:/Windows/Fonts/Inkfree.ttf"
INK = (35, 30, 26, 255)
PARCHMENT = (247, 242, 228)
CAPTION_Y_FRAC = 0.86
MAX_TEXT_W = int(W * 0.72)
GAP_BREAK = 0.35
MAX_WORDS = 6
MIN_CHUNK_DUR = 0.45
STROKE_W = 2
FONT_SIZE0 = 46
FONT_SIZE_MIN = 30


def load_config(episode_dir: Path):
    path = episode_dir / "finish_config.py"
    if not path.exists():
        sys.exit(f"missing {path}")
    spec = importlib.util.spec_from_file_location("finish_config", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def dur(p: Path) -> float:
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "default=nw=1:nk=1", str(p)],
        capture_output=True, text=True,
    ).stdout.strip()
    return float(out)


def out_path(episode_dir: Path, stem: str, stage_suffix: str, out_suffix: str) -> Path:
    return episode_dir / f"{stem}{stage_suffix}{out_suffix}.mp4"


def load_windows(episode_dir: Path) -> dict:
    rows = json.loads((episode_dir / "_spread_windows.json").read_text(encoding="utf-8"))
    return {r["name"]: r for r in rows}


def resolve_cue_window(spec, by_name: dict, total: float) -> tuple[float, float]:
    if spec == "ALL":
        return 0.0, total
    if isinstance(spec, str):
        r = by_name[spec]
        return r["start"], r["end"]
    if isinstance(spec, tuple) and len(spec) == 2:
        a, b = spec
        if isinstance(a, str) and isinstance(b, str):
            return by_name[a]["start"], by_name[b]["end"]
        return float(a), float(b)
    raise ValueError(f"bad cue spec: {spec!r}")


# ---------------------------------------------------------------- score ----

def run_score(episode_dir: Path, cfg, yes: bool, regen: bool, out_suffix: str, dry_run: bool) -> None:
    src = episode_dir / f"{cfg.STEM}.mp4"
    dst = out_path(episode_dir, cfg.STEM, "_scored", out_suffix)
    if not src.exists():
        sys.exit(f"missing base cut: {src} -- run the assembly stage first")
    if dst.exists() and not regen:
        print(f"[score] already exists -- skip (--regen to redo): {dst}")
        return

    recipe = cfg.SCORE
    V = dur(src)
    outro = recipe["outro_s"]
    total = V + outro
    gain = recipe["gain_db"]
    xfade_s = recipe["xfade_s"]
    segments = [MUSIC_LIB / (s + ".mp3") for s in recipe["segments"]]
    for seg in segments:
        if not seg.exists():
            sys.exit(f"missing music segment: {seg}")
    seg_durations = [dur(s) for s in segments]
    chained_dur = sum(seg_durations) - xfade_s * (len(segments) - 1)

    print(f"[score] source  : {src.name} ({V:.1f}s)")
    print(f"[score] segments: {[s.name for s in segments]}")
    print(f"[score] arc     : {' -> '.join(f'{d:.0f}s' for d in seg_durations)} "
          f"(xfade {xfade_s}s) = {chained_dur:.1f}s")
    print(f"[score] target  : {total:.1f}s  gain={gain}dB  outro={outro}s")
    print(f"[score] output  : {dst}")
    if dry_run or not yes:
        print("  (dry-run/no --yes -- nothing rendered)")
        return

    n = len(segments)
    if n == 1:
        chain = f"[0:a]{AFMT}[mc]"
    else:
        parts = [f"[{i}:a]{AFMT}[s{i}]" for i in range(n)]
        prev = "s0"
        for i in range(1, n):
            parts.append(f"[{prev}][s{i}]acrossfade=d={xfade_s:.1f}:c1=exp:c2=exp[x{i}]")
            prev = f"x{i}"
        parts.append(f"[{prev}]anull[mc]")
        chain = "; ".join(parts)
    trimmed = dst.with_name(f"_score_music_trimmed{out_suffix}.wav")
    trim_fc = (f"{chain}; [mc]silenceremove=stop_periods=-1:stop_threshold=-50dB:"
               f"stop_duration=0.25,asetpts=PTS-STARTPTS[m]")
    seg_inputs = [x for seg in segments for x in ["-i", str(seg)]]
    pp = subprocess.run(
        ["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", *seg_inputs,
         "-filter_complex", trim_fc, "-map", "[m]", str(trimmed)],
        capture_output=True, text=True)
    if pp.returncode != 0:
        sys.exit(f"[score] music pre-pass FAILED:\n{pp.stderr[-1500:]}")
    music_real = dur(trimmed)
    atempo = max(0.92, min(1.0, music_real / total))
    print(f"[score] music (de-tailed) {music_real:.1f}s -> atempo {atempo:.4f} to fill {total:.1f}s")

    fade_dur = 1.5
    fade_out_start = max(0.0, total - fade_dur)
    fc = (
        f"[1:a]{AFMT},atempo={atempo:.4f},asetpts=PTS-STARTPTS,"
        f"atrim=0:{total + 0.2:.3f},"
        f"afade=t=in:st=0:d=2,"
        f"afade=t=out:st={fade_out_start:.2f}:d={fade_dur},"
        f"volume={gain}dB[mus];"
        + score_mix.mix_tail(total, outro, fmt_narration=True)
    )
    cmd = (
        ["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-i", str(src), "-i", str(trimmed),
         "-filter_complex", fc]
        + score_mix.output_args(dst, preset="veryfast", total=total)
    )
    print("[score] mixing...", flush=True)
    p = subprocess.run(cmd, capture_output=True, text=True)
    if p.returncode != 0:
        sys.exit(f"[score] ffmpeg FAILED:\n{p.stderr[-2000:]}")
    print(f"[score] done -> {dst} ({dur(dst):.1f}s)")


# ------------------------------------------------------------------ sfx ----

def run_sfx(episode_dir: Path, cfg, out_suffix: str) -> None:
    scored = out_path(episode_dir, cfg.STEM, "_scored", out_suffix)
    dst = out_path(episode_dir, cfg.STEM, "_scored_sfx", out_suffix)
    if not scored.exists():
        sys.exit(f"missing scored film: {scored} -- run --stage score first")

    by_name = load_windows(episode_dir)
    total = max(r["end"] for r in by_name.values())
    cues = []
    for slug, spec, gain in cfg.SFX_CUES:
        start, end = resolve_cue_window(spec, by_name, total)
        cues.append((slug, start, end, gain))

    print(f"[sfx] total={total:.1f}s  {len(cues)} cues")
    for slug, start, end, gain in cues:
        print(f"  cue {slug:22s} [{start:7.1f}-{end:7.1f}] {gain}dB")
    sfx_bed.build(scored, dst, cues, total, work=episode_dir / f"_sfx_work{out_suffix}")


# -------------------------------------------------------------- captions ---

def load_words(episode_dir: Path) -> list:
    return json.loads((episode_dir / "_alignment.json").read_text(encoding="utf-8"))


def caption_skip_windows(episode_dir: Path, cfg) -> list[tuple[float, float]]:
    by_name = load_windows(episode_dir)
    return [(by_name[n]["start"], by_name[n]["end"]) for n in cfg.CAPTIONS["skip_spreads"]]


def chunk_words(words: list, skips: list[tuple[float, float]]) -> list:
    chunks, cur = [], []
    for w in words:
        if cur and (w["start"] - cur[-1]["end"] >= GAP_BREAK or len(cur) >= MAX_WORDS):
            chunks.append(cur)
            cur = []
        cur.append(w)
    if cur:
        chunks.append(cur)

    merged = []
    for c in chunks:
        d = c[-1]["end"] - c[0]["start"]
        if merged and d < MIN_CHUNK_DUR and len(merged[-1]) + len(c) <= MAX_WORDS + 2:
            merged[-1].extend(c)
        else:
            merged.append(c)

    out = []
    for c in merged:
        t0, t1 = c[0]["start"], c[-1]["end"]
        if any(t1 >= s0 and t0 <= s1 for s0, s1 in skips):
            continue
        out.append(c)
    return out


def render_chunk_png(chunk: list, seed: int) -> Image.Image:
    rng = random.Random(seed)
    text = " ".join(w["w"] for w in chunk)
    size = FONT_SIZE0
    font = ImageFont.truetype(F_KEEPER, size)
    probe = ImageDraw.Draw(Image.new("RGB", (8, 8)))
    while probe.textlength(text, font=font) > MAX_TEXT_W and size > FONT_SIZE_MIN:
        size -= 2
        font = ImageFont.truetype(F_KEEPER, size)

    canvas = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    sp = probe.textlength(" ", font=font)
    widths = [probe.textlength(w["w"], font=font) for w in chunk]
    total_w = sum(widths) + sp * (len(chunk) - 1)
    x = (W - total_w) / 2
    baseline_y = int(H * CAPTION_Y_FRAC)

    pad_x, pad_y = 22, 14
    scrim = Image.new("RGBA", (int(total_w) + pad_x * 2, size + pad_y * 2), (0, 0, 0, 0))
    sd = ImageDraw.Draw(scrim)
    sd.rounded_rectangle([0, 0, scrim.width - 1, scrim.height - 1], radius=14, fill=(*PARCHMENT, 158))
    scrim = scrim.filter(ImageFilter.GaussianBlur(0.6))
    canvas.alpha_composite(scrim, (int(x - pad_x), int(baseline_y - pad_y)))

    for w, wid in zip(chunk, widths):
        jx, jy, ang = rng.uniform(-2, 2), rng.uniform(-3, 3), rng.uniform(-1.6, 1.6)
        word_img = Image.new("RGBA", (int(wid) + 24, size + 24), (0, 0, 0, 0))
        wd = ImageDraw.Draw(word_img)
        wd.text((12, 8), w["w"], font=font, fill=INK, stroke_width=STROKE_W, stroke_fill=INK)
        word_img = word_img.rotate(ang, resample=Image.BICUBIC, expand=False)
        canvas.alpha_composite(word_img, (int(x + jx - 12), int(baseline_y + jy - 8)))
        x += wid + sp
    return canvas


def build_caption_segment(src: Path, seg_dir: Path, work_dir: Path, seg_idx: int,
                           seg_t0: float, seg_t1: float, chunks_in_seg: list, rebuild: bool) -> Path:
    seg_out = seg_dir / f"seg_{seg_idx:03d}.mp4"
    if seg_out.exists() and not rebuild:
        print(f"  [skip] {seg_out.name} already built")
        return seg_out

    pngs = []
    for i, chunk in enumerate(chunks_in_seg):
        img = render_chunk_png(chunk, seed=1000 * seg_idx + i)
        p = work_dir / f"seg{seg_idx:03d}_cap_{i:03d}.png"
        img.save(p)
        pngs.append((p, chunk[0]["start"] - seg_t0, chunk[-1]["end"] - seg_t0))

    inputs = ["-ss", f"{seg_t0:.3f}", "-t", f"{seg_t1 - seg_t0:.3f}", "-i", str(src)]
    filt_parts, last = [], "0:v"
    for i, (p, t0, t1) in enumerate(pngs):
        inputs += ["-i", str(p)]
        idx, label = i + 1, f"v{i + 1}"
        filt_parts.append(f"[{last}][{idx}:v]overlay=0:0:enable="
                           f"'between(t,{t0:.3f},{t1 + 0.12:.3f})'[{label}]")
        last = label

    if filt_parts:
        cmd = ["ffmpeg", "-y", "-v", "error", *inputs,
               "-filter_complex", ";".join(filt_parts), "-map", f"[{last}]", "-map", "0:a",
               "-c:v", "libx264", "-crf", "18", "-pix_fmt", "yuv420p",
               "-c:a", "aac", "-b:a", "192k", str(seg_out)]
    else:
        cmd = ["ffmpeg", "-y", "-v", "error", *inputs,
               "-c:v", "libx264", "-crf", "18", "-pix_fmt", "yuv420p",
               "-c:a", "aac", "-b:a", "192k", str(seg_out)]
    subprocess.run(cmd, check=True)
    print(f"  [ok] {seg_out.name} ({len(pngs)} caption chunks)")
    return seg_out


def run_captions(episode_dir: Path, cfg, rebuild: bool, out_suffix: str, dry_run: bool) -> None:
    src = out_path(episode_dir, cfg.STEM, "_scored_sfx", out_suffix)
    dst = out_path(episode_dir, cfg.STEM, "_cc", out_suffix)
    if not src.exists():
        sys.exit(f"missing scored+sfx film: {src} -- run --stage sfx first")

    seg_len = cfg.CAPTIONS.get("segment_seconds", 60.0)
    total = dur(src)
    words = load_words(episode_dir)
    skips = caption_skip_windows(episode_dir, cfg)
    chunks = chunk_words(words, skips)
    n_segs = int(total // seg_len) + 1
    print(f"[chunks] {len(chunks)} caption chunks across {total:.1f}s, "
          f"{len(skips)} baked-text windows skipped, {n_segs} segment(s) of ~{seg_len:.0f}s")
    if dry_run:
        print("  (dry-run -- nothing rendered)")
        return

    seg_dir = episode_dir / f"_caption_segments{out_suffix}"
    work_dir = episode_dir / f"_caption_frames{out_suffix}"
    seg_dir.mkdir(exist_ok=True)
    work_dir.mkdir(exist_ok=True)

    seg_files = []
    for seg_idx in range(n_segs):
        seg_t0 = seg_idx * seg_len
        seg_t1 = min(total, seg_t0 + seg_len)
        if seg_t0 >= total:
            break
        chunks_in_seg = [c for c in chunks if c[0]["start"] < seg_t1 and c[-1]["end"] > seg_t0]
        print(f"[seg {seg_idx:03d}] {seg_t0:.1f}-{seg_t1:.1f}s, {len(chunks_in_seg)} chunks")
        seg_files.append(build_caption_segment(src, seg_dir, work_dir, seg_idx, seg_t0, seg_t1,
                                                chunks_in_seg, rebuild))

    concat_list = seg_dir / "_concat_list.txt"
    concat_list.write_text(
        "\n".join(f"file '{p.resolve().as_posix()}'" for p in seg_files) + "\n", encoding="utf-8")
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0",
                     "-i", str(concat_list), "-c", "copy", "-movflags", "+faststart", str(dst)], check=True)
    print(f"[ok] {dst}")


# ------------------------------------------------------------- watermark ---

def run_watermark(episode_dir: Path, cfg, out_suffix: str) -> None:
    cc = out_path(episode_dir, cfg.STEM, "_cc", out_suffix)
    if not cc.exists():
        sys.exit(f"missing captioned film: {cc} -- run --stage captions first")
    spec = importlib.util.spec_from_file_location("add_watermark", ROOT / "add_watermark.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    result = mod.watermark(cc)
    print(f"  {result:<44} {cc}")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--episode-dir", required=True, type=Path)
    ap.add_argument("--stage", choices=["score", "sfx", "captions", "watermark", "all"], default="all")
    ap.add_argument("--yes", action="store_true", help="score stage: actually mix (else prints the plan)")
    ap.add_argument("--dry-run", action="store_true", help="score/captions: print the plan, render nothing")
    ap.add_argument("--regen", action="store_true", help="score: rebuild even if output exists")
    ap.add_argument("--rebuild", action="store_true", help="captions: ignore existing built segments")
    ap.add_argument("--out-suffix", default="", help="write to <STEM>_<stage><suffix>.mp4 instead of the real file")
    args = ap.parse_args()

    cfg = load_config(args.episode_dir)
    stages = ["score", "sfx", "captions", "watermark"] if args.stage == "all" else [args.stage]
    for st in stages:
        if st == "watermark" and not getattr(cfg, "WATERMARK", True):
            print("[watermark] WATERMARK=False in finish_config.py -- skipped")
            continue
        if st == "score":
            run_score(args.episode_dir, cfg, args.yes, args.regen, args.out_suffix, args.dry_run)
        elif st == "sfx":
            run_sfx(args.episode_dir, cfg, args.out_suffix)
        elif st == "captions":
            run_captions(args.episode_dir, cfg, args.rebuild, args.out_suffix, args.dry_run)
        elif st == "watermark":
            run_watermark(args.episode_dir, cfg, args.out_suffix)


if __name__ == "__main__":
    main()
