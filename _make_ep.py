"""Make ONE episode's narration (text + audio) from scratch — non-interactive.
Usage: python _make_ep.py <series_id> <episode_index>
"""
import sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.stderr.reconfigure(encoding="utf-8", errors="replace")
from pipeline import series as S
from pipeline import orchestrator

NOTE = (
    "Answer the Five Questions before writing. Smart-default opening: open on a real ache "
    "(problem-first) UNLESS the text is confrontational/identity/claim-of-deity — then cold-open "
    "in the scene or question-first. HARD GUARDRAIL: the turn AND landing go to WHO CHRIST IS, "
    "never to 'your problem solved'. Show, don't explain (no 'Notice the order' lecturing). Pick "
    "the ONE audience this most needs and speak TO them (never name them aloud). Land on a response "
    "to Jesus by grace; the takeaway is a CHANGE in how they see Christ, not a fact."
)

sid = sys.argv[1]; idx = int(sys.argv[2])
s = S.get_series(sid)
ep = s.episodes[idx]
print(f"PRODUCING: {s.name} #{idx} — {ep.title} ({ep.primary_ref}) | brand={s.brand}", flush=True)
v1 = orchestrator.start(s, ep, notes=NOTE, provider="hf")
print(f"\nGATE 1 reached. v1 folder: {v1}", flush=True)
