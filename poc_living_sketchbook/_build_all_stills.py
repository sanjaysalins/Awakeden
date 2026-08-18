"""Build one master HTML page showing every still rendered this session, grouped
by round, using absolute file:// image paths so it works regardless of where the
page itself is opened from.

  .venv\\Scripts\\python.exe poc_living_sketchbook/_build_all_stills.py
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parent  # .../poc_living_sketchbook
JPOV = ROOT / "look_and_live" / "_jesus_pov_poc"

def fu(p: Path) -> str:
    return "file:///" + str(p.resolve()).replace("\\", "/")

SECTIONS = [
    ("Round 1 — Print & Craft", "10 mediums, Christ's face test beat", JPOV / "_style_bakeoff", [
        ("01_bronze_register.png", "Bronze Register"), ("02_hewn_light.png", "Hewn Light"),
        ("03_gouged_light.png", "Gouged Light"), ("04_copper_seam.png", "The Copper Seam"),
        ("05_scarred_gold_apse.png", "Scarred-Gold Apse"), ("06_lifted_standard.png", "The Lifted Standard"),
        ("07_brazen_vigil.png", "The Brazen Vigil"), ("08_unbroken_signal.png", "The Unbroken Signal"),
        ("09_kept_cloth.png", "The Kept Cloth"), ("10_bronze_beneath.png", "The Bronze Beneath"),
    ]),
    ("Round 2 — Prince of Egypt / Hercules", "Moses raises the pole", JPOV / "_epic_bakeoff", [
        ("a_ember_horizon.png", "Ember Horizon"), ("b_seraph_frieze.png", "Seraph Frieze"),
        ("c_ember_and_ink.png", "Ember & Ink"), ("d_keypaint.png", "Key-Paint"),
    ]),
    ("Round 3 — Contemporary Spins", "Spider-Verse / Arcane / grading", JPOV / "_contemporary_bakeoff", [
        ("e_emberpress.png", "Emberpress"), ("f_struck_bronze.png", "Struck Bronze"), ("g_cold_ember.png", "Cold Ember"),
    ]),
    ("Round 4 — Viral Cut", "Seraph Frieze, dark & minimal", JPOV / "_viral_seraph", [
        ("h_viral_seraph_witnesses.png", "With witnesses"), ("i_viral_seraph_stripped.png", "Stripped"),
    ]),
    ("Round 5 — Noon Frieze, Five Scenes", "Bright daylight consistency test", JPOV / "_noon_frieze", [
        ("a_pole.png", "Moses raises the pole"), ("b_dying_camp.png", "The dying camp"),
        ("c_nicodemus.png", "Nicodemus by lamplight"), ("d_bitten_man.png", "The bitten man"),
        ("e_the_face.png", "The climax face"),
    ]),
    ("Round 6 — Cross Colors", "Five color schemes, the Landing", JPOV / "_cross_colors", [
        ("1_bone_beacon.png", "Bone & Beacon"), ("2_ember_indigo.png", "Ember Against Indigo"),
        ("3_bone_shadow.png", "Bone and Shadow"), ("4_against_deep.png", "Against the Deep"),
        ("5_potters_field.png", "Potter's Field"),
    ]),
    ("Round 7 — Reference-Matched", "Cross, matched to Moses's technique", JPOV / "_cross_matched", [
        ("a_cream_gold.png", "Cream & gold"), ("b_dusk_indigo.png", "Dusk indigo"),
    ]),
    ("Round 8 — Flat-Skin Fix", "The consistency diagnosis, solved", JPOV / "_cross_flat_skin", [
        ("cross_flat_skin.png", "Cross, flat-skin fix"),
    ]),
    ("The Second Look — Plant Test", "Double-designed shots, bronze serpent pilot", ROOT / "_second_look_format" / "_plants", [
        ("1_moses_raises.png", "Plant 1 — Moses raises"), ("2a_serpent_coil_a.png", "Plant 2a — coil A"),
        ("2b_serpent_coil_b.png", "Plant 2b — coil B"), ("3_shadow_cross.png", "Plant 3 — the shadow"),
        ("4_cruciform_pose.png", "Plant 4 — cruciform pose"),
    ]),
    ("Four Fresh Takes, Tested", "Pentimento, morph, split-screen", ROOT / "_fresh_takes_test", [
        ("1_pentimento.png", "Pentimento"), ("2_top_ascent.png", "Shadow & Body — top"),
        ("3_bottom_ascent.png", "Shadow & Body — bottom"), ("4_emmaus_hook.png", "Emmaus Loop hook"),
        ("5_shadow_and_body.png", "Shadow & Body composite"), ("6_written_twice.png", "Written Twice composite"),
    ]),
    ("Morph Test — Emmaus", "Before/after blend preview", ROOT / "_morph_test", [
        ("a_modern.png", "Modern frame"), ("b_biblical.png", "Biblical frame"),
        ("c_blend_25.png", "25% blend"), ("c_blend_50.png", "50% blend"), ("c_blend_75.png", "75% blend"),
    ]),
    ("Round Three, Tested", "Tutorial / ASMR / unboxing formats", ROOT / "_round3_test", [
        ("1_unfinishable_tutorial.png", "The Unfinishable Tutorial"), ("2_oldest_tutorial.png", "The Oldest Tutorial"),
        ("3_earwitness.png", "Earwitness"), ("4_appraised.png", "Appraised"),
    ]),
    ("Three Threads, Tested", "Rubrica / Meridian / Scarlet Line", ROOT / "_thread_systems_test", [
        ("1a_rubrica_stop.png", "Rubrica — stop"), ("1b_rubrica_gold.png", "Rubrica — gold"),
        ("2a_meridian_stop.png", "Meridian — stop"), ("2b_meridian_gold.png", "Meridian — gold"),
        ("3a_scarletline_stop.png", "Scarlet Line — stop"), ("3b_scarletline_pull.png", "Scarlet Line — pull"),
    ]),
    ("Chosen Register, Tested", "Painterly vs graphic, period-locked", ROOT / "_chosen_register_test", [
        ("a_painterly_close.png", "Painterly close v1"), ("a2_painterly_close.png", "Painterly close v2"),
        ("b_painterly_wide.png", "Painterly wide v1"), ("b2_painterly_wide.png", "Painterly wide v2"),
        ("c2_graphic_close.png", "Graphic close v2"), ("d_graphic_wide.png", "Graphic wide v1"),
        ("d2_graphic_wide.png", "Graphic wide v2"),
    ]),
    ("The Look, Ten Ways", "Exhaustive classical-media bake-off", ROOT / "_chosen_exhaustive", [
        ("01_oil_chiaroscuro.png", "Ember Tenebroso"), ("02_charcoal_study.png", "Ember Study"),
        ("03_gouache_wash.png", "Ember Wash"), ("04_ink_wash.png", "Emberwash"),
        ("05_visdev_concept.png", "Vis-Dev Ember"), ("06_egg_tempera.png", "The Sienese Ember"),
        ("07_pastel_chalk.png", "Firelit Chalk"), ("08_engraved_glaze.png", "Gilded Burin"),
        ("09_cinematic_matte.png", "The Keyframe Register"), ("10_graphite_oil.png", "Firelit Pentimento"),
    ]),
    ("Minimal Scene Setup", "Wide / two-shot / reaction / climax", ROOT / "_chosen_scene_setup", [
        ("a_wide_establishing.png", "Wide establishing"), ("b_dialogue_twoshot.png", "Dialogue two-shot"),
        ("c_peter_profile_reaction.png", "Peter's reaction"), ("d_the_look_climax.png", "The climactic look"),
    ]),
    ("Contemporary Register, Full Set", "Prestige animation, not classical painting", ROOT / "_contemporary_register", [
        ("1_knifelight.png", "Knifelight"), ("2_emberline.png", "Emberline (glitched)"),
        ("3_strokeform.png", "Strokeform"), ("4_cockcrow_silver.png", "Cockcrow Silver"),
        ("5_traced_hour.png", "The Traced Hour"), ("6_engine_realism.png", "Ember-Lit Engine Realism"),
        ("7_ember_and_slate.png", "Ember & Slate"), ("8_emberline_fixed.png", "Emberline (fixed)"),
    ]),
    ("Wide Swings, Tested", "Prince of Egypt / anime / Ethiopian / Persian", ROOT / "_wide_swings", [
        ("1_ember_gouache.png", "Ember Gouache"), ("2_ember_gekiga.png", "Ember Gekiga"),
        ("3_gondar_emberline.png", "Gondar Emberline"), ("4_herat_ember.png", "The Herat Ember"),
    ]),
    ("Jacob's Well, Covered", "Real scene coverage, not a portrait", ROOT / "_well_scene_coverage", [
        ("1_wide_establishing.png", "Wide — the request"), ("2_twoshot_water.png", "Two-shot — living water"),
        ("3_earned_closeup.png", "Close-up — five husbands"), ("4_wide_she_runs.png", "Wide — she runs"),
    ]),
]

CARD_TMPL = """    <article class="plate"><img src="{src}" alt="{alt}" loading="lazy"><div class="cap"><h3>{alt}</h3></div></article>
"""

SECTION_TMPL = """  <section class="round">
    <div class="round-head">
      <h2>{title}</h2>
      <span class="round-sub">{sub} &middot; {count} stills</span>
    </div>
    <div class="grid">
{cards}    </div>
  </section>

