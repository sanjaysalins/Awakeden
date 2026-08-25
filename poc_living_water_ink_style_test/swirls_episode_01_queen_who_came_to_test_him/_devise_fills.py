"""Build devised fills for F01-F04 (replace plain freeze per user's "I hate
the freeze" note, 2026-08-25). Per-page device picked by Fable, grounded in
the actual stills + the existing panel_animator/northstar_shortform toolkit
(see build_fills.py for the validated reference pattern this adapts):

  F01 -> Halo Tour (focal_tour, full frame): eyes panel -> chest panel ->
         city panel -> the horizon/thread in the main scene.
  F02 -> parallax_25d on the MAIN-SCENE CROP ONLY (queen as fg layer); panel
         row + title + caption stay byte-static (parallax is a real geometric
         pan, would violate "frame borders/baked text stay static" if run on
         the full frame). Falls back to a Halo Tour (hand/Solomon/gifts) if
         the rembg matte looks dirty on eye-check.
  F03 -> Live Ink Hold (ink_bloom, full frame): point on the blue pool at her
         feet, manually verified clear of the robe.
  F04 -> Lamplight (raking_light, full frame, over native+held fill) -- a
         brightness sweep, not a geometric transform, so it's safe over the
         panel row too (matches how the reference project applied it).

line_boil (the per-frame wobble) is deliberately SKIPPED here even though the
reference project used it as a universal base layer -- it's a geometric
transform (translate/rotate) and this project's own locked animation-prompt
rule requires "frame borders and all baked text stay static"; wobbling the
whole frame would violate that. The picked devices supply the "alive" feeling
without it.
"""
from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
PANEL_ANIM = HERE.parents[1] / "panel_animator"
NORTHSTAR = HERE.parent / "northstar_shortform"
sys.path.insert(0, str(PANEL_ANIM))
sys.path.insert(0, str(NORTHSTAR))

import focal_tour  # noqa: E402
from focal_tour import _render_spotlight, _DIM_FLOOR_DRAMATIC  # noqa: E402
import raking_light  # noqa: E402
import ink_bloom  # noqa: E402

from PIL import Image  # noqa: E402

STEM = HERE.name


def dur(p: Path) -> float:
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "default=nw=1:nk=1", str(p)],
        capture_output=True, text=True, check=True).stdout.strip()
    return float(out)


def clip_size(p: Path) -> tuple[int, int]:
    """Native clips render at a DIFFERENT resolution than the 2k still PNG
    (e.g. 1076x1928 vs 1536x2752) -- always probe the actual clip, never
    hardcode the still's size, or concat silently corrupts (confirmed: a
    resolution-mismatched concat produced a solid-black lower frame)."""
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-select_streams", "v:0",
         "-show_entries", "stream=width,height", "-of", "csv=s=x:p=0", str(p)],
        capture_output=True, text=True, check=True).stdout.strip()
    w, h = out.split("x")
    return int(w), int(h)


def run(cmd: list[str]) -> None:
    subprocess.run(cmd, check=True, capture_output=True)


def last_frame(clip: Path, out_png: Path) -> None:
    run(["ffmpeg", "-y", "-v", "error", "-sseof", "-0.1", "-i", str(clip),
         "-vframes", "1", str(out_png)])


def concat(parts: list[Path], out_mp4: Path, work: Path) -> None:
    """Concat FILTER, not demuxer -- the demuxer's raw stream-level join produced
    a confirmed timing bug on a devised fill (flat, then one hard jump, then flat
    again, instead of a smooth ramp) when joining two independently-encoded
    clips. The filter decodes and re-times both properly."""
    if len(parts) == 1:
        run(["ffmpeg", "-y", "-v", "error", "-i", str(parts[0]), "-c", "copy", str(out_mp4)])
        return
    inputs = []
    for p in parts:
        inputs += ["-i", str(p)]
    n = len(parts)
    filt = "".join(f"[{i}:v]" for i in range(n)) + f"concat=n={n}:v=1:a=0[out]"
    run(["ffmpeg", "-y", "-v", "error", *inputs, "-filter_complex", filt, "-map", "[out]",
         "-c:v", "libx264", "-crf", "18", "-preset", "medium", "-pix_fmt", "yuv420p",
         "-r", "24", str(out_mp4)])


def hold_png(png: Path, seconds: float, out_mp4: Path) -> None:
    run(["ffmpeg", "-y", "-v", "error", "-loop", "1", "-i", str(png), "-t", f"{seconds:.3f}",
         "-r", "24", "-c:v", "libx264", "-crf", "18", "-preset", "medium",
         "-pix_fmt", "yuv420p", str(out_mp4)])


# ---- F01: Halo Tour, full frame ------------------------------------------

