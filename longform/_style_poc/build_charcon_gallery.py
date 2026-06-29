"""Build CHARCON.html — CHARACTER-CONSISTENCY + COST review.
One row per model (cheapest->dearest). REF portrait, then P-track (prompt-only) and
R-track (reference-locked) across 5 diverse stress scenes, side by side, so face/marker/
style consistency is eyeball-obvious. Cost badge + my full-res verdict per model.
Scratchpad only."""
from pathlib import Path

HERE = Path(__file__).parent
CC = HERE / "charcon"

COST = {"z_image":0.15, "flux_2":1, "grok_image":1, "nano_banana":1,
        "seedream_v4_5":1, "seedream_v5_lite":1, "nano_banana_flash":1.5}

# model -> accepts --image reference (R track)?
HAS_R = {"z_image":False, "flux_2":True, "grok_image":True, "nano_banana":True,
         "seedream_v4_5":True, "seedream_v5_lite":True, "nano_banana_flash":True}

SCENES = [("noon_close","noon close-up"), ("night_fire","night campfire"),
          ("lamp_room","oil-lamp room"), ("storm_ridge","storm ridge"),
          ("crowd_market","crowd market")]

# my full-res verdict — model -> (tag, note)
VERDICT = {
 "seedream_v4_5":     ("WIN", "STRONG both tracks — same face + scar + gold earring + rust scarf + short black beard across all scenes, consistent inked graphic-novel style, clean anatomy; excellent dynamic full-figure (storm) + crowd. Best overall at 1cr."),
 "nano_banana":       ("WIN", "STRONG both tracks — Gemini ref-lock holds the exact face + all markers across wild scene changes, consistent inked style, clean anatomy. Co-winner at 1cr."),
 "seedream_v5_lite":  ("WIN", "STRONG both tracks — same man + all markers, consistent inked style, excellent full-figure storm; clean. 1cr."),
 "flux_2":            ("WIN", "STRONG both tracks — clean inked comic, same man + markers + style everywhere, no defects. 1cr."),
 "grok_image":        ("GOOD","Identity consistent BOTH tracks, but P-track DRIFTS photoreal on several scenes; R-track (ref-locked) holds the loved inked style. Needs the reference lock. 1cr."),
 "nano_banana_flash": ("GOOD","STRONG identity + style both tracks, great storm full-figure — BUT crowd scene hallucinated signage TEXT (we ask for none), and dearest at 1.5cr."),
 "z_image":           ("FLAG","Cheapest by far (0.15cr) and scenes come back inked + consistent WITH markers — but prompt-only (no ref-lock) and the REF portrait rendered PHOTOREAL, so style is unreliable scene-to-scene. Value pick, not the consistency winner."),
}
COLOR = {"WIN":"#1f7a3d","GOOD":"#3a5","FLAG":"#a86","WEAK":"#955","FAIL":"#a33"}


def cell(name):
    f = CC / name
    return (f'<a href="charcon/{name}" target="_blank"><img src="charcon/{name}"></a>'
            if f.exists() and f.stat().st_size > 0 else '<span class=miss>—</span>')


models = sorted(COST, key=lambda m: COST[m])
rows = []
for m in models:
    v, note = VERDICT.get(m, ("", ""))
    badge = f'<span class=badge style="background:{COLOR.get(v,"#444")}">{v}</span>' if v else ""
    has_r = HAS_R[m]
    # header + REF
    head = (f'<div class=hd><b>{m}</b> <span class=cost>{COST[m]} cr/still</span> {badge}'
            f'<div class=note>{note}</div>'
            f'<figure class=ref>{cell(f"CC__{m}__REF.png")}<figcaption>REF portrait</figcaption></figure>'
            f'</div>')
    # scene grid: each scene = P over R (or P only)
    scols = []
    for slug, lbl in SCENES:
        p = f'<figure>{cell(f"CC__{m}__P_{slug}.png")}<figcaption>P · {lbl}</figcaption></figure>'
        if has_r:
            r = f'<figure>{cell(f"CC__{m}__R_{slug}.png")}<figcaption>R · {lbl}</figcaption></figure>'
        else:
            r = '<figure><span class=miss>no ref-lock</span><figcaption>R · n/a</figcaption></figure>'
        scols.append(f'<div class=scene>{p}{r}</div>')
    rows.append(f'<div class=row>{head}<div class=scenes>{"".join(scols)}</div></div>')

html = f"""<!doctype html><meta charset=utf-8><title>Character-consistency + cost bake-off</title>
<style>
body{{background:#111;color:#eee;font-family:system-ui,Segoe UI,Arial;margin:24px}}
h1{{margin:0 0 4px}} .sub{{color:#9ab;margin:0 0 18px;max-width:980px;line-height:1.45}}
.row{{border-top:1px solid #333;padding:18px 0;display:grid;grid-template-columns:250px 1fr;gap:18px}}
.hd b{{font-size:18px;color:#fff}}
.cost{{display:inline-block;background:#234;color:#bdf;font-size:12px;padding:1px 8px;border-radius:10px;margin-left:6px}}
.badge{{display:inline-block;color:#fff;font-size:11px;font-weight:700;padding:1px 8px;border-radius:10px;margin-left:4px}}
.note{{color:#9ab;font-size:13px;margin:8px 0 10px;line-height:1.45}}
.ref img{{border:2px solid #2a6}}
.scenes{{display:grid;grid-template-columns:repeat(5,1fr);gap:10px}}
.scene{{display:grid;grid-template-rows:1fr 1fr;gap:8px}}
figure{{margin:0}}
img{{width:100%;height:auto;display:block;border-radius:5px}}
figcaption{{font-size:11px;color:#9ab;margin-top:3px}}
.miss{{display:flex;align-items:center;justify-content:center;height:80px;color:#a86;background:#1a1a1a;border-radius:5px;font-size:12px}}
a{{color:#7cf}}
.key{{color:#cd9;font-size:13px;margin:0 0 18px}}
</style>
<h1>Character consistency + cost — one witness, two tracks, 7 models</h1>
<p class=sub>One distinctive witness <b>(Caleb: scar through left eyebrow · gold hoop earring · rust-red headscarf · short black beard)</b>
stress-tested across 5 wildly different scenes. <b>P</b> = prompt-only (text-locked).
<b>R</b> = reference-locked (fed the model's own REF portrait via <code>--image</code>).
Read each scene column TOP (P) vs BOTTOM (R): does the model keep the <b>same man + same markers + the loved inked graphic-novel style</b>?
Cost = exact credits/still ($0 preflight). Click any image for full-res.</p>
<p class=key>Loved style = flat inked biblical graphic-novel (manga composition, dramatic ink shadows) — NOT photoreal drift.</p>
{''.join(rows)}
"""
out = HERE / "CHARCON.html"
out.write_text(html, encoding="utf-8")
print(f"wrote {out}")
