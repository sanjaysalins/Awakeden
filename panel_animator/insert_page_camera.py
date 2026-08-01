#!/usr/bin/env python
"""Insert-Page Camera -- generalizes the proven Style-3 controlled pan
(`poc_living_sketchbook/_style_bakeoff/_controlled_pan_test.py`) from one
hardcoded file + one hardcoded keyframe list into a reusable engine for ANY
insert page (Round 9 build,
`poc_living_sketchbook/_FABLE_ROUND9_BRONZESERPENT_E2E_PLAN.md` sec. B3).

What this is: a deterministic $0 camera move over a STATIC baked-lettering
still -- reading-order pan, controlled push/pull -- never generative motion,
which would garble the page's own baked lettering
(`feedback-never-animate-writing`). Same technique already proven in this
repo (Storm's s13 landing push-in, mapengine's Voyage Camera, the
_controlled_pan_test.py precedent): crop+resize a supersampled source, log-
space zoom interpolation so the zoom FEELS constant-rate at every scale, the
shared smoothstep `ease()` for every keyframe-to-keyframe glide (mapengine's
own `ease()`/`_controlled_pan_test.py`'s own `ease()` -- the CUBIC
smoothstep, not page_transitions.py's quintic `_smootherstep`; this module
keeps that lineage explicit rather than re-deriving the math).

Keyframes: a caller-supplied ORDERED list of dicts, each
`{"t": 0..1, "cx": 0..1, "cy": 0..1, "zoom": >=1.0, "hold_s": seconds}` --
`t`/`cx`/`cy`/`zoom` are exactly `_controlled_pan_test.py`'s own
`(t, cx_frac, cy_frac, zoom)` tuple shape, now data instead of a hardcoded
constant. `hold_s` reuses `mapengine`'s own `camera.keyframes[].hold_s`
FIELD NAME AND SEMANTICS on purpose (see `mapengine.py::build_camera_track`):
the camera ARRIVES at a keyframe's position (at `t * duration_s` seconds),
sits there for `hold_s` more seconds, THEN glides to the next keyframe,
arriving exactly at that keyframe's own `t * duration_s`. `t` fractions
retime automatically to whatever the real forced-alignment window for a
turn turns out to be -- pass the real `duration_s` at render time, not a
guess.

Two flags, both OFF by default, layered ON TOP of the base pan (never baked
into it):
  - `apply_raking_light`: a `raking_light.apply_raking_light()` +
    `apply_gold_flare()` sweep, phase-shifted so its center lines up with
    `raking_light_at` (a t-fraction) -- e.g. "the flare should arrive as the
    camera settles on the John 3 panel." Recomputed from scratch every
    frame (not cached from frame 0) because the CROP itself moves here,
    unlike raking_light.py's own static-still demo usage.
  - `apply_grid_choreography`: intentionally NOT implemented in this pass.
    Real grid choreography (`panel_animator/grid_choreography.py`) operates
    on multiple pre-rendered PANEL CLIPS with its own crossfade/dim
    machinery -- reimplementing that inside a single-still pan/zoom engine
    would be inventing behavior the spec gives no concrete numbers for
    (only raking_light gets a concrete `raking_light_at` for this episode;
    grid choreography is explicitly "not needed for this episode, only a
    literal panel-grid insert would ever need it"). Setting this flag raises
    `NotImplementedError` naming the real module to reach for instead of
    silently no-op'ing (which would falsely claim the effect happened).

Never generative motion, reaffirmed not new: baked lettering pages never go
to a generative animator. Deterministic PIL/ffmpeg crop+resize, forever.

API:
    from insert_page_camera import InsertPageCamera

    cam = InsertPageCamera(still_path, keyframes=[
        {"t": 0.00, "cx": 0.20, "cy": 0.42, "zoom": 1.85, "hold_s": 1.3},
        {"t": 0.55, "cx": 0.62, "cy": 0.35, "zoom": 1.85, "hold_s": 0.0},
        {"t": 1.00, "cx": 0.50, "cy": 0.50, "zoom": 1.00, "hold_s": 1.8},
    ], duration_s=7.36, apply_raking_light=True, raking_light_at=0.55)
    frame = cam.frame_at(t_frac)   # t_frac in 0..1, same domain as keyframe "t"

Usage (CLI):
    .venv\\Scripts\\python.exe panel_animator\\insert_page_camera.py --selftest
    .venv\\Scripts\\python.exe panel_animator\\insert_page_camera.py --demo --still page.png
        --out demo.mp4 --duration 7.36
"""
from __future__ import annotations

