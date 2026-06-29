# RESUME — i2v stress test (Pass 2)  ·  pick up tomorrow

## Where we are
- **Stills winner (done):** `seedream_v4_5` (1cr/still). Co: `nano_banana`.
  Gallery: `file:///C:/Users/sanjay/Desktop/CHARCON_bakeoff/CHARCON.html`
- **i2v Pass 1 (done):** 17 HF models on ONE storm-ridge still, one motion prompt.
  Gallery: `file:///C:/Users/sanjay/Desktop/VIDEO_bakeoff/VIDEO.html`
  - Headline: the CHEAP models won. Top picks below.

## Pass-1 finalists → STRESS-TEST these 3 (user-chosen)
| model | cost/clip | Pass-1 note |
|---|---|---|
| **seedance1_5** | 4.8cr | cheapest; held style+shout but added slight body locomotion |
| **cinematic_studio_video_v2** | 7.5cr | best value; style+shout+markers all held, clean push-in |
| **minimax_hailuo** | 6cr | most alive cloth motion; held style+shout, zero morph (omit --resolution!) |

## TODO tomorrow — Pass 2 (spend APPROVED by user)
**Goal:** consistency across DIFFERENT images + the HARDEST motion scenarios.
~3 models × ~4 hard stills ≈ **12 clips, ~75cr** (well under the ~800 ceiling).

### Stress stills (reuse what we already have first)
Available seedream_v4_5 stills in `scratchpad/visual_poc/charcon/` (use the `R_` reference-locked ones):
- `CC__seedream_v4_5__R_crowd_market.png` — **multi-figure** (hardest: other faces morphing)
- `CC__seedream_v4_5__R_night_fire.png` — **firelight flicker** (dynamic light)
- `CC__seedream_v4_5__R_lamp_room.png` — **low-light + held clay cup** (subtle motion, object stability)
- `CC__seedream_v4_5__R_noon_close.png` — **quiet close-up** (subtle micro-motion, no big action)
- (storm_ridge already covered in Pass 1)
- **GENERATE one new "walking" still** (locomotion is the classic i2v failure — figure strides → morphs). Render via `charcon_render.py` pattern: a wide shot walking a desert road, full figure.

### Per-still motion prompt (tailor verb to the scene, keep the style-lock tail)
Reuse the Pass-1 prompt skeleton from `video_bakeoff.py` PROMPT, but swap the action:
- crowd_market → "the crowd shifts and murmurs, cloth and dust drift, slow push-in on his face"
- night_fire → "the campfire flickers and casts dancing warm light, embers rise, gentle breathing"
- lamp_room → "the oil-lamp flame flickers, faint shadows shift, he breathes slowly, the clay cup steady"
- noon_close → "subtle breathing, eyes shift, sweat glistens, heat-haze shimmer, micro push-in"
- walking → "he walks steadily forward along the road, robe swaying, dust underfoot"
Keep tail verbatim: *"Keep the exact same inked biblical graphic-novel art style, the same face... No morphing, no style change, no photoreal look, no added or removed elements, no text, steady natural light, no glitter, no sparkles."*

### Score each on (same rubric as Pass 1)
1. inked-style survival (no photoreal-softening / line-melt)
2. face + marker fidelity (scar / earring / scarf / beard) — AND in crowd, do the OTHER faces stay stable?
3. hallucination / invented elements
4. expression/beat drift (mouth-melt, head-turn, gaze drift)
5. motion quality + reverence + (for walking) does locomotion morph the body?

## How to run (mirror Pass 1)
- Render script to clone: `scratchpad/visual_poc/video_bakeoff.py`
  - Change `MODELS` to just the 3 finalists; loop over the chosen stills (param the `--image`).
  - Idempotent, sequential, rate-limit-aware. Writes `bakeoff_v2/V__<model>__<still>.mp4`.
  - **minimax_hailuo: OMIT `--resolution`** (it 400s on 768; default works).
- I CAN'T watch mp4 — extract 6-frame filmstrips with ffmpeg, then Read the PNGs:
  `ffmpeg -i clip.mp4 -vf "fps=6/dur*0.999,scale=300:-1,tile=6x1" strip.png`
  ffmpeg at `/c/Users/sanjay/AppData/Local/Microsoft/WinGet/Links/`.
- Gallery: clone `build_video_gallery.py` → `bakeoff_v2` grid (rows=models, cols=stills),
  copy to `C:\Users\sanjay\Desktop\VIDEO_bakeoff2\`, give the `file:///` link.

## Hard constraints (still in force)
- Metered Anthropic API key is DEAD → all LLM work in-chat (Agent/local CLIs). HF credits + ElevenLabs WORK.
- POC on the side — **scratchpad only**, do not touch ongoing sessions.
- Budget ceiling ~800 HF credits.
- Look at images yourself with Read; don't trust SDK audit pass/fail.
- Loved style (verbatim): *biblical epic graphic novel style, cinematic manga composition, sacred
  supernatural light, ancient desert landscape, weathered robes, dramatic ink shadows, reverent
  atmosphere, realistic proportions, mature teen-and-up tone.*

## Key paths
- POC dir: `C:\Users\sanjay\AppData\Local\Temp\claude\C--Users-sanjay-PycharmProjects-JesusInTheBible\edbf7a02-0dde-4458-a47d-2691142c9cf0\scratchpad\visual_poc\`
- HF CLI: `C:\Users\sanjay\bin\hf.exe`
- Pass-1 clips: `scratchpad/visual_poc/bakeoff_v/` · strips in `bakeoff_v/strips/`
- Desktop galleries: `C:\Users\sanjay\Desktop\VIDEO_bakeoff\` · `C:\Users\sanjay\Desktop\CHARCON_bakeoff\`
