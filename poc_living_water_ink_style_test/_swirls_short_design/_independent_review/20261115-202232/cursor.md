# Independent review — cursor (OK, 95s)

## Independent review — Swirls SHORT pipeline design v3

The design is more disciplined than v2 on spend, trim, and phone-first gates, but it still treats **target state as shipped state**, leaves **critical path holes** between phases, and assumes **tools and paths that are not in this repo** or not wired yet.

---

### Feasibility vs codebase (plan ≠ disk)

1. **Section 6 “fixed” table vs §9.1 “REDO”** — Rows like “**Fixed.** Hashes taken at request and at receipt; `clip_fresh` compares file hashes to the receipt” (panel point 18) and “**Fixed.** Section 5: guard inside `openart_bridge.submit`” (point 17) are **not implemented**. On disk, `clip_fresh` still keys off `clipqc.json` + **current** still hash (`swirls_short.py` ~695–707), and `openart_bridge.submit()` has **no** `GUARD` / `REQUIRE_GUARD` hooks (`test_the_cross/openart_bridge.py` ~45–59). `_guarded_render` still uses `_bridge_credits` mtime scraping (~79–98 in `swirls_episode.py`), which v3 explicitly retires. The plan is internally inconsistent: §9.1 admits rebuild; §6 reads as done.

2. **“`RUN = … swirls_episode.py`” command surface** — Step table commands (`words`, `ok`, `align`, `animatic`, `adopt`, `paid`, `confirm --void`, `still ref:<name>`) are **absent** from the runner’s `choices=[...]` list (`swirls_episode.py` ~445–446). Pilot ops assume a CLI that does not exist yet.

3. **Frame-exact trim (§1 “`-frames:v N`”, cumulative `B(k)`)** — §9.1 says redo `make_trim`; current `make_trim` still uses **`-t f"{slot:.3f}"`** (`swirls_assemble.py` ~226–232), not per-unit frame counts. T1 is specified; the behavior §1 binds is not on disk.

4. **`build_timing` / alignment gate (Step 3 + T10)** — Plan: `timing` **refuses** stale `narration.alignment.meta.json` / non-ElevenLabs backend. `build_timing()` today only needs `narration.alignment.json` (~86–94 in `swirls_short.py`); **no** meta-file check. Step 2’s `align` + meta write are likewise unimplemented in the runner.

5. **Spend guard §5 vs `swirls_short.py`** — Design: owner gates before spend, 12h approval expiry, price from **payload**, `UNRESOLVED`, `paid` for USD steps, `confirm --void`. Code: `request_spend` checks approvals/caps only (~575–604); status is **`UNCONFIRMED`** not `UNRESOLVED` (~607–615); **`REQUIRES = {"clips": "clip_test"}`** only (~475) — **no** `clip_test_look`, `stills_animatic`, `voice_ear`, etc.; `approve()` is **credits-only** (`cap_cr` / `balance_cr`, ~512–537) while the step table prices **voice/score in USD**.

6. **§0 fact table vs Step 9 SRT** — “`build_srt.build()` calls `align(force=True)` every time” matches `build_srt.py` (~54). Step 9 promises `force=False` when meta matches and a `build()` signature change in §9.1 — **not built**. Risk of accidental re-align spend if builder only updates the runner, not every `build_srt` caller/copy.

