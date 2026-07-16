"""Round 2 fixes from the coordinator's independent spot-check (2026-07-16):
  #6  Moses drawn as a young dark-haired man -- inconsistent with the elderly
      grey-haired/grey-bearded Moses in scenes 5 and 7. Lock the description.
  #11 Leftover repeating watermark artifact ("BHEIN GIZZIHUIC SROM" tiled text)
      that the agent's own eye-audit caught earlier but never actually rerolled
      -- a real process miss, fixed now.
  #15, #24 Greco-Roman fluted columns + Gothic tracery in the Israelite temple
      scenes -- the exact anachronism category the coordinator flagged on the
      sibling piece. Replaced with explicit ancient Near-Eastern/Solomonic
      temple architecture and a hard ban on classical/Gothic detailing.
$0, no render (text only)."""
import json
from pathlib import Path

p = Path(r"C:\Users\sanjay\PycharmProjects\JesusInTheBible\longform\04_The_Bronze_Serpent\v1\visual_16x9_inked\scene_plan.json")
d = json.loads(p.read_text(encoding="utf-8"))
by_id = {s["id"]: s for s in d["scenes"]}

MOSES_LOCK = ("Moses -- an elderly Israelite prophet about 80 years old, long "
              "GREY-WHITE hair and a full long GREY-WHITE beard, weathered deeply "
              "lined face, the SAME Moses seen elsewhere in this film -- ")

by_id[6]["subject_block"] = (
    "a single seamless full-bleed inked graphic-novel panel, bold black linework, "
    "solemn and hushed: " + MOSES_LOCK + "alone kneeling in a pool of pale light on "
    "the desert floor at the edge of the Bronze-Age Israelite wilderness camp "
    "(~1400 BC) of goat-hair tents in a sun-baked desert of rock and dust, other "
    "people in simple undyed handwoven wool tunics and rough mantles, bare-headed or "
    "in plain cloth head-cloths, NO modern NO medieval NO European dress, head "
    "lifted as if listening, a great stillness and a strange holy weight around him, "
    "the camp dim and waiting behind; the command not yet seen, only awaited; "
    "reverent, expectant, one continuous image, no frame, no panels, no border, no "
    "text, no watermark, no repeating background pattern"
)

# #11: same content, just add an explicit anti-watermark guard (the prior render
# had a tiled ghost-text watermark despite the style tail already banning it).
by_id[11]["subject_block"] = (
    "a single seamless full-bleed inked graphic-novel panel, bold black linework, "
    "intimate first-century Judea night interior: the living robed Christ seated in "
    "warm lamplight in quiet conversation with Nicodemus, an older bearded Pharisee "
    "in a plain mantle leaning in to listen; a single clay oil lamp between them, "
    "deep shadow all around, the city dark beyond a low stone window; reverent, "
    "searching, intimate, one continuous image, no frame, no panels, no border, no "
    "text, no watermark, no repeating background text or pattern, clean flat colour "
    "background only"
)

TEMPLE_LOCK = ("an ancient Israelite temple court (Solomon's Temple as it stood in "
               "Hezekiah's day, 8th century BC) built of massive PLAIN cut ashlar "
               "stone blocks and dark cedar-wood beams, thick PLAIN square-cut stone "
               "or bronze pillars -- ABSOLUTELY NOT fluted Greek or Roman columns, "
               "NOT classical Doric/Ionic/Corinthian capitals, NOT pointed Gothic "
               "arches or European cathedral tracery, NOT any classical or medieval "
               "European architecture -- ancient Near-Eastern temple construction "
               "only, ")

by_id[15]["subject_block"] = (
    "a single seamless full-bleed inked graphic-novel panel, bold black linework, "
    "weighty and resolute: in " + TEMPLE_LOCK + "a godly bearded king in a plain "
    "robe swinging a heavy stone maul to STRIKE and shatter an old bronze "
    "serpent-on-a-pole idol, fragments of broken bronze flying, a thin haze of "
    "incense the people had wrongly burned to it drifting in the shadow; NO legible "
    "text anywhere; the relic smashed so none mistake the sign for the Saviour, one "
    "continuous image, no frame, no panels, no border, no text"
)

by_id[24]["subject_block"] = (
    "a single seamless full-bleed inked graphic-novel panel, bold black linework, "
    "sober and clear, DEEP composition: in " + TEMPLE_LOCK + "the shattered "
    "fragments of the broken bronze serpent lie scattered on the floor in shadow; "
    "above and beyond them a humble bare-headed Israelite turns his face away from "
    "the lifeless relic and lifts his eyes UPWARD into a single shaft of pale "
    "heavenly light -- trust aimed where God told them to aim it, not at the metal; "
    "reverent, no legible text, one continuous image, no frame, no panels, no "
    "border, no text"
)

p.write_text(json.dumps(d, indent=2, ensure_ascii=False), encoding="utf-8")
print("patched subject_block for scenes 6, 11, 15, 24")

OUT = p.parent
REROLL_FILES = ["06_not.png", "11_night.png",
                 "15_hezekiah_breaks_the_brazen_serpent.png", "24_trust.png"]
for fn in REROLL_FILES:
    fp = OUT / fn
    if fp.exists():
        fp.unlink()
        print(f"deleted {fp.name} for reroll")
