"""Score for The Queen Who Came to Test Him.

Carries forward "The Fig Tree" felt-piano identity from episode 8 (the
user's own call, 2026-08-25: "it's perhaps the best north star score" — and
explicitly asked for a fresh Fable design pass tailored to THIS episode's own
arc, not a verbatim reuse of episode 8's prompt).

Design pass (Fable, 2026-08-25): same core identity as episode 8 (one felt-
piano motif as the only voice, no drums/percussion/bassline, sparse with real
silence, a barely-audible string pad + tape hiss). Two deliberate departures,
both tied to THIS episode's own arc (not Nathanael's):
  1. Early phrases end on an unresolved, questioning note; from the midpoint
     the same phrase settles onto its resolution -- mirrors the queen's own
     doubt-motif (shaky linework) resolving by the episode's midpoint, well
     before the separate blue-thread truth-motif reaches its own full bloom.
  2. The string swell blooms later (~75-80% through, exactly on "a greater
     than Solomon is here" / the truth-thread's own full-bloom page) and then
     RECEDES into settled stillness for the closing direct-address CTA,
     rather than holding the rise to the end like episode 8's swell did --
     this story's peak lands later and is followed by a quiet landing, not a
     second crescendo.
Fallback note from the design pass: if the render comes back too melancholy,
or the "unresolved -> resolving" phrase device doesn't come through, deleting
the one sentence about hanging/resolving phrase endings collapses this prompt
back to the plain Fig Tree identity.

Run:
  .venv\\Scripts\\python.exe poc_living_water_ink_style_test\\swirls_episode_01_queen_who_came_to_test_him\\generate_score.py
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
RAW = HERE / "score_final_raw.mp3"
FITTED = HERE / "score_final.mp3"
OUTRO_HOLD = 5.0  # RETUNED (user, 2026-08-25): "linger a few seconds, feels too abrupt" -- was 3.0
OUTRO_MARGIN = 2.5

PROMPT = (
    "Intimate modern-classical felt piano, instrumental, slow and rubato, around 60 bpm. One "
    "quiet, tender felt-piano motif of just a few notes carries the entire piece as its only "
    "voice, played sparsely with long pedal decays and real silence between phrases; no drums, "
    "no percussion, no bassline, nothing rhythmic at all. Early phrases end hanging on an "
    "unresolved, questioning note; from the midpoint the same phrase settles gently onto its "
    "resolution. A soft warm string pad and a faint breath of tape hiss sit far behind the "
    "piano, barely audible, supportive never prominent. Around three-quarters of the way "
    "through the strings rise and open into one wide, radiant, awestruck swell while the piano "
    "keeps the same simple motif unchanged; the swell then softens, and the closing stretch "
    "rests in warm, settled stillness, sparse piano over a faint string glow. In the final "
    "five seconds the piano strikes one single resolved chord and holds it, the string glow "
    "sustaining audibly underneath at a soft, clearly audible volume the whole time -- do not "
    "let the sound decay away or fall silent early -- only in the very last moment does it "
    "finally fade, slowly, into silence. Vast, wondering, reverent, the feeling of crossing a "
    "great distance and finding the rumor more than true; a clean, airy, uncluttered mix with "
    "generous space."
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
