"""IMAGE-TO-VIDEO BAKE-OFF — one seedream_v4_5 still, one motion prompt, every
generative i2v model HF offers (18). 9:16, ~5s. Tests which model animates the
inked graphic-novel still REVERENTLY without morphing the line art, softening to
photoreal, hallucinating elements, or melting the face/mouth.
Idempotent, rate-limit-aware, sequential (dodges the concurrent-jobs limit).
Writes bakeoff_v/ + manifest.json. Scratchpad only."""
import re, json, subprocess, urllib.request
from pathlib import Path

HF = str(Path.home() / "bin" / "hf.exe")
URL_RE = re.compile(r"https://\S+?\.(?:mp4|webm|mov)", re.IGNORECASE)
HERE = Path(__file__).parent
OUT = HERE / "bakeoff_v"
OUT.mkdir(parents=True, exist_ok=True)
SRC = HERE / "charcon" / "CC__seedream_v4_5__R_storm_ridge.png"

PROMPT = ("Cinematic motion: heavy rain falls steadily, his rust-red headscarf and coarse linen "
          "tunic whip and ripple in the storm wind, distant lightning flickers across the dark sky, "
          "a slow steady push-in toward his face. Keep the exact same inked biblical graphic-novel "
          "art style, the same face, beard, scar over the left eyebrow and gold earring. No morphing, "
          "no style change, no photoreal look, no added or removed elements, no text, no captions, "
          "steady natural light, no glitter, no sparkles.")

# model -> extra args (aspect/duration/resolution/mode per `model get`). --image added for all.
MODELS = {
 "seedance1_5":               ["--aspect_ratio","9:16","--duration","4","--resolution","720p"],
 "veo3_1_lite":               ["--aspect_ratio","9:16","--duration","6"],
 "cinematic_studio_video_v2": ["--aspect_ratio","9:16","--duration","5"],
 "grok_video":                ["--aspect_ratio","9:16","--duration","5"],
 "kling3_0_turbo":            ["--aspect_ratio","9:16","--duration","5","--resolution","720p"],
 "wan2_7":                    ["--aspect_ratio","9:16","--duration","5","--resolution","720p"],
 "cinematic_studio_video":    ["--aspect_ratio","9:16","--duration","5"],
 "kling2_6":                  ["--aspect_ratio","9:16","--duration","5"],
 "kling3_0":                  ["--aspect_ratio","9:16","--duration","5","--mode","pro"],
 "seedance_2_0_mini":         ["--aspect_ratio","9:16","--duration","5","--resolution","720p"],
 "wan2_6":                    ["--aspect_ratio","9:16","--duration","5","--quality","720p"],
 "veo3_1":                    ["--aspect_ratio","9:16","--duration","6"],
 "veo3":                      ["--aspect_ratio","9:16"],
 "grok_video_v15":            ["--duration","5","--resolution","720p"],
 "seedance_2_0":              ["--aspect_ratio","9:16","--duration","5","--resolution","720p"],
 "cinematic_studio_3_0":      ["--aspect_ratio","9:16","--duration","5"],
 "cinematic_studio_video_3_5":["--aspect_ratio","9:16","--duration","5"],
 "minimax_hailuo":            ["--duration","6","--resolution","768"],
}


def render(model, extra):
    dest = OUT / f"V__{model}.mp4"
    if dest.exists() and dest.stat().st_size > 0:
        print(f"[skip] {model}", flush=True); return "skip"
    args = [HF, "generate", "create", model, "--prompt", PROMPT, *extra,
            "--image", str(SRC), "--wait", "--wait-timeout", "20m"]
    for attempt in (1, 2, 3):
        try:
            r = subprocess.run(args, capture_output=True, text=True, encoding="utf-8",
                               errors="replace", timeout=1500)
        except Exception as e:
            print(f"[ERR ] {model}: {e}", flush=True); continue
        blob = (r.stdout or "") + (r.stderr or "")
        m = URL_RE.search(blob)
        if m:
            req = urllib.request.Request(m.group(0), headers={"User-Agent": "poc/1.0"})
            with urllib.request.urlopen(req, timeout=300) as resp:
                dest.write_bytes(resp.read())
            print(f"[ok  ] {model} -> {dest.name}", flush=True); return "ok"
        low = blob.lower()
        transient = ("concurrent_jobs_limit" in low or "rate_limit" in low or "timeout" in low)
        tag = "retry" if (attempt < 3 and transient) else "FAIL"
        print(f"[{tag}] {model} (rc={r.returncode})\n    {blob[-300:].strip()}", flush=True)
        if not transient:
            return "fail"
    return "fail"


if __name__ == "__main__":
    results = {}
    for model, extra in MODELS.items():
        print(f"\n[gen ] {model} ...", flush=True)
        results[model] = render(model, extra)
    (OUT / "manifest.json").write_text(json.dumps(results, indent=2))
    done = sum(1 for v in results.values() if v in ("ok", "skip"))
    print(f"\nDONE {done}/{len(MODELS)} clips in {OUT}\n{json.dumps(results, indent=2)}", flush=True)
