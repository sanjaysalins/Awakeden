#!/usr/bin/env python
"""Composite the motion-comic furniture over the 12 inked clips → the finished pilot short.

Reuses the LOCKED comic engine (longform/_style_poc/ew04/_mocomic/comic_engine.py): PIL caption
boxes + red Scripture/red-letter bars + borders drawn over the animated clips via ffmpeg, then
concat + mux the narration. Piece-local (absolute paths) so it runs from anywhere. Idempotent
per segment (delete _work to force a rebuild).

  .venv\\Scripts\\python.exe batches/cluster_01_cross/father_forgive_them/build_mocomic.py
  ...                                                                        --preview   # still page per beat, $0, no video
"""
import argparse, importlib.util, json, subprocess, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = Path(__file__).resolve().parents[3]
MOCOMIC = ROOT / "longform" / "_style_poc" / "ew04" / "_mocomic"
sys.path.insert(0, str(MOCOMIC))
_s = importlib.util.spec_from_file_location("comic_engine", MOCOMIC / "comic_engine.py")
ce = importlib.util.module_from_spec(_s); _s.loader.exec_module(ce)

SPEC = json.loads((HERE / "visual" / "mocomic.spec.json").read_text(encoding="utf-8"))
CLIPS = (HERE / "visual" / SPEC["clips_dir"]).resolve()
AUDIO = (HERE / "visual" / SPEC["audio"]).resolve()
WORK = HERE / "visual" / "_mocomic_work"; WORK.mkdir(exist_ok=True)
OUT = HERE / f"{SPEC['episode']}_mocomic.mp4"


def clip_path(slug):
    return str(CLIPS / f"{slug}.mp4")


def norm(entry):
    d = dict(entry); d["path"] = clip_path(d.pop("slug")); return d


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--preview", action="store_true", help="render a still page per beat ($0), no video")
    a = ap.parse_args()

    if a.preview:
        pdir = HERE / "visual" / "_mocomic_preview"; pdir.mkdir(exist_ok=True)
        for i, b in enumerate(SPEC["beats"]):
            clips = [norm(e) for e in b["clips"]]
            ce.render_still_page(b["tpl"], clips, b.get("cap"), pdir / f"beat{i:02d}.png")
            print(f"beat {i:2d} {b['tpl']:6} {b['clips'][0]['slug']}")
        print("PREVIEW ->", pdir)
        return

    segs = []
    for i, b in enumerate(SPEC["beats"]):
        t0, t1 = b["t"]; dur = round(t1 - t0, 3)
        clips = [norm(e) for e in b["clips"]]
        fade = 0.5 if i < len(SPEC["beats"]) - 1 else 0.4
        out = WORK / f"seg{i:02d}.mp4"
        ce.build_segment(out, b["tpl"], clips, dur, b.get("cap"), WORK, fade_st=fade)
        segs.append(out)
        captype = (b.get("cap") or {}).get("type", "-")
        print(f"beat {i:2d} [{t0:5.2f}-{t1:5.2f}] {dur:4.2f}s {b['clips'][0]['slug']:24} cap={captype}", flush=True)

    lst = WORK / "_concat.txt"
    lst.write_text("".join(f"file '{p.as_posix()}'\n" for p in segs))
    joined = WORK / "_joined.mp4"
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0",
                    "-i", str(lst), "-c", "copy", str(joined)], check=True)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(joined), "-i", str(AUDIO),
                    "-map", "0:v", "-map", "1:a", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k",
                    "-shortest", str(OUT)], check=True)
    print("FINAL ->", OUT, flush=True)


if __name__ == "__main__":
    main()
