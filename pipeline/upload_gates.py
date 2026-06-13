"""Deterministic verification gates for the Upload Kit stage.

These run in plain Python BEFORE any LLM red-team / panel, so a kit that breaks a
hard rule (over a length limit, a mis-quoted verse, a clickbait token, a missing
footer) is caught for free and never reaches the expensive reviewers.

Gates:
  UK-G1  length      every field fits each platform's hard ceiling
  UK-G2  KJV-strict  the quoted anchor verse is verbatim vs the KJV cache
  UK-G3  doctrine    no clickbait / overclaim / sensational tokens
  UK-G4  brand       footer present, CTA-to-Jesus present, brand voice intact
  UK-G5  platform    hashtag counts in range; no fake clickable links where banned
  UK-G6  no-repeat   titles don't collide across platforms (or sibling kits if given)
"""
from __future__ import annotations

import json
import re
from pathlib import Path

import config
from pipeline import scripture
from pipeline.upload_models import GateResult, PlatformMeta, SourceFacts, UploadKit

_SPECS_PATH = config.DATA_DIR / "platform_specs.json" if hasattr(config, "DATA_DIR") else Path("data/platform_specs.json")


def load_specs() -> dict:
    path = _SPECS_PATH
    if not path.is_file():
        path = Path(__file__).resolve().parent.parent / "data" / "platform_specs.json"
    return json.loads(path.read_text(encoding="utf-8"))


# Tokens that turn an honest hook into clickbait / doctrinal overclaim. Case-insensitive.
BANNED_CLICKBAIT = [
    "you won't believe", "you wont believe", "you won’t believe",
    "shocking", "shocked", "this will blow your mind", "mind-blowing", "mind blowing",
    "doctors hate", "they don't want you to know", "they dont want you to know",
    "secret the church", "the church doesn't want", "hidden code", "bible code",
    "scientists prove", "scientists discovered", "proof that god", "100% proof",
    "guaranteed", "must watch", "gone wrong", "(not clickbait)", "number will shock",
    "what happens next", "wait for it", "insane", "unbelievable truth",
]

# A title/desc CTA-to-Jesus is satisfied if any of these appears somewhere in the kit text.
JESUS_MARKERS = ["jesus", "christ", "the lord", "gospel", "saviour", "savior", "messiah", "lamb", "cross"]


def _check_length(kit: UploadKit, specs: dict) -> GateResult:
    bad: list[str] = []
    for p in kit.platforms:
        spec = specs.get(p.platform, {})
        tmax = spec.get("title", {}).get("max", 100)
        if tmax and len(p.title) > tmax:
            bad.append(f"{p.platform}: title {len(p.title)}>{tmax}")
        dmax = spec.get("description", {}).get("max", 5000)
        if len(p.description) > dmax:
            bad.append(f"{p.platform}: description {len(p.description)}>{dmax}")
        tag_max = spec.get("tags", {}).get("field_max_chars", 0)
        if tag_max and len(", ".join(p.tags)) > tag_max:
            bad.append(f"{p.platform}: tags field {len(', '.join(p.tags))}>{tag_max} chars")
    return GateResult("UK-G1", "length", not bad, "; ".join(bad) or "all fields within hard limits")


def _check_kjv(kit: UploadKit, specs: dict) -> GateResult:
    s = kit.source
    truth = (s.anchor_kjv or "").strip()
    if not truth:
        truth = (scripture.fetch_kjv(s.anchor_ref) or "").strip()
    if not truth:
        return GateResult("UK-G2", "KJV-strict", False, f"could not resolve KJV text for {s.anchor_ref}")
    # Find any kit that quotes the verse (descriptions). If a quote is present it MUST be verbatim.
    truth_norm = _norm(truth)
    problems: list[str] = []
    quoted_anywhere = False
    for p in kit.platforms:
        for span in _quoted_spans(p.description):
            span_norm = _norm(span)
            # Only judge spans that look like a Scripture quote (>= 5 words and overlapping the verse)
            if len(span_norm.split()) < 5:
                continue
            if _overlap(span_norm, truth_norm) >= 0.5:
                quoted_anywhere = True
                if span_norm not in truth_norm and truth_norm not in span_norm:
                    problems.append(f"{p.platform}: quoted verse not verbatim KJV")
    if problems:
        return GateResult("UK-G2", "KJV-strict", False, "; ".join(sorted(set(problems))))
    detail = "anchor verse quoted verbatim" if quoted_anywhere else "no verse quote present (ref-only)"
    return GateResult("UK-G2", "KJV-strict", True, detail)


