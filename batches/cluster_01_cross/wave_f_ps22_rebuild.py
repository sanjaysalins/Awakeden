"""WAVE F $0 prep - PS22 shorts rebuild (2026-07-15), 5 pieces in one pass.

Executes the $0 phase of batches/_rollout/PS22_SHORTS_REBUILD_PLAN.md:
  mockers_words_ps227 / declared_brethren_ps2222 / he_hath_done_this_ps2231 /
  ends_of_earth_ps2227 / body_foretold_ps2214

NO SPEND. Byte-identical still copies from wave-gated corpus sources + hash-bound
$0 clip copies (wave_b_copies pattern: identical still bytes + verbatim move/LL
entry => identical clip_src_hash => the paid clip inherits for free). The 6 fresh
stills + 1 fresh Kling LL clip are left un-rendered behind the user's GO - exact
commands in batches/_rollout/PS22_PAID_WORKLIST.md.

Alignment provenance (regenerated this pass, $0 whisperx):
  - the four longform-shorts mp3s speak spoken_script.txt, NOT narration-tagged.md
    (stale tail on 07, stale from word 0 on 04/05/06) - alignments rebuilt against
    the true spoken text; every last word now ends within 0.16s of its mp3 end.
"""
import hashlib
import json
import shutil
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent          # batches/cluster_01_cross
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT))
from run_piece import clip_src_hash, load_piece, animate_prompts  # noqa: E402

C1 = HERE
C2 = ROOT / "batches" / "cluster_02_resurrection"

FORETOLD = C1 / "crucifixion_foretold_ps2218"
FORSAKEN = C1 / "forsaken_cry_ps221"
PIERCED = C1 / "pierced_zech1210"
PARADISE = C1 / "today_paradise_luke2343"
FINISHED = C1 / "it_is_finished_john1930"
INTO = C1 / "into_thy_hands_luke2346"
THIRST = C1 / "i_thirst_john1928"
FFT = C1 / "father_forgive_them"
WOMAN = C1 / "woman_behold_john1926"
WATCH = C1 / "watch_one_hour_matt2640"
JONAH = C2 / "sign_of_jonah_matt1240"
EMPTY = C2 / "empty_tomb_john208"

SRC_PJ = {p.name: load_piece(p) for p in
          (FORETOLD, FORSAKEN, PIERCED, PARADISE, FINISHED, INTO, THIRST, FFT,
           WOMAN, WATCH, JONAH, EMPTY)}


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def corpus_job(slug: str, prefer: Path):
    """Verbatim stills job (prompt+ref) for a copied slug: the byte-source piece first,
    then any corpus piece that defines it. Prompts only drive FUTURE re-renders."""
    order = [prefer.name] + [n for n in SRC_PJ if n != prefer.name]
    for name in order:
        j = SRC_PJ[name]["stills"]["jobs"].get(slug)
        if j:
            return dict(j)
    return None


def corpus_reg(slug: str, prefer: Path):
    order = [prefer.name] + [n for n in SRC_PJ if n != prefer.name]
    for name in order:
        r = (SRC_PJ[name].get("register") or {}).get("stills", {}).get(slug)
        if r:
            return dict(r)
    return None


# register fallbacks for corpus slugs no piece.json register describes yet
REG_FALLBACK = {
    "face_on_cross": {
        "subject": "the crucified Christ, face lifted against the darkened sky",
        "characters": ["the crucified Christ"], "elements": ["cross", "lifted face", "storm sky"],
        "setting": "the cross, low angle", "scope": "specific",
        "doctrine": "he humbled himself, and became obedient unto death, even the death of the cross (Phil 2:8)"},
    "seamless_robe_lots": {
        "subject": "the seamless tunic held spread between the soldiers",
        "characters": ["Roman soldiers"], "elements": ["seamless robe", "soldiers' hands"],
        "setting": "Golgotha", "scope": "specific",
        "doctrine": "they parted my garments among them, and cast lots upon my vesture (Psalm 22:18)"},
    "risen_christ_seeking": {
        "subject": "the risen Christ in the dawn garden, hand held toward the seeker",
        "characters": ["the risen Christ"], "elements": ["sunburst", "garden", "open hand"],
        "setting": "the garden at dawn", "scope": "hero",
        "doctrine": "the Son of man is come to seek and to save that which was lost (Luke 19:10)"},
    "psalm_scroll_night": {
        "subject": "the psalm scroll half-unrolled by lamplight at night",
        "characters": [], "elements": ["scroll", "clay lamp", "night"],
        "setting": "night chamber, c.1000 BC", "scope": "neutral",
        "doctrine": "the testimony of the LORD is sure (Psalm 19:7)"},
}

