"""Regenerate ONE topic through the hardened engine (landing-fix + clarity test),
in AGENT-MODE (in-chat / Max sub — zero metered API). Targets a single episode by
(series_id, primary_ref) so we never depend on list indices and never batch.

Usage: python _regen_one.py            # defaults to Matthew 16:15 (#24)
       python _regen_one.py "<series_id>" "<Book c:v>"
"""
import os, sys, traceback
# Agent-mode only — the user's standing direction: NO metered API. Service the
# file bridge in chat (.agent_bridge/requests/ -> responses/<id>.txt).
os.environ.setdefault("LLM_PROVIDER", "agent")
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.stderr.reconfigure(encoding="utf-8", errors="replace")
from pipeline import series as S
from pipeline import runner
import config
print(f"[regen_one] LLM_PROVIDER={config.LLM_PROVIDER}  (agent_mode={config.agent_mode()})", flush=True)

SID = sys.argv[1] if len(sys.argv) > 1 else "questions-jesus-asked"
REF = sys.argv[2] if len(sys.argv) > 2 else "Matthew 16:15"

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
    "also the coldest, pick the CLEAREST true thread instead. "
    "LANDING (the prior take was rejected as TIRED / heard-before): the close must DELIVER, not "
    "summarise — the last line does NEW work (reveal the thread's final concrete image, or name "
    "what is now true of Christ for THIS viewer). BANNED: a bare 'Will you trust Him? / Will you "
    "come? / Will you follow Him?' tacked on as the last line, and any close that would fit a "
    "different episode unchanged. Prefer ending ON a picture or a quiet declarative of grace; "
    "use a question-close ONLY if it carries new weight the body has not already implied."
)


def find_ep(s, ref):
    for ep in s.episodes:
        if ep.primary_ref.strip().lower() == ref.strip().lower():
            return ep
    return None


print("\n" + "#" * 72, flush=True)
print(f"# REGEN ONE  {SID}  ::  {REF}", flush=True)
print("#" * 72, flush=True)
try:
    s = S.get_series(SID)
    ep = find_ep(s, REF)
    if ep is None:
        print(f"!! no episode with ref {REF} in series {SID}", flush=True)
        sys.exit(2)
    print(f"PRODUCING: {s.name} — {ep.title} ({ep.primary_ref}) | brand={s.brand}", flush=True)
    # PANEL GATE (owned by the runner): produce the LOCKED text + panel_request.md,
    # NO audio. The external-LLM panel must run before the narration is finalized.
    res = runner.create_narration(s, ep, notes=NOTE, panel_gate=True)
    print(f"\n>>> TEXT DONE (panel gate)  {REF}  -> {res.folder}", flush=True)
except Exception:
    print(f"!! FAILED {SID} {REF}:", flush=True)
    traceback.print_exc()
    sys.exit(1)
print("\n===== REGEN ONE (panel gate) COMPLETE =====", flush=True)
