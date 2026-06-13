"""The Upload Kit engine: harvest finished-media facts -> generate per-platform
metadata -> in-engine red-team. LLM calls route through engine._call, so in
agent-mode (LLM_PROVIDER=agent) they go to the in-chat agent via the file bridge
(no metered API), exactly like the narration/visual stages.
"""
from __future__ import annotations

import json
from pathlib import Path

import config
from pipeline import engine, scripture
from pipeline.upload_models import (
    PlatformMeta,
    SourceFacts,
    TitleCandidate,
    UploadKit,
)

PLATFORM_ORDER = ["youtube_short", "youtube_long", "tiktok", "facebook", "instagram"]


# --------------------------------------------------------------------------
# Brand + footer
# --------------------------------------------------------------------------
def load_brand() -> dict:
    return json.loads((config.DATA_DIR / "upload_brand.json").read_text(encoding="utf-8"))


def _filled(v: str | None) -> bool:
    return bool(v) and "FILL_ME" not in str(v)


def build_footer(platform: str, brand: dict) -> str:
    """Verbatim brand footer. Full (with links) on YouTube/Facebook; minimal,
    link-free on TikTok/Instagram (links aren't clickable there)."""
    cta = (brand.get("cta_line") or "").strip()
    handles = brand.get("handles", {})
    scripture_note = (brand.get("scripture_note") or "").strip()
    website = brand.get("website")

    lines: list[str] = []
    if cta:
        lines.append(cta)

    link_friendly = platform.startswith("youtube") or platform == "facebook"
    if link_friendly:
        follow: list[str] = []
        for plat, key in [("YouTube", "youtube"), ("TikTok", "tiktok"),
                          ("Facebook", "facebook"), ("Instagram", "instagram")]:
            h = handles.get(key, {})
            handle, url = h.get("handle"), h.get("url")
            if _filled(handle):
                follow.append(f"{plat}: {handle}" + (f" — {url}" if _filled(url) else ""))
        if follow:
            lines.append("")
            lines.append("Follow:")
            lines.extend(follow)
        if _filled(website):
            lines.append("")
            lines.append(website)
    else:
        # minimal sign-off, no URLs
        key = "tiktok" if platform == "tiktok" else "instagram"
        handle = handles.get(key, {}).get("handle")
        if _filled(handle):
            lines.append(f"Follow {handle}")

    # Public-domain note only on the link-friendly long-copy platforms; keep
    # TikTok/Instagram captions punchy.
    if scripture_note and link_friendly:
        lines.append("")
        lines.append(scripture_note)
    return "\n".join(lines).strip()


# --------------------------------------------------------------------------
# Harvest source facts from a finished-media folder
# --------------------------------------------------------------------------
def _find_video(media_dir: Path, fmt: str) -> str:
    cands: list[Path] = []
    if fmt == "short":
        a = media_dir / "assembly"
        cands = [
            a / "viral_cut_sfx_captioned.mp4",
            a / "viral_cut_captioned.mp4",
            a / "viral_cut_sfx.mp4",
            a / "viral_cut.mp4",
        ]
    else:
        v = media_dir / "visual_16x9"
        cands = sorted(v.glob("*_captioned.mp4")) + sorted(v.glob("*.mp4"))
    for c in cands:
        if Path(c).is_file():
            return str(Path(c).resolve())
    return ""


def _first_sentence(text: str) -> str:
    t = " ".join(text.split())
    for end in (". ", "? ", "! "):
        i = t.find(end)
        if 0 < i < 160:
            return t[: i + 1].strip()
    return t[:160].strip()


