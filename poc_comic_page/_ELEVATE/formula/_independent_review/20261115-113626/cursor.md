# Independent review — cursor (OK, 68s)

# Independent red-team: FORMULA plan

## Feasibility vs the real repo

**The “template” in Option A step 3 does not exist; the lane is still per-episode Python.** The plan says Sonnet will build “one template (episode words + timings in, film out)” (Option A §3). In code, `build_s32.py` and `build_barabbas.py` hard-code `SH`, `PL`, `S`, clip paths, and pill PNG generation—there is no words-in/film-out parameterization. Barabbas already splits `base_A5` + `letter()` (`build_barabbas.py` ~227–230), but the thief builder still calls `T.compose("S32", shots, ov)` with pills burned in one pass (`build_s32.py` ~40–47). Step 4 (“rebuild the Thief film on the new template”) assumes a template that step 3 has not defined and that step 2’s word-free layout has not been applied to s32 yet.

**The plan’s visual DNA does not match the lane’s other “proven” format.** DNA claims “bold-ink comic, full-screen clips, close faces” and “Length 38 s, 8 lines” (`Proposed DNA`). `HANDOVER_RESUME.md` calls the **3×1 manga grid + gemini_omni_flash** pipeline the “proven comic format” and ships Barabbas at **41.6 s** with **10+ pills**, not 38/8. You are trying to formula-ize the thief short while the lane has already forked into two incompatible look/length/cost models.

**“Repo already has … Remotion” is not wired to `_ELEVATE`.** Doodles cite `annotators-circle`, `marginalia`, … and `_remotion/` (`Doodles / motion graphics`). Those devices target stills / long-form comic grids / Bartimaeus-style Remotion stacks (`EPISODE_PLAYBOOK.md` Step 10). Comic ELEVATE is **ffmpeg + PIL PNG overlays** (`build_tp.compose`, `build_w3.pill_tabs`). No plan step says whether doodles land in `base_*.mp4`, a Remotion comp, or `panel_animator/`—each is a different integration with different gotchas (Bartimaeus: guard boxes, `mix-blend-mode` under transforms; Bethlehem: pills on faces).

**Cost quote is cherry-picked and unsafe for “new story end to end.”** “a new story's clips ~$8-12 (a sibling short cost ~$8.55)” (Option A) matches **Barabbas** totals in the ledger/`HANDOVER_RESUME.md`, but that spend includes **grid stills, many moment clips, re-records, manga tests**—not “thief-like full-bleed Kling from scratch.” The thief **short32** is $0 assembly **because** it borrows `today_paradise_luke2343/visual/clips` (`build_s32.py` line 11). A greenfield Luke-scale parent (many stills + Kling) is multiples of $8–12 per parent history in `spend_ledger.jsonl` for `today_paradise_luke2343`. Quoting Barabbas as the default floor will blow the “words before money” contract.

**“bottom ~25% kept clear for subtitles” conflicts with current pill geometry.** Fix proposes clear bottom quarter (`Identified problem for global/multi-language`). `build_w3.pill_tabs` fixes pills at **`y0 = 1000`** on a 1920-tall frame (~mid-lower, not a dedicated subtitle band) and does not reserve safe area. Moving pills up for SRT still leaves **English hook cards** (`build_s32.py` hook at 0–2.2 s) and **speaker tabs / verse chips** (“LUKE 23:43”) as baked metadata. “Verse chips as numbers only (`23:43`)” does not remove **book names in speaker tabs** or KJV clause length in pills.

**Pilot step 4 is not a fair A/B without separating variables.** Rebuilding thief on “new template” from “old clips” ($0) only tests **lettering/motion/doodle** changes, not the hook, length, or clip grammar that might drive retention. Meanwhile the plan admits **“Retention / 3-second hold / share numbers have NOT yet been read”** (`Evidence it was "loved"`) and buries “read the real analytics before copying” at the bottom—should be **gate 0**, not an afterthought.

## Hidden risks & single points of failure

