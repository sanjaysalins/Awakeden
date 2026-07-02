# BATCH_PLAN.md — group longs + shorts by shared visual world (v1)

**Date:** 2026-06-30 · companion to the **base-elements library** directive (RESUME.md top).
**Supersedes v0** (2026-06-06, passion-only 5+5 slate) — its locked philosophy is carried below.

## The idea (one line)
Don't build pieces one-at-a-time. Group every long AND short that lives in the **same
visual world** (same characters · locations · objects · period), build that world's
**stills + animated clips ONCE**, then assemble every piece in the group off the shared set.

## Philosophy carried from v0 (still locked)
- **Shorts = the snack/hook** (60s, viral, one sharp truth → discovery). **Longs = meat & potatoes**
  (16:9, deep, KJV-grounded). The short is the trailer; the long is the film. **Write the long FIRST.**
- **Reuse is bounded to same-format, thread-NEUTRAL plates:** long↔long (16:9) and short↔short (9:16),
  NOT long↔short (different crop). Story-specific stills stay with their episode (topical-fit gate).
  **Jesus/THE_LORD refs cross everything** for consistency. Don't over-reuse → sameness.

## Why batch now / what already exists
- **Refs are DONE.** `ref_library/` already holds **245 locked inked anchors** — every EW
  witness (Aaron, Abraham, Joseph, Moses, Jonah, Noah, Isaiah, Passover-father, Boaz) + cast
  + 74 objects + 41 places + 54 motifs. We are NOT blocked on identity locks.
- **The cost is FINAL stills + ANIMATED clips.** `clip_library/` = 284 reuse clips (159 × 9:16,
  125 × 16:9) but **none from EW0X yet**; `image_library/` = 46 oil stills, almost all
  crucifixion/Servant. So the spend is per-world final art — exactly what batching amortizes.
- Batch unit = **visual world**, NOT series. One series (e.g. *Jesus in the OT*) scatters across
  4 worlds; one world (the Cross) pulls pieces from 5 different series + the Psalm-22 shorts.

---

## The 7 visual-world clusters

| # | World | Pieces (≈) | Long-form | Shared base set to build ONCE | Asset status |
|---|-------|-----------|-----------|-------------------------------|--------------|
| **1** | **The Cross / Golgotha** | ~14 shorts | EW07 Isaiah · (legacy 01_Isaiah53, 02_Psalm22) | Christ-on-cross, Golgotha hill, crown of thorns, titulus, Roman soldiers, nail/spear, garments+lots, temple veil→rent, Pilate, mocking crowd | **BEST** — image_library + ref CROSS/GOLGOTHA/ROMAN_* + Psalm22/Isaiah53 clips |
| **2** | **Resurrection / Empty Tomb** | ~13 shorts | EW05 Jonah | empty-tomb interior + rolling stone, risen Christ w/ wounds, upper room, Galilee beach + charcoal fire, the great fish | GOOD — EMPTY_TOMB/dawn-tomb/risen-glory exist |
| **3** | **Wilderness / Exodus / Moses** | ~8 shorts | EW01 Two Goats · EW04 Bronze Serpent · EW08 Passover | desert camp + multitude, Moses, Aaron (white linen), tabernacle/Holy-of-Holies, bronze serpent on pole, Passover lamb + blood doorposts, manna, the rock, burning bush | GOOD — EW01+EW04 already BUILT; harvest their clips |
| **4** | **Genesis / Patriarchs** | ~3 shorts | EW02 Abraham · EW03 Joseph · EW06 Noah | Moriah+altar+ram, Joseph's coat/pit/Egypt throne, the ark+one-door+flood+rainbow, Eden+serpent+Adam/Eve | GOOD — all anchors exist; longs drive it |
| **5** | **Galilean Ministry** (I AM · miracles · encounters · parables · questions) | **~24 shorts** | — | **living/ministry Christ face** (the unlock), Galilee shore + boat, crowds, synagogue, well, sheep+shepherd, pool of Bethesda | **BLOCKED** — catalogue has only crucified Christ ([[library-lacks-living-christ]]); build living-Christ first |
| **6** | **Nativity / Bethlehem** | ~4 shorts | EW09 Boaz (shares Bethlehem) | Bethlehem town, manger, star, Mary, shepherds, barley field + city gate (Boaz) | PARTIAL — BETHLEHEM/MARY exist; manger/star fresh |
| **7** | **Throne / Titles** (Revelation · Daniel) | ~5 shorts | — | heavenly throne + glory, Lion/Lamb, Son-of-man on clouds, glorified Christ (NOT the Father) | THIN — mostly fresh |

*Pieces that touch two worlds get ONE primary build-cluster + reuse the other (e.g. "Bread of
Life" builds in #3 manna, reuses #5 ministry-Christ; "Sign of Jonah" builds in #2, reuses #4 fish).*

---

## Recommended batch order (and why)

1. **Cluster 1 — The Cross.** Best-resourced + highest leverage. Every piece in the whole engine
   *lands on Christ*, so the cross/risen frames are reused EVERYWHERE. Build the definitive
   Golgotha set once → it pays into all 7 clusters' endings.
2. **Cluster 2 — Resurrection.** Immediate sibling (Golgotha → tomb). Unlocks the entire
   *Resurrection on Trial* series + the risen-Christ close every other piece needs.
3. **Cluster 3 — Wilderness/Exodus.** EW01 + EW04 are already built — first move is to **harvest
   their clips into `clip_library`**, then extend. Covers Types-&-Shadows + several Jesus-in-OT.
4. **Cluster 4 — Genesis/Patriarchs.** EW02/03/06 longs drive it; anchors all exist.
5. **Cluster 5 — Ministry.** PRECURSOR TASK FIRST: build the **living-ministry Christ reference**
   + a few neutral ministry plates (Galilee shore, synagogue, crowd). That single missing base
   element is what blocks the BIGGEST harvest (~24 shorts). Build it, then mass-produce.
6. **Clusters 6 + 7 — Nativity & Throne.** Smallest / most singular worlds; do together as a
   final build-out batch.

## The one real blocker
**Cluster 5 needs a living/ministry Christ** built before it can batch — the library only has
crucified/passion Christ. Build that ref + plates as a tiny standalone task **before** reaching #5
(it can even be done early, in parallel, since it's independent of #1–#4).

## Per-cluster workflow (same every time)
1. Pull the cluster's pieces + confirm each one's shared elements against `ref_library`.
2. **Write/lock the long(s) first** (research foundation); distill the shorts from them.
3. Render the cluster's **shared final stills** once (HF seedream, ref-locked to the anchors).
4. Animate the shared clips once (shorts → HF Kling pro 9:16 · longs → veo3_1_lite 16:9),
   **aspect-matched** — ingest into `clip_library` so the NEXT cluster reuses them.
5. Assemble each piece by referencing the shared set; only its *unique* beats need new art.
6. Run the gates: shorts engine + `landscape_validate.py` (longs) + physics + the 5-CLI doctrine panel.

---

## Next step
Say the word and I'll turn this into a machine-readable **`batches/batch_manifest.json`**
(cluster → piece list → shared-element list → asset-status from `ref_library`/`clip_library`),
so the render drivers can walk a cluster and skip anything already in the libraries.
Then we start **Cluster 1 (The Cross)**.