# fresh renders (PAID, PENDING): grounded jobs authored now, rendered later
FRESH_JOBS = {
    "wagging_heads_close": {
        "prompt": ("three Judean passers-by on the road below the cross at dusk, heads "
                   "mid-shake in scorn, mouths open in taunt, one arm pointing up toward "
                   "the cross above, weathered bearded faces, dusty wool robes and head "
                   "cloths, 1st-century Judea, vertical"),
        "ref": "../crucifixion_foretold_ps2218/visual/crowd_mocking.png"},
    "rulers_sneering": {
        "prompt": ("a knot of chief priests and scribes in rich temple vestments and head "
                   "wraps standing apart from the crowd at Golgotha, lips curled in sneers, "
                   "one gesturing dismissively up toward the cross above, Jerusalem wall "
                   "behind, 1st-century Judea, vertical"),
        "ref": "../crucifixion_foretold_ps2218/visual/crowd_mocking.png"},
    "risen_christ_congregation": {
        "prompt": ("the risen Christ standing in the midst of a seated congregation of "
                   "brethren in a lamp-lit stone hall, both arms lifted in praise with "
                   "smooth open palms, one warm golden shaft falling across Him, upturned "
                   "faces in wonder, vertical"),
        "ref": "../../../ref_library/characters/JESUS.png"},
    "nations_turning_wide": {
        "prompt": ("a vast dawn vista of many lands seen from above, plains, desert, river "
                   "valley and sea coast, small kindreds of every nation in varied period "
                   "dress all turned and bowing toward one great warm light rising on the "
                   "shared horizon, vertical"),
        "ref": None},
    "kindreds_worship": {
        "prompt": ("a gathering of worshippers of many nations, varied skin tones and "
                   "period garments and head wraps, kneeling together with hands lifted "
                   "toward warm light falling from above, faces lit with awe, 1st-century "
                   "world, vertical"),
        "ref": "../forsaken_cry_ps221/visual/look_up_faces.png"},
    "body_suspended_wide": {
        "prompt": ("a distant reverent silhouette of the crucified Christ seen from far "
                   "below against a vast storm sky, body hanging low by the outstretched "
                   "arms, weight sagging onto the shoulders, limbs drawn taut, thorn crown "
                   "on the bowed head, dark rocky hilltop, vertical"),
        "ref": "../crucifixion_foretold_ps2218/visual/face_on_cross.png"},
}
FRESH_REG = {
    "wagging_heads_close": {
        "subject": "three passers-by wagging their heads at the cross",
        "characters": ["three mockers"], "elements": ["shaking heads", "taunting mouths", "dusty robes"],
        "setting": "the road below Golgotha", "scope": "specific",
        "doctrine": "all they that see me laugh me to scorn... they shake the head (Psalm 22:7; Matt 27:39)"},
    "rulers_sneering": {
        "subject": "chief priests and scribes sneering up at the cross",
        "characters": ["chief priests", "scribes"], "elements": ["temple vestments", "sneering faces"],
        "setting": "Golgotha", "scope": "specific",
        "doctrine": "likewise also the chief priests mocking him, with the scribes and elders (Matt 27:41)"},
    "risen_christ_congregation": {
        "subject": "the risen Christ praising in the midst of the congregation",
        "characters": ["the risen Christ", "the brethren"], "elements": ["lifted arms", "lamp-lit hall", "golden shaft"],
        "setting": "a stone assembly hall", "scope": "hero",
        "doctrine": "in the midst of the congregation will I praise thee (Psalm 22:22; Heb 2:12)"},
    "nations_turning_wide": {
        "subject": "the kindreds of every land turning toward one rising light",
        "characters": ["distant kindreds of the nations"], "elements": ["many lands", "rising light", "bowing figures"],
        "setting": "the ends of the world", "scope": "specific",
        "doctrine": "all the ends of the world shall remember and turn unto the LORD (Psalm 22:27)"},
    "kindreds_worship": {
        "subject": "worshippers of many nations kneeling under one light",
        "characters": ["worshippers of many nations"], "elements": ["lifted hands", "varied garments", "warm light"],
        "setting": "the nations at worship", "scope": "specific",
        "doctrine": "all the kindreds of the nations shall worship before thee (Psalm 22:27)"},
    "body_suspended_wide": {
        "subject": "the crucified body hanging by the arms, far silhouette",
        "characters": ["the crucified Christ"], "elements": ["outstretched arms", "storm sky", "thorn crown"],
        "setting": "Golgotha, seen from far below", "scope": "specific",
        "doctrine": "I am poured out like water, and all my bones are out of joint (Psalm 22:14)"},
}

