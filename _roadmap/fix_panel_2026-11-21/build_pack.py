"""Blind fix panel pack (2026-11-21): 10 'half' shorts + Second Fire title. Spoken words only, no verdicts."""
import re, sys
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")
R = Path(r"F:\slk\PycharmProjects\JesusInTheBible")
B = R / "batches"; S = R / "poc_living_water_ink_style_test"
ITEMS = [  # id, current title, folder
 ("S1","Why One Red Cord Survived the Fall of Jericho", B/"cluster_03_ink_shorts/rahab-and-the-scarlet-cord"),
 ("S2","A Warning at Jesus' Birth Came True at the Cross", B/"cluster_01_cross/woman_behold_john1926"),
 ("S3","Why Was Jesus Born in Bethlehem?", B/"cluster_05_prophecy/bethlehem_short"),
 ("S4","Jesus Stopped Reading Mid-Sentence", B/"cluster_05_prophecy/nazareth_short"),
 ("S5","Ten Were Healed. Only One Came Back.", S/"swirls_episode_11_where_are_the_nine"),
 ("S6","Jesus Died Praying a Child's Bedtime Prayer", B/"cluster_01_cross/into_thy_hands_luke2346"),
 ("S7","God Hung Up a Snake. Looking at It Saved Them.", B/"cluster_03_ink_shorts/bronze-serpent-02-the-thing-that-killed-them"),
 ("S8","What Thief Wraps the Face-Cloth? The Empty Tomb", B/"cluster_02_resurrection/empty_tomb_john208"),
 ("S9","The Man Who Carried Jesus' Cross Was Walking the Other Way", S/"swirls_episode_13_the_cross_that_wasnt_his"),
 ("S10","Jesus Slept Through a Storm. Then He Asked One Question.", B/"cluster_03_ink_shorts/he-was-asleep-in-the-storm"),
 ("S11","The Second Fire", B/"cluster_04_encounters/second_fire_short"),
]
SKIP = re.compile(r"^\s*(#|<!--|-->|>|\||\*\*|- |---|Series:|Note:|Status:|\[)")
def spoken(d: Path) -> str:
    t = d/"audio/narration-tagged.md"
    if t.exists():
        x = t.read_text(encoding="utf-8")
        x = re.sub(r"<!--.*?-->", "", x, flags=re.S)
        x = re.sub(r"[[a-z ]+]", "", x); x = re.sub(r"<speaker[^>]*>", "", x); x = re.sub(r"<[^>]+>", " ", x)
        lines = [l.strip() for l in x.splitlines() if l.strip() and not SKIP.match(l)]
    else:
        x = re.sub(r"<!--.*?-->", "", (d/"narration.md").read_text(encoding="utf-8"), flags=re.S)
        lines = [re.sub(r"^[A-Z][A-Za-z_ ]{1,20}:\s*", "", l.strip()) for l in x.splitlines() if l.strip() and not SKIP.match(l)]
    return "\n".join(lines)
out = []
for i, t, d in ITEMS:
    out.append(f"## {i}\nTITLE NOW: {t}\nSPOKEN WORDS (as recorded):\n{spoken(d)}\n")
Path("SHORTS.md").write_text("\n".join(out), encoding="utf-8")
print("wrote SHORTS.md", sum(len(o.split()) for o in out), "words")
