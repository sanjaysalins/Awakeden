# ISAIAH 53 PAID WORKLIST (the ONLY paid steps of the inked rebuild)

Everything else is staged and $0. The spec (`v1/visual_16x9_inked/livingpage_full.spec.json`,
95 beats) already references these 15 slugs; the builder lints clean with them absent
(missing slug -> $0 dyncam fallback from the still once the still exists).

**Budget (plan quote): 12 stills x ~$0.05 x 1.3 rolls ~ $0.78 + 3 Kling hero clips x 7.5 cr
(~$0.65) ~ $1.95 = ~$2.73 total. Ceiling with re-rolls ~ $3.50. ASK THE USER before running
(memory: ask-before-spending). Log via pipeline/cost.py ledger (hf_animate logs itself).**

Pool = `longform/01_Isaiah_53_Suffering_Servant/v1/visual_16x9_inked`
Refs = `ref_library/characters`
Renderer = `batches/cluster_01_cross/father_forgive_them/byteplus_seedream.py`
(output lands in `batches/cluster_01_cross/father_forgive_them/visual/_byteplus/<name>.png`;
move each PNG into the pool). Model per plan: `seedream-4-5-251128` via env override.
All 16:9 stills at `--size 2560x1440`. The renderer appends the INKED graphic-novel STYLE
block + ONE-illustration tail automatically - prompts below are the subject block only,
positive-only (seedream has no negative channel; naming a thing to forbid it DRAWS it).

Every command below runs from the repo root with:

```
set BYTEPLUS_IMG_MODEL=seedream-4-5-251128
```

## A. The 12 stills (BytePlus seedream, ~$0.05/roll)

### A1. RE-RENDERS (same world + same ref at 16:9)

1. **isaiah_writing_lamplight** (RR, ISAIAH ref; beats 1 hero + 81 column; film-open world)

```
.venv\Scripts\python.exe batches/cluster_01_cross/father_forgive_them/byteplus_seedream.py --name isaiah_writing_lamplight --size 2560x1440 --ref ref_library/characters/ISAIAH.png --prompt "Isaiah the prophet, an old Near-Eastern man with a long grey beard and a lined weathered face, seated at a low wooden table in a small Jerusalem stone room at night, writing with a reed pen on an open blank parchment scroll, a single clay oil lamp with a warm living flame lighting his face and hands, deep warm shadows filling the room around him, the lamp flame the brightest point of the frame. Wide 16:9 tableau, the prophet and lamp whole in frame."
move batches\cluster_01_cross\father_forgive_them\visual\_byteplus\isaiah_writing_lamplight.png longform\01_Isaiah_53_Suffering_Servant\v1\visual_16x9_inked\
```

2. **nail_through_hand_16x9** (RR of the cluster-1 nail world; ref-lock on the 9:16 still.
   DYNCAM ONLY in the film - NEVER sent to Kling, blood rule; beats 25 + 92 column)

```
.venv\Scripts\python.exe batches/cluster_01_cross/father_forgive_them/byteplus_seedream.py --name nail_through_hand_16x9 --size 2560x1440 --ref longform/01_Isaiah_53_Suffering_Servant/v1/visual_16x9_inked/nail_through_hand.png --prompt "A stark close macro of the crucified Christ's open hand held flat against the dark rough wooden crossbeam, palm facing the viewer, a dark iron nail through the centre of the open palm with dark red blood running toward the wrist, a black storm sky behind the beam. Reverent, visceral 16:9 macro tableau."
move batches\cluster_01_cross\father_forgive_them\visual\_byteplus\nail_through_hand_16x9.png longform\01_Isaiah_53_Suffering_Servant\v1\visual_16x9_inked\
```

3. **us_under_cross_shadow_16x9** (RR of the cluster-1 signature wide; ref-lock on the 9:16
   still; beats 29 + 87 column)

