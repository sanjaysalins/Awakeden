"""Video (animation) providers: image -> clip, with a HYBRID default.

Validated by the 2026-05-29 bake-off:
- HF Kling 3.0 (`higgsfield generate create kling3_0 --start-image ... --duration N`)
  makes good frozen-tableau motion from a SIMPLE motion-only prompt (the elaborate
  8-beat .kling.json is NOT needed), at ~6.25 credits / 5s std clip, with variable
  integer duration. BUT HF's NSFW filter rejects the bare-torso crucifixion
  platform-wide (Kling AND Seedance).
- The existing DIRECT-Kling path (PythonProject1/jesus/image_to_kling.py) animates
  the cross fine and is hardened (cost ceiling, recovery, ffprobe validation).

So `HybridVideoProvider` runs HF for the clothed majority and falls back to
direct-Kling for any image HF rejects — guaranteeing the gospel-landing cross can
always be animated. Mirrors the ImageProvider pattern in visual_render.py.

NOTE: per-clip `duration` is plumbed through but the current pipeline still
generates a deep pool BEFORE the cut plan, so it defaults to config.VIDEO_DURATION
(10s). Part 2 (cut-aware planning) will pass each clip's target slot length here to
generate at-length and retire the speed-up hack.
"""
from __future__ import annotations

import json
import os
import re
import subprocess
import urllib.request
from abc import ABC, abstractmethod
from pathlib import Path

import config


_MP4_URL_RE = re.compile(r"https://\S+?\.mp4", re.IGNORECASE)
_NSFW_RE = re.compile(r"nsfw", re.IGNORECASE)


# Per-model HF CLI quirks (discovered in the 2026-05-30 video bake-off):
#   - media flag: most image-to-video models take --start-image, but a few only
#     accept --image (they error "Model accepts only --image").
#   - --mode/--sound are Kling-only flags; other models reject them. kling3_0 takes
#     --mode std|pro|4k + --sound on|off; kling2_6 takes ONLY a boolean --sound (no
#     --mode). Sound is a real surcharge on kling3_0 (pro 12.5cr ON -> 8.75cr OFF,
#     std 10 -> 7.5) and doubles kling2_6 — always mute it (verified 2026-07-21).
#   - duration is a fixed per-model allow-list; we snap to the nearest legal value
#     (e.g. VIDEO_DURATION=10 -> 8 for veo, whose legal set is 4/6/8).
_HF_NEEDS_IMAGE_FLAG = {"minimax_hailuo", "kling2_6", "veo3_1", "cinematic_studio_video_v2"}
_HF_DURATIONS = {
    "veo3_1_lite": (4, 6, 8),
    "veo3_1": (4, 6, 8),
    "veo3": (4, 6, 8),
    "minimax_hailuo": (6, 10),
    "seedance1_5": (4, 8, 12),
    "seedance_2_0": (4, 8, 12),
    "cinematic_studio_video_v2": (5,),   # graphic-novel anim model (POC default 5s)
}


def _hf_duration(model: str, duration: int) -> int:
    allowed = _HF_DURATIONS.get(model)
    if not allowed or duration in allowed:
        return duration
    return min(allowed, key=lambda a: abs(a - duration))


class NSFWRejected(Exception):
    """HF refused the input image as NSFW (e.g. the bare-torso crucifixion)."""


class VideoGenError(Exception):
    pass


