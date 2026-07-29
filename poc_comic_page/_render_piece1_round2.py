"""Piece 1 Gate 2 feedback round (poc_comic_page/_piece1/_ART_DIRECTION_ROUND2.md):
10 renders -- 3 fixes, 2 camera/density demos, 4 palette tests, 1 hard scene.
Prompts copied VERBATIM from Fable's doc. NBP nano_banana_pro, 2cr each, $3.00
planned (+$1.20 re-roll reserve) -- user-approved 2026-07-27.

  .venv\\Scripts\\python.exe poc_comic_page/_render_piece1_round2.py
"""
import re, subprocess, sys, time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import config
from pipeline import cost

HF = str(config.HF_CLI_PATH)
MODEL = "nano_banana_pro"
EPISODE = "CPP_InNoWise_GoldSeam"
HERE = Path(__file__).resolve().parent
OUT = HERE / "_piece1" / "round2"
OUT.mkdir(parents=True, exist_ok=True)
CS = HERE / "_piece1" / "charsheets"
JESUS_REF = CS / "jesus.png"
SEEKER_REF = CS / "seeker.png"

HARD_CAP_USD = 4.20  # 20cr planned + 8cr reroll reserve = 28cr = $4.20

TEXT_BLOCK = (
    "GLOBAL TEXTUAL CONSTRAINT: NO text of any kind anywhere -- no speech "
    "bubbles, no caption boxes, no lettering. Pure artwork only."
)
FRAME_BLOCK = (
    "GLOBAL FRAME CONSTRAINT: one single continuous full-bleed illustration "
    "-- the artwork fills the entire frame edge to edge, with no panel "
    "borders, no gutters, no page margins, no visible paper or page edges."
)

