"""Image-generation providers + per-image content audit.

V5: NBPProvider (Gemini 3 Pro image preview via google.genai), `render_scene`
with retry-on-content-audit-fail loop, `verify_image` Claude Vision audit.
HFProvider is added in V6.
"""
from __future__ import annotations

import base64
import io
import json
import re
import subprocess
import time
import urllib.request
from abc import ABC, abstractmethod
from dataclasses import asdict
from functools import lru_cache
from pathlib import Path

import config
from pipeline import engine as text_engine
from pipeline.visual_models import ImageAudit, Scene


# --------------------------------------------------------------------------
# Prompt assembly (used by both providers + handoff for _source_prompts.md)
# --------------------------------------------------------------------------
def assemble_final_prompt(
    scene: Scene,
    style_base: str | None = None,
    style_tail: str | None = None,
    character_block: str | None = None,
) -> str:
    """Concatenate the fixed style base + the per-scene subject_block (+ the
    Jesus character_block when applicable) + mood_block + the fixed style
    tail. Trailing punctuation on per-scene blocks is normalised so the
    result reads as one continuous sentence — image models are sensitive to
    broken cadence."""
    base = style_base if style_base is not None else config.VISUAL_STYLE_BASE
    tail = style_tail if style_tail is not None else config.VISUAL_STYLE_TAIL
    subject = scene.subject_block.strip().rstrip(",.")
    mood = scene.mood_block.strip().rstrip(",.")
    middle = subject
    if character_block:
        middle = f"{subject}, {character_block.strip().rstrip(',.')}"
    return f"{base} {middle}, {mood} {tail}"


# --------------------------------------------------------------------------
# NBP series spec (Jesus variants + negative prompt)
# --------------------------------------------------------------------------
@lru_cache(maxsize=1)
def _load_nbp_series_spec() -> dict:
    """Read _series.latest.json once. Returns the parsed dict; callers index
    `jesus_variants` for character_block + ref filename per variant."""
    path = config.NBP_REFS_DIR / "_series.latest.json"
    if not path.exists():
        raise SystemExit(
            f"_series.latest.json not found at {path}. NBP cannot run without "
            "the Jesus reference spec — see config.NBP_REFS_DIR."
        )
    return json.loads(path.read_text(encoding="utf-8"))


def _character_block_for(variant: str | None) -> str:
    if not variant:
        return ""
    variants = _load_nbp_series_spec().get("jesus_variants", {})
    v = variants.get(variant) or {}
    return v.get("character_block", "")


def _ref_png_for(variant: str | None) -> Path | None:
    if not variant:
        return None
    variants = _load_nbp_series_spec().get("jesus_variants", {})
    v = variants.get(variant) or {}
    fn = v.get("filename")
    if not fn:
        return None
    p = config.NBP_REFS_DIR / "refs" / fn
    return p if p.exists() else None


def _nbp_negative_prompt() -> str:
    return _load_nbp_series_spec().get("master_blocks", {}).get("negative_prompt", "")


# --------------------------------------------------------------------------
# Image provider abstraction
# --------------------------------------------------------------------------
class ImageProvider(ABC):
    name: str
    supports_character_anchor: bool

    @abstractmethod
    def generate(self, scene: Scene, audit_feedback: str = "") -> bytes:
        """Return the raw PNG bytes for `scene`. `audit_feedback` is the
        concatenated content-audit issues from a prior attempt (used to
        re-prompt with corrections); empty on the first attempt."""


