#!/usr/bin/env python
"""build_dyncomic_16x9.py — the v2 DYNAMIC comic driver (SPEC v2 §4A-§4D).

What it changes vs build_mocomic_16x9.py (which stays untouched as the v1 reference):
  CAPTIONS  no engine furniture at all — every caption is SOLVED by caption_layout
            (3-tier, keep-box aware) and drawn by caption_render16 (compact kinetic box /
            red-letter plaque / translucent band). The reserved top/bottom caption bands
            in the locked engine's templates are neutralised (panels get the full page).
  PUNCH     ACTIVE beats carry `punch: true` -> an edit-level zoom-snap on the cut-IN
            (opens ~14% tight, snaps to full over ~4 frames, $0 ffmpeg) per §4A.
  MOTION    same sources as v1: real Kling clips when present (--clips), else $0
            dynamic_cam arc/swoop (explicit `cam`) — never a static still.
  REPORT    writes <spec>_report.json with per-beat durations, caption tiers/flags and
            the Definition-of-Done numbers (§5), so the DoD pass is measured, not vibes.

  .venv\\Scripts\\python.exe longform/02_Psalm_22_Song_From_The_Cross/build_dyncomic_16x9.py --spec dyncomic_m1.spec.json --clips
"""
import argparse, importlib.util, json, statistics, subprocess
from pathlib import Path

import _polite                           # ffmpeg stays polite (POLITE_CPU env, default 50%)
import panel_fit as pf
import dynamic_cam as dc
import caption_layout as cl
import caption_render16 as cr

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
POOL = HERE / "v1" / "visual_16x9_inked"
WORK = POOL / "_dyncomic_work"; WORK.mkdir(parents=True, exist_ok=True)
DYN = POOL / "_dyncam_work"
PAGE = (1920, 1080)

ce_spec = importlib.util.spec_from_file_location("ce", ROOT / "longform" / "_style_poc" / "ew04" / "_mocomic" / "comic_engine.py")
ce = importlib.util.module_from_spec(ce_spec); ce_spec.loader.exec_module(ce)
ce.set_page(*PAGE)
# kill the reserved caption bands (§4B): captions are free overlays now, panels get the page
ce.TEMPLATES = {k: (m, "overlay" if cs in ("bottom_bar", "top_band") else cs, f)
                for k, (m, cs, f) in ce.TEMPLATES.items()}


def run(cmd, what):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode:
        raise RuntimeError(f"{what} failed:\n{r.stderr[-900:]}")


def dyncam_clip(slug: str, move: str) -> Path:
    dest = DYN / f"{slug}_{move}.mp4"
    src = POOL / f"{slug}.png"
    # stale-cache guard: a cached move rendered before the still's last change replays OLD art
    if dest.exists() and dest.stat().st_size > 0 and (
            not src.exists() or dest.stat().st_mtime >= src.stat().st_mtime):
        return dest
    anc = pf.load_anchor(POOL, slug)
    focus = anc["focus"] if anc else [0.5, 0.4]
    DYN.mkdir(parents=True, exist_ok=True)
    return dc.render_move(POOL / f"{slug}.png", move, 5.0, focus, dest)


def _reuse_check(crop_seen, out, slug, beat, crop_id):
    """R2 reuse rule, BOTH halves: a still may reappear only >=8 beats later AND in a
    different crop/shot. crop_id = (panel aspect, bias, zoom, motion) or fracture anchors."""
    if slug in crop_seen:
        prev_beat, prev_id = crop_seen[slug]
        if beat - prev_beat < 8:
            out.append(f"{slug}: beats {prev_beat}->{beat} (gap {beat - prev_beat} < 8)")
        elif crop_id == prev_id:
            out.append(f"{slug}: beats {prev_beat}->{beat} SAME CROP {crop_id}")
    crop_seen[slug] = (beat, crop_id)


def exact_frames(seg: Path, dur: float):
    """Force the segment to EXACTLY round(dur*30) frames. Kling sources are not 30fps, so
    the engine's trim=duration emits an extra frame per segment and the concat drifts off
    the word timings (+0.2s over 11 beats). Frame-exact segments concat with zero drift."""
    n = round(dur * 30)
    tmp = seg.with_name(seg.stem + "_ex.mp4")
    run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(seg), "-vf", "fps=30",
         "-frames:v", str(n), "-c:v", "libx264", "-crf", "18", "-preset", "veryfast",
         "-pix_fmt", "yuv420p", str(tmp)], f"exact_frames {seg.name}")
    tmp.replace(seg)


