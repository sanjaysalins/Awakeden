# Independent review — cursor (OK, 75s)

Independent adversarial read of the Day of Atonement upload kit. I checked the artifact against `pipeline/upload_gates.py`, the KJV cache for Leviticus 16:15, and the kit’s own gate output.

---

## Critical — do not paste as-is

### 1. Header overclaims readiness while gates are red
The kit opens with **“Copy each block straight into the platform's upload form. Title, description, tags and hashtags are pre-checked, red-teamed and panel-reviewed.”** but immediately shows **`Gates: FAILURES ❌`**, UK-G2 is red, and **`panel_verdict` is empty** in the source JSON. That is paste-ready copy on a kit that explicitly failed deterministic checks and has no external panel sign-off.

### 2. UK-G2 KJV-strict — Facebook + YouTube (Short): ellipsis quotes fail the gate
**Facebook:** `"Then shall he kill the goat of the sin offering... and sprinkle it upon the mercy seat, and before the mercy seat" - Leviticus 16:15 (KJV)`

**YouTube (Short):** `"Then shall he kill the goat of the sin offering... and sprinkle it upon the mercy seat" - Leviticus 16:15`

These are **not** continuous KJV substrings. After normalization, UK-G2 requires the quoted span to sit inside the anchor verse as one block. Leviticus 16:15 has a long middle clause between “sin offering” and “and sprinkle it upon the mercy seat” (`that is for the people, and bring his blood within the vail, and do with that blood as he did with the blood of the bullock`). The `...` skips that middle, so the gate correctly flags both platforms.

**YouTube (Long-form)** passes because it quotes the **full** verse with no interior ellipsis:
`"Then shall he kill the goat of the sin offering, that is for the people, and bring his blood within the vail, and do with that blood as he did with the blood of the bullock, and sprinkle it upon the mercy seat, and before the mercy seat:"`

**Internal contradiction:** the in-engine red-team says *“both KJV quotes (full and ellipsis-truncated) are exact verbatim substrings”* while the verification block already marks UK-G2 ❌ on exactly those ellipsis quotes. One of those cannot be true.

**Fix pattern:** use a **contiguous** fragment (e.g. the tail `"sprinkle it upon the mercy seat, and before the mercy seat"`) or the full verse — not a middle-skipping ellipsis.

---

## Doctrine

### 3. Instagram — landing line reverses the piece’s own thread
**Instagram:** `Your sin is not covered, it is carried away.`

Every other platform keeps the qualifier:
- **YouTube (Short):** `Your sin is not just covered. It is carried away.`
- **YouTube (Long):** `If your sin is on Him, it is not just covered for another year. It is carried away...`
- **TikTok / Facebook:** `Your sin is not just covered. It is carried away.`

Dropping **“just”** on Instagram reads as: Levitical blood **never** covered sin at all. That clashes with Leviticus 16 itself (real annual cleansing) and with this episode’s locked narration thread (“real, but never final”). This is not a stylistic tweak; it is a doctrinal bait-and-switch on one platform.

---

## Platform / format fit

### 4. YouTube (Short) slot is attached to the wrong asset
Header says **`Format: long`** and the video path is `DAYOFATONEMENT_LONG_living_sketchbook_cc.mp4` (~6–8 min, 16:9). Yet a full **YouTube (Short)** block is generated with the same teaching arc, `"Subscribe to Awakeden"`, tags, and a title identical to the long hook.

Project notes (RESUME) say Day of Atonement’s **3 companion shorts are still unbuilt**. Pasting the Short slot against this long file mislabels a deep-dive as `<60s` vertical content. Either remove/hold the Short slot until a real short exists, or label it explicitly as cross-post copy for a future asset — not for this file.

### 5. YouTube (Long-form) — missing chapter timestamps
For a 6–8 minute long, the description has no `0:00` chapter block. Not a UK-G1 fail in this kit, but for long-form YouTube SEO and UX it is weaker than sibling long kits and below what `/publish` expects downstream. Not blocking today, but the long slot is not fully “long-form ready.”

---

## SEO / honesty (minor)

### 6. YouTube (Long-form) tags — one stretch keyword
**Tags:** `... Bible prophecy, Christian teaching`

This episode is typology / Day of Atonement / scapegoat / Hebrews fulfillment. **“Bible prophecy”** is a reach for Leviticus 16 typology and looks like tag-stuffing next to honest tags like `scapegoat`, `mercy seat`, `types and shadows`.

### 7. Prose precision drift in short slots
**YouTube (Short) / TikTok / Facebook** use **“the priest”**; **YouTube (Long)** correctly names **“Aaron.”** Leviticus 16 is Aaron-specific. Not a KJV violation (it is prose, not a quote), but the short captions are slightly less text-faithful than the long description.

---

## What holds up (so fixes are surgical, not a rewrite)

- **Chosen title** `Why Did One Sacrifice Need Two Goats?` — honest curiosity hook; true to Lev 16’s two-goat sin offering. Not clickbait.
- **Alternate titles** — no sensational overclaim; option 4’s cross-resolution matches the locked thread.
- **YouTube (Long) KJV quote** — verbatim Leviticus 16:15.
- **Doctrine elsewhere** — grace-anchored CTAs (`Come to Him`, `You have only to come`); no fear/gain-loss/works pressure detected.
- **TikTok / Instagram first lines** — `Why did ONE sacrifice need TWO goats?` is a strong above-the-fold hook (Instagram’s hook is fine; its landing line is not).
- **Hashtag counts** — within house targets on all platforms.
- **Brand footer** — CTA-to-Jesus + `awakeden.com` + follow block present on link-capable platforms; not mangled.

---

## Templated / forgettable (non-blocking)

- Title option 2: **`The Goat That Never Died (And What It Means for You)`** — the parenthetical is generic self-help packaging; not chosen, but weak if ever rotated in.
- Fixed footer **“one panel at a time”** on a living-sketchbook long — same brand-line mismatch flagged on Seed of the Woman; intentional tagline or not, it does not describe this visual format.

---

VERDICT: REVISE
TOP FIXES:
1. Fix UK-G2 on **Facebook** and **YouTube (Short)** — replace middle-skipping ellipsis quotes with a contiguous KJV fragment or the full Leviticus 16:15 verse (match **YouTube (Long-form)**).
2. Restore **Instagram** landing to **`Your sin is not just covered. It is carried away.`** — the dropped “just” currently contradicts Leviticus 16 and the episode’s own theology.
3. Remove or clearly quarantine the **YouTube (Short)** slot until a real short-form cut exists; do not paste Short metadata onto the 16:9 long file, and strip the “copy straight in / panel-reviewed” header until UK-G2 is green and panel is done.
