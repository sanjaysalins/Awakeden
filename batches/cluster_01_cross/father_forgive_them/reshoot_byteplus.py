#!/usr/bin/env python
"""RE-SHOOT all 12 pilot stills on the LOCKED new engine: BytePlus Seedream 4.5 + ref-lock.

Why: the old Higgsfield seedream path could not render a real nail (only a hole/cube-stud),
drifted to 4 different Jesus faces, and produced period errors (dog-bone 'lots', a power-pole).
BytePlus 4.5 + a face reference fixes all of it (proven in visual/_byteplus/DECISION.html).

This driver:
  - MODEL = seedream-4-5-251128 (4.5), 9:16 1440x2560
  - ref-locks EVERY panel to the canonical Christ face (bakeoff/_ref_small.png) -> one face
  - REAL forged iron nails through the hands on the close crucifixion beats (1,7) + consistent
    nailed hands on the wide beats (3,4,2); risen beats (10,11,12) = single HEALED round scar
  - astragali (knucklebone dice) not dog-bones; period houses/wall only, NO poles/wires
  - renders to visual/_byteplus/reshoot/ (old nbp/ untouched until approved). Idempotent.

  .venv\\Scripts\\python.exe batches/cluster_01_cross/father_forgive_them/reshoot_byteplus.py            # list prompts
  .venv\\Scripts\\python.exe batches/cluster_01_cross/father_forgive_them/reshoot_byteplus.py --render   # spend ~$0.45
  ...  --render --only 01b_nailed_hands,05_pierced_hand                                                  # a subset
"""
import argparse, importlib.util, json, urllib.request, urllib.error
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = Path(__file__).resolve().parents[3]
OUT = HERE / "visual" / "_byteplus" / "reshoot"; OUT.mkdir(parents=True, exist_ok=True)
REF = HERE / "visual" / "_byteplus" / "bakeoff" / "_ref_small.png"   # RISEN face ref (green robe)
REF_CRUX = HERE / "visual" / "_byteplus" / "nail_wide_45.png"        # bare-torso CRUCIFIED ref (real nail)
# the risen-face ref bleeds a green robe + wrist-cord onto the bare cross shots, so the crucifixion
# beats lock to the bare-torso nail ref instead (same man, right body, real nail through the palm).
REF_MAP = {
    "01b_nailed_hands": REF_CRUX, "01c_soldiers_gamble": REF_CRUX, "01_golgotha_hook": REF_CRUX,
    "02_jesus_prays": REF_CRUX, "03_prayer_close": REF_CRUX, "04_cast_lots": REF_CRUX,
    "05_pierced_hand": REF_CRUX, "06_cross_over_us": REF_CRUX, "06b_our_sin": REF_CRUX,
    # risen beats keep the risen-face ref (default REF)
}
MODEL = "seedream-4-5-251128"
SIZE = "1440x2560"
BASE = "https://ark.ap-southeast.bytepluses.com/api/v3/images/generations"

# reuse the proven client helpers (key loader, ref->data-url, style/one tails)
def _load(n, rel):
    s = importlib.util.spec_from_file_location(n, HERE / rel); m = importlib.util.module_from_spec(s)
    s.loader.exec_module(m); return m
bp = _load("bp", "byteplus_seedream.py")

# canonical descriptor (identity carried mainly by the ref; this reinforces it in words)
CHRIST = ("a man in his early thirties with a calm Near-Eastern face, a lean face with high "
          "cheekbones and a slightly aquiline nose, warm olive skin, deep brown eyes, a short dark "
          "full beard and long dark wavy hair parted in the middle")
NAIL = ("a single large hand-forged square black iron Roman nail driven straight down through the very "
        "CENTRE of the open palm — midway between the fingers and the wrist — deep into the wood, the "
        "broad flat forged nail-head resting flat against the pierced skin at the middle of the palm, "
        "dark red blood welling around the iron and running down the fingers")
LOTS = ("a small scatter of pale rounded river pebbles and a few broken reddish clay pottery shards "
        "lying in the dust (the lots they cast)")
BARE = ("bare-chested, wearing only a plain undyed white cloth wrapped at his hips")

