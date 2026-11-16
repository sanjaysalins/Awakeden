# Independent review — cursor (OK, 105s)

Independent adversarial review of **SWIRLS_SHORT_PIPELINE_DESIGN v2** against the POC tree (`poc_living_water_ink_style_test/`, `swirls_episode.py`, `swirls_assemble.py`, `swirls_verify.py`, `pipeline/*`).

---

## Feasibility vs codebase

**Hold fix / `score_mix` (Section 4.1, items 2–3)** — Claims draft trim drops `-shortest` (matches today at `swirls_assemble.py:339`) and that **`score_mix.py` need not change** because `tpad=stop_mode=clone` is “cut off by … `-t total`.” Verified: `mix_tail` always appends video `tpad` (`pipeline/score_mix.py:46`). That behavior is implicit and frame-order dependent; Section **4.4** only explicitly tests “last 3 s … not frozen” on a trim build vs legacy, not a **scored** trim path through `assemble()` → `mix_tail`. One typo in ffmpeg filter graph could reintroduce a frozen outro despite Section 2’s “ONE moving clip” back rule.

**`Unit.mode = "trim"` (Section 4.1)** — `Unit` is still `Literal["freeze", "boomerang"]` only (`swirls_assemble.py:33`). The plan is coherent as design, but **4.4** must extend to `sw_a2_unit_duration` trim expectations (`swirls_verify.py:417` uses `max(slot, native)` only for `freeze`) and to any manifest/validator typing, or “six validators green” is overstated.

**Cover animation model** — Section 2 says all units use “Kling 3 Omni.” With `SWIRLS_GEN_PROVIDER=openart`, `swirls_cover.py` already uses `kling-3-omni` (`swirls_cover.py:258–263`). But `swirls_episode.py` still maps covers to **`veo3_1_lite` in `_model_tier_map`** for SW-F1 (`swirls_episode.py:49–51`), and `CoverSpec.clip_duration` still defaults to **4** with a veo comment (`swirls_cover.py:123`). Section 4.5 “not touched” on `swirls_cover.py` is consistent with “no code edits,” but **SWS-G3** (“spec `clip_duration` = `unit_timing.json`”) only works if every pilot `episode.py` sets cover durations and slots match Kling integer lengths—no runner enforcement beyond `plan`.

**`--natural` on `per_turn_synth` (Step 2)** — Not verifiable in this workspace (script lives under `PythonProject1`). If that flag is wrong or absent, `--target 42` behavior and SWS-G2 (“tempo factor … = 1.0”) are undefined.

**Step 1 `narration_pipeline.py verify`** — Swirls episodes keep narration under POC folders; ep12 notes show `narration_pipeline.py --stage verify` with a folder arg (`NOTES.md`). The plan gives a bare path with no **cwd / folder / stage** contract in SWS-G1—same gap v1 cursor flagged.

**Alignment backend (Step 2)** — `pipeline/assembly_align.py` defaults to **`ASSEMBLY_ALIGN_BACKEND=whisper`** (`assembly_align.py:31`). Step 2 names ElevenLabs and matches `build_srt.py` (which sets the env var), but **Step 2’s alignment call does not** unless the operator remembers. Slot boundaries from whisper+interpolation are weaker than the plan’s “REAL alignment boundaries” language (`swirls_assemble.py:299–301`). No gate fails wrong backend.

**`openart_account_get` (Section 3)** — Referenced for `--balance`; only documented in `AGENT_BRIDGE.md`, not wired in `swirls_episode.py` (no `approve` command exists yet). Feasible as attended workflow, not as automated fail-closed spend guard.