def apply_punch(seg: Path, dur: float):
    """§4A edit-punch: open ~14% tight, snap to full over ~4 frames — on the cut-IN only."""
    z0, T = 1.14, 0.15
    rate = (z0 - 1.0) / T
    vf = (f"scale=w='if(lt(t,{T}),trunc(iw*({z0}-{rate:.4f}*t)/2)*2,iw)':"
          f"h='if(lt(t,{T}),trunc(ih*({z0}-{rate:.4f}*t)/2)*2,ih)':eval=frame,"
          f"crop={PAGE[0]}:{PAGE[1]}:(iw-{PAGE[0]})/2:(ih-{PAGE[1]})/2,setsar=1")
    tmp = seg.with_name(seg.stem + "_pn.mp4")
    run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(seg), "-vf", vf, "-r", "30",
         "-c:v", "libx264", "-crf", "18", "-preset", "veryfast", "-pix_fmt", "yuv420p", str(tmp)],
        f"punch {seg.name}")
    tmp.replace(seg)


def apply_kinetic(seg: Path, cap: dict, sol: dict, dur: float, stem: str, delay=0.0):
    """Word-cascade overlay at the SOLVED box (same enable-window mechanic as the short).
    delay: on punch beats the cascade waits out the zoom-snap (~0.18s) so the caption never
    rides the zoomed frame; reveal is capped at 90% of the beat so no word is lost."""
    paths = cr.render_kinetic_states(cap.get("kw", ""), sol, PAGE, WORK, stem)
    n = len(paths)
    reveal = min(max(0.8, min(dur * 0.6, dur - 0.5)), dur * 0.9 - delay)
    dt = reveal / n
    bounds = [delay + k * dt for k in range(1, n)]
    cmd = ["ffmpeg", "-y", "-loglevel", "error", "-i", str(seg)]
    for p in paths:
        cmd += ["-loop", "1", "-t", f"{dur}", "-i", str(p)]
    parts = [f"[1:v]format=rgba,fade=t=in:st={delay:.3f}:d=0.12:alpha=1[k1]"]
    for j in range(2, n + 1):
        parts.append(f"[{j}:v]format=rgba[k{j}]")
    prev = "0:v"
    for idx in range(1, n + 1):
        a = delay if idx == 1 else bounds[idx - 2]
        en = f"between(t,{a:.3f},{bounds[idx-1]:.3f})" if idx < n else f"gte(t,{a:.3f})"
        out = f"o{idx}" if idx < n else "outv"
        parts.append(f"[{prev}][k{idx}]overlay=0:0:enable='{en}'[{out}]"); prev = out
    tmp = seg.with_name(seg.stem + "_kc.mp4")
    cmd += ["-filter_complex", ";".join(parts), "-map", "[outv]", "-r", "30",
            "-c:v", "libx264", "-crf", "18", "-preset", "veryfast", "-pix_fmt", "yuv420p", str(tmp)]
    run(cmd, f"kinetic caption {stem}")
    tmp.replace(seg)


def apply_redletter(seg: Path, cap: dict, sol: dict, dur: float, stem: str, at: float = 0.35):
    """at: seconds into the beat when the bar fades in (word-timed plaques, e.g. 'I thirst')."""
    png = cr.render_redletter(cap, sol, PAGE, WORK / f"_red16_{stem}.png")
    tmp = seg.with_name(seg.stem + "_rl.mp4")
    run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(seg),
         "-loop", "1", "-t", f"{dur}", "-i", str(png),
         "-filter_complex",
         f"[1:v]format=rgba,fade=t=in:st={at:.3f}:d=0.3:alpha=1[c];[0:v][c]overlay=0:0,format=yuv420p[v]",
         "-map", "[v]", "-r", "30", "-c:v", "libx264", "-crf", "18", "-preset", "veryfast",
         "-pix_fmt", "yuv420p", str(tmp)], f"redletter {stem}")
    tmp.replace(seg)