- **Timing is hand-tuned to one audio take.** `build_s32.py` documents turn starts from real segment durations; any word change or re-voice invalidates the whole `S`/`PL`/`SH` tables. A “template” without automatic alignment (`timeline.json` / whisper / `per_turn_synth` outputs) will not scale.
- **Doctrine / global-audience gates are missing from step 3 gates.** Listed gates: length, hook ≤3 s, clear bottom, no baked English, 3 s hold—nothing on **KJV fidelity**, **narration_gate**, **5 guardrails**, **film-only blind panel**, **`check_landing_hold`**, **`publish_check` / `cli_publish` SRT overwrite** (known gotcha in Bartimaeus playbook: `--index` rebuilds `captions.srt`).
- **Barabbas sound mix “never heard”** (`HANDOVER_RESUME.md`) shows the plan’s formula scope (picture + pills + doodles) understates **score/SFX/mix** as part of what audiences “loved.” Thief short may be narration-forward; Barabbas proves mix is non-trivial.
- **Option A step 1 “Fable watches cold and writes Formula Card”** duplicates `_ELEVATE_DIAGNOSIS.html`, bake-offs, `short32/draft_fable.md`, and packaging cards already in-tree—risk of a third parallel spec that drifts from `HANDOVER_RESUME.md` and `LANE_COMIC.md`.

## Over-engineering

- **New “formula template” before choosing thief-clip vs manga-grid as the repeat unit** is premature. You already have a 10-step new-episode recipe (`HANDOVER_RESUME.md` §Earlier work) and a full cross-lane playbook (Bartimaeus) with Remotion motion + type tiers.
- **Leaning on Remotion + device library + new template** in one pilot stacks three unproven integrations. Barabbas’s working pattern is **ffmpeg base + PNG letter layer**—extend that first; add Remotion only where ffmpeg cannot do timed doodles (as Bethlehem/Bartimaeus did), with an explicit per-episode cost in design time.

## Reuse gaps (duplication)

The plan should **name** extending:
- `build_barabbas.py`’s `base_*` / `letter()` split (word-free picture path exists for Barabbas, not thief),
- `_NEW_EPISODE_AND_BAKEOFF.html` / bake-off winners (Mockers-style pill already won),
- `poc_desert_storybook_heroes/EPISODE_PLAYBOOK.md` for motion/type discipline,
- existing `$0` gates (`narration_gate.py`, `check_landing_hold.py`, `release_check.py`).

Instead it proposes a parallel Sonnet “template” and vaguely cites `_remotion/` without a lineage from `BartimaeusV2.tsx` / `BethlehemV4.tsx`.

---

## (1) What is missing

1. **Analytics gate** before any Formula Card (3s hold, avg % viewed, rewatches, locale breakdown).
2. **Explicit format choice**: thief full-bleed vs Barabbas grid—or a decision rule (“dialogue-heavy cross beat → grid; …”).
3. **Audio pipeline in the formula**: score/SFX/mix steps, ear-check, landing hold verification.
4. **Words pipeline**: blind 5-guardrail panel, `narration_gate`, fresh-detail criterion (Barabbas lesson in `HANDOVER_RESUME.md` §6).
5. **Multi-language deliverable matrix**: English upload = burned EN letter layer? Other locales = base + SRT only? Per-locale `lett_<lang>/` generation + QA?
6. **Scripture sourcing workflow** (PD translations per locale, attribution, verse span consistency with on-screen chips).
7. **Publish chain**: `cli_publish`, caption red-team, `upload_tracker`, catalogue/`manifest.yaml`.
8. **Doodle sacred-window rules** (Bethlehem §4.6: no doodles on Jesus/cross close-ups) and **face-guard QC** (Bartimaeus Step 10).
9. **Independent review** on the Formula Card itself (`independent_review.py --type plan`).
10. **A/B plan already sketched** in `HANDOVER_RESUME.md` (animated vs pan-only)—not tied to formula validation.

## (2) What I would do instead (from scratch)

1. **Gate 0**: Pull YouTube (or platform) stats for thief short32 vs Barabbas vs other cluster shorts; define success metrics (not owner sentiment alone).
2. **Write one `FORMULA_CARD.md` that is lane-specific**, not generic: Mockers pill + hook card + twist structure + landing hold + **ffmpeg base/letter split** as the technical spine (already proven in Barabbas).
3. **Pilot 1 ($0)**: Refactor **only** `build_s32.py` to match Barabbas’s `base` + `letter()` pattern; English `lett_en`; export **muted base** for SRT-first locales; measure pill placement vs safe area with a deterministic lint (y-pos, max pill height).
4. **Pilot 2 ($0)**: One Fable **motion pass on the base only**—max 3 doodles, HTML artifact first; implement with the **smallest** tool (ffmpeg draw/overlay or one thin Remotion comp), not the whole device zoo.
5. **Pilot 3 (paid, quoted)**: **One** new story only after Pilot 1–2 beat or match thief on owner-chosen metrics; reuse clips where possible; log spend like Barabbas.
6. **Defer `cli_pipeline`** until two episodes ship through the ELEVATE handover path without custom rebuild hell.

