# ASSET LIBRARY + SPEND SYSTEM — design (v1, red-team-revised 2026-06-06)

One system: **spend once, reuse well, verify everything, get cheaper over time.**
Four loops, one ledger: **PLAN → SPEND → REUSE → VERIFY.**

Red-team verdict: BUILD WITH CHANGES. This v1 folds in the fixes (the original credit-balance-delta
costing was wrong; most "banks" already exist; the real verify gap is one call site).

Related: `PRODUCTION_PLAN.md` (master) · `BATCH_PLAN.md` · `TODO.md`. Memories: `image-library`,
`hero-stills-library`, `sound-library`, `topical-fit-gate`, `feedback-ask-before-spending`,
`feedback-veed-io-spend-control`, `recursive-learning-system`.

## What ALREADY exists (don't reinvent — red-team B3/B4/B5/B6)
- `image_library/` — 16:9 bank. `ImageEntry` already has subject, tags, jesus_variant, reuse_scope,
  source_episode, used_in, **aspect (=format)**. Missing only: `verified`, `consistency_ref`, `center_safe`.
- `pipeline/hero_library.py` + `cli_library.py` — the 9:16 hero bank AND a working cross-episode
  **select→gaps→animate** reuse audit with the **topical-fit gate** already built. (Loop 1 = generalize this.)
- `sound_library/` — SFX/ambience bank.
- **Canonical Jesus-face ref set already exists + is wired in:** `config.NBP_REFS_DIR` →
  `nano_banana_pro_batch_output/jesus_harmony_v1`; NBP attaches the per-variant ref on every Christ
  render (`visual_render.py`). Consistency is enforced AT GENERATION — no new ref set to build.
- `verify_image` (Claude Vision audit) already gates the SHORTS render path (`render_scene`).

## Providers (locked)
- **Stills:** hybrid — NBP (~$0.50, ref-attached Christ = consistency) for Jesus/face scenes; HF
  `nano_banana_2` (~$0.30, 2 credits) for thread-neutral plates. (User to confirm hybrid split.)
- **Long-form animation:** veo3_1_lite (HF). **Shorts animation:** Kling 3.0 (8-beat viral cut-plan).

---

## LOOP 1 — PLAN (reuse audit before spend)
Generalize the EXISTING `cli_library.py select` (today 9:16) to also cover 16:9:
1. Collect every scene needed across queued episodes (from each `scene_plan.json`).
2. Diff against the banks (topical-fit gate already there) → **render-once list** + **reuse list**.
3. **`center_safe` flag** (NOT a new pool — red-team B3): a 16:9 entry whose subject sits in the
   9:16-safe centre column gets `center_safe=true`. Loop 1 can pull these as 9:16 short **inserts**
   via centre-crop.
   - HONEST yield ~**10-15%** (red-team B3, second-highest risk): the formats fight — veo is a gentle
     frozen-tableau drift, Kling is punchy; a centre-crop drops ~44% width and the subject can drift
     off-centre mid-push-in. So: **calm B-roll inserts only, never the short's hero.** Don't bank these
     savings in a budget up front.

## LOOP 2 — SPEND (logged + capped) — *build this FIRST*
Costing done RIGHT (red-team B1 — the `hf` CLI hands us the exact primitives; drop balance-delta):
- **Pre-flight (exact, not guessy):** `hf generate cost <model> [--prompt/--image] --json` → exact
  `credits` per planned asset (nano_banana_2 = 2 cr; veo ~8 cr; queryable). Sum over the scene plan +
  ElevenLabs char×rate → batch estimate. **Gate on the per-episode ceiling** ($25/short, $40/long);
  block on breach without an explicit `--override` (mirror the veed_io red-banner pattern). Cache
  video estimates per (model,duration) to avoid re-uploading the image each time.
- **Reconcile (authoritative, concurrency-proof):** after a batch, read `hf account transactions
  --json` and match `spend`/`refund` rows by `display_name` + timestamp window. **Log CREDITS, not USD**
  (Ultimate plan = no point-of-spend USD price); carry a `credits_to_usd` config constant for display.
