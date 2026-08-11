"""Drawing Office POC -- Two Goats full assembly.

9 pieces in order: 7 $0 camera/crossfade segments (InsertPageCamera +
one custom relight_split crossfade) + 2 paid Kling inserts, normalized,
concatenated, then muxed with the real narration + INV-26 landing hold.
Timing taken directly from commission.json's beat_plan (real word alignment).
"""
from __future__ import annotations
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
PLATES = HERE / "plates"
DERIVED = HERE / "derived"
INSERTS = HERE / "inserts"
SEG = HERE / "segments"
SEG.mkdir(exist_ok=True)

sys.path.insert(0, str(HERE.parents[1] / "primitives"))
sys.path.insert(0, str(HERE.parents[2] / "panel_animator"))
from insert_page_camera import InsertPageCamera  # noqa: E402
from relight import relight_split  # noqa: E402
from compose import normalize_and_concat, mux_with_landing_hold  # noqa: E402

NARRATION_MP3 = Path(
    r"C:\Users\sanjay\PycharmProjects\JesusInTheBible\poc_living_sketchbook\two_goats\audio\narration.mp3"
)
LAST_WORD_END = 67.427
OUTRO_HOLD = 3.0

CAMERA_SEGMENTS = [
    dict(name="seg1_hook", still=PLATES / "veil.png", duration=7.90, keyframes=[
        {"t": 0.00, "cx": 0.50, "cy": 0.55, "zoom": 1.02, "hold_s": 0.3},
        {"t": 1.00, "cx": 0.50, "cy": 0.50, "zoom": 1.25, "hold_s": 0.0},
    ]),
    dict(name="seg2_proof", still=DERIVED / "goats_split.png", duration=11.90, keyframes=[
        {"t": 0.00, "cx": 0.32, "cy": 0.55, "zoom": 1.30, "hold_s": 0.5},
        {"t": 1.00, "cx": 0.68, "cy": 0.55, "zoom": 1.30, "hold_s": 0.3},
    ]),
    dict(name="seg3_held", still=DERIVED / "goats_split.png", duration=6.52, keyframes=[
        {"t": 0.00, "cx": 0.50, "cy": 0.55, "zoom": 1.15, "hold_s": 6.52},
    ]),
    # seg4_turn is a crossfade, built separately below (not InsertPageCamera).
    dict(name="seg5_christ", still=PLATES / "christ.png", duration=15.45, keyframes=[
        {"t": 0.00, "cx": 0.50, "cy": 0.45, "zoom": 1.02, "hold_s": 1.0},
        {"t": 1.00, "cx": 0.50, "cy": 0.40, "zoom": 1.22, "hold_s": 0.0},
    ]),
    dict(name="seg6_substance", still=DERIVED / "veil_open_final.png", duration=3.83, keyframes=[
        {"t": 0.00, "cx": 0.50, "cy": 0.50, "zoom": 1.02, "hold_s": 3.83},
    ]),
    dict(name="seg7_cta", still=DERIVED / "veil_open_final.png", duration=9.70, keyframes=[
        {"t": 0.00, "cx": 0.50, "cy": 0.50, "zoom": 1.02, "hold_s": 1.0},
        {"t": 1.00, "cx": 0.50, "cy": 0.48, "zoom": 1.10, "hold_s": 2.0},
    ]),
]


def build_crossfade_segment(out_mp4: Path, duration_s: float, fps: int = 30) -> Path:
    """seg4_turn: 'I know now. No single creature could hold both halves.'
    Frame-by-frame relight_split(blend=t) on the RAW two_goats plate -- the
    device's own thesis animated directly via its primitive, not a generic
    video crossfade between two static renders."""
    from PIL import Image
    raw = Image.open(PLATES / "two_goats.png")
    n_frames = max(1, int(round(duration_s * fps)))
    work = out_mp4.parent / (out_mp4.stem + "_work")
    work.mkdir(parents=True, exist_ok=True)
    for i in range(n_frames):
        t = i / max(1, n_frames - 1)
        frame = relight_split(raw, split_x_frac=0.5, left_mode="cool_still",
                               right_mode="warm_departing", blend=t, feather_px=70)
        # match camera_crop's 1080x1920 output canvas
        w, h = frame.size
        target_ar = 1080 / 1920
        cur_ar = w / h
        if cur_ar > target_ar:
            new_w = int(h * target_ar)
            x0 = (w - new_w) // 2
            frame = frame.crop((x0, 0, x0 + new_w, h))
        frame = frame.resize((1080, 1920), Image.LANCZOS)
        frame.save(work / f"f{i:05d}.png")
    subprocess.run(
        ["ffmpeg", "-y", "-framerate", str(fps), "-i", str(work / "f%05d.png"),
         "-c:v", "libx264", "-pix_fmt", "yuv420p", "-r", str(fps), str(out_mp4)],
        check=True, capture_output=True,
    )
    import shutil
    shutil.rmtree(work)
    print(f"[ok] {out_mp4.name} (crossfade, {n_frames} frames)")
    return out_mp4


if __name__ == "__main__":
    print("rendering $0 camera segments...")
    for spec in CAMERA_SEGMENTS:
        out = SEG / f"{spec['name']}.mp4"
        if out.exists():
            print(f"  [skip] {out.name}")
            continue
        cam = InsertPageCamera(spec["still"], keyframes=spec["keyframes"], duration_s=spec["duration"])
        cam.render_clip(out)

    seg4 = SEG / "seg4_turn.mp4"
    if not seg4.exists():
        build_crossfade_segment(seg4, duration_s=5.13)

    pieces = [
        SEG / "seg1_hook.mp4",
        SEG / "seg2_proof.mp4",
        INSERTS / "insert_a_goat_departs.mp4",
        SEG / "seg3_held.mp4",
        SEG / "seg4_turn.mp4",
        SEG / "seg5_christ.mp4",
        INSERTS / "insert_b_veil_tears.mp4",
        SEG / "seg6_substance.mp4",
        SEG / "seg7_cta.mp4",
    ]
    picture = HERE / "picture_track.mp4"
    print("normalizing + concatenating 9 pieces...")
    normalize_and_concat(pieces, picture)
    print(f"[ok] {picture.name}")

    final = HERE / "cut_v1_no_finish.mp4"
    print("muxing narration with landing hold...")
    mux_with_landing_hold(picture, NARRATION_MP3, final, LAST_WORD_END, OUTRO_HOLD)
    print(f"[ok] {final.name}")
