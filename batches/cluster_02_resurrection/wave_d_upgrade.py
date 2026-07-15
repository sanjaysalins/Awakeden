"""WAVE D spec upgrades — empty_tomb_john208 + sign_of_jonah_matt1240
(2026-07-14, ROLLOUT_PLAN.md v5.1 + clean-light target rule).

empty_tomb: risen_christ_wounds was x5 (13,17,18,19,20) — over the 2-use cap. Fix:
keep 13 (gridded band3 tour) + 17 (KJV, full); beat 18 'ABOUT YOU' gets ONE new
figure-free still tomb_doorway_dawn (living-light, John 20:5-7 grounded); beats 19+20
land on risen_christ_seeking copied byte-identical from women_first_witnesses (still +
audit sidecars + LL clip, verbatim-prompt hash-bound, $0).

Anchors eyeballed this wave: risen_christ_wounds, jesus_shows_thomas,
john_believes_inside, two_disciples_running, mercy_hand_into_deep, stone_rolled_dawn
(jonah), lot_falls_jonah, jesus_and_scribes. Formulaic center-line grids on the
still-lifes/singles are flagged EYE-CHECK for the build review.

Living-light (all clean-light rule compliant, viewed): jonah = mercy_hand_into_deep +
stone_rolled_dawn; empty_tomb = tomb_doorway_dawn (new) + risen_christ_seeking (copy).
KJV sacred beats stay full. LL beats lose takeover + cam keys."""
import hashlib
import json
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(ROOT))
from run_piece import clip_src_hash, load_piece, animate_prompts  # noqa: E402

C2 = ROOT / "batches" / "cluster_02_resurrection"
WOMEN = C2 / "women_first_witnesses_luke245"

# verbatim from women piece.json (hash-identity for the $0 clip copy)
_women_pj = json.loads((WOMEN / "piece.json").read_text(encoding="utf-8"))
SEEKING_LL = _women_pj["animate"]["living_light"]["risen_christ_seeking"]
SEEKING_JOB = _women_pj["stills"]["jobs"]["risen_christ_seeking"]

PIECES = {
    "empty_tomb_john208": {
        "reslug": {18: "tomb_doorway_dawn", 19: "risen_christ_seeking",
                   20: "risen_christ_seeking"},
        "grids": [
            # EYE-CHECK formulaic: 3 (mary), 6 (linen), 8 (napkin), 10 (stone), 14 (dark)
            (3, "hero_band3", [[1.0, 0.5, 0.3], [1.3, 0.5, 0.55], [1.5, 0.5, 0.75]],
             ["up", "left", "down"], 0.18),
            (5, "hero_frac3", [[1.5, 0.55, 0.38], [1.25, 0.5, 0.68], [1.6, 0.22, 0.15]],
             ["left", "down", "up"], 0.3),
            (6, "hero_frac3", [[1.0, 0.5, 0.5], [1.4, 0.5, 0.5], [1.8, 0.5, 0.55]],
             ["left", "right", "up"], 0.3),
            (8, "hero_frac3", [[1.0, 0.5, 0.5], [1.5, 0.4, 0.45], [1.8, 0.6, 0.55]],
             ["left", "up", "right"], 0.4),
            (9, "hero_frac3", [[1.8, 0.55, 0.4], [1.7, 0.8, 0.62], [1.4, 0.45, 0.8]],
             ["left", "right", "down"], 0.25),
            (10, "hero_band3", [[1.0, 0.5, 0.15], [1.3, 0.45, 0.6], [1.5, 0.7, 0.68]],
             ["up", "left", "down"], 0.28),
            (13, "hero_band3", [[1.2, 0.5, 0.12], [1.7, 0.5, 0.28], [1.6, 0.5, 0.62]],
             ["up", "left", "down"], 0.3),
            (14, "hero_band3", [[1.0, 0.5, 0.3], [1.3, 0.5, 0.55], [1.5, 0.5, 0.78]],
             ["up", "left", "down"], 0.35),
            (15, "hero_frac3", [[1.8, 0.33, 0.22], [1.7, 0.5, 0.5], [1.7, 0.72, 0.55]],
             ["up", "left", "right"], 0.25),
        ],
        "fx": {1: 6800, 2: 7200, 3: 7400, 4: 7500, 5: 7600, 6: 7700, 7: 7800, 8: 7900,
               9: 7500, 10: 7000, 11: 7300, 12: 6800, 13: 6000, 14: 7000, 15: 7200,
               16: 6600, 17: 6000, 18: 5400, 19: 5000, 20: 4900},
        "jobs": {
            "tomb_doorway_dawn": {
                "prompt": "view from inside the rock-hewn tomb, the empty stone bench "
                          "with linen cloths lying, the folded napkin apart by itself, "
                          "the open doorway glowing with golden dawn, warm light "
                          "streaming across the stone floor, vertical, 1st-century Judea",
                "ref": None},
            "risen_christ_seeking": SEEKING_JOB},
        "living_light": {
            "tomb_doorway_dawn": {
                "target": "the dawn light through the open doorway",
                "light": "the dawn light streaming through the open doorway slowly "
                         "brightens and breathes, warm haze drifting across the stone "
                         "floor, the sky beyond the doorway softly glowing"},
            "risen_christ_seeking": SEEKING_LL},
    },
    "sign_of_jonah_matt1240": {
        "reslug": {},
        "grids": [
            # EYE-CHECK formulaic: 1 (cast), 4 (nineveh), 5 (storm), 8 (deep), 12 (sinking)
            (1, "hero_frac3", [[1.0, 0.5, 0.4], [1.5, 0.5, 0.3], [1.6, 0.5, 0.65]],
             ["left", "up", "down"], 0.25),
            (4, "hero_frac3", [[1.0, 0.5, 0.45], [1.4, 0.5, 0.3], [1.7, 0.5, 0.6]],
             ["left", "up", "right"], 0.35),
            (5, "hero_band3", [[1.0, 0.5, 0.3], [1.3, 0.5, 0.55], [1.5, 0.5, 0.75]],
             ["up", "left", "down"], 0.28),
            (6, "hero_frac3", [[1.6, 0.3, 0.4], [1.5, 0.75, 0.5], [1.7, 0.32, 0.78]],
             ["left", "right", "down"], 0.35),
            (8, "hero_band3", [[1.0, 0.5, 0.35], [1.4, 0.5, 0.55], [1.6, 0.5, 0.75]],
             ["up", "left", "down"], 0.35),
            (9, "hero_frac3", [[1.1, 0.5, 0.5], [1.6, 0.5, 0.33], [1.5, 0.5, 0.78]],
             ["left", "up", "down"], 0.4),
            (12, "hero_frac3", [[1.2, 0.5, 0.3], [1.5, 0.5, 0.5], [1.7, 0.5, 0.7]],
             ["up", "left", "down"], 0.3),
        ],
        "fx": {2: 7000, 3: 7400, 4: 7100, 5: 7600, 6: 7300, 7: 7700, 8: 7900, 9: 6800,
               10: 7500, 11: 7600, 12: 7800, 13: 6800, 14: 6200, 15: 5800, 16: 6400,
               17: 5600, 18: 5800, 19: 5200,
               20: {"temp": 4900, "rays": {"at": [0.5, 0.25], "strength": 0.5,
                                           "opacity": 0.5}}},
        "jobs": {},
        "living_light": {
            "mercy_hand_into_deep": {
                "target": "the golden light streaming from the reaching hand into the water",
                "light": "the golden light streaming from the fingers slowly brightens "
                         "and breathes, the ripples on the dark water softly widening, "
                         "warm haze rising where the light meets the deep"},
            "stone_rolled_dawn": {
                "target": "the sunrise over the open tomb",
                "light": "the sunrise glow beyond the hills slowly warms and breathes, "
                         "the long shadows softening across the garden, thin golden "
                         "haze drifting over the flowering field"}},
    },
}

