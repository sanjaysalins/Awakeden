"""Style bake-off round 4 -- INSERT PAGES (Fable, 2026-07-31).

The user's ask, after seeing Style 3's label sheet + Style 13's chart: keep
Style 1 as the narrative spine, but design MANY single-page "insert modes" --
whole pages rendered in a different pictorial MODE (a chart, a diagram, a
specimen plate) that drop into an otherwise-Style-1 episode when one beat is
better told that way. Same consistent hand, a different page when the content
asks for it. 12 candidates, one proof still each, across the whole corpus
(not just Storm):

  insert01_lineage_tree     genealogy page: Abraham->David->Christ, 14/14/14 (Matt 1)
  insert02_sealed_scroll    the seven-sealed book only the Lamb opens (Rev 5)
  insert03_tabernacle_cut   architecture cutaway: the pattern of heavenly things (Ex 26/Heb 9)
  insert04_star_chart       night-sky chart: the Seed promise counted (Gen 15/Gal 3)
  insert05_lily_plate       naturalist specimen plate: consider the lilies (Matt 6)
  insert06_feast_wheel      circular feast calendar: the year preaches Christ (Lev 23)
  insert07_thirty_pieces    money-reckoning sheet: the price of the Shepherd (Zech 11/Matt 26)
  insert08_trial_docket     court-record page: the only charge ever proven (John 19)
  insert09_wilderness_road  strip-itinerary: Christ at every station (Ex/1 Cor 10)
  insert10_psalm_leaf       illuminated hymn leaf, ruled lanes left BLANK for Scribed Ink (Ps 22)
  insert11_drought_almanac  weather almanac: the shut heaven + the man's-hand cloud (1 Kgs 18)
  insert12_witness_roll     evidence roll-call: 500 witnesses at once (1 Cor 15)

Same nano_banana_pro path / canon rules as rounds 1-3. Ledgered under
LS_StyleBakeoff, notes [bakeoff-r4-insertpages]. 12 x 2cr = 24cr quote;
hard stop for the round is 15 stills total (12 + <=3 re-rolls, ~30cr).

  .venv\\Scripts\\python.exe poc_living_sketchbook/_style_bakeoff/_render_stills_round4.py [name,name]
"""
import re
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
import config
from pipeline import cost

HF = str(config.HF_CLI_PATH)
MODEL = "nano_banana_pro"
EPISODE = "LS_StyleBakeoff"
OUT = Path(__file__).resolve().parent
OUT.mkdir(parents=True, exist_ok=True)

FLATPAGE = (
    "CRITICAL FRAMING: the page is seen perfectly flat from directly above, "
    "filling the ENTIRE frame edge to edge, corner to corner -- the parchment "
    "surface itself IS the image, its texture reaching every corner of the "
    "frame; the artwork is the page, never a photographed book on a table."
)

# The shared "same hand" document base -- Style 3/13's twice-proven idiom.
DOC_BASE = (
    "in iron-gall sepia ink on aged parchment, the working page of one "
    "skilled scholarly hand: fine ruled construction lines and compass arcs, "
    "precise small hand-inked forms, fine cross-hatched shading, tactile, "
    "orderly, hand-made -- never a modern printed chart, diagram or slide. "
)

