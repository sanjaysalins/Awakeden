import sys
from pathlib import Path
sys.path.insert(0, r"F:\slk\PycharmProjects\JesusInTheBible\_roadmap\hunt_kit")
import _cli
here = Path(__file__).parent
_cli.run_panel(Path(here/"PROMPT.md").read_text(encoding="utf-8"), here, "seat", ["", "", "claude,codex"])
