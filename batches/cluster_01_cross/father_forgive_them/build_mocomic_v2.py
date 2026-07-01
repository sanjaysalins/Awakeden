#!/usr/bin/env python
"""Build the 'Father, forgive them' motion-comic from the v2 (red-teamed) spec.

$0 PREVIEW MODE (default): each still becomes a static 5s clip, run through the REAL comic engine
(full template library + caption / red-letter furniture) + narration audio. Shows the true comic
layout / pacing / sync BEFORE any Kling spend. --clips uses real animated mp4s when they exist.

  .venv\\Scripts\\python.exe batches/cluster_01_cross/father_forgive_them/build_mocomic_v2.py           # $0 static preview
"""
import argparse, importlib.util, json, subprocess
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
SPEC = HERE / "visual" / "mocomic_v2.spec.json"
BP = HERE / "visual" / "_byteplus"
CLIPS = BP / "clips"
WORK = BP / "_mocomic_work"; WORK.mkdir(parents=True, exist_ok=True)
OUT = BP / "father_forgive_them_mocomic_v2.mp4"

ce_spec = importlib.util.spec_from_file_location("ce", ROOT / "longform" / "_style_poc" / "ew04" / "_mocomic" / "comic_engine.py")
ce = importlib.util.module_from_spec(ce_spec); ce_spec.loader.exec_module(ce)
g_spec = importlib.util.spec_from_file_location("g", HERE / "build_gallery_v2.py")
g = importlib.util.module_from_spec(g_spec); g_spec.loader.exec_module(g)   # reuse IMG slug->still map
kc_spec = importlib.util.spec_from_file_location("kc", HERE / "kinetic_caption.py")
kc = importlib.util.module_from_spec(kc_spec); kc_spec.loader.exec_module(kc)   # kinetic word-cascade captions

# fracture anchor sets (zoom, biasX, biasY) — a wide panel + element crops so panels differ
ANCH = {
    "hero_frac3": [(1.0, 0.5, 0.45), (1.6, 0.5, 0.30), (1.6, 0.5, 0.70)],
    "hero_frac4": [(1.0, 0.5, 0.45), (1.7, 0.35, 0.40), (1.7, 0.65, 0.45), (1.5, 0.5, 0.72)],
    "hero_band3": [(1.2, 0.5, 0.28), (1.2, 0.5, 0.50), (1.2, 0.5, 0.72)],
}


def apply_kinetic(seg: Path, text: str, kw: str, dur: float, work: Path, stem: str):
    """Overlay a word-cascade caption onto a (caption-less) segment: words appear one at a time,
    keyword in red, with a quick snap-in. Replaces the segment file in place."""
    paths, _, _ = kc.render_states(text, kw, work, stem)
    n = len(paths)
    reveal = max(0.8, min(dur * 0.6, dur - 0.5))
    dt = reveal / n
    bounds = [k * dt for k in range(1, n)]          # window boundaries t1..t_{n-1}
    cmd = ["ffmpeg", "-y", "-loglevel", "error", "-i", str(seg)]
    for p in paths:
        cmd += ["-loop", "1", "-t", f"{dur}", "-i", str(p)]
    parts = ["[1:v]format=rgba,fade=t=in:st=0:d=0.12:alpha=1[k1]"]
    for j in range(2, n + 1):
        parts.append(f"[{j}:v]format=rgba[k{j}]")
    prev = "0:v"
    for idx in range(1, n + 1):
        a = 0.0 if idx == 1 else bounds[idx - 2]
        en = f"between(t,{a:.3f},{bounds[idx-1]:.3f})" if idx < n else f"gte(t,{a:.3f})"
        out = f"o{idx}" if idx < n else "outv"
        parts.append(f"[{prev}][k{idx}]overlay=0:0:enable='{en}'[{out}]")
        prev = out
    tmp = seg.with_name(seg.stem + "_kc.mp4")
    cmd += ["-filter_complex", ";".join(parts), "-map", "[outv]", "-r", "30",
            "-c:v", "libx264", "-crf", "18", "-preset", "veryfast", "-pix_fmt", "yuv420p", str(tmp)]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode:
        raise RuntimeError(f"kinetic caption {stem} failed:\n{r.stderr[-900:]}")
    tmp.replace(seg)


def static_clip(still: Path, dest: Path) -> Path:
    if dest.exists() and dest.stat().st_size > 0:
        return dest
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-loop", "1", "-t", "5",
                    "-i", str(still), "-r", "30", "-pix_fmt", "yuv420p",
                    "-c:v", "libx264", "-crf", "18", str(dest)], check=True)
    return dest


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--clips", action="store_true")
    a = ap.parse_args()
    spec = json.loads(SPEC.read_text(encoding="utf-8"))
    segs = []
    for i, b in enumerate(spec["beats"], 1):
        tpl = b["tpl"]; dur = round(b["t"][1] - b["t"][0], 3)
        clip_defs = b["clips"]                       # LIST: one distinct still/clip per panel
        cds = []
        for cdef in clip_defs:
            slug = cdef["slug"]
            live = CLIPS / f"{slug}.mp4"
            if a.clips and live.exists() and live.stat().st_size > 0:
                clip = live                                  # real animated Kling clip
            else:
                still = BP / g.IMG[slug]
                clip = static_clip(still, WORK / f"{slug}_static.mp4")
            cd = {"kind": "clip", "path": str(clip), "motion": cdef.get("motion", "static")}
            cds.append(cd)
        if tpl in ANCH and len(cds) == 1:            # fracture/band a single hero still
            cds[0]["anchors"] = ANCH[tpl]
        cap = b.get("cap")
        eng_cap = cap if (cap and cap.get("type") == "redletter") else None   # engine draws red bars only
        seg = WORK / f"seg_{i:02d}.mp4"
        ce.build_segment(seg, tpl, cds, dur, eng_cap, WORK)
        if cap and cap.get("type") == "caption":
            apply_kinetic(seg, cap["text"], cap.get("kw", ""), dur, WORK, f"{i:02d}")
        slugs = "+".join(c["slug"] for c in clip_defs)
        kin = " ·kin" if (cap and cap.get("type") == "caption") else (" ·RED" if eng_cap else "")
        print(f"  [{i:2}] {tpl:10} {dur:5.2f}s  {slugs}{kin}", flush=True)
        segs.append(seg)

    # concat
    lst = WORK / "concat.txt"
    lst.write_text("".join(f"file '{s.as_posix()}'\n" for s in segs), encoding="utf-8")
    silent = WORK / "_silent.mp4"
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0",
                    "-i", str(lst), "-c:v", "libx264", "-crf", "18", "-preset", "veryfast",
                    "-pix_fmt", "yuv420p", str(silent)], check=True)
    # mux narration
    audio = (HERE / "visual" / spec["audio"]).resolve()
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(silent), "-i", str(audio),
                    "-map", "0:v", "-map", "1:a", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k",
                    "-shortest", str(OUT)], check=True)
    print(f"\nDONE -> {OUT}")


if __name__ == "__main__":
    main()
