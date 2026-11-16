# Blind film panel (guardrail 5 questions + curiosity gap). Film-only pack; each CLI seat gets one lens. Fable seat is run separately as a subagent.
import sys, json
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0, r"F:\slk\PycharmProjects\ArkAIology")
from independent_review import run_one
H = Path(__file__).resolve().parent
T = Path(r"F:\slk\PycharmProjects\ArkAIology\episode-pipeline\guardrail_panel_template")
pack = (H / "FILM_PACK.md").read_text(encoding="utf-8")
kjv = (H.parent / "words" / "KJV.txt").read_text(encoding="utf-8")
L = json.loads((T / "lenses.json").read_text(encoding="utf-8"))
lens = {
 "newcomer": L["newcomer"][1].replace("never heard of Moses, Pharaoh, Sinai or Israel as a story", "never heard of Bethlehem, Herod, Micah or the Christmas story"),
 "bible": "You know the Bible well and you must check every factual claim in the SPOKEN and ON-SCREEN lines against the KJV text below (Micah 5:2-4, Matthew 2:1-11, Luke 2:1-16, John 7:41-42, 1 Corinthians 15:3-4). Question 4 is your main job: line by line, mark each claim RIGHT / OVERCLAIMED / UNSUPPORTED / WRONG, quote the line, cite the verse. Also judge the PICTURES for accuracy. Then answer the other questions as a Bible reader.\n\nKJV TEXT (the only authority):\n" + kjv,
 "hook": L["hook"][1],
 "global": L["global"][1],
}
seat = {"claude": "newcomer", "codex": "bible", "grok": "hook", "gemini": "global"}
def prompt(l):
    return (T / "header.txt").read_text(encoding="utf-8") + "\n\nYOUR LENS: " + lens[l] + "\n\n" + pack + "\n\n" + (T / "format.txt").read_text(encoding="utf-8")
def go(n):
    name, ok, out, dur = run_one(n, prompt(seat[n]), H / "_raw")
    (H / f"seat_{name}_{seat[n]}.md").write_text(out, encoding="utf-8"); print(name, ok, round(dur), flush=True)
if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--print":
        print(prompt(sys.argv[2])); sys.exit()
    with ThreadPoolExecutor(4) as ex: list(ex.map(go, list(seat)))
