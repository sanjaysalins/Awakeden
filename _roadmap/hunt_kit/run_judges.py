"""Blind judges: python run_judges.py <topic_dir> [claude,codex,gemini,grok] [--check-only]
Builds <topic_dir>/JUDGE_PROMPT.md = JUDGE_BRIEF.md + kill list (SUNDAY_SCHOOL.md) + CARDS.md + KJV_PACK.md, writes judge_<seat>.md.
Fable/Sonnet judges get ONLY JUDGE_PROMPT.md. Same prerequisites as run_seats.py."""
import sys
from pathlib import Path
from _cli import read, run_panel
from _rules import need
argv = [a for a in sys.argv if not a.startswith("--")]
T = Path(argv[1]).resolve()
need(T, "run_judges")
P = "\n\n".join(read(T / f) for f in ("JUDGE_BRIEF.md", "SUNDAY_SCHOOL.md", "CARDS.md", "KJV_PACK.md"))
(T / "JUDGE_PROMPT.md").write_text(P, encoding="utf-8")
print("wrote", T / "JUDGE_PROMPT.md", len(P.split()), "words")
if "--check-only" not in sys.argv:
    run_panel(P, T, "judge", argv)