def harvest_facts(media_dir: str) -> SourceFacts:
    d = Path(media_dir).resolve()
    creation = json.loads((d / "narration.creation.json").read_text(encoding="utf-8"))
    fmt = "short" if "shorts" in d.parts else "long"

    thread = creation.get("thread", {}) or {}
    episode = creation.get("episode", {}) or {}
    series = creation.get("series", {}) or {}
    anchor_ref = thread.get("anchor_ref") or episode.get("primary_ref") or ""
    anchor_kjv = (creation.get("kjv_text") or "").strip()
    if not anchor_kjv and anchor_ref:
        anchor_kjv = (scripture.fetch_kjv(anchor_ref) or "").strip()

    spoken = ""
    for name in ("spoken_script.txt", "narration.md"):
        p = d / name
        if p.is_file():
            spoken = p.read_text(encoding="utf-8")
            break

    beats = creation.get("beat_ids") or [b for b in (creation.get("structure", {}) or {}).get("beats", [])]

    return SourceFacts(
        media_dir=str(d),
        video_path=_find_video(d, fmt),
        format=fmt,
        series_name=series.get("name", ""),
        brand=series.get("brand", "SLK"),
        episode_title=episode.get("title", d.name),
        anchor_ref=anchor_ref,
        anchor_kjv=anchor_kjv,
        kjv_verified=bool(creation.get("kjv_verified")),
        thread=thread.get("thread", ""),
        thread_lever=thread.get("lever", ""),
        hook_line=_first_sentence(spoken) if spoken else "",
        spoken_script=" ".join(spoken.split())[:4000],
        beats=beats,
    )


# --------------------------------------------------------------------------
# Generation (LLM via engine._call -> agent bridge or API)
# --------------------------------------------------------------------------
_GEN_ROLE = """You are the UPLOAD-METADATA writer for a Christian Bible-shorts channel.
You take ONE finished video's facts and write ready-to-paste upload metadata for
five platform slots: YouTube (short), YouTube (long-form), TikTok, Facebook, Instagram.

HARD RULES (a violation makes the whole kit fail an automated gate):
- Titles are HOOKY BUT HONEST: a curiosity hook that is TRUE to the text. NEVER
  clickbait, never sensational, never an overclaim about doctrine or history.
  Freshness is about the TEXT (a surprising detail), never about the truth.
- CTA-to-Jesus spirit: the content points to Christ. No fear / gain-loss framing.
- If you quote the anchor verse, quote it VERBATIM KJV exactly as given — do not
  alter a single word. Prefer to quote it in the YouTube/Facebook descriptions.
- Do NOT write the brand footer or follow links — those are stamped in later.
  End each description with the BODY only (hook + summary + verse + a short CTA line).
- Respect platform character budgets you are given. Keep TikTok/Instagram captions
  punchy with the hook in the FIRST line.
- Hashtags start with '#', no spaces. Mix broad (#Bible #Jesus) with niche
  (passage / theme specific). Tags (YouTube only) are plain keywords, comma-free.

Return ONLY a JSON object, no prose, with this exact shape:
{
  "title_candidates": [ {"text": "...", "angle": "..."}, ... 4 items, best first ],
  "platforms": {
    "youtube_short": {"title": "...", "description_body": "...", "tags": ["kw", ...], "hashtags": ["#..", ..]},
    "youtube_long":  {"title": "...", "description_body": "...", "tags": ["kw", ...], "hashtags": ["#..", ..]},
    "tiktok":        {"title": "", "description_body": "...", "tags": [], "hashtags": ["#..", ..]},
    "facebook":      {"title": "...", "description_body": "...", "tags": [], "hashtags": ["#..", ..]},
    "instagram":     {"title": "", "description_body": "...", "tags": [], "hashtags": ["#..", ..]}
  }
}
The chosen title (title_candidates[0].text) should be reused as the youtube_short title."""


