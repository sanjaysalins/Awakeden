"""Animate the 3 NEW gospel-landing stills (i2v) — same house model + frozen-tableau
discipline as animate_ew04.py: the WORLD breathes, the camera pushes in slowly, the
figures stay still, no morph/photoreal/glitter. cinematic_studio_video_v2, 9:16, 5s."""
import re, json, subprocess, urllib.request
from pathlib import Path

HF = str(Path.home() / "bin" / "hf.exe")
URL_RE = re.compile(r"https://\S+?\.(?:mp4|webm|mov)", re.IGNORECASE)
HERE = Path(__file__).parent
SRC = HERE / "stills"
OUT = HERE / "anim"
OUT.mkdir(parents=True, exist_ok=True)
MODEL = "cinematic_studio_video_v2"
EXTRA = ["--aspect_ratio", "9:16", "--duration", "5"]

TAIL = (" Keep the exact same inked biblical graphic-novel art style, the exact same face and "
        "identity, the same clothing and composition. No morphing, no style change, no photoreal "
        "look, no added or removed figures or objects, no text, no captions, steady reverent light, "
        "no glitter, no sparkles.")

SCENES = {
 "06_cross_lifted":
   ("Cinematic motion: the dark night clouds drift slowly across the wide sky behind the cross, the "
    "warm low light glows and shifts softly, a faint ember or dust rises; Jesus stays completely still "
    "with head gently bowed, the rough wooden cross stays planted and perfectly upright; a slow reverent "
    "push-in with a faint upward tilt. The cross does NOT tilt or sway, no figures move."),

 "07_risen_christ":
   ("Cinematic motion: the warm holy light blooms and breathes softly around the risen Christ, his "
    "clean linen robe stirs very gently, he breathes calmly with a serene living face and steady lifted "
    "eyes, his open hand stays raised in invitation; a slow reverent push-in. Steady glow, no flicker, "
    "no sparkle, the figure stays still and does not step or turn."),

 "08_bitten_multitude":
   ("Cinematic motion: the low campfires flicker and throw shifting light, thin smoke and fine dust "
    "drift across the darkening camp, the scattered stricken crowd stirs faintly as they hold their "
    "eyes and hands lifted upward; a slow tender push-in. The people stay weak and still, only the fire, "
    "smoke and light move."),
}


def render(slug, prompt, src):
    dest = OUT / f"EW04__{slug}.mp4"
    if dest.exists() and dest.stat().st_size > 0:
        print(f"[skip] {slug}", flush=True); return "skip"
    args = [HF, "generate", "create", MODEL, "--prompt", prompt, *EXTRA,
            "--image", str(src), "--wait", "--wait-timeout", "20m"]
    for attempt in (1, 2, 3):
        try:
            r = subprocess.run(args, capture_output=True, text=True, encoding="utf-8",
                               errors="replace", timeout=1500)
        except Exception as e:
            print(f"[ERR ] {slug}: {e}", flush=True); continue
        blob = (r.stdout or "") + (r.stderr or "")
        m = URL_RE.search(blob)
        if m:
            req = urllib.request.Request(m.group(0), headers={"User-Agent": "poc/1.0"})
            with urllib.request.urlopen(req, timeout=300) as resp:
                dest.write_bytes(resp.read())
            print(f"[ok  ] {slug} -> {dest.name}", flush=True); return "ok"
        low = blob.lower()
        transient = ("concurrent_jobs_limit" in low or "rate_limit" in low or "timeout" in low)
        tag = "retry" if (attempt < 3 and transient) else "FAIL"
        print(f"[{tag}] {slug} (rc={r.returncode})\n    {blob[-300:].strip()}", flush=True)
        if not transient:
            return "fail"
    return "fail"


if __name__ == "__main__":
    results = {}
    for slug, motion in SCENES.items():
        src = SRC / f"{slug}.png"
        if not (src.exists() and src.stat().st_size > 0):
            print(f"[MISS] still not found: {src.name}", flush=True); continue
        print(f"\n[gen ] {slug} ...", flush=True)
        results[slug] = render(slug, motion + TAIL, src)
    print(f"\nDONE — landing clips in {OUT}\n{json.dumps(results, indent=2)}", flush=True)
