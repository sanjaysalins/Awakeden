"""Central configuration for the JesusInTheBible narration-creation engine.

All secrets come from `.env` (never hardcoded). The Anthropic key drives the
text engine (generate / review / revise). The downstream audio pipeline lives
in a separate project and reads its own keys from that project's root `.env`.
"""
from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).resolve().parent

# Load this project's .env (holds ANTHROPIC_API_KEY for the text engine).
load_dotenv(PROJECT_ROOT / ".env")

# ----------------------------------------------------------------------------
# LLM provider — agent-mode (in-chat / Max subscription) vs metered API
# ----------------------------------------------------------------------------
# "agent": the in-chat agent (Claude Code on the Max sub) answers every LLM call
#   via a file bridge (pipeline/agent_bridge.py) — NO metered API spend. The engine
#   writes a request file and blocks until the agent writes the reply. Run the
#   engine with run_in_background and service the requests from chat.
# "api": the classic metered Anthropic API path (anthropic.Anthropic).
# DEFAULT is "agent" (the user's cost direction); set LLM_PROVIDER=api for
# unattended / cron runs where no agent is in the loop to service the bridge.
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "agent").strip().lower()
AGENT_BRIDGE_DIR = os.getenv("AGENT_BRIDGE_DIR", "")  # blank -> bridge default (<repo>/.agent_bridge)
AGENT_BRIDGE_TIMEOUT = int(os.getenv("AGENT_BRIDGE_TIMEOUT", "3600"))  # seconds per call
AGENT_BRIDGE_POLL = float(os.getenv("AGENT_BRIDGE_POLL", "1.5"))


def agent_mode() -> bool:
    return LLM_PROVIDER == "agent"


def inject_agent_env(env: dict) -> dict:
    """Stamp the agent-mode bridge vars into a subprocess env so a child process
    (image_to_kling.py under PythonProject1's venv) routes its Claude calls through
    the SAME file bridge instead of the metered API. No-op outside agent-mode."""
    if agent_mode():
        env["LLM_PROVIDER"] = "agent"
        env["JITB_BRIDGE_PATH"] = str(PROJECT_ROOT / "pipeline")
        if AGENT_BRIDGE_DIR:
            env["AGENT_BRIDGE_DIR"] = AGENT_BRIDGE_DIR
    return env


# ----------------------------------------------------------------------------
# Anthropic / model
# ----------------------------------------------------------------------------
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")

# Opus 4.7 — best quality for nuanced, theologically-careful short-form writing.
# Override with CLAUDE_MODEL if you want to trade cost for speed (e.g. sonnet).
MODEL = os.getenv("CLAUDE_MODEL", "claude-opus-4-7")

# Non-streaming cap. Adaptive thinking + a ~150-word script + JSON fit easily.
# Bumped to 32K to accommodate large scene plans (14-20 scenes × rich
# per-scene fields × candidates can exceed 16K JSON output).
MAX_TOKENS = int(os.getenv("CLAUDE_MAX_TOKENS", "32000"))

# Number of revise passes allowed when a review does not return LOCKED.
MAX_REVISIONS = int(os.getenv("MAX_REVISIONS", "2"))

# Independent red-team audit is STANDARD PRACTICE: after the self-review/revise
# loop converges, a fresh adversarial auditor re-verifies the final draft from
# scratch, and its verdict is authoritative. On by default. (INDEPENDENT_REVIEW=0
# to disable for a cheap dry run.)
INDEPENDENT_REVIEW = os.getenv("INDEPENDENT_REVIEW", "1") not in ("0", "false", "False", "")

# Model used for the independent auditor. Defaults to the main model; point it at a
# different model (even a different family) for stronger independence if you wish.
REVIEW_MODEL = os.getenv("REVIEW_MODEL", "") or None  # None -> use MODEL

# Model for COARSE Vision checks (the assembly per-slot "does this frame match the
# words" verify). Haiku is plenty for that and much cheaper/faster. The SUBTLE
# per-image content audit (subject identity — the scene-11 crucifixion lesson)
# stays on MODEL/Opus; set VISION_AUDIT_MODEL=claude-opus-4-7 to use Opus here too.
VISION_AUDIT_MODEL = os.getenv("VISION_AUDIT_MODEL", "claude-haiku-4-5-20251001")

