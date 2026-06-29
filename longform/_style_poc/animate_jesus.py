"""Animate the 8 APPROVED Jesus hero stills (i2v). House model =
cinematic_studio_video_v2 (bake-off winner: steadiest faces incl. background crowd,
holds the inked style with no morph). One tailored reverent motion verb per still +
a verbatim style-lock tail so the face/hair/beard and the ink look never drift.
9:16, 5s. Idempotent, rate-limit-aware. Writes anim_jesus/. POC/scratchpad only."""
import re, json, subprocess, urllib.request
from pathlib import Path

HF = str(Path.home() / "bin" / "hf.exe")
URL_RE = re.compile(r"https://\S+?\.(?:mp4|webm|mov)", re.IGNORECASE)
HERE = Path(__file__).parent
SRC = HERE / "jesus"
OUT = HERE / "anim_jesus"
OUT.mkdir(parents=True, exist_ok=True)

MODEL = "cinematic_studio_video_v2"
EXTRA = ["--aspect_ratio", "9:16", "--duration", "5"]

TAIL = (" Keep the exact same inked biblical graphic-novel art style, the exact same face, long "
        "dark hair and full beard. No morphing, no style change, no photoreal look, no added or "
        "removed figures, no text, no captions, steady reverent light, no glitter, no sparkles.")

# still slug -> tailored, Kling-safe motion (frozen tableau; the world breathes + camera moves)
STILLS = {
 "baptism__a": "Cinematic motion: the river water ripples and streams from his hands and hair, the "
               "shaft of light glows and the faint dove of light drifts gently downward, a slow "
               "reverent push-in on him.",
 "baptism__b": "Cinematic motion: water drips slowly down his face and hair, he breathes calmly with "
               "head bowed, the light above brightens softly and the dove of light hovers, a very "
               "slow micro push-in.",
 "crowd__a":   "Cinematic motion: the surrounding villagers shift and murmur, their reaching hands "
               "move, robes and dust stir in the sunlit street, a slow steady push-in on his calm "
               "compassionate face while he stays still and dominant.",
 "crowd__b":   "Cinematic motion: he breathes calmly, his hand rests steady on the kneeling man's "
               "head, the man trembles faintly, dust drifts in the warm light, a slow gentle push-in.",
 "scourged__a":"Cinematic motion: deep shadows shift slowly across the courtyard, he breathes with "
               "head bowed in noble suffering, the two soldiers in the background stand still, a "
               "very slow reverent push-in.",
 "scourged__b":"Cinematic motion: he breathes slowly, sweat glistens and shadow shifts across his "
               "face and shoulders, the dark background still around him, a very slow micro push-in.",
 "cross__b":   "Cinematic motion: the storm clouds drift slowly behind the cross and shafts of broken "
               "gold light shift across the sky, his body hangs still with head fallen forward, a "
               "slow solemn push-in from a low angle.",
 "risen__b":   "Cinematic motion: his radiant white robe and mantle flow gently, the golden "
               "resurrection light blazes and pulses softly behind him, his lifted pierced hands "
               "stay steady, a slow majestic push-in.",
}


def render(slug, prompt, src):
    dest = OUT / f"JESUS__{slug}.mp4"
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
    for slug, verb in STILLS.items():
        src = SRC / f"JESUS__{slug}.png"
        if not (src.exists() and src.stat().st_size > 0):
            print(f"[MISS] still not found: {src.name}", flush=True); continue
        print(f"\n[gen ] {slug} ...", flush=True)
        results[slug] = render(slug, verb + TAIL, src)
    (OUT / "manifest.json").write_text(json.dumps(results, indent=2))
    done = sum(1 for v in results.values() if v in ("ok", "skip"))
    print(f"\nDONE {done}/{len(results)} clips in {OUT}\n{json.dumps(results, indent=2)}", flush=True)
