# Independent review — codex (OK, 140s)

Round 2 fixes several round-1 defects: the false `enhance.py` claim is gone, `BEAT_ALLOWED` exists, LUFS is now measured, and `_specs.py` really is the generator source. It still has real blockers.

**Findings**

1. The core placer is still handwaved. Step 1 says: “Build + prove the generate→trim→align→duck loop,” and Status says “align a track’s swell to the CTA timestamp.” There is no plan or metadata for finding the swell: no `climax_ms`, `swell_ms`, in-point, loop point, or approved usable window in `MusicEntry`/`approve.py`. LUFS is not enough to identify a musically correct climax.

2. “✅ Built: library API…” overstates engine readiness. `find_for_beat` exists, but the production pipeline does not consume `MusicLibrary`; the library is scaffolding, not integrated. Also `find_for_beat` imports `from _specs import BEAT_ALLOWED`, which is fragile outside scripts that manually alter `sys.path`.

3. The plan contradicts itself on music architecture. It says “One melodic bed per clip,” but also provides a per-beat doctrine matrix and a pilot with four moods. If one bed spans the whole clip, a hook-safe `lonely` bed can still land on the CTA. If beds swap per beat, the “one melodic bed per clip” rule is false.

4. Layering is not actually enforced. The phrase “only `glory_*` beds … may sit UNDER a melodic bed” conflicts with the matrix listing `glory` as a normal selectable mood for proof/conviction/landing. `find_for_beat` can return a `glory` pad as the only bed, and there is no primary-vs-layer selection API.

5. The audition gate is weaker than claimed. “Every track stays `status=pending`” prevents accidental selection, but `ingest.py` still hardcodes `has_vocals=False`, and `approve.py` has no required QC checklist, vocal/drum check, intelligibility check, or required Suno URL. A human can approve a bad or unverifiable take.

6. “≤20 final beds” is aspirational. Ingest registers `_a` and `_b` as separate slugs, and approval can mark both selectable. Nothing enforces “keep the best” per base slug.

7. Pilot-first discipline is not enforced. The plan says “don’t batch all 20 first,” but all 20 prompts are present and `ingest.py` accepts any catalogue slug. `PILOT_SLUGS` exists, but it does not gate ingest or approval.

8. Long-form is still mostly name-dropped. The opening says “60s shorts + 6–8 min long-form,” but there is no looping, movement, crossfade, scripture-window, or multi-bed strategy for a 6–8 minute episode.

9. Proof-beat intelligibility is a missing verification gate. `awe_revelation_build` is allowed on proof and includes “soft wordless choir pad” plus a crescendo. The local aligner explicitly documents word drops under music beds, so the pilot needs an STT/word-recovery gate before batching.

VERDICT: REVISE
TOP FIXES:
1. Define the beat-aligned placer with required metadata: climax/swell timestamp, usable window, trim math, fades, and sidechain behavior.
2. Resolve the one-bed vs per-beat architecture, including separate primary-bed and layer-pad selection.
3. Add enforceable pilot/QC gates: pilot-only ingest until pass, one approved take per slug, required provenance URL, vocal/drum/intelligibility checks.
