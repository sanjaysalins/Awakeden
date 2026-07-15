# Independent review — gemini (OK, 131s)

This plan proposes a robust architectural cleanup for drift, but it contains a critical, pipeline-blocking logic flaw regarding published assets, as well as cascading invalidation risks.

Here is the adversarial breakdown:

### 1. The "Permanent Blocker" Flaw in SYNC-G6 (Single Point of Failure)
**Citation:** *"SYNC-G6 | published coherence [...] posted `final_sha` == current final (else the LIVE video is outdated — surface it) | FAIL"*
**Critique:** This is a fatal design flaw. If a video is already published and live on YouTube, and you later re-render the local file (to fix a typo for TikTok, or by accident), the local `final_sha` will change. Because SYNC-G6 returns a `FAIL`, your entire pipeline (`release_check.py`) is now hard-blocked. You cannot deploy the website or pass gates for *other* videos until you either (a) delete and re-upload the YouTube video to match the new SHA, or (b) manually hack the ledger. 
**Fix:** `posted final_sha != current final` on a `live` status MUST be a `WARN`, or there needs to be an `acknowledged_drift` override in the ledger. It cannot be a hard `FAIL`.

### 2. Cascading Invalidation for Audio-Only Changes (Over-engineering / False Assumption)
**Citation:** *"WARN on frame sha (audio-only sfx change also shifts the sha)"* (Under SYNC-G5) and *"SYNC-G4 | thumbs exist + `_meta.json.final_sha` matches | FAIL"*
**Critique:** You correctly identified that audio-only changes shift the video SHA, but you failed to apply that logic to SYNC-G3 (publish packs) and SYNC-G4 (thumbnails). If you tweak the SFX volume and re-render the final video, the SHA changes. SYNC-G3 and SYNC-G4 will instantly `FAIL`, forcing you to unnecessarily re-extract thumbnails and rebuild publish packs even though the visual frames haven't changed at all. 
**Fix:** Provide a way to bypass thumbnail/pack invalidation if the visual pipeline hasn't been touched, or separate the video and audio SHAs if possible.

### 3. Missing Validation on the Manual Write Path (Verification Gap)
**Citation:** *"`upload_tracker.py --set <slug> <platform> <url>` writes ledger + manifest"*
**Critique:** Because posting is a manual copy-paste step, the slug is typed (or copy-pasted) by a human into the CLI. The plan does not explicitly state that `upload_tracker.py` validates the `<slug>` against `_website/manifest.yaml` before mutating the ledger. If a typo is made, does it create a zombie entry in `release_ledger.json` that never joins to the manifest? 
**Fix:** Explicitly require `upload_tracker.py` to enforce that `<slug>` exists in the registry before writing to the ledger.

### 4. Concurrency / State Tearing Risk
**Citation:** *"`upload_tracker.py` [...] writes ledger + manifest `youtube_id`"*
**Critique:** You are mutating two separate sources of truth (a JSON ledger and a YAML manifest) in a single CLI command. If the script crashes between writing the JSON and writing the YAML, the state tears, and SYNC-G6 will `FAIL` permanently until manually repaired.
**Fix:** Ensure the writes happen sequentially with error handling, or better yet, make `manifest.yaml` derive the `youtube_id` at build time from the ledger rather than storing it in two places.

VERDICT: REVISE
TOP FIXES:
1. Change SYNC-G6's `final_sha` mismatch on live videos from a hard FAIL to a WARN (or add an override), so local edits don't paralyze the entire release pipeline.
2. Prevent audio-only SHA changes from causing spurious SYNC-G3/G4 FAILs that force unnecessary thumbnail and publish pack rebuilds.
3. Explicitly enforce that `upload_tracker.py` strictly validates `<slug>` against the manifest registry before writing to the ledger to prevent orphaned records.
