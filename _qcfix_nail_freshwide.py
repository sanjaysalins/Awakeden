"""7th attempt on nail_through_hand (Isaiah 53), per user decision 2026-07-20.

Attempts 1-5 (2x Seedance reframe, 3x Kling incl. anti-motion phrasing + a
flat-matte-ink wound edit) all failed: the wound spreads into a growing blood
splash by the clip's end. Attempt 6 tried a Gemini EDIT asking for a wider
pull-back framing -- Gemini did not actually recompose the shot (edits from a
single reference image preserve the input framing), so it failed identically.

This attempt (7) renders a genuinely FRESH still from a text prompt (no
reference image to anchor the tight crop) via the project's standard
graphic-novel HF pipeline (seedream_v4_5, same style_base/style_tail as every
other ink still in this episode), explicitly composing a WIDE shot: full
forearm + long stretch of beam + storm sky, hand/nail occupying only the lower
third of frame. Then one Kling3.0 pro roll, same frozen-tableau anti-motion
prompt proven elsewhere.
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

FROZEN = ("Every figure stays perfectly frozen the entire time -- no limbs move, no heads "
          "turn, no faces change, no morphing, no new figures, hands or objects appear. "
          "INVENT NOTHING: show only what is already painted in this exact image.")

STILL_OUT = (ROOT / "longform/01_Isaiah_53_Suffering_Servant/v1/visual_16x9_inked"
             "/clips/_qcfix_test/nail_through_hand_freshwide.png")
CLIP_OUT = (ROOT / "longform/01_Isaiah_53_Suffering_Servant/v1/visual_16x9_inked"
            "/clips/_qcfix_test/nail_through_hand_freshwide_kling.mp4")

PROMPT = (
    config.VISUAL_STYLE_BASE_GN + " "
    "a wide, reverent establishing view along a rough-hewn wooden cross beam in the "
    "storm-dark of Golgotha: a single forged square iron nail driven through the center of "
    "an open palm, with the whole forearm clearly visible rising from the nailed hand up past "
    "a bound wrist cord toward the upper edge of frame, the dark wooden beam stretching away "
    "on both sides beneath the hand, heavy dark storm clouds filling roughly the upper "
    "two-thirds of the frame, the hand and nail occupying only the lower third of the overall "
    "composition -- a wide distant framing, NOT a macro close-up, the nail mark itself small "
    "and simple: a single hard-edged flat matte dark ink shape with a crisp black outline and "
    "one flat fill color, no soft gradient, no glossy sheen, no sense of wetness, reading as a "
    "printed illustration mark, one dominant subject in a wide tableau, flat muted "
    "crimson-brown and grey tones, dramatic side light, cinematic 1st-century. " +
    config.VISUAL_STYLE_TAIL_GN
)


def hf_generate(prompt: str, model: str, aspect: str, out: Path) -> bool:
    cmd = [str(config.HF_CLI_PATH), "generate", "create", model,
           "--prompt", prompt, "--aspect_ratio", aspect, "--wait"]
    r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8",
                       errors="replace", timeout=600)
    blob = (r.stdout or "") + "\n" + (r.stderr or "")
    m = re.search(r"https://\S+?\.(?:png|jpg|jpeg)", r.stdout or "", re.IGNORECASE)
    if r.returncode != 0 or not m:
        print(f"[still] FAIL ({r.returncode}): {blob[-500:]}")
        return False
    req = urllib.request.Request(m.group(0), headers={"User-Agent": "JesusInTheBible/1.0"})
    with urllib.request.urlopen(req, timeout=120) as resp:
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_bytes(resp.read())
    cost.record_hf(ep, "long", "still", model, note="nail_through_hand fresh wide render (qcfix 7th attempt)")
    print(f"[still] ok -> {out}")
    return True


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
    cost.record_hf(ep, "long", "clip", "kling3_0", note=f"{slug} (qcfix fresh-wide-render re-roll)")
    print(f"[roll] ok -> {out}")
    return True


ep = "01_Isaiah_53"
if hf_generate(PROMPT, "seedream_v4_5", "9:16", STILL_OUT):
    ok = kling_roll(
        STILL_OUT, CLIP_OUT,
        ("A still finished inked graphic-novel illustration on flat canvas, filmed as ONE "
         "very slow, gentle push toward the nail-pierced hand resting on the wooden beam in "
         "the lower part of frame. The nail stays driven EXACTLY where painted, never lifts "
         "or shifts. The flat dark mark at the nail stays EXACTLY as painted, matte and still "
         "-- no blood flows, drips, spreads, brightens, pools, or grows, not even slightly, "
         "for the entire clip. " + FROZEN + " ONLY the light is alive: the dim glow across the "
         "wood grain and storm sky breathes gently, holding its exact painted tone from first "
         "frame to last."),
        "9:16", ep, "nail_through_hand")
else:
    ok = False

print(f"\n[done] nail_through_hand_freshwide={'ok' if ok else 'FAIL'}")