7. **Step 11 publish chain** — “`check_packaging.js`” is **not in this repo** (used from `MeekAndMighty\_pipeline\` in `poc_desert_storybook_heroes\EPISODE_PLAYBOOK.md`). Same pattern as templates copied from **other projects** (Step 1): feasible only if those paths exist on the build machine; no vendoring or fallback in the plan.

8. **`release_check.py` on POC episodes** — Step 11 ends with `REPO\release_check.py` with **no** Swirls-short / `poc_living_water_ink_style_test` mapping spelled out. Earlier panel notes already flagged SYNC gates for POC layout; v3 does not close that.

9. **§0 “139 checks, ALL PASS”** — True for `_validate_swirls_short.py`, but those tests exercise the **current** guard (`request_spend` / `confirm_spend`), not T6’s **`openart_bridge.submit`-driven** guard. Passing today does **not** verify §5.

10. **T3: “equals ep13's … `unit_timing.json` for all 11 units”** — ep13 is an **11-unit** long episode (`f01`–`f09`; `unit_timing.json` on disk). The locked product is **8 units**. Equality on ep13 does **not** prove 8-unit slot/`clip_duration` math or §8 “~53 clip-seconds” unless a dedicated 8-unit fixture exists (T12 synthetic only; no golden 45s episode).

11. **Price constants** — §8 marks Kling/stills **VERIFIED 2026-11-15**; `price_clip()` docstring still says **“UNVERIFIED rate”** (`swirls_short.py` ~490–491). Builder task says mark VERIFIED — drift between design verification and code.

---

### Hidden risks / single points of failure

12. **P1 “Attended run” + open row blocks all spend** — §5: “An open row blocks every later paid command.” Combined with bridge **3600s timeout** (`openart_bridge.py` ~33) and **no HF auto-fallback**, one hung MCP job freezes the **entire** episode until manual `confirm`. §6 point 36 accepts bridge SPOF but understates **cascade** (one UNRESOLVED row + 6b one-by-one clips).

13. **ElevenLabs-only alignment, no fallback** — Step 2: “**No whisper fallback**.” Default backend in repo is still **`whisper`** (`assembly_align.py` ~31). Forced alignment needs key permission (module comment ~28–29). Any API/outage **blocks** Step 3+ with no degraded path.

14. **`_bridge_credits` until §5 lands** — Credits confirmed from gen_archive mtime (`_guarded_render` ~93) can be **wrong or missing** → `UNCONFIRMED` and global block. v3’s payload receipt fix is necessary, not optional.

15. **G14 until receipt hashes ship** — Swapping **mp4** while still unchanged would pass today’s `clip_fresh`. Plan fixes this in §5/§9.1; until then §6 point 18 is **misleading**.

16. **12-hour approval expiry vs 6b batch** — “approval is under 12 hours old” (§5) vs human phone gates on **every** still and clip. A long session can **expire mid-batch** and refuse legitimate continues unless re-approve is specified (re-approve flow is thin).

17. **SWS-G1k** — “continuous run of words inside the KJV text” (Step 1) with `fetch_kjv` per ref (`scripture.py`) is brittle: multi-ref spans (`John 1:19-29` + `Isaiah 40:3`), ellipses, confessionals not verbatim, and normalization are **unspecified**. Easy false FAILs or false PASSes; no test for **cross-verse** pilot lines beyond “John 1:23 run” (T5).

18. **SWS-G8 motion carrier** — “FAIL if more than one” page where only the speaker could move (Step 3 table). §11 admits pilot is **talk-heavy** — structural FAIL risk before first clip dollar, with no override path except `_overrides.json` (which cannot excuse guard, not gates — but encourages override culture).

---

### Over-engineering / prove-before-build

19. **Phase A–C before pilot (P3)** — Prerequisites: “Build order phase A–C is done.” Phase C exit is **T12** end-to-end dry run — large surface (guard rebuild, frame trim, lint_kjv, animatic, …) **before** Isaiah 40 words on a phone. Row 35 **rejects** “pipeline before hand-made pilot” but P3 + T12 effectively **require** most of the factory first.

20. **Step 1 panel stack** — “Blind writers (Fable + 4 others…)” → judge → “blind guardrail panel (5…)” → `independent_review.py` **before** owner page. Heavy **CLI/quorum** cost (§7) with **no** line in §8 cost table (only dollar stops).

21. **Seven money stops + seven owner HTML gates + Step 10 film panel** — Appropriate for production, heavy for **first** 45s proof where §11 lists thin evidence (6 s read, 2–3 s cover, one motif page, one clip prompt test).

22. **“no new failure against the baseline” (§9.2 phase A)** — Two of five legacy validators already fail on **unrelated** `swirls_page` prompt drift. Baseline rule can **mask** regressions in shared prompt code the short path still uses (`swirls_page` / `swirls_cover` both call `openart_bridge.submit`).

---

### Missing steps / verification gaps

23. **T12 vs Phase D ordering** — T12 sequence includes `assemble --score` and caps at “step 10”; **Phase D** places `swirls_score.py` / `swirls_sfx.py` **after** “Phase C is not done until T12 passes.” T12 cannot call a real scored assemble unless score is **mocked** — not stated. Step 8 pilot depends on `swirls_score.py`, which is **deferred** (“needed only from step 8 of the pilot”).

24. **T12 ends at `status` step 10** — Does not exercise Step 9 SFX, Step 10 film guardrail, Step 11 publish, or real Vision still/clip reads. “Every step succeeds” is **not** the full 0–11 table.

25. **Poster gate “(film final)”** (§5 approvals table) — No named `ok` gate (e.g. after `_FILM_REDTEAM.html` or post–Step 9 final). **`approve poster`** prerequisite is undefined in the Step 10/11 flow.

26. **G13 automation gap** — Table says Vision on 5 frames; `clipqc` docstring: G13 “**left to the human** reading the strip” (`swirls_short.py` ~711–712). No enforced automated G13; defect detection in 6b still **session-dependent**.

27. **9:16 still pricing** — §0: “confirm 9:16 on the first receipt.” No acceptance test; wrong aspect pricing breaks §5 payload price table.

28. **`episode.py` before north-star still** — Step 4 runs `still <north_star>` from specs written in Step 3. No gate that **`plan` passed and files committed** before first 160 cr beyond human discipline.

29. **Dual ledgers** — “Each ask also gets its row in `REPO\data\spend_ledger.jsonl`” (§5) plus episode `spend_log.jsonl`. No reconciliation rule if they diverge.

---

### Reuse / duplication

30. **“Promotion, not import” of `_compute_unit_timing.py` (§6 point 5)** — Reasonable, but T3 only regression-tests **ep13 long** timing, not reuse of one-off script edge cases (`assert 227`, import side effects).

31. **Owner pages “copy ep16's pages”** — Manual copy deferred (§10); no schema for gate names/links → **`ok` drift** risk between HTML and `approvals.json`.

32. **`swirls_cover.py` + `swirls_page.py` both `submit()`** — Guard at `submit()` (§5) is the right choke point; until it ships, **north-star cover** and page stills can diverge from episode runner guard (`_guarded_render` only on some paths).

---

### Cost / spend justification

33. **§8 ~$6.84 clean / ~$10.70 capped** — OpenArt clip line is grounded (35 cr/s, ~53 s). **Voice, score, poster** “carried from v2” with “re-quote from ledger at ask time” — weak for a **FINAL binding** doc; ElevenLabs score ~$1.00 is not re-verified here.

34. **Attended Vision** — “About 8 still reads + 8 clip reads per film, $0” (§6 point 37) — real **time** cost per episode; omitted from operational planning next to §7’s 600s/900s panel timeouts.

35. **Clip caps assume clean run** — 6b “stop on first defect” + “at most 2 rerolls per item” can blow **2,450 cr cap** without explicit cap math for rerolls (only “one change each”).

36. **Ref sprawl on north-star step** — “recurring subject not on that page gets one single-subject render (40 cr)” (Step 4) — no cap on **count** of extra refs; 160 cr headline can be wrong for multi-character pilot.

---

### Smaller inconsistencies

37. **Step 2 `--target 44`** vs §1 “voice … target **42.0**” — Allowed by bands but nudges synth toward high end; no gate ties `--target` to pre-money “estimate … **38.0-42.0**”.

38. **§0 “Builder's new tests … 139 checks, ALL PASS”** paired with “**3 pass, 2 fail**” on old validators — Good honesty on five validators; **“v2's all five stay green was wrong”** should imply short work must not rely on those two for shared prompt safety.

39. **Publish anchor** — `John 1:19-29 (…)` matches `_ANCHOR_REF_RE` (`upload_engine.py` ~165–179). OT in description only is manual (Step 11) — SYNC/content risk if packaging omits Isaiah.

40. **`units.json` token rule vs alignment** — Step 3 count check is strict (good); any SSML/pause artifact in alignment text not in `narration.md` will hard-fail timing — not documented for audio pipeline output shape.

---

**Summary:** v3 is a strong spend-and-trim specification, but it is **not build-complete**, **T12/Phase D/Step 8 conflict**, **owner-gate/spend-guard gaps** vs §5, and **publish/SYNC** assumptions outside the repo are under-specified. Treat §6 “Fixed” as **intent** until §9.1 is done and T6/T7/T12 target the **new** guard, not today’s `_guarded_render`.

VERDICT: REVISE  
TOP FIXES:  
1. Reconcile §6 “fixed” claims with §9.1: one explicit “shipped / not shipped” matrix; do not call guard, G14 receipts, owner gates, or `openart_bridge.submit` done until T6/T7 pass on the new hook.  
2. Fix phase ordering: either move minimal `swirls_score` mock into T12, drop `assemble --score` from T12, or move Phase D before Phase C exit; define poster’s concrete `ok` prerequisite.  
3. Close operational gaps: implement full `swirls_episode.py` command/gate table (incl. USD `paid`, `ok`, meta-gated `timing`), vend or document `check_packaging.js` + Swirls `release_check` path, and add an 8-unit golden timing test—not only ep13’s 11 units.