for name, plan in PIECES.items():
    piece = C2 / name
    spec_p = piece / "visual" / "livingpage_short.spec.json"
    spec = json.loads(spec_p.read_text(encoding="utf-8"))
    shutil.copy2(spec_p, spec_p.with_suffix(".json.bak_prewave"))
    spec["motion"] = "smooth"
    spec["cut_ticks"] = False
    B = spec["beats"]
    for i, slug in plan["reslug"].items():
        for c in B[i - 1]["clips"]:
            c["slug"] = slug
    for i, tpl, anchors, slides, stagger in plan["grids"]:
        b = B[i - 1]
        b["tpl"] = tpl
        b["anchors"] = anchors
        b["panel_at"] = [round(b["t"][0] + k * stagger, 2) for k in range(len(anchors))]
        b["panel_slide"] = slides
        b["flash"] = True
        b.pop("takeover", None)
    for i, k in plan["fx"].items():
        B[i - 1]["fx"] = k if isinstance(k, dict) else {"temp": k}
    for b in B:
        if {c["slug"] for c in b["clips"]} & set(plan["living_light"]):
            b.pop("takeover", None)
            for c in b["clips"]:
                c.pop("cam", None)   # a cam key would dyncam-discard the paid clip
    spec_p.write_text(json.dumps(spec, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    pj_p = piece / "piece.json"
    pj = json.loads(pj_p.read_text(encoding="utf-8"))
    pj["stills"]["jobs"].update(plan["jobs"])
    pj["animate"]["living_light"] = plan["living_light"]
    pj_p.write_text(json.dumps(pj, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"{name}: grids {[g[0] for g in plan['grids']]}, fx {len(plan['fx'])}, "
          f"ll {list(plan['living_light'])}, reslug {plan['reslug']}")

# --- $0 sibling copy: women -> empty_tomb risen_christ_seeking (still + audit + clip) ---
dst = C2 / "empty_tomb_john208"
for ext in (".png", ".audit.json", ".quality.json"):
    s, d = WOMEN / "visual" / f"risen_christ_seeking{ext}", dst / "visual" / f"risen_christ_seeking{ext}"
    if not d.exists():
        shutil.copy2(s, d)


def sha256(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


s_png = WOMEN / "visual" / "risen_christ_seeking.png"
d_png = dst / "visual" / "risen_christ_seeking.png"
assert sha256(s_png) == sha256(d_png), "seeking still copy not byte-identical"
s_prompt = animate_prompts(load_piece(WOMEN))["risen_christ_seeking"]
d_pj = load_piece(dst)
d_prompt = animate_prompts(d_pj)["risen_christ_seeking"]
if s_prompt != d_prompt:
    print("RENDER empty_tomb/risen_christ_seeking: prompts differ - no copy")
else:
    clips = dst / "visual" / "clips"
    clips.mkdir(exist_ok=True)
    shutil.copy2(WOMEN / "visual" / "clips" / "risen_christ_seeking.mp4",
                 clips / "risen_christ_seeking.mp4")
    an = d_pj["animate"]
    (clips / "risen_christ_seeking.src.sha").write_text(
        clip_src_hash(d_png, d_prompt, an.get("duration", 5), an.get("aspect_ratio", "9:16")),
        encoding="utf-8")
    print("COPIED women_first_witnesses -> empty_tomb: risen_christ_seeking still+clip ($0, hash-bound)")