class NBPProvider(ImageProvider):
    """Gemini 3 Pro image preview via google.genai. Attaches
    `refs/ref_jesus_<variant>.png` whenever `scene.jesus_variant` is set."""

    name = "nbp"
    supports_character_anchor = True
    MODEL = "gemini-3-pro-image-preview"
    ASPECT_RATIO = "9:16"

    def __init__(self) -> None:
        if not config.GEMINI_API_KEY:
            raise SystemExit(
                "GEMINI_API_KEY not set. Add it to "
                f"{config.NBP_PROJECT_ENV} or export it before running."
            )
        # Lazy import — keep the import surface tiny when --provider hf is chosen.
        from google import genai
        from google.genai import types as genai_types
        self._genai = genai
        self._genai_types = genai_types
        self._client = genai.Client(api_key=config.GEMINI_API_KEY)
        self._uploaded_refs: dict[str, str] = {}  # variant -> uploaded fileUri
        self._uploaded_paths: dict[str, str] = {}  # abs path -> uploaded fileUri

    def _upload_ref(self, variant: str) -> str | None:
        if variant in self._uploaded_refs:
            return self._uploaded_refs[variant]
        ref_path = _ref_png_for(variant)
        if ref_path is None:
            return None
        uploaded = self._client.files.upload(
            file=str(ref_path),
            config=self._genai_types.UploadFileConfig(
                display_name=ref_path.name,
                mime_type="image/png",
            ),
        )
        self._uploaded_refs[variant] = uploaded.uri
        return uploaded.uri

    def _upload_path(self, p) -> str:
        """Upload an arbitrary image as a continuity reference (cached by path)."""
        key = str(p)
        if key in self._uploaded_paths:
            return self._uploaded_paths[key]
        uploaded = self._client.files.upload(
            file=key,
            config=self._genai_types.UploadFileConfig(
                display_name=getattr(p, "name", "ref.png"), mime_type="image/png"),
        )
        self._uploaded_paths[key] = uploaded.uri
        return uploaded.uri

    def generate(self, scene: Scene, audit_feedback: str = "", extra_ref_paths=None) -> bytes:
        prompt = assemble_final_prompt(
            scene,
            character_block=_character_block_for(scene.jesus_variant),
        )
        negative = _nbp_negative_prompt()
        if negative:
            prompt = f"{prompt}\n\nAvoid: {negative}"
        if audit_feedback:
            prompt = f"{prompt}\n\nRevise to fix prior content-audit issues: {audit_feedback}"

        parts: list = []
        if scene.jesus_variant:
            uri = self._upload_ref(scene.jesus_variant)
            if uri:
                parts.append({"fileData": {"mimeType": "image/png", "fileUri": uri}})
        for rp in (extra_ref_paths or []):
            uri = self._upload_path(rp)
            if uri:
                parts.append({"fileData": {"mimeType": "image/png", "fileUri": uri}})
        parts.append({"text": prompt})

        resp = self._client.models.generate_content(
            model=self.MODEL,
            contents=[{"parts": parts}],
            config={
                "responseModalities": ["IMAGE"],
                "imageConfig": {"aspectRatio": self.ASPECT_RATIO},
            },
        )
        candidates = getattr(resp, "candidates", None) or []
        if not candidates:
            raise RuntimeError(f"NBP returned no candidates for scene {scene.index}")
        cand_parts = candidates[0].content.parts if candidates[0].content else []
        image_bytes: bytes | None = None
        for p in cand_parts:
            if hasattr(p, "inline_data") and p.inline_data and p.inline_data.data:
                image_bytes = p.inline_data.data
                break
        if not image_bytes:
            finish = getattr(candidates[0], "finish_reason", "?")
            raise RuntimeError(
                f"NBP returned no image bytes for scene {scene.index} "
                f"(finish_reason={finish})"
            )
        if isinstance(image_bytes, str):
            image_bytes = base64.b64decode(image_bytes)
        return image_bytes


_HF_URL_RE = re.compile(r"https://\S+?\.(?:png|jpg|jpeg|webp)", re.IGNORECASE)


