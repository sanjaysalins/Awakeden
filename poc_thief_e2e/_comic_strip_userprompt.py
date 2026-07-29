"""Test the user's own prompt approach (2026-07-24): a 4-panel page with
BAKED CAPTION TEXT and named characters (Gestas/Dismas), generated via
nano_banana_pro, then a second page chaining the first as a --image
reference for cross-generation character consistency. Tests the MECHANISM
(does this hold consistency better?) -- adopting baked text / apocryphal
names into final production is a separate decision, flagged, not assumed.

  .venv\\Scripts\\python.exe poc_thief_e2e/_comic_strip_userprompt.py
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
OUT = HERE / "stills" / "_comic_strip_userprompt"
OUT.mkdir(parents=True, exist_ok=True)

IMAGE_6_PROMPT = (
    "A 9:16 vertical comic book page with a dynamic multi-panel layout in a dark, vintage "
    "graphic novel style with heavy black ink lines and muted earth tones, featuring caption "
    "boxes instead of speech bubbles. \n\n"
    "Panel 1 (top full width): Full scene of Calvary hill under an oppressive stormy, dark sky. "
    "Three crosses stand on Golgotha with Roman soldiers and a crowd below. Two yellow "
    "rectangular caption boxes read: 'THE DARK HOURS BEGAN.' in the top left, and 'AND THE "
    "UNREPENANT THIEF GESTAS CRIED OUT.' in the top right.\n\n"
    "Panel 2 (middle left): Close-up of Gestas, the unrepentant thief on the left cross, roaring "
    "at the sky in anger with a contorted face. A caption box reads: 'ARE YOU NOT THE CHRIST? "
    "SAVE YOURSELF AND US!'\n\n"
    "Panel 3 (middle right): Close-up of Dismas, the penitent thief, looking across at Jesus "
    "with tearful eyes and a sorrowful expression. A caption box reads: 'DO YOU NOT FEAR GOD, "
    "SINCE YOU ARE UNDER THE SAME SENTENCE?'\n\n"
    "Panel 4 (bottom full width): A detailed close-up shot focusing on Jesus Christ on the "
    "center cross wearing a crown of thorns with blood trickling down, looking compassionately "
    "at Dismas. A yellow rectangular caption box at the bottom reads: 'TODAY, YOU WILL BE WITH "
    "ME IN PARADISE.'\n\n"
    "Dark gutters separating panels, sharp panel borders, retro comic book art style, vertical "
    "layout."
)

PAGE1_PROMPT = (
    "A detailed 9:16 vertical comic book page with dark gutters separating four distinct "
    "panels. The overall style is gritty, heavy black ink lines, and muted earth tones, "
    "maintaining the specific visual look of image_6.png. The texture is distressed comic "
    "paper.\n\n"
    "Panel 1 (top, full-width): An expanded, wide view of Calvary hill, identical to the "
    "setting in image_6.png. The three consistent crosses silhouette against the dark, stormy, "
    "turbulent sky. The Roman Centurion (wearing the red-crested helmet) is visible in the "
    "foreground, supervising a large crowd and more detailed Roman soldiers. A yellow "
    "rectangular caption box in the top-left reads: 'THE DARK HOURS BEGAN.' A separate caption "
    "box in the top-right reads: 'AND THE UNREPENANT THIEF GESTAS CRIED OUT.'\n\n"
    "Panel 2 (upper-middle, medium close-up): A focused shot on Gestas, the unrepentant thief "
    "on the left cross, visually identical (rugged beard, agonizing strain) to his appearance "
    "in image_6.png. He is straining, roaring at the crowd/sky (directionally right). No speech "
    "bubbles. A yellow rectangular caption box below him reads: 'ARE YOU NOT THE CHRIST? SAVE "
    "YOURSELF AND US!'\n\n"
    "Panel 3 (lower-middle, medium close-up): A focused shot on Dismas, the penitent thief from "
    "image_6.png, showing his tearful, short dark-bearded face. He is looking sharply towards "
    "the center cross (directionally left), his expression a mix of pain and earnest regret. No "
    "bubbles. A yellow rectangular caption box below him reads: 'DO YOU NOT FEAR GOD, SINCE YOU "
    "ARE UNDER THE SAME SENTENCE?'\n\n"
    "Panel 4 (bottom, full-width): A solemn medium-close-up shot focusing on Jesus Christ "
    "(center, wearing the consistent crown of thorns from image_6.png). His body is strained "
    "but his expression is calm. He turns his head slightly right. A low angle focuses on his "
    "suffering. No bubbles. A small yellow box at the very bottom center reads: 'AND THE LAND "
    "BECAME DARK.'"
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
    image6 = OUT / "image_6.png"
    print("[img ] image_6 (reference, no chain) ...", flush=True)
    t = time.time()
    if run(IMAGE_6_PROMPT, image6, []):
        cost.record_hf("EW_Thief_POC", "short", "stills", MODEL, note="[user-prompt] image_6")
        print(f"   ok ({time.time()-t:.0f}s)")
    else:
        print("   FAILED"); return

    page1 = OUT / "page1.png"
    print("[img ] page1 (chained to image_6) ...", flush=True)
    t = time.time()
    if run(PAGE1_PROMPT, page1, [image6]):
        cost.record_hf("EW_Thief_POC", "short", "stills", MODEL, note="[user-prompt] page1")
        print(f"   ok ({time.time()-t:.0f}s)")
    else:
        print("   FAILED")
    print(f"\n[out] {OUT}")


if __name__ == "__main__":
    main()
