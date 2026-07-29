"""Comic Page Pipeline POC -- Rung 2, user-notes REDO batch 1 (2026-07-26).

User redo notes (from _REDO_PICKER.html):
  p2b  BOTH   -- twin-portrait of panel_a; new scene: Jesus inside, side view,
                 stepping toward the door to answer.
  p4a  BOTH   -- head-backwards anatomy; new scene: seeker seen FROM BEHIND
                 (no face = no head-twist risk), also de-dupes vs p5a.
  p5a  CLIP   -- still kept; animation redone with REAL motion (embrace) --
                 deliberate user-approved exception to the frozen discipline.
  p5c  BOTH   -- door-scene dupe of p4c; new scene: macro of the open latch.

Reuses _render_panel_stills.py's run()/AESTHETIC/CONSTRAINT/STYLE_TAIL, with
a period-corrected ANCHORS block (CP-G10: scroll not codex, head cloth,
ankle-length tunic -- the module's own ANCHORS predates the period fix).

  .venv\\Scripts\\python.exe poc_comic_page/rung2/_redo_batch1.py --step stills
  .venv\\Scripts\\python.exe poc_comic_page/rung2/_redo_batch1.py --step clips [--job p5a]
"""
import argparse
import re
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
import config  # noqa
from pipeline import cost  # noqa
import poc_comic_page.rung2._render_panel_stills as R  # noqa

HF = str(config.HF_CLI_PATH)
EPISODE = "CPP_Rung2_InNoWise"
HERE = Path(__file__).resolve().parent
STILLS = HERE / "stills"
CLIPS = HERE / "clips"
R1_STILLS = HERE.parent / "rung1" / "stills"

STILLS_CAP_USD = 2.00
CLIPS_CAP_USD = 3.50

# CP-G10 period-corrected anchors (the block in _render_panel_stills.py
# predates the period fix -- ledger book / short hair are WRONG there)
ANCHORS2 = (
    "CORE CHARACTER DESIGN ANCHORS:\n"
    "Jesus Christ: a lean Jewish man in his early thirties, shoulder-length "
    "dark wavy hair, full beard, deep-set compassionate eyes, wearing a "
    "simple undyed woolen robe with a rough-woven mantle. Dignified, gentle, "
    "welcoming presence. A teaching scene -- no wounds, no crown of thorns.\n"
    "The Seeker: a weary Judean man in his forties, full greying beard, "
    "shoulder-length hair under a simple head cloth, ankle-length rough-woven "
    "earth-tone tunic with a cloth girdle and a ragged mantle, worn leather "
    "sandals, carrying a worn papyrus scroll rolled on a wooden rod, tied "
    "with a frayed cord. Posture guarded, hopeful.\n"
    "The Door: a massive ancient SINGLE-leaf arch-topped wooden door, "
    "iron-banded, set in a rough stone wall."
)
PREFIX2 = R.AESTHETIC + "\n\n" + R.CONSTRAINT + "\n\n" + ANCHORS2 + "\n\n"

# (name, backup_suffix, aspect_ratio, ref_path, composition)
STILL_JOBS = [
    ("p2b_jesus_speaks", "v1_TWINPORTRAIT", "9:16", R1_STILLS / "panel_a_jesus.png",
     "Side view from within the lamplit house: Jesus seen in full profile, "
     "mid-stride toward the great closed door, his open hand reaching out "
     "toward the door's edge to draw it open, his face calm and certain, "
     "mouth gently open mid-word. The door carries NO bolt and NO lock -- "
     "only a simple worn wooden handle; its iron is hinge-bands only. Warm "
     "lamplight models his profile and robe against the heavy dark wood; "
     "cold darkness in the room's far corner. Same man as the reference. "
     "Lighting: warm interior lamplight, the door's wood glowing where his "
     "hand approaches."),

    ("p4a_turning_away", "v2_HEADTWIST", "9:16", HERE / "stills" / "p5a_the_welcome.png",
     "Seen from directly BEHIND: the Seeker walking away from the warm open "
     "doorway into cold blue darkness, only the BACK of his head cloth and "
     "his shoulders visible, head bowed low, the rolled scroll hanging heavy "
     "in one hand at his side, his long shadow thrown forward onto the "
     "stones ahead of him by the doorway light behind. Small in the lit "
     "doorway behind him stands Jesus, one hand lifted in patient appeal. "
     "Lighting: cold shadow ahead of the walking man, warm patient radiance "
     "spilling from the doorway behind him."),

    ("p5c_never_locked", "v1_DOORDUPE", "3:4", R1_STILLS / "panel_b_door.png",
     "Extreme close-up macro of the open door's edge: a hand-forged iron "
     "latch bar hanging straight DOWN, swung fully aside on its single "
     "pivot, touching nothing -- and beside it on the stone jamb its empty "
     "catch-plate with nothing resting in it. The door edge stands ajar, "
     "warm golden light through the gap glowing across worn wood grain and "
     "rough iron. The hanging bar and the empty catch are on the SAME side "
     "of the gap, nothing crosses the gap. No keyhole anywhere, no figures, "
     "no hands. Lighting: warm and settled, intimate hardware detail."),
]

