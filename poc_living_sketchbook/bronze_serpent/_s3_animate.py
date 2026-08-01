"""Bronze Serpent episode -- step 3: animate the 11 NARRATIVE spreads (s08,
s12 are insert pages, already animated via the $0 deterministic
InsertPageCamera tool -- see _s3_animate_inserts.py, don't touch those; s14
is the torn-page landing, a deterministic device, not generative animation --
it does not belong in this JOBS list at all). Follows storm/_s3_animate.py's
exact pattern: imports the shared driver from poc_comic_page/
_animate_piece1_v2.py, reuses its LOCK/NOGLITTER-style camera-locked,
INVENT-NOTHING, named-ambient-motion-only prompting. Kling for multi-figure/
action/faces-under-pressure spreads, Seedance for everything else
(cost-tiered).

Count note (flagged, not silently fixed): the task briefing that spawned this
script said "12 narrative spreads." 14 total spreads - 2 insert pages (s08,
s12) = 12, which would include s14 -- but s14 is explicitly the deterministic
landing device and explicitly excluded from this list. The real count of
GENERATIVELY-ANIMATED narrative spreads is 11: s01, s02, s03, s04, s05, s06,
s07, s09, s10, s11, s13.

TEST GATE (2026-07-31): render ONLY s06_forge (Kling) + s10_golgotha
(Seedance) this round, per the project's standing test-gate discipline (2
real paid clips, human review, before any full batch). The other 9 spreads'
motion prompts are written and ready below so the script is complete for the
next round -- do NOT run them yet. Those 9 prompts are drafted from each
spread's own SCENE prompt (_s2_stills.py) + SHOT column (_TIMING.md), NOT yet
eye-verified against the actual rendered still at full resolution (SKILL.md
sec.8a requires that before animating) -- do that pass before next round.

  .venv\\Scripts\\python.exe poc_living_sketchbook/bronze_serpent/_s3_animate.py        # test gate (2 jobs)
  .venv\\Scripts\\python.exe poc_living_sketchbook/bronze_serpent/_s3_animate.py all     # full batch (next round)
  .venv\\Scripts\\python.exe poc_living_sketchbook/bronze_serpent/_s3_animate.py s01_wide,s02_grief  # explicit subset
"""
import contextlib
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
A.EPISODE = "LS_BronzeSerpent"
A.OUT = HERE / "clips"
A.OUT.mkdir(exist_ok=True)

STILLS = HERE / "stills"

LOCK = ("The camera does not move, zoom, or change angle at all. INVENT "
        "NOTHING new -- no new figures, objects, or marks appear; the paper "
        "texture, torn edges, and every sketch line hold perfectly still. ")
NOGLITTER = ("the light stays a steady, even glow -- it does not sparkle, "
             "flicker into particles, or scatter into glitter. ")

# TEST GATE default: exactly these 2 run unless overridden on the command line.
TEST_GATE = ("s06_forge", "s10_golgotha")

