# Independent review — cursor (OK, 121s)

## Findings (adversarial, codebase-checked)

### 1. Internal contradiction on music storage (Goal vs Decisions)

The plan contradicts itself in the same document:

- **Goal line 6 / line 14:** “reusable music palette (extend `music_library/`)” and “extends `music_library/`, source=`eleven`”
- **Decisions #2 (lines 110–112):** “a SEPARATE `eleven_music/` collection”

Those are not the same design. One path extends the existing `MusicLibrary` API; the other forks ingest/approve/find tooling into a second tree. The plan never resolves which is authoritative.

---

### 2. “Proven pattern” is #03-specific bakeoff scripts, not scalable tooling

**Lines 19–28** present a 5-step loop as if it’s a repeatable pipeline. In the repo it is **not**:

| Plan step | What actually exists |
|---|---|
| `declare-short` | ✅ `pipeline/element_manifest.py` |
| element-gate sweep → `sweep_review.html` | ⚠️ `_bakeoff/03sweep/record_sweep.py` only — hardcoded `VERDICTS` dict, no generic CLI |
| reuse-rebuild from catalogue | ⚠️ `_bakeoff/03sweep/do_reuse_swap.py` only — hardcoded `SWAPS` list |
| `cli_assemble` | ✅ exists, but each run is bridge-serviced LLM work |

There is no `pipeline/element_gate_sweep.py`, no parameterized reuse-swap tool, and no integration with `pipeline/clip_reuse.decide()`. Scaling to 11 shorts as-written means **11 bespoke scripts** unless tooling is built first — that step is missing from the plan.

---

### 3. Step 2 misstates what the #03 sweep actually did (“filmstrips + agent look”)

**Line 24:** “filmstrips + agent look -> sweep_review.html”

`record_sweep.py` does **not**:
- extract filmstrips (HTML references `strip_*.jpg`, but `_bakeoff/03sweep/` has no strip images — broken review page),
- call `clip_element_gate` vision,
- or run automated frame analysis.

It **records pre-decided human/agent verdicts** into sidecars. `clip_element_gate.py` itself says vision is “serviced by the agent (LLM_PROVIDER=agent)” — not a batch command.

**False assumption:** Phase 1 can run 11 sweeps at “$0 agent look” without specifying who performs the look, how filmstrips are generated, or wall-clock cost.

---

### 4. Reuse safety gap: `clip_reuse` ignores element-gate (catalogue sweep is under-scoped)

**Lines 41–42, 45–47** say reuse from “120 clean catalogue clips” with per-candidate eye-gating.

`pipeline/clip_reuse.is_clean_reusable()` only checks:
- file exists,
- not in `flagged_bad.json`,
- **coherence-verified still**.

It does **not** check element-gate. RESUME already documents a coherence-passing catalogue clip with a **faceted gem** (“The Cry Recorded”). The plan treats catalogue element-gate as optional (“before/while”), but #03 proved coherence-clean ≠ element-clean. Doing shorts first while catalogue is dirty **re-imports hidden defects** — exactly the failure mode this plan claims to fix.

125 clips × manual eye-gate is a large hidden labor item nowhere in the cost model.

---

### 5. Deliverable chain skips mandatory SFX stage

**Line 43:** “Deliverable per short: a clean `viral_cut.mp4` (music applied in Phase 3).”

Standing pipeline order (`.claude/skills/sfx/SKILL.md`, INV-18):

```
assemble → viral_cut.mp4 → SFX → viral_cut_sfx.mp4 → music → viral_cut_sfx_music.mp4 → caption
```

`sfx_pilots/add_music.py` **requires** `assembly/viral_cut_sfx.mp4` (line 42–44). Phase 1 stops at `viral_cut.mp4`; Phase 3 jumps to music without stating SFX rebuild per short. RESUME shows #03 final is `viral_cut_sfx_captioned.mp4` — not `viral_cut.mp4`.

---

### 6. Phase 2–3 music claims don’t match existing code

**Line 63:** “`find_for_beat(beat, tags)` then returns the best eleven/suno score by fit **(already built)**.”

**False as stated.** `music_library/music_library.py` has `find_for_beat()` for **Suno beat beds** with `BEAT_ALLOWED` / `mood` / `energy` from `_specs.py`. There is:
- no `eleven_music/` directory,
- no cross-source selector,
- no `source="eleven"` integration.

**Lines 72–73:** Phase 3 says `find_for_beat` → `add_music.py`.

`add_music.py` today:
- **requires `--prompt`** (line 97),
- **generates** via Eleven API unless `music.mp3` already exists,
- has **no `--from-library` / `--score-slug` path**,
- CLI default gain is **−17 dB** (line 98), not the locked **−8 dB** directive (plan line 114–115). Only `music_batch.py` hardcodes −8.

Reusing a library track also needs **duration/arc handling**: Eleven scores are generated to `D + outro` per short (`add_music.py` line 58). Reusing short A’s score on short B (51.83s vs ~60s) misaligns end-hold and musical arc — no trim/align step is specified.

---

