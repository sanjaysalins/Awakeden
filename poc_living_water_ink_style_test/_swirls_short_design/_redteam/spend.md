# Red team: money only (design v3.1)

Target: `SWIRLS_SHORT_PIPELINE_DESIGN_v3.md` sections 3, 5, 8. Checked against the code on disk:
`POC\test_the_cross\openart_bridge.py`, `POC\test_the_cross\swirls_page.py`, `POC\swirls_cover.py`,
`POC\swirls_episode.py`, `POC\swirls_short.py`, `POC\build_srt.py`, `REPO\pipeline\assembly_align.py`,
`REPO\AGENT_BRIDGE.md` (OpenArt section), `PythonProject1\jesus\narration\per_turn_synth.py`,
ep16 `generate_score_piano.py`. $0, read-only. No review files read.

"Stops it" = does the design as written stop it.

---

## BLOCKER

**B1. Two sessions service the same request (double spend).**
- Scenario: `REPO\.agent_bridge\gen_requests\` is shared by every session in this repo (other sessions run at the same time; memory `project_unexplained_hf_spend`). Two live sessions both see `<id>.request.json`, both call `openart_generate_video`. Two creations, two charges. The first reply wins in `submit()`; the second charge is never logged in `spend_log.jsonl`.
- Where: design 5.1 / 5.2. `openart_bridge.py` has no claim step; AGENT_BRIDGE.md servicing step 1 is just "Read the request JSON".
- Stops it: **no**.
- Fix: servicer rule 0: claim first by atomic rename `gen_requests\<id>.request.json` -> `gen_claimed\<id>.<session>.json` (`os.replace`, single winner); only the winner calls MCP; a failed rename = skip. Client cancel (B2) must use the same rename race. T6: two fake servicer threads, one request -> exactly one MCP call.

**B2. Timeout cancel does not stop an in-flight generation; void + retry pays twice; the late file is used as if free.**
- Scenario: servicer has read the request and is in `openart_creation_wait` (video often outlasts one wait window). Client hits `OPENART_BRIDGE_TIMEOUT`, moves the file to `cancelled\`, row UNRESOLVED. The session checks OpenArt history, sees nothing yet (creation still queued, or filtered to COMPLETED), runs `confirm --void`, retries. Both creations bill. Then the servicer downloads the late result straight to `out_path`; next `RUN still`/`animate` sees the file exists and skips (`render_still` / `render_animation` "[skip] already exists"), so a voided (cost 0) row's output ships.
- Where: design 5.1 bullet 4, 5.2 rule 1 (checked only at pickup), 5.3 void rule; `swirls_page.py:347,403` skip-if-exists.
- Stops it: **partly** (the move stops a not-yet-picked request only).
- Fix: (a) with B1's claim, the client may cancel only by winning the rename; if the file is already in `gen_claimed\`, the row becomes `LATE_PENDING`, never voidable. (b) Servicer writes `gen_claimed\<id>.submitted.json` with `creation_id` the moment `generate_*` returns, before waiting. (c) `--void` allowed only if the request went to `cancelled\` from `gen_requests\` (never claimed). (d) Servicer downloads to `gen_staging\<id>.<ext>`; only `guard.after()` moves it to `out_path`. A late reply re-opens the row as UNRESOLVED with its `creation_id`; its file stays in staging.

**B3. `SWIRLS_GEN_PROVIDER=hf` spends Higgsfield money with no guard at all.**
- Scenario: the env var is left set in a shell (or by another session's `.env`). Design deletes `_guarded_render` (section 9.1) - the only place that today refuses non-OpenArt for trim episodes (`swirls_episode.py:82`). The new guard lives only inside `openart_bridge.submit()`. `render_still` -> `_render_still_hf`, `render_animation` -> `_render_animation_hf`, and the cover twins (`swirls_cover.py:188,240`) call `hf.exe` directly: no approval, no cap, no row.
- Where: design 5.1 ("the boundary"), P2 (prose only), 9.1 row `swirls_episode.py`.
- Stops it: **no** (a regression the design introduces).
- Fix: in `render_still`, `render_animation`, `render_cover_still`, `render_cover_animation`: if `out_path` is under a `.swirls_short` marker and provider != `openart`, raise. Add to T6.

**B4. Every clean non-draft `assemble` calls paid ElevenLabs alignment with no row.**
- Scenario: `swirls_episode.py:370` runs `build_srt.build()` after a clean `assemble`. `build_srt.build()` calls `align(folder, force=True)` (`build_srt.py:54`) with `ASSEMBLY_ALIGN_BACKEND=elevenlabs` set at import. So step 8's `assemble --score piano`, every re-run of it, and step 9's re-checks each make a paid forced-alignment call outside the voice row. It also overwrites `narration.alignment.json`, which the design treats as the frozen timing source.
- Where: design step 9 / 9.1 ("`build()` unchanged"; the assemble hook is not in the REDO list). T12 mocks the aligner underneath, so T12 would pass while the real path pays.
- Stops it: **no**.
- Fix: in `swirls_episode.py` assemble, call `build_srt.build_from_cache()` for trim/marker folders; make `build_srt.build()` refuse under a marker. T12: patch `requests.post` to raise, not just the aligner.

**B5. Request written, then the run dies: the live request has no expiry.**
- Scenario: the client is killed (Ctrl-C, PC sleep, session context ends, background job reaped). `KeyboardInterrupt`/`SystemExit` are not `Exception`, so "on timeout or any error, move to cancelled" never runs. `<id>.request.json` stays live in `gen_requests\` forever (watcher calls it "debris" but nothing removes it). Any session may service it hours or days later. Meanwhile the session `confirm <rid> --amount 0 --note ...` (allowed for any open row) and re-runs: second request. Both bill.
- Where: design 5.1 bullet 4, 5.3 `confirm`, approval expiry removed (changelog 17).
- Stops it: **no**.
- Fix: (a) request carries `not_after` (ts + timeout); servicer rule: never service past it. (b) cancel in `finally:` / `except BaseException`. (c) `RUN` start-up sweep: any request in `gen_requests\` whose `rid` belongs to this episode and has no live client PID (write `client_pid` in the request) -> move to `cancelled\`. (d) `confirm --amount` on an OpenArt row needs a `creation_id` or a proven-never-claimed cancel.

---

## MAJOR

**M1. The owner says yes to "about X"; the guard enforces a cap of 1.6-1.9 X the owner never saw.**
- Scenario: owner pages ask "7 more pictures, about 280 cr - yes?"; the approval cap is 520. Clips: asked 1,330, cap 2,170. Test clips: 595 vs 945. Voice: $0.35 vs $0.60. Up to 840 cr can be spent beyond the number the owner agreed to. The `--note` is typed by the session and can be the words-pick note ("ok words").
- Where: section 3 table (owner page wording), section 8 cap column, 5.4.
- Stops it: **no**.
- Fix: every price question shows both: "about 280 cr, at most 520 cr - yes?". `approve` refuses unless the note contains the cap number, and refuses a note equal to any `ok` note.

**M2. Cap maths: every cap is too small for its own stated contents once the 110% reserve is applied.**
- Scenario: (all from section 8 + 5.3 "spent + 1.10 x price fits the cap")
  - north star 240 = 40 + 3x40 + 2x40; last item needs 200 + 44 = 244 > 240.
  - stills 520 = 280 + 6x40; last reroll needs 480 + 44 = 524 > 520.
  - clip test 945 = 595 + one 10 s back reroll; needs 595 + 385 = 980 > 945.
  - clips 2,170 = 1,330 + 3x280; 3rd reroll needs 1,890 + 308 = 2,198 > 2,170.
- Effect: fail-closed, but the planned reroll is always refused, so re-approval becomes routine and is typed by the session (see M1, M5).
- Stops it: n/a (design bug).
- Fix: cap = quote + rerolls, all x 1.10; or reserve 110% only on the open row and test confirmed rows at their receipt. Add these four numbers to T6.

**M3. R1 fallback receipt (`tariff_from_sent_params`) does not catch sound-on.**
- Scenario: Kling form default is sound ON (40 cr/s). The servicer forgets `generateSound: false` but writes `sent_params.sound=false` from the request (it believes it sent it). Priced from what it says it sent -> 35 x d -> confirmed. Real charge 40 x d is never seen. Design claims it "still catches sound-on".
- Where: 5.2 probe R1 fallback.
- Stops it: **no** (only if R1 finds a charged-credits field).
- Fix: fallback params must be read back from `openart_creation_show(creation_id)` (OpenArt's stored record), not typed from the call; if the record does not carry sound/duration/resolution, the row stays UNRESOLVED and the owner decides.

**M4. An open row only blocks OTHER steps; same-step requests race and stack.**
- Scenario A: clip 1 of 6b comes back UNRESOLVED (e.g. sound-on). 5.3 blocks "every paid command of every other step", so clip 2 of the same step goes ahead; the same servicer mistake repeats 6 times.
- Scenario B: two terminals (or a forgotten background job) run `animate f03` at once. `before()` is read-check-append with no lock; both pass cap and reroll checks; both see no mp4. Today's rid (`swirls_short.py:600`: step-unit-len+1-provenance) is identical for both, so `_read_log` merges them into one row: one charge vanishes from the log.
- Where: 5.3 open-row rule; `swirls_short.py` `request_spend`, `_append`.
- Stops it: **no**.
- Fix: one open row per episode, any step. Exclusive lock file (`os.open(O_CREAT|O_EXCL)`) held across check + append. `rid = uuid4`. T6: two threads, one request goes through.

**M5. Re-approval semantics undefined; today's code re-grants the whole step.**
- Scenario: 4th request for f04 needs "a new `approve ... --unit-id f04`". `swirls_short.approve()` overwrites `cap_cr` for the whole step and keeps `units=None` (whole step) when the earlier approval had no unit list. One per-unit reroll yes silently re-opens the step for every unit with a fresh cap. Design does not say how many renders a re-approval unlocks or whether the cap adds or replaces.
- Where: 5.3 reroll rule, 5.4 `approve`; `swirls_short.py:530-535`.
- Stops it: **no**.
- Fix: approvals are append-only grants `{grant_id, step, unit|null, extra_cap, renders_allowed}`; cap = sum of grants; a unit grant only adds renders for that unit; reroll count = rows for (step, kind, unit) minus granted renders.

**M6. Old-protocol servicers still answer guarded requests during the pilot.**
- Scenario: the AGENT_BRIDGE.md mirror is a coordinator task (section 12.1), outside the lane. Any other session follows AGENT_BRIDGE.md step 6 (quote or balance difference, no `creation_id`, does not read `servicer_rules`). The charge happens; the guard marks UNRESOLVED (good) but the money is gone, and M10 lets the session clear it with a typed number.
- Where: 5.2, 12.1.
- Stops it: **partly** (fail-closed after spend).
- Fix: guarded requests go to a separate dir `gen_requests_guarded\` that only a session that has read `SWIRLS_SHORT_SERVICER.md` watches. In lane (POC file + new dir).

**M7. Billed creation, failed download -> retry pays again.**
- Scenario: generation completes, `curl` to `out_path` fails (F: is full - memory `project_let_the_little_children_episode`), servicer writes `status:"error"`. No `creation_id` in error replies; the request is archived, not cancelled, so void is impossible and the only path is a new render. Paid twice for one clip.
- Where: 5.1 error path, 5.2 rule 3 (receipt fields only on success).
- Stops it: **no**.
- Fix: error replies must carry `creation_id` when one exists; `RUN fetch <rid>` re-downloads that creation for $0; `before()` refuses a new request for a unit that has an UNRESOLVED row with a `creation_id`.

**M8. The marker guard is fail-open on location.**
- Scenario: `out_path` outside the marker folder (staging on the C: scratchpad because F: is full; a `refs\` junction; a copied folder without the dot-file, which Explorer copies can drop) -> "behaves exactly as today" = no guard.
- Where: 5.1 bullet 1 and last bullet.
- Stops it: **partly**.
- Fix: also fail closed from the caller: `swirls_episode.py` refuses any paid command when `is_trim_episode()` is true and the marker is missing; `guard.before()` refuses when `out_path` is not under the guarded `episode_dir`.

**M9. ElevenLabs: price, command and receipt are all typed by the session.**
- Scenario: (a) `RUN paid <step> -- <command>` runs any command: `--force`, another script, a loop. (b) the row's "quoted price" for usd steps has no formula. (c) `confirm --amount` is a typed figure. (d) "Delete `_turns\` first if any word changed" is prose; `per_turn_synth.py:232` reuses `_turns\NN_<speaker>.mp3` by file name, so old-text audio is "paid" and confirmed; forced alignment then fits the new transcript onto old audio, so G1s (alignment as 4th list) passes and stills are bought on wrong audio.
- Where: 5.5, step 2.
- Stops it: **no**.
- Fix: whitelist the command per step (exact script path, banned `--force`); price = characters in `narration-tagged.md` turns x plan rate (score: seconds x rate); `paid voice` deletes `_turns\` itself when the `ok words` hashes differ from a `_turns\.text_sha256` sidecar; receipt from ElevenLabs `GET /v1/history` items since the row's ts (per-item character counts, filter by voice ids + text) - "no machine receipt" is not quite true.

**M10. `confirm --amount` clears an UNRESOLVED OpenArt row with any number.**
- Scenario: `after()` rightly marks UNRESOLVED (no `creation_id`, sound on, over 110%). The session types `confirm <rid> --amount 245` and carries on. Over-price spend beyond the owner's yes is never shown to the owner; the cause is never fixed (feeds M4-A).
- Where: 5.3 confirm.
- Stops it: **no**.
- Fix: for OpenArt rows `confirm` requires a `creation_id` and a `creation_record` figure; if the figure is over the row price, the note must be a new dated owner note and the step stays locked until a new grant.

**M11. Direct MCP calls by the servicer are banned "by rule only", with no detection.**
- Scenario: the attending session "just quickly" re-renders a ref or a still with `openart_generate_image` while QC-ing. Not in any log.
- Where: 5 intro, 11b.
- Stops it: **no** (stated limit).
- Fix ($0 detective control): `RUN reconcile` lists `openart_creation_list` for the episode's time window and flags any creation whose prompt sha matches an episode prompt (or whose output lands in the folder) but whose `creation_id` is not in `spend_log.jsonl`. Run it in `status` and before every `approve`.

---

## MINOR

- **m1.** Reroll count "per unit" must key on (kind, unit): f03 still rerolls would otherwise use up f03's clip renders. 5.3.
- **m2.** Still price 40 is checked only for nano-banana-pro image2image 2K 9:16. Text2image, other aspects, more refs are priced 40 blindly. Price table should key on mode + aspect too, or refuse.
- **m3.** `payload_sha256` binds the dict, not the request file the servicer reads, and not ref file contents. Servicer should echo `request_sha256`; payload should carry ref sha256s. 5.3 / 5.2.
- **m4.** `spend_log.jsonl` / `approvals.json` are hand-editable; add a hash chain (each row carries the previous row's sha) so a deleted row shows.
- **m5.** On Windows the move to `cancelled\` can fail if a servicer holds the file open; then write a `<id>.cancel` tombstone that the servicer checks. 5.1.
- **m6.** An error reply (not timeout) is archived to `gen_archive\` by `submit()` today, so `--void` can never apply; and whether a FAILED Kling creation is charged is unknown. Probe R1 should also check a failed creation.
- **m7.** Approvals are not bound to the episode: a copied folder carries `approvals.json` (ok hashes catch most of it). Put a random `episode_id` in the marker and in every grant.
- **m8.** `ok` hashes are taken by the session at `ok` time, not shown on the owner page. Print the 8-character hashes on the page and have `ok` refuse if any file is newer than the page.
- **m9.** `request_spend` compares whole-episode spend to one step's balance snapshot (`swirls_short.py:597`); stated as a sanity check, but it can refuse or pass for the wrong reason.
