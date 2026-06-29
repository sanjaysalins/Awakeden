"""EXHAUSTIVE FILL — render the remaining generative text-to-image models we hadn't
tested, same two Moses prompts (same man, same style, two beats). Writes into moses/
so the combined gallery picks them up. Idempotent, rate-limit-aware. Scratchpad only."""
import re, subprocess, urllib.request
from pathlib import Path

HF = str(Path.home() / "bin" / "hf.exe")
URL_RE = re.compile(r"https://\S+?\.(?:png|jpg|jpeg|webp)", re.IGNORECASE)
HERE = Path(__file__).parent
OUT = HERE / "moses"
OUT.mkdir(parents=True, exist_ok=True)

# remaining generative t2i models -> aspect (hazel only allows 2:3; rest take 9:16)
MODELS = {
    "soul_cast": "9:16",
    "cinematic_studio_soul_cast": "9:16",
    "soul_cinema_studio": "9:16",
    "soul_location": "9:16",
    "cinematic_studio_soul_location": "9:16",
    "flux_kontext": "9:16",
    "openai_hazel": "2:3",
}

CHAR = ("Moses, an old Hebrew prophet with a long flowing grey beard, deeply weathered "
        "sun-darkened face, intense piercing eyes, wearing a coarse undyed wool robe and a "
        "rough brown mantle, holding a gnarled wooden shepherd's staff")
STYLE = (" biblical epic graphic novel style, cinematic manga composition, sacred supernatural "
         "light, ancient desert landscape, weathered robes, dramatic ink shadows, reverent "
         "atmosphere, realistic proportions, mature teen-and-up tone. Full-bleed vertical, "
         "no panels, no gutters, no speech bubbles, no text, no lettering, no watermark, no signature.")
PROMPTS = {
 "A_bush": (CHAR + " standing before the burning bush in the wilderness at night, the bush "
   "ablaze with sacred supernatural fire and light, he lifts one hand to shield his eyes and "
   "removes a sandal, awe and holy fear on his face." + STYLE),
 "B_staff": (CHAR + " standing on a rocky desert ridge at dawn, raising his wooden staff high "
   "over a vast wilderness, storm clouds parting and sacred light breaking behind him, his "
   "mantle whipping in the wind, resolute." + STYLE),
}


def render(model, name, prompt, aspect):
    dest = OUT / f"{name}.png"
    if dest.exists() and dest.stat().st_size > 0:
        print(f"[skip] {name}", flush=True); return True
    for attempt in (1, 2, 3):
        try:
            r = subprocess.run([HF, "generate", "create", model, "--prompt", prompt,
                                "--aspect_ratio", aspect, "--wait"],
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
            print(f"[ok  ] {name}", flush=True); return True
        print(f"[{'retry' if attempt<3 else 'FAIL'}] {name} (rc={r.returncode})"
              f"{'' if attempt<3 else chr(10)+blob[-260:]}", flush=True)
    return False


if __name__ == "__main__":
    ok = total = 0
    for model, aspect in MODELS.items():
        for pk, prompt in PROMPTS.items():
            total += 1
            name = f"MS__{model}__{pk}"
            print(f"[gen ] {name} ...", flush=True)
            if render(model, name, prompt, aspect):
                ok += 1
    print(f"\nDONE {ok}/{total} fill stills in {OUT}", flush=True)
