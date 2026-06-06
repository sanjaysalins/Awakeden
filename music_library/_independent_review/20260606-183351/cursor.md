# Independent review — cursor (OK, 87s)

## Round-2 fixes that are real in code

Several round-2 findings are genuinely closed in `music_library/`, not just in prose:

- **Doctrine as data:** `BEAT_ALLOWED` in `_specs.py` matches the artifact matrix; `find_for_beat` hard-filters and subtracts `LAYER_ONLY_MOODS` (`music_library.py:108–130`).
- **Glory layer-only:** `glory` is absent from `BEAT_ALLOWED`; `find_layer()` exists (`_specs.py:28–31`, `music_library.py:132–144`). The generated matrix no longer lists `glory` as a primary mood.
- **Pilot ingest gate:** `ingest.py:89–91` skips non-`PILOT_SLUGS` unless `--all`.
- **One primary per base:** `approve.py:45–49` blocks sibling approval without `--force`.
- **`--swell` enforcement:** `approve.py:51–55` exits for arc beds (`build`/`climax`/`swell-and-rest`).
- **`swell_s` on `MusicEntry`:** `music_library.py:56–57`, stored in `approve()` at `170–171`.
- **Energy-fit:** `BEAT_PREFERRED_ENERGY` + `+1.5` bonus in `find_for_beat` (`_specs.py:35–41`, `music_library.py:126–127`).
- **LUFS measurement:** real `loudnorm` in `ingest.py:36–46`.
- **Eleven Music scope note:** matches `enhance.py:120–121` (continues on failure, not falsely claimed as default path).

---

## Critical findings (blockers before Suno spend)

### 1. Status line contradicts itself and `README.md`

The artifact claims:

> `🧩 Designed, built+proven during the pilot: the beat-aligned placer`

…but step 1 still says:

> `Build placer.py by generalizing enhance.py mix()`

There is **no `music_library/placer.py`**. `README.md` is honest (“**not built yet**”); `CATALOGUE.md` overclaims “built+proven.” Round-2’s “warehouse before forklift” risk is reduced, not removed: you can still spend on 8 pilot MP3s before the thing that validates them exists.

### 2. `enhance.py` reuse is overstated — the hard 70% is still greenfield

The artifact says only “trim-to-in-point + swell→CTA + duck-under-KJV-quote are new.” In `11labs-testing/enhance.py`, music is `bed-full` from **`start=0.0`** with `atrim=0:{length}` (`enhance.py:63`, `178–179`). No swell alignment, no KJV-specific duck, no LUFS normalization from `bed.lufs_i`.

What’s proven: sidechain duck + mux graph. What’s not: the entire reason this catalogue exists. Calling it “generalizes `mix()`” hides that the pilot deliverable is mostly new ffmpeg logic.

### 3. One-bed architecture makes ~40% of the catalogue (and 1 pilot slug) strategically orphaned

The artifact locks shorts to:

> `ONE primary melodic bed for the whole clip` … picked via `find_for_beat('landing', …)`

That auto-selector **cannot** return `lonely`, `lament`, `tension`, or `urgent` (excluded from `landing` in `BEAT_ALLOWED`). Yet the pilot includes **`lonely_searching`** and the catalogue invests heavily in hook-only moods (“narrative-only on the CTA”).

Nothing in `PLACER.md` specifies:
- landing-section attenuation/mute when a narrative-only mood was manually chosen, or
- that hook-only beds are **long-form / manual-only** under the one-bed rule.

Without that, `lonely_searching` in the pilot is either wasted Suno spend or a doctrine violation waiting to happen (unresolved ache under the CTA).

### 4. `t_cta` and `kjv_span` have no mapping in the production pipeline

`PLACER.md` assumes:
- `t_cta` = “start time of the Landing beat's first word (from `words.json`)”
- `kjv_span` = “verbatim KJV quote window, from `words.json`”

`words.json` from `_align.py` is a flat word list — **no beat IDs, no quote spans**. `pipeline/assembly_timing.py` labels sections `hook | quote | bridge | landing`, not `hook | point | proof | conviction | landing`. Gospel-five-beat timing lives in `data/structures.json` (0–8, 8–18, …) but is **never wired to word timestamps** in assembly code.

The placer design assumes infrastructure that does not exist. “Lock design (done)” is premature.

### 5. Intelligibility gate is prose-only

> `Pilot gate = STT word-recovery ≥ 98%`

`veed_io.aligner.transcribe_align` exists, but **no script computes word-recovery %**, no threshold check, no pilot automation. The KJV duck (`PLACER.md:45–47`, “extra −10 dB”) is also design-only — `enhance.py` only does global sidechain under voice.

The artifact cites the aligner-drops-words problem as motivation, then proposes a fix with no implementation path tied to `cli_assemble` / `assembly_align.py`.

