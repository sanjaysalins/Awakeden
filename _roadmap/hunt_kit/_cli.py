"""The ONE place the hunt kit touches the CLI panel. Uses this repo's own independent_review.run_one
(no ArkAIology import). Seats run in a temp folder OUTSIDE the repo so no CLAUDE.md / drafts leak in."""
import os, re, sys, tempfile
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO))
try:
    import independent_review as ir
except ImportError as e:
    sys.exit(f"hunt_kit: cannot import run_one from {REPO / 'independent_review.py'} ({e})")
os.environ.setdefault("REVIEW_TIMEOUT_MULT", "2")  # hunts are slow: claude 20 min, codex/gemini 10, grok 12
if "--skip-git-repo-check" not in ir.PROVIDERS["codex"]["args"]:
    ir.PROVIDERS["codex"]["args"].append("--skip-git-repo-check")  # the temp seat folder is not a git repo

def read(p):
    """File text with <!-- notes --> removed (template notes never reach a seat)."""
    return re.sub(r"<!--.*?-->\s*", "", Path(p).read_text(encoding="utf-8"), flags=re.S)

def run_panel(prompt, topic, kind, argv):
    """Send prompt to each CLI seat in parallel; write <topic>/<kind>_<seat>.md. kind = 'hunt' or 'judge'."""
    names = (argv[2] if len(argv) > 2 else "claude,codex,gemini,grok").split(",")
    bad = [n for n in names if n not in ir.PROVIDERS]
    if bad: sys.exit(f"hunt_kit: unknown seat {bad}; pick from {sorted(ir.PROVIDERS)}")
    os.chdir(tempfile.mkdtemp(prefix=f"blind_{kind}_"))  # run_one inherits this folder
    def go(n):
        name, ok, out, dur = ir.run_one(n, prompt, topic / "_raw")
        (topic / f"{kind}_{name}.md").write_text(out, encoding="utf-8"); print(name, ok, round(dur), flush=True)
    with ThreadPoolExecutor(4) as ex: list(ex.map(go, names))
