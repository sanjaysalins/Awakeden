"""Batch: generate the panel-selected ElevenLabs score for every short, mix ducked, caption.
Reads v2/coherence_audit/music_designs.json (best_prompt per short). METERED — pass --yes."""
import json, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from sfx_pilots.add_music import build_one  # noqa

YES = "--yes" in sys.argv
designs = json.loads((ROOT / "v2/coherence_audit/music_designs.json").read_text(encoding="utf-8"))
done, fail = [], []
for d in designs:
    title = d["title"]
    print(f"\n========== {title} ({d.get('winner_lens','?').split('(')[0].strip()}) ==========", flush=True)
    ok = build_one(d["folder"], d["best_prompt"], gain=-8.0, script=d.get("script"), yes=YES, regen=True)
    (done if ok else fail).append(title)
print(f"\n\n==== MUSIC BATCH DONE: {len(done)} ok, {len(fail)} failed ====")
if fail:
    print("  failed:", fail)
