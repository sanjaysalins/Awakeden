"""Round 6 REGRESSION build ($0, deterministic) -- the panel's mandatory
check (`poc_living_sketchbook/_FABLE_ROUND6_THE_KEEPER.md`, build order
step 1): every generalized engine must re-render the EXACT approved POC
clips, same seeds/params, side by side against the untouched originals, for
the user's own eye-check. "Looks similar on fresh demos" does not count as
"matches what was approved."

This script does NOT modify any POC script, any original .mp4, or any
existing skill. It only READS the approved POCs' own helper functions
(`_build_vault.scribed_verse_layer` for the Word's own Scribed Ink register,
which the new engines deliberately never letter -- LAW 1) and copies each
original clip byte-for-byte into this folder, alongside a freshly rendered
`_ENGINE.mp4` twin built ONLY from the five promoted `panel_animator`
engines.

Pairs covered (the panel's list):
  keeper_A_panic_entry   (_keeper_poc)      -> keeper_hand.KeeperEntry
  keeper_B_calm_line     (_keeper_poc)      -> keeper_hand.KeeperEntry
  vault_1_word_whole     (_vault_poc)       -> keeper_hand.KeeperEntry(interrupt_at=...)
                                                + _build_vault.scribed_verse_layer (unmodified, read-only)
  vault_4_inkwell        (_vault_poc)       -> keeper_hand.KeeperEntry(starve=...)
  bold_2_torn_page       (_bold_poc)        -> page_transitions.TornOutPage
  bold_3_bleed           (_bold_poc)        -> keeper_hand.KeeperEntry + bleeding_word.{locate_word,BleedingWord}
  v2_05_candle_only      (_vault2_poc)      -> candle_only.apply_candle

    ..\\..\\..\\.venv\\Scripts\\python.exe _build_regression.py
"""
import math
import random
import shutil
import subprocess
import sys
from pathlib import Path

from PIL import Image

HERE = Path(__file__).resolve().parent
STORM = HERE.parent
REPO = STORM.parents[1]

sys.path.insert(0, str(REPO / "panel_animator"))
from raking_light import scale_crop  # noqa: E402
import keeper_hand as KH  # noqa: E402
import margin_study  # noqa: E402  (imported for completeness; no regression pair needs it directly)
import page_transitions as PT  # noqa: E402
import bleeding_word as BW  # noqa: E402
import candle_only as CO  # noqa: E402

sys.path.insert(0, str(STORM / "_vault_poc"))
import _build_vault as V  # noqa: E402  -- READ-ONLY reuse of scribed_verse_layer (the Word's own register)

FPS = 30
W, H = 1080, 1920
STILLS = STORM / "stills"

PAIRS = [
    ("keeper_A_panic_entry", STORM / "_keeper_poc" / "keeper_A_panic_entry.mp4"),
    ("keeper_B_calm_line", STORM / "_keeper_poc" / "keeper_B_calm_line.mp4"),
    ("vault_1_word_whole", STORM / "_vault_poc" / "vault_1_word_whole.mp4"),
    ("vault_4_inkwell", STORM / "_vault_poc" / "vault_4_inkwell.mp4"),
    ("bold_2_torn_page", STORM / "_bold_poc" / "bold_2_torn_page.mp4"),
    ("bold_3_bleed", STORM / "_bold_poc" / "bold_3_bleed.mp4"),
    ("v2_05_candle_only", STORM / "_vault2_poc" / "v2_05_candle_only.mp4"),
]


def _render(name: str, frame_fn, dur: float):
    work = HERE / f"_{name}_work"
    if work.exists():
        shutil.rmtree(work)
    work.mkdir(parents=True)
    n = int(dur * FPS)
    for i in range(n):
        frame_fn(i / FPS).save(work / f"f{i:05d}.png")
    out = HERE / f"{name}_ENGINE.mp4"
    subprocess.run(["ffmpeg", "-y", "-framerate", str(FPS), "-i", str(work / "f%05d.png"),
                    "-c:v", "libx264", "-pix_fmt", "yuv420p", str(out)],
                   check=True, capture_output=True)
    shutil.rmtree(work)
    print(f"[ok] {out}")


def _copy_original(name: str, src: Path):
    dst = HERE / f"{name}_ORIGINAL.mp4"
    shutil.copy2(src, dst)
    print(f"[ok] {dst}  (copy of {src})")


# --------------------------------------------------------------- keeper_A


def build_keeper_A():
    base = scale_crop(Image.open(STILLS / "s01_waves.png").convert("RGB"), W, H)
    entry = KH.KeeperEntry(
        [("~~storm~~ ~~wind~~ fear.", 0, 0), ("water at our knees", 40, 100)],
        origin=(int(W * 0.36), int(H * 0.878)), size=64, energy=0.85, seed=41,
        t0=0.6, dur=2.6, skid=True)
    _render("keeper_A_panic_entry", lambda t: entry.compose(base, t), 5.0)


# --------------------------------------------------------------- keeper_B


def build_keeper_B():
    base = scale_crop(Image.open(STILLS / "s10_calm.png").convert("RGB"), W, H)
    entry = KH.KeeperEntry(
        ["not a breath of wind. not one."],
        origin=(int(W * 0.09), int(H * 0.050)), size=64, energy=0.08, seed=42,
        t0=0.8, dur=2.4)
    _render("keeper_B_calm_line", lambda t: entry.compose(base, t), 5.0)


# --------------------------------------------------------------- vault_1