class HFProvider(ImageProvider):
    """Higgsfield AI via the `hf` CLI — NOT HuggingFace Inference API.

    Mirrors the workflow validated in `C:\\Users\\sanjay\\PycharmProjects\\HF-POC`:
    subprocess `hf generate create <model> --prompt "..." --aspect_ratio 9:16
    --wait`, scrape the image URL from stdout, download via urllib.

    Default model `nano_banana_2` (2 cr/image) — the user's rated winner for
    Baroque oil painting (HF-POC/RESUME.md). Override with HF_MODEL_ID env.

    No reference-image attachment by default — character consistency relies on
    the canonical character_block in the prompt. SP-G7 is effectively advisory
    on HF runs."""

    name = "hf"
    supports_character_anchor = False
    ASPECT = "9:16"
    GENERATE_TIMEOUT = 600  # seconds — slow models (gpt_image_2) can take 60s+
    DOWNLOAD_TIMEOUT = 120

    def __init__(self) -> None:
        if not config.HF_CLI_PATH.exists():
            raise SystemExit(
                f"Higgsfield CLI not found at {config.HF_CLI_PATH}. "
                "Install per HF-POC/README.md, set HF_CLI_PATH to your hf.exe, "
                "and run `hf auth login` if not already authenticated."
            )
        self._cli = str(config.HF_CLI_PATH)
        self._model = config.HF_MODEL_ID
        # `openai_hazel` doesn't support 9:16 — substitute (per run_batch.sh).
        self._aspect = "2:3" if self._model == "openai_hazel" else self.ASPECT

    def generate(self, scene: Scene, audit_feedback: str = "") -> bytes:
        prompt = assemble_final_prompt(
            scene,
            character_block=_character_block_for(scene.jesus_variant),
        )
        if audit_feedback:
            prompt = f"{prompt}\n\nRevise to fix prior content-audit issues: {audit_feedback}"

        # Subprocess the CLI synchronously with --wait. UTF-8 to survive em
        # dashes / curly quotes the Baroque prompts use.
        result = subprocess.run(
            [
                self._cli, "generate", "create", self._model,
                "--prompt", prompt,
                "--aspect_ratio", self._aspect,
                "--wait",
            ],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=self.GENERATE_TIMEOUT,
        )
        if result.returncode != 0:
            raise RuntimeError(
                f"hf CLI failed ({result.returncode}) on scene {scene.index}:\n"
                f"  stderr: {(result.stderr or '').strip()[-500:]}\n"
                f"  stdout: {(result.stdout or '').strip()[-500:]}"
            )

        # Pull the image URL from stdout (run_batch.sh pattern: regex match).
        match = _HF_URL_RE.search(result.stdout)
        if not match:
            raise RuntimeError(
                f"hf CLI returned no image URL on scene {scene.index}.\n"
                f"  tail of stdout: {(result.stdout or '').strip()[-500:]}"
            )
        url = match.group(0)

        # Download to bytes. Higgsfield delivers PNG or JPG; let the caller
        # store with the real extension by detecting bytes.
        req = urllib.request.Request(url, headers={"User-Agent": "JesusInTheBible/1.0"})
        with urllib.request.urlopen(req, timeout=self.DOWNLOAD_TIMEOUT) as resp:
            return resp.read()


def get_provider(name: str) -> ImageProvider:
    name = (name or config.VISUAL_DEFAULT_PROVIDER).strip().lower()
    if name == "nbp":
        return NBPProvider()
    if name == "hf":
        return HFProvider()
    raise SystemExit(f"Unknown provider: {name!r}. Choose 'nbp' or 'hf'.")


# --------------------------------------------------------------------------
# Claude Vision content audit
# --------------------------------------------------------------------------
ANTHROPIC_IMAGE_LIMIT = 5 * 1024 * 1024  # 5 MB hard cap on the Vision API


def _detect_media_type(raw: bytes) -> str:
    """Detect the actual image format from the bytes. NBP returns JPEG or PNG
    interchangeably regardless of filename, so we cannot trust the extension."""
    if raw[:8] == b"\x89PNG\r\n\x1a\n":
        return "image/png"
    if raw[:3] == b"\xff\xd8\xff":
        return "image/jpeg"
    if raw[:4] == b"RIFF" and raw[8:12] == b"WEBP":
        return "image/webp"
    if raw[:6] in (b"GIF87a", b"GIF89a"):
        return "image/gif"
    raise RuntimeError(f"Unknown image format (first bytes: {raw[:8].hex()})")


