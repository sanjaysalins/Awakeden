# STORM v6 — the full-coverage device score (Fable design → Sonnet implementation)

**Date:** 2026-07-30 · **Goal:** apply EVERY user-approved device to the Storm episode
(v5 base, 63.0s, 13 spreads) → a production-ready v6. **Approved set =** the v5 paper
layer already live (blue-line, wash-creep, tide-mark, damp-cockle, raking-light,
held-breath, set-off, still-water-mirror, grain-boil) + round-3 built (margin-sentinel
already passed on these clips; scriptorium-foley) + the ROUND 6 KEEPS (ROUND6_VERDICTS.txt).
**Excluded:** everything KILLED (13 devices) and the SHELVED round-5 four (elder-leaf,
papermakers-mark, ribbon-marker, frottage) — user has not approved those for use.

**Laws in force:** LAW 1 (the Word never shakes/bleeds/starves/is-torn; it alone
arrives WHOLE) · LAW 2 (keeper text ≥54px, BOLD=1) · sacred-stillness landing ·
letterer laws (no faces — checked against the MOVING clip's filmstrip, not frame 0;
logo zone x40-240/y70-160; bottom ~18% UI band) · ≤1 overlay beat per spread ·
budget: header + 4 keeper entries max — WE ARE AT THE LIMIT, add nothing.

