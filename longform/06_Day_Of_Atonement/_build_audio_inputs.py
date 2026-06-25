"""Build narration-tagged.md + voices.json + narration.spoken.txt for #06 The Two Goats.

The LOCKED narration.md (v1.2) is PLAIN PROSE. Long-form audio (per_turn_synth)
consumes a tagged file + a voice roster. Mirrors #05's builder. Cast = 3 voices:

  - narrator   : the teaching prose
  - scripture  : the dedicated KJV reader — ALL quoted verses (Lev 16/17, Heb,
                 Isa 53:6, Mt 27:51, Ps 103:12) AND the narrative attribution
                 frame of Lev 16:2 ("And the LORD said unto Moses,")
  - god        : the LORD's own first-person command in Lev 16:2 ("Speak unto
                 Aaron thy brother… that he die not: for I will appear in the
                 cloud upon the mercy seat.") — the only divine speech in the text

Span 1 (Lev 16:2) is SPLIT at "Speak unto Aaron" so the frame stays scripture
and the divine command carries the god voice (the #05 frame->scripture rule,
applied within a single bold quote). All other 17 spans -> scripture.

PROVES zero word-drift, NEVER edits the approved narration.md. Re-runnable.
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from pipeline import narration_parse as NP  # noqa: E402

V1 = Path(__file__).resolve().parent / "v1"
SRC = V1 / "narration.md"

# Speaker per 1-based span index over the 18 extracted **"..."** quotes.
# Span 1 (Lev 16:2) is handled specially (split) — see build_needles().
SPAN_SPEAKER = {i: "scripture" for i in range(2, 19)}

VOICES = {
    "narrator":  {"voice_id": "LSi9zNCeliLuhIGGS0By", "audio_tag": None},  # Grounded Narrator
    "scripture": {"voice_id": "puDRtQWF8NtQiPMJygTb", "audio_tag": None},  # dedicated KJV reader
    "god":       {"voice_id": "UzI1NsMEV3ni5JRkRSls", "audio_tag": None},  # the LORD
}

SPLIT_AT = "Speak unto Aaron"  # split point inside Lev 16:2 (span 1)


def extract_spans(raw: str) -> list[str]:
    body = raw.split("\n---\n", 1)[1]
    spans = re.findall(r'\*\*"(.*?)"\*\*', body, flags=re.S)
    return [" ".join(m.split()) for m in spans]


def build_needles(raw: str) -> dict[str, str]:
    """Return {needle '"quote"' : speaker}, with span 1 split scripture|god."""
    spans = extract_spans(raw)
    ns: dict[str, str] = {}
    # Span 1 — Lev 16:2, split at SPLIT_AT
    s1 = spans[0]
    if SPLIT_AT not in s1:
        raise SystemExit(f"split point {SPLIT_AT!r} not in span 1:\n  {s1}")
    pre, post = s1.split(SPLIT_AT, 1)
    needle_frame = f'"{pre}'.rstrip()                 # '"And the LORD said unto Moses,'
    needle_cmd = f'{SPLIT_AT}{post}"'                 # 'Speak unto Aaron ... mercy seat."'
    ns[needle_frame] = "scripture"
    ns[needle_cmd] = "god"
    # Spans 2..18
    for i, q in enumerate(spans[1:], start=2):
        spk = SPAN_SPEAKER.get(i)
        if spk:
            ns[f'"{q}"'] = spk
    return ns


def build_body() -> str:
    raw = SRC.read_text(encoding="utf-8")
    body = raw.split("\n---\n", 1)[1]
    body = "\n".join(l for l in body.splitlines() if not l.lstrip().startswith("## "))
    paras = re.split(r"\n\s*\n", body)
    clean = []
    for p in paras:
        text = " ".join(l.strip() for l in p.splitlines() if l.strip())
        text = re.sub(r"[*_]", "", text)  # markdown emphasis only (keep — and …)
        if text:
            clean.append(text)
    return "\n\n".join(clean)


def wrap(body: str, needle_speaker: dict[str, str]) -> str:
    for needle in needle_speaker:
        if needle not in body:
            raise SystemExit(f"quote not found verbatim in body:\n  {needle}")
    pat = re.compile("(" + "|".join(re.escape(n) for n in
                     sorted(needle_speaker, key=len, reverse=True)) + ")")
    out_paras = []
    for para in body.split("\n\n"):
        lines = []
        for piece in pat.split(para):
            if not piece.strip():
                continue
            if piece in needle_speaker:
                lines.append(f'<speaker name="{needle_speaker[piece]}">{piece}</speaker>')
            else:
                lines.append(f'<speaker name="narrator">{piece.strip()}</speaker>')
        if lines:
            out_paras.append("\n".join(lines))
    return "\n\n".join(out_paras)


def main() -> int:
    raw = SRC.read_text(encoding="utf-8")
    needle_speaker = build_needles(raw)
    body = build_body()
    tagged_body = wrap(body, needle_speaker)

    header = (
        "<!-- AUTO-BUILT from narration.md v1.2 by _build_audio_inputs.py — do not hand-edit.\n"
        "     3-voice long-form read: narrator (default) · scripture (KJV reader, all quotes +\n"
        "     the Lev 16:2 frame) · god (the LORD's command in Lev 16:2).\n"
        "     Words are FROZEN — this file only adds speaker tags; spoken text is verified\n"
        "     equal to the LOCKED narration.md. -->\n\n"
    )
    tagged = header + tagged_body + "\n"
    (V1 / "narration-tagged.md").write_text(tagged, encoding="utf-8")

    spoken = NP.parse(tagged).spoken_text
    spoken_flow = re.sub(r"\s+", " ", spoken).strip()
    (V1 / "narration.spoken.txt").write_text(spoken_flow + "\n", encoding="utf-8")

    (V1 / "voices.json").write_text(json.dumps(VOICES, indent=2) + "\n", encoding="utf-8")

    orig_words = NP.normalize(body)
    tag_words = NP.normalize(spoken)
    if orig_words != tag_words:
        o, t = orig_words.split(), tag_words.split()
        for i, (a, b) in enumerate(zip(o, t)):
            if a != b:
                ctx = " ".join(o[max(0, i - 6):i + 6])
                raise SystemExit(f"WORD DRIFT at token {i}: orig={a!r} tag={b!r}\n  …{ctx}…\n"
                                 f"  len orig={len(o)} tag={len(t)}")
        raise SystemExit(f"WORD DRIFT: length differs orig={len(o)} tag={len(t)}")

    turns = NP.parse(tagged).blocks
    by_spk = {}
    for b in turns:
        by_spk[b.speaker] = by_spk.get(b.speaker, 0) + 1
    print(f"[ok] narration-tagged.md — {len(turns)} blocks: " +
          ", ".join(f"{k}={v}" for k, v in sorted(by_spk.items())))
    print(f"[ok] voices.json — {', '.join(VOICES)}")
    print(f"[ok] narration.spoken.txt — {len(tag_words.split())} words")
    print(f"[ok] WORD-PARITY VERIFIED: tagged spoken == LOCKED narration.md (0 drift)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
