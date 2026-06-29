"""Render the 5 NEW EW04 (Bronze Serpent) scene stills in the locked INKED style,
each anchored to its ref_library card(s) via --image so faces / objects / world are
inherited, not re-invented. Scenes 6-7 (cross + risen) reuse the inked Jesus clips.

seedream_v4_5, 9:16. Idempotent, rate-limit-aware, 3-attempt retry. POC/scratchpad."""
import re, json, subprocess, urllib.request
from pathlib import Path

HF = str(Path.home() / "bin" / "hf.exe")
URL_RE = re.compile(r"https://\S+?\.(?:png|jpg|jpeg|webp)", re.IGNORECASE)
ROOT = Path(r"C:\Users\sanjay\PycharmProjects\JesusInTheBible")
LIB = ROOT / "ref_library"
OUT = Path(__file__).resolve().parent / "stills"
OUT.mkdir(parents=True, exist_ok=True)
ASPECT = "9:16"

C = LIB / "characters"; O = LIB / "objects"; P = LIB / "places"

STYLE = (" Drawn in INKED BIBLICAL GRAPHIC-NOVEL / cinematic manga ILLUSTRATION style: bold clean "
         "black ink linework and outlines, flat cel-shaded comic colour, hand-drawn 2D artwork, "
         "dramatic ink shadows. NOT a photograph, NOT photorealistic, NOT a glossy 3D render, NOT "
         "soft airbrushed anime — strong visible ink lines. Reverent and holy atmosphere, ancient "
         "Near-Eastern period-accurate, mature teen-and-up tone. No text, no lettering, no panels, "
         "no speech bubbles, no watermark, no signature.")
ONE = (" ONE single uninterrupted full-bleed cinematic illustration filling the entire frame — "
       "absolutely NO split screen, NO side panel, NO inset, NO grid, NO border or divider.")

# slug -> (refs[], scene description)
SCENES = {
 "01_hook_moses": ([C/"MOSES.png"],
   "The aged Hebrew prophet Moses, an old weathered shepherd-leader with a deep-lined sun-darkened "
   "face, long grey hair and a full grey beard, wrapped in a rough desert mantle, half-lit by a low "
   "amber firelight against deep shadow. He faces the viewer with weary, knowing eyes; one open hand "
   "is half-raised as if beginning to speak. Vast dark negative space around him, one dominant hero "
   "figure, no crowd, intimate and reverent, dramatic low key lighting"),

 "02_judgment_plague": ([P/"WILDERNESS_CAMP.png"],
   "An ancient Israelite wilderness camp at dusk, a scene of plague and dread: one fallen Hebrew man "
   "collapsed on the bare rocky sand in the foreground, his face twisted in pain, while a coiling "
   "bronze-and-amber live desert serpent strikes near his bare arm. Behind, the wider camp of rough "
   "goat-hair tents and a shadowed crowd dissolve into deep darkness lit only by low fires. The venom "
   "of judgment fallen on a rebellious people, heavy dread, few lit faces"),

 "03_bronze_lifted": ([C/"MOSES.png", O/"BRONZE_SERPENT_STANDARD.png", P/"WILDERNESS_CAMP.png"],
   "In the wilderness camp at night, Moses, lit from below by firelight, lifts high with both hands a "
   "tall rough wooden pole planted in the sand; bound at its top is a single sculpted serpent of solid "
   "matte bronze glinting warm in the light, raised high above the camp — unmistakably one cast bronze "
   "serpent figure on a plain bare wooden pole, a desert standard, NOT an occult charm, NOT a medical "
   "caduceus. The camp dissolves into shadow below, a vast dim sky and negative space above, Moses' "
   "upturned face caught in the firelight"),

 "04_look_and_live": ([P/"WILDERNESS_CAMP.png", O/"BRONZE_SERPENT_STANDARD.png"],
   "In the wilderness desert, a bitten Hebrew man has fallen on the sand in the foreground, weak and "
   "pale, but he turns his face and lifts his eyes UPWARD toward a distant warm gleam of a single "
   "bronze serpent on a tall wooden pole — and life returns to his face. A single shaft of warm light "
   "falls on him from above; his hand reaches up. The bronze standard is small and bright in the upper "
   "distance, the rest of the camp in shadow, one dominant figure"),

 "05_night_teacher": ([C/"JESUS.png", C/"NICODEMUS.png", P/"JERUSALEM_NIGHT_INTERIOR.png"],
   "Inside an ancient Jerusalem stone house at night, two robed men face each other across a low clay "
   "oil lamp resting on a stone ledge. On the RIGHT sits Jesus — a calm luminous young man of about "
   "thirty, long dark-brown hair parted in the middle, a full dark beard, warm olive skin, lit gently "
   "by the lamp. On the LEFT, the older Pharisee Nicodemus, greying dark beard, fine rabbi's robes and "
   "prayer-shawl, leans in from the shadow, listening intently. Only the lamp lights their two faces; "
   "the room falls away into deep night, intimate hush"),
}


def render(refs, prompt, dest):
    if dest.exists() and dest.stat().st_size > 0:
        print(f"[skip] {dest.name}", flush=True); return "skip"
    args = [HF, "generate", "create", "seedream_v4_5", "--prompt", prompt,
            "--aspect_ratio", ASPECT, "--wait"]
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
        prompt = desc + "." + ONE + STYLE
        results[slug] = render(refs, prompt, OUT / f"{slug}.png")
    print(f"\nDONE — stills in {OUT}\n{json.dumps(results, indent=2)}", flush=True)
