"""Build style_manifest.json -- the graded, evidence-backed catalog the
STYLE_SELECTION.md mechanism reads. Combines three sources:
  1. The 35 variants themselves (parsed from STYLE_VARIANTS.md/STYLE_LAB.md
     via _run_bakeoff.build_jobs, same source of truth as the renders).
  2. Real bake-off scores (a vision agent scored every render against
     baseline -- see _SCORES_MOSES.md; _SCORES_JESUS.md once that batch's
     review completes).
  3. Beat-fit metadata (family / beat_signal / avoid_on / dosage budget) --
     authored judgment, not derived from the renders; the renders can only
     tell you IF a technique works, not WHEN a story should reach for it.

Status computed per variant:
  production_approved -- handmade_alive >= 4 AND identity_lock >= 4 on
                          every character tested
  caution              -- scores are fine but a real caveat applies (weak
                          technique visibility on a portrait scene, a
                          prompt-fidelity miss, a locked-rule conflict)
  rejected             -- any score <= 2, or a hard failure noted

Re-run any time new score data lands (e.g. once Jesus is scored) --
overwrites style_manifest.json, never the source markdown/scores.

  .venv\\Scripts\\python.exe poc_living_sketchbook/_style_identity_bakeoff/_build_manifest.py
"""
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from _run_bakeoff import build_jobs  # noqa: E402

OUT = HERE / "style_manifest.json"

# Moses scores, transcribed from the vision-agent review in
# _SCORES_MOSES.md (2026-08-01). slug -> (handmade_alive, identity_lock, note)
MOSES_SCORES = {
    "sl01_baseline_reference_plate": (3, 5, "Near-duplicate of baseline, tighter crop; no distinct technique visible"),
    "sl02_continuous_contour_line": (4, 5, "Clean linework; contour line not strongly distinct from baseline"),
    "sl03_notan_pure_silhouette": (5, 4, "Bold solid-black silhouette body; face/beard still clearly match"),
    "sl04_visible_underdrawing": (4, 5, "Nice unfinished-sketch edges with pencil grid; face fully resolved"),
    "sl05_selective_resolution": (5, 5, "Dynamic two-hand grip, striking selective detail; clean"),
    "sl06_wet_in_wet_bleed": (5, 5, "Gorgeous loose watercolor bleed halo; face crisp and true to baseline"),
    "sl07_misregistered_print": (5, 5, "Vibrant red/blue offset registration; strong printmaking feel, clean"),
    "sl08_multiple_exposure_motion_ghosting": (5, 5, "Striking triple-ghost motion blur; all three faces consistent"),
    "sl09_extreme_low_angle": (4, 4, "Wide low-angle full body; face smaller, expression differs from baseline"),
    "sl10_overhead_plan": (5, 5, "PROMPT-FIDELITY MISS: beautiful close crop but NOT overhead as named"),
    "sl11_shadow_as_subject": (4, 4, "Creative inverted-shadow concept; figure small, fine detail less certain"),
    "sl12_scratchboard_inversion": (5, 5, "Striking dark scratchboard etch with gold fleck; clean, alive"),
    "sl13_charcoal_and_eraser": (5, 5, "Gorgeous grayscale charcoal with erased highlights; hand-crafted feel"),
    "sl14_torn_paper_depth_planes": (4, 4, "Nice layered depth panels; face smaller scale reduces certainty"),
    "sl15_frame_break": (4, 5, "PROMPT-FIDELITY MISS: good scene but no visible frame-break element"),
    "sl16_foreground_occlusion": (4, 5, "Dark rock/branch occludes foreground nicely; face fully clear"),
    "sl17_gold_leaf_as_structure": (5, 5, "Striking cracked gold-leaf background; strong identity match"),
    "sl18_macro_crop": (5, 5, "Excellent extreme close detail; clean, no issues"),
    "sl19_insect_scale": (4, 5, "PROMPT-FIDELITY MISS: just a normal close crop, no scale effect applied"),
    "sl20_sketchbook_spread": (5, 5, "v2 (text-free prompt) + caption overlay, user-approved 2026-08-01 -- verified by eye, not the original scoring agent"),
    "sv01_kinetic_storm_focus": (3, 5, "WEAK ON PORTRAIT: near-identical to baseline, no visible motion/storm"),
    "sv02_chiaroscuro_pocket_wash": (4, 5, "Close to baseline; contrast subtle, not strongly dramatic"),
    "sv03_layered_collage_construction": (4, 5, "Close to baseline with slightly more visible collage layering"),
    "sv04_vertical_pillar_gold_thread": (4, 5, "Distinct vertical gold pillar bisecting composition; clean"),
    "sv05_cyanotype_blue_focus": (5, 5, "Full blue cyanotype monochrome, striking and distinct; face clear"),
    "sv06_sgraffito_surface_scratch_technique": (3, 5, "WEAK ON PORTRAIT: near-identical, no visible scratch texture"),
    "sv07_deconstructed_lithograph_with_noise": (3, 5, "WEAK ON PORTRAIT: near-identical, no visible print noise"),
    "sv08_expressive_gestural_graphite_and_ink": (4, 5, "Close to baseline; linework not markedly more gestural"),
    "sv09_hand_pulled_monotype_and_smudged_transfer": (5, 5, "Visible smudged transfer texture, distinct and alive"),
    "sv10_offset_screenprint_with_misregistered_ink_plates": (3, 5, "WEAK ON PORTRAIT: near-identical, no misregistration visible"),
    "sv11_ink_wash_chiaroscuro_and_scratched_light": (4, 5, "Close to baseline; scratched-light effect not strongly visible"),
    "sv12_ground_level_cinematic_extreme_crop": (5, 5, "Strong desert scene, manna in hand, planted staff; clean"),
    "sv13_torn_paper_relief_collage_with_translucent_layers": (5, 5, "Gold flecks, translucent torn-paper layers, striking"),
    "sv14_drypoint_etching_cross_hatching_and_plate_wear": (5, 5, "Visible cross-hatch etching texture, nice plate-wear feel"),
    "sv15_controlled_abstraction_with_one_precise_focal_point": (5, 5, "Soft abstract color blooms frame a crisp focal face"),
}

