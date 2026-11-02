import sys
from pathlib import Path
sys.path.insert(0, r"F:\slk\PycharmProjects\JesusInTheBible")
import independent_review as IR
BASE = Path(r"F:\slk\PycharmProjects\JesusInTheBible\poc_living_sketchbook\_rewrite_v4\panel_jl")
OUT = BASE / "blind_r2"; OUT.mkdir(exist_ok=True)
ROLE = {
 "claude": ("a viewer in another country who reads English as a second language and knows NOTHING about the Bible", False),
 "gemini": ("a teenager who has never opened a Bible and is half-listening on a phone", False),
 "codex": ("a Bible-reading Christian who knows the King James Bible well and checks every claim", True),
}
QS = """Answer these, short and plain. Give each score as a number 0-10.
1. WHO is speaking or who is this about, and WHAT happened, and WHY does it matter? (one line each)
2. WHO is this short for? One line.
3. MAIN TAKEAWAY in one sentence.
4. GLOBAL: copy any word or line you would not understand or would have to re-hear. Say NONE if none.
5. BIBLE: is anything doctrinally off, misquoted, or stated as the Bible's claim when it is only a Christian reading? Say NONE if none. (If you know the Bible, check quotes against the KJV.)
6. HOOK: the first 2 seconds, did it make you want to hear the answer? Did the ending PAY OFF that question? Score hook 0-10 and payoff 0-10.
7. LANDING: could the last line close a different short unchanged? Score 0-10 for how specific it is to THIS story.
8. Overall clarity 0-10. Is this the best version possible? If not, name the ONE thing you would change."""
for f in sorted((BASE / "candidates").glob("jl_FINAL*.txt")):
    text = f.read_text(encoding="utf-8")
    for seat, (role, bible) in ROLE.items():
        outp = OUT / f"{f.stem}__{seat}.md"
        if outp.exists() and len(outp.read_text(encoding="utf-8", errors="ignore")) > 100:
            continue
        prompt = f"""You are {role}. You just watched a 60-second illustrated short film. You only heard the narration below (lines in [brackets] are silences with a picture). You know nothing else about it. Do not use tools.

--- NARRATION ---
{text}
--- END ---

{QS}"""
        name, ok, out, dur = IR.run_one(seat, prompt, OUT)
        outp.write_text(out, encoding="utf-8")
        print(f.stem, seat, "ok" if ok else "FAIL", round(dur), flush=True)
print("ALL DONE", flush=True)
