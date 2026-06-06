"""ONE-SHOT migration: fold the Isaiah-53 hardcoded per-scene tables (previously
living inside _render_images_16x9.py / _animate_16x9.py / _assemble_16x9.py) INTO
its visual_16x9/scene_plan.json, so the now-episode-generic drivers reproduce the
exact same Isaiah output by reading the plan. Idempotent. Safe to re-run."""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _episode import Episode, LONGFORM

# --- the former hardcoded tables (verbatim copies) -------------------------------
MOTION = {
    1:  ("very slow push-in",            "wind-blown dust and slowly drifting clouds"),
    2:  ("very slow drift across the scroll", "a gently flickering candle flame"),
    3:  ("slow rise",                    "softly radiating golden light"),
    4:  ("extremely slow push-in to the face", "a faint shift of shadow only"),
    5:  ("slow pull-back",               "distant figures barely shifting"),
    6:  ("very slow push-in",            "hair and cloth barely stirring, somber stillness"),
    7:  ("slow lateral drift",           "a faint shift of light"),
    8:  ("slow pan across the hillside", "sheep grazing slightly and grass moving in the wind"),
    9:  ("slow follow of the lamb",      "gentle dust and light"),
    10: ("slow push-in",                 "shadowed figures still, faint flame light"),
    11: ("slow lateral track",           "the procession slowly walking, dust"),
    12: ("slow approach to the tomb",    "drifting dusk haze"),
    13: ("slow tracking alongside",      "the chariot and horses moving along the road, wheels turning, dust"),
    14: ("slow push-in to the meeting",  "warm low sun, faint dust"),
    15: ("slow tilt up into the light",  "gentle growing radiance"),
    16: ("very slow push-in",            "the shaft of heaven's light steady, clouds churning slowly, robe faintly moving"),
    17: ("slow rise with the brightening dawn", "drifting morning mist"),
    18: ("slow push-in",                 "golden light gently glowing, robe still"),
    19: ("slow reveal",                  "light softly shifting"),
    20: ("very slow push-in to the offered hand", "a faint halo glow"),
    21: ("very slow settle and hold",    "a gentle reverent glow"),
}
JESUS = {6: "passion", 15: "resurrection", 16: "passion", 18: "resurrection",
         19: "resurrection", 20: "resurrection", 21: "resurrection"}
DIRECTIONAL = {8, 9, 11, 13, 14, 20}
REDONE = {1, 2, 3, 6, 7, 10, 11, 12, 13, 14, 15, 16}  # cosmetic gallery badges
BANK = {
    1:  ("wilderness_dusk_lone_figure", "neutral", ["wilderness","desert","dusk","lone-figure","landscape"]),
    2:  ("scroll_candlelight_hands", "neutral", ["scroll","parchment","candlelight","hands","study"]),
    3:  ("glory_exalted_light_figure", "neutral", ["glory","light","exalted","heaven","radiance"]),
    4:  ("isa53_marred_face", "specific", ["suffering","face","sorrow","passion"]),
    5:  ("isa53_despised_rejected", "specific", ["rejection","crowd","isolation","sorrow"]),
    6:  ("christ_crucified_robed_pierced", "neutral", ["crucifixion","cross","christ","passion"]),
    7:  ("isa53_servant_bearing_weight", "specific", ["substitution","burden","servant"]),
    8:  ("scattered_sheep_hillside_dusk", "neutral", ["sheep","flock","hillside","astray","shepherd"]),
    9:  ("lamb_led_to_slaughter", "neutral", ["lamb","sacrifice","altar","sheep"]),
    10: ("isa53_servant_silent_trial", "specific", ["trial","silence","accusers","servant"]),
    11: ("exiled_nation_column_grey", "neutral", ["exile","nation","israel","procession","journey"]),
    12: ("rich_mans_tomb_dusk", "neutral", ["tomb","grave","burial","stone","dusk"]),
    13: ("isa53_eunuch_chariot_gaza", "specific", ["chariot","eunuch","gaza-road","acts8","desert-road"]),
    14: ("isa53_philip_meets_chariot", "specific", ["philip","chariot","meeting","road","acts8"]),
    15: ("isa53_philip_preaches_jesus", "specific", ["philip","revelation","christ","acts8"]),
    16: ("christ_crucified_dark_sky_golgotha", "neutral", ["crucifixion","cross","christ","storm-sky","golgotha"]),
    17: ("dawn_over_tomb_stone", "neutral", ["dawn","tomb","morning","resurrection","stone"]),
    18: ("christ_risen_morning_light", "neutral", ["resurrection","christ","risen","glory","morning"]),
    19: ("christ_arm_of_the_lord_hand", "neutral", ["christ","hand","arm","light","risen"]),
    20: ("christ_reaching_hand_grace", "neutral", ["christ","grace","hand","invitation"]),
    21: ("christ_risen_glory_hero", "neutral", ["christ","risen","glory","hero","light"]),
}
STYLE_BASE = ("Baroque oil painting, dramatic chiaroscuro, Caravaggio and Rembrandt lighting, "
              "deep shadow and warm golden light, reverent sacred art, muted earth tones, "
              "fine visible brushwork")
STYLE_TAIL = "no text, no modern elements, cinematic 16:9 widescreen composition"

ep = Episode(LONGFORM / "01_Isaiah_53_Suffering_Servant" / "v1")
plan = ep.plan
plan["episode"] = "Isaiah 53 — The Suffering Servant"
plan.setdefault("film_name", "Isaiah53_16x9.mp4")
plan["style_base"] = STYLE_BASE
plan["style_tail"] = STYLE_TAIL
plan.setdefault("image_provider", "nbp")
plan.setdefault("animation", {"model": "veo3_1_lite", "aspect": "16:9", "duration": 8})

for s in plan["scenes"]:
    i = s["id"]
    if i in MOTION:
        s["camera"] = MOTION[i][0]            # overwrite to the value that produced the clips
        s["atmos"] = MOTION[i][1]
    s["jesus_variant"] = JESUS.get(i)
    s["directional"] = i in DIRECTIONAL
    s["redone"] = i in REDONE
    if i in BANK:
        slug, scope, tags = BANK[i]
        s["bank"] = {"slug": slug, "scope": scope, "tags": tags}
    else:
        s.setdefault("bank", None)

ep.save_plan()
print(f"[migrated] {ep.scene_plan_path}")
print(f"  {len(plan['scenes'])} scenes · film_name={plan['film_name']}")
print(f"  jesus_variants: {sum(1 for s in plan['scenes'] if s.get('jesus_variant'))}")
print(f"  directional: {[s['id'] for s in plan['scenes'] if s.get('directional')]}")
print(f"  banked slugs: {sum(1 for s in plan['scenes'] if s.get('bank'))}")
