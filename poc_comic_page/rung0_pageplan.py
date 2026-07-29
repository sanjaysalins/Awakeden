"""Rung 0 ($0 dry-run) of the Comic Page Pipeline — CP-1 page-plan MATH ONLY.

No LLM, no rendering, no spend. Runs the page-plan math (v2/COMIC_PAGE_PIPELINE_PROPOSAL.md
section 2) over two real LOCKED narrations (one short, one long) using their existing
narration.alignment.json + narration.mp3, and writes human-readable page-plan reports.

Phrase segmentation reuses pipeline/assembly_timing.py's real functions
(build_timeline + build_phrase_board) via import — NOT reimplemented — per the worker
brief ("import them if importable standalone, otherwise replicate faithfully").

THROWAWAY script. Lives entirely in poc_comic_page/; touches no repo code outside it.
"""
from __future__ import annotations

import json
import math
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from pipeline.assembly_align import align  # noqa: E402  (reuses cache, $0)
from pipeline.assembly_timing import build_timeline, build_phrase_board  # noqa: E402
from pipeline.assembly_ffmpeg import ffprobe_duration  # noqa: E402

OUT_DIR = REPO_ROOT / "poc_comic_page"

PIECES = [
    {
        "label": "SHORT",
        "v1": Path(r"C:\Users\sanjay\PycharmProjects\PythonProject1\jesus\narration\36_In_No_Wise_Cast_Out\v1"),
        "out": OUT_DIR / "rung0_short",
    },
    {
        "label": "LONG",
        "v1": Path(r"C:\Users\sanjay\PycharmProjects\JesusInTheBible\longform\04_The_Bronze_Serpent\v1"),
        "out": OUT_DIR / "rung0_long",
    },
]

DWELL_LO, DWELL_HI, DWELL_TARGET = 8.0, 16.0, 12.0
EPS = 1e-6

LAYOUTS = {
    1: ["full-bleed"],
    2: ["2v", "2h"],
    3: ["3-big-left", "3-big-top", "3-big-right"],
    4: ["2x2"],
}


# --------------------------------------------------------------------------
# CP-1 math primitives
# --------------------------------------------------------------------------
def round_half_up(x: float) -> int:
    return int(math.floor(x + 0.5))


def compute_n_pages(T: float) -> int:
    target = round_half_up(T / DWELL_TARGET)
    lo = math.ceil(T / DWELL_HI)
    hi = math.floor(T / DWELL_LO)
    return max(lo, min(target, hi))


def panels_for(phrase_count: int) -> int:
    if phrase_count <= 1:
        return 1
    if phrase_count <= 3:
        return 2
    if phrase_count <= 5:
        return 3
    return 4


def pages_from_boundaries(bounds, phrases):
    """Partition phrases (in temporal order) into pages defined by `bounds`
    (a sorted list [0.0, ..., T]) using a pointer sweep on phrase.end_s <= t1."""
    pages = []
    j = 0
    for i in range(len(bounds) - 1):
        t0, t1 = bounds[i], bounds[i + 1]
        idxs = []
        while j < len(phrases) and phrases[j].end_s <= t1 + EPS:
            idxs.append(j)
            j += 1
        pages.append({"t0": t0, "t1": t1, "phrase_indices": idxs})
    return pages


