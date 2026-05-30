"""Re-run the audio pipeline for #26 (John 5:6) whose first run blocked at the
tag-stage round-trip word-drift guard. API mode so it runs autonomously.
"""
import os, sys
os.environ["LLM_PROVIDER"] = "api"
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.stderr.reconfigure(encoding="utf-8", errors="replace")
from pathlib import Path
from pipeline import handoff
import config
print(f"[fix26] LLM_PROVIDER={config.LLM_PROVIDER} agent_mode={config.agent_mode()}", flush=True)
folder = Path(r"C:\Users\sanjay\PycharmProjects\PythonProject1\jesus\narration\26 Jesus Walked Past the Pool\v1")
print(f"[fix26] re-running audio pipeline for: {folder}", flush=True)
code = handoff.run_audio_pipeline(folder)
print(f"[fix26] audio pipeline exit code: {code}", flush=True)
