# Independent review — cursor (OK, 227s)

## Independent adversarial review — CORPUS ROLLOUT PLAN v2

v2 clearly absorbed panel feedback (Phase 0 committed, gate hardened, `father_forgive_them` split out, honest worst-case budget). Several claims still do not match how the repo actually spends or gates.

---

### 1. “Gate is WIRED INTO the runner” is conditional, not fail-closed

**Plan (lines 21–22):** `run_piece --stage animate` refuses paid renders on any living-light piece until the gate passes.

**Code:** Gate runs only when `piece.json` already has a non-empty `animate.living_light` dict:

```343:353:C:\Users\sanjay\PycharmProjects\JesusInTheBible\run_piece.py
    # ROLLOUT GATE (panel fix 2026-07-14): a piece with living_light entries claims the
    # gold-master bar — refuse paid animate until the whole spec meets it (was CLI-only,
    # i.e. a human-discipline single point of failure).
    if (pj["animate"].get("living_light") or {}):
        from pipeline.rollout_gate import check_piece
        fails = check_piece(piece_dir)
        if fails:
            ...
            return 3
```

Wave A pieces today have **zero** `living_light` entries (`it_is_finished`, `pierced`, etc.). Until those are added, `--stage animate` can still spend on `moves` clips with **no** rollout check. The plan’s wording (“any living-light piece”) assumes a state that does not exist until late in the “$0 spec upgrade.”

**Also:** `cli_livingpage.py` (the documented resumable entry point) has no rollout-gate step between `stills-gate` and `animate` (lines 114–127). Operators using the status board never see PASS/FAIL before the paid command.

---

### 2. “$0 spec upgrade” understates Wave A — it is heavy authoring, not a preflight

**Plan (line 67):** `(1) $0 spec upgrade → rollout_gate PASS → (2) pre-flight … → paid renders`

I ran the gate on Wave A targets. All three FAIL hard:

| Piece | FAIL count | Examples |
|---|---|---|
| `it_is_finished` | 6 | 94% full-bleed, 0% fx, no `motion: "smooth"`, no living_light |
| `pierced` | 5 | 65% full-bleed, 0% fx, no living_light |
| `empty_tomb` (Wave D) | 13+ | 100% full-bleed, `risen_christ_wounds` ×5, 8 illegal full-bleed repeats |

The plan frames Wave A as a **“rate-measurement wave”** (~6 Kling clips), but each Wave A piece needs a **full spec rewrite** (grid conversion, fx arc with direction, landing light, 2+ living_light slugs wired into beats, `motion: "smooth"`). That is days of choreography per piece — not accounted for in waves, verification, or wall-clock.

`it_is_finished` still has `"cut_ticks": true`; gold master has `"cut_ticks": false`. **`cut_ticks` is not in `rollout_gate.py`** — a piece can PASS the gate and still diverge from the shipped gold master on a viewer-visible axis.

---

### 3. “HARD STOP-LOSS: 485cr cumulative (ledger-checked)” is procedural, not enforced

**Plan (line 57):** `HARD STOP-LOSS: 485cr cumulative (ledger-checked at every wave gate)`

`pipeline/cost.py` enforces **per-episode USD ceilings** (`$25/short` via `check_budget()`), not a batch cumulative credit cap. There is no `485` constant, no wave-level aggregator, no automatic halt. The stop-loss depends on a human reading the ledger at each gate — same class of failure the plan claims to have eliminated for the rollout gate.

**Tension:** Plan also requires `pipeline.cost summary --episode <id>` vs `$25/short` (line 44). Those episodes can each stay under $25 while the **batch** blows past 485cr, or hit per-episode ceiling mid-wave and block with `SystemExit` unless someone uses `override=True` — which the plan never mentions.

---

### 4. Budget math is honest about overrun but silent on what gets cut

**Plan (lines 54–57):** Worst case ~525cr **exceeding** the 485 envelope; re-quote gate before Wave B.

Good honesty. Missing: if Wave A measures ≥2.3× (pilot-observed) and cumulative spend approaches 485cr, **which work is deferred** — Wave D stills? living_light count 2→1? pieces dropped? The stop-loss says “stop and ask” but not what the default scope reduction is, so execution stalls at the first unlucky wound-CU piece.

