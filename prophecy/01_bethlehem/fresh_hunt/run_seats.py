import sys, tempfile
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0, r"F:\slk\PycharmProjects\ArkAIology")
from independent_review import run_one
H = Path(__file__).resolve().parent
P = (H / "BRIEF.md").read_text(encoding="utf-8")
CWD = Path(tempfile.mkdtemp(prefix="blind_hunt_"))  # outside repo: no CLAUDE.md / drafts leak in
names = (sys.argv[1] if len(sys.argv) > 1 else "claude,codex,gemini,grok").split(",")
def go(n):
    name, ok, out, dur = run_one(n, P, H / "_raw", cwd=CWD)
    (H / f"hunt_{name}.md").write_text(out, encoding="utf-8"); print(name, ok, round(dur), flush=True)
with ThreadPoolExecutor(4) as ex: list(ex.map(go, names))
