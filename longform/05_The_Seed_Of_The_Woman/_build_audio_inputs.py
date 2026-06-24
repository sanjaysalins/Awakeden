"""Build narration-tagged.md + voices.json + narration.spoken.txt for #05 Seed of the Woman.

The approved+LOCKED narration.md (v1.1) is PLAIN PROSE. Long-form audio
(per_turn_synth) consumes a tagged file + a voice roster. This builder mirrors
#04's, but the cast is 3 voices — only the LORD speaks in this text:

  - narrator   : the teaching prose
  - scripture  : KJV narration / Eve / the NT quotes (Gal 4:4, Luke 1:35 angel,
                 Rev 12:9, 1 John 3:8, Rom 16:20, Heb 2:14, Col 2:15) + the M6
                 analytical re-quote of Gen 3:15
  - god        : the LORD's own speech — Gen 3:9 ("Where art thou?") and
                 Gen 3:15 ("And I will put enmity…"), the divine promise itself

KJV spans are matched by their EXACT extracted text, assigned to a speaker by
their 1-based order of appearance in the body. The 2-word pointer "her seed"
(span 6) is intentionally NOT wrapped — it stays narrator, the way #04 left the
"whosoever." pointer. Span 4 (Gen 3:14) carries the narrative frame "And the LORD
God said unto the serpent," so it reads as scripture, not the god voice.

PROVES zero word-drift, and NEVER edits the approved narration.md. Re-runnable.
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

# Speaker per 1-based span index (see the 14 extracted **"..."** quotes).
SPAN_SPEAKER = {
    1: "scripture",   # Gen 3:8  — they heard the voice of the LORD God (narration)
    2: "god",         # Gen 3:9  — "Where art thou?" (the LORD's own question)
    3: "scripture",   # Gen 3:13 — Eve: "The serpent beguiled me…" (no Eve voice)
    4: "scripture",   # Gen 3:14 — carries the frame "And the LORD God said unto the serpent,"
    5: "god",         # Gen 3:15 — "And I will put enmity…" (the divine promise, first person)
    # 6: "her seed" — INTENTIONALLY left narrator (2-word rhetorical pointer)
    7: "scripture",   # Gal 4:4
    8: "scripture",   # Luke 1:35 — the angel to Mary (no angel voice)
    9: "scripture",   # Rev 12:9
    10: "scripture",  # 1 John 3:8
    11: "scripture",  # Rom 16:20
    12: "scripture",  # Gen 3:15 fragment re-quoted analytically in M6
    13: "scripture",  # Heb 2:14
    14: "scripture",  # Col 2:15
}

VOICES = {
    "narrator":  {"voice_id": "LSi9zNCeliLuhIGGS0By", "audio_tag": None},  # Grounded Narrator
    "scripture": {"voice_id": "puDRtQWF8NtQiPMJygTb", "audio_tag": None},  # dedicated KJV reader
    "god":       {"voice_id": "UzI1NsMEV3ni5JRkRSls", "audio_tag": None},  # God 1 (the LORD)
}


def extract_spans(raw: str) -> dict[str, str]:
    """Return {needle '"quote"' : speaker} for every assigned span, exact text."""
    body = raw.split("\n---\n", 1)[1]
    spans = re.findall(r'\*\*"(.*?)"\*\*', body, flags=re.S)
    needle_speaker = {}
    for i, m in enumerate(spans, 1):
        spk = SPAN_SPEAKER.get(i)
        if not spk:
            continue
        q = " ".join(m.split())          # normalize internal whitespace (matches build_body)
        needle_speaker[f'"{q}"'] = spk
    return needle_speaker


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
    needle_speaker = extract_spans(raw)
    body = build_body()
    tagged_body = wrap(body, needle_speaker)

    header = (
        "<!-- AUTO-BUILT from narration.md v1.1 by _build_audio_inputs.py — do not hand-edit.\n"
        "     3-voice long-form read: narrator (default) · scripture (KJV narration/NT quotes) ·\n"
        "     god (Gen 3:9 + 3:15, the LORD's own speech).\n"
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
