"""Rollout gate + living-light prompt channel — fail-closed teeth for the corpus rollout."""
import json
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))
from pipeline.rollout_gate import check_piece  # noqa: E402
from run_piece import animate_prompts, LIVING_LIGHT_BASE  # noqa: E402


def gold_spec():
    """A minimal spec shaped like the gold master: 10 beats, 50% full, 3 templates,
    fx on 6/10, adjacent landing two-shot, no slop."""
    beats = []
    tpls = ["quad", "hero_frac3", "full", "stack_h", "full",
            "hero_band3", "full", "hero_frac3", "full", "full"]
    for i, tpl in enumerate(tpls, 1):
        # fracture/hero templates carry ONE clip entry (panels come from anchors);
        # only fill_each grids like stack_h list one clip per panel
        slug = f"s{i:02d}" if not (tpl == "full" and i == 10) else "s09"  # landing two-shot 9+10
        clips = ([{"slug": slug}, {"slug": f"s{i:02d}b"}] if tpl == "stack_h"
                 else [{"slug": slug}])
        beats.append({"t": [i - 1.0, float(i)], "tpl": tpl, "clips": clips,
                      "cap": {"type": "caption", "text": f"plain sentence {i}"}})
    # cold->warm arc: cool doubt/death poles early, warmest at the landing
    for i, k in ((1, 7400), (2, 7400), (4, 7900), (6, 6800), (8, 5800), (9, 5400), (10, 4900)):
        beats[i - 1]["fx"] = {"temp": k}
    return {"motion": "smooth", "audio": "../audio/narration.mp3", "beats": beats}


def write_piece(tmp_path, spec, living_light=None, ll_exception=None):
    (tmp_path / "visual").mkdir(parents=True, exist_ok=True)
    (tmp_path / "visual" / "livingpage_short.spec.json").write_text(
        json.dumps(spec), encoding="utf-8")
    pj = {"animate": {"moves": {"s01": "a slow push-in"},
                      "living_light": living_light if living_light is not None
                      else {"s09": {"target": "the risen figure",
                                    "light": "the sunburst slowly intensifies"},
                            "s06": {"target": "the shining figures",
                                    "light": "golden rays slowly intensify"}}}}
    if ll_exception is not None:
        pj["animate"]["living_light_exception"] = ll_exception
    (tmp_path / "piece.json").write_text(json.dumps(pj), encoding="utf-8")
    return tmp_path


def test_gold_shape_passes(tmp_path):
    assert check_piece(write_piece(tmp_path, gold_spec())) == []


def test_classic_motion_fails(tmp_path):
    spec = gold_spec(); spec.pop("motion")
    assert any("motion" in f for f in check_piece(write_piece(tmp_path, spec)))


def test_all_fullbleed_fails(tmp_path):
    spec = gold_spec()
    for b in spec["beats"]:
        b["tpl"] = "full"; b["clips"] = b["clips"][:1]
    fails = check_piece(write_piece(tmp_path, spec))
    assert any("fullbleed" in f for f in fails) and any("template" in f for f in fails)


def test_still_overuse_fails(tmp_path):
    spec = gold_spec()
    for b in spec["beats"]:
        for c in b["clips"]:
            c["slug"] = "same"
    assert any("used > 2x" in f for f in check_piece(write_piece(tmp_path, spec)))


def test_nonadjacent_fullbleed_repeat_fails(tmp_path):
    spec = gold_spec()
    spec["beats"][2]["clips"][0]["slug"] = "s09"     # beat 3 full + beats 9/10 -> s09 3x full
    fails = check_piece(write_piece(tmp_path, spec))
    assert any("used > 2x" in f or "full-bleed repeat" in f for f in fails)


def test_missing_fx_arc_fails(tmp_path):
    spec = gold_spec()
    for b in spec["beats"]:
        b.pop("fx", None)
    fails = check_piece(write_piece(tmp_path, spec))
    assert any("grade arc" in f for f in fails)


def test_no_living_light_fails(tmp_path):
    fails = check_piece(write_piece(tmp_path, gold_spec(), living_light={}))
    assert any("living_light" in f for f in fails)


