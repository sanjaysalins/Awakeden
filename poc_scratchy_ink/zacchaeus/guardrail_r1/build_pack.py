"""Build the blind guardrail pack (words only) for Zacchaeus v2 + one prompt per seat. Leak-check."""
import json, re
from pathlib import Path
H = Path(__file__).resolve().parent; Z = H.parent; T = Path(r"F:\slk\PycharmProjects\ArkAIology\episode-pipeline\guardrail_panel_template")
src = (Z/"words"/"FINAL_WORDS.md").read_text(encoding="utf-8")
lines = [l for l in src.splitlines() if l.startswith("[") or l.strip() == "(pause)"]
num = "\n".join(f"{i}. {l}" for i, l in enumerate(lines, 1))
pack = ("=== EVIDENCE PACK ===\nA 60-70 second vertical short video (phone, 9:16), voiced by a narrator plus separate voices for Jesus, "
        "Zacchaeus and the crowd. Pictures: hand-drawn scratchy-ink comic style. Story: Luke 19:1-10. The SPOKEN WORDS, numbered "
        "(the [label] is who speaks, not spoken):\n\n" + num + "\n")
kjv = (Z/"words"/"KJV.txt").read_text(encoding="utf-8")
lens = json.loads((T/"lenses.json").read_text(encoding="utf-8"))
lens["newcomer"][1] = lens["newcomer"][1].replace("Moses, Pharaoh, Sinai or Israel as a story", "Jesus, Zacchaeus or any Bible story")
lens["bible"][1] = ("You know the Bible well and you must check every factual claim in the SPOKEN lines against the KJV text below "
    "(the film is based on Luke 19:1-10; other passages are for context). Question 4 is your main job: go line by line, mark each claim "
    "RIGHT / OVERCLAIMED / UNSUPPORTED / WRONG, quote the line, cite the verse. Check every quoted KJV phrase is word-for-word. Then answer "
    "the other questions as a Bible reader (would you send it to your church group?).\n\nKJV TEXT (the only authority; quote it):\n" + kjv)
head = (T/"header.txt").read_text(encoding="utf-8"); fmt = (T/"format.txt").read_text(encoding="utf-8")
for k, (title, body) in lens.items():
    (H/f"prompt_{k}.txt").write_text(f"{head}\n\nYOUR SEAT: {title}\n{body}\n\n{pack}\n{fmt}\n", encoding="utf-8")
bad = re.compile(r"\b(v1|v2|draft|revised|earlier version|locked|seat [A-Z]|candidate|Fable|Codex|Gemini)\b", re.I)
for f in H.glob("prompt_*.txt"):
    hits = bad.findall(f.read_text(encoding="utf-8").split("=== EVIDENCE PACK ===")[1])
    print(f.name, "LEAK" if hits else "clean", hits)
print(num)