# reading order = narration order (see visual_beats.md)
PROMPTS = {
 # 1 HOOK — "Nails through his hands." — THE real-nail macro (the shot the old set never had)
 "01b_nailed_hands": (
   "A stark close macro of BOTH of the crucified Christ's bare hands and forearms nailed to the dark "
   "rough wooden crossbeam, seen at a THREE-QUARTER ANGLE from the front and slightly above, the backs "
   "of the hands flat against the wood and the fingers relaxed, bare skin with nothing tied around the "
   "wrists. Through the middle of each hand is driven ONE short thick hand-forged square black iron "
   "Roman nail — BOTH nails identical in size and shape, each a stubby square spike with a broad flat "
   "forged head resting against the pierced skin at the centre of the palm, only a short length of iron "
   "showing, dark red blood welling around each nail and running down. Two matching nails, one per hand. "
   "Behind, a black storm sky. No face in frame. Reverent, visceral."),
 # 2 HOOK — "Soldiers at his feet, gambling for his clothes."
 "01c_soldiers_gamble": (
   "Three Roman soldiers in first-century legionary armour crouched low in the dust at the foot of the "
   f"cross, casting {LOTS} across the dust between them, their faces cold and indifferent, bent over "
   "their game. Above and behind them on the cross hangs the crucified Christ with EXACTLY TWO arms "
   "stretched straight out along the horizontal crossbeam, a forged iron nail through each open hand, "
   "his head bowed low toward his chest — only two arms and two hands, no praying hands, no extra arms. "
   "The base of the tall wooden upright is planted in rocky ground and rises out of the top of the "
   "frame. A dark storm sky; far in the distance only low flat-roofed pale limestone houses and a plain "
   "city wall. Filling the frame edge to edge as one continuous scene. Ancient Near-Eastern, period-accurate."),
 # 3 HOOK — "…a word no one expected." — WIDE reveal
 "01_golgotha_hook": (
   f"A WIDE dramatic view of the crucified Christ ({CHRIST}), {BARE}, on a tall rough wooden cross under "
   "a black storm sky, his head bowed, his bare arms stretched along the crossbeam, a forged black iron "
   "nail through the middle of each open palm into the beam, his bare feet nailed against the upright. "
   "Far below, a few small Roman soldiers. In the far distance only low flat-roofed pale limestone houses "
   "and a plain city wall, bare empty sky. Reverent, epic, desolate."),
 # 4 POINT — "It is a prayer… for the very people putting him to death." — full figure, two arms
 "02_jesus_prays": (
   f"The crucified Christ ({CHRIST}), {BARE}, on a wooden cross, his body hanging with EXACTLY TWO arms "
   "— one bare arm stretched straight out to each side, level and flat ALONG the horizontal crossbeam, "
   "both hands OPEN and flat against the beam, palms forward, a forged black iron nail through the middle "
   "of each open palm into the wood. His head is lifted and tilted back toward heaven, his face calm and "
   "softly lit, his lips parting as he speaks a prayer. A dark storm sky behind; far below, small Roman "
   "soldiers gather his garment. Correct human anatomy — only two arms and two open hands, arms straight "
   "along the beam. Reverent, merciful."),
 # 5 POINT — [jesus] "Father, forgive them…" — CLOSE face
 "03_prayer_close": (
   f"A CLOSE portrait of the crucified Christ ({CHRIST}), his face filling the frame, head lifted and "
   "eyes raised to heaven, brow strained, lips parted in prayer, a single warm shaft of light across his "
   "face against a dark storm sky, the rough wooden cross behind his head. Strong bold ink linework. "
   "Reverent, merciful, sorrowful."),
 # 6 PROOF — "…they parted his raiment, and cast lots." — ground-level lots macro
 "04_cast_lots": (
   "A ground-level close view in the dust at the foot of the cross: two weathered Roman soldiers' bare "
   f"hands casting {LOTS} across the dust, a heaped seamless white robe lying beside them, lit by the grey "
   "storm-broken daylight of the execution ground. Ancient Near-Eastern, period-accurate, no other objects."),
 # 7 PROOF — "…it intercedes for the sinner." — the real nail through the open mercy-hand (single hand)
 "05_pierced_hand": (
   "A CLOSE shot of the crucified Christ's single near hand and forearm, bare and outstretched along the "
   f"rough wooden crossbeam, the hand OPEN and flat, palm toward the viewer, and {NAIL}; his lifted "
   "bearded face soft-focus above and behind the hand. A dark storm sky, one warm shaft of light across "
   "the wounded open hand. Reverent, merciful — an open hand, not a fist."),
 # 8 CONVICTION — "the sin that put him there was ours too."
 "06b_our_sin": (
   "The long dark shadow of a tall cross falling across a small group of ordinary ancient Near-Eastern "
   "men and women standing with bowed heads, their faces in shadow beneath it, the weight of shared "
   "guilt; bare rocky ground, a dark storm sky. Reverent, sombre, period-accurate dress, no modern clothing."),
 # 9 CONVICTION — "He gave himself willingly —" — the cross from below
 "06_cross_over_us": (
   f"The crucified Christ ({CHRIST}) seen from below on a tall wooden cross planted on a rocky hilltop, "
   "one lone robed figure kneeling small at the foot, a single shaft of pale light breaking through the "
   "dark storm sky onto the cross. Reverent, epic, vertical."),
 # 10 CONVICTION — "…still lives to make intercession for sinners." — the LIVING risen Christ
 "06c_intercession_lives": (
   f"The living, risen Christ ({CHRIST}), standing calm in warm golden light, both hands lifted and OPEN "
   "in intercession, the CENTRE of EACH open palm marked by a single clear dark open nail-hole — a clean "
   "round pierced hole through the middle of the palm, dark red-brown, plainly open (not a faint dot, not "
   "a smooth circle, not a black star); the fingers and fingertips clean, natural and unmarked. A steady "
   "warm radiance around him, a plain bright background. His face calm, mature and at peace, the SAME man "
   "as the suffering Christ. Reverent, alive, merciful."),
 # 11 LANDING — "while we were yet sinners, Christ died for us." — gospel-wide, fully robed
 "07b_gospel_wide": (
   f"The risen Christ ({CHRIST}) stepping toward the viewer out of a bright ancient stone doorway flooded "
   "with warm golden morning light, wearing a FULL flowing cream robe and mantle that covers his chest, "
   "shoulders and body, his arms opening in welcome, both hands OPEN, the CENTRE of each open palm "
   "marked by a single clear dark open nail-hole — a clean round pierced hole through the middle of the "
   "palm, dark red-brown, plainly open (not a faint dot, not a smooth circle); the fingers and fingertips "
   "clean, natural and unmarked. Only his face, hands and bare feet uncovered. His face calm, mature and "
   "at peace, the SAME man as the suffering Christ. Inviting, triumphant, reverent."),
 # 12 LANDING (HERO) — "come, and receive it by faith." — the close risen hero
 "07_risen_hero": (
   f"A close hero portrait of the risen Christ ({CHRIST}), wearing a cream robe over his shoulders, his "
   "face calm and at peace, one hand OPEN and reaching gently toward the viewer. The centre of the open "
   "palm is marked by a single OLD HEALED SCAR — a thin dark closed puckered line-mark set FLUSH and "
   "LEVEL into the skin, drawn over in the same warm skin tone as the rest of the palm, dry and "
   "long-healed, lying completely flat within the surface of the skin, a shallow healed indentation "
   "with no colour of its own; the fingers and fingertips clean and unmarked. Warm golden light behind "
   "him. His face mature and at peace, the SAME man as the suffering Christ. Reverent, merciful, the "
   "mercy held out."),
}


