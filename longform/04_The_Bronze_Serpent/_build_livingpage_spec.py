"""Build v1/visual_16x9_inked/livingpage_full.spec.json (the beat spec
build_livingpage_16x9.py consumes) from the restyled scene_plan.json (27
scenes, one full-bleed beat each, real word-timed boundaries, KJV redletter
vs narrator-caption already tagged per scene). $0, no render.

PAID_HERO_IDS get a "cam" omitted so the engine prefers a real Kling clip
(clips_dir/<slug>.mp4) when present (--clips flag); everything else gets an
explicit "cam" so it always uses the $0 deterministic dynamic_cam engine.
"""
import json
from pathlib import Path

import subprocess

HERE = Path(__file__).resolve().parent
OUT = HERE / "v1" / "visual_16x9_inked"
plan = json.loads((OUT / "scene_plan.json").read_text(encoding="utf-8"))
scenes = sorted(plan["scenes"], key=lambda s: s["t"][0])

# scene-window-staleness guard (memory `scene-window-staleness`): the archived Baroque
# scene_plan.json's last window end (480.96s) is stale vs the CURRENT locked narration.mp3
# (474.23s per ffprobe / narration.meta.json final_total_seconds) -- clip the tail beat to
# the real audio end rather than building past end-of-file.
mp3_dur = float(subprocess.run(
    ["ffprobe", "-v", "error", "-show_entries", "format=duration",
     "-of", "default=noprint_wrappers=1:nokey=1", str(HERE / "v1" / "narration.mp3")],
    capture_output=True, text=True, check=True).stdout.strip())
if scenes[-1]["t"][1] > mp3_dur:
    print(f"[retime] clipping last beat end {scenes[-1]['t'][1]:.2f}s -> real mp3 duration {mp3_dur:.2f}s")
    scenes[-1]["t"][1] = round(mp3_dur, 3)

# hook / sacred-divine-speech / NT-confirmation / hero-close: the few beats worth a
# real paid Kling clip (choose_engine value rule -- everything else is $0 dynamic_cam).
PAID_HERO_IDS = {1, 7, 8, 12, 21}


def slug_for(s):
    kw = s["cap"].get("kw", s["title"])
    stem = f"{s['id']:02d}_{kw.lower().replace(' ', '_')}"
    return "".join(c if (c.isalnum() or c == "_") else "" for c in stem)[:60]


def cam_for(s):
    if s["camera"] == "locked, the faintest breathing drift":
        return "push" if s["sacred"] else "arc"
    return "push" if s["sacred"] else "swoop"


beats = []
for s in scenes:
    slug = slug_for(s)
    cdef = {"slug": slug}
    if s["id"] not in PAID_HERO_IDS:
        cdef["cam"] = cam_for(s)
    # PAID_HERO_IDS: no "cam" key -> source() tries clips_dir/<slug>.mp4 first when
    # --clips is passed, else still falls back to $0 dyncam "arc" if the clip is missing.
    cap = dict(s["cap"])
    beat = {"t": s["t"], "tpl": "full", "clips": [cdef], "cap": cap}
    if s["id"] in PAID_HERO_IDS and not s["sacred"]:
        beat["punch"] = True  # zoom-snap on cut-in for the two non-sacred hero beats (hook, signature)
    beats.append(beat)

total = mp3_dur
spec = {
    "_doc": ("BRONZE SERPENT - graphic-novel rebuild TEST (2026-07-16). 27 beats, "
             "word-timed from narration.alignment.json via the archived Baroque "
             "scene_plan.json's beat boundaries (content/camera/timing unchanged, "
             "style restyled). Sacred red-letter beats (KJV/THE LORD/JESUS quotes) "
             "carry no punch/border-break, gentlest 'push' camera only. 5 paid Kling "
             "hero clips (hook, THE LORD's command, the signature lifted-serpent wide, "
             "JESUS's own words, the risen-Christ hero close); everything else is $0 "
             "dynamic_cam (arc/swoop/push)."),
    "audio": "../narration.mp3",
    "total": total,
    "beats": beats,
}
out_path = OUT / "livingpage_full.spec.json"
out_path.write_text(json.dumps(spec, indent=2, ensure_ascii=False), encoding="utf-8")
print(f"wrote {len(beats)} beats, total {total:.2f}s -> {out_path}")
print("paid hero slugs:")
for s in scenes:
    if s["id"] in PAID_HERO_IDS:
        print(f"  #{s['id']:02d} {slug_for(s)}  [{s['t'][0]:.1f}-{s['t'][1]:.1f}]  {s['title']}")
