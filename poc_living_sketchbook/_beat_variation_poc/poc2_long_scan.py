"""POC 2 ($0, no renders): forward-looking collision-risk scan on the LIVE,
in-progress Bronze Serpent LONG pilot (68 spreads, being rendered right now
at $0.30/still — only a fraction done as of this scan).

Unlike the short episode (`poc_living_sketchbook/bronze_serpent/`, 14
spreads, which HAS an explicit per-spread Shot column + a visual_tags.json),
the long plan's 68-row table (`poc_living_sketchbook/bronze_serpent_long/
_PLAN.md`) only has a coarse Type column (NS/MV/IP/VC/LAND) + free-text
"Shows" prose — nothing structured tracks pose/framing family across 68
spreads the way spread_variety.py already does for the short. At 68
spreads (vs 14) the raw collision surface is much bigger, and the short
already proved this exact failure mode can happen silently (s07/s09/s11
shipped as one repeated "Moses standing with staff" composition before a
human eye caught it).

This scan runs the SAME text-only classifier over every row of the real
plan table (transcribed verbatim from _PLAN.md, page order, unchanged) and
flags spreads sharing a subject-family + derived (pose, framing) bucket
CLOSE TO EACH OTHER in the page sequence (the real risk zone — two similar
shots 500s apart barely register as repetition to a viewer; two within a
handful of spreads of each other read as "did I just see this?"). Proximity
threshold mirrors this project's own existing `_reuse_check` convention
("within an 8-beat gap" -- see memory: panel-variety-gate).

Cross-references against what's already rendered on disk vs still-remaining
spreads, so the output is a genuinely actionable "look harder at these
before you spend on them" list -- not just an abstract table.
"""
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
sys.path.insert(0, str(HERE))
from classify import classify, normalize_assets  # noqa: E402

PROXIMITY_WINDOW = 8  # spreads; matches this project's own reuse-check gap convention

