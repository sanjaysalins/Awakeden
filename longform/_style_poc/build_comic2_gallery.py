"""Build COMIC2.html — Wave 1 webtoon MODEL HUNT review.
14 models x 2 subjects, the loved WT flat-webtoon style. Rows = subject, cols = model.
Click any image for full-res. Scratchpad only."""
from pathlib import Path

HERE = Path(__file__).parent
COMIC = HERE / "comic2"
MODELS = ["soul_cinematic", "text2image_soul_v2", "z_image", "kling_omni_image",
          "ms_image", "flux_2", "grok_image", "nano_banana", "seedream_v4_5",
          "seedream_v5_lite", "recraft_v4_1", "nano_banana_flash", "nano_banana_2",
          "cinematic_studio_2_5"]
SUBJECTS = {"christ_face": "Christ-face (reverence gate)",
            "joseph_action": "Joseph hauled to the pit (hands/crowd/text/period)"}

# my full-res verdict per model (one line)
VERDICT = {
 "grok_image":        ("WIN", "clean faithful webtoon, dramatic, good hands, no text/border"),
 "flux_2":            ("WIN", "strong clean webtoon, no defects, minor foot anatomy"),
 "recraft_v4_1":      ("WIN", "bold ligne-claire comic, crisp outlines, distinct + faithful"),
 "seedream_v5_lite":  ("GOOD", "clean anime-webtoon, period-true, slightly young"),
 "soul_cinematic":    ("GOOD", "good webtoon, one floating-hand glitch"),
 "kling_omni_image":  ("GOOD", "soft-anime, decent, gentle"),
 "nano_banana_flash": ("GOOD", "illustrated-bible comic, clean, a touch generic"),
 "ms_image":          ("FLAG", "best style BUT baked-in narrative TEXT + 'BibleScreen' watermark"),
 "seedream_v4_5":     ("FLAG", "clean cel but hallucinated an unrequested background Christ"),
 "nano_banana":       ("FLAG", "good comic but drew a panel border + faux signature"),
 "z_image":           ("FLAG", "clean but anime-leaning, less mature"),
 "nano_banana_2":     ("WEAK", "painterly-realism, drifts off flat-webtoon"),
 "text2image_soul_v2":("FAIL", "photoreal + modern Adidas-stripe / jacket anachronisms"),
 "cinematic_studio_2_5":("FAIL", "fully photoreal — not a comic style at all"),
}
COLOR = {"WIN": "#1f7a3d", "GOOD": "#3a5", "FLAG": "#a86", "WEAK": "#955", "FAIL": "#a33"}

rows = []
for sk, slabel in SUBJECTS.items():
    rows.append(f'<h2 style="margin-top:34px">{slabel}</h2>')
    rows.append('<div class=grid>')
    for m in MODELS:
        f = COMIC / f"WT__{m}__{sk}.png"
        v, note = VERDICT.get(m, ("", ""))
        badge = f'<span class=badge style="background:{COLOR.get(v,"#444")}">{v}</span>' if v else ""
        if f.exists():
            rows.append(
                f'<figure><a href="comic2/{f.name}" target="_blank">'
                f'<img src="comic2/{f.name}"></a>'
                f'<figcaption><b>{m}</b> {badge}<br><span class=note>{note}</span></figcaption></figure>')
        else:
            rows.append(f'<figure class=missing><figcaption><b>{m}</b><br>missing</figcaption></figure>')
    rows.append('</div>')

html = f"""<!doctype html><meta charset=utf-8><title>Webtoon model hunt — Wave 1</title>
<style>
body{{background:#111;color:#eee;font-family:system-ui,Segoe UI,Arial;margin:24px}}
h1{{margin:0 0 4px}} .sub{{color:#9ab;margin:0 0 18px}}
h2{{color:#cde;border-bottom:1px solid #333;padding-bottom:6px}}
.grid{{display:grid;grid-template-columns:repeat(4,1fr);gap:14px}}
figure{{margin:0;background:#1a1a1a;border-radius:6px;padding:8px}}
img{{width:100%;height:auto;display:block;border-radius:4px}}
figcaption{{font-size:13px;color:#cde;margin-top:6px;line-height:1.35}}
.note{{color:#9ab;font-size:12px}}
.badge{{display:inline-block;color:#fff;font-size:11px;font-weight:700;
  padding:1px 7px;border-radius:10px;vertical-align:middle}}
a{{color:#7cf}}
</style>
<h1>Webtoon model hunt — Wave 1 (the loved WT flat-webtoon style)</h1>
<p class=sub>14 image models x 2 stress subjects. My own full-res review verdict on each.
Click any image for full-res. Reverence gate = Christ-face · hands/crowd/text/period = Joseph hauled.</p>
{''.join(rows)}
"""
out = HERE / "COMIC2.html"
out.write_text(html, encoding="utf-8")
print(f"wrote {out}")
