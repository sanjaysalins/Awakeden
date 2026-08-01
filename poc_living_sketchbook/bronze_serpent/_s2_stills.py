"""Bronze Serpent episode -- step 2. 14 spreads, 9:16, cast-bible anchored +
full-bleed framing. Follows storm/_s2_stills.py's exact pattern (same repo-
level cast-bible mechanism, same run()/resolve_refs()/main() shape).

Sources (read before touching this file):
- poc_living_sketchbook/bronze_serpent/_TIMING.md -- the real, word-timed
  14-spread table (real seconds, not estimates). This script's spread ORDER,
  TEXT, and SHOT column are taken verbatim from that table.
- poc_living_sketchbook/_FABLE_ROUND9_BRONZESERPENT_E2E_PLAN.md sections
  A2/A3 -- why the insert page sits at s08 and what it shows.
- poc_living_sketchbook/cast/MOSES.md + moses_ref.png (repo-level cast-bible
  anchor, elderly Numbers-21-era Moses) and poc_living_sketchbook/cast/
  JESUS.md + jesus_ref.png (already built, reused across every episode).
- .claude/skills/living-sketchbook/SKILL.md sec.0 (LAW1/LAW2), sec.2 (anchor
  + multi-pose identity-lock rules), sec.8a (still QC checklist), crowd rule
  (<=3 distinct faces, rest to shadow).
- crucifixion-still-facts memory (darkness not storm, no nail close-ups, no
  visible wounds/blood in a reverent shot, bowed head, restrained).

s08 (the Numbers-21/John-3 typology insert page) is ALREADY RENDERED and
locked from the Round 9 planning pass -- it is listed below for completeness
but main() SKIPS it and points at the existing file rather than re-requesting
it. It has a known "photographed-codex" framing flaw (visible book spine /
drop-shadow on grey studio ground) that needs a $0 crop before final
assembly -- a future step, not fixed here.

s01's "WILDERNESS. FORTIETH YEAR." Field Header is an ASSEMBLY-STAGE overlay
(same as storm's own Field Header -- see storm/_s6_assemble.py's
"---- s01 Field Header ----" block, composited on top of the finished s01
art at t=HEADER_T0, not baked into the AI render). Nothing in this script
requests it; it is a note for whoever writes bronze_serpent/_s6_assemble.py.

TEST GATE (2026-07-31): render ONLY s01 + s10 this round, per the project's
standing test-gate discipline (2 real stills, human review, before any full
batch). The other 12 spreads' SCENE prompts are written and ready below so
the script is complete for the next round -- do NOT run them yet.

  .venv\\Scripts\\python.exe poc_living_sketchbook/bronze_serpent/_s2_stills.py s01_wide,s10_golgotha
"""
import re
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
import config
from pipeline import cost

HF = str(config.HF_CLI_PATH)
MODEL = "nano_banana_pro"
EPISODE = "LS_BronzeSerpent"
HERE = Path(__file__).resolve().parent
WORLD_CAST = HERE.parent / "cast"          # repo-level cast-bible (shared across episodes)
OUT = HERE / "stills"
OUT.mkdir(parents=True, exist_ok=True)

MOSES_REF = WORLD_CAST / "moses_ref.png"
JESUS_REF = WORLD_CAST / "jesus_ref.png"
# PHASE B: after s01 is eye-approved, this resolves to stills/s01_wide.png so
# every LATER Moses still chains BOTH the repo anchor and the approved
# in-episode pose (SKILL.md sec.2 multi-pose identity lock).
MOSES_REF2 = OUT / "s01_wide.png"
# PHASE B: after s10 is eye-approved (the first NARRATIVE-scale Jesus
# appearance -- s08 is a different style register, the Scholar's-Margin
# insert page, and does not count for this purpose), this resolves to
# stills/s10_golgotha.png so every later narrative Jesus still (s12/s13/s14)
# chains BOTH the repo anchor and the approved in-episode pose.
JESUS_REF2 = OUT / "s10_golgotha.png"

