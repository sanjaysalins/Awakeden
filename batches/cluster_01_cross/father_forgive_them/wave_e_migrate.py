"""WAVE E $0 prep — father_forgive_them mocomic -> livingpage migration (2026-07-15).

Authors the gold-master piece format from the approved pilot assets. NO SPEND:
the single paid item (willing_offering living-light Kling clip, ~7.5cr) is left
un-rendered behind the user's GO; risen_mercy_hand's LL clip copies $0 from
pierced_zech1210 (byte-identical still + verbatim LL entry, hash-bound).

Still selection (eye-audited in chat 2026-07-15, provenance archaeology):
 - 3 slugs were pointing at retired/bible-fail or superseded art in the LIVE pilot:
     seamless_robe_lots_cast -> nbp/04_cast_lots.png (07-04 fix: Christ ON the
       cross alive; the live pilot still plays the RETIRED storm/empty-cross clip)
     father_forgive_them_face -> nbp/03_prayer_close.png (live pilot used the
       retired standing-before-cross version)
     golgotha_hill_wide -> the CORPUS shared still (three crucified, in 4
       wave-gated pieces); fft's own reshoot version had three EMPTY crosses
 - the red-letter Luke 23:34 beat now plays face_on_cross_speaks (Christ ON the
   cross praying) instead of the weak prayer-close art.
"""
import hashlib
import json
import shutil
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT))
from run_piece import clip_src_hash, load_piece, animate_prompts  # noqa: E402

C1 = ROOT / "batches" / "cluster_01_cross"
V = HERE / "visual"
BP = V / "_byteplus"
RS = BP / "reshoot"
CLIPS = V / "clips"
CLIPS.mkdir(exist_ok=True)

PIERCED = C1 / "pierced_zech1210"
FORSAKEN = C1 / "forsaken_cry_ps221"
INTO = C1 / "into_thy_hands_luke2346"
FORETOLD = C1 / "crucifixion_foretold_ps2218"

# ---- 1. stills: (slug, source png, legacy/corpus clip or None, audit notes) ----
STILLS = [
    ("nail_through_hand", BP / "nail_close_45.png", INTO / "visual" / "clips" / "nail_through_hand.mp4",
     "nail through the open hand ON the beam, wrist roped (nails+rope hybrid per fact card), blood; corpus-shared art (5 pieces, wave-gated)"),
    ("executioner_ignorance", RS / "executioner_ignorance.png", BP / "clips" / "executioner_ignorance.mp4",
     "executioner's fists mid-swing with mallet + nail, period bracers; single subject, animation-clean"),
    ("soldiers_gambling_establish", RS / "_retired_bible_fails" / "01c_soldiers_gamble.png", BP / "clips" / "soldiers_gambling_establish.mp4",
     "Christ ON the cross alive w/ thorn crown, 4 soldiers (John 19:23 quaternion) casting pale lot-stones, striped garment + jug, period wall; the 07-06 render the live pilot plays — was mis-filed into _retired_bible_fails"),
    ("seamless_robe_lots_cast", V / "nbp" / "04_cast_lots.png", None,
     "07-04 redo-batch fix: Christ ON the centre cross alive w/ crown (was the CRITICAL empty-cross storm fail), 4 soldiers, stone lots; NOTE side crosses empty (thieves not shown) - carried defensible, flagged at wave gate"),
    ("crowd_mocking", FORETOLD / "visual" / "crowd_mocking.png", FORETOLD / "visual" / "clips" / "crowd_mocking.mp4",
     "3 distinct mockers + shadow crowd (fft copy was byte-identical to this corpus still; corpus Kling clip reused)"),
    ("face_on_cross_speaks", RS / "02_jesus_prays.png", BP / "clips" / "face_on_cross_speaks.mp4",
     "Christ ON the cross, face lifted mid-word, nailed hands visible w/ blood; NO thorn crown (corpus crown-continuity note, flagged at wave gate); live-pilot approved art"),
    ("father_forgive_them_face", V / "nbp" / "03_prayer_close.png", None,
     "intimate close of Christ's face lifted in prayer at the cross; no crown (flagged); replaces the retired standing-before-cross version the live pilot used"),
    ("psalm22_scroll_david", RS / "psalm22_scroll_david.png", None,
     "aged psalmist over a BLANK half-unrolled scroll, lyre + clay lamp (not candle), night; 07-07 re-render; WRITING still - never Kling-animate, $0 dyncam only"),
    ("us_under_cross_shadow", RS / "06b_our_sin.png", BP / "clips" / "us_under_cross_shadow.mp4",
     "seven bowed mourners under the long cross shadow; faces distinct + bowed, no Christ-lookalike; fft's own richer version kept over the corpus 2-kneeler plate"),
    ("golgotha_hill_wide", FORSAKEN / "visual" / "golgotha_hill_wide.png", FORSAKEN / "visual" / "clips" / "golgotha_hill_wide.mp4",
     "CORPUS shared still: all three crosses OCCUPIED (Luke 23:32-33), Christ centre, mourners + Jerusalem wall, midday-black sky; replaces fft's empty-crosses version (same defect family as the retired lots still)"),
    ("willing_offering", BP / "willing_offering_v3_dark.png", None,
     "LIFE-SIZE re-render 2026-07-15 (user REJECT on the old giant-scale still): Christ w/ crown on a man-height cross, open palms flat on the beam w/ one dry wound each (no nail hardware), kneeling mourner's head at His feet, single diagonal golden shaft, featureless-black midday sky (v3 lightning retouched out - Luke 23:44 darkness not storm); NOT LL-eligible (fresh-cross still, see living-light-no-fresh-blood) - carries $0 fx.rays instead"),
    ("darkness_veil_torn", RS / "darkness_veil_torn.png", BP / "clips" / "darkness_veil_torn.mp4",
     "temple veil torn top-to-bottom between period columns, B/W ink; no writing, no figures"),
    ("risen_interceding_christ", BP / "risen_interceding_christ_dry.png", None,
     "risen Christ interceding in a light shaft, kneeling sinner silhouette below; palm marks retouched 2026-07-15 from fresh-red lines to DRY healed patches (red seeds Kling blood-growth - LL roll 1 grew the marks 2.8x, parked in _rejected); LL slot 2 target"),
    ("risen_mercy_hand", RS / "07_risen_hero.png", None,  # LL clip copied below
     "the corpus landing hero (byte-identical in 9 pieces): risen Christ, open healed hand held out; LL clip $0-copied from pierced_zech1210"),
]

