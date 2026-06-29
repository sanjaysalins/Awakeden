"""i2v BAKE-OFF PASS 2 — stress test. The 3 user-chosen Pass-1 finalists animate
the HARDEST stills (multi-figure crowd, firelight, low-light held object, quiet
close-up, walking locomotion) to see which survives consistency across DIFFERENT
images + hard motion. Tailored motion verb per still + verbatim style-lock tail.
Sequential, idempotent, rate-limit-aware. Writes bakeoff_v2/. POC/scratchpad only."""
import re, json, subprocess, urllib.request
from pathlib import Path

HF = str(Path.home() / "bin" / "hf.exe")
URL_RE = re.compile(r"https://\S+?\.(?:mp4|webm|mov)", re.IGNORECASE)
HERE = Path(__file__).parent
SRCDIR = HERE / "charcon"
OUT = HERE / "bakeoff_v2"
OUT.mkdir(parents=True, exist_ok=True)

TAIL = (" Keep the exact same inked biblical graphic-novel art style, the same face, beard, scar "
        "over the left eyebrow and gold earring. No morphing, no style change, no photoreal look, "
        "no added or removed elements, no text, no captions, steady natural light, no glitter, "
        "no sparkles.")

# still slug -> tailored motion verb (the R_ reference-locked seedream_v4_5 stills)
STILLS = {
    "crowd_market": "Cinematic motion: the marketplace crowd shifts and murmurs, robes and hanging "
                    "cloth sway, dust drifts in the air, a slow steady push-in on his anxious face.",
    "night_fire":   "Cinematic motion: the campfire flickers and casts dancing warm light across his "
                    "face, faint embers drift upward, he breathes slowly, the dark night still around him.",
    "lamp_room":    "Cinematic motion: the single oil-lamp flame flickers, faint shadows shift across "
                    "the stone wall, he breathes slowly and thoughtfully, the clay cup held steady.",
    "noon_close":   "Cinematic motion: subtle breathing, his eyes shift slightly, sweat glistens on his "
                    "brow, faint heat-haze shimmer in the blazing air, a very slow micro push-in.",
    "walking":      "Cinematic motion: he walks steadily forward along the dusty desert road, his robe "
                    "and headscarf swaying with each stride, dust stirring underfoot, the camera tracking with him.",
}

# model -> extra args (per `model get` / cost preflight). --image + --prompt added per call.
MODELS = {
    "seedance1_5":               ["--aspect_ratio", "9:16", "--duration", "4", "--resolution", "720p"],
    "cinematic_studio_video_v2": ["--aspect_ratio", "9:16", "--duration", "5"],
    "minimax_hailuo":            ["--duration", "6"],  # NO --aspect_ratio, NO --resolution (it 400s)
}


def render(model, extra, slug, prompt, src):
    dest = OUT / f"V__{model}__{slug}.mp4"
    if dest.exists() and dest.stat().st_size > 0:
        print(f"[skip] {model} {slug}", flush=True); return "skip"
    args = [HF, "generate", "create", model, "--prompt", prompt, *extra,
            "--image", str(src), "--wait", "--wait-timeout", "20m"]
    for attempt in (1, 2, 3):
        try:
            r = subprocess.run(args, capture_output=True, text=True, encoding="utf-8",
                               errors="replace", timeout=1500)
        except Exception as e:
            print(f"[ERR ] {model} {slug}: {e}", flush=True); continue
        blob = (r.stdout or "") + (r.stderr or "")
        m = URL_RE.search(blob)
        if m:
            req = urllib.request.Request(m.group(0), headers={"User-Agent": "poc/1.0"})
            with urllib.request.urlopen(req, timeout=300) as resp:
                dest.write_bytes(resp.read())
            print(f"[ok  ] {model} {slug} -> {dest.name}", flush=True); return "ok"
        low = blob.lower()
        transient = ("concurrent_jobs_limit" in low or "rate_limit" in low or "timeout" in low)
        tag = "retry" if (attempt < 3 and transient) else "FAIL"
        print(f"[{tag}] {model} {slug} (rc={r.returncode})\n    {blob[-300:].strip()}", flush=True)
        if not transient:
            return "fail"
    return "fail"


if __name__ == "__main__":
    results = {}
    for slug, verb in STILLS.items():
        src = SRCDIR / f"CC__seedream_v4_5__R_{slug}.png"
        if not (src.exists() and src.stat().st_size > 0):
            print(f"[MISS] still not found: {src.name}", flush=True)
            continue
        prompt = verb + TAIL
        for model, extra in MODELS.items():
            print(f"\n[gen ] {model} <- {slug} ...", flush=True)
            results[f"{model}__{slug}"] = render(model, extra, slug, prompt, src)
    (OUT / "manifest.json").write_text(json.dumps(results, indent=2))
    done = sum(1 for v in results.values() if v in ("ok", "skip"))
    print(f"\nDONE {done}/{len(results)} clips in {OUT}\n{json.dumps(results, indent=2)}", flush=True)
