"""Build narration-tagged.md + voices.json + narration.spoken.txt for #04 Bronze Serpent.

The approved+LOCKED narration.md (v1.3) is PLAIN PROSE. Long-form audio
(per_turn_synth) consumes a tagged file + a voice roster. This builder mirrors
#03's, but the cast is 4 voices because BOTH God and Jesus speak in this text:

  - narrator   : the teaching prose
  - scripture  : every KJV quote that is narration / a prophet / John's note
  - god        : Num 21:8 — the LORD's first-person command to Moses (+ its re-quote)
  - jesus      : John 3:14-15 + John 12:32 — Jesus' own words to Nicodemus

KJV spans are matched by their EXACT extracted text (incl. the … ellipsis char),
assigned to a speaker by their 1-based order of appearance in the body. The single
rhetorical word-pointer "whosoever." (span 15) is intentionally NOT wrapped — it
stays narrator, the way #03 left paraphrase-pointers unwrapped.

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

# Speaker per 1-based span index (see the 16 extracted **"..."** quotes).
SPAN_SPEAKER = {
    1: "scripture",   # Num 21:5  — the people murmur
    2: "scripture",   # Num 21:6  — the LORD sent fiery serpents (narration)
    3: "scripture",   # Num 21:7  — the people confess
    4: "god",         # Num 21:8  — "Make thee a fiery serpent…" (first-person command)
    5: "god",         # Num 21:8  — re-quoted promise of life
    6: "scripture",   # Num 21:9  — and Moses made a serpent of brass (narration)
    7: "jesus",       # John 3:14-15 — Jesus to Nicodemus
    8: "jesus",       # John 12:32 — "And I, if I be lifted up…"
    9: "scripture",   # John 12:33 — John's note
    10: "scripture",  # John 3:16 — contested speaker -> scripture, not jesus
    11: "scripture",  # 2 Kings 18:4 — Hezekiah brake the brasen serpent
    12: "scripture",  # 2 Cor 5:21
    13: "scripture",  # Gal 3:13
    14: "scripture",  # 1 Pet 2:24
    # 15: "whosoever." — INTENTIONALLY left narrator (rhetorical pointer)
    16: "scripture",  # John 3:15 fragment embedded in the M7 landing
}

VOICES = {
    "narrator":  {"voice_id": "LSi9zNCeliLuhIGGS0By", "audio_tag": None},  # Grounded Narrator
    "scripture": {"voice_id": "puDRtQWF8NtQiPMJygTb", "audio_tag": None},  # dedicated KJV reader
    "god":       {"voice_id": "UzI1NsMEV3ni5JRkRSls", "audio_tag": None},  # God 1
    "jesus":     {"voice_id": "tlETan7Okc4pzjD0z62P", "audio_tag": None},  # Jesus (existing tree)
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
        "<!-- AUTO-BUILT from narration.md v1.3 by _build_audio_inputs.py — do not hand-edit.\n"
        "     4-voice long-form read: narrator (default) · scripture (KJV narration/prophets) ·\n"
        "     god (Num 21:8 first-person command) · jesus (John 3:14-15 + 12:32, His own words).\n"
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
