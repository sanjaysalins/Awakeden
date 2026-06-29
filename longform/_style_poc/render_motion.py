"""Phase 2 MOTION bake-off: does a STYLIZED still survive Kling animation?
3 looks (D ink / F claymation / G charcoal) x 2 stills = 6 clips.
HF Kling pro, 5s, 9:16, --start-image local PNG. ~12.5 cr/clip (~75 cr total).

Failure mode we are testing for: Kling "photoreal-izes" a stylized still mid-clip
(ink smooths, clay loses fingerprints, charcoal grain melts). So every prompt
LEADS with a hard medium-lock + frozen-tableau face + camera-only motion.
Scratchpad only. Idempotent (skips existing mp4)."""
import re, subprocess, time
from pathlib import Path

HF = str(Path.home() / "bin" / "hf.exe")
FACES = Path(__file__).parent / "faces"
OUT = Path(__file__).parent / "motion"
OUT.mkdir(parents=True, exist_ok=True)

# medium-lock phrasing per look — the anti-photoreal-ization guard
MEDIUM = {
 "D": ("This image is a bold graphic-novel INK illustration and MUST stay pure ink "
       "in every single frame — keep the hard black ink linework, the flat spotted "
       "blacks and the limited muted palette; never smooth or render it toward photoreal."),
 "F": ("This image is a handmade STOP-MOTION CLAYMATION puppet and MUST stay sculpted "
       "clay in every single frame — keep the visible fingerprints, clay texture and "
       "miniature-set look; never smooth or render it toward photoreal."),
 "G": ("This image is a CHARCOAL and white-chalk drawing on toned paper and MUST stay "
       "a charcoal drawing in every single frame — keep the smudged strokes, paper grain "
       "and hand-drawn marks; never smooth or render it toward photoreal."),
}

# motion is camera-led + minimal; a single tear only on the already-crying pit shots
TABLEAU = ("Frozen tableau: the face holds its exact expression and shape, no morphing, "
           "no new elements appear. ")
PIT_MOTION = (TABLEAU + "Only motion: one very slow cinematic push-in toward the face, the "
              "faintest breath, and a single tear slips slowly down one cheek. Nothing else moves.")
REV_MOTION = (TABLEAU + "Only motion: one very slow reverent push-in toward the face, the "
              "faintest breath, the gentlest drift of cloth. Nothing else moves.")

# (look, still-stem, motion) — 2 per look: hardest morph test + reverence test
JOBS = [
 ("D", "D_inknovel__joseph_pit",  PIT_MOTION),
 ("D", "D_inknovel__joseph_weep", REV_MOTION),
 ("F", "F_claymation__joseph_pit", PIT_MOTION),
 ("F", "F_claymation__christ_face", REV_MOTION),
 ("G", "G_charcoal__joseph_pit",  PIT_MOTION),
 ("G", "G_charcoal__christ_face", REV_MOTION),
]


def render(look, stem, motion):
    png = FACES / f"{stem}.png"
    out = OUT / f"{stem}.mp4"
    if out.exists() and out.stat().st_size > 0:
        print(f"[skip] {stem}", flush=True); return True
    if not png.exists():
        print(f"[MISS] {stem} (no still)", flush=True); return False
    prompt = MEDIUM[look] + " " + motion
    (OUT / f"{stem}.prompt.txt").write_text(prompt, encoding="utf-8")
    print(f"[gen ] {stem} ...", flush=True)
    cmd = [HF, "generate", "create", "kling3_0", "--start-image", str(png),
           "--prompt", prompt, "--duration", "5", "--mode", "pro",
           "--sound", "off", "--aspect_ratio", "9:16", "--wait"]
    t = time.time()
    r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8",
                       errors="replace", timeout=900)
    blob = (r.stdout or "") + (r.stderr or "")
    m = re.search(r'https?://[^\s"]+\.mp4', blob)
    if not m:
        print(f"[FAIL] {stem} no url ({time.time()-t:.0f}s)\n{blob[-400:]}", flush=True); return False
    subprocess.run(["curl", "-s", "-L", m.group(0), "-o", str(out)], check=True)
    ok = out.exists() and out.stat().st_size > 0
    print(f"[{'ok  ' if ok else 'FAIL'}] {stem} -> {out} ({time.time()-t:.0f}s)", flush=True)
    return ok


if __name__ == "__main__":
    ok = 0
    for look, stem, motion in JOBS:
        try:
            if render(look, stem, motion): ok += 1
        except Exception as e:
            print(f"[ERR ] {stem}: {e}", flush=True)
    print(f"\nDONE {ok}/{len(JOBS)} motion clips in {OUT}  (~{ok*12.5:.0f} cr)", flush=True)
