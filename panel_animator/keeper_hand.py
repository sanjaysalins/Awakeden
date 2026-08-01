#!/usr/bin/env python
"""Keeper's Hand -- the flagship instrument (Round 6 promotion, panel-revised
2026-07-30, `poc_living_sketchbook/_FABLE_ROUND6_THE_KEEPER.md` build card 1).
Promotes `poc_living_sketchbook/storm/_keeper_poc/_build_poc.py`'s
`entry_events`/`keeper_line`/`compose_at` (the Performing Handwriting + Field
Header + Two Hands) plus `poc_living_sketchbook/storm/_vault_poc/_build_vault.py`
poc_1 (Word Arrives Whole -- interrupt) and poc_4 (Inkwell Runs Dry -- starve +
re-dip blot) into ONE reusable engine: a single human hand, one authored energy
number away from calm or panicked, writing into the sketchbook margin.

THE TWO LAWS (the round doc, read there for the full rationale):
  LAW 1 -- the asymmetry of the Word. The Keeper's ink shakes, heaves, gets
    struck through, skids, and starves. The WORD does none of these -- and
    this engine never letters the Word at all. `interrupt_at` is LAW 1's
    enforcement mechanism here: any glyph/strike/skid/blot event scheduled at
    or after that time simply never fires, forever -- the hand stops, and
    whatever arrives after (a Scribed Ink verse card, composited by the
    CALLER, elsewhere) does so complete between one frame and the next, with
    zero reveal choreography from this module.
  LAW 2 -- the scale law. Keeper-hand text is BIG and BOLD: >=54px at
    1080-width (56-64 standard), always with extra stroke weight (`BOLD = 1`,
    always on -- there is no caller option to turn it off). Passing
    `size < MIN_SIZE` is allowed (never silently ignored) but PRINTS A
    WARNING and clamps up to the floor: "if a mark is worth making, it is
    worth SEEING."

PRODUCTION ENERGY SOURCE (panel-corrected 2026-07-30 -- do not relitigate):
`energy` is an AUTHORED number per entry, hand-set in the episode's beat table
exactly as the taste-gated POCs did (0.85 panic / 0.08 calm were hand-set, and
that is what the user approved). `held_breath.py`'s `energy(t)` is a SILENCE
damper for the AUDIO layer only and must NEVER drive this module -- wiring it
here would calm the hand mid-scream. A derived "fear envelope" is a possible
future device with its own POC and gate, not part of this promotion.

API:
    from keeper_hand import KeeperEntry, field_header

    entry = KeeperEntry(
        lines=[("~~storm~~ ~~wind~~ fear.", 0, 0), ("water at our knees", 40, 100)],
        origin=(int(1080 * 0.36), int(1920 * 0.878)), size=64, energy=0.85,
        seed=41, t0=0.6, dur=2.6, skid=True)
    frame = entry.compose(frame, t)     # call every frame, t = seconds since the clip's own t=0
    cues = entry.foley_cues()           # [(device_key, start, duration), ...] -- scriptorium_foley.py keys

`starve=(n_glyphs, blot_xy)`: the last `n_glyphs` glyphs of the LAST line in
`lines` fade out along `starve_falloff()` (the Inkwell Runs Dry curve), then a
growing re-dip blot is drawn at `blot_xy` (absolute frame pixel coords) after
a short dead-air pause, before any further lines resume writing.

`interrupt_at=t`: no glyph/strike/skid/blot event at or after this absolute
time ever fires -- once interrupted, `compose()` returns a byte-identical
frame for every `t` beyond it (LAW 1's "it arrives whole" / "the hand simply
stops", both sides of the same instant).

`field_header(text)`: the Field Header preset (energy 0.15, size 60, top
lane) -- "the episode as an ENTRY," matching the approved POC's keeper_D
framing.

Moving clips (Two Hands at Once): `compose()` is already per-frame -- an
assembler runs it over a real clip's own frames exactly like any other
panel_animator `apply_*` function (see keeper_C in the demo below, or vault2
poc_11 in the reference POCs). Governor: plan lanes against the CLIP's own
motion, not just frame 0 -- check the filmstrip before locking an origin.

Voice governor (Round 6, not enforced by this module -- an episode-design
rule): the Keeper's words are a human voice, questions/observations only,
reviewed with the narration by the panel, never doctrine claims, never
competing with a verse card on the same spread. <=1 entry per spread, <=4
entries + 1 header per episode: it is a journal, not subtitles. The
deterministic half of this governor (entry counts, lane safety, verse-card
collisions, and a doctrine-keyword flag for the panel) is enforced by the
sibling script `keeper_lint.py` (repo root) over an episode's keeper-entry
manifest -- run it before any episode lock.

Usage (CLI):
    .venv\\Scripts\\python.exe panel_animator\\keeper_hand.py --demo --still <still.png> --out demo.mp4 --duration 5
    .venv\\Scripts\\python.exe panel_animator\\keeper_hand.py --selftest
"""
from __future__ import annotations

