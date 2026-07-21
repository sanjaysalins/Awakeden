"""6th attempt on nail_through_hand (Isaiah 53), per user decision 2026-07-20.

5 straight attempts (2x Seedance reframe, 3x Kling incl. explicit anti-motion
phrasing AND a flat-matte-ink wound edit) all failed with the SAME defect: the
wound spreads into a blood-splash shape by the end of the clip. Root cause
identified by hand-checking the frames: the macro close-up framing itself (the
wound fills ~15-20% of frame, hand fills ~70%) is what triggers the model's
physics prior, independent of how the wound mark is drawn.

Fix: pull the camera back so the hand/wound is a smaller part of a wider
composition (more forearm, more cross beam, more sky) -- same principle that
worked on the project's own successful wide hero-close shot
(04_The_Bronze_Serpent/.../21_look_to_the_one_lifted_up_hero_close.png, where
a small wound scar sits in a full face+torso+arm composition). Combines the
wide pull-back with the already-proven flat-matte-ink wound treatment in one
edit, from the native 9:16 master (not the already-tightly-cropped dry2 edit).
"""
import base64
import re
import subprocess
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
import config
from pipeline import cost

FROZEN = ("Every figure stays perfectly frozen the entire time -- no limbs move, no heads "
          "turn, no faces change, no morphing, no new figures, hands or objects appear. "
          "INVENT NOTHING: show only what is already painted in this exact image.")

SRC = (ROOT / "longform/01_Isaiah_53_Suffering_Servant/v1/visual_16x9_inked"
       "/nail_through_hand.png")
EDIT = (ROOT / "longform/01_Isaiah_53_Suffering_Servant/v1/visual_16x9_inked"
        "/clips/_qcfix_test/nail_through_hand_wide.png")
OUT = (ROOT / "longform/01_Isaiah_53_Suffering_Servant/v1/visual_16x9_inked"
       "/clips/_qcfix_test/nail_through_hand_wide_kling.mp4")


def gemini_edit(src: Path, out: Path, prompt: str, aspect: str, ep: str, note: str) -> bool:
    from google import genai
    from google.genai import types as genai_types
    client = genai.Client(api_key=config.GEMINI_API_KEY)
    up = client.files.upload(file=str(src), config=genai_types.UploadFileConfig(
        display_name=src.name, mime_type="image/png"))
    resp = client.models.generate_content(
        model="gemini-3-pro-image-preview",
        contents=[{"parts": [{"fileData": {"mimeType": "image/png", "fileUri": up.uri}},
                             {"text": prompt}]}],
        config={"responseModalities": ["IMAGE"], "imageConfig": {"aspectRatio": aspect}})
    for p in resp.candidates[0].content.parts:
        if hasattr(p, "inline_data") and p.inline_data and p.inline_data.data:
            data = p.inline_data.data
            if isinstance(data, str):
                data = base64.b64decode(data)
            out.parent.mkdir(parents=True, exist_ok=True)
            out.write_bytes(data)
            cost.record_nbp(ep, "long", "still-edit", 1, note=note)
            print(f"[edit] ok -> {out}")
            return True
    print(f"[edit] FAIL {out.name}: no image bytes")
    return False


def kling_roll(src: Path, out: Path, prompt: str, aspect: str, ep: str, slug: str) -> bool:
    cmd = [str(config.HF_CLI_PATH), "generate", "create", "kling3_0",
           "--start-image", str(src), "--prompt", prompt,
           "--duration", "5", "--aspect_ratio", aspect,
           "--mode", "pro", "--sound", "off", "--wait"]
    r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8",
                       errors="replace", timeout=900)
    blob = (r.stdout or "") + "\n" + (r.stderr or "")
    m = re.search(r"https://\S+?\.mp4", r.stdout or "", re.IGNORECASE)
    if "nsfw" in blob.lower() or r.returncode != 0 or not m:
        print(f"[roll] FAIL {out.name} ({r.returncode}): {blob[-300:]}")
        return False
    req = urllib.request.Request(m.group(0), headers={"User-Agent": "JesusInTheBible/1.0"})
    with urllib.request.urlopen(req, timeout=300) as resp:
        out.write_bytes(resp.read())
    cost.record_hf(ep, "long", "clip", "kling3_0", note=f"{slug} (qcfix wide-pullback re-roll)")
    print(f"[roll] ok -> {out}")
    return True


if gemini_edit(
    SRC, EDIT,
    "Edit this graphic-novel inked illustration by pulling the camera back to a wider view "
    "of the SAME moment. Keep the nail-pierced hand and the cross beam it rests on, but now "
    "show noticeably more of the forearm rising toward the upper left (to the wrist cord and "
    "a hint of the robe sleeve) and more of the dark wooden beam extending on both sides, plus "
    "more of the dark stormy sky, so the hand occupies roughly a third of the frame height "
    "instead of filling most of it -- a wider, more distant framing, not a macro close-up. "
    "Also replace the soft, glossy, dripping red blood mark around the nail with a small, "
    "hard-edged, completely FLAT matte dark ink mark -- drawn the same way the rest of the "
    "image is drawn, crisp black outline, one flat fill color, no gradient, no sheen, no sense "
    "of wetness or depth; it must read as a printed illustration mark, not a photo of a wound. "
    "Keep the identical art style, palette, nail, hand pose, wrist cord, and wood grain -- only "
    "the framing (pulled back / wider) and the wound rendering (flat matte) change.",
    "9:16", "01_Isaiah_53", "nail_through_hand wide-pullback + dry-flatten edit (qcfix 6th attempt)"
):
    ok = kling_roll(
        EDIT, OUT,
        ("A still finished inked graphic-novel illustration on flat canvas, filmed as ONE "
         "very slow, gentle push toward the nail-pierced hand resting on the wooden beam in "
         "the lower half of frame. The nail stays driven EXACTLY where painted, never lifts "
         "or shifts. The flat dark mark at the nail stays EXACTLY as painted, matte and still "
         "-- no blood flows, drips, spreads, brightens, pools, or grows, not even slightly, "
         "for the entire clip. " + FROZEN + " ONLY the light is alive: the dim glow across the "
         "wood grain and storm sky breathes gently, holding its exact painted tone from first "
         "frame to last."),
        "9:16", "01_Isaiah_53", "nail_through_hand")
else:
    ok = False

print(f"\n[done] nail_through_hand_wide={'ok' if ok else 'FAIL'}")
