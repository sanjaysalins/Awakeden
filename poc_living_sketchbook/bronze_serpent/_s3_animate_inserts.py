"""Bronze Serpent -- animate BOTH insert pages (s08, s12) with the reusable
`InsertPageCamera` engine (2026-07-31). $0, deterministic ffmpeg/PIL crop+
resize -- never generative motion on a baked-lettering/iconographic page
(`feedback-never-animate-writing`).

Sources:
- panel_animator/insert_page_camera.py -- the engine itself.
- poc_living_sketchbook/_FABLE_ROUND9_BRONZESERPENT_E2E_PLAN.md sec. B3 --
  s08's keyframes are given VERBATIM there (open close on Numbers 21 panel
  -> glide right across the arrow -> pull back wide, both labels legible),
  reused unchanged here, not redesigned.
- poc_living_sketchbook/bronze_serpent/_TIMING.md -- real per-spread windows.
  s08: 36.879-43.887s (full window) / 36.879-42.316s (quote only). s12:
  57.128-62.936s (single window, no sub-breakdown).

s08 duration_s choice: the FULL 7.008s spread window (43.887-36.879), not
the 5.437s quote-only span. Reasoning: the B3 keyframes were authored
against the plan's own assumed 7.36s full-turn duration (see the plan doc's
"Total window ~= 7.36s (matches s08's real turn duration...)"), including a
1.8s hold on the final wide keyframe explicitly left open "for the John
3:14 verse card overlay to arrive on top of" -- that pacing only works with
the trailing-pause room the full window provides. The real 7.008s full
window lands almost exactly on the plan's original 7.36s design assumption
(the whole episode timeline compressed ~11% from the stale metadata, but
this particular window barely moved), so it is the closer match to what
the keyframes were actually designed for. Using the 5.437s quote-only span
instead would compress the final hold to almost nothing.

s12 duration_s: 5.808s (62.936-57.128), the episode's one real window for
this spread -- no sub-breakdown to choose between.

s12 keyframes (new, this page is NOT a two-panel diagram like s08 -- see
the render script's own docstring for why): open close on the dull bronze
serpent low in the frame -> slow reverent push/rise up to Christ on the
radiant cross -> pull back wide, held, on the whole gold-ground scene.
apply_raking_light timed (raking_light_at=0.55, matching s08's own proven
demo) to arrive as the camera settles on Christ -- the glory light itself
moving like a living thing.

  .venv\\Scripts\\python.exe poc_living_sketchbook/bronze_serpent/_s3_animate_inserts.py
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PANEL_ANIMATOR = ROOT / "panel_animator"
sys.path.insert(0, str(PANEL_ANIMATOR))
from insert_page_camera import InsertPageCamera  # noqa: E402

HERE = Path(__file__).resolve().parent
CLIPS = HERE / "clips"
CLIPS.mkdir(parents=True, exist_ok=True)

S08_STILL = ROOT / "poc_living_sketchbook" / "_style_bakeoff" / "bronzeserpent_typology_numbers21_john3.png"
S12_STILL = HERE / "stills" / "s12_echo.png"


def animate_s08():
    """Verbatim keyframes from _FABLE_ROUND9_BRONZESERPENT_E2E_PLAN.md sec. B3:
    close on Numbers 21 panel -> glide right across the arrow to John 3 ->
    pull back wide, both labels legible (raking-light gold flare arrives as
    the camera settles on the John 3 / Christ panel)."""
    cam = InsertPageCamera(
        S08_STILL,
        keyframes=[
            {"t": 0.00, "cx": 0.20, "cy": 0.42, "zoom": 1.85, "hold_s": 1.3},  # close on Numbers 21 panel
            {"t": 0.55, "cx": 0.62, "cy": 0.35, "zoom": 1.85, "hold_s": 0.0},  # glide right, across the arrow
            {"t": 1.00, "cx": 0.50, "cy": 0.50, "zoom": 1.00, "hold_s": 1.8},  # pull back, wide, both labels legible
        ],
        duration_s=7.008,  # real full spread window, see module docstring
        apply_raking_light=True,
        raking_light_at=0.55,
    )
    out = CLIPS / "s08_typology.mp4"
    cam.render_clip(out)
    return out


def animate_s12():
    """New keyframes for the unified (not two-panel) composition: open low
    on the dull bronze serpent -> slow reverent push/rise to Christ on the
    radiant cross -> pull back wide on the whole gold-ground scene."""
    cam = InsertPageCamera(
        S12_STILL,
        keyframes=[
            {"t": 0.00, "cx": 0.24, "cy": 0.82, "zoom": 1.90, "hold_s": 1.0},  # open close on the dull serpent, low
            {"t": 0.55, "cx": 0.50, "cy": 0.22, "zoom": 1.60, "hold_s": 0.0},  # reverent push up to Christ / the gold
            {"t": 1.00, "cx": 0.50, "cy": 0.50, "zoom": 1.00, "hold_s": 0.0},  # pull back, wide, whole scene held
        ],
        duration_s=5.808,  # real spread window, see module docstring
        apply_raking_light=True,
        raking_light_at=0.55,
    )
    out = CLIPS / "s12_echo.mp4"
    cam.render_clip(out)
    return out


if __name__ == "__main__":
    only = sys.argv[1] if len(sys.argv) > 1 else None
    if only in (None, "s08"):
        print(f"[s08] rendering...")
        p = animate_s08()
        print(f"[s08] {p}")
    if only in (None, "s12"):
        print(f"[s12] rendering...")
        p = animate_s12()
        print(f"[s12] {p}")
