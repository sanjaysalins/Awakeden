"""Pass-2 prep: render ONE new face-locked 'walking' still (the classic i2v
failure case — a striding figure tends to morph). Reference-locked to the
existing seedream_v4_5 REF portrait so it's the same Caleb. Scratchpad/POC only."""
import re, subprocess, urllib.request
from pathlib import Path

HF = str(Path.home() / "bin" / "hf.exe")
URL_RE = re.compile(r"https://\S+?\.(?:png|jpg|jpeg|webp)", re.IGNORECASE)
HERE = Path(__file__).parent
OUT = HERE / "charcon"
REF = OUT / "CC__seedream_v4_5__REF.png"
DEST = OUT / "CC__seedream_v4_5__R_walking.png"

CHAR = ("Caleb, a Hebrew man of about twenty-five, olive skin, a lean angular face, a short "
        "black beard, deep-set dark brown eyes, thick black eyebrows, a thin pale scar through "
        "his left eyebrow, a small gold hoop earring in his left ear, wearing a faded rust-red "
        "headscarf and a coarse undyed linen tunic")
SCENE = (" wide full-figure shot, walking steadily forward along a dusty desert road at dawn, "
         "mid-stride, his rust-red headscarf and linen tunic stirring in the breeze, sandals on "
         "the dry cracked earth, low barren hills and a pale gold sky behind.")
LOCK = (" Keep the exact same face, beard, scar over the left eyebrow and gold earring as the "
        "reference image.")
STYLE = (" Biblical epic graphic novel style, cinematic manga composition, dramatic ink shadows, "
         "sacred reverent atmosphere, realistic proportions, ancient Near-Eastern period-accurate, "
         "mature teen-and-up tone. No text, no lettering, no panels, no speech bubbles, "
         "no watermark, no signature.")

if __name__ == "__main__":
    assert REF.exists(), f"missing REF: {REF}"
    if DEST.exists() and DEST.stat().st_size > 0:
        print(f"[skip] {DEST.name}"); raise SystemExit
    args = [HF, "generate", "create", "seedream_v4_5", "--prompt", CHAR + SCENE + LOCK + STYLE,
            "--image", str(REF), "--aspect_ratio", "9:16", "--wait"]
    for attempt in (1, 2, 3):
        r = subprocess.run(args, capture_output=True, text=True, encoding="utf-8",
                           errors="replace", timeout=600)
        blob = (r.stdout or "") + (r.stderr or "")
        m = URL_RE.search(blob)
        if m:
            req = urllib.request.Request(m.group(0), headers={"User-Agent": "poc/1.0"})
            with urllib.request.urlopen(req, timeout=180) as resp:
                DEST.write_bytes(resp.read())
            print(f"[ok  ] {DEST.name}"); break
        print(f"[{'retry' if attempt<3 else 'FAIL'}] (rc={r.returncode})\n{blob[-260:]}")
