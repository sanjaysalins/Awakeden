# Independent review — codex (OK, 222s)

**Findings**

1. The execution path will silently skip the intended redo. The plan says “via the existing `_render_images_16x9.py` path” and “Re-animate ONLY the redone scenes,” but the real scripts are idempotent: existing PNGs are skipped in [_render_images_16x9.py](C:/Users/sanjay/PycharmProjects/JesusInTheBible/longform/_render_images_16x9.py:79), existing MP4s are skipped in [_animate_16x9.py](C:/Users/sanjay/PycharmProjects/JesusInTheBible/longform/_animate_16x9.py:54), and existing continuations are skipped in [_animate_directional.py](C:/Users/sanjay/PycharmProjects/JesusInTheBible/longform/_animate_directional.py:76). “delete its stale `_cont*` clips” is not enough; S13’s base MP4 would still seed from stale visuals unless it is backed up/replaced too.

2. “STYLE ref + a CHARACTER ref attachment” is not currently wired, and the plan undercounts refs. The real `NBPProvider` only attaches a Jesus variant ref when `scene.jesus_variant` is set; see [visual_render.py](C:/Users/sanjay/PycharmProjects/JesusInTheBible/pipeline/visual_render.py:155). S15 needs at least Jesus + Ethiopian/S14 + style; S13 needs S14 + style. A single generic “CHARACTER ref” is not a complete design.

3. The KEEP list is false. The phrase “KEEP ... S4, S5, S6, S7...” includes S7, but S7 is a literal framed/triptych composition, directly violating “No frames: no panels, triptychs, dividers, picture-frames.” S16 is also kept despite the scene plan asking for “the robed crucified Servant” while the still shows Christ standing under light, no cross. The “5 core scenes” scope is therefore too narrow.

4. The plan risks canonizing a bad S14. “S14 is the best; redo S13 + S15 to match it” and “SAME ornate gilded chariot” propagate an ornate carriage/coach look, not an obviously 1st-century chariot. If first-century artifacts are locked, S14 needs scrutiny before it becomes the reference anchor.

5. The audit step assumes more than the current tooling enforces. “Per-PNG Claude Vision content audit (subject + dress-era + no-frame check)” is not what the generic audit reliably does today; it checks subject/banned tokens/anatomy, not a focused dress-era canon. Worse, on Anthropic usage cap it returns `passed=True` with a warning in [visual_render.py](C:/Users/sanjay/PycharmProjects/JesusInTheBible/pipeline/visual_render.py:427), so retry-on-fail would not fire.

6. The cost math is optimistic and violates the “ask before spend” discipline. “5 core scenes: ~10 image renders (≤3 attempts/scene...≈ $5)” is wrong at its own cap: 5 scenes × 3 attempts × $0.50 = $7.50 before optional S2/S11, added missed scenes, Vision calls, or failed video retries. The plan has a stop cap, but no explicit pre-spend approval gate.

7. “Only the changed scene segments differ” is not true for the real assembler. [_assemble_16x9.py](C:/Users/sanjay/PycharmProjects/JesusInTheBible/longform/_assemble_16x9.py:45) regenerates every `_assembly/scene_XX.mp4` and overwrites the final output with `-y`. The plan needs a concrete backup/compare step, not just “Keep `.frozen.bak`.”

8. The scripture-text requirement conflicts with the prompt base. The plan says “any visible scripture = Hebrew ... or Greek,” while the style anchor includes “no text,” and the actual renderer sets `VISUAL_STYLE_TAIL = "no text..."` in [_render_images_16x9.py](C:/Users/sanjay/PycharmProjects/JesusInTheBible/longform/_render_images_16x9.py:49). If legible Hebrew/Greek matters, do not rely on NBP to hallucinate it; composite controlled text or keep it non-legible.

VERDICT: REVISE
TOP FIXES:
1. Add an explicit backup/remove/replace workflow for old PNGs, base MP4s, and S13 continuations before rerendering.
2. Re-audit scope before spend: S7 and likely S16/S14 cannot stay in KEEP under the stated rules.
3. Specify the actual ref/audit implementation: multi-ref NBP support, custom dress/no-frame audit, fail-closed behavior, and corrected budget with pre-spend approval.
