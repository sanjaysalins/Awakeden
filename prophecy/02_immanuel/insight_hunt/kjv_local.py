"""Exact KJV from the local corpus (data/kjv_corpus.json, 66 books, in canon order). {..} italics/notes stripped. $0."""
import json, re
from pathlib import Path
C = json.loads(Path(r"F:\slk\PycharmProjects\JesusInTheBible\data\kjv_corpus.json").read_text(encoding="utf-8-sig"))
NAMES = ["Genesis","Exodus","Leviticus","Numbers","Deuteronomy","Joshua","Judges","Ruth","1 Samuel","2 Samuel","1 Kings","2 Kings","1 Chronicles","2 Chronicles","Ezra","Nehemiah","Esther","Job","Psalms","Proverbs","Ecclesiastes","Song of Solomon","Isaiah","Jeremiah","Lamentations","Ezekiel","Daniel","Hosea","Joel","Amos","Obadiah","Jonah","Micah","Nahum","Habakkuk","Zephaniah","Haggai","Zechariah","Malachi","Matthew","Mark","Luke","John","Acts","Romans","1 Corinthians","2 Corinthians","Galatians","Ephesians","Philippians","Colossians","1 Thessalonians","2 Thessalonians","1 Timothy","2 Timothy","Titus","Philemon","Hebrews","James","1 Peter","2 Peter","1 John","2 John","3 John","Jude","Revelation"]
def clean(t):
    t = re.sub(r"\{[^}]*:[^}]*\}", "", t)      # footnotes {x: Heb. y}
    t = re.sub(r"[{}]", "", t)                  # italics braces
    return " ".join(t.split())
def get(ref):
    m = re.match(r"(.+?) (\d+):(\d+)(?:-(\d+))?$", ref); b, c, v1, v2 = m.group(1), int(m.group(2)), int(m.group(3)), m.group(4)
    ch = C[NAMES.index(b)]["chapters"][c - 1]
    return [f"{b} {c}:{v} {clean(ch[v-1])}" for v in range(v1, int(v2 or v1) + 1)]
REFS = ["Isaiah 7:2-4", "Isaiah 7:11-15", "Isaiah 7:22", "Isaiah 8:6-18", "Isaiah 9:1-2", "Isaiah 36:2", "Isaiah 37:6",
        "2 Kings 15:29", "2 Kings 16:5-8", "2 Kings 18:17", "2 Chronicles 28:20-21",
        "Matthew 1:9", "Matthew 1:20-24", "Matthew 4:13-16", "Matthew 18:20", "Matthew 28:20",
        "Luke 2:11-12", "Luke 2:34", "Hebrews 2:11-14", "1 Peter 2:7-8", "John 7:37", "John 9:7"]
if __name__ == "__main__":
    out = "\n\n".join(f"## {r}\n" + "\n".join(get(r)) for r in REFS)
    Path(__file__).with_name("KJV_HUNT.txt").write_text(out + "\n", encoding="utf-8"); print(out)
