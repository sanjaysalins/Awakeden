"""Simple painted-comic stills gallery for the e2e POC (2026-07-23).
Shows the scenes in story order, big, labelled. One glance = keep/re-roll call.

  .venv\\Scripts\\python.exe longform/EW01_Two_Goats/_build_painted_gallery.py
"""
from pathlib import Path

HERE = Path(__file__).resolve().parent
PAINTED = HERE / "v1" / "visual_16x9_painted"
PLATE20 = HERE / "v1" / "visual_16x9_inked" / "_poc_kinetic_type" / "pc_20_veil_plate.png"
OUT = PAINTED / "_GALLERY.html"

# (id, title, light)
SCENES = [
    (1, "Once a year, only once", "dark"),
    (2, "I laid aside gold and glory", "dark"),
    (3, "Plain white linen, like a servant", "dark"),
    (4, "I went in alone", "dark"),
    (5, "The cloud upon the mercy seat", "dark"),
    (16, "A shadow waits — the body came", "dark→pivot"),
    (17, "By his own blood he entered in once", "warm"),
    (18, "The LORD laid on him the iniquity of us all", "warm"),
    (19, "He suffered without the gate", "warm"),
    (20, "He sat down — the veil rent (POC plate)", "warm"),
]

SLUGS = {1: "01_once_a_year", 2: "02_laid_aside_gold", 3: "03_plain_white_linen",
         4: "04_went_in_alone", 5: "05_cloud_mercy_seat", 16: "16_shadow_body_came",
         17: "17_entered_in_once", 18: "18_iniquity_of_us_all", 19: "19_without_the_gate"}

# status per scene: keep = good / reroll = flaw, fix pending / pending = not rendered yet
STATUS = {1: ("keep", ""), 2: ("reroll", "shown = old (border) — re-rolling"),
          3: ("keep", ""), 4: ("keep", ""), 5: ("keep", ""),
          16: ("pending", "HF 503 — rendering when it clears"),
          17: ("keep", "fixed (column removed)"), 18: ("reroll", "shown = old (too soft) — re-rolling"),
          19: ("reroll", "shown = old (two figures) — re-rolling"), 20: ("keep", "POC plate")}


def main():
    cards = []
    for sid, title, light in SCENES:
        if sid == 20:
            p = PLATE20
        else:
            p = PAINTED / f"{SLUGS[sid]}.png"
        src = p.resolve().as_uri() if p.exists() else ""
        missing = "" if p.exists() else "<div class='miss'>rendering when HF clears…</div>"
        img = f"<img src='{src}' loading='lazy'/>" if src else missing
        st, note = STATUS.get(sid, ("keep", ""))
        badge = {"keep": "✅ keep", "reroll": "🔧 re-rolling", "pending": "⏳ rendering"}[st]
        notehtml = f"<div class='note'>{note}</div>" if note else ""
        cards.append(f"""
        <div class='card {st}'>
          <div class='hd'><span class='num'>#{sid:02d}</span>
            <span class='ti'>{title}</span><span class='lt {light.split('→')[0]}'>{light}</span></div>
          <div class='badge {st}'>{badge}</div>{notehtml}
          {img}
        </div>""")
    html = f"""<!doctype html><meta charset=utf-8>
<title>EW01 painted-comic — stills gallery</title>
<style>
 body{{background:#14110d;color:#f0e9dc;font-family:system-ui,Arial;margin:0;padding:28px}}
 h1{{font-size:22px;margin:0 0 4px}} p.sub{{color:#b7ab97;margin:0 0 22px}}
 .card{{margin:0 0 30px}}
 .hd{{display:flex;align-items:center;gap:12px;margin:0 0 8px}}
 .num{{font-weight:700;color:#e9c877}} .ti{{font-size:18px}}
 .lt{{margin-left:auto;font-size:12px;padding:3px 9px;border-radius:20px}}
 .lt.dark{{background:#2a2620;color:#c9bfa9}} .lt.warm{{background:#4a361a;color:#f4d79a}}
 img{{width:100%;border-radius:8px;display:block;box-shadow:0 6px 24px rgba(0,0,0,.5)}}
 .miss{{padding:60px;text-align:center;background:#221e18;border-radius:8px;color:#8a7f6c}}
 .badge{{display:inline-block;font-size:13px;font-weight:700;padding:3px 10px;border-radius:6px;margin:0 0 6px}}
 .badge.keep{{background:#1f3a24;color:#8fe0a3}} .badge.reroll{{background:#4a3410;color:#f0c25a}}
 .badge.pending{{background:#2a2620;color:#b7ab97}}
 .note{{font-size:13px;color:#c9a34a;margin:0 0 8px}}
 .card.reroll img{{opacity:.55;filter:saturate(.8)}}
</style>
<h1>EW01 · painted-comic e2e POC — 10 stills</h1>
<p class='sub'>Story order. Dark law era (1–5,16) → warm Christ (17–20). Kinetic scripture type lands on 5,17,18,20.</p>
{''.join(cards)}
"""
    OUT.write_text(html, encoding="utf-8")
    print(f"[gallery] {OUT}")
    print(f"file:///{str(OUT).replace(chr(92), '/')}")


if __name__ == "__main__":
    main()
