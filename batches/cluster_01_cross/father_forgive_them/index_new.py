#!/usr/bin/env python
"""Register the 5 NEW v2 panels into the global asset index (root asset_index.json).
06c is HELD (white-dot scars, pending user decision) — not indexed until settled.

  .venv\\Scripts\\python.exe batches/cluster_01_cross/father_forgive_them/index_new.py
"""
import importlib.util
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = Path(__file__).resolve().parents[3]
spec = importlib.util.spec_from_file_location("ax", ROOT / "asset_index.py")
ax = importlib.util.module_from_spec(spec); spec.loader.exec_module(ax)

NBP = HERE / "visual" / "nbp"
HOLD = set()   # 06c resolved (one lifted scarred hand, healed-scar recipe) — now indexed
COMMON = dict(type="still", media="image", aspect="9:16", style="inked-graphic-novel",
              cluster="01_cross", piece="father_forgive_them",
              piece_title="Father, forgive them", verse="Luke 23:34", source="seedream_v4_5",
              created="2026-07-01", used_in=["father_forgive_them"])

PANELS = [
    ("01b_nailed_hands", 1, "HOOK", "Nailed hands (macro)",
     "stark macro of both of Christ's hands nailed to the cross-beam with plain flat-head iron nails, blood running down, black storm sky",
     ["JESUS(passion)"], ["CROSS", "iron-nail", "nailed-hands", "storm-sky"],
     "the cross (hands)", "stark, visceral",
     "the crucifixion — nails through his hands (Luke 23:33)", "neutral",
     ["nailed-hands", "iron-nail", "macro", "hook", "crucifixion", "blood"]),
    ("01c_soldiers_gamble", 1, "HOOK", "Soldiers gambling at the foot",
     "three Roman soldiers kneeling in the dust at the foot of the grounded cross, casting lots, storm sky",
     ["ROMAN_SOLDIERS"], ["CROSS", "dice-lots", "storm-sky"],
     "Golgotha, foot of the cross", "cold, indifferent",
     "the soldiers gamble for his clothes (Luke 23:34b)", "neutral",
     ["soldiers", "gambling", "lots", "golgotha", "hook"]),
    ("06b_our_sin", 6, "CONVICTION", "Our sin — the shadow of the cross",
     "the long dark shadow of the cross falls over a group of ordinary ancient figures with bowed heads",
     ["ROMAN_SOLDIERS"], ["CROSS-shadow", "bowed-figures", "hilltop"],
     "Golgotha hilltop (overhead)", "convicting, somber",
     "the sin that put him there was ours too", "neutral",
     ["cross-shadow", "crowd", "conviction", "shared-guilt"]),
    ("06c_intercession_lives", 6, "CONVICTION", "The living Christ interceding",
     "the living risen Christ standing in warm light, both scarred hands lifted in intercession",
     ["JESUS(resurrection)"], ["healed-scar", "golden-light"],
     "risen / interceding", "alive, merciful",
     "the Lord who prayed for his executioners still lives to make intercession (Heb 7:25)", "hero",
     ["living-christ", "intercession", "risen", "hands-lifted", "bridge"]),
    ("07b_gospel_wide", 7, "LANDING", "Gospel wide — risen Christ in the doorway",
     "the risen Christ standing in a light-flooded doorway, arms open in welcome, feet planted",
     ["JESUS(resurrection)"], ["doorway", "golden-light"],
     "resurrection / tomb doorway", "inviting, triumphant",
     "while we were yet sinners, Christ died for us (Rom 5:8)", "hero",
     ["risen-christ", "doorway", "open-arms", "gospel-invitation", "living-christ", "wide"]),
]


def main():
    for (slug, beat, role, title, subject, chars, elems, setting, mood, doctrine, scope, tags) in PANELS:
        if slug in HOLD:
            print(f"  [HELD] {slug} — pending decision, not indexed"); continue
        path = NBP / f"{slug}.png"
        if not (path.exists() and path.stat().st_size > 0):
            print(f"  [skip-missing] {slug}"); continue
        ax.register({**COMMON, "id": f"fft_{slug}", "path": str(path),
                     "beat": beat, "beat_role": role, "title": title, "subject": subject,
                     "characters": chars, "elements": elems, "setting": setting, "mood": mood,
                     "doctrine": doctrine, "reuse_scope": scope, "tags": tags})
        print(f"  [indexed] fft_{slug}")
    print(f"\nasset_index.json now holds {len(ax.load()['assets'])} assets.")


if __name__ == "__main__":
    main()