# --------------------------------------------------------------------------
# Prompt sourcing. The bake-off (2026-05-29) showed a MINIMAL motion prompt makes
# HF produce a bland single zoom — the RICH 8-beat cut plan from image_to_kling's
# Stage A (the `.kling.json` "prompt") is what gives HF the internal reframing
# (full -> mid -> close -> macro -> return) that matches direct-Kling. So we feed
# HF the cut-plan prompt; motion_prompt() is only a fallback when no plan exists.
# --------------------------------------------------------------------------
def cut_plan_prompt(png_path: Path, pacing: str = "controlled",
                    viral_role: str = "", log=print) -> str:
    """Return the rich Stage-A cut-plan prompt for this image. Reuses an existing
    `<stem>.kling.json`; if absent, generates it via `image_to_kling.py --plan-only`
    (the Claude-Vision cut-plan director). Falls back to motion_prompt() if neither."""
    import json
    kj = png_path.with_suffix(".kling.json")
    if not kj.exists():
        script = config.NARRATION_PROJECT_DIR / "image_to_kling.py"
        if script.exists():
            env = os.environ.copy()
            env["KLING_SKILL_PATH"] = str(config.KLING_SKILL_PATH)
            env["PYTHONIOENCODING"] = "utf-8"
            config.inject_agent_env(env)
            log(f"      [cut-plan] {kj.name} via image_to_kling --plan-only...")
            subprocess.run(
                [config.NARRATION_PYTHON, str(script), str(png_path), "--plan-only", "--skip-audit"],
                cwd=str(config.NARRATION_PROJECT_DIR.parent), env=env,
                capture_output=True, text=True, encoding="utf-8", errors="replace",
            )
    if kj.exists():
        try:
            p = str(json.loads(kj.read_text(encoding="utf-8")).get("prompt", "")).strip()
            if p:
                return p
        except Exception:
            pass
    return motion_prompt(pacing, viral_role)


def motion_prompt(pacing: str = "controlled", viral_role: str = "") -> str:
    base = ("Slow reverent cinematic camera move on a still Baroque oil painting. "
            "Only the camera moves; the painting is completely frozen — no figures "
            "move, no limbs move, no morphing, no animation, no added motion. ")
    if viral_role in ("climax", "close"):
        move = "An almost imperceptible hold, the faintest slow push toward the centre."
    elif pacing == "slower":
        move = "An almost imperceptible slow push-in toward the centre."
    elif pacing == "faster":
        move = "A steady, deliberate push-in toward the centre."
    else:
        move = "A gentle slow push-in toward the centre."
    return base + move + " Subtle living light only."


# --------------------------------------------------------------------------
# Provider abstraction
# --------------------------------------------------------------------------
class VideoProvider(ABC):
    name: str

    @abstractmethod
    def animate(self, png_path: Path, out_mp4: Path, prompt: str, duration: int) -> Path:
        """Animate png_path -> out_mp4. Return out_mp4. Raise NSFWRejected if the
        provider refuses the image, VideoGenError on other failure."""


def _episode_of(path: Path) -> str:
    """Ledger episode id from any path under <episode>/v1/... (fallback: parent name)."""
    for p in path.parents:
        if p.name == "v1":
            return p.parent.name
    return path.parent.name


def _record_clip_cost(provider: str, model: str, png_path: Path, params=None) -> None:
    """Spend-ledger row for one rendered clip. Never breaks the render."""
    try:
        from pipeline import cost
        ep = _episode_of(png_path)
        if provider == "kling":
            cost.record_kling(ep, "clip", "animate", note=png_path.name)
            return
        try:  # exact per-model estimate at the create call's own flags; flat fallback if the query flakes
            cost.record_hf(ep, "clip", "animate", model, image=png_path, note=png_path.name,
                           params=params)
        except Exception:
            cost.record(ep, "clip", "animate", "hf", model, 1,
                        est_usd=cost.KLING_USD_PER_CLIP, est_only=True,
                        note=f"{png_path.name} (flat est)")
    except Exception as e:
        print(f"      [cost] clip ledger row failed: {e}")


