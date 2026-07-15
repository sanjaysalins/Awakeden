# PS22 REBUILD - PAID WORKLIST (needs the user's GO before ANY command here runs)

Written by the Wave F $0 pass, 2026-07-15. Everything else in the 5 pieces is DONE and
$0 (byte-identical stills, hash-bound clips, specs gate-PASS, alignments fresh).
This file is the complete list of metered commands still owed, per
`batches/_rollout/PS22_SHORTS_REBUILD_PLAN.md`.

**Quote (plan): ~$1.04 base / 7.5 cr — 6 seedream stills ($0.30-0.39 w/ re-rolls) +
1 Kling living-light clip ($0.65). Ask-before-spending applies; log to
`data/spend_ledger.jsonl` (run_piece does this automatically).**

---

## 1. Seedream wave - 6 fresh stills (~$0.30, one batch)

Preferred path (P0-guarded: lint gate + guard_prompt + arm_audit + ledger + budget
ceiling + sibling-reuse pre-flight). The prompts/refs live in each `piece.json`
`stills.jobs` (authored + linted this pass; house STYLE tail appended at render):

```
.venv\Scripts\python.exe run_piece.py "batches\cluster_01_cross\mockers_words_ps227"      --stage stills --render --only wagging_heads_close,rulers_sneering
.venv\Scripts\python.exe run_piece.py "batches\cluster_01_cross\declared_brethren_ps2222" --stage stills --render --only risen_christ_congregation
.venv\Scripts\python.exe run_piece.py "batches\cluster_01_cross\ends_of_earth_ps2227"     --stage stills --render --only nations_turning_wide,kindreds_worship
.venv\Scripts\python.exe run_piece.py "batches\cluster_01_cross\body_foretold_ps2214"     --stage stills --render --only body_suspended_wide
```

Raw prompt/ref reference (exactly what the jobs carry - model `seedream-4-5-251128`,
size `1440x2560`):

| piece | slug | ref | prompt |
|---|---|---|---|
| mockers_words_ps227 | `wagging_heads_close` | `../crucifixion_foretold_ps2218/visual/crowd_mocking.png` | three Judean passers-by on the road below the cross at dusk, heads mid-shake in scorn, mouths open in taunt, one arm pointing up toward the cross above, weathered bearded faces, dusty wool robes and head cloths, 1st-century Judea, vertical |
| mockers_words_ps227 | `rulers_sneering` | `../crucifixion_foretold_ps2218/visual/crowd_mocking.png` | a knot of chief priests and scribes in rich temple vestments and head wraps standing apart from the crowd at Golgotha, lips curled in sneers, one gesturing dismissively up toward the cross above, Jerusalem wall behind, 1st-century Judea, vertical |
| declared_brethren_ps2222 | `risen_christ_congregation` | `../../../ref_library/characters/JESUS.png` | the risen Christ standing in the midst of a seated congregation of brethren in a lamp-lit stone hall, both arms lifted in praise with smooth open palms, one warm golden shaft falling across Him, upturned faces in wonder, vertical |
| ends_of_earth_ps2227 | `nations_turning_wide` | (none) | a vast dawn vista of many lands seen from above, plains, desert, river valley and sea coast, small kindreds of every nation in varied period dress all turned and bowing toward one great warm light rising on the shared horizon, vertical |
| ends_of_earth_ps2227 | `kindreds_worship` | `../forsaken_cry_ps221/visual/look_up_faces.png` | a gathering of worshippers of many nations, varied skin tones and period garments and head wraps, kneeling together with hands lifted toward warm light falling from above, faces lit with awe, 1st-century world, vertical |
| body_foretold_ps2214 | `body_suspended_wide` | `../crucifixion_foretold_ps2218/visual/face_on_cross.png` | a distant reverent silhouette of the crucified Christ seen from far below against a vast storm sky, body hanging low by the outstretched arms, weight sagging onto the shoulders, limbs drawn taut, thorn crown on the bowed head, dark rocky hilltop, vertical |