import argparse
import math
import random
import shutil
import subprocess
import sys
import warnings
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from raking_light import scale_crop  # noqa: E402 -- reuse, don't duplicate (hard rule)

FPS = 30
W, H = 1080, 1920                             # this project's standard canvas
F_KEEPER = "C:/Windows/Fonts/Inkfree.ttf"      # quick pencil hand -- NOT Kunstler (the Word's register)
KEEPER_INK = (72, 64, 54)                      # graphite-iron, a working pencil-pen
BOLD = 1                                       # LAW 2: always on, not a caller option
MIN_SIZE = 54                                  # LAW 2 floor, 1080-width reference

STARVE_MAX_ALPHA = 200
STARVE_MIN_ALPHA = 38
STARVE_GAMMA = 1.283            # power-law fit (see starve_falloff() docstring)
STARVE_PAUSE_S = 0.55           # dead-air after the driest glyph before writing resumes
BLOT_COLOR = (48, 40, 34)
BLOT_R0, BLOT_R1 = 4.0, 10.0    # growing blot radius, px
BLOT_DUR = 0.4


# --------------------------------------------------------------- falloff math


def starve_falloff(k: int, n: int) -> int:
    """The Inkwell Runs Dry alpha curve. Glyph k of n starving glyphs (k=0 is
    the FIRST to starve, k=n-1 the last/driest). Power-law fit (gamma=1.283)
    to the approved POC's hand-authored table
    (`poc_living_sketchbook/storm/_vault_poc/_build_vault.py` poc_4:
    `[200, 150, 105, 65, 38]` at n=5) -- reproduces those five values within
    rounding and generalizes to any n. A slow start that accelerates into the
    dry cliff, not a straight ramp -- matches the POC comment "alpha falls
    off a cliff." STRICTLY decreasing in k for n>1 (self-tested)."""
    if n <= 1:
        u = 1.0
    else:
        u = k / (n - 1)
    a = STARVE_MIN_ALPHA + (STARVE_MAX_ALPHA - STARVE_MIN_ALPHA) * (1.0 - u) ** STARVE_GAMMA
    return int(round(a))


def _smootherstep(t: float) -> float:
    t = min(1.0, max(0.0, t))
    return t * t * t * (t * (t * 6 - 15) + 10)


# --------------------------------------------------------- the hand (private)


def _energy_params(e: float) -> dict:
    """ONE mapping from story energy (0 calm .. 1 panic) to how the hand
    behaves -- unchanged from the approved POC. This is the whole device: the
    same hand, differently afraid."""
    return dict(
        jit_y=0.6 + 5.0 * e,
        jit_rot=0.8 + 4.5 * e,
        drift_amp=2.0 + 15.0 * e,
        rot_bias=-2.2 * e,
        gap_sigma=0.15 + 0.85 * e,
        pressure=1 if e > 0.55 else 0,
    )


