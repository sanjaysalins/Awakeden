# Independent review — cursor (OK, 87s)

Independent adversarial review of the **scene plan artifact** (26 scenes, veo3 long-form), checked against `v2/LONGFORM_SPEC.md`, `/scene-plan-long`, `/animate-long`, `/assemble-long`, and the on-disk `scene_plan.json` / `_build_scene_plan.py`.

---

## Feasibility vs real codebase

**Scene count violates a hard invariant.** The artifact says **"26 scenes"**; `_build_scene_plan.py` line 3 confirms **26 scenes**. `LF-INV-4` and `/scene-plan-long` step 2 cap at **25** (`ceil(503.4/20) = 26` is the floor, not permission to exceed the cap). This fails before render.

**Hero nomination conflicts with written assembly gates.** The spine claims **"hero S26"** (risen Christ close, M7). `LONGFORM_SPEC.md` LF-AS-G5 and `/scene-plan-long` step 4 designate the **M6 substitution/exchange/cross** scene as hero, within the final 90s. Shipped episodes (#02–#04) also close on risen Christ — so this may pass in practice — but against the spec as written, **S26 is not the nominated M6 hero**, and you now have **three crucifixion stills (S14, S20, S21) plus a separate risen close** with no `hero: true` field in JSON (Psalm 22’s plan has `"hero": true` + `bank` on its close).

**LF-SP-G6 / LF-SP-G9 binding mix is not actually met.** The plan repeatedly labels scenes **"DEEP unified composition"** (S3, S10, S13, S14, S16, S17, S18, S21, S23) and the judge brief asks for **"unified multi-element + Christ/NT-link + OT-echo."** But LF-SP-G6 requires **3–5 named vignettes** per unified scene (same as shorts SP-G6). None are named — only continuous compositions. Compare Passover S1: *"DEEP layered composition centred on… scribe's hand… parchment… doorway…"* — still not fully gate-compliant, but closer. This plan’s unified scenes are prose composites, not the required vignette discipline.

**No reuse manifest — ignores standing INV-19 workflow.** Psalm 22’s `scene_plan.json` carries **`bank` slugs on every scene** (`christ_risen_reaching_hand_hero`, `christ_crucified_wide_jerusalem`, etc.). Seed’s JSON has **zero `bank` entries**. `/scene-plan-long` step 0: **"REUSE FIRST — `clip_reuse.decide_for_scene`"** with explicit warning not to over-assume the pool (~34/125 clean). S14/S20/S21 crucifixion and S26 risen-hand are prime reuse candidates; the plan regenerates all 26 from scratch.

**S15 violates LF-CLIP-NOWRITING but is assigned veo.** S15: **"unrolled blank scroll across the knees"** with **`forward_slow`** (veo push-in). `/animate-long` step 1 and LF-CLIP-NOWRITING: writing scenes are **excluded from veo** → hold still or **ffmpeg Ken-Burns only**. The plan’s own guard says **"NO legible text"** but not the animation exclusion.

**Schema gaps vs tooling expectations.** JSON `mvt` values are **"M1 The Picture"** (full labels) — workable but no `beat_id` (e.g. `M3-01`) as the skill specifies. Christ scenes lack **`jesus_variant`** (LF-SP-G7). No **`hero: true`** on S26. No documented path to **`paper_cohesion`**, gate pre-checks, or independent scene-plan audit — all mandatory in `/scene-plan-long` steps 6–7.

---

## Hidden risks & single points of failure

**Veo locomotion despite "FROZEN" guards — several scenes invite subject animation.**

- S3: **"the man half-turning to point the blame… the woman in turn gesturing"** — action verbs veo historically animates (confirmed Prodigal failure in `/animate-long`).
- S25: **"a single human figure beginning to step OUT from the deep shadow… toward… light, face lifting"** — direct locomotion; contradicts the header **"every subject… is FROZEN"** and LF-CLIP-NOLOCOMOT.
- S26: **"reaching one open pierced hand gently forward"** — reach/morph risk on face and hand (LF-CLIP-NOMORPH).
- S12: newborn in arms — infants are a known morph target.
- S9: **"bare human HEEL poised above its head"** — ambiguous actor (Eve? future seed?); veo may animate a stomp.

**Serpent discipline is repeated but brittle.** The serpent block appears in ~half the scenes. Even **"coiled and STILL… NOT writhing"** is a single veo hallucination away from a ruined clip; there is no fallback scene in the plan if veo morphs the snake (Bronze Serpent episode exists partly because serpent+veo is treacherous).

**Robed-cross NSFW workaround is assumed, not verified.** **"all crosses robed -> veo NSFW-safe"** — hybrid Kling fallback exists, but each fallback is another paid render + different motion discipline. Three crucifixion stills triple that exposure.

**S14 prompt defect:** **"distant robed the robed Christ CRUCIFIED"** — duplicated token will propagate into NBP/HF prompts and audits.

**S17 atmos copy-paste error:** **"the shaft of light strengthening over the heel and the still serpent"** on a church-under-cross scene — signals prompt hygiene failure and will confuse veo continuation prompts (`_animate_directional.py` feeds `atmos` into continuation motion).

---

## Cost / spend — materially underestimated

The artifact implies **26 stills + 26 veo clips**. Real pipeline math from `_animate_directional.py`:

- **14 `forward_slow` scenes** with windows **19–26.5s** each need **1 base + 1–3 `_contN` continuation clips** per scene.
- Rough total: **~26 base + ~30+ continuations ≈ 55–58 veo renders**, not 26.
- Stills: ~8 Christ/face @ $0.50 + ~18 neutral @ $0.30 ≈ **$9–10** images alone.
- `/cost` skill ceiling for long-form: **~$40/episode**. This plan, with zero reuse and heavy directional fill, is on track to **blow the ceiling** without a pre-flight quote — and the plan includes **no `/cost` step or LF-INV-7 test-gate** ("render 1–2 paid stills + animate BEFORE full batch").

Passover’s plan explicitly says **"windows kept <=~25s"** and favors boomerang for static beats. This plan pushes **14 directional fills** including S24 at **26.5s** — opposite of the proven cost-control pattern.

---

## Missing steps & verification gaps

| Required (spec/skill) | Present in artifact? |
|---|---|
| LF-SP-G1..G9 deterministic pre-check | No |
| `paper_cohesion` (blocking) | No |
| Independent scene-plan audit | No |
| LF-INV-7 test stills + 2 veo pilots | No |
| `/cost` pre-flight + user OK | No |
| `clip_reuse` / `bank` slugs | No |
| Quote-level visual sync proof | Claimed only |

**"every quote's visual matches its narration cue"** is asserted in the spine but not verified. Scene windows tile the **turn timeline** (`503.4s`), not individual KJV quote timestamps. With 3-voice turns and scripture tags, quote-accurate cuts need alignment evidence — none provided.

**Beat mismatch — S17.** Title: **"Under His feet — the church shares the victory"** (Rom 16:20 corporate crushing) is tagged **M5** (252.9–319.9s). In the locked narration, that Paul/church quote sits in **Movement 4 — The Centuries-Early Match**, before M5’s **"Now slow down, because there are real objections."** S17 will likely run under objection narration — a concrete sync failure against the plan’s own spine rule.

**LF-SP-G8 composition cap likely fails.** Intimate/CLOSE/close study/close hero scenes (S1, S5, S8, S9, S11, S12, S15, S19, S24, S25, S26) ≈ **11/26 = 42%** — above the **40% max per framing** at 26 scenes.

---

## Over-engineering / premature batch

Not over-engineered structurally — if anything it **over-generates** before proof:

- **26 scenes** when 23–25 would satisfy movement coverage.
- **Three crucifixion compositions** (S14, S20, S21) plus heel triptych (S9, S18, S19) before any pilot proves veo won’t morph crosses/snakes/hands.
- **Four garden→cross trajectory landscapes** (S13, S16, S23, plus S10) — high visual repetition (LF-SP-G3 risk) before one trajectory look is approved.

The plan skips the cheap validation loop and jumps to a **~$35–45+ full batch**.

---

## Reuse — duplicates existing tooling

- Ignores **`bank` / clip_reuse** pattern proven on Psalm 22 (#02).
- Ignores **`christ_risen_reaching_hand_hero`**, **`christ_crucified_*`**, Eden garden plates, empty-tomb dawn plates likely already in the growing long-form bank (RESUME.md: reuse bank is an explicit goal).
- `_build_scene_plan.py` is a **bespoke author** (fine for format incompatibility with `cli_visual.py`) but it **does not call reuse discovery** — duplicate spend vs the repo’s own lever.

---

## Doctrinal / arc notes (scene-level)

- **S14 crucifixion during M4** while narration still says *"No NT writer quotes Gen 3:15 word for word"* — visually front-loads passion before M5 steel-man; not heresy, but **undercuts the honest trajectory beat** that S13 was meant to serve.
- **S8** embeds **"'upon thy belly shalt thou go'"** while M3 narration’s 3:14 quote stops at **"field."** — minor text/sync drift.
- Closing on **risen Christ (S26)** satisfies LF-AS-G6 gospel-frame; **M7 invitation mirror (S23–S25)** is strong. The arc holds; execution gates do not.

---

VERDICT: REVISE
TOP FIXES:
1. **Fix gate failures before spend:** cut to **≤25 scenes**; add **3–5 named vignettes** to every "DEEP unified" scene (LF-SP-G6/G9) or reclassify; run LF-SP-G8 framing audit (intimate/CLOSE is **>40%**).
2. **Re-budget animation cost:** add **`bank`/reuse slugs** (especially S14/S20/S21/S26); convert S15 scroll to **ffmpeg-only**; reduce `forward_slow` count/window lengths — current plan implies **~55–58 veo renders**, not 26, and needs `/cost` pre-flight + LF-INV-7 pilots first.
3. **Fix narration-sync errors:** move **S17 (Rom 16:20 / "under your feet")** into **M4** timing; remove locomotion language from **S25/S3**; fix **S14 typo** and **S17 atmos** copy-paste; prove quote-level sync or drop the **"every quote's visual matches"** claim.