# Thread discovery — find the sharpest *true* thread (overlooked detail / original-
# language / NT-confirmed OT echo / cultural-historical) before generation, so the
# short is fresh-yet-faithful by default instead of hand-seeded. Standard practice;
# see constitution -> "Freshness through faithful depth". THREAD_DISCOVERY=0 disables.
THREAD_DISCOVERY = os.getenv("THREAD_DISCOVERY", "1") not in ("0", "false", "False", "")

# Verses on each side of the primary reference fetched as the wider pericope
# (for thread mining + in-context accuracy in review).
PASSAGE_WINDOW = int(os.getenv("PASSAGE_WINDOW", "8"))

# Draft TOURNAMENT — instead of writing ONE draft and polishing it (which
# converges on the safe/familiar arc and a templated CTA), generate N DIVERGENT
# full drafts (different thread/hook/conviction/CTA), judge the whole hook->CTA
# ARC, and synthesize the winner + graft the strongest hook/CTA from runners-up.
# Then the normal review/revise/independent gates run on the result. This is the
# fix for "the narration feels over-used / the CTA feels formulaic".
ENGINE_TOURNAMENT = os.getenv("ENGINE_TOURNAMENT", "1") not in ("0", "false", "False", "")
ENGINE_CANDIDATES = int(os.getenv("ENGINE_CANDIDATES", "4"))
ENGINE_SYNTHESIZE = os.getenv("ENGINE_SYNTHESIZE", "1") not in ("0", "false", "False", "")

# ----------------------------------------------------------------------------
# 60-second short-form targets (from deep-research-report.md)
# ----------------------------------------------------------------------------
# ~135-160 words reads as ~60s at a measured narration pace.
TARGET_WORDS_MIN = int(os.getenv("TARGET_WORDS_MIN", "135"))
TARGET_WORDS_MAX = int(os.getenv("TARGET_WORDS_MAX", "165"))

# ElevenLabs /v1/text-to-dialogue hard cap, enforced by the downstream pipeline.
# We stay well under it; surfaced here so the engine can self-check.
DIALOGUE_CHAR_CAP = 2000

# ----------------------------------------------------------------------------
# Paths to assets and the downstream audio pipeline
# ----------------------------------------------------------------------------
DATA_DIR = PROJECT_ROOT / "data"
CONSTITUTION_PATH = DATA_DIR / "constitution.md"
SERIES_PATH = DATA_DIR / "series.json"
STRUCTURES_PATH = DATA_DIR / "structures.json"

# Which narration structure to use. None -> the file's "default" (Gospel Five-Beat).
DEFAULT_STRUCTURE = os.getenv("NARRATION_STRUCTURE") or None

# Cache of exact-KJV verse lookups (so we don't re-fetch on every run).
SCRIPTURE_CACHE_PATH = DATA_DIR / "kjv_cache.json"

# The existing audio pipeline project (PythonProject1/jesus). Generated
# narrations are written into its narration tree so its verify->tag->audit->synth
# flow consumes them directly. Override either via env if your layout differs.
NARRATION_PROJECT_DIR = Path(
    os.getenv(
        "NARRATION_PROJECT_DIR",
        r"C:\Users\sanjay\PycharmProjects\PythonProject1\jesus",
    )
)
NARRATION_TREE_DIR = Path(
    os.getenv("NARRATION_TREE_DIR", str(NARRATION_PROJECT_DIR / "narration"))
)
NARRATION_PIPELINE_SCRIPT = NARRATION_PROJECT_DIR / "narration_pipeline.py"
# Duration-targeted synth (PLAYBOOK_shorts.md) — renders per-turn and atempos the
# narrator so the final MP3 lands on a fixed Shorts/Reels slot.
PER_TURN_SYNTH_SCRIPT = NARRATION_TREE_DIR / "per_turn_synth.py"

