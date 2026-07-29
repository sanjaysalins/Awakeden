"""Piece 1 FULL PERIOD-ACCURACY PASS: all 15 stills re-rendered against the
corrected v2 character sheets, with world-consistency corrections applied
throughout (user feedback: door/lamp/boots/hood/setup all read anachronistic):
  - door: plain unadorned wood-plank, wooden bar-latch, NO iron studs/ring/knob
  - lamp: small terracotta pinched-spout saucer lamp, NO glass chimney/lantern
  - head-covering: loose mantle draped over the head, NOT a tailored hood
  - feet: leather thong sandals, NO boots
  - rooftops: flat ancient stone roofs, NOT pitched/gabled
Camera/register choices carry over unchanged from the approved set (Burden
View for p1a, Doorframe Eye for p2a, the no-invented-people fixes for
panel_b/c/d). NBP nano_banana_pro, 2cr/still, 30cr for 15.

  .venv\\Scripts\\python.exe poc_comic_page/_render_piece1_stills_v2.py
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
OUT = HERE / "_piece1" / "stills_v2"
OUT.mkdir(parents=True, exist_ok=True)
CS = HERE / "_piece1" / "charsheets_v2"
JESUS_REF = CS / "jesus.png"
SEEKER_REF = CS / "seeker.png"

HARD_CAP_USD = 6.00

CONSTRAINT = (
    "GLOBAL TEXTUAL CONSTRAINT: NO text of any kind anywhere -- no speech "
    "bubbles, no caption boxes, no lettering. Pure artwork only."
)
FIGURE_BASE = (
    "He matches the reference image exactly: same face, same build, a loose "
    "woolen mantle draped over his head (not a fitted hood), leather thong "
    "sandals on bare feet -- no boots."
)

GLORY_STYLE = (
    "Modern dynamic painted comic-book art: energetic loose black ink drawing "
    "over fully painted color; where the key light strikes a figure's edge "
    "the ink line gives way to a thin seam of warm gold rim-light, the "
    "shadow side holding thick loose ink. A palette of warm gold light, deep "
    "storm blue-black shadow, and earthy desert tans, painted with "
    "atmospheric depth. One clear key light with a stated direction. Skies "
    "are deep, still, even fields of painted tone -- calm, windless, held -- "
    "their drama carried by light and color alone. A sweeping cinematic "
    "camera angle; lean everyday human figures in simple first-century "
    "dress; expressive lifelike faces; visible painterly brushwork in cloth "
    "and ground."
)
GLORY_CLOSING = (
    "Render with the gold-seam rule throughout: light-side edges are thin "
    "warm gold seams, shadow-side ink stays thick and black."
)
GLORY_HERO_CLOSING = (
    "Render with the gold-seam rule throughout: the seam is wide and "
    "radiant, the camera a low earned hero angle looking up, triumphant."
)

PASSION_STYLE = (
    "Modern dynamic painted comic-book art: energetic loose black ink "
    "drawing over fully painted color; where the failing light touches an "
    "edge the ink line gives way to a thin, faint seam of warm gold "
    "rim-light, the shadow side holding thick loose ink. A palette of deep "
    "storm blue-black shadow and earthy desert tans under a dimmed gold "
    "light, painted with atmospheric depth. One clear key light with a "
    "stated direction. Skies are deep, still, even fields of painted tone "
    "-- calm, windless, held -- their drama carried by light and color "
    "alone. The camera stands level at the eye height of a grieving witness "
    "on the ground, a quiet mid-distance away, the horizon level and calm "
    "in frame. Everyday human figures in the servant register; expressive "
    "lifelike faces; visible painterly brushwork in cloth and ground."
)
PASSION_CLOSING = (
    "Render with the gold-seam rule throughout: the seam stays faint and "
    "close to the body, the camera level and human -- never a hero angle "
    "-- mood calm and still."
)

DOOR_CLOSED = (
    "a heavy arch-topped wood-plank door, plain and unadorned, set deep in "
    "a thick ancient stone wall -- bare timber planks only, no iron studs, "
    "no metal bands, no ring-pull, no handle or knob of any kind, closed "
    "with a simple wooden bar-latch"
)
DOOR_OPEN = (
    "a heavy arch-topped wood-plank door, plain and unadorned -- bare "
    "timber planks only, no iron studs, no metal fittings, no handle or "
    "knob of any kind -- standing open"
)
LAMP = (
    "a small squat terracotta oil lamp with a pinched wick-spout resting in "
    "the wall niche, its flame low and steady -- no glass, no chimney, no "
    "lantern of any kind"
)
ROOFTOPS = "flat ancient stone rooftops of the sleeping city, low and unadorned -- no pitched or gabled roofs"

# (name, page, aspect_ratio, refs, style, closing, scene_text)
PANELS = [
    ("p1a_night_door", "page1", "1:1", [SEEKER_REF], GLORY_STYLE, GLORY_CLOSING,
     f"SCENE: Seen from high above, looking steeply down from the top of the ancient stone wall: "
     f"a small, weary grey-haired traveler stands alone before {DOOR_CLOSED} at night, clutching a "
     f"rolled parchment scroll. Warm gold light bleeds under the door and from {LAMP}, pooling "
     f"around him on the worn flagstones and throwing his long shadow across the courtyard. Around "
     f"him the courtyard spreads wide -- cracked flagstones, drifted leaves, a shallow stone step, "
     f"the wall's massive coursing falling away below the camera -- and beyond, {ROOFTOPS}. He "
     f"looks very small before the great door. {FIGURE_BASE}"),

    ("p1b_hesitant_hand", "page1", "1:1", [SEEKER_REF], GLORY_STYLE, GLORY_CLOSING,
     f"SCENE: Close-up from behind and beside the traveler: his weathered bare hand half-raised "
     f"toward {DOOR_CLOSED}, hesitating, not touching it; his other arm presses a rolled parchment "
     f"scroll to his chest. Cold dim light, a faint warm glow from the gap beneath the door. "
     f"{FIGURE_BASE}"),

    ("p2a_rehearsing", "page2", "9:16", [SEEKER_REF], GLORY_STYLE, GLORY_CLOSING,
     f"SCENE: Shot from just beside {DOOR_CLOSED}, the door's massive plain timber edge filling the "
     f"left third of the frame close to camera in deep soft shadow. Past it, in the midground, a "
     f"weary grey-haired traveler stands in the lamplight rehearsing his words -- head lowered, one "
     f"bare hand half-raised as if practicing a plea, the rolled parchment scroll clutched in the "
     f"other. Warm gold light from {LAMP} rims his edge in a fine gold seam; behind him the stone "
     f"wall recedes into painted night depth with {ROOFTOPS} beyond. {FIGURE_BASE}"),

    ("p2b_jesus_speaks", "page2", "9:16", [JESUS_REF], GLORY_STYLE, GLORY_CLOSING,
     "SCENE: Close-up of Jesus' face in three-quarter profile, mid-speech, calm and certain, warm "
     "light on his face against deep shadow. He matches the reference image exactly: long dark "
     "wavy hair, short dark beard, simple undyed homespun tunic with a woven cord sash."),

    ("p2c_the_record", "page2", "9:16", [SEEKER_REF], GLORY_STYLE, GLORY_CLOSING,
     "SCENE: Extreme close-up: a rolled parchment scroll held in weathered bare hands, worn edges, "
     "a faint wax seal. Warm light catching the parchment against cold shadow."),

    ("panel_b_door", "page3", "1:1", [], GLORY_STYLE, GLORY_CLOSING,
     f"SCENE: {DOOR_CLOSED[0].upper()}{DOOR_CLOSED[1:]} standing ajar, warm golden light spilling "
     f"through the gap onto worn stone flags, {LAMP} beside it in the archway. Ancient stone "
     f"archway. No people or figures anywhere in the frame."),

    ("panel_a_jesus", "page3", "1:1", [JESUS_REF], GLORY_STYLE, GLORY_CLOSING,
     "SCENE: Jesus standing just within the doorway, warm golden light surrounding him, his face "
     "open, dignified, welcoming, three-quarter view. He matches the reference image: long dark "
     "wavy hair, short dark beard, simple undyed homespun tunic with a woven cord sash."),

    ("panel_c_scroll", "page3", "1:1", [], GLORY_STYLE, GLORY_CLOSING,
     "SCENE: Close-up of a rolled parchment scroll resting in open bare hands, the wax seal "
     "catching warm light."),

    ("panel_d_threshold", "page3", "1:1", [SEEKER_REF], GLORY_STYLE, GLORY_CLOSING,
     f"SCENE: A weary grey-haired traveler, mid-stride as he steps through {DOOR_OPEN} great arched "
     f"doorway, seen from a low three-quarter angle just inside the arch, the stone lines of the "
     f"archway converging dramatically above him. Warm gold light floods past him from within, "
     f"casting his long shadow onto the worn flagstones; one bare hand braces the door's edge; the "
     f"night's blue-black darkness recedes behind him with {ROOFTOPS} far below the wall. Exactly "
     f"ONE person in this image -- no second figure, no one else in the doorway. {FIGURE_BASE}"),

    ("p4a_the_exception_fear", "page4", "9:16", [SEEKER_REF], PASSION_STYLE, PASSION_CLOSING,
     f"SCENE: The traveler standing alone, half turned away from {DOOR_CLOSED}, head bowed, face "
     f"falling into shadow, the scroll hanging heavy in one hand at his side. Cold shadow on him; "
     f"behind him the door's warm light-line still glows, low and patient. Seen level, at eye "
     f"height, a quiet mid-distance. {FIGURE_BASE}"),

    ("p4b_the_record_nailed", "page4", "9:16", [], PASSION_STYLE, PASSION_CLOSING,
     "SCENE: Close-up on the rough wooden upright of a bare cross, seen against a still darkening "
     "sky. A single rolled parchment scroll, worn and travel-marked, is fixed to the wood by a "
     "single iron nail driven through it, the parchment's edges curling. No figure is on the cross "
     "in this shot -- just the wood, the nailed scroll, and the sky beyond. Still and quiet, seen "
     "level, a quiet mid-distance."),

    ("p4c_empty_threshold", "page4", "9:16", [], PASSION_STYLE, PASSION_CLOSING,
     f"SCENE: {DOOR_OPEN[0].upper()}{DOOR_OPEN[1:]} great arch-topped door standing wide open with "
     f"no one in the doorway, warm golden light flooding out across empty worn stone flags. "
     f"Radiant warm light from the empty doorway into cold surroundings. Seen level, a quiet "
     f"mid-distance."),

    ("p5a_the_welcome", "page5", "1:1", [JESUS_REF, SEEKER_REF], GLORY_STYLE, GLORY_CLOSING,
     "SCENE: Wide warm shot at the open threshold: Jesus laying one hand on the traveler's "
     "shoulder, the traveler's head lifting, radiant doorway light surrounding them both. Jesus "
     "matches the reference image: long dark wavy hair, short dark beard, simple undyed homespun "
     "tunic with a woven cord sash, leather sandals. The traveler matches the reference image: "
     "short greying hair, lined face, a loose mantle draped over his head, leather thong sandals, "
     "the scroll now hanging loose at his side, released. Full warm radiance, shadows breaking "
     "apart."),

    ("p5b_record_left_behind", "page5", "3:4", [], GLORY_STYLE, GLORY_CLOSING,
     "SCENE: Close-up: a rolled parchment scroll lying released and open on the stone floor just "
     "inside the threshold, no longer held by anyone, warm light pooling over it. Soft-focus "
     "background warmth beyond."),

    ("p5c_jesus_face_open_door", "page5", "3:4", [JESUS_REF], GLORY_STYLE, GLORY_HERO_CLOSING,
     "SCENE: Jesus standing in the open doorway, seen from a low angle looking up at him, radiant "
     "morning-gold light filling the doorway and the sky beyond, his face calm, glad, triumphant. "
     "He matches the reference image: long dark wavy hair, short dark beard, simple undyed "
     "homespun tunic with a woven cord sash, leather sandals. The gold seam here is wide and "
     "radiant, fully earned."),
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
    assert JESUS_REF.exists(), f"missing {JESUS_REF}"
    assert SEEKER_REF.exists(), f"missing {SEEKER_REF}"
    spent = 0.0
    results = []
    for name, page, ar, refs, style, closing, scene in PANELS:
        out = OUT / f"{name}.png"
        prompt = style + "\n\n" + scene + "\n\n" + closing + "\n\n" + CONSTRAINT
        print(f"[img] {page}/{name} ...", flush=True)
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
                row = cost.record_hf(EPISODE, "short", "stills_v2_period", MODEL, note=f"[piece1-v2] {page}/{name}")
                spent += float(row.get("est_usd") or 0)
            except Exception as e:
                print(f"   (ledger record skipped: {e})")
            print(f"   ok  running spend ~${spent:.2f}")
            results.append((name, "clean"))
        else:
            print("   FAILED")
            results.append((name, "FAILED"))
    print(f"\n[out] {OUT}")
    print(f"[spend] ~${spent:.2f} of ${HARD_CAP_USD:.2f} cap")
    for name, status in results:
        print(f"  {name}: {status}")


if __name__ == "__main__":
    main()
