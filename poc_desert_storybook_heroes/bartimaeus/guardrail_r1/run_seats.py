import sys
from pathlib import Path
sys.path.insert(0, r"F:\slk\PycharmProjects\ArkAIology")
from independent_review import run_one
HERE = Path(__file__).resolve().parent
for pair in sys.argv[1].split(","):
    seat, cli = pair.split(":")
    prompt = (HERE / f"prompt_{seat}.md").read_text(encoding="utf-8")
    n, ok, out, dur = run_one(cli, prompt, HERE)
    (HERE / f"seat_{seat}_{cli}.md").write_text(out, encoding="utf-8")
    print(f"{seat}/{cli}: ok={ok} {dur:.0f}s", flush=True)
