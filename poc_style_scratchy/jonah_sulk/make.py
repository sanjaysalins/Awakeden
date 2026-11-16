"""Scratchy-ink cartoon style test: Jonah sulking (Jonah 4). Owner yes 2026-11-10, quoted 2 credits each (~USD 0.20 for 2).
Style described in words only (no reference image attached) so we make our own picture, not a copy."""
import subprocess, urllib.request
from pathlib import Path
HERE = Path(__file__).resolve().parent; HF = str(Path.home()/"bin"/"hf.exe")
STYLE = ("Hand-drawn cartoon illustration: loose scratchy black pen lines, sketchy cross-hatching, slightly messy linework, "
         "flat bold colours (mustard yellow, tomato red, deep navy, warm skin tones), soft drop shadow on the wall behind. "
         "Background: a flat grungy mustard-yellow wall with worn, rough teal-blue patches near the edges. Vertical 9:16. "
         "NO text, NO signature, NO letters, NO border.")
SHOTS = {
 "v1": "Jonah from the Bible, a grumpy middle-aged Hebrew prophet with a big round cartoon head, short black beard, bushy frowning eyebrows, "
       "small eyes glaring sideways, pouting mouth, wearing a plain rust-red wool robe with a mustard sash and a simple navy head cloth. "
       "He stands with his arms crossed tightly, sulking, waist-up, centred, lots of empty yellow wall above him. A single droopy green "
       "gourd leaf hangs wilted beside his head.",
 "v2": "Jonah from the Bible sits sulking on a small rock, a grumpy cartoon prophet with a big round head, short black beard, deep frown, "
       "arms crossed, chin tucked, glaring at the viewer. Plain rust-red robe, mustard sash, navy head cloth. Above him a thin vine with "
       "one big wilted leaf curls over his head, a tiny worm chewing the stem. Full body, centred, lots of empty yellow wall around him.",
}
for k, body in SHOTS.items():
    out = HERE/f"{k}.png"
    if out.exists(): continue
    r = subprocess.run([HF,"generate","create","nano_banana_2","--prompt",STYLE+" "+body,"--aspect_ratio","9:16","--resolution","2k","--wait","--wait-timeout","10m"],capture_output=True,text=True,encoding="utf-8",errors="replace")
    url=[l for l in r.stdout.splitlines() if l.startswith("http")]
    if not url: print(k,"FAILED",r.stdout[-300:],r.stderr[-300:]); continue
    urllib.request.urlretrieve(url[-1], out); (HERE/f"{k}.url").write_text(url[-1]); print(k,"ok",flush=True)
