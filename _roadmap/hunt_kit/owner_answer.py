"""python owner_answer.py <topic_dir> <card> YES|NO "<note>"   - records the owner's answer to "Had you seen this before?"
Appends a dated line to <topic_dir>/OWNER_ANSWER.md. Words may start only when the LATEST line for the chosen card says NO."""
import datetime, sys
from pathlib import Path
T, card, ans = Path(sys.argv[1]).resolve(), sys.argv[2].upper(), sys.argv[3].upper()
if ans not in ("YES", "NO"): sys.exit('owner_answer: answer must be YES or NO')
note = sys.argv[4] if len(sys.argv) > 4 else ""
from gate import evaluate
import hashlib
try:
    row = next((r for r in evaluate(T)["rows"] if r["cid"] == card), None)
except Exception as e:
    sys.exit(f"owner_answer: REFUSED - gate cannot run here ({e.__class__.__name__})")
if not row or row["why"]:
    sys.exit(f"owner_answer: REFUSED - card {card} is not a current PASS in the gate")
h = hashlib.md5((T / "CARDS.md").read_bytes()).hexdigest()[:8]
note = f"{note} [CARDS {h}]"
f = T / "OWNER_ANSWER.md"
if not f.exists(): f.write_text("# OWNER ANSWER - Had you seen this before?  NO = new to the owner = words may start\n\n", encoding="utf-8")
with f.open("a", encoding="utf-8") as h: h.write(f"- {datetime.date.today()} | card {card} | {ans} | {note}\n")
print("wrote", f, "->", f"card {card} {ans}" + ("  (words may start)" if ans == "NO" else "  (words NOT allowed)"))
