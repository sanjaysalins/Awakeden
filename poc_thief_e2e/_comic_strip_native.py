"""Native comic-strip POC (2026-07-24): instead of generating separate stills
and compositing panels ourselves (grid_choreography.py), ask nano_banana_pro
to draw a genuine multi-panel comic-strip PAGE in one image -- real ink panel
borders, real gutters, drawn by the model itself. Tests whether a single
generation holds character consistency across its own panels better than
separate independent calls do.

Strip 1 (no ref chained): does the model hold ONE thief face across 3 panels
  on its own, with no external anchor?
Strip 2 (christ_pc_ref chained): does chaining a reference help hold Christ
  across 3 panels the same way it holds him across separate stills?

  .venv\\Scripts\\python.exe poc_thief_e2e/_comic_strip_native.py
"""
import re, subprocess, sys, time
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
import config
from pipeline import cost
HF = str(config.HF_CLI_PATH)
MODEL = "nano_banana_pro"
HERE = Path(__file__).resolve().parent
OUT = HERE / "stills" / "_comic_strip_native"
OUT.mkdir(parents=True, exist_ok=True)
CHRIST_REF = ROOT / "longform" / "EW01_Two_Goats" / "v1" / "visual_16x9_inked" / "_painted_comic_test" / "christ_pc_ref.png"

STYLE = ("Bold inked biblical graphic-novel illustration: heavy confident black ink linework and "
         "dry-brush texture over rich painting, dramatic single strong key light with deep "
         "chiaroscuro shadow, a premium comic-cover finish. Non-photoreal, not smooth airbrushed, "
         "not a 3D render, no halftone dots, no vintage newsprint.")
AVOID = ("AVOID: no text, letters, numbers, digits, captions or lettering of any kind inside or "
         "outside the panels; no photoreal live-action; no smooth 3D render; no halftone dots; no "
         "modern machinery, clothing or tools; no gore. Render in full rich natural colour "
         "throughout, painterly and reverent, not flat or garish.")
MATCH = "Keep the SAME man in every panel he appears in, matching the reference image: same face, same hair, same build."

PANEL_LAYOUT = ("Compose this as a single COMPLETE comic-strip PAGE containing exactly THREE panels "
                 "stacked vertically from top to bottom, each panel a clean rectangular frame with a "
                 "bold black hand-inked border, separated by a narrow cream-paper gutter between each "
                 "panel -- this is a real comic-book page layout, not one single scene.")

STRIP1 = (
    f"{PANEL_LAYOUT} TOP PANEL: one of two crucified criminals, hanging nailed to his wooden cross, "
    "his face twisted in scorn, sneering off-frame toward Jesus. MIDDLE PANEL: the other crucified "
    "criminal, hanging on his own cross beside him, turning his head to rebuke him, his face grave "
    "and honest. BOTTOM PANEL: both criminals crucified side by side on their crosses, the centre "
    "cross with Jesus faintly visible in the hazy distance between them. The SAME two men appear "
    "consistently in every panel they are in -- same faces, same builds, throughout the whole page."
)

STRIP2 = (
    f"{PANEL_LAYOUT} TOP PANEL: a crucified thief straining toward Jesus, pleading, his bound hand "
    "lifted toward him. MIDDLE PANEL: Jesus on the cross turning his head gently toward the thief, "
    "his face full of compassion, wearing a simple pale robe fully covering his body, thin and "
    "gaunt, no heroic muscle. BOTTOM PANEL: close on Jesus's face, robed, gaunt and marred yet "
    "radiant with tenderness, speaking gently, a soft break of light in the storm clouds behind "
    "him. The SAME Jesus appears in every panel -- same face, same robe, throughout the whole page."
)

JOBS = [
    ("strip1_rebuke_noref", STRIP1, []),
    ("strip2_promise_ref", STRIP2, [CHRIST_REF]),
]


def run(prompt, out, refs):
    cmd = [HF, "generate", "create", MODEL, "--prompt", prompt, "--aspect_ratio", "9:16",
           "--resolution", "2k", "--wait"]
    for r in refs:
        cmd += ["--image", str(r)]
    p = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    blob = (p.stdout or "") + "\n" + (p.stderr or "")
    if re.search(r"nsfw", blob, re.IGNORECASE):
        print("   NSFW-REJECTED"); return False
    urls = re.findall(r'https?://\S+?\.(?:png|jpg|jpeg|webp)', blob) or re.findall(r'https?://\S+', blob)
    if not urls:
        print(f"   no url: {blob.strip()[-300:]}"); return False
    subprocess.run(["curl", "-s", "-L", urls[-1], "-o", str(out)], check=True)
    return out.exists() and out.stat().st_size > 1000


def main():
    for name, shot, refs in JOBS:
        out = OUT / f"{name}.png"
        prompt = f"{STYLE} {shot} {AVOID}"
        if refs:
            prompt += " " + MATCH
        print(f"[img ] {name} ({'ref' if refs else 'no ref'}) ...", flush=True)
        t = time.time()
        if run(prompt, out, refs):
            cost.record_hf("EW_Thief_POC", "short", "stills", MODEL, note=f"[comic-strip-native] {name}")
            print(f"   ok ({time.time()-t:.0f}s)")
        else:
            print("   FAILED")
    print(f"\n[out] {OUT}")


if __name__ == "__main__":
    main()