# Jesus scores, transcribed from the vision-agent review in
# _SCORES_JESUS.md (2026-08-01). slug -> (handmade_alive, identity_lock, note)
JESUS_SCORES = {
    "sl01_baseline_reference_plate": (3, 5, "Near-duplicate of baseline, not a distinct style"),
    "sl02_continuous_contour_line": (5, 3, "Line-only render reads hair much lighter/blonder than baseline"),
    "sl03_notan_pure_silhouette": (5, 3, "Bold B&W silhouette; composition turned 3/4, off-center"),
    "sl04_visible_underdrawing": (4, 4, "Construction grid lines visible; slight smile, arms crossed"),
    "sl05_selective_resolution": (5, 5, "Loose pencil body, sharp hands; added staff prop (scene drift)"),
    "sl06_wet_in_wet_bleed": (5, 5, "Lovely color-bleed edges, tighter crop, strong likeness"),
    "sl07_misregistered_print": (3, 5, "Odd dark diagonal smudge top-right looks like a glitch"),
    "sl08_multiple_exposure_motion_ghosting": (5, 4, "Full pose change: riding donkey with ghost-trail figures (scene drift)"),
    "sl09_extreme_low_angle": (4, 3, "Full-body vs sky; face small/distant, harder to verify"),
    "sl10_overhead_plan": (5, 4, "HARD-RULE VIOLATION: visible survey text/labels/signature baked into image"),
    "sl11_shadow_as_subject": (5, 2, "IDENTITY FAIL: tiny distant figure, unintended halo-like light behind head"),
    "sl12_scratchboard_inversion": (5, 4, "Striking white-on-black scratchboard, strong likeness"),
    "sl13_charcoal_and_eraser": (5, 5, "Great smudged charcoal; soft erased vignette behind head, borderline halo-ish"),
    "sl14_torn_paper_depth_planes": (5, 4, "Layered torn-paper depth collage, seated with a goat (scene drift)"),
    "sl15_frame_break": (5, 5, "Donkey/hand break the frame border; strong, alive (scene drift)"),
    "sl16_foreground_occlusion": (5, 2, "IDENTITY FAIL: wide landscape, figure tiny/distant, can't confirm identity"),
    "sl17_gold_leaf_as_structure": (4, 4, "Whole background cracked gold leaf, reads iconographic/glory-adjacent"),
    "sl18_macro_crop": (5, 3, "Extreme hand/rope macro; only nose+beard of face visible"),
    "sl19_insect_scale": (4, 4, "Doesn't read as insect-scale; just a sepia group close-up"),
    "sl20_sketchbook_spread": (5, 5, "v2 (text-free prompt) + caption overlay, user-approved 2026-08-01 -- verified by eye, not the original scoring agent"),
    "sv01_kinetic_storm_focus": (3, 5, "WEAK ON PORTRAIT: almost identical to baseline, no storm energy"),
    "sv02_chiaroscuro_pocket_wash": (3, 5, "WEAK ON PORTRAIT: barely differentiated, minimal chiaroscuro"),
    "sv03_layered_collage_construction": (3, 5, "WEAK ON PORTRAIT: close to baseline, collage not clearly visible"),
    "sv04_vertical_pillar_gold_thread": (3, 5, "WEAK ON PORTRAIT: near-baseline, thin gold edge only, no pillar motif"),
    "sv05_cyanotype_blue_focus": (4, 4, "Strong monochrome cyanotype blue wash, effective and alive"),
    "sv06_sgraffito_surface_scratch_technique": (4, 4, "Visible scratch/hatch texture on garment; cropped, no hands"),
    "sv07_deconstructed_lithograph_with_noise": (3, 5, "WEAK ON PORTRAIT: subtle halftone dot noise on shoulder only"),
    "sv08_expressive_gestural_graphite_and_ink": (3, 5, "WEAK ON PORTRAIT: close to baseline, only mildly more gestural"),
    "sv09_hand_pulled_monotype_and_smudged_transfer": (4, 4, "Nice ink smudges on cheek/chest; slightly obscures face"),
    "sv10_offset_screenprint_with_misregistered_ink_plates": (3, 5, "WEAK ON PORTRAIT: subtle misregistration on shoulder edge only"),
    "sv11_ink_wash_chiaroscuro_and_scratched_light": (5, 4, "Dramatic dark ink wash; hair/beard read notably darker"),
    "sv12_ground_level_cinematic_extreme_crop": (5, 4, "Pose changed to kneeling on ground with pebbles (scene drift)"),
    "sv13_torn_paper_relief_collage_with_translucent_layers": (4, 4, "Torn-paper layers at edges, gaze turned slightly off-center"),
    "sv14_drypoint_etching_cross_hatching_and_plate_wear": (5, 4, "Great plate-wear border and cross-hatching; gaze off-center"),
    "sv15_controlled_abstraction_with_one_precise_focal_point": (5, 4, "Color-splash background, desaturated hair; striking focal contrast"),
}

