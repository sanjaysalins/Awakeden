#!/usr/bin/env python
"""Contact sheets (6-up, labeled) of the 36 v3 stills for the eye-audit."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

POOL = Path(__file__).resolve().parent / "v1" / "visual_16x9_inked"
OUT = POOL / "_v3_contact"; OUT.mkdir(exist_ok=True)
SLUGS = ["golgotha_three_crosses_ridge","ninth_hour_darkness","roman_nails_pouch","david_scroll_sealed",
 "jerusalem_night_lyre","execution_stakes_field","mockers_below_cross_low","spit_shout_macro",
 "old_king_hands_rings","shepherd_boy_sling","war_helmet_spear_rest","wrists_bound_beam_macro",
 "ribs_stretched_macro","clay_potsherd_dust","water_spilled_stone","sponge_vinegar_jar",
 "dice_cup_shadow","vesture_seamless_folded","john_at_cross_foot","scholars_debate_two",
 "quill_ink_drop","hebrew_scroll_edge_light","lion_shadow_wall","alexandria_harbor_night",
 "seventy_scribes_lamps","roads_converge_valley","cry_profile_dark","synagogue_listeners_lean",
 "hill_crowd_watching_storm","tear_track_macro","substitute_shadow","grave_clothes_folded_macro",
 "stone_rolled_groove","congregation_hands_lifted","morning_birds_hill","threshold_open_door"]
F = ImageFont.truetype(r"C:\Windows\Fonts\arialbd.ttf", 26)
W, H, COLS, ROWS = 640, 360, 2, 3
for page in range((len(SLUGS) + 5) // 6):
    sheet = Image.new("RGB", (COLS * W, ROWS * (H + 34)), (18, 18, 18))
    d = ImageDraw.Draw(sheet)
    for k, slug in enumerate(SLUGS[page * 6:(page + 1) * 6]):
        x, y = (k % COLS) * W, (k // COLS) * (H + 34)
        p = POOL / f"{slug}.png"
        if p.exists():
            sheet.paste(Image.open(p).resize((W, H)), (x, y))
        d.text((x + 8, y + H + 4), slug, font=F, fill=(240, 220, 120))
    sheet.save(OUT / f"sheet_{page + 1}.jpg", quality=88)
print("sheets:", (len(SLUGS) + 5) // 6, "->", OUT)
