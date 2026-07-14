"""Promote the QC'd living-light pilot clips into this piece (2026-07-14, user-directed).

- piece.json gains animate.living_light entries with the VERBATIM pilot prompts
  (hash binds to the words that produced each clip; template used for future slugs)
- pilot mp4s -> visual/clips/<slug>.mp4 (old clips parked in clips/_old_kling/)
- .src.sha written via run_piece.clip_src_hash so the animate stage sees them fresh
- spec: beats carried by living-light clips lose the PIL "rays" overlay (Kling IS the
  light now; doubling would over-glow) — the temp grade arc stays
"""
import json
import shutil
import sys
from pathlib import Path

PIECE = Path(__file__).parent
ROOT = PIECE.parent.parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "sfx_pilots"))
from run_piece import clip_src_hash  # noqa: E402
from fx_pilot_kling_living_light import PILOT  # noqa: E402  (the verbatim QC'd prompts)

VIS = PIECE / "visual"
CLIPS = VIS / "clips"
FXP = VIS / "_fx_pilot"
LL_TARGETS = {  # doc fields for the template channel (prompt override is what binds)
    "women_bowed": "the two shining figures",
    "risen_christ_seeking": "the whole standing figure",
    "women_tiny_dawn": "the tiny walking figures",
}


def main():
    prompts = dict(PILOT)
    pj_p = PIECE / "piece.json"
    pj = json.loads(pj_p.read_text(encoding="utf-8"))
    an = pj.setdefault("animate", {"moves": {}})
    ll = an.setdefault("living_light", {})
    bak = CLIPS / "_old_kling"
    bak.mkdir(exist_ok=True)

    for slug, target in LL_TARGETS.items():
        src = FXP / f"{slug}_livinglight.mp4"
        dst = CLIPS / f"{slug}.mp4"
        assert src.is_file() and src.stat().st_size > 0, f"pilot clip missing: {src}"
        if dst.exists():
            shutil.move(dst, bak / dst.name)
        shutil.copy2(src, dst)
        prompt = prompts[slug]
        dst.with_suffix(".src.sha").write_text(
            clip_src_hash(VIS / f"{slug}.png", prompt, an.get("duration", 5),
                          an.get("aspect_ratio", "9:16")), encoding="utf-8")
        ll[slug] = {"target": target,
                    "light": "living light (see verbatim prompt)", "prompt": prompt}
        print(f"promoted {slug} (old clip -> _old_kling/)")

    pj_p.write_text(json.dumps(pj, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")

    spec_p = VIS / "livingpage_short.spec.json"
    spec = json.loads(spec_p.read_text(encoding="utf-8"))
    dropped = []
    for i, b in enumerate(spec["beats"], 1):
        if (b.get("fx") or {}).get("rays") and \
                {c["slug"] for c in b["clips"]} & set(LL_TARGETS):
            del b["fx"]["rays"]
            dropped.append(i)
    spec_p.write_text(json.dumps(spec, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"PIL rays dropped from beats {dropped} (Kling carries the light there now)")


if __name__ == "__main__":
    main()
