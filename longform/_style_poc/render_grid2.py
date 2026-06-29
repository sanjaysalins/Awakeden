"""Wave 1 — WEBTOON MODEL HUNT. The loved WT flat-webtoon style across every viable
t2i model x 2 subjects (christ_face reverence + joseph_action hands/crowd stress).
Idempotent (skips existing). Writes comic2/. Scratchpad only.
gpt_image_2 (7cr) + ref-only models (flux_kontext/openai_hazel/cinematic_studio_image) excluded."""
import re, subprocess, urllib.request, sys
from pathlib import Path

HF = str(Path.home() / "bin" / "hf.exe")
ASPECT = "9:16"
URL_RE = re.compile(r"https://\S+?\.(?:png|jpg|jpeg|webp)", re.IGNORECASE)
OUT = Path(__file__).parent / "comic2"
OUT.mkdir(parents=True, exist_ok=True)

# all viable pure-text-to-image models (preflighted live), cheap->dear
MODELS = ["soul_cinematic", "text2image_soul_v2", "z_image", "kling_omni_image",
          "ms_image", "flux_2", "grok_image", "nano_banana", "seedream_v4_5",
          "seedream_v5_lite", "recraft_v4_1", "nano_banana_flash", "nano_banana_2",
          "cinematic_studio_2_5"]

TAIL = ("mature reverent dignified gravitas, period-accurate ancient Near East and Egypt, "
        "no modern objects; NOT childish, NOT a cape or superhero comic, NOT a cute mascot, "
        "NOT cool edgy antihero or crime-thriller; emotionally truthful face; the face of "
        "Christ is holy, never a dramatic beat. Full-bleed vertical composition, no panels, "
        "no gutters, no speech bubbles, no text or lettering.")

STYLE = ("Modern digital webtoon / manhwa illustration, clean crisp lineart, soft cel "
         "shading, bold flat color fills, limited harmonious palette, cinematic lighting, "
         "polished comic look. Subject: ")

SUBJECTS = {
 "christ_face": ("a first-century Middle Eastern Jewish man in his early thirties, weathered "
   "olive skin and a short dark beard, close-up of his face, eyes full of compassion and quiet "
   "sorrow, reverent and holy, looking slightly upward, plain undyed robe"),
 "joseph_action": ("a young Hebrew shepherd boy being seized by his older brothers and lowered "
   "into a dry desert pit, several rough robed men gripping his arms, his torn striped coat, "
   "dust and struggle, harsh midday desert light, multiple figures"),
}


def render(model, name, prompt):
    dest = OUT / f"{name}.png"
    if dest.exists() and dest.stat().st_size > 0:
        print(f"[skip] {name}", flush=True); return True
    for attempt in (1, 2):
        try:
            r = subprocess.run([HF, "generate", "create", model, "--prompt", prompt,
                                "--aspect_ratio", ASPECT, "--wait"],
                               capture_output=True, text=True, encoding="utf-8",
                               errors="replace", timeout=600)
        except Exception as e:
            print(f"[ERR ] {name}: {e}", flush=True); continue
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
        for model in MODELS:
            total += 1
            name = f"WT__{model}__{sk}"
            print(f"[gen ] {name} ...", flush=True)
            if render(model, name, STYLE + subj + ". " + TAIL): ok += 1
    print(f"\nDONE {ok}/{total} webtoon model-hunt stills in {OUT}", flush=True)
