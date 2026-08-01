#!/usr/bin/env python
"""Margin Study -- the doodle with a reason (Round 6 promotion, panel-revised
2026-07-30, `poc_living_sketchbook/_FABLE_ROUND6_THE_KEEPER.md` build card 2).
Promotes `pencil_study` + sweep reveal + leader line + Keeper caption from
`poc_living_sketchbook/storm/_keeper_poc/_build_poc.py` (poc_C, "lamp
studies") into a reusable `MarginStudy` cluster.

GOVERNORS (episode-design rules, not all enforced by this module -- see
`keeper_lint.py` for the deterministic half):
  - Studies derive ONLY from the spread's OWN approved art (a crop of the
    already-rendered still) -- they can never contradict the drawing. This
    module has no way to invent a subject; the caller must pass a real crop.
  - <=1 cluster (2-3 studies) per episode.
  - Subject = what the Keeper would fixate on -- the narration NAMES it, not
    an arbitrary detail.
  - A study of the Face is fail-closed to the user's eye (human judgment call,
    not automatable).
  - Contrast default 2.6 -- the v6.1 art-direction value (LAW 2's "bigger and
    bolder" applied to graphite: NOT the original POC's 1.9/2.3, both of which
    were pre-scale-law).
  - Foley: soft `graphite_scratch` under each reveal (cue name exported by
    `MarginStudy.foley_cues()`; not yet mapped to a sound_library asset in
    `scriptorium_foley.py` -- see that gap noted in this engine's SKILL.md).

API:
    from margin_study import pencil_study, sweep_reveal, leader_layer, MarginStudy

    crop = still.crop(lamp_box)           # the spread's OWN art, nothing invented
    cluster = MarginStudy(
        source_crop=crop,
        studies=[
            {"out_w": 240, "seed": 7, "pos": (108, 1686), "t0": 0.5, "dur": 0.7},
            {"out_w": 210, "seed": 8, "pos": (367, 1713), "t0": 1.6, "dur": 0.7},
        ],
        leader={"from_study": 1, "to_xy": (340, 1075), "seed": 9, "t0": 2.6, "dur": 0.4},
        caption=keeper_hand.KeeperEntry(["still burning."], origin=(594, 1743),
                                         size=56, energy=0.25, seed=43, t0=3.1, dur=0.9),
    )
    frame = cluster.compose(frame, t)
    cues = cluster.foley_cues()

Usage (CLI):
    .venv\\Scripts\\python.exe panel_animator\\margin_study.py --demo --still <still.png> --out demo.mp4 --duration 5
    .venv\\Scripts\\python.exe panel_animator\\margin_study.py --selftest
"""
from __future__ import annotations

import argparse
import math
import random
import shutil
import subprocess
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from raking_light import scale_crop  # noqa: E402 -- reuse, don't duplicate

FPS = 30
W, H = 1080, 1920
CONTRAST_DEFAULT = 2.6   # LAW 2 / v6.1 value -- NOT the POC's 1.9
KEEPER_INK_RGB = (66, 60, 54)


def _clamp01(x: float) -> float:
    return max(0.0, min(1.0, x))


# ---------------------------------------------------------------- the study


