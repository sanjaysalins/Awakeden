import sys
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0, r"F:\slk\PycharmProjects\ArkAIology")
from independent_review import run_one
H = Path(__file__).resolve().parent
P = "Do not use tools or read files; everything is below. Output text only.\n\n" + (H / "RETEST_PACK.md").read_text(encoding="utf-8")
def go(n):
    name, ok, out, dur = run_one(n, P, H / "_raw_retest"); (H / f"retest_{name}.md").write_text(out, encoding="utf-8"); print(name, ok, round(dur), flush=True)
with ThreadPoolExecutor(4) as ex: list(ex.map(go, ["claude", "codex", "gemini", "grok"]))