# Shorts mode: use the duration-locked per-turn synth (verify->tag->audit, then
# per_turn_synth) instead of the natural-length dialogue synth. Set SHORTS_MODE=0
# to fall back to the standard `narration_pipeline.py` full run.
SHORTS_MODE = os.getenv("SHORTS_MODE", "1") not in ("0", "false", "False", "")
SHORTS_TARGET_SECONDS = float(os.getenv("SHORTS_TARGET_SECONDS", "59"))
SHORTS_PRE_QUOTE_PAUSE = float(os.getenv("SHORTS_PRE_QUOTE_PAUSE", "0.4"))
SHORTS_STABILITY = float(os.getenv("SHORTS_STABILITY", "0.65"))

# Python interpreter used to run the audio pipeline. It must have that project's
# deps (anthropic, requests, python-dotenv) importable. We auto-detect the
# PythonProject1 venv; override with NARRATION_PYTHON if needed.
def _detect_narration_python() -> str:
    override = os.getenv("NARRATION_PYTHON")
    if override:
        return override
    # PythonProject1 is the parent of `jesus`; its venv is the natural home.
    candidates = [
        NARRATION_PROJECT_DIR.parent / ".venv" / "Scripts" / "python.exe",
        NARRATION_PROJECT_DIR.parent / ".venv" / "bin" / "python",
        NARRATION_PROJECT_DIR / ".venv" / "Scripts" / "python.exe",
        NARRATION_PROJECT_DIR / ".venv" / "bin" / "python",
    ]
    for c in candidates:
        if c.exists():
            return str(c)
    import sys

    return sys.executable  # last resort — current interpreter


NARRATION_PYTHON = _detect_narration_python()

# ----------------------------------------------------------------------------
# Visual stage — scene planning + image generation + animation
# ----------------------------------------------------------------------------
# Independent red-team audit of the scene plan (standard practice). The
# authoritative LOCKED verdict comes from this auditor, same pattern as the
# text stage. VISUAL_INDEPENDENT_REVIEW=0 disables for a cheap dry run.
VISUAL_INDEPENDENT_REVIEW = os.getenv("VISUAL_INDEPENDENT_REVIEW", "1") not in (
    "0", "false", "False", ""
)

# Default image provider. Override per-run with `cli_visual.py --provider`.
VISUAL_DEFAULT_PROVIDER = os.getenv("VISUAL_DEFAULT_PROVIDER", "nbp").strip().lower()

# Scene count window. Adaptive — short reflective narrations get fewer scenes
# than rich parables. Rich parables / Gospel encounters target 14-20 scenes
# so the user picks the rendered short_priority from a deeper candidate pool;
# the downstream Kling cut planner benefits from quantity at the selection
# stage. Short reflective verses ("I AM" meditations) compress to 4.
VISUAL_MIN_SCENES = int(os.getenv("VISUAL_MIN_SCENES", "4"))
VISUAL_MAX_SCENES = int(os.getenv("VISUAL_MAX_SCENES", "24"))

# Short-priority list size — the subset of scenes that actually get rendered
# and animated when --short-only is on (default).
VISUAL_SHORT_PRIORITY_DEFAULT = int(os.getenv("VISUAL_SHORT_PRIORITY_DEFAULT", "6"))

# Per-image content-audit retry cap (provider re-prompt with audit feedback).
# Mirrors image_to_kling.py's `--max-audit-retries 2`; we default lower because
# NBP per-image cost is the dominant spend.
MAX_NBP_RETRIES = int(os.getenv("MAX_NBP_RETRIES", "1"))

# Path to the sibling project's `.env` (holds GEMINI_API_KEY for NBP and
# HF_API_TOKEN for the HuggingFace Inference API).
NBP_PROJECT_ENV = Path(os.getenv("NBP_PROJECT_ENV", str(NARRATION_PROJECT_DIR.parent / ".env")))

# Eagerly load the sibling .env so visual_render can read GEMINI_API_KEY /
# HF_API_TOKEN at import time without re-discovering paths.
if NBP_PROJECT_ENV.exists():
    load_dotenv(NBP_PROJECT_ENV, override=False)

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")