def repair_pages(bounds, phrases, log):
    """Apply the §2.4 repair rule until every page dwell is in-band, or a
    REPAIR-FAIL is declared (never improvised past that). Returns
    (final_bounds, events) where events is [(t0_span, t1_span, note)]."""
    bounds = list(bounds)
    events: list[tuple[float, float, str]] = []
    guard = 0
    while guard < 200:
        guard += 1
        pages = pages_from_boundaries(bounds, phrases)
        dwells = [p["t1"] - p["t0"] for p in pages]
        bad = [i for i, d in enumerate(dwells) if not (DWELL_LO - EPS <= d <= DWELL_HI + EPS)]
        if not bad:
            return bounds, events
        i = bad[0]
        neighbours = [x for x in (i - 1, i + 1) if 0 <= x < len(pages)]
        if not neighbours:
            events.append((pages[i]["t0"], pages[i]["t1"],
                            f"REPAIR-FAIL: dwell {dwells[i]:.2f}s out of 8-16s band, "
                            f"no neighbour page to merge with"))
            log(f"      [REPAIR-FAIL] page {pages[i]['t0']:.2f}-{pages[i]['t1']:.2f}s "
                f"({dwells[i]:.2f}s) has no neighbour — cannot repair")
            return bounds, events
        nb = min(neighbours, key=lambda x: dwells[x])
        lo, hi = sorted([i, nb])
        merged_t0, merged_t1 = pages[lo]["t0"], pages[hi]["t1"]
        merged_dwell = merged_t1 - merged_t0
        base = (f"merged [{pages[lo]['t0']:.2f}-{pages[lo]['t1']:.2f}s] + "
                f"[{pages[hi]['t0']:.2f}-{pages[hi]['t1']:.2f}s] "
                f"(offending dwell {dwells[i]:.2f}s outside 8-16s band)")
        new_bounds = bounds[: lo + 1] + bounds[hi + 1 :]
        if merged_dwell <= DWELL_HI + EPS:
            bounds = new_bounds
            events.append((merged_t0, merged_t1, base + " -> merge OK"))
            log(f"      [repair] {base} -> merge OK ({merged_dwell:.2f}s)")
        else:
            mid = (merged_t0 + merged_t1) / 2.0
            merged_idx = pages[lo]["phrase_indices"] + pages[hi]["phrase_indices"]
            candidates = [phrases[k].end_s for k in merged_idx
                          if merged_t0 + EPS < phrases[k].end_s < merged_t1 - EPS]
            if not candidates:
                events.append((merged_t0, merged_t1,
                                base + f"; merged dwell {merged_dwell:.2f}s still >16s and "
                                       f"no legal interior phrase-end split point -> REPAIR-FAIL"))
                log(f"      [REPAIR-FAIL] {base}; merge still {merged_dwell:.2f}s (>16s), "
                    f"no split point available")
                return new_bounds, events
            split_t = min(candidates, key=lambda c: abs(c - mid))
            bounds = bounds[: lo + 1] + [split_t] + bounds[hi + 1 :]
            note = base + f"; merged dwell {merged_dwell:.2f}s >16s -> split at phrase end nearest midpoint = {split_t:.2f}s"
            events.append((merged_t0, split_t, note))
            events.append((split_t, merged_t1, note))
            log(f"      [repair] {note}")
    log("      [REPAIR] guard limit hit (200 passes) — stopping, reporting current state")
    return bounds, events


def layout_for(panel_count: int, prev_layout: str | None, log_exempt) -> str:
    candidates = LAYOUTS[panel_count]
    if len(candidates) == 1:
        choice = candidates[0]
        if prev_layout == choice:
            log_exempt(f"{choice} repeats consecutively (only legal layout at panel_count={panel_count})")
        return choice
    choice = next((c for c in candidates if c != prev_layout), candidates[0])
    return choice


