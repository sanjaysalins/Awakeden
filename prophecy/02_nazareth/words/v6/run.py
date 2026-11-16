import sys
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0, r"F:\slk\PycharmProjects\ArkAIology")
from independent_review import run_one
HERE = Path(__file__).resolve().parent
prompt = ("You are ONE independent creative voice on a blind panel. Everything you need is below. Do not use tools, do not read files, do not ask questions. Output your answer text only.\n\n"
          + (HERE / "BRIEF.md").read_text(encoding="utf-8") + "\n\n=== KJV ===\n" + (HERE / "KJV.txt").read_text(encoding="utf-8"))
(HERE / "PROMPT.txt").write_text(prompt, encoding="utf-8")
def go(n):
    n, ok, out, dur = run_one(n, prompt, HERE / "_raw")
    (HERE / f"draft_{n}.md").write_text(out, encoding="utf-8"); print(n, ok, int(dur), len(out), flush=True)
with ThreadPoolExecutor(4) as ex: list(ex.map(go, sys.argv[1].split(",")))
