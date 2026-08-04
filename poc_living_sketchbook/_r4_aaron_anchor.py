"""living-sketchbook -- Aaron repo-level cast anchor (Day of Atonement episode).

Extends the same repo-level cast-bible system _r1_worldbible.py built for
Jesus/Disciples/Boat (and _r2_moses_anchor.py for Moses) with a fifth anchor:
AARON, needed because the Day of Atonement episode's repeated-element census
(SKILL.md sec.2) found Aaron on screen in nearly every spread -- without a
locked anchor he drifts face-to-face across the episode.

Age verified against explicit KJV numbers (feedback-verify-character-age-
scale-before-render): Exodus 7:7 states Aaron was 83 ("eighty and three
years old") when he and Moses confronted Pharaoh; Numbers 33:39 states he
was 123 when he died on Mount Hor, ~39 years later. He was ALREADY an old
man when he became high priest -- there is no young/middle-aged Aaron
anywhere in this story, same finding as Moses (see cast/MOSES.md). One
canon sheet covers his whole ~39-year tenure; no separate "elder Aaron"
anchor, per the same lesson that produced (then retired) MOSES_YOUNGER.md.

  .venv\\Scripts\\python.exe poc_living_sketchbook/_r4_aaron_anchor.py
"""
import importlib.util
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from pipeline import cost

spec = importlib.util.spec_from_file_location(
    "_e1", ROOT / "poc_castbible_look" / "episode_door" / "_e1_anchors.py")
E = importlib.util.module_from_spec(spec)
spec.loader.exec_module(E)

CAST = Path(__file__).resolve().parent / "cast"
CAST.mkdir(parents=True, exist_ok=True)
EPISODE = "LS_DayOfAtonement"

AARON_CANON = (
    "Aaron: an elderly Hebrew priest of the tribe of Levi, brother of Moses "
    "(Exodus 6:20), eighty-three years old when he became Israel's first "
    "high priest (Exodus 7:7), continuing in that office into extreme old "
    "age until his death at a hundred and twenty-three (Numbers 33:39) -- "
    "an old man in every appearance in this story, never young or "
    "middle-aged. Face geometry: a broad dignified brow, a straight strong "
    "nose, deep-set solemn eyes, full weathered cheeks, a composed and "
    "steady bearing -- a priest's stillness, not a wanderer's hardness. "
    "Hair: close-cropped white hair, cut short and neat. Beard: full, "
    "long, white, carefully kept -- a high priest's beard, not unkempt. "
    "Skin: sun-weathered olive Near-Eastern complexion, deeply lined at "
    "the eyes and brow. Build: a stouter, more solid frame than a "
    "wilderness wanderer's -- upright, dignified, a man who stands and "
    "ministers rather than travels, never frail. Eyes: dark, grave, "
    "holding both authority and a private fear before the veil. Hands: "
    "broad priestly hands, steady in ritual, never hurried. Garment: the "
    "plain holy linen of the Day of Atonement (Leviticus 16:4) -- a linen "
    "coat, linen breeches upon the flesh, a linen girdle, and a linen "
    "mitre, all unadorned white linen, nothing gold, nothing dyed -- a "
    "servant's plainness on the one most set apart, worn in nearly every "
    "appearance."
)

ANCHORS = [
    ("aaron_ref", AARON_CANON,
     "Editorial portrait, head to mid-chest, three-quarter view, calm "
     "solemn expression, warm light from one side -- the figure fills "
     "nearly the whole frame, minimal surrounding blank paper.", "1:1"),
]


def run(prompt, out, ar):
    import re
    import subprocess
    cmd = [E.HF, "generate", "create", E.MODEL, "--prompt", prompt,
           "--aspect_ratio", ar, "--resolution", "2k", "--wait"]
    p = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    blob = (p.stdout or "") + "\n" + (p.stderr or "")
    urls = re.findall(r'https?://\S+?\.(?:png|jpg|jpeg|webp)', blob) or re.findall(r'https?://\S+', blob)
    if not urls:
        print(f"   no url: {blob.strip()[-250:]}")
        return False
    subprocess.run(["curl", "-s", "-L", urls[-1], "-o", str(out)], check=True)
    return out.exists() and out.stat().st_size > 1000


