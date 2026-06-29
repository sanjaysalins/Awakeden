"""Build JESUS_CLIPS.html — the animated-clip review gallery for the 8 approved
hero stills (i2v on cinematic_studio_video_v2). Each moment shows its still next to
its looping clip so the face-lock + motion can be judged together. Copies everything
to a clean Desktop folder so the link opens in one click. POC/scratchpad only."""
import shutil
from pathlib import Path

HERE = Path(__file__).parent
STILLS = HERE / "jesus"
CLIPS = HERE / "anim_jesus"
DEST = Path.home() / "Desktop" / "JESUS_clips"
(DEST / "img").mkdir(parents=True, exist_ok=True)
(DEST / "vid").mkdir(parents=True, exist_ok=True)

# slug -> (label, motion note)
MOMENTS = [
    ("baptism__a", "Baptism in the Jordan (wide)",
     "River ripples, dove of light drifts down, slow reverent push-in. Face + John (small/secondary) hold."),
    ("baptism__b", "Baptism (close)",
     "Water drips down his face, head bowed, dove hovers, micro push-in."),
    ("crowd__a", "In the press of the crowd",
     "Villagers shift and reach, dust stirs, slow push-in on his calm dominant face. Crowd faces stay coherent."),
    ("crowd__b", "Laying his hand on the sick",
     "Hand rests steady on the kneeling man, dust drifts, gentle push-in."),
    ("scourged__a", "Bound before the soldiers (wide)",
     "Shadows shift across the courtyard, soldiers stand still, very slow reverent push-in."),
    ("scourged__b", "Bound (close)",
     "Sweat and shadow shift across face + shoulders, intense face holds, micro push-in."),
    ("cross__b", "The crucifixion",
     "Storm clouds drift, broken-gold shafts shift, head fallen forward, slow low-angle push-in."),
    ("risen__b", "The risen Christ",
     "Radiant robe flows, golden resurrection light pulses, lifted hands steady, majestic push-in."),
]

cards = []
for slug, label, note in MOMENTS:
    png = STILLS / f"JESUS__{slug}.png"
    mp4 = CLIPS / f"JESUS__{slug}.mp4"
    if png.exists():
        shutil.copy2(png, DEST / "img" / png.name)
    if mp4.exists():
        shutil.copy2(mp4, DEST / "vid" / mp4.name)
    cards.append(f"""<section><h2>{label}</h2><div class=note>{note}</div>
<div class=row>
  <a href="img/{png.name}" target="_blank"><img src="img/{png.name}"><div class=vk>STILL</div></a>
  <div class=vwrap><video src="vid/{mp4.name}" autoplay loop muted playsinline></video><div class=vk>CLIP</div></div>
</div></section>""")

html = f"""<!doctype html><meta charset=utf-8><title>Jesus hero clips &mdash; review</title>
<style>
body{{background:#0e0e10;color:#eee;font-family:system-ui,Segoe UI,Arial;margin:28px;max-width:1500px}}
h1{{margin:0 0 6px}} .sub{{color:#9ab;margin:0 0 24px;max-width:1050px;line-height:1.5}}
section{{margin:0 0 34px;border-top:1px solid #2a2a30;padding-top:18px}}
h2{{margin:0 0 4px;color:#ffd98a;font-size:20px}}
.note{{color:#9ab;font-size:14px;margin:0 0 12px;line-height:1.45;max-width:1100px}}
.row{{display:flex;gap:16px;flex-wrap:wrap;align-items:flex-start}}
.row a,.vwrap{{position:relative;display:block}}
.row img,.row video{{height:520px;border-radius:8px;border:1px solid #333;display:block;background:#000}}
.vk{{position:absolute;left:8px;top:8px;background:#000a;color:#fff;font-size:12px;
     font-weight:700;padding:2px 9px;border-radius:9px}}
</style>
<h1>Jesus hero clips &mdash; animation review</h1>
<p class=sub>The 8 approved hero stills, animated on <b>cinematic_studio_video_v2</b> (9:16, 5s).
Each moment: the <b>still</b> beside its looping <b>clip</b> so you can judge the face-lock and the
motion together. Discipline: frozen tableau, the world breathes, the camera pushes in slowly,
Jesus stays the steady hero &mdash; no morph, no style change. Clips autoplay + loop muted.</p>
{''.join(cards)}
"""
out = DEST / "JESUS_clips.html"
out.write_text(html, encoding="utf-8")
print(f"wrote {out}")
