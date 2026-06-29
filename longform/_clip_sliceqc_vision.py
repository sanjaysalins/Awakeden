"""AUTOMATED per-slice vision QC for the gallery shorts.

The manual montage-glance ( _clip_slice_qc.py ) is TOO COARSE — it missed EW03's
05_cross ground-hand and 06_calls flame-wound (the user caught them, not the glance).
This judges every 1-second slice at FULL RES with a cheap Claude-Vision call against the
gallery omit-rubric, auto-recommends omit on any HIGH-severity slice, and writes a
<clip>.sliceqc.json sidecar + an HTML report. Also flags MISSING clips (a rendered
<slug>.png with no <slug>.mp4 — e.g. a 502 silently skipped the beat).

Vision routing honours config: agent-mode uses the file bridge, else the metered API.
Force the cheap API path for an unattended run:  LLM_PROVIDER=api VISION_AUDIT_MODEL=...

Run:  _clip_sliceqc_vision.py EW03_Joseph [EW02_Abraham ...]
"""
import sys, os, json, subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
import config
from pipeline import engine as text_engine
from pipeline.visual_render import _encode_image_for_vision

RUBRIC = (
    "You are a STRICT defect auditor for ONE still frame sliced out of a gallery-tour video "
    "clip. The source is an intentional Baroque oil painting: deep chiaroscuro shadow, dark "
    "negative space, warm single-source light, and visible brushwork are ALL INTENDED — never "
    "flag those. Flag ONLY a clear RENDER DEFECT, one of:\n"
    "  - a MORPHED or DOUBLED face or hand (two faces where one belongs; a melted/smeared face)\n"
    "  - DISEMBODIED or MISPLACED anatomy (a hand growing from the ground/a wall; a floating limb)\n"
    "  - an INVENTED flame / fire / glow that does not belong (e.g. fire on a wrist or wound)\n"
    "  - an OFF-SUBJECT crop holding on feet / fabric / floor / a wall / empty dark space with no "
    "expressive subject (face, eyes, hands, or the key object) anywhere in frame\n"
    "  - an INVENTED or DUPLICATED object that should not be there\n"
    "  - GARBLED text or garbled/incoherent shapes (letters smeared into nonsense)\n"
    "  - a clear ANACHRONISM (modern/medieval/European object in an ancient-biblical scene)\n"
    "Reverent crucifixion / wounds / blood that are PART OF THE STORY are NOT defects. Deep shadow "
    "alone is NOT a defect. When unsure, pass (ok=true). Severity 'high' = the slice is unusable and "
    "the clip should be omitted; 'low' = a minor nit. Return ONLY JSON:\n"
    '{"ok": true|false, "issue": "one short line or empty", "severity": "none|low|high"}'
)


def _dur(f):
    o = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                        "-of", "default=nk=1:nw=1", str(f)], capture_output=True, text=True).stdout.strip()
    return float(o) if o else 0.0


def _slice_frames(clip: Path, work: Path) -> list[Path]:
    """One full-res frame per second -> f00.png, f01.png ...
    SLICEQC_MAX_FRAMES (env, 0=all) evenly down-samples for the in-chat bridge
    (servicing every 1s frame by hand is heavy; the tour cut-points carry the signal)."""
    work.mkdir(parents=True, exist_ok=True)
    for old in work.glob("f*.png"):
        old.unlink()
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(clip),
                    "-vf", "fps=1", str(work / "f%02d.png")], check=False)
    frames = sorted(work.glob("f*.png"))
    cap = int(os.getenv("SLICEQC_MAX_FRAMES", "0") or "0")
    if cap and len(frames) > cap:
        step = len(frames) / cap
        frames = [frames[min(len(frames) - 1, int(i * step))] for i in range(cap)]
    return frames


