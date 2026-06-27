"""LOCKED Awakeden eyewitness SHORT gallery engine (see memory shorts-gallery-hardcut-engine).
A rich painting per beat, toured by HARD CUTS to NAMED elements; the MODEL renders each tight
framing at full native res (Kling 3.0 pro 9:16). Winning prompt = TIMECODED cut schedule.

This module is BOTH the reusable engine (gallery_prompt / make_clip) AND the EW01 builder.
Run: renders any missing still + all gallery clips (idempotent). Assembly is a second step."""
import sys, time
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
import config
from pipeline.visual_models import Scene
from pipeline import visual_render, video_render

GUARD = (" INVENT NOTHING — add no new elements, do not duplicate any single object, do not "
 "morph faces or hands; show ONLY what is already painted in this exact image. The painting "
 "never moves; only the EDIT changes framing. Subtle life only: smoke and flame may flicker. "
 "No glitter, no sparkles.")

def gallery_prompt(elements):
    """elements = list of short phrases naming the tight framings, in tour order.
    Builds the winning TIMECODED hard-cut schedule (10s, wide bookends)."""
    n = len(elements)
    span = 6.0 / max(n, 1)                      # elements occupy ~2.0s..8.0s
    lines = ["Film this exact Baroque oil painting as a fast edited sequence with these EXACT "
        "cuts, each a fixed locked framing with an INSTANT hard cut between them and NO "
        "movement within or between shots (no zoom, no pan, no push):",
        "0.0 to 2.0 seconds the FULL WIDE whole painting;"]
    for i, e in enumerate(elements):
        t = 2.0 + i * span
        lines.append(f"at {t:.1f} cut to {e};")
    lines.append("at 8.5 cut back to the FULL WIDE whole painting until 10.0.")
    return " ".join(lines) + GUARD

def make_clip(png, elements, out, dur=10):
    config.VIDEO_HF_MODEL = "kling3_0"; config.VIDEO_HF_ASPECT = "9:16"
    config.VIDEO_HF_MODE = "pro"; config.VIDEO_HF_SOUND = "off"
    if out.exists():
        print(f"[skip] {out.name}"); return True
    print(f"[clip] {out.name} ...", flush=True); t = time.time()
    try:
        video_render.HFVideoProvider().animate(png, out, gallery_prompt(elements), dur)
        print(f"   ok ({out.stat().st_size:,} b, {time.time()-t:.0f}s)"); return True
    except Exception as e:
        print(f"   FAIL: {str(e)[:160]}"); return False

# ---------------- EW01 Two Goats — paintings + named elements (tour order) ----------------
if __name__ == "__main__":
    SHORT = ROOT / "longform/EW01_Two_Goats/v1/short"
    VT = SHORT / "visual_9x16_test"
    GAL = VT / "gallery_demo"
    OUT = SHORT / "gallery_clips"; OUT.mkdir(exist_ok=True)

    config.VISUAL_STYLE_BASE = ("Baroque oil painting, dramatic chiaroscuro, Caravaggio and "
        "Rembrandt lighting, deep shadow and warm golden light, reverent sacred art, muted "
        "earth tones, fine visible brushwork")
    config.VISUAL_STYLE_TAIL = "no text, no modern elements, vertical 9:16 composition"

    # render the one missing still: Christ TURN (cross + tearing veil)
    turn_png = OUT / "christ_turn.png"
    if not turn_png.exists():
        subj = ("Christ on the cross at the moment of his death on a dark hill outside the "
            "city, the great embroidered temple veil tearing from top to bottom in the "
            "background, the sky darkened, a faint echo of two goats below — one fallen and "
            "slain, one walking away into the waste; broken light beginning to pierce the "
            "gloom. Tall vertical multi-story canvas, reverent, deep chiaroscuro.")
        sc = Scene(index=1, slug="christ_turn", title="The substance", scene_type="unified",
            arc_position="turn", framing="wide", purpose="the fulfilment", rationale="short turn",
            visible_elements="Christ on the cross, tearing temple veil, two goats echo, broken light",
            emotional_tone="awe, grief, dawning hope", subject_block=subj,
            mood_block="reverent, period, multi-story, vertical", jesus_variant=None)
        print("[still] christ_turn ...", flush=True); t = time.time()
        turn_png.write_bytes(visual_render.HFProvider().generate(sc))
        print(f"[still] {turn_png}  ({time.time()-t:.0f}s)")

    # (still_path, [named tight framings in tour order], output clip name)
    PAINTINGS = [
     (VT/"hook.png",            ["the priest's hand gripping the curtain","the dark gap and the golden glow beyond","the small burning oil lamp"], "01_hook.mp4"),
     (GAL/"rich_atonement.png", ["the kneeling priest's lifted face and raised hands","the two goats by the altar","the smoking stone altar","the single burning oil lamp"], "02_overview.mp4"),
     (VT/"variants/s2_two_goats.png", ["the two goats' heads","the smoking altar flame","the priest's hand"], "03_two_goats.mp4"),
     (VT/"variants/s3_blood_veil.png", ["the bronze basin of blood","the priest's raised hand","the golden glow beyond the veil"], "04_blood_veil.mp4"),
     (VT/"variants/s4_hands_confess.png", ["the priest's hands pressed on the goat's head","the priest's bowed face","the goat's eye"], "05_confess.mp4"),
     (VT/"variants/s5_scapegoat_desert.png", ["the small distant goat in the waste","the watching man's back","the empty desert horizon"], "06_scapegoat.mp4"),
     (turn_png,                 ["the face of the crucified Christ","the nail-pierced hand","the wood of the cross"], "07_turn.mp4"),
     (VT/"christ.png",          ["the face of the risen Christ","his hand extended in welcome","the torn veil opening to light"], "08_punch.mp4"),
    ]

    ok = 0
    for png, els, name in PAINTINGS:
        if not png.exists():
            print(f"[MISS still] {png}"); continue
        if make_clip(png, els, OUT/name): ok += 1
    print(f"\nDONE {ok}/{len(PAINTINGS)} gallery clips in {OUT}")
