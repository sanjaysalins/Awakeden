# Independent review — claude (OK, 114s)

I'm reviewing this as a plan. I checked a few claims against the real code on disk.

## What I checked on disk

1. **The plan no longer matches the code.** Sections 6 and 9 say a lot of work is "DESIGNED" or still to do. But most of it is already built:
   - `build_srt.build()` already refuses a marked folder.
   - `build_from_cache()` already exists, and `swirls_episode.py:266` already calls it.
   - `SWIRLS_SHORT_SERVICER.md` already exists. The plan calls it "new".
   - `swirls_short_run.py` exists (972 lines). It is missing from the file map, and it talks about a `swirls_guard` module the plan never names.
   - The "paid call at `swirls_episode.py:370`" is wrong: line 370 is just `main()`.

   So the plan's one status table is already out of date. That breaks its own **Honesty rule**.

2. **Order is broken.** Section 9.2 says v3.2 goes back to the plan panel *before phase B*. But the phase-B money code (guard, servicer, `cmd_*`) is already being written. And the pilot folder `swirls_episode_17_voice_in_the_wilderness` already has its marker, `_quotes\` and `refs\`. Either stop the build until this panel is done, or say plainly that the panel is judging code that already exists.

3. **Missing from the file map.** `swirls_short_run.py` and `swirls_guard` (if it is a file) are not in 9.1. Tests T6/T12 say "real `cmd_*`", but the plan never says where they live.

## Plan risks

4. **The money guard is too big for a $10 pilot.** Section 5 builds heartbeats, atomic claims, staging, `LATE_PENDING`/`CANCELLED_UNCLAIMED`, fetch, reconcile, an append-only log and a lock file. That protects about $6–10. And section 5 admits the guard **cannot prove the owner said yes** and **cannot see a direct OpenArt call**. Those are the two real dangers. Fix them first (coordinator task 1, a permission prompt on `approve`). Then cut the bridge state machine back to: claim, one open row, and a receipt read-back.

5. **Everything rests on probe R1.** The receipt read-back (5.2 step 5, 5.3 `after()`) assumes `openart_creation_show` returns the credits charged and the settings sent. Phase B builds all of this before R1 is run. If R1 fails, every row goes `UNRESOLVED` and needs a person each time. Run R1 (it costs $0) **before** building `after()`, and design the fallback path first.

6. **The voice steps are weak.** `--stability` is one global setting, so step 2 uses 3 passes and moves files around by hand. The turn cache works by file name, so moving character files "aside" for take B can silently reuse take A (memory: `per_turn_synth_stale_cache`). The `_turns\` hash check only covers a text change, not this move. Add a test: take A and take B must have different hashes for each character turn.

7. **G2w (the whisper check) has no proven tool.** There is no named local whisper installed on disk; the only reference is a string in the code. The 25%/10% limits are a guess. And T10b only checks that a fake mp3 fails. Name the transcriber and check it is installed before G2w counts as a gate. Or make it WARN until T10b sets real limits.

8. **G15h's limit `k` decides a FAIL before it is proven.** Until test T8 sets `k`, the moving hold can fail a good clip or pass a bad one. The plan keeps the "played-through look" as the stand-in. Make G15h WARN until T8 passes, not FAIL.

9. **Strict text check vs Vision misreads.** G9 FAILs on any wording difference, and Vision misreads handwriting (section 12). A `RUN read` record is then needed for each one. With 8 pages × about 5 strings, expect many manual reads. Plan for that time, or use a 2-read agreement before calling it a FAIL.

10. **Cost.** At most $10.62 is fine. But the voice and music rates are "unverified", so asks 1 and 4 show the owner a number nobody has checked against an invoice. Check the rates against the invoice before page 1, or label the numbers "estimate" on the page.

VERDICT: REVISE
TOP FIXES:
1. Match the plan to the code: update the status table and file map (add `swirls_short_run.py` and `swirls_guard`, fix the wrong line-370 claim), and either stop the phase-B build until this panel is done or say plainly that it is already built.
2. Run probe R1 ($0) before building the receipt read-back, and do owner-only `approve` (coordinator task 1) first. Then cut the bridge state machine back to claim, one open row and receipt — it guards $10 but cannot stop the two real dangers.
3. Make G15h and G2w WARN until tests T8 and T10b set real limits, name the whisper tool and check it is installed, and add a test that voice takes A and B really differ.
