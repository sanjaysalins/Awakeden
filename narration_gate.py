#!/usr/bin/env python
"""narration_gate.py — the EARNED HOOK + EARNED LANDING gate ($0, deterministic).

The chink in the armour (user, 2026-07-03): hooks and landings are the slots where
generic writing hides — "Come to Jesus / turn to Him / look at Jesus, go live" can pass
every doctrine + structure gate we have because no gate asks whether the ending was
EARNED from the piece's own material. This gate makes the floor machine-checkable:

  FAIL  STOCK-CLOSER: the landing uses a stock CTA phrase whose verb the piece's own
        quoted KJV text never uses. ("Look, and live" passes on Zech 12:10 because the
        verse IS "they shall look upon me"; "Come to the cross" fails on Luke 23:34.)
  FAIL  UNEARNED-LANDING: the final sentences share not one significant word with the
        piece's quoted Scripture or its hook — the ending could end any other piece.
  FAIL  TEMPLATE-HOOK: the opening line is a stock template ("Did you know...",
        "What if I told you...", "Imagine...").
  WARN  CORPUS-STALE: the landing's lead imperative verb already closes >=3 existing
        narrations (cross-piece staleness the per-piece gates are blind to).

The ceiling stays with the tournament + the 5-CLI panel (which now scores hook and
landing 1-10 explicitly); this gate only makes lazy impossible, not greatness automatic.

  .venv\\Scripts\\python.exe narration_gate.py "<narration.md>"        # gate one piece
  .venv\\Scripts\\python.exe narration_gate.py --corpus               # sweep everything

Exit 0 = pass (warnings allowed), 1 = FAIL, 2 = could not parse.
"""
from __future__ import annotations
import argparse, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
CORPUS_DIRS = [ROOT / "batches",
               ROOT.parent / "PythonProject1" / "jesus" / "narration"]

STOP = set("""the and that this with unto upon they them thou thee your yours his him her
hath have has shall will not for was were are is be been from into out of a an in on to
as at by it its own so do did does done what when who whom which there their then than
now let all any one may can more most very""".split())

# stock CTA verbs -> the regexes that make them a STOCK closer. The verb is FORGIVEN
# only when the piece's own quoted KJV text uses it (then it is the piece's material).
STOCK_CLOSERS = {
    "come":  r"\bcome (to|unto) (jesus|him|christ|the cross)\b",
    "turn":  r"\bturn to (jesus|him|christ)\b",
    "look":  r"\blook (at|to|upon) (jesus|him|christ|the cross)\b",
    "give":  r"\bgive (your|thy) (life|heart) to\b",
    "trust": r"\b(will you|wilt thou) trust (him|jesus)\b",
    "run":   r"\brun to (jesus|him|the father)\b",
    "accept": r"\baccept (jesus|him|christ)\b",
}
TEMPLATE_HOOKS = (r"^did you know\b", r"^what if i told you\b", r"^imagine\b",
                  r"^have you ever\b", r"^we all know\b", r"^picture this\b")


def _two_line_tagged(raw: list[str]) -> list[str]:
    """Legacy format: a bare **[speaker ...]** label line, spoken text on the NEXT
    line(s). Normalize to single '[speaker] text' lines."""
    out, i = [], 0
    while i < len(raw):
        m = re.match(r"^\*\*\[([^\]]+)\]\*\*:?\s*$", raw[i])
        if m:
            j = i + 1
            while j < len(raw) and not raw[j]:
                j += 1
            if j < len(raw) and not raw[j].startswith(("#", "-", ">", "|", "**[")):
                tag = re.sub(r"[^a-z_ ]", " ", m.group(1).lower()).split()[0] or "narrator"
                out.append(f"[{tag}] {raw[j].strip('\"').strip()}")
                i = j + 1
                continue
        i += 1
    return out


def _spoken(md: str) -> str:
    """Strip headers/labels/markdown down to the spoken text. If the file uses [speaker]
    tags, ONLY tagged lines are spoken (metadata headers like 'Series: ...' never leak
    into the hook)."""
    raw = [ln.strip() for ln in md.splitlines()]
    tagged = [ln for ln in raw if re.match(r"^\[[a-z_ ]+\]\s*\S", ln, flags=re.I)]
    if not tagged:
        tagged = _two_line_tagged(raw)
    lines = []
    for ln in (tagged or raw):
        if not ln or ln.startswith("#") or ln.startswith(">") or ln.startswith("|"):
            continue
        if re.match(r"^\*\*[^*]+\*\*:?\s*$", ln):            # bare **speaker** label
            continue
        if not tagged and re.match(r"^(series|rev|topic|verse|status)\s*:", ln, flags=re.I):
            continue                                          # metadata header lines
        ln = re.sub(r"^\[[a-z_ ]+\]\s*", "", ln, flags=re.I)  # [narrator] tags
        ln = re.sub(r"^\*\*\[?[a-z_ ]+\]?\*\*:?\s*", "", ln, flags=re.I)
        ln = ln.replace("**", "").replace("*", "")
        lines.append(ln)
    return " ".join(lines)