# Transcribed verbatim (Type / Shows / Assets columns only) from
# poc_living_sketchbook/bronze_serpent_long/_PLAN.md's "2. The full spread
# table" (68 rows, page order unchanged). # = the plan's own spread number.
ROWS = [
    (1, "NS", "Wide establishing: aged Moses, wilderness camp behind", "Moses"),
    (2, "MV", "Triptych memory-vignette: rod-to-serpent / Red Sea split / water from the rock", "Moses"),
    (3, "NS", "Close on Moses's eyes, haunted, follows me still", "Moses"),
    (4, "NS", "THE ICON: pole in the sand, bronze serpent revealed", "Moses, bronze-serpent"),
    (5, "NS", "Graves being dug, the dying, grief — wide", "crowd"),
    (6, "NS", "Close: a dying man's empty/reaching hand, then an eye", "crowd (1 figure)"),
    (7, "NS", "Wide: the freed-but-ungrateful camp", "crowd"),
    (8, "NS", "Wide: the wandering column, going round Edom, barren road, no end in sight", "crowd"),
    (9, "NS", "Manna falling, faithfully, being turned from/scorned", "crowd"),
    (10, "VC", "Verse card: the soul of the people was much discouraged because of the way", "crowd (bg art)"),
    (11, "NS", "Crowd turns angry, toward Moses and toward heaven", "crowd, Moses"),
    (12, "VC", "Verse card: Wherefore have ye brought us up", "crowd"),
    (13, "MV", "Memory-vignette: the sea / the rock / the golden calf under the cloud at Sinai", "Moses, calf"),
    (14, "NS", "Something slides in the dust between the tents — first hint of the serpents", "none new"),
    (15, "VC", "Verse card: And the LORD sent fiery serpents among the people + serpents among the camp", "crowd"),
    (16, "NS", "Close: the bite, burned like a coal — heat/glow, not graphic wound", "crowd (1 figure)"),
    (17, "MV", "Vignette: a strong man collapsed + a mother cradling a child", "crowd (2 figures max)"),
    (18, "NS", "Moses alone, hands empty, no remedy — atmosphere beat", "Moses"),
    (19, "NS", "The people kneel before Moses, posture shifts from anger to contrition", "crowd, Moses"),
    (20, "VC", "Verse card: We have sinned", "crowd"),
    (21, "NS", "Moses interceding, kneeling, arms raised in prayer", "Moses"),
    (22, "NS", "Moses's face — surprise the LORD did not simply remove the serpents; listening", "Moses"),
    (23, "NS", "THE LORD's presence appears — Moses shields his eyes/kneels before an overwhelming radiant light, no figure, no face", "Moses, LORD-presence"),
    (24, "VC", "Illuminated Rubric verse card: Make thee a fiery serpent, and set it upon a pole", "LORD-presence (bg glow)"),
    (25, "NS", "Moses processing — no medicine offered, negation imagery (empty hands, no jar)", "Moses"),
    (26, "NS", "Moses looking at a live serpent on the ground — resolve forming", "Moses"),
    (27, "NS", "Close-up hands, beginning the forge", "Moses (hands)"),
    (28, "NS", "Acting spread: Moses hammering the bronze serpent into shape, extreme close, motion completes then holds", "Moses (hands), bronze-serpent"),
    (29, "NS", "The pole now stands; the first bitten look up, first healing", "crowd, bronze-serpent"),
    (30, "MV", "Payoff: a man's fever breaks as he looks up at the pole", "crowd, bronze-serpent"),
    (31, "NS", "Close on Moses's face turning the question over: Why a serpent?", "Moses"),
    (32, "NS", "Wide/mid: the serpent on its pole, silhouetted against the camp at dusk", "bronze-serpent"),
    (33, "MV", "Vignette: strong man / child / dying elder, all lifting their eyes the same way", "crowd (3 vignette figures)"),
    (34, "NS", "Moses walking alone at dusk, the riddle walking home with him every evening", "Moses"),
    (35, "NS", "Close on elderly Moses's face, direct-address register begins: I will be honest with you", "Moses"),
    (36, "NS", "Mid: a proud man turning away from the pole in the background while others look", "crowd"),
    (37, "NS", "FLASHBACK, soft-focus/silhouette: grinding the golden calf to powder", "Moses (silhouette), calf"),
    (38, "NS", "THE DREAD IMAGE: Moses holding the bronze serpent, staring at it", "Moses, bronze-serpent"),
    (39, "NS", "Close, night: Moses sleepless, had God bidden the very sin I had just broken", "Moses"),
    (40, "NS", "Moses's resolve returning, hand on the bronze but eyes lifted", "Moses, bronze-serpent"),
    (41, "NS", "Wide: Moses at the camp's edge, looking down a long empty road into darkness", "Moses"),
    (42, "NS", "Close on hands finishing the forge, quiet — bookends spread 28", "Moses (hands), bronze-serpent"),
    (43, "IP", "INSERT PAGE 1: Scholar's-Margin two-panel typology diagram", "Jesus, Nicodemus"),
    (44, "NS", "Moses's realization: the bronze serpent's shadow, symbolically cross-shaped on the ground", "Moses, bronze-serpent"),
    (45, "NS", "Golgotha: Christ lifted on the cross, wide, reverent, restrained, no gore", "Jesus"),
    (46, "NS", "Paired composition: bronze serpent + the cross together in one frame", "bronze-serpent, Jesus"),
    (47, "NS", "Christ on the cross, reverent, leading into the Gal 3:13 quote", "Jesus"),
    (48, "VC", "Verse card: being made a curse for us", "Jesus (bg)"),
    (49, "NS", "Christ lifted, radiant register beginning — bore the judgment taken in our place", "Jesus"),
    (50, "NS", "Close, leading into Jesus's own words", "Jesus"),
    (51, "NS", "Red-letter, arrives whole: And I, if I be lifted up from the earth, will draw all men unto me", "Jesus, crowd (distant)"),
    (52, "NS", "Moses reflecting, resolved: it was never the bronze; it was the looking that God honoured", "Moses"),
    (53, "NS", "Brief, close on Moses: I know that now better than I once wished to", "Moses"),
    (54, "NS", "TIME SHIFT: people burning incense before the enshrined serpent — idolatry creeping in", "crowd, bronze-serpent"),
    (55, "NS", "Hezekiah, a young king, breaks the bronze serpent to pieces — decisive, corrective, not shameful", "Hezekiah"),
    (56, "NS", "Moses's voice affirms: he was right to break it. The power was never in my handiwork", "Moses"),
    (57, "NS", "Transition back to Christ/gold register: the power was in the God who said look and live", "Jesus, Moses"),
    (58, "VC", "Illuminated Rubric verse card (full ceremony): John 3:16", "Jesus (bg, radiant)"),
    (59, "NS", "Moses direct-address: So hear me — be still. Do not rush past this as my people rushed past the manna", "Moses"),
    (60, "MV", "Vignette: strong men trying to walk the fire off, each failing in his own way", "crowd (2-3 vignette figures)"),
    (61, "NS", "Intimate close on Moses: That is you. That is me", "Moses"),
    (62, "NS", "Close, resolute: you were never asked to", "Moses"),
    (63, "MV", "Christ radiant lifted; three small figures below — the least, the last, a child turning his head", "Jesus, crowd (3 vignette figures)"),
    (64, "NS", "Pause beat, near-silence: Sit with that", "Moses"),
    (65, "NS", "Christ, plain and open: costs you nothing but a look", "Jesus"),
    (66, "NS", "Moses turning the question directly to the viewer — most intimate direct-address of the film", "Moses"),
    (67, "IP", "INSERT PAGE 2 (Gilded Proclamation echo)", "bronze-serpent, Jesus"),
    (68, "LAND", "THE LANDING: Look to Him, and live. Torn-page device", "Jesus (silhouette)"),
]