def main():
    _polite.be_polite()
    ap = argparse.ArgumentParser()
    ap.add_argument("--spec", default="dyncomic_m1.spec.json")
    ap.add_argument("--clips", action="store_true")
    a = ap.parse_args()
    spec = json.loads((POOL / a.spec).read_text(encoding="utf-8"))
    for p, q in zip(spec["beats"], spec["beats"][1:]):    # a typo here desyncs every later cut
        assert p["t"][1] > p["t"][0] and abs(p["t"][1] - q["t"][0]) < 1e-6, \
            f"beats not contiguous at t={p['t'][1]} vs {q['t'][0]}"
    clips_dir = POOL / "clips"
    segs, report, fitwarn = [], [], []
    crop_seen = {}                       # slug -> (beat, crop-identity tuple) of last use
    reuse_all = []                       # BOTH halves of the R2 reuse rule, verified

    for i, b in enumerate(spec["beats"], 1):
        tpl = b["tpl"]
        # snap the window to the 30fps frame grid: non-multiple durations round UP a frame
        # per segment and the concat drifts (~+0.25s over 11 beats, worse over 70) — cuts
        # slide off the word timings. Frame-exact durations concat with zero drift.
        f0, f1 = round(b["t"][0] * 30), round(b["t"][1] * 30)
        dur = round((f1 - f0) / 30.0, 6)
        rects = ce.panels_for(tpl); mode = ce.template_mode(tpl)
        cds, panels_info, moving = [], [], []
        if mode == "fracture":
            cdef = b["clips"][0]; slug = cdef["slug"]
            live = clips_dir / f"{slug}.mp4"
            if a.clips and live.exists() and live.stat().st_size > 0:
                clip, src = live, "kling"
            else:
                clip, src = dyncam_clip(slug, cdef.get("cam", "arc")), "dyncam"
            anchors = [tuple(x) for x in b.get("anchors", [(1.0, 0.5, 0.5)] * len(rects))]
            anc = pf.load_anchor(POOL, slug) or pf.default_anchor()
            msc = cl.SRC_SCALE["kling" if src == "kling" else f"dyncam_{cdef.get('cam', 'arc')}"]
            for k, r in enumerate(rects):
                z, bx, by = anchors[k % len(anchors)]
                panels_info.append(cl.panel_boxes(r, PAGE, anc, (bx, by), z, motion_scale=msc))
            cds = [{"kind": "clip", "path": str(clip), "motion": cdef.get("motion", "pushin"),
                    "anchors": anchors}]
            moving.append(src)
            _reuse_check(crop_seen, reuse_all, slug, i, ("frac", tuple(anchors)))
        else:
            if mode == "fill_each" and len(b["clips"]) != len(rects):
                raise ValueError(f"beat {i} {tpl}: {len(b['clips'])} clips for {len(rects)} panels")
            for k, cdef in enumerate(b["clips"]):
                slug = cdef["slug"]; motion = cdef.get("motion", "static")
                cam = cdef.get("cam")
                live = clips_dir / f"{slug}.mp4"
                if cam:
                    clip, src = dyncam_clip(slug, cam), "dyncam"; motion = "pushin"
                elif a.clips and live.exists() and live.stat().st_size > 0:
                    clip, src = live, "kling"
                else:
                    clip, src, cam = dyncam_clip(slug, "arc"), "dyncam", "arc"; motion = "pushin"
                anc = pf.load_anchor(POOL, slug) or pf.default_anchor()
                r = rects[k % len(rects)]
                sol = pf.solve_crop((r[2], r[3]), (16, 9), anc, motion)
                if not sol["fit"] and max(sol["lost"]) > 0.10:
                    fitwarn.append(f"  beat {i:>2} {tpl:10} panel {k} {slug:24} {sol['reason']}")
                cds.append({"kind": "clip", "path": str(clip), "motion": motion,
                            "bias": list(sol["bias"]), "zoom": sol["zoom"]})
                msc = cl.SRC_SCALE["kling" if src == "kling" else f"dyncam_{cam}"]
                panels_info.append(cl.panel_boxes(r, PAGE, anc, sol["bias"], sol["zoom"], motion_scale=msc))
                moving.append(src)
                crop_id = (round(r[2] / r[3], 1), tuple(round(v, 1) for v in sol["bias"]),
                           round(sol["zoom"], 1), motion)
                _reuse_check(crop_seen, reuse_all, slug, i, crop_id)

        seg = WORK / f"seg_{i:02d}.mp4"
        ce.build_segment(seg, tpl, cds, dur, None, WORK)     # NO engine furniture, ever
        if b.get("punch"):
            apply_punch(seg, dur)
        cap = b.get("cap"); csol = None
        if cap:
            csol = cl.solve(PAGE, panels_info, cap)
            if csol["cls"] == "kinetic":
                apply_kinetic(seg, cap, csol, dur, f"{i:02d}", delay=0.18 if b.get("punch") else 0.0)
            else:
                apply_redletter(seg, cap, csol, dur, f"{i:02d}")
        exact_frames(seg, dur)               # LAST: intermediate passes may add a frame
        segs.append(seg)
        slugs = "+".join(c["slug"] for c in b["clips"])
        tag = f"T{csol['tier']}{'*FLAG' if csol and csol['flag'] else ''} {csol['style']}" if csol else "-"
        cap_row = None
        if csol:
            # measured honesty: how much of the caption box sits on any (motion-inflated) keep-box
            x, y, w, h = csol["box"]
            ov = 0
            for p in panels_info:
                r = p.get("keep")
                if r:
                    ov += max(0, min(x + w, r[2]) - max(x, r[0])) * max(0, min(y + h, r[3]) - max(y, r[1]))
            cap_row = {k: csol[k] for k in ("tier", "cls", "style", "box", "flag", "reason")}
            cap_row["keep_overlap_pct_of_box"] = round(100 * ov / (w * h))
        print(f"  [{i:2}] {tpl:10} {dur:5.2f}s {'PUNCH ' if b.get('punch') else '      '}"
              f"{'/'.join(moving):13} cap:{tag:14} {slugs}", flush=True)
        report.append({"beat": i, "t": b["t"], "dur": dur, "tpl": tpl, "slugs": slugs.split("+"),
                       "sources": moving, "punch": bool(b.get("punch")), "cap": cap_row})

    if fitwarn:
        print(f"\n[fit-gate] {len(fitwarn)} panel(s) over-cropped >10% (focus protected):")
        print("\n".join(fitwarn))

    lst = WORK / "concat.txt"
    lst.write_text("".join(f"file '{s.as_posix()}'\n" for s in segs), encoding="utf-8")
    silent = WORK / "_silent.mp4"
    run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", str(lst),
         "-c:v", "libx264", "-crf", "18", "-preset", "veryfast", "-pix_fmt", "yuv420p", str(silent)], "concat")
    audio = (POOL / spec["audio"]).resolve()
    total = spec.get("total", spec["beats"][-1]["t"][1])
    out = POOL / (Path(a.spec).stem + "_preview.mp4")
    run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(silent), "-i", str(audio),
         "-map", "0:v", "-map", "1:a", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k",
         "-t", f"{total:.2f}", str(out)], "mux")

    # ---- Definition-of-Done numbers (§5) ----
    durs = [r["dur"] for r in report]
    held = [d for d in durs if d > 6.0]
    move_ok = sum(1 for r in report if "kling" in r["sources"] or r["punch"])
    flags = [r["beat"] for r in report if r["cap"] and r["cap"]["flag"]]
    dod = {"median_beat_s": round(statistics.median(durs), 2),
           "max_beat_s": round(max(durs), 2), "held_beats_gt6s": len(held),
           "kling_or_punch_pct": round(100 * move_ok / len(report)),
           "reuse_violations": reuse_all, "tier3_or_flagged_beats": flags,
           "tier1_pct": round(100 * sum(1 for r in report if r["cap"] and r["cap"]["tier"] == 1)
                              / max(1, sum(1 for r in report if r["cap"]))),
           "beats": len(report)}
    rp = POOL / (Path(a.spec).stem + "_report.json")
    rp.write_text(json.dumps({"dod": dod, "beats": report}, indent=1), encoding="utf-8")
    print(f"\nDoD: {json.dumps(dod)}")
    print(f"\nDONE -> {out}\n  file:///{str(out).replace(chr(92), '/')}\n  report: {rp}")


if __name__ == "__main__":
    main()