for slug, src, clip, note in STILLS:
    dst = V / f"{slug}.png"
    if not src.exists():
        sys.exit(f"MISSING SOURCE: {src}")
    if not dst.exists() or hashlib.sha256(dst.read_bytes()).digest() != hashlib.sha256(src.read_bytes()).digest():
        shutil.copy2(src, dst)
    (V / f"{slug}.audit.json").write_text(json.dumps({
        "image": f"{slug}.png", "verdict": "PASS",
        "flags": [note, "vision-audited in-chat by Claude 2026-07-15 (Wave E migration eye pass)"],
        "reviewer": "in-chat-agent", "stage": "content",
    }, indent=1), encoding="utf-8")
    if clip is not None:
        if not clip.exists():
            sys.exit(f"MISSING CLIP: {clip}")
        shutil.copy2(clip, CLIPS / f"{slug}.mp4")
    print(f"still {slug:28} <- {src.relative_to(ROOT)}" + ("  +clip" if clip else ""))

# ---- 2. $0 living-light copy: pierced -> fft risen_mercy_hand (wave_b_copies pattern) ----
p_pj = load_piece(PIERCED)
LL_MERCY = p_pj["animate"]["living_light"]["risen_mercy_hand"]
MERCY_JOB = (p_pj["stills"]["jobs"].get("risen_mercy_hand")
             or {"prompt": "inked biblical graphic-novel of the risen Christ facing forward, one open "
                           "hand held out low bearing the faint flat healed mark, warm golden light",
                 "ref": None})

# ---- 3. piece.json ----
import re

def _clean(prompt: str) -> str:
    """Strip style tokens the house-ink lint now bans (these seeds predate the rule);
    prompts only drive FUTURE re-renders — the shipped stills stay untouched."""
    p = re.sub(r"\b(cel-shaded|cel shaded|manga|anime)\b[,;]?\s*", "", prompt, flags=re.I)
    return re.sub(r"\s{2,}", " ", p).strip(" ,")