```
.venv\Scripts\python.exe batches/cluster_01_cross/father_forgive_them/byteplus_seedream.py --name us_under_cross_shadow_16x9 --size 2560x1440 --ref longform/01_Isaiah_53_Suffering_Servant/v1/visual_16x9_inked/us_under_cross_shadow.png --prompt "Two kneeling figures in simple robes bowed in silent prayer on wide flat sand at sunset, one robed in white and one in black, kneeling on either side of a tall dark wooden cross, the long black shadow of the cross falling forward across the sand toward the viewer, a huge low golden sun behind the cross. Wide 16:9 tableau, both figures and the whole cross in frame."
move batches\cluster_01_cross\father_forgive_them\visual\_byteplus\us_under_cross_shadow_16x9.png longform\01_Isaiah_53_Suffering_Servant\v1\visual_16x9_inked\
```

4. **risen_christ_seeking_16x9** (RR of the women_first_witnesses hero world at 16:9 - Isaiah
   gets its OWN close hero, ps22's risen_hero_come is never crossed. JESUS ref via the source
   still. HEALED DRY MARKS ONLY, no crown, no fresh blood - this frame IS Kling-bound;
   beats 93 reveal + 94 hero + 95 hold)

```
.venv\Scripts\python.exe batches/cluster_01_cross/father_forgive_them/byteplus_seedream.py --name risen_christ_seeking_16x9 --size 2560x1440 --ref batches/cluster_02_resurrection/women_first_witnesses_luke245/visual/risen_christ_seeking.png --prompt "The risen Jesus of Nazareth, a bearded Near-Eastern man in his early thirties in a clean white robe, standing in a dawn garden with arms open toward the viewer, both palms forward showing a small healed dry nail mark in the centre of each palm, his face calm, warm and seeking, warm sunrise light glowing around his head and shoulders. Reverent 16:9 tableau, whole figure in frame."
move batches\cluster_01_cross\father_forgive_them\visual\_byteplus\risen_christ_seeking_16x9.png longform\01_Isaiah_53_Suffering_Servant\v1\visual_16x9_inked\
```

### A2. FRESH 16:9

5. **jerusalem_700bc_wide** (no ref - unpeopled cityscape; beat 2)

```
.venv\Scripts\python.exe batches/cluster_01_cross/father_forgive_them/byteplus_seedream.py --name jerusalem_700bc_wide --size 2560x1440 --prompt "A wide sweeping view of ancient Jerusalem seven centuries before the Romans, Iron Age stone houses with flat rooftops packed inside high city walls on a hill at golden evening light, the temple mount rising above the rooftops, distant dry Judean hills behind, tiny robed figures in the narrow streets. Epic 16:9 establishing shot."
move batches\cluster_01_cross\father_forgive_them\visual\_byteplus\jerusalem_700bc_wide.png longform\01_Isaiah_53_Suffering_Servant\v1\visual_16x9_inked\
```

6. **servant_exalted_light** (JESUS ref; DOCTRINE: the Father is NEVER depicted - light and
   sky only, the servant seen from behind; beats 11 + 43 column)

```
.venv\Scripts\python.exe batches/cluster_01_cross/father_forgive_them/byteplus_seedream.py --name servant_exalted_light --size 2560x1440 --ref ref_library/characters/JESUS.png --prompt "A lone robed servant figure seen from behind, small against a vast open sky, standing on a high rocky ridge as one great shaft of warm golden light breaks through parted clouds and falls on him from above, his head lifted into the light. Vast reverent 16:9 tableau, empty sky and light above, the figure whole in frame."
move batches\cluster_01_cross\father_forgive_them\visual\_byteplus\servant_exalted_light.png longform\01_Isaiah_53_Suffering_Servant\v1\visual_16x9_inked\
```

7. **sheep_astray_hills** (SHEEP_FLOCK ref; beat 31 column)

```
.venv\Scripts\python.exe batches/cluster_01_cross/father_forgive_them/byteplus_seedream.py --name sheep_astray_hills --size 2560x1440 --ref ref_library/characters/SHEEP_FLOCK.png --prompt "A scattered flock of sheep straying apart across wide dry Judean hills in late afternoon light, each sheep wandering alone in its own direction down separate diverging paths, the hillsides empty of any shepherd, long shadows across the slopes. Wide 16:9 tableau."
move batches\cluster_01_cross\father_forgive_them\visual\_byteplus\sheep_astray_hills.png longform\01_Isaiah_53_Suffering_Servant\v1\visual_16x9_inked\
```

