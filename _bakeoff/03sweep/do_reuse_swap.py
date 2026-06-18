"""Reuse-rebuild #03: substitute 3 clean catalogue clips into the defective slots, $0.
Backs up the old defective clips (reversible), copies the source coherence verdict, writes a
locked element manifest + an element-gate PASS sidecar (I gated each by eye)."""
import shutil
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT))
from pipeline import element_manifest as M, clip_element_gate as G, coherence  # noqa

NBP = ROOT / "longform/02_Psalm_22_Song_From_The_Cross/v1/shorts/03_The_Forsaken_Cry/visual/nbp"
BAK = NBP / "_pre_reuse"
BAK.mkdir(exist_ok=True)
ALL_PASS = {k: "pass" for k in M.PERIOD_REAL_KEYS}

SWAPS = [
    dict(slot="08_still-my-god", role="hero", st="hero",
         src=ROOT / "longform/02_Psalm_22_Song_From_The_Cross/v1/shorts/01_The_Crucifixion_Foretold/visual/nbp/13_his-name-is-jesus.mp4",
         elements=[{"id": "full", "label": "the bowed thorn-crowned face of Christ before the cross"},
                   {"id": "eyes", "label": "the downcast eyes"},
                   {"id": "crown", "label": "the crown of thorns with blood"},
                   {"id": "robe", "label": "the blue robe and white tunic"}]),
    dict(slot="10_so-you-never-will-be", role="hero", st="hero",
         src=ROOT / "v2/pilot/isaiah_53_5_with_his_stripes/v1/visual/nbp/06_in-his-own-body-on-the-tree.mp4",
         elements=[{"id": "full", "label": "the full crucified Christ on the cross at dawn"},
                   {"id": "face", "label": "the bowed thorn-crowned face"},
                   {"id": "hand", "label": "the nailed hand with blood"},
                   {"id": "landscape", "label": "the dawn landscape below the cross"}]),
    dict(slot="02_davids-forsaken-psalm", role="multi-story", st="multi-story",
         src=ROOT / "v2/pilot/mockers_words_ps22/v1/visual/nbp/02_a-script-a-thousand-years-old.mp4",
         elements=[{"id": "full", "label": "the prophet with his hand on his chest, a vision behind him"},
                   {"id": "prophet", "label": "the bearded prophet's anguished face"},
                   {"id": "vision", "label": "the haloed vision of the bound Christ among onlookers"},
                   {"id": "hand", "label": "the prophet's hand pressed to his chest"}]),
]


def main():
    for s in SWAPS:
        slot = s["slot"]
        src_mp4 = s["src"]
        src_png = src_mp4.with_suffix(".png")
        dst_mp4 = NBP / f"{slot}.mp4"
        dst_png = NBP / f"{slot}.png"
        if not src_mp4.exists() or not src_png.exists():
            print(f"  !! MISSING source for {slot}: {src_mp4}")
            continue
        # 1. backup the old defective slot (reversible)
        for ext in (".png", ".mp4"):
            old = NBP / f"{slot}{ext}"
            if old.exists():
                shutil.copy2(old, BAK / f"{slot}{ext}")
        # also clear any stale sidecars on the slot so the new content can't ride an old verdict
        coherence.clear_sidecars(dst_png)
        # 2. substitute the clean reused still + clip
        shutil.copy2(src_png, dst_png)
        shutil.copy2(src_mp4, dst_mp4)
        # 3. copy the source's real coherence verdict (re-stamped to the dst hash) — never fabricate
        coherence.copy_verdict(src_png, dst_png)
        # 4. lock an element manifest from the (eye-confirmed) reused content
        M.declare(dst_png, slot, s["elements"], subject_type=s["st"], role=s["role"])
        M.reconcile_and_lock(dst_png, verified_ids=[e["id"] for e in s["elements"]],
                             period_real=ALL_PASS, note=f"reuse from {src_mp4.parent.parent.parent.name}")
        # 5. element-gate PASS (I gated each clip by eye in the sweep)
        G.record_verdict(dst_mp4, True, note=f"reuse-gated clean from {src_png.name}")
        print(f"  {slot:28} <- {src_png.name:36} coherence={coherence.is_verified(dst_png)} "
              f"manifest_locked={M.is_locked(dst_png)} elemgate={G.is_verified(dst_mp4)}")
    print("\n  backups -> _pre_reuse/ ; excluded from the cut: 03, 07, 12")


if __name__ == "__main__":
    main()
