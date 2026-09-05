# Independent review — cursor (OK, 98s)

## Findings

### Feasibility / false assumptions

**1. “Same function, same cache file, no new code” hides a backend split (§2, lines 36–41).**  
The plan repeatedly says alignment is “ElevenLabs forced alignment,” but `pipeline/assembly_align.py` defaults to **`ASSEMBLY_ALIGN_BACKEND=whisper`**, not ElevenLabs. Only `build_srt.py` forces ElevenLabs — and it calls `align(..., force=True)`, which **overwrites** the cache:

```14:14:poc_living_water_ink_style_test/build_srt.py
os.environ["ASSEMBLY_ALIGN_BACKEND"] = "elevenlabs"
```

```54:54:poc_living_water_ink_style_test/build_srt.py
    words = align(folder, force=True)
```

If score design runs `align()` early with defaults, you get whisper timestamps; SRT rebuilds with ElevenLabs later. Score boundaries and captions can diverge by hundreds of ms. The plan never specifies which backend score design must use or that `force=True` is required after re-synth.

**2. “Today the only caller is `build_srt.py`” is wrong globally (§2, line 38).**  
True for swirls today, but `align()` is also used elsewhere (e.g. `poc_comic_page/rung0_pageplan.py`). More importantly: **nothing in the swirls pipeline invokes `align()` after `/voice`**. The plan adds a stage but no hook in `swirls_episode.py` / production docs — it’s still a manual step.

**3. The `composition_plan` / `music_v2` path is greenfield here (§6.7, §7).**  
Repo grep finds **zero** runnable `composition_plan` or `music_v2` callers. `STATE.md` already recorded this:

> “the `composition_plan` structured format a memory described turned out to be **stale/never actually built anywhere runnable**”

The plan revives that path. Section 7’s smoke test is right to gate it — but §10 already authored a full 12-chunk ep11 plan **before** that gate. That’s building the cathedral before checking the API door opens.

**4. §4 claim “Nothing downstream changes” is false (line 70).**  
§8.1 explicitly shows the assembler still cuts by word proportion:

```257:257:poc_living_water_ink_style_test/swirls_assemble.py
        slot = narration_len * u.words / total_words
```

A real-timed score **without** a matching assembler change makes sync **worse**, not better. Today score and video are both wrong vs speech, but wrong **together** (both derived from the same word weights — see ep11 `generate_score_piano.py` docstring lines 13–16). Real alignment on score only decouples them.

**5. Alignment file shape assumption is wrong (§3 line 54, §6.2).**  
The plan describes `words[]` with space/em-dash tokens. Ep11’s actual cache is ElevenLabs **`characters[]`** at char granularity (`narration.alignment.json` line 2). `_parse_words()` handles it, but any new boundary walker must reuse that parser — not assume a `words[]` schema.

---

### Hidden risks / single points of failure

**6. §8.1 is flagged but not gated — the plan’s main benefit is blocked.**  
The delta table (F10 strings **−1.65s**) is the killer finding. §8.1 says “decide with the user” and “do not silently accept the mismatch,” but §2 pipeline order puts score design **before** stills with no hard dependency on assembler fix. Adopting early score without §8.1 is a regression.

**7. Instrumental enforcement is weaker on the new path (§9.1, §6.7 table).**  
Dropping `force_instrumental` and relying on `negative_styles` + brace-only `text` is acknowledged — and the repo already hit “vocals-injecting music_v2” (`STATE.md` ~4263). One 8s smoke test may not represent 86s / 12-chunk behaviour; a pass on 2 chunks doesn’t de-risk a 12-chunk felt-piano arc.

**8. `context_adherence: high` on every chunk (§6.5) assumes cross-chunk motif continuity the API may not guarantee.**  
Chunks are independent sections. Twelve separately styled sections with high adherence each is not the same as one prose prompt with relative timing cues. No fallback if chunk boundaries audibly reset the motif.

**9. §6.3 3,000 ms minimum is a live footgun.**  
Ep11 front cover: **3,139 ms — 139 ms margin** (§10 table). Any episode with a shorter front/back unit forces merge logic that isn’t implemented yet — only described.

**10. §9.6 early-fade / `reshape_music()` risk is under-weighted.**  
`STATE.md` and `sfx_pilots/add_music.py` treat Eleven early-fade as proven enough to require `reshape_music()`. The plan’s fit step is the same simple afade trim as current `generate_score_piano.py` — not `reshape_music()`. §9.6 says margin “covers a mild case”; for v2 plans that’s an untested assumption.

---

### Over-engineering / premature building

**11. Full ep11 `score_composition_plan.json` (~727 lines) before smoke test (§10 vs §7 step 2).**  
Section 7 says: smoke test first; if vocals/drums appear, **stop, do not scale**. Section 10 is already scaled. That’s premature spend of authoring effort and sets false confidence.

