# Psalm 22 Shorts — Budget & Provider Split (LOCKED 2026-06-08)

Shorts are first-class (must be perfect). This is the planning projection; **actuals are tracked
automatically** in `data/spend_ledger.jsonl` via `pipeline/cost.py` as each asset renders.

## LOCKED provider split
| Stage | Provider | Why | Unit cost | Billed as |
|---|---|---|---|---|
| Stills — **Jesus / face scenes** | **NBP / Gemini "Nano Banana Pro"** | attaches the Christ ref face → consistent Jesus every scene (the "perfect" lever) | **$0.50 / still** | Google (est) |
| Stills — **thread-neutral plates** | **HF `nano_banana_2`** | Baroque-oil look winner, cheaper | **$0.30 / still** (2 HF credits) | HF credits |
| Animation (still → clip) | **direct-Kling** (`image_to_kling.py`) | the 8-beat viral cut-plan; HF Kling NSFW-blocks the cross | **$0.65 / clip** | Kling credits |
| Scene plan + reviews | Opus **agent-mode** | in-chat bridge | **$0** | — |
| Audio + SFX soundstage | already done | — | **$0** | — |

> Note: Psalm 22 is crucifixion-heavy → most scenes have Christ, so the split lands **NBP-heavy**.
> Because of that, **all-NBP costs almost the same as hybrid here** (~$0.50 vs a $0.30/$0.50 blend) and
> maximizes face consistency — a real option for these specific shorts.

## Per-short estimate (assumes ~16 stills: ~10 Christ + ~6 plates; ~14 animated clips; +20% QC re-render buffer)
| Line | Qty | Rate | Cost |
|---|---|---|---|
| NBP Christ stills | 10 | $0.50 | $5.00 |
| HF plate stills | 6 | $0.30 | $1.80 |
| QC re-renders (perfect bar) | +20% stills | — | ~$1.36 |
| Kling clips | 14 | $0.65 | $9.10 |
| **Per short** | | | **~$17–18** |

Comfortably under the **$25/short ceiling** enforced by the ledger.

## The 8-short cluster
| | Stills (NBP) | Stills (HF) | QC | Kling | **Total** |
|---|---|---|---|---|---|
| 8 × Psalm 22 short | 80 × $0.50 = $40 | 48 × $0.30 = $14 | ~$11 | 112 × $0.65 = $73 | **~$138–146** |

HF portion ≈ **96 credits** of your 3,296 (plenty). NBP+Kling ≈ **$113** (Google + Kling billing).

## Full remaining backlog (for budgeting)
| Work | Est |
|---|---|
| **Psalm 22 — 8 shorts** | ~$140 |
| Psalm 22 — long film (16:9) | ~$25–30 |
| 5 distinct shorts (John 8 · 1 Peter · Acts 8 · Isaiah 53 short · Matt 16) | ~$90 |
| **Grand total to finish everything** | **~$255–260** |

## How tracking works (so you can budget live)
- Every render logs a row to `data/spend_ledger.jsonl` (`record_hf` / `record_nbp` / `record_kling`).
- `python -m pipeline.cost summary` → per-episode credits + USD.
- `python -m pipeline.cost balance` → live HF credits remaining.
- `python -m pipeline.cost reconcile --episode <id> --since <ISO>` → swap estimates for HF actuals after a batch.
- Per-episode ceilings block overspend ($25 short / $40 long) unless overridden.

**These are ESTIMATES until the scene plans exist** — the per-short reuse audit (Phase 0, free) will
firm up the exact NBP/HF scene split and subtract any reusable neutral plates.