### 7. Phase 2 tag schema doesn’t map to `MusicEntry`

**Lines 59–60:** Tag from `music_designs.json`: `lens (Minimalist-Ambient | Cinematic-Redemptive)`, `mood (grief/intimate, redemptive-arc)`, `beat`.

`MusicEntry` expects `mood` ∈ `{sacred, lonely, tender, awe, …}` and `energy` ∈ `{low, build, climax, swell-and-rest}` (`music_library.py` lines 44–45). `music_designs.json` uses `winner_lens` and prose `best_prompt` — **no mapping table** from lens → `mood`/`energy`/`tags` for `find_for_beat`.

Also: Suno `find_for_beat` selects **per Gospel-Five-Beat** beds; Eleven scores in `music_designs.json` are **full 60s arc prompts**. Conflating them under one selector is a category error.

---

### 8. Phase 2 harvest timing is wrong relative to Phase 1

**Lines 57–58:** Ingest “11 generated `assembly/music.mp3` scores.”

RESUME (line 17): **“Music is STALE on #03 — old music final was built on the defective cut.”** Music batch ran at session start on **pre-rebuild** cuts. Harvesting now banks scores tied to wrong clip timing/length. Plan should harvest **after** Phase 1 rebuilds (or re-generate all scores post-rebuild), not treat existing files as canonical.

---

### 9. Cost model understates real spend

**Lines 96–103:** “Phase 1 … **$0** baseline” / “Net: mostly $0.”

Undercounts:
- **Operator time:** 11 × (sweep review + reuse eye-gate + bridge-serviced assembly reviews). `agent_bridge` requests are global and sequential (plan line 38 acknowledges this but not the bottleneck).
- **Metered clip renders:** RESUME documents **NBP gem nail-wound scenes as un-rebuildable** — exclusion, not $0. Scroll/writing scenes across #01–#08 likely force exclusions or fresh Kling ($).
- **Music:** At minimum #03 needs metered regen; cross-short reuse is unproven, so Phase 3 may be mostly metered on first pass, not “mostly $0.”
- **Catalogue sweep:** 125 clips × vision look is not “$0” in any practical sense.

---

### 10. Phase 4 is premature and conflates two music systems

**Lines 82–88:** Wire long-form via `music_library` + `find_for_beat`; future shorts via `add_music`.

The repo already has **two different music models**:
- **Suno `music_library/` + `placer.py`:** beat-aligned beds, `BED_UNDER_DB = -20.0`, CTA swell alignment (`placer.py` lines 31–34),
- **Eleven `add_music.py`:** bespoke full-length scores, −8 dB, 2.5s end-hold (`add_music.py` lines 72–79).

`music_library/README.md` still says the beat-aligned placer is “not built yet” (line 35–36) while `placer.py` claims “BUILT.” Phase 4 wires long-form before shorts prove either path — classic build-before-validate.

---

### 11. Missing verification / edge cases

Not specified anywhere:

- **Acceptance criteria** for step 5 “re-sweep → confirm clean” (0 FAIL in shipped set? all manifests locked? element-gate hard-enable?).
- **`do_not_use` sidecars** (#03 scene 12 pattern) — durable exclusion not in the loop.
- **Hero re-validation (AS-G6)** after clip swaps change gospel-pivot candidates.
- **`edit_plan.json` invalidation** — replan triggers full bridge-serviced review cycle each short.
- **Pilot shorts too thin** (RESUME: ~7–10 clips / ~70s) — sweep+reuse may produce “clean” but unpunchy cuts; plan doesn’t address pace backfill.
- **Calibration gate:** RESUME says blind-label bake-off + `JITB_REQUIRE_ELEMENT_GATE` flip is **still pending** — plan guardrails say “calibrate before HARD enable” but Phase 1 execution isn’t blocked on that.

---

### 12. Over-engineering: duplicate `eleven_music/` tooling before one reuse proof

**Lines 51–55, 110–112:** Mirror full `music_library` stack (index/ingest/approve/find_for_beat/qc) into `eleven_music/`.

Decision #2 chose isolation, but the plan builds **~5 duplicated modules** before demonstrating that **one** Eleven score can be reused on a **second** short with acceptable arc/timing. Smaller proof: extend `MusicLibrary` with `source` filter + add `--score path` to `add_music.py`, validate on 2 shorts, *then* decide on fork.

---

VERDICT: REVISE
TOP FIXES:
1. **Build (or specify) generalized sweep + reuse tooling first** — the #03 pattern is hardcoded bakeoff scripts, not a repeatable pipeline; Phase 1 cannot scale to 11 shorts as written.
2. **Block reuse on a catalogue element-gate sweep done first** — `clip_reuse.is_clean_reusable()` ignores element-gate; optional “before/while” guarantees re-importing gem/scroll defects.
3. **Fix the music path end-to-end before Phase 4** — reconcile Goal vs `eleven_music/` fork, add library-reuse to `add_music.py`, map Eleven arc scores vs Suno beat beds, harvest scores *after* rebuilds, and include the mandatory SFX step in the deliverable chain.
