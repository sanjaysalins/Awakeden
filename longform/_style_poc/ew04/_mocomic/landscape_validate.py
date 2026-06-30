#!/usr/bin/env python
"""Deterministic validators for the landscape motion-comic build (see LANDSCAPE_VALIDATION.md).

Implements the 6 DETERMINISTIC gates (the VISION / PANEL / EYE gates reuse existing tools):

  LV-G1   >=1 animated cell per page          (no all-frozen page)
  LV-G3   no duplicate animated clip          (same .mp4 reused across the episode)
  LV-G5   captions sourced + windows aligned   (caption text subset of locked narration;
                                                page windows contiguous + match audio length)
  LV-G7   reading order = story order          (no later cell sits entirely above/left of an earlier one)
  LV-G10  9:16 reuse native                     (portrait clip never cover-cropped into a 16:9 hero;
                                                16:9 hero only in a 16:9 hero cell)
  LV-G11  never animate writing                (no text-bearing asset on a generative video cell)

Reusable: validate(pages, templates, ...) takes ANY episode's authored PAGES + the engine
TEMPLATES. The EW04 sequence is wired at the bottom as the reference run.

  .venv\\Scripts\\python.exe longform/_style_poc/ew04/_mocomic/landscape_validate.py
  .venv\\Scripts\\python.exe longform/_style_poc/ew04/_mocomic/landscape_validate.py --narration "<locked narration.md>"
"""
import argparse, importlib.util, re, subprocess, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent

# text on a still that a GENERATIVE animator (veo/Kling) will morph into garbled glyphs.
TEXT_KEYWORDS = ("titulus", "scroll", "sign", "codex", "inscription", "writing",
                 "letter", "tablet", "plaque", "banner", "placard", "parchment_text")
ROW_TOL = 8   # px: y-overlap below this is "entirely above/below" (even-snap slack)


# ---------------- asset / cell introspection ----------------
def _slug(src):
    return Path(src).stem


def _is_animated(a):
    """a cell asset moves if it's a video clip, or a Ken-Burns still with real zoom."""
    if a["k"] == "v":
        return True
    return abs(a.get("z", 1.0) - 1.0) > 1e-6      # kb with z==1.0 is a frozen still


def _ar(a):
    return a.get("ar") if a["k"] == "v" else None


def _cells_for(page, templates):
    _, _, tname, assets, _ = page
    cells = templates[tname]()["cells"]
    return tname, cells, assets


def _cap_text(capspec):
    return capspec.get("text", "")


# ---------------- the gates ----------------
def g1_animated_per_page(pages, templates):
    bad = []
    for i, p in enumerate(pages):
        n_anim = sum(1 for a in p[3] if _is_animated(a))
        if n_anim == 0:
            bad.append(f"page {i:02d} ({p[2]}): all {len(p[3])} cells frozen")
    status = "FAIL" if bad else "PASS"
    detail = "every page has >=1 animated cell" if not bad else f"{len(bad)} frozen page(s)"
    return ("LV-G1", status, detail, bad)


def g3_no_dup_clip(pages):
    seen, dup_clip, still_use = {}, [], {}
    for i, p in enumerate(pages):
        for a in p[3]:
            slug = _slug(a["src"])
            if a["k"] == "v":                      # generative/reuse video clip
                if slug in seen:
                    dup_clip.append(f"clip '{slug}' reused: page {seen[slug]:02d} + page {i:02d}")
                else:
                    seen[slug] = i
            else:                                  # still (kb) -- reuse is a softer smell
                still_use.setdefault(slug, []).append(i)
    warns = [f"still '{s}' on pages {pp}" for s, pp in still_use.items() if len(pp) > 1]
    status = "FAIL" if dup_clip else "PASS"
    detail = "no animated clip reused" if not dup_clip else f"{len(dup_clip)} duplicate clip(s)"
    return ("LV-G3", status, detail, dup_clip + ([f"(warn) {w}" for w in warns] if warns else []))


def _probe_dur(path):
    try:
        out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                              "-of", "default=nw=1:nk=1", str(path)],
                             capture_output=True, text=True, check=True)
        return float(out.stdout.strip())
    except Exception:
        return None


def _norm(s):
    s = re.sub(r"\s+", " ", s.lower())
    return re.sub(r"[^a-z0-9 ]", "", s)


def g5_captions_and_windows(pages, audio_path, narration_text, sanitize):
    items, sub_status = [], None
    # (a) caption text subset of the locked narration
    if narration_text:
        nn = _norm(narration_text)
        misses = []
        for i, p in enumerate(pages):
            cap = sanitize(_cap_text(p[4]))
            if _norm(cap) and _norm(cap) not in nn:
                misses.append(f"page {i:02d}: caption not in narration -> \"{cap[:60]}\"")
        sub_status = "FAIL" if misses else "PASS"
        items += misses or ["all captions trace to the locked narration"]
    else:
        sub_status = "SKIP"
        items.append("(no --narration given; caption-subset check skipped)")

    # (b) windows contiguous
    gaps = []
    for i in range(1, len(pages)):
        prev_t1, t0 = pages[i - 1][1], pages[i][0]
        if abs(prev_t1 - t0) > 0.05:
            gaps.append(f"page {i:02d}: window gap/overlap ({prev_t1:.2f} -> {t0:.2f})")
    # (c) last window matches audio length
    last_t1 = pages[-1][1]
    dur = _probe_dur(audio_path)
    win_status = "PASS"
    if gaps:
        win_status = "FAIL"; items += gaps
    else:
        items.append("page windows are contiguous")
    if dur is None:
        items.append(f"(audio duration unreadable at {audio_path})")
    else:
        drift = abs(dur - last_t1)
        msg = f"audio={dur:.2f}s vs last window={last_t1:.2f}s (drift {drift:.2f}s)"
        if drift > 0.5:
            win_status = "FAIL"; items.append("FAIL " + msg + " -- captions will desync")
        else:
            items.append(msg)

    order = {"FAIL": 2, "SKIP": 1, "PASS": 0}
    status = max([sub_status, win_status], key=lambda s: order[s])
    detail = "captions sourced + windows aligned"
    return ("LV-G5", status, detail, items)


