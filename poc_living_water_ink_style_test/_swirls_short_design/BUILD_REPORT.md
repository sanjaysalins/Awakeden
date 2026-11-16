# Swirls SHORT build report (design v3.2) - builder, 2026-11-15

All code is $0. Every test runs with `requests.post` patched to raise, a temp bridge folder and a fake servicer.
No OpenArt MCP call, no ElevenLabs call, no commit. Final run of `_validate_swirls_short.py`: **414 checks, 0 skipped, ALL PASS**.

Files (all in lane):
`POC\swirls_guard.py` (new: spend guard) - `POC\swirls_short.py` (rewritten: gates) - `POC\swirls_short_run.py` (new: commands) -
`POC\swirls_episode.py` (wired) - `POC\swirls_verify.py` (strict judge, bound overrides) - `POC\swirls_assemble.py` (frame-exact trim) -
`POC\build_srt.py` - `POC\test_the_cross\openart_bridge.py` (guarded protocol) - `POC\test_the_cross\swirls_page.py`, `POC\swirls_cover.py`
(provider refusal) - `POC\SWIRLS_SHORT_SERVICER.md` - `POC\_short_templates\{generate_score_piano.py,build_sfx.py,SOURCE.md}` -
`POC\fixtures\golden_8unit\` - `POC\_validate_swirls_short.py`.

## Built vs not built

| Design section | File : function | Test |
|---|---|---|
| s1 timing, frames B(k), back = ceil(slot+2.0), front/page rules | swirls_short:build_timing, expected_clip_duration, lint_timing | T3, T3b (hand-computed golden), T3 ep13 |
| s1 1080x1920, scale-and-crop, `-frames:v`, no fill, no `-shortest` | swirls_assemble:make_trim, assemble | T1, T2 |
| alignment meta (ElevenLabs only, hash, count) | swirls_short:read_alignment | T3b negatives |
| G1/G1e shape + estimate; G1v speaker derived | swirls_short:lint_words, derive_speakers, lint_speakers | T4 |
| G1s sequence (4 lists) | swirls_short:lint_sequence | T5b |
| G1k KJV wrapper (no `...`/ellipsis, whole-word, case, verify_span too) | swirls_short:lint_kjv, kjv_run_found | T5 (John 1:20 `I am ... the Christ` FAILs; shared verify_span accepts it) |
| G1g | swirls_short:run_narration_gate | T12 (wired, checked on ep16; synthetic words skip it) |
| G4 baked text, G5, G5a (wide verb list), G6, G7a/b/c, G8, G8t | swirls_short:lint_* | T4, T4b |
| page_plan schema validated on load | swirls_short:validate_page_plan, load_page_plan | T4b (each missing field FAILs; old shape FAILs) |
| G9 strict raw-string judge, `read`, audit_version, WARN never pass | swirls_verify:judge_still_raw, audit_still_v3, record_read; swirls_short:is_pass | T7 |
| metered Vision refused | swirls_verify:_vision_raw, run:_vision_gate | T7 |
| G10 edge scan wired (level constants) | swirls_short:edge_scan, EDGE_*_LEVEL | T9 (see changes) |
| G11, G14 (manifest units), G14s | swirls_short:clip_tech, lint_clip_provenance, lint_still_provenance | T7, T12 |
| G12, G13 (540 px strips x6, judge), G15h | swirls_short:still_stretch, make_strips, judge_eyes, moving_hold | T7b, T8 (real ep10/13/16), T1, T12 |
| G15, G16 chain, G17 score gate, film panel pass mark | swirls_short:lint_assembly, check_chain, score_gate, film_panel_pass | T1, T12, T14 |
| Overrides narrow (gate+unit+hash+quote; 6 never) | swirls_verify:apply_overrides_bound | T7c |
| SWS-G0 guard: lock, uuid rid, one open row, grants append-only, quotes, caps (quote+rerolls)x1.10, hard stops, reroll count, unit grants, price from payload | swirls_guard:before/approve/write_quote/price_of/_check_common | T6 |
| Bridge protocol: guarded folder, atomic claim, not_after, heartbeat, claim-or-cancel, creation_id, staging, receipt read-back, fetch/confirm/void/sweep/reconcile | openart_bridge:_submit_guarded, cancel_request; swirls_guard:after/_settle/fetch/confirm/sweep/reconcile | T6 (two servicers one generate; timeout before/after claim; killed client; past not_after; error reply + creation_id; typed params; sound ON; over-price lock) |
| Provider != openart / no marker refuse | swirls_page/cover:_refuse_non_openart; run:require_marker | T6 |
| ElevenLabs boundary: whitelist, char price, `_turns` auto-delete, once-per-hash align, open row until confirm | swirls_guard:eleven_*; run:prepare_turns, cmd_voice/align/score | T6b, T12 |
| `build_srt.build()` refuses marked folder; cache-only SRT; assemble hook | build_srt:build, build_from_cache; swirls_episode:cmd_assemble | T6b, T12 (post patched to raise) |
| G2w audio says the words | swirls_short:audio_says_words | T10b (real ep13 audio via local whisper: 0% unmatched) |
| hash-bound animate, stale mp4 superseded | run:cmd_animate, clip_state | T7, T12 |
| score/SFX templates reading receipts; token refusal; `--dry-run` | _short_templates | T14 |
| hold, animatic, contact sheet, status + open WARNs | run:cmd_hold/cmd_animatic/cmd_status | T12 |
| T11 anchor ref | (existing upload_engine) | T11 |
| TRIAGE "fixed in design" items | all rows above; mouth pixel check, cross-page FAIL, hard_props, shared score/SFX, `adopt`, etc. are the design's own deferred list (s9.4): NOT built | - |

## Old validators: HEAD baseline vs final

| Validator | HEAD (temp worktree) | Main tree before edits | Final |
|---|---|---|---|
| _validate_swirls_assemble.py | could not run: sparse HEAD checkout lacks the pilot mp3/mp4 (paths too long to check out fully) | ALL PASS | ALL PASS |
| _validate_swirls_cover.py | rc 0, prints "SOME FAILED" (pre-existing) | same | same |
| test_the_cross\_validate_swirls_page.py | PASS | PASS | PASS |
| ..._page_hem.py | PASS | PASS | PASS |
| ..._page_hybrid.py | rc 0, prints a prompt diff (pre-existing) | same | same |

Final = identical to the main-tree-before result: no new failure vs baseline.

## Dry run (T12)
Real `cmd_*` in the guarded order, real bridge files, fake servicer: init, words, ok words, quote/approve/voice, ok voice_ear, align, timing, plan,
quote/approve pictures, still (north star), hold, ok northstar_look, still x7, verify, animatic, ok stills_animatic, quote/approve clips,
animate x2 + clipqc, ok clip_test_look, animate+clipqc x6, assemble --draft, ok draft_cut, quote/approve score, score, assemble --score,
SFX copy, cache SRT, FINAL_VIDEO, status. Result: all pass; status says step 10 next; logged spend pictures 320 cr (a ref crop is free),
clips 1,890 cr = quote; receipts chain clip rows -> draft receipt -> scored receipt -> final receipt -> FINAL_VIDEO.txt; each out-of-order
step refused (second still, third clip, reroll after close, spend after draft_cut). Kept at
`C:\Users\sanjay\AppData\Local\Temp\claude\6f3845a98aec2db1\e0e91fd5-0c04-40d1-b589-a7ab5c3973b3\scratchpad\swirls_episode_99_dry_run`.

## Changed from the design, and why
1. **Edge scan on covers is WARN, not FAIL** (`EDGE_COVER_LEVEL = "CONDITIONAL"`). T9 ran the shipped covers: the scan did not separate ep2/5/7/8 from ep10/13 (ep10 and ep13 covers trip it). The design's own fallback ("else stays WARN and says so"). Flip the constant when a better detector exists. Wiring and FAIL path are tested.
2. **Guard lives in `swirls_guard.py`** (new module), not inside `swirls_short.py`, to avoid an import cycle with the bridge. Re-exported from swirls_short.
3. **G15h numbers from T8:** `k=3`, absolute floor 0.5 (real back covers' windows >= 1.26; frozen / frame-0 / stops-at-1.5 copies <= 0.10 / 0.0). The frozen control's N is ~0, so the floor does the work.
4. **Receipts:** `assembly_receipt.json` is the DRAFT's; the scored cut writes `assembly_receipt_scored.json` (so the draft_cut look keeps its hash).
5. `align` may run after `voice_ear` using the voice grant (the voice step closes at voice_ear but alignment is priced inside ask 1).
6. G14s on refs accepts a hand crop whose declared `from_still` has a receipt; G7c exempts the page a ref was cropped from.
7. Cap: `at_most = ceil((about + planned rerolls) x 1.10)`; pictures about = 8 stills + 2 refs (400), rerolls 360, at most 836 (design said ~840). Clips at-most is computed from the real clip seconds.
8. Bug found and fixed in my own code: a reroll renamed the PNG before the guard check, which voided the closing look and let a paid request through; now the step is checked first.
9. Voice price rates (`$0.0003/char`, alignment $0.05, score $0.0222/s) are placeholders marked UNVERIFIED.

## Coordinator tasks (out of lane)
Owner-only approval (`approve` must prompt: settings `ask` rule); fix `pipeline\kjv_strict.py:verify_span` (ellipsis splice, in-word match); `AGENT_BRIDGE.md` pointer to `SWIRLS_SHORT_SERVICER.md` and remove "balance difference as receipt"; `per_turn_synth.py` per-speaker stability, marker check, cache by text hash; install `SKILL_v3.md` after review; decide on the HEAD-baseline note above (cover validator prints SOME FAILED at HEAD too); `release_check.py` on a POC episode before posting; real ElevenLabs rates.

## Still not run (not mine)
Probes R1 (OpenArt creation record fields: the guard assumes `creation_id`, `sent_params`, `credits_spent`), R2 (ElevenLabs alignment permission), R3 (ElevenLabs history receipt). Design v3.2 must still go back through the plan panel before the pilot spends.