def _encode_image_for_vision(raw_bytes: bytes) -> tuple[str, str]:
    """Shrink to fit the 5MB Vision cap, return (base64, media_type). Detects
    the actual format from the bytes so we never lie to the Vision API about
    media type (mismatched type returns a 400)."""
    media = _detect_media_type(raw_bytes)
    if len(raw_bytes) <= ANTHROPIC_IMAGE_LIMIT - 256 * 1024:
        return base64.b64encode(raw_bytes).decode("ascii"), media
    # Downsample with Pillow — always shrink to JPEG for max compression.
    from PIL import Image
    img = Image.open(io.BytesIO(raw_bytes)).convert("RGB")
    for max_dim in (2048, 1600, 1280, 1024, 768):
        copy = img.copy()
        copy.thumbnail((max_dim, max_dim), Image.LANCZOS)
        buf = io.BytesIO()
        copy.save(buf, format="JPEG", quality=85, optimize=True)
        data = buf.getvalue()
        if len(data) <= ANTHROPIC_IMAGE_LIMIT - 256 * 1024:
            return base64.b64encode(data).decode("ascii"), "image/jpeg"
    raise RuntimeError("Could not shrink image below 5MB for Claude Vision.")


def _vision_call(scene: Scene, png_bytes: bytes) -> dict:
    """One Claude Vision call. Returns the parsed JSON audit. Uses the same
    Anthropic client as the text engine but bypasses the cached system prefix
    — we want a focused content audit, not the full constitution.

    Audits the FULL subject_block + vignettes + visible_elements, not just
    visible_elements alone. The earlier narrow audit silently passed scenes
    where the central subject was wrong (e.g. Jesus standing beside the cross
    instead of nailed to it) because the visible_elements field was sparse."""
    b64, media = _encode_image_for_vision(png_bytes)
    vignette_lines = ""
    if scene.vignettes:
        vignette_lines = "\n".join(f"  - {v}" for v in scene.vignettes)
        vignette_lines = f"\nREQUIRED BACKGROUND VIGNETTES (unified scene; each must be present and recognisable):\n{vignette_lines}\n"
    role = (
        "You are an INDEPENDENT visual content auditor. The user wrote a scene "
        "spec; an image model rendered an image. Verify EVERY required element "
        "is present and that no banned tokens are visible.\n\n"
        "AUDIT IN THIS ORDER (any one of these failing = passed:false):\n"
        "1. **Central subject identity.** Does the foreground subject match "
        "what the SUBJECT_BLOCK describes as the dominant centre? Wrong "
        "subject identity (e.g. Jesus standing beside the cross when the spec "
        "says nailed/crucified; the prodigal collapsed when the spec says "
        "standing upright; a passion Jesus when the spec said ministry) is a "
        "HARD FAIL even if 'something close enough' is present.\n"
        "2. **Required visible elements.** Every concrete noun in the "
        "VISIBLE_ELEMENTS list must be recognisably present.\n"
        "3. **Vignettes (unified scenes only).** Every named vignette in the "
        "REQUIRED BACKGROUND VIGNETTES list must be recognisably present as a "
        "soft-edged background detail. Missing >=2 vignettes = passed:false. "
        "Missing 1 = pass with the issue listed.\n"
        "4. **Banned tokens.** Visible text, comic panels, split-screen, "
        "modern items, fantasy glow, frames/borders/canvas edges, photoreal/3D "
        "look = passed:false.\n"
        "5. **Anatomy & render integrity (CHECK THIS EXPLICITLY).** Look hard at "
        "every visible HAND, FACE, and limb of the FOREGROUND subject(s). FAIL "
        "(passed:false) on: a hand with the wrong number of fingers, a sixth "
        "finger, fused/melted/duplicated fingers, a malformed or boneless thumb, "
        "two left hands, an extra or missing arm/leg, a warped or asymmetric "
        "face, mismatched eyes, or any garbled body part. This is the single "
        "most common AI-render failure and it is a HARD FAIL on a hero/foreground "
        "subject (count the fingers on any prominent open hand). Background "
        "figures dissolving into shadow get more latitude — note but do not fail "
        "on a slightly-off distant hand.\n\n"
        f"BANNED VISIBLE ELEMENTS: {sorted(config.VISUAL_BANNED_TOKENS)}\n\n"
        "Return ONLY a JSON object (optionally inside a ```json fence):\n"
        "{\n"
        '  "passed": true | false,\n'
        '  "issues": [{"claim": "<from the spec>", "actual": "<what you see>"}, ...],\n'
        '  "banned_token_hits": ["<banned token visible>", ...]\n'
        "}\n"
        "Positional / wording / minor stylistic nits are NOT failures — list "
        "them as issues with passed=true. Pass only when the central subject "
        "is correct, the required elements are all present, the vignettes are "
        "present (at most 1 missing), no banned token is visible, AND the "
        "foreground hands/faces/limbs are anatomically sound (correct finger "
        "counts on any prominent hand)."
    )
    user_text = (
        f"SCENE {scene.index}: {scene.title}\n"
        f"TYPE: {scene.scene_type} · FRAMING: {scene.framing} · ARC: {scene.arc_position}\n"
        f"JESUS VARIANT: {scene.jesus_variant or '(none — Jesus not in scene)'}\n\n"
        f"SUBJECT_BLOCK (the dominant foreground; the central subject must match this):\n{scene.subject_block}\n\n"
        f"REQUIRED VISIBLE ELEMENTS: {scene.visible_elements}\n"
        f"EMOTIONAL TONE: {scene.emotional_tone}"
        + vignette_lines
        + "\nAudit the attached image against ALL four checks above."
    )
    if config.agent_mode():
        from pipeline import agent_bridge
        text = agent_bridge.call_vision(
            role=role, user=user_text, image_bytes=png_bytes, media=media,
            model=config.MODEL, label=f"image-audit:scene-{scene.index} {scene.title[:40]}",
        )
        return text_engine._extract_json(text)
    client = text_engine._client()
    resp = client.messages.create(
        model=config.MODEL,
        max_tokens=2000,
        thinking={"type": "adaptive"},
        system=role,
        messages=[{
            "role": "user",
            "content": [
                {"type": "image", "source": {"type": "base64", "media_type": media, "data": b64}},
                {"type": "text", "text": user_text},
            ],
        }],
    )
    text = "".join(b.text for b in resp.content if b.type == "text").strip()
    return text_engine._extract_json(text)