**12. §7.1 “derivation script” doesn’t exist.**  
Lint rules (word-count sum, style caps, `{...}` format, string-gate negatives) are specified but there’s no script in repo. The plan treats verification as built; it isn’t.

**13. §7 step 3 “RMS/novelty sweep” has no tooling.**  
No score chord / strings-entry detector exists in this codebase (unlike pixel-diff motion checks the plan cites). “$0 measurement” still needs new code; without it, duration enforcement and hero-chord placement stay unverified despite being the whole point.

---

### Missing steps / verification gaps

**14. Unit table is a third source of truth (§3 line 55, §6.1).**  
`episode.py` already defines `Unit(..., words=N)` for every page (ep11 lines 1008–1019). The plan adds a separate table with “exact contiguous narration text” + word counts. §7.1 lint checks counts sum to total — **not** that walking those counts through alignment yields the claimed unit text, or that counts match `EpisodeManifest`. An off-by-one in one unit shifts every subsequent boundary silently.

**15. §6.2 boundary rule is internally inconsistent in the worked example.**  
Rule: “Chunk k starts at the START of unit k’s first spoken word” except chunk 1 at 0.000. Derivation shows chunk 1 `first_word_start_s: 0.179` but `chunk_start_s: 0.0` — fine for chunk 1, but the doc never defines chunk **end** for non-final units (implicit: next unit’s first-word start). That gap will bite when implementing merge-for-&lt;3s logic.

**16. Re-synth invalidation is incomplete (§2 lines 43–46).**  
SHA256 on `narration.mp3` / `.alignment.json` is good, but no step says **`align(..., force=True)` must run whenever mp3 changes** before boundary derivation. `RESUME.md` already documents stale-alignment gotchas after re-synth; this plan doesn’t wire that in.

**17. §8.2 “Fable design brief receives score arc” has no acceptance criteria.**  
What changes in stills/animation if F09 is `resolution` at 55.32s vs 57.90s? Left as “open design question” — so moving score before visuals may not change visual output at all until `/swirls-of-life` Step 0 answers it.

---

### Reuse gaps

**18. Duplicates per-episode score scripts without a shared runner.**  
Six+ `generate_score_piano.py` copies exist; plan adds `score_composition_plan.json` but doesn’t say whether one shared `generate_score_from_plan.py` replaces them or every episode keeps its own script. Likely more duplication.

**19. Ignores existing alignment-aware patterns.**  
`northstar_shortform/build_fills.py` already consumes alignment JSON for timing-aware fill decisions. Plan doesn’t reference it as prior art for “real time, not word proportion.”

**20. `/swirls-of-life` SKILL still contradicts §5 (lines 71–77 of SKILL.md).**  
SKILL still mandates `SCORE_STYLE_BANK.md` (Jacob’s Ladder dream-trance/groove). Plan §5 says that bank is superseded for mainline. Pipeline docs aren’t aligned; an agent following SKILL will fight this plan.

---

### Cost / spend justification

**21. Early score spend has higher rework exposure.**  
Score moves before stills/animation (§2). If visuals later need narration trim/re-synth (even minor), score plan goes stale (§2 lines 43–46) → full re-render (~$1+ per ep11-length piece). Current late-score avoids paying until the cut length is frozen.

**22. Billing for `composition_plan` / `music_v2` unconfirmed (§9.5).**  
Assumed per-second like prompt route. 12 chunks vs one prompt — same duration, but failed renders / retries from chunk-semantics issues (§9.4) could multiply cost. No `--yes` / ledger hook specified unlike `sfx_pilots/add_music.py`.

**23. Net value unclear until §8.1 ships.**  
Paying for precision timing that video ignores (up to 1.7s on ep11 strings) isn’t justified. The plan correctly identifies this but doesn’t treat it as a blocking dependency — that’s a cost/logic error, not just a footnote.

---

### What the plan gets right (for balance)

- §9 open questions are honest (vocals, duration enforcement, hero vs “Arise”, billing).
- §8.1 mismatch table is real and measured — best part of the doc.
- Provenance hashing and HUMAN GATE 1 placement are sound.
- Reusing `score_piano.mp3` / `ScoreVariant` contract avoids assembly churn.

---

VERDICT: REVISE  
TOP FIXES:  
1. Make §8.1 assembler boundary sync a **hard prerequisite** — do not adopt early score until `swirls_assemble.py` reads the same unit timings (`derivation.chunks` or shared `unit_timing.json`); otherwise real alignment makes A/V sync worse.  
2. Pin alignment backend explicitly in the new stage (`ASSEMBLY_ALIGN_BACKEND=elevenlabs` to match `build_srt.py`, plus `force=True` after any re-synth) — the default whisper path silently invalidates the plan’s “real timing” claim.  
3. Reorder execution: **§7 step 2 smoke test first**, then minimal 2-chunk render tooling — not a full ep11 plan — before any standing-process adoption; repo history already says `composition_plan` was never runnable here.
