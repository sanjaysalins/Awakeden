"""Owner rule (2026-10-31, restated 2026-11-14: "always remove any AI tool reference"): strip AI-method wording
from every PUBLIC text file (publish packs, upload kits, paste pages). Review/panel transcripts are left alone.
Usage: python tools_strip_ai_wording.py [--apply]   (dry run by default)"""
import re, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parent
PAT = re.compile(r"[ \t]*(Art(?:, music)? and voices made with AI(?: tools)?\.|Art made with AI tools\.)")
SKIP = ("_independent_review", "red_team", "_redteam", "panel", "prompt", "_pre_")
apply = "--apply" in sys.argv
n_files = n_hits = 0
# Whole repo (2026-11-16: the old 5-folder list missed every Swirls pack).
for base in ("",):
    for p in ROOT.rglob("*"):
        if any(x in p.parts for x in (".venv", "node_modules", ".git")): continue
        if p.suffix not in (".md", ".html", ".json", ".txt") or not p.is_file(): continue
        rel = str(p.relative_to(ROOT)).replace("\\", "/")
        if any(s in rel for s in SKIP): continue
        if not any(d in rel for d in ("/publish/", "/upload/")): continue
        t = p.read_text(encoding="utf-8", errors="strict")
        new, k = PAT.subn("", t)
        if not k: continue
        new = new.replace("\n\n\n", "\n\n")  # json-escaped blank-line tidy
        new = re.sub(r"\n{3,}", "\n\n", new)
        new = new.replace("✝\n\"", "✝\"").replace(" \n", "\n")
        n_files += 1; n_hits += k
        print(("FIX " if apply else "would fix ") + f"{k:2d}  {rel}")
        if apply: p.write_text(new, encoding="utf-8")
print(f"{'fixed' if apply else 'would fix'} {n_hits} lines in {n_files} files")