SEEDS = {sc["slug"]: _clean(sc["prompt_seed"])
         for sc in json.loads((V / "scene_plan_v2.json").read_text(encoding="utf-8"))["final_plan"]["scenes"]}
SEEDS["risen_mercy_hand"] = SEEDS.pop("risen_mercy_hand_held_out")
GOLGOTHA_JOB = json.loads((FORSAKEN / "piece.json").read_text(encoding="utf-8"))["stills"]["jobs"]["golgotha_hill_wide"]

WILLING_PROMPT = (
    "a life-size crucifixion on a bare rocky hilltop at midday, the sky a smooth deep "
    "featureless black, darkness lying over the whole land: the crucified Christ with a "
    "thorn crown hangs with both arms stretched wide along the full crossbeam, open palms "
    "flat against the wood, each palm marked with one small dark dry wound, head bowed in "
    "willing surrender, a kneeling hooded mourner at the very foot of the cross, the "
    "mourner's bowed head reaching almost to Christ's feet, one single diagonal shaft of "
    "warm golden light falling across him through the darkness, 1st-century Judea, vertical")

jobs = {}
for slug, _src, _clip, _n in STILLS:
    if slug == "willing_offering":
        jobs[slug] = {"prompt": WILLING_PROMPT,
                      "ref": "../crucifixion_foretold_ps2218/visual/face_on_cross.png"}
    elif slug == "golgotha_hill_wide":
        jobs[slug] = dict(GOLGOTHA_JOB)
    elif slug == "risen_mercy_hand":
        jobs[slug] = dict(MERCY_JOB)
    else:
        jobs[slug] = {"prompt": SEEDS.get(slug, f"inked biblical graphic-novel, {slug.replace('_', ' ')}, vertical, 1st-century Judea"),
                      "ref": None}

