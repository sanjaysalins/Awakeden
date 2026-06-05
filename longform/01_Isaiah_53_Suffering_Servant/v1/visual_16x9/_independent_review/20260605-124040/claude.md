# Independent review — claude (OK, 139s)

Verified the plan against the actual code. Findings below cite exact lines.

## Feasibility checks (what I confirmed)

- **21 stills confirmed** (PNGs `01`–`21`). KEEP(14)+REDO(5)+MINOR(2)=21 — the audit math is honest.
- `_render_images_16x9.py`, `_assemble_16x9.py`, `_animate_directional.py`, `_retime.py` all exist. The directional re-chain tool for S13 is real.
- veo NSFW→Kling fallback is moot here — none of the 5 redo scenes is the bare-torso cross (S6/S16 are KEPT). Good.

## Concrete findings

**1. (BLOCKER) The redo will silently render nothing.** `_render_images_16x9.py:80` — `if png.exists(): skip`. The script is idempotent by PNG existence. Section 4 calls this "the existing `_render_images_16x9.py` path" and RT8 only deletes the stale `_cont*` **clips** — nowhere does the plan delete the stale **PNGs** for S1/S3/S10/S13/S15. Re-run as written → all five skip → zero re-renders. Deleting the target PNGs is a mandatory, missing step.

**2. "Existing path" oversells reuse — the audit/retry loop is NOT on this path.** Section 4 promises "Per-PNG Claude Vision content audit … retry-on-fail with a hard cap of 3 attempts/scene." But `_render_images_16x9.py:90-99` only does `write_bytes` + `bank` — **no audit, no retry**. `verify_image` exists in `visual_render.py` but is never called by the long-form script. So refs + audit + retry + montage QC are *all* net-new code on this path, not "extend the driver." The plan reads as a small tweak; it's a re-plumb.

**3. Multi-ref role confusion (RT3 under-scoped).** `NBPProvider.generate` (`visual_render.py:154-159`) attaches **exactly one** ref — the jesus variant. The plan wants a STYLE ref (S6/S4) **plus** a CHARACTER ref (S14) **plus** the existing jesus ref = up to 3 unlabeled images in `parts`. Gemini multi-image with no per-image role text risks identity bleed (S14's Ethiopian face contaminating Christ; S6's composition overriding the new scene). The plan never says how each ref is role-labeled in the prompt.

**4. Image attempts are capped; animation is not.** RT6's "hard cap 3 attempts/scene" is **image-only**. There is no cap or budget line for veo re-animation. Section 6 costs ~7 clips assuming one success each. Given RT4 (veo over-animates), the unbounded loop is on the *animation* side, not the image side — the cap is on the wrong stage.

**5. S3/S15 motion contradicts the locked veo finding.** S3 MOTION = "exalted figure … slow rise"; S15 = "luminous figure of Christ … rises." CLAUDE.md's locked verdict: veo *invents subject motion* ("the father actually ran"). A figure that "rises" is subject motion — veo's exact failure mode. Mitigation (camera-only/push-in fallback) rests entirely on manual montage QC, which combines badly with #4's missing retry budget.

**6. Library re-banking is unaddressed.** `_render_images_16x9.py:96` `bank()` runs on every fresh render and `import_file`s into `image_library` under the same slug (e.g. `wilderness_dusk_lone_figure`, scope `neutral`). Re-rendering S1 silently overwrites/duplicates the banked reusable plate with the new epic version. Given the topical-fit gate discipline, this needs an explicit decision, not a silent side effect.

**7. (Minor) "only the changed scene segments differ" is misleading.** `_assemble_16x9.py` re-scales/re-concats every scene each run (`:50-98`); it's a full re-assembly, not a targeted segment swap. Harmless, but the claim isn't true.

## What's right
Visuals-only blast radius, audio/soundstage/windows untouched, backups kept (RT10), faithful to locked rules (KJV, 1st-c dress, no frames, close-on-Christ), and genuinely red-teamed (RT1 premature-cross-reveal and RT7 S3-pre-reveal are sharp catches). Cost ~$10–15 is justified and bounded on the image side. Open questions #1/#2 are legitimately panel-worthy and correctly left open.

VERDICT: REVISE
TOP FIXES:
1. Add the missing mandatory step: delete the stale PNGs for S1/S3/S10/S13/S15 before re-running (the script skips existing PNGs at `_render_images_16x9.py:80`), and decide whether to re-bank or preserve the original `image_library` plates.
2. Scope the driver work honestly: the audit + 3-attempt retry + multi-ref attach are net-new on `_render_images_16x9.py` (not "the existing path"), and the STYLE vs CHARACTER vs jesus refs must each be role-labeled in the prompt to prevent identity bleed.
3. Add an animation-attempt cap/budget for veo (mirroring the image cap) — the real morph/over-animation risk (RT4, and S3/S15's "rising figure") is on the animation stage, which is currently uncapped.
