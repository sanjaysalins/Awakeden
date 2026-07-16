"""Animate the 5 paid hero clips for the Bronze Serpent graphic-novel rebuild
(2026-07-16) via HF Kling3.0 "living light" prompts (figures FROZEN, only light/
air move -- the proven pattern from sfx_pilots/fx_pilot_kling_living_light.py).
16:9, $0.65/clip via _hf_animate_short.hf_animate (gated: budget ceiling + still
PASS check -- JITB_SKIP_STILL_GATE=1 since these stills were eye-audited by the
agent directly, not through the render_lint sidecar pipeline, per the project's
own "look yourself" standing rule)."""
import os
import sys
from pathlib import Path

os.environ.setdefault("JITB_SKIP_STILL_GATE", "1")
ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT))
from _hf_animate_short import hf_animate  # noqa: E402

OUT = Path(__file__).resolve().parent / "v1" / "visual_16x9_inked"
CLIPS = OUT / "clips"
CLIPS.mkdir(exist_ok=True)

FROZEN = ("Every figure stays perfectly frozen the entire time -- no limbs move, no heads "
          "turn, no faces change, no morphing, no new figures, hands or objects appear. "
          "INVENT NOTHING: show only what is already painted in this exact image. ")

CLIPS_TO_RENDER = [
    ("01_snakebite",
     "A still finished inked graphic-novel illustration on flat canvas, filmed as ONE slow, "
     "steady push-in across the wilderness camp. " + FROZEN +
     "ONLY the light and the air are alive: heat-shimmer rises faintly off the sun-baked "
     "rock, fine dust drifts on the wind, and the tent cloth and robes stir almost "
     "imperceptibly."),
    ("07_make_a_fiery_serpent_set_it_on_a_pole",
     "A still finished inked graphic-novel illustration on flat canvas, filmed as ONE slow, "
     "steady push-in toward Moses and the bronze serpent. " + FROZEN +
     "ONLY the light and the fire are alive: the forge-fire glows and pulses warm over the "
     "bronze, embers drift upward, a thin thread of smoke curls, and the still metal "
     "catches the firelight."),
    ("08_raised",
     "A still finished inked graphic-novel illustration on flat canvas, filmed as ONE very "
     "slow, steady push-in toward the lifted bronze serpent on its pole. " + FROZEN +
     "ONLY the light and the sky are alive: heat-haze and fine dust rise past the still "
     "bronze, low cloud drifts slowly behind the pole, and robes stir faintly far below -- "
     "the bronze serpent itself stays perfectly still."),
    ("12_even_so_must_the_son_of_man_be_lifted_up",
     "A still finished inked graphic-novel illustration on flat canvas, filmed as ONE slow, "
     "steady push-in toward the centre of the frame, holding both the bronze serpent and "
     "the crucified Christ in view. " + FROZEN +
     "ONLY the light is alive: warm light pulses gently across the cross, heat-haze drifts "
     "past the still bronze serpent, and slow cloud and fine dust motes drift through the "
     "scene."),
    ("21_look_to_the_one_lifted_up_hero_close",
     "A still finished inked graphic-novel illustration on flat canvas, filmed as ONE very "
     "slow, gentle push-in toward the risen Christ's face and outstretched hand, keeping "
     "the same gentle expression the whole time -- his eyes, brow and mouth never shift, "
     "harden or blink. The small nail-wound scar on his open palm stays EXACTLY as "
     "painted, dry and still -- no blood flows, drips, spreads, brightens or grows. "
     + FROZEN +
     "ONLY the light is alive: the warm golden radiance behind him glows and breathes "
     "gently brighter and dimmer, and his robe and hair stir almost imperceptibly."),
    ("15_hezekiah_breaks_the_brazen_serpent",
     "A still finished inked graphic-novel illustration on flat canvas, filmed as ONE slow, "
     "steady push-in toward the king and the shattering bronze serpent, holding the maul "
     "already mid-strike exactly as painted -- the king's pose, arms and the maul NEVER "
     "move or swing, no new motion of the strike itself. " + FROZEN +
     "ONLY the light, dust and smoke are alive: fine stone dust and small bronze fragments "
     "already shown drift and settle slowly through the air, the thin haze of incense curls "
     "and thins, and a shaft of temple light glows and breathes gently across the scene."),
]


def main():
    ok = fail = 0
    for slug, prompt in CLIPS_TO_RENDER:
        png = OUT / f"{slug}.png"
        out = CLIPS / f"{slug}.mp4"
        if out.exists() and out.stat().st_size > 0:
            print(f"[skip] {slug}: already rendered")
            continue
        if not png.exists():
            print(f"[FAIL] {slug}: missing still {png}")
            fail += 1
            continue
        print(f"[clip] {slug}: rendering (Kling pro 5s 16:9) ...", flush=True)
        success = hf_animate(png, out, prompt, duration=5, aspect_ratio="16:9")
        if success:
            print(f"       ok -> {out}")
            ok += 1
        else:
            print(f"       FAILED (no fallback for this test)")
            fail += 1
    print(f"\n[done] {ok} animated, {fail} failed")


if __name__ == "__main__":
    main()
