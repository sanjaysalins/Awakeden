# Independent review — cursor (OK, 225s)

Round-2 fixes are real — `rollout_gate.py`, `rollout_spend.py`, and the animate hook in `run_piece.py` match several claims. What’s still wrong is mostly **integration gaps**: tools named in the plan that don’t fit the living-page layout, deliverables that don’t exist yet, and controls that still depend on humans at the moment money moves.

## Findings (specific, adversarial)

### 1. **`clip_anim_qc.py` is the wrong tool for this pipeline** (Human checklist item 5 / Wave A(b))

Plan: *"filmstrip per new clip via `pipeline/clip_anim_qc.py`"*.

Reality: `clip_anim_qc.run()` loads `visual/scene_plan.json` and scans `visual/nbp/[0-9][0-9]_*.mp4` — the v1 scene-plan layout:

```194:205:pipeline/clip_anim_qc.py
def _load_scenes(v1: Path) -> dict[int, dict]:
    sp = json.loads((v1 / "visual" / "scene_plan.json").read_text(encoding="utf-8"))
    ...
def run(v1: Path, provider: str = "nbp", only: list[int] | None = None) -> list[dict]:
    nbp = v1 / "visual" / provider
    ...
    for mp4 in sorted(nbp.glob("[0-9][0-9]_*.mp4")):
```

Living-page batch pieces use `visual/clips/{slug}.mp4` and `livingpage_short.spec.json` (via `cli_livingpage.py` / `run_piece.py`). Running `clip_anim_qc` on a cluster piece will fail or no-op. The gold-master pilot used hand-built filmstrips in `visual/_fx_pilot/compare.html`, not this module.

**Risk:** Wave A(b)’s “measured re-roll rate” has no working automated QC path as written.

---

### 2. **Wave A(a) deliverables are planned, not built — but Wave A(b) spend depends on them**

Plan Wave A(a): *"generalized `pipeline/living_light_promote.py` … before/after page builder + backup helper"*, recorded as `$0` deliverable.

Reality:
- No `pipeline/living_light_promote.py` — only piece-local `batches/.../women_first_witnesses_luke245/promote_living_light.py`, hard-wired to `fx_pilot_kling_living_light.PILOT`.
- No `visual/wave_checklist.json` anywhere in the repo.
- No shared before/after page builder or backup script — only the convention *"`.bak_prelivinglight`"* in prose.

**Risk:** A(a) is a multi-day authoring + tooling sprint disguised as a preflight. Calling it “$0” hides labor and blocks A(b) until three tools exist.

---

### 3. **Stop-loss is improved but still not fail-closed at the spend chokepoint**

Plan: *"Stop-loss is now a script, not prose"* and *"Run at EVERY wave gate + before any render batch"*.

Reality:
- `rollout_spend.py` exists and honestly documents limits (a–c) — good.
- **`run_piece.run_animate()` calls `rollout_gate` but never `rollout_spend`.** The only automated spend gate in `_hf_animate_short.hf_animate` is per-episode USD via `check_budget()` at `$25/short` — a different unit and scope from the 485cr envelope.

**Risk:** You can breach 485cr while every per-episode check still passes, or blow the batch cap if someone skips the manual script (same failure class grok flagged in round 1, only half-fixed).

---

### 4. **Dual budget model is still internally tense**

Plan requires both:
- *"`rollout_spend` + `cost summary --episode` pre-flight ($25/short ceiling)"*

Problems:
- `cost summary` credits column is **0 for animate rows** (`est_credits: null`) — plan admits this; only `rollout_spend` sees clip credits.
- Per-episode USD sums **all historical ops** for that episode; batch cap counts **only clips since 2026-07-14** for rollout episodes. A piece can sit under $25 while the batch is over 485cr, or hit `$25` mid-wave and hard-stop via `SystemExit` while the plan never mentions `override=True` (which `check_budget` supports in `pipeline/cost.py`).

**Risk:** Operators get conflicting stop signals; “ASK THE USER near ceiling” is undefined for already-spent Cross finals with 10+ ledger animate rows.

---

### 5. **Machine bar vs human checklist: most “quality” is still un-gateable**

Plan machine bar: 21 tests in `pipeline/test_rollout_gate.py` — **verified, that claim holds**.

But human checklist items **1, 2, 3, 4** are not enforced by `rollout_gate`:
- *"Scale variety (CU+wide+detail+medium)"* — not checked.
- *"grids only on multi-figure stills, Christ singles stay full-bleed"* — gate only caps overall full-bleed at 60%; it does **not** enforce Christ-single vs multi-figure rules.
- *"hook-open / Christ-close bookend"* — landing light is checked; hook-open is not.
- Audio item 3 says *"grep the piece's `_sfx.py` bed builder"* — **wrong path**. Living-page SFX goes through `sfx_pilots/build_cluster1_sfx.py` (cluster 1) or piece-specific `build_*_sfx.py`, discovered by `cli_livingpage._sfx_builder()`. Spec beats also carry inline `"sfx"` arrays — doubling is plausible and the grep target is misnamed.

