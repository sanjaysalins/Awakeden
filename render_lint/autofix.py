#!/usr/bin/env python
"""LAYER 2 — deterministic PROMPT auto-fix (positivize). Run BEFORE spending a render credit.

The rules in rules.json already know the fixes; this applies the SAFE, unambiguous ones
mechanically so a bad token never reaches the model in the first place:

  - candle / lantern / candlestick / sconce / glass-globe lamp  ->  clay oil lamp
  - dice / dominoes / tiles / game pieces                        ->  carved knucklebone astragali
  - foreign art-style words (anime, ukiyo-e/Hokusai, watercolour, photoreal, oil painting, ...)
        -> stripped (rely on the project INK house style)
  - classical / Islamic / medieval architecture (parthenon, colonnade, onion dome, minaret,
        gothic, leaded glass, crenellated, steeple, church) -> flat-roofed limestone building
  - negation clauses ("no text", "without nails", "never a cross") -> stripped
        (seedream has no negative channel — naming a noun to forbid it DRAWS it)

The RISKY rewrite (the passion 'nail' -> describe only the wound) is NOT auto-applied because it
needs context; it is surfaced as guidance instead (lint.py still BLOCKs the word, and
redteam_brief() carries the pure-positive rewrite). This module never invents doctrine; it only
swaps a known-poison token for the known-good positive end-state.

  .venv\\Scripts\\python.exe -m render_lint.autofix --prompt "…"
  .venv\\Scripts\\python.exe -m render_lint.autofix --file prompt.txt

  from render_lint.autofix import positivize
  fixed, changes, guidance = positivize(prompt)
"""
from __future__ import annotations
import argparse, re, sys
from pathlib import Path

# (regex, replacement, rule_id) — SAFE 1:1 swaps only. Order matters (specific before generic).
_SWAPS: list[tuple[str, str, str]] = [
    # --- light source: candle / lantern family -> clay oil lamp (consume leading adjectives) ---
    (r"\b(?:a\s+)?(?:glass|metal|iron|brass|tin)?[- ]?(?:globe[- ]?|chimney[- ]?)?(?:hurricane|kerosene|carriage|storm)?[- ]?lanterns?\b", "a clay oil lamp", "no-glass-or-metal-lantern"),
    (r"\b(?:a\s+)?glass[- ]?(?:globe|chimney)[- ]?lamp\b", "a clay oil lamp", "no-glass-or-metal-lantern"),
    (r"\b(?:hurricane|kerosene|carriage|storm)\s+lamp\b", "clay oil lamp", "no-glass-or-metal-lantern"),
    (r"\b(?:candlesticks?|candelabra|chambersticks?|sconces?)\b", "clay oil lamp", "no-glass-or-metal-lantern"),
    (r"\bcandle ?lights?\b", "warm oil-lamp light", "no-freestanding-candle-outdoors"),
    (r"\bcandles?\b", "clay oil lamp", "no-freestanding-candle-outdoors"),
    # --- lots -> knucklebone astragali ---
    (r"\bdomino(?:es)?\b", "carved knucklebone astragali", "lots-are-knucklebones-not-dominoes"),
    (r"\b(?:dice|game\s+pieces?|gaming\s+tiles?)\b", "carved knucklebone astragali", "lots-are-knucklebones-not-dominoes"),
    # --- architecture: classical / Islamic / medieval -> period stone ---
    (r"\b(?:the\s+)?parthenon\b", "a flat-roofed limestone building", "no-classical-or-islamic-or-medieval-skyline"),
    (r"\bacropolis\b", "a flat-roofed limestone town", "no-classical-or-islamic-or-medieval-skyline"),
    (r"\b(?:corinthian|ionic|doric)\s+(?:columns?|colonnades?|pillars?)\b", "plain stone pillars", "no-classical-or-islamic-or-medieval-skyline"),
    (r"\bcolonnades?\b", "a plain stone wall", "no-classical-or-islamic-or-medieval-skyline"),
    (r"\bpediments?\b", "a flat stone lintel", "no-classical-or-islamic-or-medieval-skyline"),
    (r"\bdome of the rock\b", "the plain Second-Temple stone platform", "no-classical-or-islamic-or-medieval-skyline"),
    (r"\b(?:a\s+)?(?:great\s+)?(?:golden|gold|onion|bulbous)\s+(?:onion\s+)?domes?\b", "a flat stone roof", "no-classical-or-islamic-or-medieval-skyline"),
    (r"\bdomed?\s+(?:roof|building|temple|structure)\b", "a flat-roofed stone building", "no-classical-or-islamic-or-medieval-skyline"),
    (r"\bminarets?\b", "a plain stone tower", "no-classical-or-islamic-or-medieval-skyline"),
    (r"\bpointed(?:\s+gothic)?\s+arch(?:es)?\b", "a round stone arch", "no-classical-or-islamic-or-medieval-skyline"),
    (r"\bgothic\b", "plain stone", "no-classical-or-islamic-or-medieval-skyline"),
    (r"\b(?:leaded|lattice|stained)\s+glass\b", "an unglazed window opening", "no-classical-or-islamic-or-medieval-skyline"),
    (r"\b(?:crenellat|castellat|battlement)\w*\b", "a plain parapet", "no-classical-or-islamic-or-medieval-skyline"),
    (r"\b(?:campanile|bell[- ]?tower|steeples?|spires?|cathedrals?|chapels?)\b", "a flat-roofed stone house", "no-church-in-scene"),
    (r"\bchurch(?:es)?\b", "a flat-roofed stone house", "no-church-in-scene"),
    # --- foreign art style -> stripped (rely on the INK house style) ---
    (r"\b(?:anime|manga|chibi|cel[- ]?shad\w*|ukiyo[- ]?e|hokusai|woodblock|photoreal\w*|photo[- ]?realistic|3d ?render|pixar|disney|impasto)\b", "", "no-style-drift-keep-house-ink"),
    (r"\bwater ?colou?r\b", "", "no-style-drift-keep-house-ink"),
    (r"\b(?:baroque )?oil painting\b", "", "no-style-drift-keep-house-ink"),
]

