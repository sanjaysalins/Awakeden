"""Build VIDEO.html — IMAGE-TO-VIDEO bake-off review.
One row per model (cheapest->dearest): embedded <video> + 6-frame filmstrip +
cost/duration badge + my full-res verdict. Copies clips+strips to a clean Desktop
folder so the link opens in one click. Scratchpad only."""
import shutil
from pathlib import Path

HERE = Path(__file__).parent
SRC_CLIPS = HERE / "bakeoff_v"
SRC_STRIPS = SRC_CLIPS / "strips"
DEST = Path.home() / "Desktop" / "VIDEO_bakeoff"
(DEST / "clips").mkdir(parents=True, exist_ok=True)
(DEST / "strips").mkdir(parents=True, exist_ok=True)
SRC_STILL = HERE / "charcon" / "CC__seedream_v4_5__R_storm_ridge.png"

# exact credits/clip ($0 preflight, credits_exact) + rendered duration (s)
COST = {
 "seedance1_5":4.8, "veo3_1_lite":6, "minimax_hailuo":6, "cinematic_studio_video_v2":7.5,
 "grok_video":7.5, "kling3_0_turbo":7.5, "wan2_7":7.5, "cinematic_studio_video":8,
 "kling2_6":10, "kling3_0":12.5, "seedance_2_0_mini":12.5, "wan2_6":13, "veo3_1":16.5,
 "veo3":22, "grok_video_v15":22.5, "seedance_2_0":22.5, "cinematic_studio_3_0":25,
 "cinematic_studio_video_3_5":25,
}
DUR = {
 "seedance1_5":4.05, "veo3_1_lite":6.0, "minimax_hailuo":5.875, "cinematic_studio_video_v2":5.04,
 "grok_video":5.04, "kling3_0_turbo":5.04, "wan2_7":5.04, "cinematic_studio_video":5.04,
 "kling2_6":5.04, "kling3_0":5.04, "seedance_2_0_mini":5.09, "wan2_6":5.01, "veo3_1":6.02,
 "veo3":8.0, "grok_video_v15":5.04, "seedance_2_0":5.06, "cinematic_studio_3_0":5.04,
}

# my full-res verdict — model -> (tag, note). Judges: inked-style survival, face/marker
# fidelity (scar/earring/scarf/beard), hallucination, mouth-melt (shout drift), motion.
VERDICT = {
 "cinematic_studio_video_v2": ("WIN", "BEST VALUE. Holds the inked graphic-novel style perfectly through a clean push-in; the shouting mouth STAYS open, scar+earring+rust scarf all held, scarf whips in the wind, lightning flickers. Faithful, no morph, no photoreal drift. 7.5cr."),
 "minimax_hailuo":            ("WIN", "Most ALIVE motion. Style stays inked, dramatic scarf/cloth whip in the storm wind, shout held, full figure stable, lightning flickers — reverent and faithful, zero morph. Cheap at 6cr."),
 "kling3_0":                  ("WIN", "Cleanest faithful push-in — inked line art fully survives, mouth stays shouting, all markers held, no invented elements. The premium-clean pick. 12.5cr (pro)."),
 "seedance_2_0_mini":         ("WIN", "Pushes to extreme close-up and the SHOUT survives the whole way; style stays inked, scar+earring held, sweat/rain reads natural. Strong. 12.5cr."),
 "kling3_0_turbo":            ("GOOD","Cheaper Kling — holds the inked style + shout + markers through the push-in, very slight render-up on the closest frame. Strong budget Kling. 7.5cr."),
 "veo3_1_lite":               ("GOOD","Holds inked style + shout cleanly across 6s, scarf+lightning motion good; faint photoreal warmth on the close frames. Great cheap 6s option. 6cr."),
 "cinematic_studio_video":    ("GOOD","Solid — inked style + shout held through an extreme push-in, slightly more rendered on the closest frame. 8cr."),
 "kling2_6":                  ("GOOD","Faithful inked push-in, mouth stays shouting, markers held; a touch softer than kling3_0. 10cr."),
 "seedance_2_0":              ("GOOD","Inked style + shout held, good cloth motion — but no real gain over seedance_2_0_mini at nearly 2x the price. 22.5cr."),
 "veo3_1":                    ("GOOD","Holds inked style + shout across 6s, clean motion; faint photoreal warmth on close. Pricey. 16.5cr."),
 "cinematic_studio_3_0":      ("GOOD","Inked style + shout held through extreme close, slight painterly render-up; no edge over v2 at 3x+ the cost. 25cr."),
 "seedance1_5":               ("FLAG","Cheapest (4.8cr) and holds the inked style + shout — but adds slight body LOCOMOTION (he shifts/strides) we didn't ask for; fine if you want a touch more body."),
 "grok_video":                ("FLAG","Style stays inked + shout held, but the arms BEEF UP / render harder than the still and motion is a bit generic. 7.5cr."),
 "veo3":                      ("FLAG","Pushes to extreme close-up and SOFTENS toward photoreal — line art thins, mouth half-closes by the end. 8s but drifts off-style. 22cr."),
 "wan2_7":                    ("FLAG","Holds style early but INVENTS a head-turn to profile mid-clip — the shout closes and he looks away. Pose/expression drift. 7.5cr."),
 "wan2_6":                    ("FLAG","Style holds but the SHOUT MELTS to a calm upward gaze by the end — expression drifts off the beat. 13cr."),
 "grok_video_v15":            ("WEAK","Mouth MELT — opens shouting then closes to a somber/tearful calm, expression breaks the beat; and dearest-tier at 22.5cr. Avoid."),
 "cinematic_studio_video_3_5":("FAIL","Did not render — server-side 'IP check not finished for input media' (failed twice). Long-form 15s model, 25cr. N/A this round."),
}
COLOR = {"WIN":"#1f7a3d","GOOD":"#3a5","FLAG":"#a86","WEAK":"#955","FAIL":"#a33"}


