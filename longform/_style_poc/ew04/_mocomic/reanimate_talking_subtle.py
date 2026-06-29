"""Re-animate the TALKING clips with the subtle 'talk' motion policy (face held still),
backing up the originals. cinematic_studio_video_v2, 9:16, 5s. Idempotent on backup."""
import re, subprocess, urllib.request, shutil
from pathlib import Path
import motion_policy as mp

HF = str(Path.home() / "bin" / "hf.exe")
URL_RE = re.compile(r"https://\S+?\.(?:mp4|webm|mov)", re.IGNORECASE)
EW = Path(r"C:\Users\sanjay\PycharmProjects\JesusInTheBible\longform\_style_poc\ew04")
ST = EW / "stills"; ANIM = EW / "anim"
LOUD = ANIM / "_loud_talk"; LOUD.mkdir(exist_ok=True)

# talking close scenes (the ones whose face motion fights the narration)
TALK = {
 "01b_moses_close": "A tight close-up of the aged prophet Moses' weathered face, half-lit by warm "
                    "firelight against deep shadow, his weary eyes on the viewer.",
 "05_night_teacher": "Inside a dark Jerusalem stone house, Jesus on the right and the older Pharisee "
                     "Nicodemus on the left face each other across a low oil lamp.",
 "05b_jesus_speaks": "A warm close-up of Jesus lit by a low oil lamp in the night, the shadowed "
                     "shoulder of Nicodemus in the foreground.",
}


def render(slug, prompt):
    dest = ANIM / f"EW04__{slug}.mp4"
    if (LOUD / dest.name).exists():
        print(f"[skip] {slug} (already reanimated)", flush=True); return
    if dest.exists():
        shutil.move(str(dest), str(LOUD / dest.name))   # keep the loud original
    args = [HF, "generate", "create", "cinematic_studio_video_v2", "--prompt", prompt,
            "--aspect_ratio", "9:16", "--duration", "5", "--image", str(ST / f"{slug}.png"),
            "--wait", "--wait-timeout", "20m"]
    for attempt in (1, 2, 3):
        r = subprocess.run(args, capture_output=True, text=True, encoding="utf-8",
                           errors="replace", timeout=1500)
        blob = (r.stdout or "") + (r.stderr or "")
        m = URL_RE.search(blob)
        if m:
            req = urllib.request.Request(m.group(0), headers={"User-Agent": "poc/1.0"})
            with urllib.request.urlopen(req, timeout=300) as resp:
                dest.write_bytes(resp.read())
            print(f"[ok  ] {slug}", flush=True); return
        low = blob.lower()
        if not ("concurrent_jobs_limit" in low or "rate_limit" in low or "timeout" in low) or attempt == 3:
            print(f"[FAIL] {slug} (rc={r.returncode}) {blob[-200:].strip()}", flush=True)
            if not dest.exists() and (LOUD / dest.name).exists():
                shutil.move(str(LOUD / dest.name), str(dest))  # restore on failure
            return


if __name__ == "__main__":
    for slug, desc in TALK.items():
        print(f"[gen ] {slug} ...", flush=True)
        render(slug, mp.prompt_for("talk", desc))
    print("DONE reanimate talking subtle", flush=True)
