"""WhisperX forced alignment — exact word timings for long-form.

faster_whisper's ``word_timestamps`` drop words under a music bed (Isaiah 53:
heard 1171 of ~1643) and the missing words get interpolated, which drifts the
captions. WhisperX adds a phoneme-level (wav2vec2) forced-alignment pass that
snaps every word to the audio.

Two entry points:

* ``transcribe_align`` — ASR + phoneme align. Much higher recall + frame-accurate
  times than faster_whisper. Use when the exact script is unknown.

* ``forced_align_script`` — THE exact path when the KJV script is known. It uses
  the ASR only to find rough time windows, then force-aligns the *script's own
  words* to the audio. Dropped-by-ASR words are recovered (the aligner finds them
  acoustically) and nothing is ever interpolated, so timing is exact.

CPU-only, offline after the one-time model download. No metered API.
"""

from __future__ import annotations

import difflib
import re
from pathlib import Path

_WORD_RE = re.compile(r"[A-Za-z0-9']+")

_MODEL_CACHE: dict = {}
_ALIGN_CACHE: dict = {}


def _key(token: str) -> str:
    return "".join(_WORD_RE.findall(token.lower()))


def _lang_of(model_size: str) -> str:
    return "en" if model_size.endswith(".en") else "en"     # English-only project


def _load_asr(model_size: str):
    if model_size not in _MODEL_CACHE:
        import whisperx
        _MODEL_CACHE[model_size] = whisperx.load_model(
            model_size, device="cpu", compute_type="int8", language=_lang_of(model_size))
    return _MODEL_CACHE[model_size]


def _load_align(language: str):
    if language not in _ALIGN_CACHE:
        import whisperx
        _ALIGN_CACHE[language] = whisperx.load_align_model(
            language_code=language, device="cpu")
    return _ALIGN_CACHE[language]


def _backfill_times(words: list[dict]) -> list[dict]:
    """WhisperX occasionally emits a word with no start/end (e.g. a bare number).
    Carry timing from neighbours so every word has a monotonic window."""
    n = len(words)
    for i, wd in enumerate(words):
        if wd.get("start") is None or wd.get("end") is None:
            prev_end = words[i - 1]["end"] if i > 0 and words[i - 1].get("end") is not None else None
            nxt_start = None
            for j in range(i + 1, n):
                if words[j].get("start") is not None:
                    nxt_start = words[j]["start"]
                    break
            s = prev_end if prev_end is not None else (nxt_start if nxt_start is not None else 0.0)
            e = nxt_start if nxt_start is not None else s + 0.20
            if e <= s:
                e = s + 0.10
            wd["start"], wd["end"] = float(s), float(e)
    return words


def _monotonic(words: list[dict]) -> list[dict]:
    """Force a strictly non-overlapping, forward timeline.

    Independent per-window forced alignment can place a new window's first word
    a few tenths *before* the previous window's last word (seam overlap), which
    would flash two caption phrases at once. Clamp each word to start no earlier
    than the previous word ended, keeping a minimum visible duration.
    """
    prev_end = 0.0
    for wd in words:
        s = max(float(wd["start"]), prev_end)
        e = max(float(wd["end"]), s + 0.05)
        wd["start"], wd["end"] = round(s, 3), round(e, 3)
        prev_end = e
    return words


def _flatten(aligned: dict) -> list[dict]:
    out: list[dict] = []
    for seg in aligned.get("segments", []):
        for w in seg.get("words", []):
            tok = (w.get("word") or "").strip()
            if tok:
                out.append({"w": tok, "start": w.get("start"), "end": w.get("end")})
    return _monotonic(_backfill_times(out))


def transcribe_align(wav_path: str, model_size: str = "small.en",
                     language: str | None = None, _audio=None) -> list[dict]:
    """ASR + phoneme forced alignment. Returns [{w, start, end}] (accurate)."""
    import whisperx
    lang = language or _lang_of(model_size)
    audio = _audio if _audio is not None else whisperx.load_audio(wav_path)
    result = _load_asr(model_size).transcribe(audio, batch_size=8)
    lang = result.get("language", lang)
    align_model, metadata = _load_align(lang)
    aligned = whisperx.align(result["segments"], align_model, metadata, audio,
                             "cpu", return_char_alignments=False)
    return _flatten(aligned)