SHOTS = [
    # 1 ── GENEALOGY / LINEAGE PAGE ─ Matthew 1 ────────────────────────────
    ("insert01_lineage_tree",
     "A hand-drawn genealogical lineage page " + DOC_BASE,
     "The generations from Abraham to the Christ drawn as one climbing "
     "olive tree filling the page from foot to head: at the foot the root "
     "and rootstock drawn strong and deep; midway up the trunk a small "
     "hand-inked royal crown marks the kingly line; and at the very top the "
     "tree crowns in the page's ONLY gold element -- a blazing star-burst "
     "pressed in real burnished gold leaf. Along the trunk run three neat "
     "separated groups of small vertical tally strokes -- fourteen strokes, "
     "then fourteen strokes, then fourteen strokes -- the counted "
     "generations. Small plain leaf and bud marks stand for the unnamed "
     "generations along every branch. The ONLY text anywhere on the page is "
     "three short hand-lettered labels in rubric-red antique serif "
     "capitals: exactly the word \"ABRAHAM\" beside the root, exactly the "
     "word \"DAVID\" beside the crown, and exactly the words \"MATTHEW 1\" "
     "in the lower margin -- no other words, letters or numerals anywhere. "
     + FLATPAGE),

    # 2 ── SEALED-DOCUMENT PAGE ─ Revelation 5 ─────────────────────────────
    ("insert02_sealed_scroll",
     "A hand-drawn document study page " + DOC_BASE,
     "Lying diagonally across the sheet, drawn large: a tightly rolled "
     "parchment scroll, written within and on the backside yet rolled shut "
     "so no writing shows, its closure bound by EXACTLY SEVEN dark wax "
     "seals in one row -- seven seals, count them, one two three four five "
     "six seven, every one of the seven visible -- every seal's face "
     "smooth unbroken blank wax; beside the scroll "
     "an enlarged detail study of one single seal impression, drawn as a "
     "circle bearing the device of a standing lamb -- and this one "
     "lamb-seal study is the page's ONLY element touched with real "
     "burnished gold leaf. Fine ruled construction lines frame both "
     "studies; cross-hatched shadow grounds the scroll. The ONLY text "
     "anywhere on the page is one short hand-lettered label in rubric-red "
     "antique serif capitals: exactly the words \"REVELATION 5\" in the "
     "lower margin -- no other words, letters or numerals anywhere; every "
     "corner and margin of the sheet is bare parchment. " + FLATPAGE),

    # 3 ── ARCHITECTURE CUTAWAY ─ Exodus 26 / Hebrews 9 ────────────────────
    ("insert03_tabernacle_cut",
     "A hand-drawn architectural cutaway study " + DOC_BASE,
     "The tabernacle tent of the wilderness drawn in cut-away section "
     "view, its near coverings peeled open to show the chambers within: "
     "the outer court with its bronze altar and bronze laver; the first "
     "chamber holding the seven-branched lampstand, the table of bread and "
     "the small altar of incense; then the great veil hanging full-height; "
     "and behind the veil the innermost chamber where the ark of the "
     "covenant stands beneath two winged cherubim -- the ark's lid, the "
     "mercy seat between the cherubim, is the page's ONLY element touched "
     "with real burnished gold leaf. Faint ruled dimension lines with "
     "plain tick marks measure the structure, carrying no numerals. The "
     "ONLY text anywhere on the page is two short hand-lettered labels in "
     "rubric-red antique serif capitals: exactly the words \"EXODUS 26\" "
     "in the upper margin and exactly the words \"HEBREWS 9\" in the lower "
     "margin -- no other words, letters or numerals anywhere. " + FLATPAGE),

    # 4 ── NIGHT-SKY CHART ─ Genesis 15 / Galatians 3 ──────────────────────
    ("insert04_star_chart",
     "A hand-drawn astronomical observation chart in iron-gall sepia ink "
     "on aged parchment: the night sky itself charted as one deep "
     "charcoal-blue ink wash field held inside ruled margins, hundreds of "
     "star points left as bright pricks of bare parchment in the dark "
     "wash, faint hairlines joining star to star into drawn figures, "
     "small plain circles ringing the notable stars, faint ruled arcs "
     "sweeping the field. Tactile, orderly, hand-made -- a patriarch's "
     "counting of the heavens, never a modern printed star map. ",
     "The desert night sky as the patriarch saw it when he was told to "
     "number the stars: the dark charted field filling the page, "
     "uncountably many fine star pricks, hairline joins, ringed "
     "clusters; along the foot of the chart a low drawn horizon of dark "
     "desert hills; and low above that horizon ONE single star pressed in "
     "real burnished gold leaf, set apart, ringed twice, with fine "
     "hairlines converging upon it from across the whole field -- the "
     "promised Seed among the numberless. The ONLY text anywhere on the "
     "chart is two short hand-lettered labels in rubric-red antique serif "
     "capitals: exactly the words \"GENESIS 15\" in the upper margin and "
     "exactly the words \"GALATIANS 3\" in the lower margin -- no other "
     "words, letters or numerals anywhere. " + FLATPAGE),

    # 5 ── NATURALIST SPECIMEN PLATE ─ Matthew 6 ───────────────────────────
    ("insert05_lily_plate",
     "A hand-drawn naturalist's specimen study plate in iron-gall sepia "
     "ink with muted watercolor washes on aged parchment: one botanical "
     "subject drawn whole at the center with smaller detail studies set "
     "around it inside fine ruled frame lines, fine cross-hatched and "
     "wash shading, tactile, orderly, hand-made -- a field scholar's own "
     "plate, never a modern printed botanical poster. ",
     "A wild scarlet lily of the Galilean field drawn whole from root to "
     "crown at the center of the plate -- bulb and fine roots, leaning "
     "stem, slender leaves, one open crimson-flushed bloom -- washed in "
     "muted crimson-madder and olive; around it smaller detail studies: "
     "the closed bud, the bloom's open face seen straight on, a single "
     "leaf; and in the lower corner one small honest study of the same "
     "flower's stem withered dry, the grass of the field that today is. "
     "Every wash is muted and mineral; nothing on this plate carries "
     "gold. The ONLY text anywhere on the plate is one short "
     "hand-lettered label in rubric-red antique serif capitals: exactly "
     "the words \"MATTHEW 6\" in the lower margin -- no other words, "
     "letters or numerals anywhere. " + FLATPAGE),

    # 6 ── CIRCULAR FEAST CALENDAR ─ Leviticus 23 ──────────────────────────
    ("insert06_feast_wheel",
     "A hand-drawn circular calendar diagram " + DOC_BASE,
     "One great compass-drawn year-wheel drawn WHOLE at the center of the "
     "page -- the complete circle entirely visible inside the frame, its "
     "full rim unbroken, with generous bands of blank parchment above the "
     "wheel and below it: its rim divided into twelve parts by fine ruled "
     "spokes, the compass center-prick and construction arcs still "
     "visible; at seven stations around the wheel small precise "
     "hand-inked symbols mark the appointed feasts of the LORD -- a young "
     "lamb, a flat unleavened loaf, a cut barley sheaf, two baked loaves "
     "side by side, a curved ram's-horn trumpet, ONE single station "
     "bearing a pair of he-goats drawn together touching shoulder to "
     "shoulder as one symbol, and a leafy harvest booth -- and of them "
     "all the small lamb ALONE is touched with real burnished gold leaf. "
     "Fine cross-hatched shading grounds each symbol; the wheel reads as "
     "one turning year drawn by one careful hand. The ONLY text anywhere on the page is one short "
     "hand-lettered label in rubric-red antique serif capitals: exactly "
     "the words \"LEVITICUS 23\" in the lower margin -- no other words, "
     "letters or numerals anywhere. " + FLATPAGE),

    # 7 ── MONEY-RECKONING SHEET ─ Zechariah 11 / Matthew 26 ───────────────
    ("insert07_thirty_pieces",
     "A hand-drawn money-reckoning sheet " + DOC_BASE,
     "At the head of the sheet a hand-inked balance scale drawn in fine "
     "line: one pan sunk low under a small heap of ancient silver "
     "shekels, the other pan holding a shepherd's wooden rod laid across "
     "it -- the Shepherd himself weighed out and priced. Below the "
     "balance the counted price is set out plainly in EXACTLY THREE ruled "
     "rows of coins and not one row more -- three rows only, each row "
     "holding exactly ten coins, thirty coins in all, generous blank "
     "parchment left beneath the third row -- every "
     "coin a plain ancient silver shekel washed in cool silver-gray. "
     "Fine cross-hatched shading, ruled frame lines. Every coin on this "
     "sheet is cold silver-gray; nothing on this page carries gold. The "
     "ONLY text anywhere on the sheet is two short hand-lettered labels "
     "in rubric-red antique serif capitals: exactly the words "
     "\"ZECHARIAH 11\" in the upper margin and exactly the words "
     "\"MATTHEW 26\" in the lower margin -- no other words, letters or "
     "numerals anywhere. " + FLATPAGE),

    # 8 ── COURT-RECORD PAGE ─ John 19 ─────────────────────────────────────
    ("insert08_trial_docket",
     "A hand-drawn court-record study page " + DOC_BASE,
     "At the head of the page, a careful study of the rough wooden "
     "titulus board from the execution, drawn with its wood grain and a "
     "nail hole at each upper corner, bearing hand-lettered dark serif "
     "capitals reading exactly the words \"KING OF THE JEWS\" -- the only "
     "charge ever recorded. Below it a Roman wax writing-tablet lies "
     "open as two hinged wooden leaves, both wax faces smooth, dark and "
     "utterly blank; a bronze reed stylus lies across the lower leaf; "
     "beside the tablet one round wax seal impression bears a plain "
     "laurel-wreath device. Fine ruled frame lines and cross-hatched "
     "shadow ground each object. The ONLY text anywhere on the page is "
     "the titulus board's own words \"KING OF THE JEWS\" and one short "
     "hand-lettered label in rubric-red antique serif capitals: exactly "
     "the words \"JOHN 19\" in the lower margin -- no other words, "
     "letters or numerals anywhere. " + FLATPAGE),

    # 9 ── STRIP-ITINERARY ROAD PAGE ─ Exodus / 1 Corinthians 10 ───────────
    ("insert09_wilderness_road",
     "A hand-drawn linear road-itinerary page " + DOC_BASE,
     "In the idiom of an ancient traveler's strip itinerary: one "
     "continuous hand-inked road runs from the foot of the page to its "
     "head in long drawn switchbacks, plain distance ticks along its "
     "whole length, carrying no numerals; stations along the road drawn "
     "as small hand-inked symbols -- at the foot a cluster of mud-brick "
     "kilns; then the sea drawn as two hatched standing walls of water "
     "with the dry road passing between them; then a bitter spring with "
     "a cast-in tree branch; then a fall of small round manna dots; then "
     "a split rock pouring water, and this rock ALONE is touched with "
     "real burnished gold leaf; then a serpent lifted high on a pole; "
     "and at the head of the page a mountain wrapped in drawn smoke and "
     "fire. Fine cross-hatched hills flank the road. The ONLY text "
     "anywhere on the page is three short hand-lettered labels in "
     "rubric-red antique serif capitals: exactly the word \"EGYPT\" at "
     "the foot, exactly the word \"SINAI\" at the head, and exactly the "
     "words \"1 CORINTHIANS 10\" in the lower margin -- no other words, "
     "letters or numerals anywhere. " + FLATPAGE),

    # 10 ── ILLUMINATED HYMN LEAF (built FOR the $0 overlay) ─ Psalm 22 ────
    ("insert10_psalm_leaf",
     "A hand-drawn illuminated hymn leaf prepared for writing, in "
     "iron-gall sepia ink on aged parchment: a scribe's ruled and "
     "bordered page awaiting its text, tactile, orderly, hand-made -- "
     "never a printed book page. ",
     "A border of interlaced thorn branches drawn in fine sepia line "
     "frames the page on all four sides, sparse sharp thorns, no "
     "blossoms; at the head of the page one single great illuminated "
     "initial letter \"M\" fills a small square panel, its letter-form "
     "pressed in real burnished gold leaf over fine ink pen-flourishes; "
     "below the initial the body of the page lies open and EMPTY -- wide "
     "bands of untouched blank cream parchment between fine ruled "
     "hairlines, the ruled leaf still waiting for its scribe's first "
     "word. The ONLY text anywhere on the page is the single gold "
     "initial \"M\" and one short hand-lettered label in rubric-red "
     "antique serif capitals: exactly the words \"PSALM 22\" in the "
     "lower margin -- no other words, letters or numerals anywhere; "
     "every ruled lane between the hairlines is bare untouched "
     "parchment. " + FLATPAGE),

    # 11 ── WEATHER ALMANAC ─ 1 Kings 18 ───────────────────────────────────
    ("insert11_drought_almanac",
     "A hand-drawn weather-almanac sheet " + DOC_BASE,
     "Three long ruled month-rows cross the sheet, each row carrying a "
     "run of small hand-inked moon phases waxing from new to full to new "
     "again; beside the moons each row carries a ruled rain-tally lane: "
     "in the first row a few short slanted rain strokes, and after them "
     "the lanes run EMPTY -- bare parchment month after month where rain "
     "marks should be; small drawn suns grow heavier and more hatched "
     "down the rows, and fine drawn cracks open in the ground-line under "
     "the last row; then at the very end of the last row, rising from a "
     "small drawn strip of sea horizon, one small hand-inked cloud the "
     "size of a man's hand. Nothing on this sheet carries gold. The ONLY "
     "text anywhere on the sheet is one short hand-lettered label in "
     "rubric-red antique serif capitals: exactly the words \"1 KINGS 18\" "
     "in the lower margin -- no other words, letters or numerals "
     "anywhere. " + FLATPAGE),

    # 12 ── WITNESS ROLL-CALL ─ 1 Corinthians 15 ───────────────────────────
    ("insert12_witness_roll",
     "A hand-drawn evidence roll-call page " + DOC_BASE,
     "At the head of the page a small study of a rock-cut tomb with its "
     "round stone rolled aside, and the light standing in the open "
     "doorway is the page's ONLY element touched with real burnished "
     "gold leaf. Beneath the tomb, three small ink portrait studies in "
     "ruled frames, three distinct ancient Judean men: a weathered "
     "broad-faced fisherman with short gray-streaked hair and a thick "
     "beard; a sober elder with a long full beard; a small keen "
     "bald-crowned man with a short pointed beard. Below the portraits, "
     "filling the lower half of the page, ruled row upon ruled row of "
     "tiny anonymous head-and-shoulder marks drawn in quick single "
     "strokes -- five hundred witnesses at once, far too many to name, "
     "each ruled row ticked at its end. The ONLY text anywhere on the "
     "page is one short hand-lettered label in rubric-red antique serif "
     "capitals: exactly the words \"1 CORINTHIANS 15\" in the lower "
     "margin -- no other words, letters or numerals anywhere. "
     + FLATPAGE),
]


