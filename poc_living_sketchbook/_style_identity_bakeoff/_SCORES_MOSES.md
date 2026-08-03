# Moses bake-off scores — raw agent review, 2026-08-01

Produced by a vision-capable subagent that opened every one of the 36
PNGs in `stills/` and scored each against `baseline.png`. Not hand-edited
below (see `_MANIFEST_NOTES.md` for the interpretation pass). Scale 1-5 on
two axes: HANDMADE_ALIVE (does it look genuinely hand-crafted) and
IDENTITY_LOCK (does it still read as the same Moses as baseline).

| slug | handmade_alive | identity_lock | note |
|---|---|---|---|
| sl01_baseline_reference_plate | 3 | 5 | Near-duplicate of baseline, tighter crop; no distinct new technique visible |
| sl02_continuous_contour_line | 4 | 5 | Clean linework, close match to baseline; contour line not strongly distinct |
| sl03_notan_pure_silhouette | 5 | 4 | Bold solid-black silhouette body; face/beard still clearly match baseline |
| sl04_visible_underdrawing | 4 | 5 | Nice unfinished-sketch edges with pencil grid; face fully resolved and matching |
| sl05_selective_resolution | 5 | 5 | Dynamic two-hand grip, open mouth, striking selective detail; clean |
| sl06_wet_in_wet_bleed | 5 | 5 | Gorgeous loose watercolor bleed halo; face crisp and true to baseline |
| sl07_misregistered_print | 5 | 5 | Vibrant red/blue offset registration lines; strong printmaking feel, clean |
| sl08_multiple_exposure_motion_ghosting | 5 | 5 | Striking triple-ghost profile motion blur; all three faces consistent |
| sl09_extreme_low_angle | 4 | 4 | Wide low-angle full body; face smaller, open-mouth expression differs from baseline |
| sl10_overhead_plan | 5 | 5 | Beautiful close crop but NOT an overhead angle as name implies |
| sl11_shadow_as_subject | 4 | 4 | Creative inverted-shadow concept; figure small so fine detail less certain |
| sl12_scratchboard_inversion | 5 | 5 | Striking dark scratchboard etch with gold fleck; clean, alive |
| sl13_charcoal_and_eraser | 5 | 5 | Gorgeous grayscale charcoal with erased highlights; very hand-crafted feel |
| sl14_torn_paper_depth_planes | 4 | 4 | Nice layered depth panels with rabbit; face smaller scale reduces certainty |
| sl15_frame_break | 4 | 5 | Good donkey-pack/tents scene; no obvious frame-breaking element actually visible |
| sl16_foreground_occlusion | 4 | 5 | Dark rock/branch occludes foreground nicely; face fully clear and matching |
| sl17_gold_leaf_as_structure | 5 | 5 | Striking cracked gold-leaf background; clean, alive, strong identity match |
| sl18_macro_crop | 5 | 5 | Excellent extreme close detail; clean, no issues |
| sl19_insect_scale | 4 | 5 | Just a normal close crop; no real insect-scale/macro effect applied |
| sl20_sketchbook_spread | 5 | 5 | Charming multi-study spread (hand/boot/profile/figure); consistent identity throughout |
| sv01_kinetic_storm_focus | 3 | 5 | Near-identical to baseline; no visible storm or kinetic motion effect |
| sv02_chiaroscuro_pocket_wash | 4 | 5 | Close to baseline; chiaroscuro contrast is subtle, not strongly dramatic |
| sv03_layered_collage_construction | 4 | 5 | Close to baseline with slightly more visible collage layering |
| sv04_vertical_pillar_gold_thread | 4 | 5 | Distinct vertical gold pillar bisecting composition; clean, good identity |
| sv05_cyanotype_blue_focus | 5 | 5 | Full blue cyanotype monochrome, striking and distinct; face still clear |
| sv06_sgraffito_surface_scratch_technique | 3 | 5 | Near-identical to baseline; no visible scratch/sgraffito surface texture |
| sv07_deconstructed_lithograph_with_noise | 3 | 5 | Near-identical to baseline; no visible lithograph noise/deconstruction effect |
| sv08_expressive_gestural_graphite_and_ink | 4 | 5 | Close to baseline; linework not markedly more gestural or loose |
| sv09_hand_pulled_monotype_and_smudged_transfer | 5 | 5 | Visible smudged fingerprint/transfer texture in background, distinct and alive |
| sv10_offset_screenprint_with_misregistered_ink_plates | 3 | 5 | Near-identical to baseline; no visible screenprint misregistration/offset effect |
| sv11_ink_wash_chiaroscuro_and_scratched_light | 4 | 5 | Close to baseline; scratched-light effect not strongly visible |
| sv12_ground_level_cinematic_extreme_crop | 5 | 5 | Strong desert scene, manna in outstretched hand, planted staff; clean |
| sv13_torn_paper_relief_collage_with_translucent_layers | 5 | 5 | Gold leaf flecks and translucent torn-paper layers, striking and alive |
| sv14_drypoint_etching_cross_hatching_and_plate_wear | 5 | 5 | Visible cross-hatch etching texture in background, nice plate-wear feel |
| sv15_controlled_abstraction_with_one_precise_focal_point | 5 | 5 | Soft abstract color blooms frame a crisp focal face, effective |

## Reading this (before it becomes the manifest)

**Identity-lock held far better than the preliminary risk table in
STYLE_SELECTION.md guessed** — almost every variant scored 4-5, including
the ones flagged "high risk" (Cyanotype 5, Layered Collage 4, Sgraffito 5,
Torn-Paper Collage 5). That preliminary table was a hypothesis, not a
finding — this is the correction, on THIS composition (close, direct-
address portrait). Don't assume it generalizes to every pose/framing
without re-checking (a wide multi-figure shot is a different test).

**A real, separate finding: several STYLE_VARIANTS.md prompts (1, 6, 7,
10, and to a lesser extent 2/3/8/11) barely changed anything vs baseline.**
Those 15 were originally written AROUND a crowd/manna scene — a lot of
each technique's visible expression was tied to elements (falling manna,
figures turned away, environmental texture) that don't exist in a single
portrait scene. The STYLE_LAB.md 20 (engineered as a pure technique-axis
bake-off, subject-agnostic by design) transferred far more reliably. This
matters for the manifest: a technique "not working" here may mean it needs
its ORIGINAL kind of busy/populated scene, not that it's a bad technique.

**Prompt-fidelity misses (worth noting, not fatal):** sl10 (Overhead Plan)
didn't actually go top-down; sl15 (Frame Break) didn't visibly break the
frame; sl19 (Insect Scale) didn't shrink the subject. The model followed
the SCENE (Moses close-up) more strongly than some of the STYLE prefix's
compositional instructions when the two conflicted. Flag these three as
"needs stronger prompt wording, re-test before relying on the named
compositional effect" rather than rejecting the underlying technique.