# Higgsfield CLI (`hf.exe`) — NOT HuggingFace Inference API. The CLI is the
# user's preferred path for generation (paid Ultimate plan, validated model
# preferences in C:\Users\sanjay\PycharmProjects\HF-POC). Auth is handled by
# the CLI itself via `hf auth login`; no env-var token needed in our code.
HF_CLI_PATH = Path(os.getenv("HF_CLI_PATH", str(Path.home() / "bin" / "hf.exe")))
HF_API_TOKEN = os.getenv("HF_API_TOKEN", "") or os.getenv("HUGGINGFACEHUB_API_TOKEN", "")

# NBP reference series. Holds `_series.latest.json` (master style + negative
# prompt) and the `refs/ref_jesus_<variant>.png` anchors used for character
# consistency when a scene specifies `jesus_variant`.
NBP_REFS_DIR = Path(os.getenv(
    "NBP_REFS_DIR",
    str(NARRATION_PROJECT_DIR / "nano_banana_pro_batch_output" / "jesus_harmony_v1"),
))

# Default Higgsfield model for the Baroque oil painting aesthetic. Per the
# user's rated winners (HF-POC/RESUME.md "Oil painting / Baroque / dramatic
# lighting"): nano_banana_2 (2 cr/image, painterly, dramatic). Override with
# HF_MODEL_ID env if you want to A/B (seedream_v5_lite, marketing_studio_image,
# cinematic_studio_2_5, image_auto are the second-tier picks).
HF_MODEL_ID = os.getenv("HF_MODEL_ID", "nano_banana_2")

# Locked Kling cut-plan SKILL — passed via env to the image_to_kling.py
# subprocess. Per HANDOVER.md, this MUST be set for the locked-discipline run.
KLING_SKILL_PATH = Path(os.getenv(
    "KLING_SKILL_PATH",
    str(NARRATION_PROJECT_DIR / "adhoc" / "SKILL_locked.md"),
))

# ----------------------------------------------------------------------------
# Video (animation) provider — image -> clip
# ----------------------------------------------------------------------------
# DIRECT-KLING is the default (2026-05-29 bake-off verdict): the user judged
# direct-Kling's motion clearly better than HF Kling 3.0 — even when HF was fed the
# SAME rich 8-beat cut-plan prompt. HF also isn't cheaper (~6.25cr/5s ≈ direct-Kling)
# and its NSFW filter blocks the crucifixion platform-wide. So HF earns no place as
# default. The hybrid/HF code stays available (VIDEO_PROVIDER=hybrid|hf) for future
# re-evaluation (e.g. HF `pro` mode, or the variable-duration redesign), but `kling`
# is primary. Tradeoff: direct-Kling is fixed ~10s, so the assembly speed/trim (with
# the reverence cap) remains how clips are fit — the variable-duration win is parked.
VIDEO_PROVIDER = os.getenv("VIDEO_PROVIDER", "kling").strip().lower()
# HF video model for the LONG-FORM pipeline only (image->clip via HFVideoProvider).
# Bake-off (2026-05-30): veo3_1_lite keeps the Baroque oil look without softening it to
# photoreal, across every scene type, at ~half Kling's credits — chosen for long-form.
# seedance1_5 is the fallback (more dynamic but photoreal-softens). SHORTS are unaffected:
# they use direct-Kling (VIDEO_PROVIDER=kling), which executes the viral 8-beat cut-plan.
VIDEO_HF_MODEL = os.getenv("VIDEO_HF_MODEL", "veo3_1_lite")       # `higgsfield model list`
VIDEO_HF_MODE = os.getenv("VIDEO_HF_MODE", "std")                 # std | pro | 4k
VIDEO_HF_ASPECT = os.getenv("VIDEO_HF_ASPECT", "9:16")
VIDEO_HF_SOUND = os.getenv("VIDEO_HF_SOUND", "off")              # narration muxed separately
# Default clip length. 10s keeps deep-pool curation flexible (any clip can fill any
# slot); Part 2 (cut-aware planning) will pass per-slot target durations to shrink
# this and kill the speed-up hack. ~6.25 credits / 5s std clip (bake-off).
VIDEO_DURATION = int(os.getenv("VIDEO_DURATION", "10"))
VIDEO_HF_GEN_TIMEOUT = int(os.getenv("VIDEO_HF_GEN_TIMEOUT", "900"))  # seconds