def _keeper_line(text: str, size: int, energy: float, seed: int):
    """Layout one line of the Keeper's Hand. `~~word~~` marks a struck word.
    Returns (glyphs, strikes, width): glyphs [(layer, dx, dy)] in draw order;
    strikes [(after_glyph_idx, x0, x1, y)] wobbly strike segments.
    Coordinates are relative to the line's left/baseline-top origin.
    Unchanged from the approved POC (`_keeper_poc/_build_poc.py`)."""
    p = _energy_params(energy)
    rng = random.Random(seed)
    font = ImageFont.truetype(F_KEEPER, size)
    probe = ImageDraw.Draw(Image.new("RGB", (8, 8)))

    tokens = []
    for raw in text.split():
        if raw.startswith("~~") and raw.endswith("~~") and len(raw) > 4:
            tokens.append((raw[2:-2], True))
        else:
            tokens.append((raw, False))

    glyphs, strikes = [], []
    x = 0.0
    drift_phase = rng.uniform(0, 2 * math.pi)
    space_w = probe.textlength(" ", font=font)
    total_w = sum(probe.textlength(w, font=font) for w, _ in tokens) \
        + space_w * (len(tokens) - 1)

    for word, struck in tokens:
        wx0 = x
        for ch in word:
            cw = probe.textlength(ch, font=font)
            frac = x / max(1.0, total_w)
            drift = p["drift_amp"] * math.sin(2 * math.pi * 1.3 * frac + drift_phase)
            jy = drift + rng.uniform(-p["jit_y"], p["jit_y"])
            jr = p["rot_bias"] + rng.uniform(-p["jit_rot"], p["jit_rot"])
            layer = Image.new("RGBA", (int(size * 2.2), int(size * 2.4)), (0, 0, 0, 0))
            d = ImageDraw.Draw(layer)
            d.text((12, 12), ch, font=font, fill=(*KEEPER_INK, 225),
                   stroke_width=p["pressure"] + BOLD, stroke_fill=(*KEEPER_INK, 225))
            layer = layer.rotate(jr, resample=Image.BICUBIC, center=(12, 12 + size * 0.55))
            glyphs.append((layer, int(x) - 12, int(jy) - 12))
            x += cw
        if struck:
            ymid = size * 0.55 + p["drift_amp"] * math.sin(
                2 * math.pi * 1.3 * (wx0 / max(1.0, total_w)) + drift_phase)
            strikes.append((len(glyphs) - 1, wx0 - 2, x + 2, ymid))
        x += space_w
    return glyphs, strikes, x - space_w