def _provisional_times(asr_words: list[dict], script_tokens: list[str]) -> list[float]:
    """A rough, monotonic time per SCRIPT token, from the ASR word times.

    Matched script tokens take the ASR word's start; unmatched runs (ASR missed
    them) are linearly interpolated between the surrounding anchors.
    """
    n = len(script_tokens)
    times: list[float | None] = [None] * n
    if asr_words:
        a_keys = [_key(w["w"]) for w in asr_words]
        s_keys = [_key(t) for t in script_tokens]
        for tag, i1, i2, j1, j2 in difflib.SequenceMatcher(
                None, a_keys, s_keys, autojunk=False).get_opcodes():
            if tag in ("equal", "replace"):
                m = min(i2 - i1, j2 - j1)
                for k in range(m):
                    times[j1 + k] = float(asr_words[i1 + k]["start"])
    # interpolate the Nones (and clamp monotonic)
    last_t = 0.0
    last_i = -1
    end_t = float(asr_words[-1]["end"]) if asr_words else float(n)
    for i in range(n):
        if times[i] is not None:
            if last_i < i - 1:                     # fill the gap before this anchor
                span = times[i] - last_t
                for k in range(last_i + 1, i):
                    times[k] = last_t + span * (k - last_i) / (i - last_i)
            last_t, last_i = times[i], i
    for k in range(last_i + 1, n):                 # tail
        times[k] = last_t + (end_t - last_t) * (k - last_i) / max(1, n - last_i)
    out, prev = [], 0.0
    for t in times:
        t = max(prev, float(t))
        out.append(t)
        prev = t
    return out


def _bucket_segments(script_tokens: list[str], prov: list[float],
                     total_dur: float, max_words: int = 10, pad: float = 0.6
                     ) -> list[dict]:
    """Group script tokens into short windows for the phoneme aligner.

    Breaks on sentence-ending punctuation OR every ``max_words``, so each window
    is a few seconds — short enough for accurate wav2vec2 alignment, with padded
    edges so a slightly-off provisional boundary never clips a word.
    """
    segs: list[dict] = []
    cur: list[str] = []
    cur_start_i = 0
    for i, tok in enumerate(script_tokens):
        cur.append(tok)
        ends_sentence = tok.endswith((".", "!", "?", ";", ":"))
        if len(cur) >= max_words or ends_sentence or i == len(script_tokens) - 1:
            s = max(0.0, prov[cur_start_i] - pad)
            e = min(total_dur, prov[i] + pad)
            if e <= s:
                e = min(total_dur, s + 0.30)
            segs.append({"start": s, "end": e, "text": " ".join(cur)})
            cur, cur_start_i = [], i + 1
    return segs


def forced_align_script(wav_path: str, script_text: str,
                        model_size: str = "small.en",
                        language: str | None = None) -> list[dict]:
    """EXACT path: force-align the known script's words to the audio.

    ASR is used only to bound rough time windows; the wav2vec2 pass then places
    every SCRIPT word acoustically, recovering ASR-dropped words with correct
    timing and interpolating nothing. Returns [{w, start, end}].
    """
    import whisperx
    lang = language or _lang_of(model_size)
    audio = whisperx.load_audio(wav_path)
    total_dur = float(len(audio)) / 16000.0

    asr_words = transcribe_align(wav_path, model_size, lang, _audio=audio)

    script_tokens = [t for t in script_text.split() if _key(t)]
    if not script_tokens:
        return asr_words

    prov = _provisional_times(asr_words, script_tokens)
    segs = _bucket_segments(script_tokens, prov, total_dur)

    align_model, metadata = _load_align(lang)
    aligned = whisperx.align(segs, align_model, metadata, audio, "cpu",
                             return_char_alignments=False)
    words = _flatten(aligned)

    # report how complete the exact alignment is (no interpolation used)
    print(f"  forced-aligned {len(words)} script words "
          f"(ASR heard {len(asr_words)}; script has {len(script_tokens)})")
    return words
