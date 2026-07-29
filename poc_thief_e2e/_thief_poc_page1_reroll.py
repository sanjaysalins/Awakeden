"""Re-roll Page 1 (2026-07-25): chain to page2.png (not blank) so the Penitent
Criminal matches the look Pages 2-3 already agreed on, and tighten the Christ
body/blood wording (page1's original render showed visible ab definition and
reddish marks at the wrists -- borderline against the servant-register /
faint-blood-only gate).

  .venv\\Scripts\\python.exe poc_thief_e2e/_thief_poc_page1_reroll.py
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
OUT = HERE / "stills" / "_thief_poc"

AESTHETIC = (
    "A 9:16 vertical comic book page containing a structured 4-panel grid layout. The overall "
    "piece is rendered in a vintage graphic novel illustration style characterized by heavy "
    "black ink linework, high-contrast chiaroscuro shadows, cross-hatching, and a desaturated, "
    "muted earth-tone color palette (dominant slate grays, deep ochre, raw umber, muted blues). "
    "The paper has a subtle aged, textured vintage comic print finish with crisp panel borders "
    "and dark gutters separating each section.\n\n"
    "GLOBAL TEXTUAL CONSTRAINT: NO text of any kind anywhere on the page -- no speech bubbles, "
    "no caption boxes, no lettering, no words. The page is pure artwork only.\n\n"
    "CORE CHARACTER DESIGN ANCHORS (must exactly match the reference image's cast):\n"
    "- Jesus Christ: on the center cross, a lean, gaunt, sorrowful figure -- servant register, "
    "NOT heroic or muscular, ribs visible, no defined abdominal muscles. A crown of thorns. "
    "Skin unmarked and clean except faint matted blood at the brow only -- absolutely NO blood, "
    "no red marks, no wounds visible anywhere on the hands, wrists, feet, or torso. A simple "
    "loincloth per period convention. Marred, weary, dignified expression, not theatrical "
    "suffering.\n"
    "- The Penitent Criminal: an older, weathered condemned man with graying, thinning hair and "
    "a deeply lined face, on the cross to Jesus' one side, identical to his appearance in the "
    "reference image. A simple ragged loincloth. His face shows dawning humility and "
    "conviction.\n"
    "- The Mocking Criminal: another ordinary condemned man on the cross to Jesus' other side, "
    "gaunt and weathered, identical to his appearance in the reference image, his face "
    "contorted in bitterness and scorn.\n"
    "- Environmental Setting: Golgotha, a barren rocky hill outside Jerusalem's walls, an "
    "oppressive dark midday sky (the sun darkened), a distant crowd and Roman soldiers at the "
    "foot of the crosses.\n\n"
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
    "\n\nEXPLICIT STYLE CONSTRAINTS: Vintage comic book art, heavy black ink hatching, muted "
    "earth tones, sharp black panel borders, dark gutters, high structural consistency, "
    "reverent and dignified treatment throughout, absolutely no text or lettering anywhere, "
    "absolutely no visible blood anywhere on Jesus except a faint trace at the brow."
)


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
    page2 = OUT / "page2.png"
    out = OUT / "page1_reroll.png"
    print("[img ] page1 reroll (chained to page2) ...", flush=True)
    t = time.time()
    if run(AESTHETIC, out, [page2]):
        cost.record_hf("EW_Thief_POC", "short", "stills", MODEL, note="[poc-pages] page1 reroll")
        print(f"   ok ({time.time()-t:.0f}s)")
    else:
        print("   FAILED")
    print(f"\n[out] {out}")


if __name__ == "__main__":
    main()
