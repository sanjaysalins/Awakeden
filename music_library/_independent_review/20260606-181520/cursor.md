# Independent review — cursor (OK, 51s)

## Independent adversarial review — Music Library Catalogue (round 2)

Round 2 genuinely fixes several round-1 lies and gaps. The `enhance.py` false-trim claim is gone, doctrine is in data, LUFS is measured, pilot-first is stated, boundaries are named, and `_specs.py` → `CATALOGUE.md` is real. **That is not the same as being shippable.** The plan still describes a library the engine cannot use, and the hardest architectural question — one bed vs five beats — is still unanswered.

---

### What round 1 fixed (credit where due)

| Round-1 finding | Round-2 status |
|---|---|
| False `enhance.py` in-point trim | **Fixed** — `⛔ NOT built yet: the beat-aligned music placer` + `trims from t=0 only` |
| Doctrine prose-only | **Fixed in code** — `BEAT_ALLOWED` + `find_for_beat` in `_specs.py` / `music_library.py` |
| Missing Point beat | **Fixed** — `neutral_teaching_warm` / `neutral_teaching_low` + Point in matrix |
| Batch-20 before proof | **Mostly fixed** — `Staged plan (test-gate discipline — don't batch all 20 first)` + 4 ⭐PILOT slugs |
| Wrong loudness metric | **Fixed** — `ingest measures real LUFS + dBFS` matches `loudnorm=print_format=json` in `ingest.py` |
| Dual maintenance | **Fixed** — `AUTO-GENERATED from _specs.py` |
| `lonely_*` on Conviction | **Fixed** — Conviction row excludes `lonely` |
| music vs sound boundary | **Partially fixed** — prose rule at `Don't stack a glory_* pad AND the choir SFX` |

---

### Feasibility vs real codebase / tools

**1. The “✅ Built” checklist overstates integration.**

The Status block claims:

> `✅ Built: library API, specs, ingest (LUFS + dBFS), audition/approve gate, doctrine-aware selection (find_for_beat).`

`find_for_beat` exists, but **nothing in `cli_assemble.py`, `cli_pipeline.py`, or `pipeline/assembly_*.py` imports `MusicLibrary`**. The selector is a dead API until a mix stage calls it. “Built” here means “Python module exists,” not “engine can use it.”

**2. `index.json` is still `[]`.**

The entire workflow — ingest → audition → selection — is unvalidated on a single real Suno take. The plan is still paper atop scaffolding.

**3. The Phase-1 pilot prerequisite is mislabeled in step 1.**

Staged plan step 1:

> `Build + prove the generate→trim→align→duck loop on one real short (John 4).`

“Duck” is proven in `11labs-testing/enhance.py` (`sidechaincompress` in the mix filtergraph). **Trim + align to CTA timestamp is not.** Bundling all four under one “loop” obscures that the pilot’s actual deliverable is a **new Suno placer script** — not Suno generation + `approve.py`. Generating 4×2=8 pilot MP3s before that script exists repeats round-1’s “warehouse before forklift” risk, just smaller.

**4. `enhance.py` is correctly demoted but still misread as partial reuse.**

The artifact says the Well POC `is not a reusable Suno placer` — accurate. But the pilot does not name what gets forked: the **ffmpeg sidechain graph** from `enhance.py`, or a greenfield `music_library/placer.py`. Without that decision, “prove the loop” has no implementation target.

**5. `music_library.py` docstring still promises downstream behavior that does not exist.**

```17:19:music_library/music_library.py
Selection discipline: pick by emotional ARC, not just genre. Each clip's narration is
forced-aligned, so the chosen track's natural build can be timed (in-point) to land on
the gospel pivot, then trimmed + ducked under the voice downstream.
```

That reads like built plumbing. It is the same class of overclaim round 1 flagged in `CATALOGUE.md`.

---

### Hidden risks, false assumptions, single points of failure

**6. The core five-beat / one-bed contradiction is unresolved — and round 2 makes it worse.**

Two locked rules collide:

- `One melodic bed per clip otherwise (the 'two music' clash).`
- `find_for_beat` — per-beat, doctrine-safe selection (implies beat-level picking)

A 60s short has five beats with different intents (`hook` 0–8s ache → `landing` 52–60s grace per `data/structures.json`). The pilot picks **four different moods** (`lonely_searching`, `neutral_teaching_warm`, `sacred_grace_rise`, `glory_holy_stillness`). The plan never states whether John 4 uses:
- one bed for 59s with magical in-point alignment,
- beat-boundary cuts + crossfades,
- or hook-only lonely then swap at 8s.

