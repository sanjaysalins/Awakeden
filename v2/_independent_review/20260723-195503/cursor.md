# Independent review — cursor (OK, 112s)

Independent adversarial review of the v0.3 DNA plan, checked against `pipeline/visual_render.py`, `config.py`, `_remotion/`, and the `_retro_dna/` ad-hoc scripts.

---

## Feasibility — claims vs. what actually exists

**§1 “Character drift FIXED” / “proven to hold the same man across 3 scenes” (lines 17–19, 68–69)** — Overstated evidence. `_prove_it.py` renders three Christ poses from one ref (`christ_hero`, welcome, cross). That is a smoke test, not a lock: no Aaron, no oblique lighting, no crowd occlusion, no re-run blind audit. Three PNGs do not justify **“Character lock (MANDATORY)”** (§1, line 68).

**§1 “`seedream_v4_5` = neutral plates only” (line 19) vs. what the POC actually shipped** — The living POC contradicts this. `_dnapoc_animate.py` animates `crucifixion_crowd__seedream_v4_5.png` and `atonement_crowd__seedream_v4_5.png` — multi-figure seedream plates that almost certainly include Christ/onlookers, not “backgrounds with no recurring named character.” The plan’s two-model rule is not what the demo used.

**§1 HF `nano_banana_pro` vs. production `NBPProvider` (lines 58–62)** — Correct that they diverge, but the gap analysis is incomplete. `NBPProvider.generate()` already attaches `refs/ref_jesus_<variant>.png` when `scene.jesus_variant` is set (`visual_render.py` 169–172). Production has a ref path for Christ on NBP; the DNA recipe locks HF subprocess ref-chaining. The plan never picks a single production provider or explains migrating off the living `graphic_novel` registry entry (`config.py` 487–490: still = `seedream_v4_5`, anim = `cinematic_studio_video_v2`).

**§1 “`render_scene()` never passes `HFProvider.extra_ref_paths`” (lines 71–72)** — Verified. Line 592 calls `provider.generate(scene, audit_feedback=feedback)` with no refs. But the fix is smaller than “BUILD from scratch”: wire `scene`-level ref metadata (or reuse NBP’s `jesus_variant` pattern) through `render_scene()`. The plan treats this as greenfield while half the plumbing exists on the NBP side only.

**§3 “Kalam-Bold.ttf / Kalam-Regular.ttf in `_remotion/public/` … ✓ in repo” (lines 118–119)** — Not reproducible from git. `git ls-files _remotion/public` returns nothing; components load fonts via `staticFile("Kalam-Bold.ttf")` etc. Fresh clone → Remotion render failure unless fonts are manually vendored. Correcting an earlier false “missing” claim created a new false “in repo.”

**§8 Cast reference bank “`christ_pc_ref.png` only” (line 224)** — Partially wrong. `_painted_comic_test.py` was written to bootstrap **both** Aaron and Christ refs (`aaron_pc_ref.png`, `christ_pc_ref.png`). The plan acknowledges Aaron’s “bare muscular arm” defect (§1, line 73) but still understates that painted-comic ref infrastructure already tried to solve Aaron — and those PNGs are not in git (media untracked).

**§6 “Word-timed panel slams are a TARGET, not yet built” (lines 207–209)** — Honest, but it undermines §5’s tier grammar (“cliffhanger bottom-right”, beat-mapped 6/9 grids). `EW01Slices.tsx` line 114–115 confirms **“40% into the scene window (approx; no forced alignment)”**. A pilot built on current Remotion code cannot validate the comic grammar the plan sells in §5.

---

## Hidden risks & single points of failure

**§1 print-finish on animation / dot-crawl (lines 84–86) vs. §6 + shipped POC** — Internal contradiction. §1 warns a fixed screen-space dot grid will moiré on motion and says finish is **“NOT yet proven on animation.”** §6 still says **“print-finish over the top.”** Meanwhile `DnaSplashHook.tsx` already stacks screen-space `Grain` + `Misregister` over animated `OffthreadVideo` (lines 140–154, 292–293) — exactly the risky pattern §1 flags. `_dnapoc_animate.py` comment claims baked-in seedream dots avoid crawl, but the Remotion hook adds a *second* print layer on top. No mandatory bake-off gate before §9 spend.

