# Independent review — cursor (OK, 146s)

## Independent adversarial review

### 1. Goal promises ≠ what `rollout_gate.py` actually enforces

The **Goal** section (lines 12–23) lists eight quality bars. Phase 0 (lines 27–30) claims the gate covers the gold-master bar. It does not.

| Goal claim | Enforced in `rollout_gate.py`? |
|---|---|
| `"motion": "smooth"` | Yes |
| ≤60% full-bleed, ≥3 templates | Yes |
| no still >2 uses, ≤2 adjacent FB pairs | Yes |
| cold→warm `fx.temp` arc (7900K→4900K) | **No** — only `fx` present on ≥50% of beats; no `temp` key, no monotonic arc |
| scale variety (CU/wide/detail/medium) | **No** |
| shatter only on multi-figure stills | **No** |
| 2–3 `living_light` clips per piece | **No** — minimum is `>= 1` (lines 75–76) |
| sound accents / no hype drop on sacred beats | **No** |
| double-lighting forbidden | **Named as risk** (lines 69–70) but **not gated** |

A piece can **PASS** the gate while missing most of what the user approved on the gold master (`women_first_witnesses` has **3** `living_light` entries and **83%** fx coverage per the gate’s own comments; the gate would pass a 50%-fx, 1-clip piece).

### 2. “Deterministic blocking gate” is not wired into the pipeline

Phase 0 says the gate “runs at spec-authoring time” and the per-piece flow is:

> rollout_gate PASS → paid renders → rebuild (lines 47–50)

In the codebase, `rollout_gate` is only invokable as a standalone CLI (`pipeline/rollout_gate.py` lines 7–9). It is **not** called from `cli_livingpage.py`, `run_piece.py`, or `pipeline/test_run_piece.py`. `cli_livingpage.py` jumps from `spec` → `manifest` → `stills` → `animate` with no gate step (lines 78–127).

This is a **human-discipline SPOF**: the plan treats the gate as blocking; the runner treats it as optional.

### 3. `father_forgive_them` scope is badly understated

Wave C (line 44) lists `father_forgive_them` with a one-line note: “mocomic→livingpage spec migration first.”

Facts in the repo:
- No `livingpage_short.spec.json` under `father_forgive_them/` (0 files).
- No `piece.json` (unlike the other 13 batch pieces).
- Published final is `father_forgive_them_mocomic_v2_scored.mp4` (mocomic builder), not the living-page builder (`build_livingpage_16x9.py` via `cli_livingpage.py` line 31).

This is not a “$0 spec upgrade” — it is **greenfield living-page authoring** (spec + manifest + stills + gate + animate + build + score + sfx + register), then living-light on top. Budgeting it at “≈ 35cr migration extras” (line 57) looks low for a full format migration, and burying it in Wave C (line 44) mixes a greenfield build with three routine upgrades.

### 4. Budget math conflicts with per-episode ceiling enforcement

The plan’s **485cr ≈ $25** figure (lines 4, 58) is a **batch** subscription view.

Code enforces a **per-episode** ceiling: `CEILING_SHORT_USD = 25` in `pipeline/cost.py` (lines 37–38), checked on **every** Kling call in `_hf_animate_short.hf_animate` (lines 124–134) using `KLING_USD_PER_CLIP = 0.65` and **cumulative** `episode_total_usd()`.

`empty_tomb_john208` already has **53** ledger rows (stills + clips + re-renders). Living-light promotion **changes prompts** → `clip_src_hash` stale → **paid re-rolls count against the same episode cap**, not a fresh batch bucket.

The plan never says: (a) pre-flight `python -m pipeline.cost summary --episode <id>` per piece before Wave A, or (b) how to handle ceiling breaches on already-spent episodes. The 485cr batch approval does **not** override `check_budget()` unless someone uses `override=True` — which the plan does not mention.

### 5. Wave A does not stress the highest-failure living-light targets

Wave A (line 42) is “prove the repeatable transform” on `it_is_finished`, `pierced`, `crucifixion_foretold`.

`it_is_finished` today is almost entirely `tpl: "full"` (16/17 beats in the spec), `cut_ticks: true`, no top-level `"motion": "smooth"` — a large grid/fx/living-light rewrite, not a light touch. It also includes wound/CU stills (`nail_through_hand`, `bowed_head_finished`) where the pilot locks (expression / dry-wound / whole-figure) are most likely to trip the “~1 in 3” QC lottery (lines 64–65).

Wave A should include at least one **Christ CU + wound** living-light proof before batching 30 clips.

### 6. Wave D / `empty_tomb` de-dup is under-scoped

