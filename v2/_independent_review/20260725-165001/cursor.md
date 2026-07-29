# Independent review — cursor (OK, 141s)

## Independent adversarial review — COMIC PAGE PIPELINE PROPOSAL

### Feasibility vs. real codebase / tools

**1. Word alignment is mislabeled and not wired as a prerequisite step.**

§1 table (line ~63): *"word-level forced alignment | existing WhisperX path (`assembly_align.py` produces it for assembly)"* — **wrong on two counts**.

- `pipeline/assembly_align.py` defaults to **local faster-whisper** (`ASSEMBLY_ALIGN_BACKEND`, default `"whisper"`), not WhisperX. WhisperX is the long-form **caption** path (`veed_io`, `/caption` skill).
- Alignment is **not** produced at narration lock. It is produced later, on demand, as `narration.alignment.json` at the v1 root — and only when someone runs `assembly_align.align()`. The prior E2E review already flagged this exact false claim (`v2/_independent_review/20260725-102625/cursor.md`).

CP-1 depends on per-word timestamps for page boundaries, bubble pop timing, and `focus` windows — but CP-1..7 never include an explicit **CP-0: run alignment** step. Calling it "existing" in §1 hides a hard gate.

**2. Shorts canvas orientation is unspecified against `grid_choreography.py` defaults.**

§6 (line ~187): *"`grid_choreography.py` with: layout from the plan..."* — the module defaults to **1920×1080 landscape** (`W, H = 1920, 1080` in `panel_animator/grid_choreography.py`, argparse `--w`/`--h` defaults). A 9:16 short needs explicit `--w 1080 --h 1920`. The plan never states this for the short format. The POC text layer hardcodes **1536×2752** (`poc_thief_e2e/_comic_text_layer.py`), which doesn't match either default — cell-relative text math won't port without a declared output contract.

**3. Narration-timed spotlight is described as a "small upgrade" but doesn't exist.**

§6 (line ~190): *"Small, contained upgrade: `render()` accepts explicit focus windows"* — **`activeness()` is still a uniform metronome** (`per_panel` seconds, cyclic `% n`). The JSON schema's per-panel `focus` windows (§2, line ~108) have no consumer in code. This is a rewrite of the camera model, not a parameter tweak. The POC explicitly documented why post-composite text fails when the virtual camera pans (`_comic_text_layer.py` lines 46–50) — the fix requires in-pass, cell-relative drawing tied to a focus model that isn't built.

**4. CP-4 boomerang/loop extension has no reusable implementation in `panel_animator/`.**

§5 item 1 (line ~167): *"Boomerang extension... the project's standard static fill"* — boomerang lives in **`longform/_assemble_16x9.py`** (scene-level assembly), not in panel-level tooling. `panel_animator/` has **zero** boomerang/forward_slow code (grep confirms). CP-4 is a new subsystem, not a reuse of "the project's standard."

**5. Physics gate doesn't fit the proposed data contract.**

§5 item 1 (line ~166): *"Physics gate applies (`physics-motion-check`)"* — `physics_motion_check.py` scans **`scene_plan.json`** `subject_block` fields. The plan's contract is **`page_plan.json`** with a `composition` string. The tool won't run as-is; the plan doesn't budget adapting it or define fill metadata on panels.

**6. Foundation technique spec is explicitly unstable.**

Opening block (line ~8): technique evidence stands on `.claude/skills/comic-strip-native/COMIC_STRIP_NATIVE_SPEC.md` — that file's header says **"DRAFT — NOT LOCKED"** with independent review **FAIL/REVISE** (gemini FAIL, others REVISE). Building a full system spec on top of an unsettled technique spec is a single point of failure the plan understates despite §13 open items.

---

### Hidden risks, false assumptions, single points of failure

**7. "Freeze fix half-done" overstates what's landed, understates what's left.**

§5 item 2 (line ~173): *"grid_choreography freeze fix... already half-done (2026-07-25), must be finished"* — the **frame-wrap fix IS in code** (lines 155–183 of `grid_choreography.py`: loop `i % len(src_frames)` instead of holding last frame). What remains is (a) **pre-extended source clips** via boomerang (CP-4), (b) **narration-timed focus**, and (c) verification that wrap-only loops don't read as stroboscopic repetition on 12–16s dwells. RESUME.md documents that wrap alone wasn't enough — boomerang on sources was still required for the Zacchaeus regression class.

**8. Two loop mechanisms can fight each other.**

