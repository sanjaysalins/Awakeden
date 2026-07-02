#!/usr/bin/env python
"""Register the 7 finished 'Father, forgive them' inked stills into the GLOBAL asset index
with rich reuse metadata (root asset_index.json). Idempotent (upsert by id). Redo'd assets
are already deleted from disk, so only the good finals are indexed.

  .venv\\Scripts\\python.exe batches/cluster_01_cross/father_forgive_them/index_stills.py
"""
import importlib.util
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = Path(__file__).resolve().parents[3]
spec = importlib.util.spec_from_file_location("ax", ROOT / "asset_index.py")
ax = importlib.util.module_from_spec(spec); spec.loader.exec_module(ax)

NBP = HERE / "visual" / "nbp"
COMMON = dict(
    type="still", media="image", aspect="9:16", style="inked-graphic-novel",
    cluster="01_cross", piece="father_forgive_them",
    piece_title="Father, forgive them", verse="Luke 23:34", source="seedream_v4_5",
    used_in=["father_forgive_them"],
)

# (slug, beat, beat_role, title, subject, characters, elements, setting, mood, doctrine, reuse_scope, tags, created)
PANELS = [
    ("01_golgotha_hook", 1, "HOOK", "Golgotha — the cross and the gamblers",
     "wide vertical Golgotha under a black storm sky: a single rough cross with the crucified Christ, "
     "Roman soldiers crouched at the foot dividing a folded robe",
     ["JESUS(passion)"], ["CROSS", "ROMAN_SOLDIERS", "divided-garment", "storm-sky"],
     "Golgotha hilltop", "ominous, reverent",
     "the crucifixion scene of Luke 23:33-34 — He is put to death while men gamble below",
     "neutral", ["crucifixion", "golgotha", "wide", "storm", "soldiers", "establishing", "cross"], "2026-06-30"),
    ("02_jesus_prays", 2, "POINT", "He prays for His killers",
     "the crucified Christ on the cross, head lifted to the dark sky, lips parted to speak; soldiers small below; one cold shaft of light on His face",
     ["JESUS(passion)"], ["CROSS", "shaft-of-light"],
     "the cross", "sorrowful mercy",
     "Jesus intercedes for those crucifying Him (Luke 23:34)",
     "neutral", ["crucifixion", "praying-christ", "cross", "light-shaft"], "2026-06-30"),
    ("03_prayer_close", 3, "red-letter", "Father, forgive them (close)",
     "intimate close of the crucified Christ's face, eyes lifted to heaven in prayer, sorrow and mercy together, a shaft of light across His features",
     ["JESUS(passion)"], ["shaft-of-light"],
     "the cross (close)", "tender, holy",
     "the red-letter prayer 'Father, forgive them; for they know not what they do'",
     "neutral", ["christ-face", "close-up", "praying", "red-letter", "mercy"], "2026-06-30"),
    ("04_cast_lots", 4, "Scripture", "They cast lots for His raiment",
     "low on the dusty ground at the foot of the cross: weathered Roman soldiers' hands casting carved lots and knucklebones, a folded seamless robe heaped beside them, torchlight",
     ["ROMAN_SOLDIERS"], ["dice-lots", "seamless-robe", "torchlight"],
     "foot of the cross, ground level", "cold, indifferent",
     "'And they parted his raiment, and cast lots' (Luke 23:34b; cf. Ps 22:18)",
     "neutral", ["dice", "lots", "gambling", "garments", "soldier-hands", "psalm-22"], "2026-06-30"),
    ("05_pierced_hand", 5, "intercession", "The pierced hand — mercy, not a fist",
     "close shot of the crucified Christ's face lifted to the light and one outstretched open hand with a clean dark pierced wound + blood (no nail hardware); other wrist rope-bound to the beam; storm sky",
     ["JESUS(passion)"], ["CROSS", "pierced-hand", "wound", "shaft-of-light"],
     "on the cross (close, face + hand)", "merciful, reverent",
     "the pierced open hand as intercession — it does not excuse the sin, it intercedes for the sinner",
     "neutral", ["crucifixion", "pierced-hand", "wound", "open-hand", "christ-face", "mercy", "close"], "2026-07-01"),
    ("06_cross_over_us", 6, "CONVICTION", "The cross over us",
     "the cross from a low angle against a breaking storm sky, Christ high upon it, the upright planted firmly in the rocky hilltop; one ordinary figure kneels at the foot, a shaft of light between them",
     ["JESUS(passion)"], ["CROSS", "kneeling-figure", "hilltop", "shaft-of-light"],
     "Golgotha hilltop, low angle", "humbling, weighty",
     "the sin that put Him there was ours too; the One who prayed for His killers still lives to intercede",
     "neutral", ["cross-from-below", "kneeling", "conviction", "hilltop", "grounded", "light-shaft"], "2026-07-01"),
    ("07_risen_hero", 7, "LANDING", "The risen Christ — mercy held out (HERO)",
     "the risen Christ in warm golden morning light, clean flowing robes, glorified face at peace, one open hand with a round healed scar reaching toward the viewer in welcome",
     ["JESUS(resurrection)"], ["healed-scar", "golden-light"],
     "resurrection morning", "warm, inviting, triumphant",
     "'While we were yet sinners, Christ died for us' — the gospel invitation to receive it by faith (Rom 5:8)",
     "hero", ["risen-christ", "resurrection", "reaching-hand", "healed-scar", "hero", "gospel-invitation", "living-christ"], "2026-07-01"),
]


def main():
    for (slug, beat, role, title, subject, chars, elems, setting, mood, doctrine, scope, tags, created) in PANELS:
        path = NBP / f"{slug}.png"
        if not (path.exists() and path.stat().st_size > 0):
            print(f"  [skip-missing] {slug}"); continue
        ax.register({
            **COMMON,
            "id": f"fft_{slug}",
            "path": str(path),
            "beat": beat, "beat_role": role, "title": title,
            "subject": subject, "characters": chars, "elements": elems,
            "setting": setting, "mood": mood, "doctrine": doctrine,
            "reuse_scope": scope, "tags": tags, "created": created,
        })
        print(f"  [indexed] fft_{slug}")
    d = ax.load()
    print(f"\nasset_index.json now holds {len(d['assets'])} assets.")


if __name__ == "__main__":
    main()