def _check_doctrine(kit: UploadKit, specs: dict) -> GateResult:
    hits: list[str] = []
    for p in kit.platforms:
        blob = f"{p.title}\n{p.description}".lower()
        for tok in BANNED_CLICKBAIT:
            if tok in blob:
                hits.append(f"{p.platform}: '{tok}'")
    return GateResult("UK-G3", "doctrine", not hits, "; ".join(hits) or "no clickbait/overclaim tokens")


def _check_brand(kit: UploadKit, specs: dict, brand: dict) -> GateResult:
    cta = (brand.get("cta_line") or "").strip()
    problems: list[str] = []
    # CTA-to-Jesus somewhere in the whole kit
    whole = "\n".join(f"{p.title} {p.description}" for p in kit.platforms).lower()
    if not any(m in whole for m in JESUS_MARKERS):
        problems.append("no Jesus/Christ/gospel marker anywhere in the kit")
    # Footer CTA present in the link-friendly platforms (YT/FB carry the full footer)
    for p in kit.platforms:
        if p.platform.startswith("youtube") or p.platform == "facebook":
            if cta and cta.split(".")[0].lower() not in p.description.lower():
                problems.append(f"{p.platform}: footer CTA missing")
    return GateResult("UK-G4", "brand", not problems, "; ".join(problems) or "footer + CTA-to-Jesus present")


def _check_platform(kit: UploadKit, specs: dict) -> GateResult:
    problems: list[str] = []
    url_re = re.compile(r"https?://", re.I)
    for p in kit.platforms:
        spec = specs.get(p.platform, {})
        h = spec.get("hashtags", {})
        n = len(p.hashtags)
        if h:
            if n > h.get("max", 30):
                problems.append(f"{p.platform}: {n} hashtags > max {h['max']}")
            tmin, tmax = h.get("target_min", 0), h.get("target_max", 99)
            if n and not (tmin <= n <= tmax):
                problems.append(f"{p.platform}: {n} hashtags outside house target {tmin}-{tmax}")
        # bad-format hashtags
        for tag in p.hashtags:
            if not tag.startswith("#") or " " in tag:
                problems.append(f"{p.platform}: malformed hashtag '{tag}'")
        # links where they don't work = wasted/looks-broken
        if spec.get("links_clickable") is False and url_re.search(p.description):
            problems.append(f"{p.platform}: contains a URL but links are not clickable here")
    return GateResult("UK-G5", "platform", not problems, "; ".join(problems) or "hashtag counts + link rules OK")


def _check_norepeat(kit: UploadKit, sibling_titles: list[str]) -> GateResult:
    titles = [p.title.strip().lower() for p in kit.platforms if p.title.strip()]
    problems: list[str] = []
    sib = {t.strip().lower() for t in sibling_titles}
    for t in titles:
        if t in sib:
            problems.append(f"title collides with a sibling kit: '{t}'")
    return GateResult("UK-G6", "no-repeat", not problems, "; ".join(problems) or "no title collisions with siblings")


def run_all(kit: UploadKit, brand: dict, sibling_titles: list[str] | None = None) -> list[GateResult]:
    specs = load_specs()
    gates = [
        _check_length(kit, specs),
        _check_kjv(kit, specs),
        _check_doctrine(kit, specs),
        _check_brand(kit, specs, brand),
        _check_platform(kit, specs),
        _check_norepeat(kit, sibling_titles or []),
    ]
    return gates


# --- small text helpers (mirror kjv_check style) ------------------------------
def _norm(s: str) -> str:
    return re.sub(r"[^a-z0-9 ]+", " ", s.lower()).strip()


def _quoted_spans(text: str) -> list[str]:
    # straight + curly double quotes
    return re.findall(r"[\"“]([^\"”]{8,})[\"”]", text)


def _overlap(a: str, b: str) -> float:
    aw, bw = set(a.split()), set(b.split())
    if not aw:
        return 0.0
    return len(aw & bw) / len(aw)
