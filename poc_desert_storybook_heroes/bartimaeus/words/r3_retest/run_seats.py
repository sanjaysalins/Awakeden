import sys
from pathlib import Path
sys.path.insert(0, r"F:\slk\PycharmProjects\ArkAIology")
from independent_review import run_one
HERE = Path(__file__).resolve().parent
prompt = ("You are ONE independent reviewer on a blind panel. Everything you need is below. Do not use tools, do not read files. Output your answer text only.\n\n"
          + (HERE / "BRIEF.md").read_text(encoding="utf-8") + "\n\n" + (HERE / "CANDIDATES.md").read_text(encoding="utf-8")
          + "\n\n=== KJV ===\n" + (HERE / "KJV.txt").read_text(encoding="utf-8"))
for name in sys.argv[1].split(","):
    n, ok, out, dur = run_one(name, prompt, HERE)
    (HERE / f"test_{n}.md").write_text(out, encoding="utf-8")
    print(f"{n}: ok={ok} {dur:.0f}s", flush=True)
