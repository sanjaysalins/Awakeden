"""Image-model bake-off for native comic-strip generation (2026-07-25): same
Thief page1+page2 prompts (tightened Christ-gate wording) that nano_banana_pro
was tested on, run across 5 other HF-hosted image models to see which holds
character/color consistency best across a chained 2-page test. None of these
expose a seed parameter through this CLI (checked first) -- the real
variable under test is each model's reference-image mechanism, not
determinism.

  .venv\\Scripts\\python.exe poc_thief_e2e/_image_model_bakeoff.py
"""
import re, subprocess, sys, time
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
import config
from pipeline import cost
HF = str(config.HF_CLI_PATH)
HERE = Path(__file__).resolve().parent
OUT = HERE / "stills" / "_image_model_bakeoff"
OUT.mkdir(parents=True, exist_ok=True)

# Reuse the exact validated wording from _thief_poc_pages_v2.py
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

MODELS = [
    ("flux_2", ["--resolution", "2k", "--variant", "pro"]),
    ("seedream_v5_pro", ["--resolution", "2k"]),
    ("gpt_image_2", ["--resolution", "2k", "--quality", "high"]),
    ("kling_omni_image", ["--resolution", "2k"]),
    ("flux_kontext", []),
]


def run(model, prompt, out, refs, extra):
    cmd = [HF, "generate", "create", model, "--prompt", prompt, "--aspect_ratio", "9:16", "--wait"] + extra
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
    for model, extra in MODELS:
        p1 = OUT / f"{model}_page1.png"
        print(f"[img ] {model} page1 ...", flush=True)
        t = time.time()
        if run(model, PAGE1, p1, [], extra):
            try:
                cost.record_hf("EW_Thief_POC", "short", "stills", model, note="[image-model-bakeoff] page1")
            except Exception as e:
                print(f"   (ledger skipped: {e})")
            print(f"   ok ({time.time()-t:.0f}s)")
        else:
            print("   FAILED"); continue

        p2 = OUT / f"{model}_page2.png"
        print(f"[img ] {model} page2 (chained) ...", flush=True)
        t = time.time()
        if run(model, PAGE2, p2, [p1], extra):
            try:
                cost.record_hf("EW_Thief_POC", "short", "stills", model, note="[image-model-bakeoff] page2")
            except Exception as e:
                print(f"   (ledger skipped: {e})")
            print(f"   ok ({time.time()-t:.0f}s)")
        else:
            print("   FAILED")
    print(f"\n[out] {OUT}")


if __name__ == "__main__":
    main()
