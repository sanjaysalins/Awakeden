"""CONSISTENCY + COST bake-off. Two prompts (same Moses, same style, different beat)
across every HF generative text-to-image model. For each model: $0 cost preflight ->
record per-still cost, then render both prompts. Idempotent, rate-limit-aware.
Writes moses/ + costs.json. Scratchpad only."""
import re, json, subprocess, urllib.request
from pathlib import Path

HF = str(Path.home() / "bin" / "hf.exe")
ASPECT = "9:16"
URL_RE = re.compile(r"https://\S+?\.(?:png|jpg|jpeg|webp)", re.IGNORECASE)
HERE = Path(__file__).parent
OUT = HERE / "moses"
OUT.mkdir(parents=True, exist_ok=True)

# every generative text-to-image model HF offers (utility/upscale/bg/ref-only excluded)
MODELS = ["soul_cinematic", "text2image_soul_v2", "z_image", "kling_omni_image",
          "ms_image", "flux_2", "grok_image", "nano_banana", "seedream_v4_5",
          "seedream_v5_lite", "recraft_v4_1", "nano_banana_flash", "nano_banana_2",
          "cinematic_studio_2_5", "gpt_image_2"]

# locked character so consistency (style AND person) is testable across both prompts
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


def cost(model, prompt):
    try:
        r = subprocess.run([HF, "generate", "cost", model, "--prompt", prompt,
                            "--aspect_ratio", ASPECT, "--json"],
                           capture_output=True, text=True, encoding="utf-8",
                           errors="replace", timeout=120)
        blob = (r.stdout or "") + (r.stderr or "")
        mt = re.search(r'"(?:cost|credits|price|total)"\s*:\s*([0-9.]+)', blob)
        if mt:
            return float(mt.group(1))
        mt = re.search(r'([0-9]+\.?[0-9]*)\s*credit', blob, re.I)
        return float(mt.group(1)) if mt else None
    except Exception as e:
        print(f"[cost ERR] {model}: {e}", flush=True); return None


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
              f"{'' if attempt==1 else chr(10)+blob[-260:]}", flush=True)
    return False


if __name__ == "__main__":
    costs = {}
    cfile = HERE / "costs.json"
    if cfile.exists():
        costs = json.loads(cfile.read_text())
    print("=== COST PREFLIGHT ($0) ===", flush=True)
    for model in MODELS:
        if model not in costs:
            costs[model] = cost(model, PROMPTS["A_bush"])
        print(f"  {model:24s} {costs[model]}", flush=True)
    cfile.write_text(json.dumps(costs, indent=2))

    print("\n=== RENDER ===", flush=True)
    ok = total = 0
    for model in MODELS:
        for pk, prompt in PROMPTS.items():
            total += 1
            name = f"MS__{model}__{pk}"
            print(f"[gen ] {name} ...", flush=True)
            if render(model, name, prompt):
                ok += 1
    print(f"\nDONE {ok}/{total} consistency stills in {OUT}", flush=True)