- **Third chokepoint (red-team B2):** the ledger must NOT go blind when `LLM_PROVIDER=api`. Wrap the
  text/Vision client: under `api` log `input/output tokens × rate`; under `agent` log `$0 (agent)`.
  **Every row carries a `mode` field** so off-API LLM cost is explicit, not forgotten.
- **`data/spend_ledger.jsonl`** row: `{ts, episode, kind, stage, provider, model, units, est_credits,
  actual_credits, est_usd, mode, est_only, note}`. Track est-vs-actual drift as its own KPI (catches HF
  price changes). ElevenLabs rows = `est_only:true` (no transactions API).
- **Rollup** → a `$ / credits Spent` column in `PRODUCTION_TRACKER` (real actuals replace the estimate).

## LOOP 3 — REUSE (the existing banks + 3 new fields)
- Add to the entry schema (red-team B4): `verified: bool`, `consistency_ref: str`, `center_safe: bool`.
  No new bank. (Non-blocking: unify the two diverging manifest shapes — `image_library/index.json` vs
  `_hero_library/library.json` — into one entry dataclass first.)
- Topical-fit gate (locked): only thread-NEUTRAL plates cross episodes; story-specific stay home.
- Reuse savings are **booked only after they appear in the ledger** — never assumed up front.

## LOOP 4 — VERIFY (close the ONE real gap)
- **The real gap (red-team B5):** `longform/_render_images_16x9.py` banks NBP output **unconditionally**
  (calls `bank()` straight after `generate`, no `verify_image`). The shorts path is already gated.
  **Fix = 3 lines:** run `verify_image` before `bank()`; skip + flag on fail; stamp `ImageEntry.verified`.
- Audit checks (already in `verify_image`): subject/vignettes match, anatomy (hands), banned tokens,
  full-res (never a contact sheet — the Isaiah lesson).
- **DEFER the drift audit (red-team B6):** consistency is already enforced by the ref attachment at
  generation; a Vision sweep over the bank is premature until the Christ bank exceeds ~30 images.

---

## Backup (red-team B8 — the libraries are the accumulated value)
- No rclone/gcloud; the Drive MCP is interactive. BUT **Google Drive for Desktop is mounted** at
  `C:\Users\sanjay\My Drive` (confirm exact path with user). So `_backup.py` = a ~30-line incremental
  `shutil`/`robocopy` copy (mtime/size compare) of the DURABLE set into a backup folder under that
  mount; Drive-desktop syncs it. Durable set: the 3 libraries, finished films + mp3s, narrations,
  `data/learning/`, `spend_ledger.jsonl`, the trackers, refs. Do a restore-drill once. Not a framework.

## Continuous improvement (defer until there's data)
- Extend `recursive-learning-system` from text to visual/assembly — but only after ~10 episodes of
  ledger + defect data exist (red-team: nothing to calibrate against yet). The SPEND ledger gives the
  cost-per-episode KPI; the learning loop gives the defect-rate KPI; both should trend down.

## BUILD ORDER (red-team-approved)
1. **`pipeline/cost.py` + `spend_ledger.jsonl`** — pre-flight (`hf generate cost`) + reconcile
   (`hf account transactions`) + the LLM `mode` chokepoint + the per-episode ceiling gate. Credits not
   USD. The whole headline value; concurrency-safe; touches only the 2 HF wrappers + the text client.
2. **Close the verify gap** — 3 lines in `longform/_render_images_16x9.py` (verify before bank).
3. `center_safe` flag + generalize `cli_library.py select` to 16:9 (the reuse audit).
4. `_backup.py` to the My Drive mount (quick win, on path-confirm).
- **Defer:** dual-center as a "pool" (it's a flag), the drift audit (premature), any new bank (exist),
  the learning extension (need data first). Each piece stays a <100-line script, not a framework.

## Risks that remain
- R1 `generate cost` for video auto-uploads the image (small per-estimate cost) → cache per (model,duration).
- R2 dual-center yield is ~10-15% not 30-40% — don't budget the savings.
- R3 ElevenLabs cost stays an estimate (no transactions API) — flag those rows `est_only`.
- R4 budget ceiling must have a clean `--override` + audit trail (don't block a legit big batch silently).
