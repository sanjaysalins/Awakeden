"""Build the Jesus REFERENCE GRID (face + body) — the proper anchor.
The old REF was head-and-shoulders only, so seedream had no locked BODY to scale
against and each scene invented its own proportions (the scaling issues).
This makes a full-body standing reference (locked to the face), then composes a
single grid PNG: [face close-up | full body] -> JESUS__GRID.png, the new anchor
passed as --image on every scene. seedream_v4_5, 9:16 face / full-body. POC only."""
import re, subprocess, urllib.request
from pathlib import Path
from PIL import Image

HF = str(Path.home() / "bin" / "hf.exe")
URL_RE = re.compile(r"https://\S+?\.(?:png|jpg|jpeg|webp)", re.IGNORECASE)
HERE = Path(__file__).parent
OUT = HERE / "jesus"
REF = OUT / "JESUS__REF.png"          # existing face portrait (inked)
BODY_REF = OUT / "JESUS__risen__a.png"  # an already-INKED full standing figure -> style anchor
BODY = OUT / "JESUS__BODY.png"        # new full-body reference
GRID = OUT / "JESUS__GRID.png"        # composed face+body anchor

JESUS = ("Jesus of Nazareth, a Jewish man of about thirty, warm olive-brown skin, a calm noble "
         "face, long dark brown hair parted in the middle falling to the shoulders, a full dark "
         "brown beard, deep compassionate brown eyes, strong gentle features")
# HARD style enforcement — the body MUST match the inked face panel, never photoreal.
STYLE = (" Drawn in INKED BIBLICAL GRAPHIC-NOVEL / cinematic manga ILLUSTRATION style, exactly like "
         "the reference portrait: bold clean ink linework, flat cel-shaded comic colour, hand-drawn "
         "2D artwork. NOT a photograph, NOT photorealistic, NOT a real person, no photo texture, no "
         "skin pores, no 3D render. Clean reverent lighting, realistic accurate human proportions, "
         "ancient Near-Eastern period-accurate, mature teen-and-up tone. No text, no lettering, no "
         "panels, no speech bubbles, no watermark, no signature.")
LOCK = (" Keep the exact same inked face, hair and beard and the exact same illustrated art style as "
        "the reference portrait — this is the SAME drawn character, full body.")

BODY_PROMPT = (JESUS + ", full-body INKED comic character model-sheet reference, standing straight and "
               "facing forward in a calm neutral pose, arms relaxed slightly away from the sides, his "
               "WHOLE body from the top of the head down to the bare feet fully visible and "
               "centred, wearing a simple ancient Near-Eastern ankle-length tunic with a mantle, "
               "plain flat neutral grey studio background, even soft light, correct realistic adult "
               "male proportions (about seven-and-a-half heads tall)." + LOCK + STYLE)


def gen(prompt, dest, aspect, ref=None):
    if dest.exists() and dest.stat().st_size > 0:
        print(f"[skip] {dest.name}", flush=True); return True
    args = [HF, "generate", "create", "seedream_v4_5", "--prompt", prompt]
    if ref:
        args += ["--image", str(ref)]
    args += ["--aspect_ratio", aspect, "--wait"]
    for attempt in (1, 2, 3):
        r = subprocess.run(args, capture_output=True, text=True, encoding="utf-8",
                           errors="replace", timeout=600)
        blob = (r.stdout or "") + (r.stderr or "")
        m = URL_RE.search(blob)
        if m:
            req = urllib.request.Request(m.group(0), headers={"User-Agent": "poc/1.0"})
            with urllib.request.urlopen(req, timeout=180) as resp:
                dest.write_bytes(resp.read())
            print(f"[ok  ] {dest.name}", flush=True); return True
        print(f"[{'retry' if attempt<3 else 'FAIL'}] {dest.name} (rc={r.returncode})", flush=True)
    return False


def compose_grid():
    """[ face portrait (square-ish) | full body (tall) ] on a neutral canvas."""
    face = Image.open(REF).convert("RGB")
    body = Image.open(BODY).convert("RGB")
    H = 1600
    bw = int(body.width * H / body.height)
    body = body.resize((bw, H))
    fh = int(H * 0.55)                       # face panel a bit over half height
    fw = int(face.width * fh / face.height)
    face = face.resize((fw, fh))
    pad = 40
    canvas = Image.new("RGB", (fw + bw + pad * 3, H + pad * 2), (235, 235, 235))
    canvas.paste(face, (pad, pad + (H - fh) // 2))
    canvas.paste(body, (fw + pad * 2, pad))
    canvas.save(GRID)
    print(f"[grid] {GRID.name}  {canvas.size}", flush=True)


if __name__ == "__main__":
    assert REF.exists(), "face REF missing"
    assert BODY_REF.exists(), "inked full-figure body-ref missing"
    gen(BODY_PROMPT, BODY, "9:16", ref=BODY_REF)   # full body, INKED-style-locked to an existing inked figure
    assert BODY.exists(), "body ref failed"
    compose_grid()
    print("[done] reference grid ->", GRID, flush=True)
