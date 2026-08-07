# Motion Lint Report

Thresholds used: {"narrative": 0.15, "card": 0.1}
Segments analyzed: 5

**6 FAIL, 2 WARN**

- **[FAIL] DEVICE-QUOTA** `dramatic_spotlight` -- 1/5 = 20.0% > 15% FAIL threshold
- **[FAIL] DEVICE-QUOTA** `device` -- 2/5 = 40.0% > 15% FAIL threshold
- **[FAIL] DEVICE-QUOTA** `verse_card` -- 1/5 = 20.0% > 15% FAIL threshold
- **[FAIL] DEVICE-QUOTA** `breath_synced_halo` -- 1/5 = 20.0% > 15% FAIL threshold
- **[FAIL] DEVICE-QUOTA-FULLSCOPE** `dramatic_spotlight` -- 1/5 = 20.0% full-scope > 8% FAIL threshold
- **[FAIL] DEVICE-QUOTA-FULLSCOPE** `breath_synced_halo` -- 1/5 = 20.0% full-scope > 8% FAIL threshold
- **[WARN] FROZEN-SHORT** `s05_where_art_thou` -- p95=0.000 < T_frozen(narrative)=0.15, dur=2.3s (short, WARN only)
- **[WARN] MOTION-CLIFF** `s04_god_walking -> s05_where_art_thou` -- outgoing p95=0.44 vs incoming p95=0.00 (T=0.15), unseen_hand transition -- consider escalating