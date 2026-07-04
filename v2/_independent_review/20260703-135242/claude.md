# Independent review — claude (OK, 492s)

Checked the plan against the repo: `batches/batch_manifest.json`, `BATCH_PLAN.md`, `asset_index.json`, `_website/build_catalog.py`, `data/learning/`, and the 8 cluster-1 piece folders (with `livingpage_short.spec.json` + stills) all exist. `publish_log.json` does not exist yet — the plan correctly schedules creating it. Commit `d6e294b` is real and is HEAD. Cost claims (~$4–5/short, $20–40/long) match the ledgered cluster-1 spend. So the foundation is sound. But there are real problems.

## Findings

**1. The runway math contradicts the plan's own rule (§5).**
"Runway rule: ≥3 weeks banked at all times" + "Cluster 1 gives ~3 weeks of runway on day one." 8 shorts ÷ 3/week = **2.67 weeks** — the rule is violated on day one, and worse after "never publish the last piece" holds one back (7 publishable = 2.33 weeks). By end of week 1 you're at 5 banked unless Cluster 2 shorts are already finishing — which they can't be, because…

**2. Cluster 2 has a serial bottleneck the schedule ignores (§3 rule + §10 step 6).**
The plan's own rule: "write the long first where a cluster has one." Cluster 2's long (EW05 Jonah) is **unbuilt**, costs $20–40, and historically longs take much longer than shorts. So the ~13 Resurrection shorts are blocked behind a long that must be written, panel-reviewed, voiced, and built inside the same 3-week window as website v2, channel dress, publishing 3×/week, and cross-posting to 3 platforms — all solo. Phase 1 is the heaviest phase of the whole plan while claiming the cadence was "chosen BECAUSE it is sustainable."

**3. "The Cross — DONE building" is wrong (§4 item 1).**
`BATCH_PLAN.md` (the companion doc this plan defers to) sizes the Cross world at **~14 shorts** plus the EW07 Isaiah long. 8 are banked. The plan's own ~71-piece total (14+13+8+3+24+4+5) only works with the 14. The remaining ~6 Cross shorts vanish from the release order entirely — never built, never scheduled. Building them is also the cheapest possible runway fix (the Golgotha set is done, ~$4 each), which makes finding #1 easy to solve — but the plan doesn't see it.

**4. Reuse gap: the publishing machinery already exists and isn't mentioned (§6, §10 step 5).**
This repo has `/upload` (Stage 5, verified metadata, 6 deterministic gates) and `/publish` (Stage 6, per-platform copy + captions.srt + PUBLISH_INDEX.html, gated UK-G1..G7). Phase 1 step 5 just says "Publish Cross shorts; descriptions link Read-pages" — implying hand-written descriptions, duplicating what the gates already enforce. The plan should route every release through /upload + /publish, and the Read-page link belongs in those skills' description templates, not in ad-hoc process.

**5. The A/B mechanism doesn't exist for Shorts (§5).**
"Two title/thumbnail variants per piece where the platform allows" — YouTube's Test & Compare is long-form thumbnails only; Shorts surface in the feed with no thumbnail and title A/B isn't natively supported. For shorts the real A/B unit is the **hook itself** (first 3s), which the C0 gate already scores. As written, this step produces no data on the product that ships 12×/month.

**6. Smaller gaps.**
- §5 "log hook-style vs %-watched in `data/learning/`" — the folder exists (calibration.jsonl etc.) but no mechanism is named for getting YouTube analytics into it (manual entry? API?). Unspecified = won't happen.
- §7 Read-page: panels exist as stills, but the red-letter bars/captions live only as spec-JSON + PIL rendering — the web version needs a CSS or image-export re-implementation, which is more than "extend build_catalog.py" suggests. Feasible, just under-scoped.
- §1 metrics are all listed but no baseline or review owner beyond "checked monthly" — fine for v1, watch it.

What's good: objective hierarchy is clear, quality law (§9) explicitly outranks cadence, the reuse economics match the ledger, the site plan reuses the existing Netlify pipeline instead of a rebuild, and phase 3+ scope is correctly deferred.

VERDICT: REVISE
TOP FIXES:
1. Fix the day-one runway violation and the "Cross DONE" claim together: the Cross world is ~14 shorts per BATCH_PLAN, not 8 — schedule the remaining ~6 (cheapest runway, set already built) or explicitly rescope the cluster and recompute the ≥3-week rule.
2. Unblock Cluster 2's serial bottleneck: either pre-declare a shorts-first exception for Resurrection or move the EW05 Jonah long out of the overloaded 3-week launch window — as written, "long first" + launch + website v2 collide.
3. Route Phase 1 publishing through the existing /upload + /publish gate machinery (UK-G1..G7) instead of ad-hoc descriptions, and replace title/thumbnail A/B (unsupported for Shorts) with in-video hook A/B fed into data/learning/ via a named analytics-entry step.
