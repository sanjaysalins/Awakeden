# Independent review — claude (OK, 98s)

**Adversarial review: Swirls SHORT design v3**

I checked several claims against the code. These hold up: `openart_bridge.submit()` is the single entry point (line 45), `per_turn_synth.py` is under `PythonProject1\jesus\narration\`, the anchor regex in `upload_engine.py` matches `John 1:19-29 (`, alignment defaults to `whisper`, and `build_srt.build()` takes no `force` argument today and calls `align(force=True)`. The plan's "facts verified" table is mostly honest. The problems are below.

### High: the spend guard is weaker than section 5 claims

1. **The "receipt" is not a receipt.** `after()` trusts `credits_spent` from the response file. The live Claude session servicing the bridge writes that file (`AGENT_BRIDGE.md:102`). Nothing says where the servicer gets the number. It could be copied from the `openart_model_cost` quote or guessed. Reading the balance before and after won't work either, because other sessions spend from the same account (memory `project_unexplained_hf_spend`). So the 110% check and the "sound ON = 114%, caught" claim only test a number the agent wrote itself. **Fix:** say the servicer must take cost from the job's own record (`openart_creation_get` / history id). If it can't, mark the row `UNRESOLVED`. Call this an honest limit in section 11, as the plan already does for ElevenLabs.
2. **A timeout leaves a live request behind.** On `OpenArtBridgeTimeout`, `submit()` raises but never moves `<id>.request.json` out of `gen_requests\`. The default timeout is 3,600 s. A servicer can still run that request later. Credits get spent after the row says `UNRESOLVED`, and a "re-run" sends a second request. **Fix:** on timeout or error, `failed()` moves the request file to a `cancelled\` folder before raising. Add this to test T6.
3. **The guard only covers bridge traffic.** Two things go around it. The poster bake-off (step 11, "2-model bake-off", likely gpt-image-2) is usually done by direct MCP calls. Any servicer can also call `openart_generate_*` directly. "A trim episode cannot send an unguarded request" is only true for code paths. **Fix:** state the rule that every paid OpenArt call for a trim episode goes through `submit()`, poster included. Or put the poster in the ledger as manual `paid` rows.
4. **Owner gates are typed by the agent.** `RUN ok <gate> --note "<owner's words>"` is run by the same session the guard is meant to restrain. That's fine, but section 5 should say it guards code mistakes, not the agent. Today it reads as a hard owner check.

### Medium: the steps contradict themselves

5. **Open rows will stall the run.** "An open row blocks every later paid command." ElevenLabs rows "stay open until confirm." So `align` (inside the voice cap, but a paid call) is blocked until someone confirms the voice row. The same happens to every later step. Test T12's sequence has no `confirm` steps and no `paid voice` or `paid score`. As written, T12 cannot pass, or it passes only because the fake skips the rule. **Fix:** either `align` shares the voice row, or T12 adds explicit `confirm` steps. Define which one.
6. **The word budget and the estimate gate disagree.** Section 1 targets 86-94 words at 2.2 words/s, but 94 / 2.2 = 42.7 s. That fails the 38.0-42.0 estimate before any character-turn pauses are added. The per-unit ranges allow 70 to 106 words in total (31.8-48.2 s). **Fix:** one total-word range that fits 38-42 s once turns are counted, about 80-88 words, and gate it in G1.
7. **The clip is stretched, not scaled.** "1072x1928, scaled to 1080x1920" changes the aspect ratio (0.556 vs 0.5625), about a 1.2% horizontal stretch. That shows on lettering and faces. **Fix:** scale to width 1080 and crop height, or pad. Assert it in G15.
8. **The "older drift" call comes before the test.** Section 0 already blames the 2 red validators on older drift. Step 9.2-1 then "reports, not fixes" them. If the baseline at HEAD is green, the builder's uncommitted tree caused the break, and it must be fixed, not just reported. **Fix:** make the rule depend on what the HEAD baseline shows.
9. **ElevenLabs forced alignment is not proven to work.** The `assembly_align.py` comments say the backend "needs the key's forced_alignment permission." The plan removes the whisper fallback with no check that this key has that permission. **Fix:** one $0 permission probe (or a tiny paid call) in phase C, before the pilot depends on it.
10. **Landing motion is the known defect, but its gate stays WARN.** A single 7-10 s Kling back clip has to keep moving through the 3 s hold. Kling clips often settle near the end, and G15f stays WARN unless T8 tunes it. **Fix:** design rule 8 needs a fallback. Either render the back clip 2 s longer and trim the settled end, or check the true last frame against the frame 3 s before it in clipqc at step 6, before money moves on.

### Low: over-engineering and cost

11. **The build is big next to the risk.** About 13 tests, a guard, provenance hashes and 7 money stops, to protect a pilot whose total cap is about $10.70. Rejecting point 35 ("safety, not polish") is fair for trim and provenance. The full guard machinery (12-hour expiry, unit lists, void flows) is still heavier than the risk. Building it costs more attended time than the credits it protects.
12. **Seven separate money asks is a lot for this owner.** The owner wants simple pages with one pick each. Northstar + stills could be one ask with two caps without losing safety.
13. **Small leftovers.** T12 ends with `status` at step 10, but steps 9-11 never run in the test. Rename it "status reports step 9 next".

VERDICT: REVISE
TOP FIXES:
1. Make the bridge "receipt" real: credits come from OpenArt's job record, not the servicer's own number. On timeout or error, move the request file to a cancelled folder so it can't run late or twice. Route the poster through `submit()` or a `paid` row.
2. Fix the open-row deadlock. Define how `align` and the ElevenLabs rows clear before the next paid step, and add those `confirm` steps to T12 so the dry run checks the real order.
3. Fix the numbers: one total-word range that fits the 38-42 s estimate, a scale-and-crop (not stretch) to 1080x1920, and a $0 probe that the ElevenLabs alignment permission works before whisper is removed.