# clip jobs: (provider, ar, seedance_duration, prompt)
CLIP_JOBS = {
    "p2b": dict(provider="seedance", ar="9:16",
                backup="v1_twinportrait",
                prompt=("The figure holds his exact mid-stride pose and reaching hand, "
                        "frozen. Only: the warm lamplight on his profile and the door "
                        "breathes gently brighter and softer, faint dust motes drift "
                        "through the light. No other movement.")),
    "p4a": dict(provider="seedance", ar="9:16",
                backup="v1_headtwist",
                prompt=("The walking figure and the figure in the doorway hold their "
                        "exact poses, frozen. Only: the warm doorway light behind pulses "
                        "softly, his long shadow on the stones flickers faintly with it, "
                        "his mantle hem stirs. No other movement.")),
    "p5c": dict(provider="seedance", ar="3:4",
                backup="v1_doordupe",
                prompt=("The composition holds its exact framing, the latch perfectly "
                        "still. Only: the warm light through the door gap breathes "
                        "softly along the iron and wood grain. No other movement.")),
    # THE exception: real, gentle motion -- user-approved embrace on the landing.
    # 10s (not 5): the page dwells 13.9s -- a longer take nearly kills the loop
    # (user 2026-07-26: the looped hold "feels like AI slop"). The embrace is
    # directed to COMPLETE early and then hold, so the calm tail extends
    # seamlessly to the dwell (directional motion must never boomerang).
    "p5a": dict(provider="kling", ar="1:1", duration="10",
                backup="v1_calmhold",
                prompt=("The camera does not move at all. Slowly, gently and with "
                        "dignity, Jesus draws the Seeker into a welcoming embrace: the "
                        "Seeker steps forward over the threshold as Jesus's extended arm "
                        "wraps around his shoulders, the Seeker's bowed head coming to "
                        "rest against Jesus's shoulder, Jesus's other hand rising to "
                        "rest on his back. The movement is slow, warm and natural, and "
                        "the embrace is fully complete by the middle of the clip -- for "
                        "the whole second half both men simply hold the finished embrace "
                        "perfectly still, breathing gently, nothing else moving. Both "
                        "faces keep exactly their appearance from the image -- same "
                        "features, same hair, same beards. The scroll stays in the "
                        "Seeker's hand. No new figures, marks or objects appear; the "
                        "door, archway and stonework do not move; the camera stays "
                        "fixed. The radiant doorway light glows warm and steady.")),
}


def _backup(path: Path, suffix: str):
    if not path.exists():
        return
    bak = path.with_name(f"{path.stem}.{suffix}{path.suffix}")
    if not bak.exists():
        path.rename(bak)
        print(f"   backed up -> {bak.name}")


def do_stills(only=None):
    spent = 0.0
    for name, bak_suffix, ar, ref, comp in STILL_JOBS:
        if only and not name.startswith(only):
            continue
        if spent >= STILLS_CAP_USD:
            print(f"STOP: stills cap ${STILLS_CAP_USD:.2f} reached")
            break
        out = STILLS / f"{name}.png"
        _backup(out, bak_suffix)
        prompt = PREFIX2 + R.CHAIN_LINE + f"SINGLE PANEL COMPOSITION: {comp}\n\n" + R.STYLE_TAIL
        print(f"[img ] {name} (AR {ar}, ref {ref.name}) ...", flush=True)
        t = time.time()
        ok = R.run(prompt, out, [ref], ar)
        if ok:
            try:
                row = cost.record_hf(EPISODE, "short", "stills", R.MODEL,
                                      note=f"[redo-batch1] {name}")
                spent += float(row.get("est_usd") or 0)
            except Exception as e:
                print(f"   (ledger skipped: {e})")
            print(f"   ok ({time.time()-t:.0f}s)  spend ~${spent:.2f}")
        else:
            print("   FAILED")
    print(f"[stills spend] ~${spent:.2f} of ${STILLS_CAP_USD:.2f} cap")


STILL_FOR = {
    "p2b": STILLS / "p2b_jesus_speaks.png",
    "p4a": STILLS / "p4a_turning_away.png",
    "p5c": STILLS / "p5c_never_locked.png",
    "p5a": STILLS / "p5a_the_welcome.png",
}


def do_clip(name):
    j = CLIP_JOBS[name]
    png = STILL_FOR[name]
    if not png.exists():
        print(f"   missing still: {png}")
        return False
    out = CLIPS / f"{name}.mp4"
    _backup(out, j["backup"])
    if j["provider"] == "seedance":
        model = "seedance1_5"
        extra = ["--duration", "4", "--resolution", "720p", "--aspect_ratio", j["ar"],
                 "--generate_audio", "false"]
    else:
        model = "kling3_0"
        extra = ["--mode", "pro", "--sound", "off", "--duration", j.get("duration", "5"),
                 "--aspect_ratio", j["ar"]]
    cmd = [HF, "generate", "create", model, "--start-image", str(png), "--prompt", j["prompt"],
           "--wait"] + extra
    print(f"[clip] {name} ({model}) ...", flush=True)
    t = time.time()
    r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    blob = (r.stdout or "") + "\n" + (r.stderr or "")
    if re.search(r"nsfw", blob, re.IGNORECASE):
        print("   NSFW-REJECTED")
        return False
    m = re.search(r'https?://\S+?\.mp4', blob)
    if not m:
        print(f"   no mp4 url: {blob.strip()[-500:]}")
        return False
    subprocess.run(["curl", "-s", "-L", m.group(0), "-o", str(out)], check=True)
    if out.exists() and out.stat().st_size > 0:
        try:
            cost.record_hf(EPISODE, "short", "animate", model, image=png,
                            note=f"[redo-batch1] {name}")
        except Exception as e:
            print(f"   (ledger skipped: {e})")
        print(f"   ok ({time.time()-t:.0f}s) -> {out}")
        return True
    print("   FAILED")
    return False


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--step", required=True, choices=["stills", "clips"])
    ap.add_argument("--job", default=None)
    a = ap.parse_args()
    if a.step == "stills":
        do_stills(a.job)
    else:
        names = [a.job] if a.job else list(CLIP_JOBS.keys())
        for n in names:
            do_clip(n)
