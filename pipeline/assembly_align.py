"""ElevenLabs forced-alignment for the assembly stage (per-word timing).

The shorts audio is synthesized by per_turn_synth WITHOUT word timestamps, so the
assembler only had per-TURN timing (a single narrator turn can be ~25s ≈ a whole
section) — far too coarse to pin a clip under the exact phrase it depicts. This
module runs ElevenLabs forced-alignment over the FINAL muxed narration.mp3 + the
known transcript to recover per-word start/end times on the final timeline, cached
to <v1>/narration.alignment.json.

This is an ElevenLabs call (not Anthropic), so the agent-mode bridge does not apply
and the cost is tiny. The key is read from PythonProject1/.env, which config.py
already loads eagerly (NBP_PROJECT_ENV) into os.environ.
"""
from __future__ import annotations

import json
import os
from dataclasses import dataclass
from pathlib import Path

import config  # noqa: F401  — importing config eagerly loads PythonProject1/.env (ELEVENLABS_API_KEY)


_ALIGN_URL = "https://api.elevenlabs.io/v1/forced-alignment"
ALIGN_CACHE = "narration.alignment.json"

# Word-timing backend: "whisper" (local faster-whisper ASR + transcript alignment, free,
# offline, no key — DEFAULT) or "elevenlabs" (forced-alignment endpoint; needs the key's
# forced_alignment permission). Override with ASSEMBLY_ALIGN_BACKEND.
import os as _os
ALIGN_BACKEND = _os.getenv("ASSEMBLY_ALIGN_BACKEND", "whisper").strip().lower()
WHISPER_MODEL = _os.getenv("ASSEMBLY_WHISPER_MODEL", "base").strip()


@dataclass
class Word:
    text: str
    start: float          # absolute seconds on the final timeline
    end: float

    @property
    def mid(self) -> float:
        return (self.start + self.end) / 2.0


# --------------------------------------------------------------------------
# Transcript (what was actually spoken, in order)
# --------------------------------------------------------------------------
def transcript(v1_folder: Path) -> str:
    """Plain spoken text, in order, speaker/emotion tags stripped — exactly what
    ElevenLabs synthesized. Reuses assembly_timing's tagged-md chunker so the
    transcript matches the audio the timeline is built from."""
    from pipeline.assembly_timing import _parse_tagged_chunks
    tagged = Path(v1_folder) / "narration-tagged.md"
    if not tagged.exists():
        raise SystemExit(f"No narration-tagged.md at {tagged} — cannot align.")
    chunks = _parse_tagged_chunks(tagged)
    return " ".join(t for _sp, t in chunks if t).strip()


# --------------------------------------------------------------------------
# Parse the ElevenLabs response → words
# --------------------------------------------------------------------------
def _parse_words(d: dict) -> list[Word]:
    """Pull word-level timestamps out of an alignment doc. Handles the
    forced-alignment shape (`words: [{text,start,end}]`), and falls back to
    grouping the character stream (either list-of-dicts or the parallel-array
    `with-timestamps` shape) into words on whitespace."""
    words: list[Word] = []
    for w in (d.get("words") or []):
        t = str(w.get("text", "")).strip()
        if not t:
            continue
        try:
            words.append(Word(t, float(w.get("start", 0.0)), float(w.get("end", 0.0))))
        except (TypeError, ValueError):
            continue
    if words:
        return words

    # fallback A: characters as list-of-dicts [{text,start,end}, ...]
    chars = d.get("characters")
    triples: list[tuple[str, float, float]] = []
    if isinstance(chars, list) and chars and isinstance(chars[0], dict):
        for c in chars:
            triples.append((str(c.get("text", "")),
                            float(c.get("start", 0.0) or 0.0),
                            float(c.get("end", 0.0) or 0.0)))
    # fallback B: parallel arrays (the /with-timestamps shape)
    elif isinstance(chars, list) and chars:
        starts = d.get("character_start_times_seconds") or []
        ends = d.get("character_end_times_seconds") or []
        for i, ch in enumerate(chars):
            s = float(starts[i]) if i < len(starts) else 0.0
            e = float(ends[i]) if i < len(ends) else s
            triples.append((str(ch), s, e))

    if triples:
        return _words_from_chars(triples)
    return words


def _words_from_chars(triples: list[tuple[str, float, float]]) -> list[Word]:
    """Group a (char, start, end) stream into words on whitespace."""
    out: list[Word] = []
    cur = ""
    cur_start = None
    cur_end = 0.0
    for ch, s, e in triples:
        if ch.isspace():
            if cur:
                out.append(Word(cur, cur_start or 0.0, cur_end))
                cur, cur_start = "", None
            continue
        if cur_start is None:
            cur_start = s
        cur += ch
        cur_end = e
    if cur:
        out.append(Word(cur, cur_start or 0.0, cur_end))
    return out


# --------------------------------------------------------------------------
# The API call
# --------------------------------------------------------------------------
def _resolve_key() -> str | None:
    """Prefer the key in PythonProject1/.env over any inherited OS environment
    variable. config loads .env with override=False, so a stale Windows env var
    would otherwise shadow a freshly-pasted .env key (the forced-alignment trap)."""
    try:
        from dotenv import dotenv_values
        v = dotenv_values(config.NBP_PROJECT_ENV).get("ELEVENLABS_API_KEY")
        if v and v.strip():
            return v.strip()
    except Exception:
        pass
    return os.getenv("ELEVENLABS_API_KEY")


