"""One new hero-splash still for the DnaSplashHook title card: Aaron and the two
goats (Day of Atonement, Lev 16), gold glory light breaking through — replaces the
title card's reuse of the "welcome" clip. Same locked recipe as _seedream_ref.py.
  .venv\\Scripts\\python.exe longform/EW01_Two_Goats/_retro_dna/_hook_splash.py
"""
import re, subprocess, sys, time
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent.parent.parent
sys.path.insert(0, str(ROOT))
import config
from pipeline import cost
HF = str(config.HF_CLI_PATH)
MODEL = "seedream_v4_5"
OUT = Path(__file__).resolve().parent
OUT.mkdir(exist_ok=True)

# FIXED 2026-07-23: "printed on aged cream newsprint" + "low-fi retro print texture" made
# nano_banana_pro render a physical PAGE (black border + cream margin) instead of just applying
# the style — confirmed reproducible (this splash + a render_scene() smoke test both showed it).
# Positive full-bleed phrasing instead (matches [[seedream-no-negative-channel]]: describe the
# desired end-state, don't rely on "no panel borders" to suppress a concrete drawable object).
RETRO = ("Vintage 1960s Silver Age comic book illustration style, bold black ink holding lines, "
         "flat limited four-colour comic colour with NO gradients, clearly visible coarse Ben-Day "
         "halftone dots in the sky and shadows, slight CMYK misregistration, warm cream colour palette")
SUBJ = ("An ancient Hebrew high priest (Aaron) in a simple undyed linen robe laying both hands on the "
        "head of a goat resting calmly on a wilderness altar draped in plain unmarked pale cloth, a "
        "golden shaft of glory light breaking through dark clouds above him; in the background a second "
        "goat is led away into the wilderness by an attendant, receding toward the horizon; wide "
        "composition, dramatic sky, ancient Near-Eastern desert tabernacle setting")
TAIL = ("reverent, solemn, ancient Near-Eastern period-accurate, the goat calm, docile and completely "
        "unharmed, a full-bleed digital illustration filling the entire canvas edge-to-edge")
AVOID = "no text, no lettering, no captions, no speech balloons, no watermark, no modern clothing, no heroic musculature"


def run(prompt, out):
    cmd = [HF, "generate", "create", MODEL, "--prompt", prompt, "--aspect_ratio", "16:9", "--wait"]
    p = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    blob = (p.stdout or "") + "\n" + (p.stderr or "")
    urls = re.findall(r'https?://\S+?\.(?:png|jpg|jpeg|webp)', blob) or re.findall(r'https?://\S+', blob)
    if not urls:
        print(f"   no url: {blob.strip()[-300:]}"); return False
    subprocess.run(["curl", "-s", "-L", urls[-1], "-o", str(out)], check=True)
    return out.exists() and out.stat().st_size > 1000


def main():
    out = OUT / "two_goats_splash_v2.png"
    prompt = f"{RETRO}. {SUBJ}. {TAIL} AVOID: {AVOID}"
    print("[img ] two_goats_splash (seedream, no ref) ...", flush=True); t = time.time()
    if run(prompt, out):
        cost.record_hf("EW01_Two_Goats", "long", "stills", MODEL, note="[hook-splash] two_goats_splash")
        print(f"   ok ({time.time()-t:.0f}s) -> {out}")
    else:
        print("   FAILED")


if __name__ == "__main__":
    main()
