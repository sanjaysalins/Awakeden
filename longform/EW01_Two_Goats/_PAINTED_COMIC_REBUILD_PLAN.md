# EW01 Two Goats — PAINTED-COMIC + REMOTION motion-comic REBUILD plan

**Drafted 2026-07-23. Paper only ($0). No render runs until the user OKs the spend (§6).**

This is the rebuild we owe: EW01's 9:44 body redone in the **chosen** go-forward look
(painted-comic stills) and assembled as a **Remotion motion-comic** — replacing the
**rejected** calm boomerang cut (user: "can't go back to boomerang"). It becomes the
FIRST episode in the new house style, and the template for the rest of the slate.

Two habits borrowed from ArkAIology's VOX skill are baked in — the **method**, never the
**look** (we do NOT want the Vox editorial/highlighter aesthetic):

1. **Reserved-negative-space plates** — every still is rendered with a quiet in-scene dead
   zone (deep shadow / simple sky) so the Remotion type has a clean home and never fights
   the art. (VOX §10 + painted-comic SPEC §6.)
2. **All type is a Remotion layer, never baked into the AI still** — zero AI-text
   corruption, and the type can actually *animate in*. Matches our hard rule
   [[feedback-never-animate-writing]]. Remotion IS the ffmpeg-composite method VOX proved,
   done better (React/CSS over clips).

Plus **one genuinely-new beat to POC** (this session): kinetic **ink**-lettering (a
scripture chip + a KJV phrase, in OUR ink idiom) composited over a *living* painted-comic
plate. If it lands it becomes a standard motion-comic beat; if not we've lost ~$0.80.

---

## 1. What is reused ($0) vs rebuilt

**Reused as-is (no spend):**
- **Narration** `v1/narration.spoken.txt` + `v1/visual_16x9_inked/` timeline (25 beats,
  timestamps, 584.5s) — the story spine is LOCKED, doctrine already panel-proven. We keep it.
- **Duration-locked `narration.mp3`** (~9:44, 3-voice) — reused verbatim. The Remotion
  timeline is cut TO this audio.
- **Score** (`epic_atonement_*` tracks, already in music_library) + **SFX** cues — reused.
- **Canon painted-comic refs** — `_painted_comic_test/aaron_pc_ref.png` +
  `christ_pc_ref.png` (already rendered, user-approved) chained into every shot for
  character consistency.
- **Remotion engine** (`_remotion/`, Remotion 4.0.290) — data-table→`<Sequence>` timeline,
  `spring()`+`interpolate()` kinetic type, `useFonts` loader, grain/vignette/flash overlays.
  Fonts present: `Bangers.ttf` (impact) + `PermanentMarker.ttf` (hand-inked, unused today).
- **Noir cold-open TRAILER** (`_remotion/out/EW01_TWO_GOATS_TRAILER_noir_v3.mp4`, 38s) —
  prepends the film (or ships standalone). Its B&W→colour bloom at the veil tear rhymes with
  the body's dark→bright pivot (see §3 arc).

**Rebuilt (spend):**
- **25 painted-comic stills** (nano_banana_pro via HF), reserved-space, brightness-arc'd.
- **~25 living-plate clips** (tiered Seedance/Kling) — every screen a real generative clip
  per the locked no-Ken-Burns rule [[comic-grid-cost-tiered-animation]].
- **New Remotion composition** `EW01Film` — the motion-comic body ($0 compute).

---

## 2. The 25-beat still list (backbone)

Timestamps + subjects come straight from the locked inked `scene_plan.json`. Each beat = ONE
full painted-comic scene (no model-drawn grids — SPEC §5). "2nd still?" flags beats whose
diptych/grid is better composed in Remotion from separate stills (a decision, §6-C).

