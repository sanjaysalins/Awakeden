#!/usr/bin/env python
"""Load the resolved spec, auto-substitute the LATER slug in each reuse violation
with a safe alternative from the right content pool (OT beats only swap among the
episode's own OT stills; NT beats swap among NT stills + the 21 reused Cross-cluster
clips), re-validate, repeat to a fixed point. Prints every substitution made."""
import json
from pathlib import Path
from collections import Counter

POOL_DIR = Path(__file__).resolve().parents[1] / "v1" / "visual_16x9_inked"
SPEC = POOL_DIR / "livingpage_full.spec.json"
d = json.loads(SPEC.read_text(encoding="utf-8"))
beats = d["beats"]

OT_STILLS = {f"{n:02d}_{s}" for n, s in [
    (1, "snakebite"), (2, "worn_down_they_despise_the_bread_of_heaven"),
    (3, "the_lord_sent_fiery_serpents__and_people_died"), (4, "venom"),
    (5, "they_beg_moses_take_the_serpents_away"), (6, "not"),
    (7, "make_a_fiery_serpent_set_it_on_a_pole"), (8, "raised"), (9, "look"),
    (10, "and_moses_made_a_serpent_of_brass_the_camp_looks")]}
NT_STILLS = {f"{n}_{s}" for n, s in [
    (11, "night"), (12, "even_so_must_the_son_of_man_be_lifted_up"),
    (13, "lifted_up__signifying_what_death_he_should_die"), (14, "for_god_so_loved_the_world"),
    (15, "hezekiah_breaks_the_brazen_serpent"), (16, "the_likeness_of_the_curse_lifted_up"),
    (17, "made_a_curse_for_us__on_the_tree"), (18, "curse"), (19, "look"), (20, "whosoever"),
    (21, "look_to_the_one_lifted_up_hero_close"), (22, "curse"), (23, "himself"), (24, "trust"),
    (25, "we_are_all_bitten__the_cure_outside_us"), (26, "strong"), (27, "outward")]}
REUSE_CLIPS = {f"reuse_{s}" for s in [
    "cross_at_dawn", "face_on_cross", "golgotha_hill_wide", "nail_through_hand", "risen_mercy_hand",
    "two_thieves_wide", "us_under_cross_shadow", "bowed_head_finished", "darkness_veil_torn",
    "grace_poured_sky", "look_up_faces", "ninth_hour_darkness", "risen_christ_wounds",
    "risen_christ_seeking", "risen_christ_congregation", "stone_rolled_dawn", "man_lifting_face_dawn",
    "jesus_looks_down", "hands_of_light_open", "kingdom_light_clouds", "first_day_morning"]}
NT_POOL = NT_STILLS | REUSE_CLIPS


def crop_seen_check(beats):
    crop_seen, violations = {}, []
    for i, b in enumerate(beats, 1):
        tpl = b["tpl"]
        if tpl == "hero_frac3":
            slugs_this = [(b["clips"][0]["slug"], ("frac", tuple(tuple(a) for a in b["anchors"])))]
        elif tpl == "full":
            slugs_this = [(b["clips"][0]["slug"], ("full", b["clips"][0].get("cam")))]
        else:
            slugs_this = [(cd["slug"], ("grid", tpl, cd.get("cam"))) for cd in b["clips"]]
        for slug, crop_id in slugs_this:
            if slug in crop_seen:
                prev_beat, prev_id = crop_seen[slug]
                if i - prev_beat < 8:
                    violations.append((i, slug, "gap", prev_beat))
                elif crop_id == prev_id:
                    violations.append((i, slug, "cropdupe", prev_beat))
            crop_seen[slug] = (i, crop_id)
    return violations


def usage_positions(beats):
    pos = {}
    for i, b in enumerate(beats, 1):
        for cd in b["clips"]:
            pos.setdefault(cd["slug"], []).append(i)
    return pos


# The final landing hold (repeated hero-close still) is a DELIBERATE sacred-stillness
# bookend, not an accidental repeat — the locked Isaiah 53 reference does the exact same
# thing for its last 3 beats (risen_christ_seeking_16x9 x3, gap=1). Leave it alone.
EXEMPT = {"21_look_to_the_one_lifted_up_hero_close"}

skip_beats = set()
for round_no in range(60):
    violations = [v for v in crop_seen_check(beats) if v[1] not in EXEMPT and v[0] not in skip_beats]
    if not violations:
        print(f"CLEAN (of fixable violations) after {round_no} fix rounds")
        break
    i, slug, kind, prev_beat = violations[0]
    b = beats[i - 1]
    pool = OT_STILLS if i <= 16 else NT_POOL
    used_positions = usage_positions(beats)
    candidates = []
    for cand in pool:
        ok = True
        for p in used_positions.get(cand, []):
            if abs(p - i) < 8:
                ok = False
                break
        if ok and cand != slug:
            candidates.append(cand)
    if not candidates:
        print(f"!! no safe candidate for beat {i} slug {slug} ({kind}) — leaving as-is, skipping")
        skip_beats.add(i)
        continue
    candidates.sort(key=lambda s: len(used_positions.get(s, [])))
    new_slug = candidates[0]
    for cd in b["clips"]:
        if cd["slug"] == slug:
            cd["slug"] = new_slug
            break
    print(f"[fix] beat {i} ({kind} vs beat {prev_beat}): {slug} -> {new_slug}")
else:
    print("hit round cap without clean result")

violations = crop_seen_check(beats)
print(f"\nfinal violation count: {len(violations)}")
for v in violations:
    print("  remaining:", v)

durs = [b["t"][1] - b["t"][0] for b in beats]
tplc = Counter(b["tpl"] for b in beats)
print(f"\nbeats: {len(beats)}  avg: {sum(durs)/len(durs):.2f}s  median: {sorted(durs)[len(durs)//2]:.2f}s  max: {max(durs):.2f}s")
print("template mix:", dict(tplc))

d["beats"] = beats
SPEC.write_text(json.dumps(d, indent=1), encoding="utf-8")
print(f"\nwrote {SPEC}")