# ---------------------------------------------------------------- piece tables
# still rows: (slug, source_piece_dir_or_None_for_fresh, clip_mode)
#   clip_mode: "move" = copy clip + verbatim animate.moves + hash-bind
#              "ll"   = copy clip + verbatim living_light entry + hash-bind
#              "raw"  = copy clip unmanaged (legacy/custom-base source; $0, mtime-safe)
#              None   = no clip (writing stills play $0 dyncam; fresh stills pend)
PIECES = {
    "mockers_words_ps227": {
        "title": "The Mockers' Words (Psalm 22:7-8)",
        "verse": "Psalm 22:7-8 + Matthew 27:39-43",
        "prefix": "mw",
        "mood": "the taunts at the cross were a thousand-year-old script",
        "palette": "inked cel-flat, dusk taunts to risen gold",
        "tags": ["livingpage", "psalm22", "mockers_words", "cross"],
        "stills": [
            ("crowd_mocking", FORETOLD, "raw"),
            ("psalm_scroll_night", FORETOLD, None),
            ("david_writing_psalm", FORETOLD, None),
            ("wagging_heads_close", None, None),
            ("rulers_sneering", None, None),
            ("golgotha_hill_wide", FORETOLD, "move"),
            ("ninth_hour_darkness", FORSAKEN, "move"),
            ("face_on_cross", FORETOLD, "raw"),
            ("seamless_robe_lots", FORETOLD, "move"),
            ("lots_cup_close", FORETOLD, "ll"),
            ("jesus_looks_down", FORETOLD, "raw"),
            ("two_thieves_wide", PARADISE, "raw"),
            ("us_under_cross_shadow", FORETOLD, "move"),
            ("look_up_faces", FORSAKEN, "raw"),
            ("grace_poured_sky", PIERCED, "ll"),
            ("risen_mercy_hand", PIERCED, "ll"),
        ],
        "score": {"dark_trim_end": "52", "grace": "sacred_grace_rise_a.mp3",
                  "dips": [["10.06", "17.02", "0.4"], ["23.76", "31.95", "0.4"],
                           ["41.03", "46.37", "0.4"]],
                  "cta_dip": ["74.72", "0.5"]},
    },
    "declared_brethren_ps2222": {
        "title": "Declared to the Brethren (Psalm 22:22)",
        "verse": "Psalm 22:22 + Hebrews 2:11-12",
        "prefix": "dtb",
        "mood": "the forsaken cry turns to praise in the mouth of the risen Christ",
        "palette": "inked cel-flat, forsaken dark to family gold",
        "tags": ["livingpage", "psalm22", "declared_brethren", "resurrection"],
        "stills": [
            ("ninth_hour_darkness", FORSAKEN, "move"),
            ("face_on_cross", FORSAKEN, "raw"),
            ("psalm_scroll_night", FORSAKEN, None),
            ("david_writing_psalm", FORSAKEN, None),
            ("risen_christ_congregation", None, None),   # FRESH hero + FRESH Kling LL (pending)
            ("look_up_faces", FORSAKEN, "raw"),
            ("risen_christ_wounds", JONAH, "move"),
            ("stone_rolled_dawn", JONAH, "ll"),
            ("cross_at_dawn", FINISHED, "ll"),
            ("us_under_cross_shadow", FORSAKEN, "move"),
            ("golgotha_hill_wide", FORSAKEN, "move"),
            ("risen_christ_seeking", EMPTY, "ll"),
            ("risen_mercy_hand", PIERCED, "ll"),
        ],
        "score": {"dark_trim_end": "34", "grace": "glory_holy_stillness_a.mp3",
                  "dips": [["15.98", "21.85", "0.4"], ["39.50", "43.98", "0.4"]],
                  "cta_dip": ["55.90", "0.5"]},
    },
    "he_hath_done_this_ps2231": {
        "title": "He Hath Done This (Psalm 22:31)",
        "verse": "Psalm 22:31 + John 19:30",
        "prefix": "hhd",
        "mood": "two final words, ten centuries apart, the same finished work",
        "palette": "inked cel-flat, lamplit night to finished dawn",
        "tags": ["livingpage", "psalm22", "he_hath_done_this", "cross"],
        "stills": [
            ("david_writing_psalm", FORSAKEN, None),
            ("bowed_head_finished", THIRST, "move"),
            ("psalm_scroll_night", FORSAKEN, None),
            ("carpenter_bench_rest", FINISHED, "move"),
            ("child_waking_dawn", INTO, "move"),
            ("look_up_faces", FORSAKEN, "raw"),
            ("vinegar_sponge_reed", FINISHED, "move"),
            ("face_on_cross", THIRST, "raw"),
            ("cross_at_dawn", FINISHED, "ll"),
            ("father_lamp_doorway", FORSAKEN, "raw"),
            ("risen_mercy_hand", PIERCED, "ll"),
        ],
        "score": {"dark_trim_end": "28", "grace": "sacred_grace_rise_a.mp3",
                  "dips": [["15.45", "18.55", "0.4"], ["24.15", "25.85", "0.4"]],
                  "cta_dip": ["40.50", "0.5"]},
    },
    "ends_of_earth_ps2227": {
        "title": "The Ends of the Earth (Psalm 22:27)",
        "verse": "Psalm 22:27",
        "prefix": "eote",
        "mood": "one man dying alone, and every nation turning",
        "palette": "inked cel-flat, lone darkness to worldwide dawn",
        "tags": ["livingpage", "psalm22", "ends_of_earth", "nations"],
        "stills": [
            ("ninth_hour_darkness", FORSAKEN, "move"),
            ("face_on_cross", FORSAKEN, "raw"),
            ("psalm_scroll_night", FORSAKEN, None),
            ("grace_poured_sky", PIERCED, "ll"),
            ("nations_turning_wide", None, None),
            ("golgotha_hill_wide", FORSAKEN, "move"),
            ("look_up_faces", FORSAKEN, "raw"),
            ("us_under_cross_shadow", FORSAKEN, "move"),
            ("stone_rolled_dawn", JONAH, "ll"),
            ("nineveh_distant_walls", JONAH, "move"),
            ("kindreds_worship", None, None),
            ("risen_christ_wounds", JONAH, "move"),
        ],
        "score": {"dark_trim_end": "36", "grace": "glory_holy_stillness_a.mp3",
                  "dips": [["11.70", "21.45", "0.4"]],
                  "cta_dip": ["63.05", "0.5"]},
    },
    "body_foretold_ps2214": {
        "title": "The Body Foretold (Psalm 22:14-17)",
        "verse": "Psalm 22:14-17",
        "prefix": "tbf",
        "mood": "a dying body described a thousand years before the cross",
        "palette": "inked cel-flat, storm-cold body beats to mercy gold",
        "tags": ["livingpage", "psalm22", "body_foretold", "cross"],
        "stills": [
            ("david_writing_psalm", FORETOLD, None),
            ("face_on_cross", FORETOLD, "raw"),
            ("psalm_scroll_night", FORETOLD, None),
            ("golgotha_hill_wide", FORETOLD, "move"),
            ("body_suspended_wide", None, None),
            ("blood_water_wood", PIERCED, "raw"),
            ("two_thieves_wide", PARADISE, "raw"),
            ("crowd_mocking", FORETOLD, "raw"),
            ("ninth_hour_darkness", FORSAKEN, "move"),
            ("us_under_cross_shadow", FORETOLD, "move"),
            ("nail_through_hand", INTO, "raw"),
            ("bowed_head_finished", THIRST, "move"),
            ("cross_at_dawn", FINISHED, "ll"),
            ("risen_mercy_hand", PIERCED, "ll"),
        ],
        "score": {"dark_trim_end": "57", "grace": "sacred_grace_rise_a.mp3",
                  "dips": [["18.25", "24.60", "0.4"], ["31.20", "35.95", "0.4"]],
                  "cta_dip": ["63.60", "0.5"]},
    },
}


# ---------------------------------------------------------------- spec helpers
def beat(t0, t1, tpl, clips, cap, temp, **kw):
    b = {"t": [t0, t1], "tpl": tpl,
         "clips": [c if isinstance(c, dict) else {"slug": c, "motion": "pushin"} for c in clips],
         "cap": cap, "fx": {"temp": temp}}
    b.update(kw)
    return b


def grid(t0, t1, tpl, slug, cap, temp, anchors, slides, stagger, **kw):
    return beat(t0, t1, tpl, [slug], cap, temp,
                anchors=anchors,
                panel_at=[round(t0 + k * stagger, 2) for k in range(len(anchors))],
                panel_slide=slides, flash=True, **kw)


def cpt(text, kw):
    return {"type": "caption", "text": text, "kw": kw}


def red(text, speaker, ref):
    return {"type": "redletter", "text": text, "speaker": speaker, "ref": ref}


# eyeballed grid anchors (full-res Read pass 2026-07-15): [zoom, cx, cy]
A_DAVID = [[1.0, 0.5, 0.5], [1.5, 0.47, 0.32], [1.6, 0.42, 0.70]]
A_GOLGOTHA_FT = [[1.0, 0.5, 0.35], [1.5, 0.5, 0.24], [1.5, 0.5, 0.80]]
A_GOLGOTHA_FK = [[1.0, 0.5, 0.35], [1.5, 0.5, 0.26], [1.5, 0.5, 0.78]]
A_WOUNDS = [[1.2, 0.5, 0.24], [1.7, 0.13, 0.62], [1.7, 0.87, 0.62]]
A_VINEGAR = [[1.0, 0.5, 0.5], [1.5, 0.42, 0.38], [1.6, 0.75, 0.68]]
A_NINEVEH = [[1.0, 0.5, 0.45], [1.4, 0.5, 0.20], [1.5, 0.5, 0.78]]
A_THIEVES = [[1.0, 0.5, 0.40], [1.5, 0.5, 0.22], [1.5, 0.22, 0.32]]
A_US_UNDER = [[1.0, 0.5, 0.40], [1.5, 0.30, 0.34], [1.5, 0.68, 0.34]]
# body_suspended_wide is PENDING render: anchors follow the prompt design (distant
# centred silhouette, crown top-third) - RE-EYEBALL after the paid render lands.
A_BODY = [[1.0, 0.5, 0.42], [1.5, 0.5, 0.22], [1.6, 0.5, 0.58]]

SPECS = {}

