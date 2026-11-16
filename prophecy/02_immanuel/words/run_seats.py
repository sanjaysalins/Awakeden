"""Blind writer seats for Ep 02 Immanuel words. Same pack for every seat. $0 (subscription CLIs).
  ..\..\..\.venv\Scripts\python.exe run_seats.py [--write-only] [claude,codex,gemini,grok]"""
import sys
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0, r"F:\slk\PycharmProjects\ArkAIology")
from independent_review import run_one
H = Path(__file__).resolve().parent
P = ("You are ONE independent creative voice on a blind panel. Everything you need is below. Do not use tools, do not read files, do not ask questions. Output your answer text only.\n\n"
     + (H / "BRIEF.md").read_text(encoding="utf-8") + "\n\n=== KJV ===\n" + (H / "KJV.txt").read_text(encoding="utf-8"))
for bad in ("Before anyone went to Him" + " X", "draft_", "CAND_"):
    assert bad not in P, bad
(H / "PROMPT.md").write_text(P, encoding="utf-8")
names = [a for a in sys.argv[1:] if not a.startswith("--")]
names = (names[0] if names else "claude,codex,gemini,grok").split(",")
def go(n):
    name, ok, out, dur = run_one(n, P, H / "_raw"); (H / f"draft_{name}.md").write_text(out, encoding="utf-8"); print(name, ok, round(dur), len(out), flush=True)
if __name__ == "__main__":
    if "--write-only" in sys.argv: print("prompt", len(P.split()), "words"); sys.exit()
    with ThreadPoolExecutor(4) as ex: list(ex.map(go, names))
