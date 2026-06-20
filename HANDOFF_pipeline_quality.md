# HANDOFF — pipeline quality work (read me first)

Self-contained resume for a fresh Claude session continuing in this repo (JesusInTheBible / Awakeden).
Written 2026-06-20. The previous session built a hook/quality gate + an upload lint and applied the
scroll-test fixes to the Psalm 22 shorts. **One thing is left: RE-RENDER the 6 fixed shorts.**

---

## WHAT WAS DONE (all committed on `main`)

1. **`pipeline/hook_gate.py`** + `pipeline/test_hook_gate.py` (commit `9891b0b`) — the hook + 60s-budget
   quality gate. Fills the gap: `data/structures.json` DEFINES the Gospel Five-Beat but nothing enforced
   it. Deterministic teeth: short **duration vs the 60s budget** (caught **4 of 8 shorts at 67-73s**),
   hook lands fast, hook not manufactured/fear-based (reuses `doctrine_gate.scan`), landing points to
   Christ, word budget. `--judge` = a free scroll-test via `independent_review` local CLIs.
   Run: `.venv\Scripts\python.exe -m pipeline.hook_gate "<short folder>" [--strict|--judge]`.
   Tests: `.venv\Scripts\python.exe -m pipeline.test_hook_gate` (7/7; pytest NOT installed, tests have a
   `__main__` runner — that's the repo convention).

2. **Wired hook_gate into `lock.py`** (commit `69e5549`) — `run_lock()` returns a `hook` key (like
   `doctrine`); `cli_lock.py` prints `[HOOK ADVISORY]/[HOOK WARN]`. **ADVISORY — never blocks the lock**
   (some locked shorts overrun 60s). Existing lock tests still 13/13. Enforce hard only via
   `-m pipeline.hook_gate <folder> --strict` when authoring a NEW short.

3. **`upload_gates.py` UK-G7 lint** + `pipeline/test_upload_lint.py` (commit `1e3453f`) — added to
   `run_all`. Plain-ASCII anti-slop (no em/en-dash, ellipsis glyph, curly quotes), grace-tone landmines
   in the COPY (reuses `doctrine_gate`), and SEO verse-front-load (anchor ref in the first 157 chars).
   Tests 5/5. NOTE: `upload_handoff.render_md` already writes a paste-ready `upload_kit.md`, and
   `upload_engine.generate()` + `independent_review` already exist — UK-G7 was the only real gap.

4. **Applied the scroll-test hook/landing fixes to 6 Psalm 22 shorts** (commit `101d27b`):
   - HOOK front-loaded: `03_The_Forsaken_Cry`, `04_Declared_To_The_Brethren`, `05_He_Hath_Done_This`,
     `06_The_Ends_Of_The_Earth` (open on the concrete image / KJV pivot, dropped the commentary setup).
   - LANDING → Christ + invitation: `07_The_Body_Foretold`, `08_I_Thirst` (dropped the benefit-chain /
     evidence recap; #08 now ends "Come to Him").
   - KJV quotes UNTOUCHED. `cluster_gate` caught 2 accidental templates I introduced ("a thousand years"
     opener, "the One who" CTA) → de-duped. All 6 **re-lock clean** (kjv/doctrine/cluster/parity).
   - Edited BOTH `narration.md` AND `narration-tagged.md` per short (lock checks parity between them).
   - `01_The_Crucifixion_Foretold` + `02_The_Mockers_Words`: judge re-run = **VERDICT: PASS**
     (ship-ready). Left unchanged (optional tightenings would re-trigger the cluster gate). Verdicts in
     `<short>/_hook_review/claude.md`.

---

## ⚠️ THE ONE THING LEFT — RE-RENDER the 6 fixed shorts

I changed only the **narration TEXT**. So `narration.mp3` + the assembled video + the captions for the 6
edited shorts are now **STALE** (they still carry the OLD hook/landing). Nothing reaches a viewer until
each fixed short is re-rendered:

  **re-synth (ElevenLabs $) -> re-assemble -> re-caption**, for each of:
  `03_The_Forsaken_Cry`, `04_Declared_To_The_Brethren`, `05_He_Hath_Done_This`,
  `06_The_Ends_Of_The_Earth`, `07_The_Body_Foretold`, `08_I_Thirst`.

Use this repo's existing pipeline for each short folder (confirm exact flags in `RESUME.md`/`STATE.md`/
`CLAUDE.md` first):
  - audio: `per_turn_synth.py` (multi-voice, duration-locked ~60s; updates `narration.meta.json`)
  - assemble: `cli_assemble.py` (the assembly stage)
  - captions: `.venv\Scripts\python.exe -m veed_io.caption --video "<clip>"`
  - (or the seamless `cli_pipeline.py` per short, with its human gates)

**It costs ElevenLabs credits** — confirm the budget with the user before synthing all 6.

### Also flag
- `01_The_Crucifixion_Foretold` separately runs **73s** (the deterministic gate flagged it) — that's an
  over-budget **whole-short trim**, not a hook swap. Worth a re-cut when convenient.

---

## GOTCHAS / FACTS for the new session
- **Working dir:** all files are in THIS repo. Python = `.venv\Scripts\python.exe`. Gates live in
  `pipeline/<domain>_gate.py`, run by `lock.py` (the chokepoint) + `cli_lock.py`; tests `-m pipeline.test_*`.
- **narration.meta.json** turns have `final_seconds` (+ `final_total_seconds`, `target_seconds`) —
  **NO start_s/end_s**; quote turns show `final_seconds` 0.4 (a quirk — don't trust per-quote-turn timing).
- **Narration em-dashes are FINE** (spoken pacing cues). The anti-slop typography rule (no em-dash/curly/
  ellipsis) applies ONLY to **published upload copy** (UK-G7), not the narration.
- **cluster_gate** blocks templated openers (>=2 content words shared by >=3 shorts) + repeated CTA shapes
  — when editing a short, vary the opener n-gram + the CTA so you don't collide with siblings.
- **Don't duplicate** existing gates: `kjv_strict` (KJV), `doctrine_gate` (9 landmines incl fear-pressure/
  gain-loss), `cluster_gate` (repetition), `independent_review` (multi-CLI red-team), the Upload Kit
  (`upload_engine`/`upload_gates`/`upload_models` + `data/platform_specs.json`), `veed_io` (captions).
- **Uncommitted working-tree changes** are harmless derived state: re-written `.locked` files,
  `data/learning/freshness_registry.json`, and `_hook_review/*.md` judge verdicts. Safe to leave or commit.
- The cross-project memory `jitb_pipeline_port` (in the user's Claude memory) mirrors this; the sister
  project is HF-POC/Furgiven (where the same hook-gate + publish patterns originated).

## NEXT ACTION
Ask the user to confirm the ElevenLabs spend, then re-synth -> re-assemble -> re-caption the 6 shorts
listed above (and consider trimming #01 to ~60s). Then the scroll-test fixes are live.