SPECS["mockers_words_ps227"] = {
    "_doc": "THE MOCKERS' WORDS (Psalm 22:7-8 + Matt 27:39-43) 9:16 SHORT - living page "
            "(Wave F ps22 rebuild). 22 beats / 78.02s. Script hook -> David's taunt written "
            "1000 years early -> Matthew's mockers recite it -> He stayed -> the song ends "
            "with the world turning -> mercy-hand landing. Grade 7200->7900K at the taunts, "
            "landing 4900K.",
    "audio": "../audio/narration.mp3",
    "total": 78.02,
    "cut_ticks": False,
    "motion": "smooth",
    "heartbeat": {"from": 52.21, "to": 59.83, "gain": -9, "bpm": 60},
    "beats": [
        beat(0.0, 3.06, "big_inset",
             [{"slug": "crowd_mocking", "motion": "pushin"},
              {"slug": "psalm_scroll_night", "motion": "pushin"}],
             cpt("The crowd mocking Jesus at the cross was reading from a script", "A SCRIPT"),
             7200, punch=True, ramp=True,
             sfx=[["impact_low_boom", 0.1, -12]],
             takeover={"panel": 0, "start": 2.0, "zoom": 1.24}),
        beat(3.06, 4.58, "full", ["crowd_mocking"],
             cpt("They just didn't know it", "DIDN'T KNOW"), 7300, whip=True),
        grid(4.58, 10.06, "hero_frac3", "david_writing_psalm",
             cpt("A thousand years before, Psalm twenty-two recorded how the Messiah would be mocked",
                 "A THOUSAND YEARS"),
             7400, A_DAVID, ["left", "up", "down"], 0.35),
        beat(10.06, 15.94, "full", ["wagging_heads_close"],
             red("they shake the head, saying, He trusted on the LORD that he would deliver him:",
                 "DAVID", "PSALM 22:7-8"), 7600),
        beat(15.94, 17.02, "full", ["wagging_heads_close"],
             red("let him deliver him.", "DAVID", "PSALM 22:8"), 7700),
        beat(17.02, 19.32, "stack_h",
             [{"slug": "golgotha_hill_wide", "motion": "pushin"},
              {"slug": "rulers_sneering", "motion": "pushin"}],
             cpt("At the cross, Matthew's gospel records it", "MATTHEW RECORDS IT"),
             7500, whip=True),
        beat(19.32, 23.76, "full", ["rulers_sneering"],
             cpt("The passers-by wagging their heads, the rulers sneering nearly line for line",
                 "LINE FOR LINE"), 7600),
        beat(23.76, 28.81, "two_v",
             ["ninth_hour_darkness", "face_on_cross"],
             red("He trusted in God; let him deliver him now, if he will have him:",
                 "MOCKER", "MATTHEW 27:43"), 7800),
        beat(28.81, 31.95, "full", ["face_on_cross"],
             red("for he said, I am the Son of God.", "MOCKER", "MATTHEW 27:43"), 7900),
        beat(31.95, 34.41, "full", ["david_writing_psalm"],
             cpt("They thought they were inventing the cruelty", "INVENTING"), 7700),
        beat(34.41, 39.63, "two_v",
             ["seamless_robe_lots", "lots_cup_close"],
             cpt("They were reciting prophecy, unwilling witnesses that this was the One",
                 "UNWILLING WITNESSES"), 7700),
        beat(39.63, 41.03, "stack_h",
             ["jesus_looks_down", "ninth_hour_darkness"],
             cpt("And they threw one more taunt at Him", "ONE MORE TAUNT"), 7800, whip=True),
        beat(41.03, 44.99, "full", ["two_thieves_wide"],
             red("save thyself. If thou be the Son of God,", "MOCKER", "MATTHEW 27:40"), 7900),
        beat(44.99, 46.37, "full", ["two_thieves_wide"],
             red("come down from the cross.", "MOCKER", "MATTHEW 27:40"), 7900),
        beat(46.37, 48.13, "full", ["jesus_looks_down"],
             cpt("But He could have come down", "HE COULD HAVE"), 7500),
        grid(48.13, 52.21, "hero_band3", "golgotha_hill_wide",
             cpt("He showed He was the Son not by escaping the cross, but by staying on it",
                 "BY STAYING"),
             7400, A_GOLGOTHA_FT, ["up", "left", "down"], 0.3),
        grid(52.21, 56.51, "hero_frac3", "us_under_cross_shadow",
             cpt("Bearing the scorn He could have silenced, for the very people throwing it",
                 "FOR THE VERY PEOPLE"),
             7300, A_US_UNDER, ["up", "left", "right"], 0.35),
        beat(56.51, 59.83, "full", ["look_up_faces"],
             cpt("The man they mocked is the One the whole song was about", "THE WHOLE SONG"),
             7200),
        beat(59.83, 63.25, "big_inset",
             [{"slug": "seamless_robe_lots", "motion": "pushin"},
              {"slug": "us_under_cross_shadow", "motion": "pushin"}],
             cpt("They told the King to come down, and He never did", "HE NEVER DID"),
             7400, punch=True),
        beat(63.25, 68.50, "two_v",
             [{"slug": "look_up_faces", "motion": "pushin"},
              {"slug": "lots_cup_close", "motion": "pushin", "zoom": 1.25}],
             cpt("He stayed under scorn, theirs and ours, to win the scorners",
                 "TO WIN THE SCORNERS"), 6900),
        beat(68.50, 74.72, "full", ["grace_poured_sky"],
             cpt("The song ends with all the ends of the world turning to Him",
                 "TURNING TO HIM"), 6200),
        beat(74.72, 78.02, "full", ["risen_mercy_hand"],
             cpt("Turn, and come to the One who would not come down", "TURN, AND COME"),
             4900, punch=True, border_break={"at": 75.0},
             sfx=[["dawn_morning_warm", 74.85, -13]]),
    ],
}

