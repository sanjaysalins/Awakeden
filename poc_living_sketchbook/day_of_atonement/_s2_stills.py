"""living-sketchbook -- Day of Atonement, step 2 (TEST GATE, 3 spreads).

Source: `poc_living_sketchbook/day_of_atonement/_PLAN.md` -- the 76-spread
plan. Follows the exact code pattern of
`poc_living_sketchbook/bronze_serpent_long/_s2_stills.py` (same STYLE
constant, same repo-level cast-bible anchor chaining, same FULLBLEED framing
note, same run()/resolve_refs()/main() shape).

TEST GATE (2026-08-03): 3 spreads before the full 76-spread batch, per the
user's own "small test batch first" choice --
  s13_door_curtain_sl13 -- the ONE style-variant candidate the plan flagged
    (sl13 charcoal-and-eraser), needs an Aaron identity test before it's
    committed; if it drifts, ships in spine style instead, no rebuild needed.
  s27_sprinkling -- multi-anchor chain test: Aaron + the holyofholies world
    anchor + a LORD-glow (no-figure light, ref_library convention) together
    in one frame, not just a standalone character portrait.
  s51_jesus_pivot -- Jesus's FIRST appearance in this episode; once approved
    this becomes the second reference for every later Jesus spread in this
    episode (multi-pose identity lock, SKILL.md sec.2) -- not yet chained
    here since it doesn't exist until this render is approved.

  .venv\\Scripts\\python.exe poc_living_sketchbook/day_of_atonement/_s2_stills.py
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
EPISODE = "LS_DayOfAtonement"
HERE = Path(__file__).resolve().parent
CAST = HERE.parent / "cast"      # repo-level cast-bible (shared across episodes)
WORLD = HERE.parent / "world"    # repo-level object/setting anchors
OUT = HERE / "stills"
OUT.mkdir(parents=True, exist_ok=True)

AARON_REF = CAST / "aaron_ref.png"
MOSES_REF = CAST / "moses_ref.png"
JESUS_REF = CAST / "jesus_ref.png"
TABERNACLE_REF = WORLD / "tabernacle_ref.png"
VEIL_REF = WORLD / "veil_ref.png"
HOLYOFHOLIES_REF = WORLD / "holyofholies_ref.png"
ALTAR_REF = WORLD / "altar_ref.png"
GOAT_REF = WORLD / "goat_ref.png"

REF_MAP = {
    "aaron": AARON_REF, "moses": MOSES_REF, "jesus": JESUS_REF,
    "tabernacle": TABERNACLE_REF, "veil": VEIL_REF,
    "holyofholies": HOLYOFHOLIES_REF, "altar": ALTAR_REF, "goat": GOAT_REF,
}

# Canon text -- pasted VERBATIM from cast/AARON.md and cast/JESUS.md.
AARON = (
    "Aaron: an elderly Hebrew priest of the tribe of Levi, brother of "
    "Moses (Exodus 6:20), eighty-three years old when he became Israel's "
    "first high priest (Exodus 7:7), continuing in that office into "
    "extreme old age until his death at a hundred and twenty-three "
    "(Numbers 33:39) -- an old man in every appearance in this story, "
    "never young or middle-aged. Face geometry: a broad dignified brow, a "
    "straight strong nose, deep-set solemn eyes, full weathered cheeks, a "
    "composed and steady bearing -- a priest's stillness, not a "
    "wanderer's hardness. Hair: close-cropped white hair, cut short and "
    "neat. Beard: full, long, white, carefully kept -- a high priest's "
    "beard, not unkempt. Skin: sun-weathered olive Near-Eastern "
    "complexion, deeply lined at the eyes and brow. Build: a stouter, "
    "more solid frame than a wilderness wanderer's -- upright, dignified, "
    "a man who stands and ministers rather than travels, never frail. "
    "Eyes: dark, grave, holding both authority and a private fear before "
    "the veil. Hands: broad priestly hands, steady in ritual, never "
    "hurried. Garment: the plain holy linen of the Day of Atonement "
    "(Leviticus 16:4) -- a linen coat, linen breeches upon the flesh, a "
    "linen girdle, and a linen mitre, all unadorned white linen, nothing "
    "gold, nothing dyed -- a servant's plainness on the one most set "
    "apart. the SAME man as the reference image(s) -- identical face, "
    "beard, hair, and clothing."
)
MOSES = (
    "Moses: an elderly Hebrew man in his eighties, at the time of the "
    "tabernacle's institution (Exodus 40:17, year 2 after the Exodus) -- "
    "his eye not dim, his natural force not abated (Deuteronomy 34:7), "
    "so drawn upright and vital despite his age, never frail or feeble. "
    "Face geometry: a broad weathered forehead, deep-set eyes beneath "
    "heavy grey brows, hollowed cheeks, a strong jaw beneath the beard. "
    "Hair: long white and grey hair swept back off the forehead, "
    "thinning at the crown. Beard: long, full, white streaked with "
    "iron-grey, a patriarch's beard reaching mid-chest. Skin: "
    "sun-weathered, creased and leathery. Build: an old man's spare, "
    "sinewed frame -- still upright and strong-shouldered, not frail. "
    "Eyes: dark, steady, weighted with authority. Hands: large, veined, "
    "weathered elder's hands. Garment: a plain undyed woolen robe with "
    "a coarse mantle draped over one shoulder, a woven cord girdle at "
    "the waist, plain leather sandals -- a shepherd-prophet's dress, "
    "nothing ornamented. Signature prop: a tall wooden staff, worn "
    "smooth by decades of use. the SAME man as the reference image -- "
    "identical face, beard, hair, and clothing."
)
JESUS = (
    "Jesus: a Judean man in his early thirties. Face geometry: a strong "
    "straight nose, defined cheekbones, a broad calm forehead, an angular "
    "jaw beneath the beard. Hair: long dark wavy hair falling past the "
    "shoulders, parted center. Beard: short, close-cropped, dark, "
    "well-kept. Skin: sun-weathered olive Mediterranean complexion. "
    "Build: lean and wiry-strong, a carpenter's and traveler's frame. "
    "Eyes: warm deep brown, level and calm, looking in the same "
    "direction, never wide or staring. Hands: strong, calloused, a "
    "craftsman's hands. Garment: simple undyed homespun ankle-length "
    "tunic with a woven cord sash, leather sandals. the SAME man as the "
    "reference image(s) -- identical face, beard, hair, and clothing."
)
VEIL = (
    "the great inner veil of the tabernacle: a massive hanging curtain "
    "the SAME exact curtain design, weave, and colors as the reference "
    "image -- deep blue-violet and dusky crimson woven fabric hung from "
    "four gold-capped pillars, worked with ancient composite cherubim "
    "exactly as in the reference image: a winged lion-sphinx figure in "
    "profile, a robed winged figure with crossed wings bowing its head, "
    "and a robed winged figure in a head-covering -- Ezekiel-style "
    "ancient composite forms with adult solemn faces. This is NEVER a "
    "red-and-gold ornamental tapestry, and there are NEVER small chubby "
    "Western cherub-babies, cupids, or putti of any kind anywhere on it."
)
LORD_GLOW = (
    "the presence of the LORD: no figure, no face, no human or angelic "
    "form of any kind -- only a low radiant golden cloud-glow, warm and "
    "even, filling the space with light and shadow, felt as an "
    "overwhelming presence rather than seen as a person."
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
# sl13 charcoal-and-eraser, verbatim from .claude/skills/living-sketchbook/STYLE_LAB.md #13
STYLE_SL13 = (
    "Editorial documentary sketch illustration on aged warm cream paper: "
    "soft charcoal laid down as broad smudged tone across the whole "
    "sheet, then the image LIFTED OUT with a kneaded eraser -- highlights "
    "are erased, not painted. Visible fingerprints, smears, dust and "
    "hand-drag across the surface. Minimal ink accents, almost no colour "
    "beyond a single muted ink-red note. Narrow torn-paper margin. "
    "Completely wordless image -- no lettering, numerals or captions "
    "anywhere."
)
# sl12 scratchboard inversion, verbatim from STYLE_LAB.md #12 -- IDENTITY TEST
# ONLY (spread 8 candidate), not yet an adopted swap.
STYLE_SL12 = (
    "Editorial documentary sketch illustration inverted: white and pale "
    "ochre linework scratched out of a deep ink-black ground, scratchboard "
    "technique, fine incised hatching building form out of darkness. The "
    "aged paper texture shows only as a narrow torn margin around a dense "
    "black field. One accent of gold leaf. Completely wordless image -- no "
    "lettering, numerals or captions anywhere."
)
# sl10 overhead plan, verbatim from STYLE_LAB.md #10 -- ADOPTED for s07
# (crowd scale/isolation beat), reversing the earlier over-cautious
# rejection now that camera dynamism is being taken seriously.
STYLE_SL10 = (
    "Editorial documentary sketch illustration on aged warm cream paper: "
    "strict top-down overhead view, figures seen only as compressed "
    "shapes and their long cast shadows, the ground reading as an "
    "abstract field of texture and pattern, dry precise ink linework, "
    "restrained wash, soft raking museum light. Narrow torn-paper "
    "margin. Completely wordless image -- no lettering, numerals, "
    "coordinates, scale bars, or captions anywhere."
)
NADAB_ABIHU = (
    "Nadab and Abihu, two adult Hebrew priests in their thirties, sons of "
    "Aaron -- dressed in plain priestly linen coats similar in cut to "
    "their father's ceremonial dress but without a mitre. Clearly two "
    "distinct individuals, never twins or duplicates: one broader-built "
    "with a fuller short beard, the other leaner with a thinner beard and "
    "different hair length. Each holds a bronze censer from which strange "
    "fire glows unnaturally bright and wrong-colored -- not the sacred "
    "altar-fire."
)
FIT_MAN = (
    "an anonymous fit man, an ordinary wilderness-worn Hebrew in his "
    "thirties in a plain undyed tunic, unnamed and never repeated as a "
    "named character -- a servant's plain competence, no distinguishing "
    "features worth remembering"
)
PEOPLE = (
    "the assembled nation of Israel: ordinary wilderness-worn Hebrew men, "
    "women, and children in plain undyed tunics and mantles, unnamed and "
    "never repeated as named characters -- AT MOST three faces rendered "
    "with any individual detail anywhere in the frame, count them: no "
    "more than three -- every other figure present is turned away, "
    "downcast, or held in soft shadow so no further face reads as "
    "distinct. All hushed and still, faces turned toward the tabernacle, "
    "holding their breath."
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

# (name, style, refs-tag, scene)
SHOTS_TEST = [
    # spread 13 | Beat 2 | 65.6-72.3s | Aaron at the tabernacle door-curtain,
    # forbidden to mourn -- STYLE VARIANT TEST (sl13, per _PLAN.md sec.6)
    ("s13_door_curtain_sl13", STYLE_SL13, "aaron,tabernacle",
     f"{AARON} stands alone at the plain needlework door-curtain of the "
     f"tabernacle entrance (NOT the inner cherubim veil -- a simpler "
     f"undecorated hanging), gripping the edge of his own robe with one "
     f"hand as though about to tear it in grief, then stopping himself, "
     f"forbidden to mourn -- his face rigid with held-back grief, "
     f"forbidden restraint written in his posture. {FULLBLEED}"),

    # spread 27 | Beat 3 | 171.4-175.44s | Sprinkling before the mercy
    # seat, alone in the dark chamber, cloud-glow -- multi-anchor chain test
    ("s27_sprinkling", STYLE, "aaron,holyofholies",
     f"Inside the Holy of Holies: a small, perfectly square, windowless "
     f"chamber, utterly dark except for a low golden cloud-glow filling "
     f"the space. {AARON} kneels alone before the ark, one hand "
     f"sprinkling blood from a plain basin toward the gold mercy seat "
     f"whose two cherubim wings stretch up and inward above it -- "
     f"{LORD_GLOW}. Nothing else stands in this room -- no other "
     f"furniture, no chair, bare shadow on every side. {FULLBLEED}"),

    # spread 51 | Beat 6 | 368.3-382.08s | JESUS 1 -- the pivot, first
    # Jesus appearance in this episode
    ("s51_jesus_pivot", STYLE, "jesus",
     f"{JESUS} stands radiant, entering a threshold of golden light -- "
     f"the true High Priest passing once for all into the holy place, "
     f"gold leaf light gathering around His form, calm and resolute, "
     f"looking forward -- no crowd, no other figure, the gold register "
     f"of His glory beginning to fill the frame around Him. {FULLBLEED}"),
]

# Batch 1: spreads 1-10 (Beat 1 vesting rite + Beat 2 opening), all spine
# style per _PLAN.md sec.6's reasoning -- plus one extra sl12 IDENTITY TEST
# on spread 8 (a genuine second-candidate threshold-into-dark beat), not a
# committed swap, just data on whether Aaron survives that variant too.
SHOTS_BATCH1 = [
    # spread 1 | Beat 1 | 0.00-3.2s | Cold open: Aaron's face arrives
    ("s01_cold_open", STYLE, "aaron",
     f"Extreme close-up on {AARON}'s face alone, filling the frame corner "
     f"to corner, solemn and direct, meeting the viewer's gaze -- the "
     f"very first image of the film. {FULLBLEED}"),

    # spread 2 | Beat 1 | 3.2-9.3s | Wide: the tabernacle in its courtyard
    # -- CAMERA: low angle from ground level near the outer fence, looking
    # UP at the tabernacle, foreground fence-posts as a depth layer
    ("s02_tabernacle_wide", STYLE, "tabernacle",
     f"LOW-ANGLE view from ground level just outside the linen courtyard "
     f"fence, camera looking steeply UP past a foreground row of fence "
     f"posts (strong depth layering, posts large and dark in the near "
     f"foreground) toward the tabernacle rising beyond -- the structure "
     f"looming and imposing against the sky, desert light, no figure "
     f"present -- the place no other man was permitted to enter. "
     f"{FULLBLEED}"),

    # spread 3 | Beat 1 | 9.3-13.9s | The golden garments laid aside --
    # CAMERA: high angle looking DOWN at the garments, Aaron's hands
    # entering frame from below -- a "letting go" composition
    ("s03_golden_garments", STYLE, "aaron",
     f"HIGH-ANGLE view looking steeply DOWN onto a stone ledge, "
     f"{AARON}'s hands entering the frame from the bottom edge, just "
     f"having laid aside his golden high-priestly garments of glory and "
     f"beauty (Exodus 28:2): a blue robe hemmed with pomegranates and "
     f"small gold bells, a jewelled breastplate, a gold-and-linen "
     f"ephod, and a small plain gold plate bound to a linen mitre by a "
     f"blue cord, all arranged below the camera -- these golden "
     f"garments appear only in this one moment of the film, no text or "
     f"lettering visible anywhere on them. {FULLBLEED}"),

    # spread 4 | Beat 1 | 13.9-22.2s | Aaron in plain linen, tying girdle
    # -- CAMERA: low angle from waist height looking UP, more solemn/
    # heroic than a flat portrait
    ("s04_donning_linen", STYLE, "aaron",
     f"LOW-ANGLE view from waist height looking UP at {AARON}, now "
     f"dressed in the plain holy linen of the Day of Atonement, tying "
     f"the linen girdle at his waist, the tent canopy and open sky "
     f"visible above him, a plain bronze laver of water in the "
     f"foreground at camera level -- like a servant, a man with nothing "
     f"to boast of. {FULLBLEED}"),

    # spread 5 | Beat 1 | 22.2-26.8s | Walking toward the veil, gloom
    ("s05_walking_to_veil", STYLE, "aaron,veil",
     f"{AARON} walks alone through the dim gold-walled Holy Place toward "
     f"the great inner veil ahead of him, small against its height, his "
     f"face tense with dread -- the space around him mostly shadow, only "
     f"the distant veil catching any light. Aaron is the ONLY person "
     f"present in this scene -- the cherubim visible are exclusively "
     f"woven figures within the curtain's own fabric, flat and "
     f"two-dimensional as embroidery, never standing separately on the "
     f"floor as a third figure in the room. {FULLBLEED}"),

    # spread 6 | Beat 1 | 26.8-34.5s | Behind the curtain: mercy seat,
    # cloud-glow, room otherwise EMPTY -- CAMERA: low, near floor level,
    # looking UP at the ark so the glow towers rather than sitting flat
    ("s06_holy_of_holies_empty", STYLE, "holyofholies",
     f"LOW-ANGLE view from near floor level looking UP at the ark, "
     f"inside the Holy of Holies: a small, perfectly square, windowless "
     f"chamber, utterly dark except for a low golden cloud-glow towering "
     f"above the ark and its two gold cherubim wings stretched upward, "
     f"the glow filling the upper frame -- {LORD_GLOW} -- the room "
     f"otherwise entirely EMPTY, no figure present. {FULLBLEED}"),

    # spread 7 | Beat 1 | 34.5-39.4s | Wide: the whole nation outside --
    # ADOPTED sl10 overhead style (scale/isolation is exactly its own
    # manifest signal; reversing the earlier over-cautious rejection)
    ("s07_nation_outside", STYLE_SL10, "",
     f"Strict top-down overhead view of the tabernacle's linen courtyard "
     f"and the vast crowd gathered outside its fence -- the whole "
     f"multitude compressed into small dark shapes and long cast "
     f"shadows on the sand, no individual face readable at this "
     f"distance, the tabernacle's rectangular footprint and courtyard "
     f"fence-line visible at the frame's center, emphasizing the sheer "
     f"scale of the nation against the one small sacred structure."),

    # spread 8 | Beat 1 | 39.4-46.4s | Curtain falls shut, close on
    # Aaron's face in the dark -- ADOPTED sl12 (already identity-tested
    # this session; the genuine second candidate, no longer held back)
    ("s08_curtain_shut", STYLE_SL12, "aaron,veil",
     f"Close on {AARON}'s face, scratched out of the black ground in "
     f"pale incised linework, just after the great veil has fallen shut "
     f"behind him, only a thin scratched line of light catching his "
     f"features, his expression tense, uncertain he will come out "
     f"alive."),

    # spread 9 | Beat 2 | 46.4-49.6s | Aaron's grief, close
    ("s09_grief_close", STYLE, "aaron",
     f"Close on {AARON}'s face, eyes lowered in raw private grief, a "
     f"single held breath of sorrow. {FULLBLEED}"),

    # spread 10 | Beat 2 | 49.6-54.3s | Nadab and Abihu with censers,
    # strange fire (multi-stage hard cut, stage 1 of 2) -- CAMERA: low
    # angle near ground level looking UP through the flames, ominous
    ("s10_strange_fire", STYLE, "",
     f"LOW-ANGLE view from near ground level looking UP through the "
     f"rising flames toward {NADAB_ABIHU}, standing side by side before "
     f"the altar, each lifting a bronze censer high above the camera -- "
     f"the flames looming large in the foreground, the moment just "
     f"before judgment falls, tension and wrongness in the glow. "
     f"{FULLBLEED}"),
]


def run(prompt, out, refs):
    cmd = [HF, "generate", "create", MODEL, "--prompt", prompt,
           "--aspect_ratio", "16:9", "--resolution", "2k", "--wait"]
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
    for t in tag.split(","):
        t = t.strip()
        if t and REF_MAP.get(t) and REF_MAP[t].exists():
            refs.append(REF_MAP[t])
    return refs


# Batch 2: spreads 11-33 (rest of Beat 2 + all of Beat 3, the ritual
# itself), skipping 13 and 27 (already rendered in earlier batches).
SHOTS_BATCH2 = [
    # spread 11 | Beat 2 | 54.3-58.9s | Struck down (multi-stage, stage 2 of 2 w/ 10)
    ("s11_struck_down", STYLE, "",
     f"A sudden burst of overwhelming light and fire falling from above "
     f"onto the two censers dropped in the sand -- {LORD_GLOW} -- NO "
     f"human figure visible in the frame, no gore, only the fire and the "
     f"aftermath of judgment. {FULLBLEED}"),

    # spread 12 | Beat 2 | 58.9-65.6s | The cousins carrying the bodies out
    # -- CAMERA: low angle, slightly ahead of the procession looking back
    # at it, tent poles receding into deep foreground/background depth
    ("s12_bodies_carried_out", STYLE, "tabernacle",
     f"LOW-ANGLE view from slightly ahead of the procession looking "
     f"back toward it, a row of tent poles receding sharply from near "
     f"foreground to far background for strong depth. EXACTLY two "
     f"figures and no more, count them: two grown Hebrew men in plain "
     f"tunics carrying a linen-wrapped body between them out of the "
     f"camp, somber, restrained, no wound or blood visible, the "
     f"wrapping fully concealing -- there is no third or fourth person "
     f"visible anywhere in the frame. {FULLBLEED}"),

    # spread 14 | Beat 2 | 72.3-82.0s | Aaron's hand at the veil's edge
    ("s14_hand_at_veil", STYLE, "aaron,veil",
     f"Extreme close-up on {AARON}'s hand trembling at the very edge of "
     f"the great veil, fingers just touching the woven fabric, not yet "
     f"pulling it back -- his face barely visible at the frame's edge, "
     f"the focus entirely on the hand. {FULLBLEED}"),

    # spread 15 | Beat 2 | 82.0-87.92s | Moses comes bearing the word --
    # CAMERA: tight, slightly low angle, strong side-lighting for weight
    ("s15_moses_charge", STYLE, "aaron,moses",
     f"Tight two-shot, camera slightly LOW looking up at both faces, "
     f"strong raking side-light carving deep shadow across them: "
     f"{MOSES} stands facing {AARON}, two old brothers close together, "
     f"Moses's hand resting on Aaron's shoulder as he delivers a solemn "
     f"charge -- the weight of the word passing between them, no one "
     f"else present. {FULLBLEED}"),

    # spread 16 | Beat 2 | 87.92-106.24s | [the LORD] Lev 16:2 -- Illuminated
    # Rubric card, whole-arrival, LONGEST single card of the film
    ("s16_lords_charge_card", STYLE, "holyofholies",
     f"Inside the Holy of Holies, the golden cloud-glow above the ark "
     f"burning brighter and more intense than any other appearance of "
     f"it in the film -- {LORD_GLOW} -- the room otherwise empty, "
     f"reserved as background art for the film's central formal verse "
     f"card. {FULLBLEED}"),

    # spread 17 | Beat 2 | 106.24-112.3s | Aaron squared at the veil --
    # CAMERA: low angle, heroic framing against the towering curtain
    ("s17_squared_at_veil", STYLE, "aaron,veil",
     f"LOW-ANGLE view looking UP at {AARON}, standing squarely facing "
     f"the great veil which towers above and behind him filling the "
     f"upper frame, shoulders set, resolved to his charge -- to stand "
     f"at the veil for the people and not be consumed. {FULLBLEED}"),

    # spread 18 | Beat 2 | 112.3-122.3s | Aaron with the basin, own sin
    # first -- CAMERA: side profile silhouette against the altar's glow.
    # FIXED: 1st roll rendered a SECOND priest handing Aaron the basin --
    # wrong, the whole point is he does this himself, alone. Tightened to
    # explicitly ban a second figure.
    ("s18_own_sin_first", STYLE, "aaron",
     f"Side-profile view, {AARON} kneeling alone in silhouette against "
     f"the warm glow of the bronze altar beyond him, his own two hands "
     f"holding a plain basin of blood for his own sin offering -- the "
     f"mediator who is himself a sinner, his face humble and grave, "
     f"never a substitute. Aaron is the ONLY person present -- no "
     f"attendant, no second priest, no other figure of any kind "
     f"anywhere in the frame, only Aaron and the basin he holds in his "
     f"own hands. {FULLBLEED}"),

    # spread 19 | Beat 2 | 122.3-133.28s | The bronze altar mid-ministry --
    # revised after NSFW filter rejection on the original blood-at-base
    # wording; smoke/ash conveys ongoing ministry instead. CAMERA: low
    # 3/4 angle, smoke dominating more of the frame
    ("s19_altar_ministry", STYLE, "altar,aaron",
     f"LOW 3/4-ANGLE view, {AARON} ministering at the bronze altar, one "
     f"hand extended over it in a ministering gesture, thick smoke and "
     f"ash billowing upward to dominate the upper half of the frame -- "
     f"ritual, reverent, no wound or blood visible anywhere. "
     f"{FULLBLEED}"),

    # spread 20 | Beat 2 | 133.28-137.20s | Verse card bg: Lev 17:11
    ("s20_blood_atonement_card", STYLE, "altar",
     f"The bronze altar alone, smoke drifting upward, no figure present "
     f"-- reserved as background art for the verse 'it is the blood "
     f"that maketh an atonement for the soul.' {FULLBLEED}"),

    # spread 21 | Beat 2 | 137.20-141.2s | The goat's innocent face, close
    ("s21_goat_innocent", STYLE, "goat",
     f"Extreme close-up on the goat's calm, innocent face alone, filling "
     f"the frame -- foreshadowing, before anything has happened to it. "
     f"{FULLBLEED}"),

    # spread 22 | Beat 3 | 141.2-148.5s | Close on Aaron's old hands
    ("s22_ritual_hands", STYLE, "aaron",
     f"Extreme close-up on {AARON}'s old, weathered hands alone, at "
     f"rest, ritual muscle-memory in their stillness -- could do this "
     f"work in the dark after so many years. {FULLBLEED}"),

    # spread 23 | Beat 3 | 148.5-156.08s | The two goats brought before
    # Aaron -- CAMERA: elevated, slightly overhead angle looking down the
    # line, diagonal composition instead of a flat frontal lineup
    ("s23_two_goats_brought", STYLE, "aaron,goat",
     f"Elevated view, camera slightly overhead looking down at a "
     f"DIAGONAL line running from near foreground to far background: "
     f"{AARON} stands before two identical goats brought for the "
     f"people's sin offering -- ONE design, both animals, deliberately "
     f"indistinguishable from each other. EXACTLY two handlers and no "
     f"more, count them: (1) a man holding the first goat's tether; "
     f"(2) a man holding the second goat's tether -- there is no third "
     f"or fourth person present besides Aaron and these two handlers. "
     f"{FULLBLEED}"),

    # spread 24 | Beat 3 | 156.08-163.36s | Verse card bg: Lev 16:8, the lots
    ("s24_lots_card", STYLE, "aaron,goat",
     f"Close on {AARON}'s open palm holding two plain lots, the two "
     f"goats soft and out of focus behind -- reserved as background art "
     f"for the verse describing the casting of lots. {FULLBLEED}"),

    # spread 25 | Beat 3 | 163.36-167.4s | The slaying at the altar (stage
    # 1 of 3) -- CAMERA: low, from ground level, the raised knife against
    # open sky for heightened tension
    ("s25_slaying_stage1", STYLE, "altar,aaron,goat",
     f"LOW-ANGLE view from near ground level, {AARON} kneeling at the "
     f"bronze altar with the first goat, a plain knife raised in hand "
     f"silhouetted against open sky above him, the moment poised just "
     f"before the act -- wound-FREE, no blood shown yet, restrained and "
     f"reverent, staging only. {FULLBLEED}"),

    # spread 26 | Beat 3 | 167.4-171.4s | Basin through the veil (stage 2 of 3)
    ("s26_through_veil_stage2", STYLE, "aaron,veil",
     f"{AARON}, half-swallowed by the great veil's heavy fabric as he "
     f"passes through it into the thick dark beyond, a plain basin held "
     f"close to his chest -- a threshold shot, his form already fading "
     f"into shadow on the far side. {FULLBLEED}"),

    # spread 28 | Beat 3 | 175.44-182.16s | Verse card bg: Lev 16:15
    ("s28_bring_blood_card", STYLE, "holyofholies",
     f"The dark interior of the Holy of Holies, the cloud-glow steady "
     f"above the ark, no figure present -- reserved as background art "
     f"for the verse 'bring his blood within the vail.' {FULLBLEED}"),

    # spread 29 | Beat 3 | 182.16-188.1s | ACTING SPREAD: hands on the
    # goat -- CAMERA: low, intimate angle, strong side-light on the hands
    ("s29_hands_on_goat", STYLE, "aaron,goat",
     f"LOW, intimate angle close on the hands and heads only, strong "
     f"raking side-light: {AARON} lays both his hands firmly upon the "
     f"live goat's head, the rite's iconic gesture -- his face solemn, "
     f"the goat calm beneath his hands. {FULLBLEED}"),

    # spread 30 | Beat 3 | 188.1-193.92s | The confession, different framing
    ("s30_confession", STYLE, "aaron,goat",
     f"{AARON}'s bowed face close, eyes shut, mouth moving in "
     f"confession, hands still resting on the goat's head just visible "
     f"below -- a different framing from the hands-laying moment, more "
     f"intimate, on his face. {FULLBLEED}"),

    # spread 31 | Beat 3 | 193.92-215.44s | Verse card bg LIVE-WRITE: Lev 16:21
    ("s31_confession_card", STYLE, "aaron,goat",
     f"{AARON}'s hands still resting on the live goat's head, a quiet "
     f"held moment, soft and slightly hazy as though ghosted -- reserved "
     f"as background art for the film's longest lettered verse card. "
     f"{FULLBLEED}"),

    # spread 32 | Beat 3 | 215.44-223.68s | The goat led away, receding
    ("s32_goat_led_away", STYLE, "goat",
     f"Wide shot: {FIT_MAN} leads the goat away from the camp by a "
     f"tether, the two figures small and receding into a vast empty "
     f"wilderness horizon, growing smaller into the distance. "
     f"{FULLBLEED}"),

    # spread 33 | Beat 3 | 223.68-229.92s | Verse card bg: Lev 16:22, same
    # horizon now EMPTY (continuity pair with 32)
    ("s33_empty_horizon_card", STYLE, "",
     f"The SAME vast wilderness horizon as the previous shot, composed "
     f"identically, but now completely empty -- no goat, no man, "
     f"nothing but sand and distance -- reserved as background art for "
     f"the verse 'unto a land not inhabited.' {FULLBLEED}"),
]

# Batch 3: spreads 34-38 (Beat 4, "the riddle") -- camera-angle discipline
# applied from the FIRST prompt this time, not as an after-the-fact fix.
SHOTS_BATCH3 = [
    # spread 34 | Beat 4 | 229.92-239.20s | Riddle recap, MV vignette --
    # CAMERA: eye-level close on Aaron, but the two memory-vignettes sit
    # at DIFFERENT depths behind him (real layering, not a flat diptych)
    ("s34_riddle_recap", STYLE, "aaron,goat",
     f"Eye-level close on {AARON}'s turning, thoughtful face in the near "
     f"foreground -- behind him, two soft hazy memory-vignettes at "
     f"DIFFERENT depths (one nearer and larger, one farther and "
     f"smaller, true layered depth not a flat side-by-side split): the "
     f"goat at the altar, and the goat receding into the wilderness. "
     f"{FULLBLEED}"),

    # spread 35 | Beat 4 | 239.20-246.24s | Verse card bg: Lev 16:5, two
    # goats together -- CAMERA: slightly elevated, looking down at both
    # goats standing side by side, emphasizing ONE offering/two creatures
    ("s35_two_kids_card", STYLE, "goat",
     f"Slightly elevated view looking down at two identical goats "
     f"standing calmly side by side, close together -- reserved as "
     f"background art for the verse 'two kids of the goats for a sin "
     f"offering,' no figure present. {FULLBLEED}"),

    # spread 36 | Beat 4 | 246.24-255.4s | Night, the two lots -- REDESIGNED
    # 2026-08-04 (Fable): the original open-palm framing risked invented
    # casting/rolling motion at animation stage AND was the 4th close-on-
    # hands shot in the film. New concept "Two Shadows, One Flame": the
    # lots lie flat and still (unambiguously at rest), the doubled shadow
    # carries the "why two?" question instead of the hand.
    ("s36_two_shadows_one_flame", STYLE, "aaron",
     f"Table-level view across the surface of a low wooden chest inside "
     f"Aaron's dark tent at night: in sharp foreground, two plain lots "
     f"lie flat and still side by side on the wood, a single small clay "
     f"lamp just beside them throwing each lot its own long ink-blue "
     f"shadow stretching toward the camera -- the doubled shadow is the "
     f"image's real subject. In the soft middle distance beyond the "
     f"chest, {AARON} sits dim and half-lost in shadow, hands folded "
     f"quietly in his lap, watching. The rest of the tent falls to "
     f"near-total darkness. {FULLBLEED}"),

    # spread 37 | Beat 4 | 255.4-264.6s | Split composition: altar vs
    # empty horizon -- CAMERA: literal diptych per the plan, but each
    # half gets its own foreground/background depth, not a flat block
    ("s37_split_two_things", STYLE, "altar",
     f"A vertical split composition, two halves in one frame: LEFT half "
     f"-- the bronze altar close in the foreground, smoke rising, "
     f"warm firelight; RIGHT half -- a vast empty wilderness horizon "
     f"stretching into cool distance, no figure. Each half reads with "
     f"its own real depth, not a flat panel. {FULLBLEED}"),

    # spread 38 | Beat 4 | 264.6-269.4s | Aaron walking home at dusk --
    # CAMERA: low, from ground level, small figure against a layered
    # receding dusk landscape
    ("s38_walking_home_dusk", STYLE, "aaron",
     f"LOW-ANGLE view from near ground level, {AARON} small and alone "
     f"in the middle distance, walking at dusk, a long shadow stretching "
     f"toward camera -- the tent-camp a layered silhouette receding "
     f"behind him, warm dying light low on the horizon. {FULLBLEED}"),
]

# Batch 4: spreads 39-48 (rest of Beat 5 "the honest confession" + start of
# Beat 6 "the turn to Christ") -- camera-angle discipline applied from the
# FIRST prompt, per the two standing rules from this session.
SHOTS_BATCH4 = [
    # spread 39 | Beat 5 | 269.4-276.9s | Direct-address honesty register --
    # CAMERA: deliberately EYE-LEVEL, not low/heroic or high/small -- this
    # beat is Aaron meeting the viewer as an equal witness, not glorified
    # or diminished
    ("s39_honesty_close", STYLE, "aaron",
     f"EYE-LEVEL close on {AARON}'s face, meeting the viewer's gaze "
     f"directly and plainly, an old man's honest unguarded expression, "
     f"no ornament or glory in the framing -- a witness speaking plainly, "
     f"not a hero posed. {FULLBLEED}"),

    # spread 40 | Beat 5 | 276.9-288.0s | The people going home CLEAN,
    # real relief -- CAMERA: low, intimate, AMONG the crowd at their own
    # height (deliberate contrast with s07's distant top-down nation shot)
    ("s40_people_home_clean", STYLE, "",
     f"LOW-ANGLE view from within the crowd itself, at the height of the "
     f"people. EXACTLY TWO figures with any face detail, count them: "
     f"(1) one ancient Hebrew woman with a loose plain undyed cloth "
     f"draped over her hair and shoulders, smiling gently, at ease; "
     f"(2) one ancient Hebrew man with plain uncovered dark hair and a "
     f"short beard, smiling, at ease -- both wearing loose plain undyed "
     f"wilderness robes with a woven cord or cloth sash, ancient "
     f"Near-Eastern wilderness dress ONLY, no head coverings other than "
     f"loose draped cloth, absolutely no fitted skullcaps or caps of any "
     f"kind, nothing resembling modern ceremonial dress of any era. "
     f"Every other person present in the frame is a plain unlit "
     f"silhouette or fully turned away, with no facial detail rendered "
     f"at all -- no third distinct face anywhere. Warm evening "
     f"firelight, relief plainly visible in relaxed shoulders and "
     f"loosened posture -- the fear of the day genuinely lifted, not "
     f"tense or anxious. {FULLBLEED}"),

    # spread 41 | Beat 5 | 288.0-297.2s | MV: the rite repeated across
    # years, three vignettes by season/light -- CAMERA: eye-level on
    # Aaron foreground, three vignettes staggered at different depths
    # behind him, each lit differently (dawn cool / dusk warm / haze soft)
    ("s41_repetition_vignettes", STYLE, "aaron,goat",
     f"Eye-level on {AARON}'s weathering, resigned face in the near "
     f"foreground -- behind him, three soft hazy memory-vignettes at "
     f"THREE DIFFERENT depths (nearest, middle, farthest -- true layered "
     f"staggering, never a flat row), each of the same rite at the altar "
     f"with the goat but lit differently: one in cool pale dawn light, "
     f"one in warm dying dusk light, one hazy and indistinct as though "
     f"from further back in memory -- the same act, year upon year. "
     f"{FULLBLEED}"),

    # spread 42 | Beat 5 | 297.2-307.5s | Object insert: basin + linen
    # ready again -- CAMERA: high, overhead, looking straight DOWN, an
    # inventory/insert framing distinct from any figure shot
    ("s42_basin_linen_ready", STYLE, "",
     f"Strict overhead view looking straight DOWN onto a stone ledge: a "
     f"plain bronze basin, scrubbed bright and empty, beside a neatly "
     f"folded stack of plain white linen garments, both set out and "
     f"ready again -- no figure present, only the objects waiting, "
     f"quiet and orderly. {FULLBLEED}"),

    # spread 43 | Beat 5 | 307.5-314.0s | Old Aaron at night, unspoken
    # fear -- REDESIGNED 2026-08-04 (Fable): was the 1st of 4 near-
    # identical face-close shots in a row (43/44/46/47). New concept
    # "The Fear on the Tent Wall": the dread is carried by a projected
    # shadow at monumental scale, not a lit face -- also gives the
    # downstream candle-only device (this spread's own tagged device) a
    # real subject to close down around.
    ("s43_shadow_on_tent_wall", STYLE, "aaron",
     f"WIDE, LOW-ANGLE interior view pulled back from ground level: "
     f"{AARON}, small at the right of frame, sits upright on his mat in "
     f"a priest's stillness, profile, mitre set aside, a single small "
     f"clay lamp burning on the ground before him -- the lamp throws "
     f"his seated shadow immense and distorted up the sloping tent "
     f"canvas behind him, hunched and looming far larger than the man "
     f"himself, its head bent low where his own is held straight. "
     f"Darkness swallows the rest of the frame -- the fear is the "
     f"shadow, not the face. {FULLBLEED}"),

    # spread 44 | Beat 5 | 314.0-323.9s | The pointing image -- WIDENED
    # 2026-08-04 (Fable): kept the smoke-pointing idea (it's a real
    # device) but pushed the scale WAY out so it doesn't read as a twin
    # of 43/46/47's medium-close framing -- the torn paper edge itself
    # now literalizes "pointing beyond the frame."
    ("s44_pointing_smoke", STYLE, "aaron,altar",
     f"VAST WIDE view, low horizon: the bronze altar sits small at the "
     f"very bottom of the frame, its column of smoke the largest "
     f"element on the page, rising and leaning on a steep diagonal all "
     f"the way up to the torn paper edge at the top of the frame, as "
     f"though continuing beyond the page itself onto the kraft board "
     f"behind it. {AARON}, a small full-length figure beside the "
     f"altar, head tilted back, following the smoke's line upward -- "
     f"his face unreadable at this distance, his posture alone "
     f"carrying the gaze. Muted dawn wash, the smoke in cool graphite "
     f"grey-blue. {FULLBLEED}"),

    # spread 45 | Beat 5 | 323.9-327.0s | Near-silence: Aaron a small
    # silhouette before the veil -- CAMERA: wide, elevated, deliberately
    # SMALL figure (direct contrast with s17's heroic low-angle framing
    # at the same veil)
    ("s45_sign_before_veil", STYLE, "aaron,veil",
     f"WIDE, slightly elevated view, {AARON} reduced to a small dark "
     f"silhouette standing before the great veil, which fills most of "
     f"the towering frame around him -- deliberately small and quiet, a "
     f"sign pointing beyond himself, not the substance. Aaron is the "
     f"ONLY person present -- no other figure of any kind, human or "
     f"otherwise, stands anywhere at the base of the curtain or "
     f"elsewhere in the frame, only Aaron and the veil. {FULLBLEED}"),

    # spread 46 | Beat 6 | 327.0-334.5s | Aaron aged, the veil unchanged
    # -- REDESIGNED 2026-08-04 (Fable, adapted): Fable's original idea
    # showed Aaron 3 times at staggered ages in one frame -- rejected,
    # conflicts with this episode's own locked rule that Aaron gets ONE
    # unchanging appearance throughout (same reasoning as Moses's
    # retired "younger" anchor), and a triple-age single-character
    # render is a high-failure-risk identity task besides. Kept Fable's
    # real insight (the veil receding to a vanishing point = time
    # itself) but with Aaron rendered ONCE, from behind/in profile --
    # also finally breaks the run of face-close shots.
    ("s46_aged_unchanged_veil", STYLE, "aaron,veil",
     f"WIDE, LOW-ANGLE view from behind and to the side of {AARON} -- "
     f"never a face-close -- his aged, visibly stooped frame small in "
     f"the near foreground, back three-quarter to the camera, one hand "
     f"resting on a staff, looking down the immense receding length of "
     f"{VEIL}, the same curtain and cherubim repeating stage after "
     f"stage into a hazy vanishing point far in the distance, utterly "
     f"unchanged. The corridor is longer than any one lifetime could "
     f"cross. {FULLBLEED}"),

    # spread 47 | Beat 6 | 334.5-342.6s | Cross-time turn -- REDESIGNED
    # 2026-08-04 (Fable) "The Seam of Gold": was the 4th face-close in
    # the run; moved the light-arrival event to room scale instead of
    # half a face, and literalizes the STYLE constant's own "thin strip
    # of gold leaf at one edge" as the arriving light itself -- also the
    # deliberate visual reversal of 43 (there his own lamp's circle
    # closed down; here light from beyond the frame comes to him).
    ("s47_light_arrives", STYLE, "aaron",
     f"WIDE interior view, the tent still holding its old dim blue-grey "
     f"palette everywhere in the frame: {AARON}, full-figure, seated "
     f"upright on his mat at mid-distance, face turned toward the "
     f"frame's right edge. Down the entire right edge of the frame, a "
     f"single thin blade of warm gold light enters through the tent "
     f"seam, laying one narrow warm stripe of light across the floor "
     f"that reaches all the way to his feet -- nothing else in the "
     f"frame is warmed by it yet, his eyes open toward the light. "
     f"{FULLBLEED}"),

    # spread 48 | Beat 6 | 342.6-352.88s | The insufficiency image: the
    # little basin at the foot of the towering veil -- CAMERA: low,
    # basin in extreme near-foreground, veil towering behind for scale
    # disparity
    ("s48_small_basin_towering_veil", STYLE, "veil",
     f"LOW-ANGLE view, a single small plain basin sitting in the "
     f"extreme near foreground, disproportionately tiny against {VEIL} "
     f"towering the entire height of the frame behind it -- no human or "
     f"angelic figure of any kind stands anywhere at the base of the "
     f"curtain or elsewhere in the frame, only the empty basin and the "
     f"vast unfinished curtain. {FULLBLEED}"),
]

# Batch 5: spreads 49, 50, 52, 53 (start of Beat 6's Christ section) --
# skips 51 (already rendered/approved as the Jesus identity-lock ref) and
# 54-61 (multi-vignette Thread Device + new city-gate asset -- own pass).
SHOTS_BATCH5 = [
    # spread 49 | Beat 6 | 352.88-363.36s | DOUBLE verse card bg (Heb
    # 10:3/10:4) -- CAMERA: close DETAIL crop on one cherub panel, not
    # the whole curtain -- this is the 9th veil appearance in the film,
    # needs a genuinely different framing from the previous 8 wide/
    # full-curtain shots
    ("s49_veil_detail_card", STYLE, "veil",
     f"A medium view on a single panel of {VEIL} from its gold-capped "
     f"pillar-hooks at the top down to its hem at the floor, the "
     f"panel's own crossed-wing cherub woven FLAT into the fabric "
     f"exactly as part of the weave, thread and dye, not a separate "
     f"three-dimensional being standing apart from the curtain -- soft "
     f"dim raking light, no figure present, the fabric utterly still. "
     f"Reserved as calm background art for the film's two-verse "
     f"Scribed Ink card. {FULLBLEED}"),

    # spread 50 | Beat 6 | 363.36-368.3s | THE SHADOW, no-figure
    # atmosphere -- CAMERA: elevated, looking down the shadow's length
    # stretching toward camera from an unseen source -- distinct from
    # the film's other wide desert horizons (32/33/38)
    ("s50_the_shadow", STYLE, "",
     f"Elevated view looking down across open wilderness sand at dusk, "
     f"warm dying light raking low across the ground -- a single long "
     f"dark shadow stretches from just beyond the frame's own edge "
     f"toward the camera, its source entirely unseen, the rest of the "
     f"vast sand otherwise empty and undisturbed. No figure, no object, "
     f"only the shadow and the waiting ground. {FULLBLEED}"),

    # spread 52 | Beat 6 | 382.08-392.48s | Illuminated Rubric bg, Jesus
    # entering -- CAMERA: wide, formal, symmetrical threshold framing,
    # deliberately distinct from s51's close push-in (this is reserved
    # background for a formal dropped-cap card, not the pivot moment
    # itself)
    ("s52_jesus_entering_formal", STYLE, "jesus",
     f"WIDE, formal, symmetrical view from just inside a grand gold-"
     f"walled passage that fills the ENTIRE frame edge to edge -- its "
     f"gold walls occupy the full left and right of the frame in "
     f"architectural perspective lines receding toward the far "
     f"threshold, no blank margin anywhere. {JESUS} entering fully "
     f"into frame through that far threshold, centered, full figure "
     f"visible head to foot, gold light gathering low around His feet "
     f"and rising -- calm and resolute, a wide ceremonial framing left "
     f"open for a formal dropped-cap verse card. {FULLBLEED}"),

    # spread 53 | Beat 6 | 392.48-399.0s | The cross, reverent restrained
    # -- CAMERA: extreme wide, low horizon, small solitary silhouette
    # against a vast darkened sky -- matches this project's established
    # crucifixion treatment (darkness not storm, nothing graphic)
    ("s53_the_cross", STYLE, "jesus",
     f"VAST WIDE view, low horizon: a single cross stands small and "
     f"solitary in silhouette against a vast sky gone unnaturally dark "
     f"at midday, as though the sun itself has been blotted out -- a "
     f"flat, heavy, even blackness settling over the whole sky, "
     f"perfectly still, NOT storm clouds, NOT billowing weather, no "
     f"wind, no rain, no roiling cloud shapes -- an eerie, supernatural "
     f"dimming of the light itself. The figure of {JESUS} upon the "
     f"cross seen only in reverent, restrained wound-free silhouette -- "
     f"no visible wound, no blood, no graphic detail of any kind. "
     f"{FULLBLEED}"),
]

ALL_SHOTS = SHOTS_TEST + SHOTS_BATCH1 + SHOTS_BATCH2 + SHOTS_BATCH3 + SHOTS_BATCH4 + SHOTS_BATCH5


def main(only=None):
    shots = ALL_SHOTS if only is None else [s for s in ALL_SHOTS if s[0] in only]
    for name, style, tag, scene in shots:
        out = OUT / f"{name}.png"
        if out.exists():
            print(f"[skip] {name}")
            continue
        refs = resolve_refs(tag)
        prompt = style + "\n\nSCENE: " + scene
        print(f"[img] {name} (refs={len(refs)}) ...", flush=True)
        ok = run(prompt, out, refs)
        if not ok:
            time.sleep(5)
            ok = run(prompt, out, refs)
        if ok:
            try:
                cost.record_hf(EPISODE, "long", "stills_test", MODEL, note=f"[dayofatonement] {name}")
            except Exception as e:
                print(f"   (ledger skipped: {e})")
            print("   ok")
        else:
            print("   FAILED")
    print(f"[out] {OUT}")


if __name__ == "__main__":
    only = sys.argv[1].split(",") if len(sys.argv) > 1 else None
    main(only)
