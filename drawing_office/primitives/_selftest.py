"""Self-test runner for drawing_office/primitives -- exercises every function
against a synthetic PNG (no AI generation) and saves outputs to
_selftest_output/ for eye-check. Run:
    .venv\\Scripts\\python.exe drawing_office\\primitives\\_selftest.py
"""
from __future__ import annotations

import subprocess
import sys
import traceback
from pathlib import Path

from PIL import Image, ImageDraw

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
OUT = HERE / "_selftest_output"
OUT.mkdir(parents=True, exist_ok=True)

import relight  # noqa: E402
import crop_study  # noqa: E402
import path_draw  # noqa: E402
import compose  # noqa: E402

results: list[tuple[str, bool, str]] = []


def check(name: str, fn):
    try:
        fn()
        results.append((name, True, ""))
        print(f"  PASS  {name}")
    except Exception as e:  # noqa: BLE001
        results.append((name, False, f"{e!r}"))
        print(f"  FAIL  {name}: {e!r}")
        traceback.print_exc()


def make_synthetic_still() -> Image.Image:
    img = Image.new("RGB", (400, 600), (232, 221, 194))
    d = ImageDraw.Draw(img)
    d.ellipse((120, 220, 280, 380), fill=(120, 70, 40), outline=(40, 20, 10), width=4)
    d.rectangle((0, 500, 400, 600), fill=(90, 110, 130))
    return img


def ffmpeg_still_to_mp4(png: Path, mp4: Path, seconds: float = 1.0, fps: int = 30) -> None:
    subprocess.run(
        ["ffmpeg", "-y", "-loop", "1", "-i", str(png), "-t", str(seconds),
         "-r", str(fps), "-c:v", "libx264", "-pix_fmt", "yuv420p", str(mp4)],
        check=True, capture_output=True,
    )


def ffmpeg_silence_to_mp3(mp3: Path, seconds: float = 2.0) -> None:
    subprocess.run(
        ["ffmpeg", "-y", "-f", "lavfi", "-i", "anullsrc=r=44100:cl=stereo",
         "-t", str(seconds), "-q:a", "9", "-acodec", "libmp3lame", str(mp3)],
        check=True, capture_output=True,
    )


def ffprobe_duration(path: Path) -> float:
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "default=noprint_wrappers=1:nokey=1", str(path)],
        capture_output=True, text=True, check=True,
    ).stdout.strip()
    return float(out)


