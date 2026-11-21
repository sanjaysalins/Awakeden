SLUG: bronze-serpent
STATUS: READY
VERDICT: FIX
FILLS: poc_living_sketchbook/bronze_serpent_long/_s7_assemble.py still uses forward+REVERSE bounce. Reverse confirmed by mirror test at 4.04 s (mirror diff 1.5 vs 10.5 forward). _spread_windows.json: 40 pingpong, 5 slow_pingpong, 4 fwd_tail_bounce = 49 of 68 spreads; ~231 s of 592 s (39%) is fill. Slow_pingpong = bounce AND slow-mo. Worst:
  209.8 s s30_payoff_fever_breaks 18.5 s from a 5.0 s clip - slow_pingpong x3.66
  232.9 s s32_pole_silhouette_dusk 25.9 s from 8.0 s - slow_pingpong x3.23
  293.2 s s36_proud_man_turns_away 21.4 s from 5.0 s - slow_pingpong x4.25
  325.4 s s38_dread_image 19.4 s from 4.0 s - slow_pingpong x4.79
  364.5 s s41_moses_long_road 18.5 s from 8.0 s - slow_pingpong x2.30
  258.8 s s33_vignette_universal 13.8 s from 5.0 s - pingpong (x2.7)
  350.2 s s40_moses_resolve_returning 14.3 s from 4.0 s - pingpong (x3.5)
  272.6 s s34_moses_walking_dusk 11.6 s from 4.0 s - fwd_tail_bounce (walking figure, reverse tail = backward walking risk)
  Also 40+ pingpongs of 4-5 s clips into 8-11 s slots: 0.0 s (x1.84), 7.4 s, 42.9 s and 52.4 s (tail-bounce), 138.4 s (x2.4), 154.0 s (x2.6), 168.5 s (x2.4), 184.1 s, 314.6 s, 408.9 s (x2.7), 424.9 s, 464.8 s (x2.6), 565.0 s (x2.7)
  498.3 s s57_bridge_moses_christ once_hold 10.1 s from a 4.0 s clip (x2.5 = last-frame hold)
  585.0 s s68_landing static_still (7.4 s, a still)
  Contact sheet at 3 s steps shows many consecutive near-identical frames (s30, s32, s36, s38 = 17-26 s of almost no motion).
SLOP: Low-med. Jesus on the cross is drawn in a plain white tunic with feet on a block (not Roman-historical; consistent through the film, so style not error). Moses/serpent/pole consistent across shots; no extra people or hand errors seen at sheet scale. Nothing at PULL level.
TEXT: NONE. Burned captions are the forced-aligned voice words (alignment file) - match the voice by construction. No unspoken cards.
END: hold=5.84 silent_end=no (last word 589.12 s, film 594.96 s; music sits at -26 dB until ~3.5 s from the end then falls only ~25 dB in ~1.5 s; last 0.25 s = -50.8 dB, not near-silent; fade is shorter than the 2.5 s owner template)
FIX_IDEA: $0 first: re-run the end score fade as a slow 2.5 s fade; for the fills, adopt the Day of Atonement fwd_drift recipe is a half-fix (still zoom on last frame) - honest fix = about 25-30 new 8-10 s clips for the long spreads (paid, needs quote) or shorten/merge the 8 spreads over 10 s of fill.
