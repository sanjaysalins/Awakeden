# Independent review — claude (OK, 142s)

I verified the plan against the actual codebase. Findings below cite real files.

## Feasibility — the consumption tool the plan leans on does not exist

**Red-team #6 is false.** It claims: *"enhance.py trims to any window and picks the in-point, so a 2–3 min Suno track gives several usable 60s sections."* The only `enhance.py` in the repo is `C:\Users\sanjay\PycharmProjects\JesusInTheBible\11labs-testing\enhance.py` — its own docstring says it's a one-off test that scores an **ElevenLabs Music** bed under the **Well (John 4)** clip. It is not a reusable Suno trimmer, and it is not in `music_library/`. I grepped `music_library/*.py` for `trim|window|duck|sidechain|in_point|place` — **zero matches** except one docstring sentence. `music_library/index.json` is `[]` (nothing ingested). So you'd generate 40 audio files before the thing that places them under narration exists. That's building the warehouse before the forklift.

## Over-engineering — this violates the user's own LOCKED test-gate rule

Memory `feedback-test-gate-before-batch`: *lock the look on 1–2 paid test scenes BEFORE the full batch; ~$18–20 of Isaiah 53 was avoidable redo.* This plan batches all 20 prompts (×2 takes = 40 files) with **zero Suno beds validated end-to-end** (generate → trim → sidechain-duck → under a real narration). The same rule that governs stills and animation applies to beds. Generate 2 (e.g. `sacred_grace_rise` + `lament_suffering_cello`), prove the trim+duck loop, then batch the other 18.

## Spend not quoted — breaks the hard spend rule

Memories `feedback-ask-before-spending` and `feedback-veed-io-spend-control` ("every generation cost shown in the boldest/loudest colour", fail-closed `--yes` gate). The plan's only cost line is *"Generate once on the paid Suno plan"* and a License footer. No credit count, no gate. 20 prompts × "let it run 2–3 min" × 2 takes consumes real subscription credits — state the number, even if "covered by flat plan."

## Unproven provider pivot, no fallback

Every "proven on Well" claim borrows credibility from a **different tool**: red-team #2 (two-music clash) and #7 (loudness) both happened with ElevenLabs / `sound_library` beds, **not Suno**. Suno is end-to-end unvalidated here, and the plan documents no fallback to the working Eleven path if a batch comes back unusable. (Your own prior panel `music_library/_independent_review/20260606-173432/cursor.md:63` flagged the same single-point-of-failure — it has not been addressed in this artifact.)

## Suno prompt craft

- **Arc placement, not just length.** *"let it run ~2–3 min so there's a full arc to trim from"* — Suno's Style box controls neither duration nor *where* the swell lands. For the arc beds (`sacred_grace_rise` *"slowly swells to a climax"*, `awe_revelation_build` *"rising to a peak"*) you cannot guarantee the peak sits inside a trimmable 59s window. Static pads (`glory_*`) are safe; the plan only mitigates length (#6), never climax placement — the actual risk on the flagship beds.
- **Verify "v5.5" is a real Suno version.** Every prompt header and the title say *Suno v5.5*. Confirm that string exists before it's stamped into 20 filenames and `license` records.
- Negatives (#4) and stealth-vocals (#5) self-identified correctly; mitigations are reasonable.

## Coverage gap — no neutral / exposition bed

All 10 moods are emotionally loaded. The Five-Beat **Point** beat (plain exposition) and the long-form **connective narration stretches** (6–8 min needs low-key "under-teaching wallpaper") have nothing assigned. Closest is `sacred_intimate_piano`, but that's devotional, not neutral. Red-team #8 lists considered gaps (childlike, courtroom, worship-vocal) but misses this obvious one.

## Two sources of truth already drifting

`ingest.py` reads tags/prompts from `music_library/_specs.py`, **not** from `CATALOGUE.md` (the plan says *"it reads this catalogue for tags"* — technically the parallel mirror). They've **already drifted**: CATALOGUE #7 says *"steadily rising **tension** to an awe-struck peak"*; `_specs.py awe_revelation_build` dropped "tension." Pick one source or have `ingest.py` assert they match.

## What's genuinely good (so REVISE, not FAIL)

Doctrine handling is correct and well-guarded: red-team #1 bans `tension_*` from Conviction/Landing — fully consistent with grace-anchored conviction. The melody-vs-pad layering rule (#2, only `glory_*` drones layer) is sound and the prompts back it (melody-free). Mood separation (#3) is real and defensible. The 20-slug `_specs.py` mirror, `ingest.py`, and naming convention are already built and coherent.

VERDICT: REVISE
TOP FIXES:
1. Build (or name honestly as TODO) the reusable Suno trim + sidechain-duck consumption tool inside `music_library/` before batching — red-team #6 currently points to a Well-specific ElevenLabs script that can't do this.
2. Test-gate 2 beds end-to-end (generate→trim→duck under a real narration) and quote the Suno credit spend with the fail-closed gate, per the user's locked test-gate + ask-before-spending rules, before generating the remaining 18.
3. Address arc-placement risk on the swell beds and add a neutral/exposition bed for the Point beat + long-form connective stretches; collapse the CATALOGUE.md ↔ `_specs.py` drift to one source of truth.
