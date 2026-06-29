"""Render the 3 NEW gospel-LANDING stills for EW04 (beats 8-10) in the locked
INKED graphic-novel style, anchored to ref_library so the Jesus face / world match.
  06_cross_lifted    — Christ lifted on the Roman cross (antitype of the serpent-pole)
  07_risen_christ    — the risen, living, luminous Christ (the final landing hero)
  08_bitten_multitude— the bitten people lifting their eyes ("every one of us")
seedream_v4_5, 9:16. Idempotent, rate-limit-aware, 3-attempt retry. POC/scratchpad."""
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
 # 06 — the cross: deliberate visual rhyme with 03b (serpent lifted on a pole)
 "06_cross_lifted": ([C/"JESUS.png"],
   "A dramatic low-angle HERO view looking UP at Jesus Christ lifted high on a tall rough-hewn Roman "
   "wooden cross planted against a vast darkening sky — the same calm young man of about thirty, long "
   "dark-brown hair, full dark beard, warm olive skin, a plain cloth at his waist, head gently bowed, "
   "arms outstretched along the crossbeam. Solemn and REVERENT, NOT gory, no blood, no emphasised "
   "wounds, no written sign on the cross. Warm low light breaks behind the cross against deep shadow, "
   "vast negative space of sky, one dominant hero figure, holy sorrow — deliberately echoing a serpent "
   "lifted on a pole, the antitype of the bronze standard"),

 # 07 — the risen living Christ (the final landing hero) — own-world living Christ
 "07_risen_christ": ([C/"JESUS.png"],
   "A radiant cinematic view of the RISEN, living Jesus Christ standing and lifted up in warm glory — "
   "the same young man of about thirty, long dark-brown hair parted in the middle, full dark beard, "
   "warm olive skin, clothed in clean flowing linen, his face serene and fully ALIVE, eyes lifted, one "
   "open hand reaching toward the viewer in gentle invitation. Warm holy light blooms around him from "
   "above against deep shadow — NOT crucified, NOT wounded, victorious and luminous, one dominant hero "
   "figure, vast soft negative space of light, awe and hope"),

 # 08 — the bitten multitude lifting their eyes ("every one of us")
 "08_bitten_multitude": ([P/"WILDERNESS_CAMP.png"],
   "In the ancient wilderness camp at dusk, a scattered crowd of bitten, stricken Hebrew people — men, "
   "women and the old — sink weak and pale on the bare rocky sand among rough goat-hair tents, yet "
   "every one of them turns and lifts their eyes and hands UPWARD toward an unseen warm gleam of light "
   "above. Faces of dread turning to fragile hope. Low firelight and deep shadow, period-accurate rough "
   "desert garments, a few lit faces among many in shadow, the whole bitten people looking up to live"),
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
    print(f"\nDONE — landing stills in {OUT}\n{json.dumps(results, indent=2)}", flush=True)