def call(prompt: str, dest: Path, ref: Path) -> str:
    if dest.exists() and dest.stat().st_size > 0:
        return "skip"
    body = {"model": MODEL, "prompt": prompt + bp.STYLE + bp.ONE, "size": SIZE,
            "response_format": "url", "watermark": False,
            "image": bp._ref_to_field(str(ref)), "sequential_image_generation": "disabled"}
    req = urllib.request.Request(BASE, data=json.dumps(body).encode(),
        headers={"Authorization": f"Bearer {bp._load_key()}", "Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=240) as r:
            resp = json.loads(r.read())
    except urllib.error.HTTPError as e:
        return f"HTTP {e.code}: {e.read().decode()[:300]}"
    url = resp.get("data", [{}])[0].get("url")
    if not url:
        return "no-url: " + json.dumps(resp)[:300]
    with urllib.request.urlopen(url, timeout=240) as im:
        dest.write_bytes(im.read())
    return "ok"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--render", action="store_true")
    ap.add_argument("--only", default="", help="comma slugs; default = all 12")
    a = ap.parse_args()
    only = {s.strip() for s in a.only.split(",") if s.strip()}
    if not REF.exists():
        raise SystemExit(f"ref missing: {REF}")
    for i, (slug, prompt) in enumerate(PROMPTS.items(), 1):
        if only and slug not in only:
            continue
        ref = REF_MAP.get(slug, REF)
        if not a.render:
            print(f"[{i:2}] {slug}  (ref={ref.name})\n     {prompt[:150]}...\n")
            continue
        print(f"[{i:2}] {slug:24} ref={ref.name:18} -> {call(prompt, OUT / f'{slug}.png', ref)}", flush=True)
    if not a.render:
        print(f"\n[list only] 12 panels · model {MODEL}. Add --render (~$0.45).")
    else:
        print(f"\nDONE -> {OUT}")


if __name__ == "__main__":
    main()
