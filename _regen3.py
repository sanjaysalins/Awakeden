"""Regenerate the three narrations the user rejected (#19/#21/#22) from scratch
through the upgraded pipeline (first-hearing clarity test + shorter word target +
fixed audio: god voice, dialogue gaps). Finds episodes by scripture ref so we
don't depend on list indices. Each run writes a NEW numbered folder (text+audio).
Usage: python _regen3.py
"""
import os, sys, traceback
# Force API mode BEFORE importing config (config reads LLM_PROVIDER at import time).
# The Anthropic usage cap has been lifted, so run autonomously via the metered API
# rather than the in-chat file bridge.
os.environ["LLM_PROVIDER"] = "api"
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.stderr.reconfigure(encoding="utf-8", errors="replace")
from pipeline import series as S
from pipeline import orchestrator
import config
assert not config.agent_mode(), "expected API mode but config is in agent mode"
print(f"[regen] LLM_PROVIDER={config.LLM_PROVIDER}  (agent_mode={config.agent_mode()})", flush=True)

NOTE = (
    "Answer the Five Questions AND the first-hearing test before writing. Write for a TIRED "
    "STRANGER with zero Bible background hearing this ONCE at speed: every beat must land on "
    "first hearing. The spine must be a felt TRUTH, never a writerly conceit — no geography "
    "trivia, grammar/pronoun gymnastics, or wordplay carrying the point; those may only season "
    "a line. No logic-tricks ('only one kind of man would...'). No self-contradiction (the "
    "landing must resolve the thread, never reverse it). No exegetically false aside a skeptic "
    "could disprove. Smart-default opening: problem-first UNLESS the text is confrontational/"
    "identity/claim-of-deity — then cold-open or question-first. HARD GUARDRAIL: the turn AND "
    "landing go to WHO CHRIST IS, never 'your problem solved'. Show, don't explain. Pick the ONE "
    "audience this most needs and speak TO them (never name them aloud). Land on a response to "
    "Jesus by grace; the takeaway is a CHANGE in how they see Christ. If the freshest thread is "
    "also the coldest, pick the CLEAREST true thread instead."
)

# (series_id, primary_ref) — the three rejected topics, found by ref.
TARGETS = [
    ("questions-jesus-asked", "Matthew 16:15"),  # was #19 The Cliff of Rival Gods
    ("jesus-in-ot",           "Isaiah 53:5"),    # was #21 The Pronouns That Preached the Gospel
    ("questions-jesus-asked", "John 5:6"),       # was #22 He Never Answered Jesus
]


def find_ep(s, ref):
    for ep in s.episodes:
        if ep.primary_ref.strip().lower() == ref.strip().lower():
            return ep
    return None


for sid, ref in TARGETS:
    print("\n" + "#" * 72, flush=True)
    print(f"# REGEN  {sid}  ::  {ref}", flush=True)
    print("#" * 72, flush=True)
    try:
        s = S.get_series(sid)
        ep = find_ep(s, ref)
        if ep is None:
            print(f"!! no episode with ref {ref} in series {sid} — SKIPPED", flush=True)
            continue
        print(f"PRODUCING: {s.name} — {ep.title} ({ep.primary_ref}) | brand={s.brand}", flush=True)
        v1 = orchestrator.start(s, ep, notes=NOTE, provider="hf")
        print(f"\n>>> DONE {ref}  -> {v1}", flush=True)
    except Exception:
        print(f"!! FAILED {sid} {ref}:", flush=True)
        traceback.print_exc()

print("\n===== ALL THREE REGEN RUNS COMPLETE =====", flush=True)
