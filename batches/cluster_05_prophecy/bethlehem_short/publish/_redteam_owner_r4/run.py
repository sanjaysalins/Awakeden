import sys
from pathlib import Path
sys.path.insert(0, r"F:\slk\PycharmProjects\ArkAIology")
from concurrent.futures import ThreadPoolExecutor
from independent_review import run_one
D = Path(__file__).resolve().parent; P = (D/"PROMPT.md").read_text(encoding="utf-8")
with ThreadPoolExecutor(4) as ex:
    for name, ok, text, dur in ex.map(lambda n: run_one(n, P, D/"_raw", cwd=__import__("tempfile").mkdtemp(prefix="blind_rt3_")), ["claude", "codex", "gemini", "grok"]):
        (D/f"seat_{name}.md").write_text(text, encoding="utf-8"); print(name, ok, round(dur), flush=True)
