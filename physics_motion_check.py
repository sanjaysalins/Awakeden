"""physics_motion_check.py — flag scenes whose motion is ONE-WAY / irreversible, so the
assembler must NOT boomerang them (a reverse runs gravity backwards: lots leap out of the
bowl, poured blood un-pours, smoke sucks downward, a strike rewinds).

The 16:9 assembler fills a scene's window by SLOW BOOMERANG (forward+reverse) for "static"
scenes. That reverse is fine for a frozen tableau with only a camera drift, but BREAKS any
scene depicting falling / pouring / dripping / casting-into-a-vessel / rising smoke / a
strike. Those need fill="forward_slow" (forward-only, time-stretched) instead.

This is the deterministic verification: scan each scene's subject_block + atmos for one-way
physics cues and recommend fill="forward_slow". Run it BEFORE assembling (or to audit a plan).

Usage:  python physics_motion_check.py longform/EW01_Two_Goats/v1/visual_16x9/scene_plan.json
        python physics_motion_check.py <plan> --apply   # write fill=forward_slow on flagged scenes
"""
import argparse, json, re, sys
from pathlib import Path

# one-way / gravity / irreversible motion — a reverse looks physically wrong
ONE_WAY = {
    "falling/dropping": r"\b(fall(s|ing|en)?|fell|drop(s|ping|ped)?|tumbl\w*|plung\w*)\b",
    "pouring/spilling": r"\b(pour(s|ing|ed)?|spill(s|ing|ed)?|splash\w*|tipp\w*|emptying)\b",
    "dripping/flowing": r"\b(drip(s|ping|ped)?|trickl\w*|flow(s|ing|ed)?|stream(s|ing|ed)?|runs? down|running down|bleeding)\b",
    "casting/throwing":  r"\b(cast(s|ing)?\s+(\w+\s+){0,2}(lots?|lot[- ]?stones?|the goat|stones?)|lot[- ]?stones?|throw(s|ing|n)?|toss(es|ing|ed)?|hurl\w*|fling\w*|flung|sending away|driven|drives)\b",
    "sprinkling":        r"\b(sprinkl\w*|scatter(s|ing|ed)?|spray\w*)\b",
    "rising smoke/fire": r"\b(rising\s+(smoke|incense|fire|flame)|smoke\s+ris\w*|incense\s+ris\w*|flames?\s+(leap\w*|ris\w*)|sparks?\s+ris\w*|embers?\s+ris\w*)\b",
    "strike/impact":     r"\b(strik\w*|struck|smites?|smit\w*|slay(s|ing)?|slain|kill(s|ing|ed)?|shatter\w*|breaking)\b",
    "walking/locomotion":r"\b(walk(s|ing)?|stride\w*|march(es|ing)?|running|runs|approach\w*|departing|leaving|fleeing)\b",
}
# soft cues that only matter if combined with a vessel
VESSEL = r"\b(bowl|basin|vessel|cup|laver|altar|bason)\b"


# things that look like motion but are static (a cast shadow that "falls", an emptying court)
STATIC_FP = re.compile(r"\b(shadow|light)\b[^.]{0,40}\b(fall|falls|falling|cast)\b|emptying\s+(court|room|hall)|\bslain\b|\bkilled\b")


def scan(text):
    low = text.lower()
    hits = []
    for label, rx in ONE_WAY.items():
        for m in re.finditer(rx, low):
            frag = m.group(0)
            # skip a hit that sits inside a known static-phrase false positive
            ctx = low[max(0, m.start() - 30): m.end() + 10]
            if STATIC_FP.search(ctx) and label in ("falling/dropping", "strike/impact", "pouring/spilling"):
                continue
            hits.append((label, frag))
            break
    return hits


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("plan")
    ap.add_argument("--apply", action="store_true", help="write fill='forward_slow' on flagged scenes")
    args = ap.parse_args()
    p = Path(args.plan)
    d = json.loads(p.read_text(encoding="utf-8"))
    scenes = d["scenes"]
    flagged = []
    print(f"[physics] {p}  ·  {len(scenes)} scenes\n")
    for s in scenes:
        text = (s.get("subject_block", "") + " " + s.get("atmos", ""))
        hits = scan(text)
        # 'walking/locomotion' alone is handled by `directional`; only flag it if not already directional
        strong = [h for h in hits if h[0] != "walking/locomotion"]
        loco = [h for h in hits if h[0] == "walking/locomotion"]
        cur = s.get("fill") or ("directional" if s.get("directional") else "boomerang")
        if strong and cur == "boomerang":
            flagged.append(s["id"])
            print(f"  #{s['id']:02d} [FLAG] ONE-WAY MOTION (boomerang would reverse it) -> forward_slow")
            for lbl, frag in strong:
                print(f"       {lbl}: \"{frag}\"")
            print(f"       {s['title']}")
        elif loco and cur == "boomerang":
            print(f"  #{s['id']:02d} · locomotion ({loco[0][1]!r}) — review: boomerang ok if subject is static, else mark directional")
    print("\n" + "=" * 60)
    if flagged:
        print(f"FLAGGED (set fill='forward_slow'): {flagged}")
        if args.apply:
            for s in scenes:
                if s["id"] in flagged:
                    s["fill"] = "forward_slow"
            p.write_text(json.dumps(d, ensure_ascii=False, indent=2), encoding="utf-8")
            print(f"[applied] wrote fill='forward_slow' on {flagged} -> {p}")
        else:
            print("re-run with --apply to set fill='forward_slow' on them, then re-assemble.")
        return 1
    print("PASS — no one-way-motion scenes left on boomerang.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