def _sentences(text: str) -> list[str]:
    return [s.strip() for s in re.split(r"(?<=[.!?])\s+", text) if s.strip()]


def _words(text: str) -> set[str]:
    return {w for w in re.findall(r"[a-z']+", text.lower()) if len(w) >= 4 and w not in STOP}


def _quotes(text: str) -> str:
    """Everything inside straight/curly double quotes = the piece's KJV material."""
    return " ".join(re.findall(r"[\"“]([^\"”]+)[\"”]", text))


def _scripture(md: str) -> str:
    """In multi-voice pieces the KJV is spoken by non-narrator voices ([scripture],
    [jesus], [david]...) with no quote marks — those lines ARE the piece's material."""
    raw = [ln.strip() for ln in md.splitlines()]
    lines = [ln for ln in raw if re.match(r"^\[[a-z_ ]+\]\s*\S", ln, flags=re.I)]
    if not lines:
        lines = _two_line_tagged(raw)
    out = []
    for ln in lines:
        m = re.match(r"^\[([a-z_ ]+)\]\s*(\S.*)$", ln.strip(), flags=re.I)
        if m and m.group(1).strip().lower() != "narrator":
            out.append(m.group(2))
    return " ".join(out)


def analyse(path: Path) -> dict:
    md = path.read_text(encoding="utf-8")
    text = _spoken(md)
    sents = _sentences(text)
    if len(sents) < 4:
        return {"error": f"could not parse enough sentences from {path}"}
    hook = " ".join(sents[:2])
    closer = " ".join(sents[-3:])
    kjv = (_quotes(text) + " " + _scripture(md)).strip()
    findings = []

    low = closer.lower()
    for verb, pat in STOCK_CLOSERS.items():
        if re.search(pat, low):
            if re.search(rf"\b{verb}\w*\b", kjv.lower()):
                findings.append(("PASS", f"closer verb '{verb}' is stock-shaped but EARNED: "
                                         f"the piece's own KJV text uses it"))
            else:
                findings.append(("FAIL", f"STOCK-CLOSER: '{verb}' CTA ({pat}) and the piece's "
                                         f"quoted Scripture never uses '{verb}' — the ending "
                                         f"could end any piece. Rebuild it from the thread's "
                                         f"own image/verb."))
    anchor = _words(kjv) | _words(hook)
    shared = _words(" ".join(sents[-2:])) & anchor
    if not shared:
        findings.append(("FAIL", "UNEARNED-LANDING: the final sentences share no significant "
                                 "word with the piece's quoted Scripture or its hook."))
    else:
        findings.append(("PASS", f"landing anchored to the piece's material: {sorted(shared)[:4]}"))
    hlow = hook.lower()
    for pat in TEMPLATE_HOOKS:
        if re.search(pat, hlow):
            findings.append(("FAIL", f"TEMPLATE-HOOK: opens on a stock template ({pat})"))
    return {"path": path, "hook": hook, "closer": sents[-1], "findings": findings}


def corpus_closers() -> dict[str, int]:
    """Lead imperative verb of every existing closer -> count (cross-piece staleness)."""
    counts: dict[str, int] = {}
    for d in CORPUS_DIRS:
        if not d.exists():
            continue
        for p in d.rglob("narration.md"):
            try:
                sents = _sentences(_spoken(p.read_text(encoding="utf-8")))
            except Exception:
                continue
            if not sents:
                continue
            m = re.match(r"^([a-z]+)", sents[-1].lower())
            if m:
                counts[m.group(1)] = counts.get(m.group(1), 0) + 1
    return counts


def gate(path: Path, stale: dict[str, int] | None = None) -> int:
    r = analyse(path)
    if "error" in r:
        print(f"[??] {r['error']}")
        return 2
    def _safe(s):
        return s.encode("ascii", "replace").decode()
    print(f"\n=== {path}")
    print(f"  hook   : {_safe(r['hook'][:110])}")
    print(f"  closer : {_safe(r['closer'][:110])}")
    fails = 0
    for level, msg in r["findings"]:
        print(f"  [{level}] {msg}")
        fails += level == "FAIL"
    if stale:
        m = re.match(r"^([a-z]+)", r["closer"].lower())
        verb = m.group(1) if m else ""
        n = stale.get(verb, 0)
        if n >= 3:
            print(f"  [WARN] CORPUS-STALE: closers opening on '{verb}' already used {n}x in the corpus")
    return 1 if fails else 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("narration", nargs="?", help="path to narration.md")
    ap.add_argument("--corpus", action="store_true", help="sweep every narration.md")
    a = ap.parse_args()
    stale = corpus_closers()
    if a.corpus:
        worst = 0
        for d in CORPUS_DIRS:
            if not d.exists():
                continue
            for p in sorted(d.rglob("narration.md")):
                worst = max(worst, gate(p, stale))
        sys.exit(worst)
    if not a.narration:
        ap.error("give a narration.md or --corpus")
    sys.exit(gate(Path(a.narration), stale))


if __name__ == "__main__":
    main()
