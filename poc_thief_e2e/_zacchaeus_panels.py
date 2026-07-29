"""Zacchaeus (Luke 19:1-10) visual panels -- new architecture (2026-07-25):
separate, purpose-built, full-resolution panel stills, chained panel-to-panel,
per COMIC_STRIP_NATIVE_SPEC.md §0.5. First ministry-register (not passion,
not glory) test of the Character Anchor discipline.

  .venv\\Scripts\\python.exe poc_thief_e2e/_zacchaeus_panels.py
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
OUT = HERE / "stills" / "_zacchaeus"
OUT.mkdir(parents=True, exist_ok=True)

ANCHORS = (
    "Rendered in a vintage graphic novel illustration style: heavy black ink linework, "
    "high-contrast chiaroscuro shadows, cross-hatching, a desaturated muted earth-tone color "
    "palette (slate grays, deep ochre, raw umber, muted blues), aged textured comic print "
    "finish. NO text, no lettering, no speech bubbles anywhere -- pure artwork only.\n\n"
    "CHARACTER ANCHORS (must exactly match across every image):\n"
    "- Jesus Christ: a Jewish teacher in his early thirties, ordinary ministry register -- "
    "dignified, warm, approachable, NOT suffering and NOT radiant/triumphant (this is neither "
    "a passion beat nor a glory beat). Simple first-century Judean robes (undyed linen tunic, "
    "a plain outer mantle), dark hair and short beard, calm and direct gaze, a kind but "
    "authoritative expression.\n"
    "- Zacchaeus: a short, slight man in his forties, finely dressed in richer robes than "
    "everyone around him (a wealthy tax collector's clothing, out of place among the ordinary "
    "crowd), clean-shaven or close-cropped beard, an anxious, eager face -- a man used to "
    "being looked down on, risking dignity just to see.\n"
    "- Setting: Jericho, a dusty first-century street, a large sycamore tree with wide "
    "spreading branches, a dense crowd of ordinary Judean men and women in period dress, "
    "bright midday sun.\n\n"
)

PANEL_A = ANCHORS + (
    "SINGLE PANEL, wide shot. A dense crowd fills a dusty Jericho street. Above them, "
    "Zacchaeus -- small, richly dressed, out of place -- has climbed up into the wide branches "
    "of a sycamore tree, straining to see over the heads of the crowd below. Reverent, warm, "
    "sunlit. No text anywhere."
)
PANEL_B = ANCHORS + (
    "This continues directly from the reference image: same cast, same world.\n\n"
    "SINGLE PANEL, medium close-up on Jesus. He has stopped walking and is looking directly "
    "up and slightly to the side, toward someone above him, his face warm and direct, calling "
    "out. The crowd is a soft blur behind him. Reverent, warm, sunlit. No text anywhere."
)
PANEL_C = ANCHORS + (
    "This continues directly from the reference image: same cast, same world.\n\n"
    "SINGLE PANEL, close-up on Zacchaeus's face, still up in the sycamore tree, looking down "
    "-- his anxious expression breaking into stunned, joyful disbelief at being seen and "
    "called by name. Leaves and branches frame his face. Reverent, warm, sunlit. No text "
    "anywhere."
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
    a = OUT / "panel_a_wide.png"
    print("[img ] panel_a_wide (reference, no chain) ...", flush=True)
    t = time.time()
    if run(PANEL_A, a, [], ar="16:9"):
        cost.record_hf("Zacchaeus_Luke19", "short", "stills", MODEL, note="[zacchaeus] panel_a")
        print(f"   ok ({time.time()-t:.0f}s)")
    else:
        print("   FAILED"); return

    b = OUT / "panel_b_jesus.png"
    print("[img ] panel_b_jesus (chained to a) ...", flush=True)
    t = time.time()
    if run(PANEL_B, b, [a], ar="1:1"):
        cost.record_hf("Zacchaeus_Luke19", "short", "stills", MODEL, note="[zacchaeus] panel_b")
        print(f"   ok ({time.time()-t:.0f}s)")
    else:
        print("   FAILED"); return

    c = OUT / "panel_c_zacchaeus.png"
    print("[img ] panel_c_zacchaeus (chained to b) ...", flush=True)
    t = time.time()
    if run(PANEL_C, c, [b], ar="1:1"):
        cost.record_hf("Zacchaeus_Luke19", "short", "stills", MODEL, note="[zacchaeus] panel_c")
        print(f"   ok ({time.time()-t:.0f}s)")
    else:
        print("   FAILED")
    print(f"\n[out] {OUT}")


if __name__ == "__main__":
    main()
