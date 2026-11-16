# Independent review — cursor (OK, 85s)

## Independent adversarial review

### Feasibility and codebase drift

**“G5 website checks RETIRED … read pages / read_url are not gated”** (artifact `pipeline/release_state.py` hunk): only *piece-level* G5 checks were removed. `run_gates` still emits `SYNC-G5` WARN for **orphan read pages** (`test_g5_orphan_read_page_warns` unchanged). The pack overstates retirement while `release_check.py` still advertises **SYNC-G1..G7** and `v2/SPEC.md` still documents G5 FAIL rules (awakeden read URLs, frame freshness). GREEN after this change is partly **self-inflicted blind spot**, not proof packs/site are clean.

**YouTube-only tracking** (`TRACKED_PLATFORMS = ["youtube"]`, tracker copy “YouTube links only”): the **write path** is unchanged. `upload_tracker.py` still accepts all `PLATFORMS`, `--list` still prints four platform columns, and docstring example still shows `@awakeden` TikTok (line 14 in repo). Ledger can still accumulate TikTok/FB/IG while the UI ignores them—stale data and accidental `--set … tiktok` remain possible. `episode_state.shorts_posted_any` still treats **any** ledger key as “progress,” with comments still citing “24–48h cross-post lag” though CANON dropped that—board/episode copy can lie about campaign status.

**Hide/unhide** (`hide_btn`, `localStorage yt_tracker_hidden`): feasible but **not owner-grade** if they meant durable state. Per-browser only, no sync, wipes on cache clear. Hide applies only when `posted = bool(s.ledger.get("youtube"))` on cards in **Posted**—not a general “link is filled” control. Header **`Posted ({n_posted})` does not shrink** when cards are hidden; only CSS `display:none`.

**Burned logo “remove at $0” / 17-video patch**: thumbnails call `draw_wordmark` which **returns 0.0** (good for new JPGs), but `add_watermark.py` still overlays `_brand/awakeden_watermark_overlay.png`, and `brand_assets()` was **disabled** in `thumbnails.py`—no replacement Salt and Light Kingdom asset path. Any future run through the normal watermark step can still burn **Awakeden pixels**. The one-off ffmpeg mask script is **not** wired into `finality`/assembly; it assumes clean vs watermarked sources differ **only** in the logo box—hook/decode edits elsewhere break the mask logic (artifact’s own comment admits keeping re-cut diffs outside the box).

### Owner requirements vs what was actually proven

**“remove any reference … to AI, please recheck”**: `tools_strip_ai_wording.py` PAT only removes **two fixed sentences** (`Art…made with AI tools`). It does not catch variants, “AI-generated,” upload-kit gate text (“AI-slop typography”), or copy in paths skipped via `_pre_` (`_pre_redteam` still contains full AI disclosure lines in repo). Artifact cites clean `publish/*.md` samples but **no** automated post-check in `release_check.py` for AI/awakeden strings on shipped packs—one-shot scripts, then trust.

**“remove all of their reference completely” / Awakeden**: `tools_strip_awakeden.py` scopes to `"/publish/"`, `"/upload/"`, `publish_meta.json` and **skips `_website`**. Artifact admits **~547+ `awakeden.com` canonical URLs** remain in `_website`. `upload_tracker.py` still **rebuilds read pages** and updates manifest on every YouTube `--set`—continued coupling to the retired site, while the tracker flow **drops** “deploy `_website`” (step 4) but the CLI still says “deploy _website when the batch is finished.” Contradiction for anyone following the HTML loop only.

Stale Awakeden **outside** the strip scope exists today (e.g. `…/red_team_r2/_before_publish/PUBLISH_INDEX.html` with “Subscribe to Awakeden” and `awakeden.com`)—easy to open the wrong paste page even if canonical `publish/PUBLISH_INDEX.html` is clean.

### Verification theater

**“release_check.py after the change: 89 items, 0 FAIL, GREEN”**: presented as validation without stating that **G5 body checks were removed** and `publish_meta.read_url` / awakeden mismatches no longer FAIL. That GREEN does **not** verify owner asks 3–4 on locked episodes going forward—only that remaining gates pass.

**“pytest pipeline: 463 pass, 9 fail (pre-existing)”**: no mention of tests that **encode** old G5 behavior being replaced with “assert not hits … G5” rather than new invariants (e.g. “no awakeden in publish footer,” “no AI disclosure line”). Regression protection for the new rules is thin.

### Missing steps / edge cases

- **No mandatory republish**: `upload_brand.json` changed but artifact does not require regenerating every locked `publish/` pack and proving freshness (e.g. pack sha vs brand file). Samples prove two slugs, not the catalogue.
- **Multi-platform publish files still maintained** (tiktok.md / instagram.md in samples): consistent with “track YouTube only” but **not** with a literal reading of “just track youtube links”—operational ambiguity for whether non-YT packs should still be posted or deleted.
- **Partial ledger migration**: shorts with only legacy TikTok/FB/IG ledger entries may show as unposted on YouTube while `shorts_posted_any` shows progress—no cleanup/migration step documented.
- **`data/upload_brand.json` `website: ""`**: footer_order drops `website` but TikTok/IG/Facebook handles remain filled—future regen may still stamp long brand footers on non-YouTube artifacts the owner may not want to maintain.
- **Instagram handle `@salt.andlightkingdomorg`** (owner choices + brand JSON): unusual tokenization; no verification step that handles match real accounts (typo risk).

### Reuse / duplication

New `tools_strip_awakeden.py` overlaps `tools_strip_ai_wording.py` (both full-tree `rglob`, similar SKIP lists). Reasonable for a one-off, but **no shared lint** invoked from `release_check.py` or publish stage—duplicated one-shot tools instead of one `$0` public-text gate (the codebase already has upload kit gates; they weren’t extended for “no awakeden / no AI sentence”).

### Cost

Spend is mostly $0 scripts and 17 re-encodes—appropriate. Risk is ** false economy**: disabling G5 + declaring GREEN avoids Opus/site work but leaves **awakeden.com** live in `_website` and in watermark assets, so later fixes may cost more than a scoped site/brand migration plan upfront.

---

VERDICT: REVISE  
TOP FIXES:  
1. Align enforcement with owner rules: add a deterministic `$0` scan (or extend `release_check` / upload UK gates) for **no `awakeden` / no AI-disclosure sentences** on all **shippable** paths (`publish/`, `upload/`, `PUBLISH_INDEX.html`), not one-off strip scripts—**do not** cite GREEN after weakening G5 without saying so.  
2. Finish the logo story: disable or retarget `add_watermark.py`, regenerate `_brand` assets (or remove burn-in from the pipeline), and document which finals still carry Awakeden on disk vs the 17 patched files—`draw_wordmark` no-op alone is insufficient.  
3. Make “YouTube-only” consistent end-to-end: narrow `upload_tracker.py` `--set`/`--list` to tracked platforms (or WARN on non-YouTube), migrate/ignore legacy ledger keys, update episode rollup copy, and fix the tracker loop vs `upload_tracker` deploy/read-page behavior so operators are not told to skip deploy while the CLI still rebuilds awakeden read pages.
