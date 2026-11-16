"""Score for a Swirls SHORT episode: felt-piano identity, TWO-PART generation split at the north-star
page (copy of ep16's generate_score_piano.py, parameterised: design v3.2 step 8).

Inputs come from the EPISODE, never from another episode's file:
  assembly_receipt.json  -> the draft cut path and its length (`output`, `total`)
  unit_timing.json       -> the turning points (start of each unit)
  page_plan.json         -> `north_star`, where the score resolves
It exits unless it is called by `swirls_episode.py <dir> score` (an environment token set by the
runner), so a bare run can never spend ElevenLabs money. `--dry-run` prints the inputs and stops (no
key, no network). Free-text music_v1, never composition_plan (a proven dead end).
"""
from __future__ import annotations

import hashlib
import json
import os
import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = Path(os.environ["JITB_ROOT"]) if os.environ.get("JITB_ROOT") else next(
    p for p in HERE.parents if (p / "sfx_pilots").is_dir())
sys.path.insert(0, str(ROOT))

RAW = HERE / "score_piano_raw.mp3"
FITTED = HERE / "score_piano.mp3"
PART1_RAW = HERE / "score_piano_part1_raw.mp3"
PART2_RAW = HERE / "score_piano_part2_raw.mp3"
OUTRO_MARGIN = 2.5
CROSSFADE_S = 0.4


def run_token() -> str:
    eid = json.loads((HERE / ".swirls_short").read_text(encoding="utf-8")).get("episode_id")
    return hashlib.sha256(("score:" + str(eid)).encode()).hexdigest()[:16]


def read_inputs() -> dict:
    rec = json.loads((HERE / "assembly_receipt.json").read_text(encoding="utf-8"))
    timing = json.loads((HERE / "unit_timing.json").read_text(encoding="utf-8"))
    ns = json.loads((HERE / "page_plan.json").read_text(encoding="utf-8"))["north_star"]
    return {"cut": Path(rec["output"]), "total": float(rec["total"]), "split": float(timing["units"][ns]["start_s"]),
            "north_star": ns, "turns": {t: float(u["start_s"]) for t, u in timing["units"].items()}}


def prompts(inp: dict) -> tuple[str, str]:
    marks = ", ".join(f"{t} at {s:.0f} seconds" for t, s in inp["turns"].items())
    p1 = ("Intimate modern-classical felt piano, instrumental, slow and rubato, around 60 bpm. One quiet, "
          "tender felt-piano motif of just a few notes carries the entire piece as its lead and almost only "
          "voice, played sparsely with long pedal decays; the piano is audibly present and playing "
          "throughout, from its very first second onward, never falling fully silent for more than a couple "
          "of seconds at a time; no drums, no percussion, no bassline, nothing rhythmic at all, ever. The "
          f"piece opens quiet and a little lonely and gathers slowly; its turning points fall at: {marks}. "
          f"It thins to one soft, open, expectant phrase near {inp['split']:.0f} seconds, always clearly "
          "audible, waiting, ending unresolved and open. Clean, airy, uncluttered mix, generous headroom.")
    p2 = ("Intimate modern-classical felt piano, instrumental, slow and rubato, around 60 bpm, continuing "
          "directly from a quiet, open, expectant phrase. Around two seconds in, the SAME tender felt-piano "
          "motif resolves outright at last: one plain, warm, full chord held long in the pedal. No drums, no "
          "percussion, no bassline, nothing rhythmic at all, ever; the piano remains audibly present "
          "throughout. It keeps playing steadily at the same soft level right through to the very last "
          "second, with no fade-out and no early ending; the final chord is still ringing when the piece "
          "stops. Clean, airy, uncluttered mix with generous headroom.")
    return p1, p2


def dur(p: Path) -> float:
    return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of",
                                 "default=nw=1:nk=1", str(p)], capture_output=True, text=True, check=True).stdout.strip())


def _mean_db(p: Path, ss: float, t: float) -> float | None:
    out = subprocess.run(["ffmpeg", "-ss", str(ss), "-i", str(p), "-t", str(t), "-af", "volumedetect", "-f", "null", "-"],
                         capture_output=True, text=True).stderr
    m = re.search(r"mean_volume:\s*(-?[0-9.]+) dB", out)
    return float(m.group(1)) if m else None


def check_timeline_sweep(p: Path, window: float = 5.0, threshold: float = -55.0) -> None:
    """Sweep the WHOLE timeline (a whole-file mean hides a 50 s dead stretch in the middle)."""
    total, t, dead = dur(p), 0.0, []
    while t < total:
        w = min(window, total - t)
        m = _mean_db(p, t, w)
        if m is None or m <= threshold:
            dead.append((round(t, 1), round(t + w, 1)))
        t += window
    if dead:
        sys.exit(f"[FAIL] {p.name}: dead/near-silent span(s): {dead} -- do not ship; regenerate.")


def _gen_music(prompt: str, glen: float, out: Path, key: str) -> None:
    import requests
    r = requests.post("https://api.elevenlabs.io/v1/music",
                      headers={"xi-api-key": key, "Content-Type": "application/json", "Accept": "audio/mpeg"},
                      json={"prompt": prompt, "music_length_ms": int(glen * 1000), "force_instrumental": True,
                            "model_id": "music_v1"}, timeout=300)
    if r.status_code != 200:
        sys.exit(f"FAILED [{r.status_code}]: {r.text[:300]}")
    out.write_bytes(r.content)


def main() -> None:
    inp = read_inputs()
    if "--dry-run" in sys.argv:
        print(json.dumps({k: str(v) if isinstance(v, Path) else v for k, v in inp.items()}, indent=2))
        return
    if os.environ.get("SWIRLS_RUN_SCORE") != run_token():
        sys.exit("refused: run the score only through `swirls_episode.py <episode> score` (the guarded command)")
    from pipeline.assembly_align import _resolve_key
    key = _resolve_key()
    if not key:
        sys.exit("no ELEVENLABS_API_KEY (PythonProject1/.env)")
    total, split = inp["total"], inp["split"]
    p1, p2 = prompts(inp)
    if not PART1_RAW.exists():
        _gen_music(p1, split + OUTRO_MARGIN, PART1_RAW, key)
    if not PART2_RAW.exists():
        _gen_music(p2, (total - split) + 8.0, PART2_RAW, key)
    t1, t2 = HERE / "_p1_trim.mp3", HERE / "_p2_trim.mp3"
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", str(PART1_RAW), "-t", f"{split + CROSSFADE_S:.2f}", str(t1)], check=True)
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", str(PART2_RAW), "-t", f"{total - split:.2f}", str(t2)], check=True)
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", str(t1), "-i", str(t2), "-filter_complex",
                    f"acrossfade=d={CROSSFADE_S}:c1=tri:c2=tri", str(RAW)], check=True)
    t1.unlink()
    t2.unlink()
    check_timeline_sweep(RAW)
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", str(RAW), "-af", "afade=t=in:st=0:d=1.0", "-t", f"{total:.2f}",
                    str(FITTED)], check=True)
    check_timeline_sweep(FITTED)
    print(f"[done] {FITTED} {dur(FITTED):.2f}s")


if __name__ == "__main__":
    main()
