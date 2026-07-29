"""Captionless re-test (2026-07-25): the earlier bake-off disqualified
Seedance 2.0 Mini specifically for garbled caption text. If baked captions
move to post (per the native-panel-captions-minimal decision), that failure
mode is moot. This generates a fresh David & Goliath page with the SAME
template/character anchors but ZERO caption boxes, then animates it with
both Seedance 2.0 Mini and Kling 3.0 (as a control, since Kling was the
earlier top pick) to see if Mini is genuinely competitive once text is out
of the picture.

  .venv\\Scripts\\python.exe poc_thief_e2e/_test_captionless_bakeoff.py
"""
import re, subprocess, sys, time
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
import config
from pipeline import cost
HF = str(config.HF_CLI_PATH)
MODEL_IMG = "nano_banana_pro"
HERE = Path(__file__).resolve().parent
OUT_STILL = HERE / "stills" / "_comic_strip_template_test"
OUT_CLIP = HERE / "clips" / "_bakeoff_i2v"
OUT_CLIP.mkdir(parents=True, exist_ok=True)

PROMPT_IMG = (
    "A 9:16 vertical comic book page containing a structured 4-panel grid layout. The overall "
    "piece is rendered in a vintage graphic novel illustration style characterized by heavy "
    "black ink linework, high-contrast chiaroscuro shadows, cross-hatching, and a desaturated, "
    "muted earth-tone color palette (dominant slate grays, deep ochre, raw umber, and muted "
    "blues). The paper has a subtle aged, textured vintage comic print finish with crisp panel "
    "borders and dark gutters separating each section.\n\n"
    "GLOBAL TEXTUAL CONSTRAINT: NO text of any kind anywhere on the page -- no speech bubbles, "
    "no caption boxes, no lettering, no words. The page is pure artwork only.\n\n"
    "CORE CHARACTER DESIGN ANCHORS (To maintain visual continuity):\n"
    "- Primary Figure: David, a young Israelite shepherd, small and slight build next to his "
    "opponent, dark curly hair, no armor, wearing a simple brown shepherd's tunic, a leather "
    "sling coiled in one hand, a shepherd's staff on his back.\n"
    "- Secondary Figure: Goliath, a towering Philistine champion, heavily muscled, bronze scale "
    "armor and a bronze helmet, a long dark beard, a massive bronze spear.\n"
    "- Environmental Setting: The valley of Elah, dry rocky terrain with a shallow brook cutting "
    "through it, two armies on opposing ridges, an overcast, tense sky.\n\n"
    "PANEL BREAKDOWN & SPATIAL COMPOSITION:\n\n"
    "PANEL 1 (Top Section - Full Width, Landscape Aspect):\n"
    "- Scene Type: Wide establishing shot.\n"
    "- Composition: Wide view of the valley of Elah from above. The Israelite army lines one "
    "ridge, the Philistine army the other. Goliath stands alone in the gap between them, spear "
    "raised, dwarfing the soldiers around him. David is a small figure just descending the "
    "Israelite side, sling in hand.\n"
    "- Lighting: Atmospheric, overcast, high contrast with a single shaft of light on the valley "
    "floor.\n\n"
    "PANEL 2 (Middle Left - Vertical Portrait Box):\n"
    "- Scene Type: Intense close-up shot.\n"
    "- Composition: Extreme close-up on Goliath's face, sneering down at the camera, bronze "
    "helmet framing a scarred, contemptuous expression, spear point visible at the frame's "
    "edge.\n"
    "- Lighting: Deep side-shadows (chiaroscuro) emphasizing his scale and menace.\n\n"
    "PANEL 3 (Middle Right - Vertical Portrait Box):\n"
    "- Scene Type: Medium close-up reaction shot.\n"
    "- Composition: Medium close-up on David's face, looking up and across toward Goliath, "
    "expression calm and resolute, not afraid, a stone already set in his lowered sling.\n"
    "- Lighting: Soft, single directional highlight on his face against a dark background.\n\n"
    "PANEL 4 (Bottom Section - Full Width, Panoramic Aspect):\n"
    "- Scene Type: Climactic wide/medium shot.\n"
    "- Composition: Wide shot of the valley floor the instant after the sling's release: Goliath "
    "staggering backward off-balance, his shield arm dropping, dust kicked up around his feet, "
    "David in the foreground still in his follow-through stance. No blood or graphic wound "
    "visible.\n"
    "- Lighting: Dramatic light shift, a shaft of light breaking through the clouds onto David.\n\n"
    "EXPLICIT STYLE CONSTRAINTS: Vintage comic book art, heavy black ink hatching, muted earth "
    "tones, sharp black panel borders, dark gutters, high structural consistency, absolutely no "
    "text or lettering anywhere."
)