import argparse
import math
import shutil
import subprocess
import sys
from pathlib import Path

from PIL import Image

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from raking_light import apply_gold_flare, apply_raking_light  # noqa: E402 -- reuse, don't duplicate

FPS = 30
OUT_W, OUT_H = 1080, 1920
SUPERSAMPLE = 2.0   # fixed implementation default -- plumbing, not a per-page creative choice


def _ease(t: float) -> float:
    """Smootherstep -- SAME formula as mapengine.py's own `ease()` and
    `_controlled_pan_test.py`'s own local `ease()` (the cubic smoothstep,
    NOT page_transitions.py's quintic `_smootherstep`): a constant-feel
    accelerate/decelerate, never a linear ramp. Kept explicit here rather
    than importing mapengine (a whole different-aspect-ratio route engine)
    for one two-line function."""
    t = min(1.0, max(0.0, t))
    return t * t * (3 - 2 * t)


class InsertPageCamera:
    """A deterministic reading-order pan/push/pull camera over ONE static
    insert-page still. Caller supplies the keyframe list; this class only
    knows how to glide between them (log-space zoom + linear cx/cy, eased,
    hold-then-glide per `hold_s`) and crop+resize the result."""

    def __init__(self, still_path, keyframes: list[dict], duration_s: float = 5.5,
                 apply_raking_light: bool = False, raking_light_at: float = 0.5,
                 apply_grid_choreography: bool = False,
                 out_w: int = OUT_W, out_h: int = OUT_H,
                 raking_light_kwargs: "dict | None" = None):
        """
        still_path: path to the already-rendered, already-lettered insert
            page PNG.
        keyframes: ordered list of {"t","cx","cy","zoom","hold_s"} dicts.
            List order = time order (not re-sorted, matching mapengine's own
            "list order = time order" convention). May be empty or a single
            entry -- both are handled without crashing (see frame_at()).
        duration_s: the REAL total seconds this camera's output will run for
            -- needed to convert each keyframe's `hold_s` (real seconds)
            into the same 0..1 `t` domain the keyframes themselves use.
            Retime this per-episode against the real forced-alignment
            window; do not hardcode it into the keyframe list.
        apply_raking_light / raking_light_at: see module docstring.
        apply_grid_choreography: see module docstring -- raises
            NotImplementedError if set True (not built in this pass).
        out_w/out_h: output frame size (default matches this style's 9:16
            page canvas, same as page_transitions.py/measuring_reed.py).
        raking_light_kwargs: optional dict of extra kwargs forwarded to
            raking_light.apply_raking_light()/apply_gold_flare() (k,
            band_width_px, angle_deg, intensity, ...).
        """
        if apply_grid_choreography:
            raise NotImplementedError(
                "apply_grid_choreography is not implemented on InsertPageCamera -- "
                "real grid choreography operates on multiple pre-rendered panel "
                "clips (see panel_animator/grid_choreography.py), not a single "
                "still's pan/zoom camera. Only a literal panel-grid insert page "
                "would need this; composite with grid_choreography.render() "
                "directly for that case instead of setting this flag."
            )
        self.still_path = Path(still_path)
        self.duration_s = duration_s
        self.apply_raking_light = apply_raking_light
        self.raking_light_at = raking_light_at
        self.raking_light_kwargs = raking_light_kwargs or {}
        self.out_w, self.out_h = out_w, out_h

        still = Image.open(self.still_path).convert("RGB")
        sw, sh = still.size
        self._big = still.resize((int(sw * SUPERSAMPLE), int(sh * SUPERSAMPLE)), Image.LANCZOS)

        if not keyframes:
            # empty list: handled without crashing -- fall back to one
            # implicit full-frame-centered keyframe.
            keyframes = [{"t": 0.0, "cx": 0.5, "cy": 0.5, "zoom": 1.0, "hold_s": 0.0}]
        self.keyframes = [
            dict(t=float(k["t"]), cx=float(k.get("cx", 0.5)), cy=float(k.get("cy", 0.5)),
                 zoom=float(k.get("zoom", 1.0)), hold_s=float(k.get("hold_s", 0.0)))
            for k in keyframes
        ]

        # precompute each keyframe's real-second arrival + hold-end time
        arrivals = [kf["t"] * self.duration_s for kf in self.keyframes]
        hold_ends = [arrivals[i] + self.keyframes[i]["hold_s"] for i in range(len(self.keyframes))]
        self._arrivals = arrivals
        self._hold_ends = hold_ends

    def _camera_at_seconds(self, t_s: float):
        kfs = self.keyframes
        if len(kfs) == 1:
            k = kfs[0]
            return k["cx"], k["cy"], k["zoom"]
        if t_s <= self._arrivals[0]:
            k = kfs[0]
            return k["cx"], k["cy"], k["zoom"]
        if t_s >= self._arrivals[-1]:
            k = kfs[-1]
            return k["cx"], k["cy"], k["zoom"]
        for i in range(len(kfs) - 1):
            if self._arrivals[i] <= t_s <= self._arrivals[i + 1]:
                a, b = kfs[i], kfs[i + 1]
                hold_end = self._hold_ends[i]
                if t_s <= hold_end:
                    return a["cx"], a["cy"], a["zoom"]
                glide_span = max(1e-6, self._arrivals[i + 1] - hold_end)
                e = _ease((t_s - hold_end) / glide_span)
                cx = a["cx"] + (b["cx"] - a["cx"]) * e
                cy = a["cy"] + (b["cy"] - a["cy"]) * e
                # log-space zoom interpolation (Voyage Camera technique) --
                # the zoom FEELS constant-rate at every scale, not slow-then-fast.
                zoom = math.exp(math.log(max(1e-6, a["zoom"])) * (1 - e)
                                 + math.log(max(1e-6, b["zoom"])) * e)
                return cx, cy, zoom
        k = kfs[-1]
        return k["cx"], k["cy"], k["zoom"]

    def _crop_for(self, cx_frac: float, cy_frac: float, zoom: float) -> Image.Image:
        bw, bh = self._big.size
        cx, cy = cx_frac * bw, cy_frac * bh
        target_aspect = self.out_w / self.out_h
        crop_h = bh / max(1e-6, zoom)
        crop_w = crop_h * target_aspect
        x0 = max(0.0, min(bw - crop_w, cx - crop_w / 2))
        y0 = max(0.0, min(bh - crop_h, cy - crop_h / 2))
        frame = self._big.crop((x0, y0, x0 + crop_w, y0 + crop_h))
        return frame.resize((self.out_w, self.out_h), Image.LANCZOS)

    def _sweep_progress_for(self, t_frac: float) -> float:
        """Phase-shift the raking-light sweep so its center (where the
        band -- and any gold flare -- peaks) lines up with
        `raking_light_at` instead of always the clip's geometric middle."""
        shift = 0.5 - self.raking_light_at
        return max(0.0, min(1.0, t_frac + shift))

    def frame_at(self, t_frac: float) -> Image.Image:
        """t_frac: 0..1, the SAME domain as keyframes' own `t` field (a
        fraction of duration_s, not raw seconds). frame_at(0) lands exactly
        on the first keyframe's crop; frame_at(1) lands exactly on the last
        keyframe's crop, for any keyframe list including empty/single-entry."""
        t_frac = max(0.0, min(1.0, t_frac))
        t_s = t_frac * self.duration_s
        cx, cy, zoom = self._camera_at_seconds(t_s)
        frame = self._crop_for(cx, cy, zoom)
        if self.apply_raking_light:
            sweep = self._sweep_progress_for(t_frac)
            kw = self.raking_light_kwargs
            frame = apply_raking_light(frame, sweep, tooth=None, **{
                k: v for k, v in kw.items() if k in ("k", "band_width_px", "angle_deg")
            })
            frame = apply_gold_flare(frame, sweep, gold_mask=None, **{
                k: v for k, v in kw.items()
                if k in ("intensity", "band_width_px", "angle_deg", "boost", "bloom_radius")
            })
        return frame

    def render_clip(self, out_mp4: Path, fps: int = FPS):
        n_frames = max(1, int(round(self.duration_s * fps)))
        work = out_mp4.parent / (out_mp4.stem + "_work")
        if work.exists():
            shutil.rmtree(work)
        work.mkdir(parents=True)
        for i in range(n_frames):
            t_frac = i / max(1, n_frames - 1)
            self.frame_at(t_frac).save(work / f"f{i:05d}.png")
        subprocess.run(
            ["ffmpeg", "-y", "-framerate", str(fps), "-i", str(work / "f%05d.png"),
             "-c:v", "libx264", "-pix_fmt", "yuv420p", "-r", str(fps), str(out_mp4)],
            check=True, capture_output=True,
        )
        shutil.rmtree(work)
        print(f"[ok] {out_mp4}")


