# Independent review — cursor (OK, 112s)

## Findings

### 1. Diagnosis and fix target different lanes (feasibility / false assumption)

The plan correctly retracts “whole pipeline decay” and pins pain on **living-sketchbook** (Storm/Bronze Serpent) plus **agent-bridge** debris. But Step 2A instruments **core pipeline milestones only**:

> “`{episode, stage, ts}` … at existing milestone write-points … narration locked, audio done, scene plan locked, images done, clips done, final cut assembled”

Those hooks live in `cli.py` / `pipeline/runner.py` / `visual_runner.py` / `assembly_runner.py`. The cited pain does **not** go through that path. Living-sketchbook is adhoc under `poc_living_sketchbook/` (`_s1_anchor.py`, `_s2_stills.py`, `_s3_animate.py`, `_s4_assemble.py`), explicitly **DRAFT / not panel-locked** per `.claude/skills/living-sketchbook/SKILL.md`. Instrumenting the stable core measures the lane the plan already says is unchanged (“byte-identical since May”), not the lane that took 38h / 14h24m.

### 2. Step 2B misreads Bronze Serpent evidence (hidden risk / wrong root cause)

The plan claims:

> “Bronze Serpent's failures suggest a gap between the rule and what actually got rendered; audit that the routing is actually applied before first render”

The codebase contradicts that. `poc_living_sketchbook/bronze_serpent/_s3_animate.py` already hard-codes provider per spread in `JOBS` tuples with explicit Kling/Seedance tier comments (e.g. s03_complaint → Kling, s02_grief → Seedance). Failures happened **with routing applied**:

- **s06_forge**: 3 strikes across **2× Kling + 1× Seedance** (motion invention, not missing routing).
- **s10_golgotha**: Seedance failure led to `_s3b_reroll_s10.py` — reroll script, not a routing omission.

A manual “pre-flight checklist” re-checking rules already in comments will not stop model motion invention or NSFW false positives. The skill itself already requires eye-verify-before-animate (§8a in `_s3_animate.py` header) — that discipline was the actual gap, not absent routing logic.

### 3. Step 2C overclaims “reliability” — detection only (single point of failure)

`watcher_service.py` line 13–14 is explicit:

> “v1 scope is detect + surface, not auto-answer”

The bridge still **blocks up to 3600s** per `pipeline/agent_bridge.py`. The watcher writes `data/.watcher_status.json` for the `cost_status.py` statusline chip. Step 2C’s success metric (“time-to-first-notice under 30s/5min thresholds”) only helps if someone is **staring at the statusline** during a run. It does not:

- Auto-start on boot (`start_watcher.bat` is manual; no Task Scheduler step in the plan)
- Alert when the watcher itself dies (`cost_status.py` only marks watcher stale after 60s of no updates)
- Reduce wall-clock stall when requests go unserviced for days (the 6–16 day debris likely correlates with **no active session servicing the bridge**, not absence of a watcher)

Calling this a “bridge reliability POC” is scope inflation; it’s a **visibility POC**.

### 4. Step 2A duplicates existing instrumentation (reuse failure)

The plan proposes a new `pipeline/stage_log.py` → `data/stage_timings.jsonl`, but:

- **`pipeline/cost.py`** already appends `{ts, episode, stage, ...}` to `data/spend_ledger.jsonl` on every paid HF op. Living-sketchbook scripts already call `cost.record_hf` (e.g. `_s2_stills.py`, `_animate_piece1_v2.py` via `_s3_animate.py`).
- **`cli_livingpage.detect()`** already derives stage completion from artifact presence/mtimes for the livingpage lane; **`production_board.py`** consumes that.

A parallel jsonl without schema for **human-wait time**, **bridge block time**, or **$0 ffmpeg stages** will still leave the biggest wall-clock gaps unmeasured. The plan also says it follows `cost_status.py`’s try/except ledger pattern, but the actual append path is `pipeline/cost.py` `record()` — **no try/except on write** (lines 88–89). Copying the wrong pattern risks either silent drops or uncaught IO failures unless fixed.

### 5. Step 0 verification is not reproducible (verification gap)

Step 0 claims DONE with:

> “Archived the 3 abandoned bridge requests into `.agent_bridge/_stale_cleared_20260801/`”

