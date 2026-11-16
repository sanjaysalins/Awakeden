"""CONTEXT seat: python context_check.py <topic_dir> <card letters, e.g. A C F> [--prompt-only]
For each card: +-10 verses around ANCHOR-1 and ANCHOR-2 (from data/kjv_full) + the card, to a hostile reader
(codex + gemini): "does the link survive the context of both passages?" -> context_codex.md, context_gemini.md.
Give ALL candidate cards in ONE run (each run rewrites the files). gate.py needs PASS from both.
--prompt-only: write CONTEXT_PROMPT.md and stop (no CLI call)."""
import sys
from pathlib import Path
from _rules import card_text, context_block, fmt, field, ref_quote, parse_ref
args = [a for a in sys.argv[1:] if not a.startswith("--")]
T = Path(args[0]).resolve()
letters = [x.upper() for a in args[1:] for x in a.replace(",", " ").split()]
texts = card_text(T)
head = ("You are a hostile, careful Bible reader. Do not use tools, do not read files, do not ask questions.\n"
        "Below are candidate links between two passages. For EACH card you get the card and the KJV text around BOTH anchors "
        "(lines marked >> are the anchor verses). Ask: does the link survive the CONTEXT of both passages, or does it "
        "only work if you pull the verses out of their setting? Look at who speaks, who is spoken to, what the paragraph is about.\n"
        "Answer one line per card, exactly: ANGLE <letter> | PASS or FAIL | one short reason\n")
blocks = []
for c in letters:
    if c not in texts:
        sys.exit(f"context_check: no ANGLE {c} in CARDS.md")
    anchors = {k: parse_ref(ref_quote(field(texts[c], k))[0]) if ref_quote(field(texts[c], k)) else None for k in ("ANCHOR-1", "ANCHOR-2")}
    if not all(anchors.values()):
        sys.exit(f"context_check: card {c} has no valid ANCHOR-1 / ANCHOR-2 reference")
    blocks.append(f"=== ANGLE {c} ===\n{texts[c].strip()}\n\n--- context of ANCHOR-1 ({fmt(anchors['ANCHOR-1'])}) ---\n"
                  f"{context_block(anchors['ANCHOR-1'])}\n\n--- context of ANCHOR-2 ({fmt(anchors['ANCHOR-2'])}) ---\n{context_block(anchors['ANCHOR-2'])}")
P = head + "\n\n" + "\n\n".join(blocks) + "\n"
(T / "CONTEXT_PROMPT.md").write_text(P, encoding="utf-8")
print("wrote", T / "CONTEXT_PROMPT.md", len(P.split()), "words,", len(letters), "cards")
if "--prompt-only" not in sys.argv:
    from _cli import run_panel  # imported late: --prompt-only needs no CLI
    run_panel(P, T, "context", ["", "", "codex,gemini"])