Without that, the pilot cannot pass or fail — there is no acceptance criterion.

**7. `neutral_teaching_warm` on Conviction/Landing is doctrine-safe but arc-hostile.**

Per-beat matrix allows `neutral` on `conviction` and `landing`. Catalogue tags:

> `neutral_teaching_warm` · beats: `hook, point, proof, conviction, landing`

An “unobtrusive… steady understated bed that leaves room for a speaking voice” under the **Conviction** beat (40–52s, “holy tension… pierces”) and **Landing** CTA is likely emotionally flat. `find_for_beat("landing", …)` can legally return neutral and undermine the grace climax the catalogue optimizes for with `sacred_grace_rise` / `triumphant_resurrection`.

**8. Proof-beat intelligibility risk is unaddressed.**

`awe_revelation_build` is still tagged for `proof` (18–40s), which is **KJV quote at NORMAL pace** per `structures.json`. Prompt:

> `building orchestral strings layered with a soft wordless choir pad, mounting wonder and revelation, steadily rising to an awe-struck peak`

`veed_io/aligner.py` already documents that music beds cause STT word drops. The plan has no duck-level gate, no faster_whisper recovery test, no “music off during verbatim KJV” rule. This is a production blocker for captioned shorts.

**9. Layering rule is data, not enforcement.**

`LAYERABLE_MOODS = {"glory"}` exists in `_specs.py`, and the catalogue says:

> `only glory_* beds (melody-free, rhythm-free) may sit UNDER a melodic bed`

No API prevents stacking two melodic beds, or `glory_light_descending` (prompt includes `glassy bells` and `soft high strings` — likely melodic) under another melodic bed. “Melody-free” is asserted, never measured.

**10. Audition gate is human-only; `has_vocals=False` is still a lie at ingest.**

`ingest.py` line 91 hardcodes `has_vocals=False` for every take. Round-1’s stealth “aah” vocal risk is shifted to `approve.py --reject` with no structured QC checklist, no STT test, no drum-detection. `Every track stays status=pending until a human audition approves` is better than nothing, but not a verification gate comparable to image Vision audit.

**11. ≤20 final beds vs 40 ingestible takes.**

`Count: 20 prompts × 2 takes = 40 raw files → audition → keep the best (≤20 final beds)` — but ingest registers **each take as its own slug** (`sacred_grace_rise_a`, `_b`). Nothing rejects the loser automatically. Approving both `_a` and `_b` yields 40 selectable entries, not ≤20. The cap is aspirational, not enforced.

**12. Suno single-vendor risk with no batch fallback.**

`Suno v5.5` + `Instrumental = ON` across 20 prompts, with known failures (`tension_dread_pulse`: `sparse low percussion pulse`; `triumphant_resurrection`: `light timpani swells`). `Eleven Music remains the fallback` is prose — no routing rule, no per-mood “regenerate on Suno fail → Eleven” workflow.

**13. License is more honest but still unverified.**

`Suno paid plan grants commercial USE but not copyright protection` is an improvement. Still no ToS clause, no export-rights check, no per-track artifact beyond `approve.py --url`. “Commercial rights” in the opening paragraph is still an assumption, not evidence.

---

### Over-engineering / premature building

**14. 18 non-pilot prompts are fully specified before any Suno take is heard.**

Staged plan says batch later, but the artifact still ships complete prompts for all 20 beds (`urgent_call_rising`, `lament_forsaken`, etc.). That is fine as a design doc, but the `Count: … 40 raw files` header and full catalogue invite scope creep the moment pilot “looks good.” No code enforces `PILOT_SLUGS` — `ingest.py` accepts any matching slug.

**15. Long-form is named but not planned.**

Opening line: `60s shorts + 6–8 min long-form`. No movement-level matrix (Isaiah 53 M1–M7, Psalm 22, etc.). `longform/SOUNDSTAGE_SPEC.md` designs **ElevenLabs SFX ambience**, not Suno melodic beds. The plan does not say whether long-form reuses the same beds, a subset, or a different stack. Round-1 gap #16 is **not** resolved.

---

### Missing steps, edge cases, verification gaps

**16. No pilot acceptance criteria.**

What proves the John 4 loop?
- LUFS after duck?
- STT word recovery on Proof beat?
- Subjective listen only?
- A/B vs Eleven Well score?