def g7_reading_order(pages, templates):
    bad = []
    for i, p in enumerate(pages):
        tname, cells, _ = _cells_for(p, templates)
        rects = [c["rect"] for c in cells]
        for a in range(len(rects)):
            ax, ay, aw, ah = rects[a]
            for b in range(a + 1, len(rects)):     # b defined AFTER a
                bx, by, bw, bh = rects[b]
                # b entirely above a -> b reads first but is defined later
                if by + bh <= ay + ROW_TOL:
                    bad.append(f"page {i:02d} ({tname}): cell {b} sits above cell {a}")
                # same band, b entirely left of a -> b reads first but is defined later
                v_overlap = min(ay + ah, by + bh) - max(ay, by)
                if v_overlap > ROW_TOL and bx + bw <= ax + ROW_TOL:
                    bad.append(f"page {i:02d} ({tname}): cell {b} is left of cell {a} (same row)")
    status = "FAIL" if bad else "PASS"
    detail = "cells follow reading order" if not bad else f"{len(bad)} out-of-order cell(s)"
    return ("LV-G7", status, detail, bad)


def g10_native_reuse(pages, templates):
    bad, warn = [], []
    for i, p in enumerate(pages):
        tname, cells, assets = _cells_for(p, templates)
        for j, a in enumerate(assets):
            if a["k"] != "v":
                continue
            fid = cells[j]["fid"] if j < len(cells) else "?"
            ar = _ar(a)
            if ar is None:
                bad.append(f"page {i:02d} ({tname}) cell {j}: video clip has no 'ar' (renderer can't pick native vs cover)")
                continue
            if ar >= 1:                            # 16:9 hero clip
                if fid != "hero":
                    bad.append(f"page {i:02d} ({tname}) cell {j}: 16:9 hero clip in '{fid}' cell -> will be cropped")
            else:                                  # portrait reuse clip
                if fid == "hero":
                    warn.append(f"page {i:02d} ({tname}) cell {j}: portrait clip in a hero(16:9) slot (renders native, but wastes the wide slot)")
    items = bad + [f"(warn) {w}" for w in warn]
    status = "FAIL" if bad else "PASS"
    detail = "reuse clips kept native" if not bad else f"{len(bad)} aspect mismatch(es)"
    return ("LV-G10", status, detail, items or ["all video clips aspect-correct for their cell"])


def g11_no_animated_writing(pages):
    bad = []
    for i, p in enumerate(pages):
        for j, a in enumerate(p[3]):
            slug = _slug(a["src"]).lower()
            if any(k in slug for k in TEXT_KEYWORDS) and a["k"] == "v":
                bad.append(f"page {i:02d} cell {j}: generative clip on text asset '{slug}' (letters will garble)")
    status = "FAIL" if bad else "PASS"
    detail = "no text generatively animated" if not bad else f"{len(bad)} animated-text violation(s)"
    return ("LV-G11", status, detail, bad)


# ---------------- runner ----------------
def validate(pages, templates, audio_path, narration_text, sanitize):
    return [
        g1_animated_per_page(pages, templates),
        g3_no_dup_clip(pages),
        g5_captions_and_windows(pages, audio_path, narration_text, sanitize),
        g7_reading_order(pages, templates),
        g10_native_reuse(pages, templates),
        g11_no_animated_writing(pages),
    ]


def _print(results):
    mark = {"PASS": "[PASS]", "FAIL": "[FAIL]", "WARN": "[WARN]", "SKIP": "[SKIP]"}
    print("\n=== LANDSCAPE DETERMINISTIC VALIDATION ===\n")
    for gate, status, detail, items in results:
        print(f"{mark[status]} {gate}  {detail}")
        for it in items:
            print(f"         - {it}")
        print()
    n_fail = sum(1 for _, s, _, _ in results if s == "FAIL")
    print("=" * 44)
    print(f"{'ALL DETERMINISTIC GATES PASS' if not n_fail else str(n_fail) + ' GATE(S) FAIL'}\n")
    return n_fail


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--narration", help="locked narration .md/.txt to check captions against")
    args = ap.parse_args()

    # load the EW04 sequence module (gives PAGES, the engine TEMPLATES, AUDIO, sanitize)
    spec = importlib.util.spec_from_file_location("bm", HERE / "build_ew04_sequence.py")
    bm = importlib.util.module_from_spec(spec); spec.loader.exec_module(bm)

    narration_text = None
    if args.narration:
        narration_text = Path(args.narration).read_text(encoding="utf-8")

    results = validate(bm.PAGES, bm.le.TEMPLATES, bm.AUDIO, narration_text, bm.le.lt.sanitize)
    sys.exit(1 if _print(results) else 0)


if __name__ == "__main__":
    main()
