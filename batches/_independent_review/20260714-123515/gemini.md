# Independent review — gemini (OK, 95s)

I have reviewed the v5 rollout plan. While previous iterations patched several holes, this version still relies on fragile human promises to protect system integrity and budget. Here are the critical failures:

**1. Cross-Piece Dependency Timebomb (Single Point of Failure)**
*Citation:* "Wave E must never move/delete assets other pieces reference (`it_is_finished` refs `../father_forgive_them/visual/_byteplus/face_on_cross_fix2.png`)"
*Finding:* This is a massive architectural risk. `it_is_finished` (Wave A) is hard-coupled to an asset inside `father_forgive_them` (Wave E). Wave E is explicitly defined as a "greenfield mocomic→livingpage migration" that will happen *after* Wave A ships. Greenfield migrations inherently restructure or regenerate their `visual/` folders. Relying on a human behavioral rule ("must never move/delete") to protect a shipped, locked piece from a future greenfield migration is a guaranteed point of failure.

**2. Stop-Loss Blind Spot (Budget Overrun)**
*Citation:* "billed possibly ~+15cr in 502s — limit (c), balance eyeball... The stop-loss refuses PROJECTED breaches (spent + one clip > cap)... Counts attributable ledger rows... cross-checked against rendered mp4s on disk"
*Finding:* The automated stop-loss is blind to 502/NSFW blocks because they "leave neither row nor mp4". If the system has already leaked ~15cr to 502s, the stop-loss calculation (`ledger_or_disk + 1_clip`) is under-reporting the real spend by 15cr. This means your "fail-closed AT THE CHOKEPOINT" will silently allow the real-world HF balance to breach the 485cr hard cap before the code exits. The machine bar is not a true ceiling if it ignores known ghost-spend.

**3. Bulk Guard Loophole (False Assumption)**
*Citation:* "A(b) invocations MUST use `--only <ll_slugs>` — a bare `--stage animate` re-renders every hash-stale clip and burns the envelope... refuses when >2 clips would render (BULK GUARD, exit 5)"
*Finding:* If a user forgets `--only` (which they will), the bulk guard only trips if `>2` clips would render. If there are exactly 1 or 2 hash-stale *non-living-light* clips, the guard allows them to render, instantly burning 7.5–15cr of the envelope on the wrong assets. A human "MUST" rule is not a system constraint.

**4. Manual Verification of Machine-Readable Data (Missing Automation)**
*Citation:* "Human checklist per piece... 3. audio-diff: spec beat `sfx` arrays vs the piece's REAL bed builder... as discovered by `cli_livingpage._sfx_builder()`"
*Finding:* You are asking a human to manually cross-reference an array in a JSON/spec file against a Python dictionary. This is highly error-prone and tedious. Since you already have a programmatic way to discover the builder (`cli_livingpage._sfx_builder()`), this should not be a human checklist item.

VERDICT: REVISE
TOP FIXES:
1. Break the cross-piece dependency: copy `face_on_cross_fix2.png` into `it_is_finished` (or a shared `_assets` folder) before Wave A locks so Wave E's greenfield migration doesn't break it.
2. Add a manual ghost-spend offset to `rollout_spend.check()` so 502/NSFW blocks are factored into the calculation, preventing the automated stop-loss from breaching the 485cr hard cap.
3. Automate the `sfx` array vs bed builder diff as a fail-closed gate check instead of relying on a human eyeball check.