ANIM_PROMPT = (
    "Animate this comic book page. Bring all four panels to life with subtle, natural motion "
    "in each one, while keeping every character exactly as drawn."
)


def run_img(prompt, out):
    cmd = [HF, "generate", "create", MODEL_IMG, "--prompt", prompt, "--aspect_ratio", "9:16",
           "--resolution", "2k", "--wait"]
    p = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    blob = (p.stdout or "") + "\n" + (p.stderr or "")
    if re.search(r"nsfw", blob, re.IGNORECASE):
        print("   NSFW-REJECTED"); return False
    urls = re.findall(r'https?://\S+?\.(?:png|jpg|jpeg|webp)', blob) or re.findall(r'https?://\S+', blob)
    if not urls:
        print(f"   no url: {blob.strip()[-300:]}"); return False
    subprocess.run(["curl", "-s", "-L", urls[-1], "-o", str(out)], check=True)
    return out.exists() and out.stat().st_size > 1000


def run_clip(model, src, prompt, out, extra):
    cmd = [HF, "generate", "create", model, "--start-image", str(src), "--prompt", prompt,
           "--wait"] + extra
    r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    blob = (r.stdout or "") + "\n" + (r.stderr or "")
    if re.search(r"nsfw", blob, re.IGNORECASE):
        print("   NSFW-REJECTED"); return False
    m = re.search(r'https?://\S+?\.mp4', blob)
    if not m:
        print(f"   no mp4 url: {blob.strip()[-300:]}"); return False
    subprocess.run(["curl", "-s", "-L", m.group(0), "-o", str(out)], check=True)
    return out.exists() and out.stat().st_size > 0


def main():
    still = OUT_STILL / "david_goliath_nocaption.png"
    print("[img ] david_goliath_nocaption ...", flush=True)
    t = time.time()
    if run_img(PROMPT_IMG, still):
        cost.record_hf("EW_Thief_POC", "short", "stills", MODEL_IMG, note="[captionless-test] david_goliath_nocaption")
        print(f"   ok ({time.time()-t:.0f}s)")
    else:
        print("   FAILED"); return

    jobs = [
        ("seedance_2_0_mini", ["--duration", "5", "--aspect_ratio", "9:16"]),
        ("kling3_0", ["--mode", "pro", "--sound", "off", "--duration", "5", "--aspect_ratio", "9:16"]),
    ]
    for model, extra in jobs:
        out = OUT_CLIP / f"{model}_nocaption.mp4"
        print(f"[clip] {model} nocaption -> {out.name} ...", flush=True)
        t = time.time()
        if run_clip(model, still, ANIM_PROMPT, out, extra):
            try:
                cost.record_hf("EW_Thief_POC", "short", "animate", model, note="[captionless-test]")
            except Exception as e:
                print(f"   (ledger record skipped: {e})")
            print(f"   ok ({time.time()-t:.0f}s)")
        else:
            print("   FAILED")
    print(f"\n[out] {OUT_CLIP}")


if __name__ == "__main__":
    main()
