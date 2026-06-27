"""Generic 3-voice audio-input builder for ANY Awakeden eyewitness narration (long OR short).

Routes by the **[Speaker]** tag in narration.md:
  - **[the LORD]** "..."  -> the_LORD  (God 2 — distinct divine voice, NOT the witness)
  - **[Jesus]**    "..."  -> jesus
  - **[the kinsman]** ".."-> kinsman
  - bare **"..."**        -> scripture (the KJV reader)
  - untagged prose        -> witness  (the witness lead; default = the user-loved UzI1Ns)

Fail-closed on the lock; proves 0 word-drift vs the LOCKED narration.md; re-runnable.
Usage:  python _build_eyewitness_audio.py <v1-or-short-folder> --form long|short
"""
import argparse, json, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from cli_witness_lock import require_lock      # noqa: E402
from pipeline import eyewitness_gates as EW    # noqa: E402

# 3-voice (+named) cast. Witness = the loved deep voice; God 2 = the user-picked distinct divine voice.
WITNESS_VOICE = "UzI1NsMEV3ni5JRkRSls"   # Aaron/witness — deep, weathered (user-loved)
VOICES = {
    "witness":   {"voice_id": WITNESS_VOICE,            "audio_tag": None},
    "scripture": {"voice_id": "puDRtQWF8NtQiPMJygTb",   "audio_tag": None},  # KJV reader
    "the_LORD":  {"voice_id": "BvKkUzf75BfURv388O3G",   "audio_tag": None},  # God 2 (user-picked)
    "jesus":     {"voice_id": "tlETan7Okc4pzjD0z62P",   "audio_tag": None},  # established Jesus voice
    "kinsman":   {"voice_id": "LSi9zNCeliLuhIGGS0By",   "audio_tag": None},  # nearer kinsman (EW09)
}

# a bold KJV quote span, with an OPTIONAL leading **[Speaker]** — matches inline OR own-line
_QSPAN = re.compile(r'(?:\*\*\[(?P<tag>[^\]]+)\]\*\*\s*)?\*\*"(?P<q>[^"]+)"\*\*')

def _role_for_tag(tag: str) -> str:
    t = tag.strip().lower().replace("the ", "").replace("_", " ").strip()
    if t in ("lord", "god"):       return "the_LORD"
    if t in ("jesus", "christ"):   return "jesus"
    if "kinsman" in t:             return "kinsman"
    return "scripture"             # unknown tag -> reader

def _clean_prose(t: str) -> str:
    lines = [ln for ln in t.splitlines() if not ln.strip().startswith("#") and ln.strip() != "---"]
    t = re.sub(r"[*_`]", "", " ".join(lines))
    return re.sub(r"\s+", " ", t).strip()

def build_blocks(body: str) -> list[tuple[str, str]]:
    """Span-based: split body into witness prose + each bold quote (routed by its tag), inline or own-line."""
    blocks: list[tuple[str, str]] = []
    def add(role: str, text: str):
        text = text.strip()
        if not text or not re.search(r"[A-Za-z]", text):   # skip empty / pure-punctuation (e.g. a lone "—")
            return
        if blocks and blocks[-1][0] == role:
            blocks[-1] = (role, (blocks[-1][1] + " " + text).strip())
        else:
            blocks.append((role, text))
    pos = 0
    for m in _QSPAN.finditer(body):
        add("witness", _clean_prose(body[pos:m.start()]))
        role = _role_for_tag(m.group("tag")) if m.group("tag") else "scripture"
        add(role, m.group("q").strip())
        pos = m.end()
    add("witness", _clean_prose(body[pos:]))
    return blocks

def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("folder")
    ap.add_argument("--form", choices=["long", "short"], required=True)
    ap.add_argument("--witness-voice", default=WITNESS_VOICE)
    args = ap.parse_args()
    folder = Path(args.folder).resolve()
    require_lock(folder, args.form)               # fail-closed
    VOICES["witness"]["voice_id"] = args.witness_voice

    raw = (folder / "narration.md").read_text(encoding="utf-8")
    body = raw.split("\n---", 1)[1]
    blocks = build_blocks(body)

    used = {v for v, _ in blocks}
    roster = {k: VOICES[k] for k in VOICES if k in used}
    header = (f"<!-- AUTO-BUILT from narration.md by _build_eyewitness_audio.py — eyewitness {args.form.upper()}.\n"
              f"     voices: {', '.join(roster)} (witness != the_LORD; God 2 on divine lines).\n"
              "     Words FROZEN; only speaker tags added; verified == the LOCKED narration.md. -->\n\n")
    tagged = header + "\n".join(f'<speaker name="{v}">{t}</speaker>' for v, t in blocks) + "\n"
    (folder / "narration-tagged.md").write_text(tagged, encoding="utf-8")
    spoken = re.sub(r"\s+", " ", " ".join(t for _, t in blocks)).strip()
    (folder / "narration.spoken.txt").write_text(spoken + "\n", encoding="utf-8")
    (folder / "voices.json").write_text(json.dumps(roster, indent=2) + "\n", encoding="utf-8")

    # word-parity vs LOCKED spoken text
    a = re.findall(r"[A-Za-z']+", EW.parse_witness(raw).spoken_text.lower())
    b = re.findall(r"[A-Za-z']+", spoken.lower())
    if a != b:
        for i, (x, y) in enumerate(zip(a, b)):
            if x != y:
                raise SystemExit(f"WORD DRIFT at {i}: locked={x!r} tagged={y!r} (len {len(a)} vs {len(b)})")
        raise SystemExit(f"WORD DRIFT: length {len(a)} vs {len(b)}")

    from collections import Counter
    print(f"[ok] {folder.name}: {len(blocks)} blocks {dict(Counter(v for v, _ in blocks))}; "
          f"roster={list(roster)}; {len(b)} words, 0 drift")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
