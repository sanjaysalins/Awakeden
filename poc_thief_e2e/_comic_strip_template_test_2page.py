"""2-page chained generalization test (2026-07-24): David and Goliath (1 Samuel
17), fresh beats from the earlier single-page template test. Page 1 is the
reference-establishing page (no chain); Page 2 is generated chained to Page 1
as a --image reference, mirroring the proven Thief image_6 -> page1
consistency mechanism. Every caption is a real contiguous KJV excerpt.

  .venv\\Scripts\\python.exe poc_thief_e2e/_comic_strip_template_test_2page.py
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

AESTHETIC = (
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
    "- Primary Figure: David, a young Israelite shepherd, small and slight build, dark curly "
    "hair, no armor, wearing a simple brown shepherd's tunic, a leather sling and a shepherd's "
    "bag, a staff.\n"
    "- Secondary Figure: Goliath, a towering Philistine champion, heavily muscled, bronze scale "
    "armor and a crested bronze helmet, a long dark beard, a massive bronze spear.\n"
    "- Environmental Setting: The valley of Elah, dry rocky terrain with a shallow brook cutting "
    "through it, two armies on opposing ridges, an overcast, tense sky.\n\n"
)
STYLE_TAIL = (
    "\n\nEXPLICIT STYLE CONSTRAINTS: Vintage comic book art, heavy black ink hatching, muted "
    "earth tones, yellow caption boxes only, no speech bubbles, sharp black panel borders, dark "
    "gutters, high structural consistency."
)

PAGE1 = AESTHETIC + (
    "PANEL BREAKDOWN & SPATIAL COMPOSITION:\n\n"
    "PANEL 1 (Top Section - Full Width, Landscape Aspect):\n"
    "- Scene Type: Wide establishing shot.\n"
    "- Composition: Wide view of the valley of Elah. Goliath strides out alone into the gap "
    "between the two armies on the ridges, spear in hand, calling out his daily challenge.\n"
    "- Lighting: Atmospheric, overcast, high contrast.\n"
    "- Text Element: A sharp, yellow rectangular caption box in the top-left corner reads: "
    "'CHOOSE YOU A MAN...LET HIM COME DOWN TO ME.'\n\n"
    "PANEL 2 (Middle Left - Vertical Portrait Box):\n"
    "- Scene Type: Intense close-up shot.\n"
    "- Composition: Extreme close-up on Goliath's sneering face, bronze helmet, spear point "
    "visible at the frame's edge, shouting toward the Israelite ridge.\n"
    "- Lighting: Deep side-shadows (chiaroscuro).\n"
    "- Text Element: A sharp, yellow rectangular caption box at the bottom reads: 'I DEFY THE "
    "ARMIES OF ISRAEL THIS DAY.'\n\n"
    "PANEL 3 (Middle Right - Vertical Portrait Box):\n"
    "- Scene Type: Medium shot.\n"
    "- Composition: David, freshly arrived among the fearful Israelite soldiers, provisions bag "
    "still on his shoulder, looking toward Goliath with a resolute, indignant expression while "
    "the soldiers around him look afraid.\n"
    "- Lighting: Soft directional light on David against a duller crowd behind him.\n"
    "- Text Element: A sharp, yellow rectangular caption box at the bottom reads: 'WHO IS THIS "
    "UNCIRCUMCISED PHILISTINE, THAT HE SHOULD DEFY THE ARMIES OF THE LIVING GOD?'\n\n"
    "PANEL 4 (Bottom Section - Full Width, Panoramic Aspect):\n"
    "- Scene Type: Medium two-shot.\n"
    "- Composition: David standing before King Saul inside a tent, declining Saul's offered "
    "armor and sword, holding only his staff and sling.\n"
    "- Lighting: Warm torchlight inside the tent against the cold light outside.\n"
    "- Text Element: A sharp, yellow rectangular caption box centered at the bottom reads: 'THE "
    "LORD THAT DELIVERED ME OUT OF THE PAW OF THE LION...HE WILL DELIVER ME OUT OF THE HAND OF "
    "THIS PHILISTINE.'"
) + STYLE_TAIL

PAGE2 = AESTHETIC + (
    "This page continues directly from the reference page: same David, same Goliath, same "
    "world.\n\n"
    "PANEL BREAKDOWN & SPATIAL COMPOSITION:\n\n"
    "PANEL 1 (Top Section - Full Width, Landscape Aspect):\n"
    "- Scene Type: Wide establishing shot.\n"
    "- Composition: David kneeling at the shallow brook in the valley floor, choosing smooth "
    "stones from the water and placing them in his shepherd's bag, Goliath a distant silhouette "
    "behind him.\n"
    "- Lighting: Atmospheric, overcast, high contrast with light catching the water.\n"
    "- Text Element: A sharp, yellow rectangular caption box in the top-left corner reads: 'AND "
    "HE CHOSE HIM FIVE SMOOTH STONES OUT OF THE BROOK.'\n\n"
    "PANEL 2 (Middle Left - Vertical Portrait Box):\n"
    "- Scene Type: Intense close-up shot.\n"
    "- Composition: Extreme close-up on Goliath's face, now seeing David approach up close, "
    "disdainful and insulted.\n"
    "- Lighting: Deep side-shadows (chiaroscuro).\n"
    "- Text Element: A sharp, yellow rectangular caption box at the bottom reads: 'AM I A DOG, "
    "THAT THOU COMEST TO ME WITH STAVES?'\n\n"
    "PANEL 3 (Middle Right - Vertical Portrait Box):\n"
    "- Scene Type: Medium close-up reaction shot.\n"
    "- Composition: David mid-swing, sling whirling overhead, expression calm and focused, not "
    "afraid.\n"
    "- Lighting: Soft, single directional highlight on his face against a dark background.\n"
    "- Text Element: A sharp, yellow rectangular caption box at the bottom reads: 'THE LORD "
    "SAVETH NOT WITH SWORD AND SPEAR...FOR THE BATTLE IS THE LORD'S.'\n\n"
    "PANEL 4 (Bottom Section - Full Width, Panoramic Aspect):\n"
    "- Scene Type: Climactic wide/medium shot.\n"
    "- Composition: The instant the stone strikes Goliath's forehead: he staggers, shield arm "
    "dropping, beginning to fall backward, dust rising. No blood or graphic wound visible. David "
    "in the foreground, still in his follow-through stance.\n"
    "- Lighting: Dramatic light shift, a shaft of light breaking through the clouds.\n"
    "- Text Element: A sharp, yellow rectangular caption box centered at the bottom reads: 'THE "
    "STONE SUNK INTO HIS FOREHEAD...AND HE FELL UPON HIS FACE TO THE EARTH.'"
) + STYLE_TAIL


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
    p1 = OUT / "david_goliath_p1.png"
    print("[img ] david_goliath_p1 (reference, no chain) ...", flush=True)
    t = time.time()
    if run(PAGE1, p1, []):
        cost.record_hf("EW_Thief_POC", "short", "stills", MODEL, note="[template-test-2page] p1")
        print(f"   ok ({time.time()-t:.0f}s)")
    else:
        print("   FAILED"); return

    p2 = OUT / "david_goliath_p2.png"
    print("[img ] david_goliath_p2 (chained to p1) ...", flush=True)
    t = time.time()
    if run(PAGE2, p2, [p1]):
        cost.record_hf("EW_Thief_POC", "short", "stills", MODEL, note="[template-test-2page] p2")
        print(f"   ok ({time.time()-t:.0f}s)")
    else:
        print("   FAILED")
    print(f"\n[out] {OUT}")


if __name__ == "__main__":
    main()