**Reference implementations (promote, don't rewrite; keep seeds):**
`_keeper_poc/_build_poc.py` (keeper hand: entry_events/compose_at, BOLD=1 already),
`_vault_poc/_build_vault.py` (scribed_verse_layer bold + poc_4 starve pattern),
`_bold_poc/_build_bold.py` (poc_2 torn page, poc_3 bleed),
`_vault2_poc/_build_vault2.py` (poc_candle, poc_two_hands frame loop).
Base assembler: `_s4_assemble.py` (v5). Timing authority: `_storm_alignment.json`
(bind every cue to real word times, never guess).

---

## The spread-by-spread score

| Spread | v5 keeps | v6 ADDS (device · content · timing) |
|---|---|---|
| s01 waves | blue-line cold open | **Field Header**: "Galilee. evening. crossing over." — energy 0.18, size 60, origin x≥0.26W (clear of logo zone), writes ~0.6s AFTER blue-line's ink front completes. Foley: keeper scratch (reuse nib asset, −4dB below Scribed Ink level). |
| s02 water | tide-mark etc. | nothing (governor: spread budget) |
| s03 screaming | (clip is MOVING — all entries here are Two-Hands applications) | **Entry 1 + Bleeding Word**: "~~storm~~ ~~wind~~ fear." energy 0.85, size 64, TOP cream lane (x 0.28–0.75; strikes must land on CREAM — check the filmstrip). Then ONE drop hits "fear." and it blooms + short trails (bind drop to the narration's fear-beat word in the alignment). Foley: scratch + single drop (reuse a library drip). |
| s04 asleep | damp-cockle | **Candle-Only**: as the narration says he was asleep (alignment), night closes to the drawn lamp (R→~330px over 1.2s), flicker-holds, REOPENS on the spread's final 0.5s (they go to wake him). Grade sits over the clip, under any lettering. |
| s05 hands (the 10.84–18.36 hold) | raking-light | **Entry 2 = Inkwell**: "we bailed and bailed and the" (starve last 5 glyphs) → blot → "water kept coming." darker. Write ≈11.5–13.5s, blot ≈14.2, resume ≈14.5–16.5 (re-bind to alignment). Top lane. If raking-light + entry crowd the spread by eye, DROP raking here and say so in the report. |
| s06 shaken | v5 stack | at spread END: **Torn-Out Page** s06→s07 bound to the "woke him" beat — grab/lift 0.3s, rip-away 0.35s, s07 already beneath. Neither page carries the Word ✓. Foley: rip (reuse a tear asset if the library has one; else SKIP and report — no new spend). |
| s07 eyes | v5 stack | **Margin Studies**: 2 lamp studies (contrast ≥1.9) + wobbly leader to the lamp + caption "still burning." (size 56). Lane by eye against the moving clip. FALLBACK if s07 truly has no room: studies move to s05's tail and s05's raking-light is dropped. |
| s08 verse (23.75–27.10) | verse card | **THE WORD ARRIVES WHOLE** (LAW 1 flagship): "Why are ye fearful, O ye of little faith?" is JESUS' speech — the card now appears COMPLETE between two frames at the quote's first word (alignment), REPLACING v5's letter-by-letter reveal. Precede: keeper stub "he stood up and" writing from s08's open, interrupted mid-word at the card's arrival, never finished. Foley: keeper scratch STOPS DEAD at arrival; no nib cue under the verse (near-silence + low tone per §7 stands). **FLAG in the report: this amends §5's reveal choreography for red-letter speech — pending panel.** |
| s09 rebuke | (sentinel-cleaned clip) | nothing — the spread IS the rebuke |
| s10 calm | still-water-mirror, wash-creep retreat | **Entry 3 (calm register)**: "not a breath of wind. not one." energy 0.08, size 64, upper-sky lane (POC-B proven), timed to the calm narration beat. The A/B pair with s03 inside one film. |
| s11 EXACTLY. | stamp | nothing |
| s12 knees | tide-mark full snap | nothing (narration owns the beat) |
| s13 landing | torn page, set-off, ≥3.0s hold | **NOTHING. The landing is untouchable.** |

Budget check: header (s01) + entries s03/s05/s08-stub/s10 = 4 entries + header = AT the
governor limit ✓. One bleed ✓, one transition ✓, one candle spread ✓, one study cluster ✓.

## Audio
Extend `scriptorium_foley.storm_cue_list()` with the new device windows (each composite
exports its cue: keeper_scratch, drop, rip, dry-scratch+dip for the starve). REUSE-ONLY
from sound_library; missing asset ⇒ skip + report. All cues ambience-level, sidechain-
ducked, held-breath-multiplied — the standing constants, no remix.

## Gates + deliverables (all $0)
1. Rebuild the full cut over the v5 chain (narration/score/foley mix intact + new cues).
2. `check_landing_hold.py` PASS · watermark per INV-27 (`add_watermark.py`) · byte-still
   verification on the landing hold.
3. Extract QC frames at EVERY device moment (~14 timestamps) — LOOK at them (Read), don't
   trust the pipeline; verify each lane against faces in motion.
4. Deliverables: `STORM_living_sketchbook_v6.mp4` (watermarked; keep v5 untouched, back
   up prewm) + `_STORM_V6_REVIEW.html` (device map, v5-vs-v6 at the changed moments,
   honest flags incl. anything skipped) + updated cue list + this score marked with
   as-built timestamps.

---

## AS BUILT (Sonnet implementation, 2026-07-30) -- amendments to the table above

Implemented in `_s6_assemble.py` (a new script that imports `_s4_assemble.py` as S4
rather than a `--v6` flag threaded through it -- `_s4_assemble.py` is the shipped v5
deliverable, HARD RULE says keep it intact, zero lines touched). Every timestamp below
is bound to a real word in `_storm_alignment.json` or a real SHOTS boundary; none guessed.

| Spread | AS-BUILT timing | Notes / deviations from the score |
|---|---|---|
| s01 Field Header | write 1.50-3.30s (blue-line ends 0.9 + 0.6), origin (302,86) i.e. x=0.28W | text hard-exits at 4.25 (s02's own end) so it doesn't bleed onto s03's new text. Foley keeper_scratch at -26dB (nib_scratch's -22dB base, score's own "-4dB below Scribed Ink"). |
| s03 Bleeding Word | entry write 4.35-5.00s, drop at 5.032s, bloom/trail through 6.67 | Score's alignment has no literal "fear" token in this window ("Men screaming for their lives." is what's spoken) -- drop bound to **"screaming" ending (5.032s)**, the actual fear-word; "lives." (5.375-5.739, the sentence's own climax) was the runner-up reading, not used. Lane moved from the POC's bottom-anchored y=0.878H to a **TOP cream lane (y=0.05H)** per the score's own instruction and the v6 letterer law (bottom ~18% band forbidden for text). |
| s04 Candle-Only | collapse 8.843 ("asleep." onset) -> 10.043 (1.2s, matches score exactly), flicker-hold 10.043-10.34, reopen 10.34-10.84 | Grade applied AFTER S4's full wash/tide/damp chain (simplification: candle's fixed-lamp-position vignette is computed on the already-warped frame, not before damp_cockle the way raking-light precedes it in s05 -- accepted as negligible given damp_cockle's amplitude is only ~3-6px; flagged, not hidden). |
| s05 Inkwell + Margin Studies (fallback) | write 11.628-14.146, blot 14.146-14.546, resume 14.589-16.551, margin studies 16.551-17.95 | All four score approx-numbers (11.5/13.5/14.2/14.5/16.5) re-bound to the nearest real alignment word boundary (diffs 0.05-0.19s, see file header comment for each). **Margin Studies fallback TRIGGERED**: s07's 1.6s window was genuinely too short (POC needs ~3.5s) AND its leader-line geometry only makes sense pointing at a lamp actually visible in frame (s04/s05's lamp, not s07's eyes) -- studies moved to s05's tail, s05's raking-light DROPPED, exactly as the score's own escape hatch specifies. |
| s06->s07 Torn-Out Page | grab/lift 21.30-21.60 (0.3s), rip-away 21.60-21.95 (0.35s) -- lands exactly on the s06/s07 cut | Matches score's 0.3s/0.35s split exactly. "Bound to the woke him beat" read as the s06/s07 spread cut itself (the whole s06 spread IS the waking-him beat; there is no single "woke" token in the alignment -- closest is "shake...awake" at 18.505-19.109, spoken at s06's START, not its end, so the cut-boundary reading was used instead of that literal word). |
| s08 THE WORD ARRIVES WHOLE | card complete at t=23.545 ("Why" onset) through 27.10 (unchanged exit); keeper stub 22.756 ("eyes:" ends) -> interrupted at 23.545 | LAW 1 confirmed literally satisfiable: frame quantization (30fps) puts the LAST card-less frame at t=23.5333 and the FIRST complete-card frame at t=23.5667 -- a real between-two-frames arrival, not an approximation. Stub given ~0.79s of real screen time before the cut (the score's "writes from s08's open" was ambiguous since the card also arrives at s08's open; resolved by starting the stub at s07's own last word instead, so it has room to look like a real interrupted word). §5 amendment flag carried forward as instructed -- pending panel. |
| s10 calm Entry 3 | write 31.35 ("calm." ends + a beat) -> 33.35, i.e. 2.0s | **Deviates from the score's implicit same-spread framing**: s10's own tail (31.35 to its 32.20 window end) is only 0.85s, too short for a calm-register reveal to read (POC-B used 2.4s for similar-length text at the same low energy). Entry bleeds ~1.15s into s11's own window, which is visually compatible (s11 is the companion calm/water spread) and clear of s11's own EXACTLY. stamp (35.05). Documented deviation, not a silent one. |

**Devices dropped from the original spread siting, both via the score's own escape
hatches:** s05 raking-light (Margin Studies fallback) and s07 Margin Studies' original
siting (moved to s05's tail). No device was cut outright; both are relocations the score
itself pre-authorized.

**Foley:** `panel_animator/scriptorium_foley.py`'s `storm_cue_list()` gained a
`v6_devices=True` parameter (additive, default False -- v5's own call is untouched) plus
two new DEVICE_SOUND_MAP entries (`keeper_scratch`, `ink_drop`, both reused-asset
substitutes, no new spend). The s06 rip cue reuses the EXISTING `paper_tear` mapping
(bread_tearing) rather than needing a new one -- the library already had a matching
"tear" asset, so nothing was skipped there. s07/s10 got no foley cue (score didn't call
either out explicitly; not invented beyond spec).