# Force-rejected regardless of numeric scores -- hard-rule violations
# (visible/garbled text baked into the image) are disqualifying no matter
# how good the rest of the render is. The violation is in the prompt/
# technique, not the character, so it applies to both.
# sl20 EXCLUDED 2026-08-01: fixed via the v2 prompt (drops "marginal
# studies"/"pencil ticks", the trigger concepts) + a deterministic
# caption-overlay pass (pipeline/style_select-adjacent tool:
# poc_living_sketchbook/_style_identity_bakeoff/_caption_mockup.py) --
# real chosen words, KUNSTLER.TTF hand-script, never asked of the image
# model. User-approved on both characters ("very nice, love it, we should
# use more of this visual"). See META's sl20 entry for the two-step
# requirement this status now assumes.
HARD_FAIL_SLUGS = {"sl10_overhead_plan"}

# Beat-fit metadata -- authored judgment (family / when to reach for it /
# what to avoid it on / dosage caps), NOT derived from the renders. See
# STYLE_SELECTION.md sec.3 for the fuller per-variant rationale on the 15
# STYLE_VARIANTS entries; STYLE_LAB entries are tagged fresh here since
# STYLE_SELECTION.md only scored their identity-risk hypothesis, not beat fit.
META = {
    "sv01_kinetic_storm_focus": dict(family="linework", beat_signal=["kinetic", "urgent", "storm", "fleeing"], avoid_on=["calm", "landing"]),
    "sv02_chiaroscuro_pocket_wash": dict(family="light-contrast", beat_signal=["dread", "judgment", "before-a-turn", "night"], avoid_on=["landing", "glory"]),
    "sv03_layered_collage_construction": dict(family="collage", beat_signal=["memory", "flashback", "composite"], avoid_on=["single-clear-action"]),
    "sv04_vertical_pillar_gold_thread": dict(family="camera-light", beat_signal=["divine-presence", "theophany", "pillar"], avoid_on=["ordinary-narrative"], gold_leaf_conflict=False),
    "sv05_cyanotype_blue_focus": dict(family="palette", beat_signal=["judgment", "exile", "testimony", "cold-register"], avoid_on=["landing", "glory"]),
    "sv06_sgraffito_surface_scratch_technique": dict(family="texture", beat_signal=["hardship", "forge", "roughness"], avoid_on=["calm-portrait"]),
    "sv07_deconstructed_lithograph_with_noise": dict(family="print-process", beat_signal=["time-shift", "corruption", "drift"], avoid_on=["present-tense-witness"]),
    "sv08_expressive_gestural_graphite_and_ink": dict(family="linework", beat_signal=["crowd", "busy", "populated"], avoid_on=[]),
    "sv09_hand_pulled_monotype_and_smudged_transfer": dict(family="print-process", beat_signal=["doubt", "hesitation", "half-remembered"], avoid_on=["clear-resolve"]),
    "sv10_offset_screenprint_with_misregistered_ink_plates": dict(family="print-process", beat_signal=["tense", "documentary", "graphic"], avoid_on=["calm"]),
    "sv11_ink_wash_chiaroscuro_and_scratched_light": dict(family="light-contrast", beat_signal=["dread-with-one-focal-light"], avoid_on=["landing", "glory"]),
    "sv12_ground_level_cinematic_extreme_crop": dict(family="camera", beat_signal=["hook", "cold-open", "immediacy"], avoid_on=["establishing-wide"]),
    "sv13_torn_paper_relief_collage_with_translucent_layers": dict(family="collage", beat_signal=["memory", "composite"], avoid_on=["single-clear-action"]),
    "sv14_drypoint_etching_cross_hatching_and_plate_wear": dict(family="texture", beat_signal=["urgent", "ancient", "tactile"], avoid_on=["calm-portrait"]),
    "sv15_controlled_abstraction_with_one_precise_focal_point": dict(family="composition", beat_signal=["single-object-focus", "held-detail"], avoid_on=["wide-establishing"]),
    "sl01_baseline_reference_plate": dict(family="reference", beat_signal=[], avoid_on=["*"], note="not a real variant, keep as reference row only"),
    "sl02_continuous_contour_line": dict(family="linework", beat_signal=["calm", "single-gesture"], avoid_on=[]),
    "sl03_notan_pure_silhouette": dict(family="reduction", beat_signal=["threshold", "judgment", "stark"], avoid_on=["face-detail-critical"]),
    "sl04_visible_underdrawing": dict(family="process-reveal", beat_signal=["uncertainty", "deliberation", "in-progress"], avoid_on=[]),
    "sl05_selective_resolution": dict(family="focus", beat_signal=["one-object-matters", "held-detail"], avoid_on=[]),
    "sl06_wet_in_wet_bleed": dict(family="wash-process", beat_signal=["grief", "overflow", "water", "weather"], avoid_on=[]),
    "sl07_misregistered_print": dict(family="print-process", beat_signal=["documentary", "historical-distance"], avoid_on=[]),
    "sl08_multiple_exposure_motion_ghosting": dict(family="motion", beat_signal=["journey", "repeated-action", "passage-of-time"], avoid_on=[]),
    "sl09_extreme_low_angle": dict(family="camera", beat_signal=["awe", "monumental", "hero-moment"], avoid_on=[]),
    "sl10_overhead_plan": dict(family="camera", beat_signal=["scale", "isolation", "map-like"], avoid_on=[], note="UNRELIABLE -- did not render top-down, re-test wording before use"),
    "sl11_shadow_as_subject": dict(family="light", beat_signal=["foreboding", "the-past-looms"], avoid_on=[]),
    "sl12_scratchboard_inversion": dict(family="texture-inversion", beat_signal=["night", "danger", "threshold-into-dark"], avoid_on=["landing"], gold_leaf_conflict=True),
    "sl13_charcoal_and_eraser": dict(family="tonal", beat_signal=["memory", "erasure", "soft-grief"], avoid_on=[]),
    "sl14_torn_paper_depth_planes": dict(family="collage", beat_signal=["memory", "layered-time", "composite"], avoid_on=[]),
    "sl15_frame_break": dict(family="composition-device", beat_signal=["overflow", "breaking-through"], avoid_on=[], note="UNRELIABLE -- frame-break not visible, re-test wording before use"),
    "sl16_foreground_occlusion": dict(family="camera", beat_signal=["hidden-observer", "threshold"], avoid_on=[]),
    "sl17_gold_leaf_as_structure": dict(family="palette", beat_signal=["glory-ONLY"], avoid_on=["*-non-glory"], gold_leaf_conflict=True),
    "sl18_macro_crop": dict(family="camera", beat_signal=["tactile", "intimate-detail", "object-focus"], avoid_on=[]),
    "sl19_insect_scale": dict(family="camera", beat_signal=["vastness", "smallness-before-God"], avoid_on=[], note="UNRELIABLE -- scale effect not visible, re-test wording before use"),
    "sl20_sketchbook_spread": dict(family="composite", beat_signal=["study", "culmination", "character-intro"], avoid_on=[],
                                    note="REQUIRES the v2 prompt (STYLE_LAB.md) + a caption-overlay pass "
                                         "(_caption_mockup.py pattern) -- the raw v1 single-render prompt is "
                                         "still text-unsafe, only the two-step combo is approved. User-loved "
                                         "this look 2026-08-01: 'we should use more of this visual.'"),
}