**Risk:** Plan claims “fail-closed” rollout; most visual/audio regressions still depend on a JSON checklist nobody has tooling to validate.

---

### 6. **“fit-gate” in Wave A(a) is advisory, not a gate**

Plan A(a): *"grid conversion + anchors + fit-gate"*.

`build_livingpage_16x9.py` (what `cli_livingpage` actually calls for 9:16 shorts) prints fit warnings and **continues**:

```698:699:longform/02_Psalm_22_Song_From_The_Cross/build_livingpage_16x9.py
    if fitwarn:
        print(f"\n[fit-gate] {len(fitwarn)} over-cropped panel(s):\n" + "\n".join(fitwarn))
```

No exit code, no sidecar, not in `rollout_gate`. Converting `it_is_finished` from ~94% `full` templates (current spec: `"cut_ticks": true`, no `"motion": "smooth"`, no `living_light`) to ≤60% grids is the hardest authoring step — and the “gate” is a stdout warning.

---

### 7. **Wave A(b) proof subject is harder than the gold master**

Plan: *"first roll = the wound/CU proof (`it_is_finished`'s bowed-head/nail still)"*.

Gold master pilot (`women_first_witnesses_luke245`) validated living-light on **resurrection/glow** scenes. Crucifixion CU/nail imagery is where the pilot contract explicitly bans bleeding/morph (`LIVING_LIGHT_BASE` in `run_piece.py`). Pilot ledger already shows **2 re-rolls on one slug** (`risen_christ_seeking` ×3 animate rows on 2026-07-14). Plan’s *"~1.5× (locks now baked in)"* base forecast (371cr) is hope, not measurement; *"2.3× worst case ≈ 569cr — over the 485 envelope"* is the honest branch — and Wave A hasn’t measured wound-CU yet.

**Risk:** Budget breach at conservative reroll is likely before Wave B; scope cuts are listed but not pre-committed.

---

### 8. **Wave D ordering fix is correct; Waves A–C omit reuse discipline**

Plan fixed gemini’s ordering: *"fact cards FIRST → author still jobs → `run_piece.reuse_check` → render only the gaps"* for Wave D — matches `reuse_check()` needing finalized prompts (`run_piece.py:103–124`).

But Waves A–C say nothing about `reuse_check` on any still work. If grid conversion or living-light slugs trigger still re-renders, you can re-pay BytePlus for plates siblings already have. `run_stills` auto-runs reuse only when `--render` is used without `--no-reuse` — the plan doesn’t name this for non-D waves.

---

### 9. **Hidden dependency: `father_forgive_them` (Wave E) on Wave A pieces**

Out of scope per plan, but `it_is_finished` still references `../father_forgive_them/visual/_byteplus/face_on_cross_fix2.png` as a still ref. Wave E is “greenfield migration” while Wave A already depends on that asset. If Wave E rework moves paths, Wave A stills break silently.

---

### 10. **Regression control is still thin for shipped Cross finals**

Plan: *"The wave-gate user review of before/after pages IS the re-approval of shipped finals"* and excludes `independent_review` on deterministic rebuilds.

That’s a policy choice, not a control. Rebuild changes motion (`smooth`), grid crops, fx arc, and living-light clips while publish/upload metadata can stay green. Before/after tooling doesn’t exist yet; backup is a filename convention only.

---

### What the plan got right (so this isn’t FAIL)

- `rollout_gate.py` matches the stated machine bar (temp arc, dyncam waste, double-lighting, etc.).
- Round-2 animate hook: gate fires on **any** piece with `livingpage_short.spec.json`, not only when `living_light` is populated (`run_piece.py:348–357`).
- `rollout_spend.py` + test exist; 37.5cr / 447.5 headroom math matches ledger rows since 2026-07-14.
- BytePlus claim (`run_piece.py:34` ARK endpoint) is correct.
- Wave D ordering fix is chronologically sound.
- Budget honesty on 2.3× breach and re-quote before Wave B is better than v2.

---

VERDICT: REVISE
TOP FIXES:
1. Replace or adapt checklist item 5: either extend `clip_anim_qc` (or a thin wrapper) for `visual/clips/{slug}.mp4` + livingpage specs, or explicitly adopt the gold-master `_fx_pilot/compare.html` filmstrip workflow and drop the false `clip_anim_qc` reference.
2. Wire `rollout_spend` into the same chokepoint as `rollout_gate` (`run_piece.run_animate` / `_hf_animate_short`) so 485cr is fail-closed, not “run manually at wave gate”; reconcile the dual `$25/short` vs 485cr pre-flight into one operator-facing decision.
3. Before Wave A(b) spend: deliver the A(a) tooling (promote/backup/before-after/wave_checklist) or descope them; fix the audio checklist to diff `livingpage_short.spec.json` `"sfx"` beats against the correct `sfx_pilots/build_*` layer map; treat fit-gate as a named human step or make over-crop block the build for rollout pieces.