# ----------------------------------------------------------------------------
# Assembly stage — fit clips + narration into the deliverable vertical cut
# ----------------------------------------------------------------------------
# The viral cut uses the best N clips; all clips go in the all-takes reel. 16
# clips in ~59s forces ~2.9x average speed (a strobe on slow Baroque footage),
# so the cut defaults to ~11. Override per-run with `cli_assemble.py --clips`.
ASSEMBLY_CLIP_BUDGET = int(os.getenv("ASSEMBLY_CLIP_BUDGET", "11"))

# Hard speed cap. 2.2x (not 2.5x) because low-motion oil-painting clips read
# "too fast" sooner than action footage. Clips needing more are trimmed-past-cap.
ASSEMBLY_SPEED_CAP = float(os.getenv("ASSEMBLY_SPEED_CAP", "2.2"))

# Reverence cap: sacred clips (Christ / cross / resurrection / climax / close) must
# not be sped past this — accelerating a crucifixion or the gospel landing into a
# fast-cut "viral" feel fights the grace-anchored tone (constitution). Exceeding it
# is a hard gate FAIL, not a warning.
ASSEMBLY_REVERENCE_CAP = float(os.getenv("ASSEMBLY_REVERENCE_CAP", "1.3"))

# No slot shorter than this (seconds) — avoids subliminal flashes.
ASSEMBLY_MIN_SLOT = float(os.getenv("ASSEMBLY_MIN_SLOT", "0.8"))

# Bookend hold times. The cut always holds the HERO (the Christ / cross / NT-gospel
# pivot) for ASSEMBLY_HERO_TAIL seconds at the very end as the CTA landing. In the
# legacy "hero" open mode it ALSO holds the hero for ASSEMBLY_HERO_HEAD seconds at the
# very start; in the default "hook" open mode the head hold is unused (body plays from 0).
ASSEMBLY_HERO_HEAD = float(os.getenv("ASSEMBLY_HERO_HEAD", "2.0"))
ASSEMBLY_HERO_TAIL = float(os.getenv("ASSEMBLY_HERO_TAIL", "2.0"))

# How the cut OPENS (social-media decision, 2026-05-30: lead with MOTION, not a static
# hero — the first frame has to stop the scroll):
#   "hook" (DEFAULT) — open on the animated HOOK clip (the strongest scroll-stopper,
#       topic-driven; it does NOT have to be Jesus). No hero head bookend: the body plays
#       from t=0. The hero (Christ / cross / NT-pivot) still CLOSES the cut as the CTA.
#   "hero" — legacy: the hero bookends BOTH the open and the close (loop feel).
ASSEMBLY_OPEN_MODE = os.getenv("ASSEMBLY_OPEN_MODE", "hook").strip().lower()

# Render the HERO bookend(s) as a frozen STILL (default ON) instead of the animated hero
# clip. In "hook" open mode this affects only the CLOSING hero hold (a clean, reverent CTA
# freeze on Christ); in "hero" mode it affects both ends. Set ASSEMBLY_HERO_STILL=0 for a
# moving hero close/open.
ASSEMBLY_HERO_STILL = os.getenv("ASSEMBLY_HERO_STILL", "1") not in ("0", "false", "False", "")

# Default hero scene index (0 = let the planner choose; must be climax/kiss-family).
ASSEMBLY_HERO_SCENE = int(os.getenv("ASSEMBLY_HERO_SCENE", "0"))

# Output canvas + frame rate. 1080x1920 keeps the Kling source resolution; 30fps
# CFR so every segment shares cadence and concat stream-copies cleanly.
ASSEMBLY_CANVAS_W = int(os.getenv("ASSEMBLY_CANVAS_W", "1080"))
ASSEMBLY_CANVAS_H = int(os.getenv("ASSEMBLY_CANVAS_H", "1920"))
ASSEMBLY_FPS = int(os.getenv("ASSEMBLY_FPS", "30"))

