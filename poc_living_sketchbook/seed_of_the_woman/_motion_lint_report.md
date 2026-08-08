# Motion Lint Report

Thresholds used: {"narrative": 0.15, "card": 0.1}
Segments analyzed: 36

**3 FAIL, 9 WARN**

- **[FAIL] DEVICE-QUOTA** `fwd_drift` -- 14/36 = 38.9% > 15% FAIL threshold
- **[FAIL] DEVICE-QUOTA** `bespoke` -- 9/36 = 25.0% > 15% FAIL threshold
- **[FAIL] FROZEN-SPREAD** `s24_before_their_sentences` -- p95=0.145 < T_frozen(narrative)=0.15, dur=6.6s
- **[WARN] FROZEN-SHORT** `s05_where_art_thou` -- p95=0.000 < T_frozen(narrative)=0.15, dur=3.1s (short, WARN only)
- **[WARN] FROZEN-SHORT** `s07_beguiled_card` -- p95=0.099 < T_frozen(card)=0.1, dur=3.6s (short, WARN only)
- **[WARN] FROZEN-SHORT** `s09_unexpected_place` -- p95=0.091 < T_frozen(narrative)=0.15, dur=4.6s (short, WARN only)
- **[WARN] FROZEN-SHORT** `s17_not_adam_not_eve` -- p95=0.107 < T_frozen(narrative)=0.15, dur=4.7s (short, WARN only)
- **[WARN] MOTION-CLIFF** `s04_god_walking -> s05_where_art_thou` -- outgoing p95=0.44 vs incoming p95=0.00 (T=0.15), unseen_hand transition -- consider escalating
- **[WARN] MOTION-CLIFF** `s06_blame_circle -> s07_beguiled_card` -- outgoing p95=0.40 vs incoming p95=0.10 (T=0.1), unseen_hand transition -- consider escalating
- **[WARN] MOTION-CLIFF** `s08_coming_apart -> s09_unexpected_place` -- outgoing p95=0.68 vs incoming p95=0.09 (T=0.15), unseen_hand transition -- consider escalating
- **[WARN] MOTION-CLIFF** `s16_watch_closely -> s17_not_adam_not_eve` -- outgoing p95=9.59 vs incoming p95=0.11 (T=0.15), unseen_hand transition -- consider escalating
- **[WARN] MOTION-CLIFF** `s23_let_that_land -> s24_before_their_sentences` -- outgoing p95=0.31 vs incoming p95=0.15 (T=0.15), unseen_hand transition -- consider escalating