"""Build EW04_stills.html — review gallery for the 5 NEW inked EW04 scene stills
(scenes 6-7 reuse the inked Jesus cross + risen clips). Copies to a clean Desktop
folder for one-click review. POC/scratchpad."""
import shutil
from pathlib import Path

HERE = Path(__file__).parent
STILLS = HERE / "stills"
DEST = Path.home() / "Desktop" / "EW04_stills"
(DEST / "img").mkdir(parents=True, exist_ok=True)

# slug -> (beat label, timecode, caption)  — each beat now has a PAIR (wide + close)
# so each 8-13s beat can hold 2x 5s clips and the cut stays punchy.
SCENES = [
    ("01_hook_moses", "1 — Hook / Moses (wide)", "0:00–0:11",
     "The witness. Aged Moses, firelit, weary knowing eyes, one hand opening to speak."),
    ("01b_moses_close", "1b — Moses (close)", "0:00–0:11",
     "Tight on Moses' half-lit face, eyes on the viewer — the intimate cut into the hook."),
    ("02_judgment_plague", "2 — The plague (single)", "0:11–0:24",
     "Venom of judgment: a man fallen, a live serpent striking, the crowd in shadow."),
    ("02b_serpents_spread", "2b — The plague (wide)", "0:11–0:24",
     "The plague spreading across the whole camp — serpents rearing over the tents, figures fleeing."),
    ("03_bronze_lifted", "3 — The bronze lifted (wide)", "0:24–0:34",
     "Moses lifts the pole — bronze serpent SET UPON the top (not coiled / not a caduceus), above the camp."),
    ("03b_serpent_atop_sky", "3b — The bronze (hero close)", "0:24–0:34",
     "Low-angle hero: the bronze serpent mounted on top, bare shaft below, against the night sky."),
    ("04_look_and_live", "4 — Look and live (wide)", "0:34–0:42",
     "A bitten man turns his eyes UP to the lifted serpent — the empty hand of faith — and life returns."),
    ("04b_face_to_life", "4b — Look and live (close)", "0:34–0:42",
     "Extreme close: an ordinary stricken man (snakebite on the neck) turns his face up — colour returns."),
    ("05_night_teacher", "5 — Night teacher (two-shot)", "0:42–0:51",
     "Jesus to Nicodemus by lamplight: 'As Moses lifted up the serpent... even so must the Son of man be lifted up.'"),
    ("05b_jesus_speaks", "5b — Night teacher (close)", "0:42–0:51",
     "Warm close on Jesus speaking, Nicodemus' grey shoulder in foreground — the line lands."),
]
REUSE = [
    ("The crucifixion", "0:51–1:01", "REUSE — inked Jesus cross clip (lifted up)."),
    ("The risen Christ", "1:01–1:10", "REUSE — inked risen Christ clip (look and live)."),
]

cards = []
for slug, label, tc, cap in SCENES:
    png = STILLS / f"{slug}.png"
    if png.exists():
        shutil.copy2(png, DEST / "img" / png.name)
    cards.append(f"""<section><h2>{label} <span class=tc>{tc}</span></h2><div class=note>{cap}</div>
<a href="img/{png.name}" target="_blank"><img src="img/{png.name}"></a></section>""")
reuse_html = "".join(
    f'<div class=rcard><h3>{lab} <span class=tc>{tc}</span></h3><div class=note>{cap}</div></div>'
    for lab, tc, cap in REUSE)

html = f"""<!doctype html><meta charset=utf-8><title>EW04 Bronze Serpent — inked stills review</title>
<style>
body{{background:#0e0e10;color:#eee;font-family:system-ui,Segoe UI,Arial;margin:28px;max-width:900px}}
h1{{margin:0 0 6px}} .sub{{color:#9ab;margin:0 0 24px;max-width:820px;line-height:1.5}}
section{{margin:0 0 30px;border-top:1px solid #2a2a30;padding-top:16px}}
h2{{margin:0 0 4px;color:#ffd98a;font-size:21px}} .tc{{color:#6f8;font-size:14px;font-weight:600}}
.note{{color:#9ab;font-size:14px;margin:0 0 12px;line-height:1.45}}
img{{width:100%;max-width:520px;border-radius:8px;border:1px solid #333;display:block;background:#000}}
.reuse{{margin-top:30px;border-top:2px solid #3a3a44;padding-top:18px}}
.rcard{{background:#16161c;border:1px dashed #44485a;border-radius:8px;padding:12px 16px;margin:0 0 12px}}
.rcard h3{{margin:0 0 4px;color:#bcd;font-size:16px}}
</style>
<h1>EW04 — Bronze Serpent · inked scene stills</h1>
<p class=sub>The 5 NEW scene stills in the locked <b>inked biblical graphic-novel</b> style, each
anchored to its <code>ref_library</code> card. <b>Doctrine fix applied:</b> the bronze serpent is now
<b>SET UPON the top of the pole</b> (Num 21:8), not coiled around the shaft — no caduceus / occult read.
Scenes 6–7 reuse the inked Jesus cross + risen clips. <b>Click any still for full resolution.</b></p>
{''.join(cards)}
<div class=reuse><h2 style="border:0;color:#bcd">Scenes 6–7 — reused Jesus clips</h2>{reuse_html}</div>
"""
out = DEST / "EW04_stills.html"
out.write_text(html, encoding="utf-8")
print(f"wrote {out}")