8. **lamb_to_slaughter** (SHEEP_FLOCK ref for world consistency; beat 36 HERO frame -
   Kling-bound, so a CLEAN UNMARKED lamb, no wound marks anywhere)

```
.venv\Scripts\python.exe batches/cluster_01_cross/father_forgive_them/byteplus_seedream.py --name lamb_to_slaughter --size 2560x1440 --ref ref_library/characters/SHEEP_FLOCK.png --prompt "A single clean white lamb with unmarked wool standing quietly on flat stone ground before a low ancient stone altar, a loose rope lead resting on its neck, its head calm and slightly lowered, one shaft of warm side light across its wool, a dark solemn background of shadowed stone. Reverent still 16:9 tableau, the lamb whole in frame."
move batches\cluster_01_cross\father_forgive_them\visual\_byteplus\lamb_to_slaughter.png longform\01_Isaiah_53_Suffering_Servant\v1\visual_16x9_inked\
```

9. **jesus_silent_accusers** (JESUS ref; PRE-CROSS TRIAL SCENE: bound, NO crown of thorns -
   correct for the trial, note this in its fact card at /bible-check; beat 35)

```
.venv\Scripts\python.exe batches/cluster_01_cross/father_forgive_them/byteplus_seedream.py --name jesus_silent_accusers --size 2560x1440 --ref ref_library/characters/JESUS.png --prompt "Jesus of Nazareth, a bearded Near-Eastern man in his early thirties with long dark hair and a simple robe, standing calm and silent with his wrists bound with rope in front of a row of shadowed accusers in a torch-lit stone courtyard at night, his mouth closed, his eyes steady, the accusers gesturing angrily from the shadows around him, warm torchlight on his face. 16:9 tableau, Jesus whole in frame."
move batches\cluster_01_cross\father_forgive_them\visual\_byteplus\jesus_silent_accusers.png longform\01_Isaiah_53_Suffering_Servant\v1\visual_16x9_inked\
```

10. **israel_servant_nation** (ISRAEL_NATION ref; DIGNIFIED exile imagery, never caricature;
    beats 41 + 43 column)

```
.venv\Scripts\python.exe batches/cluster_01_cross/father_forgive_them/byteplus_seedream.py --name israel_servant_nation --size 2560x1440 --ref ref_library/characters/ISRAEL_NATION.png --prompt "A long line of Israelite exiles walking a dusty road away from a distant smoking city at dusk, men, women and children in simple period robes carrying bundles and leading donkeys, their heads bowed but their bearing dignified and unbroken, a heavy grey sky above the road. Respectful wide 16:9 tableau."
move batches\cluster_01_cross\father_forgive_them\visual\_byteplus\israel_servant_nation.png longform\01_Isaiah_53_Suffering_Servant\v1\visual_16x9_inked\
```

11. **chariot_desert_road_wide** (ETHIOPIAN_EUNUCH ref; beat 58)

```
.venv\Scripts\python.exe batches/cluster_01_cross/father_forgive_them/byteplus_seedream.py --name chariot_desert_road_wide --size 2560x1440 --ref ref_library/characters/ETHIOPIAN_EUNUCH.png --prompt "A dignified Ethiopian court official, a dark-skinned man in fine embroidered robes and gold neck ornament, riding in an open wooden chariot drawn by two horses along a straight desert road from Jerusalem toward Gaza in bright daylight, holding an open parchment scroll in his hands, a driver at the reins in front of him, wide empty desert and a pale hot sky around the road. Wide 16:9 tableau."
move batches\cluster_01_cross\father_forgive_them\visual\_byteplus\chariot_desert_road_wide.png longform\01_Isaiah_53_Suffering_Servant\v1\visual_16x9_inked\
```

12. **philip_eunuch_scroll** (PHILIP the evangelist + ETHIOPIAN_EUNUCH; the seedream CLI takes
    ONE `--ref` - use ETHIOPIAN_EUNUCH.png (his face carries the sacred close-up in beat 61)
    and describe Philip; if Philip drifts across rolls, re-roll with
    `--ref ref_library/characters/PHILIP.png` and pick the better pairing. Beats 60 + 61 fracture)