piece = {
    "piece": "father_forgive_them",
    "title": "Father, Forgive Them (Luke 23:34)",
    "cluster": "cluster_01_cross",
    "verse": "Luke 23:34 + Psalm 22:18 + Romans 5:8 + Hebrews 7:25",
    "stills": {"model": "seedream-4-5-251128", "size": "1440x2560", "jobs": jobs},
    "animate": {
        "duration": 5, "aspect_ratio": "9:16",
        "moves": {},   # legacy pilot/corpus clips are unmanaged; only LL is manifest-driven
        "living_light": {
            # SINGLE living light by user grant (below). willing_offering: 3 rejects
            # (blood threads); risen_interceding_christ: 2 rejects (blood REGENERATED on
            # dry-retouched raised palms). Memory: living-light-no-fresh-blood.
            "risen_mercy_hand": LL_MERCY,
        },
        "living_light_exception": {
            "user": "sanjay", "date": "2026-07-15",
            "reason": "cross piece has no second wound-free still that fits a lit beat; "
                      "5/5 Kling blood rejects on wound-marked stills (37.5cr, parked in "
                      "clips/_rejected/); the Rom 5:8 reveal carries $0 fx.rays instead",
        },
    },
    "score": {
        "src": "visual/livingpage_short.spec_preview.mp4",
        "out": "visual/father_forgive_them_scored.mp4",
        "dark": "lonely_searching_a.mp3",
        "grace": "sacred_grace_rise_a.mp3",
        "base_seconds": 57.15, "outro_hold": 1.5,
        "dark_trim_end": "33", "grace_trim": ["20", "90"], "crossfade": "6", "tpad": "1.5",
        "dips": [["16.94", "22.06", "0.4"], ["42.84", "48.5", "0.35"]],
        "cta_dip": ["51.85", "0.5"],
        "dips_meta": [
            {"phrase": "Father, forgive them; for they know not what they do."},
            {"phrase": "While we were yet sinners, Christ died for us."},
        ],
        "cta_meta": {"phrase": "That mercy is held out to you now: come, and receive it by faith."},
    },
    "register": {
        "id_prefix": "fft", "source": "byteplus seedream-4-5", "created": "2026-07-15",
        "style": "graphic_novel_inked", "aspect": "9:16",
        "palette": "inked cel-flat, storm dark to risen gold",
        "mood": "the prayer from the cross for the ones driving the nails",
        "tags_still": ["livingpage", "luke2334", "father_forgive_them", "cross"],
        "tags_clip": ["livingpage", "luke2334", "kling"],
        "used_in": ["father_forgive_them short"],
        "clip_title_suffix": " (clip)",
        "clip_source": "pilot byteplus i2v / corpus HF kling3_0 pro 9:16 / pierced LL copy",
        "extra_rows": [],
        "stills": {
            "nail_through_hand": {
                "subject": "a forged square iron nail through the open hand on the beam",
                "characters": [], "elements": ["nail", "open hand", "rope", "beam", "blood"],
                "setting": "the cross, close", "scope": "specific",
                "doctrine": "they pierced my hands and my feet (Psalm 22:16)"},
            "executioner_ignorance": {
                "subject": "the executioner's fists mid-swing, mallet and nail",
                "characters": ["Roman executioner"], "elements": ["mallet", "nail", "bracers"],
                "setting": "Golgotha", "scope": "specific",
                "doctrine": "they know not what they do (Luke 23:34)"},
            "soldiers_gambling_establish": {
                "subject": "four soldiers casting lots beneath the occupied cross",
                "characters": ["four Roman soldiers", "the crucified Christ"],
                "elements": ["lot-stones", "garment", "jug", "cross", "city wall"],
                "setting": "Golgotha", "scope": "specific",
                "doctrine": "then the soldiers... took his garments... and also his coat (John 19:23)"},
            "seamless_robe_lots_cast": {
                "subject": "lots cast for the garments while Christ hangs alive above",
                "characters": ["Roman soldiers", "the crucified Christ"],
                "elements": ["lot-stones", "garments", "three crosses"],
                "setting": "Golgotha", "scope": "specific",
                "doctrine": "they parted his raiment, and cast lots (Luke 23:34)"},
            "crowd_mocking": {
                "subject": "three mockers pointing up, the crowd in shadow",
                "characters": ["three mockers", "shadow crowd"],
                "elements": ["pointing hands", "open mouths"],
                "setting": "Golgotha", "scope": "neutral",
                "doctrine": "and the people stood beholding... deriding him (Luke 23:35)"},
            "face_on_cross_speaks": {
                "subject": "the crucified Christ, face lifted, speaking from the cross",
                "characters": ["the crucified Christ"],
                "elements": ["cross", "nailed hands", "lifted face"],
                "setting": "the cross, low angle", "scope": "specific",
                "doctrine": "Father, forgive them (Luke 23:34)"},
            "father_forgive_them_face": {
                "subject": "close of Christ's face lifted in prayer at the cross",
                "characters": ["the crucified Christ"],
                "elements": ["lifted face", "cross beam"],
                "setting": "the cross, close", "scope": "specific",
                "doctrine": "Father, forgive them (Luke 23:34)"},
            "psalm22_scroll_david": {
                "subject": "the aged psalmist over a blank scroll, lyre and clay lamp",
                "characters": ["David the psalmist"],
                "elements": ["scroll", "lyre", "clay lamp", "night"],
                "setting": "night chamber, c.1000 BC", "scope": "specific",
                "doctrine": "they part my garments among them, and cast lots upon my vesture (Psalm 22:18)"},
            "us_under_cross_shadow": {
                "subject": "seven bowed mourners under the long shadow of the cross",
                "characters": ["seven bowed figures"],
                "elements": ["cross shadow", "bowed heads", "dust"],
                "setting": "Golgotha", "scope": "neutral",
                "doctrine": "the sin that put him there was ours (Rom 3:23)"},
            "golgotha_hill_wide": {
                "subject": "three occupied crosses on Golgotha outside the wall, midday-black sky",
                "characters": ["the crucified Christ", "two thieves", "mourners"],
                "elements": ["three crosses", "city wall", "black sky"],
                "setting": "Golgotha wide", "scope": "specific",
                "doctrine": "and there were also two other, malefactors, led with him (Luke 23:32)"},
            "willing_offering": {
                "subject": "the crucified Christ under a single golden shaft through the darkness",
                "characters": ["the crucified Christ", "kneeling mourner"],
                "elements": ["cross", "light shaft", "crown of thorns", "darkness"],
                "setting": "Golgotha", "scope": "specific",
                "doctrine": "he gave himself for us (Titus 2:14); no man taketh it from me (John 10:18)"},
            "darkness_veil_torn": {
                "subject": "the temple veil torn from top to bottom",
                "characters": [], "elements": ["torn veil", "temple columns"],
                "setting": "the temple", "scope": "specific",
                "doctrine": "the veil of the temple was rent in the midst (Luke 23:45)"},
            "risen_interceding_christ": {
                "subject": "the risen Christ interceding in a shaft of light, a sinner kneeling below",
                "characters": ["the risen Christ", "kneeling sinner"],
                "elements": ["raised healed hands", "light shaft"],
                "setting": "heavenly light", "scope": "specific",
                "doctrine": "he ever liveth to make intercession for them (Hebrews 7:25)"},
            "risen_mercy_hand": {
                "subject": "the risen Christ holding out the open healed hand",
                "characters": ["the risen Christ"],
                "elements": ["open hand", "healed mark", "warm light"],
                "setting": "golden light", "scope": "hero",
                "doctrine": "come, and receive mercy by faith (Rom 5:8; Heb 4:16)"},
        },
    },
}
(HERE / "piece.json").write_text(json.dumps(piece, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
print("piece.json written")

# hash-bound $0 clip copy (still bytes identical + verbatim LL entry => identical prompt+hash)
d_pj = load_piece(HERE)
s_prompt = animate_prompts(p_pj)["risen_mercy_hand"]
d_prompt = animate_prompts(d_pj)["risen_mercy_hand"]
s_png = PIERCED / "visual" / "risen_mercy_hand.png"
d_png = V / "risen_mercy_hand.png"
assert hashlib.sha256(s_png.read_bytes()).digest() == hashlib.sha256(d_png.read_bytes()).digest(), "mercy still not byte-identical"
assert s_prompt == d_prompt, "mercy LL prompts differ - no copy"
shutil.copy2(PIERCED / "visual" / "clips" / "risen_mercy_hand.mp4", CLIPS / "risen_mercy_hand.mp4")
an = d_pj["animate"]
(CLIPS / "risen_mercy_hand.src.sha").write_text(
    clip_src_hash(d_png, d_prompt, an["duration"], an["aspect_ratio"]), encoding="utf-8")
print("COPIED pierced_zech1210 -> father_forgive_them: risen_mercy_hand LL still+clip ($0, hash-bound)")

# ---- 4. livingpage_short.spec.json (16 beats, 57.15s) ----
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


spec = {
    "_doc": "FATHER FORGIVE THEM (Luke 23:34) 9:16 SHORT - living page (Wave E migration "
            "from the mocomic pilot). 16 beats / 57.15s. Nails hook -> the prayer nobody "
            "expected -> red-letter Luke 23:34 -> Psalm 22:18 receipt -> conviction (ours "
            "too) -> Rom 5:8 living-light reveal -> risen mercy-hand landing. Grade "
            "7200->7900K at the cross, warming to 4900K on the held-out hand.",
    "audio": "../audio/narration.mp3",
    "total": 57.15,
    "cut_ticks": False,
    "motion": "smooth",
    "heartbeat": {"from": 28.0, "to": 36.2, "gain": -9, "bpm": 60},
    "beats": [
        beat(0.0, 3.4, "big_inset",
             [{"slug": "nail_through_hand", "motion": "pushin"},
              {"slug": "executioner_ignorance", "motion": "pushin"}],
             {"type": "caption", "text": "Nails through his hands.", "kw": "NAILS"},
             7200, punch=True, ramp=True,
             sfx=[["nail_strike_single", 0.15, -10]],
             takeover={"panel": 0, "start": 2.3, "zoom": 1.24}),
        beat(3.4, 7.0, "two_v",
             ["soldiers_gambling_establish", "seamless_robe_lots_cast"],
             {"type": "caption", "text": "Soldiers at his feet, gambling for his clothes.", "kw": "GAMBLING"},
             7400),
        beat(7.0, 10.31, "stack_h",
             [{"slug": "crowd_mocking", "motion": "pushin"},
              {"slug": "father_forgive_them_face", "motion": "pushin", "bias": [0.5, 0.3]}],
             {"type": "caption", "text": "A word no one expected. Not a curse.", "kw": "NOT A CURSE"},
             7600, whip=True),
        beat(10.31, 12.46, "full", ["father_forgive_them_face"],
             {"type": "caption", "text": "It is a prayer.", "kw": "A PRAYER"}, 7500),
        grid(12.46, 16.94, "hero_frac3", "us_under_cross_shadow",
             {"type": "caption", "text": "Jesus prays for the very people putting him to death.", "kw": "PRAYS FOR THEM"},
             7700,
             [[1.0, 0.5, 0.5], [1.5, 0.3, 0.55], [1.6, 0.52, 0.55]],
             ["left", "up", "down"], 0.35),
        beat(16.94, 22.06, "full", ["face_on_cross_speaks"],
             {"type": "redletter", "text": "Father, forgive them; for they know not what they do.",
              "speaker": "JESUS", "ref": "Luke 23:34"},
             7900),
        beat(22.06, 24.22, "two_v",
             ["psalm22_scroll_david", "seamless_robe_lots_cast"],
             {"type": "caption", "text": "Luke records it as they gambled:", "kw": "GAMBLED"},
             7700),
        beat(24.22, 28.0, "full", ["psalm22_scroll_david"],
             {"type": "redletter", "text": "And they parted his raiment, and cast lots.",
              "speaker": "SCRIPTURE", "ref": "Luke 23:34 / Psalm 22:18"},
             7800),
        beat(28.0, 32.37, "big_inset",
             [{"slug": "executioner_ignorance", "motion": "pushin"},
              {"slug": "nail_through_hand", "motion": "pushin"}],
             {"type": "caption", "text": "It does not excuse the sin; it intercedes for the sinner.", "kw": "INTERCEDES"},
             7500),
        grid(32.37, 36.2, "hero_band3", "golgotha_hill_wide",
             {"type": "caption", "text": "The sin that put him there was ours too.", "kw": "OURS TOO"},
             7300,
             [[1.0, 0.5, 0.28], [1.45, 0.5, 0.18], [1.6, 0.5, 0.72]],
             ["up", "left", "down"], 0.3, whip=True),
        beat(36.2, 39.8, "stack_h",
             [{"slug": "willing_offering", "motion": "pushin", "bias": [0.5, 0.4]},
              {"slug": "darkness_veil_torn", "motion": "pushin", "bias": [0.5, 0.45]}],
             {"type": "caption", "text": "He gave himself willingly.", "kw": "WILLINGLY"},
             7000),
        beat(39.8, 42.84, "full", ["risen_interceding_christ"],
             {"type": "caption", "text": "He still lives to make intercession for sinners.", "kw": "HE LIVES"},
             6400),
        {**beat(42.84, 48.5, "full", ["willing_offering"],
                {"type": "redletter", "text": "While we were yet sinners, Christ died for us.",
                 "speaker": "SCRIPTURE", "ref": "Romans 5:8"},
                6000),
         "fx": {"temp": 6000, "rays": {"at": [0.1, 0.03], "strength": 0.5}}},
        grid(48.5, 51.85, "hero_frac3", "risen_interceding_christ",
             {"type": "caption", "text": "Pleading mercy before we knew we needed it.", "kw": "MERCY"},
             5800,
             [[1.15, 0.5, 0.4], [1.55, 0.5, 0.21], [1.5, 0.3, 0.82]],
             ["left", "up", "down"], 0.35),
        beat(51.85, 54.4, "full", ["risen_mercy_hand"],
             {"type": "caption", "text": "That mercy is held out to you now", "kw": "HELD OUT TO YOU"},
             5400, punch=True,
             border_break={"at": 52.1},
             sfx=[["dawn_morning_warm", 51.95, -13]]),
        beat(54.4, 57.15, "full", ["risen_mercy_hand"],
             {"type": "caption", "text": "Come, and receive it by faith.", "kw": "BY FAITH"},
             4900),
    ],
}
(V / "livingpage_short.spec.json").write_text(json.dumps(spec, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
print(f"livingpage_short.spec.json written: {len(spec['beats'])} beats")

# ---- 5. wave checklist seed ----
(V / "wave_checklist.json").write_text(json.dumps({
    "piece": "father_forgive_them", "created": "2026-07-15",
    "items": [{"name": n, "pass": None, "note": "", "reviewer": "sanjay"} for n in
              ("scale_variety", "grids_multi_figure", "audio_diff", "bookend",
               "filmstrip_qc", "before_after_review", "fit_gate_disposition",
               "swapped_stills_review")],
}, indent=1), encoding="utf-8")
print("wave_checklist.json seeded")
