# Independent review — cursor (OK, 44s)

## Independent adversarial review — Upload Kit *Why Was Jesus Born in Bethlehem?*

### Process / integrity

- **YouTube (Short), YouTube (Long-form), Facebook — footer:** `Scripture quoted from the King James Version (KJV), public domain.` Your own in-artifact red-team already flagged this as wrong (KJV is **not** universally public domain; UK Crown letters patent). The body still ships the bad line while the header claims **UK-G2 pass** and **ALL PASS ✅** — that’s credibility damage, not a nit.
- **Verification block vs embedded red-team:** Header says gates **ALL PASS**; hostile auditor block says **`VERDICT: REVISE`** on the same footer. You’re asking the uploader to trust a checklist that disagrees with the audit printed underneath it.

### HOOKY BUT HONEST / bait-and-switch

- **All platforms — opening:** `The experts knew. Who went to see the King?` Honest **if** the viewer finishes the short (narration pays off: experts cited Bethlehem; Scripture doesn’t say they went; wise men went). On **TikTok** and **Instagram**, the caption **ends on the unanswered question** with no spoiler line — fine as a watch hook, but borderline bait on scroll-off platforms where most never hear the payoff.
- **YouTube (Short) — description:** Full block quotes for **Micah 5:2** and **John 6:38** read like “what you’ll hear.” The locked narration only speaks a **fragment** of Micah (“ruler in Israel”) and **paraphrases** heaven/resurrection (no spoken John 6:38; no verbatim 1 Cor 15). Not false doctrine, but metadata oversells **spoken KJV** vs **study quotes in the box**.
- **YouTube + Facebook — body:** `the prophet Micah named a small town` — same wording as narration; sceptical readers may hear “Micah invented Bethlehem” rather than “Micah **identified** Bethlehem among towns.” Safer: “named **which** town” or “pointed to Bethlehem.”

Titles (`Why Was Jesus Born in Bethlehem?`) are search-honest; the **experts** angle is the actual differentiator (option 3 in your list is sharper for click honesty than option 1).

### KJV verbatim (quoted strings in kit)

- **Micah 5:2 quote (YouTube Short, Facebook):** Matches project KJV cache — no altered words in the pasted verse.
- **John 6:38 (YouTube Short only):** Standard KJV wording; not re-verified in `kjv_cache.json` here, but no obvious corruption (`mine own will`, `him that sent me`).
- **1 Corinthians 15:3–4:** Cited in “Read it yourself” / tags, **never quoted** — OK, but **YouTube Short tags** `1 corinthians 15 3-4` advertises a reference the description doesn’t quote and the video doesn’t speak verbatim.

### Doctrine

- Gospel landing **YouTube / Facebook:** `Before anyone went to Him, He came to us` plus resurrection/sin thread in the film — evangelical, Christ-pointing, no fear/works hustle.
- **TikTok / Instagram:** That landing line is **dropped**; only `Find Jesus in the whole Bible… Follow Awakeden. ✝` — on-brand but **weaker Christ-landing** than sibling platforms for the same file.

### Platform fit

- **Format mismatch — `YouTube (Long-form 16:9)` section:** Artifact says **`Format: short`** and points at `bethlehem_final.mp4` (9:16 short). A full long-form title/description/tags block invites a **second upload shape that doesn’t exist** for this piece — wrong template, duplicate SEO, uploader error risk.
- **TikTok — first line:** `Why was Jesus born in Bethlehem?` — strong question hook; good.
- **Instagram — first line:** Same structure as TikTok with tiny edits — **interchangeable**, not tuned for IG save/discovery habits.
- **Instagram hashtags:** `#WiseMen #ChristmasStory` — very broad; weak signal vs `#Nativity` / `#Micah` / prophecy cluster (your red-team already noted optional trim).
- **TikTok hashtags:** Only five (`#Bethlehem #BibleProphecy #Jesus #Bible #Micah5`) while IG gets eight including seasonal tags — uneven seasonal capture for a nativity-adjacent piece.
- **TikTok / Instagram:** No `awakeden.com`, no KJV attribution line — may be intentional, but **Facebook/YouTube get the full footer; short social gets a thin strip**.

### SEO honesty / templating

- **YouTube Short — tags:** `who was micah in the bible` — the video never teaches Micah’s biography; **keyword stretch** for prophecy fulfilment content.
- **YouTube Short — tags:** `king herod and the wise men` **and** `the wise men and herod` — near-duplicate intent, not distinct search angles.
- **Repeated boilerplate** across YouTube Short, Long, Facebook: `Bible prophecy (Micah 5:2): Bethlehem was named 700 years before Jesus. The experts knew. Who went to see the King?` — honest but **same card everywhere**; title option 1 is the safest SEO title and also the **most generic** (hard to win click without the experts hook in the title itself).

### Brand / CTA / links

- **YouTube / Facebook:** `Subscribe to Awakeden` / `Follow Awakeden`, `https://awakeden.com`, `@awakeden` link — not mangled.
- **TikTok / Instagram:** CTA present; **no** subscribe link block (platform-normal).

### What’s actually fine (so this isn’t FAIL)

- No copy says experts **refused** or **stayed home** (matches narration).
- `tax order` / Luke 2 framing is correct.
- `700 years` is conventional rounding, not sensational chronology.
- Chosen title matches the piece topic and doesn’t overclaim miracle footage you don’t have.

---

VERDICT: REVISE  
TOP FIXES:  
1. Replace every footer `Scripture quoted from the King James Version (KJV), public domain.` with neutral wording (e.g. `Scripture quotations: King James Version (KJV).`) and align the **ALL PASS** header with that fix.  
2. Remove or clearly gate the **`YouTube (Long-form 16:9)`** block for this **short-only** asset so uploaders can’t paste long-form metadata onto a Short.  
3. Add the spoken payoff (`Before anyone went to Him, He came to us.`) to **TikTok/Instagram** captions; trim **Instagram** broad tags and **YouTube Short** tag fluff (`who was micah in the bible`, duplicate Herod/wisemen tags); label description block quotes as **read-in-KJV** if they’re not spoken verbatim in the cut.