### 6. “✅ Built” still means “module exists,” not “engine can use it”

> `✅ Built: library API, specs, ingest … find_for_beat … find_layer`

`MusicLibrary` is imported only inside `music_library/*.py`. **`cli_assemble.py`, `cli_pipeline.py`, and `pipeline/assembly_*.py` have zero music references.** `index.json` is `[]` — no real Suno take has exercised ingest → approve → select.

Round-2 integration gap is **unresolved**.

### 7. `neutral` on Landing is still arc-hostile and selectable

The matrix still allows `neutral` on `landing`. `neutral_teaching_warm` is pilot-flagged and tagged for exposition (`_specs.py:136–140`). Under one-bed selection, an empty-tag `find_for_beat('landing')` can still return a flat underscore through the CTA if tag/energy scoring ties break wrong — and nothing deprioritizes `neutral` on `landing` in code.

Round-2’s “neutral undermines grace climax” finding is **not** addressed.

### 8. `swell_s` is a manual single point of failure

The placer’s core alignment is `bed_start = t_cta - bed.swell_s` (`PLACER.md:39–40`). `swell_s` is a human `--swell` guess at audition with **no validation** (no onset detection, no listen-back auto-check). Wrong by 2s = swell misses CTA; the fallback (“accept swell early”) is acceptance of failure, not a fix.

### 9. Energy-fit is a weak tie-breaker, not real fitness

`+1.5` on tag overlap (`music_library.py:126–127`) is easily beaten by one matching tag. It does not hard-exclude wrong energy (e.g. `sacred_grace_rise` with `energy=build` remains legal for `point` in `BEAT_ALLOWED`; it just won’t get the `low` bonus). Under one-bed-via-`landing` this matters less, but the matrix still advertises per-beat fitness that the selector doesn’t strictly enforce.

### 10. `use_cases` metadata is dead weight

`_specs.py` carries rich `use_cases` (`"grace-climax"`, `"the-ache"`, etc.) and the catalogue lists per-slug beats via `beats_for_mood()`, but `find_for_beat` ignores both. Slug-level intent (`sacred_grace_rise` vs `sacred_intimate_piano`) is not selectable — only mood + tags + weak energy bonus.

### 11. Import fragility will bite on integration

`music_library.py:114` does `from _specs import …` (relative to CWD/`sys.path` hack). Importing `music_library` from `pipeline/` or `cli_assemble` without the same `sys.path` insert will fail. Integration is not designed yet.

### 12. README still contradicts the one-bed architecture

`README.md:26–27` says `find_for_beat(beat, tags)` picks per Gospel-Five-Beat beat. `CATALOGUE.md` says shorts use **only** `find_for_beat('landing', …)`. Operators will follow the wrong doc.

---

## Cost / spend judgment

- **Suno flat plan:** catalogue cost is fine *if* beds are reusable.
- **Pilot order is wrong:** generating `lonely_searching` before `placer.py` exists and before the one-bed vs hook-only strategy is codified risks ~25% of pilot spend on a bed the auto-path can’t use.
- **Eleven Music fallback:** correctly demoted to metered; no issue.
- **QC budget (`_c`/`_d` takes):** `ingest.py` `base_of()` supports extra suffixes — real and good.

---

## Verdict summary

Round 3 honestly fixes layering, pilot gating, swell metadata, energy hints, and the `enhance.py` trim lie. But it **re-introduces overclaim** (“built+proven”), leaves the placer unbuilt, and papers over the hook-only vs one-bed contradiction. The acceptance gates (98% STT, KJV duck, CTA swell align) are **design text**, not code. Do not batch Suno until `placer.py` exists on John 4 and the beat/quote timestamp mapping is specified against `assembly_timing` + forced align, not imaginary `words.json` fields.

VERDICT: REVISE
TOP FIXES:
1. **Build `placer.py` first (before Suno pilot spend)** — fork `enhance.py`’s sidechain graph only; implement swell→CTA trim, KJV-span duck, and LUFS gain; derive `t_cta`/`kjv_span` from `build_timeline()` + `forced_align_script`, not an underspecified `words.json`; delete “built+proven” until John 4 passes coded gates.
2. **Resolve hook-only beds vs one-bed shorts** — either document `lonely`/`lament`/`tension`/`urgent` as long-form/manual-only (drop `lonely_searching` from pilot), or add landing-section attenuation rules in the placer; deprioritize or ban `neutral` on `landing` in `BEAT_ALLOWED` if the arc matters.
3. **Wire a real production consumer + automated intelligibility gate** — e.g. post-mux step in assembly or a `music_library/mix_pilot.py` that calls `MusicLibrary`, runs `transcribe_align` vs script with ≥98% threshold, and fixes the `from _specs import` packaging so `pipeline/` can import it.