```
.venv\Scripts\python.exe batches/cluster_01_cross/father_forgive_them/byteplus_seedream.py --name philip_eunuch_scroll --size 2560x1440 --ref ref_library/characters/ETHIOPIAN_EUNUCH.png --prompt "Two men leaning over one open parchment scroll in an open wooden chariot halted on a desert road in bright daylight: an Ethiopian court official in fine embroidered robes holding the scroll open on his lap, and Philip the evangelist, a plain-robed Jewish man with a short dark beard, seated beside him pointing at the open scroll, both faces clear and engaged, the desert road stretching behind them. 16:9 two-shot tableau."
move batches\cluster_01_cross\father_forgive_them\visual\_byteplus\philip_eunuch_scroll.png longform\01_Isaiah_53_Suffering_Servant\v1\visual_16x9_inked\
```

### A3. After the 12 stills land

1. `/bible-check` fact cards for the peopled frames (note: jesus_silent_accusers = pre-cross,
   no crown BY DESIGN; risen_christ_seeking_16x9 = healed dry marks, no crown).
2. Fail-closed Vision audit + record PASS sidecars
   (`render_lint verify --record` flow) - `hf_animate` REFUSES un-PASSed stills.
3. Stills human gate (`stills_gate.py`) over the pool before any build
   (the builder is fail-closed on it without `--skip-stills-gate`).
4. Eyeball each still full-res; re-roll the weak ones (budget headroom ~2 extra rolls).

## B. The 3 paid Kling hero clips (HF Kling 3.0 pro, 16:9, 5s, ~7.5 cr each)

LIVING-LIGHT prompts (run_piece.py `LIVING_LIGHT_BASE` contract: figures frozen, ONLY light
and air move; no glitter words - beams/glow/haze/mist only). Wound-free stills only
(lamb + risen hero comply; the Isaiah frame has no wounds). Run AFTER the stills pass the
gate. Each command below is the standing chokepoint (`_hf_animate_short.hf_animate`) which
enforces the PASS-sidecar gate + budget ceiling + ledger row.

1. **isaiah_writing_lamplight** (beat 1, film open - lamp flame breathing)

```
.venv\Scripts\python.exe -c "import sys; sys.path.insert(0,'.'); from pathlib import Path; from _hf_animate_short import hf_animate; hf_animate(Path('longform/01_Isaiah_53_Suffering_Servant/v1/visual_16x9_inked/isaiah_writing_lamplight.png'), Path('longform/01_Isaiah_53_Suffering_Servant/v1/visual_16x9_inked/clips/isaiah_writing_lamplight.mp4'), 'A finished inked graphic-novel comic panel - flat printed art with bold black ink outlines, cel-flat color and cross-hatching, filmed as ONE very slow, gentle push-in toward the old prophet writing at his lamplit table, keeping the subject whole in frame. Every figure stays perfectly frozen - no limbs move, no heads turn; every painted face keeps its exact same expression from first frame to last, the eyes, brows and mouths NEVER shift, harden, frown or blink. Any wound marks stay exactly as painted, dry and still - no blood flows, drips, spreads or grows. INVENT NOTHING: no new figures, hands, wings, objects or lines appear; show ONLY what is already inked in this exact panel. ONLY the light and the air are alive: the single lamp flame sways and breathes, its warm glow swelling and settling gently across his face and the open scroll, a soft warm haze drifting in the dark room.', 5, aspect_ratio='16:9')"
```

2. **lamb_to_slaughter** (beat 36 - dawn light breathing over the lamb; target/light per spec)

