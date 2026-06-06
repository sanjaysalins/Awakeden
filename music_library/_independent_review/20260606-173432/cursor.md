# Independent review — cursor (OK, 56s)

## Independent adversarial review — Music Library Catalogue (plan)

### Feasibility vs. real codebase / tools

**1. The plan claims tooling that does not exist for Suno beds.**

RED-TEAM #6 says: *"`enhance.py` trims to any window and picks the in-point, so a 2–3 min Suno track gives several usable 60s sections."* That is false against the repo. `11labs-testing/enhance.py` generates a **~59s ElevenLabs Music score** (`music_length_ms: int(DUR * 1000)`) and mixes with `atrim=0:{length}` from t=0 — no in-point search, no climax detection, no Suno integration:

```104:116:11labs-testing/enhance.py
    # 1) Eleven Music — instrumental score
    ...
    json={"prompt": MUSIC_PROMPT,
          "music_length_ms": int(DUR * 1000),
          ...
```

RED-TEAM #7 says sidechain ducking is *"proven on Well"* — the Well POC used **metered Eleven Music + `sound_library` SFX**, not `music_library` Suno clips. The README repeats the false claim: *"trim + duck under the voice (same engine as the Well enhance)."*

**2. `music_library` has zero production consumers.**

`MusicLibrary` is only imported by `music_library/ingest.py`. Nothing in `cli_assemble.py`, `cli_pipeline.py`, `pipeline/assembly_*.py`, or long-form soundstage code selects or mixes these beds. The plan describes an engine integration that is not built.

**3. `index.json` is empty (`[]`).**

The catalogue is a paper spec atop scaffolding with **no generated, ingested, or auditioned tracks**. Spending on 20×2 Suno generations before a single hand-mixed pilot is premature (same discipline `longform/SOUNDSTAGE_SPEC.md` already demanded: *"Pilot the experience by hand before building any tooling"*).

**4. Loudness claim uses the wrong metric.**

RED-TEAM #7: *"Suno masters hot (~-8 LUFS)"* and *"`ingest.py` measures each track."* `ingest.py` runs `volumedetect` and stores `mean_volume` / `max_volume` in **dBFS**, not LUFS. Comparing Suno loudness to a −8 LUFS target and planning mix headroom from ingest output is unreliable.

**5. RED-TEAM #5 mitigation is not implemented.**

Ingest hardcodes `has_vocals=False` for every track regardless of content. Stealth "aah" pads called out in RED-TEAM #5 will be registered as vocal-free with no audition gate in the pipeline.

---

### Hidden risks, false assumptions, single points of failure

**6. One bed per 60s clip cannot serve the Gospel Five-Beat arc.**