**§5a Body gate — Vision-only (lines 131–133)** — Passion Christ relies on Vision audit + banned prompt tokens (`muscular / heroic / six-pack`). `config.VISUAL_BANNED_TOKENS` has `gore`, `blood spatter` but **not** `muscular`, `heroic`, `six-pack`, `athletic` (`config.py` 523–534). Combined with §1’s seedream **“no true negative-prompt channel”** (lines 80–82), passion crosses are two fragile mechanisms stacked. One successful `_prove_it/christ_cross_marred.png` is not a gate.

**§1 luminance-only dot mask “naive” (lines 82–83)** — Correct self-critique, but **`rembg` face exclusion is listed as “the real fix” with no pilot step, cost, or failure mode.** Night frames and bright desert frames will still break reverence rules silently.

**§9.3 format split vs. locked comic-grid discipline** — **“full-bleed single-focal-point for 9:16 Shorts (no tier grids / page-turns on a phone)”** conflicts with workspace rules requiring real animated panels in comic grids for 9:16, panel-variety lint, etc. The plan never states which standard wins for shorts that ship through the living-page lane (`v2/SPEC.md` §2L).

**§9.2 cold-audience A/B** — **“the same piece cut two ways: retro-comic vs. plain cinematic-inked”** implies a full second still set + second assembly path. §9’s **“3-piece pilot ≈ $45–75”** (lines 178–179) budgets one look only. A/B real cost is closer to 2× stills + 2× Remotion/livingpage builds + traffic tooling — not mentioned.

**§10 lock process — “free audience kitsch-test” (line 289)** — Undefined: platform, N, duration, what “kill” means, who cuts the asset. §10 also admits **“A/B protocol sample-size/kill-criteria”** still open (line 291). Scheduling pilot after a vague free test is process theater.

---

## Over-engineering / premature build

**§10 `/dna-check` (lines 296–303)** — Proposed before the look is locked, and mostly duplicates existing tooling (`check_landing_hold.py`, watermark, `validate`, render lint). Worse: the plan correctly admits it is **“mostly provenance stamping, not look-verification”** — so building it now adds ceremony without enforcing the DNA substance (dots-on-faces, Scripture treatment, Christ register).

**§8 incorporation map — website + thumbnail retro skin (lines 226–227)** — Listed as BUILD alongside core identity work, before pilot/A/B proves the look survives YouTube compression (§9.3 itself says halftone dies at 168px). Skin work before audience signal is scope creep.

**Three (four) print-finish stacks** — §1 names `_print_finish.py`, `panel_animator/print_grade.py`, `_retro_grade_demo.py`, plus Remotion `Grain`/`Misregister`. §8 marks reconciliation as BUILD but the POC already uses the non-canonical Remotion stack. Pilot will cement the wrong path unless reconciliation is a **hard prerequisite**, not a “before lock” item.

**§8 “~55% owned, ~45% to build” (line 231)** — Optimistic. Genuinely missing for the *promised* identity: production ref wiring, Aaron/cast bank, balloons, 6/9-tier grid, page-turns, word-synced slams, one print pass proven on motion, livingpage integration, long-form Christ bookend gate, deterministic passion tokens. What exists is a **16:9 Remotion POC** (`DnaPocFilm`, `DnaSplashHook`), not a shippable lane.

---

## Missing steps, edge cases, verification gaps

**No integration plan with the shipping lane** — `v2/SPEC.md` §2L: living-page via `cli_livingpage.py` + `build_livingpage_16x9.py` is what ships today. This DNA plan lives in `_remotion/` ad-hoc compositions. Nowhere does it say: extend livingpage, replace it, or fork a new `cli_*` entry. Pilot pieces will be assembled by hand unless this is specified.

**§5 “long-form Remotion path needs its own bookend check — coverage gap” (line 122)** — Acknowledged but not scheduled. AS-G6/G7 exist for shorts assembly; long-form retro has no gate ID, no owner file, no test.

**§9 “Cluster-1 scale, a handful of pieces” (line 173)** — No named pieces, no scene count, no Remotion vs. livingpage choice, no definition of “done” for a pilot episode (stills only? scored mp4? upload-ready?).

**`_seedream_ref.py` ignored** — Repo contains an active test of **seedream + chained Christ ref** (4 jobs including cross). Plan locks seedream to neutral plates without citing pass/fail of that experiment. If seedream+ref works, the two-model cost split collapses; if it fails, that should be evidence against using seedream for any Christ-adjacent crowd plate.

