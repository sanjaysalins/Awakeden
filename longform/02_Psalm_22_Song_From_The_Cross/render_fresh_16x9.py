#!/usr/bin/env python
"""Render the 18 FRESH inked 16:9 stills for the red-teamed Psalm-22 long page plan.

Reuses the LOCKED short pilot's BytePlus Seedream 4.5 client (INV-15) at 2560x1440. Ref-lock per
the pilot strategy: SUFFERING Christ -> bare-torso ref; RISEN Christ -> risen-face ref; context /
David / scribe / text / landscape -> NO ref (face-bleed fix). Every doctrine/render guardrail from
the 3-reviewer red-team is baked into the prompt. Idempotent. List-only until --render (INV-20).

  ...python longform/02_Psalm_22_Song_From_The_Cross/render_fresh_16x9.py            # list
  ...python longform/02_Psalm_22_Song_From_The_Cross/render_fresh_16x9.py --render   # ~$0.72
"""
import argparse, importlib.util, json, urllib.request, urllib.error
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
OUT = HERE / "v1" / "visual_16x9_inked"; OUT.mkdir(parents=True, exist_ok=True)
PILOT = ROOT / "batches" / "cluster_01_cross" / "father_forgive_them"
REF_RISEN = PILOT / "visual" / "_byteplus" / "bakeoff" / "_ref_small.png"
REF_CRUX = PILOT / "visual" / "_byteplus" / "nail_wide_45.png"
MODEL, SIZE = "seedream-4-5-251128", "2560x1440"
BASE = "https://ark.ap-southeast.bytepluses.com/api/v3/images/generations"

bp_spec = importlib.util.spec_from_file_location("bp", PILOT / "byteplus_seedream.py")
bp = importlib.util.module_from_spec(bp_spec); bp_spec.loader.exec_module(bp)

CH = ("a man in his early thirties with a calm Near-Eastern face, high cheekbones, warm olive skin, "
      "deep brown eyes, a short dark full beard and long dark wavy hair parted in the middle")
INK = "inked biblical graphic-novel, a wide cinematic 16:9 composition, bold black ink outlines, cel-flat color, dramatic cross-hatched shadow, reverent"

