"""Phase 1B FACE bake-off: 6 looks x 3 face subjects = 18 stills (gpt_image_2, 9:16).
Faces are where AI slop shows + where each look lives or dies.
Reuses the proven HFProvider pattern. Scratchpad only."""
import re, subprocess, urllib.request, sys
from pathlib import Path

HF = str(Path.home() / "bin" / "hf.exe")
MODEL = "gpt_image_2"
ASPECT = "9:16"
URL_RE = re.compile(r"https://\S+?\.(?:png|jpg|jpeg|webp)", re.IGNORECASE)
OUT = Path(__file__).parent / "faces"
OUT.mkdir(parents=True, exist_ok=True)

ANTI_SLOP = ("period-accurate ancient Near East and ancient Egypt, no modern objects, "
             "no plastic AI sheen, no waxy skin, no glitter, no over-saturation, "
             "restrained muted palette, masterful composition, emotionally truthful face")

# The three hardest face tests from EW03 Joseph.
SUBJECTS = {
 "joseph_pit": ("a seventeen-year-old Hebrew shepherd boy, close-up of his dust-streaked "
   "tear-streaked face, wide frightened eyes, raw betrayal and fear, the stone rim of a deep "
   "desert pit and a harsh shaft of noon light above him"),
 "joseph_weep": ("a man about thirty-eight years old dressed as an Egyptian vizier in fine "
   "linen with a broad gold collar, extreme close-up of his face overcome and weeping, tears "
   "on his cheeks, the moment he reveals himself to his brothers, restrained royal dignity"),
 "christ_face": ("a first-century Middle Eastern Jewish man in his early thirties, weathered "
   "olive skin and a short dark beard, close-up of his face, eyes full of compassion and quiet "
   "sorrow, reverent and holy, looking slightly upward, plain undyed robe"),
}

# Six candidate looks, deliberately broad. {key: style prefix}
LOOKS = {
 "R_chiaroscuro": ("Hyperreal cinematic photographic portrait, dramatic single-source "
   "chiaroscuro light from one side, deep black background, tenebrism, realistic detailed skin "
   "with real texture, shot on 85mm, shallow depth of field, fine film grain. Subject: "),
 "B_engraving": ("Gustave Dore antique steel engraving, dense fine cross-hatching, high-contrast "
   "black ink on aged sepia paper, antique illustrated-Bible book plate, masterful linework. Subject: "),
 "D_inknovel": ("Bold modern graphic-novel ink illustration, strong black spotting and dramatic "
   "shadow shapes, limited muted palette with one restrained accent colour, expressive confident "
   "linework, cinematic comic panel in the spirit of Mignola and Sienkiewicz. Subject: "),
 "F_claymation": ("Handcrafted stop-motion claymation character, visible fingerprints and sculpted "
   "clay texture, miniature practical set, tactile macro with shallow depth of field, soft studio "
   "light, in the spirit of Laika and Aardman, charming and reverent never cartoonish. Subject: "),
 "G_charcoal": ("Expressive charcoal and white-chalk drawing on warm toned paper, smudged soft "
   "shadows and bold confident strokes, visible paper grain, hand-made fine-art sketch. Subject: "),
 "W_woodcut": ("Stark German Renaissance woodcut in the style of Albrecht Durer, bold black relief "
   "lines, dramatic high contrast, hand-printed on antique laid paper. Subject: "),
}

def render(name, prompt):
    dest = OUT / f"{name}.png"
    if dest.exists():
        print(f"[skip] {name}", flush=True); return True
    print(f"[gen ] {name} ...", flush=True)
    r = subprocess.run([HF, "generate", "create", MODEL, "--prompt", prompt,
                        "--aspect_ratio", ASPECT, "--wait"],
                       capture_output=True, text=True, encoding="utf-8",
                       errors="replace", timeout=600)
    if r.returncode != 0:
        print(f"[FAIL] {name} rc={r.returncode}\n{(r.stderr or '')[-400:]}", flush=True); return False
    m = URL_RE.search(r.stdout or "")
    if not m:
        print(f"[FAIL] {name} no url\n{(r.stdout or '')[-400:]}", flush=True); return False
    req = urllib.request.Request(m.group(0), headers={"User-Agent": "poc/1.0"})
    with urllib.request.urlopen(req, timeout=180) as resp:
        dest.write_bytes(resp.read())
    print(f"[ok  ] {name} -> {dest}", flush=True); return True

if __name__ == "__main__":
    ok = total = 0
    for lk, prefix in LOOKS.items():
        for sk, subj in SUBJECTS.items():
            total += 1
            name = f"{lk}__{sk}"
            prompt = prefix + subj + ". " + ANTI_SLOP
            try:
                if render(name, prompt): ok += 1
            except Exception as e:
                print(f"[ERR ] {name}: {e}", flush=True)
    print(f"\nDONE {ok}/{total} face stills in {OUT}", flush=True)