**§2 palette “single source of truth” (line 91)** — Good intent, but no automated check that `DnaSplashHook.tsx` constants (`CAPTION_YELLOW`, `PROCESS_CYAN`, etc.) match the table hexes. Reference card drift already happened once; no lint proposed.

---

## Reuse — duplicating instead of extending

**Ad-hoc `_prove_it.py` / `_painted_comic_bright.py` vs. `/painted-comic` skill** — The painted-comic skill already documents HF `nano_banana_pro` + repeated `--image` ref chaining (skill lines 57–64). DNA R&D reimplemented that in `_retro_dna/` instead of extending the skill with a retro STYLE BLOCK variant and one shared ref-bank module.

**Ref-chain BUILD item vs. existing NBP path** — Plan asks to wire HF refs through `scene_plan` + runner while NBP already chains Jesus refs via `jesus_variant`. Two parallel consistency systems unless one is deprecated explicitly.

**§6 “Port the livingpage word-timing into the retro Remotion path” (line 208)** — Correct direction, but no mention of reusing `build_livingpage_16x9.py` forced-alignment output or beat specs (`livingpage_short.spec.json` pattern from SPEC §2L). Risk of a third timing system in `_remotion/` only.

---

## Cost / spend — understated or misaligned

**§9 “~$15–25/piece” with “~18–20 stills+clips/piece” (lines 176–178)** — EW01 painted rebuild plans ~25 stills; long-form Remotion slices (`EW01Open`, `EW01Climax`) use multi-minute windows over 5s clips with stretch — animation count ≠ scene count. Budget may be low.

**§9 animation line “Seedance/Kling tiering” (line 178)** — Misaligned with production registry: `graphic_novel` anim model is `cinematic_studio_video_v2`; locked long-form norm elsewhere is `veo3_1_lite`. DNA POC used `kling3_0` + `seedance1_5` (`_dnapoc_animate.py`). Pilot cost quote mixes three different animation stacks without picking one.

**§10 `/dna-check` Vision substance (lines 299–302)** — Paid Vision on “dots visible but faces flat”, “Christ dignified + marred-not-heroic”, etc. per episode is not in §9’s $45–75 pilot envelope.

**§10 correction on R&D spend (lines 307–309)** — Good honesty that bake-offs already spent. Weak follow-through: no cumulative ledger line item or cap before “explicit OK per [[feedback-ask-before-spending]]” beyond pilot batch.

---

## What the plan gets right (still not PASS)

- Corrected the false Seedream identity claim (§1 correction block, lines 54–57) — verified against `_prove_it.py` line 19.
- §0 “system with range, not dial-to-11” matches what `_print_finish.py` and restrained prompts actually do.
- §6 honesty on approximate 40% timing matches `EW01Slices.tsx`.
- §9 “do NOT lock 76 episodes yet” and kitsch skepticism are the right strategic posture.
- §10 admission that `/dna-check` is mostly provenance, not look verification, is rare good discipline.

Those are necessary corrections, not sufficient to lock or greenlight spend. The plan still describes a Remotion POC aesthetic while the repo’s shipping contract is the living-page lane, with unresolved provider split, unproven motion print-finish, and an A/B protocol that doubles work without a budget line.

---

VERDICT: REVISE
TOP FIXES:
1. **Pick one production path before pilot** — resolve HF `nano_banana_pro` vs. NBP vs. registry `seedream_v4_5`, wire ref-chaining through `render_scene()` (or standardize on NBP `jesus_variant`), and state whether pilot runs via `cli_livingpage`/`build_livingpage_16x9.py` or `_remotion/` only.
2. **Make dot-crawl + print-finish a hard $0 gate before any pilot render spend** — reconcile the four stacks (three Python + Remotion Grain/Misregister); ban screen-space halftone over video until a clip bake-off passes; align §6 with §1 (bake into plates OR per-frame, not both).
3. **Rewrite §9 pilot + A/B as a funded experiment with kill metrics** — dual-cut cost (~2× stills/assembly), named pieces/scene counts, sample size & cringe/kitsch kill criteria, deterministic passion tokens in `VISUAL_BANNED_TOKENS`, Aaron ref in scope, and vendored fonts tracked in git or documented as a blocking dependency.