CP-4 extends clips to page dwell via boomerang/crossfade; CP-5/`grid_choreography` **also** loops short sources (`i % len(src_frames)`). If CP-4 fails silently or physics gate routes a panel to forward-loop-only, the grid's modulo loop becomes the fallback — exactly the visible-repetition/freeze class this plan claims to eliminate. No step verifies the **combined** behavior end-to-end before Rung 2 spend.

**9. Layout variety rule vs. panel-count logic is underspecified.**

§2 step 6 (line ~89): layouts from `LAYOUTS` include fixed cell counts (2x2=4, 3-big-left=3, etc.), while step 5 allows **1–4 panels per page**. The plan says full-bleed hero skips the grid, but never defines: (a) what happens when beat density says 2 panels but variety forbids repeating the previous layout and only 2x2 was used; (b) whether 4-panel pages always use 2x2 or can use asymmetric layouts; (c) padding/empty cells. This will break CP-G6 "layout variety" checks or force ad-hoc overrides.

**10. "Last page = Christ" is not machine-checkable from the shown schema.**

CP-G6 (line ~255): *"last page = Christ"* as a deterministic code gate — `page_plan.json` example has no `jesus_variant`, `sacred`, or subject tag field. Without a structured landing marker, CP-G6 either false-passes on string grep or requires an LLM judge (not $0).

**11. Hailuo-as-calm-tier rests on n=2.**

§4 table + honest evidence note (lines ~157–161): *"Hailuo... validated zero-invention on THESE ink panels (2 tests)"* — two panels is not production tiering evidence. The plan correctly defers Seedance to Rung 1 bake-off but simultaneously lists Seedance as the *"locked project default for composited panels"* in the tier table — contradictory defaults that will cause spend on the wrong model if someone runs CP-3 before Rung 1 completes.

---

### Over-engineering / premature building

**12. §12 bundles four code units before the paid ladder proves the hardest integration.**

§12 items 1–4 (lines ~282–290) include `cli_comic.py` + full runner orchestration alongside `page_compose.py` (focus windows + freeze + boomerang inputs + in-pass text). Item 2 alone is four subsystems. The validation ladder (lines ~292–301) is sound in ordering **spend**, but the build plan doesn't **forbid** writing the orchestrator before Rung 1 passes — repeating the pattern of building wiring before the composite pass is proven (the POC validated post-composite text; production explicitly rejects that path).

**13. Third parallel entry point without retirement plan.**

§12 item 4: `cli_comic.py` joins `cli_pipeline.py`, `cli_visual.py`, `cli_livingpage.py`, and `run_piece.py`'s livingpage path. No migration/deprecation for livingpage (`livingpage_short.spec.json` + `build_livingpage_16x9.py`) despite the technique spec deprecating painted-comic/Remotion. Risk of two comic-grid systems diverging on gates, alignment paths (`audio/alignment.json` vs `narration.alignment.json`), and assembly.

---

### Missing steps, edge cases, verification gaps

**14. Triple-caption conflict with binding INV-16 not resolved.**

§7 muted-viewing note (line ~218) + §8 CP-7 (line ~227): in-pass bubbles/captions **plus** existing serif/WhisperX caption stage. `/caption` skill: *"Caption is the final step on every finished clip (INV-16)"* with ivory WhisperX burn-in. The plan defers muted-viewing policy to user confirmation but doesn't address **INV-16 compliance** — skip captions (gate fail), caption everything (double text over bubbles), or caption only non-bubbled lines (needs a new caption filter spec). This is blocking for release, not cosmetic.

**15. Reuse workflow skips the actual reuse engine and its gates.**

§3 (line ~130): *"check the banks (`asset_index`, shorts clip bank, stills banks)"* — production reuse runs through **`pipeline/clip_reuse.py` + `clip_library/`** with **coherence verification (INV-23)**, clip_qc, element_gate, and topical-fit rules. `asset_index.json` is a parallel index (`run_piece.py register`). The plan never mentions coherence/clip_qc before banking, so reused panels can enter the bank uncleared and fail later — or worse, ship.

**16. Panel variety gate exists but isn't in the gate registry.**

§9 (line ~232): tags per `panel_variety_lint` — the shared implementation is **`pipeline/panel_variety.py`**, wired to **livingpage beat specs**, not `page_plan.json`. No step converts page plans into the lint's expected shape or mandates `visual_tags.json` creation for new comic pieces (required once the first multi-panel grid ships — grandfathering ends).

**17. Cost model omits material Opus spend and mandatory review.**

§11 (lines ~262–276): compares to *"current locked pipeline ≈ $23/short"* but counts only stills + animation. Missing: CP-1 **LLM composition pass** (scene-plan analog ≈ $3–5 Opus), revision loops, **independent audit** (project-enforced), and still Vision/content audits if reusing `visual_render.verify_image` patterns. Short cost parity claim is optimistic.

