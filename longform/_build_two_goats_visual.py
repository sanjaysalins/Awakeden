"""EW01 Two Goats — long-form 16:9 visual batch (stills + clips), HF-ONLY.

Generalizes the PROVEN proof-slice pattern (_render_slice_two_goats.py) to all 25 scenes:
period-documentary Baroque oil stills via HF nano_banana_2 @16:9, animated with veo3_1_lite
using the scene's GREEN-palette camera move + glitter-kill + frozen-tableau anti-morph lock.
slice_NN naming (matches the existing proofs). Idempotent. Reuse #10 from test_hero.

Usage:
  python _build_two_goats_visual.py stills [--scenes 4,20] [--force]
  python _build_two_goats_visual.py anim   [--scenes 4,20] [--force]
"""
import sys, time, json, shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
import config
from pipeline.visual_models import Scene
from pipeline import visual_render, video_render, cost

V1 = ROOT / "longform" / "EW01_Two_Goats" / "v1"
OUT = V1 / "visual_16x9"
TEST_HERO = V1 / "visual_16x9_test" / "test_hero.png"
plan = json.loads((OUT / "scene_plan.json").read_text(encoding="utf-8"))
SCENES = {s["id"]: s for s in plan["scenes"]}

# --- locked look (proven on slice 01/06/25 + #25 Christ) ---
config.VISUAL_STYLE_BASE = ("Baroque oil painting, dramatic chiaroscuro, Caravaggio and "
    "Rembrandt lighting, deep shadow and warm golden light, reverent sacred art, muted "
    "earth tones, fine visible brushwork")
config.VISUAL_STYLE_TAIL = ("no text, no modern elements, FULL-BLEED composition filling the "
    "entire 16:9 frame edge to edge, NOT a framed canvas, no painting frame, no gilt or gold "
    "border, no matte or passe-partout, cinematic 16:9 widescreen composition")
visual_render.HFProvider.ASPECT = "16:9"
config.VIDEO_HF_MODEL = "veo3_1_lite"
config.VIDEO_HF_ASPECT = "16:9"

TORN_VEIL = {20, 23}            # directional torn-veil — minimal move, never a fabric tear
CAM = {
    "pull_back": "Cinematic slow crane pull-back, the camera rising and drawing back to reveal the full scale",
    "smooth_cinematic": "Smooth cinematic camera movement, a gentle gliding drift with subtle parallax",
    "dolly_in": "Cinematic slow dolly push-in toward the subject",
    "dolly_shot": "Cinematic smooth dolly shot tracking steadily forward",
    "zoomed_in": "Cinematic slow telephoto zoom-in onto the subject",
    "tracking_drone_view": "Cinematic tracking drone glide forward over the scene",
}
MINIMAL = "An almost imperceptible, very slow cinematic drift; the camera barely moves"
GLITTER = (" Steady natural light only; absolutely no glowing particles, sparkles, dust "
    "motes, glitter, embers or floating lights; no lens bloom.")
LOCK = (" Keep it a frozen Baroque oil painting tableau; the subjects stay perfectly still; "
    "only the camera and faint {atmos} move; no morphing, no new elements, do not invent or "
    "duplicate any figure or face.")
TEAR_LOCK = (" The torn curtain is already rent exactly as painted and must stay completely "
    "still — NO fabric movement, NO tearing motion, NO cloth animation; the rip does not grow.")


def to_scene(s):
    return Scene(
        index=s["id"], slug=f"slice_{s['id']:02d}", title=s["title"],
        scene_type="single", arc_position="body", framing=s.get("framing", "cinematic wide"),
        purpose=s["title"], rationale=s.get("mvt", ""),
        visible_elements=s["subject_block"][:200], emotional_tone=s.get("atmos", ""),
        subject_block=s["subject_block"],
        mood_block="reverent, period-documentary, " + s.get("framing", "wide"),
        jesus_variant=None,    # HF-ONLY — no NBP ref attach even on Christ scenes
    )


def motion_for(s):
    cam = MINIMAL if s["id"] in TORN_VEIL else CAM[s["camera"]]
    m = cam + "." + LOCK.format(atmos=s.get("atmos", "atmosphere"))
    if s["id"] in TORN_VEIL:
        m += TEAR_LOCK
    return m + GLITTER


def parse_args():
    mode = sys.argv[1] if len(sys.argv) > 1 else "stills"
    force = "--force" in sys.argv
    ids = None
    if "--scenes" in sys.argv:
        ids = [int(x) for x in sys.argv[sys.argv.index("--scenes") + 1].split(",")]
    return mode, (ids or sorted(SCENES)), force


def main():
    mode, ids, force = parse_args()
    # reuse test_hero for scene 10 (scapegoat wilderness) — never re-render
    s10 = OUT / "slice_10.png"
    if not s10.exists() and TEST_HERO.exists():
        shutil.copy(TEST_HERO, s10); print(f"[reuse] test_hero.png -> {s10.name}")

    imgp = visual_render.HFProvider() if mode == "stills" else None
    vidp = video_render.HFVideoProvider() if mode == "anim" else None
    ok = skip = fail = 0
    for sid in ids:
        s = SCENES[sid]; scene = to_scene(s)
        png = OUT / f"slice_{sid:02d}.png"
        mp4 = OUT / f"slice_{sid:02d}.mp4"
        if mode == "stills":
            if png.exists() and not force:
                print(f"[skip] {png.name}"); skip += 1; continue
            try:
                print(f"[img ] #{sid:02d} {s['title'][:42]} (HF 16:9) ...", flush=True); t = time.time()
                png.write_bytes(imgp.generate(scene))
                cost.record_hf("EW01_Two_Goats", "long", "stills", config.HF_MODEL_ID, note=f"#{sid:02d}")
                print(f"       ok ({png.stat().st_size:,} b, {time.time()-t:.0f}s)"); ok += 1
            except Exception as e:
                print(f"       FAIL #{sid}: {e}"); fail += 1
        else:  # anim
            if mp4.exists() and not force:
                print(f"[skip] {mp4.name}"); skip += 1; continue
            if not png.exists():
                print(f"[MISS png] slice_{sid:02d}.png"); fail += 1; continue
            try:
                tag = " [TORN-VEIL minimal/no-tear]" if sid in TORN_VEIL else ""
                print(f"[anim] #{sid:02d} cam={s['camera']}{tag} (veo3_1_lite 8s) ...", flush=True); t = time.time()
                vidp.animate(png, mp4, motion_for(s), 8)   # writes its own ledger row
                print(f"       ok ({mp4.stat().st_size:,} b, {time.time()-t:.0f}s)"); ok += 1
            except Exception as e:
                print(f"       FAIL #{sid}: {str(e)[:160]}"); fail += 1
    print(f"\n[done] {mode}: ok {ok}, skipped {skip}, failed {fail}  -> {OUT}")


if __name__ == "__main__":
    main()