def rendered_numbers() -> set[int]:
    stills = ROOT / "poc_living_sketchbook" / "bronze_serpent_long" / "stills"
    done = set()
    for p in stills.glob("s*.png"):
        m = re.match(r"s(\d+)_", p.name)
        if m and "defect" not in p.name:
            done.add(int(m.group(1)))
    return done


def main() -> int:
    done = rendered_numbers()
    print(f"{len(done)}/68 spreads currently rendered on disk.\n")

    derived = []
    for num, type_, shows, assets in ROWS:
        subj = normalize_assets(assets)
        d = classify(shows)
        derived.append({"num": num, "type": type_, "subj": subj, **d,
                         "shows": shows, "rendered": num in done})

    # Only NS (narrative single-figure) rows carry real repeat-composition
    # risk -- VC/IP/LAND/MV are structurally distinct (verse card, insert
    # page, landing device, multi-vignette) and exempted, same as this
    # project's own §3 shot-list-variety floor treats them differently.
    candidates = [r for r in derived if r["type"] == "NS"]

    flags = []
    for i, a in enumerate(candidates):
        for b in candidates[i + 1:]:
            if b["num"] - a["num"] > PROXIMITY_WINDOW:
                break
            if a["subj"] == b["subj"] and a["pose"] == b["pose"] and a["framing"] == b["framing"]:
                flags.append((a, b))

    print(f"Collision-risk pairs (same subject-family + same derived pose+framing, "
          f"within {PROXIMITY_WINDOW} spreads of each other): {len(flags)}\n")
    for a, b in flags:
        status = lambda r: "RENDERED" if r["rendered"] else "remaining"
        print(f"  #{a['num']:02d} <-> #{b['num']:02d}  subj={a['subj']!r:<20} "
              f"pose={a['pose']!r} framing={a['framing']!r}")
        print(f"       #{a['num']:02d} [{status(a)}]: {a['shows'][:70]}")
        print(f"       #{b['num']:02d} [{status(b)}]: {b['shows'][:70]}")

    # Cluster view: consecutive runs of the same subject-family among NS
    # rows, regardless of bucket match -- these are the zones worth a human
    # eye even where the classifier's buckets happen to differ, because the
    # short's own real defect (s07/s09/s11) proved buckets this coarse can
    # still look identical once actually rendered.
    print("\n--- consecutive same-subject NS runs (>=3 in a row) ---")
    run = []
    for r in candidates:
        if run and r["subj"] == run[-1]["subj"] and r["num"] - run[-1]["num"] <= 2:
            run.append(r)
        else:
            if len(run) >= 3:
                nums = [x["num"] for x in run]
                remain = sum(1 for x in run if not x["rendered"])
                print(f"  subj={run[0]['subj']!r:<10} spreads {nums} "
                      f"({remain}/{len(run)} still remaining)")
            run = [r]
    if len(run) >= 3:
        nums = [x["num"] for x in run]
        remain = sum(1 for x in run if not x["rendered"])
        print(f"  subj={run[0]['subj']!r:<10} spreads {nums} ({remain}/{len(run)} still remaining)")

    return 0


if __name__ == "__main__":
    sys.exit(main())
