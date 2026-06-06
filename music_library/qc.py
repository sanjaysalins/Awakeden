"""qc.py — objective audition helper for ingested music takes.

Catches the WORST "instrumental"-leak failure automatically, and surfaces the placement
metadata, so you only ear-check what matters:
  * VOCALS (lyrics)  — reuses the project's Whisper ASR to "listen" for sung words. RELIABLE:
                       if it transcribes real words, there are vocals → reject.
  * swell + LUFS     — the climax time the placer aligns + loudness (already measured at ingest)

Honest scope: automated DRUM detection is NOT included. A pure-numpy beat heuristic
false-positived on smooth orchestral/pad content (a drone scored as "drums"), and a reliable
detector needs librosa/Demucs (not installed, not worth the dependency here). So percussion is
EAR-checked at the audition gate — the "no drums" prompt tags + a quick listen cover it, and a
stray drum kit on an orchestral bed is obvious. (Wordless "aah" pads also need the ear.)

  python qc.py                 # QC every pending take
  python qc.py --all           # QC every track
  python qc.py sacred_grace_rise_a
  python qc.py --apply         # write has_vocals + qc_notes into the index (still advisory)
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from music_library import MusicLibrary          # noqa: E402
from placer import detect_swell                 # noqa: E402  (reuse)

VOCAL_WORDS_FLAG = 12        # confident transcribed words above which vocals are likely


def vocal_words(path: Path):
    """(count, sample) of confident transcribed words — reuses faster_whisper. None if unavailable."""
    try:
        from faster_whisper import WhisperModel
    except Exception:
        return None, ""
    try:
        model = WhisperModel("small.en", device="cpu", compute_type="int8")
        segs, _ = model.transcribe(str(path), beam_size=1, vad_filter=True)
        words, sample = 0, []
        for s in segs:
            if getattr(s, "no_speech_prob", 1.0) < 0.5 and getattr(s, "avg_logprob", -9) > -1.0:
                txt = s.text.strip()
                words += len(txt.split())
                if len(sample) < 3 and txt:
                    sample.append(txt)
        return words, " | ".join(sample)[:80]
    except Exception as e:
        return None, f"(asr error: {e})"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("slug", nargs="?")
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--apply", action="store_true", help="persist has_vocals + qc_notes to the index")
    ap.add_argument("--no-vocal", action="store_true", help="skip the (slower) Whisper vocal pass")
    a = ap.parse_args()

    lib = MusicLibrary()
    if a.slug:
        tracks = [lib.by_slug(a.slug)] if lib.by_slug(a.slug) else sys.exit(f"no such track: {a.slug}")
    elif a.all:
        tracks = lib.entries
    else:
        tracks = [e for e in lib.entries if e.status == "pending"]
    if not tracks:
        print("[qc] nothing to check (no pending tracks; use --all or a slug)")
        return

    print(f"{'slug':<30}{'mood':<10}{'LUFS':>7}{'swell':>7}  vocals")
    for e in sorted(tracks, key=lambda x: x.slug):
        clip = lib.clip_path(e.slug)
        sw = detect_swell(clip)
        lufs = f"{e.lufs_i}" if e.lufs_i is not None else "?"
        vc, sample = (None, "") if a.no_vocal else vocal_words(clip)
        if vc is None:
            verdict = "(no ASR)"
        elif vc >= VOCAL_WORDS_FLAG:
            verdict = f"!VOCALS?({vc}w)"
        else:
            verdict = "clean"
        print(f"{e.slug:<30}{e.mood:<10}{lufs:>7}{sw:>6.0f}s  {verdict}"
              + (f'   "{sample}"' if sample else ""))
        if a.apply:
            e.has_vocals = bool(vc and vc >= VOCAL_WORDS_FLAG)
            if e.has_vocals:
                e.qc_notes = (e.qc_notes + " | " if e.qc_notes else "") + f"qc: vocals?({vc}w)"
            lib._save()
    print("\nVOCALS flag is reliable (transcribed words = sung lyrics -> reject). DRUMS + wordless "
          "'aah' pads are EAR-checked at audition (no offline detector). swell = climax the placer aligns.")


if __name__ == "__main__":
    main()