SPECS["declared_brethren_ps2222"] = {
    "_doc": "DECLARED TO THE BRETHREN (Psalm 22:22 + Heb 2:11-12) 9:16 SHORT - living page "
            "(Wave F ps22 rebuild). 16 beats / 58.96s. Stop-reading hook -> the psalm turns "
            "-> JESUS redletter Ps 22:22 -> Hebrews puts it in the risen Christ's mouth -> "
            "not ashamed -> family landing on the mercy hand. NOTE: risen_christ_congregation "
            "still + its Kling LL clip are the piece's one PAID pending item.",
    "audio": "../audio/narration.mp3",
    "total": 58.96,
    "cut_ticks": False,
    "motion": "smooth",
    "heartbeat": {"from": 39.50, "to": 46.10, "gain": -9, "bpm": 60},
    "beats": [
        beat(0.0, 3.62, "big_inset",
             [{"slug": "ninth_hour_darkness", "motion": "pushin"},
              {"slug": "face_on_cross", "motion": "pushin"}],
             cpt("Most people stop reading Psalm twenty-two at the cross", "STOP READING"),
             7200, punch=True, ramp=True,
             sfx=[["impact_low_boom", 0.1, -12]],
             takeover={"panel": 0, "start": 2.4, "zoom": 1.24}),
        beat(3.62, 7.44, "full", ["ninth_hour_darkness"],
             cpt("Keep going, it doesn't end in a grave", "KEEP GOING"), 7400),
        beat(7.44, 10.60, "two_v",
             ["face_on_cross", "psalm_scroll_night"],
             cpt("But the cry doesn't stay forsaken", "FORSAKEN"), 7800),
        grid(10.60, 15.98, "hero_frac3", "david_writing_psalm",
             cpt("Later, the psalm turns, the same voice moves from anguish to praise",
                 "THE PSALM TURNS"),
             7600, A_DAVID, ["left", "up", "down"], 0.35, whip=True),
        beat(15.98, 19.35, "full", ["risen_christ_congregation"],
             red("I will declare thy name unto my brethren:", "JESUS", "PSALM 22:22"), 7000),
        beat(19.35, 21.85, "full", ["risen_christ_congregation"],
             red("in the midst of the congregation will I praise thee.", "JESUS",
                 "PSALM 22:22"), 6800),
        beat(21.85, 25.55, "stack_h",
             ["psalm_scroll_night", "look_up_faces"],
             cpt("Who is that praising voice?", "PRAISING VOICE"), 7300),
        grid(25.55, 28.90, "hero_frac3", "risen_christ_wounds",
             cpt("Hebrews takes that opening line word for word", "WORD FOR WORD"),
             7000, A_WOUNDS, ["up", "left", "right"], 0.3),
        beat(28.90, 32.20, "full", ["risen_christ_wounds"],
             cpt("and puts it in the mouth of the risen Christ", "THE RISEN CHRIST"), 6600),
        beat(32.20, 36.60, "full", ["stone_rolled_dawn"],
             cpt("The psalm's turn is Jesus, alive on the far side of the cross", "ALIVE"),
             6200),
        beat(36.60, 39.50, "stack_h",
             ["cross_at_dawn", "look_up_faces"],
             cpt("And hear what He calls us", "WHAT HE CALLS US"), 6800),
        beat(39.50, 43.98, "full", ["cross_at_dawn"],
             red("not ashamed to call them brethren", "SCRIPTURE", "HEBREWS 2:11"), 6400),
        beat(43.98, 47.50, "full", ["us_under_cross_shadow"],
             cpt("Brothers. Family.", "FAMILY"), 6000, punch=True),
        grid(47.50, 51.30, "hero_band3", "golgotha_hill_wide",
             cpt("The same Jesus who cried out forsaken now lives", "NOW LIVES"),
             7200, A_GOLGOTHA_FK, ["up", "left", "down"], 0.3),
        beat(51.30, 55.90, "full", ["risen_christ_seeking"],
             cpt("and the risen Christ is not ashamed to call His own brethren",
                 "HIS OWN BRETHREN"), 5600),
        beat(55.90, 58.96, "full", ["risen_mercy_hand"],
             cpt("He is calling you into that family", "CALLING YOU"),
             4900, punch=True, border_break={"at": 56.15},
             sfx=[["dawn_morning_warm", 56.05, -13]]),
    ],
}

SPECS["he_hath_done_this_ps2231"] = {
    "_doc": "HE HATH DONE THIS (Psalm 22:31 + John 19:30) 9:16 SHORT - living page (Wave F "
            "ps22 rebuild). 13 beats / 42.70s. Two final words hook -> SCRIPTURE redletter "
            "Ps 22:31 -> JESUS redletter John 19:30 -> nothing left to finish -> come home "
            "landing on the mercy hand. Fully bank-served: $0 piece.",
    "audio": "../audio/narration.mp3",
    "total": 42.70,
    "cut_ticks": False,
    "motion": "smooth",
    "heartbeat": {"from": 32.60, "to": 38.00, "gain": -9, "bpm": 60},
    "beats": [
        beat(0.0, 3.60, "big_inset",
             [{"slug": "david_writing_psalm", "motion": "pushin"},
              {"slug": "bowed_head_finished", "motion": "pushin"}],
             cpt("A psalm's last line and Jesus' last breath in John", "LAST BREATH"),
             7200, punch=True, ramp=True,
             sfx=[["impact_low_boom", 0.1, -12]],
             takeover={"panel": 1, "start": 2.3, "zoom": 1.24}),
        beat(3.60, 7.86, "two_v",
             ["psalm_scroll_night", "carpenter_bench_rest"],
             cpt("close on the very same note: it is done", "THE SAME NOTE"), 7300),
        grid(7.86, 11.40, "hero_frac3", "david_writing_psalm",
             cpt("The psalm closes looking ahead to God's saving work, accomplished",
                 "ACCOMPLISHED"),
             7400, A_DAVID, ["left", "up", "down"], 0.3),
        beat(11.40, 15.45, "stack_h",
             ["child_waking_dawn", "look_up_faces"],
             cpt("and told to a people not yet born", "NOT YET BORN"), 7000),
        beat(15.45, 18.55, "full", ["psalm_scroll_night"],
             red("that he hath done this.", "SCRIPTURE", "PSALM 22:31"), 7500),
        beat(18.55, 20.45, "full", ["bowed_head_finished"],
             cpt("Done.", "DONE"), 7600, punch=True, whip=True),
        grid(20.45, 24.15, "hero_frac3", "vinegar_sponge_reed",
             cpt("And as Jesus hung dying, John records His final word", "HIS FINAL WORD"),
             7600, A_VINEGAR, ["left", "up", "down"], 0.3),
        beat(24.15, 25.85, "full", ["face_on_cross"],
             red("It is finished.", "JESUS", "JOHN 19:30"), 7600),
        beat(25.85, 29.60, "two_v",
             ["carpenter_bench_rest", "cross_at_dawn"],
             cpt("Different words, in different tongues, a thousand years apart",
                 "DIFFERENT TONGUES"), 6800),
        beat(29.60, 32.60, "full", ["cross_at_dawn"],
             cpt("but the same note: a finished work", "A FINISHED WORK"), 6400),
        beat(32.60, 36.45, "full", ["look_up_faces"],
             cpt("So what's left for you to finish?", "WHAT'S LEFT"), 6000),
        beat(36.45, 40.50, "full", ["father_lamp_doorway"],
             cpt("Nothing, only Someone to come home to", "COME HOME"), 5600),
        beat(40.50, 42.70, "full", ["risen_mercy_hand"],
             cpt("the One who said it is done", "IT IS DONE"),
             4900, punch=True, border_break={"at": 40.75},
             sfx=[["dawn_morning_warm", 40.65, -13]]),
    ],
}

