# Awakeden website — session handoff (2026-06-20)

Read this first for any **www.awakeden.com** work. The video pipeline is separate
(see `RESUME.md` / `STATE.md`). Memory: `[[awakeden-catalogue-placeholders]]`.

> **When the user says "update website" → run the `/update-website` skill**
> (`.claude/skills/update-website/SKILL.md`). It encodes the full loop: orient on this
> doc → find the delta (below) → wire `manifest.yaml` → cut-outs + OG card → build
> (slop guard) → verify → commit `_website` + push to `main` (Netlify deploys). Start
> by reading this doc's **OPEN ITEMS / TODO** to see what's still outstanding.

## What it is
Static catalogue + study site for the Awakeden gospel-shorts series.
- **Live:** https://awakeden.com (apex is canonical) · also https://awakeden.netlify.app
- **Repo:** `github.com:sanjaysalins/Awakeden.git`, branch `main` (THIS repo = `JesusInTheBible`; Netlify publishes only the `_website/` dir).
- **Local:** `C:\Users\sanjay\PycharmProjects\JesusInTheBible\_website`
- **Host:** Netlify (auto-deploys on push to main) · DNS on Cloudflare (grey-cloud, www→apex). **noindex is OFF — the site is indexable.**

## Build / preview / deploy
```
.venv\Scripts\python.exe _website\build_catalog.py          # build (has a fail-closed AI-slop guard)
cd _website && python -m http.server 8080                   # preview at http://127.0.0.1:8080/
# Netlify runs build_catalog.py itself on every push; just commit + push to deploy.
```
A local preview server may still be running in the background from this session — restart it if not.

## Current state (42 catalogue items, 6 series)
- **11 rich v2 studies** (the showcase): Psalm 22 ×9 (long + 8 shorts) + Isaiah 53 + Zechariah 12:10. Full illustrated "study behind this" pages. (Psalm 22 #2 "Mockers' Words" now sourced from its v2 reprocess `v2/pilot/mockers_words_ps22/v1`.)
- **31 placeholders** (back-catalogue): real title/verse/series/hook, SVG card, `in_production`/`planned`. NO study page yet.
- Series: jesus-in-ot 16 · i-am-sayings 9 · questions-jesus-asked 8 · miracles-of-jesus 3 · parables-of-jesus 3 · people-who-encountered-jesus 3.

### Promote-delta (the migration is the work)
The catalogue tracks the v2 migration; the delta = finished v2 narration folders not yet wired to a rich page. To find it: glob finished folders (`v2/pilot/**/v1/narration.md`, `longform/**/v1/narration.md` with a `visual/nbp/` still set + `.locked`) and compare against the `study_source`/`preview_source` paths in `manifest.yaml`. Anything finished but unwired is a promote candidate (see `/update-website` step 1). Already promoted: Isaiah 53, Psalm 22 (long + 8 shorts), Zechariah 12:10.

## THE MODEL (don't break this)
The catalogue is a **public tracker of the v2 migration**. Back-catalogue pieces (in the SEPARATE `PythonProject1/jesus/narration/` repo, OLD format) stay placeholders. **When the v2 pipeline re-processes a piece**, give its `manifest.yaml` item a `study_source` (in-repo v2 narration folder) + a real `preview_source`, rebuild, and **its rich page builds itself**. Do NOT retrofit the old format.

## The rich study page (how it's built — all in `_website/`)
- `build_catalog.py` — `load_study()` parses `narration.md` (v2 format: `**[speaker — KJV, Ref]**` + `## MOVEMENT`), `render_study_html()` (setting + Prophecy→Fulfilment two-panel + reading), `build_study_figures()` keyword-matches scene paintings to narration moments (long-form pools stills from sibling shorts).
- `make_cutouts.py` — LOCAL tool (needs `rembg`, already pip-installed): background-removes clean single-figure Christ paintings → `assets/study/<slug>/cut/*.webp`; the page floats them with CSS `shape-outside` so text wraps the silhouette. Run BEFORE build. Quality gates: single-subject dominance + halo cleanup + multi-figure slug exclusion.
- Study assets are committed (`assets/study/`, `assets/og/`, `assets/previews/`) so Netlify serves them without the source media (which is gitignored). `.gitignore` has explicit re-allow rules for these after the media-ignore block.

## Other tools / files
- `import_catalogue.py` — regenerates the 31 placeholder manifest items from the back-catalogue folders (no media copied).
- `manifest.yaml` — the catalogue source of truth (items + roadmap + clusters). `config.yaml` — brand/site. Both are human-edited.
- `make_og_cards.py` — per-study 1200×630 social share cards. `assets/og-cover.jpg` — the site-wide card.
- SEO: OG/Twitter/JSON-LD on every page; favicon; sitemap; 404.html. `netlify.toml` blocks source files + sets HSTS.

## GOTCHAS
- **AI-slop guard** (`check_ai_slop` in build_catalog): em-dashes, en-dashes, curly quotes, ellipsis (+ HTML entities) FAIL the build in any shipped `.html`/`.yaml`. Use commas/colons/periods + straight quotes. Authored narration is auto-normalised via `slopless()`.
- **rembg / cut-outs** run LOCALLY only (commit the webp results); Netlify never runs them.
- **Mobile:** cut-outs stop floating ≤640px (centered). Cut-outs anchor before a prose block so text wraps cleanly.
- **Internal docs** (`COPY_REWRITE.md`, `_independent_review/`) are gitignored so they don't deploy. This handoff lives at the repo ROOT (outside `_website`), so it isn't published either.

## OPEN ITEMS / TODO
1. **User's two pre-existing-copy flags** (their call, not auto-changed): Psalm 22 hook "before *Rome invented it*" (historically brittle — crucifixion predates Rome); the "Who do you say I am? / Why are you afraid?" series titles are modern paraphrase not KJV verbatim.
2. **Series mapping** of placeholders is best-effort — spot-check when browsing; one-line `series_id` fixes in `manifest.yaml`.
3. **Untracked side-effect files** in the repo root from the `npx skills` install: `skills/`, `skills-lock.json`, `data/skills/`, `CONTEXT.md`, `agent/` — NOT committed; gitignore or remove if unwanted.
4. **Going live on YouTube:** when a video publishes, set its item `youtube_id` + flip `config.yaml` `site.mode: live`; the work page then embeds it.
5. **Google Search Console:** add `awakeden.com`, submit `sitemap.xml`, request indexing (user action).
6. **Catalogue UX (optional):** cards don't show a series label/grouping yet; nav still has a Psalm-22-specific link.

## Session log (2026-06-20b)
Promoted two finished v2 pieces to rich pages: **Zechariah 12:10 "The One They Pierced"** (new card, `jesus-in-ot`, added the `zechariah` `STUDY_SETTING` paragraph in `build_catalog.py`) + **Psalm 22 #2 "Mockers' Words"** re-pointed to its v2 reprocess. Built + verified + deployed (commit `6a3bf27`). Added the `/update-website` skill (`.claude/skills/`, gitignored/local). Last commit: `6a3bf27`.

## Session log (2026-06-20, what shipped)
Whole-Bible copy reframe (red-team + 5-CLI panel) → AI-slop guard → warm light "gallery" theme → kinetic scroll-reveal → Netlify deploy prep → fixed apex/www redirect loop → full SEO + indexable + per-study social cards → real preview images (all 10) → rich illustrated study pages (prophecy device + reading + contextual paintings + rembg cut-outs with text-wrap) → 31 back-catalogue placeholders (v2-migration tracker) → series-mapping fixes. Last commit: `ee71cc2`.
