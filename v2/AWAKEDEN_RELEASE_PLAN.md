# AWAKEDEN RELEASE PLAN — from validated pilots to a publishing engine (v1)

> Date: 2026-07-03 · Decided with the user (objective / cadence / website scope / platform
> all chosen explicitly). Companion to `BATCH_PLAN.md` (the 7-cluster build slate),
> `v2/EYEWITNESS_FOUNDATION.md` (the signature format) and `v2/LIVINGPAGE_STANDARD.md`
> (the craft bar). This doc governs WHAT ships, WHEN, WHERE, and what the website is FOR.

---

## 1. The objective (decided: MINISTRY REACH FIRST)

**The mission (user, 2026-07-03 — this is the spine of everything):**
*Finding Jesus in the whole Bible — Old Testament and New. How people SAW him, and how
events LED to him. The end of every piece is the same: the viewer finds and knows Jesus
better, from both Testaments, with fresh perspective — fully and completely grounded
and rooted in the Bible.*

**One line for the public:** *Awakeden — finding Jesus in the whole Bible, one panel at a time.*

Three lenses every piece uses (they ARE the content styles we've validated):
1. **He is THERE** — Jesus in the OT: shadows, types, prophecies (Zech 12:10, Psalm 22,
   the two goats, the bronze serpent...).
2. **They SAW him** — through people's eyes: eyewitnesses, the thief, Mary, Simeon,
   Peter in the garden (the POV/eyewitness device).
3. **It LED to him** — events and threads that walk forward to Christ (thirty pieces of
   silver, Passover → the cross, creation → "It is finished").

- **Optimize for:** watch-through, shares, and the CTA landing on Christ. Every piece
  lands on Jesus (non-negotiable, unchanged). Fresh perspective is always about the
  TEXT, never a new "truth" — grounded in the Bible is the whole game.
- **Second:** a platform-proof home base — awakeden.com + an email list. YouTube can
  change the rules; the list and the site cannot be taken away.
- **Last:** revenue (AdSense/memberships) exists only to fund production. It never
  shapes the CTA, the doctrine, or the cadence. Grace-anchored stays law.

**Success metrics (checked monthly):**
1. Average % watched on shorts (target: >70% at 60s) and swipe-away rate in first 3s.
2. Shares + saves per 1k views (the "worth passing on" signal).
3. Site sessions on Read-pages + email signups.
4. Slate health: pieces published vs. pieces in the bank (never publish the last piece —
   keep ≥3 weeks of runway banked).

## 2. Positioning (what we project)

- **The lane:** hand-inked Bible storytelling with word-timed panel choreography,
  verbatim KJV red-letter bars, and sound doctrine. Not AI-slop POV content, not
  lecture essays. NOTE (user, 2026-07-03): it is NOT strictly "a comic" — the ink
  is the DEPICTION STYLE across every layer.
- **The three-course strategy (user, 2026-07-03 — the shape of the whole brand):**
  the 60s SHORTS are the quick snack · the 10-min LONGS are the pudding · the
  WEBSITE is the MAIN MEAL — the place people sit down and actually read and study
  deeper. The site is the destination, not the companion; shorts and longs feed it.
- **Wordmark:** in AWAKEDEN, the word EDEN stands out (AWAK + emphasized EDEN)
  everywhere the name appears.
- **The promise a viewer learns to trust:** every short is 60 seconds, every panel is
  drawn, every quote is the actual Bible, and every story ends at Jesus — and you will
  keep seeing Jesus in places of Scripture you never noticed him before (both Testaments).
- **The website's framing follows the mission, not the format:** the site already says
  "Find Jesus in the whole Bible" — that stays THE headline; the comic identity is how,
  not what.
- **Voice:** reverent, punchy, never clickbait about the TRUTH (freshness lives in the
  entry point, orthodoxy in the claim — unchanged from v2/SPEC).

## 3. The two products (both validated)

| | Living-page SHORT | Inked LONG |
|---|---|---|
| Pilot | Cluster 1: 8 Cross shorts (LOCKED d6e294b) | Psalm 22 16:9 living-page + EW eyewitness longs |
| Shape | 9:16 · ~60s · hook→turn→CTA · punch grammar | 16:9 · 9–12 min · 7-movement / eyewitness spine |
| Cost | ~$5.20 MEASURED (cluster-1 ledger: ~$31 / 6 new pieces; falls with reuse) | ~$20–40 |
| Role | The snack/trailer — discovery | The meal — depth, retention, the site anchor |

*Cost note (panel-checked): the legacy "~$23/episode" model in CLAUDE.md is the old
Baroque pipeline (API Opus planning + ~16 fresh Kling clips per piece). The living-page
short is ledgered at ~$4–5 because planning is in-chat, stills are ~$0.05, and reuse
covers a growing share of clips. Budget on the measured number, watch it per cluster —
and expect re-roll variance (a bad Kling batch or safe-zone failure eats margin).*

Rule carried from BATCH_PLAN: **write the long first** where a cluster has one; distill
shorts from it. Reuse is same-format only (9:16↔9:16, 16:9↔16:9); Christ refs cross everything.

## 4. Topics = the 7-world slate (~71 pieces, already mapped)

Build+release order (reuse compounds in this order):
1. **The Cross — reconciled against `batch_manifest.json` (13 shorts, panel-forced
   precision):** 8 banked living-page (pierced, thirty_pieces, father_forgive_them,
   today_paradise, woman_behold, it_is_finished, into_thy_hands, watch_one_hour) ·
   2 duplicates EXCLUDED (it-is-finished-last-week, thief-on-cross) · **3 legacy
   Baroque single-narrator pieces (Crucifixion Foretold Ps22, My-God-why-forsaken,
   I Thirst) — DECISION: re-roll all 3 to inked living-page** (multi-voice, narrations
   already doctrine-audited) rather than publish old-style pieces that break the
   channel's visual promise in its first weeks. Those 3 re-rolls are the Phase-0 build
   task (~$5 each + voice) and take the bank to 11. Plus the EW07 Isaiah long (16:9,
   not built) as the month-1-or-2 long candidate.
2. **Resurrection / Empty Tomb** (~13 shorts + EW05 Jonah long) — Golgotha assets feed in.
3. **Wilderness / Exodus** (~8 shorts; EW01/EW04/EW08 longs exist — harvest their clips first).
4. **Genesis / Patriarchs** (~3 shorts; EW02/03/06 longs drive it).
5. **Galilean Ministry** (~24 shorts — the biggest harvest). PRECURSOR: build the
   living-ministry Christ ref + neutral plates EARLY and in parallel (the one real blocker).
6. **Nativity / Bethlehem** (~4 shorts + EW09 Boaz).
7. **Throne / Titles** (~5 shorts).

Corpus-diversity gate runs per BATCH (hooks, closers, subject mix) — sameness is the
scale killer, and per-piece gates are blind to it.

## 5. Release plan (decided: 3 SHORTS/WEEK + 1 LONG/MONTH)

- **Cadence:** Mon/Wed/Fri short (consistent slots); one long per month; the long's
  cluster shorts publish around it (the short is the long's trailer).
- **Launch gate (hard, one-time):** ≥9 publish-ready shorts banked before the first
  upload. 8 exist → the 3 legacy re-rolls (§4) take the bank to 11. Month 1 may ship
  shorts-only — the monthly long starts with month 2 (Jonah). The long is NOT part of
  the launch gate.
- **Bank invariant (sustaining, honest about evidence):** during publish weeks we must
  BUILD at roughly the rate we publish (≈3 shorts/week) or the bank drains. Cluster 1's
  ~6 shorts/week was measured INSIDE an already-built world — that pace does NOT
  automatically transfer to Cluster 2 (new tomb/Jonah assets + publishing ops on top).
  The stated unblock (not a parenthetical): **Resurrection shorts distill per SECTION
  of the Jonah long as each section locks — never wait for the full long.** If the bank
  falls below 2 weeks (6 shorts), the schedule slips — publicly, via the tracker —
  rather than rushing a gate.
- **Order within a cluster:** strongest hook first (pull viewers into the world), the
  hero/landing piece (e.g. It Is Finished) mid-run, close the cluster with the piece
  that best bridges to the NEXT cluster (e.g. first_day_morning → Resurrection).
- **Hook learning (observational, honest):** YouTube doesn't support A/B for Shorts,
  and cross-platform "A/B" (variant A on YT vs B on TikTok) is invalid — different
  audiences, different retention baselines. So: NO variant production. Instead, tag
  every piece's hook archetype at C0 time, and log weekly per-piece analytics
  (manual, ~15 min: {hook_archetype, pct_watched, swipe_3s, shares_per_1k, platform})
  into `data/learning/yt_analytics.jsonl` (created at first entry). Compare archetypes
  WITHIN a platform over rolling windows. This informs MANUAL updates to the C0 rules —
  `narration_gate.py` has no weights; no automated loop is claimed until one is built.
  One-time backfill: tag the hook archetype of all banked pieces before launch, or the
  first month's analytics has no labels (panel-caught).

## 6. Platform strategy (decided: YOUTUBE-FIRST)

- **YouTube = home channel:** Shorts (3/wk) + longs (1/mo) on ONE channel so shorts
  feed long-form watch time. End screens + pinned comments → awakeden.com Read-page.
- **Same-day cross-posts:** TikTok, Instagram Reels, Facebook Reels (same file, captions
  burned in). **Safe-zone check first (panel-caught):** platform UI masks differ (TikTok
  right rail + bottom third); verify the living-page caption band sits inside the common
  safe zone on one test upload per platform before the cadence starts.
- **TikTok link reality (panel-caught):** new accounts can't put clickable links in
  descriptions — the site link lives in BIO on TikTok/IG; spoken/visual "awakeden.com"
  on the end-card carries the rest. Descriptions link the Read-page only where links work
  (YouTube), and only once Read-pages are LIVE (never link a 404).
- **Every release goes through the existing gate machinery:** `/upload` (verified
  metadata, deterministic gates) → `/publish` (per-platform copy + captions.srt +
  PUBLISH_INDEX.html, UK-G1..G7). **BUT (panel-caught, code-cited): the publish engine
  reads the v2 folder layout (`narration.creation.json`, `assembly/viral_cut_*`), which
  cluster pieces don't have.** Phase 0 therefore includes a small batch→publish adapter
  (extend `upload_engine.harvest_facts`/`_find_video` to accept
  `batches/<cluster>/<slug>/` with `narration.md` + `visual/<slug>_scored.mp4` + a
  captions source from `audio/alignment.json`), and the gate is: **publish_check GREEN
  on one living-page piece end-to-end BEFORE launch.** `data/upload_brand.json` FILL_ME
  fields (channel, handles, website) get filled in Phase 0 or UK-G4 footers ship broken.

## 7. Website v2 (decided: COMIC READ-PAGES + PUBLIC TRACKER)

The insight: **every piece is already a comic.** `livingpage_short.spec.json` holds the
beats, captions, and red-letter bars; the stills are the panels. So the site publishes
each piece twice — Watch (video embed) and **Read (auto-generated scrollable comic
strip: panels + captions + Scripture bars + verse links)**.

- **Read-page v1 = beat frames, not a CSS re-build (panel-improved):** the cheapest
  faithful version is to extract ONE representative frame per beat from the finished
  video — panels arrive with captions and red-letter bars already rendered, pixel-
  identical to the film, zero re-implementation. `build_readpage.py` walks
  `livingpage_short.spec.json` (exists in 7 of the 8 banked pieces) for beat times +
  verse metadata, extracts frames, writes the static strip page. A styled-HTML/CSS
  version is a later polish, not launch scope.
- **The pilot exception (panel-caught):** `father_forgive_them` predates the living-page
  spec (`mocomic*.spec.json`) — it gets a Watch-only page at launch; spec migration is
  backlog, not a blocker.
- **The Plan page (public tracker):** ONE source of truth — extend the site's existing
  `manifest.yaml` `public_status` (which `build_catalog.py` already reads) rather than
  inventing a parallel `publish_log.json` (panel-caught duplicate-truth risk). The
  tracker renders three columns: OUT (linked) / IN PRODUCTION / NEXT, fed by manifest
  entries the publish step updates.
- **Home:** latest piece + the one-line mission + email capture. **Email infra is a
  Phase 0 step, not an afterthought (panel-caught):** pick the provider, set up the
  domain auth (SPF/DKIM/DMARC), embed the form — the signups metric is dead until this
  exists.
- Ship order: tracker → Read-pages v1 → identity copy refresh.
- **About / What we believe:** KJV, the whole Bible through Jesus, grace-anchored CTA.
- **Identity refresh, not relaunch:** update copy + hero art from Baroque-era wording to
  the inked comic identity. Keep the existing Netlify pipeline, typography, structure.
- Out of scope for now (phase 3+): full offline reader, per-world hub deep pages,
  memberships.

## 8. Reuse economics (why this gets cheaper)

- Cluster 1 holds **74 registered stills + 63 clips** under `cluster_01_cross` in
  `asset_index.json` (verified against the index 2026-07-03 — includes both pilots'
  assets). Every cluster ingests its art on completion (already standard).
- Expected cost curve per short: ~$5.20 measured (cluster-1 roll: ~$31 across the 6 NEW
  pieces; the 8 banked include the 2 earlier pilots) → cluster 2 target ~$3–4 **only
  after a fresh asset audit** (Resurrection needs non-Golgotha art: tomb interior,
  risen Christ, the fish — the target is a hypothesis until the audit prices it).
  Kling clips are the spend; stills are pennies — never ration stills (standing rule).
- **Style-match rule for reuse (panel-caught):** the legacy clip_library is largely
  Baroque-oil; the universe is now inked graphic-novel. Reuse must match STYLE as well
  as aspect — inked↔inked only. Baroque assets don't count toward the inked cost curve.
- The living-ministry Christ ref unlocks 24 Ministry shorts — highest-leverage single
  asset left to build.

## 9. Quality law (unchanged, restated so release pressure never erodes it)

C0 earned-hook gate before any spend · doctrine proven BOTH ways (red-team + 5-CLI
panel, clean artifact) · KJV verbatim with clause-boundary tags · living-page DoD gates
(0 reuse violations, motion floor, median beat) · every still eye-audited · sacred bars
never slam · release cadence NEVER overrides a failed gate — slip the schedule, not the gate.

## 10. Step-by-step (the way forward)

**Phase 0 — prep (weeks 0–1, BEFORE launch; launch happens when the gates pass, not
on a date):**
1. Panel-review this plan (5-CLI) → fold verdicts → user sign-off. *(round 1: degraded
   2/5, REVISE ×2, folded. round 2: quorum 4/5, REVISE ×3, folded — see §12)*
2. **Re-roll the 3 legacy Cross pieces to living-page** (Crucifixion Foretold Ps22 ·
   My-God-why-forsaken · I Thirst — inked, multi-voice; narrations already
   doctrine-audited, re-voice + full visual). Bank 8 → 11, launch gate satisfied,
   channel style-coherent from day one. Backfill hook-archetype tags on all 11.
3. **Run `corpus_diversity.py` over the full Cross batch** before anything publishes
   (the per-batch sameness gate this plan already promises in §4).
4. **Batch→publish adapter + prove it:** extend upload/publish to read
   `batches/<cluster>/<slug>/` layout; gate = `publish_check` GREEN on one living-page
   piece end-to-end. Fill `data/upload_brand.json` (channel/handles/website).
5. YouTube channel dress: banner/avatar/about in the inked identity; playlists per world.
6. Email CAPTURE only (provider chosen + form embedded); full sending DNS auth
   (SPF/DKIM/DMARC) can follow before the first email SEND — launch only needs the
   list to exist (panel scope-trim).
7. Website v2: tracker (extend manifest.yaml `public_status`) → Read-page v1 (beat-frame
   extractor) → copy refresh → deploy. Safe-zone test upload per platform — if the
   caption band fails a platform mask, the fix is a scripted batch re-render (the band
   position is an engine parameter) + re-score; bounded, not a launch-stopper.
8. **Off-machine backup, AUTOMATED (panel-caught SPOF):** scheduled robocopy/rclone
   job for `batches/`, `asset_index.json`, refs, libraries, and narration trees —
   one Windows machine currently holds everything; a manual "weekly copy" habit is
   not a control. Verify Suno tier commercial-use grant (see §11) in the same pass.

**Phase 1 — launch (weeks 1–3):**
9. Publish Cross shorts Mon/Wed/Fri via the adapted /upload + /publish; cross-post
   same day (TikTok/IG link in bio, not description).
10. Keep building at publish rate (§5 bank invariant): start Cluster 2 — write the
    **EW05 Jonah long** AND distill its first Resurrection shorts as sections lock.
    Month 1 ships shorts only; the monthly-long lane starts month 2 with Jonah.
11. Weekly analytics entry starts with the first published week (named step, §5).

**Phase 2 — rhythm (months 2–3):**
12. Publish Resurrection: ~13 shorts at 3/wk + the Jonah long as month-2's long.
13. Build Cluster 3 (harvest EW01/EW04 clips into the library first) + the
    living-ministry Christ ref in parallel (pre-flight its cost before the batch).
14. First analytics review: hook archetypes vs. watch-through → manual C0 rule update.

**Phase 3 — scale (months 3–6):**
15. Clusters 4–5 (Ministry mass-production once the living-Christ ref lands).
16. Site: per-world hub pages + whatever the analytics say readers actually use.
17. Revisit monetization ONLY if it funds production without touching the CTA.

## 11. Risks (named so we watch them)

- **Sameness at scale** → batch-level corpus diversity gate, rotating hook archetypes.
- **Doctrine drift under speed** → the panel is mandatory; slip schedule, never the gate.
- **Platform risk** → the site + list from day one; videos always link home.
- **Solo-operator burnout** → the 3+1 cadence is chosen BECAUSE it is sustainable; the
  runway rule (≥3 weeks banked) absorbs life happening.
- **Rights (panel-corrected, watched not waved away):** KJV is public domain in most of
  the world but under Crown patent in the UK — our use (new video/comic works quoting
  Scripture) is standard practice, named here for honesty. Suno music: VERIFY the
  subscription tier grants commercial use (Phase 0 checklist item) and treat YouTube
  Content-ID collisions on AI-generated music as a watched risk (dispute path ready:
  our generation records). All art generated in-house — keep it that way.

## 12. Panel record (independent review — ENFORCED)

**Round 1 (2026-07-03, `v2/_independent_review/20260703-135242`):** degraded panel —
2/5 voices (claude, gemini; cursor/codex/grok timed out). Both REVISE. Disposition:
- **Fixed:** day-one runway violation (launch now gated on ≥9 banked; remaining ~6 Cross
  shorts scheduled first) · "Cross DONE" overclaim (8 of ~14) · Cluster-2 long-first
  collision with launch week (Jonah long moved out of the crunch, ships month 2) ·
  Shorts title/thumbnail A/B replaced with hook-level A/B + named weekly analytics step ·
  publishing routed through /upload + /publish gates · Read-page scope honesty (CSS
  re-render, tracker ships first).
- **Answered (verified false / by-design):** gemini's "livingpage_short.spec.json is
  hallucinated" — the file exists in all 7 cluster-1 pieces (CLAUDE.md's file map
  predates the living-page pipeline) · gemini's "$23/episode contradiction" — $4–5 is
  the MEASURED cluster-1 ledger; $23 is the legacy Baroque/API model (note added §3) ·
  "website is premature" — explicit user decision (scope kept small, tracker-first).
- **Round 2 pending:** re-run for quorum (≥4/5) after fixes; do not LOCK on round 1.

**Round 2 (2026-07-03, `v2/_independent_review/20260703-140926`):** quorum — 4/5
responded (claude, gemini, cursor REVISE; grok returned no verdict; codex timed out).
Disposition of convergent findings:
- **Fixed:** bank invariant now has a stated sustaining build rate + slip trigger (was:
  hard rule with no production math) · launch gate simplified to ≥9 shorts, month-1
  long removed from the gate · variant A/B DROPPED entirely (cross-platform comparison
  invalid + hidden 2× production cost) → observational hook-archetype logging, manual
  C0 rule updates ("feeds gate weights" was fictional wiring — narration_gate.py has no
  weights) · batch→publish adapter + publish_check-GREEN-on-one-piece added to Phase 0
  (upload_engine reads v2 layout only — code-cited) · upload_brand.json FILL_ME step ·
  corpus_diversity.py run scheduled before publishing · Read-page v1 re-scoped to
  beat-frame extraction (pixel-true, zero re-implementation) · father_forgive_them
  spec-gap stated (Watch-only at launch; 7 of 8 have livingpage specs) · tracker uses
  manifest.yaml public_status as the ONE source (no parallel publish_log.json) · email
  infra + DNS auth added to Phase 0 · TikTok no-links + caption safe-zone checks added ·
  off-machine backup step added (solo-machine SPOF) · style-match reuse rule added ·
  cost denominator clarified ($31/6 new) · phase numbering fixed.
- **Answered:** "~6 remaining Cross shorts" → corrected to ~4 unique (manifest minus 2
  duplicates); "launch could go with just 1 more short" → true for the gate, but the ~4
  are built anyway for bank margin (cheapest builds available).
- **Round 3:** targeted re-run (the fixes are mechanical; if round 3 returns PASS or
  REVISE on style-only notes, LOCK with user sign-off).

**Round 3 (2026-07-03, `v2/_independent_review/20260703-141845`):** 3/5 substantive
(claude, gemini, codex — all REVISE; grok no verdict, cursor tool error). Disposition:
- **Fixed:** Cross scope replaced with the exact manifest reconciliation (13 = 8 banked
  + 2 duplicates excluded + 3 legacy Baroque) and the DECISION to re-roll the 3 legacy
  pieces to living-page (brand promise wins; "~4 remaining" was wrong — verified) ·
  §8 asset counts corrected to the verified index (74 stills + 63 clips under
  cluster_01_cross; both my earlier figure and reviewers' counts were off) · cluster-2
  cost target demoted to hypothesis-pending-asset-audit · capacity claim honesty
  (cluster-1 pace measured inside a built world; section-level distillation promoted to
  the stated unblock) · §3 table formatting fixed · hook-archetype backfill step added ·
  Suno commercial-tier verification + Content-ID watched risk + KJV UK caveat added ·
  email trimmed to capture-only at launch · backup automated (scheduled job, not habit) ·
  safe-zone failure mitigation named (scripted caption-band re-render).
- **Answered:** gemini's "cut the tracker from Phase 0" — explicit user decision, kept
  (sequenced after the publish adapter); "budget assumes 100% first-pass Kling" — §3
  cost note now names re-roll variance; codex's "panel record stale" — this section IS
  the current record.
- **LOCK basis (per the panel-calibration rule: the bar is no remaining
  factual/doctrinal error, not unanimous PASS):** every concrete, verifiable finding
  across 3 rounds is either fixed or answered with evidence; round-3 claude explicitly
  called the remaining defects "concrete numbers... cheaply fixable," all now fixed.
  **Status: LOCKED — user signed off 2026-07-03 ("go, re-roll the 3 legacy pieces and
  start phase 0"). The 3-legacy-re-roll decision is confirmed.**