| # | t (s) | title | type | light | Kling? | 2nd still? |
|---|-------|-------|------|-------|--------|-----------|
| 1 | 0–19 | Once a year, only once | single | dark | | |
| 2 | 19–39 | I laid aside gold and glory | still-life | dark | | |
| 3 | 39–58 | Plain white linen, like a servant | single | dark | | |
| 4 | 58–78 | I went in alone | single | dark | | |
| 5 | 78–99 | The cloud upon the mercy seat | ot_echo | dark | | |
| 6 | 99–121 | I buried two of my own sons | unified | dark | ✔ | ✔ (memory panels) |
| 7 | 121–144 | Two goats, and I cast lots | ot_echo | dark | | |
| 8 | 144–167 | The first goat I killed | single | dark | | |
| 9 | 167–191 | Both my hands upon the live goat | single | dark | | |
| 10 | 191–214 | I watched it go — a land not inhabited | single | dark | | |
| 11 | 214–240 | One offering — yet it took two goats | unified | dark | ✔ | ✔ (diptych) |
| 12 | 240–265 | Why two? | single | dark | | |
| 13 | 265–289 | The people went home clean | single | dark→warm | ✔ | |
| 14 | 289–314 | Every year I came back and did it again | unified | dark | ✔ | maybe (echo) |
| 15 | 314–338 | I was only ever pointing — a sign | single | dark | | |
| 16 | 338–361 | A shadow waits — the body came | jesus_link | **PIVOT** | | |
| 17 | 361–383 | By his own blood he entered in once | jesus_link | warm | | |
| 18 | 383–406 | The LORD laid on him the iniquity of us all | unified | warm | ✔ | ✔ (fulfillment canvas) |
| 19 | 406–428 | He suffered without the gate | jesus_link | warm | | |
| 20 | 428–451 | He sat down — the veil rent from the top | jesus_link | warm | ✔ | maybe (diptych) |
| 21 | 451–478 | Do not come to me, or a goat, or an altar | single | warm | ✔ | |
| 22 | 478–504 | Come to Jesus — as far as east from west | jesus_link | warm | | |
| 23 | 504–531 | The way is thrown wide open | single | bright | | |
| 24 | 531–558 | Boldness to enter into the holiest | unified | bright | ✔ | maybe (crowd) |
| 25 | 558–584 | HERO: Will you come in? — be carried clean | jesus_link | bright | | |

**Tiering** (carried from the ink migration): Kling for the 8 action/crowd/complex beats
(6,11,13,14,18,20,21,24) + a firm face-lock on every Christ beat; Seedance for the 17 calm
single-figure beats. **Hero = #25** (also the trailer/thumbnail first frame).

---

## 3. The brightness arc (the painted-comic selling point)

Painted-comic is **brightness-tunable** (proven on the test renders: dark `pc_12_aaron`
brightness 65 → bright `pc_25_christ_bright` brightness 105). We use that as the story arc:

- **Beats 1–15 = DARK chiaroscuro** — Aaron's law-era: the veil, the fear, the blood, the
  weary repetition. Deep single-key shadow.
- **Beat 16 = the PIVOT** — "a shadow waits for the body; the body came." The cross-shadow.
- **Beats 17–25 = WARM → BRIGHT** — Christ, fulfillment, the open veil, the welcome. Warm
  radiant key light; #23–25 fully bright.

This rhymes the noir trailer, which blooms B&W→colour at the veil tear. The body brightens at
the same gospel pivot. **One through-line across trailer + film.**

---

## 4. Pipeline (4 stages, each gated)

**Stage 1 — Stills** (`_paint_ew01_stills.py`, to write): loop the 25 (+grid secondaries)
beats; per beat build `<STYLE BLOCK[dark|bright]> Compose this frame: <SHOT + reserved
negative-space clause> <AVOID> <MATCH>`, chain the right canon ref (`aaron_pc_ref` on Aaron
beats, `christ_pc_ref` on Christ beats), `hf generate create nano_banana_pro --aspect_ratio
16:9 --resolution 2k --wait`. Idempotent (skip if PNG+passed sidecar). **Eyeball QC every PNG
at 1:1** (baked-fact-prone — SPEC §8) → reroll fails. → **HUMAN GATE: stills gallery.**

**Stage 2 — Animate** (`_paint_ew01_animate.py`, fork of `_animate_inked.py`): tiered
Seedance/Kling living plates, camera-only + living light, frozen faces (per-scene face-lock on
Christ). Test-gate 2 clips first, then batch. Filmstrip QC. → clips in `_remotion/public/clips/`
normalized 1920×1080 30fps.

**Stage 3 — Remotion assembly** (`_remotion/src/EW01Film.tsx` + register in `Root.tsx`):
- Data-table timeline (`[durationFrames, sceneId]`) reduced to `<Sequence>`s, cut to the real
  `narration.mp3` timestamps (§2 table). `durationInFrames` ≈ 17 535 (584.5s @ 30fps).
- `<Audio>` = narration.mp3 (later: + score + sfx premixed, or layered in Remotion).
- **Kinetic type layers** (our ink idiom, NOT Vox highlighter): a small hand-inked **scripture
  chip** on quote beats (e.g. "MATTHEW 27:51"), and the **KJV phrase** animating in on the
  reserved dead-zone — PermanentMarker/brush styling, `spring()` pop + ink-draw-on underline
  (reuse `Poc.tsx` `InkStroke`). Reverent, not the trailer's loud red slams.
