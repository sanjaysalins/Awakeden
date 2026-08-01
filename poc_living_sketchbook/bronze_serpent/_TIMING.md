# Bronze Serpent — real forced-alignment timing (2026-07-31)

Supersedes the **estimated** windows in `poc_living_sketchbook/
_FABLE_ROUND9_BRONZESERPENT_E2E_PLAN.md` section A1 only. That plan's spread
COUNT, ORDER, beat/text/shot/device assignments are unchanged — this document
replaces its `Est. window` column with real word-onset timings from a forced
WhisperX alignment of the actual, current `narration.mp3` bytes. Do not edit
the Round 9 plan doc itself (it's a dated planning record); this doc is the
correction.

Source files:
`poc_living_sketchbook/bronze_serpent/_s0_align.py` (aligner script, follows
`storm/_s0_align.py`'s exact pattern) → `poc_living_sketchbook/bronze_serpent/
_bronzeserpent_alignment.json` (198 words, `{w, start, end}` per entry, forced-
aligned against `longform/EW04_Bronze_Serpent/v1/short/narration.spoken.txt`).

---

## ⚠️ BLOCKING FINDING — the episode's own sidecar metadata is stale

`narration.meta.json` + `_synth.log` (both dated 2026-06-26) claim the locked
narration.mp3 is **77.65s** total, in 3 turns (witness 0.30–40.62 / jesus
40.87–48.23 / witness 48.53–76.85). The Round 9 plan's A1 table was built on
that claim.

**The actual `narration.mp3` file on disk right now is 69.31s, not 77.65s —
an 8.34s / ~11% discrepancy.** This is not an alignment artifact; I verified
it three independent ways before trusting it:

1. **WhisperX forced alignment** (this pass) — matched all 198 script words
   (ASR independently heard 199) in clean, monotonic, in-order sequence from
   "I" at 0.387s to "live." ending at 68.297s. The word sequence visibly walks
   through Beat 1 → Beat 2 → Beat 3 (incl. the John 3:14 quote) → Beat 4 in
   the correct order with no skips or reordering — strong evidence the
   alignment itself is sound, not broken.
2. **`ffmpeg -i ... -f null -` full decode** (authoritative, not the
   container-header estimate) — reports `Duration: 00:01:09.31`, i.e. 69.31s.
3. **`ffmpeg silencedetect`** (a completely independent method, no
   forced-alignment model involved) — finds the file's last silence region
   ending at `69.309410`s (the true end of file), and its pause locations
   line up with the forced-alignment word gaps to within ~0.02–0.08s at every
   major beat boundary (e.g. silence 26.448→28.068s brackets "live."→"I" at
   the Beat2/Beat3 seam; silence 42.335→43.868s brackets "up:"→"My" at the
   John 3:14 quote's own end).

All three agree. **The real, current `narration.mp3` is ~69.3s.**

**File mtimes make this a genuine staleness bug, not a fluke:**
`narration.mp3` and `_synth.log` are both dated 2026-06-26 14:35; `narration.md`,
`narration.meta.json`, `narration.spoken.txt`, and `.locked` are all dated
2026-06-29 22:40 — three days later. The TEXT content is effectively
unchanged (current `narration.spoken.txt` is 963 chars / 203 words vs. the
old turn split's 543+95+323=961 chars), so this isn't a case of the script
being edited after the audio was cut. Whatever produced the 2026-06-29 touch
on the text/meta files did not regenerate `narration.mp3` or `_synth.log` to
match — or the reverse happened and `narration.mp3` was replaced by a
shorter, real re-render whose metadata was never written back. Either way,
**`narration.meta.json`'s 77.65s / 3-turn-boundary numbers do not describe
the file that is actually on disk today.**

**I did not touch either file** (out of scope for this pass — no text/audio
edits, no spend). **Recommendation: before building this episode, confirm
with the user which is authoritative** — is 69.3s the real final cut (and
`narration.meta.json`/`_synth.log` just need regenerating to match), or is
the 69.3s file an accidental wrong/older render that should be replaced by
the true 77.65s locked version? Everything below uses the REAL, CURRENT
69.3s file, since that's the actual audio bytes that would ship if this
episode were built today — but that choice should be confirmed, not assumed.

**Sanity-check called for by the task, and its result:** "a word timestamped
at 45s should be part of the Jesus quote turn, not witness turns" — under the
STALE boundaries (quote = 40.87–48.23) this holds; under the REAL timeline
the quote is 36.88–42.32s, so a word at 45s is actually well inside the
following witness turn ("...bearing our judgment in our place," 44s-51s
range). This is exactly the kind of contradiction the task told me to treat
as a red flag rather than paper over, and it's consistent with (not
contradicted by) the finding above: the whole real timeline is compressed
~11% relative to the stale metadata, so anything anchored to the old
boundaries reads as "wrong" against the real file for the same reason.

---

## Real total duration

**69.31s** (three independent measurements, see above), vs. the plan's
assumed 77.65s. **Flagged clearly per the instructions above — this is a
meaningfully different number, not a rounding difference.**

## s08 (the insert page) — real bounds

- **Start** — "And" (first word of "And as Moses lifted up the serpent in the
  wilderness..."): **36.879s**. (The word "as" specifically, named in the
  task, starts at **37.040s** if the boundary should sit on "as" rather than
  the leading "And" — I used the full quote's first word, "And," as the
  spread boundary, matching how every other spread in the table starts on
  its first spoken word.)
- **End** — "up:" (last word of the John 3:14 quote, "...be lifted up:"):
  **42.316s**.
- **Quote span (spoken-only): 36.879 – 42.316s = 5.437s**, vs. the plan's
  assumed 7.36s (the full turn-1 duration under the stale metadata).
- Real trailing pause before s09 begins ("My bronze..."): 42.316 → 43.887s
  (1.571s) — independently confirmed by `silencedetect` (42.335→43.868s).

## Landing hold (INV-26) — real anchor

Last word, "live.": **onset (start) = 68.035s, offset (end) = 68.297s.**

- Per the task's literal formula ("real onset ... + 3.0s"): 68.035 + 3.0 =
  **71.035s** minimum file/cut end.
- Per INV-26's own wording ("after the last spoken word" — i.e. once "live."
  has finished being spoken, not when it starts): 68.297 + 3.0 = **71.297s**
  minimum file/cut end. This is the number I'd treat as authoritative for the
  actual gate check (`check_landing_hold.py` compares real audio/video
  durations, and "live." isn't finished being heard until 68.297s) — the two
  differ by only 0.26s, but using the offset is the more correct reading of
  the standing rule.
- Either way: **the current raw `narration.mp3` (69.31s) already ends before
  even the onset-based minimum (71.035s)** — confirming (as expected) that
  the ≥3.0s hold is something the ASSEMBLY stage must add after the
  narration ends (silent hold on the landing still), not something baked
  into the narration.mp3 itself. This matches how INV-26 already works
  elsewhere in this project.

---

## The 14-spread table — real windows

Same spreads, same order, same Beat/Text/Shot/Device columns as
`_FABLE_ROUND9_BRONZESERPENT_E2E_PLAN.md` section A1. `Real window (s)`
replaces `Est. window`. Window = [real start of the spread's first spoken
word, real start of the next spread's first spoken word); s14 ends at the
real last-word offset.

| # | Beat | Real window (s) | Text | Shot | Device |
|---|---|---|---|---|---|
| s01 | 1 | 0.387–3.657 | "I am Moses. My people were dying of snakebite..." (opening clause) | Wide establishing: the camp of tents at the wilderness's edge, Moses in the foreground, a stricken family in the middle distance | **Field Header** overlay ("WILDERNESS. FORTIETH YEAR.") — episode's one header, composited on s01's own art |
| s02 | 1 | 3.657–8.230 | "...and God told me to forge a snake of bronze and lift it on a pole." | Close/mid: Moses's face, grief and urgency, kneeling by a stricken figure | face close-up (shot-variety floor) |
| s03 | 2 | 8.230–11.433 | "The serpents were no accident — we had spoken against God..." | Wide: a knot of the people, gesturing in complaint/discouragement, Moses standing apart | — |
| s04 | 2 | 11.433–14.856 | "...and the venom was the judgment our sin had earned." — the plan's A1 row labels this "(judgment)" and paraphrases Numbers 21:6 ("...the LORD sent fiery serpents..."), but that exact clause is **not** in the locked spoken script; the real audio in this window is the sentence above. Flagged, not fixed — content call, not a timing call. | Serpents among the rocks and tent-lines, people recoiling | — |
| s05 | 2 | 14.856–18.798 | "I begged Him to take the snakes away. He would not." | Moses alone, kneeling in intercession against open sky | no-figure-adjacent atmosphere beat (shot-variety floor) |
| s06 | 2 | 18.798–28.105 | "Instead He told me to forge the image... The bitten had only to look — and live." | Close on Moses's hands at the forge, hammering the bronze serpent into shape | close-up hands (shot-variety floor) |
| s07 | 3 | 28.105–36.879 | "I speak now from the far side of my life, by the light that came after — a night I never saw, when one they called Teacher answered a seeker:" | Moses's face turned toward the horizon/light | **lift_away** transition begins in this spread's last ~0.4s, finishes crossing into s08 |
| **s08** | **3** | **36.879–43.887** (quote itself: 36.879–42.316) | **"And as Moses lifted up the serpent in the wilderness, even so must the Son of man be lifted up:"** (red-letter, John 3:14) | **INSERT PAGE 1 of 2** — Scholar's-Margin (Style 3) typology sheet, two-panel labeled comparison (NUMBERS 21 / JOHN 3) | insert page + controlled reading-order pan + THE WORD ARRIVES WHOLE (LAW 1) |
| s09 | 3 | 43.887–46.386 | "My bronze was only a shadow." | Moses's face, humble, bronze serpent visually smaller/plainer than the gold page just shown — hard cut back from s08 | — |
| s10 | 3 | 46.386–52.572 | "They lifted Jesus on a Roman pole, made a curse for us, bearing our judgment in our place." | Christ lifted up, a reverent Golgotha beat — sacred, restrained, no gore | sacred/reverence beat |
| s11 | 4 | 52.572–57.128 | "So hear me, you who are bitten — that is every one of us." | Moses turns to address the reader directly | — |
| **s12** | **4** | **57.128–62.936** | **"The cure was never in you; it hangs in plain sight, and costs you nothing but a look."** | **INSERT PAGE 2 of 2** — Gilded Proclamation (Style 6) plate, REBUILT 2026-07-31 from a plain Style-1 render: ONE unified gold-ground composition (not a split diagram, no labels) — the dull bronze serpent low/small in the earthbound foreground, Christ lifted on the cross rising radiant in gold leaf above/behind it | insert page + reading-order camera push (see clips/s12_echo.mp4) |
| s13 | 4 | 62.936–66.723 | "Lift your eyes to Jesus, lifted up for you." | Christ lifted, radiant, the landing's approach | — |
| **s14** | **4** | **66.723–68.297** + ≥3.0s hold | **"Look, and live."** | **THE LANDING** — torn-page device, gold light from beneath the tear | torn-page (mandatory), sacred stillness hold ≥3.0s (INV-26) |

**Real finished-cut minimum: ~71.3s** (68.297s last-word-offset + 3.0s
INV-26 hold), vs. the plan's original "~80s" target under the stale 77.65s
assumption — a real, material difference that changes the pacing math (14
spreads over ~69s real narration ≈ 4.9s average, tighter than the plan's own
"~5.5s average" estimate), not just the per-spread boundaries.

---

## Word-by-word hand-check (3+ specific words vs. known/expected anchors)

| word | real time | check |
|---|---|---|
| "And" (start of Jesus quote) | 36.879s | Under the STALE turn boundary this "should" land at ~40.87s — it doesn't (see blocking finding above); it DOES land exactly on `silencedetect`'s pause-end at 36.774s (small pre-quote silence 36.251–36.774s immediately before), independently confirming the real word timing. |
| "up:" (end of Jesus quote) | 42.316s | Immediately followed by a 1.53s silence (42.335→43.868s per `silencedetect`), the largest gap in the entire quote's neighborhood — a real, audible seam, exactly where the quote should end. |
| "live." (final word) | 68.035–68.297s | Followed by the file's last silence region, which runs to the literal end of the file (68.374→69.309s per `silencedetect`) — "live." is genuinely the last spoken content, nothing trails it but room tone. |

All three check out against an independent (non-forced-alignment) silence
analysis of the same file, which is the confirmation the task asked for.