# (name, ar, refs, style, scene, closing_and_figure_constraint)
RENDERS = [
    ("R1_panel_b_door_fix", "1:1", [],
     "Modern dynamic painted comic-book art: energetic loose black ink drawing over fully painted color; "
     "where the key light strikes an edge the ink line gives way to a thin unbroken seam of warm gold "
     "rim-light, the shadow side holding thick loose ink. A palette of warm gold light, deep storm "
     "blue-black shadow, and earthy desert tans, painted with atmospheric depth. One clear key light with "
     "a stated direction. Every region of the frame carries drawn painted incident -- weathered stone "
     "coursing, small period objects resting in shadow, drifting dust and lamp-glow haze -- all held dark "
     "and quiet beneath the key light, so the subject keeps the brightest value and the sharpest edge. "
     "Skies are deep, still and windless, painted with quiet incident -- banked cloud masses edged in "
     "faint moonlight, scattered stars.",
     "SCENE: A heavy arched wooden door, closed, set deep in a thick ancient stone wall, first-century "
     "Judea, at night -- seen level from a quiet three-quarter angle so the arch and wall recede with "
     "depth. Warm gold lamplight bleeds through the seam between the door's planks and spills under the "
     "sill onto worn flagstones. An oil lamp in a wall niche beside the arch, a moth circling its flame; "
     "drifted leaves against the sill; the courtyard before the door empty and still; beyond the wall, "
     "dark rooftops of the sleeping city under the painted night sky. The door itself is the whole "
     "subject -- patient, lit from within, waiting.",
     "Painted comic-book art, gold seam rim-light, full painted depth. " + TEXT_BLOCK + " " + FRAME_BLOCK +
     " GLOBAL FIGURE CONSTRAINT: this scene contains NO human figures -- no people, no silhouettes, no "
     "bystanders anywhere in the frame."),

    ("R2_panel_c_scroll_fix", "1:1", [SEEKER_REF],
     "Modern dynamic painted comic-book art: energetic loose black ink drawing over fully painted color; "
     "where the key light strikes a figure's edge the ink line gives way to a thin unbroken seam of warm "
     "gold rim-light, the shadow side holding thick loose ink. A palette of warm gold light, deep storm "
     "blue-black shadow, and earthy desert tans, painted with atmospheric depth. One clear key light with "
     "a stated direction. Every region of the frame carries drawn painted incident held dark and quiet "
     "beneath the key light, so the subject keeps the brightest value and the sharpest edge.",
     "SCENE: Extreme close-up, filling the whole frame: a weary traveler's two weathered hands clutching "
     "a rolled parchment scroll bound with cord and a dark wax seal, lamplight catching the hands' edges "
     "in a fine gold seam, the ragged sleeves of a rough cloak in deep shadow. Behind the hands the night "
     "courtyard falls away in soft painted depth -- dark stone, the faint warm glow of a distant lamplit "
     "arch, drifting dust in the light. The hands match the reference image: the same aged, weathered man.",
     "Painted comic-book art, gold seam rim-light, full painted depth. " + TEXT_BLOCK + " " + FRAME_BLOCK +
     " GLOBAL FIGURE CONSTRAINT: exactly ONE person appears, shown only from the forearms down -- no "
     "other people, no faces, no background figures."),

    ("R3_panel_d_threshold_fix", "1:1", [SEEKER_REF],
     "Modern dynamic painted comic-book art: energetic loose black ink drawing over fully painted color; "
     "where the key light strikes a figure's edge the ink line gives way to a thin unbroken seam of warm "
     "gold rim-light, the shadow side holding thick loose ink. A palette of warm gold light, deep storm "
     "blue-black shadow, and earthy desert tans, painted with atmospheric depth. One clear key light with "
     "a stated direction. Every region of the frame carries drawn painted incident -- weathered stone "
     "coursing, drifting dust in the light -- held dark and quiet beneath the key light, so the figure "
     "keeps the brightest value and the sharpest edge.",
     "SCENE: A weary grey-haired traveler in a rough ragged hooded cloak, mid-stride as he steps through "
     "a great open arched doorway, seen from a low three-quarter angle just inside the arch, the stone "
     "lines of the archway converging dramatically above him. Warm gold light floods past him from "
     "within, casting his long shadow onto the worn flagstones; one hand braces the door's edge; the "
     "night's blue-black darkness recedes behind him with the sleeping city's rooftops far below the "
     "wall. He matches the reference image exactly: the same aged, weathered face and rough cloak.",
     "Painted comic-book art, gold seam rim-light, full painted depth. " + TEXT_BLOCK + " " + FRAME_BLOCK +
     " GLOBAL FIGURE CONSTRAINT: exactly ONE person appears in this image -- no second figure, no one in "
     "the doorway behind him, no silhouettes, no bystanders."),

    ("R4_p1a_dense_burden_view", "1:1", [SEEKER_REF],
     "Modern dynamic painted comic-book art: energetic loose black ink drawing over fully painted color; "
     "where the key light strikes a figure's edge the ink line gives way to a thin unbroken seam of warm "
     "gold rim-light, the shadow side holding thick loose ink. A palette of warm gold light, deep storm "
     "blue-black shadow, and earthy desert tans, painted with atmospheric depth. One clear key light with "
     "a stated direction. Every region of the frame carries drawn painted incident -- weathered stone "
     "coursing, worn flagstones, small period objects resting in shadow, drifting dust and lamp-glow haze "
     "-- all held dark and quiet beneath the key light, so the figure keeps the brightest value and the "
     "sharpest edge.",
     "SCENE: Seen from high above, looking steeply down from the top of the ancient stone wall: a small, "
     "weary grey-haired traveler in a rough ragged hooded cloak stands alone before a heavy arched wooden "
     "door at night, clutching a rolled parchment scroll. Warm gold lamplight bleeds under the door and "
     "from a wall-niche oil lamp, pooling around him on the worn flagstones and throwing his long shadow "
     "across the courtyard. Around him the courtyard spreads wide -- cracked flagstones, drifted leaves, "
     "a shallow stone step, the wall's massive coursing falling away below the camera -- and beyond, the "
     "dark rooftops of the sleeping city. He looks very small before the great door. He matches the "
     "reference image exactly.",
     "Painted comic-book art, gold seam rim-light, full painted depth. " + TEXT_BLOCK + " " + FRAME_BLOCK +
     " GLOBAL FIGURE CONSTRAINT: exactly ONE person appears in this image -- no other people, no "
     "background figures, no silhouettes."),

    ("R5_p2a_doorframe_eye", "9:16", [SEEKER_REF],
     "Modern dynamic painted comic-book art: energetic loose black ink drawing over fully painted color; "
     "where the key light strikes a figure's edge the ink line gives way to a thin unbroken seam of warm "
     "gold rim-light, the shadow side holding thick loose ink. A palette of warm gold light, deep storm "
     "blue-black shadow, and earthy desert tans, painted with atmospheric depth. One clear key light with "
     "a stated direction. Every region of the frame carries drawn painted incident -- weathered stone, "
     "hanging oil lamp, a moth at the flame, drifting dust in the lamp glow -- held dark and quiet beneath "
     "the key light, so the figure keeps the brightest value and the sharpest edge.",
     "SCENE: Shot from just beside the great door, the door's massive iron-banded wooden edge filling the "
     "left third of the frame close to camera in deep soft shadow. Past it, in the midground, a weary "
     "grey-haired traveler in a rough ragged hooded cloak stands in the lamplight rehearsing his words -- "
     "head lowered, one hand half-raised as if practicing a plea, the rolled parchment scroll clutched in "
     "the other. Warm gold light from the wall lamp rims his edge in a fine gold seam; behind him the "
     "stone wall recedes into painted night depth with the city rooftops beyond. He matches the reference "
     "image exactly.",
     "Painted comic-book art, gold seam rim-light, full painted depth. " + TEXT_BLOCK + " " + FRAME_BLOCK +
     " GLOBAL FIGURE CONSTRAINT: exactly ONE person appears in this image -- no other people, no "
     "background figures, no silhouettes."),

    ("R6_moonlight_night", "1:1", [SEEKER_REF],
     "Modern dynamic painted comic-book art: energetic loose black ink drawing over fully painted color; "
     "where the moonlight strikes a figure's edge the ink line gives way to a thin unbroken seam of cool "
     "silver-blue rim-light, the shadow side holding thick loose ink. A nocturne palette of deep indigo "
     "and slate blue-black shadow, bone-pale moonlit stone and cool grey cloth -- with warm amber "
     "lamplight held ONLY inside doorways and windows, small warm promises against the cold silver night. "
     "One clear key light: the moon, its direction stated. Every region of the frame carries drawn "
     "painted incident -- weathered stone coursing, worn flagstones, drifted leaves, drifting night mist "
     "-- all held dark and quiet beneath the moonlight, so the figure keeps the brightest value and the "
     "sharpest edge. Skies are deep, still and windless, painted with quiet incident -- banked cloud "
     "masses edged in silver moonlight, scattered stars.",
     "SCENE: A weary grey-haired traveler in a rough ragged hooded cloak stands alone before a heavy "
     "arched wooden door in a thick ancient stone wall at night, first-century Judea, clutching a rolled "
     "parchment scroll, moonlight from high left rimming his cloak's edge in a fine silver seam. Warm "
     "amber lamplight bleeds through the door's seams and under the sill -- the only warmth in the frame. "
     "Worn flagstones in the foreground, the sleeping city's rooftops beyond the wall. He matches the "
     "reference image exactly.",
     "Painted comic-book art, silver-blue moonlight seam rim-light, cold nocturne palette with warm light "
     "only inside the doorway, full painted depth. " + TEXT_BLOCK + " " + FRAME_BLOCK +
     " GLOBAL FIGURE CONSTRAINT: exactly ONE person appears in this image -- no other people, no "
     "background figures, no silhouettes."),

    ("R7_moonlight_glory", "3:4", [JESUS_REF],
     "Modern dynamic painted comic-book art: energetic loose black ink drawing over fully painted color; "
     "where the light strikes a figure's edge the ink line gives way to a thin unbroken seam of radiant "
     "silver-white rim-light, the shadow side holding thick loose ink. A nocturne palette of deep indigo "
     "and slate blue-black, bone-pale stone -- with warm amber interior light pouring through the open "
     "door around the figure. One clear key light: the doorway's light behind and around him. Every "
     "region of the frame carries drawn painted incident -- the arch's carved stone, drifting dust "
     "glowing in the light shaft, worn flagstones -- held quiet beneath the light, so the figure keeps "
     "the brightest value and the sharpest edge.",
     "SCENE: Jesus -- long dark hair, short dark beard, simple cream first-century robe with a cloth sash "
     "-- stands in a great open arched doorway, seen from a low angle looking up, the painted night sky "
     "and the arch rising behind him, his face open and glad, one hand extended in welcome. Light floods "
     "around him from the doorway, his whole edge burning in a radiant silver-white seam, his long shadow "
     "reaching toward the camera down the worn steps. He matches the reference image exactly: same face, "
     "same build, same dress.",
     "Painted comic-book art, radiant silver seam rim-light, nocturne palette with warm doorway light, "
     "full painted depth. " + TEXT_BLOCK + " " + FRAME_BLOCK +
     " GLOBAL FIGURE CONSTRAINT: exactly ONE person appears in this image -- no other people, no "
     "background figures, no silhouettes."),

    ("R8_ember_night", "1:1", [SEEKER_REF],
     "Modern dynamic painted comic-book art: energetic loose black ink drawing over fully painted color; "
     "where the firelight strikes a figure's edge the ink line gives way to a thin unbroken seam of warm "
     "copper-rose rim-light, the shadow side holding thick loose ink. A palette of burnt umber, wine-dark "
     "shadow, ash-violet and dusk-rose sky, deep earthy tans -- the light of banked embers and oil lamps, "
     "warm and low. One clear key light with a stated direction. Every region of the frame carries drawn "
     "painted incident -- weathered stone coursing, worn flagstones, drifted leaves, drifting smoke from "
     "evening fires -- all held dark and quiet beneath the key light, so the figure keeps the brightest "
     "value and the sharpest edge. Skies are deep, still and windless, painted with quiet incident -- "
     "banked cloud masses edged faintly in dusk-rose, early stars.",
     "SCENE: A weary grey-haired traveler in a rough ragged hooded cloak stands alone before a heavy "
     "arched wooden door in a thick ancient stone wall at dusk, first-century Judea, clutching a rolled "
     "parchment scroll, low lamplight from the wall niche rimming his cloak's edge in a fine copper-rose "
     "seam. Warm light bleeds through the door's seams and under the sill onto the worn flagstones; the "
     "sleeping city's rooftops fade into the ash-violet dusk beyond the wall. He matches the reference "
     "image exactly.",
     "Painted comic-book art, copper-rose ember seam rim-light, warm low-light palette, full painted "
     "depth. " + TEXT_BLOCK + " " + FRAME_BLOCK +
     " GLOBAL FIGURE CONSTRAINT: exactly ONE person appears in this image -- no other people, no "
     "background figures, no silhouettes."),

    ("R9_ember_glory", "3:4", [JESUS_REF],
     "Modern dynamic painted comic-book art: energetic loose black ink drawing over fully painted color; "
     "where the light strikes a figure's edge the ink line gives way to a thin unbroken seam of radiant "
     "copper-gold rim-light, the shadow side holding thick loose ink. A palette of burnt umber, wine-dark "
     "shadow, ash-violet dusk and deep earthy tans -- with a great warm light pouring through the open "
     "door around the figure. One clear key light: the doorway's light behind and around him. Every "
     "region of the frame carries drawn painted incident -- the arch's carved stone, drifting dust "
     "glowing in the light shaft, worn flagstones -- held quiet beneath the light, so the figure keeps "
     "the brightest value and the sharpest edge.",
     "SCENE: Jesus -- long dark hair, short dark beard, simple cream first-century robe with a cloth sash "
     "-- stands in a great open arched doorway, seen from a low angle looking up, the dusk sky and the "
     "arch rising behind him, his face open and glad, one hand extended in welcome. Light floods around "
     "him from the doorway, his whole edge burning in a radiant copper-gold seam, his long shadow reaching "
     "toward the camera down the worn steps. He matches the reference image exactly: same face, same "
     "build, same dress.",
     "Painted comic-book art, radiant copper-gold seam rim-light, warm low-light palette, full painted "
     "depth. " + TEXT_BLOCK + " " + FRAME_BLOCK +
     " GLOBAL FIGURE CONSTRAINT: exactly ONE person appears in this image -- no other people, no "
     "background figures, no silhouettes."),

    ("R10_mockers_hard_scene", "16:9", [JESUS_REF],
     "Modern dynamic painted comic-book art: energetic loose black ink drawing over fully painted color; "
     "where the failing light touches a figure's edge the ink line gives way to a thin, faint seam of "
     "warm gold rim-light, the shadow side holding thick loose ink. A palette of deep storm blue-black "
     "shadow and earthy desert tans under a dimmed gold light, painted with atmospheric depth. One clear "
     "key light with a stated direction: the last dim light from the west. Every region of the frame "
     "carries drawn painted incident -- trampled dust and stones, scattered garments, spear tips of "
     "distant soldiers, the far city wall of Jerusalem -- all held dark and quiet. Skies are deep, still, "
     "even fields of painted tone -- the sun blotted out, daylight failed to a deep still dusk -- calm, "
     "windless, held, their drama carried by light and color alone.",
     "SCENE: The camera stands level at the eye height of a grieving witness on the ground, a quiet "
     "mid-distance from Golgotha, the horizon level and calm. Filling the frame's right edge, close to "
     "camera: the dark soft silhouette of a witness's shoulder and bowed head in profile, storm blue-black "
     "shadow, no light on them. In the midground three mockers caught mid-motion -- heads thrown back "
     "wagging, one arm flung out pointing, mouths open in scorn -- their edges catching a faint gold "
     "seam, their faces clear. Behind them a sparse crowd stands as massed dark silhouettes in the failed "
     "light. Beyond and above, one wooden cross stands alone on the rocky crest -- a single upright, a "
     "single crossbeam -- and Jesus hangs on that one cross, the whole figure visible and small at this "
     "distance, his arms stretched out along the crossbeam with his wrists near its ends, his body gaunt "
     "and wasted, his head bowed beneath the crown of thorns, the seam of light on his edge thin and "
     "faint. His face matches the reference image: long dark hair, short dark beard. Still, silent, "
     "reverent.",
     "Painted comic-book art, faint gold seam rim-light in failed light, storm blue-black palette, full "
     "painted depth. " + TEXT_BLOCK + " " + FRAME_BLOCK +
     " GLOBAL FIGURE CONSTRAINT: exactly ONE cross and ONE crucified figure; three mockers with visible "
     "faces; all other people only as dark featureless silhouettes; the foreground witness is a silhouette "
     "only, with no visible face."),
]