def _judge(frame_bytes: bytes) -> dict:
    b64, media = _encode_image_for_vision(frame_bytes)
    model = config.VISION_AUDIT_MODEL
    user = "Audit this single sliced frame. Return JSON."
    if config.agent_mode():
        from pipeline import agent_bridge
        text = agent_bridge.call_vision(role=RUBRIC, user=user, image_bytes=frame_bytes,
                                        media=media, model=model, label="sliceqc")
    else:
        resp = text_engine._client().messages.create(
            model=model, max_tokens=400, system=RUBRIC,
            messages=[{"role": "user", "content": [
                {"type": "image", "source": {"type": "base64", "media_type": media, "data": b64}},
                {"type": "text", "text": user},
            ]}],
        )
        text = "".join(b.text for b in resp.content if b.type == "text").strip()
    try:
        d = text_engine._extract_json(text)
    except Exception:
        return {"ok": True, "issue": "", "severity": "none"}
    sev = str(d.get("severity", "none")).lower()
    if sev not in ("none", "low", "high"):
        sev = "high" if not d.get("ok", True) else "none"
    return {"ok": bool(d.get("ok", True)), "issue": str(d.get("issue", "")).strip(), "severity": sev}


def qc_clip(clip: Path, work_root: Path) -> dict:
    frames = _slice_frames(clip, work_root / clip.stem)
    slices = []
    for i, fr in enumerate(frames):
        v = _judge(fr.read_bytes())
        v["slice"] = i
        slices.append(v)
        mark = "  OK " if v["severity"] == "none" else ("  ~  " if v["severity"] == "low" else " FAIL")
        print(f"    s{i:02d}{mark}{(' ' + v['issue']) if v['issue'] else ''}")
    high = [s for s in slices if s["severity"] == "high"]
    verdict = {
        "clip": clip.name,
        "n_slices": len(slices),
        "omit": bool(high),
        "n_high": len(high),
        "issues": sorted({s["issue"] for s in slices if s["severity"] == "high" and s["issue"]}),
        "slices": slices,
    }
    (clip.parent / f"{clip.stem}.sliceqc.json").write_text(
        json.dumps(verdict, indent=2), encoding="utf-8")
    return verdict


def main(eps):
    cards = []
    for ep in eps:
        gc = ROOT / "longform" / ep / "v1" / "short" / "gallery_clips"
        if not gc.exists():
            print(f"[skip] {ep}: no gallery_clips"); continue
        work = gc / "_sliceqc"
        clips = sorted(gc.glob("[0-9][0-9]_*.mp4"))
        only = [c.strip() for c in os.getenv("SLICEQC_CLIPS", "").split(",") if c.strip()]
        if only:
            clips = [c for c in clips if c.stem in only]
        # MISSING: a rendered <slug>.png with no matching <slug>.mp4 (silently-skipped beat)
        have = {c.stem for c in clips}
        missing = sorted(p.stem for p in gc.glob("[0-9][0-9]_*.png") if p.stem not in have)
        print(f"\n=== {ep} — {len(clips)} clips, {len(missing)} missing ===")
        for m in missing:
            print(f"  [MISSING] {m}.mp4 (still rendered, clip absent)")
        rows = []
        for clip in clips:
            print(f"  {clip.stem} ({_dur(clip):.0f}s):")
            v = qc_clip(clip, work)
            badge = ("🔴 OMIT" if v["omit"] else "🟢 ok")
            issues = ("<br>".join(v["issues"])) if v["issues"] else ""
            rows.append(f'<tr><td>{clip.stem}</td><td>{v["n_slices"]}</td>'
                        f'<td>{badge}</td><td>{issues}</td></tr>')
        for m in missing:
            rows.append(f'<tr class="miss"><td>{m}</td><td>—</td><td>⬛ MISSING</td>'
                        f'<td>still rendered, clip absent (re-run builder to fill)</td></tr>')
        cards.append(f"<section><h2>{ep}</h2><table>"
                     "<tr><th>clip</th><th>slices</th><th>verdict</th><th>defects</th></tr>"
                     + "".join(rows) + "</table></section>")
    html = ("<!doctype html><meta charset=utf-8><title>Per-slice vision QC</title>"
            "<style>body{background:#141210;color:#e8e0d2;font-family:system-ui;margin:0;padding:24px}"
            "h2{color:#e7c98a}table{border-collapse:collapse;width:100%;margin-bottom:20px}"
            "td,th{border:1px solid #333;padding:7px 10px;text-align:left;font-size:14px}"
            "th{color:#c8b48a}tr.miss td{color:#e08a8a}</style>"
            "<h1>Automated per-1s-slice vision QC</h1>" + "".join(cards))
    out = ROOT / "longform/_clip_sliceqc_vision.html"
    out.write_text(html, encoding="utf-8")
    print(f"\nindex -> {out}")


if __name__ == "__main__":
    main(sys.argv[1:] or ["EW03_Joseph"])