def copy_media():
    for m in COST:
        clip = SRC_CLIPS / f"V__{m}.mp4"
        if clip.exists():
            shutil.copy2(clip, DEST / "clips" / clip.name)
        strip = SRC_STRIPS / f"V__{m}.strip.png"
        if strip.exists():
            shutil.copy2(strip, DEST / "strips" / strip.name)
    if SRC_STILL.exists():
        shutil.copy2(SRC_STILL, DEST / "source_still.png")


copy_media()
models = sorted(COST, key=lambda m: COST[m])
rows = []
for m in models:
    v, note = VERDICT.get(m, ("", ""))
    badge = f'<span class=badge style="background:{COLOR.get(v,"#444")}">{v}</span>'
    dur = DUR.get(m)
    durtxt = f"{dur:.1f}s" if dur else "—"
    clip = DEST / "clips" / f"V__{m}.mp4"
    strip = DEST / "strips" / f"V__{m}.strip.png"
    vid = (f'<video controls preload=metadata src="clips/V__{m}.mp4"></video>'
           if clip.exists() else '<span class=miss>no clip</span>')
    strp = (f'<a href="strips/V__{m}.strip.png" target="_blank"><img src="strips/V__{m}.strip.png"></a>'
            if strip.exists() else '<span class=miss>no strip</span>')
    head = (f'<div class=hd><b>{m}</b> <span class=cost>{COST[m]} cr</span>'
            f'<span class=dur>{durtxt}</span> {badge}<div class=note>{note}</div></div>')
    rows.append(f'<div class=row>{head}<div class=media><div class=vid>{vid}</div>'
                f'<figure class=strip>{strp}<figcaption>6-frame filmstrip (start &rarr; end)</figcaption></figure></div></div>')

html = f"""<!doctype html><meta charset=utf-8><title>Image-to-video bake-off</title>
<style>
body{{background:#111;color:#eee;font-family:system-ui,Segoe UI,Arial;margin:24px}}
h1{{margin:0 0 4px}} .sub{{color:#9ab;margin:0 0 14px;max-width:1000px;line-height:1.45}}
.src{{display:flex;gap:16px;align-items:flex-start;border:1px solid #2a6;border-radius:8px;padding:12px;margin:0 0 18px;max-width:1000px}}
.src img{{width:170px;border-radius:6px}}
.src .t{{color:#9ab;font-size:13px;line-height:1.5}}
.row{{border-top:1px solid #333;padding:18px 0;display:grid;grid-template-columns:280px 1fr;gap:20px}}
.hd b{{font-size:18px;color:#fff}}
.cost{{display:inline-block;background:#234;color:#bdf;font-size:12px;padding:1px 8px;border-radius:10px;margin-left:6px}}
.dur{{display:inline-block;background:#333;color:#ccc;font-size:12px;padding:1px 8px;border-radius:10px;margin-left:4px}}
.badge{{display:inline-block;color:#fff;font-size:11px;font-weight:700;padding:1px 8px;border-radius:10px;margin-left:4px}}
.note{{color:#9ab;font-size:13px;margin:8px 0 0;line-height:1.5}}
.media{{display:grid;grid-template-columns:300px 1fr;gap:16px;align-items:start}}
.vid video{{width:300px;border-radius:6px;background:#000}}
.strip img{{width:100%;height:auto;display:block;border-radius:5px}}
figcaption{{font-size:11px;color:#9ab;margin-top:4px}}
.miss{{display:flex;align-items:center;justify-content:center;height:120px;color:#a86;background:#1a1a1a;border-radius:6px;font-size:13px}}
a{{color:#7cf}}
.key{{color:#cd9;font-size:13px;margin:0 0 8px}}
</style>
<h1>Image-to-video bake-off &mdash; one still, one motion prompt, every HF i2v model</h1>
<p class=sub>The <b>seedream_v4_5</b> winning still (a shouting Hebrew witness on a storm ridge) animated by
<b>17 of HF's 18 generative image-to-video models</b> with one held motion prompt (rain, whipping scarf,
distant lightning, slow push-in). The test: which model adds motion while keeping the <b>inked
graphic-novel style</b>, the <b>same face + markers</b> (scar / gold earring / rust scarf / black beard),
and the <b>shouting beat</b> &mdash; with no photoreal-softening, morphing, or invented elements?</p>
<div class=src><img src="source_still.png"><div class=t><b>Source still</b> &mdash; seedream_v4_5, 1cr.<br>
Watch each <b>video</b> on the left; the <b>filmstrip</b> on the right shows start&rarr;end at a glance
(spot mouth-melt / style-drift / invented motion without playing).<br>Sorted cheapest&rarr;dearest.
Click a filmstrip for full-res.</div></div>
<p class=key>WIN = motion + style + beat all held &nbsp;|&nbsp; GOOD = solid, minor softening &nbsp;|&nbsp;
FLAG = real drift (pose/expression/photoreal) &nbsp;|&nbsp; WEAK = breaks the beat &nbsp;|&nbsp; FAIL = didn't render</p>
{''.join(rows)}
"""
out = DEST / "VIDEO.html"
out.write_text(html, encoding="utf-8")
print(f"wrote {out}")