**18. Rung 1 budget may be tight and excludes planning spend.**

§12 Rung 1 (line ~293): *"~$8–10"* for 4 stills + 2-panel calm bake-off + Kling action panels + reroll headroom. Floor math: 4×$0.30 stills + 2×$1.13 Kling + 2×$0.72–0.90 calm ≈ **$4.46–4.86** animation alone before rerolls — workable if zero rerolls, but **no line item for page-plan LLM** and action-tier count unspecified (if 3 of 4 are action, Rung 1 exceeds $10 easily).

**19. CP-G8 freeze lint edge cases unaddressed.**

§5 item 3 (line ~176): consecutive-frame diff >0.8s threshold — no handling for: (a) boomerang turnaround zones with near-zero motion; (b) dimmed panels where brightness pulsing from spotlight could mask true stasis or cause false motion; (c) exempt "line-boil/caption cells" without defining how cell types are declared in `page_plan.json`.

**20. NBP chained-anchor rendering path not tied to existing provider.**

§3 (line ~118): *"one `nano_banana_pro` call per panel... chained anchors"* — `NBPProvider` in `visual_render.py` supports `extra_ref_paths`, but the plan proposes new ad-hoc per-panel renders without specifying whether it reuses `render_scene` + audit sidecars or new POC scripts. Idempotence rule (§12 item 4: *"PNG + passed-audit sidecar = skip"*) assumes an audit loop that isn't specified for panels.

---

### Reuse: duplication vs. existing tools

**21. Duplicates orchestration instead of extending `run_piece.py` / `cli_livingpage.py`.**

Livingpage already implements: narration → voice → spec → stills gate → animate → build → score → sfx → register (`cli_livingpage.py`). The comic plan reinvents a parallel runner (`comic_page_runner.py`) rather than adding a `page_plan.json` mode to an existing stage detector — guaranteed drift on landing hold, watermark, spend ledger, and registration.

**22. Duplicates panel animation scripts instead of `pipeline/video_render.py`.**

POCs use raw `hf generate create` subprocesses (`poc_thief_e2e/_animate_*.py`). The plan's tier table doesn't reference **`HFVideoProvider` / `HybridVideoProvider`** (`pipeline/video_render.py`) which already handles model-aware duration, NSFW fallback, and ledger hooks — another maintenance fork.

---

### Cost / spend justification

**23. Short cost parity is marketing, not honest.**

§11 (line ~273): *"The short is comparable"* at $22–30 vs $23 current — only true if Opus planning, audits, and alignment are $0 (they aren't) and reroll rate stays at 1-in-3. Long-form **$140–180 cold** (line ~270) is honestly scary; the **≥40% warm reuse** discount (line ~315, §13 item 6) is acknowledged unproven — yet Rung 3 is only **one 16:9 page** (~$8), insufficient to validate reuse economics before committing to a 33-page long.

**24. Validation ladder doesn't gate the expensive failure mode.**

Rung 1 is one page; Rung 2 immediately spends **$15–25 on the remaining 4 pages** before any cross-page anchor drift, colour session drift (§13 item 4), or inter-page layout readability is validated at full-short length. A 5-page short could fail on page 4's anchor break — after 3 pages of spend.

---

### What the plan does well (for balance, not praise)

- Explicit validation ladder with user OK before spend (§12) — right instinct.
- Honest open items (§13), especially dwell-band hypothesis and Seedance gap.
- Correct rejection of post-composite text (§7, POC evidence).
- Freeze lint as a deterministic gate (CP-G8) targets a real regression class.
- Reuse-first intent aligns with project discipline — execution path is wrong, not the goal.

---

VERDICT: REVISE
TOP FIXES:
1. Add **CP-0: generate `narration.alignment.json`** (fix the WhisperX mislabel), declare **9:16 vs 16:9 canvas contracts**, and **resolve INV-16 caption policy** (skip/filter/dual-layer) before any build — CP-1 cannot run without alignment, and release gates will block ambiguous caption stacking.
2. **Defer `cli_comic.py`/full runner**; prove Rung 1 with ad-hoc scripts reusing **`pipeline/clip_reuse.py` + coherence/clip_qc + `panel_variety.py`**, and implement narration-timed focus + panel boomerang as **separate, tested units** before monolithing `page_compose.py`.
3. Fix reuse/banking to the **`clip_library` authoritative path** (not `asset_index` alone), add **`visual_tags.json` + panel-variety** to the gate registry, and extend Rung 2 to require **full-short anchor/colour pass** before scaling — Rung 3 alone doesn't prove long-form or reuse economics.
