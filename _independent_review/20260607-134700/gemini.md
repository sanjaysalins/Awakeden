# Independent review — gemini (OK, 67s)

This is an adversarial code review of Phase B (`pipeline/kjv_strict.py`). The implementation contains severe logical gaps that compromise its role as a strict verification gate.

**1. FALSE-PASS: Out-of-Order & Overlapping Ellipsis**
*Location:* `_fragments_in` -> `if f and f not in text: return False`
*Critique:* The function verifies each ellipsis fragment independently against the entire verse string. It completely fails to enforce sequential order or prevent overlap. A drastically altered quote like `"forsaken me … My God"` will falsely verify as "OK" against Psalm 22:1 because both fragments exist *somewhere* in the text. 

**2. FALSE-BLOCK: Missing Boundary Punctuation**
*Location:* `_TERMINAL = ' .!?"\'’”'`
*Critique:* The terminal strip list omits commas (`,`), colons (`:`), and semicolons (`;`). If a scriptwriter grammatically adapts the trailing boundary of a quote (e.g., using `"my brethren,"` in a sentence where the KJV text has `"my brethren:"`), `strip(_TERMINAL)` leaves the trailing comma intact. The rigid substring check then fails, flagging an honest quote as a `MISQUOTE`. This directly contradicts the docstring's claim of allowing honest truncation boundaries.

**3. FALSE-PASS: Inline Resolution Cross-Verse Masking**
*Location:* `_chapter_text` -> `return _canon(_strip_markers(" ".join(chapters[chap - 1])))`
*Critique:* Concatenating an entire chapter with spaces (`" ".join`) creates a single contiguous string where the end of one verse touches the start of the next. An inline quote that falsely bridges two unrelated verses will seamlessly match as a substring. Furthermore, searching the whole chapter allows a corrupted quote to pass if its fragments randomly match words scattered across totally different verses in that chapter.

**4. FALSE-BLOCK: Dash Whitespace Strictness**
*Location:* `_canon` -> `s.replace("—", "-").replace("–", "-")`
*Critique:* The canonicalizer normalizes the dash character but ignores surrounding whitespace. If the KJV corpus contains unspaced dashes (`"worm-and"`) and the user writes spaced dashes (`"worm - and"`), the verification will FALSE-BLOCK a correct quote.

**5. ROBUSTNESS: Fragile Hardcoded Paths**
*Location:* `_KNOWN` array and `_load_sg_kjv()`
*Critique:* The fallback imports rely on a hardcoded absolute Windows path (`r"C:\Users\sanjay\..."`) and an extremely fragile sibling-repo assumption (`here.parents[2] / "PythonProject1"`). If `JITB_SHORT_GATE_KJV` isn't set, this guarantees an immediate crash in CI or on any other machine. It is a severe deployment risk.

VERDICT: REVISE
TOP FIXES:
1. Rewrite `_fragments_in` to enforce sequential, non-overlapping substring matching (e.g., keeping track of `last_index` using `text.find(f, start)`).
2. Add `,`, `:`, and `;` to `_TERMINAL` to prevent false-blocking legitimate boundary punctuation changes.
3. Do not `" ".join()` entire chapters for inline resolution; check the span against each verse individually or enforce verse boundaries.
