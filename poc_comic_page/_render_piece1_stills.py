"""Piece 1 production (v2/PRODUCTION_PLAN_400CR.md): the 15 stills for "In No Wise
Cast Out," rebuilt in the Action Painterly / Gold Seam grammar, chained to the NEW
charsheets in poc_comic_page/_piece1/charsheets/. Bowed Camera register set per beat
(ordinary/pivot/passion/glory) per the plan's panel map. Includes the new p4b Col 2:14
"the record nailed" panel. NBP nano_banana_pro, 2cr/still, 30cr for 15 -- Gate 2 stops
here for user review before any animation credit moves.

  .venv\\Scripts\\python.exe poc_comic_page/_render_piece1_stills.py
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
OUT = HERE / "_piece1" / "stills"
OUT.mkdir(parents=True, exist_ok=True)
CS = HERE / "_piece1" / "charsheets"
JESUS_REF = CS / "jesus.png"
SEEKER_REF = CS / "seeker.png"

HARD_CAP_USD = 6.00  # 30cr headroom incl. small buffer

CONSTRAINT = (
    "GLOBAL TEXTUAL CONSTRAINT: NO text of any kind anywhere -- no speech "
    "bubbles, no caption boxes, no lettering. Pure artwork only."
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

# (name, page, aspect_ratio, refs, style, closing, scene_text)
PANELS = [
    ("p1a_night_door", "page1", "1:1", [SEEKER_REF], GLORY_STYLE, GLORY_CLOSING,
     "SCENE: Wide establishing view at night: a weary grey-haired traveler stands "
     "alone and small before a great arch-topped iron-banded wooden door, shut, "
     "set in a rough stone wall. Cold darkness everywhere; one thin line of warm "
     "light escapes beneath the door. He stands a few paces back, a rolled "
     "parchment scroll clutched to his chest. He matches the reference image: "
     "short greying hair, lined face, ragged hooded cloak."),

    ("p1b_hesitant_hand", "page1", "1:1", [SEEKER_REF], GLORY_STYLE, GLORY_CLOSING,
     "SCENE: Close-up from behind and beside the traveler: his weathered hand "
     "half-raised toward the closed door's dark wood, hesitating, not touching "
     "it; his other arm presses a rolled parchment scroll to his chest. Cold dim "
     "light, a faint warm glow from the gap beneath the door."),

    ("p2a_rehearsing", "page2", "9:16", [SEEKER_REF], GLORY_STYLE, GLORY_CLOSING,
     "SCENE: Tall view: the traveler leaning his forehead against the closed "
     "door's frame, eyes shut, lips parted mid-whisper, rehearsing his plea. The "
     "scroll pressed between his chest and the door frame. Cold surroundings, "
     "warm light touching his sandals from beneath the door."),

    ("p2b_jesus_speaks", "page2", "9:16", [JESUS_REF], GLORY_STYLE, GLORY_CLOSING,
     "SCENE: Close-up of Jesus' face in three-quarter profile, mid-speech, calm "
     "and certain, warm light on his face against deep shadow. He matches the "
     "reference image exactly: long dark wavy hair, short dark beard, simple "
     "cream robe with a cloth sash."),

    ("p2c_the_record", "page2", "9:16", [SEEKER_REF], GLORY_STYLE, GLORY_CLOSING,
     "SCENE: Extreme close-up: a rolled parchment scroll held in weathered "
     "hands, worn edges, a faint wax seal. Warm light catching the parchment "
     "against cold shadow."),

    ("panel_b_door", "page3", "1:1", [], GLORY_STYLE, GLORY_CLOSING,
     "SCENE: The great arch-topped iron-banded door standing ajar, warm golden "
     "light spilling through the gap onto worn stone flags. Ancient stone "
     "archway."),

    ("panel_a_jesus", "page3", "1:1", [JESUS_REF], GLORY_STYLE, GLORY_CLOSING,
     "SCENE: Jesus standing just within the doorway, warm golden light "
     "surrounding him, his face open, dignified, welcoming, three-quarter view. "
     "He matches the reference image: long dark wavy hair, short dark beard, "
     "cream robe."),

    ("panel_c_scroll", "page3", "1:1", [], GLORY_STYLE, GLORY_CLOSING,
     "SCENE: Close-up of a rolled parchment scroll resting in open hands, the "
     "wax seal catching warm light."),

    ("panel_d_threshold", "page3", "1:1", [], GLORY_STYLE, GLORY_CLOSING,
     "SCENE: The stone threshold of the great door, worn flagstones, warm light "
     "pooling at the doorway's edge, cold shadow beyond."),

    ("p4a_the_exception_fear", "page4", "9:16", [SEEKER_REF], PASSION_STYLE, PASSION_CLOSING,
     "SCENE: The traveler standing alone, half turned away from the door, head "
     "bowed, face falling into shadow, the scroll hanging heavy in one hand at "
     "his side. Cold shadow on him; behind him the door's warm light-line still "
     "glows, low and patient. Seen level, at eye height, a quiet mid-distance."),

    ("p4b_the_record_nailed", "page4", "9:16", [], PASSION_STYLE, PASSION_CLOSING,
     "SCENE: Close-up on the rough wooden upright of a bare cross, seen against "
     "a still darkening sky. A single rolled parchment scroll, worn and "
     "travel-marked, is fixed to the wood by a single iron nail driven through "
     "it, the parchment's edges curling. No figure is on the cross in this shot "
     "-- just the wood, the nailed scroll, and the sky beyond. Still and quiet, "
     "seen level, a quiet mid-distance."),

    ("p4c_empty_threshold", "page4", "9:16", [], PASSION_STYLE, PASSION_CLOSING,
     "SCENE: The great arch-topped door standing wide open with no one in the "
     "doorway, warm golden light flooding out across empty worn stone flags. "
     "Radiant warm light from the empty doorway into cold surroundings. Seen "
     "level, a quiet mid-distance."),

    ("p5a_the_welcome", "page5", "1:1", [JESUS_REF, SEEKER_REF], GLORY_STYLE, GLORY_CLOSING,
     "SCENE: Wide warm shot at the open threshold: Jesus laying one hand on the "
     "traveler's shoulder, the traveler's head lifting, radiant doorway light "
     "surrounding them both. Jesus matches the reference image: long dark wavy "
     "hair, short dark beard, cream robe. The traveler matches the reference "
     "image: short greying hair, lined face, earth-tone cloak, the scroll now "
     "hanging loose at his side, released. Full warm radiance, shadows breaking "
     "apart."),

    ("p5b_record_left_behind", "page5", "3:4", [], GLORY_STYLE, GLORY_CLOSING,
     "SCENE: Close-up: a rolled parchment scroll lying released and open on the "
     "stone floor just inside the threshold, no longer held by anyone, warm "
     "light pooling over it. Soft-focus background warmth beyond."),

    ("p5c_jesus_face_open_door", "page5", "3:4", [JESUS_REF], GLORY_STYLE, GLORY_HERO_CLOSING,
     "SCENE: Jesus standing in the open doorway, seen from a low angle looking "
     "up at him, radiant morning-gold light filling the doorway and the sky "
     "beyond, his face calm, glad, triumphant. He matches the reference image: "
     "long dark wavy hair, short dark beard, cream robe. The gold seam here is "
     "wide and radiant, fully earned."),
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
                row = cost.record_hf(EPISODE, "short", "stills", MODEL, note=f"[piece1] {page}/{name}")
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