SPECS["ends_of_earth_ps2227"] = {
    "_doc": "THE ENDS OF THE EARTH (Psalm 22:27) 9:16 SHORT - living page (Wave F ps22 "
            "rebuild). 18 beats / 67.50s. Dying-alone hook -> SCRIPTURE redletter Ps 22:27 "
            "on the fresh nations plate -> impossible -> cross + empty tomb -> nation after "
            "nation -> wherever you are -> rays landing on the risen Christ. NOTE: "
            "nations_turning_wide + kindreds_worship are the PAID pending stills.",
    "audio": "../audio/narration.mp3",
    "total": 67.50,
    "cut_ticks": False,
    "motion": "smooth",
    "heartbeat": {"from": 52.20, "to": 57.55, "gain": -9, "bpm": 60},
    "beats": [
        beat(0.0, 4.20, "big_inset",
             [{"slug": "ninth_hour_darkness", "motion": "pushin"},
              {"slug": "face_on_cross", "motion": "pushin"}],
             cpt("Psalm twenty-two opens with one forsaken man dying alone", "DYING ALONE"),
             7300, punch=True, ramp=True,
             sfx=[["impact_low_boom", 0.1, -12]],
             takeover={"panel": 1, "start": 2.6, "zoom": 1.24}),
        beat(4.20, 7.55, "full", ["psalm_scroll_night"],
             cpt("and ends with every nation on earth", "EVERY NATION"), 7200),
        beat(7.55, 11.70, "stack_h",
             ["face_on_cross", "grace_poured_sky"],
             cpt("After the suffering, the song throws its arms open to every nation",
                 "ARMS OPEN"), 7000),
        beat(11.70, 16.80, "full", ["nations_turning_wide"],
             red("All the ends of the world shall remember and turn unto the LORD:",
                 "SCRIPTURE", "PSALM 22:27"), 6800),
        beat(16.80, 21.45, "full", ["nations_turning_wide"],
             red("and all the kindreds of the nations shall worship before thee.",
                 "SCRIPTURE", "PSALM 22:27"), 6600),
        grid(21.45, 24.70, "hero_band3", "golgotha_hill_wide",
             cpt("A man dying in one corner of the Roman Empire", "ONE CORNER"),
             7400, A_GOLGOTHA_FK, ["up", "left", "down"], 0.3),
        beat(24.70, 28.80, "two_v",
             ["psalm_scroll_night", "look_up_faces"],
             cpt("and his song says the ends of the earth will turn to God",
                 "THE ENDS OF THE EARTH"), 7200),
        beat(28.80, 31.10, "full", ["ninth_hour_darkness"],
             cpt("It sounded impossible", "IMPOSSIBLE"), 7800, whip=True),
        beat(31.10, 32.60, "full", ["us_under_cross_shadow"],
             cpt("But from that cross", "THAT CROSS"), 7400),
        beat(32.60, 35.90, "full", ["stone_rolled_dawn"],
             cpt("and the empty tomb, the gospel went out", "THE EMPTY TOMB"), 6600),
        grid(35.90, 39.35, "hero_frac3", "nineveh_distant_walls",
             cpt("and people in nation after nation have turned to the LORD",
                 "NATION AFTER NATION"),
             6800, A_NINEVEH, ["up", "left", "down"], 0.3),
        beat(39.35, 42.90, "stack_h",
             ["look_up_faces", "kindreds_worship"],
             cpt("worshipping the One who died and rose", "DIED AND ROSE"), 6400),
        grid(42.90, 45.95, "hero_band3", "risen_christ_wounds",
             cpt("That is the reach of the cross", "THE REACH"),
             6200, A_WOUNDS, ["up", "left", "right"], 0.3),
        beat(45.95, 48.10, "full", ["golgotha_hill_wide"],
             cpt("It was never a local tragedy", "NEVER A LOCAL TRAGEDY"), 7000),
        beat(48.10, 52.20, "two_v",
             ["kindreds_worship", "stone_rolled_dawn"],
             cpt("it was for the nations, all the kindreds of the earth", "FOR THE NATIONS"),
             6600),
        beat(52.20, 57.55, "full", ["grace_poured_sky"],
             cpt("And the ends of the world includes wherever you are, right now",
                 "WHEREVER YOU ARE"), 5800),
        grid(57.55, 63.05, "hero_frac3", "us_under_cross_shadow",
             cpt("The song that began with one man dying alone has swept the whole earth",
                 "THE WHOLE EARTH"),
             6000, A_US_UNDER, ["up", "left", "right"], 0.35),
        {**beat(63.05, 67.50, "full", ["risen_christ_wounds"],
                cpt("the Lord it promised still has room for you to turn to Him",
                    "ROOM FOR YOU"),
                5000, punch=True, border_break={"at": 63.30},
                sfx=[["dawn_morning_warm", 63.20, -13]]),
         "fx": {"temp": 5000, "rays": {"at": [0.5, 0.12], "strength": 0.5}}},
    ],
}