def build_f01(extend: float) -> Path:
    """Fable's 4-stop tour design doesn't fit the real budget: focal_tour's own
    'never rush an element' floor (>=1.0s per stop, default 2.5s holds either
    end) needs >=10s structurally for 4 stops; only extend=2.93s is available.
    Collapsed to ONE stop -- the horizon/thread, the subtlest detail and the
    one most worth a spotlight -- with custom short timing that still respects
    the >=1.0s floor honestly instead of silently rushing 4 stops past it."""
    tag = "f01"
    native = HERE / f"{STEM}_{tag}_9x16.mp4"
    w, h = clip_size(native)
    work = HERE / f"_fillwork_{tag}"
    work.mkdir(exist_ok=True)
    lf = work / "last.png"
    last_frame(native, lf)

    regions = [
        {"bbox": [55.0, 33.0, 20.0, 15.0]},      # the horizon notch + blue thread, main scene
    ]
    tail = work / "tail.mp4"
    src = Image.open(lf).convert("RGB")
    if src.size != (w, h):
        src = src.resize((w, h), Image.LANCZOS)
    _render_spotlight(src, regions, extend, w, h, tail, dim_floor=_DIM_FLOOR_DRAMATIC,
                      initial_hold_sec=0.2, move_sec=0.5, final_hold_sec=0.3)

    out = HERE / f"{STEM}_{tag}_9x16_devised.mp4"
    concat([native, tail], out, work)
    shutil.rmtree(work)
    print(f"[f01] halo tour, extend={extend:.2f}s -> {out.name} ({dur(out):.2f}s)")
    return out


# ---- F02: parallax on the main-scene crop only ---------------------------

def build_f02(extend: float) -> Path:
    tag = "f02"
    native = HERE / f"{STEM}_{tag}_9x16.mp4"
    w, h = clip_size(native)
    main_top = int(h * 0.24)
    main_bot = int(h * 0.90)
    if (main_bot - main_top) % 2:  # libx264 requires an even encode height
        main_bot -= 1
    work = HERE / f"_fillwork_{tag}"
    work.mkdir(exist_ok=True)
    lf = work / "last.png"
    last_frame(native, lf)

    full = Image.open(lf).convert("RGB")
    if full.size != (w, h):
        full = full.resize((w, h), Image.LANCZOS)
    main_crop_path = work / "main_crop.png"
    full.crop((0, main_top, w, main_bot)).save(main_crop_path)
    crop_h = main_bot - main_top

    from parallax_25d import render as parallax_render
    parallax_mp4 = work / "parallax.mp4"
    parallax_render(main_crop_path, parallax_mp4, extend, fg_amp=10.0, bg_amp=4.0)

    # composite each parallax frame back under the byte-static panel row + caption
    frames_dir = work / "pframes"
    frames_dir.mkdir(exist_ok=True)
    run(["ffmpeg", "-y", "-v", "error", "-i", str(parallax_mp4), str(frames_dir / "f%05d.png")])
    comp_dir = work / "cframes"
    comp_dir.mkdir(exist_ok=True)
    n = 0
    for fp in sorted(frames_dir.glob("f*.png")):
        band = Image.open(fp).convert("RGB")
        if band.size != (w, crop_h):
            band = band.resize((w, crop_h), Image.LANCZOS)
        canvas = full.copy()
        canvas.paste(band, (0, main_top))
        canvas.save(comp_dir / fp.name)
        n += 1
    tail = work / "tail.mp4"
    run(["ffmpeg", "-y", "-v", "error", "-framerate", "30", "-i", str(comp_dir / "f%05d.png"),
         "-r", "24", "-c:v", "libx264", "-crf", "18", "-preset", "medium",
         "-pix_fmt", "yuv420p", str(tail)])

    out = HERE / f"{STEM}_{tag}_9x16_devised.mp4"
    concat([native, tail], out, work)
    shutil.rmtree(work)
    print(f"[f02] parallax (main-scene crop), extend={extend:.2f}s -> {out.name} ({dur(out):.2f}s)")
    return out


def build_f02_fallback_halo(extend: float) -> Path:
    """Fallback per Fable's own brief if the rembg matte is dirty."""
    tag = "f02"
    native = HERE / f"{STEM}_{tag}_9x16.mp4"
    w, h = clip_size(native)
    work = HERE / f"_fillwork_{tag}"
    work.mkdir(exist_ok=True)
    lf = work / "last.png"
    last_frame(native, lf)
    regions = [
        {"bbox": [4.23, 11.12, 28.32, 22.64]},   # panel 1: hard questions (her hand)
        {"bbox": [35.94, 11.12, 28.26, 22.64]},  # panel 2: nothing hid (Solomon's face)
        {"bbox": [67.45, 11.12, 28.39, 22.64]},  # panel 3: gold and spices
    ]
    tail = work / "tail.mp4"
    focal_tour.render_clip(lf, regions, "dramatic_spotlight", extend, w, h, tail)
    out = HERE / f"{STEM}_{tag}_9x16_devised.mp4"
    concat([native, tail], out, work)
    shutil.rmtree(work)
    print(f"[f02] FALLBACK halo tour, extend={extend:.2f}s -> {out.name} ({dur(out):.2f}s)")
    return out


