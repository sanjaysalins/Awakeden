"""Generalization test (2026-07-24): take the user's own Master Comic Blueprint
template verbatim in structure, fill it in cold for a BRAND NEW story (David
and Goliath, 1 Samuel 17 -- never touched this session), using real KJV
verbatim excerpts in every caption box instead of paraphrase. Tests whether
the template generalizes beyond the Thief story it was written against.

  .venv\\Scripts\\python.exe poc_thief_e2e/_comic_strip_template_test.py
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
OUT = HERE / "stills" / "_comic_strip_template_test"
OUT.mkdir(parents=True, exist_ok=True)

PROMPT = (
    "A 9:16 vertical comic book page containing a structured 4-panel grid layout. The overall "
    "piece is rendered in a vintage graphic novel illustration style characterized by heavy "
    "black ink linework, high-contrast chiaroscuro shadows, cross-hatching, and a desaturated, "
    "muted earth-tone color palette (dominant slate grays, deep ochre, raw umber, and muted "
    "blues). The paper has a subtle aged, textured vintage comic print finish with crisp panel "
    "borders and dark gutters separating each section.\n\n"
    "GLOBAL TEXTUAL CONSTRAINT: No speech bubbles or voice bubbles of any kind are permitted. "
    "All dialogue, narrative context, and spoken statements must strictly appear inside solid, "
    "bright yellow rectangular caption boxes located in designated corners of the panels with "
    "crisp, bold, hand-lettered comic book typography.\n\n"
    "CORE CHARACTER DESIGN ANCHORS (To maintain visual continuity):\n"
    "- Primary Figure: David, a young Israelite shepherd, small and slight build next to his "
    "opponent, dark curly hair, no armor, wearing a simple brown shepherd's tunic, a leather "
    "sling coiled in one hand, a shepherd's staff on his back.\n"
    "- Secondary Figure: Goliath, a towering Philistine champion, heavily muscled, bronze scale "
    "armor and a bronze helmet, a long dark beard, a massive bronze spear.\n"
    "- Environmental Setting: The valley of Elah, dry rocky terrain with a shallow brook cutting "
    "through it, two armies on opposing ridges, an overcast, tense sky.\n\n"
    "PANEL BREAKDOWN & SPATIAL COMPOSITION:\n\n"
    "PANEL 1 (Top Section - Full Width, Landscape Aspect):\n"
    "- Scene Type: Wide establishing shot.\n"
    "- Composition: Wide view of the valley of Elah from above. The Israelite army lines one "
    "ridge, the Philistine army the other. Goliath stands alone in the gap between them, spear "
    "raised, dwarfing the soldiers around him. David is a small figure just descending the "
    "Israelite side, sling in hand.\n"
    "- Lighting: Atmospheric, overcast, high contrast with a single shaft of light on the valley "
    "floor.\n"
    "- Text Element: A sharp, yellow rectangular caption box in the top-left corner reads: 'AND "
    "THEY PITCHED BY THE VALLEY OF ELAH.'\n\n"
    "PANEL 2 (Middle Left - Vertical Portrait Box):\n"
    "- Scene Type: Intense close-up shot.\n"
    "- Composition: Extreme close-up on Goliath's face, sneering down at the camera, bronze "
    "helmet framing a scarred, contemptuous expression, spear point visible at the frame's "
    "edge.\n"
    "- Lighting: Deep side-shadows (chiaroscuro) emphasizing his scale and menace.\n"
    "- Text Element: A sharp, yellow rectangular caption box at the bottom reads: 'COME TO ME, "
    "AND I WILL GIVE THY FLESH UNTO THE FOWLS OF THE AIR.'\n\n"
    "PANEL 3 (Middle Right - Vertical Portrait Box):\n"
    "- Scene Type: Medium close-up reaction shot.\n"
    "- Composition: Medium close-up on David's face, looking up and across toward Goliath, "
    "expression calm and resolute, not afraid, a stone already set in his lowered sling.\n"
    "- Lighting: Soft, single directional highlight on his face against a dark background.\n"
    "- Text Element: A sharp, yellow rectangular caption box at the bottom reads: 'I COME TO "
    "THEE IN THE NAME OF THE LORD OF HOSTS...WHOM THOU HAST DEFIED.'\n\n"
    "PANEL 4 (Bottom Section - Full Width, Panoramic Aspect):\n"
    "- Scene Type: Climactic wide/medium shot.\n"
    "- Composition: Wide shot of the valley floor the instant after the sling's release: Goliath "
    "staggering backward off-balance, his shield arm dropping, dust kicked up around his feet, "
    "David in the foreground still in his follow-through stance. No blood or graphic wound "
    "visible.\n"
    "- Lighting: Dramatic light shift, a shaft of light breaking through the clouds onto David.\n"
    "- Text Element: A sharp, yellow rectangular caption box centered at the bottom reads: "
    "'DAVID PREVAILED...WITH A SLING AND A STONE...BUT THERE WAS NO SWORD IN THE HAND OF "
    "DAVID.'\n\n"
    "EXPLICIT STYLE CONSTRAINTS: Vintage comic book art, heavy black ink hatching, muted earth "
    "tones, yellow caption boxes only, no speech bubbles, sharp black panel borders, dark "
    "gutters, high structural consistency."
)


def main():
    out = OUT / "david_goliath.png"
    cmd = [HF, "generate", "create", MODEL, "--prompt", PROMPT, "--aspect_ratio", "9:16",
           "--resolution", "2k", "--wait"]
    print("[img ] david_goliath (template test, no reference) ...", flush=True)
    t = time.time()
    p = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    blob = (p.stdout or "") + "\n" + (p.stderr or "")
    if re.search(r"nsfw", blob, re.IGNORECASE):
        print("   NSFW-REJECTED"); return
    urls = re.findall(r'https?://\S+?\.(?:png|jpg|jpeg|webp)', blob) or re.findall(r'https?://\S+', blob)
    if not urls:
        print(f"   no url: {blob.strip()[-300:]}"); return
    subprocess.run(["curl", "-s", "-L", urls[-1], "-o", str(out)], check=True)
    if out.exists() and out.stat().st_size > 1000:
        cost.record_hf("EW_Thief_POC", "short", "stills", MODEL, note="[template-test] david_goliath")
        print(f"   ok ({time.time()-t:.0f}s)")
    else:
        print("   FAILED")
    print(f"\n[out] {OUT}")


if __name__ == "__main__":
    main()
