"""Spec-driven episode builder — the repeatable entry point.
  python build_episode.py [spec.json]
Reads beats from the spec, renders each via the template library + fill-mode
guardrail (comic_engine), concats, and muxes the narration. Idempotent per segment."""
import sys, json, subprocess
from pathlib import Path
import comic_engine as ce

HERE = Path(__file__).parent
SPEC = Path(sys.argv[1]) if len(sys.argv) > 1 else HERE / "ew04.spec.json"
spec = json.loads(SPEC.read_text(encoding="utf-8"))

ANIM = (HERE / spec["anim_dir"]).resolve()
PREFIX = spec["prefix"]
AUDIO = (HERE / spec["audio"]).resolve()
WORK = HERE / "_work"; WORK.mkdir(exist_ok=True)
OUT = HERE / f"{spec['episode']}_comic.mp4"


def clip(slug):
    return str(ANIM / f"{PREFIX}{slug}.mp4")


def norm(entry):
    """spec clip entry -> dict the engine understands (slug resolved to a path)."""
    if isinstance(entry, dict):
        d = dict(entry); d["path"] = clip(d.pop("slug")); return d
    slug, motion = entry
    return {"path": clip(slug), "motion": motion}


segs = []
for i, b in enumerate(spec["beats"]):
    t0, t1 = b["t"]
    dur = round(t1 - t0, 3)
    clips = [norm(e) for e in b["clips"]]
    fade = 0.5 if i < len(spec["beats"]) - 1 else 0.4
    out = WORK / f"seg{i:02d}.mp4"
    ce.build_segment(out, b["tpl"], clips, dur, b.get("cap"), WORK, fade_st=fade)
    segs.append(out)
    tags = "+".join(e["motion"] if isinstance(e, dict) else e[1] for e in b["clips"])
    print(f"beat {i:2d} [{t0:5.1f}-{t1:5.1f}] {b['tpl']:11s} {tags}", flush=True)

lst = WORK / "_concat.txt"
lst.write_text("".join(f"file '{p.as_posix()}'\n" for p in segs))
joined = WORK / "_joined.mp4"
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0",
                "-i", str(lst), "-c", "copy", str(joined)], check=True)
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(joined), "-i", str(AUDIO),
                "-map", "0:v", "-map", "1:a", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k",
                "-shortest", str(OUT)], check=True)
print("FINAL ->", OUT, flush=True)