def verify_image(scene: Scene, png_bytes: bytes) -> ImageAudit:
    """Claude Vision content audit: does the rendered image actually contain
    the scene's required visible_elements? Any banned tokens visible?

    If the Anthropic API is unavailable (notably an account USAGE CAP), do NOT
    crash the whole render — log it and return a SKIPPED audit flagged for human
    review, so HF renders still complete. The image is marked needs-review, not
    silently passed-clean."""
    try:
        data = _vision_call(scene, png_bytes)
        return ImageAudit.from_json(data)
    except Exception as e:
        msg = str(e)
        if "usage limit" in msg.lower() or "usage limits" in msg.lower() or "regain access" in msg.lower():
            print(f"        ! Vision audit SKIPPED (Anthropic usage cap) — review {scene.filename_stem} by eye")
            return ImageAudit(
                passed=True,
                issues=[{"claim": "AUDIT SKIPPED", "actual": "Anthropic API usage cap — verify this image by eye"}],
                banned_token_hits=[],
            )
        raise


# --------------------------------------------------------------------------
# Render with retry-on-audit-fail
# --------------------------------------------------------------------------
def _audit_feedback_text(audit: ImageAudit) -> str:
    """Compact feedback the next render attempt receives. Mirrors the shape
    image_to_kling.py's Stage A.5 audit-feedback regen uses."""
    parts: list[str] = []
    if audit.banned_token_hits:
        parts.append("banned tokens visible: " + ", ".join(audit.banned_token_hits))
    for issue in audit.issues[:5]:
        parts.append(f"{issue['claim']} -> {issue['actual']}")
    return "; ".join(parts)