def test_living_light_wasted_on_dyncam_fails(tmp_path):
    spec = gold_spec()
    for b in spec["beats"]:                       # every s09 play forced through dyncam
        for c in b["clips"]:
            if c["slug"] == "s09":
                c["cam"] = "arc"
    fails = check_piece(write_piece(tmp_path, spec))
    assert any("dyncam" in f for f in fails)


def test_living_light_unused_slug_fails(tmp_path):
    fails = check_piece(write_piece(
        tmp_path, gold_spec(),
        living_light={"s09": {"target": "x", "light": "y"},
                      "ghost": {"target": "x", "light": "y"}}))
    assert any("NO beat uses" in f for f in fails)


def test_single_living_light_fails(tmp_path):
    fails = check_piece(write_piece(
        tmp_path, gold_spec(),
        living_light={"s09": {"target": "x", "light": "y"}}))
    assert any("< 2" in f for f in fails)


def test_single_living_light_with_user_exception_passes(tmp_path):
    fails = check_piece(write_piece(
        tmp_path, gold_spec(),
        living_light={"s09": {"target": "x", "light": "y"}},
        ll_exception={"user": "sanjay", "date": "2026-07-15",
                      "reason": "no second wound-free still; Kling regenerates blood"}))
    assert not any("living_light clip(s)" in f for f in fails)


def test_malformed_exception_does_not_lower_the_bar(tmp_path):
    fails = check_piece(write_piece(
        tmp_path, gold_spec(),
        living_light={"s09": {"target": "x", "light": "y"}},
        ll_exception={"reason": "no user grant recorded"}))
    assert any("< 2" in f for f in fails)


def test_double_lighting_fails(tmp_path):
    spec = gold_spec()
    spec["beats"][8]["fx"]["rays"] = {"at": [0.5, 0.1], "strength": 0.5}  # beat 9 plays s09
    spec["beats"][8]["clips"][0]["slug"] = "s09"
    fails = check_piece(write_piece(tmp_path, spec))
    assert any("double-lit" in f for f in fails)


def test_flat_arc_fails(tmp_path):
    spec = gold_spec()
    for b in spec["beats"]:
        if b.get("fx"):
            b["fx"]["temp"] = 5400                 # no cool pole
    fails = check_piece(write_piece(tmp_path, spec))
    assert any("flat" in f for f in fails)


def test_cold_landing_fails(tmp_path):
    spec = gold_spec()
    spec["beats"][-1]["fx"]["temp"] = 7900         # landing colder than the piece
    fails = check_piece(write_piece(tmp_path, spec))
    assert any("landing temp" in f for f in fails)


def test_rays_only_fx_fails(tmp_path):
    spec = gold_spec()
    for b in spec["beats"]:                        # fx present but carries NO temp grade
        if b.get("fx"):
            b["fx"] = {"rays": {"at": [0.5, 0.1], "strength": 0.3}}
    for b in spec["beats"]:                        # avoid double-lit noise on ll beats
        if {c["slug"] for c in b["clips"]} & {"s06", "s09"}:
            b.pop("fx", None)
    fails = check_piece(write_piece(tmp_path, spec))
    assert any("no temp grade" in f for f in fails)


def test_cut_ticks_fails(tmp_path):
    spec = gold_spec()
    spec["cut_ticks"] = True
    fails = check_piece(write_piece(tmp_path, spec))
    assert any("cut_ticks" in f for f in fails)


