"""Phase 1C: stylized 'teen+ reach' stills bake-off (5 looks x 2 subjects = 10).
Tests the popular animation style-families the LLMs recommended, using DESCRIPTIVE
strings (no studio/IP names, which drift). Writes into faces/ so the existing
gallery picks them up. gpt_image_2, 9:16. Idempotent. Scratchpad only.
See PLAN_styles2.md."""
import re, subprocess, urllib.request
from pathlib import Path

HF = str(Path.home() / "bin" / "hf.exe")
MODEL = "gpt_image_2"
ASPECT = "9:16"
URL_RE = re.compile(r"https://\S+?\.(?:png|jpg|jpeg|webp)", re.IGNORECASE)
OUT = Path(__file__).parent / "faces"
OUT.mkdir(parents=True, exist_ok=True)

TAIL = ("mature reverent dignified tone, period-accurate ancient Near East and Egypt, "
        "no modern objects; NOT childish, NOT a cute mascot, NOT preschool cartoon, "
        "no plastic toy sheen, no goofy expression, emotionally truthful face")

# decisive 2 of the 3 subjects (same wording as render_faces.py for comparability)
SUBJECTS = {
 "joseph_pit": ("a seventeen-year-old Hebrew shepherd boy, close-up of his dust-streaked "
   "tear-streaked face, wide frightened eyes, raw betrayal and fear, the stone rim of a deep "
   "desert pit and a harsh shaft of noon light above him"),
 "christ_face": ("a first-century Middle Eastern Jewish man in his early thirties, weathered "
   "olive skin and a short dark beard, close-up of his face, eyes full of compassion and quiet "
   "sorrow, reverent and holy, looking slightly upward, plain undyed robe"),
}

LOOKS = {
 "S_comic3d": ("Stylized 3D comic-book animation, bold black ink outlines, halftone dot "
   "shading, subtle chromatic-aberration offset, graphic flat color blocks, dynamic "
   "cinematic comic framing, non-photoreal CGI. Subject: "),
 "A_painterly25d": ("Painterly 2.5D animated-series style, visible textured brushwork over "
   "sculpted 3D forms, rich hand-painted surfaces, dramatic volumetric side light, gritty "
   "cinematic fantasy-drama mood. Subject: "),
 "P_painterly3d": ("Painterly stylized 3D animated film still, soft hand-painted textures and "
   "visible brush strokes, expressive stylized features, warm cinematic lighting, storybook "
   "depth, never plastic-smooth. Subject: "),
 "N_anime": ("Modern high-quality 2D cinematic anime film still, clean sharp character art, "
   "dramatic cinematic lighting, detailed painted background, fluid expressive face, serious "
   "mature tone. Subject: "),
 "C_folkart": ("Hand-drawn 2D folk-art animation, flat geometric stylization, decorative "
   "medieval-illumination patterning, muted earthy palette, reverent storybook composition. "
   "Subject: "),
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
            try:
                if render(name, prefix + subj + ". " + TAIL): ok += 1
            except Exception as e:
                print(f"[ERR ] {name}: {e}", flush=True)
    print(f"\nDONE {ok}/{total} stylized stills in {OUT}  (~{ok*7:.0f} cr)", flush=True)
