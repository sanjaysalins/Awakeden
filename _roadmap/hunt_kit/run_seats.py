"""Blind hunt seats: python run_seats.py <topic_dir> [claude,codex,gemini,grok] [--check-only]
Builds <topic_dir>/HUNT_PROMPT.md = BRIEF.md + kill list (SUNDAY_SCHOOL.md) + KJV_PACK.md, writes hunt_<seat>.md.
Fable/Sonnet seats get ONLY HUNT_PROMPT.md. REFUSES unless loom.md, SUNDAY_SCHOOL.md (5+ items), BRIEF.md, KJV_PACK.md are good.
--check-only: check prerequisites, save HUNT_PROMPT.md, call no seat."""
import sys
from pathlib import Path
from _cli import read, run_panel
from _rules import need
argv = [a for a in sys.argv if not a.startswith("--")]
T = Path(argv[1]).resolve()
need(T, "run_seats")
P = "\n\n".join(read(T / f) for f in ("BRIEF.md", "SUNDAY_SCHOOL.md", "KJV_PACK.md"))
(T / "HUNT_PROMPT.md").write_text(P, encoding="utf-8")
print("wrote", T / "HUNT_PROMPT.md", len(P.split()), "words")
if "--check-only" not in sys.argv:
    run_panel(P, T, "hunt", argv)
