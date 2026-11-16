"""Run the ideas brief through the local CLI panel voices ONE AT A TIME (gentle mode).
Uses ArkAIology independent_review.run_one (subscription CLIs, metered keys stripped). Pack is inline; tools banned.
  F:\\slk\\PycharmProjects\\ArkAIology\\.venv\\Scripts\\python.exe run_cli_seats.py codex,gemini,grok,cursor"""
import sys
from pathlib import Path

sys.path.insert(0, r"F:\slk\PycharmProjects\ArkAIology")
from independent_review import run_one  # noqa: E402

HERE = Path(__file__).resolve().parent
prompt = ("You are ONE independent creative voice on a blind panel. Everything you need is below. "
          "Do not use tools, do not read files, do not ask questions. Output your answer text only.\n\n"
          + (HERE / "BRIEF.md").read_text(encoding="utf-8")
          + "\n\n=== KJV.txt ===\n" + (HERE / "KJV.txt").read_text(encoding="utf-8"))
for name in (sys.argv[1] if len(sys.argv) > 1 else "codex,gemini,grok,cursor").split(","):
    n, ok, out, dur = run_one(name, prompt, HERE)
    (HERE / f"idea_{n}.md").write_text(out, encoding="utf-8")
    print(f"{n}: ok={ok} {dur:.0f}s {len(out)} chars", flush=True)
