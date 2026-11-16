"""Blind check seats: score the pooled insights. $0 (subscription CLIs). No seat names in the pool."""
import sys
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0, r"F:\slk\PycharmProjects\ArkAIology")
from independent_review import run_one
H = Path(__file__).resolve().parent
P = ("You are ONE independent judge on a blind panel. Everything you need is below. Do not use tools, do not read files, do not ask questions. Output your answer text only.\n\n"
     + (H / "BRIEF_CHECK.md").read_text(encoding="utf-8") + "\n\n" + (H / "POOL.md").read_text(encoding="utf-8")
     + "\n\n=== KJV (exact) ===\n" + (H / "KJV_HUNT.txt").read_text(encoding="utf-8"))
for bad in ("fable", "claude", "codex", "gemini", "grok", "seat", "hunt_"):
    assert bad not in P.lower(), bad
(H / "CHECK_PROMPT.md").write_text(P, encoding="utf-8")
names = [a for a in sys.argv[1:] if not a.startswith("--")]
names = (names[0] if names else "claude,codex,gemini,grok").split(",")
def go(n):
    name, ok, out, dur = run_one(n, P, H / "_raw_check"); (H / f"check_{name}.md").write_text(out, encoding="utf-8"); print(name, ok, round(dur), len(out), flush=True)
if __name__ == "__main__":
    with ThreadPoolExecutor(4) as ex: list(ex.map(go, names))