# slug -> (prompt, ref)   ref: "crux" bare-torso | "risen" risen-face | None
PROMPTS = {
 "david_psalmist": (f"{INK}: the aged shepherd-king David seated at night, eyes lifted and mouth open as he SINGS a psalm aloud toward the stars, a lyre held in his arms, a small clay oil lamp beside him; a rolled scroll lies closed on the ground with its written face turned away so only its blank back and rolled edge catch the light and no writing shows at all; his weathered singing face fills the frame as the clear subject; Iron-Age Israelite wool robe; 1st-millennium-BC", None),
 "david_old_deathbed": (f"{INK}: the aged King David as a very old bare-headed man with loose grey hair dying peacefully on a low plain wooden bed in a bare stone Iron-Age Israelite chamber, wrapped only in simple undyed wool blankets, a few sons in plain robes standing quietly nearby, warm low lamplight; humble and plain, his head uncovered; 1st-millennium-BC", None),
 "worm_reproach": (f"{INK}: the suffering Christ ({CH}), stripped to a plain loin cloth and bowed low under scorn, a despised and rejected man, the pointing hands and dark shadows of mockers around the edges, his face lowered in anguish; absolutely NO literal worm anywhere in the image; dark, 1st-century", "crux"),
 "poured_out_bones": (f"{INK}: the crucified Christ ({CH}) hanging on the cross seen from below, both arms stretched wide and nailed along the wooden beam, his body weary and drawn, a plain dark sky behind; reverent, 1st-century", "crux"),
 "thirst_dust": (f"{INK}: an extreme tight CLOSE-UP of only the crucified Christ's ({CH}) face and throat, lips cracked and parched, mouth slightly open in thirst, eyes half-closed, head sunk low, the top of the rough cross-bar just behind his head; a hard shaft of light across the face; no full body, just the face filling the frame; reverent, restrained; 1st-century", "crux"),
 "convergence_on_cross": (f"{INK}: the crucified Christ ({CH}) seen from the front, both arms spread straight out wide and nailed to the full width of the wooden cross-beam, head lifted, against plain deep shadow; cinematic, 1st-century", "crux"),
 "crane_cross_soldiers": (f"{INK}: a wide view down the cross of Christ ({CH}), both arms stretched wide along the beam, toward Roman soldiers gambling small on the rocky ground far below; a plain dark sky above; 1st-century", "crux"),
 "the_turn": (f"{INK}: the risen Christ ({CH}) rising into warm golden light out of deep shadow, serene and alive, one open hand lifted; hopeful, 1st-century", "risen"),
 "risen_worshipper": (f"{INK}: the risen Christ ({CH}) standing alive and glorified in warm radiant light, arms opening as he declares the Father's name, a REAL bodily risen man (not a ghost, not transparent), a single closed HEALED nail-print flat in each open palm; triumphant restraint, 1st-century", "risen"),
 "finished_work": (f"{INK}: the risen Christ ({CH}) at rest in warm golden light, a finished work, calm and complete, one open hand bearing a closed HEALED nail-print resting open; resolved and peaceful, NO words or text; 1st-century", "risen"),
 "storm_over_jerusalem": (f"{INK}: a vast wide view of three rough wooden crosses on a rocky hill above the ancient walled city of Herodian Jerusalem, the great Second Temple with its broad pale limestone platform and colonnaded courts and a plain golden facade dominating the city skyline, under a black thunderous noon sky torn by a single pale shaft of light onto the central cross; historically accurate 1st-century Jerusalem, dwarfing epic scale", None),
 "parting_storm_light": (f"{INK}: a wide view of the cross on the hill as the black storm finally PARTS and warm golden light floods down over it and over the small bowed figures gathered below, darkness breaking into dawn; hopeful, grace; 1st-century", None),
 "mockers_wag_heads": (f"{INK}: a knot of 1st-century onlookers at the foot of a cross laughing the sufferer to scorn, shooting out the lip and shaking their heads, three distinct scornful foreground faces and a dark featureless silhouette crowd behind; dusty earth tones; not cartoonish; 1st-century", None),
 "scribe_over_manuscripts": (f"{INK}: an ancient Near-Eastern bearded scribe-copyist bent in concentration over spread parchment manuscripts by lamplight, a reed pen in hand, his thoughtful weathered face the clear focus, the writing on the parchments only faint indistinct strokes with NO legible letters; period robes, NOT modern, NOT medieval; antiquity", None),
 "disputed_word_marks": (f"{INK}: an extreme macro of a worn, faded, weathered ancient parchment surface in warm lamplight, its writing almost entirely rubbed away to soft brown smudges and a few broken hairline ink specks - abstract texture only, deliberately blank and unreadable, with no letters, no characters, no words anywhere; antiquity", None),
 "greek_ot_scroll": (f"{INK}: an ancient open papyrus SCROLL unrolled on a wooden table in warm lamplight, its surface bearing only faint even rows of tiny indistinct ink flecks reading as soft grey texture with no letters, no title and no readable words anywhere; clearly a rolled papyrus scroll, not a bound book; antiquity", None),
 "ends_of_earth": (f"{INK}: a vast cinematic-epic wide - a great multitude of people from every nation streaming from the far horizons toward a single cross lifted on a hill catching warm light, dwarfing scale, countless tiny figures flowing home across the land; awe, epic", None),
 "ends_of_earth_faces": (f"{INK}: inked close portraits of a few diverse faces from different nations lifting their eyes with dawning hope and turning toward warm light; reverent, different peoples", None),
}
REFMAP = {"crux": REF_CRUX, "risen": REF_RISEN}


def call(prompt, dest, ref):
    if dest.exists() and dest.stat().st_size > 0:
        return "skip"
    body = {"model": MODEL, "prompt": prompt + bp.STYLE + bp.ONE, "size": SIZE,
            "response_format": "url", "watermark": False}
    if ref is not None:
        body["image"] = bp._ref_to_field(str(ref)); body["sequential_image_generation"] = "disabled"
    req = urllib.request.Request(BASE, data=json.dumps(body).encode(),
        headers={"Authorization": f"Bearer {bp._load_key()}", "Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=240) as r:
            resp = json.loads(r.read())
    except urllib.error.HTTPError as e:
        return f"HTTP {e.code}: {e.read().decode()[:200]}"
    url = resp.get("data", [{}])[0].get("url")
    if not url:
        return "no-url: " + json.dumps(resp)[:200]
    with urllib.request.urlopen(url, timeout=240) as im:
        dest.write_bytes(im.read())
    return "ok"


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--render", action="store_true")
    ap.add_argument("--only", default="")
    a = ap.parse_args()
    only = {s.strip() for s in a.only.split(",") if s.strip()}
    for slug, (prompt, refk) in PROMPTS.items():
        if only and slug not in only:
            continue
        ref = REFMAP.get(refk)
        print(f"\n{slug:24} ref={refk or 'NONE':5}")
        if a.render:
            print(f"   -> {call(prompt, OUT / f'{slug}.png', ref)}", flush=True)
    if not a.render:
        print(f"\n[list only] {len(PROMPTS)} fresh 16:9 stills @ {SIZE}. --render ~$0.72")


if __name__ == "__main__":
    main()