def main() -> int:
    raw = make_synthetic_still()
    raw_path = OUT / "raw.png"
    raw.save(raw_path)
    print(f"[setup] synthetic still -> {raw_path} size={raw.size}")

    # ---------------------------------------------------------- relight.py
    def t_radial_vignette():
        mask = relight.radial_vignette(raw, 0.5, 0.5, inner_frac=0.15, outer_frac=0.6, dark_to=0.2)
        mask.save(OUT / "relight_radial_vignette_mask.png")
        assert mask.mode == "L"
        assert mask.size == raw.size

    def t_relight_radial_night():
        img = relight.relight_radial(raw, mode="night", cx_frac=0.5, cy_frac=0.55)
        img.save(OUT / "relight_radial_night.png")
        assert img.size == raw.size
        assert img.mode == "RGB"

    def t_relight_radial_dawn():
        img = relight.relight_radial(raw, mode="dawn", cx_frac=0.5, cy_frac=0.55)
        img.save(OUT / "relight_radial_dawn.png")
        assert img.size == raw.size

    def t_relight_radial_bad_mode():
        try:
            relight.relight_radial(raw, mode="nonexistent")
            raise AssertionError("expected ValueError for unknown mode")
        except ValueError:
            pass

    def t_relight_split_pure():
        img = relight.relight_split(raw, split_x_frac=0.5, left_mode="cool_still",
                                     right_mode="warm_departing", blend=0.0, feather_px=40)
        img.save(OUT / "relight_split_blend0.png")
        assert img.size == raw.size

    def t_relight_split_half():
        img = relight.relight_split(raw, split_x_frac=0.5, left_mode="cool_still",
                                     right_mode="warm_departing", blend=0.5, feather_px=40)
        img.save(OUT / "relight_split_blend0.5.png")
        assert img.size == raw.size

    def t_relight_split_unified():
        img = relight.relight_split(raw, split_x_frac=0.5, left_mode="cool_still",
                                     right_mode="warm_departing", blend=1.0, feather_px=40)
        img.save(OUT / "relight_split_blend1.png")
        assert img.size == raw.size

    check("relight.radial_vignette", t_radial_vignette)
    check("relight.relight_radial(mode=night)", t_relight_radial_night)
    check("relight.relight_radial(mode=dawn)", t_relight_radial_dawn)
    check("relight.relight_radial(bad mode raises ValueError)", t_relight_radial_bad_mode)
    check("relight.relight_split(blend=0.0)", t_relight_split_pure)
    check("relight.relight_split(blend=0.5)", t_relight_split_half)
    check("relight.relight_split(blend=1.0)", t_relight_split_unified)

    # -------------------------------------------------------- crop_study.py
    def t_crop_zoom_default_size():
        img = crop_study.crop_zoom(raw, box_frac=(0.2, 0.3, 0.8, 0.75))
        img.save(OUT / "crop_zoom_default.png")
        assert img.size == raw.size

    def t_crop_zoom_explicit_size():
        img = crop_study.crop_zoom(raw, box_frac=(0.3, 0.35, 0.6, 0.6), out_size=(200, 200))
        img.save(OUT / "crop_zoom_explicit.png")
        assert img.size == (200, 200)

    def t_camera_crop():
        img = crop_study.camera_crop(raw, cx_frac=0.5, cy_frac=0.5, zoom=1.6, out_w=540, out_h=960)
        img.save(OUT / "camera_crop.png")
        assert img.size == (540, 960)

    check("crop_study.crop_zoom(out_size=None)", t_crop_zoom_default_size)
    check("crop_study.crop_zoom(out_size=(200,200))", t_crop_zoom_explicit_size)
    check("crop_study.camera_crop", t_camera_crop)

    # --------------------------------------------------------- path_draw.py
    def t_draw_wobbled_path():
        out_path = OUT / "path_draw_wobbled.png"
        path_draw.draw_wobbled_path(
            raw_path, out_path,
            start_frac=(0.5, 0.86), end_frac=(0.27, 0.5),
        )
        assert out_path.exists() and out_path.stat().st_size > 0
        with Image.open(out_path) as im:
            assert im.size == raw.size

    check("path_draw.draw_wobbled_path", t_draw_wobbled_path)

    # ----------------------------------------------------------- compose.py
    def t_tear_vertical():
        img = compose.tear_vertical(raw, tear_x_frac=0.5, jag_amplitude_px=18, gap_px=14)
        img.save(OUT / "compose_tear_vertical.png")
        assert img.size == raw.size

    check("compose.tear_vertical", t_tear_vertical)

    concat_out = OUT / "compose_normalize_and_concat.mp4"

    def t_normalize_and_concat():
        clip_a = OUT / "_clip_a.mp4"
        clip_b = OUT / "_clip_b.mp4"
        ffmpeg_still_to_mp4(raw_path, clip_a, seconds=1.0)
        img_b = relight.relight_radial(raw, mode="dawn")
        img_b_path = OUT / "_clip_b_source.png"
        img_b.save(img_b_path)
        ffmpeg_still_to_mp4(img_b_path, clip_b, seconds=1.0)
        compose.normalize_and_concat([clip_a, clip_b], concat_out, canvas_w=400, canvas_h=600, fps=30)
        assert concat_out.exists() and concat_out.stat().st_size > 0
        dur = ffprobe_duration(concat_out)
        assert 1.8 <= dur <= 2.2, f"unexpected concat duration {dur}"

    check("compose.normalize_and_concat", t_normalize_and_concat)

    def t_mux_with_landing_hold():
        narration = OUT / "_narration.mp3"
        ffmpeg_silence_to_mp3(narration, seconds=1.5)
        mux_out = OUT / "compose_mux_with_landing_hold.mp4"
        last_word_end = 1.5
        outro_hold = 3.0
        compose.mux_with_landing_hold(concat_out, narration, mux_out,
                                       last_word_end_s=last_word_end, outro_hold_s=outro_hold)
        assert mux_out.exists() and mux_out.stat().st_size > 0
        dur = ffprobe_duration(mux_out)
        expected = last_word_end + outro_hold
        assert abs(dur - expected) <= 0.3, f"expected ~{expected}s, got {dur}s"

    check("compose.mux_with_landing_hold", t_mux_with_landing_hold)

    # ------------------------------------------------------------- summary
    n_pass = sum(1 for _, ok, _ in results if ok)
    n_fail = len(results) - n_pass
    print(f"\n{n_pass}/{len(results)} PASS, {n_fail} FAIL")
    for name, ok, err in results:
        if not ok:
            print(f"  FAILED: {name}  {err}")
    return 0 if n_fail == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
