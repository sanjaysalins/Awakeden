"""Reproducibility test (2026-07-25): re-run the Thief POC recipe from a cold
start, using the TIGHTENED Christ-gate wording (proven via the page1 reroll)
consistently across all 3 pages from the beginning, instead of discovering
the issue after the fact. nano_banana_pro has no seed control, so this also
tests whether the documented recipe is reliably good or whether the first
run's clean pages 2-3 were partly luck.

  .venv\\Scripts\\python.exe poc_thief_e2e/_thief_poc_pages_v2.py
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
OUT = HERE / "stills" / "_thief_poc_v2"
OUT.mkdir(parents=True, exist_ok=True)

AESTHETIC = (
    "A 9:16 vertical comic book page containing a structured 4-panel grid layout. The overall "
    "piece is rendered in a vintage graphic novel illustration style characterized by heavy "
    "black ink linework, high-contrast chiaroscuro shadows, cross-hatching, and a desaturated, "
    "muted earth-tone color palette (dominant slate grays, deep ochre, raw umber, muted blues). "
    "The paper has a subtle aged, textured vintage comic print finish with crisp panel borders "
    "and dark gutters separating each section.\n\n"
    "GLOBAL TEXTUAL CONSTRAINT: NO text of any kind anywhere on the page -- no speech bubbles, "
    "no caption boxes, no lettering, no words. The page is pure artwork only.\n\n"
    "CORE CHARACTER DESIGN ANCHORS (must exactly match across every panel and every page):\n"
    "- Jesus Christ: on the center cross, a lean, gaunt, sorrowful figure -- servant register, "
    "NOT heroic or muscular, ribs visible, no defined abdominal muscles. A crown of thorns. "
    "Skin unmarked and clean except faint matted blood at the brow only -- absolutely NO blood, "
    "no red marks, no wounds visible anywhere on the hands, wrists, feet, or torso. A simple "
    "loincloth per period convention. Marred, weary, dignified expression, not theatrical "
    "suffering.\n"
    "- The Penitent Criminal: an older, weathered condemned man with graying, thinning hair and "
    "a deeply lined face, on the cross to Jesus' one side. A simple ragged loincloth. His face "
    "shows dawning humility and conviction.\n"
    "- The Mocking Criminal: another ordinary condemned man on the cross to Jesus' other side, "
    "gaunt and weathered, dark hair, his face contorted in bitterness and scorn.\n"
    "- Environmental Setting: Golgotha, a barren rocky hill outside Jerusalem's walls, an "
    "oppressive dark midday sky (the sun darkened), a distant crowd and Roman soldiers at the "
    "foot of the crosses.\n\n"
)
STYLE_TAIL = (
    "\n\nEXPLICIT STYLE CONSTRAINTS: Vintage comic book art, heavy black ink hatching, muted "
    "earth tones, sharp black panel borders, dark gutters, high structural consistency, "
    "reverent and dignified treatment throughout, absolutely no text or lettering anywhere, "
    "absolutely no visible blood anywhere on Jesus except a faint trace at the brow."
)

PAGE1 = AESTHETIC + (
    "PANEL BREAKDOWN & SPATIAL COMPOSITION:\n\n"
    "PANEL 1 (Top Section - Full Width, Landscape Aspect):\n"
    "- Scene Type: Wide establishing shot.\n"
    "- Composition: Golgotha from a distance. Three crosses stand against the dark, oppressive "
    "sky. Jesus hangs on the center cross, the two criminals on crosses to either side. A "
    "distant crowd and Roman soldiers stand at the foot of the hill.\n"
    "- Lighting: Dark, stormy, the sun darkened, oppressive atmosphere.\n\n"
    "PANEL 2 (Middle Left - Vertical Portrait Box):\n"
    "- Scene Type: Intense close-up.\n"
    "- Composition: Close-up on the Mocking Criminal's face, jeering and bitter, shouting "
    "toward Jesus.\n"
    "- Lighting: Deep chiaroscuro shadows.\n\n"
    "PANEL 3 (Middle Right - Vertical Portrait Box):\n"
    "- Scene Type: Close-up reaction shot.\n"
    "- Composition: Close-up on the Penitent Criminal's face, quieter, listening, his "
    "expression troubled rather than mocking.\n"
    "- Lighting: Soft, single directional light on his face.\n\n"
    "PANEL 4 (Bottom Section - Full Width, Panoramic Aspect):\n"
    "- Scene Type: Medium wide shot.\n"
    "- Composition: Jesus on the center cross, overhearing the mockery, his expression weary "
    "but composed, eyes open, enduring. Clean, unmarked skin on his hands and wrists -- no "
    "blood, no red marks.\n"
    "- Lighting: A single shaft of light breaks faintly through the dark clouds behind him.\n"
) + STYLE_TAIL

PAGE2 = AESTHETIC + (
    "This page continues directly from the reference page: same three figures, same crosses, "
    "same world.\n\n"
    "PANEL BREAKDOWN & SPATIAL COMPOSITION:\n\n"
    "PANEL 1 (Top Section - Full Width, Landscape Aspect):\n"
    "- Scene Type: Medium shot.\n"
    "- Composition: The Penitent Criminal turning his head toward the Mocking Criminal, "
    "rebuking him -- his expression firm, not angry.\n"
    "- Lighting: Dark, stormy, oppressive.\n\n"
    "PANEL 2 (Middle Left - Vertical Portrait Box):\n"
    "- Scene Type: Close-up.\n"
    "- Composition: Close-up on the Penitent Criminal's face, humbled, eyes lowered slightly, "
    "an expression of honest admission.\n"
    "- Lighting: Soft, single directional light.\n\n"
    "PANEL 3 (Middle Right - Vertical Portrait Box):\n"
    "- Scene Type: Close-up.\n"
    "- Composition: Close-up on the Penitent Criminal's face now turned toward Jesus, "
    "pleading, his eyes wet, desperate but sincere.\n"
    "- Lighting: A faint warm light beginning to fall across his face.\n\n"
    "PANEL 4 (Bottom Section - Full Width, Panoramic Aspect):\n"
    "- Scene Type: Medium shot.\n"
    "- Composition: Jesus turning his head slightly toward the Penitent Criminal, listening, "
    "his expression full of quiet compassion despite his suffering. Clean, unmarked skin on "
    "his hands and wrists -- no blood, no red marks.\n"
    "- Lighting: The same faint warm light now touching Jesus' face against the dark sky.\n"
) + STYLE_TAIL

PAGE3 = AESTHETIC + (
    "This page continues directly from the reference page: same three figures, same crosses, "
    "same world.\n\n"
    "PANEL BREAKDOWN & SPATIAL COMPOSITION:\n\n"
    "PANEL 1 (Top Section - Full Width, Landscape Aspect):\n"
    "- Scene Type: Close-up.\n"
    "- Composition: Close-up on Jesus' face, speaking, weary but resolute, a faint warm light "
    "now on his face against the dark storm clouds.\n"
    "- Lighting: Warm light breaking through the dark sky behind him.\n\n"
    "PANEL 2 (Middle Left - Vertical Portrait Box):\n"
    "- Scene Type: Close-up.\n"
    "- Composition: Close-up on the Penitent Criminal's face receiving the words -- relief and "
    "peace breaking through his pain, eyes glistening.\n"
    "- Lighting: The same warm light now on his face.\n\n"
    "PANEL 3 (Middle Right - Vertical Portrait Box):\n"
    "- Scene Type: Symbolic wide shot.\n"
    "- Composition: A break of warm light piercing through the dark storm clouds directly above "
    "the three crosses.\n"
    "- Lighting: Dramatic light breaking through darkness.\n\n"
    "PANEL 4 (Bottom Section - Full Width, Panoramic Aspect):\n"
    "- Scene Type: Wide landing shot.\n"
    "- Composition: The three crosses silhouetted against the darkening sky, seen from a "
    "distance, the light breaking through the clouds directly above the center cross.\n"
    "- Lighting: Somber, reverent, the light breaking through as the dominant visual note.\n"
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
    p1 = OUT / "page1.png"
    print("[img ] v2 page1 (reference, no chain, tightened wording) ...", flush=True)
    t = time.time()
    if run(PAGE1, p1, []):
        cost.record_hf("EW_Thief_POC", "short", "stills", MODEL, note="[poc-pages-v2] page1")
        print(f"   ok ({time.time()-t:.0f}s)")
    else:
        print("   FAILED"); return

    p2 = OUT / "page2.png"
    print("[img ] v2 page2 (chained to page1) ...", flush=True)
    t = time.time()
    if run(PAGE2, p2, [p1]):
        cost.record_hf("EW_Thief_POC", "short", "stills", MODEL, note="[poc-pages-v2] page2")
        print(f"   ok ({time.time()-t:.0f}s)")
    else:
        print("   FAILED"); return

    p3 = OUT / "page3.png"
    print("[img ] v2 page3 (chained to page2) ...", flush=True)
    t = time.time()
    if run(PAGE3, p3, [p2]):
        cost.record_hf("EW_Thief_POC", "short", "stills", MODEL, note="[poc-pages-v2] page3")
        print(f"   ok ({time.time()-t:.0f}s)")
    else:
        print("   FAILED")
    print(f"\n[out] {OUT}")


if __name__ == "__main__":
    main()
