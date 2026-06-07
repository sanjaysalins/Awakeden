# Independent review — claude (OK, 208s)

Verified the plan's claims against the actual code. Most check out. Here's my adversarial read.

## What I verified TRUE (the plan is honest about the codebase)

- **Corpus has the comma:** HF-POC `kjv.json` Ps 22:7 = `shake the head, {saying},` ✅
- **Cache drops it:** `data/kjv_cache.json:53` = `shake the head saying,` (no comma after "head") ✅
- **`norm()` is punctuation-blind:** `short_gate/kjv.py:74` `re.sub(r"[^A-Za-z0-9'\s]", " ", text)` — would miss the comma even with the right corpus ✅
- **G7 is too weak:** `gates.py:346` landing match is `conditional` (non-blocking); only `thread_slug` is blocking (`:336`); no CTA/opener check ✅
- **8/8 close on "Come to Him"** and #02 uses lowercase + em-dash (`That's Jesus — come to him`) — confirms exact-match catches 7, normalized catches 8 ✅
- **Block format matches A1's regex:** `**[narrator — KJV, Psalm 22:7-8]**` with range refs ✅
- **Learning loop inert:** `append_record` (`learning.py:45`) has zero callers ✅

So the reuse-first discovery is real and porting-not-editing genuinely avoids duplication. Good. But there are **new risks the port introduces** that the plan under-specifies:

## 🔴 Risk 1 (headline) — Blocking CTA-fingerprint collides with the CTA-to-Jesus lock

A2: *"CTA/opener repetition is BLOCKING"* and *"the normalized CTA match always runs and is never whitelisted."*

But the **model is locked to CTA-to-Jesus** (`CLAUDE.md` locked decisions). Every short SHOULD invite to Christ. If you fingerprint the **invitation verb** (`come to him`) and block on repeat, you make it **structurally impossible to ever lock two CTA-to-Jesus shorts** — across all 76. The gate would fight the doctrine.

The defect isn't "they invite to Christ" — it's "they invite in **identical phrasing**." The gate must fingerprint the **whole closing sentence's wording/shape**, distinguishing *templated identical phrasing* from *same doctrinal destination*. As written, "never whitelisted" bans the destination. **This is the single biggest design hole and it's one sentence of hand-waving.**

## 🔴 Risk 2 — Root cause #2 is only HALF closed

The plan hardens the **lock** (catches a corrupt quote). It does **not** touch the **generation input**: `pipeline/kjv_check.py` + `data/kjv_cache.json` + bible-api still feed the author the comma-less verse while drafting. You'll catch the bad quote at lock — *after* a human wrote against a corrupt source. The plan never retires/redirects the corrupt cache, yet C1 claims *"quote logic consolidated (no parallel module)."* Either redirect `kjv_check.py` to the pinned corpus or say plainly that the corrupt cache stays live upstream.

## 🟠 Risk 3 — Copying the corpus forks the source of truth

B2 copies HF-POC → `data/kjv_corpus.json`. But `short_gate.kjv.resolve_kjv_path()` still reads the **live** HF-POC file (or `JESUS_KJV_CORPUS`). Now there are 3 KJV sources. A copy **goes stale** if HF-POC's corpus is ever corrected. Cleaner: point at the pinned path via `JESUS_KJV_CORPUS` (the env hook already exists, `kjv.py:41`) rather than duplicating. The "single source of truth" goal undercuts itself by copying.

## 🟠 Risk 4 — Rebuild-from-disk must read the LOCKED snapshot, not the live md

A2's rebuild-from-disk is a good fix for phantom entries. But `.locked` hashes **spoken text** — it doesn't store the fingerprints. If a folder is `.locked` then its `narration.md` is edited *without* re-locking, rebuild ingests the **edited** text into the registry = phantom problem in a new costume (registry reflects working tree, not locked state). The rebuild must read the snapshot the `.locked` hash certifies, or re-validate the hash before ingesting.

## 🟠 Risk 5 — A1 and B3 contradict on untagged inline quotes

- A1: untagged spans *"resolve or are explicitly listed (not silently dropped)."*
- B3: *"Unwitnessed/unmappable ref → BLOCK lock."*

The existing LOCKED shorts contain untagged inline fragments (#01 `"that the scripture might be fulfilled"`). Which wins — listed-and-pass, or unmappable-and-block? If block, none of the current shorts lock without retagging. Resolve the contract explicitly.

## 🟡 Minor but real

- **A3 is a self-fulfilling fixture.** The detector is *built* to find `come to him`; passing A3 proves it catches the one string it was written for, not that it generalizes. Fine as a **regression fixture** — wrong to call it *"the whole-effort gate."*
- **"Non-bypassable" is overstated.** `per_turn_synth --no-gate` stays (you don't edit it). The plan itself calls it a *"documented, discouraged bypass."* Then don't headline the keystone as non-bypassable.
- **`_extract_spoken.py` has zero importers** (grep confirms) — so retiring it is *safe*, but the premise that captions currently flow through it is stale. Low risk, just inaccurate.
- **Punctuation-strict needs whitespace-renorm AFTER stripping `{…}`** (corpus `head, {saying},` → double space). One line, easy to miss.
- **`cli_lock.py` vs `verify_narration.py` overlap** — both run the deterministic tier. Two verify entrypoints is the "parallel module" the plan says it avoids. Have the lock *call* verify.

## Go/no-go

Direction is **correct**: reuse-first is right, porting avoids duplication legitimately, and the two root causes are real. But it is **not yet safe to implement** — Risk 1 (blocking CTA vs locked doctrine) would brick the whole catalogue, and Risk 2 leaves half the Scripture-trust hole open. Both are design-level, not code-level. Fix those two in the plan, resolve the A1/B3 contract, and it's a build.

VERDICT: REVISE
TOP FIXES:
1. Redefine the CTA gate to fingerprint **closing-sentence phrasing/shape**, not the invitation verb — drop "never whitelisted" for the destination, or you make it impossible to ever lock two CTA-to-Jesus shorts (collides with the locked CTA-to-Jesus model).
2. Close root cause #2 on the **input** side: redirect `pipeline/kjv_check.py` off `data/kjv_cache.json` to the witnessed corpus (and read it via `JESUS_KJV_CORPUS`, don't fork a stale copy), so the author never drafts against a corrupt verse — not just catch it at lock.
3. Resolve the **A1↔B3 contradiction** on untagged inline quotes (resolve-or-list vs block-the-lock) and make rebuild-from-disk read the **locked snapshot**, not the live md.
