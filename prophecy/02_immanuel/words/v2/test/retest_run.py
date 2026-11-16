"""Blind X/Y global-audience + guardrail test for Immanuel v2 words. $0."""
import sys, re
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0, r"F:\slk\PycharmProjects\ArkAIology")
from independent_review import run_one
H = Path(__file__).resolve().parent
KJV = (H.parent.parent.parent / "insight_hunt" / "KJV_HUNT.txt").read_text(encoding="utf-8") + "\n" + (H.parent.parent / "KJV.txt").read_text(encoding="utf-8")
X = (H / "CAND_X2.md").read_text(encoding="utf-8"); P = f"""You are ONE independent judge on a blind panel. Everything you need is below. Do not use tools, do not read files, do not ask questions. Output your answer text only.

One version of the spoken words for a 60-second vertical Bible video, read by voice actors over animated comic pictures. Speaker tags: narrator, prophet, angel, jesus. Audience: worldwide, many have no Bible knowledge, many speak English as a second language.

Answer:
1. NEWCOMER: pretend you know nothing of the Bible and English is your second language. In your own words: who is this about, what happened, why does it matter? List any word or line you would not understand.
2. BIBLE READER: is there something here a churchgoer has probably NOT heard before? What?
3. CURIOSITY GAP: does the first line make you want to keep watching (0-10)? Does the ending pay it off (0-10)?
4. GUARDRAILS: who is it for; the main take-away in one sentence; global audience OK?; biblically accurate (check every quote and claim against the KJV below, list any error or overclaim); is this the best version possible - what one change would improve it most?
5. OVERALL 0-10.
Then list the 3 most important fixes, if any. Plain words.

=== SCRIPT ===
{X}
=== KJV (exact) ===
{KJV}"""
for bad in ("CAND_", "Fable", "draft", "seat"): assert bad not in P, bad
(H / "RETEST_PROMPT.md").write_text(P, encoding="utf-8")
def go(n):
    name, ok, out, dur = run_one(n, P, H / "_raw"); (H / f"retest_{name}.md").write_text(out, encoding="utf-8"); print(name, ok, round(dur), len(out), flush=True)
if __name__ == "__main__":
    names = (sys.argv[1] if len(sys.argv) > 1 else "claude,codex,gemini,grok").split(",")
    with ThreadPoolExecutor(4) as ex: list(ex.map(go, names))