def run(prompt, out):
    cmd = [HF, "generate", "create", MODEL, "--prompt", prompt,
           "--aspect_ratio", "9:16", "--resolution", "2k", "--wait"]
    p = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    blob = (p.stdout or "") + "\n" + (p.stderr or "")
    urls = re.findall(r'https?://\S+?\.(?:png|jpg|jpeg|webp)', blob) or re.findall(r'https?://\S+', blob)
    if not urls:
        return False, blob.strip()[-250:]
    subprocess.run(["curl", "-s", "-L", urls[-1], "-o", str(out)], check=True)
    return out.exists() and out.stat().st_size > 1000, ""


def one(name, style, scene):
    out = OUT / f"{name}.png"
    if out.exists():
        return name, "skip"
    prompt = style + "\n\nSCENE: " + scene
    ok, err = run(prompt, out)
    if not ok:
        time.sleep(3)
        ok, err = run(prompt, out)
    if ok:
        try:
            cost.record_hf(EPISODE, "short", "stills", MODEL, note=f"[bakeoff-r4-insertpages] {name}")
        except Exception:
            pass
        return name, "ok"
    return name, f"FAILED {err}"


def main(only=None):
    shots = SHOTS if only is None else [s for s in SHOTS if s[0] in only]
    with ThreadPoolExecutor(max_workers=6) as ex:
        futs = {ex.submit(one, n, s, sc): n for n, s, sc in shots}
        for fut in as_completed(futs):
            name, status = fut.result()
            print(f"[{status}] {name}", flush=True)
    print(f"[out] {OUT}")


if __name__ == "__main__":
    only = sys.argv[1].split(",") if len(sys.argv) > 1 else None
    main(only)
