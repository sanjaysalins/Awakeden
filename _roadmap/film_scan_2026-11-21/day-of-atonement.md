SLUG: day-of-atonement
STATUS: READY
VERDICT: FIX
FILLS: day_of_atonement/_s6_assemble.py removed pingpong (2026-08-05, after owner "backwards walking"), now fwd_drift: clip plays once forward then a $0 camera push/arc over its LAST FRAME for the rest of the slot. No reverse. But 53 of 76 spreads, ~207 s of 591 s (35%) is push-on-a-still. That breaks the later owner rule (no freeze/zoom fill, each clip >= its slot). Longest:
  194.0 s s31_confession_card 21.5 s from 8.0 s clip - 13.5 s on last frame
  88.0 s s16_lords_charge_card 18.3 s from 8.0 s - 10.3 s
  558.3 s s74_every_year_gone 13.1 s from 8.0 s - 5.0 s
  489.5 s s65_ritual_uninks 11.6 s from 4.0 s - 7.6 s
  571.4 s s75_the_reach 11.7 s from 5.0 s - 6.7 s
  353 s s49_veil_detail_card 10.7 s from 4.0 s - 6.7 s; 343 s s48 10.1 s from 4.0 s - 6.1 s
  297 s s42 10.0/4.0; 277 s s40 11.0/5.0; 123 s s19 10.4/4.0; 113 s s18 10.3/4.0; 444.5 s s59_no_chair 9.6/4.0; 516.8 s s68 9.4/4.0
  17 spreads have 5-13 s of fill.
  Contact sheet shows the same image for 12-18 s at several points (e.g. goat/hand-laying scene 182-215 s; final seated-Jesus image 9.6 s).
  _motion_lint_report.md: 0 FAIL, 5 WARN (s05 and s26 near-frozen, device quota, one motion cliff).
SLOP: Low-med. 255 s: bronze altar drawn with a sea/ocean horizon (wilderness tabernacle) - setting error. 393 s: crucified Jesus in a tunic, arms laid over the beam, face in shadow - weak pose (low). ~63 s: bodies of Nadab/Abihu carried out wrapped like mummies (Egyptian look, low). Aaron narrates and quotes Hebrews/Isaiah (voice device, not slop).
TEXT: NONE spoken-mismatch. Burned captions = forced-aligned voice (alignment file); verse cards (Lev 16 lots, confession, "BLOOD", "BOLDNESS", Heb 10:19) echo spoken lines.
END: hold=5.54 silent_end=no (last word 588.01 s, film 593.55 s; music ~-25 dB until ~3.5 s from the end, drops to -47.5 dB in the last 0.25 s; fade ~1.5 s, not the 2.5 s owner template)
FIX_IDEA: $0: re-do the end fade as a slow 2.5 s fade and paint-out/replace the sea backdrop on s37_split_two_things (one still); for the fills, paid: about 17 new longer clips for the spreads with 5+ s of last-frame push, or shorten/merge those spreads to their clip length.
