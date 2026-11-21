"""Blind fix panel pack (2026-11-21): 10 'half' shorts + Second Fire title. Spoken words only, no verdicts."""
import re, sys
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")
R = Path(r"F:\slk\PycharmProjects\JesusInTheBible")
B = R / "batches"; S = R / "poc_living_water_ink_style_test"
ITEMS = [  # id, current title, folder
 ("T1","A Widow Was Burying Her Only Son. Jesus Stopped the Funeral.", S/"swirls_episode_07_the_bier_he_touched"),
 ("T2","Martha Asked Jesus If He Cared. He Said Her Name Twice.", B/"cluster_04_encounters/mary_martha_short"),
 ("T3","God Spoke a Promise Before Adam and Eve's Sentence", B/"cluster_03_ink_shorts/seed-of-woman-01-first-gospel-in-the-curse"),
 ("T4","Asked for a Miracle, Jesus Gave Them a Drowned Prophet", B/"cluster_02_resurrection/sign_of_jonah_matt1240"),
 ("T5","Why Is Jesus Called Immanuel?", B/"cluster_05_prophecy/immanuel_short"),
 ("T6","She Was Dead. Jesus Went Anyway", S/"swirls_episode_06_talitha_cumi"),
 ("T7","Two Thieves. Same Cross. Opposite Eternities.", B/"cluster_01_cross/today_paradise_luke2343"),
 ("T8","He Said No Three Times. Jesus Made Him Breakfast. (title already being changed)", B/"cluster_04_encounters/second_fire_short"),
]
SKIP = re.compile(r"^\s*(#|<!--|-->|>|\||\*\*|- |---|Series:|Note:|Status:|\[)")
def spoken(d: Path) -> str:
    t = d/"audio/narration-tagged.md"
    if t.exists():
        x = t.read_text(encoding="utf-8")
        x = re.sub(r"<!--.*?-->", "", x, flags=re.S)
        x = re.sub(r"\[[a-z ]+\]", "", x); x = re.sub(r"<speaker[^>]*>", "", x); x = re.sub(r"<[^>]+>", " ", x)
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
