import sys
from pathlib import Path
sys.path.insert(0, r"F:\slk\PycharmProjects\ArkAIology")
from independent_review import run_one
D = Path(__file__).resolve().parent
P = "You are ONE independent judge on a blind panel. Everything is below. Do not use tools or read files. Output your answer only.\n\n" + (D/"TEST_PACK.md").read_text(encoding="utf-8")
for n in sys.argv[1].split(","):
    name, ok, text, dur = run_one(n, P, D/"_raw")
    (D/f"test_{name}.md").write_text(text, encoding="utf-8"); print(name, ok, round(dur), flush=True)
