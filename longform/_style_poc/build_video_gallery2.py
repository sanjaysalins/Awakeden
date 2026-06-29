"""Build VIDEO2.html — i2v Pass-2 stress-test review GRID.
Rows = the 5 hard stills, columns = the 3 finalist models. Each cell: embedded
<video> + 6-frame filmstrip (start->end). Extracts strips via ffmpeg (fps=6/dur),
copies everything to a clean Desktop folder so the link opens in one click.
Verdicts filled in after my full-res review. POC/scratchpad only."""
import json, shutil, subprocess
from pathlib import Path

HERE = Path(__file__).parent
CLIPS = HERE / "bakeoff_v2"
STRIPS = CLIPS / "strips"
STRIPS.mkdir(parents=True, exist_ok=True)
SRCDIR = HERE / "charcon"
DEST = Path.home() / "Desktop" / "VIDEO_bakeoff2"
(DEST / "clips").mkdir(parents=True, exist_ok=True)
(DEST / "strips").mkdir(parents=True, exist_ok=True)
(DEST / "stills").mkdir(parents=True, exist_ok=True)

WINGET = Path.home() / "AppData/Local/Microsoft/WinGet/Links"
FFMPEG = str(WINGET / "ffmpeg.exe")
FFPROBE = str(WINGET / "ffprobe.exe")

MODELS = ["seedance1_5", "cinematic_studio_video_v2", "minimax_hailuo"]
COST = {"seedance1_5": 4.8, "cinematic_studio_video_v2": 7.5, "minimax_hailuo": 6}
STILLS = ["crowd_market", "night_fire", "lamp_room", "noon_close", "walking"]
STILL_LABEL = {
    "crowd_market": "Crowd / multi-figure (other faces morph?)",
    "night_fire": "Firelight flicker (dynamic light)",
    "lamp_room": "Low-light + held clay cup (object stability)",
    "noon_close": "Quiet close-up (subtle micro-motion)",
    "walking": "Walking (locomotion → body morph?)",
}

# verdict per cell key f"{model}__{slug}" -> (tag, note). My full-res filmstrip review.
VERDICT = {
 "seedance1_5__crowd_market": ("WIN", "Smooth push-in; face + markers hold, background crowd faces stay coherent (no melt). Inked throughout."),
 "seedance1_5__night_fire": ("WIN", "Flame flickers, embers rise tastefully (not glitter), face steady, style inked."),
 "seedance1_5__lamp_room": ("WIN", "Lamp flickers, clay cup held stable (no melt), clean push-in, markers held."),
 "seedance1_5__noon_close": ("WIN", "Lovely micro push-in, eyes alive, sweat glistens, face rock-solid. Inked."),
 "seedance1_5__walking": ("WIN", "ONLY model with a true WALK CYCLE — natural gait, no morph, style holds. Best for locomotion + cheapest."),
 "cinematic_studio_video_v2__crowd_market": ("WIN", "BEST crowd: background faces stay rock-stable through the push-in. Caleb + markers held. Inked."),
 "cinematic_studio_video_v2__night_fire": ("WIN", "Beautiful — flame flickers, embers + smoke drift, warm light plays on the face; reverent, no morph."),
 "cinematic_studio_video_v2__lamp_room": ("WIN", "Cup held dead steady, lamp flickers, face locked. Best object stability."),
 "cinematic_studio_video_v2__noon_close": ("WIN", "A sweat bead rolls down the cheek — subtle, reverent; eyes shift, face holds."),
 "cinematic_studio_video_v2__walking": ("WIN", "Dynamic walk + dust kick + billowing scarf; face holds. Most 'directed' cinematic motion."),
 "minimax_hailuo__crowd_market": ("WIN", "Gentle push-in, background faces stable, Caleb steady. Subtle, clean."),
 "minimax_hailuo__night_fire": ("WIN", "Strong fire flicker, face dead-steady, style inked. Reverent."),
 "minimax_hailuo__lamp_room": ("WIN", "Cup steady, lamp flickers, subtle breathing/head motion. Holds."),
 "minimax_hailuo__noon_close": ("WIN", "Subtle micro-motion, eyes shift, face solid. Faint warmth, stays inked."),
 "minimax_hailuo__walking": ("WIN", "Most ALIVE cloth — scarf flows dramatically + push-in; natural stride, no morph."),
}
COLOR = {"WIN": "#1f7a3d", "GOOD": "#3a5", "FLAG": "#a86", "WEAK": "#955", "FAIL": "#a33", "": "#444"}


def dur(clip):
    try:
        r = subprocess.run([FFPROBE, "-v", "error", "-show_entries", "format=duration",
                            "-of", "default=nw=1:nk=1", str(clip)],
                           capture_output=True, text=True, timeout=60)
        return float(r.stdout.strip())
    except Exception:
        return 5.0


