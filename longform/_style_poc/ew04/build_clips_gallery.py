"""Build EW04_clips.html — review gallery for the 10 animated inked EW04 clips
(wide+close per beat) plus the 3 reused Jesus clips (2 crucifixion + risen).
Copies every mp4 to a clean Desktop folder and embeds inline <video>. POC."""
import shutil
from pathlib import Path

POC = Path(r"C:\Users\sanjay\PycharmProjects\JesusInTheBible\longform\_style_poc")
ANIM = POC / "ew04" / "anim"
JES = POC / "anim_jesus"
DEST = Path.home() / "Desktop" / "EW04_clips"
(DEST / "v").mkdir(parents=True, exist_ok=True)

# (filename in source dir, source dir, beat label, timecode, caption, flag)
ROWS = [
 ("EW04__01_hook_moses.mp4", ANIM, "1 — Hook / Moses (wide)", "0:00–0:11",
  "Aged Moses by firelight, slow push-in.", ""),
 ("EW04__01b_moses_close.mp4", ANIM, "1b — Moses (close)", "0:00–0:11",
  "Tight on his half-lit face, eyes on the viewer.", ""),
 ("EW04__02_judgment_plague.mp4", ANIM, "2 — The plague (single)", "0:11–0:24",
  "A man fallen, a serpent striking, crowd in shadow.", ""),
 ("EW04__02b_serpents_spread.mp4", ANIM, "2b — The plague (wide)", "0:11–0:24",
  "Live serpents reared over the whole camp, figures fleeing.", ""),
 ("EW04__03_bronze_lifted.mp4", ANIM, "3 — The bronze lifted (wide)", "0:24–0:34",
  "Moses lifts the pole — serpent set on top, over the camp.", ""),
 ("EW04__03b_serpent_atop_sky.mp4", ANIM, "3b — The bronze (hero close)", "0:24–0:34",
  "Low-angle hero of the lifted serpent.",
  "FLAG: the cast bronze serpent shows a slight head/tongue shift — meant to stay dead-still."),
 ("EW04__04_look_and_live.mp4", ANIM, "4 — Look and live (wide)", "0:34–0:42",
  "A bitten man turns his eyes UP to the lifted serpent — life returns.",
  "FLAG: the looking-up man reads a bit Jesus-like (dark hair/beard + blood) before the Jesus reveal."),
 ("EW04__04b_face_to_life.mp4", ANIM, "4b — Look and live (close)", "0:34–0:42",
  "Ordinary stricken elder (neck-bite) turns up — colour returns. Non-Jesus (rerolled).", ""),
 ("EW04__05_night_teacher.mp4", ANIM, "5 — Night teacher (two-shot)", "0:42–0:51",
  "Jesus to Nicodemus by lamplight — the type meets its fulfilment.", ""),
 ("EW04__05b_jesus_speaks.mp4", ANIM, "5b — Night teacher (close)", "0:42–0:51",
  "Warm close on Jesus speaking; the line lands.", ""),
 ("JESUS__cross__b.mp4", JES, "6 — The crucifixion (a)", "0:51–1:01",
  "REUSE — inked Jesus lifted up on the cross.", ""),
 ("JESUS__cross__a.mp4", JES, "6 — The crucifixion (b)", "0:51–1:01",
  "REUSE — 2nd crucifixion angle (storm-sky push-in) for beat depth.", ""),
 ("JESUS__risen__b.mp4", JES, "7 — The risen Christ", "1:01–1:10",
  "REUSE — risen Christ, the contemplative landing (held slow).", ""),
]

cards = []
for fn, srcdir, label, tc, cap, flag in ROWS:
    src = srcdir / fn
    if src.exists():
        shutil.copy2(src, DEST / "v" / fn)
    flag_html = f'<div class=flag>⚠ {flag}</div>' if flag else ''
    cards.append(f"""<section><h2>{label} <span class=tc>{tc}</span></h2>
<div class=note>{cap}</div>{flag_html}
<video src="v/{fn}" controls preload=metadata loop muted playsinline></video></section>""")

html = f"""<!doctype html><meta charset=utf-8><title>EW04 Bronze Serpent — inked clips review</title>
<style>
body{{background:#0e0e10;color:#eee;font-family:system-ui,Segoe UI,Arial;margin:28px;max-width:900px}}
h1{{margin:0 0 6px}} .sub{{color:#9ab;margin:0 0 24px;max-width:820px;line-height:1.5}}
section{{margin:0 0 30px;border-top:1px solid #2a2a30;padding-top:16px}}
h2{{margin:0 0 4px;color:#ffd98a;font-size:21px}} .tc{{color:#6f8;font-size:14px;font-weight:600}}
.note{{color:#9ab;font-size:14px;margin:0 0 8px;line-height:1.45}}
.flag{{color:#ffb4a0;background:#2a1414;border:1px solid #5a2a22;border-radius:6px;
       padding:6px 10px;font-size:13px;margin:0 0 10px}}
video{{width:100%;max-width:420px;border-radius:8px;border:1px solid #333;display:block;background:#000}}
</style>
<h1>EW04 — Bronze Serpent · inked animated clips</h1>
<p class=sub>The 10 animated EW04 clips (wide + close per beat) on <b>cinematic_studio_video_v2</b>,
plus the 3 reused Jesus clips for beats 6–7. Each beat now has ~2× 5s clips so the ~70s cut stays
punchy. <b>2 flags below for your call.</b> Click ▶ to watch each.</p>
{''.join(cards)}
"""
out = DEST / "EW04_clips.html"
out.write_text(html, encoding="utf-8")
print(f"wrote {out}")
