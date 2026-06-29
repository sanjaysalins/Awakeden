"""Build MOSES.html — CONSISTENCY + COST review.
One row per model (sorted cheapest->dearest): prompt A (bush) | prompt B (staff)
side by side, so style+character consistency across the two prompts is eyeball-obvious.
Cost badge per model. My full-res verdict per model. Scratchpad only."""
from pathlib import Path

HERE = Path(__file__).parent
MOS = HERE / "moses"

# exact per-still cost (cr) from $0 preflight (credits_exact)
COST = {"soul_cinematic":0.12,"text2image_soul_v2":0.12,"soul_cast":0.12,
        "cinematic_studio_soul_cast":0.12,"soul_cinema_studio":0.12,"soul_location":0.12,
        "cinematic_studio_soul_location":0.12,"z_image":0.15,"kling_omni_image":0.5,
        "ms_image":0.5,"flux_2":1,"grok_image":1,"nano_banana":1,"seedream_v4_5":1,
        "seedream_v5_lite":1,"recraft_v4_1":1.25,"flux_kontext":1.5,"nano_banana_flash":1.5,
        "nano_banana_2":2,"cinematic_studio_2_5":2,"openai_hazel":4,"gpt_image_2":7}

# my full-res consistency verdict — model -> (tag, note). Tag judges SAME MAN + SAME STYLE across A vs B.
VERDICT = {
 "soul_location":      ("WIN", "bold inked COLOUR comic, same grizzled grey Moses + same dramatic ink-shadow style across both — gorgeous AND 0.12cr, the new value champion"),
 "cinematic_studio_soul_location": ("WIN", "striking B&W MANGA ink (Vagabond/Inoue feel), same man + same monochrome style both beats — a distinct lane, also 0.12cr"),
 "openai_hazel":       ("WIN", "rich inked graphic-novel plates, same grizzled man + same vintage-comic style both beats — beautiful and consistent, but 4cr/still"),
 "z_image":            ("WIN", "true graphic-novel ink, SAME grizzled grey Moses + same style across both — the cheapest genuinely-good option, standout value"),
 "seedream_v4_5":      ("WIN", "same fur-collared grey Moses + same manga ink across both beats — among the most consistent in the field"),
 "seedream_v5_lite":   ("WIN", "same grey Moses + same dramatic colour-comic across both, clean and faithful"),
 "flux_2":             ("WIN", "clean biblical-epic comic ink, same Moses, same style, no defects"),
 "grok_image":         ("WIN", "bold inked comic, same man, dramatic, very consistent A->B"),
 "recraft_v4_1":       ("WIN", "bold ligne-claire ink, same man, crisp outlines, very consistent"),
 "kling_omni_image":   ("GOOD", "both comic, same grey man — A inkier / B a touch more painterly"),
 "nano_banana":        ("GOOD", "same man + style BUT B drew a faint panel border (minor)"),
 "nano_banana_flash":  ("GOOD", "illustrated-bible comic, same man + style, slightly generic"),
 "soul_cinema_studio": ("FLAG", "stunning comic art, but A (modern colour-comic ink) vs B (vintage plate) drift apart + faux signature/printed border — gorgeous, not clean"),
 "flux_kontext":       ("FLAG", "A is bold comic ink, but B drifts to painterly digital realism — style breaks across the pair"),
 "soul_cinematic":     ("FLAG", "comic ink in both, but A vs B read as different men — style family holds, character drifts (cheapest, but)"),
 "nano_banana_2":      ("WEAK", "painterly-realism, drifts off the loved flat graphic-novel look"),
 "ms_image":           ("FAIL", "renders advertisements with baked-in branding / text overlays — unusable"),
 "soul_cast":          ("FAIL", "outputs a photoreal 3-panel character TURNAROUND sheet (front/back/closeup), not a styled scene — wrong format"),
 "cinematic_studio_soul_cast": ("FAIL", "same photoreal turnaround triptych — character-design tool, not a scene renderer"),
 "text2image_soul_v2": ("FAIL", "both photoreal, not a comic style at all"),
 "cinematic_studio_2_5":("FAIL", "photoreal cinematic, not a comic style"),
 "gpt_image_2":        ("FAIL", "A is gorgeous inked comic but B drifts fully PHOTOREAL — style breaks across the pair, and 7cr/still is cost-prohibitive"),
}
COLOR = {"WIN":"#1f7a3d","GOOD":"#3a5","FLAG":"#a86","WEAK":"#955","FAIL":"#a33"}

models = sorted(COST, key=lambda m: COST[m])
rows = []
for m in models:
    a = MOS / f"MS__{m}__A_bush.png"
    b = MOS / f"MS__{m}__B_staff.png"
    v, note = VERDICT.get(m, ("", ""))
    badge = f'<span class=badge style="background:{COLOR.get(v,"#444")}">{v}</span>' if v else ""
    def cell(f):
        return (f'<a href="moses/{f.name}" target="_blank"><img src="moses/{f.name}"></a>'
                if f.exists() else '<span style="color:#a33">missing</span>')
    rows.append(
        f'<div class=row><div class=hd><b>{m}</b> '
        f'<span class=cost>{COST[m]} cr/still</span> {badge}'
        f'<div class=note>{note}</div></div>'
        f'<div class=pair><figure>{cell(a)}<figcaption>A — burning bush</figcaption></figure>'
        f'<figure>{cell(b)}<figcaption>B — staff over desert</figcaption></figure></div></div>')

html = f"""<!doctype html><meta charset=utf-8><title>Moses consistency + cost bake-off</title>
<style>
body{{background:#111;color:#eee;font-family:system-ui,Segoe UI,Arial;margin:24px}}
h1{{margin:0 0 4px}} .sub{{color:#9ab;margin:0 0 18px;max-width:900px;line-height:1.4}}
.row{{border-top:1px solid #333;padding:16px 0;display:grid;grid-template-columns:230px 1fr;gap:18px}}
.hd b{{font-size:17px;color:#fff}}
.cost{{display:inline-block;background:#234;color:#bdf;font-size:12px;padding:1px 8px;border-radius:10px;margin-left:6px}}
.badge{{display:inline-block;color:#fff;font-size:11px;font-weight:700;padding:1px 8px;border-radius:10px;margin-left:4px}}
.note{{color:#9ab;font-size:13px;margin-top:8px;line-height:1.4}}
.pair{{display:grid;grid-template-columns:1fr 1fr;gap:14px}}
figure{{margin:0}}
img{{width:100%;height:auto;display:block;border-radius:5px}}
figcaption{{font-size:12px;color:#9ab;margin-top:4px}}
a{{color:#7cf}}
</style>
<h1>Moses — consistency + cost bake-off (biblical-epic graphic-novel style)</h1>
<p class=sub>Same Moses, same style language, two different beats, run across ALL 22 HF
generative text-to-image models (EXHAUSTIVE). Read each row LEFT vs RIGHT: does the model keep the
<b>same man + same art style</b> across two prompts? That is the consistency test for an
episode. Cost = exact credits/still ($0 preflight). Click any image for full-res.</p>
{''.join(rows)}
"""
out = HERE / "MOSES.html"
out.write_text(html, encoding="utf-8")
print(f"wrote {out}")
