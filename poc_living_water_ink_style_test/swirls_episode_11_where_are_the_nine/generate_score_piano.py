"""Score for Where Are the Nine (Luke 17:11-19, the ten lepers).

CORRECTED 2026-09-05 (score-design-early rebuild): the musical identity and
arc below are UNCHANGED from the original version -- only the timing cues are
now REAL per-word alignment timestamps (from narration.alignment.json, walked
through the unit word-counts, verified word-for-word against the raw
alignment file) instead of word-count-proportional estimates. See
`.claude/skills/swirls-of-life/SCORE_DESIGN_EARLY.md` for the corrected
process this implements, and its own history note on why this is a free-text
`music_v1` prompt and not an ElevenLabs `composition_plan`/`music_v2` request
(that structured route is a confirmed dead end in this project -- STATE.md
2026-08-10 and 2026-06-24 -- never built anywhere runnable / injects vocals).

Reuses the felt-piano "Fig Tree" identity validated on episode 8 ("love this
score, this perhaps the best north star score", see
[[feedback_score_felt_piano_over_trance]]) and evolved on Naaman ep4, the
Barrel ep5, the Bier ep7, and She Loved Much ep10 (a five-episode-validated
series identity), now extended to a sixth arc. Per
[[feedback_fable_prompt_rewrite_dilutes_proven_direction]], this is a
near-verbatim evolution of the prior episodes' own winning prompt, not a
reinvention: same instrument, same core rules (no drums/percussion/bassline
ever, no big swell, strings widen but never peak, real silence between
phrases). The only real change from the ORIGINAL version of this file is
WHEN the cues land -- now real seconds, not estimated ones (real vs. old
estimate; some moved earlier, some later):

  0.0-3.1s    front  the paradox -- sent before a single one was healed
  3.1-11.0s   f01    the stakes -- only one of them ever came back            (was ~3.2s, ~same)
  11.0-19.2s  f02    the cry -- "have mercy on us", plaintive, reaching
  19.2-25.4s  f03    obeyed before they could see any difference --          (was ~18.4s, +0.8s)
                       faith before sight, still withheld, nothing resolved
  25.4-29.9s  f04    the miracle itself, off-page, on the road -- a first    (was ~25.1s, ~same)
                       quiet opening (the gift is free and universal here,
                       NOT yet the personal turn -- do not fully resolve)
  29.9-35.7s  f05    the fork -- nine keep going, one turns back             (was ~29.9s, ~same)
  35.7-41.9s  f06    he falls at his feet, giving thanks -- tenderness builds (was ~35.1s, +0.6s)
  41.9-50.8s  f07    "where are the nine?" -- a held, questioning stillness   (was ~41.9s, ~same)
  50.8-55.3s  f08    "this stranger" -- the naming, still unresolved         (was ~50.7s, ~same)
  55.3-62.2s  f09    HERO -- "thy faith hath made thee whole" -- the piece's (was ~56.2s, -0.9s)
                       one true resolution, exactly here and not before
  62.2-74.6s  f10    strings gather -- "Luke calls it thanks, Jesus calls it (was ~63.8s, -1.6s)
                       faith", reflective, warm
  74.6-80.5s  back   the landing -- "go back and find him", plain and settled (was ~73.0s, +1.6s)

The two biggest real corrections: the hero resolution chord now lands 0.9s
EARLIER (matching Christ's word actually arriving sooner than the old
word-count estimate assumed) and the strings' entry now lands 1.6s EARLIER
(matching f10's real page-turn). `unit_timing.json` in this folder carries
these same real boundaries so `swirls_assemble.py` cuts the video at the
SAME timestamps this score is built from -- see SCORE_DESIGN_EARLY.md's
assembler fix. Without that file, assembly would silently fall back to the
old proportional cuts and the two would drift apart again.

Distinct from ep10's held-back-through-two-tender-pages arc: THIS piece's
gift (the cleansing, f04) is genuinely free and given to all ten without
condition, so it earns a small, real opening in the music -- but the piece's
true resolution belongs to the ONE encounter alone (f09, Christ's personal
word), matching this project's locked rule that the doctrinal hero carries
the landing, not the moment of general blessing. So f04 brightens briefly
but pulls back again by f05-f08 (the fork, the fall, the question, the
naming all stay searching, not yet home), and only fully resolves at f09.
Strings enter after that resolution (f10), same rule as every prior episode.
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
    "and plain, faintly searching, the motif cool and unresolved in the piano's middle register, "
    "small phrases that stop short rather than land -- ten men sent away before anything has "
    "changed. Around three seconds in, the motif quickens very slightly, still unresolved, a "
    "quiet urgency entering -- a cry reaching out, not yet answered. Around nineteen seconds in "
    "the piano goes plainer and more careful, the phrases shorter, obedience without any proof "
    "yet, nothing given away. Around twenty-five seconds in, on a single clear moment, the piano "
    "opens briefly -- one gentle, warmer interval struck and left to ring, a real but modest "
    "brightening, as if something ordinary and good has just happened out of sight -- then within "
    "a few seconds it draws back again, unresolved, because this is not yet the piece's true "
    "turn. Around thirty seconds in the motif splits its attention, half the phrases continuing "
    "plainly onward, half lingering half a beat longer, searching. Around thirty-six seconds in a "
    "held, private tenderness enters, phrases aching rather than settling, still incomplete. "
    "Around forty-two seconds in the piece goes almost still: one long sustained tone, held far "
    "longer than anything before it, a held breath, a question left hanging in the air, withheld "
    "on purpose. Around fifty-one seconds in the stillness continues, quiet, searching, one "
    "name almost spoken. Around fifty-five seconds in, on a single clear moment, that held "
    "stillness resolves outright at last: one plain, warm, unambiguous chord, held long in the "
    "pedal, the motif returning steadied and simple, as if a person had finally been met face to "
    "face. From around sixty-two seconds, strings begin to gather underneath one section at a "
    "time, each entry almost imperceptible: soft violas first, then muted violins, then low "
    "cellos, sustaining long warm tones that slowly widen the harmony beneath the unchanged piano "
    "motif -- peace, not triumph -- and crucially this piece never rises to a big swell or "
    "crescendo: the strings only ever widen and warm, staying far behind the piano, a supportive "
    "glow that deepens gradually to the end without ever reaching a peak. Around seventy-five "
    "seconds in the closing stretch settles into plain, humble stillness -- the motif one last "
    "time, slower and simpler than it has ever been, over the wide soft string glow, resolving "
    "completely and fading gently to silence. Searching, withheld, finally met; a clean, airy, "
    "uncluttered mix with generous headroom, everything soft, underneath, and unhurried."
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
