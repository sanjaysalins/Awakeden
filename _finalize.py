"""FINALIZE — render audio AFTER the panel gate, once narration.md holds the final
(paneled + judged) beats. Runs the bridged audio pipeline (verify -> tag -> audit ->
per_turn_synth) on the folder. Agent-mode: service the .agent_bridge requests in chat.

Usage: python _finalize.py "<path-to-v1-folder>"
"""
import os, sys, traceback
os.environ.setdefault("LLM_PROVIDER", "agent")
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.stderr.reconfigure(encoding="utf-8", errors="replace")
from pathlib import Path
from pipeline import handoff
import config

if len(sys.argv) < 2:
    print('usage: python _finalize.py "<v1 folder>"', flush=True)
    sys.exit(2)
folder = Path(sys.argv[1])
if not (folder / "narration.md").exists():
    print(f"!! no narration.md in {folder}", flush=True)
    sys.exit(2)

print(f"[finalize] LLM_PROVIDER={config.LLM_PROVIDER}  folder={folder}", flush=True)
# Clear stale artifacts so tag + synth regenerate from the FINALIZED narration.md
# (the tag stage is idempotent and would otherwise reuse an old narration-tagged.md).
for stale in ("narration-tagged.md", "narration.mp3"):
    p = folder / stale
    if p.exists():
        p.unlink()
        print(f"[finalize] cleared stale {stale}", flush=True)
print("[finalize] rendering audio from the finalized narration.md ...", flush=True)
try:
    code = handoff.run_audio_pipeline(folder)
    print(f"[finalize] audio pipeline exit code: {code}", flush=True)
    if code == 0:
        print(f"[finalize] DONE -> {folder / 'narration.mp3'}", flush=True)
    else:
        sys.exit(code)
except Exception:
    traceback.print_exc()
    sys.exit(1)