def _strike_layer(x0: float, x1: float, y: float, seed: int, width: int = 3):
    """A wobbly hand strike across [x0,x1] at height y (line-local coords).
    Unchanged from the approved POC."""
    rng = random.Random(seed)
    pad = 8
    lw = int(x1 - x0) + 2 * pad
    layer = Image.new("RGBA", (lw, 40), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    pts = []
    n = max(6, lw // 14)
    for i in range(n):
        t = i / (n - 1)
        pts.append((pad + t * (x1 - x0),
                    20 + rng.uniform(-2.5, 2.5) + 3.0 * math.sin(math.pi * t)))
    d.line(pts, fill=(*KEEPER_INK, 235), width=width, joint="curve")
    return layer, int(x0) - pad, int(y) - 20


def _skid_layer(size: int, seed: int):
    """The interrupted stroke: ink skidding away as something hits the desk.
    Unchanged from the approved POC."""
    rng = random.Random(seed)
    layer = Image.new("RGBA", (240, 160), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    x, y = 10.0, 30.0
    vx, vy = 6.0, 1.5
    pts = [(x, y)]
    for i in range(16):
        vx *= 1.13
        vy += rng.uniform(0.4, 1.3)
        x += vx
        y += vy + rng.uniform(-1.5, 1.5)
        pts.append((x, y))
    for i in range(len(pts) - 1):
        wdt = max(1, int(4 * (1 - i / len(pts))))
        d.line([pts[i], pts[i + 1]], fill=(*KEEPER_INK, 210), width=wdt)
    return layer


# ------------------------------------------------------------------ KeeperEntry


class KeeperEntry:
    """One Keeper's-hand journal entry: one or more lines, one seed, one
    AUTHORED energy. Lays itself out once at construction (deterministic);
    `compose(frame, t)` is a pure per-frame read of that layout, called every
    frame like any other panel_animator `apply_*` function."""

    def __init__(self, lines, origin, size: int = 64, energy: float = 0.5,
                 seed: int = 0, t0: float = 0.0, dur: float | None = None,
                 skid: bool = False, starve=None, interrupt_at: float | None = None,
                 starve_pause: float | None = None):
        """
        lines: list of str, OR list of (text, dx, dy) tuples for per-line
            offsets from `origin` (multi-line entries, e.g. keeper_A's two-
            line panic entry). `~~word~~` marks a struck word.
        origin: (x, y) absolute pixel coords, the FIRST line's left/baseline
            anchor.
        size: font px @ 1080-width. LAW 2 floor is MIN_SIZE (54) -- passing
            less WARNS and clamps up, never silently drops below it.
        energy: 0.0 (calm) .. 1.0 (panic), AUTHORED per entry -- see the
            module docstring's "production energy source" note.
        seed: deterministic layout/jitter seed. Multi-line entries reuse the
            approved POC's own convention: line index `li` nudges the seed
            (`seed + li`) so each line gets a related-but-distinct hand.
        t0: this entry's write-on start time, same seconds unit `compose(t)`
            receives.
        dur: total glyph/strike burst duration (seconds), EXCLUDING any
            starve pause. Defaults to a glyph-count/energy heuristic if None
            -- pass it explicitly to match an authored beat.
        skid: append the interrupted-stroke skid tail after the last glyph.
        starve: (n_glyphs, blot_xy) -- see module docstring.
        interrupt_at: absolute time; no event at or after it ever fires
            (LAW 1).
        starve_pause: seconds of dead air between the driest glyph and the
            resume (the pen lifts, dips, returns). None -> STARVE_PAUSE_S
            (0.55, the engine's auto value). The approved vault_4 POC used an
            AUTHORED 0.9s gap -- pass it explicitly to reproduce that clip
            (the regression drift the promotion round flagged; authored beats
            belong to the author, not the engine).
        """
        if size < MIN_SIZE:
            warnings.warn(
                f"KeeperEntry size={size} is below the LAW 2 floor ({MIN_SIZE}px "
                f"@ 1080-width) -- clamped up to {MIN_SIZE}. If a mark is worth "
                f"making, it is worth SEEING.", stacklevel=2)
            size = MIN_SIZE

        norm_lines = []
        for ln in lines:
            if isinstance(ln, str):
                norm_lines.append((ln, 0, 0))
            else:
                norm_lines.append(tuple(ln))
        if not norm_lines:
            raise ValueError("KeeperEntry needs at least one line")

        self.lines = norm_lines
        self.origin = origin
        self.size = size
        self.energy = energy
        self.seed = seed
        self.t0 = t0
        self.skid = skid
        self.starve = starve
        self.interrupt_at = interrupt_at
        self._starve_pause = STARVE_PAUSE_S if starve_pause is None else float(starve_pause)

        if dur is None:
            n_glyphs_est = sum(len(t.replace("~~", "").replace(" ", "")) for t, _, _ in norm_lines)
            dur = max(0.8, 0.075 * n_glyphs_est / (0.5 + 0.6 * energy))
        self.dur = dur

        self._events, self._layers = self._build()

    # ---------------------------------------------------------------- layout

    def _build(self):
        rng = random.Random(self.seed + 99)
        p = _energy_params(self.energy)
        layers: list[tuple[Image.Image, int, int]] = []
        order: list[int] = []          # indices into `layers`, in draw order
        ox, oy = self.origin
        line_glyph_positions: list[list[int]] = []   # per line: positions in `order` that are glyph events

        for li, (text, dx, dy) in enumerate(self.lines):
            glyphs, strikes, _w = _keeper_line(text, self.size, self.energy, self.seed + li)
            smap: dict[int, list] = {}
            for si, (after, x0, x1, y) in enumerate(strikes):
                smap.setdefault(after, []).append((x0, x1, y, si))
            this_line_positions = []
            for gi, (layer, gx, gy) in enumerate(glyphs):
                layers.append((layer, ox + dx + gx, oy + dy + gy))
                order.append(len(layers) - 1)
                this_line_positions.append(len(order) - 1)
                for (x0, x1, y, si) in smap.get(gi, []):
                    sl, sx, sy = _strike_layer(x0, x1, y, self.seed + 31 * li + si)
                    layers.append((sl, ox + dx + sx, oy + dy + sy))
                    order.append(len(layers) - 1)
            line_glyph_positions.append(this_line_positions)

        if self.skid and layers:
            last_layer, lx, ly = layers[-1]
            sk = _skid_layer(self.size, self.seed + 7)
            layers.append((sk, lx + last_layer.width - 20, ly + int(self.size * 0.35)))
            order.append(len(layers) - 1)

        # --- starve: fade the last n_glyphs of the LAST line, mark where the
        # blot's dead-air pause goes ---
        starve_last_order_pos = None
        if self.starve is not None:
            n_starve, _blot_xy = self.starve
            last_line_positions = line_glyph_positions[-1] if line_glyph_positions else []
            n_starve = max(0, min(n_starve, len(last_line_positions)))
            starved = last_line_positions[-n_starve:] if n_starve else []
            for k, pos in enumerate(starved):
                layer_idx = order[pos]
                layer, x, y = layers[layer_idx]
                a = starve_falloff(k, n_starve)
                layers[layer_idx] = (layer.point(lambda v, aa=a: min(v, aa) if v else 0), x, y)
            if starved:
                starve_last_order_pos = starved[-1]

        # --- bursty timing: same lognormal-gap algorithm as the approved
        # POC, generalized to splice the starve pause into the stream ---
        gaps = [rng.lognormvariate(0, p["gap_sigma"]) for _ in order]
        total = sum(gaps) if gaps else 1.0
        events, t = [], self.t0
        blot_time = None
        for i, (layer_idx, g) in enumerate(zip(order, gaps)):
            events.append((t, layer_idx))
            if starve_last_order_pos is not None and i == starve_last_order_pos:
                blot_time = t + 0.15   # the ink runs dry right as the driest glyph lands
                t += self._starve_pause  # the pen lifts, dips in the well, returns
            t += self.dur * g / total

        if self.interrupt_at is not None:
            events = [(et, idx) for (et, idx) in events if et < self.interrupt_at]
            if blot_time is not None and blot_time >= self.interrupt_at:
                blot_time = None       # LAW 1: the blot is hand activity too -- it stops as well

        self._blot_time = blot_time
        return events, layers

    # --------------------------------------------------------------- compose

    def compose(self, frame: Image.Image, t: float) -> Image.Image:
        """Composite this entry's state at time `t` onto `frame`. Byte-stable
        for any `t` at or beyond the last event (self-tested)."""
        out = frame.convert("RGBA")
        for et, idx in self._events:
            if t >= et:
                layer, x, y = self._layers[idx]
                out.alpha_composite(layer, (x, y))
            else:
                break   # events are stored in non-decreasing time order
        if self.starve is not None and self._blot_time is not None and t >= self._blot_time:
            out = self._draw_blot(out, t)
        return out.convert("RGB")

    def _draw_blot(self, out: Image.Image, t: float) -> Image.Image:
        _n_glyphs, (bx, by) = self.starve
        p = _smootherstep((t - self._blot_time) / BLOT_DUR)
        d = ImageDraw.Draw(out, "RGBA")
        r = BLOT_R0 + (BLOT_R1 - BLOT_R0) * p
        d.ellipse([bx - r, by - r, bx + r, by + r], fill=(*BLOT_COLOR, 205))
        d.ellipse([bx - r * 1.7, by - r * 1.7, bx + r * 1.7, by + r * 1.7],
                  outline=None, fill=(*BLOT_COLOR, int(35 * p)))
        return out

    # ----------------------------------------------------------------- foley

    def foley_cues(self):
        """This entry's foley schedule as (device_key, start, duration)
        triples, keyed to `scriptorium_foley.py`'s existing DEVICE_SOUND_MAP
        (`keeper_scratch` one-shot for the write window; starve additionally
        exports a `nib_scratch` dry-scratch under the starving tail and an
        `ink_drop` for the re-dip blot). Empty entries (interrupted before
        any event fires) export no cues."""
        if not self._events:
            return []
        t_start = self._events[0][0]
        t_end = self._events[-1][0]
        cues = [("keeper_scratch", t_start, max(0.05, t_end - t_start))]
        if self.starve is not None and self._blot_time is not None:
            dry_start = max(t_start, self._blot_time - self._starve_pause - 0.15)
            cues.append(("nib_scratch", dry_start, (self._blot_time - dry_start)))
            cues.append(("ink_drop", self._blot_time, BLOT_DUR))
        return cues


# ------------------------------------------------------------------- presets


def field_header(text: str, seed: int = 44, t0: float = 0.6, dur: float = 1.8,
                  w: int = W, h: int = H) -> KeeperEntry:
    """The Field Header preset (Round 6 KEEP): energy 0.15, size 60, top lane
    -- "the episode as an ENTRY." Matches the approved POC's keeper_D framing
    (`_keeper_poc/_build_poc.py` poc_D)."""
    origin = (int(w * 0.15), int(h * 0.014))
    return KeeperEntry([text], origin=origin, size=60, energy=0.15, seed=seed, t0=t0, dur=dur)


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
    im = scale_crop(Image.open(still).convert("RGB"), W, H)
    entry = KeeperEntry(
        [("~~storm~~ ~~wind~~ fear.", 0, 0), ("water at our knees", 40, 100)],
        origin=(int(W * 0.36), int(H * 0.878)), size=64, energy=0.85, seed=41,
        t0=0.6, dur=2.6, skid=True)
    header = field_header("Galilee. evening. crossing over.", t0=0.0, dur=1.6)

    def frame(t):
        out = header.compose(im, t)
        return entry.compose(out, t)

    _render(out_mp4.stem, frame, duration, out_mp4.parent)


# ------------------------------------------------------------------ selftest


def run_selftests() -> int:
    ok = True

    def check(cond, label):
        nonlocal ok
        print(f"  {'PASS' if cond else 'FAIL'}  {label}")
        ok = ok and cond

    # 1. jitter(0.85) > jitter(0.1) on measured glyph offsets
    text = "we bailed and bailed and the water kept coming."
    g_panic, _s, _w = _keeper_line(text, 64, 0.85, seed=1)
    g_calm, _s, _w = _keeper_line(text, 64, 0.10, seed=1)
    dy_panic = np.array([gy for (_l, _gx, gy) in g_panic], dtype=np.float64)
    dy_calm = np.array([gy for (_l, _gx, gy) in g_calm], dtype=np.float64)
    check(float(np.std(dy_panic)) > float(np.std(dy_calm)),
          f"jitter(0.85) std={np.std(dy_panic):.2f} > jitter(0.1) std={np.std(dy_calm):.2f}")

    # 2. byte-stable after the last event
    entry = KeeperEntry(["fear.", "water at our knees"], origin=(100, 100),
                         size=60, energy=0.7, seed=5, t0=0.0, dur=1.0)
    base = Image.new("RGB", (W, H), (238, 226, 194))
    last_t = entry._events[-1][0] if entry._events else 0.0
    frame_a = entry.compose(base, last_t + 5.0)
    frame_b = entry.compose(base, last_t + 50.0)
    check(np.array_equal(np.asarray(frame_a), np.asarray(frame_b)),
          "compose() is byte-stable long after the last event")

    # 3. starve alpha strictly decreasing
    n = 5
    curve = [starve_falloff(k, n) for k in range(n)]
    check(all(curve[i] > curve[i + 1] for i in range(n - 1)),
          f"starve_falloff strictly decreasing over n={n}: {curve}")
    check(curve[0] == STARVE_MAX_ALPHA and curve[-1] == STARVE_MIN_ALPHA,
          f"starve_falloff endpoints hit {STARVE_MAX_ALPHA}/{STARVE_MIN_ALPHA}: {curve}")
    print(f"        (reference POC table at n=5: [200, 150, 105, 65, 38] -> engine: {curve})")

    # 4. interrupt leaves trailing glyphs unrendered forever
    interrupted = KeeperEntry(
        ["we woke him. someone screamed"], origin=(100, 1700), size=60,
        energy=0.8, seed=71, t0=0.7, dur=3.4, interrupt_at=3.0)
    full = KeeperEntry(
        ["we woke him. someone screamed"], origin=(100, 1700), size=60,
        energy=0.8, seed=71, t0=0.7, dur=3.4)
    frame_int = interrupted.compose(base, 10.0)
    frame_full = full.compose(base, 10.0)
    check(not np.array_equal(np.asarray(frame_int), np.asarray(frame_full)),
          "interrupted entry renders FEWER glyphs than the uninterrupted twin, even at t=10")
    frame_int_at_cut = interrupted.compose(base, 3.0)
    frame_int_later = interrupted.compose(base, 20.0)
    check(np.array_equal(np.asarray(frame_int_at_cut), np.asarray(frame_int_later)),
          "interrupted entry is byte-identical from interrupt_at onward -- nothing fires after")

    # 5. LAW 2: size < MIN_SIZE warns and clamps
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        small = KeeperEntry(["too small."], origin=(100, 100), size=30, energy=0.2, seed=1)
    check(small.size == MIN_SIZE and any("LAW 2" in str(w.message) for w in caught),
          f"size=30 clamped to {MIN_SIZE} with a LAW 2 warning")

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