def make_strip(clip, strip):
    if strip.exists() and strip.stat().st_size > 0:
        return True
    d = max(dur(clip), 0.1)
    fps = 6.0 / d * 0.999
    r = subprocess.run([FFMPEG, "-y", "-i", str(clip), "-vf",
                        f"fps={fps:.5f},scale=300:-1,tile=6x1", "-frames:v", "1", str(strip)],
                       capture_output=True, text=True, timeout=120)
    return strip.exists()


# copy stills + build strips + copy media
for slug in STILLS:
    s = SRCDIR / f"CC__seedream_v4_5__R_{slug}.png"
    if s.exists():
        shutil.copy2(s, DEST / "stills" / f"{slug}.png")
for slug in STILLS:
    for m in MODELS:
        clip = CLIPS / f"V__{m}__{slug}.mp4"
        if clip.exists() and clip.stat().st_size > 0:
            shutil.copy2(clip, DEST / "clips" / clip.name)
            strip = STRIPS / f"V__{m}__{slug}.strip.png"
            if make_strip(clip, strip):
                shutil.copy2(strip, DEST / "strips" / strip.name)

# build grid
head_cells = "".join(f'<th>{m}<br><span class=cost>{COST[m]} cr</span></th>' for m in MODELS)
body = []
for slug in STILLS:
    cells = [f'<td class=stillcell><div class=lbl>{STILL_LABEL[slug]}</div>'
             f'<img src="stills/{slug}.png"></td>']
    for m in MODELS:
        key = f"{m}__{slug}"
        v, note = VERDICT.get(key, ("", ""))
        badge = f'<span class=badge style="background:{COLOR[v]}">{v}</span>' if v else ""
        clip = DEST / "clips" / f"V__{m}__{slug}.mp4"
        strip = DEST / "strips" / f"V__{m}__{slug}.strip.png"
        vid = (f'<video controls preload=metadata src="clips/V__{m}__{slug}.mp4"></video>'
               if clip.exists() else '<span class=miss>no clip</span>')
        strp = (f'<a href="strips/V__{m}__{slug}.strip.png" target="_blank">'
                f'<img class=strip src="strips/V__{m}__{slug}.strip.png"></a>'
                if strip.exists() else '')
        cells.append(f'<td>{badge}{vid}{strp}<div class=note>{note}</div></td>')
    body.append("<tr>" + "".join(cells) + "</tr>")

html = f"""<!doctype html><meta charset=utf-8><title>i2v Pass 2 — stress test</title>
<style>
body{{background:#111;color:#eee;font-family:system-ui,Segoe UI,Arial;margin:24px}}
h1{{margin:0 0 4px}} .sub{{color:#9ab;margin:0 0 16px;max-width:1100px;line-height:1.45}}
table{{border-collapse:collapse;width:100%}}
th,td{{border:1px solid #333;padding:10px;vertical-align:top;text-align:center}}
th{{background:#1a2233;color:#fff;font-size:15px}}
.cost{{display:inline-block;background:#234;color:#bdf;font-size:12px;padding:1px 8px;border-radius:10px}}
.stillcell{{width:220px;background:#161616}}
.stillcell img{{width:200px;border-radius:6px}}
.lbl{{color:#cd9;font-size:12px;margin-bottom:6px;line-height:1.35}}
video{{width:240px;border-radius:6px;background:#000;display:block;margin:0 auto 6px}}
.strip{{width:240px;border-radius:5px;display:block;margin:0 auto}}
.badge{{display:inline-block;color:#fff;font-size:11px;font-weight:700;padding:1px 8px;border-radius:10px;margin-bottom:6px}}
.note{{color:#9ab;font-size:12px;margin-top:6px;line-height:1.4;text-align:left}}
.miss{{display:block;color:#a86;font-size:13px;padding:30px 0}}
a{{color:#7cf}}
</style>
<h1>Image-to-video Pass 2 &mdash; consistency + hard-motion stress test</h1>
<p class=sub>The 3 Pass-1 finalist video models (<b>seedance1_5</b> 4.8cr, <b>cinematic_studio_video_v2</b> 7.5cr,
<b>minimax_hailuo</b> 6cr) animating the <b>5 hardest stills</b> &mdash; multi-figure crowd, firelight,
low-light held object, quiet close-up, and walking locomotion. The test: which model holds the
<b>inked graphic-novel style + the same face/markers</b> across DIFFERENT images and hard motion,
with no morph / photoreal-softening / invented elements?<br>
Each cell: play the <b>video</b>, or scan the <b>6-frame filmstrip</b> (start&rarr;end) below it. Click a strip for full-res.</p>
<table><tr><th>Stress still</th>{head_cells}</tr>
{''.join(body)}
</table>
"""
out = DEST / "VIDEO2.html"
out.write_text(html, encoding="utf-8")
print(f"wrote {out}")
