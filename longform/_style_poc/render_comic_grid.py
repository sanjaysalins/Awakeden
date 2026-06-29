"""Phase A — comic style x model grid (per PLAN_comic_v2.md).
4 styles x 3 cheap stylization models x 3 subjects = 36 stills.
Models all ~1cr (seedream/flux 1, recraft 1.25). gpt_image (7cr) deliberately NOT used here.
Descriptive style strings only (no IP tokens). Full-bleed 9:16, no panels/lettering.
Idempotent (skips existing). Writes comic/. Scratchpad only."""
import re, subprocess, urllib.request
from pathlib import Path

HF = str(Path.home() / "bin" / "hf.exe")
ASPECT = "9:16"
URL_RE = re.compile(r"https://\S+?\.(?:png|jpg|jpeg|webp)", re.IGNORECASE)
OUT = Path(__file__).parent / "comic"
OUT.mkdir(parents=True, exist_ok=True)

MODELS = ["seedream_v4_5", "flux_2", "recraft_v4_1"]

TAIL = ("mature reverent dignified gravitas, period-accurate ancient Near East and Egypt, "
        "no modern objects; NOT childish, NOT a cape or superhero comic, NOT a cute mascot, "
        "NOT cool edgy antihero or crime-thriller; emotionally truthful face; the face of "
        "Christ is holy, never a dramatic beat. Full-bleed vertical composition, no panels, "
        "no gutters, no speech bubbles, no text or lettering.")

STYLES = {
 "MI_brushink": ("Mature seinen manga illustration, expressive sumi brush-ink linework with "
   "dynamic hatching and grey screentone, dramatic ink-wash shadows, historical and meditative, "
   "monochrome with restrained tone. Subject: "),
 "WT_webtoon": ("Modern digital webtoon / manhwa illustration, clean crisp lineart, soft cel "
   "shading, bold flat color fills, limited harmonious palette, cinematic lighting, polished "
   "comic look. Subject: "),
 "NR_noir": ("High-contrast noir graphic-novel ink, heavy black spot-blacks and stark "
   "chiaroscuro, bold brush inking, a single warm golden accent color amid near-monochrome, "
   "dramatic tenebrism. Subject: "),
 "PG_painted": ("Fully painted graphic-novel realism, rich oil-painted rendering, dramatic "
   "cinematic lighting, heroic painterly comic-book illustration, detailed brushwork. Subject: "),
}

SUBJECTS = {
 "christ_face": ("a first-century Middle Eastern Jewish man in his early thirties, weathered "
   "olive skin and a short dark beard, close-up of his face, eyes full of compassion and quiet "
   "sorrow, reverent and holy, looking slightly upward, plain undyed robe"),
 "joseph_pit": ("a young Hebrew shepherd boy about seventeen, close-up of his dust-streaked "
   "tear-streaked face, wide frightened eyes, raw betrayal and fear, the stone rim of a deep "
   "desert pit and a harsh shaft of noon light above him"),
 "joseph_action": ("a young Hebrew shepherd boy being seized by his older brothers and lowered "
   "into a dry desert pit, several rough robed men gripping his arms, his torn striped coat, "
   "dust and struggle, harsh midday desert light, multiple figures"),
}


def render(model, name, prompt):
    dest = OUT / f"{name}.png"
    if dest.exists() and dest.stat().st_size > 0:
        print(f"[skip] {name}", flush=True); return True
    for attempt in (1, 2):
        r = subprocess.run([HF, "generate", "create", model, "--prompt", prompt,
                            "--aspect_ratio", ASPECT, "--wait"],
                           capture_output=True, text=True, encoding="utf-8",
                           errors="replace", timeout=600)
        blob = (r.stdout or "") + (r.stderr or "")
        m = URL_RE.search(blob)
        if m:
            req = urllib.request.Request(m.group(0), headers={"User-Agent": "poc/1.0"})
            with urllib.request.urlopen(req, timeout=180) as resp:
                dest.write_bytes(resp.read())
            print(f"[ok  ] {name} -> {dest}", flush=True); return True
        print(f"[{'retry' if attempt==1 else 'FAIL'}] {name} (rc={r.returncode})"
              f"{'' if attempt==1 else chr(10)+blob[-300:]}", flush=True)
    return False


if __name__ == "__main__":
    ok = total = 0
    for sk, subj in SUBJECTS.items():
        for st, prefix in STYLES.items():
            for model in MODELS:
                total += 1
                name = f"{st}__{model}__{sk}"
                print(f"[gen ] {name} ...", flush=True)
                try:
                    if render(model, name, prefix + subj + ". " + TAIL): ok += 1
                except Exception as e:
                    print(f"[ERR ] {name}: {e}", flush=True)
    print(f"\nDONE {ok}/{total} comic-grid stills in {OUT}", flush=True)