class HFVideoProvider(VideoProvider):
    """Higgsfield CLI image-to-video (default kling3_0)."""

    name = "hf"

    def __init__(self) -> None:
        if not config.HF_CLI_PATH.exists():
            raise SystemExit(f"Higgsfield CLI not found at {config.HF_CLI_PATH}.")
        self._cli = str(config.HF_CLI_PATH)

    def animate(self, png_path: Path, out_mp4: Path, prompt: str, duration: int) -> Path:
        model = config.anim_model()
        media_flag = "--image" if model in _HF_NEEDS_IMAGE_FLAG else "--start-image"
        params = {"duration": _hf_duration(model, duration),
                  "aspect_ratio": config.VIDEO_HF_ASPECT}
        if model == "kling3_0":
            params["mode"] = config.VIDEO_HF_MODE
            params["sound"] = config.VIDEO_HF_SOUND
        elif model == "kling2_6":   # boolean --sound only, no --mode (see quirks above)
            params["sound"] = "false" if config.VIDEO_HF_SOUND == "off" else "true"
        cmd = [self._cli, "generate", "create", model,
               media_flag, str(png_path), "--prompt", prompt]
        for k, v in params.items():
            cmd += [f"--{k}", str(v)]
        cmd += ["--wait"]
        result = subprocess.run(
            cmd, capture_output=True, text=True, encoding="utf-8",
            errors="replace", timeout=config.VIDEO_HF_GEN_TIMEOUT,
        )
        blob = (result.stdout or "") + "\n" + (result.stderr or "")
        if _NSFW_RE.search(blob):
            raise NSFWRejected(f"HF refused {png_path.name} as NSFW")
        if result.returncode != 0:
            raise VideoGenError(
                f"hf kling failed ({result.returncode}) on {png_path.name}:\n"
                f"  {blob.strip()[-500:]}"
            )
        m = _MP4_URL_RE.search(result.stdout or "")
        if not m:
            raise VideoGenError(
                f"hf returned no .mp4 URL for {png_path.name}: {blob.strip()[-400:]}")
        url = m.group(0)
        out_mp4.parent.mkdir(parents=True, exist_ok=True)
        req = urllib.request.Request(url, headers={"User-Agent": "JesusInTheBible/1.0"})
        with urllib.request.urlopen(req, timeout=300) as resp:
            out_mp4.write_bytes(resp.read())
        _record_clip_cost("hf", model, png_path, params=params)
        return out_mp4


class KlingDirectProvider(VideoProvider):
    """The proven direct-Kling path — subprocess image_to_kling.py on a single PNG.
    Used as the NSFW fallback (it animates the crucifixion). image_to_kling writes
    `<stem>.mp4` next to the PNG and is idempotent (skips if it already exists)."""

    name = "kling"

    def animate(self, png_path: Path, out_mp4: Path, prompt: str, duration: int) -> Path:
        script = config.NARRATION_PROJECT_DIR / "image_to_kling.py"
        if not script.exists():
            raise VideoGenError(f"image_to_kling.py not found at {script}")
        env = os.environ.copy()
        env["KLING_SKILL_PATH"] = str(config.KLING_SKILL_PATH)
        env["PYTHONIOENCODING"] = "utf-8"
        config.inject_agent_env(env)
        png_abs = png_path.resolve()  # subprocess runs in PythonProject1 cwd — pass an absolute path
        pre_exists = png_abs.with_suffix(".mp4").exists()  # image_to_kling is idempotent — no spend if so
        result = subprocess.run(
            [config.NARRATION_PYTHON, str(script), str(png_abs), "--skip-audit"],
            cwd=str(config.NARRATION_PROJECT_DIR.parent), env=env,
            capture_output=True, text=True, encoding="utf-8", errors="replace",
        )
        produced = png_abs.with_suffix(".mp4")
        if not produced.exists():
            raise VideoGenError(
                f"direct-Kling produced no mp4 for {png_path.name} "
                f"(exit {result.returncode}): {(result.stderr or '')[-400:]}")
        if produced.resolve() != out_mp4.resolve():
            out_mp4.parent.mkdir(parents=True, exist_ok=True)
            out_mp4.write_bytes(produced.read_bytes())
        if not pre_exists:
            _record_clip_cost("kling", "kling-direct", png_path)
        return out_mp4


