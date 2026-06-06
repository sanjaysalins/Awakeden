# Independent review — codex (OK, 125s)

**Findings**

1. **False tool capability.** The claim “`enhance.py` trims to any window and picks the in-point” is not supported. In the repo, `11labs-testing/enhance.py` is a hardcoded Well/John 4 experiment that trims from `0` with `atrim`; it does not detect musical climaxes, keys, phrase boundaries, or CTA timing. This is a plan-breaking assumption for 60s Five-Beat sync.

2. **The “hard usage rule” is not enforceable yet.** “`tension_*` ... banned from the Conviction and Landing beats” and “hard usage rule in the catalogue” are only prose/tags. `MusicLibrary.find()` has no beat-aware guard, no doctrine filter, and no selection code currently consumes `music_library` outside the library itself.

3. **The count is confused.** “Coverage map (10 moods × 2 = 20)” conflicts with “Suno makes 2 versions per prompt” and 20 listed prompts. That is potentially **40 files/takes**, not 20, because every row has `_a` and `_b`. The plan undercounts audition, curation, storage, and rejection work.

4. **“AI-panel-reviewed” is overstated.** The artifact says “A curated, AI-panel-reviewed catalogue,” but the local review folder has one successful Gemini review with `VERDICT: REVISE` and one failed Grok run. That is not a passed panel.

5. **Ingest does not verify the risks the plan identifies.** “reject any take that comes back with a drum kit” and “reject vocal takes” are manual intentions, but `ingest.py` unconditionally registers tracks with `has_vocals=False`. No vocal/drum/midrange/QC status is stored before tracks become selectable.

6. **Loudness claim is imprecise.** “Suno masters hot (~-8 LUFS)... `ingest.py` measures each track” implies LUFS handling, but the current ingest uses ffmpeg `volumedetect` mean/max dB, not integrated LUFS. That is not enough to prove narration-safe loudness or compare beds consistently.

7. **Long-form is underspecified.** The plan targets “60s shorts + 6–8 min long-form,” but the generation instruction is “let it run ~2–3 min.” There is no long-form strategy for looping, movement boundaries, crossfades, clean scripture windows, or whether one bed vs multiple beds should cover a 7-movement episode.

8. **Prompt craft risks remain.** Exact tempo prompts like “~48 bpm,” “~62 bpm,” and “~108 bpm” are weak controls in Suno. Also “soft wordless choir pad” and “glory_* pad/drone ... safe to layer” are not safe by assertion; voice-like pads can collide with narration and doctrine-heavy scripture moments.

9. **Coverage is emotionally lopsided.** The plan acknowledges “sacred / awe / glory / tender” overlap, but most beds cluster around reverent swell, lament, and cinematic tension. Missing are neutral documentary proof beds, sober exegetical/legal gravity that is not dread, and low-motion teaching beds for long-form argument sections.

10. **License note is directionally right but too thin.** Suno’s current help says paid-plan songs are granted commercial use, but also says commercial use does **not guarantee copyright protection**. The plan’s “`license: suno-paid-commercial` recorded per entry” should also record generation date, paid plan/account proof, Suno URL/export ID, and whether the track was generated while subscribed. Sources checked: Suno paid rights and commercial-use help pages: https://help.suno.com/en/articles/9601665 and https://help.suno.com/en/articles/9601985.

VERDICT: REVISE
TOP FIXES:
1. Replace the false `enhance.py` trimming assumption with a real beat-timed music selection/editing/QC step tied to Hook/Proof/Conviction/Landing timestamps.
2. Add enforceable metadata and gates: beat bans, vocal/drum QC, LUFS/SNR checks, audition status, and “approved/rejected” before tracks become selectable.
3. Fix scope/count/cost: decide whether this is 20 final beds or 40 raw takes, add long-form movement rules, and record license provenance per generated track.