```
.venv\Scripts\python.exe -c "import sys; sys.path.insert(0,'.'); from pathlib import Path; from _hf_animate_short import hf_animate; hf_animate(Path('longform/01_Isaiah_53_Suffering_Servant/v1/visual_16x9_inked/lamb_to_slaughter.png'), Path('longform/01_Isaiah_53_Suffering_Servant/v1/visual_16x9_inked/clips/lamb_to_slaughter.mp4'), 'A finished inked graphic-novel comic panel - flat printed art with bold black ink outlines, cel-flat color and cross-hatching, filmed as ONE very slow, gentle push-in toward the quiet lamb standing before the stone altar, keeping the subject whole in frame. Every figure stays perfectly frozen - no limbs move, no heads turn; every painted face keeps its exact same expression from first frame to last, the eyes, brows and mouths NEVER shift, harden, frown or blink. Any wound marks stay exactly as painted, dry and still - no blood flows, drips, spreads or grows. INVENT NOTHING: no new figures, hands, wings, objects or lines appear; show ONLY what is already inked in this exact panel. ONLY the light and the air are alive: the warm shaft of side light slowly strengthens and softens across the wool, a gentle haze of dawn light breathing over the stone.', 5, aspect_ratio='16:9')"
```

3. **risen_christ_seeking_16x9** (beats 94-95, "His name is Jesus" close - sunrise glow breathing)

```
.venv\Scripts\python.exe -c "import sys; sys.path.insert(0,'.'); from pathlib import Path; from _hf_animate_short import hf_animate; hf_animate(Path('longform/01_Isaiah_53_Suffering_Servant/v1/visual_16x9_inked/risen_christ_seeking_16x9.png'), Path('longform/01_Isaiah_53_Suffering_Servant/v1/visual_16x9_inked/clips/risen_christ_seeking_16x9.mp4'), 'A finished inked graphic-novel comic panel - flat printed art with bold black ink outlines, cel-flat color and cross-hatching, filmed as ONE very slow, gentle push-in toward the risen Christ with open hands in the dawn garden, keeping the subject whole in frame. Every figure stays perfectly frozen - no limbs move, no heads turn; every painted face keeps its exact same expression from first frame to last, the eyes, brows and mouths NEVER shift, harden, frown or blink. Any wound marks stay exactly as painted, dry and still - no blood flows, drips, spreads or grows. INVENT NOTHING: no new figures, hands, wings, objects or lines appear; show ONLY what is already inked in this exact panel. ONLY the light and the air are alive: the sunrise glow behind him slowly swells and breathes, warm beams strengthening softly through the garden haze.', 5, aspect_ratio='16:9')"
```

NEVER animate: nail_through_hand_16x9 (fresh blood - dyncam only), any scroll/writing still
(hebrew_scroll_edge_light, greek_ot_scroll, two_scrolls_compared, quill_ink_drop,
prophet_scroll, scholar_hand_on_text, scribe_over_manuscripts - letters garble; all are
static/gentle-dyncam in the spec, none flagged for Kling).

## C. Build (after A + B, all $0)

```
.venv\Scripts\python.exe longform/02_Psalm_22_Song_From_The_Cross/build_livingpage_16x9.py --spec livingpage_full.spec.json --pool "longform/01_Isaiah_53_Suffering_Servant/v1/visual_16x9_inked" --clips
```

(then the standing $0 finishing stages: /sfx bed + serif captions if wanted - audio is LOCKED,
`../narration.mp3`, total 405.26s.)

## D. Accepted lint findings (documented, plan-mandated)

- `israel_servant_nation` beats 41->43 (gap 2): sacred KJV reprise - the film's only
  Israel-nation image; full-bleed then column crop.
- `philip_eunuch_scroll` beats 60->61 (gap 1): designed hold from the two-shot into the
  eunuch's spoken question (full -> fracture, sacred, no slams).
- `risen_christ_seeking_16x9` beats 93/94/95 (3 uses, full-bleed x3, gap-1 x2): the designed
  film close - partial-reveal still -> "His name is Jesus" hero clip -> silent hold.
- fit-gate rows (74): the solver measures every source as 16:9 (it passes the page size as
  the still size). All 9:16 columns are actually ~15%-height centre crops of portrait Kling
  clips (safe - eyeballed risen_mercy_hand / look_up_faces / prophet_scroll /
  risen_christ_wounds / face_on_cross / us_under_cross_shadow full-res); 16:9-in-column rows
  are the standard ps22 column-crop look with measured anchors protecting the focus.
- `held_gt6s` (16 beats over 6s): quote-dense chapter - the long holds are the 25 sacred
  red-letter beats and punched/slammed beats; median 4.0s matches the ps22 gold master.
