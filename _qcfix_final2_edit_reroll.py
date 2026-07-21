"""Still-edit-then-reroll on the final 2 stubborn clip-QC-fix clips, per the
user's explicit go-ahead (2026-07-20): both failed 4 straight animation
attempts (2x Seedance, 2x Kling incl. proven anti-motion phrasing) with the
IDENTICAL defect every time -- strong evidence the STILL's own composition
(a wound with soft/diffuse coloring; bones genuinely suspended in open air)
is what invites the model's physics prior to override the text instruction.
Fix at the source, same technique already proven on the Bronze Serpent
blood-drip clips this session.

1. nail_through_hand: flatten the wound mark to a hard-edged, flat, matte
   dark-dried-blood ink shape (no soft gradient/sheen suggesting wet liquid),
   drawn like the rest of the illustration's line-and-flat-color style --
   removes the "wet, has depth, could flow" visual cue.
2. lots_dice_closeup: remove the bones genuinely suspended in open air
   (nothing touching them = strongest "please let this fall" cue); keep only
   bones resting in the palm or already settled in the pouch.

Then one Kling3.0 pro re-roll per clip from the corrected still.
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

NAIL_SRC = (ROOT / "longform/01_Isaiah_53_Suffering_Servant/v1/visual_16x9_inked"
            "/clips/_qcfix_test/nail_through_hand_dry.png")
NAIL_EDIT2 = (ROOT / "longform/01_Isaiah_53_Suffering_Servant/v1/visual_16x9_inked"
              "/clips/_qcfix_test/nail_through_hand_dry2.png")
NAIL_OUT = (ROOT / "longform/01_Isaiah_53_Suffering_Servant/v1/visual_16x9_inked"
            "/clips/_qcfix_test/nail_through_hand_kling3.mp4")

LOTS_SRC = (ROOT / "longform/02_Psalm_22_Song_From_The_Cross/v1/visual_16x9_inked"
            "/lots_dice_closeup.png")
LOTS_EDIT = (ROOT / "longform/02_Psalm_22_Song_From_The_Cross/v1/visual_16x9_inked"
             "/clips/_qcfix_test/lots_dice_closeup_settled.png")
LOTS_OUT = (ROOT / "longform/02_Psalm_22_Song_From_The_Cross/v1/visual_16x9_inked"
            "/clips/_qcfix_test/lots_dice_closeup_kling3.mp4")


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
    cost.record_hf(ep, "long", "clip", "kling3_0", note=f"{slug} (qcfix final still-edit re-roll)")
    print(f"[roll] ok -> {out}")
    return True


# 1. nail_through_hand
if gemini_edit(
    NAIL_SRC, NAIL_EDIT2,
    "Edit this graphic-novel inked illustration with a single, minimal change: replace the "
    "soft, diffuse reddish smudge around the nail with a small, hard-edged, completely FLAT "
    "matte dark ink mark -- drawn the same way the rest of the image is drawn, with a crisp "
    "black outline and one flat fill color, no soft gradient, no glossy sheen, no sense of "
    "wetness or depth. It must read as a printed illustration mark, not a photo of a wound. "
    "Change absolutely nothing else -- keep the identical nail, hand pose, fingers, wrist "
    "cord, wood grain, dark sky, composition, and inked line style.",
    "9:16", "01_Isaiah_53", "nail_through_hand dry-flatten edit v2 (qcfix final)"
):
    ok1 = kling_roll(
        NAIL_EDIT2, NAIL_OUT,
        ("A still finished inked graphic-novel illustration on flat canvas, filmed as ONE "
         "very slow, gentle push toward the outstretched fingertips at the lower right of "
         "the frame. The nail stays driven EXACTLY where painted, never lifts or shifts. "
         "The flat dark mark at the nail stays EXACTLY as painted, matte and still -- no "
         "blood flows, drips, spreads, brightens, pools, or grows, not even slightly, for "
         "the entire clip. " + FROZEN + " ONLY the light is alive: the dim glow across the "
         "wood grain breathes gently, holding its exact painted tone from first frame to "
         "last."),
        "9:16", "01_Isaiah_53", "nail_through_hand")
else:
    ok1 = False

# 2. lots_dice_closeup
if gemini_edit(
    LOTS_SRC, LOTS_EDIT,
    "Edit this graphic-novel inked illustration with one change: remove the bones that are "
    "shown falling loose in open air between the dropping hand and the cloth below (the "
    "ones with nothing touching them), and remove the single bone pinched at the dropping "
    "hand's fingertips -- that hand is now open and empty, lowered slightly, no longer "
    "holding or releasing anything. Add those same bones into the pile already resting on "
    "the white cloth below instead, so the cloth now shows a slightly fuller settled pile. "
    "Change nothing else -- keep the identical soldiers, the other hand's held bones, the "
    "cloth folds, the background figures, the composition, and the inked line style.",
    "16:9", "02_Psalm_22", "lots_dice_closeup settled-bones edit (qcfix final)"
):
    ok2 = kling_roll(
        LOTS_EDIT, LOTS_OUT,
        ("A still finished inked graphic-novel illustration on flat canvas, filmed as ONE "
         "very slow push down toward the folds of the white garment at the lower right of "
         "frame. Every knucklebone stays held EXACTLY where painted -- none move, fall, or "
         "shift, for the entire clip; the soldiers' hands and arms stay exactly as painted, "
         "never move, reach, or open further. " + FROZEN + " ONLY the light is alive: the "
         "warm dusty light across the cloth breathes gently, holding its exact painted tone "
         "from first frame to last."),
        "16:9", "02_Psalm_22", "lots_dice_closeup")
else:
    ok2 = False

print(f"\n[done] nail_through_hand={'ok' if ok1 else 'FAIL'} lots_dice_closeup={'ok' if ok2 else 'FAIL'}")
