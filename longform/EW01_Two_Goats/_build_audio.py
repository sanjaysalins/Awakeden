"""Build narration-tagged.md + voices.json + narration.spoken.txt for the Awakeden eyewitness
LONG 'The Two Goats' (Aaron). 2-voice: witness (Aaron — the deep weathered voice the user
loved on the pilot) + scripture (the KJV reader for every bold quote, incl. the Lev 16:2 line
Aaron recounts). Enforces the lock guard first (require_lock). Proves 0 word-drift; re-runnable."""
import json, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from cli_witness_lock import require_lock      # noqa: E402  (fail-closed: must be locked)
from pipeline import eyewitness_gates as EW    # noqa: E402

V1 = Path(__file__).resolve().parent / "v1"
SRC = V1 / "narration.md"

VOICES = {
    "witness":   {"voice_id": "UzI1NsMEV3ni5JRkRSls", "audio_tag": None},  # Aaron — deep/weathered
    "scripture": {"voice_id": "puDRtQWF8NtQiPMJygTb", "audio_tag": None},  # dedicated KJV reader
}

_TAG = re.compile(r"^\s*\*\*\[[^\]]+\]\*\*\s*")     # leading **[Speaker]**
_QUOTE = re.compile(r'^\*\*"(.+)"\*\*$')             # a bold KJV quote line


def _voice_and_text(line: str):
    s = line.strip()
    if not s or s == "---" or s.startswith("## ") or s.startswith("# ") or s.startswith("**Witness:**") \
       or s.startswith("**Status:**") or s.startswith("**Core text"):
        return None
    s = _TAG.sub("", s)                              # drop any **[Speaker]** tag (the LORD line -> its quote)
    m = _QUOTE.match(s)
    if m:
        return ("scripture", m.group(1).strip())
    text = re.sub(r"[*_`]", "", s).strip()           # witness prose: strip emphasis markers
    return ("witness", text) if text else None


def main() -> int:
    require_lock(V1, "long")                          # fail-closed: never voice an unlocked narration
    raw = SRC.read_text(encoding="utf-8")
    body = raw.split("\n---", 1)[1]
    blocks: list[tuple[str, str]] = []
    for line in body.splitlines():
        vt = _voice_and_text(line)
        if not vt:
            continue
        if blocks and blocks[-1][0] == vt[0]:
            blocks[-1] = (vt[0], (blocks[-1][1] + " " + vt[1]).strip())
        else:
            blocks.append(vt)

    header = ("<!-- AUTO-BUILT from narration.md (v1.2) by _build_audio.py — Awakeden eyewitness LONG.\n"
              "     2-voice: witness (Aaron, deep) · scripture (all KJV quotes incl. the Lev 16:2 line).\n"
              "     Words FROZEN; this only adds speaker tags; verified == the LOCKED narration.md. -->\n\n")
    tagged = header + "\n".join(f'<speaker name="{v}">{t}</speaker>' for v, t in blocks) + "\n"
    (V1 / "narration-tagged.md").write_text(tagged, encoding="utf-8")

    spoken = re.sub(r"\s+", " ", " ".join(t for _, t in blocks)).strip()
    (V1 / "narration.spoken.txt").write_text(spoken + "\n", encoding="utf-8")
    (V1 / "voices.json").write_text(json.dumps(VOICES, indent=2) + "\n", encoding="utf-8")

    # word-parity vs the LOCKED narration's spoken text
    locked_spoken = EW.parse_witness(raw).spoken_text
    a = re.findall(r"[A-Za-z']+", locked_spoken.lower())
    b = re.findall(r"[A-Za-z']+", spoken.lower())
    if a != b:
        for i, (x, y) in enumerate(zip(a, b)):
            if x != y:
                ctx = " ".join(a[max(0, i-5):i+5])
                raise SystemExit(f"WORD DRIFT at {i}: locked={x!r} tagged={y!r}  …{ctx}…\n  len {len(a)} vs {len(b)}")
        raise SystemExit(f"WORD DRIFT: length {len(a)} vs {len(b)}")

    from collections import Counter
    c = Counter(v for v, _ in blocks)
    print(f"[ok] narration-tagged.md — {len(blocks)} blocks: {dict(c)}")
    print(f"[ok] voices.json — {', '.join(VOICES)}")
    print(f"[ok] WORD-PARITY VERIFIED: tagged == LOCKED narration.md ({len(b)} words, 0 drift)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
