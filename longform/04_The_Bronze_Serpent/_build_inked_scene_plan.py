"""Restyle the LOCKED 04_The_Bronze_Serpent scene_plan.json (27 scenes) from the
LEGACY Baroque oil-painting wrapper to the graphic-novel/inked wrapper, per the
migration model: keep scene CONTENT (subject/camera/atmos/timing), change ONLY
the style. Writes v1/visual_16x9_inked/scene_plan.json ($0, no render).

Also carries the beat-level caption/redletter plan (hand-built from
narration-tagged.md + narration.alignment.json word times, verified 2026-07-16)
into each scene as `cap` for the livingpage build."""
import json
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
V1 = HERE / "v1"
OUT_DIR = V1 / "visual_16x9_inked"
OUT_DIR.mkdir(exist_ok=True)

plan = json.loads((V1 / "scene_plan.json").read_text(encoding="utf-8"))

BAROQUE_OPEN = "a single seamless full-bleed Baroque oil painting, hard Caravaggio chiaroscuro, "
INK_OPEN = "a single seamless full-bleed inked graphic-novel panel, bold black linework, "

RE_REMBRANDT = re.compile(r"deep Rembrandt shadow")

# Hand-built caption/redletter plan, one entry per scene id (see conversation
# working notes: matched against narration-tagged.md speaker spans + exact
# word times from narration.alignment.json).
CAPTIONS = {
    1:  {"type": "caption", "text": "A whole camp is dying of snakebite.", "kw": "SNAKEBITE"},
    2:  {"type": "redletter", "speaker": "THE PEOPLE", "ref": "Numbers 21:5",
         "text": "Wherefore have ye brought us up out of Egypt to die in the wilderness? for there is no bread, neither is there any water; and our soul loatheth this light bread."},
    3:  {"type": "redletter", "speaker": "NUMBERS 21", "ref": "Numbers 21:6",
         "text": "And the LORD sent fiery serpents among the people, and they bit the people; and much people of Israel died."},
    4:  {"type": "caption", "text": "The venom is already inside him.", "kw": "VENOM"},
    5:  {"type": "redletter", "speaker": "THE PEOPLE", "ref": "Numbers 21:7",
         "text": "We have sinned, for we have spoken against the LORD, and against thee; pray unto the LORD, that he take away the serpents from us."},
    27: {"type": "caption", "text": "Even their confession reaches outward.", "kw": "OUTWARD"},
    6:  {"type": "caption", "text": "God does not do what they asked.", "kw": "NOT"},
    7:  {"type": "redletter", "speaker": "THE LORD", "ref": "Numbers 21:8",
         "text": "Make thee a fiery serpent, and set it upon a pole: and it shall come to pass, that every one that is bitten, when he looketh upon it, shall live."},
    22: {"type": "caption", "text": "The cure is shaped like the curse.", "kw": "CURSE"},
    8:  {"type": "caption", "text": "Raised on a pole, for all to see.", "kw": "RAISED"},
    9:  {"type": "caption", "text": "One act. Look.", "kw": "LOOK"},
    10: {"type": "redletter", "speaker": "NUMBERS 21", "ref": "Numbers 21:9",
         "text": "And Moses made a serpent of brass, and put it upon a pole, and it came to pass, that if a serpent had bitten any man, when he beheld the serpent of brass, he lived."},
    11: {"type": "caption", "text": "A man comes to Jesus in the dark.", "kw": "NIGHT"},
    23: {"type": "caption", "text": "Jesus Himself names it.", "kw": "HIMSELF"},
    12: {"type": "redletter", "speaker": "JESUS", "ref": "John 3:14-15",
         "text": "And as Moses lifted up the serpent in the wilderness, even so must the Son of man be lifted up: That whosoever believeth in him should not perish, but have eternal life."},
    13: {"type": "redletter", "speaker": "JESUS", "ref": "John 12:32",
         "text": "And I, if I be lifted up from the earth, will draw all men unto me."},
    14: {"type": "redletter", "speaker": "SCRIPTURE", "ref": "John 3:16",
         "text": "For God so loved the world, that he gave his only begotten Son..."},
    15: {"type": "redletter", "speaker": "2 KINGS 18", "ref": "2 Kings 18:4",
         "text": "brake in pieces the brasen serpent that Moses had made."},
    24: {"type": "caption", "text": "Looking was never magic. It was trust.", "kw": "TRUST"},
    16: {"type": "redletter", "speaker": "2 CORINTHIANS 5", "ref": "2 Corinthians 5:21",
         "text": "hath made him to be sin for us, who knew no sin."},
    17: {"type": "redletter", "speaker": "GALATIANS 3", "ref": "Galatians 3:13",
         "text": "being made a curse for us: for it is written, Cursed is every one that hangeth on a tree."},
    25: {"type": "redletter", "speaker": "1 PETER 2", "ref": "1 Peter 2:24",
         "text": "his own self bare our sins in his own body on the tree."},
    18: {"type": "caption", "text": "The curse fell on the lifted One.", "kw": "CURSE"},
    19: {"type": "caption", "text": "The cure was a look.", "kw": "LOOK"},
    26: {"type": "caption", "text": "You do not have to climb, or pay, or be strong.", "kw": "STRONG"},
    20: {"type": "caption", "text": "Whosoever. A nation turns its eyes up.", "kw": "WHOSOEVER"},
    21: {"type": "redletter", "speaker": "JOHN 3", "ref": "John 3:15",
         "text": "should not perish, but have eternal life."},
}
SACRED_TYPES = {"redletter"}

changed = 0
for s in plan["scenes"]:
    sb = s["subject_block"]
    if sb.startswith(BAROQUE_OPEN):
        sb = INK_OPEN + sb[len(BAROQUE_OPEN):]
        changed += 1
    sb = RE_REMBRANDT.sub("deep ink shadow", sb)
    s["subject_block"] = sb
    cap = CAPTIONS.get(s["id"])
    if cap is None:
        raise SystemExit(f"no caption plan for scene id {s['id']} ({s['title']})")
    s["cap"] = cap
    s["sacred"] = cap["type"] in SACRED_TYPES

plan["style_base"] = None   # style now comes from config.STYLE_REGISTRY[VISUAL_STYLE]
plan["style_tail"] = None
plan["image_provider"] = "hf"
plan["animation"] = {"model": "kling3_0", "aspect": "16:9"}
plan["film_name"] = "BronzeSerpent_16x9_inked.mp4"
plan["_migration_note"] = ("graphic-novel rebuild test, 2026-07-16 — restyled from the "
                            "archived Baroque scene_plan.json (archive/bronze_serpent_baroque/); "
                            "scene content/camera/timing unchanged, only style_base/tail + "
                            "subject_block style wrapper changed, per memory "
                            "graphic-novel-style-migration.")

out_path = OUT_DIR / "scene_plan.json"
out_path.write_text(json.dumps(plan, indent=2, ensure_ascii=False), encoding="utf-8")
print(f"restyled {changed}/{len(plan['scenes'])} scenes -> {out_path}")
print(f"captions: {sum(1 for s in plan['scenes'] if s['cap']['type']=='caption')} caption / "
      f"{sum(1 for s in plan['scenes'] if s['cap']['type']=='redletter')} redletter")
