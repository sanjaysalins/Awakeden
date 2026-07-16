import json, re
from pathlib import Path
HERE = Path(__file__).resolve().parent.parent
ALIGN = HERE / "v1" / "narration.alignment.json"
d = json.loads(ALIGN.read_text(encoding="utf-8"))
allwords = d["words"]
first_real = next(i for i, w in enumerate(allwords) if w["end"] > 0)
WORDS = allwords[first_real:]
def norm(s):
    s = s.lower()
    s = re.sub(r"[^a-z0-9']", "", s)
    return s
for i,w in enumerate(WORDS):
    if norm(w['text']).startswith('wherefore'):
        print(i, w)
print("---")
for i,w in enumerate(WORDS):
    if norm(w['text']).startswith('ithappens') or norm(w['text'])=='it':
        pass
# find "It happens"
for i in range(len(WORDS)-1):
    if norm(WORDS[i]['text'])=='it' and norm(WORDS[i+1]['text']).startswith('happen'):
        print('It happens at', i, WORDS[i], WORDS[i+1])
for i,w in enumerate(WORDS):
    if norm(w['text']).startswith('lord') :
        print('lord-ish', i, w)