def test_rollout_spend_tally(tmp_path, monkeypatch):
    import pipeline.rollout_spend as rs
    rows = [
        {"ts": "2026-07-14T09:00:00", "episode": "it_is_finished_john1930",
         "kind": "clip", "provider": "hf", "units": 1},
        {"ts": "2026-07-14T09:01:00", "episode": "it_is_finished_john1930",
         "kind": "clip", "provider": "hf", "units": 1},
        {"ts": "2026-07-14T09:02:00", "episode": "empty_tomb_john208",
         "kind": "still", "provider": "byteplus", "est_usd": 0.05},
        {"ts": "2026-07-13T09:00:00", "episode": "it_is_finished_john1930",
         "kind": "clip", "provider": "hf", "units": 1},                      # pre-rollout
        {"ts": "2026-07-14T09:03:00", "episode": "unrelated_piece",
         "kind": "clip", "provider": "hf", "units": 1},                      # out of scope
        {"ts": "2026-07-14T09:04:00", "episode": "women_first_witnesses_luke245",
         "stage": "reconcile", "actual_credits": 80.0},                      # excluded
    ]
    lg = tmp_path / "ledger.jsonl"
    lg.write_text("\n".join(json.dumps(r) for r in rows), encoding="utf-8")
    monkeypatch.setattr(rs, "LEDGER", lg)
    clips, credits, stills_usd, per_ep = rs.tally()
    assert clips == 2 and credits == 15.0 and stills_usd == 0.05
    assert per_ep == {"it_is_finished_john1930": 2}


def test_disk_clip_count_dedup_and_rejects(tmp_path):
    """One HF bill = one count: promoted copy2 duplicates collapse; parked rejects and
    stale clips still count; pre-rollout mp4s and out-of-scope episodes don't."""
    import os
    import shutil
    import pipeline.rollout_spend as rs
    vis = tmp_path / "cluster_01_cross" / "it_is_finished_john1930" / "visual"
    (vis / "clips" / "_rejected").mkdir(parents=True)
    (vis / "_fx_pilot").mkdir(parents=True)
    pilot = vis / "_fx_pilot" / "a_livinglight.mp4"
    pilot.write_bytes(b"AAAA")                                  # 1 bill (pilot render)
    shutil.copy2(pilot, vis / "clips" / "a.mp4")                # promoted copy - same bill
    (vis / "clips" / "b.mp4").write_bytes(b"BBBBBB")            # 1 bill (production render)
    (vis / "clips" / "_rejected" / "c.mp4").write_bytes(b"CC")  # 1 bill (parked QC reject)
    old = vis / "clips" / "old.mp4"
    old.write_bytes(b"OLDOLD")                                  # pre-rollout - not charged
    os.utime(old, (10_000, 10_000))
    other = tmp_path / "cluster_01_cross" / "not_in_scope" / "visual" / "clips"
    other.mkdir(parents=True)
    (other / "x.mp4").write_bytes(b"XX")                        # out of scope
    assert rs.disk_clip_count(root=tmp_path) == 3


def test_dash_slop_fails(tmp_path):
    spec = gold_spec()
    spec["beats"][0]["cap"]["text"] = "one thing - another thing"
    assert any("captions" in f for f in check_piece(write_piece(tmp_path, spec)))


def test_missing_spec_fails(tmp_path):
    assert check_piece(tmp_path)  # empty dir -> migrate-first fail


# ---- living-light prompt channel (run_piece.animate_prompts) ----

def test_living_light_prompt_built():
    pj = {"animate": {"moves": {"a": "a slow push-in"},
                      "living_light": {"b": {"target": "the two shining figures",
                                             "light": "golden rays slowly intensify"}}}}
    out = animate_prompts(pj)
    assert "Animate it as a slow push-in" in out["a"]
    assert out["b"] == LIVING_LIGHT_BASE.format(
        target="the two shining figures", light="golden rays slowly intensify")
    assert "NEVER shift, harden, frown or blink" in out["b"]
    assert "no blood flows" in out["b"]


def test_living_light_overrides_move():
    pj = {"animate": {"moves": {"a": "a slow push-in"},
                      "living_light": {"a": {"target": "the figure",
                                             "light": "warm haze shimmers"}}}}
    assert "ONLY the light and the air are alive" in animate_prompts(pj)["a"]


def test_living_light_glitter_banned():
    pj = {"animate": {"moves": {},
                      "living_light": {"a": {"target": "the figure",
                                             "light": "golden sparkle particles drift"}}}}
    with pytest.raises(ValueError, match="banned particle"):
        animate_prompts(pj)