# Build the 160s all-takes reel alongside the viral cut. Disable with --no-reel.
ASSEMBLY_REEL = os.getenv("ASSEMBLY_REEL", "1") not in ("0", "false", "False", "")

# Independent red-team audit of the edit plan (standard practice). Reuses the
# global INDEPENDENT_REVIEW unless overridden.
ASSEMBLY_INDEPENDENT_REVIEW = os.getenv(
    "ASSEMBLY_INDEPENDENT_REVIEW", "1" if INDEPENDENT_REVIEW else "0"
) not in ("0", "false", "False", "")

# ----------------------------------------------------------------------------
# Visual style base — Python constants, NOT model-returned.
#
# The scene-planning model returns ONLY the per-scene `subject_block` and
# `mood_block`. The renderer concatenates:
#
#   final_prompt = VISUAL_STYLE_BASE + " " + subject_block + ", " + mood_block + " " + VISUAL_STYLE_TAIL
#
# SP-G5 (Prompt Conformance) is therefore a regex on the per-scene blocks for
# banned tokens — the style base itself is unchangeable by construction.
# Pulled from the user's visual-director mega-prompt + master_blocks.style_block
# in PythonProject1/jesus/nano_banana_pro_batch_output/jesus_harmony_v1/_series.latest.json.
# ----------------------------------------------------------------------------
VISUAL_STYLE_BASE = (
    "Masterpiece Flemish Baroque oil painting in the style of Peter Paul Rubens, "
    "plain painted surface only with no frame, no borders, no canvas edges, no "
    "wooden frame visible,"
)

VISUAL_STYLE_TAIL = (
    "background fading into deep shadow, strong emotional intimacy, cinematic "
    "depth, rich ultramarine shadows and warm gold highlights, soft natural skin "
    "tones, dramatic chiaroscuro, visible brushstrokes, thick impasto, subtle "
    "craquelure, pure Flemish Baroque style only, no text, no modern elements, "
    "no fantasy glow, no excess drama --ar 9:16"
)

# Banned tokens checked by SP-G5 against `subject_block` + `mood_block`.
# Lower-case substring match; case-insensitive at check time.
VISUAL_BANNED_TOKENS = (
    "comic panel", "split screen", "split-screen", "diagram", "text overlay",
    "caption", "label", "frame", "border", "canvas edge", "wooden frame",
    "fantasy glow", "neon", "lens flare", "halo glow added", "glowing aura",
    "modern", "wristwatch", "eyeglasses", "smartphone", "photograph",
    "photorealistic", "3d render", "cartoon", "anime", "stained glass",
    "lightsaber", "gore", "blood spatter",
)


