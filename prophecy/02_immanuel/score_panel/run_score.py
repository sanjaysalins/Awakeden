"""Blind score panel seats for Immanuel v2. $0."""
import sys
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0, r"F:\slk\PycharmProjects\ArkAIology")
from independent_review import run_one
H = Path(__file__).resolve().parent
P = (H / "PROMPT.md").read_text(encoding="utf-8")
def go(n):
    name, ok, out, dur = run_one(n, P, H / "_raw"); (H / f"{name}_score.md").write_text(out, encoding="utf-8"); print(name, ok, round(dur), len(out), flush=True)
with ThreadPoolExecutor(4) as ex: list(ex.map(go, (sys.argv[1] if len(sys.argv) > 1 else "claude,codex,grok").split(",")))
