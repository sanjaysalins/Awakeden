# PLAN v4 — Fix every short (element-gate sweep + reuse-rebuild) + a reusable music library

> **Status: v4 (2026-06-18) after TWO review rounds** (round 1: 2 internal + 4-CLI panel = 6×
> REVISE; round 2: 2 internal verifiers). v1's headline claims were wrong; this folds every
> convergent finding. Reviews: `v2/_independent_review/20260618-132326/`.
>
> **Round-2 design resolution (user-approved):** the music collection is **ONE collection with a
> `source="eleven"` lane-filter**, storing **RECIPES (regenerate-on-demand), not baked mp3s** (the
> 8 scores are pivot-timed one-offs that can't be reused as audio), with a **thin Eleven schema**
> (don't inherit the Suno `MusicEntry`), a **shared doctrine gate**, and an optional Eleven-only
> browse view. Small fixes folded: write-once backups, JIT element-gate (default-PASS on missing
> sidecar, never auto-exclude), a `queue_state.json` for park-and-proceed, caption recovery over
> the spoken region only.
>
> **The two corrections that change everything:**
> 1. **It is NOT mostly $0.** Reuse only covers the Christ/cross/landing bookends. The beats that
>    actually fail — scrolls, David, mockers (hook/proof beats) — are topic-SPECIFIC and excluded
>    from cross-episode reuse by the topical-fit rule, so they need **metered renders or exclusion**.
>    Phase-3 music is **~11 metered generations** (the reuse path does not exist yet).
> 2. **The #03 "pattern" is two hardcoded one-off scripts** (`record_sweep.py`, `do_reuse_swap.py`),
>    not reusable tooling. Scaling to 11 shorts requires **building generic tooling FIRST** (Phase 0).

---

## Goal (unchanged)

Every shipped short defect-free; the locked music directive on each; a reusable Eleven-Music
collection so long-form + future shorts pull a score instead of regenerating.

## Honest cost reality (the corrected model)

| Item | Real cost |
|---|---|
| Phase 0 tooling | $0 (code) |
| Sweep all 11 (agent looks) | $0 in $, but **~140+ agent looks + 11 human review gates** (the real cost is attention) |
| Reuse-rebuild **landing/Christ** defects | $0 (catalogue covers these) |
| Rebuild **hook/proof/writing** defects (scroll/David/mockers) | **METERED render or exclusion** — no clean neutral reuse exists; quoted per short |
| Phase-3 music | **~11 METERED Eleven generations** on first pass (8 exist as files, 3 pilots have none; `add_music` has no reuse path yet) |
| Phase 4 long-form music layer | **a real BUILD** (no music layer exists today), not "wiring" |

→ **No work starts until a per-short coverage table + a spend quote is approved.** (INV: ask-before-spend.)

---

## Phase 0 — BUILD the generic tooling first (was missing; $0)

The #03 run used `_bakeoff/03sweep/record_sweep.py` (hardcoded VERDICTS) + `do_reuse_swap.py`
(hardcoded SWAPS). Generalize into real, parameterized tools:

1. **`pipeline/element_gate_sweep.py <short>`** — auto-extract filmstrips for every clip, run the
   agent element-gate look, write `<short>/_sweep/sweep_review.html` + per-clip `.elementgate.json`
   sidecars. (Today filmstrips are built ad-hoc and `record_sweep` only stores pre-decided verdicts.)
2. **`pipeline/reuse_swap.py <short> --swap scene=<lib_clip> --exclude <n,..>`** — parameterized
   substitute (the #03 logic): backup **WRITE-ONCE** to `_pre_reuse/` (`if not dst.exists()` — never
   overwrite a real original on a second run), copy clip+still, copy coherence verdict,
   declare→reconcile→relock the manifest, element-gate PASS.
3. **Catalogue gating, JIT not mass** (gemini): element-gate a clip **at the moment it's pulled for
   reuse**; cache the `.elementgate.json`. Extend `clip_reuse.is_clean_reusable()` to **gate-THEN-decide**:
   a MISSING element-gate sidecar triggers the JIT look (**default-PASS** until calibrated), it does NOT
   auto-exclude (that would empty the pool — the exact trap `clip_reuse.py`'s own comments warn about).
   Only a recorded FAIL excludes.
4. **Music = recipes, regenerate-on-demand** (NOT loop-to-length — that breaks an arc score's swell).
   `add_music.py --from-recipe`: take a library RECIPE (lens/mood/beat/prompt/directive/model_id),
   regenerate via the Eleven API at the new short's exact length (D+2.5s), mix at the locked directive.
   The baked mp3 is cached provenance, never the reuse source.

## Phase 1 — Sweep + reuse-rebuild all shipped shorts (STRICT NUMERIC #01→#08 → pilots)

1. **Sweep ALL 11 first** (parallelizable agent looks, no bridge contention) → 11 review pages.
2. **User reviews them in 1–2 sittings** (batched, not 11 separate sit-downs) — reject = gate ∪ human.
3. **Per-short coverage table** (beat → clean neutral reuse? y/n) → quote the metered renders/exclusions.
4. **Reuse-rebuild** with the Phase-0 tools. **Unblocking state machine** (gemini): if a short needs a
   fresh render, PARK it and proceed to the next — don't halt the queue.
4b. **ALWAYS PUNCHY ([[feedback-always-punchier]], standing rule):** after removing defects, never
   ship a slow cut — **backfill more clips until punchy** (reuse-first from `clip_library`, element-
   gated; `reuse_swap` creates empty slots; create new only on no fit), then speed the clips to fit.
   Target many distinct moments (≈1 per 3–4s). Fast cuts cover *minor* flaws; HORRIBLE clips are
   deleted, not speed-hidden. (Proven on #02: a 32s hold → 8 clips, max ~9s.)
5. **Re-sweep → DEFINITION OF DONE:** (a) re-sweep clean (gate ∪ user flag empty), (b) music applied
   at the locked directive, (c) re-captioned, word-recovery ≥98% (narration MP3 is frozen by the
   rebuild, so timing holds), (d) old final renamed `_PRE_REUSE.mp4`, (e) `_pre_reuse/` backup verified.
   Rollback = restore from `_pre_reuse/`.

## Phase 2 — The Eleven music collection: ONE collection, source-lane, RECIPES (mostly $0)

- **Count correction: 8 scores exist** (Psalm-22 #01–#08 `assembly/music.mp3`); the 3 pilots have none.
- **DESIGN (resolved 2026-06-18, round-2 review + user):** ONE collection with a **`source="eleven"`
  lane-filter** on the selector — this satisfies every requirement (separate lanes via the filter,
  Eleven as default, its own API-ingest path, its own metadata) with the least code and a single
  doctrine gate (no drift). Suno `music_library/` stays legacy.
- **Reusable unit = the RECIPE, not the baked mp3.** Store `{lens, mood, beat, prompt, directive
  (−8/2.5/duck), model_id}`; the mp3 is cached per-render provenance. Reuse = regenerate at the target
  length via the API. (The 8 existing scores are pivot-timed one-offs — only their recipes are reusable.)
- **Thin Eleven schema** — do NOT inherit the Suno `MusicEntry` (it carries `suno_url`, `_a/_b` take
  siblings, `swell_s` — all Suno-workflow baggage). Give Eleven its own small recipe row; share ONLY the
  doctrine table (`BEAT_ALLOWED` & friends, already pure data in `_specs.py`) via one import.
- **Ingest the 8 as recipes:** this needs a **human lens→(mood,beat) classification** step (the briefs
  in `music_designs.json` carry a *lens* + free-text *why* but NO mood/beat — the doctrine gate needs
  those). Not a lookup — a short doctrinal tagging pass, audition-gated by ear.
- Optional **Eleven-only browse view** (cosmetic) if the user wants to see them as a set.

## Phase 3 — Apply music to every rebuilt cut

- Needs Phase-0 item 4 (`--from-library` + length-match) for reuse to be real.
- First pass is **~11 metered generations** (8 to re-apply on the rebuilt cuts since old finals are
  stale + 3 pilots have none) — **quote + approve**. Each generated score is **banked** to the library
  so the SECOND time (future shorts / long-form) is a true $0 reuse.
- Mix at the LOCKED directive (−8 dB · 2.5 s end-hold · gentle duck 0.12/2.5) → re-caption.
- **Music quota: explicitly UNKNOWN/unmetered $** (Eleven Music bills an invisible quota) — say so, don't fake a number.

## Phase 4 — Long-form music: a REAL BUILD, not "wiring" (scope or defer)

`longform/_soundstage_cinematic.py` is the long-form audio pipeline; **every cue is an explicit
"no music" SFX/ambience bed — there is no music layer**, and `find_for_beat` is consumed by **zero**
production files today. So Phase 4 = *build a music-bed layer* that calls the eleven_music selector.

**DECISION (resolved 2026-06-18): DEFERRED to separate work.** This plan is now Phases 0–3 only
(fix shorts + build the eleven_music collection + apply music). The long-form music-layer build is
filed as its own future task.

---

## Decisions — RESOLVED (2026-06-18)

1. **Music store:** ONE collection + `source="eleven"` lane-filter; store RECIPES (regenerate-on-demand),
   not baked mp3s; thin Eleven schema; shared doctrine gate; optional Eleven-only browse view.
2. **Phase 4:** DEFERRED to separate work — this plan is Phases 0–3.
3. **Honest cost:** accepted — Phase-1 hook/proof defects + Phase-3 music are METERED, quoted per short
   via the coverage table BEFORE running. Nothing metered runs without an explicit OK.
4. **Vet:** the user asked to RE-RED-TEAM this revised plan before building (in progress).
5. **Start with Phase 0** (build the generic tooling, $0) once the re-red-team clears.

## Standing guardrails carried in

Reject = gate ∪ human · calibrate before HARD enable · ask-before-spend on every metered step (quote
the coverage table first) · audition every music take by ear · doctrine-gated selection (BEAT_ALLOWED) ·
reuse-first then render/generate · write-once backups · caption last, word-recovery ≥98%.