def _gen_user(facts: SourceFacts, specs: dict) -> str:
    budgets = {
        k: {
            "title_max": specs[k]["title"]["max"],
            "title_target": [specs[k]["title"].get("target_min"), specs[k]["title"].get("target_max")],
            "desc_target": [specs[k]["description"].get("target_min"), specs[k]["description"].get("target_max")],
            "hashtags_target": [specs[k]["hashtags"].get("target_min"), specs[k]["hashtags"].get("target_max")],
            "tags_target": [specs[k]["tags"].get("target_count_min"), specs[k]["tags"].get("target_count_max")],
        }
        for k in PLATFORM_ORDER
    }
    fmt_note = ("This is a 60-second VERTICAL SHORT." if facts.format == "short"
               else "This is a 6-8 minute 16:9 LONG-FORM deep-dive.")
    return (
        f"FORMAT: {fmt_note}\n"
        f"SERIES: {facts.series_name} (brand {facts.brand})\n"
        f"EPISODE TITLE (internal): {facts.episode_title}\n"
        f"ANCHOR VERSE ({facts.anchor_ref}), EXACT KJV — quote verbatim if you quote it:\n"
        f"  \"{facts.anchor_kjv}\"\n"
        f"THREAD (the one spine, hook->CTA): {facts.thread}\n"
        f"LEVER: {facts.thread_lever}\n"
        f"OPENING SPOKEN HOOK: {facts.hook_line}\n"
        f"FULL NARRATION (for keyword grounding, do not quote loosely):\n{facts.spoken_script}\n\n"
        f"PER-PLATFORM CHARACTER/COUNT BUDGETS (targets to aim for, never exceed 'max'):\n"
        f"{json.dumps(budgets, indent=2)}\n\n"
        "Write the JSON now."
    )


def generate(facts: SourceFacts) -> dict:
    """Call the model to produce the raw per-platform metadata JSON."""
    from pipeline.upload_gates import load_specs
    specs = load_specs()
    raw = engine._call(_GEN_ROLE, _gen_user(facts, specs), label="upload-gen")
    return engine._extract_json(raw)


def assemble_kit(facts: SourceFacts, raw: dict, brand: dict) -> UploadKit:
    """Turn the model's raw JSON + the brand footer into a structured UploadKit."""
    from pipeline.upload_gates import load_specs
    specs = load_specs()
    platforms: list[PlatformMeta] = []
    for key in PLATFORM_ORDER:
        block = (raw.get("platforms", {}) or {}).get(key, {}) or {}
        body = (block.get("description_body") or "").strip()
        footer = build_footer(key, brand)
        description = f"{body}\n\n{footer}".strip() if footer else body
        platforms.append(PlatformMeta(
            platform=key,
            label=specs[key]["label"],
            title=(block.get("title") or "").strip(),
            description=description,
            tags=[t.strip() for t in (block.get("tags") or []) if t.strip()],
            hashtags=[h.strip() for h in (block.get("hashtags") or []) if h.strip()],
        ))
    cands = [TitleCandidate(text=c.get("text", ""), angle=c.get("angle", ""))
             for c in (raw.get("title_candidates") or [])]
    if cands:
        cands[0].chosen = True
        cands[0].reason = "highest-ranked hook by the generator"
    return UploadKit(source=facts, platforms=platforms, title_candidates=cands)


# --------------------------------------------------------------------------
# In-engine red-team (hostile auditor)
# --------------------------------------------------------------------------
_REDTEAM_ROLE = """You are a HOSTILE, independent auditor of upload metadata for a
Christian Bible-shorts channel. Your job is to BREAK this kit, not bless it.

Scrutinise every title/description/hashtag for:
- Clickbait / sensationalism / curiosity-gap that LIES about the text.
- Doctrinal overclaim or anything a careful believer would call misleading.
- A quoted verse that is not verbatim KJV.
- Off-thread metadata (promises something the video doesn't deliver).
- Platform mismatch (wrong tone for TikTok vs YouTube long-form, weak first line).
- Generic / templated / forgettable titles that won't earn the click honestly.

Output plain text:
VERDICT: PASS | REVISE | FAIL
Then a short bullet list of the most important problems, each citing the exact
platform + offending phrase, and a concrete fix. Be specific and ruthless."""


def redteam(kit: UploadKit) -> str:
    payload = {
        "source": {
            "episode": kit.source.episode_title,
            "anchor_ref": kit.source.anchor_ref,
            "anchor_kjv": kit.source.anchor_kjv,
            "thread": kit.source.thread,
        },
        "platforms": [p.to_dict() for p in kit.platforms],
        "title_candidates": [c.to_dict() for c in kit.title_candidates],
    }
    user = ("Audit this upload kit. Be hostile.\n\n" + json.dumps(payload, indent=2, ensure_ascii=False))
    return engine._call(_REDTEAM_ROLE, user, model=config.REVIEW_MODEL or None, label="upload-redteam").strip()
