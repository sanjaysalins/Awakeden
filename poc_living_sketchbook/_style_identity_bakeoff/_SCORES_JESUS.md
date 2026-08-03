# Jesus bake-off scores — raw agent review, 2026-08-01

Same method as `_SCORES_MOSES.md`: a vision agent opened every one of the
36 PNGs in `stills_jesus/` and scored each against `baseline.png`.

| slug | handmade_alive | identity_lock | note |
|---|---|---|---|
| sl01_baseline_reference_plate | 3 | 5 | Near-duplicate of baseline.png, not a distinct style |
| sl02_continuous_contour_line | 5 | 3 | Line-only render reads hair much lighter/blonder than baseline |
| sl03_notan_pure_silhouette | 5 | 3 | Bold B&W silhouette; composition turned 3/4, off-center |
| sl04_visible_underdrawing | 4 | 4 | Construction grid lines visible; slight smile, arms crossed |
| sl05_selective_resolution | 5 | 5 | Loose pencil body, sharp hands; added staff prop |
| sl06_wet_in_wet_bleed | 5 | 5 | Lovely color-bleed edges, tighter crop, strong likeness |
| sl07_misregistered_print | 3 | 5 | Odd dark diagonal smudge top-right looks like a glitch |
| sl08_multiple_exposure_motion_ghosting | 5 | 4 | Full pose change: riding donkey with ghost-trail figures |
| sl09_extreme_low_angle | 4 | 3 | Full-body vs sky; face small/distant, harder to verify |
| sl10_overhead_plan | 5 | 4 | **HARD-RULE VIOLATION: visible text/labels ("DOC.02: SURVEY", grid refs, signature)** |
| sl11_shadow_as_subject | 5 | 2 | Tiny distant figure; bright sun disc sits behind head like a halo |
| sl12_scratchboard_inversion | 5 | 4 | Striking white-on-black scratchboard, strong likeness |
| sl13_charcoal_and_eraser | 5 | 5 | Great smudged charcoal; soft erased vignette behind head, borderline halo-ish |
| sl14_torn_paper_depth_planes | 5 | 4 | Layered torn-paper depth collage, seated with a goat |
| sl15_frame_break | 5 | 5 | Donkey/hand break the frame border; strong, alive |
| sl16_foreground_occlusion | 5 | 2 | Wide landscape, figure tiny/distant, can't confirm identity closely |
| sl17_gold_leaf_as_structure | 4 | 4 | Whole background is cracked gold leaf — reads iconographic/glory-adjacent |
| sl18_macro_crop | 5 | 3 | Extreme hand/rope macro; only nose+beard of face visible |
| sl19_insect_scale | 4 | 4 | Doesn't read as insect-scale; just a sepia group close-up |
| sl20_sketchbook_spread | 4 | 4 | **HARD-RULE VIOLATION: garbled illegible captions ("doumanting plesres" etc)** |
| sv01_kinetic_storm_focus | 3 | 5 | Almost identical to baseline; no storm energy evident |
| sv02_chiaroscuro_pocket_wash | 3 | 5 | Barely differentiated from baseline; minimal chiaroscuro |
| sv03_layered_collage_construction | 3 | 5 | Close to baseline; collage construction not clearly visible |
| sv04_vertical_pillar_gold_thread | 3 | 5 | Near-baseline; thin gold edge strip, no pillar motif |
| sv05_cyanotype_blue_focus | 4 | 4 | Strong monochrome cyanotype blue wash, effective and alive |
| sv06_sgraffito_surface_scratch_technique | 4 | 4 | Visible scratch/hatch texture on garment; cropped, no hands/rope |
| sv07_deconstructed_lithograph_with_noise | 3 | 5 | Subtle halftone dot noise on shoulder only |
| sv08_expressive_gestural_graphite_and_ink | 3 | 5 | Close to baseline; expressive line only mildly stronger |
| sv09_hand_pulled_monotype_and_smudged_transfer | 4 | 4 | Nice ink smudges on cheek/chest; smudge slightly obscures face |
| sv10_offset_screenprint_with_misregistered_ink_plates | 3 | 5 | Subtle red misregistration line on shoulder edge only |
| sv11_ink_wash_chiaroscuro_and_scratched_light | 5 | 4 | Dramatic dark ink wash; hair/beard read notably darker |
| sv12_ground_level_cinematic_extreme_crop | 5 | 4 | Pose changed to kneeling on ground with pebbles |
| sv13_torn_paper_relief_collage_with_translucent_layers | 4 | 4 | Torn-paper layers at edges, gaze turned slightly off-center |
| sv14_drypoint_etching_cross_hatching_and_plate_wear | 5 | 4 | Great plate-wear border and cross-hatching; gaze off-center |
| sv15_controlled_abstraction_with_one_precise_focal_point | 5 | 4 | Color-splash background, desaturated hair; striking focal contrast |

## Reading this (before it becomes the manifest)

**Two real hard-rule violations, both fatal regardless of their other
scores:** `sl10_overhead_plan` baked in visible survey-document text/labels
and a signature; `sl20_sketchbook_spread` baked in garbled illegible
captions. This project's rule is absolute — NO lettering/numerals/text
anywhere, ever (SKILL.md sec.1). Both get force-rejected in the manifest
regardless of their handmade/identity numbers.

**Two real identity-lock failures:** `sl11_shadow_as_subject` (2/5 — figure
too small/distant to verify, plus an unintended halo-like light disc behind
the head) and `sl16_foreground_occlusion` (2/5 — same distance problem).
Both force-rejected.

**A methodological caveat, not a defect in Jesus specifically:** several
STYLE_LAB technique descriptions narrate action ON "the walking figure and
pack animal" AS PART OF describing the technique itself (not just in the
later SUBJECT/SCENE block) — e.g. sl08's motion-ghosting technique text
literally says "the walking figure and pack animal drawn three times."
When this bake-off's own Moses/Jesus scene got appended after stripping
only the SUBJECT/SCENE marker, that leftover language sometimes pulled in
invented props/poses (a donkey in sl08, kneeling-with-pebbles in sv12, a
goat in sl14, an added staff in sl05) that were never in the actual control
scene. Identity mostly held anyway, but this means STYLE_LAB's
handmade/alive scores are somewhat confounded for those entries — a
cleaner re-test would need the technique prefix re-authored to remove
embedded subject language, not just split on a marker.

**Same cross-character pattern as Moses confirmed:** sv01/02/03/04/07/08/10
(the STYLE_VARIANTS.md entries whose named technique needs a busy/crowd
scene to read) scored low handmade_alive (3) on BOTH Moses and Jesus now —
strengthens that finding from a single data point to a reproducible one.

**Gold-leaf flag confirmed again:** `sl17_gold_leaf_as_structure` reads
"iconographic/glory-adjacent" on Jesus too, same as Moses — the existing
`gold_leaf_conflict` flag in the manifest is doing its job.
