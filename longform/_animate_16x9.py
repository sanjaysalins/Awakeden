"""Animate an episode's approved 16:9 stills with veo3_1_lite (HF). Slow camera on a
frozen Baroque tableau; anti-morph prompt protects faces/hands. EPISODE-GENERIC: pass an
episode slug/dir as the first arg (bare = Isaiah). Per-scene (camera, atmos) come from the
scene_plan, not a hardcoded MOTION dict. Idempotent (skips existing mp4). TEST-GATE: animate
1-2 test clips, STOP for QC + --approved. Cross scenes are robed -> veo should pass; on NSFW
block, falls back to direct-Kling."""
import sys, time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(Path(__file__).resolve().parent))
import config
from pipeline import video_render
from _episode import resolve  # noqa: E402
from _test_gate import apply_test_gate  # noqa: E402

ep = resolve(sys.argv)
anim = ep.plan.get("animation", {})
config.VIDEO_HF_MODEL = anim.get("model", "veo3_1_lite")
config.VIDEO_HF_ASPECT = anim.get("aspect", "16:9")
DURATION = int(anim.get("duration", 8))


def base(move, atmos):
    return (f"Cinematic {move}. Keep it a FROZEN Baroque oil painting tableau — preserve the "
            f"exact faces, hands and composition, NO morphing of faces or hands, NO new elements, "
            f"NO invented body motion. Only {atmos}.")


# TEST GATE: a calm scene + a directional scene (generic analog of Isaiah's [2,13]).
calm = next((s["id"] for s in ep.scenes if not s.get("directional")), ep.scenes[0]["id"])
direc = next((s["id"] for s in ep.scenes if s.get("directional")), None)
default_test = [calm] + ([direc] if direc else [])
gate_ids, gate_stop, gate_banner = apply_test_gate(
    sys.argv, ep.out, stage="animation",
    all_ids=[s["id"] for s in ep.scenes],
    default_test=default_test,
    qc_hint="Watch the WHOLE clip (>=6 frames): living motion, no morph/glitter, no comical reverse.",
)

vp = video_render.HFVideoProvider()
kling = None
ok = fail = skip = 0
for s in ep.scenes:
    if s["id"] not in gate_ids:
        continue
    png = ep.png(s)
    mp4 = ep.mp4(s)
    if mp4.exists():
        print(f"[skip] {mp4.name}"); skip += 1; continue
    if not png.exists():
        print(f"[MISS png] {png.name}"); fail += 1; continue
    move = s.get("camera", "very slow push-in")
    atmos = s.get("atmos", "subtle atmosphere")
    prompt = base(move, atmos)
    print(f"[anim] {s['id']:02d} {s['title'][:38]} ...", flush=True)
    t = time.time()
    try:
        vp.animate(png, mp4, prompt, DURATION)
        print(f"       ok ({mp4.stat().st_size:,} b, {time.time()-t:.0f}s)")
        ok += 1
    except Exception as e:
        msg = str(e)[:160]
        print(f"       veo FAILED: {msg}")
        if "nsfw" in msg.lower() or "blocked" in msg.lower() or "moderation" in msg.lower():
            try:
                if kling is None:
                    kling = video_render.KlingDirectProvider()
                print("       -> falling back to direct-Kling ...", flush=True)
                kling.animate(png, mp4, prompt, DURATION); ok += 1
                print(f"       ok via Kling ({mp4.stat().st_size:,} b)")
            except Exception as e2:
                print(f"       Kling FAILED too: {str(e2)[:160]}"); fail += 1
        else:
            fail += 1
print(f"\n[done] {ep.slug}: animated {ok}, skipped {skip}, failed {fail} -> {ep.out}")
if gate_stop:
    print(gate_banner); sys.exit(0)
