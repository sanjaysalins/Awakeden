"""Record the #03 element-gate sweep: my honest look at all 13 existing clips vs each still.
Writes element-gate sidecars, reconciles/locks the CLEAN stills, flags the defective ones,
and emits a review page + results json. $0 (no render)."""
import json
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT))
from pipeline import element_manifest as M, clip_element_gate as G  # noqa

SHORT = ROOT / "longform/02_Psalm_22_Song_From_The_Cross/v1/shorts/03_The_Forsaken_Cry"
NBP = SHORT / "visual" / "nbp"
OUT = ROOT / "_bakeoff" / "03sweep"
ALL_PASS = {k: "pass" for k in M.PERIOD_REAL_KEYS}
SHIPPED = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 13}   # from edit_plan (12 excluded)
DO_NOT_USE = {12}   # USER: never reuse/animate scene 12 (a-thousand-years-apart)

# clip stem -> (passed, foreign[], note, still_period_override)
VERDICTS = {
    "01_the-cry":                 (True,  [], "clean face tour; thorn-blood is in the still", None),
    "02_davids-forsaken-psalm":   (False, ["garbled Hebrew scroll text toured into focus"],
                                   "scroll lettering pushed into frame (F5 + writing surface)", {"T5": "fail"}),
    "03_the-first-line":          (False, ["entire clip is a garbled Hebrew scroll macro"],
                                   "writing scene animated — flagrant never-animate-writing", {"T5": "fail"}),
    "04_the-ninth-hour":          (True,  [], "faithful; no invented titulus (unlike the bake-off direct clip)", None),
    "05_my-god-my-god":           (True,  [], "clean crying-face tour", None),
    "06_darkness-over-the-land":  (True,  [], "three crosses + eclipse; titulus small/background (OK per F5)", None),
    "07_the-same-words":          (False, ["garbled Hebrew scroll macro"],
                                   "writing surface toured to garbled letters", {"T5": "fail"}),
    "08_still-my-god":            (False, ["gold picture-frame border revealed"],
                                   "still is on a gilt frame/panel (F2 frame/border)", {"T2": "fail"}),
    "09_bearing-the-forsaking":   (True,  [], "faithful (lamb/shackle in the still); manifest under-declares", None),
    "10_so-you-never-will-be":    (False, ["floating half-body bust — figure cut off at the chest into a dark void, no grounded body"],
                                   "USER FLAG (gate missed): half-body Jesus floating — REPLACE the still", {"T4": "fail"}),
    "11_the-way-opened-from-the-dark": (True, [], "clean; light-break is painted into the still", None),
    "12_a-thousand-years-apart":  (False, ["garbled scroll + writing quill"],
                                   "scroll/writing toured — USER: DO NOT USE (never reuse/animate)", {"T5": "fail"}),
    "13_however-far-youve-run":   (True,  [], "clean landing — lone figure to the cross on the horizon", None),
}


def main():
    rows = []
    for stem, (passed, foreign, note, override) in VERDICTS.items():
        idx = int(stem[:2])
        mp4 = NBP / f"{stem}.mp4"
        png = NBP / f"{stem}.png"
        # element-gate sidecar (my frame look)
        G.record_verdict(mp4, passed, foreign=foreign, note=note)
        # reconcile the still manifest: clean -> lock; defective -> failing guardrail (won't lock)
        m = M.read(png)
        if m:
            vids = [e["id"] for e in m["elements"]]
            pr = dict(ALL_PASS, **(override or {}))
            M.reconcile_and_lock(png, verified_ids=vids, period_real=pr, note=note)
        dnu = idx in DO_NOT_USE
        if dnu:   # durable marker so the clip is never reused/animated again
            (NBP / f"{stem}.do_not_use.json").write_text(
                json.dumps({"do_not_use": True, "reason": note, "by": "user", "date": "2026-06-18"}),
                encoding="utf-8")
        rows.append({"scene": idx, "clip": stem, "gate": "PASS" if passed else "FAIL",
                     "shipped": idx in SHIPPED, "do_not_use": dnu, "foreign": foreign, "note": note,
                     "still_locked": M.is_locked(png)})

    shipped_fail = [r for r in rows if r["gate"] == "FAIL" and r["shipped"]]
    OUT.mkdir(exist_ok=True)
    (OUT / "sweep_results.json").write_text(json.dumps(rows, indent=2), encoding="utf-8")

    # review page
    cards = []
    for r in rows:
        cls = "fail" if r["gate"] == "FAIL" else "pass"
        ship = "🚢 SHIPPED" if r["shipped"] else "—pool—"
        cards.append(
            f'<div class="card {cls}"><div class="lab">scene {r["scene"]:02d} · {r["clip"][3:]} '
            f'· <b>{r["gate"]}</b> · {ship}</div>'
            f'<img src="strip_{r["clip"]}.jpg"><div class="note">{r["note"]}'
            + (f'<br><span class="bad">foreign: {", ".join(r["foreign"])}</span>' if r["foreign"] else "")
            + '</div></div>')
    html = ("<!doctype html><meta charset=utf-8><title>#03 element-gate sweep</title>"
            "<style>body{background:#111;color:#eee;font-family:system-ui;padding:20px}"
            ".card{margin:10px 0;padding:8px;border-radius:8px;border:1px solid #333}"
            ".pass{border-color:#3a6}.fail{border-color:#e44;background:#2a1414}"
            "img{width:100%;max-width:1000px;border-radius:6px;display:block;margin:6px 0}"
            ".lab{font-size:14px}.note{font-size:12px;color:#bbb}.bad{color:#f88}"
            f"</style><h1>#03 The Forsaken Cry — element-gate sweep ($0, no render)</h1>"
            f"<p>13 clips · <b>{sum(1 for r in rows if r['gate']=='PASS')} PASS / "
            f"{sum(1 for r in rows if r['gate']=='FAIL')} FAIL</b> · "
            f"<b style='color:#f88'>{len(shipped_fail)} FAIL clips SHIPPED in the final cut</b></p>"
            + "".join(cards))
    (OUT / "sweep_review.html").write_text(html, encoding="utf-8")

    print(f"=== #03 ELEMENT-GATE SWEEP ===")
    for r in rows:
        flag = "  <<< SHIPPED DEFECT" if (r["gate"] == "FAIL" and r["shipped"]) else ""
        print(f"  scene {r['scene']:02d} {r['clip'][3:]:30} {r['gate']:>4}  "
              f"{'shipped' if r['shipped'] else 'pool':>7}  still_locked={r['still_locked']}{flag}")
    print(f"\n  {sum(1 for r in rows if r['gate']=='FAIL')} FAIL / 13; "
          f"{len(shipped_fail)} of them SHIPPED: {[r['clip'] for r in shipped_fail]}")
    print(f"  review -> {OUT/'sweep_review.html'}")


if __name__ == "__main__":
    main()