# ------------------------------------------------------------------ selftest
def run_selftests() -> int:
    import numpy as np

    ok = True

    def check(cond, label):
        nonlocal ok
        print(f"  {'PASS' if cond else 'FAIL'}  {label}")
        ok = ok and cond

    # build a synthetic still (no font/asset dependency for the selftest)
    still = Image.new("RGB", (400, 720), (232, 221, 194))
    tmp_path = Path(__file__).resolve().parent / "_ipc_selftest_still.png"
    still.save(tmp_path)

    try:
        kfs = [
            {"t": 0.00, "cx": 0.20, "cy": 0.42, "zoom": 1.85, "hold_s": 1.3},
            {"t": 0.55, "cx": 0.62, "cy": 0.35, "zoom": 1.85, "hold_s": 0.0},
            {"t": 1.00, "cx": 0.50, "cy": 0.50, "zoom": 1.00, "hold_s": 1.8},
        ]
        cam = InsertPageCamera(tmp_path, keyframes=kfs, duration_s=7.36)

        f_t0 = cam.frame_at(0.0)
        f_first = cam._crop_for(kfs[0]["cx"], kfs[0]["cy"], kfs[0]["zoom"])
        check(np.array_equal(np.asarray(f_t0), np.asarray(f_first)),
              "frame_at(0.0) lands exactly on the first keyframe's crop")

        f_t1 = cam.frame_at(1.0)
        f_last = cam._crop_for(kfs[-1]["cx"], kfs[-1]["cy"], kfs[-1]["zoom"])
        check(np.array_equal(np.asarray(f_t1), np.asarray(f_last)),
              "frame_at(1.0) lands exactly on the last keyframe's crop")

        # empty keyframe list: handled without crashing
        try:
            cam_empty = InsertPageCamera(tmp_path, keyframes=[], duration_s=5.0)
            _ = cam_empty.frame_at(0.3)
            _ = cam_empty.frame_at(1.0)
            check(True, "empty keyframe list handled without crashing")
        except Exception as e:  # noqa: BLE001
            check(False, f"empty keyframe list handled without crashing (raised {e!r})")

        # single keyframe: handled without crashing, and stays constant
        try:
            cam_single = InsertPageCamera(tmp_path, keyframes=[
                {"t": 0.0, "cx": 0.3, "cy": 0.7, "zoom": 1.4, "hold_s": 0.0}
            ], duration_s=4.0)
            a = np.asarray(cam_single.frame_at(0.0))
            b = np.asarray(cam_single.frame_at(1.0))
            check(np.array_equal(a, b), "single-keyframe list handled without crashing, constant crop")
        except Exception as e:  # noqa: BLE001
            check(False, f"single keyframe list handled without crashing (raised {e!r})")

        # apply_grid_choreography=True raises NotImplementedError, not a silent no-op
        try:
            InsertPageCamera(tmp_path, keyframes=kfs, duration_s=7.36, apply_grid_choreography=True)
            check(False, "apply_grid_choreography=True raises NotImplementedError")
        except NotImplementedError:
            check(True, "apply_grid_choreography=True raises NotImplementedError")
    finally:
        tmp_path.unlink(missing_ok=True)

    print(f"\n{'ALL PASS' if ok else 'FAILURES ABOVE'}")
    return 0 if ok else 1


