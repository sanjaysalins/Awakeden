import sys
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0, r"F:\slk\PycharmProjects\ArkAIology")
from independent_review import run_one
H = Path(__file__).resolve().parent
P = ("You are ONE independent creative voice on a blind panel. Everything you need is below. Do not use tools, do not read files, do not ask questions. Output your answer text only.\n\n"
     + (H / "BRIEF_v2.md").read_text(encoding="utf-8") + "\n\n=== KJV ===\n" + (H.parent / "KJV.txt").read_text(encoding="utf-8")
     + "\n## 1 Corinthians 15:3-4\nFor I delivered unto you first of all that which I also received, how that Christ died for our sins according to the scriptures; And that he was buried, and that he rose again the third day according to the scriptures:\n")
(H / "PROMPT.md").write_text(P, encoding="utf-8")
names = (sys.argv[1] if len(sys.argv) > 1 else "claude,codex,gemini,grok").split(",")
def go(n):
    name, ok, out, dur = run_one(n, P, H / "_raw"); (H / f"draft_{name}.md").write_text(out, encoding="utf-8"); print(name, ok, round(dur), flush=True)
if __name__ == "__main__":
    if "--write-only" in sys.argv: sys.exit()
    with ThreadPoolExecutor(4) as ex: list(ex.map(go, names))
