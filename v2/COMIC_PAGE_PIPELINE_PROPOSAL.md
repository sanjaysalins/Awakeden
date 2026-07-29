# COMIC PAGE PIPELINE — narration-driven, from scratch (PROPOSAL, rev 2.1)

> **rev 2.1 (2026-07-25, user direction): TEXT POLICY SIMPLIFIED — NO speech
> bubbles anywhere. The narrator's voice does the main lifting. On-page text
> is only (a) small KJV REFERENCE boxes and (b) rare EMPHASIS boxes for an
> element the viewer should concentrate on. Not much text. This resolves the
> caption-policy and red-letter decisions and removes the speaker-attribution
> risk class entirely (§7). Matches locked memory
> `native-panel-captions-minimal`.**

> **STATUS: DRAFT PROPOSAL — not wired, not locked.**
> Rev 1 written 2026-07-25 from the user's direction: *"start from scratch —
> take our narration, plan how many pages from the narration time, no
> freeze-frame anywhere, decide panels per page so it looks like a comic
> strip, build the individual panel stills, animate with Kling or Seedance,
> composite into a single animated comic page. Clips reusable in long format
> later. Fable designs; other models execute."*
>
> **Rev 2 (same day): independent 5-CLI panel review complete —
> REVISE×4 (cursor, claude, gemini, grok; codex timed out, backend outage).**
> Full reviews: `v2/_independent_review/20260725-165001/`. Every convergent
> finding is fixed in place below and marked `[R]`. The biggest corrections:
> a missing CP-0 alignment stage (the "clock" input was mislabeled and not
> guaranteed to exist), the narration-timed spotlight honestly re-scoped as a
> core rewrite (not a "small upgrade"), a split text policy (KJV-verbatim is
> impossible for original narrator prose), loop-mode decisions moved to AFTER
> animation (an LLM can't predict rendered physics), freeze-lint claims
> softened + calibration required, cost model holes filled (LLM pass, 10s
> renders, audits), and the build plan shrunk to throwaway-scripts-first.
>
> Technique evidence this stands on: `.claude/skills/comic-strip-native/
> COMIC_STRIP_NATIVE_SPEC.md` (itself DRAFT — a real dependency risk,
> §13.9) and the $0 text-layer POC
> (`poc_thief_e2e/clips/_text_layer/_REVIEW.html`). Where this doc and the
> technique spec disagree, the technique spec wins on technique; this doc
> owns the SYSTEM (timing math, contracts, gates, wiring).

---

## 0. One-paragraph summary

The narration is the clock. Its word-aligned timeline decides how many comic
PAGES a piece needs, where each page starts and ends (always on a phrase
boundary), and how long each page holds. Each page gets 1–4 panels chosen by
beat density; every panel is a separate, purpose-built, full-resolution NBP
still; every panel is animated individually (Kling for action,
Seedance/Hailuo for calm — bake-off decides); panel clips are loop-extended
AFTER their real motion is known so **no panel ever freezes** (a calibrated
lint enforces this); the page is composited with real gutters + wobbled ink
borders and a virtual page camera whose spotlight follows the narration word
timings; on-page text is MINIMAL — KJV reference boxes + rare emphasis
boxes, no speech bubbles, drawn by code INSIDE the composite pass,
cell-relative. Pages concatenate under the narration with the existing
score/SFX/caption/landing-hold/watermark stages. Every panel clip is banked
full-res, through the real reuse engine, for the 16:9 long format.

```
CP-0  alignment           narration.alignment.json (forced alignment — MUST run)
CP-1  page_plan.json      T seconds → N pages → panels per page (phrase-driven)
CP-2  panel stills        1 NBP call per panel, full res, chained anchors
      ── HUMAN GATE (stills)  + mouth/tail anchors recorded ──
CP-3  panel clips         Kling (action) / calm-tier winner, 5s or 10s
CP-3.5 clip QC + loop mode  per ACTUAL rendered motion: boomerang | fwd-loop | 10s
CP-4  loop extension      every clip extended to EXACTLY its page dwell
CP-5  page composite      gutters, ink borders, narration-timed focus schedule
CP-6  text layer          bubbles + captions, cell-relative, in-pass
      ── HUMAN GATE (pages) ──
CP-7  assembly            concat + narration + score/SFX/captions + hold + mark
      └── bank             clip_reuse path (coherence-gated) → 16:9 reuse
```

---

## 1. Inputs + CP-0 (the stage rev 1 forgot) `[R: all four reviewers]`

| Input | Source | Used for |
|---|---|---|
| `narration.mp3` (duration-locked) | existing audio stage | the clock |
| `_turns/` per-turn audio + `voices.json` | existing | speaker per line → deterministic bubble attribution |
| `narration.md` / `narration.creation.json` | existing | line text, KJV refs |
| `data/kjv_cache.json` | existing | byte-verbatim scripture strings |

**CP-0 — generate `narration.alignment.json`.** Word-level timing comes from
`pipeline/assembly_align.py` — **ElevenLabs forced alignment first, local
faster-whisper fallback** (NOT WhisperX; that's the caption path — rev 1 had
this wrong). It is produced on demand, not at narration lock, so CP-0 runs
it explicitly and FAILs the pipeline if alignment is missing or stale
(`alignment-cache-staleness` rules apply). ElevenLabs availability is on the
critical path — the fallback keeps CP-0 runnable offline. No circular
dependency: alignment needs only the locked audio, nothing visual.

Precondition: the narration is LOCKED. This pipeline never runs on an
unlocked script.

---

## 2. CP-1 — Page plan: the timing math

**Deterministic core (code, $0), then an LLM pass for composition only.**

1. `T` = narration duration.
2. **Page dwell band: 8–16s, target 12s** (hypothesis — validated only by
   12s POC pages; Rung 1 tests it, §12).
3. `N_pages = clamp(round(T / 12), ceil(T / 16), floor(T / 8))` with
   **round-half-up pinned** (Python's banker's rounding differs — CP-G6
   gates on this math) `[R: claude]`. 59s → 5 pages.
4. **Boundaries snap to phrase ends** — the existing clause-sized phrase
   builder (`build_phrase_board`, `pipeline/assembly_timing.py`) over CP-0's
   words. Pages are NOT uniform length. **Out-of-band repair rule
   `[R: claude, grok]`:** if snapping pushes a page outside 8–16s, merge it
   with its shorter neighbour; if the merge exceeds 16s, split at the
   nearest phrase end to the midpoint; if no legal split exists, CP-G6
   FAILs to the human — never silently ship an out-of-band page.
5. **Panels per page (1–4) from beat density** — thresholds stated so a
   lesser model can execute them `[R: grok]`: 1 panel if the page span is a
   single phrase OR is flagged `sacred`/landing; 2 if 2–3 phrases or a
   two-speaker exchange; 3 if 4–5 phrases; 4 if ≥6 phrases or ≥3 speaker
   turns. The LLM pass may move a page ±1 panel with a stated reason;
   CP-G6 logs every override.
6. **Layout per page** from panel count: 1 → `full-bleed` (a NEW layout
   entry to add — `LAYOUTS` has no 1-panel mode today, "skip the grid" is
   not a contract `[R: grok, cursor]`); 2 → `2v`/`2h`; 3 → `3-big-*`;
   4 → `2x2`. **Variety rule:** no two consecutive pages share a layout
   when a legal alternative exists at that panel count (2x2 is the only
   4-panel layout — a page may repeat it rather than force a wrong panel
   count; CP-G6 records the exemption) `[R: cursor]`. At least one
   full-bleed hero page per piece; **the LAST page carries
   `landing_subject: "christ"` — a structured, machine-checkable field,
   not a string grep** `[R: cursor]` (inherits AS-G6/G7 spirit).
7. **LLM pass** (composition only): per panel — composition, speaker (from
   the deterministic `voices.json`/turn map, LLM may not invent speakers
   `[R: grok]`), `animation_tier` (calm|action), text elements (§7 policy),
   `sacred` flag, reuse candidates. Runs through the project's standard
   self-review + independent-audit **process** (the SP-G gate *process*,
   not the SP-G gate IDs — those belong to scene_plan `[R: grok]`).
   Operational note: LLM calls run over the agent bridge
   (`LLM_PROVIDER=agent`) — attended runs only, and $0 marginal cost; if a
   metered key returns, budget ~$3–5 Opus per piece `[R: claude]`.

**Output — `page_plan.json`:**

```json
{ "piece": "<v1 folder>", "total_s": 59.2, "canvas": {"w": 1080, "h": 1920},
  "pages": [
    { "n": 1, "t0": 0.0, "t1": 11.8, "layout": "2x2",
      "landing_subject": null,
      "panels": [
        { "id": "p1a", "composition": "...", "speaker": "narrator",
          "sacred": false, "animation_tier": "action",
          "aspect": "3:4", "reuse": null,
          "focus": {"t0": 0.0, "t1": 3.1},
          "loop_mode": null,
          "text": [ {"kind": "ref", "source": "Luke 23:40"} ] } ] } ] }
```

`focus` windows come from the words spoken while that panel carries the
story. `text` elements are `kind: "ref" | "emphasis"` ONLY (§7 — no
bubbles). `loop_mode` is EMPTY here — it is decided at clip QC (§4), never
predicted by the LLM `[R: gemini]`.
**Canvas contract `[R: cursor]`:** shorts = 1080×1920; long = 1920×1080;
`grid_choreography` must be called with explicit `--w/--h` (its default is
landscape). Panel still aspects snap to the provider-legal set (9:16, 3:4,
1:1, 4:3, 16:9) nearest the cell shape; the composite mattes/crops the
overflow inside the cell — never feed a video model an arbitrary crop
`[R: gemini]`.

---

## 3. CP-2 — Panel stills (separate, full-res, chained)

**CP-G10 — BIBLICAL-PERIOD GATE (locked by user 2026-07-25, rev 2.3;
inherits the project-wide `feedback-stills-biblical-period-gate` fail-closed
rule):** every character and prop anchor MUST state first-century-Judea
period detail explicitly — ankle-length rough-woven tunics, girdles, mantles,
head cloths, sandals, full beards/period hair; NO modern or medieval-European
tailoring, hairstyles, or silhouettes. **Bound codex books are FORBIDDEN —
written records are SCROLLS (or wax tablets)**; a codex is an anachronism
(and the scroll is the doctrinally correct image — Col 2:14's "handwriting
of ordinances"). The stills self-check and the human gate both include an
explicit period pass per panel, fail-closed. POC evidence: the Rung 2 seeker
+ ledger-codex read modern and were caught by the USER at the gate —
executor and designer passes both missed it because the anchors never
stated the period.

Technique spec §0.5 path unchanged: one `nano_banana_pro` call per panel via
the existing provider layer (`pipeline/visual_render.py` NBPProvider +
`extra_ref_paths` chaining + audit sidecars — NOT new ad-hoc scripts
`[R: cursor]`), Character Anchors verbatim, Christ body gate written
positively into every passion anchor, no baked text ever.

**Reuse-first through the real engine `[R: cursor]`:** candidate lookups and
banking go through `pipeline/clip_reuse.py` + `clip_library/` with coherence
verification and clip QC — `asset_index.json` alone is not the reuse path.
Every new still that will enter any multi-panel grid gets a
`visual_tags.json` category tag at this stage (panel-variety rules apply to
comic pages from piece one).

**HUMAN GATE — stills:** full-res eye check (CSN-G1..G4 from the technique
spec, unchanged — this doc does not duplicate them `[R: grok]`), every
passion panel every time. (rev 2.1: mouth/tail anchor recording DROPPED —
no bubbles means no tails to aim `[R: grok #5 → moot]`.)
**Consistency is checked SIDE-BY-SIDE, not per panel** (rev 2.2, POC
lesson): the gate gallery must show all of a page's panels together, and
each named character is compared feature-by-feature across panels (hair,
face/build, wardrobe, key props, recurring set pieces like the door).
Rung 1 evidence: per-panel glances passed 4 stills that a side-by-side look
showed had three drifts (seeker's hair colour, Jesus' face+robe, the door's
shape) — caught by the USER, missed by executor and designer alike. Baked-
text checks likewise require native-pixel crop-zoom of hardware/edge
regions (tiny "PBD:O" glyphs survived a full-res glance).
**Anatomy/pose coherence is an explicit checklist item** (rev 2.2b, POC
lesson #3): for every figure, check the head faces a direction the BODY
can support (a walking-away figure with a full-profile or twisted head =
FAIL), plus the standard hands/limb count. The POC's head-twist case was
again caught by the user after executor and designer passes.

---

## 4. CP-3 / CP-3.5 — Panel animation + the loop-mode decision

| Tier | Model | ~Cost | When |
|---|---|---|---|
| action / crowd / complex | Kling 3.0 pro, sound off | ~$1.13 / 5s, ~$2.25 / 10s | real story motion |
| calm single-figure | **winner of the Rung-1 bake-off** — Seedance 1.5 Pro (~$0.72) vs Minimax Hailuo (~$0.90, 2/2 clean on ink panels) | ~$0.72–0.90 / 5s | held expressions, drift, breathing stillness |

Rev 1 listed Seedance as a default AND deferred it to a bake-off — a
contradiction `[R: cursor]`. **Rule: no at-scale CP-3 run before the
bake-off names the calm tier.** All renders go through
`pipeline/video_render.py` providers (model-aware flags, NSFW→direct-Kling
fallback, ledger hooks) — no raw `hf` subprocess forks `[R: cursor]`.

**CP-3.5 — clip QC + loop-mode decision `[R: gemini, grok, cursor]`.**
5-timestamp frame check per clip (CSN-G5), then the loop mode is chosen
from the ACTUAL rendered motion — never predicted from the prompt:
- reversible motion (drift, mist, breathing, flicker) → `boomerang`;
- directional motion with a low-motion tail → `fwd-loop` (crossfade on the
  tail);
- directional motion, no usable tail → **10s render** (priced in §11) or
  re-roll calmer.
The decision is recorded into `page_plan.json.loop_mode`. The physics
check here is a NEW lightweight eye/Vision step on the rendered clip —
`physics_motion_check.py` expects `scene_plan.json` and is not reusable
as-is `[R: cursor, grok]`.

## 5. CP-4 — The NO-FREEZE guarantee

1. **CP-4 is the SOLE owner of looping `[R: claude]`.** Every panel clip is
   pre-extended to EXACTLY its page dwell using its `loop_mode`. The
   composite asserts `len(clip) == dwell` and **errors** on mismatch — the
   in-grid frame-wrap (already in `grid_choreography.py`) becomes an
   assertion failure, not a silent fallback, because its hard jump cut
   evades the freeze lint.
2. **Repetition honesty `[R: claude]`:** a 5s clip boomeranged over a 16s
   dwell shows its motion ~3×. POC evidence is 12s pages only. Rung 1
   renders one ≥14s page deliberately to judge repetition by eye before
   any bigger spend.
3. **`page_freeze_lint.py` — CP-G8, calibrated, not almighty
   `[R: claude, gemini]`.** Per panel cell, motion is measured on the
   PRE-COMPOSITE extended clips (full brightness — the composite dims
   unfocused cells to ~45%, which crushes pixel diffs) plus a
   composite-level pass; frames are downscaled+blurred before diffing to
   kill H.264 noise; boomerang turnaround zones get a grace window;
   declared static cell types (typography/infographic) are exempt via
   `page_plan.json`. **The gate ships only after calibration against
   labeled clips — the frozen Zacchaeus pages (known-bad) and the clean
   POC pages (known-good)** (`gate-calibration-human-authority`). It is a
   floor under the eye gate, not a replacement — rev 1's "kills this
   regression class permanently" was overclaim.

## 6. CP-5 — Page composite (honest scope: a core rewrite) `[R: all four]`

`grid_choreography.py`'s `activeness()` is a uniform cyclic metronome and
the pan model assumes it. Narration-timed focus needs a NEW focus-schedule
model: variable-length windows, non-cyclic order, possible revisits, defined
**gap behavior** (no window active → hold the page-wide neutral frame, no
pan drift), defined **end behavior** (after the last window: neutral
full-page view until page end), and a `full-bleed` single-panel mode.
This lands in a new `panel_animator/page_compose.py` that reuses the
drawing primitives (gutters, wobbled borders, dim/spotlight) — the
choreography core is rewritten, not parameterized. Rev 1 called this a
"small, contained upgrade"; that was wrong.

## 7. CP-6 — Minimal text layer (rev 2.1 — user's call: the narrator does
the lifting, NOT on-page text)

**NO speech bubbles, anywhere, ever, in this format.** The narration voice
carries every word. Exactly two on-page element kinds:

- **`kind: "ref"` — KJV reference box.** A small parchment tag (e.g.
  "LUKE 23:42"), panel corner, when that panel's beat quotes scripture.
  $0 deterministic check: the reference must exist in `kjv_cache` AND match
  the verse the narration actually quotes at that timestamp (no decorative
  refs). At most one per panel; not every panel gets one.
- **`kind: "emphasis"` — concentration box.** RARE, deliberate — a short
  phrase or word the user wants the viewer to focus on, parchment-band
  treatment (the project's standard, `panel-animator-intentional-use`
  memory: chosen per beat, never mechanical). Text byte-verbatim from the
  locked `narration.md` line or the KJV verse it cites ($0 check). Budget
  guidance: ≤3 per short; the LLM pass PROPOSES, the user's stills-gate
  eye APPROVES.

**Anti-clutter (simplified by the no-bubble rule):** an element pops at its
first aligned word, expires when its panel's focus window ends + 1.5s grace;
max ONE text element on screen at a time; dimmed panel → its text dims with
it. Muted-viewing note: muted viewers get the standing burned caption layer
(unchanged, next paragraph) — on-page text no longer needs to carry dialogue
`[R: cursor #14, gemini #3, claude #6 → all resolved by this policy]`.

**Caption stage: UNCHANGED.** The standing ivory caption layer burns the
full spoken narration exactly as on every other format — no filter spec, no
double-print risk (nothing spoken is on-page), no INV conflict. The
rev-2 "blocking caption decision" is RESOLVED by the no-bubble policy.
Red-letter is moot (no bubble text). The bubble-drawing code from the POC is
kept as evidence but NOT carried into production; the ref/emphasis boxes
reuse the POC's parchment caption-box drawing.

**HUMAN GATE — pages:** watch every composited page with text before
assembly; excludes/re-rolls are per-panel.

## 8. CP-7 — Assembly

Concat pages (hard cuts; `/ink-transition` selectively), mux narration,
then the existing standing stages: score, SFX bed, captions per the §7
policy, landing hold ≥3.0s (INV-26), watermark (INV-27),
`check_landing_hold.py`, release gates. New $0 checks `[R: grok]`:
`sum(page dwells) == T` before concat, and an A/V duration match after mux.

**What this replaces `[R: cursor, grok]`:** for comic-format pieces this
pipeline REPLACES the livingpage build path (same narration/voice/score/
caption stages, different visual middle). Livingpage remains for its own
format; no third orphan path — `run_piece.py` stage detection gets a
`page_plan.json` branch ONLY after Rung 2 passes. Until then nothing is
wired (throwaway scripts, §12).

---

## 9. Reuse — the 16:9 long format

- Panel stills full-res + panel clips banked through `clip_reuse` +
  coherence gates + `visual_tags.json` (§3) — reuse candidates for 16:9
  grids per the locked `vertical-panels-cross-aspect-reuse` rule.
- The long runs the SAME pipeline: CP-1 on a 6–8 min narration (~30+ pages),
  16:9 canvas, horizontal-leaning layouts, reuse-first pulling banked
  panels.
- **Unproven and priced as such `[R: claude, cursor]`:** the ≥40% warm-bank
  assumption has no evidence until 2–3 shorts ship in one visual world;
  16:9 native panels are untested; and **no rung below spends on a full
  long** — Rung L0 (a $0 dry-run of CP-0/CP-1 on a real locked long
  narration) must pass before long-form costs are treated as more than
  projections.

---

## 10. Gate registry (NEW gates only — CSN-G1..G5 apply by reference)

| Gate | Type | Checks |
|---|---|---|
| CP-G6 page-plan sanity | code, $0 | boundaries on phrase ends; dwell in band or repaired per §2.4; panel-count thresholds + logged overrides; layout variety (with 2x2 exemption); hero page present; `landing_subject=="christ"` on last page; round-half-up math; `sum(dwells)==T` |
| CP-G7 text layer | code + eye | NO bubbles (zero `kind:"bubble"` elements — hard FAIL); ref boxes match the verse actually quoted at that timestamp ($0); emphasis text byte-verbatim + ≤3/short + user-approved; expiry + max-1 rules |
| CP-G8 freeze lint | code, $0, **calibrated before trusted** | no cell static >0.8s (pre-composite measure + composite pass); jump-cut wrap = assertion error |
| CP-G9 assembly | existing + $0 | INV-26 hold, INV-27 mark, A/V match, release sync |

---

## 11. Cost model (rev 2 — holes filled `[R: cursor, claude, grok]`)

Per 4-panel page: stills ~$1.20 · animation ~$3.40–4.50 (5s mix) · +$1.10
per tail-less action clip needing 10s · LLM plan/audit $0 over the agent
bridge (attended; ~$3–5 Opus per piece if metered) · text/composite/lints $0.

| Piece | Honest range |
|---|---|
| 59s short (5 pages, ~14–16 panels) | **$24–36** incl. 1-in-3 rerolls + one or two 10s clips — no longer claimed "comparable" to the $23 locked-pipeline short; it is somewhat dearer `[R: cursor]` |
| 6:30 long, cold | ~$140–190 — **projection only until Rung L0 + real bank data** |
| 6:30 long, warm bank | ~$85–115 — same caveat |

All metered calls pre-flight through `/cost` + explicit user OK.

---

## 12. Build plan + validation ladder (shrunk `[R: cursor, grok]`)

**Nothing production-shaped is written before Rung 2 passes.** No
`cli_comic.py`, no runner, no `run_piece` branch. Rungs 1–2 run on
throwaway scripts in a POC folder (the `poc_thief_e2e/` pattern), reusing
`visual_render` providers, `video_render` providers, `grid_choreography`
primitives, and the POC text-layer drawing code.

| Rung | Spend | Proves | GO/NO-GO |
|---|---|---|---|
| **0 (short dry-run)** | $0 | CP-0 alignment + CP-1 math + CP-G6 on a real locked short narration; dwell report | page plan reads right by eye |
| **L0 (long dry-run)** | $0 | same on a real locked 6–8 min narration `[R: claude]` | ~30-page plan is sane |
| **1** | **~$10–14** | ONE page end-to-end incl. calm-tier bake-off (2 panels Seedance vs Hailuo), one ≥14s dwell, CP-3.5 loop modes, draft CP-G8 run + dwell report `[R: grok]` | eye + draft lint both pass |
| **2** | ~$18–28 | remaining pages + full assembly; **page-by-page GO** (anchor/colour drift checked per page, not all-at-once `[R: cursor]`); caption policy decided | finished watchable short |
| **3** | ~$8–12 | one 16:9 page (banked + new panels) | long-format + reuse proof |

Only after all rungs: build `pipeline/comic_page_plan.py`,
`panel_animator/page_compose.py`, `page_freeze_lint.py`, runner + CLI, and
wire into `run_piece.py`/spec registry.

---

## 13. Open items / honest risks

1. Dwell band 8–16s is a hypothesis (Rung 0/1 test it).
2. Calm-tier model undecided until the Rung-1 bake-off.
3. 16:9 native panels untested (Rung 3).
4. NBP cross-session colour drift unmitigated — generate a piece's stills
   in one continuous run.
5. Christ-body gate has no Vision check (eye-only) — standing gap.
6. Warm-bank economics unproven; long costs are projections.
7. ~~Caption policy~~ RESOLVED rev 2.1 — no bubbles; standing caption layer
   unchanged.
8. ~~Red-letter bubbles~~ MOOT rev 2.1 — no bubbles.
9. **The technique spec this stands on is itself DRAFT** `[R: cursor]` —
   if its second review round moves, this doc follows.
10. Stochastic Christ-body recurrence: the eye gate is permanent per-panel
    overhead, priced in.
11. Focus-schedule rewrite (§6) is the largest new code risk — it is $0 but
    non-trivial; Rung 1 builds it in throwaway form first.

---

## 14. Execution model — Fable designs, other models execute (user directive)

- **This document is the interface.** Every stage above states its exact
  input artifact, output artifact, commands/providers, thresholds, and gate.
  An executor (Sonnet/Haiku, a CLI agent, a workflow subagent) follows it
  WITHOUT design judgment.
- **Escalation boundaries — the executor never decides:** doctrine calls
  (anything touching CSN-G3/G4, sacred flags, landing subject), spend beyond
  the approved rung, any gate FAIL, any ambiguity between this doc and the
  technique spec, any deviation from a stated threshold. All of these go
  back to the user (decisions) or to Fable (design revisions).
- **Determinism ladder:** machine gate > recorded human judgment (anchors,
  gate sign-offs) > executor judgment. Where rev 2 added thresholds
  (§2.5 panel counts, §5 loop rules, §7 expiry rules), that is deliberate —
  the design carries the judgment so the executor doesn't have to.
- **Worker briefs:** each rung's execution is a short brief derived from
  this doc (stage, inputs, commands, acceptance checks, escalation list) —
  written by Fable at rung start, executed by the cheaper model, results
  reviewed against the acceptance checks before the next rung.
