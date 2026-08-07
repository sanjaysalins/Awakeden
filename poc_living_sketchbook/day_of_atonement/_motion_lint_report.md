# Motion Lint Report

Thresholds used: {"narrative": 0.15, "card": 0.1}
Segments analyzed: 76

**0 FAIL, 5 WARN**

- **[WARN] DEVICE-QUOTA** `palette_pivot` -- 8/76 = 10.5% > 10% WARN threshold
- **[WARN] DEVICE-QUOTA** `locked_plate_parallax` -- 10/76 = 13.2% > 10% WARN threshold
- **[WARN] FROZEN-SHORT** `s05_walking_to_veil` -- p95=0.083 < T_frozen(narrative)=0.15, dur=4.0s (short, WARN only)
- **[WARN] FROZEN-SHORT** `s26_through_veil_stage2` -- p95=0.069 < T_frozen(narrative)=0.15, dur=4.3s (short, WARN only)
- **[WARN] MOTION-CLIFF** `s68_east_west_horizon -> s69_east_west_card` -- outgoing p95=0.60 vs incoming p95=0.10 (T=0.1), unseen_hand transition -- consider escalating