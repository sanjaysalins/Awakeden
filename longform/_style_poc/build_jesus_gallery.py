"""Build JESUS.html — the Jesus hero-still review gallery (the crucial test:
Jesus appears in nearly every clip, so the face must lock across every moment).
One canonical REF portrait + the keeper stills grouped by moment, each full-res
clickable. Copies everything to a clean Desktop folder so the link opens in one click.
POC/scratchpad only."""
import shutil
from pathlib import Path

HERE = Path(__file__).parent
SRC = HERE / "jesus"
DEST = Path.home() / "Desktop" / "JESUS_stills"
(DEST / "img").mkdir(parents=True, exist_ok=True)

# moment -> (label, [variant files], note)
MOMENTS = [
    ("GRID", "Reference GRID — face + body (the NEW anchor)",
     ["JESUS__GRID.png"], "The fix for the scaling issues: face AND full standing body in one anchor, so the model inherits both the face and the correct proportions (head about 1/7 of height) instead of inventing them per scene."),
    ("REF", "Canonical reference portrait (the face)",
     ["JESUS__REF.png"], "The original face portrait. Folded into the left panel of the grid above."),
    ("baptism", "Baptism in the Jordan",
     ["JESUS__baptism__a.png", "JESUS__baptism__b.png"],
     "Hero-reframed: Jesus dominant + large, John small/secondary, dove + shaft of light. (No camel — earlier drafts leaked a literal camel and made him co-equal with John.)"),
    ("crowd", "In the press of the crowd",
     ["JESUS__crowd__a.png", "JESUS__crowd__b.png"],
     "Compassionate among the sick + poor. Background crowd faces stay coherent (no melt). b lays his hand on the sick."),
    ("scourged", "Scourged before the soldiers",
     ["JESUS__scourged__a.png", "JESUS__scourged__b.png"],
     "Hero-reframed: Jesus large + central + dominant, the Roman soldiers small/secondary in the background (no longer towering over him). Restrained + reverent — no gore."),
    ("cross", "The crucifixion",
     ["JESUS__cross__b.png"],
     "Nailed wrists, loincloth, head bowed, broken-gold storm sky. Reverent, no gore. (Only one framing kept — the wide framing kept drifting to roped/robed or a spike-studded cross.)"),
    ("risen", "The risen Christ",
     ["JESUS__risen__b.png"],
     "Glorified hero, radiant, pierced hands lifted with nail-scars. (Wide variant 'a' dropped — its golden glow kept rendering soft glossy-anime instead of bold inked.)"),
]

cards = []
for slug, label, files, note in MOMENTS:
    files = [f for f in files if (SRC / f).exists()]
    for f in files:
        shutil.copy2(SRC / f, DEST / "img" / f)
    imgs = "".join(
        f'<a href="img/{f}" target="_blank"><img src="img/{f}">'
        f'<div class=vk>{f.split("__")[-1].replace(".png","").upper() if "__" in f else "REF"}</div></a>'
        for f in files)
    cards.append(
        f'<section><h2>{label}</h2><div class=note>{note}</div>'
        f'<div class=row>{imgs}</div></section>')

html = f"""<!doctype html><meta charset=utf-8><title>Jesus hero stills — review</title>
<style>
body{{background:#0e0e10;color:#eee;font-family:system-ui,Segoe UI,Arial;margin:28px;max-width:1500px}}
h1{{margin:0 0 6px}} .sub{{color:#9ab;margin:0 0 24px;max-width:1000px;line-height:1.5}}
section{{margin:0 0 34px;border-top:1px solid #2a2a30;padding-top:18px}}
h2{{margin:0 0 4px;color:#ffd98a;font-size:20px}}
.note{{color:#9ab;font-size:14px;margin:0 0 12px;line-height:1.45;max-width:1100px}}
.row{{display:flex;gap:16px;flex-wrap:wrap}}
.row a{{position:relative;display:block}}
.row img{{height:460px;border-radius:8px;border:1px solid #333;display:block}}
.vk{{position:absolute;left:8px;top:8px;background:#000a;color:#fff;font-size:12px;
     font-weight:700;padding:2px 9px;border-radius:9px}}
</style>
<h1>Jesus hero stills &mdash; the crucial face-lock test</h1>
<p class=sub>Jesus is in nearly every clip, so one canonical face must hold across every moment.
One <b>REF</b> portrait, then each hero moment rendered <b>reference-locked</b> to it (inked
biblical graphic-novel style, seedream_v4_5, 9:16). <b>Click any image for full resolution.</b>
Reviewed at full res &mdash; reverent, period-accurate, face holds throughout. Nothing animated yet.</p>
{''.join(cards)}
"""
out = DEST / "JESUS.html"
out.write_text(html, encoding="utf-8")
print(f"wrote {out}")