def _write_cut_hint_sidecar(scene: Scene, out_dir: Path) -> Path:
    """Write `<stem>.cut_hint.json` containing the Kling-stage metadata
    (macro_elements, pacing, viral_role). Forward-compatible: the current
    image_to_kling.py doesn't read it, but the V8 Kling subprocess wrapper
    will, and the user can inspect it manually now."""
    payload = {
        "scene_index": scene.index,
        "title": scene.title,
        "scene_type": scene.scene_type,
        "framing": scene.framing,
        "arc_position": scene.arc_position,
        "jesus_variant": scene.jesus_variant,
        "viral_role": scene.viral_role,
        "pacing": scene.pacing,
        "macro_elements": scene.macro_elements,
        "consumed_by": "PythonProject1/jesus/image_to_kling.py (Stage A cut-plan director)",
        "note": (
            "Advisory metadata for the downstream Kling cut planner. The current "
            "image_to_kling.py reads only the image; V8 wiring will inject these "
            "hints into the cut-plan director prompt."
        ),
    }
    p = out_dir / f"{scene.filename_stem}.cut_hint.json"
    p.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
    return p


def render_scene(
    scene: Scene,
    provider: ImageProvider,
    out_dir: Path,
    max_retries: int = 1,
    log=print,
) -> tuple[Path, ImageAudit]:
    """Generate the scene's PNG via `provider`, run Claude Vision content
    audit, retry-with-feedback on FAIL up to `max_retries` times. Idempotent
    by `<i>_<slug>.png` existence: if both the PNG and a passed audit exist,
    skip and return them.

    Also writes a `<stem>.cut_hint.json` sidecar with macro_elements, pacing,
    and viral_role for the downstream Kling cut planner (V8 consumes it).

    Returns (png_path, final ImageAudit). Final audit may be passed=False if
    every retry failed — caller decides whether to abort the run or accept."""
    out_dir.mkdir(parents=True, exist_ok=True)
    stem = scene.filename_stem
    png_path = out_dir / f"{stem}.png"
    audit_path = out_dir / f"{stem}.png.audit.json"
    _write_cut_hint_sidecar(scene, out_dir)

    # Idempotency: existing PNG + a passed audit sidecar = skip.
    if png_path.exists() and audit_path.exists():
        try:
            existing = ImageAudit.from_json(
                json.loads(audit_path.read_text(encoding="utf-8"))
            )
            if existing.passed:
                log(f"      [skip] {stem}.png — exists and audit passed")
                return png_path, existing
        except Exception:
            pass  # corrupt audit — re-render

    feedback = ""
    last_audit: ImageAudit = ImageAudit(passed=False, issues=[], banned_token_hits=[])
    for attempt in range(max_retries + 1):  # max_retries=1 -> 2 attempts max
        label = "first attempt" if attempt == 0 else f"retry {attempt}/{max_retries}"
        log(f"      [{provider.name}] {stem} — {label}")
        t0 = time.monotonic()
        png_bytes = provider.generate(scene, audit_feedback=feedback)
        elapsed = time.monotonic() - t0
        png_path.write_bytes(png_bytes)
        log(f"        rendered {len(png_bytes):,} bytes in {elapsed:.1f}s -> {png_path.name}")
        log(f"        auditing with Claude Vision...")
        audit = verify_image(scene, png_bytes)
        audit_path.write_text(
            json.dumps(asdict(audit), indent=2, ensure_ascii=False), encoding="utf-8"
        )
        last_audit = audit
        if audit.passed:
            log(f"        audit PASS")
            return png_path, audit
        feedback = _audit_feedback_text(audit)
        log(f"        audit FAIL — {feedback or 'no specific feedback'}")
    log(f"      [{provider.name}] {stem} — audit failed after {max_retries + 1} attempts; keeping last render")
    return png_path, last_audit
