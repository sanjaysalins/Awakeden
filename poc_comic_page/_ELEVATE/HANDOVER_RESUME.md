# ELEVATE (Comic lane) - handover + resume. Written 2026-11-08 night.

Lane: comic (Higgsfield). Worker brief: `F:\slk\PycharmProjects\JesusInTheBible\coord\LANE_COMIC.md`.
**Spend so far: $0.** Nothing paid. Every paid step needs a quoted price + the owner's own yes.
Owner is dyslexic: short plain words, ONE question at the end, full absolute paths + `file:///` links, NEVER auto-open anything.

## Goal (owner, 2026-11-08)
"Deep analysis of how to elevate the graphic comic to a significantly better version, build a pipeline, do a bake-off."
Then: "Don't fix current (Mockers). Work on how to elevate NEW episodes and what a great bake-off looks like."
Budget chosen: **$0 first.**

## What is DONE
1. **Diagnosis** (4 blind seats that SAW frames: Fable, Opus, Sonnet artist, Sonnet viewer) on the finished Mockers film.
   Page: `F:\slk\PycharmProjects\JesusInTheBible\poc_comic_page\_ELEVATE\_ELEVATE_DIAGNOSIS.html`
   Avg scores: art 6.9, layout 4.8, motion 3.9, lettering 3.8, story 5.8, premium 4.6.
   Convergence: 4/4 lettering = subtitles (no tails); 4/4 slideshow (long holds); 3/4 no panel grammar (split panels);
   3/4 story too long / weak open; 3/4 face drift. Split: real clips at peaks (2 yes, Fable no).
   Key finding: our old panels were TEXT-ONLY. Seats must SEE frames.
2. **New-episode recipe (10 steps) + bake-off design.**
   Page: `F:\slk\PycharmProjects\JesusInTheBible\poc_comic_page\_ELEVATE\_NEW_EPISODE_AND_BAKEOFF.html`
   Plan page: `...\_ELEVATE\_ELEVATE_PLAN.html`
3. **Test episodes chosen by AI panel (4 seats):** story = **today_paradise_luke2343** (OWNER PICKED; 2 seat votes, Fable preferred woman_behold).
   Proof = **thirty_pieces_zech11** (3 of 4 seats; NOT yet confirmed by owner; second bake-off not started).
   Design cautions from seats: keep SAME audio in every arm; test one change per arm; blind + random order; hook-first changes WORDS so test it separately.
4. **Bake-off 1 plan page:** `F:\slk\PycharmProjects\JesusInTheBible\poc_comic_page\_ELEVATE\_BAKEOFF_1_TODAY_PARADISE.html`
5. **Pilot (Mockers, $0, evidence only, not fixing):** arms A/B/C in `...\_ELEVATE\arms\A.mp4 B.mp4 C.mp4`, builder `...\_ELEVATE\build_arms.py`. A rebuild with a shorter balloon tail was STOPPED at owner's request.
6. **Bake-off 1 arms BUILT ($0), all 59.07s, same audio (shipped film mix):**
   `...\_ELEVATE\arms\TP_R0.mp4` shipped film (control) - `TP_B0` rebuilt base, old grey pills - `TP_L` +new lettering - `TP_S` +fast cut-ins - `TP_P` +3 split panels - `TP_R1` = L+S+P - `TP_W` Fable's blind wild-card recipe.
   Builder: `...\_ELEVATE\build_tp.py <arm>` (arms R0 B0 L S P R1 W). Fable recipe: `...\_ELEVATE\tp\W_recipe.json`, rationale `...\tp\W_rationale.md`.
   Run: `.venv\Scripts\python.exe poc_comic_page/_ELEVATE/build_tp.py <arm>` (~5-8 min per arm; run 3 in parallel).
7. **Blind pack BUILT:** `...\_ELEVATE\pack_tp\` = film_A..G.png (24-frame sheets) + `measures.md` (cuts, longest gap, cuts/min).
   Code key (PRIVATE, do NOT show seats): `...\_ELEVATE\KEY_tp_PRIVATE.json`
   = A:S B:B0 C:R1 D:W E:L F:R0 G:P.
   Measures: cuts A31 B18 C26 D28 E18 F21 G17; longest still-hold (s) A2.8 B5.0 C5.0 D3.5 E5.0 F7.9 G5.0.

## NEXT (do in this order)
1. **Send blind judge seats** (Fable + Opus + Sonnet artist + Sonnet newcomer viewer; add Codex/Grok only if they can read images). Each Reads
   `pack_tp\film_A..G.png`, `pack_tp\measures.md`, and `batches\cluster_01_cross\today_paradise_luke2343\narration.md`. NO key, NO arm names, NO my notes.
   Ask: score 0-10 each film on stop / finish / feel / share / premium / who-what-why; rank all 7; pick best of each pair (best two vs each other);
   top 3 reasons; "which ONE change made the difference". Note seats judge FRAMES only (not motion): motion shown by the measures.
2. Unblind with the key. Compute per-lever gain: L vs B0 (lettering), S vs B0 (rhythm), P vs B0 (split), R1 vs B0 (all), W vs R1 (wild card), R0 vs B0.
   Apply the pre-set rule: adopt a lever only if most seats rate it +1.0 or more.
3. ONE simple HTML result page (big images, short words, before/after scores, "still weak" list, my pick + ONE question). Never auto-open.
4. Paid rungs, ONLY after owner sees step 3, each with a real quote + owner yes: R3 cast sheets + cut-in plates; R4 three real clips (thief plea, Jesus turns, paradise).
5. Confirm 2nd episode (`thirty_pieces_zech11`) with owner, then repeat on it. A win must repeat on 2 episodes.
6. Seed viewers (5-10 real people), report odds with error bars. Simulated seats are not real viewers.

## Known flaws in the pilot (not bugs to chase)
- Panels judge FRAMES; motion is only visible through the measures. Say so in the result page.
- R1 split-panel windows show a stamp that repeats the caption text ("SAME NAILS. SAME HILL.") - minor redundancy.
- Balloon tail anchors are estimated crop positions; some tails may be slightly off a mouth.
- R0 (shipped film) was made by the livingpage engine; B0/L/S/P/R1 are my rebuild with old-style grey pills. Compare levers against B0, show R0 as the real baseline.
- Hook-first WORDS not tested (audio fixed). Separate later test.

## Rules to keep
- Lane folders only: `poc_comic_page/`, `poc_living_sketchbook/`, `batches/`. Never edit coordinator-only files (RESUME.md, STATE.md, tracker, pipeline/, etc.). Never git add/commit.
- Piece `comic_elevate` is NOT on the board (only the coordinator can add). Notes go via `coord.py note comic "..."`.
- Panels are BLIND: independent Fable seat + AI panel, no draft shown, no key. A panel pass never authorizes spend.
- Do not auto-open any file or link.
