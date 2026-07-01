#!/usr/bin/env python
"""Build the full-13 review gallery for the v2 (red-teamed) scene plan.

Maps each scene to its actual PNG (reused reshoot still or a new depth still) and emits
visual/_byteplus/GALLERY_v2.html in reading order with beat / subject_type / bible ref / timing.
"""
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
PLAN = HERE / "visual" / "scene_plan_v2.json"
OUT = HERE / "visual" / "_byteplus" / "GALLERY_v2.html"

# scene slug -> image file (relative to visual/_byteplus/)
IMG = {
    "nail_through_hand": "nail_close_45.png",
    "soldiers_gambling_establish": "reshoot/01c_soldiers_gamble.png",
    "crowd_mocking": "reshoot/crowd_mocking.png",
    "face_on_cross_speaks": "reshoot/02_jesus_prays.png",
    "father_forgive_them_face": "reshoot/03_prayer_close.png",
    "psalm22_scroll_david": "reshoot/psalm22_scroll_david.png",
    "seamless_robe_lots_cast": "reshoot/04_cast_lots.png",
    "executioner_ignorance": "reshoot/executioner_ignorance.png",
    "us_under_cross_shadow": "reshoot/06b_our_sin.png",
    "willing_offering": "reshoot/06_cross_over_us.png",
    "risen_interceding_christ": "reshoot/risen_interceding_christ.png",
    "darkness_veil_torn": "reshoot/darkness_veil_torn.png",
    "risen_mercy_hand_held_out": "reshoot/07_risen_hero.png",
    "golgotha_hill_wide": "reshoot/golgotha_hill_wide.png",   # NEW epic wide -> rebuilds beat 9
    "nail_through_hand_punch": "nail_close_45.png",           # beat 1 hook: zoom-snap impact variant
    "crowd_mocking_punch": "reshoot/crowd_mocking.png",       # beat 3: zoom-snap impact variant
}
LINE = {
    1: "Nails through his hands.", 2: "Soldiers at his feet, gambling for his clothes.",
    3: "…a word no one expected — not a curse.", 4: "It is a prayer… for the very people killing him.",
    5: "Father, forgive them; for they know not what they do.", 6: "Luke records it as they gambled:",
    7: "And they parted his raiment, and cast lots.", 8: "…does not excuse the sin; it intercedes for the sinner.",
    9: "The sin that put him there was ours too.", 10: "He gave himself willingly.",
    11: "…still lives to make intercession for sinners.", 12: "…while we were yet sinners, Christ died for us.",
    13: "Come, and receive it by faith.",
}
COLOR = {"christ_hero": "#e8c069", "christ_detail": "#e8c069", "christ_risen": "#e8c069",
         "context_scene": "#7fb0d1", "ot_echo": "#9d7fd1", "human_us": "#7fd18b", "symbolic": "#d17f9d"}


def main():
    scenes = json.loads(PLAN.read_text(encoding="utf-8"))["final_plan"]["scenes"]
    cards = []
    for s in scenes:
        i = s["index"]; slug = s["slug"]; st = s["subject_type"]
        img = IMG.get(slug, "")
        new = s.get("reuse") == "new"
        badge = "🆕 NEW" if new else "♻ reuse"
        col = COLOR.get(st, "#aaa")
        cards.append(
            f'<div class="card"><div class="imgwrap"><img src="{img}" loading="lazy"></div>'
            f'<div class="cap"><span class="n">#{i}</span> <b>{slug}</b> '
            f'<span class="badge" style="background:{col}22;color:{col};border-color:{col}66">{st}</span> '
            f'<span class="reuse">{badge}</span><br>'
            f'<span class="t">{s["t_start"]:.1f}–{s["t_end"]:.1f}s · {s["beat"]} · {s["bible_ref"]}</span><br>'
            f'<span class="line">“{LINE.get(i,"")}”</span></div></div>')
    html = (
        '<!doctype html><html><head><meta charset="utf-8"><title>Father, forgive them — v2 (red-teamed) · 13 stills</title>'
        '<style>body{background:#14110d;color:#f3ead6;font-family:system-ui,Arial;margin:0;padding:24px;max-width:1600px}'
        'h1{font-size:22px;margin:0 0 4px}p.note{color:#a89b7d;font-size:13px;margin:2px 0 18px;line-height:1.5}'
        '.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(240px,1fr));gap:16px}'
        '.card{background:#1e1a13;border:1px solid #3a3226;border-radius:10px;overflow:hidden}'
        '.imgwrap{aspect-ratio:9/16;background:#000}.card img{width:100%;height:100%;object-fit:cover;display:block}'
        '.cap{padding:8px 10px;font-size:12px;line-height:1.45}.n{color:#e8c069;font-weight:bold}.cap b{color:#fff}'
        '.badge{font-size:10px;padding:1px 6px;border-radius:7px;border:1px solid}.reuse{font-size:10px;color:#8a7f66}'
        '.t{color:#b3a681;font-size:11px}.line{color:#c9b892;font-style:italic}</style></head><body>'
        '<h1>“Father, forgive them” (Luke 23:34) — v2 scene plan, red-teamed · 13 stills</h1>'
        '<p class="note">Reading order = narration order (57.15s). '
        '<span style="color:#e8c069">christ</span> · <span style="color:#7fb0d1">context</span> · '
        '<span style="color:#9d7fd1">ot_echo</span> · <span style="color:#7fd18b">human_us</span> · '
        '<span style="color:#d17f9d">symbolic</span>. 6/13 Christ-centric (46%) — passes the subject-variety gate. '
        '🆕 = the 4 new depth stills; ♻ = reused from the approved reshoot.</p>'
        f'<div class="grid">{"".join(cards)}</div></body></html>')
    OUT.write_text(html, encoding="utf-8")
    print("wrote", OUT)


if __name__ == "__main__":
    main()