**External templates (Step 1, Step 10)** — Paths under `MeekAndMighty\` and `ArkAIology\` are outside `REPO`; no copy or pin in POC. Machine-specific SPOF for every pilot.

---

## Hidden risks / single points of failure

**Clip spend before the “clip gate” (Steps 6b vs 7)** — Table marks Step 7 as “approve the cut (**this is the clip gate**),” but Step **6b** spends “about **1,610 cr**” after only **6a’s one clip**. Bad motion, pacing, or text fade on non-turn pages is discovered only at draft assembly—most animation money is already gone. The plan admits expect “1–3 rounds” for image-content issues (Section 7) but caps rerolls at **2 per item** (Section 3); batch 6b fights both.

**Attended bridge (P1, Section 3, SWS-G9/G13)** — Stills (8× Vision), clips (5-frame Vision), and OpenArt servicing share one live session. Stall or timeout on one bridge job blocks the whole runway; **UNCONFIRMED** spend rows block **all** later paid commands—a single malformed `credits_spent` is a hard stop.

**Manual `--balance` at `approve`** — Live balance typed by the human is not re-fetched at each paid call; concurrent sessions on “about 8,000 cr” (Section 6) can approve overlapping caps.

**`page_plan.json` + `episode.py` (Step 3)** — Two authoring surfaces with **no sync gate**; SWS-G4–G6 lint `episode.py` fields only. Drift between Sonnet’s plan and the executable spec is likely and undetected.

**Three-way token count (Step 3)** — “Spoken tokens … equal in `units.json`, `narration.md` and `narration.alignment.json`” will fight KJV punctuation, multi-voice tags, and `narration-tagged.md` emotion cues unless tokenization is specified; fail-closed without a spec tends to either noise or false PASS.

---

## Over-engineering / premature build

v2 genuinely shrinks v1 (pace test first, one test clip, deferred scaffold). Remaining weight:

- New module **`swirls_short.py`** aggregating timing, **SWS-G1**, G3–G8, spend guard, clip QC, edge scan, freeze check, status (Section 4.2) while **G1 runs at Step 1** before `unit_timing.json` exists—splits gate ownership between modules and `swirls_verify.py` without a single gate registry.
- **`build_timing()`** reimplements ep13’s `_compute_unit_timing.py` (present on disk) instead of importing it—duplicate logic risk (Section 4.2 vs ep13 script).

Section 0 claims “**Build = 1 new module + 4 small commands**” understates work: trim assembly path, `audit_still_v2`, SWS-G15, draft vs scored assemble, and spend wiring across `still`/`animate`/`assemble`.

---

## Missing steps / verification gaps

**Dual still-audit stacks** — Step 5 introduces **SWS-G9 `audit_still_v2`** (fuzzy text, head count). Existing **`audit_page_still`** + sidecars remain what `cmd_verify` / **SW-V2-gate** use on assemble (`swirls_episode.py:193–204`, `swirls_verify.py:365–389`). Section **4.3** does not say assemble migrates to v2 or that G9 replaces SW-V2. You can PASS old audit, FAIL G9, or the reverse—spend and ship safety split.

**Pace test vs real slots (Section 1)** — Fixed **6.0 s** pages and **2.5 s** front do not use `unit_timing.json` voice-driven slots (Section 2: “4.0–8.0 s each”). A PASS on 390 px labels does not validate SWS-G3 timing on the pilot.

**SWS-G1 length rule** — “Total estimate **40.0 s or less**” while format targets “**about 45 s**” film and Step 2 `--target **42**` plus 3 s hold—internal mismatch; margin story is not tied to a single measurement.

**Step 11 publish chain** — `release_check.py`, `cli_publish.py`, `check_packaging.js` are named with no Swirls-specific checklist mapping (v1 reviews noted `_DESIGN_BRIEF.md` line 1; v2 fixes Step 0 template but not `release_check` SYNC gates for POC episodes).

**Stale alignment** — Step 2 says `force=True` after voice; Step 9 `build_srt.py` calls `align(..., force=True)` again. No hash check that alignment matches current `narration.mp3` before Step 3 timing (known repo gotcha in `RESUME.md`).

---

## Reuse

Good: `build_srt.py`, `score_mix.mix_tail`, `openart_bridge`, `narration_gate.py`, `check_landing_hold.py`, existing five validators named in 4.4.

Weak: timing walk not tied to **`_compute_unit_timing.py`**; new fuzzy audit parallel to **`audit_page_still`** instead of evolving one audit; **`sw_l5_word_count_parity`** (`swirls_verify.py:123`) overlapped by three-way count without deprecating the old gate.

---

## Cost / spend

Clean **~$6.80** / worst **~$12.25** (Section 6) is plausible vs ledger examples (e.g. kling-3-omni ~315 cr/clip). **6b before holistic QC** is the main economic risk: worst-case caps assume rerolls on 30% of items but batch 6b spends full clip budget before Step 7. **Step 4 north star “inside the pictures cap”** is not broken out in the approvals table—40 cr ref render can blow the Step 5 mental budget without its own sub-cap.

Vision audits (8 stills + up to 8 clips) are $0 API in plan but **high attended-session cost**, not in the table.

---

## What v2 fixed (credit where due)

Pace test first, trim/hold diagnosis tied to real `-shortest`/`score_mix` behavior, spend fail-closed direction, fuzzy text audit, G7a/G7b split, ep10 lacking `unit_timing.json` acknowledged, independent narration review before owner pick, honest thin-evidence list (Section 7), defer scaffold until pilot.

That is not enough for PASS given **6b/7 spend ordering**, **audit migration gap**, **alignment backend not gated**, and **scored trim + `score_mix` unproven**.

---

VERDICT: REVISE
TOP FIXES:
1. Reorder spend so holistic draft review (Step 7) precedes batch clip animation—or split 6b into per-unit approve after `clipqc`—and align the table with what “clip gate” actually gates.
2. Unify still QA: make `assemble`/`verify` use `audit_still_v2` (or one audit), drop duplicate SW-V2 vs SWS-G9, and add a scored-trim regression test through `score_mix.mix_tail`, not draft-only.
3. Fail closed on alignment (`ASSEMBLY_ALIGN_BACKEND=elevenlabs` + audio/transcript hash before `timing`), reuse `_compute_unit_timing.py`, and specify how SWS-G1 runs `narration_pipeline verify` on a POC episode folder.
