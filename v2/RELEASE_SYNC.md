# RELEASE SYNC — one desk for publish · upload · website · tracking

Status: DESIGN + BUILD 2026-07-15. Modeled on HF-POC's fg-publish/fg-upload chain,
keeping what worked (paste-ready packs, deterministic gates, never auto-upload)
and designing out its failures (two hand-synced URL stores, no dates, browser
localStorage as primary state, hardcoded episode lists, fuzzy joins).

## The problem this solves

Five drift seams existed in JITB (2026-07-15 audit):

1. FOUR different "what is the final video" implementations
   (`production_board.final_video`, `publish_pack.final_video_and_words`,
   `upload_engine._find_video`, `thumbnails._sfx_video`) — only one skipped
   `.bak` backups.
2. The production board joined manifest↔lane by FUZZY letters-match — already
   produced one false FINAL (`ew-jonah` → `sign_of_jonah`, 2026-07-15).
3. Publish packs went silently stale when finals were re-rendered
   ("14 packs stale vs the new finals", commit 9007339).
4. Only YouTube was tracked, with no dates; TikTok/FB/IG posting state lived
   nowhere. Thumbnails existed on disk but the gate couldn't see them
   (`_source.json.thumbnail` hardcoded `""`).
5. The long↔short relationship was encoded three inconsistent ways (folder
   nesting, manifest `cluster`, batch_manifest plan) with no authoritative link.

## The design — one registry, one finality rule, one write path, one gate, one board

```
_website/manifest.yaml          THE REGISTRY (already existed; now the hard join)
  + source:  ../batches/...     stable link: catalogue item -> lane folder
  + parent:  <long slug>        stable link: derived short -> its long

pipeline/finality.py            THE ONE RULE: final_video(dir, kind) + content sha
                                (sha cached by size+mtime in data/.sha_cache.json;
                                mtime alone is NOT freshness — dyncam lesson)

data/release_ledger.json        THE POSTING LEDGER: slug -> platform ->
                                {url, video_id, posted (date), final_sha}
                                written ONLY by upload_tracker.py --set

upload_tracker.py               THE ONE WRITE PATH: --set <slug> <platform> <url>
                                writes ledger + manifest youtube_id (+status live)
                                + rebuilds read pages. Never uploads, never deploys.

pipeline/release_state.py       ONE computation of per-piece state, shared by:
release_check.py                the $0 fail-closed SYNC gate (exit 1 on drift)
production_board.py             the human board (renders the same state)
```

### Freshness chain (sha, not mtime) — TWO anchors

There are two anchors, because two different videos feed the surfaces:

**Anchor 1 — the postable FINAL** (`*_sfx.mp4` per the caption policy):
- publish pack   -> `publish/_source.json.final_sha` (written on every pack build/refresh)
- thumbnails     -> `publish/thumbs/_meta.json.final_sha`
- posting        -> `release_ledger.json[slug][platform].final_sha` (what was actually posted)

**Anchor 2 — the READ video** (`read_video:` else the `read_source` folder's
`*_scored.mp4` — exactly build_readpage.py's rule; the sfx bed changes audio
only, frames are identical, so read pages track the scored copy):
- read frames    -> `_website/assets/study/read/<slug>/_meta.json.source_sha`

A surface whose recorded sha != its anchor is STALE and the gate says exactly
which command refreshes it. NOTE an audio-only re-bed changes Anchor 1 and
correctly flags pack + thumbs: the postable BYTES changed, and both refreshes
are $0 one-liners — fail-closed beats guessing whether a change "counts".

### The SYNC gates (all $0 deterministic, in release_check.py)

