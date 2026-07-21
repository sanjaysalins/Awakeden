"""Clip-QC fix test-gate ROUND 2 (~$2): the two classes that leaked in round 1.

1. BLOOD root-cause test: Gemini-edit Bronze still 31 to remove the painted
   hanging drips (tiny dry flush marks stay), then Seedance re-roll from the
   edited still. Round 1 proved the animator CONTINUES painted drips even on a
   positive-only prompt — so remove the drips at the source.
2. SNOW alternative-model test: the same EW01 scene on seedance1_5 instead of
   veo3_1_lite (which re-grew the particle overlay even with zero particle
   words). Checks whether Seedance holds the Baroque oil look on a near-static
   tableau (the 2026-05-30 bake-off's softening concern was on MOVING scenes).

Everything renders into _qcfix_test/ — approved stills/clips untouched.
"""
import re
import subprocess
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
import config
from pipeline import cost

LF = ROOT / "longform"
BR31 = LF / "04_The_Bronze_Serpent/v1/visual_16x9_inked/31_his_own_self_bare_our_sins_in_his_own_body_on_the_tree.png"
BR31_DRY = LF / "04_The_Bronze_Serpent/v1/visual_16x9_inked/clips/_qcfix_test/31_dry_test.png"
EW07 = LF / "EW01_Two_Goats/v1/visual_16x9/07_they_brought_me_two_goats_and_i_cast_lot.png"

STILL_RULE = ("The entire painting holds perfectly still like a printed page — every "
              "figure, face, and mark stays fixed exactly as painted. Only the camera moves.")


def gemini_edit_still():
    from google import genai
    from google.genai import types as genai_types
    client = genai.Client(api_key=config.GEMINI_API_KEY)
    up = client.files.upload(
        file=str(BR31),
        config=genai_types.UploadFileConfig(display_name=BR31.name, mime_type="image/png"))
    prompt = (
        "Edit this graphic-novel inked illustration with a single, minimal change: "
        "remove the two long hanging red drip lines that run down from the wrists and "
        "below the crossbeam, and reduce the red marking at each nail to one small dry "
        "dark mark flush against the skin. Change absolutely nothing else — keep the "
        "identical composition, framing, faces, robe, cross, storm clouds, line work, "
        "colors, and inked style. The result must look like the same page with the "
        "drips simply never inked.")
    resp = client.models.generate_content(
        model="gemini-3-pro-image-preview",
        contents=[{"parts": [
            {"fileData": {"mimeType": "image/png", "fileUri": up.uri}},
            {"text": prompt}]}],
        config={"responseModalities": ["IMAGE"], "imageConfig": {"aspectRatio": "16:9"}})
    import base64
    for p in resp.candidates[0].content.parts:
        if hasattr(p, "inline_data") and p.inline_data and p.inline_data.data:
            data = p.inline_data.data
            if isinstance(data, str):
                data = base64.b64decode(data)
            BR31_DRY.parent.mkdir(parents=True, exist_ok=True)
            BR31_DRY.write_bytes(data)
            cost.record_nbp("04_The_Bronze_Serpent", "long", "still-edit", 1,
                            note="31 dry-drip edit (qcfix test-gate r2)")
            print(f"[edit] ok -> {BR31_DRY}")
            return True
    print("[edit] FAIL: no image bytes returned")
    return False


def hf_roll(model, png, out, prompt, dur):
    cmd = [str(config.HF_CLI_PATH), "generate", "create", model,
           "--start-image", str(png), "--prompt", prompt,
           "--duration", dur, "--aspect_ratio", "16:9", "--wait"]
    r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8",
                       errors="replace", timeout=900)
    blob = (r.stdout or "") + "\n" + (r.stderr or "")
    m = re.search(r"https://\S+?\.mp4", r.stdout or "", re.IGNORECASE)
    if "nsfw" in blob.lower() or r.returncode != 0 or not m:
        print(f"[roll] FAIL {png.stem} ({r.returncode}): {blob[-300:]}")
        return False
    out.parent.mkdir(parents=True, exist_ok=True)
    req = urllib.request.Request(m.group(0), headers={"User-Agent": "JesusInTheBible/1.0"})
    with urllib.request.urlopen(req, timeout=300) as resp:
        out.write_bytes(resp.read())
    print(f"[roll] ok -> {out}")
    return True


if not gemini_edit_still():
    raise SystemExit(1)

ok1 = hf_roll(
    "seedance1_5", BR31_DRY,
    BR31_DRY.parent / "31_dryroll.mp4",
    ("Graphic novel inked illustration, a frozen painted tableau. Christ crucified on a "
     "wooden cross against a darkened storm sky, head bowed low, arms outstretched, "
     "wearing a simple cream-white robe, one small dry dark mark at each wrist fixed "
     "exactly as painted. " + STILL_RULE + " The camera settles almost imperceptibly, "
     "resting on the scene. The storm clouds hold their painted shapes."), "4")
if ok1:
    cost.record_hf("04_The_Bronze_Serpent", "long", "clip", "seedance1_5",
                   note="31 dry-still re-roll (qcfix test-gate r2)")

ok2 = hf_roll(
    "seedance1_5", EW07,
    LF / "EW01_Two_Goats/v1/visual_16x9/_qcfix_test/07_seedance.mp4",
    ("Classical Baroque oil painting on canvas with visible brushwork, a frozen painted "
     "moment. An old high priest in white robes holds two small stone lots above a "
     "bronze basin, two goats standing beside him before the goat-hair tent. The one "
     "thin plume of incense smoke already in the painting drifts slowly upward. "
     + STILL_RULE + " The camera pushes in very slowly toward the priest's hands. The "
     "painting keeps its oil-on-canvas texture in every frame."), "4")
if ok2:
    cost.record_hf("EW01_Two_Goats", "long", "clip", "seedance1_5",
                   note="07 seedance snow-fix test (qcfix test-gate r2)")

print(f"\n[done] dryroll={'ok' if ok1 else 'FAIL'} seedance_snow={'ok' if ok2 else 'FAIL'}")