# s08 is already rendered from the Round 9 planning pass -- do NOT re-request it.
S08_EXISTING = ROOT / "poc_living_sketchbook" / "_style_bakeoff" / "bronzeserpent_typology_numbers21_john3.png"

MOSES = (
    "Moses: an elderly Hebrew man in his eighties, forty years into the "
    "wilderness wandering -- the aged lawgiver of Numbers, NOT the young "
    "Moses of the Exodus/burning-bush years -- a broad weathered forehead, "
    "deep-set eyes beneath heavy grey brows, hollowed cheeks, a strong jaw "
    "beneath the beard, long white and grey hair swept back off the "
    "forehead and thinning at the crown, a long full white beard streaked "
    "with iron-grey reaching mid-chest, deeply sun-weathered leathery "
    "skin, an old man's spare sinewed frame -- still upright and "
    "strong-shouldered, never frail or youthful -- dark steady eyes "
    "weighted with authority and grief, large veined elder's hands, a "
    "plain undyed woolen robe with a coarse mantle draped over one "
    "shoulder, a woven cord girdle, plain leather sandals, always holding "
    "or beside a tall wooden staff worn smooth by decades of use. the SAME "
    "man as the reference image(s) -- identical face, beard, hair, and "
    "clothing."
)
JESUS = (
    "Jesus: a Judean man in his early thirties, long dark wavy hair past "
    "the shoulders parted center, short close-cropped dark beard, a "
    "strong straight nose and defined cheekbones, warm deep brown eyes "
    "level and calm, sun-weathered olive skin, lean wiry-strong build, "
    "simple undyed homespun ankle-length tunic with a woven cord sash, "
    "leather sandals. the SAME man as the reference image(s) -- identical "
    "face, beard, hair, and clothing."
)
PEOPLE = (
    "the stricken Israelites: ordinary wilderness-worn Hebrew men, women, "
    "and children in plain undyed tunics and mantles, unnamed and never "
    "repeated as named characters -- AT MOST three faces rendered with "
    "any individual detail anywhere in the frame, count them: no more "
    "than three -- every other figure present is turned away, downcast, "
    "or held in soft shadow so no further face reads as distinct, and "
    "there is no fourth or fifth clearly-detailed face anywhere, even "
    "partially hidden or turned away. Distress is shown ONLY through "
    "posture and gesture -- slumped shoulders, a hand pressed to an arm "
    "or leg, huddled closeness, faces turned down or away -- NEVER a "
    "visible wound, bite mark, snake attached to skin, or blood anywhere "
    "on any figure."
)
LIVE_SERPENTS = (
    "small venomous desert serpents darting and coiling among the rocks "
    "and tent-stakes -- no serpent shown biting or attached to any "
    "figure's skin anywhere in the frame"
)
# s04-only crowd cap, ported from storm/_s2_stills.py's proven DISCIPLES wording
# (2026-07-31 face-count fix -- the shared PEOPLE constant's "at most three,
# rest in shadow" phrasing let a render slip to 7-8 detailed faces because it
# never hard-capped the TOTAL number of figures, only how much detail each
# got. This version follows the Storm precedent exactly: an EXACT headcount,
# enumerated positions, and a hard "no one else present" close, not a soft
# "push the rest to shadow" allowance).
PEOPLE_S04 = (
    "EXACTLY two stricken Israelites and no more -- count them: (1) a man "
    "clutching his own forehead in grief, eyes shut, head bowed low; (2) a "
    "woman clutching her chest in distress, her face drawn and stricken, "
    "one hand pressed flat over her heart -- both ordinary wilderness-worn "
    "Hebrews in plain undyed tunics, unnamed and never repeated as named "
    "characters elsewhere. There is NO third person, no fourth person, no "
    "fifth person, no partial figure, no extra head or body visible "
    "anywhere in the frame, even partially hidden, turned away, silhouetted "
    "near a tent flap, or in the far background -- no other man, woman, or "
    "child present anywhere in the scene, only these two figures and no "
    "one else. Distress is shown ONLY through posture and gesture -- "
    "slumped shoulders, a hand pressed to the chest or forehead -- NEVER a "
    "visible wound, bite mark, snake attached to skin, or blood anywhere "
    "on either figure."
)
BRONZE_SERPENT = (
    "a serpent cast in plain dull bronze and copper, coiled around a "
    "tall wooden pole, catching only dull worked-metal highlights -- "
    "never gold; gold is reserved for Christ's glory alone in this "
    "episode, never for the serpent or its pole"
)
FULLBLEED = (
    "CRITICAL FRAMING: zoom in close enough that the illustrated subject "
    "and its immediate surroundings occupy the ENTIRE frame, corner to "
    "corner. There must be NO large empty cream-paper or kraft-paper "
    "region anywhere inside the frame, and no blank kraft-paper rectangle "
    "or sticky-note patch used as filler -- the torn-edge collage texture "
    "is only a narrow border treatment along the outermost margin, never a "
    "wide blank zone."
)

