# data/kjv_full/ — full KJV text corpus

**Provenance:** copied verbatim (2026-07-30) from the sibling project
`C:\Users\sanjay\PycharmProjects\ArkAIology\kjv\Bible-kjv-master\` — a
public-domain King James Version text, one JSON file per book (66 books)
plus `Books.json` (canonical book-name/order list, not a book of the Bible
itself). This repo does not modify or write back to the ArkAIology copy;
this is a one-time, read-only copy so `pipeline/concordance.py` has no live
runtime dependency on the sibling repo's path.

Format (unchanged from the source):

```json
{"book": "Matthew", "chapters": [{"chapter": "1", "verses": [{"verse": "1", "text": "..."}, ...]}, ...]}
```

Consumed by `pipeline/concordance.py` (the Concordance Loom — see
`.claude/skills/concordance-loom/SKILL.md`). Do not hand-edit; if the
upstream corpus is ever corrected, re-copy from ArkAIology rather than
patching here.
