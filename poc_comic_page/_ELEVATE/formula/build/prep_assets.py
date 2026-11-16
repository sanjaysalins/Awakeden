"""prep_assets.py - $0 Python pre-step: pre-loop clips to 30 fps for Remotion, export pill/hook PNGs (same code as the
shipped build: build_w3.pill_tabs, build_tp.light_text) + pill geometry. Run with the repo .venv python."""
import sys, json, subprocess, shutil
from pathlib import Path
ROOT = Path(r"F:\slk\PycharmProjects\JesusInTheBible"); EL = ROOT / "poc_comic_page/_ELEVATE"
sys.path.insert(0, str(EL))
import build_tp as T, build_w3 as W, build_arms as BA, build_s32 as S32
from PIL import ImageDraw
PUB = ROOT / "_remotion/public/comic_thief"; CL = ROOT / "batches/cluster_01_cross/today_paradise_luke2343/visual/clips"
CLIPS = ["jesus_turns_to_thief", "penitent_thief_face", "mocker_thief_face", "two_thieves_wide", "golgotha_hill_wide", "mocker_taunts_jesus",
         "confession_face_hands", "kingdom_light_clouds", "answer_light_profile", "risen_mercy_hand", "thief_looks_to_jesus", "us_under_cross_shadow", "paradise_dawn", "nail_through_hand"]


def clips():
    PUB.mkdir(parents=True, exist_ok=True)
    for c in CLIPS:
        o = PUB / (c + ".mp4")
        if o.exists(): continue
        subprocess.run(["ffmpeg", "-y", "-v", "error", "-threads", "2", "-stream_loop", "3", "-i", str(CL / (c + ".mp4")), "-vf", "scale=1080:1920,fps=30",
                        "-t", "13", "-an", "-c:v", "libx264", "-preset", "veryfast", "-crf", "12", "-g", "15", "-pix_fmt", "yuv420p", str(o)], check=True)


def pills(hook_top=200):
    d = PUB / "pills"; d.mkdir(exist_ok=True); out = []
    f = BA.KAL(54); dd = ImageDraw.Draw(T.canvas())
    for i, (a, b, text, who, ref, j) in enumerate(S32.PL):
        p = d / ("p%02d.png" % i); W.pill_tabs(p, text, who, ref, jesus=j)
        lines = BA.wrap(dd, text.split(), f, 820)[:3]; h = 60 + 62 * len(lines)
        out.append(dict(png="pills/p%02d.png" % i, f0=int(round(a * 30)), f1=int(round(b * 30)), box=[70, 1000, 940, h], radius=46, jesus=bool(j), text=text))
    T.light_text(d / "hook.png", "PARADISE FOR A CRIMINAL?", hook_top, size=130, maxw=900)
    return out


if __name__ == "__main__":
    clips(); P = pills(); (Path(__file__).parent / "pills.json").write_text(json.dumps(P, indent=1)); print("assets ok", len(P))
