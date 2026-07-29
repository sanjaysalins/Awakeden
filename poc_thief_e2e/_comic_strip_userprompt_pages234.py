"""Render Pages 2, 3, 4 of the user's own prompt sequence (2026-07-24), each
chained to image_6.png as the consistency reference, exactly as they
specified ("Character models for Jesus, Gestas, and Dismas are consistent").

  .venv\\Scripts\\python.exe poc_thief_e2e/_comic_strip_userprompt_pages234.py
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
IMAGE6 = OUT / "image_6.png"

PAGE2_PROMPT = (
    "A 9:16 vertical comic book page, continuing the narrative of Page 1. Dark gutters, heavy "
    "ink, and the muted earth tone aesthetic established in image_6.png are maintained across "
    "four new panels. Character models for Jesus, Gestas, and Dismas are consistent.\n\n"
    "Panel 1 (top, full-width): A tight close-up shot focused on the hands of Dismas (the "
    "penitent thief) tied to the rough wood of the cross. A yellow rectangular caption box in "
    "the top-left reads: 'HE WEIGHED HIS LIFE...'\n\n"
    "Panel 2 (upper-middle, medium shot): Dismas, visibly consistent with image_6.png, looks "
    "past the center cross toward Gestas (left). His face is intense with sincere rebuke. No "
    "bubbles. A yellow rectangular caption box in the bottom-right reads: '...BUT THIS MAN HAS "
    "DONE NOTHING WRONG.'\n\n"
    "Panel 3 (lower-middle, medium close-up): A tight, respectful close-up on the suffering but "
    "compassionate face of Jesus Christ (consistent with image_6.png), looking down towards "
    "Dismas (right). The light from Page 1 is fading. No bubbles. A yellow rectangular caption "
    "box in the top-right reads: 'AND THEN, A PLEA.'\n\n"
    "Panel 4 (bottom, full-width): An intimate, dual close-up, focusing purely on the faces of "
    "Jesus (center) and Dismas (right) as they share a private, silent moment of connection. "
    "Jesus's eyes show profound mercy. Dismas looks up with hope. No bubbles. A yellow caption "
    "box at the very bottom-center reads: 'JESUS, REMEMBER ME WHEN YOU COME INTO YOUR KINGDOM.'"
)

PAGE3_PROMPT = (
    "A 9:16 vertical comic book page, strictly maintaining the gritty, heavy ink, muted "
    "earth-tone aesthetic and character models defined in image_6.png. The sequence continues "
    "across four panels with dark gutters.\n\n"
    "Panel 1 (top, full-width): A medium-close-up shot focused on Jesus Christ on the center "
    "cross, identical to image_6.png with the crown of thorns and expression. He strains to "
    "speak. The background is a stark, dark stormy sky. No bubbles. A yellow rectangular "
    "caption box in the top-left reads: 'HE LOOKED UPON HIM WITH GRACE...'\n\n"
    "Panel 2 (upper-middle, medium close-up): A tightly focused close-up on the face of Dismas "
    "(consistent model), capturing his tearful eyes wide with expectation and dawning peace, "
    "looking left towards Jesus. The light highlights his features. No bubbles. A yellow "
    "caption box in the bottom-right reads: '...AND A PROMISE WAS SPOKEN.'\n\n"
    "Panel 3 (lower-middle, intimate dual close-up): An intimate, dual profile shot, showing "
    "Jesus (left, crown of thorns) speaking directly to Dismas (right). Their faces are inches "
    "apart. Jesus's eyes are full of love. The scene is illuminated by a subtle warm glow. No "
    "bubbles. A yellow caption box below their interaction reads: 'TODAY, YOU WILL BE WITH ME "
    "IN PARADISE.'\n\n"
    "Panel 4 (bottom, full-width): A solemn close-up shot, looking up at Jesus Christ on the "
    "cross (consistent profile). He is exhausted, but a serene look replaces his pain. The "
    "crown of thorns is visible. The light on his face is fading. No bubbles. A yellow caption "
    "box at the very bottom right reads: 'IT IS FINISHED.'"
)

PAGE4_PROMPT = (
    "A detailed 9:16 vertical comic book page summarizing the scene from image_6.png, "
    "maintaining all visual continuity across four concluding panels with dark gutters. "
    "Gritty, heavy ink style, and muted earth tones.\n\n"
    "Panel 1 (top, full-width establishes): A high-angle view looking down Calvary hill. Below "
    "the consistent three crosses (seen as rough timber), the ground is rocky. The Roman "
    "Centurion (red-crested helmet) is seen at the edge of the cliff with his back partially to "
    "the viewer, looking down with a grim expression at the large, diverse, troubled crowd of "
    "people. A yellow caption box in the top-left reads: 'AND THE CROWD DEPARTED.'\n\n"
    "Panel 2 (upper-middle, medium-close-up, Left): A medium-close-up of Gestas (the "
    "unrepentant thief), consistent with image_6.png, but now silent and slumped, staring down "
    "at the ground with an agonizing, defeated expression. The crowd is a blurred mass below. A "
    "yellow caption box in the bottom-left corner reads: 'A PROPHECY IGNORED.'\n\n"
    "Panel 3 (lower-middle, medium-close-up, Right): An intimate, detailed close-up shot of the "
    "face of Dismas (consistent model). His head is still turned towards where Jesus was, his "
    "eyes now closed in peaceful rest, a calm serenity replacing his previous pain. A subtle "
    "light fades on his features. A yellow caption box in the bottom-right corner reads: 'A "
    "PROMISE KEPT.'\n\n"
    "Panel 4 (bottom, full-width): A final, powerful high-angle shot looking down at the three "
    "completed, silent crosses. Darkness (the ninth hour) has almost fully consumed the "
    "landscape. A single, distinct star begins to pierce the stormy clouds directly above the "
    "central cross. A small yellow caption box at the bottom-center reads: 'THE PROMISE OF "
    "MERCY.'"
)

JOBS = [("page2", PAGE2_PROMPT), ("page3", PAGE3_PROMPT), ("page4", PAGE4_PROMPT)]


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
    for name, prompt in JOBS:
        out = OUT / f"{name}.png"
        print(f"[img ] {name} (chained to image_6) ...", flush=True)
        t = time.time()
        if run(prompt, out, [IMAGE6]):
            cost.record_hf("EW_Thief_POC", "short", "stills", MODEL, note=f"[user-prompt] {name}")
            print(f"   ok ({time.time()-t:.0f}s)")
        else:
            print("   FAILED")
    print(f"\n[out] {OUT}")


if __name__ == "__main__":
    main()