def _find_job(model, started_after_iso):
    try:
        r = subprocess.run([HF, "generate", "list", "--image", "--size", "10", "--json"],
                            capture_output=True, text=True, encoding="utf-8", errors="replace")
        import json
        jobs = json.loads(r.stdout or "[]")
    except Exception as e:
        print(f"   (job lookup failed: {e})")
        return None
    for j in jobs:
        if j.get("job_type") == model and j.get("created_at", "") >= started_after_iso:
            if j.get("status") == "completed" and j.get("result_url"):
                return j["result_url"]
    return None


def run(prompt, out, refs, ar):
    started = time.strftime("%Y-%m-%dT%H:%M:%S", time.gmtime())
    cmd = [HF, "generate", "create", MODEL, "--prompt", prompt, "--aspect_ratio", ar,
           "--resolution", "2k", "--wait"]
    for r in refs:
        cmd += ["--image", str(r)]
    p = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    blob = (p.stdout or "") + "\n" + (p.stderr or "")
    if re.search(r"nsfw", blob, re.IGNORECASE):
        print("   NSFW-REJECTED"); return False
    urls = re.findall(r'https?://\S+?\.(?:png|jpg|jpeg|webp)', blob) or re.findall(r'https?://\S+', blob)
    if not urls and re.search(r"time(d)?\s*out|timeout", blob, re.IGNORECASE):
        print("   --wait timed out; polling `hf generate list` ...")
        for _ in range(20):
            time.sleep(15)
            u = _find_job(MODEL, started)
            if u:
                urls = [u]
                print("   recovered job via `hf generate list`")
                break
    if not urls:
        print(f"   no url: {blob.strip()[-300:]}"); return False
    subprocess.run(["curl", "-s", "-L", urls[-1], "-o", str(out)], check=True)
    return out.exists() and out.stat().st_size > 1000