Without metrics, step 2 (`Batch the rest only after the loop is proven`) is unenforceable.

**17. No beat-boundary mix strategy.**

Missing: cut music at beat boundaries, crossfade between beds, duck-to-silence during KJV, or “music only on Hook + Landing.” This is the assembly design gap round 1 flagged; round 2 added `find_for_beat` but did not close it.

**18. `use_cases` in `_specs.py` drift from beat IDs.**

`use_cases` still uses loose strings (`"landing"`, `"cta"`, `"grace-climax"`, `"the-ache"`) while selection uses `hook|point|proof|conviction|landing`. `find_for_beat` ignores `use_cases` entirely — only `mood` + tags. Slug-level intent (e.g. `sacred_grace_rise` as landing climax vs `sacred_intimate_piano` as quiet conviction) is not selectable.

**19. Boundary vs `sound_library` is advisory only.**

The Well `enhance.py` PLAN still stacks `GEN:music.mp3` + `heavenly_choir_soft.mp3` on landing. The new rule `Don't stack a glory_* pad AND the choir SFX` is not wired into any mixer. Existing enhanced cuts can violate it today.

---

### Reuse / duplication

**20. Ducking is duplicated conceptually, not reused.**

Sidechain logic lives in `11labs-testing/enhance.py`, not `music_library/`. The plan does not say “extract `mix()` filtergraph into shared module.” Risk of a second, divergent duck implementation during Phase-1.

**21. Choir/pad overlap remains.**

`awe_revelation_build` (`soft wordless choir pad`) vs `sound_library`’s `heavenly_choir_soft`. Boundary prose helps; enforcement does not.

**22. Suno vs Eleven decision matrix is still manual.**

`Use a bespoke Eleven Music score only when a clip needs a custom-timed climax` — no `if beat==landing and no_approved_match: eleven` rule. Operator judgment only.

---

### Cost / spend

**23. Pilot spend is reasonable; full-catalog spend is still front-loaded in the doc.**

4 beds × 2 takes = 8 generations is aligned with test-gate discipline. But the prominent `40 raw files` line and 16 fully-written non-pilot prompts create pressure to batch before proof. No quoted Suno credit/time per take, no “≥N of 8 pilots must pass QC before batch” gate.

**24. Eleven fallback cost is unbounded.**

If 30–40% of Suno takes fail (drums, stealth vocals, wrong arc), effective cost is regen time + possible Eleven bespoke scores — neither quantified.

---

### Suno prompt craft (remaining)

**25. Percussion prompts contradict “no drums” spine.**

`tension_dread_pulse`: `sparse low percussion pulse` · `triumphant_resurrection`: `light timpani swells` · `urgent_journey_drive`: `taut frame-drum pulse`. Fine for narrative-only hooks if approved, but high QC rejection rate — not budgeted.

**26. Middle-Eastern aesthetic spine from round 1 is gone.**

Only `sacred_grace_rise` (duduk) and `lonely_searching` (duduk/ney) carry it. Most beds are generic `cinematic orchestral`. May not sound like one catalogue family across episodes.

---

### Bottom line

Round 2 is a **materially more honest** plan. It does **not** resolve the execution blockers: zero production consumer, zero ingested tracks, no beat-aligned placer spec, no five-beat mix architecture, no STT/intelligibility gate, no long-form mapping. The pilot cannot succeed on its stated terms until those are designed — and step 1 should say “build placer first,” not “generate 4 beds first.”

VERDICT: REVISE
TOP FIXES:
1. **Define and spec the beat-aligned placer before any Suno spend** — explicit deliverable (e.g. `music_library/placer.py`): in-point selection from `build_timeline`/word timestamps, trim window, reuse `enhance.py` sidechain graph; fork nothing from the Eleven-only Well path for trim logic.
2. **Resolve one-bed vs five-beat architecture with acceptance criteria** — document whether shorts use one 59s bed, per-beat swaps/crossfades, or music-off during Proof KJV; add STT word-recovery test under duck; ban or deprioritize `neutral` on Conviction/Landing in `BEAT_ALLOWED` if the arc matters.
3. **Wire a minimal production consumer before catalogue expansion** — e.g. extend `11labs-testing/enhance.py` or `cli_assemble` to call `find_for_beat` + placer on John 4; enforce `PILOT_SLUGS`-only ingest until pilot passes; auto-reject duplicate `_a/_b` so ≤20 approved beds is real.