def main():
    (CAST / "AARON.md").write_text(f"""# AARON -- cast canon sheet (sketch-style family, repo-level)

Built 2026-08-03 for the Day of Atonement episode (Leviticus 16), following
the same repo-level /cast-bible pattern `_r1_worldbible.py` used for JESUS/
DISCIPLES/BOAT/MOSES. Anchor: `cast/aaron_ref.png` -- a regenerated portrait
is a DIFFERENT face, never lose the anchor.

**Age verified against explicit KJV numbers** (feedback-verify-character-
age-scale-before-render, don't estimate): Exodus 7:7 states Aaron was 83
("eighty and three years old") when he and Moses confronted Pharaoh, before
the tabernacle existed. The tabernacle was reared up in the SECOND year
after the Exodus (Exodus 40:17), so Aaron was ~84 when the Day of Atonement
ritual was first instituted and performed. Numbers 33:39 states he was 123
when he died on Mount Hor, ~39 years later. **He was already an old man at
the very START of his priesthood** -- there is no young/middle-aged Aaron
anywhere in this story, the same finding as `cast/MOSES.md`'s golden-calf
note. ONE canon sheet covers his entire ~39-year tenure (Beat 1's
institution through Beat 5's "in my old age"); no separate elder anchor was
built, on purpose -- see the retired `cast/MOSES_YOUNGER.md` for why that
kind of split anchor is the wrong move for a gap that's elderly at both
ends.

**Cross-character distinctness checked against `cast/MOSES.md`** (SKILL.md
sec.2's anchor-approval-gate rule -- 2+ named recurring figures must differ
on hair length/style AND build/age at minimum): Moses = long hair swept
back, thinning at the crown, spare sinewed shepherd's frame, plain woolen
robe + staff. Aaron = close-cropped hair, stouter solid priestly frame,
plain linen priestly garments -- differs on both axes, plus an entirely
different signature garment.

Needed because the repeated-element census (SKILL.md sec.2) found Aaron on
screen in nearly every spread of this episode -- without a locked anchor he
drifts face-to-face across the film, the same failure mode this cast
discipline exists to prevent. Moses appears once in this story (Beat 2,
bringing the LORD's charge, at the SAME early point in the timeline as the
golden-calf flashback) -- reuse the existing `cast/moses_ref.png` per that
sheet's own "Golden-calf flashback" note (~80 years old, not the ~120
Bronze Serpent portrayal); no new Moses render needed.

## Canon description (paste VERBATIM into every prompt that shows Aaron)

> {AARON_CANON}

## The one exception -- the golden garments (Beat 1 prologue only)

Before he puts on the plain linen above, Aaron briefly wears the ordinary
high-priestly "garments of glory and beauty" (Exodus 28:2) -- a blue robe
hemmed with pomegranates and bells, a jewelled breastplate, a gold-and-linen
ephod, and a gold plate engraved HOLINESS TO THE LORD bound to his mitre by
a blue lace. This appears in ONE prologue moment (him laying these aside
before he washes and dresses in linen) and nowhere else in the film -- do
NOT use it as the default appearance; every ritual spread uses the plain
linen above.

## Usage
Chain the anchor via --image + append: "the SAME man as the reference image
-- identical face, beard, hair, and clothing." For any spread where Aaron
appears in a dramatically different pose, chain the first APPROVED
in-episode render as a SECOND reference alongside this anchor for every
later appearance (multi-pose identity lock, SKILL.md sec.2).
""", encoding="utf-8")
    print("[sheet] AARON.md written")

    for name, canon, framing, ar in ANCHORS:
        out = CAST / f"{name}.png"
        if out.exists():
            print(f"[skip] {name}")
            continue
        prompt = E.STYLE + "\n\nSCENE: " + canon + " " + framing
        print(f"[ref] {name} ...", flush=True)
        ok = run(prompt, out, ar)
        if not ok:
            ok = run(prompt, out, ar)
        if ok:
            cost.record_hf(EPISODE, "long", "cast_anchor", E.MODEL, note=f"[dayofatonement] {name}")
            print("   ok")
        else:
            print("   FAILED")


if __name__ == "__main__":
    main()
