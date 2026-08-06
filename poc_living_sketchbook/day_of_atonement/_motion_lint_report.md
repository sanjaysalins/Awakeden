# Motion Lint Report

Thresholds used: {"narrative": 0.15, "card": 0.1}
Segments analyzed: 76

**2 FAIL, 7 WARN**

- **[FAIL] FROZEN-SPREAD** `s50_the_shadow` -- p95=0.027 < T_frozen(narrative)=0.15, dur=5.3s
- **[FAIL] FROZEN-SPREAD** `s69_east_west_card` -- p95=0.099 < T_frozen(card)=0.1, dur=6.2s
- **[WARN] DEVICE-QUOTA** `palette_pivot` -- 8/76 = 10.5% > 10% WARN threshold
- **[WARN] DEVICE-QUOTA** `locked_plate_parallax` -- 10/76 = 13.2% > 10% WARN threshold
- **[WARN] FROZEN-SHORT** `s05_walking_to_veil` -- p95=0.018 < T_frozen(narrative)=0.15, dur=4.0s (short, WARN only)
- **[WARN] FROZEN-SHORT** `s26_through_veil_stage2` -- p95=0.036 < T_frozen(narrative)=0.15, dur=4.3s (short, WARN only)
- **[WARN] MOTION-CLIFF** `s04_donning_linen -> s05_walking_to_veil` -- outgoing p95=80.63 vs incoming p95=0.02 (T=0.15), unseen_hand transition -- consider escalating
- **[WARN] MOTION-CLIFF** `s49_veil_detail_card -> s50_the_shadow` -- outgoing p95=0.85 vs incoming p95=0.03 (T=0.15), unseen_hand transition -- consider escalating
- **[WARN] MOTION-CLIFF** `s68_east_west_horizon -> s69_east_west_card` -- outgoing p95=0.60 vs incoming p95=0.10 (T=0.1), unseen_hand transition -- consider escalating