**Wave A sample size:** ~6 clips (2/piece × 3) is too small to re-forecast 18+ remaining clips. One Christ-CU/wound slug at 5+ rolls (pilot: `risen_christ_seeking` ×3) can dominate the measured rate.

---

### 5. Operational steps named but not wired to existing tools

| Plan step | Gap |
|---|---|
| **“BEFORE/AFTER compare page built per piece”** (line 31, 46) | No command, script, or reuse of `women_first_witnesses`’s `visual/_fx_pilot/compare.html` / `promote_living_light.py` pattern. Hand-built per piece at scale. |
| **“Filmstrip QC every new clip”** (line 30) | `pipeline/clip_anim_qc.py` exists (filmstrip + Vision sidecar) but plan mandates manual eye only — no PASS sidecar, no parking rejects in a standard location. |
| **“panel_fit fit-gate + hand-tuned anchors”** (line 101) | After grid conversion (94%→≤60% full-bleed on `it_is_finished`), no build/fit-gate step in the per-piece flow; only a risk bullet. |
| **Wave D: “bible-check fact cards + vision audit + stills-gate + asset_index”** (line 40) | `empty_tomb` has cluster `_bible_check/fact_sheet.md`, not `bib_validate` / `scene_facts.json`. Plan does not say which path is authoritative for **new** stills vs grandfathered plates. |

**Reuse (good):** Wave D’s `reuse_check FIRST` matches `run_piece.reuse_check()` (lines 103–124), which already runs on the stills stage. BytePlus rebuttal (lines 64–65) is correct — `run_piece.py:34` + `SEEDREAM_USD_PER_IMG` are real.

**Duplication risk:** `promote_living_light.py` + `fx_pilot_kling_living_light.py` pilot path vs production `run_piece.py --stage animate` — plan never states whether Wave A **pilots then promotes** (gold-master pattern) or authors `living_light` entries cold. That choice directly affects re-roll rate and prompt-hash binding.

---

### 6. Verification gaps on shipped-piece regression

**Plan (lines 76, 100):** backup + before/after + wave-gate user review for 10 already-approved Cross finals.

No `independent_review.py` step on rebuilt finals despite project standing rule for significant spend-bearing batches. Publish metadata can stay GREEN while `motion: smooth`, fx arc, grids, and living_light clips change the viewer-facing MP4 — the human checklist (lines 24–31) has no recording format (signed checklist artifact, gate JSON, etc.).

**SFX double-audio** (checklist #3): correctly flagged as un-gateable, but no step to diff spec beat `sfx` vs `sfx_pilots/build_*_sfx.py` layer maps before rebuild.

---

### 7. Answered objections — one still thin

**“tests 305 vs STATE 278”** (lines 66–67): asserted fixed, not reproducible from the plan. Phase 0 **is** in git (`bbe943f` tracks `rollout_gate.py`, `test_rollout_gate.py`, `ROLLOUT_PLAN.md`) — that specific panel fix holds.

---

### Summary

v2 is materially better than v1: gate rules match the gold master much more closely, budget honesty improved, `father_forgive_them` correctly scoped out, BytePlus path is real. Remaining problems are **execution wiring** (gate bypass until `living_light` exists, `cli_livingpage` blind spot), **under-scoped authoring** (Wave A is not mainly a 6-clip rate probe), and **manual-only** stop-loss / QC / before-after steps that reintroduce single points of failure the plan claims to have removed.

VERDICT: REVISE
TOP FIXES:
1. Make rollout gate unconditional for all 12 rollout pieces (or any piece with `livingpage_short.spec.json`), wire it into `cli_livingpage.py` before the animate step, and block paid animate on any slug when gate FAILs — not only when `living_light` is already populated.
2. Split Wave A into explicit phases: (a) spec authoring + gate PASS per piece with logged FAIL reasons, (b) then living-light render + filmstrip QC with measured re-roll rate; add `cut_ticks` (and any other gold-master deltas) to the gate or a named checklist artifact.
3. Implement the 485cr cumulative stop-loss in `pipeline/cost.py` (or a wave preflight script), document `check_budget(override=True)` handling for near-ceiling episodes, and define default scope cuts when worst-case 525cr > 485cr before Wave B spend.