STYLE = (
    "Editorial documentary sketch illustration: loose confident graphite-and-ink "
    "linework with muted watercolor wash, drawn on aged warm cream paper. "
    "Aged-print paper-collage aesthetic: warm cream and kraft textured stock, "
    "torn and cut-paper edges, subtle offset-halftone dot texture, faint "
    "engineering-grid hairlines, soft raking museum light, tactile hand-made "
    "feel, muted ink-red and ink-blue accents, a thin strip of gold leaf at one "
    "edge. CRITICAL: absolutely NO lettering, numerals, words, newsprint, "
    "printed book-page text, handwriting, ruler markings, dates, or captions "
    "ANYWHERE on ANY layer -- every paper surface is BLANK textured stock."
)

# (name, refs-tag, scene) -- scene=None marks an already-rendered spread (s08),
# skipped by main() rather than re-requested.
# Beat/window/text/shot columns below are taken verbatim from _TIMING.md.
SHOTS_ALL = [
    # s01 | Beat 1 | 0.387-3.657s | "I am Moses. My people were dying of
    # snakebite..." | Wide establishing: camp of tents, Moses foreground, a
    # stricken family at a distance | Field Header composited at ASSEMBLY,
    # not requested here (see module docstring)
    ("s01_wide", "moses1",
     f"Wide establishing shot at the edge of a wilderness encampment: rows "
     f"of weathered goat-hair tents recede into the distance beneath a "
     f"vast pale desert sky, {MOSES} stands in the foreground gripping his "
     f"tall staff, looking back over his shoulder toward a stricken family "
     f"in the middle distance -- EXACTLY three family members and no more: "
     f"a mother, a father, and a child, huddled together, the father's arm "
     f"draped over the child's shoulder, all downcast and slumped, "
     f"distress shown ONLY through posture -- no wound, no bite mark, no "
     f"blood, no snake touching any of them anywhere in the frame. "
     f"{FULLBLEED}"),

    # s02 | Beat 1 | 3.657-8.230s | "...and God told me to forge a snake of
    # bronze and lift it on a pole." | Close/mid: Moses's face, grief and
    # urgency, kneeling by a stricken figure
    ("s02_grief", "moses2",
     f"Close/mid shot: {MOSES} kneeling on the sand beside a single "
     f"stricken figure lying on a woven mat, his weathered face etched "
     f"with grief and urgency as he reaches one hand toward them -- ONE "
     f"stricken figure only, their face turned away and downcast, their "
     f"distress shown through a limp arm and a turned face, never a "
     f"visible wound or blood. {FULLBLEED}"),

    # s03 | Beat 2 | 8.230-11.433s | "The serpents were no accident -- we
    # had spoken against God..." | Wide: a knot of the people, gesturing in
    # complaint/discouragement, Moses standing apart
    ("s03_complaint", "moses2",
     f"Wide shot: a knot of the Israelites gathered in complaint, {PEOPLE} "
     f"gesturing with raised open hands and turned frustrated faces toward "
     f"the sky, {MOSES} standing apart at the frame's edge with his staff, "
     f"his back partly to them, his own weathered face heavy with sorrow. "
     f"{FULLBLEED}"),

    # s04 | Beat 2 | 11.433-14.856s | "...and the venom was the judgment
    # our sin had earned." (continues s03's sentence -- real spoken text
    # per _TIMING.md, not the plan's paraphrase) | Serpents among the
    # rocks and tent-lines, people recoiling
    ("s04_serpents", "",
     f"Among sunbaked rocks and tent-lines at dusk, {LIVE_SERPENTS}, "
     f"{PEOPLE_S04} Both figures are recoiling and drawing back in fear, "
     f"arms raised protectively, bodies twisted away from the rocks, "
     f"tension shown through composition and long shadow, never through a "
     f"visible bite or wound. The tents and rocks behind them are empty "
     f"environment only -- no additional person anywhere in that space. "
     f"{FULLBLEED}"),

    # s05 | Beat 2 | 14.856-18.798s | "I begged Him to take the snakes
    # away. He would not." | Moses alone, kneeling in intercession against
    # open sky (no-figure-adjacent atmosphere, shot-variety floor)
    ("s05_intercession", "moses2",
     f"A no-figure-adjacent atmosphere spread: {MOSES} kneels alone in "
     f"intercession on open barren ground beneath a vast empty sky, his "
     f"staff laid on the sand beside him, head bowed and both hands "
     f"lifted in prayer, utterly alone -- no other person, tent, or "
     f"animal anywhere in the frame. {FULLBLEED}"),

    # s06 | Beat 2 | 18.798-28.105s | "Instead He told me to forge the
    # image... The bitten had only to look -- and live." | Close on
    # Moses's hands at the forge, hammering the bronze serpent into shape
    # (close-up hands, shot-variety floor)
    ("s06_forge", "moses2",
     f"Extreme close on {MOSES} at a small desert forge, hammering a "
     f"serpent shape out of glowing bronze on an anvil stone -- the frame "
     f"fills with his weathered hands and forearms working the metal, "
     f"sparks rising, an ochre-and-copper firelight glow catching his "
     f"knuckles and the coiling half-formed serpent, no other person "
     f"present. {FULLBLEED}"),

    # s07 | Beat 3 | 28.105-36.879s | "I speak now from the far side of my
    # life, by the light that came after -- a night I never saw, when one
    # they called Teacher answered a seeker:" | Moses's face turned toward
    # the horizon/light, older register | lift_away transition begins in
    # this spread's last ~0.4s, finishes crossing into s08
    # REVISED 2026-07-31 (spread-variety fix): the original "mid shot,
    # staff at his side, standing" pose was an undisguised repeat of
    # s01/s03's standing-staff-grip silhouette. Genuinely different
    # blocking: extreme close-up on the face and eyes ONLY, no staff, no
    # hands, no shoulders in frame at all -- see poc_living_sketchbook/
    # spread_variety_lint.py.
    ("s07_horizon", "moses2",
     f"Extreme close-up spread, a much tighter and more intimate crop than "
     f"a waist-up portrait: {MOSES} -- but frame ONLY his face and eyes, "
     f"cropped tight from the top of his brow to his upper beard, filling "
     f"the entire frame corner to corner -- his staff, hands, shoulders, "
     f"and robe are NOT visible anywhere in this crop, only his weathered "
     f"face -- his eyes lifted and turned toward an unseen warm golden "
     f"light source off-frame, deep creases at the corners of his eyes, an "
     f"inward, reflective, aged expression, a hint of night sky just "
     f"visible at the frame's outer edge behind him. {FULLBLEED}"),

    # s08 | Beat 3 | 36.879-43.887s (quote itself 36.879-42.316s) | "And as
    # Moses lifted up the serpent in the wilderness, even so must the Son
    # of man be lifted up:" (red-letter, John 3:14) | THE ONE INSERT PAGE
    # -- Scholar's-Margin typology sheet | ALREADY RENDERED -- see
    # S08_EXISTING above. scene=None => main() skips and reports the path.
    ("s08_typology", None, None),

    # s09 | Beat 3 | 43.887-46.386s | "My bronze was only a shadow." |
    # Moses's face, humble, bronze serpent visually smaller/plainer than
    # the gold page just shown -- hard cut back from s08
    ("s09_shadow", "moses2",
     f"Mid shot: {MOSES}'s face, humble and quiet, his gaze lowered, not "
     f"fixed on the object in his own hand -- he holds the "
     f"{BRONZE_SERPENT} down low at his side, its pole tipped so the "
     f"coiled serpent hangs at waist height or lower, well below his "
     f"shoulder, NEVER raised, lifted, or held up near his face or "
     f"overhead -- small in the frame relative to Moses himself, sitting "
     f"in the shade his own body casts, dull and plain, unremarkable, "
     f"easy to miss, not the first thing the eye finds in the "
     f"composition. {FULLBLEED}"),

    # s10 | Beat 3 | 46.386-52.572s | "They lifted Jesus on a Roman pole,
    # made a curse for us, bearing our judgment in our place." | Christ
    # lifted up, a reverent Golgotha beat -- sacred, restrained, no gore
    ("s10_golgotha", "jesus1",
     f"A reverent Golgotha spread, respectful mid-distance framing: "
     f"{JESUS} lifted up on a plain wooden Roman cross atop a bare hill, "
     f"arms stretched out along the single crossbeam, head bowed low in "
     f"stillness and peace, a plain white loincloth His only garment, no "
     f"visible wound, no blood, no nail shown in close-up -- sacred and "
     f"restrained, never graphic. A darkened sky presses low over the "
     f"hill -- supernatural darkness, NOT a storm, no lightning, no rain, "
     f"no wind-blown debris -- no crowd, no soldiers, no other figure "
     f"anywhere in the frame -- Christ lifted up, alone against the "
     f"darkened sky. {FULLBLEED}"),

    # s11 | Beat 4 | 52.572-57.128s | "So hear me, you who are bitten --
    # that is every one of us." | Moses turns to address the reader
    # directly
    # REVISED 2026-07-31 (spread-variety fix): the original "standing,
    # staff in hand, three-quarter-turned-toward-viewer" pose collided
    # exactly with s07's old blocking (both moses-alone/standing-staff-
    # grip/mid). Genuinely different body position: SEATED, staff set
    # down rather than gripped, hands open, facing the viewer fully
    # straight-on rather than three-quarter -- see poc_living_sketchbook/
    # spread_variety_lint.py.
    # RE-ROLL 2026-07-31 (1st attempt rendered bare feet -- breaks the
    # MOSES canon's "plain leather sandals," never caught in the standing
    # shots where feet stayed out of frame; this seated pose brings feet
    # into view for the first time in the episode, so sandals are now
    # named explicitly).
    ("s11_hearme", "moses2",
     f"A seated direct-address spread, a genuinely different body "
     f"position from any other spread in this episode: {MOSES} sits low "
     f"on a flat sunbaked rock, leaning forward with his forearms resting "
     f"on his knees, his staff laid flat on the ground beside him rather "
     f"than held or gripped, both hands open and empty, turned fully to "
     f"face the viewer straight-on -- not a three-quarter profile -- his "
     f"weathered face open, searching, and close to the frame's "
     f"foreground -- his plain leather sandals clearly visible on both "
     f"feet, the same worn sandals as every other spread, never bare feet "
     f"-- plain wilderness ground behind him. {FULLBLEED}"),

    # s12 | Beat 4 | 57.128-62.936s | "The cure was never in you; it hangs
    # in plain sight, and costs you nothing but a look." | Echo
    # composition: the bronze serpent and the cross both visible/implied
    ("s12_echo", "jesus2",
     f"A symbolic echo composition: the {BRONZE_SERPENT} stands upright "
     f"in the near foreground, and beyond it, smaller in the distance yet "
     f"clearly visible, {JESUS} lifted up on a plain wooden cross against "
     f"an open sky -- both hang in plain sight within the same single "
     f"unbroken view, nothing hidden, nothing obscured. {FULLBLEED}"),

    # s13 | Beat 4 | 62.936-66.723s | "Lift your eyes to Jesus, lifted up
    # for you." | Christ lifted, radiant, the landing's approach
    ("s13_lifted", "jesus2",
     f"A reverent glorified Golgotha spread, the landing's approach: "
     f"{JESUS} lifted up ON a plain wooden cross, arms outstretched "
     f"along the crossbeam -- the wooden crossbeam and upright post are "
     f"clearly visible and unmistakably support Him, never absent, never "
     f"hidden by cloud or light -- warm gold light pours from and around "
     f"the cross so His form reads as radiant and glorified rather than "
     f"in agony, head lifted rather than bowed, face open toward the "
     f"light -- His feet remain at the foot of the upright post, not "
     f"dangling free in open air -- no visible wound, no blood -- gold "
     f"reserved only for this glory light, never on any other element in "
     f"the frame -- the wooden cross itself stays the clear unmoving "
     f"anchor of the composition even as glory light blazes around it. "
     f"{FULLBLEED}"),

    # s14 | Beat 4 | 66.723-68.297s + >=3.0s hold | "Look, and live." |
    # THE LANDING -- torn-page device, gold light from beneath the tear
    ("s14_landing", "jesus2",
     f"THE LANDING spread: the page itself is torn open in a ragged hole "
     f"near center, radiant warm gold light streaming up from beneath the "
     f"torn page, a small still silhouette of {JESUS} standing within the "
     f"golden light beyond the tear, arms open, sacred stillness -- "
     f"nothing else moves, no other figure, no serpent, no camp, only the "
     f"torn page and the light. {FULLBLEED}"),
]