But `.gitignore` line 25 ignores `.agent_bridge/`. Cleanup, stale count, and “watcher confirmed running” are **not auditable from the repo** by a reviewer or future you. Step 0 verification (“`git status` shows the 3 stale requests moved”) cannot work as written — those paths are gitignored.

### 6. “60 skills, zero wired” is overstated (false precision)

Confirmed section:

> “zero of the 60 skills are wired into the core pipeline code … Real cost = cognitive/tracking load, not extra runtime”

Skills markdown isn’t imported by `cli*.py`, but **deterministic gates are wired**: `animated_gate.py`, `narration_gate.py`, `keeper_lint.py`, `stills_gate.py`, etc. Those add real runtime friction (e.g. `animated_gate.py` notes a blocked `--clips` build pays full render before exit). Treating “skills ≠ wired” as “no runtime cost” understates gate enforcement on livingpage/living-sketchbook paths.

### 7. Baselines and success criteria are weak (verification / edge cases)

- **Apples-to-oranges baselines**: Storm (38h, 6 rebuilds, Round 6 keeper devices) vs Bronze Serpent (14h24m) vs “earlier builds' clean 1.5-2h passes” — no control for episode complexity, cast size, or keeper-device count. One “better” next episode proves little.
- **“Reroll/reject file count”** is fragile: `_rejected/`, `v3_seedance_reject`, separate `_s3b_reroll_*.py` scripts, manual patches — no canonical counter exists.
- **Step 3 lock-in after 1–2 episodes**: “write the checklist into `CLAUDE.md`'s Locked decisions” is statistically thin for a format with 20× wall-clock variance and known model nondeterminism.
- **Guardrail excluding LLM_PROVIDER switch** leaves the primary stall mechanism untouched while claiming to address “slow/error-prone” creation — flagged as “future POC” but it’s the actual blocking call path for all engine LLM/Vision work.

### 8. Missing steps the plan never names

- Instrument **`poc_living_sketchbook/` shared drivers** (`poc_comic_page/_animate_piece1_v2.py` already logs per-clip duration to stdout and ledger) — that’s where animate time lives.
- Log **bridge block intervals** (request mtime → response mtime) — the watcher sees age but doesn’t record serviced latency distributions.
- **Human gate idle time** (GATE 2 image review for the 11 shorts is explicitly nudged but excluded from measurement — yet that’s real throughput drag if “content creation” means end-to-end).
- **Pre-render routing linter** — `animated_gate.py` itself rejects a pre-render classifier because it would duplicate `source()` logic; Step 2B’s checklist has the same fork-drift risk if written as a second manual ruleset instead of one enforced function on the `JOBS` list.

### 9. Cost justification is thin for Step 2B

Step 2B says “no new spend beyond that episode's normal cost,” but the checklist doesn’t reduce spend unless it **prevents paid rerolls**. Bronze Serpent shows rerolls happened **after** routing was correct — so the POC may burn the same credits with extra pre-flight labor. The plan’s cost gate (“explicit quote + go-ahead”) is fine; the **expected savings mechanism** is unspecified.

---

**Summary:** Retractions and guardrails are honest and good. The POC framing is right. But Step 2A measures the wrong pipeline, Step 2B targets a hypothesis the repo disproves, Step 2C rebrands detection as reliability, and verification relies on gitignored artifacts and n=1–2 comparisons. Proceed only after retargeting instrumentation and reframing 2B around proven gaps (test-gate discipline, eye-verify-before-animate, NSFW fallback in `_animate_piece1_v2.run_job`, bridge servicing SOP) rather than re-auditing existing Kling/Seedance tuples.

VERDICT: REVISE
TOP FIXES:
1. Retarget Step 2A to living-sketchbook adhoc milestones (shared `_animate_piece1_v2.py` / `_s2_stills.py` / assemble scripts) and log bridge block time — core `cli.py` hooks won't measure Storm/Bronze Serpent pain.
2. Rewrite Step 2B around demonstrated failure modes (motion invention, missing SKILL §8a eye-verify, no NSFW auto-fallback in `run_job`) — not “routing wasn't applied”; Bronze Serpent already had correct Kling/Seedance in `JOBS`.
3. Downscope Step 2C to “detection + alerting POC” with watcher auto-start persistence and an explicit alert path beyond the statusline chip, or admit stall time is unchanged until bridge requests are serviced.
