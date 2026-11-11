"""CLI seats one at a time (gentle). bible->claude, hook->codex, global->grok."""
import sys
from pathlib import Path
sys.path.insert(0, r"F:\slk\PycharmProjects\ArkAIology")
from independent_review import run_one
H = Path(__file__).resolve().parent
for seat, cli in [("bible", "claude"), ("hook", "codex"), ("global", "grok")]:
    n, ok, out, d = run_one(cli, (H/f"prompt_{seat}.txt").read_text(encoding="utf-8"), H)
    (H/f"seat_{seat}_{n}.md").write_text(out, encoding="utf-8"); print(f"{seat}/{n}: ok={ok} {d:.0f}s {len(out)} chars", flush=True)
