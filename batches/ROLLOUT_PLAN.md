# CORPUS ROLLOUT PLAN v3 — gold-master format × 12 living-page shorts (2026-07-14)

**Status:** v3 after panel round 2 (quorum 4/5: claude PASS, grok REVISE, cursor REVISE,
gemini FAIL — every finding below verified against the code, fixed or answered).
**User approval:** GO at 485cr HARD envelope (pilot spend COUNTS INSIDE it — zero point
defined below). Wave A starts only on a clean panel verdict for this revision.
Out of scope: EW01–09, QJA, and `father_forgive_them` (Wave E, separately quoted).

## Machine bar (all fail-closed, tested — 21 gate tests green)

- `pipeline/rollout_gate.py`: ≤60% full-bleed · ≥3 templates · still ≤2 uses · full-bleed
  repeats only as ≤2 adjacent two-shots · fx ≥50% of beats · **temp grade REQUIRED**
  (rays-only fx fails; cool pole ≥7000K; landing = warmest ≤5500K) · `motion:"smooth"` ·
  `cut_ticks:false` · ≥2 living_light clips, each actually PLAYED (not dyncam'd) · landing
  lit · no double-lighting · no dash/`…`/mojibake captions.
- **Gate fires on EVERY `run_piece --stage animate` where a livingpage spec exists**
  (round-2 fix: the living_light-presence condition left a mid-migration bypass window).
  `JITB_SKIP_ROLLOUT_GATE=1` = loud, discouraged escape for surgical repairs only.
- **Stop-loss is now a script, not prose:** `python -m pipeline.rollout_spend` sums
  attributable ledger rows (rollout episodes since 2026-07-14; Kling clips × 7.5cr observed
  billing; BytePlus stills reported separately in USD) against the 485cr cap, exit 1 on
  breach. Run at EVERY wave gate + before any render batch. Known limits, stated honestly:
  (a) `cost summary` credits can't see animate rows (est_usd only) — that's why this script;
  (b) account-level `reconcile` OVER-attributes when the user spends in parallel (observed)
  — excluded by design; (c) failed-but-billed rolls (502s) write no ledger row — cross-check
  the HF balance by eye at each wave gate. Current reading: 37.5cr attributed, 447.5 headroom.

## Human checklist per piece (recorded as `visual/wave_checklist.json`, reviewed at wave gate)

1. Scale variety (CU+wide+detail+medium) · 2. grids only on multi-figure stills, Christ
singles stay full-bleed · 3. audio-diff: grep the piece's `_sfx.py` bed builder for every
spec-beat `sfx` name — no doubled accents (answer to "un-gateable": it IS a $0 diff, done
as a named step; unifying the two audio systems = post-rollout refactor) · 4. hook-open /
Christ-close bookend · 5. filmstrip per new clip via `pipeline/clip_anim_qc.py`, rejects
parked in `visual/clips/_rejected/` · 6. BEFORE/AFTER page + backup via the shared tooling
(Wave A deliverable below).

## Waves

| Wave | Pieces | Gate |
|---|---|---|
| A(a) | it_is_finished, pierced, crucifixion_foretold — SPEC AUTHORING: baseline gate FAILs logged per piece → full spec rewrite (grid conversion + anchors + fit-gate, fx arc, smooth, living_light entries) → gate PASS. **Deliverable: shared tooling** (generalized `pipeline/living_light_promote.py` from the gold-master script + before/after page builder + backup helper). $0. | — |
| A(b) | Wave A renders: 2 living-light clips/piece (6 total), **first roll = the wound/CU proof** (`it_is_finished`'s bowed-head/nail still — names finalized at authoring, logged in wave_checklist) → filmstrip QC → measured re-roll rate | HUMAN + stop-loss |
| B | forsaken_cry, i_thirst, into_thy_hands, today_paradise | **RE-QUOTE FIRST** (below) |
| C | watch_one_hour, woman_behold, thirty_pieces | HUMAN + stop-loss |
| D | empty_tomb, sign_of_jonah — ordering fixed per panel: fact cards FIRST → author still jobs → `run_piece.reuse_check` → render only the gaps → stills-gate → asset_index registration → clips | HUMAN + stop-loss |
| E | father_forgive_them — greenfield mocomic→livingpage migration; scoped + quoted separately after Wave A | — |

Per piece: backup final (`.bak_prelivinglight`) → spec upgrade → gate PASS → `rollout_spend`
+ `cost summary --episode` pre-flight ($25/short ceiling; a near-ceiling episode = ASK THE
USER, never silent `override=True`) → renders → QC → rebuild → before/after page → register.
**The wave-gate user review of before/after pages IS the re-approval of shipped finals**
(answer to "run independent_review on every rebuild": the standing panel rule covers locked
narrations + significant plans — this plan — not every deterministic rebuild; the narrations
are unchanged).

## Budget v3 (derived, single currency per line)

- Living-light: 12 pieces × 2 clips = 24 × 7.5cr = **180cr base**
- Wave D de-dup (derived, was hand-waved): empty_tomb ~6 replacement stills → 6 new clips
  (45cr) + sign_of_jonah ~3 → 3 clips (22.5cr) = **67.5cr base**; stills themselves ≈
  **$0.45 BytePlus (USD, separate)**
- Base total 247.5cr. At pilot-observed 2.3×/keeper worst case ≈ **569cr — over the 485
  envelope**; at the hoped ~1.5× (locks now baked in) ≈ **371cr — inside it**
- **Forecast rule (panel fix): B–D are forecast at max(Wave A measured rate, pilot 2.3×)
  unless Wave A shows ≤1.5× across all 6 rolls.** Re-quote the user before Wave B either way.
- **Default scope cuts if the forecast breaches 485** (user picks at re-quote): (1) drop to
  1 living-light clip (landing only) on Waves B–C, saves ~52–120cr; (2) defer Wave D de-dup
  to its own quote, saves ~68–155cr; (3) drop pieces. No silent spending through the cap.
- Zero point: pilot + promotion spend counts INSIDE 485. Attributed so far: 37.5cr
  (ledger) — billed possibly up to ~52.5cr incl. one billed 502; balance eyeball at gates.

## Answered panel objections (round 2)

- **gemini "BytePlus unsupported" (round 1):** wrong — `run_piece.py:34` ARK endpoint; all
  cluster stills render there. Confirmed by grok + claude round 2.
- **gemini "reuse_check before fact cards impossible":** correct — Wave D ordering fixed
  above (fact cards → jobs → reuse_check → render gaps).
- **grok "stop-loss is a false control":** correct — replaced with `pipeline/rollout_spend.py`
  (mechanics + limits above).
- **cursor "Wave A is heavy authoring, not a preflight":** correct — Wave A split into A(a)
  authoring/$0 and A(b) render/rate-measurement, with tooling as an explicit deliverable.
- **claude "gate window / zero point / derive Wave D":** all fixed above.
