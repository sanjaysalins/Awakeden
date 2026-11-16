"""Confirm pack for Y3 (one version, guardrail format). Same lenses/format as round 3."""
import json
from pathlib import Path
ROOT = Path(r"F:\slk\PycharmProjects\JesusInTheBible"); R3 = ROOT / "poc_comic_page" / "_words_mockers_r3"
D = ROOT / "poc_comic_page" / "_words_mockers_r4"; (D / "panel_r1").mkdir(parents=True, exist_ok=True)
Y3 = (R3 / "cand_Y3.md").read_text(encoding="utf-8")
kjv = (R3 / "pack.md").read_text(encoding="utf-8").split("## KJV TEXT SUPPLIED FOR CHECKING (authority)")[1]
# the pack's Matthew 26:53 line came from a corpus with a missing verse; replace with the true KJV text
kjv = kjv.replace("Matthew 26:53 But how then shall the scriptures be fulfilled, that thus it must be?",
                  "Matthew 26:53 Thinkest thou that I cannot now pray to my Father, and he shall presently give me more than twelve legions of angels?")
pack = """# FILM-ONLY PACK (what the viewer hears and sees)
Format: a 65-70 second vertical (9:16) Bible short for YouTube Shorts / TikTok, narrated, comic-style pictures; the quoted Bible lines also appear in speech balloons; first on-screen card (first 2.6 seconds): WHO WROTE THE MOCKERY?
Title shown on upload: The Mockers' Words (Psalm 22:7-8)
One extra on-screen card: DELIVER = RESCUE (during the first Psalm quote).
Voices: [narrator], [david] (David's Psalm words), [mocker] (the crowd's Matthew taunts). Bible quotes are KJV; references are in brackets.

## EVERYTHING THE VIEWER HEARS (numbered lines)
""" + "\n".join("%d. %s" % (i + 1, l) for i, l in enumerate(Y3.split("\n"))) + "\n\n## KJV TEXT SUPPLIED FOR CHECKING (authority)" + kjv
(D / "pack.md").write_text(pack, encoding="utf-8")
for f in ("lenses.json", "format.txt", "header.txt"):
    (D / f).write_text((R3 / f).read_text(encoding="utf-8"), encoding="utf-8")
print("ok", len(pack))
