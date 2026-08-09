"""Seed of the Woman LONG -- animate stage. Spreads 1-5 promoted from the
POC30 process-validation test (memory `day-of-atonement-retro-learnings`);
extend JOBS as the full plan is authored. Reuses the shared
driver from poc_comic_page/_animate_piece1_v2.py (run_job_with_fallback),
same pattern day_of_atonement/_s4_animate.py follows -- fix #9 (check the
sibling episode's real script chain, don't assume a generic skill applies).
Only 2 clips for this tiny excerpt: s02 (multi-figure -> Kling, per the
locked comic-grid cost-tiering) and s04 (calm single light-presence ->
Seedance).

  .venv\\Scripts\\python.exe poc_living_sketchbook/seed_of_the_woman/_s4_animate.py
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "poc_comic_page"))
import _animate_piece1_v2 as driver  # noqa: E402

HERE = Path(__file__).resolve().parent
STILLS = HERE / "stills"
driver.OUT = HERE / "clips"
driver.OUT.mkdir(parents=True, exist_ok=True)
driver.EPISODE = "SeedOfTheWoman"

LOCK = ("The camera does not move, zoom, or change angle at all. INVENT "
        "NOTHING new -- no new figures, objects, or marks appear; the "
        "paper texture, torn edges, and every sketch line hold perfectly "
        "still. ")
PAGE = ("A finished ink-and-watercolor drawing on an aged sketchbook page, "
        "filmed as a perfectly still page under steady light. The framing "
        "stays fixed and locked for the entire clip. The drawing is "
        "finished and dry: every figure, face, hand, and object in it is "
        "ink on paper and stays exactly as drawn from the first frame to "
        "the last. ")

JOBS = [
    # test-tier (2026-08-07, independent-review staged build order): the
    # hardest identity+motion still in the episode -- Adam+Eve+serpent,
    # multi-figure, per the locked comic-grid cost-tiering (Kling for
    # action/crowd/complexity). Same house convention as every other job
    # here: the STILL already carries the completed pose (arm extended,
    # Eve turning), the CLIP only adds named ambient motion -- never a new
    # gesture, per this project's own camera-locked/invent-nothing rule.
    ("s06_blame_circle", "kling", 5,
     PAGE + LOCK +
     "Both human figures and the serpent hold their exact positions and "
     "postures, perfectly still -- Adam's extended arm does not move "
     "further, Eve's turning head does not turn further, the serpent "
     "does not move at all. Only: the surrounding leaves stir very "
     "slightly in a light breeze, and the light breathes very gently. "
     "Nothing else changes."),
    ("s02_the_hiding", "kling", 5,
     PAGE + LOCK +
     "Both figures hold their exact crouched positions and postures, "
     "perfectly still -- neither turns, stands, or shifts weight. Only: "
     "the surrounding leaves and ferns stir very slightly in a light "
     "breeze, and the light breathes very gently. Nothing else changes."),
    ("s04_god_walking", "seedance", 4,
     PAGE + LOCK +
     "The trees, canopy, and ground hold their exact shapes and "
     "positions, perfectly still -- no figure of any kind ever appears. "
     "Only: the golden light drifts and breathes gently through the "
     "canopy, and a few motes of dust/pollen drift slowly in the beams. "
     "Nothing else changes."),
    # s51: Christ on the cross -- Seedance ONLY, per this repo's own
    # locked rule (living-light-no-fresh-blood / CLAUDE.md "Comic-grid
    # cost-tiered animation"): Kling regenerates wounds/blood even on a
    # retouched-clean wound-free still. Never Kling for this content.
    ("s51_bearing_wages", "seedance", 4,
     PAGE + LOCK +
     "The figure upon the cross holds His exact bowed pose, perfectly "
     "still -- His head does not lift, His hands do not move or grip "
     "further, nothing about His posture changes. Only: His hair and the "
     "edge of His garment stir very slightly as if in a faint breath of "
     "wind, and the thin gold-leaf edge of the page catches the light "
     "very faintly. Nothing else changes -- no new wound, mark, or "
     "detail ever appears."),
    # batch 2 (2026-08-08, spreads 7-15) -- device column per _PLAN.md
    ("s08_coming_apart", "seedance", 4,
     PAGE + LOCK +
     "Both figures hold their exact separated positions and turned-away "
     "postures, perfectly still. Only: the few leaves already falling "
     "between them continue drifting slowly down, and the light breathes "
     "very gently. Nothing else changes."),
    ("s10_judgment_falls", "seedance", 4,
     PAGE + LOCK +
     "The garden canopy below holds its exact shape, perfectly still. "
     "Only: the single long shadow already crossing it grows very "
     "slightly longer and darker as the moment holds, extending further "
     "across the trees. Nothing else changes."),
    ("s11_afraid_of_presence", "kling", 5,
     PAGE + LOCK +
     "Both figures hold their EXACT crouched positions and their EXACT "
     "head angle and gaze direction, perfectly still -- neither turns, "
     "stands, shifts weight, or turns their head even slightly toward "
     "the other person. The man does not turn to face the woman; the "
     "woman does not turn to face the man; their gazes do not meet at "
     "any point in the clip -- both keep looking in their own original "
     "direction the entire time, exactly as in the first frame. Only: "
     "the surrounding leaves and ferns stir very slightly in a light "
     "breeze, and the light beyond the trunks breathes very gently. "
     "Nothing else changes."),
    ("s12_creatures_word", "seedance", 4,
     PAGE + LOCK +
     "Her turned profile holds its exact position, perfectly still, and "
     "the serpent does not move at all -- not one coil shifts. Only: the "
     "branches and leaves around them sway very slightly in a light "
     "breeze. Nothing else changes."),
    # batch 3 (2026-08-08, spreads 17-25) -- device column per _PLAN.md
    ("s17_not_adam_not_eve", "kling", 5,
     PAGE + LOCK +
     "Both figures hold their EXACT braced positions and their EXACT head "
     "angle, perfectly still -- neither turns, stands, or shifts weight, "
     "and neither turns their head toward the other or toward the "
     "camera. Only: the surrounding leaves stir very slightly in a light "
     "breeze, and the light breathes very gently. Nothing else changes."),
    ("s18_turns_to_serpent", "seedance", 4,
     PAGE + LOCK +
     "The serpent does not move at all -- not one coil shifts, not one "
     "muscle. Only: the light falling on it breathes and brightens very "
     "gently, as if slowly settling onto it. Nothing else changes."),
    ("s20_pure_curse", "seedance", 4,
     PAGE + LOCK +
     "The serpent's exact flattened position and posture do not change "
     "at all -- it does not move, coil, or shift. Only: fine dust "
     "settles very slowly around its body, drifting down and coming to "
     "rest. Nothing else changes."),
    ("s24_before_their_sentences", "kling", 5,
     PAGE + LOCK +
     "Both figures hold their EXACT waiting positions and EXACT head "
     "angle, perfectly still -- neither turns, stands, shifts weight, or "
     "turns their head toward the other. Only: the soft presence-light "
     "in the corner of the frame breathes very gently. Nothing else "
     "changes."),
    # batch 4 (2026-08-08, spreads 26-35) -- device column per _PLAN.md
    ("s28_clue_lights_up", "seedance", 4,
     PAGE + LOCK +
     "Eve holds her exact seated position and posture, perfectly still "
     "-- she does not move, turn further, or shift at all. Only: the "
     "single warm point of light far in the distance grows very "
     "slightly brighter and warmer as the moment holds, and the "
     "surrounding forest breathes gently in the low light. Nothing else "
     "changes."),
    # s30: _PLAN.md's own "designed ACTING spread" -- but the STILL
    # already carries the completed gesture (hands already gathered at
    # her heart, per _s2_stills.py's MARY block), so "motion completes,
    # holds" is satisfied by the still itself, not by asking Kling to
    # invent a hand movement live. Same frozen-tableau+ambient-only
    # discipline as every other job here -- deliberately NOT an
    # open-ended acting prompt, given this project's own hard-won lesson
    # about Kling inventing unwanted gesture/head-turn motion (s11).
    ("s30_annunciation", "kling", 5,
     PAGE + LOCK +
     "The bowed figure holds her EXACT position, posture, and hand "
     "gesture, perfectly still -- she does not move, turn, or shift, "
     "and her hands do not move further at all. Only: the light above "
     "her breathes and shifts very gently, and the edge of her veil "
     "stirs almost imperceptibly. Nothing else changes."),
    # s33: the one spread this batch asked for genuinely striking motion
    # (user, 2026-08-08) -- a deliberate slow push toward the gold point,
    # camera-only per this project's own locked "camera moves, nothing
    # else invented" rule. Longer duration (8s vs the usual 4s) so the
    # push reads as a real continuous movement across most of the real
    # spread length, not a short clip padded out by a static hold.
    ("s33_trajectory", "seedance", 8,
     PAGE + LOCK.replace("does not move, zoom, or change angle at all", "does not change angle, and does not invent any new content") +
     "The camera slowly, steadily pushes inward along the diagonal "
     "sweep of fanned pages, drawing closer toward the single point of "
     "warm gold light at the frame's edge -- a smooth, continuous, "
     "unhurried push, never a jump or cut. Every page and book holds "
     "its EXACT shape, position, and fanned arrangement, perfectly "
     "still -- no page turns, lifts, or moves at all. Only: the camera "
     "moves closer, and the gold light grows very slightly brighter and "
     "warmer as it is approached. Nothing else changes."),
    # batch 5 (2026-08-08+, spreads 36-45) -- s41/s44 both get a real
    # deliberate camera move (same fix as s33, per this session's own
    # lesson that ambient-only LOCK reads as "very basic" camera when the
    # beat calls for real presence -- _PREFLIGHT calls both of these
    # "ESCAPE" shots, the movement's hero wides). s43 stays ambient-only
    # on purpose: a genuinely brief (4.6s) ground-level beat that "lives
    # in the composition, no card" per _PLAN.md -- not every beat needs a
    # camera move, and a hard push on a floor-height crowd crop would
    # invent drama the text doesn't ask for.
    # REDESIGNED (2026-08-08, re-roll 1): duration=6 isn't a valid
    # seedance1_5 value (only 4/8/12 -- the estimator doesn't validate
    # this, the API call does), so the driver silently fell back to
    # Kling -- which then invented real page-fold changes on several
    # page-tips between frames (caught by eye-checking start/mid/end
    # frames, not assumed clean because the render succeeded). Fixed to
    # a valid seedance duration (8s, matching s33's own precedent) so
    # this stays on the intended calm-content provider.
    ("s41_shape_of_canon", "seedance", 8,
     PAGE + LOCK.replace("does not move, zoom, or change angle at all", "does not change angle, and does not invent any new content") +
     "The camera slowly arcs and glides along the length of the fanned "
     "pages, tracing their long curved sweep from one end toward the "
     "other in one smooth, continuous, unhurried movement -- a real "
     "camera move, not a static hold. Every page holds its EXACT "
     "fanned shape and position, perfectly still -- no page turns, "
     "lifts, curls, or shifts at all. Only: the camera itself moves "
     "along the arc, and the pages' own surface catches the light very "
     "faintly as the camera passes. Nothing else changes."),
    ("s43_under_your_feet", "kling", 5,
     PAGE + LOCK +
     "Every pair of feet in the crowd holds its EXACT position and "
     "stance, perfectly still -- none shift weight, step, or move at "
     "all. Only: the light falling across the stone breathes very "
     "gently. Nothing else changes."),
    # NOTE: duration=6 hit the same invalid-value fallback as s41 (only
    # 4/8/12 valid for seedance1_5) and this one also landed on Kling --
    # but eye-checked clean (figures/serpent held their exact shapes,
    # no invention), so the render itself was kept. Left the duration
    # at 6 here so a future --rebuild doesn't silently re-trigger the
    # same fallback without this note; change to 8 if this ever needs
    # a genuine re-render.
    ("s44_stands_on_one", "seedance", 6,
     PAGE + LOCK.replace("does not move, zoom, or change angle at all", "does not change angle, and does not invent any new content") +
     "The camera slowly, steadily pushes upward and inward toward the "
     "small figures on the high ground, a smooth continuous rise, "
     "never a jump or cut. Every figure and the serpent's coiled "
     "shadow hold their EXACT shapes and positions, perfectly still -- "
     "nothing shifts, no figure moves. Only: the camera moves closer "
     "and slightly upward, and the gold light grows very slightly "
     "warmer as it is approached. Nothing else changes."),
    # batch 6 (2026-08-09, spreads 46-55, "the crushing") -- device table
    # per _PREFLIGHT.md. s48 is the one sanctioned action-serpent frame
    # (Kling, the locked action-panel animator); the still ALREADY shows
    # the strike at contact, so the clip must hold that exact moment, not
    # complete or extend it -- per memory [[living-light-no-fresh-blood]]
    # (Kling reliably regenerates/invents blood near wound-adjacent
    # content, 5/5 + 3/3 reject history on a sibling project), an explicit
    # no-blood/no-new-mark line is added on TOP of the standard LOCK, not
    # trusted to the generic wording alone.
    ("s48_heel_strike", "kling", 5,
     PAGE + LOCK +
     "The serpent and the heel hold their EXACT positions, exactly as "
     "drawn -- the jaws do not close further, the heel does not move or "
     "flinch, no bite completes, no new contact occurs beyond what is "
     "already drawn. CRITICAL: no blood, no red mark, no wound, no new "
     "color of any kind ever appears anywhere in the clip -- the skin "
     "and the serpent's scales stay exactly as painted, first frame to "
     "last. Only: the loose dust and small stones on the ground shift "
     "and settle very slightly. Nothing else changes."),
    # s54: calm state-only "shadow deepens" per the device table -- the
    # coil is ALREADY a risen shadow-mass in the still (not a creature),
    # so the only legal motion is that shadow reading very slightly
    # darker/denser as the moment holds, matching s52's own wash-retreat
    # companion beat. Seedance, not Kling -- nothing wound-adjacent in
    # frame at all, but kept on the calm-content provider regardless.
    ("s54_seeming_win", "seedance", 4,
     PAGE + LOCK +
     "The shadow-mass of the coiled serpent and the small distant cross "
     "both hold their EXACT shapes and positions, perfectly still -- "
     "neither moves, grows, or shifts shape at all. Only: the shadow-mass "
     "reads very slightly darker and denser as the moment holds, and the "
     "unnatural midday darkness in the sky presses very slightly heavier. "
     "Nothing else changes -- no storm, no lightning, no wind, no new "
     "shape ever appears."),
]


def main():
    for name, provider, duration, prompt in JOBS:
        out = driver.OUT / f"{name}.mp4"
        if out.exists():
            print(f"[skip] {name}")
            continue
        still = STILLS / f"{name}.png"
        ok, used = driver.run_job_with_fallback(name, provider, still, "16:9", prompt, duration=duration)
        print(f"  -> {'ok' if ok else 'FAILED'} (provider={used})")


if __name__ == "__main__":
    main()
