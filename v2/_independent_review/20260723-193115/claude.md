# Independent review — claude (OK, 530s)

# Independent adversarial review — AWAKEDEN COMIC DNA v0.2

I checked the plan's factual claims against the actual repo state, not just the prose. Several are wrong or already stale.

## 1. The core "PROVEN FIXABLE" claim is internally contradicted — and wrong

Lines 15-17 correctly attribute the character-drift fix to **`nano_banana_pro`** with a chained `--image` ref, and explicitly say `seedream_v4_5` = "neutral plates only." But §1 (lines 54-65) then locks the recipe as **"Model = `seedream_v4_5` for EVERYTHING"** and claims (line 62): *"proven: Seedream 4.5 + `christ_pc_ref` held the SAME man across hero / welcome / teaching / cross."*

I read `longform/EW01_Two_Goats/_retro_dna/_prove_it.py` — the actual script behind that claim. `MODEL = "nano_banana_pro"` (line 26 of that file), and all three JOBS (`christ_hero`, `christ_welcome`, `christ_cross_marred`) render on it. The spend ledger confirms: three `nano_banana_pro` entries tagged `[prove-it]` at 11:37-11:40, none on `seedream_v4_5`. **The multi-scene character-consistency proof was never run on Seedream 4.5.** The doc contradicts itself two paragraphs apart, and the wrong half is the one stamped "LOCKED." This matters because character-lock is the single most safety-critical blocker this whole document exists to close — and the recipe it locks was never tested against it. It also silently changes the cost model: `nano_banana_pro` is 2 HF credits ($0.30) vs `seedream_v4_5`'s 1 credit ($0.15) per `pipeline/cost.py` / the ledger — so "cheap ($0.15)... for EVERYTHING" (line 56) doesn't hold for any scene with a recurring character, which per SP-G9 is most of them.

## 2. The Incorporation Map (§8) is already out of date

Lines 199, 201-202 mark the narrator caption box, SFX overlays, and tier/grid panels as **BUILD** ("CSS mockup only" / "not built" / "`EW01Slices` is full-bleed, has NO grid"). I read `_remotion/src/DnaSplashHook.tsx`, mtime **2026-07-23 19:24** — four hours *after* this doc's own mtime (15:37). It already contains a working `CaptionBox` component matching §3 exactly (Kalam, top-left, italic caps, `#FFE100`), a split-panel tier system with a torn-ink `Gutter`, and an `ImpactBurst` ink-star SFX component. The map cites `EW01Slices.tsx` as its evidence for "no grid" while ignoring the file sitting right next to it that already has one. The "honest ~40% owned" correction — the document's own selling point over the "optimistic 80%" draft — is stale before it reaches the external panel, which will now be reviewing a scope/cost estimate built on outdated ground truth.

## 3. A specific claimed gap doesn't exist

Line 123 and line 203 both flag **"`Kalam.ttf` not yet in `_remotion/public/`, acquire it."** `_remotion/public/Kalam-Bold.ttf` and `Kalam-Regular.ttf` are both already present and already loaded/used in `DnaSplashHook.tsx` and `DnaPocFilm.tsx`. Minor on its own, but it's the second factual miss in the same "honesty" table, which undercuts the credibility of the one section (§8) whose entire purpose is to be the trustworthy build/no-build inventory.

## 4. No dollar figure for the pilot

§9 (lines 222-227) commits to building a "PILOT batch (~Cluster-1 scale)" with real renders, and line 261 says "Nothing costs render money until the pilot" — but no episode count × per-still cost × per-episode estimate is ever stated. CLAUDE.md's own standing rule (`feedback-ask-before-spending`) requires a quote + explicit OK before any metered batch. Given finding #1 (character-locked Christ scenes actually need the pricier `nano_banana_pro`, not the quoted `seedream_v4_5`), the real pilot cost is both unstated and understated by the recipe as currently written.

## 5. Two things are both called "nano_banana_pro" and the plan never reconciles them

`_painted_comic_bright.py` / `_prove_it.py` call `nano_banana_pro` through **`hf generate create`** (HF-billed, $0.30/still). But the existing `NBPProvider` in `pipeline/visual_render.py` (referenced via `[[locked-stills-provider-split]]`, which this doc cites at line 16 and 64) is a *different* code path — direct `google.genai gemini-3-pro-image-preview`, Google-billed at $0.50/still per that memory. The plan treats these as the same lineage without saying whether the pilot uses the HF path, the Google path, or whether they even produce equivalent output. That's a real ambiguity feeding into a "LOCKED" decision.

## Secondary gap
§6 discusses motion/print-finish risk on animated panels but the plan never states which video-generation model actually animates the new-style stills (Seedance vs Kling vs the `cinematic_studio_video_v2` already in `STYLE_REGISTRY["graphic_novel"]`), despite the whole point being a look that feeds a motion-comic pipeline. Worth a line before the pilot, not necessarily a blocker.

---

VERDICT: REVISE
TOP FIXES:
1. Re-run (or correctly re-attribute) the character-lock proof: either prove `seedream_v4_5` holds a character across scenes, or change §1's locked recipe to `nano_banana_pro`-for-recurring-characters / `seedream_v4_5`-for-plates (matching the doc's own §Red-team-outcome), and correct the cost model accordingly.
2. Refresh §8's Incorporation Map against current repo state (`DnaSplashHook.tsx` already implements the caption box, tier grid, and an SFX burst component) before this goes to the external panel — the "~40% owned" number is stale.
3. Attach a real dollar estimate (episode count × corrected per-still cost) to the PILOT batch in §9, per the project's own ask-before-spending rule.