class HybridVideoProvider(VideoProvider):
    """HF Kling primary; fall back to direct-Kling on NSFW rejection (the cross)
    or any HF error — so the gospel-landing image always animates."""

    name = "hybrid"

    def __init__(self) -> None:
        self._hf = HFVideoProvider()
        self._kling = KlingDirectProvider()

    def animate(self, png_path: Path, out_mp4: Path, prompt: str, duration: int) -> Path:
        try:
            return self._hf.animate(png_path, out_mp4, prompt, duration)
        except NSFWRejected:
            return self._kling.animate(png_path, out_mp4, prompt, duration)
        except VideoGenError:
            return self._kling.animate(png_path, out_mp4, prompt, duration)


def get_video_provider(name: str = "") -> VideoProvider:
    name = (name or config.VIDEO_PROVIDER).strip().lower()
    if name == "hf":
        return HFVideoProvider()
    if name == "kling":
        return KlingDirectProvider()
    if name == "hybrid":
        return HybridVideoProvider()
    raise SystemExit(f"Unknown VIDEO_PROVIDER {name!r} (use hybrid|hf|kling).")


def animate_clip(
    png_path: Path,
    out_mp4: Path,
    pacing: str = "controlled",
    viral_role: str = "",
    duration: int | None = None,
    provider: VideoProvider | None = None,
    prompt: str | None = None,
    log=print,
) -> Path:
    """Idempotent: skip if out_mp4 exists. Returns the mp4 path. Uses the rich
    cut-plan prompt by default (the bake-off proved a minimal prompt = bland zoom)."""
    if out_mp4.exists():
        log(f"      [skip] {out_mp4.name} exists")
        return out_mp4
    provider = provider or get_video_provider()
    if prompt is None:
        prompt = cut_plan_prompt(png_path, pacing, viral_role, log=log)
    dur = duration or config.VIDEO_DURATION
    log(f"      [{provider.name}] animating {png_path.name} ({dur}s)...")
    result = provider.animate(png_path, out_mp4, prompt, dur)
    out_mp4.with_suffix(".style.json").write_text(
        json.dumps(config.style_provenance(), indent=2), encoding="utf-8")
    log(f"      -> {result.name}")
    return result


def animate_scenes(
    v1_folder: Path,
    image_provider_folder: str,
    indices: list[int] | None = None,
    provider_name: str = "",
    log=print,
) -> int:
    """Animate the scene PNGs in <v1>/visual/<image_provider_folder>/ into
    `<stem>.mp4` via the configured video provider (default hybrid). Idempotent —
    skips any clip already on disk. `indices` restricts to those scene indices
    (e.g. the non-excluded set). Returns the count animated this run."""
    import json
    from pipeline import bible_kb
    from pipeline.visual_models import ScenePlan

    # /bible-check chokepoint: don't spend animation credits unless the piece's
    # biblical accuracy is GREEN. Grandfather-safe — a piece with no _bible_check/
    # is skipped with a notice; BIBLE_GATE=off bypasses; BIBLE_GATE=strict enforces
    # even on un-checked pieces. Mirrors longform/_animate_16x9.py's gate call.
    bible_kb.gate(Path(v1_folder), stage="animate")

    plan_path = v1_folder / "visual" / "scene_plan.json"
    if not plan_path.exists():
        raise SystemExit(f"No scene_plan.json at {plan_path}.")
    plan = ScenePlan.from_json(json.loads(plan_path.read_text(encoding="utf-8")).get("plan", {}))
    render_dir = v1_folder / "visual" / image_provider_folder
    provider = get_video_provider(provider_name)
    log(f"      [video] provider='{provider.name}' over {render_dir}")

    wanted = set(indices) if indices else None
    made = 0
    for scene in plan.scenes:
        if wanted is not None and scene.index not in wanted:
            continue
        stem = scene.filename_stem
        png = render_dir / f"{stem}.png"
        mp4 = render_dir / f"{stem}.mp4"
        if not png.exists():
            log(f"      ! no PNG for scene {scene.index} ({png.name}); skipping")
            continue
        if mp4.exists():
            log(f"      [skip] {mp4.name} exists")
            continue
        animate_clip(png, mp4, pacing=scene.pacing, viral_role=scene.viral_role,
                     provider=provider, log=log)
        made += 1
    log(f"      [video] animated {made} new clip(s).")
    return made