# (name, provider, duration, motion)
JOBS = [
    # NSFW-REJECTED twice on Seedance (2026-07-31, unclear cause -- likely a
    # false positive on the stricken-family group). Switched to Kling per
    # this project's own precedent (different moderation profile; already
    # working for s03_complaint in this same episode).
    ("s01_wide", "kling", 4,
     "Moses and the distant stricken family hold their exact positions and "
     "postures, perfectly still -- no steps, no gesture change, no turning "
     "toward or away from each other. Only: faint dust drifts low across the "
     "open ground, the distant tent fabric stirs very slightly in the wind. "
     "Nothing else changes."),

    ("s02_grief", "seedance", 4,
     "Moses and the stricken figure hold their exact positions and postures, "
     "perfectly still -- his reaching hand does not move closer or touch "
     "them, no new gesture. Only: the warm light on Moses's face breathes "
     "very gently. Nothing else changes."),

    # Multi-figure crowd gesture (raised hands) -- same tier reasoning as
    # storm's s03_screaming (three straining figures): Kling for
    # multi-figure/gesture fidelity, not Seedance.
    ("s03_complaint", "kling", 5,
     "Every figure in the complaining crowd holds their exact raised-hand "
     "gesture and posture perfectly frozen -- no new gesture, no stepping, "
     "no change of expression. Moses stands apart in his exact pose, "
     "unmoving. INVENT NOTHING new. Only: faint dust drifts across the "
     "ground, the sky beyond breathes very slightly. Nothing else in the "
     "frame changes."),

    # Multi-figure recoiling crowd + live serpents. Kling tier for the
    # crowd -- and the serpents themselves are LOCKED frozen, not given
    # named motion: the comic-grid-cost-tiered-animation memory documents
    # Kling specifically hallucinating "a coiled serpent uncoiled and
    # slithered" on a different project's panel. Same content class here,
    # so no serpent motion is offered at all, only ambient dust/shadow.
    # Prompt rewritten (2026-07-31) after the still itself was fixed for a
    # crowd-face violation (7-8 sharp faces -> exactly 2: a grieving man
    # clutching his own forehead, a distressed woman with one hand on her
    # chest and the other raised toward a tent flap). Original prompt below
    # described "recoiling Israelites... raised arms" -- language written
    # for the OLD 7-8-person still, no longer accurate. Serpent-lock
    # language (no uncoiling/slithering) carried over unchanged -- still the
    # right guardrail regardless of headcount, per the documented Kling
    # serpent-hallucination risk.
    ("s04_serpents", "kling", 5,
     "Every serpent on the ground holds its EXACT current coiled shape and "
     "position, perfectly frozen -- no serpent moves, uncoils, or slithers "
     "anywhere in the frame. The man's hands stay exactly clutched to his "
     "own forehead, his posture unmoving. The woman's hand stays exactly "
     "where it rests on her chest, and her other hand stays exactly raised "
     "toward the tent flap, at its current height and angle -- it does not "
     "lower, lift further, or change position. Neither figure steps, turns, "
     "or changes expression. INVENT NOTHING new -- no new figures, marks, "
     "or objects appear anywhere. Only: faint dust drifts low across the "
     "ground, the tent fabric behind them stirs very slightly in the wind. "
     "Nothing else in the frame changes."),

    ("s05_intercession", "seedance", 4,
     "Moses holds his exact kneeling posture, head bowed and hands lifted, "
     "perfectly still -- no gesture change, no head movement. Only: faint "
     "dust drifts across the open ground, the vast sky beyond him breathes "
     "very slightly. Nothing else changes."),

    # === TEST GATE JOB 1 of 2 (this round) ===
    # Eye-checked at full resolution before writing this prompt: the hammer
    # is already at/just above the glowing serpent on the anvil with sparks
    # already bursting between them -- i.e. the still itself is a frozen
    # mid-strike moment, not a wind-up.
    #
    # RE-ROLL (2026-07-31, 1st Kling attempt): the hammer descended visibly
    # toward the metal between first and last frame (sparks vanished, the
    # serpent's coiled shape flattened into a plain hook, a new bright
    # white-hot blob appeared at the contact point). 2nd Kling attempt
    # (tightened to Storm's p5a "pixel-for-pixel identical... like statues"
    # language, glow-pulse only, no spark drift) FAILED WORSE: a full
    # down-then-back-up hammer swing (a bright blown-out flash at contact
    # mid-clip, hammer ends RAISED HIGHER than its start position). Both
    # rejects parked in clips/_rejected/ (v1/v2) -- matches the exact
    # failure mode `comic-grid-cost-tiered-animation` already documents for
    # Kling on a different project ("a frozen hammer-strike continued its
    # swing"). Per SKILL.md sec.4, two real content failures -> switch
    # models; user approved ONE Seedance attempt (2026-07-31).
    #
    # 3rd attempt: SEEDANCE, reverting to the v1 attempt's language style
    # (plain "holds its exact position" framing, not Kling-tier "pixel-for-
    # pixel identical... like a statue" redundancy -- that extra emphasis
    # didn't help Kling and there's no evidence it's needed on a different
    # model/prompt-parser) -- but restoring v1's explicit named-anatomy list
    # (hammer, gripping hand, forearm, tongs-hand, serpent shape) instead of
    # v2's shorter list, since naming every part explicitly is strictly more
    # information, never looser. Motion restored to v1's ambient-spark-
    # drift-only pairing (sparks already in the air drift/fade + the glow
    # pulses) rather than v2's glow-only -- s10_golgotha's own successful
    # Seedance prompt on this episode also names more than one small ambient
    # motion (cloud drift) without issue, so a second small named motion is
    # not itself the risk; not looser than v1 on any axis.
    #
    # RESULT (2026-07-31, Seedance attempt): FAILED THE SAME WAY. First/
    # mid/last frame eye-check (clips/_verify_frames_seedance/s06v3_*.png)
    # shows the hammer visibly descending across the clip -- first frame has
    # a clear gap between hammer face and the coiled serpent with sparks
    # flying in that gap; by the mid frame the hammer head is already
    # touching the coil and the coil's shape has flattened/shifted under it;
    # by the last frame the hammer is buried into the metal with a bright
    # blown-out contact flare and the coil compressed further. Same
    # invented-strike defect as both Kling rejects, now on a 3rd model
    # config. Reject parked as clips/_rejected/s06_forge.v3_seedance_reject.mp4.
    # This is now a 3-STRIKES case (2x Kling + 1x Seedance, all three
    # inventing the same hammer-strike motion despite three different
    # prompt strategies) -- per SKILL.md sec.4 this is a USER decision, not
    # a silent retry or fallback build. clips/s06_forge.mp4 does not exist;
    # the JOBS entry below is left pointing at "seedance" only as the
    # last-tried config, NOT a recommendation -- do not re-run this job
    # unattended. The $0 deterministic ffmpeg push-in fallback is the
    # documented next step, pending the user's go-ahead.
    #
    # RESOLVED (2026-07-31, user go-ahead): generative animation abandoned
    # for this spread after the 3-strikes case above. clips/s06_forge.mp4 is
    # now a $0 deterministic InsertPageCamera push-in over the static still
    # (open on the full composition, slow push toward the hammer/anvil,
    # zoom 1.00->1.35, 5.0s, no raking-light) -- guaranteed no invented
    # motion since it's a pure crop+resize of one frame, at the cost of
    # losing the spark/glow animation this JOBS entry was written for.
    # REMOVED FROM JOBS (below) so no future full-batch run re-attempts
    # Kling/Seedance on this spread -- clips/s06_forge.mp4 already exists
    # and should be left alone. The motion-prompt text above is kept for
    # the historical record only, not for re-use.

    ("s07_horizon", "seedance", 4,
     "Moses's face holds its exact expression and gaze, turned toward the "
     "unseen light, perfectly still -- no blink, no head turn. Only: the "
     "faint warm light off-frame on one side of his face breathes very "
     "gently. Nothing else changes."),

    ("s09_shadow", "seedance", 4,
     "Moses holds his exact pose, lowered gaze, and grip on the bronze "
     "serpent low at his side, perfectly still -- the serpent does not "
     "lift, rise, or change position. Only: the shade across his face "
     "breathes very gently as the light shifts. Nothing else changes."),

    # === TEST GATE JOB 2 of 2 (this round) ===
    # Eye-checked at full resolution before writing this prompt: Christ's
    # hands (both pierced by the crossbeam nails per the drawing's own
    # linework at the wrist/palm) and feet crossed at the upright's base
    # show NO wound, NO blood, NO red mark anywhere -- confirmed clean.
    # Seedance chosen per the task's explicit instruction (wound-regeneration
    # risk documented in living-light-no-fresh-blood: Kling has REGENERATED
    # blood from crucifixion iconography alone even on a retouched-clean
    # still; Seedance has not shown this failure in this project's history).
    # Motion kept to the minimum offered: sky only, nothing on Christ's body
    # at all, camera locked.
    ("s10_golgotha", "seedance", 4,
     "The camera does not move, zoom, or change angle at all. Christ's "
     "entire body, the cross, and His head, arms, hands, and feet hold "
     "their EXACT current position and shape, perfectly still -- His hands "
     "and feet stay exactly as drawn, with no wound, no blood, no red mark, "
     "no nail, no puncture appearing or growing anywhere on them at any "
     "point in the clip. INVENT NOTHING new -- no new figures, marks, or "
     "objects appear anywhere in the frame. Only: the dark clouds in the "
     "sky behind Him drift very slowly and evenly. Nothing else in the "
     "frame moves."),

    ("s11_hearme", "seedance", 4,
     "Moses holds his exact seated pose and searching expression, perfectly "
     "still -- no head turn, no gesture, his open hands do not move. Only: "
     "faint dust drifts across the ground behind him. Nothing else "
     "changes."),

    # Same crucifixion-iconography wound-regeneration risk as s10 (see that
    # job's comment) applies here too -- Christ radiant on the cross, arms
    # outstretched. Seedance chosen over Kling for the same reason, even
    # though this is not a multi-figure/action shot; the wound risk
    # dominates the tiering call. Longer hold (8s) matches storm's own
    # precedent for a pivotal glory beat (s08_verse, s04_asleep = 8s).
    ("s13_lifted", "seedance", 8,
     "The camera does not move, zoom, or change angle at all. Christ's "
     "entire body, the cross, and His head, arms, hands, and feet hold "
     "their EXACT current position and shape, perfectly still -- His hands "
     "and feet stay exactly as drawn, with no wound, no blood, no red mark, "
     "no nail, no puncture appearing or growing anywhere on them at any "
     "point in the clip. INVENT NOTHING new. Only: the warm gold light "
     "around and behind Him pulses very gently brighter and dimmer in a "
     "steady, even glow -- " + NOGLITTER + "Nothing else in the frame "
     "moves."),
]


