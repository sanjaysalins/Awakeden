"""Render the 5 COMPLEMENTARY ('b') EW04 stills — a second framing/moment per new
beat (wide<->close pairs) so each 8-13s beat has 2x 5s clips and the cut stays punchy.
Inked style, anchored to ref_library cards. seedream_v4_5, 9:16. Idempotent, retry."""
import re, json, subprocess, urllib.request
from pathlib import Path

HF = str(Path.home() / "bin" / "hf.exe")
URL_RE = re.compile(r"https://\S+?\.(?:png|jpg|jpeg|webp)", re.IGNORECASE)
ROOT = Path(r"C:\Users\sanjay\PycharmProjects\JesusInTheBible")
LIB = ROOT / "ref_library"
OUT = Path(__file__).resolve().parent / "stills"
OUT.mkdir(parents=True, exist_ok=True)
C = LIB / "characters"; O = LIB / "objects"; P = LIB / "places"

STYLE = (" Drawn in INKED BIBLICAL GRAPHIC-NOVEL / cinematic manga ILLUSTRATION style: bold clean "
         "black ink linework and outlines, flat cel-shaded comic colour, hand-drawn 2D artwork, "
         "dramatic ink shadows. NOT a photograph, NOT photorealistic, NOT a glossy 3D render, NOT "
         "soft airbrushed anime — strong visible ink lines. Reverent and holy atmosphere, ancient "
         "Near-Eastern period-accurate, mature teen-and-up tone. No text, no lettering, no panels, "
         "no speech bubbles, no watermark, no signature.")
ONE = (" ONE single uninterrupted full-bleed cinematic illustration filling the entire frame — "
       "absolutely NO split screen, NO side panel, NO inset, NO grid, NO border or divider.")

SCENES = {
 # 1b — close on the witness (pairs with the wide hook)
 "01b_moses_close": ([C/"MOSES.png"],
   "A tight cinematic CLOSE-UP of the aged Hebrew prophet Moses' weathered face — deep-lined "
   "sun-darkened skin, long grey hair and full grey beard, weary knowing eyes fixed directly on the "
   "viewer as he begins to speak. Half-lit by warm low firelight against deep black shadow, intimate "
   "and reverent, vast dark negative space, one face filling the frame"),

 # 2b — the plague spreading across the camp (wide, pairs with the single fallen man)
 "02b_serpents_spread": ([P/"WILDERNESS_CAMP.png"],
   "An ancient Israelite wilderness camp at dusk overrun by judgment: several long bronze-and-amber "
   "LIVE desert serpents move and rear among the rough goat-hair tents, while shadowed Hebrew figures "
   "recoil and flee in dread, a few fallen on the sand. Low firelight, heavy darkness, the venom of "
   "judgment spreading across a rebellious camp, crowds in shadow with only a few lit faces"),

 # 3b — the lifted standard, low-angle hero close (the element of beat 3)
 "03b_serpent_atop_sky": ([O/"BRONZE_SERPENT_STANDARD.png"],
   "A dramatic low-angle hero close-up looking up at a single cast bronze serpent MOUNTED ON TOP of a "
   "tall bare wooden pole, its head raised high and silhouetted against a dim night sky, warm "
   "firelight glinting on the solid bronze. The long lower shaft is plain bare wood — the serpent does "
   "NOT coil down the pole. A serpent set upon a pole and lifted up, NOT a snake-wrapped staff, NOT a "
   "caduceus, awe and reverence, deep negative space of sky around it"),

 # 4b — the payoff: a dying face turning to life (extreme close, pairs with the wide look-and-live)
 "04b_face_to_life": ([P/"WILDERNESS_CAMP.png"],
   "An extreme cinematic CLOSE-UP of a bitten Hebrew man's face and one reaching open hand: his grey "
   "ashen pallor warms back to living colour, his eyes lift UPWARD toward an unseen warm gleam above, "
   "hope and life returning, a single shaft of warm light falling across his face. Deep shadow "
   "around, one face and hand filling the frame, intimate and tender"),

 # 5b — the line lands on Jesus (close, pairs with the two-shot)
 "05b_jesus_speaks": ([C/"JESUS.png", P/"JERUSALEM_NIGHT_INTERIOR.png"],
   "A warm cinematic CLOSE-UP of Jesus — a calm luminous young man of about thirty, long dark-brown "
   "hair parted in the middle, full dark beard, warm olive skin — lit gently by a low clay oil lamp "
   "as he speaks earnestly in the night, his gaze steady and grave. In the soft dark foreground, the "
   "shadowed shoulder and back of the older seeker Nicodemus listening. Only lamplight on Jesus' face, "
   "the stone room falling away into deep night, intimate and holy"),
}


def render(refs, prompt, dest):
    if dest.exists() and dest.stat().st_size > 0:
        print(f"[skip] {dest.name}", flush=True); return "skip"
    args = [HF, "generate", "create", "seedream_v4_5", "--prompt", prompt, "--aspect_ratio", "9:16", "--wait"]
    for r in refs:
        args += ["--image", str(r)]
    for attempt in (1, 2, 3):
        proc = subprocess.run(args, capture_output=True, text=True, encoding="utf-8",
                              errors="replace", timeout=900)
        blob = (proc.stdout or "") + (proc.stderr or "")
        m = URL_RE.search(blob)
        if m:
            req = urllib.request.Request(m.group(0), headers={"User-Agent": "poc/1.0"})
            with urllib.request.urlopen(req, timeout=180) as resp:
                dest.write_bytes(resp.read())
            print(f"[ok  ] {dest.name}", flush=True); return "ok"
        low = blob.lower()
        transient = ("concurrent_jobs_limit" in low or "rate_limit" in low or "timeout" in low)
        tag = "retry" if (attempt < 3 and transient) else "FAIL"
        print(f"[{tag}] {dest.name} (rc={proc.returncode})\n    {blob[-300:].strip()}", flush=True)
        if not transient:
            return "fail"
    return "fail"


if __name__ == "__main__":
    results = {}
    for slug, (refs, desc) in SCENES.items():
        results[slug] = render(refs, desc + "." + ONE + STYLE, OUT / f"{slug}.png")
    print(f"\nDONE — alt stills in {OUT}\n{json.dumps(results, indent=2)}", flush=True)