# negation clauses that BACKFIRE (seedream draws the forbidden noun) — strip the whole clause.
_POISON_NOUN = (r"(?:text|words?|letters?|writing|speech\s*bubbles?|inscriptions?|scrolls?|titulus|"
                r"nails?|spikes?|blood|crosses?|cross|child(?:ren)?|boy|halo|fists?|rope)")
_NEGATIONS = [
    (rf",?\s*\b(?:no|without|never)\s+{_POISON_NOUN}(?:\s+(?:or|and)\s+{_POISON_NOUN})*\b", "negation-draws-the-noun"),
]


def positivize(prompt: str) -> tuple[str, list[dict], list[str]]:
    """Apply the safe positive rewrites. Returns (fixed_prompt, changes, guidance)."""
    fixed = prompt
    changes: list[dict] = []
    for pat, repl, rid in _SWAPS:
        def _sub(m):
            changes.append({"rule": rid, "from": m.group(0), "to": repl})
            return repl
        fixed = re.sub(pat, _sub, fixed, flags=re.I)
    for pat, rid in _NEGATIONS:
        def _sub(m):
            changes.append({"rule": rid, "from": m.group(0).strip(", "), "to": "(removed)"})
            return ""
        fixed = re.sub(pat, _sub, fixed, flags=re.I)
    # tidy whitespace/commas/articles left by removals
    fixed = re.sub(r"\b(an?)\s+(an?)\s+", r"\2 ", fixed, flags=re.I)          # "a a flat" -> "a flat"
    fixed = re.sub(r"\bthe\s+(an?)\s+", r"the ", fixed, flags=re.I)            # "the a plain" -> "the plain"
    fixed = re.sub(r"\bin\s+(?:the\s+)?style\b\s*[;,.]?", "", fixed, flags=re.I)  # orphaned "in the style"
    fixed = re.sub(r"\s+style\b\s*(?=[;,.]|$)", "", fixed, flags=re.I)         # orphaned trailing " style"
    fixed = re.sub(r"\s{2,}", " ", fixed)
    fixed = re.sub(r"\s+([,.;])", r"\1", fixed)
    fixed = re.sub(r"([,;])\s*([,;])", r"\1", fixed)
    fixed = re.sub(r",\s*,", ",", fixed).strip(" ,;")

    # RISKY rewrites we refuse to auto-apply — surface as guidance instead.
    guidance: list[str] = []
    if re.search(r"\b(nails?|spikes?)\b", prompt, re.I):
        guidance.append("NAIL: drop the word 'nail'/'spike' entirely — describe ONLY the wound "
                        "('a dark ragged pierced hole in the centre of the palm, blood running down'); "
                        "risen = 'a single round healed scar, smooth pale skin' (rule nail-renders-as-stud).")
    if re.search(r"\b(coins?|shekels?)\b", prompt, re.I):
        guidance.append("COIN: keep coin faces small + soft ('a faint indistinct archaic head, edges "
                        "corroded') — a detailed/modern face or any emblem draws a logo (rule no-brand-or-modern-logo).")
    return fixed, changes, guidance


def report(prompt: str) -> tuple[str, list[dict], list[str]]:
    fixed, changes, guidance = positivize(prompt)
    print("=== render_lint autofix (Layer 2 — positivize) ===")
    if not changes:
        print("  no safe auto-swaps needed.")
    else:
        print(f"  applied {len(changes)} safe swap(s):")
        for c in changes:
            print(f"    [{c['rule']}]  '{c['from']}' -> '{c['to'] or '(removed)'}'")
    if guidance:
        print("  GUIDANCE (apply by hand — too context-dependent to auto-swap):")
        for g in guidance:
            print(f"    ! {g}")
    if changes:
        print("\n-- fixed prompt --")
        print(fixed)
    return fixed, changes, guidance


def main():
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
    ap = argparse.ArgumentParser()
    ap.add_argument("--prompt", default="")
    ap.add_argument("--file", default="")
    a = ap.parse_args()
    prompt = a.prompt or (Path(a.file).read_text(encoding="utf-8") if a.file else sys.stdin.read())
    report(prompt)


if __name__ == "__main__":
    main()
