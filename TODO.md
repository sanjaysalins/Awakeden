# TODO — running backlog of work + improvements

Master checklist so good ideas don't get lost. Grouped by theme. `[ ]` open · `[x]` done · `[~]` in progress.
Keep this current; it complements `STATE.md` (status) and `RESUME.md` (what to do first next session).

## 🎬 Production — next actions (PROOF-FIRST order, per the panel)
- [ ] **Publish Isaiah 53** — it's captioned/ready. Build upload kit (title/desc/hashtags/thumbnail), post to YT (+TT/FB/IG), link the short cuts. PROVE the publish loop once. **← Priority #1**
- [ ] **Finish Psalm 22 long** end-to-end: author `scene_plan.json` → red-team → panel → stills → clips → assemble → caption → publish (the 2nd template; validates the episode-generic drivers).
- [ ] **Audit the 9 existing cut POCs** (keep / re-cut / retire) → publish the keepers with kits.
- [ ] **Passion BATCH** (words-from-cross + types-shadows flagships + shorts) — only after the loop + reuse-audit tool exist.
- [ ] Roll out remaining series by brand (SLK → Awakeden → Either), measured against analytics.

## 💰 Spend tracking + cost control — BUILD FIRST (ASSET_LIBRARY_PLAN.md Loop 2, red-team-approved)
- [ ] **`pipeline/cost.py` + `data/spend_ledger.jsonl`** — the headline value. NOT credit-balance-delta (red-team: wrong/fragile). Use:
  - pre-flight: `hf generate cost <model> --json` → EXACT credits before spend (nano_banana_2=2cr, veo~8cr) + ElevenLabs char×rate.
  - reconcile: `hf account transactions --json` → authoritative spend/refund rows, match by name+timestamp. **Log CREDITS not USD** (Ultimate plan).
  - **3rd chokepoint:** LLM cost when `LLM_PROVIDER=api` (token×rate); `$0 (agent)` otherwise. Every row has a `mode` field (don't go blind on the flag).
- [ ] Per-episode budget ceiling ($25/short, $40/long) — pre-flight estimate + block-on-breach with clean `--override` (veed_io red-banner pattern).
- [ ] `$ / credits Spent` column in PRODUCTION_TRACKER (actuals replace the estimate); track est-vs-actual drift as a KPI.
- [ ] KPI: cost-per-finished-episode trending DOWN as the bank grows (proves reuse savings — only book savings AFTER they hit the ledger).

## 🗂 Asset library + reuse system  (ASSET_LIBRARY_PLAN.md Loops 1/3/4 — most already exists!)
- [ ] **Close the ONE real verify gap (3 lines):** `longform/_render_images_16x9.py` banks NBP output UNCONDITIONALLY — add `verify_image` before `bank()`. (Shorts path already gated.)
- [ ] Add 3 fields to the existing `ImageEntry`: `verified`, `consistency_ref`, `center_safe`. (NOT a new pool — red-team B3/B4.)
- [ ] **Dual-format reuse via a `center_safe` FLAG** (not a new bank): 16:9 long clips with subject in the 9:16-safe centre → centre-crop → short INSERTS. Honest yield ~**10-15%** (B-roll only, not hero — red-team cut 30-40%→10-15%).
- [ ] Generalize the EXISTING `cli_library.py select` cross-episode reuse audit (today 9:16) to also cover 16:9. (Don't build a new audit tool — it exists w/ topical-fit gate.)
- [ ] Unify the two diverging manifest shapes (`image_library/index.json` vs `_hero_library/library.json`) into one entry dataclass.
- [ ] ~~Jesus-face ref set~~ — ALREADY EXISTS + wired in (`NBP_REFS_DIR`/jesus_harmony_v1). DEFER the drift audit until the Christ bank > ~30 images (premature now).
- [ ] Wire `hero_library` plates into the shorts engine image stage (still queued from RESUME).

## 🧠 Memory + self-learning system
- [ ] Extend the recursive-learning calibration loop (`data/learning/`) from TEXT to VISUAL + ASSEMBLY stages (log every red-team/panel/QA finding).
- [ ] Per-episode RETROSPECTIVE: short structured "what went wrong / learned / bake-in" entry → defect ledger + memory.
- [ ] Defect taxonomy → recurring defects auto-promote to deterministic gates.
- [ ] Prediction-gap KPI: measure the engine learning to predict what the panel will flag (gap should shrink).
- [ ] Keep writing file-memories (user/feedback/project/reference); periodic consolidation/prune of MEMORY.md.

## 💾 Backup system (red-team B8: use the mounted Drive, not MCP/rclone)
- [ ] `_backup.py` — ~30-line incremental `shutil`/`robocopy` (mtime/size) copy of the DURABLE set into `C:\Users\sanjay\My Drive\<backup-root>` (Google Drive for Desktop mount — CONFIRM exact path). Drive-desktop syncs it. No rclone/MCP needed.
- [ ] Durable set: 3 libraries · finished films + mp3s · narrations · `data/learning/` · `spend_ledger.jsonl` · trackers · refs.
- [ ] One restore-drill (a backup you can't restore isn't a backup). Git already covers code+text; this is for the big binaries.

## 🎛 Provider decisions
- [x] Long-form animation = **veo3_1_lite** (HF) · Short animation = **Kling 3.0**.
- [ ] Stills: **HF ~$0.30/img (cheaper) vs NBP ~$0.50/img (consistent via Jesus-face ref).** DECIDE: hybrid (NBP for Christ/face scenes, HF for neutral plates) is likely cheapest path to consistency. **← needs your call**

## 📋 Plan / catalog
- [ ] Greenlight decision on the BACKLOG 'core-gospel' buckets (Resurrection morning, Incarnation, Sermon on Mount, parables, Last Supper, Pentecost…).
- [ ] Resolve cross-series collisions (canonical backing for John 19:30, Jonah, John 21:17, Luke 23:43, Lamb of God).
- [ ] Multi-dimension policy: how many faithful dims per episode (affects cost + counts).
- [ ] Pull the GDrive register to align episode numbers to what's already planned there.
- [ ] Distribution: posting cadence + per-clip upload kit wired to `0 Christianity/PRODUCTION & POSTING TRACKER.md`.

## 🛠 Engine improvements
- [ ] Make `_soundstage_cinematic.py` episode-generic (currently hand-authored cues).
- [ ] Make `_animate_directional.py` / `_redo_stills.py` / `_reanimate_one.py` episode-generic.
- [ ] Auto status-discovery from disk for the tracker (replace the manual `ST` overlay).

## ✅ Commits pending
- [ ] Commit the Psalm 22 episode (script/audio/reviews) + the production tracker + plans + TODO.
- [x] Caption-as-final-step fix · test-gate · long-form episode-generic refactor (committed earlier).
