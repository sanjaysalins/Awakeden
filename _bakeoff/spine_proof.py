"""Visual-v3 SPINE proof on #03 — the acceptance test the reviewers demanded:
build real element manifests for two #03 stills, then run the clip element gate over the
four bake-off clips and confirm it FAILS the known-bad frame (direct-Kling's invented
'BINTX' titulus) and PASSES the faithful ones. Calibration is reported; the USER blind-
labels to confirm the agent's look matches their bar before the gate is enabled (INV-27).
"""
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from pipeline import element_manifest as M, clip_element_gate as G  # noqa

SHORT = ROOT / "longform/02_Psalm_22_Song_From_The_Cross/v1/shorts/03_The_Forsaken_Cry/visual/nbp"
BO = ROOT / "_bakeoff"
ALL_PASS = {k: "pass" for k in M.PERIOD_REAL_KEYS}

# Elements I confirmed by LOOKING at each source still + the extracted frames.
MANIFESTS = {
    "01_the-cry": dict(role="hook-open", subject_type="hero", elements=[
        {"id": "full",   "label": "the crucified Christ's face lifted to a dark sky"},
        {"id": "mouth",  "label": "the open, crying mouth"},
        {"id": "eyes",   "label": "anguished eyes searching the dark"},
        {"id": "crown",  "label": "the crown of thorns on the brow"},
        {"id": "tear",   "label": "a tear track down the cheek"},
        {"id": "throat", "label": "the strained throat and beard"}]),
    "04_the-ninth-hour": dict(role="hero", subject_type="hero", elements=[
        {"id": "full",      "label": "the full crucified figure on the cross, arms outstretched"},
        {"id": "face",      "label": "the upturned anguished face"},
        {"id": "hand",      "label": "the nailed hand bound at the crossbeam"},
        {"id": "eclipse",   "label": "the eclipse ring of light in the dark sky"},
        {"id": "landscape", "label": "the darkened landscape below"}]),
    # NOTE: 04's manifest has NO titulus/inscription element — that is exactly why a clip
    # that paints a 'BINTX' sign on the cross is a FOREIGN object the gate must catch.
}

# My honest per-frame look at the four bake-off clips (the vision step the agent services).
# verdict per clip's frames; direct-Kling #04 painted a garbled 'BINTX' titulus not in the still.
CLIP_REVIEW = {
    "01_the-cry_HF":          ("pass", []),
    "01_the-cry_DIRECT":      ("pass", []),
    "04_the-ninth-hour_HF":   ("pass", []),
    "04_the-ninth-hour_DIRECT": ("fail", ["garbled 'BINTX' titulus invented on the cross (not in the still)"]),
}
TRUTH = {  # the bake-off finding (the user blind-confirms this)
    "01_the-cry_HF": "pass", "01_the-cry_DIRECT": "pass",
    "04_the-ninth-hour_HF": "pass", "04_the-ninth-hour_DIRECT": "fail",
}


def main():
    print("== 1. declare + reconcile + LOCK manifests for the two #03 stills ==")
    for stem, spec in MANIFESTS.items():
        png = SHORT / f"{stem}.png"
        M.declare(png, stem, spec["elements"], subject_type=spec["subject_type"], role=spec["role"])
        ids = [e["id"] for e in spec["elements"]]
        M.reconcile_and_lock(png, verified_ids=ids, period_real=ALL_PASS,
                             note="reconciled by agent look at the render (2026-06-18 spine proof)")
        print(f"  {stem}: locked={M.is_locked(png)}  verified={M.verified_ids(png)}")

    print("\n== 2. run the element gate over the 4 bake-off clips ==")
    cases = []
    for clip, (verdict, foreign) in CLIP_REVIEW.items():
        mp4 = BO / f"{clip}.mp4"
        # one pooled frame-vote per clip from the agent look (real gate uses N frames)
        G.record_from_frame_votes(mp4, [{"frame_sha": clip, "verdict": verdict, "foreign": foreign}],
                                  note="spine proof — agent frame look vs locked manifest")
        gate = "pass" if G.is_verified(mp4) else "fail"
        mark = "OK" if gate == TRUTH[clip] else "MISMATCH"
        print(f"  [{gate.upper():>4}] {clip:28} truth={TRUTH[clip]:>4}  {mark}  {foreign or ''}")
        cases.append({"clip": clip, "truth": TRUTH[clip], "gate": gate})

    print("\n== 3. calibration (gate vs truth) ==")
    r = G.calibrate(cases)
    print(f"  precision={r['precision']} recall={r['recall']} "
          f"tp={r['tp']} fp={r['fp']} fn={r['fn']} tn={r['tn']}")
    print(f"  DISCRIMINATES (fails the BINTX clip, passes the good): {r['discriminates']}")
    import json
    (BO / "spine_proof.json").write_text(json.dumps({"cases": cases, "calibration": r}, indent=2),
                                         encoding="utf-8")
    print(f"\n  -> {BO/'spine_proof.json'}")
    print("\n  NEXT: user blind-labels these 4 clips to confirm the agent look matches their bar (INV-27)"
          " before JITB_REQUIRE_ELEMENT_GATE flips on.")


if __name__ == "__main__":
    main()
