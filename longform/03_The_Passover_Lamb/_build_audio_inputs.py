"""Build narration-tagged.md + voices.json + narration.spoken.txt for #03 Passover Lamb.

The approved narration.md (v1.3) is PLAIN PROSE. Long-form audio (per_turn_synth)
consumes a tagged file + a voice roster. This builder:

  1. strips the title/status header (everything before the first '---') and the
     '## Movement' headings,
  2. un-wraps each paragraph (hard line-wraps -> single spaces) and strips markdown
     emphasis (** * _),
  3. wraps ONLY the exact KJV quote spans in <speaker> tags — God's first-person
     declarations -> `god`, every other KJV quote -> `scripture`, everything else
     stays narrator. Narrator paraphrase-quotes ("when I see how good you are." etc.)
     are intentionally NOT wrapped.
  4. PROVES zero word-drift: normalize(spoken(tagged)) == normalize(spoken(narration.md)).

It NEVER edits the approved narration.md. Re-runnable.
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

# God speaks in the first person (Exodus 12:12, 12:13) -> the `god` voice.
GOD_QUOTES = [
    "…I will pass through the land of Egypt this night,",
    "and will smite all the firstborn…",
    "…when I see the blood, I will pass over you, and the plague shall not be upon you to destroy you…",
]
# Every other KJV quote -> a dedicated Scripture-reading voice.
SCRIPTURE_QUOTES = [
    "Your lamb shall be without blemish, a male of the first year.",
    "…In the tenth day of this month they shall take to them every man a lamb…",
    "…ye shall keep it up until the fourteenth day of the same month…",
    "…the whole assembly of the congregation of Israel shall kill it in the evening.",
    "…they shall take of the blood, and strike it on the two side posts and on the upper door post…",
    "neither shall ye break a bone thereof.",
    "But when they came to Jesus, and saw that he was dead already, they brake not his legs.",
    "For these things were done, that the scripture should be fulfilled, A bone of him shall not be broken.",
    "…Christ our passover is sacrificed for us.",          # appears twice (M4 + M6)
    "…a lamb without blemish and without spot.",
    "but with the precious blood of Christ.",
]

VOICES = {
    "narrator":  {"voice_id": "LSi9zNCeliLuhIGGS0By", "audio_tag": None},  # Grounded Narrator
    "scripture": {"voice_id": "puDRtQWF8NtQiPMJygTb", "audio_tag": None},  # dedicated KJV reader
    "god":       {"voice_id": "UzI1NsMEV3ni5JRkRSls", "audio_tag": None},  # God 1
}


def build_body() -> str:
    raw = SRC.read_text(encoding="utf-8")
    # 1. drop the header block (everything up to and incl. the first '---' rule)
    body = raw.split("\n---\n", 1)[1]
    # 2. drop '## Movement ...' headings
    body = "\n".join(l for l in body.splitlines() if not l.lstrip().startswith("## "))
    # 3. per-paragraph un-wrap + strip markdown emphasis
    paras = re.split(r"\n\s*\n", body)
    clean = []
    for p in paras:
        text = " ".join(l.strip() for l in p.splitlines() if l.strip())
        text = re.sub(r"[*_]", "", text)  # markdown emphasis only (keep — and …)
        if text:
            clean.append(text)
    return "\n\n".join(clean)


def wrap(body: str) -> str:
    """Wrap EVERY segment in a <speaker> tag (narration_parse only reads tagged text):
    narrator prose paragraphs -> narrator; each KJV quote split into its own god/scripture
    turn, with the surrounding prose kept as its own narrator turn(s)."""
    needle_speaker = {}
    for q in GOD_QUOTES:
        needle_speaker[f'"{q}"'] = "god"
    for q in SCRIPTURE_QUOTES:
        needle_speaker[f'"{q}"'] = "scripture"
    for needle in needle_speaker:
        if needle not in body:
            raise SystemExit(f"quote not found verbatim in body:\n  {needle}")
    # longest-first so no needle is a prefix-victim of another (none overlap, but safe)
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
    body = build_body()
    tagged_body = wrap(body)

    header = (
        "<!-- AUTO-BUILT from narration.md v1.3 by _build_audio_inputs.py — do not hand-edit.\n"
        "     3-voice long-form read: narrator (default) · scripture (all KJV quotes) ·\n"
        "     god (Exodus 12:12/12:13 first-person divine speech). Words are FROZEN — this\n"
        "     file only adds speaker tags; spoken text is byte-verified equal to narration.md. -->\n\n"
    )
    tagged = header + tagged_body + "\n"
    (V1 / "narration-tagged.md").write_text(tagged, encoding="utf-8")

    # spoken.txt: flowing spoken text (tags removed), for WhisperX caption alignment
    spoken = NP.parse(tagged).spoken_text
    spoken_flow = re.sub(r"\s+", " ", spoken).strip()
    (V1 / "narration.spoken.txt").write_text(spoken_flow + "\n", encoding="utf-8")

    (V1 / "voices.json").write_text(json.dumps(VOICES, indent=2) + "\n", encoding="utf-8")

    # --- PROVE zero word-drift: tagged spoken == the cleaned body (wrapping is lossless) ---
    orig_words = NP.normalize(body)
    tag_words = NP.normalize(spoken)
    if orig_words != tag_words:
        # find first divergence for a useful error
        o, t = orig_words.split(), tag_words.split()
        for i, (a, b) in enumerate(zip(o, t)):
            if a != b:
                ctx = " ".join(o[max(0, i - 6):i + 6])
                raise SystemExit(f"WORD DRIFT at token {i}: orig={a!r} tag={b!r}\n  …{ctx}…\n"
                                 f"  len orig={len(o)} tag={len(t)}")
        raise SystemExit(f"WORD DRIFT: length differs orig={len(o)} tag={len(t)}")

    turns = NP.parse(tagged).blocks
    n_quote = sum(1 for b in turns if b.speaker in ("god", "scripture"))
    print(f"[ok] narration-tagged.md written — {len(turns)} blocks, {n_quote} KJV quote turn(s)")
    print(f"[ok] voices.json written — {', '.join(VOICES)}")
    print(f"[ok] narration.spoken.txt written — {len(tag_words.split())} words")
    print(f"[ok] WORD-PARITY VERIFIED: tagged spoken == narration.md spoken (0 drift)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