@contextlib.contextmanager
def _note_override(note):
    """A.run_job's cost.record_hf call hardcodes note=f"[piece1-v2] {name}"
    (confirmed in data/spend_ledger.jsonl -- every LS_Storm animate row
    carries that literal prefix even though episode="LS_Storm" is correct).
    Rather than fork run_job's ~40 lines of subprocess/curl/retry logic just
    to change one string, patch cost.record_hf for the duration of one call.
    `A.cost` and `pipeline.cost` are the same module object (A did
    `from pipeline import cost`), so this also affects any other importer."""
    orig = A.cost.record_hf
    def patched(*a, **kw):
        kw["note"] = note
        return orig(*a, **kw)
    A.cost.record_hf = patched
    try:
        yield
    finally:
        A.cost.record_hf = orig


def main(only=None):
    jobs = JOBS if only is None else [j for j in JOBS if j[0] in only]
    A.cost.record_stage(A.EPISODE, "animate_start", note=f"{len(jobs)} jobs")
    results = []
    for name, provider, dur, motion in jobs:
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
        with _note_override(f"[bronzeserpent] {name}"):
            ok, used = A.run_job_with_fallback(name, provider, still, "9:16", prompt, duration=dur)
        if not ok:
            status = "FAILED"
        elif used == provider:
            status = "clean"
        else:
            status = f"clean (fallback:{used})"
        results.append((name, status))
    A.cost.record_stage(A.EPISODE, "animate_end", note=f"{len(results)} jobs processed")
    print("\n=== summary ===")
    for name, status in results:
        print(f"  {name}: {status}")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        arg = sys.argv[1]
        only = None if arg == "all" else arg.split(",")
    else:
        only = list(TEST_GATE)
        print(f"[test-gate] running {only} -- pass 'all' or an explicit list to override")
    main(only)