Line 45: `empty_tomb = 9 stills/20 beats, one still ×5`.

The spec shows `risen_christ_wounds` on **five** beats and multiple other slugs at 2×. Fixing that to `MAX_STILL_USES = 2` means **new still variants + anchors + vision audit + stills-gate + new clips** — not just “~15 de-dup stills” (line 56) with a single line in Wave D.

The plan’s doctrine line (lines 76–78) is right for new stills, but there is **no** step for `run_piece.reuse_check()` before paying BytePlus (that helper exists in `run_piece.py` lines 103–124). You may re-pay for plates siblings already have.

### 7. Re-roll margin is optimistic for the stated reject model

Lines 64–65: “~1 in 3 first rolls fails.” Lines 55, 85: “~50% QC-lottery re-roll margin.”

For independent 33% failures, expected rolls ≈ `n / 0.67` → **~50% over nominal** only if every clip succeeds on the **second** try. Hard CU/wound clips that fail twice (pilot history: stern-face, bleeding-palm) blow through 50% fast. The margin also does not budget **re-rolls on non-living-light** clips made stale by spec motion/grid changes.

### 8. “10 already-approved Cross finals” — asked, not answered; regression path is thin

Open question #3 (line 84) is the right question. The mitigation (lines 71–73) is only `.bak_prelivinglight` + “publish stays GREEN” because filenames are unchanged.

That does **not** prevent silent viewer-facing regression: `motion: smooth`, grid crops, fx arc, and new living-light clips change the final MP4 while publish metadata stays green. There is no per-piece human re-approval gate after rebuild, no `independent_review.py` step, and no before/after filmstrip in the workflow (lines 47–51).

### 9. Sound-accent step is incomplete in the per-piece recipe

Goal (line 21): “riser/reveal accents from sound_library.”

Per-piece flow step (1) (line 47) adds “sound accents” to the spec, but step (3) (line 50) only says `score → sfx` without requiring **sfx layer-map updates** in `sfx_pilots/build_cluster1_sfx.py` / `build_empty_tomb_sfx.py` / etc. Beat-level `sfx` in the spec and the scored-bed builders are separate systems; changing beat accents without updating the builder can leave stale or doubled audio.

### 10. Feasibility / verification gaps

- **“305 passed / 1 skip”** (line 25): `STATE.md` still says “278 tests pass.” Unreconciled; don’t treat 305 as verified in this review.
- **“it_is_finished FAILs 6”** (line 30): plausible (classic motion, ~94% full-bleed, no `living_light`, likely no fx arc, `cut_ticks`, etc.) but the plan does not list the six reasons — makes Wave A sizing guesswork.
- **`promote_living_light.py`** exists only on the gold master piece; the plan does not say whether Wave A reuses that pattern or hand-edits `piece.json` — error-prone at scale.
- **Pilot script** `sfx_pilots/fx_pilot_kling_living_light.py` is separate from production `run_piece.py --stage animate`; fine for pilot, but the plan should state production path explicitly to avoid duplicate animate entry points.

### 11. What is solid (not letting everything slide)

- Phase 0 artifacts exist and match the described shape (`rollout_gate.py`, `animate.living_light` in `run_piece.py`, pilot locks, glitter ban, hash binding).
- Wave human gates (line 38) are appropriate for a QC-lottery workflow.
- `SHORTS_SAFE_BOT=0.18` claim is real — `build_livingpage_16x9.py` sets it when `h > w` (portrait 1080×1920), which is how `cli_livingpage.py` invokes the builder (lines 140–141).
- BytePlus path reuses `father_forgive_them/byteplus_seedream.py` via `run_piece._bp()` — good reuse, not duplication.
- Known risks section (lines 63–78) is honest about Kling disobedience and grid-crop pain; the Women piece anchor rounds are a fair warning.

---

VERDICT: REVISE
TOP FIXES:
1. Close the Goal↔gate gap: add deterministic checks for double-lighting, `living_light` count (≥2), `fx.temp` arc, and wire `rollout_gate` into `cli_livingpage.py` / `run_piece.py` so PASS is mandatory before any paid animate.
2. Re-scope `father_forgive_them` as its own migration wave (greenfield living-page, not a line item in Wave C) and pre-flight every episode with `pipeline.cost summary` against the $25/short ceiling before batch spend.
3. Fix Wave A to prove living-light on hardest stills (Christ CU/wound), add per-piece post-rebuild approval + answer open Q3 for the 10 shipped Cross finals; bump QC budget or cap living-light picks until Wave A measured reject rate is known.