# Known ElevenLabs voices, validated in the existing narration tree / README.
# Only speakers actually present in a script are written to voices.json.
#
# Parable / miracle / encounter cast voices are *reused* from the six core
# voices above (until dedicated voice_ids are added). Sensible reuse: younger
# / mid males map to `disciples`, gravitas / authority males map to `god`,
# religious-authority and adversarial males map to `crowd` / `mocker`.
# FEMALE SPEAKERS are intentionally absent — there is no female voice_id in
# the core set yet, so `woman`, `mary`, `martha`, etc. fall through to the
# narrator (with a handoff warning) until a female voice is added.
VOICE_MAP = {
    "narrator":  "LSi9zNCeliLuhIGGS0By",   # Grounded Narrator (SLK IVC)
    "jesus":     "tlETan7Okc4pzjD0z62P",   # used across the existing narration tree
    "disciples": "puDRtQWF8NtQiPMJygTb",
    "crowd":     "SOYHLrjzK2X1ezoPC6cr",   # Harry – Fierce Warrior (mocking crowd)
    "mocker":    "SOYHLrjzK2X1ezoPC6cr",
    "god":       "1SSD79Zwju3tH7iqJo8a",   # God 1

    # Parable cast (re-using existing voices).
    "son":       "puDRtQWF8NtQiPMJygTb",   # ← disciples (younger/mid male)
    "father":    "1SSD79Zwju3tH7iqJo8a",   # ← god (gravitas, older)
    "servant":   "puDRtQWF8NtQiPMJygTb",   # ← disciples
    "master":    "1SSD79Zwju3tH7iqJo8a",   # ← god (parable master/king)
    "king":      "1SSD79Zwju3tH7iqJo8a",   # ← god
    "friend":    "puDRtQWF8NtQiPMJygTb",   # ← disciples
    "neighbour": "puDRtQWF8NtQiPMJygTb",   # ← disciples
    "traveler":  "puDRtQWF8NtQiPMJygTb",   # ← disciples
    "publican":  "puDRtQWF8NtQiPMJygTb",   # ← disciples (humbler male)

    # Religious authorities + miracle / encounter cast.
    "pharisee":  "SOYHLrjzK2X1ezoPC6cr",   # ← crowd/mocker (adversarial edge)
    "scribe":    "SOYHLrjzK2X1ezoPC6cr",   # ← crowd/mocker
    "lawyer":    "SOYHLrjzK2X1ezoPC6cr",   # ← crowd/mocker
    "priest":    "1SSD79Zwju3tH7iqJo8a",   # ← god (solemn)
    "centurion": "SOYHLrjzK2X1ezoPC6cr",   # ← crowd (warrior fits)
    "soldier":   "SOYHLrjzK2X1ezoPC6cr",   # ← crowd
    "man":       "puDRtQWF8NtQiPMJygTb",   # ← disciples (generic male)
    "paralytic": "puDRtQWF8NtQiPMJygTb",   # ← disciples
    "blind_man": "puDRtQWF8NtQiPMJygTb",   # ← disciples
    "leper":     "puDRtQWF8NtQiPMJygTb",   # ← disciples
    "demoniac":  "SOYHLrjzK2X1ezoPC6cr",   # ← crowd (rough/angry edge fits)

    # Named NT speakers — reuse the disciples (younger/mid male) voice so any
    # named character SPEAKS in dialogue rather than collapsing to the narrator
    # (the "multi-voice wherever the scene has speakers" rule). Adversaries take
    # the crowd/mocker edge; female names still fall through (no female voice yet).
    "peter":      "puDRtQWF8NtQiPMJygTb", "simon":   "puDRtQWF8NtQiPMJygTb",
    "john":       "puDRtQWF8NtQiPMJygTb", "james":   "puDRtQWF8NtQiPMJygTb",
    "andrew":     "puDRtQWF8NtQiPMJygTb", "philip":  "puDRtQWF8NtQiPMJygTb",
    "thomas":     "puDRtQWF8NtQiPMJygTb", "nathanael":"puDRtQWF8NtQiPMJygTb",
    "matthew":    "puDRtQWF8NtQiPMJygTb", "disciple": "puDRtQWF8NtQiPMJygTb",
    "apostle":    "puDRtQWF8NtQiPMJygTb", "bartimaeus":"puDRtQWF8NtQiPMJygTb",
    "zacchaeus":  "puDRtQWF8NtQiPMJygTb", "nicodemus": "puDRtQWF8NtQiPMJygTb",
    "thief":      "puDRtQWF8NtQiPMJygTb", "beggar":    "puDRtQWF8NtQiPMJygTb",
    "ruler":      "puDRtQWF8NtQiPMJygTb", "judas":     "SOYHLrjzK2X1ezoPC6cr",
}

# Per-speaker sticky audio tag prepended to each of that speaker's turns.
VOICE_AUDIO_TAGS = {
    "crowd": "[mocking]",
    "mocker": "[mocking]",
}


def require_api_key() -> str:
    # Agent-mode answers every LLM call via the in-chat bridge — no metered API,
    # so a missing/cap-limited key must NOT block the run.
    if agent_mode():
        return ANTHROPIC_API_KEY
    if not ANTHROPIC_API_KEY:
        raise SystemExit(
            "ANTHROPIC_API_KEY is not set. Add it to "
            f"{PROJECT_ROOT / '.env'} (KEY=value)."
        )
    return ANTHROPIC_API_KEY