| Gate | Check | Level |
|------|-------|-------|
| SYNC-G1 | every catalogue item hard-joins to a real folder (`source`/`read_source`/`study_source`); fuzzy match is DEAD | FAIL (studio_complete/live) / WARN (in_production) |
| SYNC-G2 | `studio_complete`/`live` items have a final video under the ONE finality rule | FAIL |
| SYNC-G3 | publish pack exists + `final_sha` matches the current final (stale pack cannot be GREEN) | FAIL |
| SYNC-G4 | thumbs exist + `_meta.json.final_sha` matches | FAIL (live) / WARN (studio_complete) |
| SYNC-G5 | read page built for promoted items; frame `_meta.source_sha` matches; `publish_meta.json.read_url` points at the real `read/<slug>.html` | FAIL on read_url mismatch; WARN on frame sha (audio-only sfx change also shifts the sha) |
| SYNC-G6 | published coherence: `youtube_id` ⟺ `public_status: live` ⟺ dated ledger entry with URL; posted `final_sha` == current final (else the LIVE video is outdated — surface it) | FAIL |
| SYNC-G7 | long↔short: shorts in a cluster that has a long carry `parent:`; parent exists and is a long | FAIL |
| SYNC-G8 | art style: a `studio_complete`/`live` item's rendered art style is not the LEGACY Baroque oil-painting look (`pipeline/art_style.py`, deterministic text-scan over `scene_plan.json`/`_panel_scene_plan.md`/`piece.json`) | FAIL |

Platforms not yet posted are reported as the TO-POST queue, never a FAIL
(posting is the human's move; the gate only guards *recorded truth*).

### SYNC-G8 — the Baroque-legacy ban (added 2026-07-16)

🔒 HARDENED (user, 2026-07-15, memory `graphic-novel-style-migration`):
"everything from the oil-painting era is LEGACY and will NEVER BE UPLOADED...
don't count legacy finals as upload-ready on any board or plan." No Baroque
final ships, ever. This was a real gap: `production_board.py`'s readiness
calc and every SYNC gate checked finality/pack/thumbs freshness but never a
piece's *art style* — four Types & Shadows longs (Passover Lamb, Bronze
Serpent, Seed of the Woman, Day of Atonement) were built through score/SFX/
caption and given GREEN publish packs while still rendered Baroque, a direct
regression against the hardened rule (caught 2026-07-16).