SPECS["body_foretold_ps2214"] = {
    "_doc": "THE BODY FORETOLD (Psalm 22:14-17) 9:16 SHORT - living page (Wave F ps22 "
            "rebuild). 17 beats / 66.94s. Eyewitness hook -> DAVID redletter Ps 22:14 on "
            "the fresh suspended-body plate -> Ps 22:17 -> David never saw a crucifixion -> "
            "what Jesus bore -> crushed in your place landing. Captions follow the LOCKED "
            "mp3 (spoken_script.txt), not the stale tagged file. NOTE: body_suspended_wide "
            "is the PAID pending still.",
    "audio": "../audio/narration.mp3",
    "total": 66.94,
    "cut_ticks": False,
    "motion": "smooth",
    "heartbeat": {"from": 52.55, "to": 59.90, "gain": -9, "bpm": 60},
    "beats": [
        beat(0.0, 3.50, "big_inset",
             [{"slug": "david_writing_psalm", "motion": "pushin"},
              {"slug": "face_on_cross", "motion": "pushin"}],
             cpt("A king described a dying body so exactly", "SO EXACTLY"),
             7200, punch=True, ramp=True,
             sfx=[["impact_low_boom", 0.1, -12]],
             takeover={"panel": 0, "start": 2.2, "zoom": 1.24}),
        beat(3.50, 7.60, "full", ["david_writing_psalm"],
             cpt("it reads like an eyewitness account of a crucifixion he never saw",
                 "AN EYEWITNESS"), 7300),
        beat(7.60, 10.05, "full", ["psalm_scroll_night"],
             cpt("Psalm twenty-two", "PSALM TWENTY-TWO"), 7400, whip=True),
        beat(10.05, 15.30, "two_v",
             ["golgotha_hill_wide", "psalm_scroll_night"],
             cpt("David wrote it in the first person, but he was describing someone else's death",
                 "SOMEONE ELSE'S DEATH"), 7500),
        beat(15.30, 18.25, "full", ["blood_water_wood"],
             cpt("Watch the body of the dying man", "WATCH THE BODY"), 7600),
        beat(18.25, 24.60, "full", ["body_suspended_wide"],
             red("I am poured out like water, and all my bones are out of joint",
                 "DAVID", "PSALM 22:14"), 7900),
        grid(24.60, 31.20, "hero_frac3", "body_suspended_wide",
             cpt("Drained, and every joint pulled loose, the way a body hangs suspended by the arms",
                 "EVERY JOINT"),
             7800, A_BODY, ["up", "left", "down"], 0.4),
        beat(31.20, 35.95, "full", ["face_on_cross"],
             red("I may tell all my bones: they look and stare upon me.",
                 "DAVID", "PSALM 22:17"), 7800),
        grid(35.95, 38.60, "hero_frac3", "two_thieves_wide",
             cpt("He could count every bone, stretched and exposed", "COUNT EVERY BONE"),
             7700, A_THIEVES, ["left", "up", "down"], 0.3),
        beat(38.60, 41.60, "stack_h",
             ["crowd_mocking", "ninth_hour_darkness"],
             cpt("while onlookers stood and stared at him", "STOOD AND STARED"), 7600),
        beat(41.60, 44.65, "full", ["crowd_mocking"],
             cpt("David never saw a crucifixion", "NEVER SAW"), 7300),
        beat(44.65, 47.90, "two_v",
             [{"slug": "golgotha_hill_wide", "motion": "pushin", "zoom": 1.25},
              {"slug": "ninth_hour_darkness", "motion": "pushin"}],
             cpt("Rome would not make it its instrument for centuries", "FOR CENTURIES"),
             7400),
        grid(47.90, 52.55, "hero_band3", "us_under_cross_shadow",
             cpt("Yet the dying man of his song bears the marks of one, written early",
                 "WRITTEN EARLY"),
             7000, A_US_UNDER, ["up", "left", "right"], 0.3),
        beat(52.55, 56.20, "full", ["nail_through_hand"],
             cpt("This is what Jesus bore to bring you home", "TO BRING YOU HOME"), 6600),
        beat(56.20, 59.90, "two_v",
             ["blood_water_wood", "bowed_head_finished"],
             cpt("every wrenched joint, every cold stare", "EVERY WRENCHED JOINT"), 6800),
        beat(59.90, 63.60, "full", ["cross_at_dawn"],
             cpt("recorded centuries early so you'd know none of it was chance",
                 "CENTURIES EARLY"), 6000),
        beat(63.60, 66.94, "full", ["risen_mercy_hand"],
             cpt("He was crushed in your place", "IN YOUR PLACE"),
             4900, punch=True, border_break={"at": 63.85},
             sfx=[["dawn_morning_warm", 63.75, -13]]),
    ],
}


# ---------------------------------------------------------------- build
def phrase_meta(align, a, b):
    words = [w for w in align if a <= (w["start"] + w["end"]) / 2 <= b]
    if not words:
        return None
    return {"phrase": " ".join(w["w"] for w in words),
            "pre": round(words[0]["start"] - a, 2),
            "post": round(b - words[-1]["end"], 2)}