- Grade arc via animated CSS `filter` (grayscale/brightness) OR the dark/bright bake is already
  in the stills (§3) — likely the latter, so Remotion just adds grain/vignette (reuse trailer
  overlays) + subtle Ken-Burns drift is unnecessary (plates already move).
- **Render:** `npm run render -- EW01Film out/EW01_TWO_GOATS_painted_v1.mp4`.

**Stage 4 — Finish:** score (reuse; `_add_score_lf.py` already inked-aware; outro 3.0s per
INV-26) → sfx (port `_sfx_two_goats.py` to the new track duration) → captions decision (§6-D)
→ `check_landing_hold.py` (INV-26) → INV-27 watermark (top-right 16:9, `add_watermark.py`) →
validator suite → publish pack (6-CLI panel) → the ONE rebuild commit.

---

## 5. New scripts / files

- `longform/EW01_Two_Goats/_paint_ew01_stills.py` — Stage 1 (fork of `_painted_comic_bright.py`)
- `longform/EW01_Two_Goats/_paint_ew01_animate.py` — Stage 2 (fork of `_animate_inked.py`)
- `_remotion/src/EW01Film.tsx` + `Root.tsx` registration — Stage 3
- Stills land in `v1/visual_16x9_painted/`; clips in `_remotion/public/clips/` (colour)
- (This session) `_poc_kinetic_type/` + `_remotion/src/PocKineticType.tsx` — the POC

---

## 6. Spend quote + open decisions

**Rates:** $0.15/credit. painted-comic still ≈ 2cr ≈ **$0.30** (HF nano_banana_pro).
Kling 7.5cr ≈ **$1.13**. Seedance 4.8cr ≈ **$0.72**. (Ledger is truth; a formal `/cost`
pre-flight runs BEFORE the batch.)

| item | count | est |
|---|---|---|
| Stills (25 + ~5 grid) + ~30% reroll ≈ 39 × $0.30 | ~39 | ~$12 |
| Clips: 8 Kling + 17 Seedance + ~20% reroll | ~30 | ~$25 |
| Remotion assembly / kinetic type / finish | — | $0 (compute) |
| Audio (narration/score/sfx reuse + port) | — | $0 |
| **TOTAL rebuild** | | **~$35–45** |
| POC (this session): 1 plate + 1 clip | | **~$0.80** |

⚠️ **This is a THIRD visual pass** (oil ~$102 archived → ink ~$35.80 → painted-comic ~$35–45).
The ink-migration ledger is already ~$35.80/$40. The painted-comic rebuild needs its **own
budget OK** — a fresh ceiling, not the ink ledger. **No batch spend until you approve.**

**Decisions for you:**
- **A — Trailer:** prepend the 38s noir trailer as the film's cold-open, or keep it standalone?
- **B — Grade:** bake the dark→bright arc into the stills (§3, my rec) vs an animated Remotion
  grayscale→colour bloom like the trailer? (Baked = richer ink; Remotion = matches trailer.)
- **C — Grids:** the ~5 "unified"/diptych beats (6,11,18,±14,±24) — single unified still each
  (fewer renders, simpler) vs split + Remotion-composed diptych (more control, ~+$1.50 each)?
- **D — Captions:** full burned captions, or lean on the kinetic-type key-phrase beats + no
  full caption track (motion-comic style)? (Long-form has usually been captioned.)

---

## 7. POC (running this session)

**Beat:** scene 20 — "He sat down; the veil rent from the top" (Matthew 27:51). A scripture
moment where kinetic type shines, with reserved dark negative space for the type.

**Steps:** (1) render one painted-comic plate with a reserved lower-left dead zone
[`_poc_veil_plate.py`, ~$0.30] → (2) animate it (Kling, frozen Christ, slow push) [~$1.13,
Kling is 7.5cr — corrected from the $0.50 guess] → (3) `PocKineticType.tsx`: composite an ink
scripture-chip + the KJV phrase animating in over the living plate → (4) `npm run render`.

**RESULT (2026-07-23): PASS.** `_remotion/out/poc_kinetic_type_v2.mp4`. All three claims proved:
reserved-space plate gave the type a clean home; kinetic ink-type (never baked) is fully legible
and reads as OUR idiom (PermanentMarker, not Vox highlighter); Christ stayed frozen across the
Kling push. One defect found + fixed: 90px overflowed the frame → **64px is the validated size**
(more reverent anyway). Validated treatment: gold PermanentMarker chip (42px) + drawn-on ink
underline; white phrase (64px, 1.5px ink stroke, shadow) revealing top→bottom to mirror the tear;
Remotion scrim on the dead zone for legibility. **Adopt as a standard beat, used SELECTIVELY on
scripture-quote beats** (not every screen) — matches [[panel-animator-intentional-use]]. POC spend
~$1.43.
