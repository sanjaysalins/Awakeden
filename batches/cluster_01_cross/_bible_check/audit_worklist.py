# -*- coding: utf-8 -*-
"""Build the cross-cluster FAIL worklist: md5-dedupe the flagged stills across pieces,
write _bible_check/audit_worklist.json (groups + every piece/slug it clears)."""
import hashlib, json, sys
from pathlib import Path
sys.stdout.reconfigure(errors="replace")
ROOT = Path(r"C:\Users\sanjay\PycharmProjects\JesusInTheBible\batches\cluster_01_cross")

# (piece, slug) rows the 4 audit agents FAILED (pilot uses explicit relative paths)
FAILS = [
 ("crucifixion_foretold_ps2218","us_under_cross_shadow"),("crucifixion_foretold_ps2218","soldiers_gambling"),
 ("crucifixion_foretold_ps2218","golgotha_hill_wide"),("crucifixion_foretold_ps2218","seamless_robe_lots"),
 ("crucifixion_foretold_ps2218","lots_cup_close"),("crucifixion_foretold_ps2218","john_watching"),
 ("forsaken_cry_ps221","ninth_hour_darkness"),("forsaken_cry_ps221","us_under_cross_shadow"),
 ("forsaken_cry_ps221","golgotha_hill_wide"),("forsaken_cry_ps221","bowed_head_finished"),
 ("i_thirst_john1928","bowed_head_finished"),("i_thirst_john1928","us_under_cross_shadow"),
 ("into_thy_hands_luke2346","bowed_head_finished"),("into_thy_hands_luke2346","face_on_cross"),
 ("into_thy_hands_luke2346","golgotha_hill_wide"),
 ("it_is_finished_john1930","bowed_head_finished"),("it_is_finished_john1930","face_on_cross"),
 ("it_is_finished_john1930","golgotha_hill_wide"),("it_is_finished_john1930","hands_shaping_light"),
 ("it_is_finished_john1930","us_under_cross_shadow"),("it_is_finished_john1930","vinegar_sponge_reed"),
 ("pierced_zech1210","blood_water_wood"),("pierced_zech1210","face_on_cross"),
 ("pierced_zech1210","golgotha_hill_wide"),("pierced_zech1210","seamless_robe_lots"),
 ("pierced_zech1210","soldiers_gambling"),("pierced_zech1210","us_under_cross_shadow"),
 ("thirty_pieces_zech11","face_on_cross"),
 ("today_paradise_luke2343","golgotha_hill_wide"),("today_paradise_luke2343","us_under_cross_shadow"),
 ("watch_one_hour_matt2640","sleeping_peter_close"),("watch_one_hour_matt2640","us_under_cross_shadow"),
 ("watch_one_hour_matt2640","golgotha_hill_wide"),("watch_one_hour_matt2640","face_on_cross"),
 ("woman_behold_john1926","mary_at_cross"),("woman_behold_john1926","mary_and_john"),
 ("woman_behold_john1926","jesus_looks_down"),("woman_behold_john1926","john_leads_home"),
 ("woman_behold_john1926","golgotha_hill_wide"),("woman_behold_john1926","face_on_cross"),
 ("woman_behold_john1926","us_under_cross_shadow"),
 ("father_forgive_them", r"visual\_byteplus\reshoot\01c_soldiers_gamble.png"),
 ("father_forgive_them", r"visual\_byteplus\reshoot\04_cast_lots.png"),
 ("father_forgive_them", r"visual\_byteplus\reshoot\03_prayer_close.png"),
]

groups = {}
for piece, ref in FAILS:
    p = (ROOT/piece/ref) if ref.endswith(".png") else (ROOT/piece/"visual"/f"{ref}.png")
    if not p.is_file():
        print("MISSING:", p); continue
    h = hashlib.md5(p.read_bytes()).hexdigest()[:12]
    g = groups.setdefault(h, {"canonical": str(p), "uses": []})
    g["uses"].append({"piece": piece, "slug": Path(ref).stem, "path": str(p)})

out = ROOT/"_bible_check"/"audit_worklist.json"
out.write_text(json.dumps(groups, indent=1), encoding="utf-8")
print(f"{len(FAILS)} fail rows -> {len(groups)} unique files")
for h, g in groups.items():
    print(f"  {h}  x{len(g['uses'])}  {Path(g['canonical']).name}  [{', '.join(sorted(set(u['piece'] for u in g['uses']))[:4])}{'...' if len(set(u['piece'] for u in g['uses']))>4 else ''}]")