def _call_elevenlabs(mp3: Path, text: str, log=print) -> dict:
    import requests  # available in this project's venv
    key = _resolve_key()
    if not key:
        raise SystemExit(
            "ELEVENLABS_API_KEY not set — expected in PythonProject1/.env. "
            "Cannot run forced-alignment.")
    with mp3.open("rb") as fh:
        resp = requests.post(
            _ALIGN_URL,
            headers={"xi-api-key": key},
            files={"file": (mp3.name, fh, "audio/mpeg")},
            data={"text": text},
            timeout=180,
        )
    if resp.status_code != 200:
        raise SystemExit(
            f"ElevenLabs forced-alignment failed [{resp.status_code}]: {resp.text[:400]}")
    return resp.json()


# --------------------------------------------------------------------------
# Local whisper backend (free, offline) — ASR word times aligned to the KNOWN
# transcript so phrases keep the exact script text + punctuation.
# --------------------------------------------------------------------------
import re as _re

_MODEL_CACHE: dict = {}


def _whisper_asr(mp3: Path, log=print) -> list[Word]:
    """Transcribe with faster-whisper and return its word stream (text+times)."""
    from faster_whisper import WhisperModel
    model = _MODEL_CACHE.get(WHISPER_MODEL)
    if model is None:
        log(f"      [align] loading faster-whisper '{WHISPER_MODEL}' (first run downloads it)...")
        model = WhisperModel(WHISPER_MODEL, device="cpu", compute_type="int8")
        _MODEL_CACHE[WHISPER_MODEL] = model
    segs, _info = model.transcribe(str(mp3), language="en", word_timestamps=True)
    out: list[Word] = []
    for seg in segs:
        for w in (seg.words or []):
            t = (w.word or "").strip()
            if t:
                out.append(Word(t, float(w.start or 0.0), float(w.end or 0.0)))
    return out


def _norm_tok(t: str) -> str:
    return _re.sub(r"[^a-z0-9']", "", t.lower())


def _align_known_to_asr(known_text: str, asr: list[Word]) -> list[Word]:
    """Map ASR word times onto the KNOWN transcript words (forced-alignment-style),
    so the phrase board keeps the exact script text + punctuation. Matches the two
    word sequences and assigns each known word the time of its ASR counterpart;
    unmatched/replaced spans are interpolated across the ASR span; gaps carry the
    previous end."""
    import difflib
    known = known_text.split()
    a = [_norm_tok(w.text) for w in asr]
    b = [_norm_tok(t) for t in known]
    times: list[tuple[float, float] | None] = [None] * len(known)
    sm = difflib.SequenceMatcher(a=a, b=b, autojunk=False)
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag == "equal":
            for k in range(j2 - j1):
                w = asr[i1 + k]
                times[j1 + k] = (w.start, w.end)
        elif tag == "replace":
            span = asr[i1:i2]
            if span:
                s0, e0 = span[0].start, span[-1].end
                n = max(1, j2 - j1)
                for k in range(j2 - j1):
                    times[j1 + k] = (s0 + (e0 - s0) * k / n, s0 + (e0 - s0) * (k + 1) / n)
        # "delete" = extra ASR words (skip); "insert" = known words with no ASR (leave None)
    out: list[Word] = []
    last_end = 0.0
    for tok, tm in zip(known, times):
        if tm is None:
            s = e = last_end
        else:
            s, e = max(tm[0], last_end), max(tm[1], tm[0])
        out.append(Word(tok, round(s, 3), round(max(e, s), 3)))
        last_end = out[-1].end
    return out


def _whisper_align(mp3: Path, text: str, log=print) -> list[Word]:
    asr = _whisper_asr(mp3, log=log)
    log(f"      [align] whisper ASR: {len(asr)} words -> aligning to {len(text.split())} script words")
    return _align_known_to_asr(text, asr)


# --------------------------------------------------------------------------
# Public entry point (idempotent on the cache)
# --------------------------------------------------------------------------
def align(v1_folder: Path, force: bool = False, log=print) -> list[Word]:
    """Return per-word timestamps for <v1>/narration.mp3, caching the raw
    ElevenLabs response to narration.alignment.json. Idempotent: a cache with
    parseable words is reused unless force=True."""
    v1_folder = Path(v1_folder)
    cache = v1_folder / ALIGN_CACHE
    mp3 = v1_folder / "narration.mp3"
    if not mp3.exists():
        raise SystemExit(f"No narration.mp3 at {mp3} — run the audio stage first.")

    if cache.exists() and not force:
        try:
            words = _parse_words(json.loads(cache.read_text(encoding="utf-8")))
            if words:
                log(f"      [align] reuse {cache.name} ({len(words)} words)")
                return words
        except Exception:
            pass  # fall through to a fresh alignment

    text = transcript(v1_folder)
    if ALIGN_BACKEND == "whisper":
        words = _whisper_align(mp3, text, log=log)
        doc = {"backend": "whisper", "model": WHISPER_MODEL,
               "words": [{"text": w.text, "start": w.start, "end": w.end} for w in words]}
    else:
        log(f"      [align] ElevenLabs forced-alignment over {mp3.name} "
            f"({len(text)} chars of transcript)...")
        doc = _call_elevenlabs(mp3, text, log=log)
        words = _parse_words(doc)
    if not words:
        cache.write_text(json.dumps(doc, ensure_ascii=False, indent=2), encoding="utf-8")
        raise SystemExit(
            f"Alignment returned no usable word timestamps (wrote raw to {cache.name}).")
    cache.write_text(json.dumps(doc, ensure_ascii=False, indent=2), encoding="utf-8")
    log(f"      [align] {len(words)} word timestamps ({ALIGN_BACKEND}) -> {cache.name}")
    return words
