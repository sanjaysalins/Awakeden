"""FX PILOT (2026-07-14, user-approved ~$1.20-2.00): can Kling carry the viral effects
natively — living light/atmosphere baked into the clip — instead of PIL/ffmpeg overlays?

3 test clips on women_first_witnesses_luke245 (angels reveal / landing / dawn), rendered
to visual/_fx_pilot/ so the piece's shipped hash-bound clips stay untouched. Discipline:
figures stay FROZEN (the locked anti-morph rule); ONLY light and air move. No "particle/
sparkle/glitter" words (memory feedback-veo-no-glitter-glow — they bloom AI-glitter).

Run:  .venv\\Scripts\\python.exe sfx_pilots\\fx_pilot_kling_living_light.py
"""
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))
from _hf_animate_short import hf_animate  # noqa: E402  (proven HF Kling call: gate+ledger inside)

PIECE = ROOT / "batches" / "cluster_02_resurrection" / "women_first_witnesses_luke245"
STILLS = PIECE / "visual"
OUT = STILLS / "_fx_pilot"

FROZEN = ("Every figure stays perfectly frozen the entire time — no limbs move, no heads turn, "
          "no faces change, no morphing, no new figures, hands, wings or objects appear. "
          "INVENT NOTHING: show only what is already painted in this exact image. ")

PILOT = [
    ("women_bowed",
     "A still finished inked graphic-novel illustration on flat canvas, filmed as ONE slow, "
     "steady push-in toward the two shining figures. " + FROZEN +
     "ONLY the light and the air are alive: volumetric golden light rays from above slowly "
     "intensify and sweep almost imperceptibly, fine dust motes drift down through the beams, "
     "and the soft glow around the shining garments breathes gently brighter and dimmer."),
    # v3 re-roll (2026-07-14): v1 hardened the face (stern frown); v2 fixed the face but the
    # push-into-the-palm made Kling BLEED the wound (red bloomed + dripped). v3 = whole-figure
    # gentle push (never enlarge the wound), expression lock kept, explicit dry-wound lock.
    ("risen_christ_seeking",
     "A still finished inked graphic-novel illustration on flat canvas, filmed as ONE very slow, "
     "gentle push-in toward the whole standing figure, keeping him fully in frame. His face keeps "
     "the exact same gentle, calm expression from first frame to last — the eyes, brow and mouth "
     "are painted and NEVER shift, harden, frown or blink. The small wound marks on his open palm "
     "stay EXACTLY as painted, dry and still — no blood flows, drips, spreads, brightens or grows. "
     + FROZEN +
     "ONLY the light and the garden air are alive: the sunburst behind him slowly intensifies, "
     "its rays sweeping gently, warm morning haze shimmers in the light, and the flowers and "
     "grasses at the very edges of the frame sway faintly in a light breeze."),
    ("women_tiny_dawn",
     "A still finished inked graphic-novel illustration on flat canvas, filmed as ONE slow, "
     "steady push-in toward the tiny walking figures. " + FROZEN +
     "ONLY the sky and the air are alive: the dawn glow on the horizon slowly warms and "
     "brightens, thin mist drifts low across the ground, and the clouds creep almost "
     "imperceptibly across the sky."),
]


def main():
    OUT.mkdir(exist_ok=True)
    for slug, prompt in PILOT:
        png = STILLS / f"{slug}.png"
        out = OUT / f"{slug}_livinglight.mp4"
        if out.exists() and out.stat().st_size > 0:
            print(f"-- {slug}: already rendered, skip")
            continue
        print(f"-- {slug}: rendering (Kling pro 5s 9:16)")
        ok = hf_animate(png, out, prompt, duration=5)
        print(f"   {'SAVED ' + str(out) if ok else 'FAILED — no fallback (pilot only)'}")


if __name__ == "__main__":
    main()
