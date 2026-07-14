# CORPUS ROLLOUT PLAN v2 — gold-master format × 12 living-page shorts (2026-07-14)

**Status:** v2 after independent panel REVISE (3/3 voices: claude, cursor, gemini —
grok/codex dead, DEGRADED, re-running on this revision). Wave A NOT started.
**User approval:** GO 2026-07-14 at ~485cr envelope. **v2 change: the envelope is now a
HARD stop-loss, and Wave A re-measures the re-roll rate before any further quote.**
EW01–09 + QJA back-catalogue explicitly OUT. `father_forgive_them` moved OUT to its own
separately-quoted migration wave (panel: it is greenfield authoring, not an upgrade).

## Goal

Bring the 12 spec'd living-page shorts up to the user-approved gold master
(`women_first_witnesses_luke245`, incl. living light, shipped 2026-07-14):

**Machine-gated** (`pipeline/rollout_gate.py`, hardened per panel):
- ≤60% full-bleed, ≥3 templates; no still >2 uses; full-bleed repeat only as ≤2 adjacent two-shots
- cold→warm grade arc with DIRECTION: a ≥7000K cool pole and the landing = warmest (≤5500K)
- fx on ≥50% of beats; `"motion": "smooth"`; no dash/ellipsis/mojibake captions (incl. `…`)
- ≥2 `living_light` clips (pinned default 2/piece, 3 by exception), each actually PLAYED by a
  beat (not dyncam'd); landing beat lit; **no double-lighting** (living-light beat + `fx.rays` = FAIL)
- Gate is WIRED INTO the runner: `run_piece --stage animate` refuses paid renders on any
  living-light piece until the gate passes (no longer CLI-only human discipline)

**Human checklist per piece** (un-gateable, panel fix — checked at the piece's eye review):
1. Scale variety: CU + wide + detail + medium all present
2. Shatter/grids only on multi-figure stills; Christ/single heroes stay full-bleed
3. Sound accents tasteful, NO hype drop on sacred beats; verify no doubled audio vs the
   piece's sfx-bed builder (spec beat `sfx` and the `_sfx.py` bed are separate systems)
4. Bookend: motion hook open, close on Christ
5. Filmstrip QC every new clip (frozen figures; moving figures acceptable ONLY at extreme wide)
6. BEFORE/AFTER compare page built per piece; user reviews at the wave gate

## Waves (HUMAN GATE after each; cumulative-spend check at every gate)

| Wave | Pieces | Notes |
|---|---|---|
| A | it_is_finished, pierced, crucifixion_foretold | **rate-measurement wave**: includes ≥1 Christ-CU/wound living-light proof (hardest target, per panel); measure actual re-roll rate |
| B | forsaken_cry, i_thirst, into_thy_hands, today_paradise | only after re-quote (below) |
| C | watch_one_hour, woman_behold, thirty_pieces | |
| D | empty_tomb, sign_of_jonah | de-dup stills: reuse_check FIRST (never re-pay for plates siblings have), then bible-check fact cards + vision audit + stills-gate + asset_index registration |
| E | father_forgive_them | SEPARATE: mocomic→livingpage greenfield migration; scoped + quoted on its own after Wave A proves the transform |

Per piece: (1) $0 spec upgrade → **rollout_gate PASS** → (2) pre-flight
`pipeline.cost summary --episode <id>` vs the $25/short ceiling (breach → ASK THE USER,
never silent override) → paid renders → filmstrip QC each → (3) $0 rebuild → score → sfx
→ before/after page → register. Backup each final pre-rebuild (`.bak_prelivinglight`).

## Budget (v2 — panel-corrected)

- Pilot observed: 7 rolls → 3 keepers (the 3 template locks were CREATED by those failures,
  so the go-forward rate should beat 2.3×/keeper — but that is a hypothesis, not a plan input).
- **Wave A measures the true rate** on ~6 clips (2/piece) incl. one wound/CU proof.
  After Wave A: re-forecast B–D at the measured rate and **re-quote the user** before Wave B.
- Base: 12 pieces × 2 clips = 24 × 7.5cr = 180cr. At pilot-observed worst case (2.3×):
  ~415cr + Wave D stills/clips ≈ 110cr → **~525cr worst case, exceeding the 485 envelope —
  this is why the re-quote gate exists.** At the hoped ~1.5× rate: ~380cr total, inside it.
- **HARD STOP-LOSS: 485cr cumulative** (ledger-checked at every wave gate); breach = stop
  and ask, never spend through.
- Spent so far: ~52.5cr pilot + promotion. empty_tomb episode ceiling headroom verified
  ($10.95 of $25 used).

## Answered panel objections

- **gemini "BytePlus stills unsupported":** WRONG — the batch pipeline renders stills via
  BytePlus ARK (`run_piece.py:34` `ark.ap-southeast.bytepluses.com`, `SEEDREAM_USD_PER_IMG`);
  every cluster still was made there. gemini read the older `cli_visual` provider docs.
- **claude "tests 305 vs STATE 278":** STATE's old block was stale; verified now = 40 gate/
  runner tests green within the full suite (305+ passed / 1 skipped as of this revision).
- **Phase 0 pinned:** rollout_gate + tests + living_light channel committed to git BEFORE
  Wave A (panel fix).

## Known risks & mitigations (unchanged from v1 where not superseded above)

- Kling QC lottery → filmstrip QC every clip; rejects parked, never deleted; rate re-measured.
- Kling disobeys "frozen" → moving figures pass ONLY at extreme wide (checklist #5).
- Shipped-piece regression → per-piece backup + before/after page + wave-gate user review
  (the review IS the re-approval for the 10 already-approved Cross finals).
- Grid crops chopping heads → panel_fit fit-gate + hand-tuned anchors per face.
- Doctrine → no content changes except light/atmosphere; new Wave D stills take the full
  bible-check + vision-audit + stills-gate + asset_index path.
