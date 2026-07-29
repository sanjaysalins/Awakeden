"""Aaron's locked reference PNG for the retro-comic DNA — punch-list item #2.
The existing `aaron_pc_ref.png` (old painted-comic style) has Greek/Roman fluted
temple columns behind him, an anachronism the project's own audit rubric bans
outright — not reused. Same fixed no-border retro recipe as _hook_splash.py.
  .venv\\Scripts\\python.exe longform/EW01_Two_Goats/_retro_dna/_aaron_ref.py
"""
import re, subprocess, sys, time
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent.parent.parent
sys.path.insert(0, str(ROOT))
import config
from pipeline import cost
HF = str(config.HF_CLI_PATH)
MODEL = "nano_banana_pro"
OUT = Path(__file__).resolve().parent
OUT.mkdir(exist_ok=True)

RETRO = ("Vintage 1960s Silver Age comic book illustration style, bold black ink holding lines, "
         "flat limited four-colour comic colour with NO gradients, clearly visible coarse Ben-Day "
         "halftone dots in the sky and shadows, slight CMYK misregistration, warm cream colour palette")
SUBJ = ("An elderly ancient Hebrew high priest named Aaron: dignified, a long grey beard, grey hair, "
        "deep-set weathered eyes, wearing a simple undyed linen robe, standing before a wilderness "
        "tent tabernacle with woven curtain walls and desert hills behind him, warm dusk light")
TAIL = ("reverent, solemn, ancient Near-Eastern period-accurate, NOT high-priestly vestments, a "
        "full-bleed digital illustration filling the entire canvas edge-to-edge")
AVOID = ("no text, no lettering, no captions, no speech balloons, no watermark, no modern clothing, "
         "no Greek columns, no Roman architecture, no marble temple")


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
    out = OUT / "aaron_retro_ref_v2.png"
    prompt = f"{RETRO}. {SUBJ}. {TAIL} AVOID: {AVOID}"
    print("[img ] aaron_retro_ref (nano_banana_pro, no ref) ...", flush=True); t = time.time()
    if run(prompt, out):
        cost.record_hf("EW01_Two_Goats", "long", "stills", MODEL, note="[aaron-ref] aaron_retro_ref")
        print(f"   ok ({time.time()-t:.0f}s) -> {out}")
    else:
        print("   FAILED")


if __name__ == "__main__":
    main()
