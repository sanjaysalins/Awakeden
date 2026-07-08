#!/usr/bin/env python
"""run_piece.py — ONE manifest-driven runner for a living-page batch piece (P1 keystone).

Replaces the per-piece copy-paste quartet (_render_stills.py / _animate.py / _score.py /
_register_assets.py) with a single tested path driven by <piece>/piece.json. Behavior is
byte-compatible with the old scripts (proven on into_thy_hands_luke2346 — same request
bodies, same Kling prompts, same ffmpeg argv, same asset rows) with every P0 guard on
by construction: lint gate + guard_prompt + arm_audit on stills; PASS-sidecar gate +
budget ceiling + ledger row on animate (via _hf_animate_short.hf_animate); ledger rows
on stills too.

Usage:
  .venv\\Scripts\\python.exe run_piece.py "<piece dir>" --stage stills            # $0 lint dry-run
  .venv\\Scripts\\python.exe run_piece.py "<piece dir>" --stage stills --render   # spend
  .venv\\Scripts\\python.exe run_piece.py "<piece dir>" --stage animate           # spend (gated)
  .venv\\Scripts\\python.exe run_piece.py "<piece dir>" --stage score             # $0 ffmpeg
  .venv\\Scripts\\python.exe run_piece.py "<piece dir>" --stage register          # $0 index
  Flags: --force (re-render existing) --only slug1,slug2
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import subprocess
import sys
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

BASE_URL = "https://ark.ap-southeast.bytepluses.com/api/v3/images/generations"
SEEDREAM_USD_PER_IMG = 0.05          # ledger estimate per BytePlus still

# The shared INK camera-only animation contract (was copy-pasted per piece).
INK_BASE = ("A finished inked graphic-novel comic panel - flat printed art with bold black ink "
            "outlines, cel-flat color and cross-hatching. Animate it as {move}. The drawing itself "
            "never moves, redraws, repaints, breathes or changes; the ink lines and flat colors stay "
            "exactly as printed; only the camera moves. No hard cuts, no dissolves, no morphing, no "
            "subject motion, no limbs moving, no new lines drawn. INVENT NOTHING: show ONLY what is "
            "already inked in this exact panel. Keep the subject whole in frame.")


def load_piece(piece_dir: Path) -> dict:
    return json.loads((piece_dir / "piece.json").read_text(encoding="utf-8"))


def _bp(piece_dir: Path):
    """The shared BytePlus module (style tail + key loader) — lives in the cluster's
    father_forgive_them folder (pilot); loaded by path exactly like the old scripts."""
    p = piece_dir.parent / "father_forgive_them" / "byteplus_seedream.py"
    spec = importlib.util.spec_from_file_location("bp", p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


# ---------------------------------------------------------------- stage: stills
def stills_bodies(piece_dir: Path, pj: dict, bp=None) -> dict[str, tuple[dict, Path]]:
    """slug -> (request body, dest png). Pure — no network, no writes."""
    from render_lint import guard_prompt
    bp = bp or _bp(piece_dir)
    st = pj["stills"]
    out = {}
    for slug, job in st["jobs"].items():
        prompt = guard_prompt(job["prompt"])
        body = {"model": st["model"], "prompt": prompt + bp.STYLE + bp.ONE,
                "size": st["size"], "response_format": "url", "watermark": False}
        if job["ref"]:
            ref = (piece_dir / job["ref"]).resolve()
            body["image"] = bp._ref_to_field(str(ref))
            body["sequential_image_generation"] = "disabled"
        out[slug] = (body, piece_dir / "visual" / f"{slug}.png")
    return out


def run_stills(piece_dir: Path, pj: dict, *, render: bool, force: bool, only: set[str]) -> int:
    from render_lint import arm_audit, lint
    jobs = pj["stills"]["jobs"]
    block = False
    for slug, job in jobs.items():
        finds = lint(job["prompt"], stage="still")
        bad = [f for f in finds if str(f.get("level", f.get("severity", "warn"))).lower() == "block"]
        print(f"{slug:24} lint: {len(finds)} finding(s){' BLOCK' if bad else ''}")
        for f in finds:
            print("   !", json.dumps(f)[:110])
        block |= bool(bad)
    if block:
        sys.exit("BLOCKED by lint")
    if not render:
        n = len([s for s in jobs if not only or s in only])
        print(f"\n$0 dry-run. --render to spend (~${n * SEEDREAM_USD_PER_IMG:.2f}).")
        return 0

    from pipeline import cost
    bp = _bp(piece_dir)
    bodies = stills_bodies(piece_dir, pj, bp)
    todo = [s for s in jobs if (not only or s in only)
            and (force or not (piece_dir / "visual" / f"{s}.png").exists())]
    cost.check_budget(pj["piece"], "short", len(todo) * SEEDREAM_USD_PER_IMG)
    for slug in jobs:
        if only and slug not in only:
            continue
        body, dest = bodies[slug]
        if dest.exists() and not force:
            print(f"[skip] {slug}")
            continue
        req = urllib.request.Request(
            BASE_URL, data=json.dumps(body).encode(),
            headers={"Authorization": f"Bearer {bp._load_key()}",
                     "Content-Type": "application/json"})
        try:
            with urllib.request.urlopen(req, timeout=240) as r:
                resp = json.loads(r.read())
        except urllib.error.HTTPError as e:
            print(f"{slug:24} -> HTTP {e.code}: {e.read().decode()[:200]}")
            continue
        url = resp.get("data", [{}])[0].get("url")
        if not url:
            print(f"{slug:24} -> no-url")
            continue
        with urllib.request.urlopen(url, timeout=240) as im:
            dest.write_bytes(im.read())
        arm_audit(dest)   # fail-closed: pending-FAIL sidecar until a real PASS is recorded
        cost.record(pj["piece"], "still", "stills", "byteplus", pj["stills"]["model"], 1,
                    est_usd=SEEDREAM_USD_PER_IMG, est_only=True, note=dest.name)
        print(f"{slug:24} -> ok")
    print("DONE")
    return 0


# ---------------------------------------------------------------- stage: animate
def animate_prompts(pj: dict) -> dict[str, str]:
    an = pj.get("animate") or {"moves": {}}
    base = an.get("base") or INK_BASE   # per-piece verbatim override (e.g. em-dash variant)
    return {slug: base.format(move=move) for slug, move in an["moves"].items()}


def run_animate(piece_dir: Path, pj: dict, *, only: set[str]) -> int:
    if not pj.get("animate"):
        print("(no animate section — this piece's clips come from elsewhere)")
        return 0
    from _hf_animate_short import hf_animate   # carries the PASS-sidecar + budget gates
    pool = piece_dir / "visual"
    clips = pool / "clips"
    clips.mkdir(exist_ok=True)
    an = pj["animate"]
    for slug, prompt in animate_prompts(pj).items():
        if only and slug not in only:
            continue
        still, out = pool / f"{slug}.png", clips / f"{slug}.mp4"
        if out.exists() and out.stat().st_size > 0:
            print(f"[skip] {slug}")
            continue
        ok = hf_animate(still, out, prompt, an["duration"], aspect_ratio=an["aspect_ratio"])
        print(f"SAVED {slug}" if ok else f"FAILED {slug}")
    print("DONE")
    return 0


# ---------------------------------------------------------------- stage: score
def score_cmd(piece_dir: Path, pj: dict) -> list[str]:
    """The exact ffmpeg argv the old _score.py built (byte-compatible: the numeric
    tokens live in piece.json as VERBATIM strings — "56.0" stays "56.0")."""
    sc = pj["score"]
    mus = ROOT / "music_library" / "clips"
    src = piece_dir / Path(sc["src"])
    out = piece_dir / Path(sc["out"])
    total = sc["base_seconds"] + sc["outro_hold"]
    dips = "".join(
        f"volume=volume={v}:enable='between(t,{a},{b})'," for a, b, v in sc["dips"])
    cta_start, cta_vol = sc["cta_dip"]
    fc = (
        f"[1:a]atrim=0:{sc['dark_trim_end']},aformat=sample_fmts=fltp:channel_layouts=stereo:sample_rates=44100[d];"
        f"[2:a]atrim={sc['grace_trim'][0]}:{sc['grace_trim'][1]},aformat=sample_fmts=fltp:channel_layouts=stereo:sample_rates=44100[g];"
        f"[d][g]acrossfade=d={sc['crossfade']}:c1=exp:c2=exp[mch];"
        f"[mch]atrim=0:{total},afade=t=in:st=0:d=1.5,afade=t=out:st={total - 1.5:.2f}:d=1.5,volume=-13dB,"
        + dips +
        f"volume=volume={cta_vol}:enable='between(t,{cta_start},{total})'[mus];"
        f"[0:a]asplit=2[main][key];"
        f"[mus][key]sidechaincompress=threshold=0.12:ratio=2.5:attack=20:release=250[musd];"
        f"[main][musd]amix=inputs=2:normalize=0,alimiter=limit=0.97,aresample=44100[mix];"
        f"[0:v]tpad=stop_mode=clone:stop_duration={sc['tpad']}[vout]"
    )
    return ["ffmpeg", "-y", "-loglevel", "error", "-i", str(src),
            "-i", str(mus / sc["dark"]), "-i", str(mus / sc["grace"]),
            "-filter_complex", fc, "-map", "[vout]", "-map", "[mix]",
            "-c:v", "libx264", "-crf", "18", "-preset", "medium", "-pix_fmt", "yuv420p",
            "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", str(out)]


def run_score(piece_dir: Path, pj: dict) -> int:
    r = subprocess.run(score_cmd(piece_dir, pj), capture_output=True, text=True)
    if r.returncode:
        sys.exit(f"score failed:\n{r.stderr[-800:]}")
    print(f"DONE -> {piece_dir / Path(pj['score']['out'])}")
    return 0


# ---------------------------------------------------------------- stage: register
def register_rows(piece_dir: Path, pj: dict) -> list[dict]:
    rg = pj["register"]
    v = piece_dir / "visual"
    common = dict(aspect=rg["aspect"], style=rg["style"], cluster=pj["cluster"],
                  piece=pj["piece"], piece_title=pj["title"], verse=pj["verse"],
                  source=rg["source"], created=rg["created"])
    rows = []
    for slug, s in rg["stills"].items():
        rows.append({**common, "id": f"{rg['id_prefix']}_{slug}", "type": "still",
                     "media": "image", "path": v / f"{slug}.png",
                     "title": s["subject"], "subject": s["subject"],
                     "characters": s["characters"], "elements": s["elements"],
                     "setting": s["setting"], "palette": rg["palette"], "mood": rg["mood"],
                     "doctrine": s["doctrine"], "reuse_scope": s["scope"],
                     "tags": rg["tags_still"], "used_in": rg["used_in"]})
    # clip rows: an explicit kling_slugs list registers exactly those (unconditional,
    # matching the KLING = [...] variant scripts); otherwise scan for existing mp4s
    kling = rg.get("kling_slugs")
    clip_slugs = kling if kling is not None else \
        [s for s in rg["stills"] if (v / "clips" / f"{s}.mp4").exists()]
    for slug in clip_slugs:
        s = rg["stills"][slug]
        clip = v / "clips" / f"{slug}.mp4"
        rows.append({**common, "id": f"{rg['id_prefix']}_{slug}_clip", "type": "clip",
                     "media": "video", "path": clip,
                     "title": s["subject"] + rg["clip_title_suffix"],
                     "subject": s["subject"], "characters": s["characters"],
                     "elements": s["elements"], "setting": s["setting"],
                     "source": rg["clip_source"], "doctrine": s["doctrine"],
                     "reuse_scope": s["scope"], "tags": rg["tags_clip"],
                     "used_in": rg["used_in"]})
    # bespoke extra rows (e.g. a clip borrowed from a sibling piece) — registered only
    # if the referenced file exists, matching the old scripts' `if <path>.exists():`
    for extra in rg.get("extra_rows", []):
        p = piece_dir / extra["path"]
        if not p.exists():
            continue
        rows.append({**common, **extra, "path": p})
    return rows


def run_register(piece_dir: Path, pj: dict) -> int:
    import asset_index as ax
    rows = register_rows(piece_dir, pj)
    for row in rows:
        ax.register(row)
    stills = sum(1 for r in rows if r["type"] == "still")
    print(f"registered {stills} stills + {len(rows) - stills} clips")
    return 0


# ---------------------------------------------------------------- main
def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="manifest-driven living-page piece runner")
    ap.add_argument("piece", help="piece folder containing piece.json")
    ap.add_argument("--stage", required=True,
                    choices=["stills", "animate", "score", "register", "all"])
    ap.add_argument("--render", action="store_true", help="stills: actually spend")
    ap.add_argument("--force", action="store_true", help="stills: re-render existing")
    ap.add_argument("--only", default="", help="comma slugs subset")
    a = ap.parse_args(argv)
    piece_dir = Path(a.piece).resolve()
    pj = load_piece(piece_dir)
    only = {s for s in a.only.split(",") if s.strip()}
    stages = ["stills", "animate", "score", "register"] if a.stage == "all" else [a.stage]
    for st in stages:
        print(f"== {pj['piece']} :: {st} ==")
        if st == "stills":
            run_stills(piece_dir, pj, render=a.render, force=a.force, only=only)
        elif st == "animate":
            run_animate(piece_dir, pj, only=only)
        elif st == "score":
            run_score(piece_dir, pj)
        elif st == "register":
            run_register(piece_dir, pj)
    return 0


if __name__ == "__main__":
    sys.exit(main())
