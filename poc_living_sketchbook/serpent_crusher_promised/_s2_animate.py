"""The Serpent-Crusher Promised -- step 2: animate the 7 spreads whose
intended effect genuinely needs generated motion (s02/s05 are $0 devices,
see _kenburns.py).

Design pass per shot (not a mechanical wide=veo/close=kling split):
  s01 -- three listeners frozen mid-story, warm lamplight -- atmospheric
    light breathing is the whole ask, no body gesture -> veo3_1_lite
    (this cluster's proven strength for exactly this kind of shot).
  s03 -- LOCKED round 1, armor + unseen light arriving, no body gesture
    -> veo3_1_lite, matches this cluster's own precedent.
  s04 -- Paul's hand actually moving the pen is a real cued gesture ->
    Kling (veo does not reliably execute designed/cued motion, per this
    project's own bake-off).
  s06 -- LOCKED round 1, empty cross + shadow reaching a small distant
    crushed serpent -- atmospheric light/shadow only, serpent stays
    small and untouched -> veo3_1_lite.
  s07 -- the watchman's white-knuckled grip tightening, lamp flame
    catching, is a real cued gesture -> Kling, same precedent as heel_vs
    head's own s06 (hands gripping tighter under tension).
  s08 -- LOCKED round 1, the gold beam breathing brighter is pure
    atmosphere, no body gesture -> veo3_1_lite.
  s09 -- LANDING, Christ reverent radiant hold -> veo3_1_lite, this
    cluster's clearest proven win (matches heel_vs_head's own s07),
    POSITIVE-ONLY glow phrasing (the known glitter gotcha).

  .venv\\Scripts\\python.exe poc_living_sketchbook/serpent_crusher_promised/_s2_animate.py
"""
import importlib.util
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
HERE = Path(__file__).resolve().parent

spec = importlib.util.spec_from_file_location(
    "_anim", ROOT / "poc_comic_page" / "_animate_piece1_v2.py")
A = importlib.util.module_from_spec(spec)
spec.loader.exec_module(A)
A.EPISODE = "LS_SerpentCrusherPromised"
A.OUT = HERE / "clips"
A.OUT.mkdir(exist_ok=True)

STILLS = HERE / "stills"

LOCK = ("The camera does not move, zoom, or change angle at all. INVENT "
        "NOTHING new -- no new figures, objects, or marks appear; the paper "
        "texture, torn edges, and every sketch line hold perfectly still. ")

# (name, provider, duration, motion)
# 2026-08-15: s01/s03/s08/s09 were originally veo3_1_lite (atmospheric-only,
# no cued gesture) but the user watched real playback and called them too
# static/Ken-Burns-equivalent -- moved to Kling per the Heel vs Head s01/s04
# precedent (frame-strip brightness diffs are not proof of visible motion).
JOBS = [
    ("s01_recap_curse", "kling", 5,
     "All three figures hold their exact pose and position, perfectly "
     "still -- no one moves, speaks further, or changes expression. "
     "Only: the small oil lamp's flame breathes very gently, flickering "
     "warm light and soft shadow across the three faces. Nothing else "
     "in the frame changes."),

    ("s03_armor_set_aside", "kling", 5,
     "The armor and sword hold their exact position, perfectly still -- "
     "nothing shifts or falls. Only: the soft unseen light falling on "
     "the armor breathes very gently brighter and dimmer, as if an "
     "unseen presence has just arrived. Nothing else in the frame "
     "changes."),

    ("s04_pauls_letter", "kling", 5,
     "The hand holding the reed pen completes ONE slow, deliberate "
     "stroke -- the pen tip moves a short distance along the parchment, "
     "leaving a new short line of ink behind it -- then the hand lifts "
     "very slightly and holds still for the rest of the clip. The "
     "person's face and body stay out of frame the whole time. INVENT "
     "NOTHING new otherwise. Nothing else in the frame changes."),

    ("s06_empty_cross_shadow", "veo", 4,
     "The cross and the small distant serpent's head both hold their "
     "exact position, perfectly still -- neither moves at all. Only: "
     "the shadow on the ground breathes very gently, deepening and "
     "lightening slightly, as if a cloud is passing far overhead. "
     "Nothing else in the frame changes."),

    ("s07_night_watchman", "kling", 5,
     "The watchman's hands complete ONE slow, small motion -- gripping "
     "the stone coping noticeably tighter, knuckles tensing -- while "
     "the small lamp flame beside him catches and flickers once, "
     "brighter for a moment. Then everything holds still for the rest "
     "of the clip. His face and posture otherwise stay exactly as they "
     "are. INVENT NOTHING new otherwise. Nothing else in the frame "
     "changes."),

    ("s08_gold_thread_bridge", "kling", 5,
     "The dark storm-garden scene and the small distant serpent's head "
     "hold their exact position, perfectly still. Only: the gold beam "
     "of light breathes very gently, growing a little brighter and more "
     "radiant, alive and warm, exactly as golden as it already is, "
     "unchanged in color. Nothing else in the frame changes."),

    ("s09_landing_christ_in_arch", "kling", 5,
     "Christ stays perfectly frozen in His exact pose, no movement at "
     "all, His extended hand held steady. The warm gold light flooding "
     "through the archway stays exactly as warm and steady as it "
     "already is, breathing very gently brighter and softer, alive and "
     "unchanged in color. Nothing else in the frame changes."),
]


def main():
    only = set(sys.argv[1:]) or None
    results = []
    for name, provider, dur, motion in JOBS:
        if only and name not in only:
            continue
        still = STILLS / f"{name}.png"
        out = A.OUT / f"{name}.mp4"
        if out.exists():
            print(f"[skip] {name}")
            results.append((name, "cached"))
            continue
        if not still.exists():
            print(f"[HOLD] {name}: still missing")
            results.append((name, "NO-STILL"))
            continue
        prompt = LOCK + motion
        ok, used = A.run_job_with_fallback(name, provider, still, "9:16", prompt, duration=dur)
        results.append((name, f"clean ({used})" if ok else "FAILED"))
    print("\n=== summary ===")
    for name, status in results:
        print(f"  {name}: {status}")


if __name__ == "__main__":
    main()