# --------------------------------------------------------------------------
# Per-piece run
# --------------------------------------------------------------------------
def run_piece(label: str, v1: Path, out_dir: Path) -> dict:
    print(f"\n=== {label}: {v1} ===")
    align_path = v1 / "narration.alignment.json"
    mp3_path = v1 / "narration.mp3"
    if not align_path.exists():
        raise SystemExit(f"Missing {align_path}")
    if not mp3_path.exists():
        raise SystemExit(f"Missing {mp3_path}")

    raw = json.loads(align_path.read_text(encoding="utf-8"))
    print(f"  alignment top-level keys: {list(raw.keys())}")
    sample = raw.get("words", [{}])[0]
    print(f"  sample word[0]: {sample}")
    print(f"  word count (raw): {len(raw.get('words', []))}")

    words = align(v1, force=False, log=lambda *a, **k: None)  # reuse cache, $0
    segments = build_timeline(v1, log=lambda *a, **k: None)
    phrases = build_phrase_board(segments, words, log=lambda *a, **k: None)
    print(f"  phrases: {len(phrases)}")

    escalations: list[str] = []

    # --- junk-preamble detection (leaked multi-line HTML comment, see report) ---
    junk_word_count = sum(1 for w in words if w.start == 0.0 and w.end == 0.0)
    # only flag if it's a real leading run, not incidental
    leading_junk = 0
    for w in words:
        if w.start == 0.0 and w.end == 0.0:
            leading_junk += 1
        else:
            break
    if leading_junk >= 5:
        escalations.append(
            f"ESCALATE: alignment word stream has {leading_junk} leading zero-duration "
            f"junk tokens (e.g. {[w.text for w in words[:min(5, leading_junk)]]}...) that "
            f"are not spoken narration — traced to a multi-line <!-- --> HTML comment in "
            f"narration-tagged.md not being fully stripped by "
            f"pipeline/assembly_timing.py::_parse_tagged_chunks (it only checks if a line "
            f"STARTS WITH '<!--', so continuation lines of a multi-line comment block leak "
            f"into the transcript that pipeline/assembly_align.py::transcript() feeds to "
            f"whisper alignment). This corrupts phrase 0's word span and inflates page 1's "
            f"phrase/panel count. NOT fixed here (outside poc_comic_page/, a design decision "
            f"per the brief) — reported for Fable/user triage."
        )

    # --- T: word-end vs ffprobe mp3 duration ---
    T_word = words[-1].end
    T_audio = ffprobe_duration(mp3_path)
    diff = abs(T_word - T_audio)
    print(f"  T (last word end)  = {T_word:.3f}s")
    print(f"  T (ffprobe mp3)    = {T_audio:.3f}s")
    print(f"  diff               = {diff:.3f}s")
    if diff > 0.5:
        escalations.append(
            f"ESCALATE: word-end T ({T_word:.3f}s) vs ffprobe mp3 duration ({T_audio:.3f}s) "
            f"differ by {diff:.3f}s (>0.5s threshold) — using audio duration per brief."
        )
        T = T_audio
    else:
        T = T_word
    print(f"  T used             = {T:.3f}s")

    # --- N_pages ---
    n_pages_formula = compute_n_pages(T)
    n_pages_recheck = max(math.ceil(T / DWELL_HI), min(round_half_up(T / DWELL_TARGET), math.floor(T / DWELL_LO)))
    n_pages_match = (n_pages_formula == n_pages_recheck)
    print(f"  N_pages = clamp(round_half_up(T/12)={round_half_up(T/12)}, "
          f"ceil(T/16)={math.ceil(T/16)}, floor(T/8)={math.floor(T/8)}) = {n_pages_formula}")

    # --- initial boundaries: N_pages-1 interior boundaries snapped to nearest phrase end ---
    phrase_ends = [p.end_s for p in phrases]
    interior = []
    for k in range(1, n_pages_formula):
        target = k * T / n_pages_formula
        nearest = min(phrase_ends, key=lambda e: abs(e - target))
        interior.append(nearest)
    # dedupe + sort (collisions collapse two targets onto one boundary -> fewer pages)
    interior = sorted(set(interior))
    bounds = [0.0] + interior + [T]

    n_boundaries_deduped = len(interior)
    if n_boundaries_deduped < n_pages_formula - 1:
        print(f"  (note: {n_pages_formula - 1 - n_boundaries_deduped} boundary target(s) "
              f"collided onto the same nearest phrase end -> {n_boundaries_deduped} unique "
              f"interior boundaries before repair)")

    # --- repair pass ---
    bounds, repair_events = repair_pages(bounds, phrases, log=print)
    pages_raw = pages_from_boundaries(bounds, phrases)

    def repairs_for(t0, t1):
        notes = []
        for a, b, note in repair_events:
            if t0 >= a - EPS and t1 <= b + EPS:
                notes.append(note)
        return notes

    # --- panels + layout ---
    pages_out = []
    prev_layout = None
    for n, pg in enumerate(pages_raw, start=1):
        idxs = pg["phrase_indices"]
        phrase_count = len(idxs)
        panel_count = panels_for(phrase_count)
        exempt_notes: list[str] = []
        layout = layout_for(panel_count, prev_layout, lambda msg: exempt_notes.append(msg))
        prev_layout = layout
        text = " ".join(phrases[k].text for k in idxs).strip()
        dwell = pg["t1"] - pg["t0"]
        repairs = repairs_for(pg["t0"], pg["t1"]) + exempt_notes
        pages_out.append({
            "n": n,
            "t0": round(pg["t0"], 3),
            "t1": round(pg["t1"], 3),
            "dwell_s": round(dwell, 3),
            "phrase_count": phrase_count,
            "panel_count": panel_count,
            "layout": layout,
            "text": text,
            "repairs": repairs,
        })

    # --- CHECKS ---
    checks = {}
    sum_dwell = sum(p["dwell_s"] for p in pages_out)
    checks["sum_dwells_eq_T"] = (abs(sum_dwell - T) <= 0.05, f"sum={sum_dwell:.3f}s vs T={T:.3f}s")

    phrase_end_set = phrase_ends
    boundary_ok = True
    boundary_detail = []
    for p in pages_out[:-1]:
        t1 = p["t1"]
        if not any(abs(t1 - e) <= 1e-3 for e in phrase_end_set):
            boundary_ok = False
            boundary_detail.append(f"page {p['n']} t1={t1:.3f}s not a phrase end")
    checks["boundaries_are_phrase_ends"] = (boundary_ok, "; ".join(boundary_detail) or "all interior boundaries match a phrase end")

    dwell_ok = True
    dwell_detail = []
    for p in pages_out:
        d = p["dwell_s"]
        in_band = DWELL_LO - EPS <= d <= DWELL_HI + EPS
        has_repair = bool(p["repairs"])
        has_fail = any("REPAIR-FAIL" in r for r in p["repairs"])
        if has_fail:
            dwell_ok = False
            dwell_detail.append(f"page {p['n']} REPAIR-FAIL (dwell {d:.2f}s)")
        elif not in_band and not has_repair:
            dwell_ok = False
            dwell_detail.append(f"page {p['n']} dwell {d:.2f}s out of band, UNEXPLAINED (no repair logged)")
    checks["dwells_in_band_or_repaired"] = (dwell_ok, "; ".join(dwell_detail) or "all pages in 8-16s band or carry a logged repair")

    checks["n_pages_matches_formula"] = (n_pages_match, f"formula={n_pages_formula} recheck={n_pages_recheck}")

    layout_ok = True
    layout_detail = []
    for i in range(1, len(pages_out)):
        a, b = pages_out[i - 1], pages_out[i]
        if a["layout"] == b["layout"]:
            exempted = any("only legal layout" in r for r in b["repairs"])
            if not exempted:
                layout_ok = False
                layout_detail.append(f"pages {a['n']}-{b['n']} both '{a['layout']}' without exemption")
    checks["no_unlogged_consecutive_layout_repeat"] = (layout_ok, "; ".join(layout_detail) or "no unlogged consecutive repeats")

    any_repair_fail = any("REPAIR-FAIL" in r for p in pages_out for r in p["repairs"])
    if any_repair_fail:
        escalations.append("ESCALATE: at least one page hit REPAIR-FAIL — see repairs field / report.")

    for name, (ok, detail) in checks.items():
        print(f"  CHECK {name}: {'PASS' if ok else 'FAIL'} ({detail})")

    # --- write outputs ---
    out_dir.mkdir(parents=True, exist_ok=True)
    plan_doc = {
        "piece": str(v1),
        "T_word_end_s": round(T_word, 3),
        "T_audio_s": round(T_audio, 3),
        "T_used_s": round(T, 3),
        "n_pages": n_pages_formula,
        "pages": [{k: v for k, v in p.items() if k != "text"} for p in pages_out],
        "checks": {k: {"pass": v[0], "detail": v[1]} for k, v in checks.items()},
        "escalations": escalations,
    }
    plan_path = out_dir / "page_plan.dryrun.json"
    plan_path.write_text(json.dumps(plan_doc, ensure_ascii=False, indent=2), encoding="utf-8")

    report_lines = []
    report_lines.append(f"# PAGE PLAN REPORT — {label}")
    report_lines.append("")
    report_lines.append(f"Source: `{v1}`")
    report_lines.append("")
    report_lines.append(f"- T (last word end): {T_word:.3f}s")
    report_lines.append(f"- T (ffprobe mp3): {T_audio:.3f}s")
    report_lines.append(f"- T used: {T:.3f}s")
    report_lines.append(f"- N_pages: {n_pages_formula}")
    report_lines.append(f"- Final page count after repair: {len(pages_out)}")
    report_lines.append("")
    if escalations:
        report_lines.append("## ESCALATIONS")
        for e in escalations:
            report_lines.append(f"- {e}")
        report_lines.append("")
    report_lines.append("## Pages")
    report_lines.append("")
    for p in pages_out:
        is_last = (p["n"] == len(pages_out))
        tag = " **(LAST PAGE)**" if is_last else ""
        report_lines.append(f"### Page {p['n']}{tag}")
        report_lines.append(f"- t0-t1: {p['t0']:.2f}s - {p['t1']:.2f}s")
        report_lines.append(f"- dwell: {p['dwell_s']:.2f}s")
        report_lines.append(f"- phrases: {p['phrase_count']}")
        report_lines.append(f"- panels: {p['panel_count']}")
        report_lines.append(f"- layout: {p['layout']}")
        if p["repairs"]:
            report_lines.append(f"- repairs: {p['repairs']}")
        report_lines.append(f"- text: {p['text']}")
        report_lines.append("")
    report_lines.append("## CHECKS")
    for name, (ok, detail) in checks.items():
        report_lines.append(f"- {name}: {'PASS' if ok else 'FAIL'} — {detail}")
    if escalations:
        report_lines.append("")
        report_lines.append("## ESCALATIONS (repeat)")
        for e in escalations:
            report_lines.append(f"- {e}")
    report_path = out_dir / "PAGE_PLAN_REPORT.md"
    report_path.write_text("\n".join(report_lines), encoding="utf-8")

    return {
        "label": label,
        "T": T,
        "T_word": T_word,
        "T_audio": T_audio,
        "n_pages": n_pages_formula,
        "pages": pages_out,
        "checks": checks,
        "escalations": escalations,
        "plan_path": plan_path,
        "report_path": report_path,
    }


def main():
    results = []
    for piece in PIECES:
        results.append(run_piece(piece["label"], piece["v1"], piece["out"]))

    print("\n\n=== SUMMARY ===")
    for r in results:
        print(f"\n{r['label']}: T={r['T']:.2f}s N_pages={r['n_pages']} "
              f"final_pages={len(r['pages'])} escalations={len(r['escalations'])}")
        print(f"  {'n':>3} {'t0':>7} {'t1':>7} {'dwell':>6} {'phr':>4} {'pan':>4} {'layout':>14}")
        for p in r["pages"]:
            print(f"  {p['n']:>3} {p['t0']:>7.2f} {p['t1']:>7.2f} {p['dwell_s']:>6.2f} "
                  f"{p['phrase_count']:>4} {p['panel_count']:>4} {p['layout']:>14}")
        for name, (ok, detail) in r["checks"].items():
            print(f"  CHECK {name}: {'PASS' if ok else 'FAIL'} ({detail})")
        for e in r["escalations"]:
            print(f"  {e}")
        print(f"  -> {r['plan_path']}")
        print(f"  -> {r['report_path']}")


if __name__ == "__main__":
    main()