# -------------------------------------------------------------------- CLI
if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--demo", action="store_true")
    ap.add_argument("--still", help="source insert-page PNG (--demo mode)")
    ap.add_argument("--out", help="output mp4 (--demo mode)")
    ap.add_argument("--duration", type=float, default=5.5, help="real seconds this clip should run")
    ap.add_argument("--flare", action="store_true", help="enable apply_raking_light + gold flare")
    ap.add_argument("--flare-at", type=float, default=0.55, dest="flare_at")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()

    if a.selftest:
        raise SystemExit(run_selftests())
    if a.demo:
        if not a.still or not a.out:
            ap.error("--demo requires --still and --out")
        kfs = [
            {"t": 0.00, "cx": 0.20, "cy": 0.42, "zoom": 1.85, "hold_s": 1.3},
            {"t": 0.55, "cx": 0.62, "cy": 0.35, "zoom": 1.85, "hold_s": 0.0},
            {"t": 1.00, "cx": 0.50, "cy": 0.50, "zoom": 1.00, "hold_s": 1.8},
        ]
        cam = InsertPageCamera(Path(a.still), keyframes=kfs, duration_s=a.duration,
                                apply_raking_light=a.flare, raking_light_at=a.flare_at)
        cam.render_clip(Path(a.out))
    else:
        ap.print_help()
