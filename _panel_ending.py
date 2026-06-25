"""_panel_ending.py — ask the local-CLI panel to PROPOSE a richer ending (generation, not review).

Reuses independent_review.py's provider plumbing (run_one / PROVIDERS) so it stays $0 on the
user's local CLI subscriptions. Each reviewer proposes richer landings for the #31 narration;
output saved next to the narration for synthesis.

Usage: .venv\\Scripts\\python.exe _panel_ending.py "<narration.md>" [--providers cursor,claude,...]
"""
from __future__ import annotations
import argparse, sys
from datetime import datetime
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

import independent_review as IR

GEN_TEMPLATE = """You are a gifted gospel-short writer helping sharpen ONE thing: the ENDING (landing) of a
60-second YouTube Short narration. You are NOT reviewing the whole thing — you are PROPOSING a much
richer, more resolved final beat for THE EXACT NARRATION pasted below.

FIRST, read the full narration below and identify ITS OWN thread/spine and its CURRENT last beat. The
problem to fix: the current landing often feels unfinished / abstract / writerly — a clever verdict that
doesn't fully RESOLVE or turn the viewer toward Christ. Propose a landing that lands with weight and
completes the gospel turn, while staying true to THIS piece's own thread (do NOT swap the thread, and do
NOT import imagery or a Bible passage the narration didn't use).

HARD CONSTRAINTS (binding — a proposal that breaks these is useless):
- KJV verbatim: do NOT alter, add, or re-quote Scripture. Any Bible quote already in the script stays
  exactly as it is. Your new ending is NARRATOR voice (no new quotation marks unless exact KJV).
- Grace-anchored: NO fear, NO gain/loss, NO self-interest, NO works/"try harder" framing, NO
  manufactured pressure. The Spirit convicts; the script INVITES.
- Evangelical, biblically faithful. No invented doctrine, no contrarian/clickbait reading.
- CTA-to-Jesus: the landing should turn the viewer toward Christ / WHO HE IS, and may invite, but must
  NOT be the tired generic "Will you trust Him?" close. It must do NEW work.
- Clarity on first hearing — a listener with zero Bible knowledge must follow it.
- Length: a SHORT landing — roughly the last 2-4 spoken sentences, ~25-45 words total. It must speak
  in ~9-15 seconds. Punchy, not a sermon.
- It should pair with a closing IMAGE of Christ (these shorts close on Jesus).

DELIVER EXACTLY THIS:
PROPOSAL A:
<the richer ending — only the final beat, the words to be spoken>
WHY A: <1-2 sentences on why this lands richer / what new work it does>

PROPOSAL B:
<a different richer ending, different angle>
WHY B: <1-2 sentences>

(Optional) ONE-LINE NOTE: <anything the writer should know>

----- FULL NARRATION (for context; only the ENDING changes) -----
{artifact}
----- END -----
"""


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("artifact")
    ap.add_argument("--providers", default="cursor,claude,gemini,codex,grok")
    a = ap.parse_args()

    art = Path(a.artifact)
    text = art.read_text(encoding="utf-8").strip()
    prompt = GEN_TEMPLATE.format(artifact=text)

    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    outdir = art.parent / "_panel_ending" / stamp
    outdir.mkdir(parents=True, exist_ok=True)
    (outdir / "prompt.txt").write_text(prompt, encoding="utf-8")

    names = [p.strip() for p in a.providers.split(",") if p.strip()]
    print(f"[panel-ending] asking {names} for richer endings ... ($0, local CLIs)")
    results = {}
    with ThreadPoolExecutor(max_workers=len(names)) as ex:
        futs = {ex.submit(IR.run_one, n, prompt, outdir): n for n in names}
        for f in as_completed(futs):
            name, ok, out, dur = f.result()
            results[name] = (ok, out, dur)
            (outdir / f"{name}.md").write_text(out, encoding="utf-8")
            print(f"  {'OK ' if ok else 'XX '} {name:8s} {dur:5.1f}s  ({len(out)} chars)")

    print(f"\n[panel-ending] saved -> {outdir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
