"""Score v2 for "The Second Fire" -- merged from the blind score+SFX panel (score_sfx_panel/panel_r1,
5/5 seats): one 3-note motif, falling/unresolved in D minor at night, rising/resolved in D major from
sunrise. Oud + wooden flute + low cello (+ soft frame drum after sunrise only). Two parts split at
the night->sunrise cut (23.6 s). Free-text music_v1, never composition_plan. Owner yes 2026-11-13.
Also generates 3 new SFX (rooster, splash, fish sizzle), 2 takes each, into sfx_new/.
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
sys.path.insert(0, str(HERE))
from pipeline.assembly_align import _resolve_key  # noqa: E402
from generate_score_piano import check_no_dead_intro, check_timeline_sweep, dur  # noqa: E402

FINAL_VIDEO = HERE / "SECOND_FIRE_PREVIEW_v2.mp4"
OUTDIR = HERE / "score_v2"
PART1_RAW = OUTDIR / "part1_raw.mp3"
PART2_RAW = OUTDIR / "part2_raw.mp3"
RAW = OUTDIR / "score_v2_raw.mp3"
FITTED = OUTDIR / "score_v2.mp3"
SPLIT_S = 23.6
CROSSFADE_S = 0.6

PART1_PROMPT = (
    "Instrumental only, intimate acoustic folk film music beneath spoken narration, key of D minor, "
    "slow, about 56 bpm, Middle Eastern Galilee feeling. Rounded finger-plucked oud, one low bowed "
    "cello holding long quiet notes, a breathy wooden ney flute used only once or twice. The music is "
    "audible from the very first second, no silent lead-in. Signature melody: three slow oud notes "
    "that step DOWN, D, C, A, and stop short without resolving, like a man saying no. Around 2 seconds "
    "in the oud plays the three falling notes. Around 9 seconds in the three falling notes again, "
    "thinner, over the low cello. Around 13 seconds in the three falling notes a third time, very "
    "quiet. Around 16 seconds in almost only the low cello, hushed and still, then one soft high "
    "ney note of hope. Around 19 seconds in a few lonely isolated oud plucks over a dark empty night "
    "sea. Keep playing continuously to the very end and end on a held low D cello note with no "
    "cadence and no fade-out. Cold, lonely, tender, unresolved. No piano, no drums, no choir, no "
    "vocals, no orchestral swell, never epic, not a trailer."
)

PART2_PROMPT = (
    "Instrumental only, intimate acoustic folk film music beneath spoken narration, key of D major, "
    "warm, about 60 bpm, Middle Eastern Galilee feeling, continuing the same piece: the same "
    "rounded finger-plucked oud, low bowed cello and breathy wooden ney flute. Starts immediately on "
    "an open D and A fifth like sunrise over water, no silent lead-in. Signature melody: three oud "
    "notes that now step UP, D, F sharp, A, hopeful. In the first second the ney plays the three "
    "rising notes. Around 5 seconds in a gentle rolling oud pattern with a very soft hand frame drum "
    "like a slow heartbeat, quiet joy. Around 13 seconds in the drum stops and the music drops back "
    "to just soft cello and single oud notes, very still and close. Around 24 seconds in warm, "
    "welcoming oud and cello, simple and kind, like a meal shared with friends. Around 30 seconds in "
    "very spacious and gentle: the oud plays the three rising notes, waits, plays them again, waits, "
    "and a third time, each a little closer, like a quiet question. Around 37 seconds in a short "
    "shade of minor, a few low aching cello notes, never loud. Around 48 seconds in the cello opens "
    "into warm major harmony. Around 54 seconds in the three rising notes once more, fuller, the ney "
    "joins. Around 57 seconds in the oud plays the three rising notes slowly and adds a fourth note "
    "that lands home on D, and the warm D major chord rings and keeps ringing to the very last second "
    "with no fade-out and no early ending. No piano, no choir, no vocals, no brass, no big drums, no "
    "epic build, never a trailer. Continuous, no silent gaps."
)

SFX = {
    "rooster": ("one single rooster crowing once, far away across a stone courtyard at night, natural "
                "field recording, real farm bird, slight distance, no second crow, no other animals, no music", 3.0),
    "splash": ("one man jumping from a small wooden boat into calm shallow lake water, a single heavy "
               "natural splash then water settling, realistic, no voices, no music", 3.0),
    "sizzle": ("fish gently sizzling on hot charcoal embers outdoors by a lake, soft, close, natural, "
               "quiet ticking coals, no voices, no music", 8.0),
}


def gen_music(prompt: str, glen: float, out: Path, key: str) -> None:
    import requests
    if out.exists():
        print(f"  reuse {out.name} (no re-spend)")
        check_no_dead_intro(out)
        return
    print(f"  requesting {out.name} ~{glen:.1f}s ...", flush=True)
    r = requests.post("https://api.elevenlabs.io/v1/music",
                      headers={"xi-api-key": key, "Content-Type": "application/json", "Accept": "audio/mpeg"},
                      json={"prompt": prompt, "music_length_ms": int(glen * 1000),
                            "force_instrumental": True, "model_id": "music_v1"}, timeout=300)
    if r.status_code != 200:
        sys.exit(f"FAILED [{r.status_code}]: {r.text[:300]}")
    out.write_bytes(r.content)
    check_no_dead_intro(out)


def gen_sfx(key: str) -> None:
    import requests
    d = HERE / "sfx_new"
    d.mkdir(exist_ok=True)
    for name, (prompt, secs) in SFX.items():
        for take in (1, 2):
            out = d / f"{name}_t{take}.mp3"
            if out.exists():
                continue
            print(f"  sfx {out.name} ...", flush=True)
            r = requests.post("https://api.elevenlabs.io/v1/sound-generation",
                              headers={"xi-api-key": key, "Content-Type": "application/json", "Accept": "audio/mpeg"},
                              json={"text": prompt, "duration_seconds": secs, "prompt_influence": 0.4}, timeout=180)
            if r.status_code != 200:
                sys.exit(f"SFX FAILED [{r.status_code}]: {r.text[:300]}")
            out.write_bytes(r.content)


def main() -> None:
    key = _resolve_key()
    if not key:
        sys.exit("no ELEVENLABS_API_KEY")
    OUTDIR.mkdir(exist_ok=True)
    total = dur(FINAL_VIDEO)
    p1_len, p2_len = SPLIT_S, total - SPLIT_S
    print(f"[v2] video {total:.2f}s, split {SPLIT_S}s (part1 {p1_len:.2f} / part2 {p2_len:.2f})")
    gen_music(PART1_PROMPT, p1_len + 3.0, PART1_RAW, key)
    gen_music(PART2_PROMPT, p2_len + 6.0, PART2_RAW, key)
    p1, p2 = OUTDIR / "_p1.mp3", OUTDIR / "_p2.mp3"
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", str(PART1_RAW), "-t", f"{p1_len + CROSSFADE_S:.2f}", str(p1)], check=True)
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", str(PART2_RAW), "-t", f"{p2_len:.2f}", str(p2)], check=True)
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", str(p1), "-i", str(p2), "-filter_complex",
                    f"acrossfade=d={CROSSFADE_S}:c1=tri:c2=tri", str(RAW)], check=True)
    p1.unlink(); p2.unlink()
    check_timeline_sweep(RAW)
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", str(RAW), "-af",
                    f"afade=t=in:st=0:d=0.5,afade=t=out:st={total - 1.5:.2f}:d=1.5", "-t", f"{total:.2f}", str(FITTED)], check=True)
    check_timeline_sweep(FITTED)
    print(f"[done] {FITTED} {dur(FITTED):.2f}s")
    gen_sfx(key)
    print("[done] sfx_new/")


if __name__ == "__main__":
    main()