The plan assumes *"pick by emotional arc, trimmed"* for a whole clip, but also locks *"one melodic bed per clip"* (RED-TEAM #2). A 60s short has five beats with different intents (`data/structures.json`: Hook ache → Point claim → Proof KJV quote → Conviction pierce → Landing grace). The coverage map assigns different moods to different beats (`lonely_searching` for **hook**, `awe_revelation_build` for **proof**, `sacred_grace_rise` for **landing/CTA**), yet selection is **one track for ~59s**. Arbitrary trimming cannot make a single 3-minute Suno arc hit Hook loneliness at ~0s, Proof swell at ~18s, and Landing grace climax at ~52s unless the track was composed to that exact timeline — which these generic mood prompts are not.

**7. Proof-beat music fights the most important audio.**

`awe_revelation_build` is tagged for the **proof** beat (18–40s), which carries the **KJV quote at NORMAL pace** per `structures.json`. A *"steadily rising tension to an awe-struck peak"* with *"soft wordless choir pad"* under 22s of verbatim Scripture is a intelligibility risk. The repo already documents that music beds break word alignment (`veed_io/aligner.py`: *"faster_whisper's word_timestamps drop words under a music bed"*). The plan has no STT/intelligibility gate for music-under-voice.

**8. Doctrinal usage rule is internally inconsistent.**

RED-TEAM #1 bans `tension_*` from Conviction/Landing but explicitly allows **`lonely_*` on Conviction**. Lonely prompts are *"hollow and searching, unresolved, aching loneliness"* (#3) and *"bleak and barren… isolation"* (#4). That is unresolved ache under the conviction beat, which `structures.json` defines as *"grace-anchored… NO fear-selling, NO manufactured pressure."* Allowing lonely beds on conviction is the same class of risk RED-TEAM #1 tries to block for tension — just with different adjectives.

**9. `urgent_*` is a pressure vector with no ban.**

`urgent_call_rising` asks for *"mounting resolve to a decisive hit"* (#20). Unlike `tension_*`, urgent tracks have **no narrative-only / beat-ban rule**. Mis-assigned to Conviction or Landing, they violate the locked grace framing as easily as dread pulses.

**10. Usage rules are markdown-only — not enforceable.**

`tension_*` gets a `narrative-only` tag in `_specs.py`, but `MusicLibrary.find()` has no beat-aware filter, no `conviction-safe` exclusion logic, and no connection to `gospel-five-beat` beat IDs. RED-TEAM #1 says *"hard usage rule in the catalogue, not a suggestion"* — it is still only a suggestion in code.

**11. Single vendor, single generation pass.**

The entire library depends on Suno v5.5 honoring *"Instrumental = ON"* and aesthetic negatives across 20 prompts. RED-TEAM #4 admits *"Suno ignores negatives"* for drums. One bad batch wastes the catalogue spend; there is no fallback to the already-working Eleven Music path in `11labs-testing/enhance.py`.

**12. "AI-panel-reviewed" is asserted before evidence.**

Opening line: *"A curated, AI-panel-reviewed catalogue"* — but `index.json` is empty, no tracks have been auditioned, and this review is the panel pass. The claim is premature.

---

### Over-engineering / build-before-proof

**13. Full 20-track catalogue + dual-file metadata before validation.**

Built: `music_library.py` API, `_specs.py` (106 lines mirroring prompts), `ingest.py`, `CATALOGUE.md`. Not built: beat-aligned trim, mix integration, vocal/drum rejection, listen gate. This is infrastructure for a library that has not proven one usable bed on one real short.

**14. 20 tracks is overspecified for an unproven workflow.**

RED-TEAM #8 defers expansion with *"expand later from real usage"* — but the plan still commits to generating all 20 now. Two near-duplicate pairs (`triumphant_resurrection` / `triumphant_kingdom_brass`; `sacred_grace_rise` / `tender_dawn_hope` / `awe_revelation_build` all "build to climax") multiply Suno spend before knowing whether 6–8 core beds cover 80% of clips.

---

### Missing steps, edge cases, verification gaps

**15. No **Point** beat coverage.**

The coverage map jumps from Hook (`lonely_*`) to Proof (`awe_*`) with nothing for **Point** (8–18s: *"one unbreakable biblical claim… stated plainly"*). Point is not a hook ache and not yet proof swell — the map leaves a structural hole.

**16. No 7-movement long-form mapping.**

The brief requires long-form (Isaiah 53's Report → Scandal → Exchange → … → Arm of the LORD). The catalogue only tags `isaiah-53`, `psalm-22`, etc. as loose `use_cases` — no movement-level bed plan. Meanwhile `longform/SOUNDSTAGE_SPEC.md` designs beds as **ElevenLabs SFX ambience** (wind, thunder, nails), not Suno melodic scores, and is itself red-teamed as *"DON'T BUILD THIS YET."* The plan does not say how `music_library` relates to that spec.

**17. `glory_*` "layerable / no melody" is not verified.**

#15 claims *"pad/drone, **safe to layer**"*, but #16 includes *"soft high strings"* and *"glassy bells"* — likely melodic content. Layering two beds that both occupy midrange will mud the narration band; there is no key-compatibility or spectral-gap check.

**18. No crossfade / multi-segment strategy for shorts.**

If one bed cannot cover five beats, the plan never specifies whether to cut music at beat boundaries, crossfade between beds, or duck to silence for KJV quotes. That is a core assembly design gap.

**19. No listen/audit gate.**

Unlike images (Vision audit) or narration (independent red-team), the plan ends at ingest + manual *"audition; delete the weaker take."* No RMS-under-voice check, no STT recovery test, no human-listen gate before catalogue lock.

---

### Reuse / duplication

**20. Overlaps `sound_library` without a boundary.**

`heavenly_choir_soft` already lives in `sound_library` as *"soft ethereal wordless choir… gentle holy ambient swell"* and is used on Well landing and Isaiah 53 cinematic mix. `awe_revelation_build` (*"soft wordless choir pad"*) and `glory_*` pads duplicate that role. The plan never defines **music_library vs sound_library**: when is a bed melodic score vs ambient SFX? Using both on one clip revives RED-TEAM #2's *"two music clash"* via a different door.

**21. Duplicates the Eleven Music path without a decision matrix.**

`11labs-testing/enhance.py` already produces per-clip bespoke 59s scores (metered). The plan does not say when to use reusable Suno beds vs bespoke Eleven Music. You risk paying twice for the same function.

**22. `_specs.py` mirrors `CATALOGUE.md` verbatim.**

Dual maintenance surface; any prompt edit must touch two files or ingest tags drift.

---

### Cost / spend justification

**23. Suno spend is unquantified and front-loaded.**

*Generate once on the paid Suno plan* × 20 prompts × 2 takes × *~2–3 min* generations. No credit/time estimate, no acceptance criteria per mood, no "generate 4 pilots first" gate. If 30–40% of takes fail RED-TEAM #4/#5 (drums/vocals), effective cost is higher than stated.

**24. Commercial license is asserted, not verified.**

*`license: suno-paid-commercial`* is recorded by ingest, but the plan cites no Suno ToS clause, export rights check, or per-track license artifact. Treating subscription = perpetual commercial reuse for a YouTube channel is an assumption that should be verified before 20-track investment.

---

### Coverage, redundancy, Suno prompt craft

**25. Middle-Eastern aesthetic spine is inconsistently applied.**

Spine: *"tasteful Middle-Eastern colour (duduk, ney, oud, frame drum)"* — but only ~4/20 prompts name those instruments. Most are generic *"cinematic orchestral"* / *"chamber"*, so the catalogue may not sound like one family.

**26. Numerical BPMs in Suno style prompts are low-signal.**

Prompts like *"~48 bpm"*, *"~108 bpm"* across #1–#20 are unlikely to be honored by Suno; musical terms (*adagio*, *andante*, *allegro*) would be more reliable.

**27. Triumphant pair is redundant.**

#9 *"radiant and victorious, redemptive resurrection swell"* vs #10 *"majestic and kingly, prophecy fulfilled, grand processional"* — same narrative slot (resurrection/kingdom landing). Two slots consumed for one beat type.

**28. Tension #13 contradicts the aesthetic spine while relying on genre framing.**

Spine: *"NO modern drums/EDM"* — but #13 explicitly requests *"sparse low percussion pulse, ~90 bpm"*. RED-TEAM #4 says genre framing does the anti-drum work elsewhere; here percussion is intentional, increasing bleed into wrong beats if mis-tagged.

---

### Summary

The mood taxonomy and ingest scaffolding are directionally sensible, but the plan's **execution story is broken**: it claims proven downstream tooling that does not exist, assumes one trimmed Suno bed can serve a five-beat emotional arc without beat-aligned composition, leaves Point and 7-movement long-form unmapped, duplicates `sound_library` choir/drone assets, and builds a 20-track library before a single pilot mix proves Suno beds work under KJV narration. RED-TEAM mitigations for vocals, drums, and doctrine are prose-only.

VERDICT: REVISE
TOP FIXES:
1. **Do not generate all 20 tracks yet** — hand-mix 3–4 pilot beds on one real short (e.g. John 4) with beat-aligned in-points tied to `pipeline/assembly_timing.build_timeline` / word timestamps; delete the false `enhance.py` trim claim until that script exists.
2. **Publish an explicit beat/movement → mood matrix** (Hook/Point/Proof/Conviction/Landing + M1–M7) and resolve the single-bed-vs-five-beat mismatch; ban `lonely_*` and `urgent_*` from Conviction/Landing in `_specs.py` tags the selector can enforce.
3. **Add verification before catalogue lock** — vocal/drum rejection at ingest (or human gate), STT intelligibility under duck, and a clear boundary vs `sound_library` (`heavenly_choir_soft` etc.) so landing swells don't double-stack.
