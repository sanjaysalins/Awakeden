# Awakeden site copy — reframe (2026-06-20)

## The change in one line
The site was framed as a single narrow topic — **"Jesus in the Old Testament. Prophecy, fulfilment, trust Him."** The brand is actually about **finding Jesus in the WHOLE Bible — every encounter, every prophecy, every promise, Old Testament AND New.** "Jesus in the Old Testament" is just **one topical series among several** (miracles, questions, encounters, titles, "I AM", kingdom). The whole-Bible identity leads everywhere (H1 "Find Jesus in the whole Bible"). Honesty about current inventory is carried by (a) a stated on-page line under "Launching first", (b) the meta description, and (c) the featured cards — the homepage states the *mission*, never that NT videos are watchable yet.

## Scope (from the user's Drive: `0 Christianity/`)
Eight series folders exist; seven are public-facing, "Suffering" is exploratory and omitted from the public roadmap.
1. Jesus in the Old Testament (Isaiah 53, Psalm 22 — already in the studio; lives in the catalogue, NOT the roadmap)
2. Questions Jesus Asked
3. The Miracles of Jesus
4. People Who Encountered Jesus
5. Titles of Jesus
6. The "I AM" Sayings
7. The Kingdom of God
8. (Suffering — exploratory; not shown publicly)

The public **roadmap** = the **six** genuinely-forthcoming series (2–7). Series 1 is already in the studio, so it appears in the catalogue, not the slate.

## Doctrinal guardrails kept (from CLAUDE.md / locked decisions)
- KJV verbatim for Scripture; gospel kept clear, not buried.
- Grace-anchored — no fear / gain-loss / manufactured-pressure framing.
- Freshness = faithful depth: novel entry point, orthodox claim and landing.
- OT and NT both witness to Christ — "the same Lord in both" (does not demote the OT's witness, which is the project's own thesis).
- Claims stay defensible: "every **promise** points to Him" (2 Cor 1:20), NOT "every word" (which over-reads the text).

## Final copy — exact strings now live in the files

### Brand (`config.yaml`)
- **Tagline:** Finding Jesus in the whole Bible — every encounter, every prophecy, every promise.
- **Mission:** Awakeden is a video series about finding Jesus in the whole Bible — Old Testament and New, the same Lord in both. He is the thread running through all of it: the encounters, the prophecies, the promises kept. We go a little deeper into the text to meet Him, and ask what it means for life now. Some series focus on one window — the Old Testament, His miracles, the questions He asked, the people who met Him. Serious about the Bible. Clear about the gospel. Made to draw you in, not wear you down.

### Home (`index.html`)
- **Title:** Find Jesus in the Whole Bible | Awakeden Series
- **Meta:** A video series finding Jesus across the whole Bible — Old Testament and New. First up: Isaiah 53 and Psalm 22, with New Testament series on the way.
- **Hero H1:** Find Jesus in the whole Bible
- **Hero lead:** A video series about finding Jesus across all of Scripture — Old Testament and New. Every encounter, every prophecy, every promise. We go deeper into the text to meet Him, and to see why it still speaks today.
- **"Launching first" note (visible on-page honesty line):** The first studies are from the Old Testament — Isaiah 53 and Psalm 22. New Testament series are on the way.

### About (`about.html`)
- **Lead:** Bible films and shorts about finding Jesus in the whole Bible — Old Testament and New — and why it still speaks today.
- **Body 1:** Awakeden is about finding Jesus in the Bible — Old Testament and New. He is the same Lord across all of Scripture, the thread running from the first promise to the empty tomb. We read closely, go a little deeper, and ask what it means for the life you are living now.
- **What to expect:** Some series focus on one window of Scripture — Jesus in the Old Testament, the Miracles of Jesus, the Questions Jesus Asked, the people who met Him, His titles and "I AM" sayings, the Kingdom of God. The first studies are Isaiah 53 and Psalm 22, with more on the way.

### Roadmap (`manifest.yaml` → roadmap)
The six forthcoming series (2–7), rendered on the Roadmap page ("on the slate"). The live OT series is deliberately NOT in the roadmap — it's in the catalogue.

## Honesty model (how the whole-Bible promise stays truthful at prelaunch)
The whole-Bible line states what the series is *about* (its mission), not that NT videos exist. Three on-page signals keep it honest: the "Launching first" note naming the two OT studies, the meta description ("First up: Isaiah 53 and Psalm 22"), and the featured cards (OT titles + status badges). No line claims anything is published — site `mode: prelaunch`, all `youtube_id: null`, CTA reads "Launching on YouTube soon."

## Review history (red-team + AI panel, this session)
Two red-team agents + two 5-CLI panel runs (3/5 valid each — gemini/grok fail on a Windows env warning + garbled output, a known panel-health issue). Convergent flags caught and FIXED:
- Bait-and-switch (OT+NT promised, OT-only inventory) → added the visible "Launching first" OT-first note + meta + cards.
- Doctrinal over-read "every **word** points to Him" → changed to "every **promise**" (2 Cor 1:20).
- Doctrinal demotion "Old points / New reveals" → "the same Lord in both" (now on About + mission).
- Over-repeated triad (6×) → full triad twice (tagline, hero), varied elsewhere.
- "First studies **out**" implied published → "First up" / "The first studies are".
- About listed the live series under "planned" → removed; planned list = the 6 forthcoming only.
- Meta over-length → tightened, honest phrase front-loaded.

## Flagged to the user — NOT auto-changed (pre-existing copy in shipped shorts; your call)
1. **"David wrote the crucifixion a thousand years before *Rome invented it*"** (Psalm 22 hook, `manifest.yaml` + `series/psalm-22.html`) — historically brittle: crucifixion predates Rome. One-word fix: "before Rome perfected it" / "before the cross existed."
2. **"Who do you say I am? / Why are you afraid?"** — modern paraphrase, not KJV verbatim (KJV: "whom say ye that I am?" / "why are ye fearful?"). But these are your episode *titles*, not Scripture in narrator voice.

## Known follow-ups (UX, not copy — not done this pass)
- Catalogue cards don't show a **series label**, so "Jesus in the Old Testament" isn't visible as one series among many (the reframe is prose-only in the catalogue). A small `catalog.js` change would render the series on each card.
- `config.yaml` tagline/mission are compiled into `catalog.json` but never rendered (no template reads `brand.*`). They're a source-of-truth record only; wiring them to the footer/About would remove the dead-copy drift.

## What did NOT change
- Per-item hooks/blurbs for Isaiah 53 and the Psalm 22 cluster (apart from the flagged "Rome" line) — they sit *inside* the "Jesus in the Old Testament" series.
- Wordmark "Awakeden", scripture note, launch CTA, all structure/JS.
