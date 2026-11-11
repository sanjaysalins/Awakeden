import sys
from pathlib import Path
sys.path.insert(0, r"F:\slk\PycharmProjects\ArkAIology")
from independent_review import run_one
H = Path(__file__).resolve().parent
p = ("You are ONE independent blind voice. Everything you need is below. Do not use tools or read files. Output your answer text only.\n\n"
     + (H / "Q.md").read_text(encoding="utf-8") + "\n\n=== candidates.md ===\n" + (H / "candidates.md").read_text(encoding="utf-8")
     + "\n\n=== KJV.txt ===\n" + (H / "KJV.txt").read_text(encoding="utf-8"))
for n in sys.argv[1].split(","):
    n, ok, out, d = run_one(n, p, H)
    (H / f"seat_{n}.md").write_text(out, encoding="utf-8"); print(f"{n}: ok={ok} {d:.0f}s", flush=True)