def build_vault_1():
    base = scale_crop(Image.open(STILLS / "s09_rebuke.png").convert("RGB"), W, H)
    T_WORD = 3.0
    entry = KH.KeeperEntry(
        ["we woke him. someone screamed"],
        origin=(int(W * 0.08), int(H * 0.930)), size=60, energy=0.8, seed=71,
        t0=0.7, dur=3.4, interrupt_at=T_WORD)
    # The Word itself is NOT lettered by keeper_hand (LAW 1) -- reuse the
    # approved POC's own Scribed Ink verse layer, unmodified, exactly as the
    # original caller composited it: no reveal, simply there at T_WORD.
    verse = V.scribed_verse_layer("Peace, be still.", "MARK 4:39", size=62, seed=12, bold=True)

    def frame(t):
        out = entry.compose(base, t).convert("RGBA")
        if t >= T_WORD:
            out.alpha_composite(verse, (0, int(H * 0.006)))
        return out.convert("RGB")

    _render("vault_1_word_whole", frame, 5.5)


# --------------------------------------------------------------- vault_4


def build_vault_4():
    # The POC is TWO entries (a line that starves and dies; a separate darker
    # resume at an AUTHORED 3.3s), not one two-line entry -- modeling it as one
    # entry starved the WRONG line ("coming." instead of "the") and compressed
    # every beat. Structure is part of what the user approved; mirror it.
    base = scale_crop(Image.open(STILLS / "s02_water.png").convert("RGB"), W, H)
    line1_origin = (int(W * 0.06), int(H * 0.008))
    line2_origin = (int(W * 0.13), int(H * 0.044))
    blot_xy = (int(W * 0.115), int(H * 0.049))
    e1 = KH.KeeperEntry([("we bailed and bailed and the", 0, 0)],
                        origin=line1_origin, size=54, energy=0.6, seed=91,
                        t0=0.5, dur=1.9, starve=(5, blot_xy))
    e2 = KH.KeeperEntry([("water kept coming.", 0, 0)],
                        origin=line2_origin, size=54, energy=0.6, seed=92,
                        t0=3.3, dur=1.3)
    # residual, documented: the engine fires the blot at driest-glyph+0.15
    # (~2.55) where the POC authored 3.0 -- a ~0.45s earlier dot, nothing else.
    _render("vault_4_inkwell", lambda t: e2.compose(e1.compose(base, t), t), 6.0)


# --------------------------------------------------------------- bold_2


def build_bold_2():
    above = scale_crop(Image.open(STILLS / "s03_screaming.png").convert("RGB"), W, H)
    below = scale_crop(Image.open(STILLS / "s04_asleep.png").convert("RGB"), W, H)
    tr = PT.TornOutPage(above, below, grab_t=0.9, rip_t=1.5, gone_t=1.95, seed=13)
    _render("bold_2_torn_page", lambda t: tr.compose(t), 4.5)


# --------------------------------------------------------------- bold_3


def build_bold_3():
    base = scale_crop(Image.open(STILLS / "s01_waves.png").convert("RGB"), W, H)
    entry = KH.KeeperEntry(
        [("~~storm~~ ~~wind~~ fear.", 0, 0), ("water at our knees", 40, 100)],
        origin=(int(W * 0.36), int(H * 0.878)), size=64, energy=0.85, seed=41,
        t0=0.5, dur=2.2, skid=True)
    cx, cy = BW.locate_word(entry, line_index=0, word="fear.")
    bleed = BW.BleedingWord(cx, cy, drop_t=3.2, seed=21)

    def frame(t):
        out = entry.compose(base, t)
        return bleed.compose(out, t)

    _render("bold_3_bleed", frame, 5.5)


# --------------------------------------------------------------- v2_05


def build_v2_05():
    """apply_candle() takes ANY R(t) callable -- reproduce the approved POC's
    own hand-authored 4-phase curve (hold / ease-down / FLICKER-ONLY-IN-THE-
    FLAT-MIDDLE / ease-up) exactly, rather than the module's generic
    radius_from_keyframes()+flicker_R() composition (which would flicker
    across the ease phases too -- a real, honestly-disclosed difference, see
    the regression report)."""
    base = scale_crop(Image.open(STILLS / "s04_asleep.png").convert("RGB"), W, H)
    LAMP = (W * 0.295, H * 0.495)
    rng = random.Random(51)
    flick = [rng.uniform(-1, 1) for _ in range(400)]

    def ss(u):
        u = min(1.0, max(0.0, u))
        return u * u * u * (u * (u * 6 - 15) + 10)

    def R_of(t):
        if t < 0.8:
            return 3000.0
        if t < 2.4:
            return 3000.0 - (3000.0 - 330.0) * ss((t - 0.8) / 1.6)
        if t < 5.2:
            f = flick[int(t * 12) % 400] * 0.5 + flick[int(t * 5) % 400] * 0.5
            return 330.0 + 10.0 * f
        return 330.0 + (950.0 - 330.0) * ss((t - 5.2) / 1.6)

    _render("v2_05_candle_only", lambda t: CO.apply_candle(base, t, LAMP, R_of), 7.5)


if __name__ == "__main__":
    build_keeper_A()
    build_keeper_B()
    build_vault_1()
    build_vault_4()
    build_bold_2()
    build_bold_3()
    build_v2_05()
    for name, src in PAIRS:
        _copy_original(name, src)
    print("REGRESSION_BUILD_DONE")
