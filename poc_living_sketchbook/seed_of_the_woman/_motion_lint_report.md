# Motion Lint Report

Thresholds used: {"narrative": 0.15, "card": 0.1}
Segments analyzed: 22

**2 FAIL, 7 WARN**

- **[FAIL] DEVICE-QUOTA** `fwd_drift` -- 8/22 = 36.4% > 15% FAIL threshold
- **[FAIL] DEVICE-QUOTA-FULLSCOPE** `dramatic_spotlight` -- 2/22 = 9.1% full-scope > 8% FAIL threshold
- **[WARN] DEVICE-QUOTA** `verse_card` -- 3/22 = 13.6% > 10% WARN threshold
- **[WARN] FROZEN-SHORT** `s05_where_art_thou` -- p95=0.000 < T_frozen(narrative)=0.15, dur=3.1s (short, WARN only)
- **[WARN] FROZEN-SHORT** `s07_beguiled_card` -- p95=0.099 < T_frozen(card)=0.1, dur=3.6s (short, WARN only)
- **[WARN] FROZEN-SHORT** `s09_unexpected_place` -- p95=0.091 < T_frozen(narrative)=0.15, dur=4.6s (short, WARN only)
- **[WARN] MOTION-CLIFF** `s04_god_walking -> s05_where_art_thou` -- outgoing p95=0.44 vs incoming p95=0.00 (T=0.15), unseen_hand transition -- consider escalating
- **[WARN] MOTION-CLIFF** `s06_blame_circle -> s07_beguiled_card` -- outgoing p95=0.40 vs incoming p95=0.10 (T=0.1), unseen_hand transition -- consider escalating
- **[WARN] MOTION-CLIFF** `s08_coming_apart -> s09_unexpected_place` -- outgoing p95=0.68 vs incoming p95=0.09 (T=0.15), unseen_hand transition -- consider escalating