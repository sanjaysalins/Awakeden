# bible_kb — the Biblical-Universe knowledge base

A growing, reusable, **Scripture-cited** fact bank that makes every generated
still *biblically driven* and *checkable*. Sibling to `image_library/`,
`sound_library/`, `music_library/`.

Engine: `pipeline/bible_kb.py`. Driver/proof: `bib_validate.py`.

## Layout

```
bible_kb/
  characters/   aaron-high-priest.json, ...
  places/       holy-of-holies.json, tabernacle.json, ...
  objects/      priestly-garments.json, ark-mercy-seat.json, ...
  customs/      day-of-atonement.json, ...
  eras/         wilderness-tabernacle.json, ...
```

Each file is ONE entity. The KB **grows from VERIFIED derivations** — when an
episode's fact sheet passes citation-hydration + the panel, its facts are
promoted here (`bible_kb.promote_to_kb`). Don't hand-author guesses; cite.

## Entity schema

```json
{
  "slug": "day-of-atonement",
  "name": "The Day of Atonement (Yom Kippur)",
  "facts": [ <FactCard>, ... ]
}
```

## FactCard schema

```json
{
  "claim": "On the Day of Atonement two goats were taken for one sin offering.",
  "bucket": "specified",
  "scripture": ["Leviticus 16:7", "Leviticus 16:5"],
  "kjv_text": "<fetched VERBATIM from scripture.py — never hand-typed>",
  "historical_note": "<secondary; may never override Scripture; usually empty>",
  "visual_directive": "Show TWO goats together before the priest, not one.",
  "banned_anachronisms": ["a single goat", "a lamb or bull in the goats' place"],
  "verified": true,
  "entity": "day-of-atonement"
}
```

### The three buckets (the whole point)

| bucket | meaning | gate |
|---|---|---|
| **specified** | the Bible STATES this visual fact | **fail-closed** — image must match |
| **constrained** | not stated, but a depiction could CONTRADICT the text | fail only on contradiction |
| **free** | artistic licence; Bible is silent | not checked |

Without the buckets the check fails on everything (most of a painting is not in
the Bible). Scripture is **binding**; historical notes are **secondary** and may
never override it.

### Citation integrity

The LLM proposes only the `claim` + `scripture` reference. `kjv_text` is fetched
**verbatim** from `pipeline/scripture.py` (bible-api.com, cached). A `specified`
fact whose citation can't be verified is **downgraded to constrained** and
tagged — it can never gate a pass on a guess.
