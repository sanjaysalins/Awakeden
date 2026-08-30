"""Score for The Barrel That Did Not Waste.

Reuses the felt-piano "Fig Tree"/epic-soft identity validated on episode 8
("love this score, this perhaps the best north star score", see
[[feedback_score_felt_piano_over_trance]]) and evolved again on Naaman ep4
("lock this, this is great", see [[feedback_naaman_score_cello_rejected]]) --
now a two-episode-validated series identity, not a one-off. Per
[[feedback_fable_prompt_rewrite_dilutes_proven_direction]], this is a
near-verbatim evolution of Naaman's own winning prompt, not a reinvention:
same instrument, same core rules (no drums/percussion/bassline ever, no big
swell, strings widen but never peak). The only real change is WHAT the
piano's hardening moment means and WHEN things land, re-timed to this
episode's own arc: dread (not anger) peaks at her "we may eat it, and die"
line, resolves at "Fear not," strings gather at the miracle ("wasted not"),
and the piece closes in plain stillness under "He needs it open."

Run:
  .venv\\Scripts\\python.exe poc_living_water_ink_style_test\\swirls_episode_05_barrel_that_did_not_waste\\generate_score_piano.py
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from pipeline.assembly_align import _resolve_key  # noqa: E402

HERE = Path(__file__).resolve().parent
NARRATION = HERE / "narration.mp3"
RAW = HERE / "score_piano_raw.mp3"
FITTED = HERE / "score_piano.mp3"
OUTRO_HOLD = 3.0
OUTRO_MARGIN = 2.5

PROMPT = (
    "Intimate modern-classical felt piano, instrumental, slow and rubato, around 60 bpm. One "
    "quiet, tender felt-piano motif of just a few notes carries the entire piece as its lead and "
    "almost only voice, played sparsely with long pedal decays and real silence between phrases; "
    "no drums, no percussion, no bassline, nothing rhythmic at all, ever. The opening is spare "
    "and hollow, the motif hesitant and unfinished in the piano's middle-to-low register, small "
    "phrases trailing off into real silence rather than resolving -- a private, hungry, "
    "uncertain moment. Around fifteen seconds in, the piano's own hesitation deepens into real "
    "dread: the motif drops lower still, the touch grows heavier and more tentative at once, "
    "one or two bare dissonant intervals struck softly and left to hang unresolved in the pedal, "
    "the phrases growing sparser and further apart rather than tighter -- fear as absence and "
    "hesitation, never as volume or rhythm; no percussion arrives, no pulse forms. Around "
    "twenty-five seconds in, on a single clear moment, the dissonance resolves outright: one "
    "plain, warm, unambiguous chord in the middle register, held long in the pedal, the motif "
    "returning steadied and simple, as if a held breath had finally been let out. From around "
    "thirty-five seconds, strings begin to gather underneath one section at a time, each entry "
    "almost imperceptible: soft violas first, then muted violins, then low cellos, sustaining "
    "long warm tones that slowly widen the harmony beneath the unchanged piano motif -- wonder, "
    "not triumph -- and crucially this piece never rises to a big swell or crescendo: the "
    "strings only ever widen and warm, staying far behind the piano, a supportive glow that "
    "deepens gradually to the end without ever reaching a peak. The closing stretch settles "
    "into plain, humble stillness -- the motif one last time, slower and simpler than it has "
    "ever been, over the wide soft string glow, resolving completely and fading gently to "
    "silence. Tender, hungry, steadied, the feeling of an empty hand opened first and found "
    "never quite empty; a clean, airy, uncluttered mix with generous headroom, everything soft, "
    "underneath, and unhurried."
)


def dur(p: Path) -> float:
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "default=nw=1:nk=1", str(p)],
        capture_output=True, text=True, check=True).stdout.strip()
    return float(out)


def main() -> None:
    key = _resolve_key()
    if not key:
        sys.exit("no ELEVENLABS_API_KEY (PythonProject1/.env)")
    import requests
    total = dur(NARRATION) + OUTRO_HOLD
    glen = total + OUTRO_MARGIN
    print(f"[full] narration={dur(NARRATION):.2f}s + {OUTRO_HOLD}s hold -> generating ~{glen:.1f}s ...")
    r = requests.post(
        "https://api.elevenlabs.io/v1/music",
        headers={"xi-api-key": key, "Content-Type": "application/json", "Accept": "audio/mpeg"},
        json={"prompt": PROMPT, "music_length_ms": int(glen * 1000),
              "force_instrumental": True, "model_id": "music_v1"},
        timeout=300,
    )
    if r.status_code != 200:
        sys.exit(f"FAILED [{r.status_code}]: {r.text[:300]}")
    RAW.write_bytes(r.content)
    subprocess.run(
        ["ffmpeg", "-y", "-v", "error", "-i", str(RAW), "-af",
         f"afade=t=in:st=0:d=1.0,afade=t=out:st={total-2.0:.2f}:d=2.0",
         "-t", f"{total:.2f}", str(FITTED)], check=True)
    print(f"[done] {FITTED} ready at {dur(FITTED):.2f}s")


if __name__ == "__main__":
    main()
