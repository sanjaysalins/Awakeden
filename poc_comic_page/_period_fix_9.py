"""Comic Page Pipeline -- BIBLICAL-PERIOD FIX re-rolls (CP-G10).

The user's gate caught the Seeker + his ledger as anachronistic (modern
haircut/tunic; bound CODEX book) across 9 already-rendered stills spanning
Rung 1 (3 panels) and Rung 2 (6 panels). CP-G10 (v2/COMIC_PAGE_PIPELINE_
PROPOSAL.md sec3) locks: everything first-century Judea; codex books
FORBIDDEN -- the record is a SCROLL.

Re-renders all 9 in place (originals backed up separately as *_CODEX.png
before this script ran) with a NEW set of character anchors (period-correct
Seeker + Scroll) chained panel-to-panel: step 1 (panel_d_threshold, ref =
the unchanged panel_a_jesus.png) establishes the new Seeker for the first
time; every later panel chains off a freshly-rendered NEW still so the new
design propagates consistently. Reuses the aesthetic / GLOBAL TEXTUAL
CONSTRAINT / style-tail blocks and the ledger try/except call shape from
poc_comic_page/rung1/_render_panel_stills.py and rung2/_render_panel_stills.py.

  .venv\\Scripts\\python.exe poc_comic_page/_period_fix_9.py
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import config
from pipeline import cost
import poc_comic_page.rung1._render_panel_stills as R1MOD  # noqa -- reuse run()/_find_job()

EPISODE = "CPP_Rung2_InNoWise"
MODEL = "nano_banana_pro"
R1 = ROOT / "poc_comic_page" / "rung1" / "stills"
R2 = ROOT / "poc_comic_page" / "rung2" / "stills"

HARD_CAP_USD = 4.20

# ---- Reused verbatim from rung1/rung2 _render_panel_stills.py --------------
AESTHETIC = (
    "A 9:16 vertical single comic-book panel illustration. Rendered in a "
    "vintage graphic novel illustration style characterized by heavy black "
    "ink linework, high-contrast chiaroscuro shadows, cross-hatching, and a "
    "desaturated, muted earth-tone color palette (dominant slate grays, deep "
    "ochre, raw umber, muted blues). Subtle aged, textured vintage comic "
    "print finish."
)

CONSTRAINT = (
    "GLOBAL TEXTUAL CONSTRAINT: NO text of any kind anywhere -- no speech "
    "bubbles, no caption boxes, no lettering, no words. Pure artwork only."
)

# ---- NEW period-correct anchors (CP-G10 fix) --------------------------------
ANCHORS = (
    "CORE CHARACTER DESIGN ANCHORS:\n"
    "Jesus Christ: a lean Jewish man in his early thirties, broader rugged "
    "face, shoulder-length dark wavy hair, full beard, deep-set compassionate "
    "eyes, wearing a simple undyed woolen robe with a rough-woven mantle. "
    "Dignified, gentle, welcoming. A teaching scene -- no wounds, no crown of "
    "thorns.\n"
    "The Seeker: a weary Judean man in his forties, first-century Judea -- "
    "full greying beard, weathered lined face, shoulder-length greying hair "
    "under a simple cloth head covering, an ankle-length rough-woven "
    "earth-tone tunic bound with a cloth girdle, a draped woolen mantle, worn "
    "leather sandals. He carries the Scroll.\n"
    "The Scroll: a worn papyrus scroll wound around a single wooden rod, tied "
    "shut with a frayed cord -- the written record of his debts, aged and "
    "stained. It always appears ROLLED SHUT, never open, no visible writing "
    "ever.\n"
    "The Door: a massive ancient ARCH-TOPPED wooden door, iron-banded, set in "
    "a rough stone wall.\n"
    "PERIOD CONSTRAINT: everything depicts first-century Judea -- clothing, "
    "hair, objects, hardware. Nothing modern, nothing medieval-European: no "
    "tailored haircuts, no fitted garments, no bound books."
)

PREFIX = AESTHETIC + "\n\n" + CONSTRAINT + "\n\n" + ANCHORS + "\n\n"

CHAIN_LINE = (
    "This panel continues directly from the reference image: same figures, "
    "same world, same ink style.\n\n"
)

STYLE_TAIL = (
    "EXPLICIT STYLE CONSTRAINTS: Vintage graphic novel comic-book art, heavy "
    "black ink linework, high-contrast chiaroscuro, muted earth tones, "
    "reverent and dignified treatment throughout, absolutely no text or "
    "lettering anywhere."
)

# (name, out_path, ar, ref_path, composition) -- ref_path resolved lazily via
# the canonical output path of an EARLIER step in this same list, so each
# entry always chains off the freshly re-rendered file (sequential order
# matters -- do not reorder / parallelize).
PANELS = [
    ("panel_d_threshold", R1 / "panel_d_threshold.png", "9:16", R1 / "panel_a_jesus.png",
     "Wide shot -- the Seeker crossing the threshold into the light, door "
     "swung open, and beyond it the standing figure of Jesus with a hand "
     "extended in welcome. The Seeker carries the rolled scroll in one hand. "
     "Lighting: the warm light dominant, shadows breaking."),

    ("panel_b_door", R1 / "panel_b_door.png", "9:16", R1 / "panel_d_threshold.png",
     "The Seeker seen from DIRECTLY BEHIND at medium distance, walking "
     "toward the great ancient arch-topped door standing ajar -- ONLY THE "
     "BACK OF HIS HEAD visible (head cloth + shoulder-length greying hair), "
     "no profile, face completely hidden. The rolled scroll carried under "
     "his left arm, right hand reaching toward the door handle. Warm golden "
     "light through the gap onto stone. Lighting: cold slate surroundings, "
     "warm light only from the door gap."),

    ("panel_c_ledger", R1 / "panel_c_ledger.png", "9:16", R1 / "panel_d_threshold.png",
     "Extreme close-up of the Seeker's weathered hands clutching the rolled "
     "papyrus scroll to his chest -- the wooden rod ends visible, the "
     "frayed cord tie hanging, knuckles tense. Ankle-length tunic and "
     "mantle folds behind. Lighting: dim, a sliver of warm light catching "
     "the scroll's edge."),

    ("p5a_the_welcome", R2 / "p5a_the_welcome.png", "1:1", R1 / "panel_d_threshold.png",
     "Wide warm shot at the open threshold: Jesus laying one hand on the "
     "Seeker's shoulder, the Seeker's head lifting, the radiant doorway "
     "light around them both, the rolled scroll in the Seeker's hand. "
     "Lighting: full warm radiance, shadows breaking apart."),

    ("p1a_night_door", R2 / "p1a_night_door.png", "1:1", R1 / "panel_b_door.png",
     "Wide establishing shot at night: the Seeker standing alone and small "
     "before the great arch-topped door, shut, in a vast rough stone wall "
     "-- cold slate-blue darkness, one thin line of warm light under the "
     "door. He stands a few paces back, the rolled scroll held to his "
     "chest. Lighting: cold moonless night, the only warmth the light-line "
     "under the door."),

    ("p1b_hesitant_hand", R2 / "p1b_hesitant_hand.png", "1:1", R1 / "panel_c_ledger.png",
     "Close-up from behind and beside the Seeker: his weathered hand "
     "half-raised toward the closed door's dark wood, hesitating, NOT "
     "touching it; the other arm presses the rolled papyrus scroll to his "
     "chest, cord tie hanging. Lighting: dim cold light, faint warm glow "
     "from below the door edge."),

    ("p2a_rehearsing", R2 / "p2a_rehearsing.png", "9:16", R1 / "panel_d_threshold.png",
     "Tall portrait: the Seeker leaning his forehead against the closed "
     "door's frame, eyes shut, lips parted mid-whisper, rehearsing his "
     "plea -- the rolled scroll pressed between his chest and the frame. "
     "Lighting: cold, the warm under-door light touching his sandaled feet "
     "and tunic hem."),

    ("p4a_turning_away", R2 / "p4a_turning_away.png", "9:16", R1 / "panel_d_threshold.png",
     "Tall portrait, TWO figures (this composition is user-approved): the "
     "Seeker half-turned AWAY from the open door, head bowed, the rolled "
     "scroll hanging heavy in one hand -- while Jesus stands at the "
     "doorway behind him, head inclined, patient, light around him. "
     "Lighting: the Seeker in cold shadow, the warm light behind him low "
     "and patient."),

    ("p5b_record_received", R2 / "p5b_record_received.png", "3:4", R2 / "p5a_the_welcome.png",
     "Close-up: the worn rolled papyrus scroll with its frayed cord now "
     "resting in Jesus' open hand, held gently, the Seeker's empty hands "
     "releasing it in the soft warm background. Lighting: warm light on "
     "the scroll and the receiving hand."),
]


def main():
    spent_usd = 0.0
    results = []
    for name, out, ar, ref, comp in PANELS:
        prompt = PREFIX + CHAIN_LINE + f"SINGLE PANEL COMPOSITION: {comp}\n\n" + STYLE_TAIL
        print(f"[img ] {name} (AR {ar}, ref {ref.name}) ...", flush=True)
        if spent_usd >= HARD_CAP_USD:
            print(f"   STOP: hard cap ${HARD_CAP_USD:.2f} reached before this panel -- escalating.")
            results.append((name, "ESCALATED-cap", None))
            continue
        ok = R1MOD.run(prompt, out, [ref], ar)
        if ok:
            try:
                row = cost.record_hf(EPISODE, "short", "stills", MODEL,
                                      note=f"[period-fix] {name} CP-G10 re-roll")
                spent_usd += float(row.get("est_usd") or 0)
            except Exception as e:
                print(f"   (ledger record skipped: {e})")
            print(f"   ok  running spend ~${spent_usd:.2f}")
            results.append((name, "clean", out))
        else:
            print("   FAILED")
            results.append((name, "FAILED", None))
    print(f"\n[spend] ~${spent_usd:.2f} of ${HARD_CAP_USD:.2f} cap")
    for name, status, out in results:
        print(f"  {name}: {status}" + (f" -> {out}" if out else ""))


if __name__ == "__main__":
    main()
