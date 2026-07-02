#!/usr/bin/env python
"""Build the Psalm-22 long the SHORT's way, at 16:9 — the proper motion-comic (not the flat fastcut).

Reuses the LOCKED shared comic_engine.py (multi-panel template library, panel borders, red Scripture
bars) retargeted to 1920x1080 via ce.set_page(), plus the short's kinetic word-cascade captions. Each
panel is a DISTINCT still; `full` is reserved for the sacred red-letter singles. $0 static preview:
every still becomes a 5s static clip run through the real engine (no Kling spend). --clips would swap
in real animated mp4s when they exist (none yet).

  .venv\\Scripts\\python.exe longform/02_Psalm_22_Song_From_The_Cross/build_mocomic_16x9.py --spec mocomic_16x9_m1.spec.json
"""
import argparse, importlib.util, json, subprocess
from pathlib import Path

import _polite                           # keep ffmpeg from hogging the machine (POLITE_CPU env, default 50%)
import panel_fit as pf                   # solved subject-safe panel crops (no more chopped heads)
import dynamic_cam as dc                 # $0 deterministic dimensional camera (no static stills, no morph)

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]                   # .../JesusInTheBible (HERE = longform/02_Psalm...)
POOL = HERE / "v1" / "visual_16x9_inked"
WORK = POOL / "_mocomic16x9_work"; WORK.mkdir(parents=True, exist_ok=True)
PAGE = (1920, 1080)

ce_spec = importlib.util.spec_from_file_location("ce", ROOT / "longform" / "_style_poc" / "ew04" / "_mocomic" / "comic_engine.py")
ce = importlib.util.module_from_spec(ce_spec); ce_spec.loader.exec_module(ce)
ce.set_page(*PAGE)                       # retarget the locked engine to 16:9 for THIS process only
kc_spec = importlib.util.spec_from_file_location(
    "kc", ROOT / "batches" / "cluster_01_cross" / "father_forgive_them" / "kinetic_caption.py")
kc = importlib.util.module_from_spec(kc_spec); kc_spec.loader.exec_module(kc)


def apply_kinetic(seg: Path, text: str, kw: str, dur: float, stem: str):
    """Overlay a word-cascade caption (keyword in red) onto a caption-less segment, in place."""
    paths, _, _ = kc.render_states(text, kw, WORK, stem, page=PAGE)
    n = len(paths); reveal = max(0.8, min(dur * 0.6, dur - 0.5)); dt = reveal / n
    bounds = [k * dt for k in range(1, n)]
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
        parts.append(f"[{prev}][k{idx}]overlay=0:0:enable='{en}'[{out}]"); prev = out
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


DYN = POOL / "_dyncam_work"


def dyncam_clip(slug: str, move: str) -> Path:
    """$0 deterministic dimensional-camera clip (arc/swoop/push) on a still — cached, no morph."""
    dest = DYN / f"{slug}_{move}.mp4"
    if dest.exists() and dest.stat().st_size > 0:
        return dest
    anc = pf.load_anchor(POOL, slug)
    focus = anc["focus"] if anc else [0.5, 0.4]
    return dc.render_move(POOL / f"{slug}.png", move, 5.0, focus, dest)


def main():
    _polite.be_polite()                  # ffmpeg children inherit BelowNormal priority + core cap
    ap = argparse.ArgumentParser()
    ap.add_argument("--spec", default="mocomic_16x9_m1.spec.json")
    ap.add_argument("--clips", action="store_true")
    a = ap.parse_args()
    spec = json.loads((POOL / a.spec).read_text(encoding="utf-8"))
    clips_dir = POOL / "clips"
    segs = []
    warnings = []                        # VERIFY gate: (clip x panel) pairings that can't contain the subject
    for i, b in enumerate(spec["beats"], 1):
        tpl = b["tpl"]; dur = round(b["t"][1] - b["t"][0], 3)
        rects = ce.panels_for(tpl)       # panel geometry -> solve each clip's crop to keep the subject
        cds = []
        for k, cdef in enumerate(b["clips"]):
            slug = cdef["slug"]; motion = cdef.get("motion", "static")
            cam = cdef.get("cam")                                    # explicit $0 dimensional-camera move
            live = clips_dir / f"{slug}.mp4"
            if cam:
                clip = dyncam_clip(slug, cam); motion = "pushin"     # dimensional camera on the still
            elif a.clips and live.exists() and live.stat().st_size > 0:
                clip = live                                          # real animated Kling clip
            else:
                clip = dyncam_clip(slug, "arc"); motion = "pushin"   # NO static stills: $0 arc fallback
            anc = pf.load_anchor(POOL, slug) or pf.default_anchor()
            rw, rh = rects[k % len(rects)][2], rects[k % len(rects)][3]
            sol = pf.solve_crop((rw, rh), (16, 9), anc, motion)      # -> subject-safe bias/zoom
            if not sol["fit"] and max(sol["lost"]) > 0.10:           # warn only on MEANINGFUL over-crop (>10%)
                warnings.append(f"  beat {i:>2} {tpl:9} panel {k} {slug:24} {sol['reason']}")
            cds.append({"kind": "clip", "path": str(clip), "motion": motion,
                        "bias": list(sol["bias"]), "zoom": sol["zoom"]})
        cap = b.get("cap")
        eng_cap = cap if (cap and cap.get("type") == "redletter") else None   # engine draws red bars only
        seg = WORK / f"seg_{i:02d}.mp4"
        ce.build_segment(seg, tpl, cds, dur, eng_cap, WORK)
        if cap and cap.get("type") == "caption":
            apply_kinetic(seg, cap["text"], cap.get("kw", ""), dur, f"{i:02d}")
        slugs = "+".join(c["slug"] for c in b["clips"])
        kin = " ·kin" if (cap and cap.get("type") == "caption") else (" ·RED" if eng_cap else "")
        print(f"  [{i:2}] {tpl:10} {dur:5.2f}s  {slugs}{kin}", flush=True)
        segs.append(seg)

    if warnings:                         # VERIFY gate: subject can't fully fit these panels (crop bias saved the focus)
        print(f"\n[fit-gate] {len(warnings)} panel(s) the still can't fully fill (focus protected, edges cropped):")
        for w in warnings:
            print(w)
        print("  -> fix by moving that beat to a template whose panels match ~1.78:1 (e.g. quad/two_v), or accept the crop.")

    lst = WORK / "concat.txt"
    lst.write_text("".join(f"file '{s.as_posix()}'\n" for s in segs), encoding="utf-8")
    silent = WORK / "_silent.mp4"
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0",
                    "-i", str(lst), "-c:v", "libx264", "-crf", "18", "-preset", "veryfast",
                    "-pix_fmt", "yuv420p", str(silent)], check=True)
    audio = (POOL / spec["audio"]).resolve()
    total = spec.get("total", spec["beats"][-1]["t"][1])
    out = POOL / (Path(a.spec).stem + "_preview.mp4")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(silent), "-i", str(audio),
                    "-map", "0:v", "-map", "1:a", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k",
                    "-t", f"{total:.2f}", str(out)], check=True)
    print(f"\nDONE -> {out}\n  file:///{str(out).replace(chr(92),'/')}")


if __name__ == "__main__":
    main()
