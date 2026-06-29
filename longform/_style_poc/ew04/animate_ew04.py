"""Animate the 5 NEW EW04 (Bronze Serpent) inked stills (i2v). House model =
cinematic_studio_video_v2 (bake-off winner: steady faces, holds the inked style,
no morph). Frozen-tableau discipline: the WORLD breathes (fire, smoke, light), the
camera pushes in slowly, the figures and the bronze serpent stay still. Scenes 6-7
reuse the existing inked Jesus cross + risen clips (anim_jesus/), not re-rendered.

9:16, 5s. Idempotent, rate-limit-aware, 3-attempt retry. Writes anim/. POC/scratchpad."""
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

# style + identity lock shared by every clip
TAIL = (" Keep the exact same inked biblical graphic-novel art style, the exact same faces and "
        "identities, the same clothing and composition. No morphing, no style change, no photoreal "
        "look, no added or removed figures or objects, no text, no captions, steady reverent light, "
        "no glitter, no sparkles.")
# extra lock for the serpent scenes — the cast bronze must NOT come alive
SERPENT_LOCK = (" The bronze serpent on the pole is solid cast metal and stays completely still — it "
                "does NOT slither, coil, move or come alive; the pole stays planted and upright.")

# slug -> (motion prompt, extra-lock)
SCENES = {
 "01_hook_moses":
   ("Cinematic motion: the low amber firelight flickers and glows across Moses' weathered face and "
    "mantle, faint embers and smoke drift in the dark, his grey hair and robe stir very gently as he "
    "breathes, his gaze steady on the viewer; a slow reverent push-in.", ""),

 "02_judgment_plague":
   ("Cinematic motion: the scattered low campfires flicker and throw shifting light, thin smoke and "
    "dust drift across the darkening camp, the shadowed crowd stirs faintly in the distance, the "
    "fallen man lies still in pain; a slow dread-filled push-in. The desert serpent stays low and "
    "taut, only its tongue flickers once.", ""),

 "03_bronze_lifted":
   ("Cinematic motion: the fire at the base of the pole flickers and sends warm light climbing up the "
    "bare wooden shaft, the night clouds drift slowly across the dim sky, the bronze glints, Moses "
    "holds the pole steady and gazes up; a slow reverent push-in with a faint upward tilt.",
    SERPENT_LOCK),

 "04_look_and_live":
   ("Cinematic motion: the single shaft of warm light glows and softly intensifies, fine dust drifts "
    "in the beam, the bitten man's reaching hand stays steady as faint colour and life return to his "
    "face, the camp lies still in shadow; a slow push-in toward the lifted serpent in the distance.",
    SERPENT_LOCK),

 "05_night_teacher":
   ("Cinematic motion: the small clay oil-lamp flame flickers and its warm light wavers gently across "
    "the two faces, soft shadows shift on the stone wall behind them, both men sit still and breathe "
    "calmly as they speak in the hush; a slow gentle push-in.", ""),

 # ---- complementary 'b' stills (wide<->close pairs) ------------------------
 "01b_moses_close":
   ("Cinematic motion: warm firelight flickers and glows across Moses' weathered face, faint embers "
    "drift in the dark, his grey hair and beard stir very gently as he breathes, his weary eyes stay "
    "fixed on the viewer; a slow intimate push-in.", ""),

 "02b_serpents_spread":
   ("Cinematic motion: the scattered campfires flicker and throw shifting light across the tents, thin "
    "smoke and dust drift over the camp, the shadowed figures stir and recoil in the distance; the tall "
    "desert serpents stay reared and taut, only a tongue flickers once. A slow dread-filled push-in.", ""),

 "03b_serpent_atop_sky":
   ("Cinematic motion: the warm firelight glints and shifts on the bronze, the night clouds drift "
    "slowly across the dim sky behind it, a faint ember rises; a slow reverent push-in with a gentle "
    "upward tilt toward the lifted serpent.", SERPENT_LOCK),

 "04b_face_to_life":
   ("Cinematic motion: the single shaft of warm light glows and softly intensifies across the old "
    "man's face, fine dust drifts in the beam, faint living colour returns to his ashen skin as his "
    "eyes lift upward and his hand stays raised; a slow tender push-in. The bite-mark serpent on his "
    "neck stays completely still and does NOT slither or move.", ""),

 "05b_jesus_speaks":
   ("Cinematic motion: the clay oil-lamp flame flickers and its warm light wavers across Jesus' face, "
    "soft shadows shift on the stone wall, he breathes and speaks calmly while Nicodemus' shadowed "
    "shoulder stays still in the foreground; a slow gentle push-in.", ""),
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
    for slug, (motion, lock) in SCENES.items():
        src = SRC / f"{slug}.png"
        if not (src.exists() and src.stat().st_size > 0):
            print(f"[MISS] still not found: {src.name}", flush=True); continue
        print(f"\n[gen ] {slug} ...", flush=True)
        results[slug] = render(slug, motion + lock + TAIL, src)
    (OUT / "manifest.json").write_text(json.dumps(results, indent=2))
    done = sum(1 for v in results.values() if v in ("ok", "skip"))
    print(f"\nDONE {done}/{len(results)} clips in {OUT}\n{json.dumps(results, indent=2)}", flush=True)
