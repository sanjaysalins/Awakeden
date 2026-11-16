# Pinned templates (design v3.2, step 1 / 8 / 9)

Copied 2026-11-15 from the shipped episodes, then PARAMETERISED so a new episode reads its inputs from its
own receipts (not from another episode's files).

| Template | Source (path, sha256 of the source at copy time) | What changed |
|---|---|---|
| generate_score_piano.py | poc_living_water_ink_style_test/swirls_episode_16_let_the_little_children/generate_score_piano.py  sha256 4cda26ee93add11802b1cf1429d2fec5fb20c29fcaa9605fe5fe115b99d4eb32 | cut path + length from assembly_receipt.json; turning points from unit_timing.json; split at the north-star page; refuses unless run by the guarded score command; --dry-run; ep16 wording replaced by generic felt-piano wording (identity kept) |
| build_sfx.py | poc_living_water_ink_style_test/swirls_episode_13_the_cross_that_wasnt_his/build_sfx.py  sha256 52b6f76404b493a5a4a5386ec2949079cef40c58b5a0f73411e880435eb0bfcf | cut read from assembly_receipt_scored.json; cues placed by unit tag from unit_timing.json; --dry-run |

Copy a template into the episode folder; the episode copy is the one that runs.
