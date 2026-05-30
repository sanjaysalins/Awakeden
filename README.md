# JesusInTheBible — 60-second gospel-short narration engine

Turns a Bible topic into an engaging, viral-hook, **CTA-to-Jesus** 60-second
narration (KJV), then hands it straight to your existing audio pipeline to
become an MP3.

```
pick series + episode (or custom topic)
        │
        ▼
[1] fetch exact KJV text + surrounding context   (bible-api.com, cached)
[2] generate draft   (Opus 4.7, Gospel Five-Beat: Hook→Point→Proof→Conviction→Landing)
[3] self-review + revise   (5-agent panel + 6 gates; revise while any gate FAILs)
[4] INDEPENDENT red-team audit   (fresh hostile auditor, authoritative — STANDARD, always on)
        │
        ▼
write  <NN Title>/v1/  into the existing narration tree
   narration.md            ← plain prose, paragraphs = beats (audio-pipeline input)
   voices.json             ← narrator + any character voices (jesus, disciples, …)
   narration.creation.json        ← provenance (draft + full review)
   narration.creation-review.md   ← human-readable red-team report
        │
        ▼
auto-run audio  (Shorts mode, default):
   verify → tag → audit   (narration_pipeline.py stages)
   per_turn_synth.py --target 59 --pre-quote-pause 0.4 --stability 0.65
                          → duration-locked narration.mp3 (~59s)
   (set SHORTS_MODE=0 for the natural-length one-shot dialogue synth instead)
```

## Setup

```
python -m pip install -r requirements.txt
```

`.env` (this project) needs:

```
ANTHROPIC_API_KEY=...        # the text engine
# CLAUDE_MODEL=claude-opus-4-7   (default; set a cheaper model to trade quality for cost)
```

The downstream audio pipeline reads `ELEVENLABS_API_KEY` (and its own
`ANTHROPIC_API_KEY`) from the **PythonProject1 root `.env`** — unchanged.

## Run

```
python cli.py                 # interactive: pick series → episode → notes
python cli.py --no-audio      # write the narration folder, skip the MP3 step
```

It prints the verdict, the folder path, and where the review report landed.

## What it produces

A folder in your existing narration tree
(`PythonProject1/jesus/narration/<NN Title>/v1/`) shaped exactly the way
`narration_pipeline.py` expects, so its `verify → tag → audit → synth` flow,
versioning, the 59s-Shorts path (`per_turn_synth.py` / `PLAYBOOK_shorts.md`),
and Hindi translation all apply unchanged.

## How the writing is controlled

- **`data/constitution.md`** — the 60-second charter: hook craft, word budget,
  KJV-verbatim rule (incl. keeping narrative frames in the narrator's voice),
  **grace-anchored conviction** (no gain/loss selling, no manufactured pressure),
  and the plain-prose output discipline the audio tagger needs.
- **`data/structures.json`** — the narration **structures**. Default is the
  **Gospel Five-Beat** (`Hook → Point → Proof → Conviction → Landing`), each beat
  with a time + word budget and pace. The engine writes one block per beat;
  `narration.md` is the beats joined.
- **`data/series.json`** — the 8 greenlit series (hook/CTA patterns, binding
  guardrails, episodes with KJV refs).
- Constitution + series are a **prompt-cached** system prefix shared across calls.

### Validation — four pillars + structure + craft (always independently audited)

Every draft is graded on blocking gates that cite evidence:
1. **Biblical accuracy** — KJV verbatim, reference correct, sound *in context*
   (the surrounding verses are fetched and given to the auditor; flags proof-texting).
2. **Relevance** — a real, present human ache named in the hook and sustained.
3. **Conviction** — pierces (holy tension), grace-anchored, never manipulative.
4. **CTA lands with Jesus** — a grace-based invitation to Christ, ending on a question.
5. **Structure conformance** — all beats present, in order, within budget.
6. **Craft** — standalone, plain prose, clean pacing.

A self-review drives revisions; then an **independent red-team audit** (a fresh,
deliberately hostile auditor that assumes the writer and the self-review are biased)
re-verifies the final draft from scratch. Its verdict is authoritative — nothing
ships on the self-review alone. The revise loops stop when there are **zero FAIL
gates** (CONDITIONAL/CAUTION are advisory). Both reviews are saved in the sidecars.

To add a series/episode, edit `data/series.json`. To add/select a structure, edit
`data/structures.json` (or set `NARRATION_STRUCTURE`). To change global rules, edit
`data/constitution.md`.

## Configuration (env, all optional)

| Var | Default | Purpose |
|---|---|---|
| `CLAUDE_MODEL` | `claude-opus-4-7` | text-engine model |
| `INDEPENDENT_REVIEW` | `1` | always-on independent red-team audit; `0` to disable (cheap dry run) |
| `REVIEW_MODEL` | = `CLAUDE_MODEL` | model for the independent auditor (point at another for stronger independence) |
| `NARRATION_STRUCTURE` | `gospel-five-beat` | which structure in `data/structures.json` to use |
| `MAX_REVISIONS` | `2` | revise passes (shared across self-review and independent audit) |
| `TARGET_WORDS_MIN` / `_MAX` | `135` / `165` | ~60s word band |
| `NARRATION_PROJECT_DIR` | `…/PythonProject1/jesus` | where the audio pipeline lives |
| `NARRATION_TREE_DIR` | `…/jesus/narration` | where narration folders are written |
| `NARRATION_PYTHON` | auto-detected | interpreter used to run the audio pipeline |
| `SHORTS_MODE` | `1` | `1` = duration-locked per-turn synth; `0` = natural-length dialogue synth |
| `SHORTS_TARGET_SECONDS` | `59` | final MP3 duration target in Shorts mode |
| `SHORTS_PRE_QUOTE_PAUSE` | `0.4` | silence before each character (e.g. Jesus) quote |
| `SHORTS_STABILITY` | `0.65` | eleven_v3 stability (steadier reused character voices) |

Voice IDs for character speakers live in `config.VOICE_MAP`. If a script uses a
speaker with no mapping, it's flagged and reads as the narrator until you add it.

## Notes

- **Scripture accuracy:** the exact KJV verse is fetched and handed to the model
  to quote verbatim; a gate checks it. If the lookup is offline, the verse is
  flagged "unverified" in the review — check it by hand.
- **Cost:** ~ a few cents per narration for the text engine (2–4 Opus calls with
  prompt caching), plus the audio pipeline's ~$0.18/narration.
```