### Eye-QC criteria (full-res, per still, BEFORE any Kling / build spend)

- **wagging_heads_close**: exactly 3 figures, heads visibly mid-shake/turn (not static
  portraits), hostile not mournful, period dress, faces consistent with the
  crowd_mocking world; no modern items, no text. Animation-clean (<=3 faces).
- **rulers_sneering**: reads as RULERS (richer vestments) vs the commoner passers-by;
  sneers not grief; no cross IN frame needed (they gesture up/out); period temple dress,
  no writing/phylactery text.
- **risen_christ_congregation**: WOUND-FREE hands (smooth open palms - this is a
  living-light target; Kling regrows blood on marked palms, hard rule); face matches
  the JESUS ref; warm single light shaft (the LL clip animates THIS light); brethren
  seated, reverent; no halos-with-text, no anachronism.
- **nations_turning_wide**: many small distant figures (no big faces to garble), varied
  lands reading as ONE vista, all orientation toward the single horizon light; NO text,
  no map labels, no modern skylines.
- **kindreds_worship**: varied skin tones + garments genuinely distinct, hands lifted,
  faces awed not agonized; no duplicate-face artifacts (check every face - crowd shots
  are the known anatomy risk); period only.
- **body_suspended_wide**: REVERENT distant silhouette - no gore, no visible wounds
  detail at this distance; weight visibly ON the arms/shoulders (the Ps 22:14 point);
  thorn crown present (bank rule: every cross frame carries it); body ATTACHED to the
  cross (no floating figure).

### Post-render $0 steps (same wave)

1. Vision content audit per PNG (fail-closed, sidecar must go PASS).
2. `stills_gate.py <piece> --build` (re-hash), `--quality <slug> PASS --axes ... --notes`,
   then the USER approves the fresh stills in the review page (these are NEW art, not
   corpus copies - human gate applies for real).
3. body_foretold: RE-EYEBALL the `A_BODY` grid anchors in
   `batches/cluster_01_cross/body_foretold_ps2214/visual/livingpage_short.spec.json`
   (beat 7 hero_frac3) against the actual render - they are prompt-designed placeholders.
4. Re-run builder lint on the 4 affected pieces (missing-still findings must be gone).

## 2. Kling living-light clip - declared_brethren (7.5 cr / ~$0.65)

Only after `risen_christ_congregation.png` is rendered, audited PASS, and
user-approved in the stills gate (run_piece enforces the gate + rollout gate + budget):

```
.venv\Scripts\python.exe run_piece.py "batches\cluster_01_cross\declared_brethren_ps2222" --stage animate --only risen_christ_congregation
```

The living_light entry (already in piece.json, drives the prompt):
- target: "the risen Christ standing in the midst of the brethren"
- light: "the warm lamplight around Him slowly builds and breathes, the single golden
  shaft widening gently across the hall, soft haze glowing where the light falls"

### Eye-QC criteria (the clip)

- Figures FROZEN: no limb/head motion, no face drift on Christ or any brother
  (frame-step the ends).
- ONLY the light/haze moves; light builds smoothly - no flicker, no AI-glitter
  particles/bokeh (glitter = reject).
- NO blood appears anywhere across the 5s (wound-free source is the defence; verify).
- No new figures/objects invented at frame edges.
- On PASS: nothing else to do - the clip is hash-bound by run_piece automatically.

## 3. After all paid items land ($0 finishing, per piece)

1. Full builder run (no --lint) -> `livingpage_short.spec_preview.mp4` per piece.
2. `run_piece.py <piece> --stage score` then the standing /sfx + compare pages.
3. corpus_diversity.py re-check + the 5-CLI panel on the batch per the standing gate.

## Contingency ceiling (from the plan)

+1 Kling re-roll on the congregation LL (7.5 cr / $0.65) + still re-rolls inside the
1.3x budget = worst case ~$1.70 / 15 cr total.
