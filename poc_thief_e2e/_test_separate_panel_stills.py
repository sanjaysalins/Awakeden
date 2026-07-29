"""Consistency check for the separate-panel-stills architecture (2026-07-25):
generate 3 full-resolution, purpose-built panel stills (NOT cropped from a
whole page) for different beats of the Thief story, chained panel-to-panel,
using the same validated Character Anchors as the native-page recipe. Tests
whether chaining holds consistency as well when panels are independently
generated as it did when they were all part of one page.

  .venv\\Scripts\\python.exe poc_thief_e2e/_test_separate_panel_stills.py
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
OUT = HERE / "stills" / "_separate_panels"
OUT.mkdir(parents=True, exist_ok=True)

# Same validated Character Anchors as the native-page recipe (COMIC_STRIP_NATIVE_SPEC.md §2a fix)
ANCHORS = (
    "Rendered in a vintage graphic novel illustration style: heavy black ink linework, "
    "high-contrast chiaroscuro shadows, cross-hatching, a desaturated muted earth-tone color "
    "palette (slate grays, deep ochre, raw umber, muted blues), aged textured comic print "
    "finish. NO text, no lettering, no speech bubbles anywhere -- pure artwork only.\n\n"
    "CHARACTER ANCHORS (must exactly match across every image):\n"
    "- Jesus Christ: on the center cross, a lean, gaunt, sorrowful figure in the servant "
    "register -- a marred, weary body with visible ribs and a soft, undefined torso. A crown "
    "of thorns, with faint, dried, matted blood at the brow and at the wrists and feet where "
    "the nails pierce -- dark and dull, never bright or fresh. A simple loincloth per period "
    "convention. A marred, weary, dignified expression, not theatrical suffering.\n"
    "- The Penitent Criminal: an older, weathered condemned man with graying, thinning hair "
    "and a deeply lined face, on the cross to Jesus' one side. A simple ragged loincloth.\n"
    "- The Mocking Criminal: another ordinary condemned man, gaunt and weathered, dark hair, "
    "his face contorted in bitterness and scorn.\n"
    "- Setting: Golgotha, a barren rocky hill outside Jerusalem's walls, an oppressive dark "
    "midday sky, a distant crowd and Roman soldiers.\n\n"
)

PANEL_A = ANCHORS + (
    "SINGLE PANEL, close-up on Jesus Christ's face, speaking, weary but resolute, a faint "
    "warm light breaking through the dark storm clouds behind him against the crown of "
    "thorns. Reverent, dignified, no text anywhere."
)
PANEL_B = ANCHORS + (
    "This continues directly from the reference image: same cast, same world.\n\n"
    "SINGLE PANEL, close-up on the Penitent Criminal's face, receiving the words -- relief "
    "and peace breaking through his pain, eyes glistening, the same warm light now on his "
    "face. Reverent, dignified, no text anywhere."
)
PANEL_C = ANCHORS + (
    "This continues directly from the reference image: same cast, same world.\n\n"
    "SINGLE PANEL, wide establishing shot of Golgotha from a distance. Three crosses stand "
    "against the dark, oppressive sky. Jesus hangs on the center cross, the two criminals on "
    "crosses to either side. A distant crowd and Roman soldiers at the foot of the hill. "
    "Reverent, dignified, no text anywhere."
)


def run(prompt, out, refs, ar="1:1"):
    cmd = [HF, "generate", "create", MODEL, "--prompt", prompt, "--aspect_ratio", ar,
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
    a = OUT / "panel_a_jesus.png"
    print("[img ] panel_a_jesus (reference, no chain) ...", flush=True)
    t = time.time()
    if run(PANEL_A, a, [], ar="1:1"):
        cost.record_hf("EW_Thief_POC", "short", "stills", MODEL, note="[separate-panels] panel_a")
        print(f"   ok ({time.time()-t:.0f}s)")
    else:
        print("   FAILED"); return

    b = OUT / "panel_b_penitent.png"
    print("[img ] panel_b_penitent (chained to a) ...", flush=True)
    t = time.time()
    if run(PANEL_B, b, [a], ar="1:1"):
        cost.record_hf("EW_Thief_POC", "short", "stills", MODEL, note="[separate-panels] panel_b")
        print(f"   ok ({time.time()-t:.0f}s)")
    else:
        print("   FAILED"); return

    c = OUT / "panel_c_wide.png"
    print("[img ] panel_c_wide (chained to b) ...", flush=True)
    t = time.time()
    if run(PANEL_C, c, [b], ar="16:9"):
        cost.record_hf("EW_Thief_POC", "short", "stills", MODEL, note="[separate-panels] panel_c")
        print(f"   ok ({time.time()-t:.0f}s)")
    else:
        print("   FAILED")
    print(f"\n[out] {OUT}")


if __name__ == "__main__":
    main()