"""

def main():
    total = 0
    sections_html = []
    for title, sub, folder, files in SECTIONS:
        cards = []
        for fname, label in files:
            path = folder / fname
            if not path.exists():
                cards.append(f'    <article class="plate missing"><div class="cap"><h3>{label} (missing)</h3></div></article>\n')
                continue
            cards.append(CARD_TMPL.format(src=fu(path), alt=label))
            total += 1
        sections_html.append(SECTION_TMPL.format(title=title, sub=sub, count=len(files), cards="".join(cards)))

    html = HTML_SHELL.format(total=total, sections="".join(sections_html))
    out = ROOT / "_ALL_STILLS_EVER.html"
    out.write_text(html, encoding="utf-8")
    print(f"[ok] {total} stills -> {out}")


HTML_SHELL = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Every Still, One Page</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,300..900;1,9..144,300..900&family=Source+Serif+4:ital,wght@0,400;0,600;1,400&family=IBM+Plex+Mono:wght@400;500&display=swap">
<style>
  :root {{
    --ink: #211c16; --paper: #efe6d2; --paper-raised: #f8f2e4;
    --bronze: #9a5c2c; --line: rgba(33,28,22,0.16); --line-strong: rgba(33,28,22,0.32); --muted: #6b5f4e;
    --shadow: 0 1px 0 rgba(33,28,22,0.06), 0 6px 16px -12px rgba(33,28,22,0.35);
  }}
  @media (prefers-color-scheme: dark) {{
    :root {{
      --ink: #ece3d0; --paper: #17130f; --paper-raised: #201a13; --bronze: #d99a54;
      --line: rgba(236,227,208,0.16); --line-strong: rgba(236,227,208,0.32); --muted: #a89a83;
      --shadow: 0 1px 0 rgba(0,0,0,0.4), 0 8px 20px -14px rgba(0,0,0,0.7);
    }}
  }}
  * {{ box-sizing: border-box; }}
  body {{ margin: 0; background: var(--paper); color: var(--ink); font-family: "Source Serif 4", Georgia, serif; line-height: 1.5; -webkit-font-smoothing: antialiased; }}
  .wrap {{ max-width: 1400px; margin: 0 auto; padding: 56px 28px 100px; }}
  .eyebrow {{ font-family: "IBM Plex Mono", monospace; font-size: 12px; letter-spacing: 0.12em; text-transform: uppercase; color: var(--bronze); margin-bottom: 16px; }}
  h1 {{ font-family: "Fraunces", Georgia, serif; font-weight: 600; font-size: clamp(2rem, 4.4vw, 3rem); margin: 0 0 40px; letter-spacing: -0.01em; }}
  .round {{ margin-bottom: 46px; }}
  .round-head {{ display: flex; align-items: baseline; gap: 14px; flex-wrap: wrap; margin-bottom: 14px; border-bottom: 1px solid var(--line-strong); padding-bottom: 8px; }}
  .round-head h2 {{ font-family: "Fraunces", Georgia, serif; font-weight: 600; font-size: 1.3rem; margin: 0; }}
  .round-sub {{ font-family: "IBM Plex Mono", monospace; font-size: 11px; color: var(--muted); }}
  .grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(150px, 1fr)); gap: 12px; }}
  .plate {{ background: var(--paper-raised); border: 1px solid var(--line); box-shadow: var(--shadow); overflow: hidden; }}
  .plate.missing {{ display: flex; align-items: center; justify-content: center; min-height: 220px; opacity: 0.5; }}
  .plate img {{ width: 100%; aspect-ratio: 9/16; object-fit: cover; display: block; }}
  .plate .cap {{ padding: 8px 10px; }}
  .plate h3 {{ font-family: "Fraunces", Georgia, serif; font-size: 0.82rem; font-weight: 600; margin: 0; line-height: 1.25; }}
</style>
</head>
<body>
<div class="wrap">
  <div class="eyebrow">{total} stills &middot; every round, this session</div>
  <h1>Every Still, One Page</h1>
{sections}</div>
</body>
</html>
"""

if __name__ == "__main__":
    main()