def main():
    spent = 0.0
    results = []
    for name, ar, refs, style, scene, closing in RENDERS:
        out = OUT / f"{name}.png"
        prompt = style + "\n\n" + scene + "\n\n" + closing
        print(f"[img] {name} ...", flush=True)
        if spent >= HARD_CAP_USD:
            print(f"   STOP: hard cap ${HARD_CAP_USD:.2f} reached.")
            results.append((name, "ESCALATED-cap")); continue
        ok = run(prompt, out, refs, ar)
        if not ok:
            print("   retrying once ...")
            time.sleep(5)
            ok = run(prompt, out, refs, ar)
        if ok:
            try:
                row = cost.record_hf(EPISODE, "short", "round2", MODEL, note=f"[piece1-r2] {name}")
                spent += float(row.get("est_usd") or 0)
            except Exception as e:
                print(f"   (ledger record skipped: {e})")
            print(f"   ok  running spend ~${spent:.2f}")
            results.append((name, "clean"))
        else:
            print("   FAILED (twice)")
            results.append((name, "FAILED"))
    print(f"\n[out] {OUT}")
    print(f"[spend] ~${spent:.2f} of ${HARD_CAP_USD:.2f} cap")
    for name, status in results:
        print(f"  {name}: {status}")


if __name__ == "__main__":
    main()