def run(prompt, out, refs):
    cmd = [HF, "generate", "create", MODEL, "--prompt", prompt,
           "--aspect_ratio", "9:16", "--resolution", "2k", "--wait"]
    for r in refs:
        cmd += ["--image", str(r)]
    p = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    blob = (p.stdout or "") + "\n" + (p.stderr or "")
    urls = re.findall(r'https?://\S+?\.(?:png|jpg|jpeg|webp)', blob) or re.findall(r'https?://\S+', blob)
    if not urls:
        print(f"   no url: {blob.strip()[-250:]}")
        return False
    subprocess.run(["curl", "-s", "-L", urls[-1], "-o", str(out)], check=True)
    return out.exists() and out.stat().st_size > 1000


def resolve_refs(tag):
    refs = []
    if not tag:
        return refs
    if "moses1" in tag:
        refs.append(MOSES_REF)
    if "moses2" in tag:
        refs.append(MOSES_REF)
        if MOSES_REF2.exists():
            refs.append(MOSES_REF2)
    if "jesus1" in tag:
        refs.append(JESUS_REF)
    if "jesus2" in tag:
        refs.append(JESUS_REF)
        if JESUS_REF2.exists():
            refs.append(JESUS_REF2)
    return refs


def main(only=None):
    shots = SHOTS_ALL if only is None else [s for s in SHOTS_ALL if s[0] in only]
    for name, tag, scene in shots:
        if scene is None:
            print(f"[skip] {name} -- already rendered, see {S08_EXISTING}")
            continue
        out = OUT / f"{name}.png"
        if out.exists():
            print(f"[skip] {name}")
            continue
        refs = resolve_refs(tag)
        prompt = STYLE + "\n\nSCENE: " + scene
        print(f"[img] {name} (refs={len(refs)}) ...", flush=True)
        ok = run(prompt, out, refs)
        if not ok:
            time.sleep(5)
            ok = run(prompt, out, refs)
        if ok:
            try:
                cost.record_hf(EPISODE, "short", "stills", MODEL, note=f"[bronzeserpent] {name}")
            except Exception as e:
                print(f"   (ledger skipped: {e})")
            print("   ok")
        else:
            print("   FAILED")
    print(f"[out] {OUT}")


if __name__ == "__main__":
    import sys as _sys
    only = _sys.argv[1].split(",") if len(_sys.argv) > 1 else None
    main(only)