def build_piece(name: str, cfg: dict) -> None:
    print(f"\n================ {name}")
    piece_dir = HERE / name
    V = piece_dir / "visual"
    CLIPS = V / "clips"
    CLIPS.mkdir(parents=True, exist_ok=True)
    spec = SPECS[name]

    moves, lls, ll_pending = {}, {}, []
    copies = []   # (slug, src_dir, mode) for the post-piece.json hash-bound clip copies

    # ---- stills + audit sidecars + anchors + clips
    for slug, src_dir, mode in cfg["stills"]:
        if src_dir is None:   # FRESH - paid, pending; job only
            (V / f"{slug}.pending.json").write_text(json.dumps({
                "slug": slug, "status": "PENDING PAID RENDER",
                "note": "fresh still per PS22_SHORTS_REBUILD_PLAN.md; exact byteplus "
                        "command in batches/_rollout/PS22_PAID_WORKLIST.md",
            }, indent=1), encoding="utf-8")
            print(f" still {slug:26} FRESH (pending paid render)")
            continue
        src_png = src_dir / "visual" / f"{slug}.png"
        if not src_png.exists():
            sys.exit(f"MISSING SOURCE STILL: {src_png}")
        dst = V / f"{slug}.png"
        if not dst.exists() or sha(dst) != sha(src_png):
            shutil.copy2(src_png, dst)
        src_audit = src_dir / "visual" / f"{slug}.audit.json"
        prov = ""
        if src_audit.exists():
            try:
                sa = json.loads(src_audit.read_text(encoding="utf-8"))
                prov = f"source audit {sa.get('verdict')}: " + "; ".join(map(str, sa.get("flags", [])))[:220]
            except Exception:
                prov = "source audit present but unreadable"
        (V / f"{slug}.audit.json").write_text(json.dumps({
            "image": f"{slug}.png", "verdict": "PASS",
            "flags": [f"byte-identical corpus copy from {src_dir.name} (wave-gated source)",
                      prov or "no source audit sidecar",
                      "Wave F ps22 rebuild $0 migration 2026-07-15"],
            "reviewer": "in-chat-agent", "stage": "content",
        }, indent=1), encoding="utf-8")
        src_anchor = src_dir / "visual" / f"{slug}.anchor.json"
        if src_anchor.exists():
            shutil.copy2(src_anchor, V / f"{slug}.anchor.json")
        if mode == "raw":
            src_clip = src_dir / "visual" / "clips" / f"{slug}.mp4"
            if not src_clip.exists():
                sys.exit(f"MISSING SOURCE CLIP: {src_clip}")
            shutil.copy2(src_clip, CLIPS / f"{slug}.mp4")
        elif mode == "move":
            moves[slug] = SRC_PJ[src_dir.name]["animate"]["moves"][slug]
            copies.append((slug, src_dir, mode))
        elif mode == "ll":
            lls[slug] = dict(SRC_PJ[src_dir.name]["animate"]["living_light"][slug])
            copies.append((slug, src_dir, mode))
        print(f" still {slug:26} <- {src_dir.name}"
              + {"raw": "  +clip(raw)", "move": "  +clip(move-bound)",
                 "ll": "  +clip(LL-bound)", None: ""}[mode])

    # the fresh Kling LL for declared_brethren: authored now, rendered later (paid)
    if name == "declared_brethren_ps2222":
        lls["risen_christ_congregation"] = {
            "target": "the risen Christ standing in the midst of the brethren",
            "light": ("the warm lamplight around Him slowly builds and breathes, the "
                      "single golden shaft widening gently across the hall, soft haze "
                      "glowing where the light falls"),
        }
        ll_pending.append("risen_christ_congregation")

    # ---- piece.json
    jobs, reg_stills = {}, {}
    for slug, src_dir, _mode in cfg["stills"]:
        if src_dir is None:
            jobs[slug] = dict(FRESH_JOBS[slug])
            reg_stills[slug] = dict(FRESH_REG[slug])
        else:
            job = corpus_job(slug, src_dir)
            if job is None:
                sys.exit(f"no corpus job found for {slug}")
            jobs[slug] = job
            reg_stills[slug] = corpus_reg(slug, src_dir) or dict(REG_FALLBACK[slug])

    aud = piece_dir / "audio"
    align = json.loads((aud / "alignment.json").read_text(encoding="utf-8"))
    import subprocess
    base = round(float(subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0",
         str(aud / "narration.mp3")], capture_output=True, text=True).stdout.strip()), 2)
    sc = cfg["score"]
    dips_meta = [phrase_meta(align, float(a), float(b)) for a, b, _v in sc["dips"]]
    cta_meta = phrase_meta(align, float(sc["cta_dip"][0]), base + 1.5)
    piece = {
        "piece": name,
        "title": cfg["title"],
        "cluster": "cluster_01_cross",
        "verse": cfg["verse"],
        "stills": {"model": "seedream-4-5-251128", "size": "1440x2560", "jobs": jobs},
        "animate": {
            "duration": 5, "aspect_ratio": "9:16",
            "moves": moves,
            "living_light": lls,
        },
        "score": {
            "src": "visual/livingpage_short.spec_preview.mp4",
            "out": f"visual/{name}_scored.mp4",
            "dark": "lonely_searching_a.mp3",
            "grace": sc["grace"],
            "base_seconds": base, "outro_hold": 1.5,
            "dark_trim_end": sc["dark_trim_end"], "grace_trim": ["20", "90"],
            "crossfade": "6", "tpad": "1.5",
            "dips": sc["dips"], "cta_dip": sc["cta_dip"],
            "dips_meta": dips_meta,
            "cta_meta": {"phrase": cta_meta["phrase"], "pre": cta_meta["pre"]} if cta_meta else {},
        },
        "register": {
            "id_prefix": cfg["prefix"], "source": "corpus byte-identical reuse + byteplus seedream-4-5",
            "created": "2026-07-15",
            "style": "graphic_novel_inked", "aspect": "9:16",
            "palette": cfg["palette"],
            "mood": cfg["mood"],
            "tags_still": cfg["tags"],
            "tags_clip": [t for t in cfg["tags"] if t != "cross"] + ["kling"],
            "used_in": [f"{name} short"],
            "clip_title_suffix": " (clip)",
            "clip_source": "corpus HF kling3_0 pro 9:16 copies (hash-bound where manifest-driven)",
            "extra_rows": [],
            "stills": reg_stills,
        },
    }
    (piece_dir / "piece.json").write_text(
        json.dumps(piece, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    print(" piece.json written")

    # ---- hash-bound $0 clip copies (wave_b_copies pattern; refuses on any mismatch)
    d_pj = load_piece(piece_dir)
    d_prompts = animate_prompts(d_pj)
    an = d_pj["animate"]
    for slug, src_dir, _mode in copies:
        s_pj = SRC_PJ[src_dir.name]
        s_prompt = animate_prompts(s_pj)[slug]
        d_prompt = d_prompts[slug]
        s_png = src_dir / "visual" / f"{slug}.png"
        d_png = V / f"{slug}.png"
        if sha(s_png) != sha(d_png):
            sys.exit(f"RENDER {name}/{slug}: stills differ - no copy")
        if s_prompt != d_prompt:
            sys.exit(f"RENDER {name}/{slug}: prompts differ - no copy")
        src_clip = src_dir / "visual" / "clips" / f"{slug}.mp4"
        if not src_clip.exists():
            sys.exit(f"MISSING SOURCE CLIP: {src_clip}")
        shutil.copy2(src_clip, CLIPS / f"{slug}.mp4")
        (CLIPS / f"{slug}.src.sha").write_text(
            clip_src_hash(d_png, d_prompt, an["duration"], an["aspect_ratio"]),
            encoding="utf-8")
        # provenance check only (never blocks): does the SOURCE sha match its own manifest?
        s_sha = src_clip.with_suffix(".src.sha")
        if s_sha.exists() and s_sha.read_text(encoding="utf-8").strip() != \
                clip_src_hash(s_png, s_prompt, s_pj["animate"]["duration"],
                              s_pj["animate"]["aspect_ratio"]):
            print(f"   ! note: {src_dir.name}/{slug} source sha differs from its own manifest")
        print(f" COPIED {src_dir.name} -> {name}: {slug} ($0, hash-bound)")
    for slug in ll_pending:
        print(f" PENDING PAID: living_light[{slug}] Kling render (see PS22_PAID_WORKLIST.md)")

    # ---- spec + checklist
    (V / "livingpage_short.spec.json").write_text(
        json.dumps(spec, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f" livingpage_short.spec.json written: {len(spec['beats'])} beats / {spec['total']}s")
    (V / "wave_checklist.json").write_text(json.dumps({
        "piece": name, "created": "2026-07-15",
        "items": [{"name": n, "pass": None, "note": "", "reviewer": "sanjay"} for n in
                  ("scale_variety", "grids_multi_figure", "audio_diff", "bookend",
                   "filmstrip_qc", "before_after_review", "fit_gate_disposition",
                   "swapped_stills_review")],
    }, indent=1), encoding="utf-8")
    print(" wave_checklist.json seeded")


if __name__ == "__main__":
    only = set(sys.argv[1:])
    for name, cfg in PIECES.items():
        if only and name not in only:
            continue
        build_piece(name, cfg)
    print("\nDONE (all $0)")