# ---- F03: Live Ink Hold, full frame ---------------------------------------

def build_f03(extend: float) -> Path:
    tag = "f03"
    native = HERE / f"{STEM}_{tag}_9x16.mp4"
    w, h = clip_size(native)
    work = HERE / f"_fillwork_{tag}"
    work.mkdir(exist_ok=True)
    lf = work / "last.png"
    last_frame(native, lf)

    tail = work / "tail.mp4"
    # point manually verified on the rendered still: the blue pool at her feet,
    # well clear of the robe hem and the sandals themselves.
    ink_bloom.render_hold(
        lf, tail, extend,
        cx_frac=0.50, cy_frac=0.84, radius_frac=0.10, max_strength=0.45,
        energy_fn=lambda t: 1.0, t0_global=0.0, w=w, h=h, fps=24,
    )
    out = HERE / f"{STEM}_{tag}_9x16_devised.mp4"
    concat([native, tail], out, work)
    shutil.rmtree(work)
    print(f"[f03] live ink hold, extend={extend:.2f}s -> {out.name} ({dur(out):.2f}s)")
    return out


# ---- F04: Lamplight, over native+held fill --------------------------------

def build_f04(extend: float) -> Path:
    """RETUNED (user, 2026-08-25): Lamplight still read as "a freeze frame" --
    too subtle to register as real motion. F04 has camels, so boomerang is
    off the table here (that's the original bug this whole detour started
    from). Swapped to the same Halo Tour device that clearly worked on F01,
    single stop on the small blue-gold bloom pooled in the trodden sand
    (found by direct crop inspection, two blooms close together, tour
    targets the region spanning both)."""
    tag = "f04"
    native = HERE / f"{STEM}_{tag}_9x16.mp4"
    w, h = clip_size(native)
    work = HERE / f"_fillwork_{tag}"
    work.mkdir(exist_ok=True)
    lf = work / "last.png"
    last_frame(native, lf)

    regions = [
        {"bbox": [65.0, 70.0, 20.0, 12.0]},  # the two small blue-gold blooms in the sand track
    ]
    tail = work / "tail.mp4"
    src = Image.open(lf).convert("RGB")
    if src.size != (w, h):
        src = src.resize((w, h), Image.LANCZOS)
    _render_spotlight(src, regions, extend, w, h, tail, dim_floor=_DIM_FLOOR_DRAMATIC,
                      initial_hold_sec=0.2, move_sec=0.5, final_hold_sec=0.3)
    out = HERE / f"{STEM}_{tag}_9x16_devised.mp4"
    concat([native, tail], out, work)
    shutil.rmtree(work)
    print(f"[f04] halo tour (bloom in sand), extend={extend:.2f}s -> {out.name} ({dur(out):.2f}s)")
    return out


# ---- F02/F03: simple boomerang of the native clip (per user's own call --
# ambient/non-directional motion boomerangs fine; only camel-walking pages
# needed the freeze/devised-fill treatment) ---------------------------------

def build_boomerang(tag: str) -> Path:
    native = HERE / f"{STEM}_{tag}_9x16.mp4"
    work = HERE / f"_fillwork_{tag}b"
    work.mkdir(exist_ok=True)
    ndur = dur(native)
    reversed_mp4 = work / "reversed.mp4"
    run(["ffmpeg", "-y", "-v", "error", "-i", str(native), "-vf", "reverse", "-an", str(reversed_mp4)])
    out = HERE / f"{STEM}_{tag}_9x16_devised.mp4"
    concat([native, reversed_mp4], out, work)
    shutil.rmtree(work)
    print(f"[{tag}] boomerang (native {ndur:.2f}s x2), -> {out.name} ({dur(out):.2f}s)")
    return out


if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--pages", default="f01,f02,f03,f04")
    ap.add_argument("--f02-fallback", action="store_true")
    args = ap.parse_args()
    wanted = set(args.pages.split(","))

    EXTEND = {"f01": 2.93, "f02": 3.26, "f03": 3.26, "f04": 3.26}

    if "f01" in wanted:
        build_f01(EXTEND["f01"])
    if "f02" in wanted:
        build_boomerang("f02")
    if "f03" in wanted:
        build_boomerang("f03")
    if "f04" in wanted:
        build_f04(EXTEND["f04"])
