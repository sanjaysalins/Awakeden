# EW01 — The Two Goats (eyewitness short) — living-sketchbook pilot

Source: `longform/EW01_Two_Goats/v1/short/` (`.locked`, 2026-06-29). Witness:
Aaron, the first high priest of Israel. Core text: Leviticus 16. Real audio
78.1s (`narration.mp3`), real forced word alignment written to
`narration.alignment.json` (`.venv\Scripts\python.exe -c "from pipeline import
assembly_align as AA; AA.align(Path('longform/EW01_Two_Goats/v1/short'),
force=True)"`).

Never yet built in sketchbook (4 prior attempts: Baroque 208 stills,
painted-comic 8, retro-comic 25, inked 25 — see `STYLE_MIGRATION_TRACKER.html`).
This build pilots the Stationer (`MEDIUM_SELECTION.md`) on real production
work for the first time.

Cast (both REUSED, $0, no new renders):
- **Aaron / the Priest** — `poc_living_sketchbook/two_goats/cast/priest_sketch_ref.png`
  (`PRIEST.md` canon text, written for this exact Leviticus 16 role already)
- **Jesus** — `poc_castbible_look/episode_door/cast/jesus_sketch_ref.png`
  (`JESUS.md`, sketch-family anchor)

## Spread table (17 spreads, word-timed)

| # | Slug | Window | Dur | Text | Medium | Figures |
|---|---|---|---|---|---|---|
| 1 | s01_hook | 0.0-6.4 | 6.4 | "Once a year I walked behind a curtain to meet God -- and I was never sure I would walk back out." | home | Aaron |
| 2 | s02_two_goats | 6.4-10.0 | 3.6 | "The law gave me two goats for one sin." | home | Aaron |
| 3 | s03_blood_veil | 10.0-14.2 | 4.2 | "I killed the first and carried its blood inside the veil." | home | Aaron |
| 4 | s04_hands_head | 14.2-18.6 | 4.4 | "The second I did not kill -- I laid my hands on its head," | home | Aaron |
| 5 | s05_confess | 18.6-21.2 | 2.6 | "confessed every sin of the people over it," | home | Aaron (hands insert) |
| 6 | s06_scapegoat | 21.2-24.4 | 3.2 | "and sent it away into the desert to be lost." | **md_survey_plate** | none (goat only) |
| 7 | s07_one_one | 24.4-28.1 | 3.7 | "One to pay. One to carry it away." | home | Aaron |
| 8 | s08_why_two | 28.1-31.6 | 3.5 | "For years I asked why it took two." | home | Aaron |
| 9 | s09_turn | 31.6-37.6 | 6.0 | "I know now. No single creature could hold both halves." | home | Aaron |
| 10 | s10_jesus_intro | 37.6-42.8 | 5.2 | "Long after me a Man named Jesus did what my two goats only pictured --" | home | Jesus |
| 11 | s11_price_guilt | 42.8-46.6 | 3.8 | "He was the price paid, and the One the guilt was laid on:" | home | Jesus |
| 12 | s12_scripture | 46.6-51.0 | 4.4 | "and the LORD hath laid on him the iniquity of us all." (scripture voice) | home | Jesus |
| 13 | s13_sat_down | 51.0-56.2 | 5.2 | "He carried it away Himself -- once -- and sat down. Finished." | home | Jesus |
| 14 | s14_tore | 56.2-61.2 | 5.0 | "The curtain I trembled behind tore in two the hour He died." | home | none (veil event, stage 1) |
| 15 | s15_sign_substance | 61.2-64.7 | 3.5 | "I was only the sign; He is the substance." | home | Aaron |
| 16 | s16_torn_top_bottom | 64.7-71.9 | 7.2 | "The curtain I trembled behind is torn from top to bottom -- and no hand will ever sew it shut." | home | none (veil event, stage 2) |
| 17 | s17_landing | 71.9-78.1(+3.0 hold) | 9.2 | "The holiest place is open, and Jesus is already inside. Walk in." | home (LANDING LAW) | Jesus |

## Medium proposal -- REVISED (first pass was too conservative)

**First pass (rejected by the user):** only s06 got a medium; everything
else defaulted to home. User's objection, verbatim: "the idea was that you
would see this with fresh eyes... I need to understand the pipeline will be
objective and decide which style to use... keep it consistent character but
over different styles." Two real gaps in the first pass: (1) it never tested
whether a NAMED figure holds identity under a non-home medium (s06 has no
figure at all), and (2) it rejected a second genuine candidate (s12) on a
rule ("spoken quote != physical document") that doesn't survive scrutiny --
a spoken KJV quote landing on a scroll-fragment page is not decoration, it's
the most direct possible match to Scroll's own `right_tool_for`.

**Revised proposal -- 3 non-home spreads:**

- **s01_hook -> `md_night_ink`, WITH Aaron.** Re-read: "I walked behind a
  curtain to meet God -- and I was never sure I would walk back out" is not
  merely a dark room, it's a genuine THRESHOLD -- a doorway into a space
  Aaron might not return from. That is exactly Night Threshold's own
  conceit ("the door at midnight"), not "night mood on an ordinary page"
  (the disqualifying case the design doc itself names). Puts the medium at
  the HOOK -- the highest-visibility spread -- and chains AARON, a THIRD
  character never tested under this medium (the 2026-08-11 mini bake-off
  only tested Moses and Jesus).
- **s06_scapegoat -> `md_survey_plate`.** Unchanged from the first pass --
  still the strongest, most obviously-earned fit (isolation-in-vastness).
- **s12_scripture -> `md_scroll`, no figure.** Reversed from the first
  pass's rejection. "and the LORD hath laid on him the iniquity of us all"
  IS the-Word-itself, Scroll's own `right_tool_for`. Recomposed with NO
  figure (Scroll is `figure_mode: artifact_only`) -- a scroll fragment
  under a single light shaft, surface blank/abstract-marked, never legible.
  This is Scroll's FIRST real use anywhere in production (status: caution,
  never rendered before this build).

**What the real guardrail run showed (not silently bypassed):**
`pipeline/medium_variety.lint()` on this exact proposal returns 2 real
FAILs: both `md_night_ink` and `md_scroll` are `status: caution`, not
`production_approved`, so the deterministic layer correctly refuses to
auto-pass them -- exactly its job. Both are used here via an EXPLICIT human
override, not a silent LLM proposal, per the same rule `style_variety.py`
already enforces for the sibling technique-variant axis. This is the actual
proof the system is objective: it does not rubber-stamp a wider style
choice just because a human wants to see more variety -- it makes the
override visible and requires it be deliberate.

**Deliberately still NOT used here: Archive, Ledger.** Both are
`artifact_only` and their `right_tool_for` (an accession-catalogued object;
a debt/reckoning ledger line) has no honest match anywhere in this
narration -- there is no exhibit-object beat and no count/record beat in
the Two Goats text. Forcing either in would be exactly the decorative,
unearned use the mechanism exists to prevent. Their absence here is a
result, not an oversight.

Net: 3 medium-spreads (Night Threshold, Survey Plate, Scroll), 14 home.
Over Stage 2's default budget (2) for a 17-spread episode -- accepted
consciously as a deliberate pilot decision, not a silent default.