def pencil_study(src: Image.Image, out_w: int, seed: int,
                  contrast: float = CONTRAST_DEFAULT) -> Image.Image:
    """A quick graphite STUDY derived from the spread's own art: gray ->
    invert-blur-dodge (classic pencil conversion) -> soft irregular border.
    Unchanged math from the approved POC
    (`_keeper_poc/_build_poc.py::pencil_study`); the default `contrast` is
    the ONLY change (2.6, the v6.1 LAW-2-era value)."""
    rng = random.Random(seed)
    im = src.convert("L")
    s = out_w / im.width
    im = im.resize((out_w, int(im.height * s)), Image.LANCZOS)
    g = np.asarray(im, dtype=np.float32)
    inv = 255.0 - g
    blur = np.asarray(Image.fromarray(inv.astype(np.uint8))
                       .filter(ImageFilter.GaussianBlur(6 + 4 * rng.random())), dtype=np.float32)
    dodge = np.clip(g * 255.0 / np.clip(255.0 - blur, 12, 255), 0, 255)
    pencil = 255.0 - np.clip((255.0 - dodge) * (1.5 * contrast), 0, 255)

    h, w = pencil.shape
    ys, xs = np.mgrid[0:h, 0:w].astype(np.float32)
    cx, cy = w / 2, h / 2
    r = np.maximum(np.abs(xs - cx) / (w * 0.52), np.abs(ys - cy) / (h * 0.52))
    edge = np.clip((1.05 - r) * 6.0, 0, 1)
    noise = np.asarray(Image.fromarray(
        (np.random.default_rng(seed).random((h // 8 + 1, w // 8 + 1)) * 255).astype(np.uint8)
    ).resize((w, h), Image.BICUBIC), dtype=np.float32) / 255.0
    edge = np.clip(edge - 0.35 * noise * (r > 0.7), 0, 1)

    alpha = (1.0 - pencil / 255.0) * edge
    rgba = np.zeros((h, w, 4), dtype=np.uint8)
    rgba[..., 0], rgba[..., 1], rgba[..., 2] = KEEPER_INK_RGB
    rgba[..., 3] = np.clip(alpha * 235, 0, 255).astype(np.uint8)
    return Image.fromarray(rgba, "RGBA").rotate(rng.uniform(-4, 4), expand=True,
                                                 resample=Image.BICUBIC)


def sweep_reveal(layer: Image.Image, frac: float, angle_deg: float = 38.0) -> Image.Image:
    """Reveal a study along a diagonal front -- quick hatching, not a fade.
    Unchanged from the approved POC."""
    if frac >= 1.0:
        return layer
    w, h = layer.size
    ys, xs = np.mgrid[0:h, 0:w].astype(np.float32)
    proj = xs * math.cos(math.radians(angle_deg)) + ys * math.sin(math.radians(angle_deg))
    pr = (proj - proj.min()) / max(1e-6, proj.max() - proj.min())
    m = np.clip((frac - pr) * 12.0, 0, 1)
    a = np.asarray(layer.split()[3], dtype=np.float32) * m
    out = layer.copy()
    out.putalpha(Image.fromarray(a.astype(np.uint8)))
    return out


def leader_layer(p0, p1, seed: int):
    """Wobbly leader line from a study toward the detail it studies. Returns
    (layer, ox, oy, pts). Unchanged from the approved POC."""
    rng = random.Random(seed)
    x0, y0 = p0
    x1, y1 = p1
    pad = 12
    lw, lh = abs(x1 - x0) + 2 * pad, abs(y1 - y0) + 2 * pad
    layer = Image.new("RGBA", (max(lw, 4), max(lh, 4)), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    ox, oy = min(x0, x1), min(y0, y1)
    n = 14
    pts = []
    for i in range(n):
        t = i / (n - 1)
        px = x0 + (x1 - x0) * t
        py = y0 + (y1 - y0) * t + 10 * math.sin(math.pi * t) + rng.uniform(-1.5, 1.5)
        pts.append((px - ox + pad, py - oy + pad))
    d.line(pts, fill=(*KEEPER_INK_RGB, 200), width=2, joint="curve")
    return layer, ox - pad, oy - pad, pts


# ------------------------------------------------------------------ cluster


class MarginStudy:
    """One margin-study CLUSTER: 1-3 quick pencil studies of a detail already
    present in the spread's own art (never invented), each swept-reveal along
    a diagonal front, an optional leader line pointing back at the studied
    detail, and an optional short Keeper caption. Governors (<=1 cluster,
    2-3 studies, per episode) are the caller's responsibility -- this class
    draws exactly ONE cluster, whatever it's given."""

    def __init__(self, source_crop: Image.Image, studies: list[dict],
                 leader: dict | None = None, caption=None,
                 contrast: float = CONTRAST_DEFAULT):
        """
        source_crop: the ALREADY-CROPPED region of the spread's own approved
            art the studies are drawn from (e.g. `still.crop(lamp_box)`).
        studies: list of dicts, one per study --
            {"out_w": int, "seed": int, "pos": (x, y), "t0": float,
             "dur": float, "contrast": float (optional, overrides cluster
             default)}. `pos` is the absolute frame pixel top-left the
             rendered study is composited at.
        leader: optional {"from_study": index, "to_xy": (x, y), "seed": int,
            "t0": float, "dur": float} -- draws from the given study's top
            edge toward `to_xy` (the studied detail's own position), revealed
            upward as `dur` elapses, matching the approved POC's "draws
            toward the lamp" direction.
        caption: optional `keeper_hand.KeeperEntry` (LAW 2 stays enforced by
            that class itself) -- composited after the studies/leader.
        """
        self.contrast = contrast
        self._rendered = []
        for s in studies:
            img = pencil_study(source_crop, s["out_w"], s["seed"],
                                contrast=s.get("contrast", contrast))
            self._rendered.append(dict(s, image=img))

        self.leader = leader
        self._leader_layer = None
        if leader is not None:
            from_study = self._rendered[leader["from_study"]]
            p0 = (from_study["pos"][0] + from_study["image"].width // 2,
                  from_study["pos"][1] + 6)
            self._leader_layer = leader_layer(p0, leader["to_xy"], leader["seed"])

        self.caption = caption

    def compose(self, frame: Image.Image, t: float) -> Image.Image:
        out = frame.convert("RGBA")
        for s in self._rendered:
            frac = _clamp01((t - s["t0"]) / max(1e-6, s["dur"]))
            if frac > 0:
                out.alpha_composite(sweep_reveal(s["image"], frac), s["pos"])
        if self._leader_layer is not None and t >= self.leader["t0"]:
            fl = _clamp01((t - self.leader["t0"]) / max(1e-6, self.leader["dur"]))
            layer, lx, ly, _pts = self._leader_layer
            l = layer.copy()
            if fl < 1.0:
                a = np.asarray(l.split()[3], dtype=np.float32)
                cut = int(a.shape[0] * (1 - fl))
                a[:cut, :] = 0   # draws upward toward the studied detail
                l.putalpha(Image.fromarray(a.astype(np.uint8)))
            out.alpha_composite(l, (lx, ly))
        out = out.convert("RGB")
        if self.caption is not None:
            out = self.caption.compose(out, t)
        return out

    def foley_cues(self):
        """Soft `graphite_scratch` under each reveal, plus the caption's own
        cues if a caption was given. `graphite_scratch` is a NEW cue key not
        yet present in `scriptorium_foley.py`'s DEVICE_SOUND_MAP (see this
        engine's SKILL.md) -- exported here so the mapping work is a single
        drop-in addition, not a re-audit of every caller."""
        cues = [("graphite_scratch", s["t0"], s["dur"]) for s in self._rendered]
        if self.caption is not None:
            cues += self.caption.foley_cues()
        return cues


# ---------------------------------------------------------------------- demo


def _render(name: str, frame_fn, dur: float, outdir: Path):
    work = outdir / f"_{name}_work"
    if work.exists():
        shutil.rmtree(work)
    work.mkdir(parents=True)
    n = int(dur * FPS)
    for i in range(n):
        frame_fn(i / FPS).save(work / f"f{i:05d}.png")
    out = outdir / f"{name}.mp4"
    subprocess.run(["ffmpeg", "-y", "-framerate", str(FPS), "-i", str(work / "f%05d.png"),
                    "-c:v", "libx264", "-pix_fmt", "yuv420p", str(out)],
                   check=True, capture_output=True)
    shutil.rmtree(work)
    print(f"[ok] {out}")


def render_demo(still: Path, out_mp4: Path, duration: float):
    sys.path.insert(0, str(HERE))
    import keeper_hand as K

    base = scale_crop(Image.open(still).convert("RGB"), W, H)
    lamp_box = (int(W * 0.185), int(H * 0.435), int(W * 0.415), int(H * 0.565))
    crop = base.crop(lamp_box)
    cluster = MarginStudy(
        source_crop=crop,
        studies=[
            {"out_w": 240, "seed": 7, "pos": (int(W * 0.10), int(H * 0.878)), "t0": 0.5, "dur": 0.7},
            {"out_w": 210, "seed": 8, "pos": (int(W * 0.34), int(H * 0.892)), "t0": 1.6, "dur": 0.7},
        ],
        leader={"from_study": 1, "to_xy": (int(W * 0.315), int(H * 0.56)),
                "seed": 9, "t0": 2.6, "dur": 0.4},
        caption=K.KeeperEntry(["still burning."], origin=(int(W * 0.55), int(H * 0.908)),
                               size=56, energy=0.25, seed=43, t0=3.1, dur=0.9),
    )
    _render(out_mp4.stem, lambda t: cluster.compose(base, t), duration, out_mp4.parent)


# ------------------------------------------------------------------ selftest


def run_selftests() -> int:
    ok = True

    def check(cond, label):
        nonlocal ok
        print(f"  {'PASS' if cond else 'FAIL'}  {label}")
        ok = ok and cond

    src = Image.new("RGB", (300, 300), (150, 130, 100))
    d = ImageDraw.Draw(src)
    d.ellipse([80, 80, 220, 220], fill=(40, 30, 20))

    # 1. default contrast is the LAW 2 / v6.1 value, not the old POC default
    check(CONTRAST_DEFAULT == 2.6, f"default contrast is 2.6 (v6.1), got {CONTRAST_DEFAULT}")

    # 2. sweep_reveal(frac=0) is fully transparent, frac=1 is unchanged
    study = pencil_study(src, 120, seed=1)
    revealed_none = sweep_reveal(study, 0.0)
    revealed_full = sweep_reveal(study, 1.0)
    a0 = np.asarray(revealed_none.split()[3])
    check(int(a0.max()) == 0, "sweep_reveal(frac=0.0) is fully transparent")
    check(revealed_full is study, "sweep_reveal(frac=1.0) returns the study unchanged")

    # 3. cluster composes without error and changes pixels once a study is due
    base = Image.new("RGB", (W, H), (238, 226, 194))
    cluster = MarginStudy(
        source_crop=src,
        studies=[{"out_w": 120, "seed": 1, "pos": (400, 1000), "t0": 0.5, "dur": 0.5}],
    )
    before = np.asarray(cluster.compose(base, 0.0))
    after = np.asarray(cluster.compose(base, 1.0))
    check(np.array_equal(before, np.asarray(base)), "before t0, frame is unchanged")
    check(not np.array_equal(after, np.asarray(base)), "after t0+dur, frame has the study composited")

    # 4. foley cue export
    cues = cluster.foley_cues()
    check(cues == [("graphite_scratch", 0.5, 0.5)], f"foley_cues() exports the reveal window: {cues}")

    print(f"\n{'ALL PASS' if ok else 'FAILURES ABOVE'}")
    return 0 if ok else 1


# -------------------------------------------------------------------- CLI


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--demo", action="store_true", help="render a demo clip from a still")
    ap.add_argument("--still", help="source still (--demo mode)")
    ap.add_argument("--out", help="output mp4 (--demo mode)")
    ap.add_argument("--duration", type=float, default=5.0, help="--demo clip length, seconds")
    ap.add_argument("--selftest", action="store_true", help="run the engine self-tests")
    a = ap.parse_args()

    if a.selftest:
        raise SystemExit(run_selftests())
    if a.demo:
        if not a.still or not a.out:
            ap.error("--demo requires --still and --out")
        render_demo(Path(a.still), Path(a.out), a.duration)
    else:
        ap.print_help()
