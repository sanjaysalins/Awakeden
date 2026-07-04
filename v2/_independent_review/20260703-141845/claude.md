# Independent review — claude (OK, 274s)

Verification done. Most of the plan's code-cited claims check out against the repo — I confirmed the batch layout (`narration.md`, `audio/alignment.json`, `visual/<slug>_scored.mp4` in all 7 pieces), `livingpage_short.spec.json` in exactly 7 of 8 pieces with beat times + captions, `upload_engine.py:80-133` reading only the v2 layout, `manifest.yaml public_status` existing, `corpus_diversity.py` existing, and `data/upload_brand.json` full of FILL_ME. The panel-fold work in §12 is genuinely reflected in the doc. But adversarial checking of the *numbers* turned up real problems.

## Findings

**1. The launch-runway build task is arithmetically broken — three different numbers, none matching the manifest (§4 vs §5/§10.2 vs `batches/batch_manifest.json:33-46`).**
§4 says "The remaining ~6 Cross shorts are the FIRST build task"; §5 and §10 step 2 say "~4 unique (manifest minus the 2 duplicates)". The actual manifest has **13** shorts (not ~14): 8 banked in `batches/cluster_01_cross/`, 2 duplicates ("It is finished (last-week)" duplicates it_is_finished; "thief on the cross" duplicates today_paradise), and **3 marked `built` from the legacy pipeline** (Crucifixion Foretold Ps22, "My God why forsaken", "I thirst"). So the remaining *unique unbuilt* count is **zero** — the "~4" only makes sense if the 3 legacy pieces are being re-rolled, which the plan never says. This matters because the ≥9 launch gate and the bank-runway math both hang on this number. The plan needs an explicit slug list of what gets built, not "~4/~6".

**2. The 3 legacy-built Cross pieces silently violate the brand promise (§2 vs manifest lines 34/40/41).**
§2 promises "every panel is drawn, every quote is the actual Bible" — a consistent inked comic universe. The three legacy Cross shorts are old-pipeline Baroque, and per your own memory the Psalm-22 shorts are 100% single-narrator (re-voicing pending). Either they publish and break the promise/style coherence of the channel's first weeks, or they're rebuilt to living-page — which is unbudgeted, unscheduled work the plan doesn't name. Decide and write it down.

**3. §8 reuse figures don't match the actual index (§8 "50 registered stills + 42 clips").**
`asset_index.json` today contains **44 stills + 34 clips**. Either registration wasn't completed for all 8 pieces (in which case Phase 0 needs a "verify cluster-1 registration complete" step — reuse economics is the plan's central cost claim) or the figure is projected/stale. Fourteen assets is not rounding error.

**4. "Copyright: music from our own Suno library... all art generated in-house" (§11) overclaims settled rights.**
Suno commercial-use rights depend on the subscription tier, AI-music copyright is unsettled, and Content ID collisions with other Suno users' similar generations are a known monetization/claim risk on YouTube. This is exactly the kind of platform risk §11 exists to name, and it's currently written as a non-risk. Verify the Suno plan tier grants commercial use and add Content-ID claims to the watched-risk list.

**5. Cluster-2 serialization is the real bank threat, understated (§5 bank invariant vs §3 "write the long first" rule vs §10 step 10).**
The Cross bank at launch is ~9–12 pieces ≈ 3–4 weeks at 3/wk. Every Resurrection short is gated behind the Jonah long per the long-first rule, and a 9–12-min long with full panel discipline is not a same-week artifact. Step 10's "distill shorts as sections lock" is the right mitigation but it's a parenthetical; the plan should state explicitly that section-level distillation (not full-long lock) is the unblock, or the measured "~6 shorts/week" claim — which was earned inside an already-built Golgotha world — doesn't transfer to week 4.

**6. Minor: the §3 cost-note paragraph is inserted mid-table**, orphaning the "Role" row from the Markdown table — it will render broken. And the §5 hook-archetype tagging "at C0 time" needs a one-time backfill for the 8 already-banked pieces or the first month of analytics has no archetype labels.

**7. Minor scope trim (Phase 0 step 6):** SPF/DKIM/DMARC is *sending* infrastructure; the launch metric only needs *capture* (a form + provider list). Domain auth can slip to before the first send — Phase 0 is already 8 workstreams for a solo operator.

The plan's structure, gates, and honesty discipline are good; the defects are concrete numbers and two unnamed risks, all cheaply fixable.

VERDICT: REVISE
TOP FIXES:
1. Replace "~4/~6 remaining Cross shorts" with an explicit slug list reconciled against batch_manifest.json (13 entries: 8 banked, 2 duplicates, 3 legacy-built), and decide explicitly whether the 3 legacy Baroque/single-narrator pieces are re-rolled to living-page or excluded from the channel — the launch gate and brand promise both depend on it.
2. Correct §8 to the real index counts (44 stills + 34 clips today) or add a Phase 0 step to complete cluster-1 asset registration before citing reuse economics.
3. Re-write the §11 copyright line: verify the Suno tier's commercial-use grant and name YouTube Content-ID collision on AI music as a watched risk; and promote §10 step 10's "distill shorts as sections lock" from parenthetical to the stated mitigation for the Jonah-long serialization of the cluster-2 bank.