DEFAULT_MAX_PER_EPISODE = 1
DEFAULT_MIN_GAP = 8


def _one_char_status(ha, il, note):
    """Per-character read: rejected / caution / clean. Combined across
    characters by main() -- a variant needs 'clean' on EVERY tested
    character to reach production_approved."""
    if ha <= 2 or il <= 2:
        return "rejected"
    if "UNRELIABLE" in note or "WEAK ON PORTRAIT" in note or "PROMPT-FIDELITY MISS" in note:
        return "caution"
    if ha >= 4 and il >= 4:
        return "clean"
    return "caution"


def status_for(slug, per_character_status):
    """Combine per-character reads (a dict of char -> 'rejected'/'caution'/
    'clean'/None) into one manifest status. Any hard-fail or rejected
    character reading rejects the whole variant; any caution demotes to
    caution; only clean-on-every-tested-character reaches
    production_approved."""
    if slug in HARD_FAIL_SLUGS:
        return "rejected"
    statuses = [s for s in per_character_status.values() if s is not None]
    if not statuses:
        return "caution"  # untested
    if "rejected" in statuses:
        return "rejected"
    if "caution" in statuses:
        return "caution"
    return "production_approved"


def main():
    jobs = {slug: (name, src) for slug, name, prefix, src in build_jobs()}
    manifest = {}
    all_slugs = set(MOSES_SCORES) | set(JESUS_SCORES)
    for slug in all_slugs:
        name, src = jobs.get(slug, (slug, "?"))
        meta = META.get(slug, {})
        m_score = MOSES_SCORES.get(slug)
        j_score = JESUS_SCORES.get(slug)
        per_char = {
            "moses": _one_char_status(*m_score) if m_score else None,
            "jesus": _one_char_status(*j_score) if j_score else None,
        }
        manifest[slug] = {
            "id": slug,
            "name": name,
            "source": src,
            "family": meta.get("family", "unclassified"),
            "beat_signal": meta.get("beat_signal", []),
            "avoid_on": meta.get("avoid_on", []),
            "gold_leaf_conflict": meta.get("gold_leaf_conflict", False),
            "max_per_episode": DEFAULT_MAX_PER_EPISODE,
            "min_spread_gap": DEFAULT_MIN_GAP,
            "scores": {
                "moses": ({"handmade_alive": m_score[0], "identity_lock": m_score[1], "note": m_score[2]}
                          if m_score else None),
                "jesus": ({"handmade_alive": j_score[0], "identity_lock": j_score[1], "note": j_score[2]}
                          if j_score else None),
            },
            "status": status_for(slug, per_char),
            "manifest_note": meta.get("note", ""),
        }
    OUT.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    counts = {}
    for v in manifest.values():
        counts[v["status"]] = counts.get(v["status"], 0) + 1
    print(f"[out] {OUT}  ({len(manifest)} variants: {counts})")
    rejected = sorted(k for k, v in manifest.items() if v["status"] == "rejected")
    print(f"[rejected] {rejected}")


if __name__ == "__main__":
    main()