## (3) Biggest risk of stale / repetitive formula

Locking **“paradox question hook + two contrast pairs + soft invitation landing”** (`Proposed DNA`) across a series will read as **the same rhetorical machine** every time—especially with **identical pill UI** (`build_w3.py` Mockers look won bake-off 2). Barabbas only escaped “tired, heard it before” by finding a **fresh true detail** (the name Bar-Abba), after blind rounds (`HANDOVER_RESUME.md`). The plan encodes **structure and look** but not **mandatory fresh-detail discovery** per episode, so repetition is the default.

## (4) Multi-language / SRT pitfalls not covered

- **`cli_publish --index` overwrites `captions.srt`**—hand-fixed SRTs (Bartimaeus pattern) need a standing re-copy step; not mentioned.
- **~32-char SRT cues vs ~3-line pills** at `y0=1000`: translators cannot mirror clause structure; **cue count ≠ pill count** breaks read-along if you ever burn localized pills.
- **Spanish/German “~25% longer”** breaks **38 s** lock unless words are cut, audio re-timed, or length cap relaxes (undermines DNA).
- **English master strategy unclear**: word-free master + SRT helps ES viewers but **English viewers lose read-along** unless you ship **two masters** (EN-burned vs clean)—not specified.
- **KJV on-screen in English vs PD translation in SRT** for the same beat: doctrine/consistency review per language.
- **Speaker tabs** (“THE OTHER THIEF”) need localization or icons; plan only mentions verse numbers.
- **Platform double-caption**: auto-translate + uploaded SRT + burned pills (if any slip through).
- **RTL / CJK**: no line-break or font strategy for pills if you generate localized letter PNGs.
- **Dubbing “later”**: SRT-first viewers get mismatched emotional performance vs doodle timing keyed to English stress.

## (5) Doodle / motion-graphic pitfalls

- **“Calendar page (‘someday’)”** violates **“Every doodle must read without words”**—calendar trope is text-literacy dependent; same for **ink underline beneath Jesus’ words** (needs reading order).
- **annotators-circle on a zooming Kling clip**: circle must track face/cross in screen space while `build_tp` does push-ins—static PNG doodles will **drift off-subject** unless designed in Remotion with motion-aware anchors (Bartimaeus `GUARD` pattern).
- **Split-screen mocker/thief** fights **full-bleed single-clip grammar** of the source film—either re-cut base (new timing risk) or squeeze panels (not what audiences loved).
- **3–5 doodles** on **sacred close-ups** (Jesus promise shot) risks Bethlehem-class failures: pills/doodles on **eyes/face**; FABLE_EPISODE_DESIGN explicitly moves pills off Herod’s glare.
- **Device library mismatch**: `impact-burst` / `grid-choreography` assume **comic grid layout**, not thief’s continuous full-bleed—visual noise reads as **CapCut template**, not elevation.
- **Remotion without `$0` face guard lint** on **moving** video: Bartimaeus warns measuring guards on stills is insufficient.
- **Ken-Burns-flat clips**: doodles may draw attention to **invented motion** or static pans (veo/Kling discipline)—elevation can worsen weak shots.

---

## Line-level verdict highlights

| Claim | Problem |
|--------|---------|
| “Length 38 s, 8 lines, ~85 words” | Thief narration is one closing turn; **10 pill rows** in `build_s32.py` `PL`; twist is **split across three pills** (26.55–35.3). |
| “3 voices: narrator + character(s) + Jesus” | **Four roles** in audio: mocker, penitent, Jesus, narrator (`narration.md`). |
| “Fix: word-free master + swappable lettering layer” | **Correct direction**; **already partial** in Barabbas, **not** in s32; no per-lang generation step. |
| “Steps 1–4 ~$0” | True only if no new clips and no Remotion render churn; **Fable/Sonnet time** and Remotion iteration are not $0 in practice. |
| “Also: read the real analytics before copying” | Contradicts proceeding with Formula Card (step 1) as written; should block step 1. |

---

VERDICT: REVISE  
TOP FIXES:  
1. Move analytics + format fork decision (thief full-bleed vs Barabbas grid) to **Gate 0** before any Formula Card or template build.  
2. Replace “one template” with **extend `build_barabbas` base/letter pattern to s32 first**, plus explicit multi-master strategy (EN-burned vs word-free + per-locale SRT/`lett_<lang>`).  
3. Add full ship path to the formula: words gate, audio/mix ear-check, doodle sacred-window + face-guard QC, publish/SRT overwrite rules, and **honest clip spend** when parent clips do not exist.
