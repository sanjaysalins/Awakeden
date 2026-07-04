# Independent review — codex (OK, 282s)

**Findings**

1. **Publish adapter is underspecified.** The plan says “extend `upload_engine.harvest_facts`/`_find_video` … captions source from `audio/alignment.json`” and gate on “`publish_check` GREEN.” But the current publish pack also expects `assembly/*` and sibling `.words.json` for `captions.srt`. Updating only `upload_engine` will still fail the SRT gate.

2. **`build_readpage.py` appears nonexistent.** The claim “`build_readpage.py` walks `livingpage_short.spec.json`” assumes a tool that is not in the repo. There are frame extraction helpers, but no website Read-page builder wired into `_website/build_catalog.py`.

3. **Manifest automation is fictional.** The tracker is “fed by manifest entries the publish step updates,” but `cli_publish.py`/`publish_pack.py` explicitly produce paste-ready packs and “NEVER uploads.” They cannot know `youtube_id` or mark `public_status: live` without a separate post-upload step.

4. **The Cross count contradicts itself.** §4 says “remaining ~6 Cross shorts,” while §5/Phase 0 says “remaining ~4 unique Cross shorts.” The plan must name the exact four slugs and update `batches/batch_manifest.json`; otherwise launch scope and spend are ambiguous.

5. **Production capacity is overclaimed.** “cluster-1 measured pace was ~6 shorts/week … so 3/week alongside one long-in-progress is within evidence” does not transfer to Cluster 2. Cluster 1 reused one built world; Cluster 2 adds Jonah, tomb assets, publishing ops, cross-posting, analytics, and website work.

6. **Cost curve is not proven.** “~$3–4 (cluster 2, Golgotha reuse)” is optimistic without a fresh asset audit. Resurrection/Jonah needs non-Golgotha assets, and the plan excludes real labor costs for QA, publish packs, safe-zone testing, email, DNS, and site deployment.

7. **Copyright note is too broad.** “KJV is public domain” needs a jurisdiction caveat. External rights references indicate KJV is public domain in much of the world, but UK publication has royal-prerogative restrictions. Source: [King James Version copyright status](https://en.wikipedia.org/wiki/King_James_Version#Copyright_status).

8. **Panel record is stale.** The plan says “Round 3: targeted re-run,” but the repo contains `v2/_independent_review/20260703-141845` with only a Cursor failure and no verdict. That cannot support “LOCK with user sign-off.”

VERDICT: REVISE
TOP FIXES:
1. Specify and test the full batch-to-publish adapter, including SRT generation and publish_check GREEN.
2. Replace assumed tools/automation with concrete Read-page and manifest-update implementation steps.
3. Recompute exact Cross scope, Cluster 2 capacity, and per-cluster cost from the real manifest/assets.