No per-piece `art_style` field is persisted at render time yet, so
`pipeline/art_style.py::detect_art_style()` is the deterministic stopgap: it
scans `visual_16x9_inked/scene_plan.json` (wins over `visual_16x9`, matching
`finality.py`'s own inked-first precedence), the self-review
`_panel_scene_plan.md`, and a shorts/batches `piece.json`'s still-job prompts
for an explicit "baroque"/"graphic-novel" marker. It is fail-SAFE, not
fail-closed: only a POSITIVE "baroque" hit blocks a piece; anything the
scanner can't classify returns `"unknown"` and is left alone, so it cannot
retroactively fail already-shipped pieces built through a format this
heuristic doesn't recognise. `config.VISUAL_STYLE` also flips default
`baroque` → `graphic_novel` the same day (config.py; Baroque stays selectable
only via an explicit env override for one-off reference renders).

**Follow-up (not done here):** persist a real `art_style` field on every
piece at render time and treat `"unknown"` as `baroque` (fail-closed) once the
whole catalogue has been swept and confirmed clean under the loose heuristic.

### Long + short combined — the EPISODE (added 2026-07-15, user ask: "unlike
Furgiven I don't have a long+shorts unit of work I can track — it feels
chaotic")

`pipeline/episode_state.py` — an Episode's identity IS the long's own manifest
slug (no new id to invent). It is DETECTED, never hand-declared: a long
becomes a tracked episode the moment its first short sets `parent:` to it.
Standalone shorts with no `parent:` (I AM Sayings, Parables, Miracles,
Questions Jesus Asked, ...) are NOT forced into this shape — scope decision
2026-07-15: only true long-anchored families become episodes; everything else
keeps its existing per-piece tracking. This is a DATA-layer concept only —
no folders were moved (the user's wave-F rebuild was actively running in
`batches/cluster_01_cross` at the time; physical `episodes/<id>/shorts/`
nesting to match Furgiven exactly is a later, lower-risk-window decision).

- `EpisodeState.status`: `long in production` → `long done, no shorts yet` →
  `shorts building (N/M)` → `built, ready to release` → `releasing (N/M shorts
  posted)` → `COMPLETE — fully released`.
- `production_board.py` renders an EPISODES roll-up (progress bars: shorts
  built / shorts fully posted, chip-per-short jump links) above the flat
  per-piece table — the "one line I can point to and say where are we"
  the user wanted.
- `build_upload_tracker.py` wraps an episode's long + shorts in one
  `epblock` — a single release CAMPAIGN card, long first then shorts in
  `cluster_order`, instead of N unrelated flat cards (shorts funnel to the
  long — memory `shorts-longform-funnel`). Standalone shorts stay as
  individual cards below, unchanged.
- `EpisodeState.long_ready` distinguishes "built but not yet catalogue-approved
  (`public_status` still `in_production`)" from "approved and just not posted
  yet" — the tracker says which, rather than silently omitting the long's card
  with no explanation (found live on Psalm 22: video/pack/thumbs all fresh,
  but `public_status` was never bumped past `in_production` — a human
  approval call, not something this tooling should flip on its own).

### What stays manual (by design, same as HF-POC)

Posting itself. The chain is: board shows TO-POST -> open the piece's
`publish/PUBLISH_INDEX.html` (copy buttons) -> upload by hand -> paste the URL:
`upload_tracker.py --set <slug> <platform> <url>` -> gate + board go green.
One paste per platform is the entire bookkeeping burden.

## Commands

```
.venv\Scripts\python.exe release_check.py              # the SYNC gate (exit 1 on drift)
.venv\Scripts\python.exe release_check.py --slug X     # one piece
.venv\Scripts\python.exe production_board.py           # board (renders the same state)
.venv\Scripts\python.exe build_upload_tracker.py       # _UPLOAD_TRACKER.html - the paste-ready
                                                       # posting runbook (per-platform URL boxes
                                                       # -> copy the --set command; ledger-driven,
                                                       # NO browser state - the HF-POC localStorage
                                                       # lesson). Thumbs per piece: 16:9 (YouTube)
                                                       # + 9:16 (Shorts) + 1:1 + TikTok centre-safe
                                                       # cover (feed crops to the middle 3:4).
.venv\Scripts\python.exe upload_tracker.py --list
.venv\Scripts\python.exe upload_tracker.py --set <slug> youtube <url>
.venv\Scripts\python.exe upload_tracker.py --set <slug> tiktok <url>
.venv\Scripts\python.exe upload_tracker.py --set <slug> youtube <url> --repost   # after a REAL re-post
.venv\Scripts\python.exe pipeline\thumbnails.py        # manifest-driven, writes _meta.json
.venv\Scripts\python.exe cli_publish.py <dir> --copy-ok   # after RE-READING copy vs a new final
# pin an ambiguous lane: <piece>/FINAL_VIDEO.txt, first line = relative path to the postable
```

## Refresh order (when a final is re-rendered)

```
1. the final lands            (build/score/sfx lane)
2. pipeline\thumbnails.py     (re-cut + _meta stamp; BEFORE the pack, so
                               _source.json picks up the thumbnail path)
3. cli_publish.py <dir> --index   (mechanical refresh: srt + _source + sha stamp;
                                   copy survives — re-read it, --redraft if it must change)
4. _website\build_readpage.py     (only if the SCORED video changed - frames + _meta)
5. release_check.py           GREEN
```

## Policies (decided 2026-07-15)

- **SYNC-G6 posted-sha divergence is a hard FAIL** (panel debated WARN): if the
  public copy and the repo's final differ, the drift is real and the human must
  choose — re-post the new final, or restore the old one. The gate never guesses.
- **Read-frame staleness stays WARN** (not FAIL): the read page is a derived
  study surface, refresh is $0, and baseline stamps predate some finals.
- `upload_tracker.py --set` refuses unknown slugs/platforms; manifest + ledger
  writes are atomic (temp + os.replace).

## Standing rule + enforcement

`release_check.py` runs before any deploy of `_website/` (wired into the
update-website skill's Deploy step) and after any posting batch. The board is
`production_board.py` — same state, rendered. Tests: `pipeline/test_finality.py`
+ `pipeline/test_release_state.py` (31 cases incl. the ew-jonah no-fuzzy-join
regression and the G6/G7 fire-without-video regression).

## Red-team record (implementation, 2026-07-15)

Two hostile agents (false-GREEN hunter + corruption/ops attacker) + one empirical
probe attacked the BUILT system. Verified findings, all fixed + regression-tested:

- **C1 wrong anchor (live on Isaiah):** finality broke ties alphabetically
  (unscored `Isaiah53_16x9_captioned` beat `scored_captioned`) and checked
  visual_16x9 fully before the inked dir. Fixed: pattern outranks directory,
  deeper chain ("scored") wins ties; Isaiah thumbs re-cut from the right final.
- **sha-cache spoof (empirical):** same-size + restored-mtime swap returned a
  stale sha. Fixed: cache trust = size + an always-recomputed head/tail-64KB
  fingerprint; cache writes atomic, dead keys pruned.
- **C2/C3 stamp laundering:** ffmpeg past-EOF exits 0 writing nothing — thumbs
  composed the previous `_frame.png` and stamped fresh; partial read-frame
  extraction stamped mixed-provenance dirs. Fixed: pre-delete + verify the frame
  exists, clamp `thumb.t`; read `_meta` stamped only on full-coverage runs,
  dropped on partial (gate WARNs until `--force`).
- **Laundering the human steps:** `--index` restamps mechanicals but now
  PRESERVES `copy_final_sha` (what the copy was authored against) — mismatch
  WARNs until `--copy-ok`/`--redraft`. `upload_tracker --set` refuses to replace
  a differing ledger entry without `--repost` (re-pasting a URL no longer clears
  the posted-sha FAIL).
- **Gate blind spots:** `--slug` runs gates over the FULL catalogue (filter only
  narrows output — it used to fabricate a G7 FAIL); G6 now checks the REVERSE
  direction (youtube ledger entry without manifest youtube_id = the interrupted
  --set half-state that caused double-upload risk); unstamped ledger entries
  WARN; read pages without `read_source` WARN (freshness was silently disarmed);
  orphan `read/*.html` WARN; longform lanes join the orphan sweep; same-tier
  rival finals WARN with a pin instruction.
- **Ops:** manifest re-read at the last moment before `--set` writes (user
  co-edits live); atomic writes retry on Windows PermissionError with unique tmp
  names; the read-page rebuild failing mid-`--set` now prints exact recovery;
  malformed manifest/ledger/_source fail CLOSED with the file named; a `--slug`
  matching nothing exits 2, never GREEN.
- **Pin:** `FINAL_VIDEO.txt` (first line = relative path) in a piece folder
  overrides the rule for ALL callers; a dangling pin is NO VIDEO, never a silent
  fallback. Psalm 22 pinned to `LivingPage_Psalm22_16x9_scored_sfx.mp4`.
  **OPEN (user call): EW01 Two Goats** — rule picks `..._scored_sfx.mp4`; the
  serif-captioned `..._scored_sfx_captioned.mp4` may be the intended postable.
- **Accepted residual risk (documented, not fixed):** ledger sha is "repo final
  at record time", not proof of what was uploaded; trust-on-first-use baselines
  (packs/read frames stamped against today's finals — one-off `--force` audit is
  the recovery if ever doubted); alignment-vs-final caption drift is the lane's
  LP-RETIME concern, not the desk's.

## Panel record

Reviewed 2026-07-15 (`v2/_independent_review/20260715-171754/`): cursor, claude,
gemini, grok = REVISE (codex timed out). Convergent flags fixed: G6/G7 were
unreachable for pieces with no video; read-frame anchor now mirrors
build_readpage (read_source, not source precedence); dangling *_source fields
now FAIL; parent must be kind=long; atomic writes; SYNC tests added; the
imaginary `--board` flag removed from this doc; refresh order documented above.
Answered (not changed): G6 FAIL-on-divergence kept (fail-closed policy above);
audio-only sha flags kept (see anchors note); upload_engine's uncaptioned-cut
fallbacks kept for legacy lanes — finality wins whenever a blessed final exists.
