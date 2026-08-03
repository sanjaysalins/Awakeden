"""POC 1 ($0, no renders): does the text-only classifier (classify.py) agree
with the FINAL, human-approved shot choices on an episode that's already
shipped?

Ground truth = `poc_living_sketchbook/bronze_serpent/visual_tags.json`
(the tags the team actually locked, AFTER the real defect-and-fix cycle
that STATE.md records: s07/s09/s11 originally collapsed onto the same
"Moses standing with staff" pose and had to be re-shot with different
blocking). Input = the per-spread Text/Shot description transcribed
verbatim from `poc_living_sketchbook/bronze_serpent/_TIMING.md`'s own
14-row table (real WhisperX-timed, the doc this project already trusts).

This is a sanity check, not a grading exercise: the classifier's vocabulary
will never match the shipped tags' vocabulary word-for-word. What matters:
(a) does it correctly keep spreads the team judged genuinely-different in
DIFFERENT buckets, and (b) where does it fail to separate spreads that the
team's own judgment DID separate — because that gap is exactly what a
planning-time tool would need a human to still catch.
"""
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
sys.path.insert(0, str(HERE))
from classify import classify  # noqa: E402

# Transcribed verbatim from poc_living_sketchbook/bronze_serpent/_TIMING.md's
# "14-spread table — real windows" (the Text + Shot columns), in page order.
# Slug order matches visual_tags.json's own key order 1:1 (both are the
# episode's page sequence).
SPREADS = [
    ("s01_wide", "I am Moses. My people were dying of snakebite, and God told me to forge a snake of bronze and lift it on a pole.",
     "Wide establishing: the camp of tents at the wilderness's edge, Moses in the foreground, a stricken family in the middle distance"),
    ("s02_grief", "...and God told me to forge a snake of bronze and lift it on a pole.",
     "Close/mid: Moses's face, grief and urgency, kneeling by a stricken figure"),
    ("s03_complaint", "The serpents were no accident — we had spoken against God...",
     "Wide: a knot of the people, gesturing in complaint/discouragement, Moses standing apart"),
    ("s04_serpents", "...and the venom was the judgment our sin had earned.",
     "Serpents among the rocks and tent-lines, people recoiling"),
    ("s05_intercession", "I begged Him to take the snakes away. He would not.",
     "Moses alone, kneeling in intercession against open sky"),
    ("s06_forge", "Instead He told me to forge the image... The bitten had only to look — and live.",
     "Close on Moses's hands at the forge, hammering the bronze serpent into shape"),
    ("s07_horizon", "I speak now from the far side of my life, by the light that came after — a night I never saw, when one they called Teacher answered a seeker:",
     "Moses's face turned toward the horizon/light"),
    ("s08_typology", "And as Moses lifted up the serpent in the wilderness, even so must the Son of man be lifted up:",
     "INSERT PAGE 1 of 2 — Scholar's-Margin typology sheet, two-panel labeled comparison"),
    ("s09_shadow", "My bronze was only a shadow.",
     "Moses's face, humble, bronze serpent visually smaller/plainer than the gold page just shown — hard cut back from s08"),
    ("s10_golgotha", "They lifted Jesus on a Roman pole, made a curse for us, bearing our judgment in our place.",
     "Christ lifted up, a reverent Golgotha beat — sacred, restrained, no gore"),
    ("s11_hearme", "So hear me, you who are bitten — that is every one of us.",
     "Moses turns to address the reader directly"),
    ("s12_echo", "The cure was never in you; it hangs in plain sight, and costs you nothing but a look.",
     "INSERT PAGE 2 of 2 — Gilded Proclamation plate, one unified gold-ground composition"),
    ("s13_lifted", "Lift your eyes to Jesus, lifted up for you.",
     "Christ lifted, radiant, the landing's approach"),
    ("s14_landing", "Look, and live.",
     "THE LANDING — torn-page device, gold light from beneath the tear"),
]


def main() -> int:
    tags_path = ROOT / "poc_living_sketchbook" / "bronze_serpent" / "visual_tags.json"
    ground_truth = json.loads(tags_path.read_text(encoding="utf-8"))

    print(f"{'slug':<18} {'derived pose':<22} {'derived framing':<14} "
          f"{'shipped pose':<32} {'shipped framing':<8}")
    print("-" * 100)
    derived_rows = []
    for slug, text, shot in SPREADS:
        d = classify(f"{text} {shot}")
        gt = ground_truth[slug]
        derived_rows.append((slug, d))
        print(f"{slug:<18} {d['pose']:<22} {d['framing']:<14} "
              f"{gt['pose']:<32} {gt['framing']:<8}")

    # The real historical defect: s07/s09/s11 shipped as ONE identical
    # composition ("Moses standing with staff") and had to be re-shot.
    # Would the classifier's derived buckets have kept them apart, using
    # ONLY the planning-stage text (no image, no hindsight)?
    print("\n--- the known defect trio (s07/s09/s11), text-only buckets ---")
    trio = {slug: d for slug, d in derived_rows if slug in ("s07_horizon", "s09_shadow", "s11_hearme")}
    for slug, d in trio.items():
        print(f"  {slug}: pose={d['pose']} framing={d['framing']}")
    keys = [(d["pose"], d["framing"]) for d in trio.values()]
    if len(set(keys)) == len(keys):
        print("  -> all three land in DIFFERENT buckets: classifier would not have "
              "silently repeated them.")
    else:
        print("  -> two or more land in the SAME bucket: classifier alone would "
              "have missed this collision too (same conclusion as the real "
              "history — it took a human eye + the post-render lint).")

    # How often did the framing classifier fall back to its 'mid' default
    # (i.e. the Shot/Text prose didn't state a framing at all)?
    defaulted = sum(1 for _, d in derived_rows if d["framing"] == "mid")
    print(f"\nframing defaulted to 'mid' (no explicit keyword in the text) on "
          f"{defaulted}/{len(derived_rows)} spreads.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
