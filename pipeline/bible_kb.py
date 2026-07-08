"""bible_kb — the Biblical-Universe knowledge base + accuracy check for stills.

Purpose
-------
Make every still BIBLICALLY DRIVEN and CHECKABLE. For each scene we derive a set
of FACT CARDS — concrete, Scripture-cited claims about the location, time, place,
customs and characters that the painting must honour — then we (1) feed them into
the still prompt and (2) audit the rendered image against them, fail-closed.

Two truths, both enforced (the project's locked non-negotiable):
  * the FACTS are sound       -> the 5-CLI independent panel reviews the fact sheet
  * the PICTURE obeys them     -> a Claude-Vision audit checks image-vs-facts

The trichotomy (the heart of the design — avoids the calibration disaster of a
gate that fails on everything because most of a painting is not in the Bible):

  specified   the Bible STATES it (two goats, Lev 16; white linen, Lev 16:4)
              -> the image MUST match it            -> FAIL-CLOSED (hard block)
  constrained not stated, but must not CONTRADICT (it is a tent, not a stone
              temple)                               -> fail only on contradiction
  free        artistic licence (Aaron's exact face) -> NOT checked

Citation integrity
------------------
The LLM proposes only the CLAIM and the reference. The KJV text is fetched
VERBATIM from pipeline/scripture.py (bible-api.com, cached) — never generated —
so the panel checks claim-vs-real-verse, not claim-vs-vibe. A `specified` fact
whose citation cannot be verified is downgraded and flagged: it can never gate a
pass on a guess.

LLM calls route through pipeline/agent_bridge (LLM_PROVIDER=agent) — the in-chat
agent / Max subscription, NO metered Anthropic API (the project key is dead).
"""
from __future__ import annotations

import hashlib
import json
import os
import re
from dataclasses import asdict, dataclass, field
from pathlib import Path

import config
from pipeline import agent_bridge, scripture

# ---------------------------------------------------------------------------
# Paths — bible_kb/ sits at the repo root, sibling to image_library/ etc.
# ---------------------------------------------------------------------------
REPO_ROOT = Path(__file__).resolve().parent.parent
KB_DIR = REPO_ROOT / "bible_kb"
KB_CATEGORIES = ("characters", "places", "objects", "customs", "eras")

BUCKETS = ("specified", "constrained", "free")


# ---------------------------------------------------------------------------
# Fact model
# ---------------------------------------------------------------------------
@dataclass
class FactCard:
    """One checkable claim about the biblical world of a scene.

    `kjv_text` is filled DETERMINISTICALLY from scripture.py, not by the model.
    `verified` is True only when every cited reference resolved to real KJV text.
    """
    claim: str
    bucket: str                       # specified | constrained | free
    scripture: list[str] = field(default_factory=list)
    kjv_text: str = ""                # fetched verbatim; "" if unfetchable
    historical_note: str = ""         # SECONDARY — never overrides Scripture
    visual_directive: str = ""        # what the painting should show
    banned_anachronisms: list[str] = field(default_factory=list)
    verified: bool = False            # citations resolved to real KJV text
    entity: str = ""                  # KB entity slug this fact attaches to (for promotion/reuse)

    @classmethod
    def from_json(cls, d: dict) -> "FactCard":
        bucket = str(d.get("bucket", "")).strip().lower()
        if bucket not in BUCKETS:
            bucket = "constrained"    # safest default: must-not-contradict
        refs = [str(r).strip() for r in (d.get("scripture") or []) if str(r).strip()]
        bans = [str(b).strip() for b in (d.get("banned_anachronisms") or []) if str(b).strip()]
        return cls(
            claim=str(d.get("claim", "")).strip(),
            bucket=bucket,
            scripture=refs,
            kjv_text=str(d.get("kjv_text", "")).strip(),
            historical_note=str(d.get("historical_note", "")).strip(),
            visual_directive=str(d.get("visual_directive", "")).strip(),
            banned_anachronisms=bans,
            verified=bool(d.get("verified", False)),
            entity=str(d.get("entity", "")).strip(),
        )


@dataclass
class SceneFacts:
    sid: int
    title: str
    subject_block: str
    facts: list[FactCard] = field(default_factory=list)

    def specified(self) -> list[FactCard]:
        return [f for f in self.facts if f.bucket == "specified"]

    def constrained(self) -> list[FactCard]:
        return [f for f in self.facts if f.bucket == "constrained"]


@dataclass
class EpisodeFacts:
    episode: str
    source_narration: str
    source_scene_plan: str
    world_facts: list[FactCard] = field(default_factory=list)
    scenes: list[SceneFacts] = field(default_factory=list)

    def to_json(self) -> dict:
        return {
            "episode": self.episode,
            "source_narration": self.source_narration,
            "source_scene_plan": self.source_scene_plan,
            "world_facts": [asdict(f) for f in self.world_facts],
            "scenes": [
                {"id": s.sid, "title": s.title, "subject_block": s.subject_block,
                 "facts": [asdict(f) for f in s.facts]}
                for s in self.scenes
            ],
        }

    @classmethod
    def from_json(cls, d: dict) -> "EpisodeFacts":
        scenes = [
            SceneFacts(
                sid=int(s.get("id", i + 1)),
                title=str(s.get("title", "")).strip(),
                subject_block=str(s.get("subject_block", "")).strip(),
                facts=[FactCard.from_json(f) for f in (s.get("facts") or [])],
            )
            for i, s in enumerate(d.get("scenes") or [])
        ]
        return cls(
            episode=str(d.get("episode", "")).strip(),
            source_narration=str(d.get("source_narration", "")).strip(),
            source_scene_plan=str(d.get("source_scene_plan", "")).strip(),
            world_facts=[FactCard.from_json(f) for f in (d.get("world_facts") or [])],
            scenes=scenes,
        )


# ---------------------------------------------------------------------------
# Knowledge base load
# ---------------------------------------------------------------------------
def load_kb() -> dict[str, dict]:
    """Load every entity json under bible_kb/<category>/. Returns
    {entity_slug: entity_dict}. The KB grows from VERIFIED derivations
    (see promote_to_kb); on a fresh repo it may be near-empty, which is fine."""
    kb: dict[str, dict] = {}
    for cat in KB_CATEGORIES:
        d = KB_DIR / cat
        if not d.is_dir():
            continue
        for p in sorted(d.glob("*.json")):
            try:
                ent = json.loads(p.read_text(encoding="utf-8"))
            except json.JSONDecodeError:
                continue
            slug = str(ent.get("slug") or p.stem).strip()
            ent["_category"] = cat
            ent["_path"] = str(p)
            kb[slug] = ent
    return kb


def _kb_digest(kb: dict[str, dict]) -> str:
    """A compact text digest of the KB to prime fact derivation (reuse-first)."""
    if not kb:
        return "(the knowledge base is currently empty — derive facts from the narration + Scripture)"
    lines = []
    for slug, ent in sorted(kb.items()):
        facts = ent.get("facts") or []
        lines.append(f"### {slug} [{ent.get('_category','')}] — {ent.get('name', slug)}")
        for f in facts[:8]:
            refs = ", ".join(f.get("scripture") or [])
            lines.append(f"  - ({f.get('bucket','')}) {f.get('claim','')}  [{refs}]")
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Scene-plan loading — tolerant of the short (index/slug) and long-form
# (id/title/subject_block) scene_plan.json shapes AND the living-page batch
# spec (livingpage_short.spec.json: beats -> still slugs; the visual content
# description comes from the sibling piece.json still prompts).
# ---------------------------------------------------------------------------
def _scenes_from_livingpage_spec(spec_path: Path, d: dict) -> list[dict]:
    """One scene per unique STILL slug used by the beats (the still, not the beat,
    is the unit the biblical audit checks). subject_block = the piece.json render
    prompt for that slug (what the image was actually generated from); caption
    texts of the beats that use it are appended as context."""
    piece_json = spec_path.parents[1] / "piece.json"
    jobs, reg = {}, {}
    if piece_json.is_file():
        pj = json.loads(piece_json.read_text(encoding="utf-8"))
        jobs = (pj.get("stills") or {}).get("jobs") or {}
        reg = (pj.get("register") or {}).get("stills") or {}
    order: list[str] = []
    caps: dict[str, list[str]] = {}
    for beat in d.get("beats") or []:
        sources = list(beat.get("clips") or []) + list(beat.get("panels") or [])
        cap = ((beat.get("cap") or {}).get("text") or "").strip()
        for src in sources:
            slug = (src.get("slug") or "").strip() if isinstance(src, dict) else str(src)
            if not slug:
                continue
            if slug not in order:
                order.append(slug)
            if cap:
                caps.setdefault(slug, []).append(cap)
    out = []
    for i, slug in enumerate(order):
        prompt = (jobs.get(slug) or {}).get("prompt", "")
        subject = prompt or (reg.get(slug) or {}).get("subject", "")
        ctx = "; ".join(dict.fromkeys(caps.get(slug, [])))
        out.append({
            "id": i + 1,
            "title": slug,
            "subject_block": (subject + (f" (narration beat: {ctx})" if ctx else "")).strip(),
            "scene_type": "livingpage_still",
            "refs": [],
        })
    return out


def load_scene_list(scene_plan_path: Path) -> list[dict]:
    d = json.loads(Path(scene_plan_path).read_text(encoding="utf-8"))
    if "beats" in d and not d.get("scenes"):
        return _scenes_from_livingpage_spec(Path(scene_plan_path), d)
    raw = d.get("scenes") or []
    out: list[dict] = []
    for i, s in enumerate(raw):
        sid = s.get("id", s.get("index", i + 1))
        try:
            sid = int(sid)
        except (TypeError, ValueError):
            sid = i + 1
        out.append({
            "id": sid,
            "title": str(s.get("title", "")).strip(),
            "subject_block": str(s.get("subject_block", "")).strip(),
            "scene_type": str(s.get("scene_type", "")).strip(),
            "refs": list(s.get("refs") or []),
        })
    return out


# ---------------------------------------------------------------------------
# Citation hydration — fill kjv_text VERBATIM, set verified, downgrade guesses
# ---------------------------------------------------------------------------
def hydrate_citations(facts: list[FactCard], *, offline_ok: bool = False) -> list[FactCard]:
    """Fetch verbatim KJV for every reference (cached). A fact is `verified`
    only when ALL its refs resolve. An UNVERIFIED `specified` fact is downgraded
    to `constrained` and tagged so it can never gate a pass on a guess."""
    for f in facts:
        if not f.scripture:
            f.verified = False
            f.kjv_text = ""
            if f.bucket == "specified":
                f.bucket = "constrained"
                f.claim = f.claim + "  [DOWNGRADED: no citation]"
            continue
        chunks: list[str] = []
        all_ok = True
        for ref in f.scripture:
            txt = scripture.fetch_kjv(ref)
            if not txt:
                all_ok = False
                continue
            chunks.append(f"[{ref}] {txt}")
        f.kjv_text = "\n".join(chunks)
        f.verified = all_ok and bool(chunks)
        if not f.verified and f.bucket == "specified" and not offline_ok:
            f.bucket = "constrained"
            f.claim = f.claim + "  [DOWNGRADED: citation unverified]"
    return facts


# ---------------------------------------------------------------------------
# Fact derivation (LLM via agent-bridge) — proposes claims + refs + buckets
# ---------------------------------------------------------------------------
_DERIVE_ROLE = (
    "You are a biblical-accuracy researcher building a FACT SHEET that will drive "
    "and police a set of devotional paintings. For each scene you list the "
    "concrete, checkable facts about the LOCATION, TIME/ERA, PLACE, CUSTOMS and "
    "CHARACTERS that the painting must honour, each pinned to Scripture.\n\n"
    "RULES (non-negotiable):\n"
    "1. SCRIPTURE IS BINDING. Every fact must cite a real verse reference "
    "(book chap:verse). Do NOT quote the verse text — only the reference; the "
    "engine fetches the verbatim KJV itself. Never invent a citation.\n"
    "2. BUCKET every fact honestly:\n"
    "   - 'specified'   = the Bible explicitly STATES this visual fact (e.g. the "
    "high priest wore plain linen on the Day of Atonement, Lev 16:4; there were "
    "TWO goats, Lev 16:7). The painting MUST match it.\n"
    "   - 'constrained' = not stated, but a depiction could CONTRADICT the text "
    "(e.g. it was a portable TENT, not a stone temple — Ex 26). Flag the "
    "contradiction to avoid.\n"
    "   - 'free'        = artistic licence, the Bible is silent (a character's "
    "exact face). Only list these if they guard against a common anachronism.\n"
    "3. HISTORICAL notes are SECONDARY and must be marked as such; they may never "
    "override or contradict Scripture. Leave empty unless genuinely useful.\n"
    "4. Prefer facts that map to something VISIBLE in the painting. Give a "
    "concrete `visual_directive` (what to show) and `banned_anachronisms` (what "
    "must not appear) for each.\n"
    "5. Reuse the KNOWN ENTITIES below where they apply (cite the same way).\n\n"
    "Return ONLY a JSON object (optionally in a ```json fence):\n"
    "{\n"
    '  "world_facts": [ <fact>, ... ],        // episode-global: era, place, customs\n'
    '  "scenes": [ {"id": <int>, "facts": [ <fact>, ... ]}, ... ]\n'
    "}\n"
    "where <fact> = {\n"
    '  "claim": "<one concrete checkable sentence>",\n'
    '  "bucket": "specified|constrained|free",\n'
    '  "scripture": ["Book c:v", ...],\n'
    '  "historical_note": "<secondary, optional>",\n'
    '  "visual_directive": "<what the painting should show>",\n'
    '  "banned_anachronisms": ["<what must not appear>", ...],\n'
    '  "entity": "<kb entity slug if it maps to one, else \\"\\">"\n'
    "}\n"
    "Be rigorous and specific. A wrong or invented citation is worse than no fact."
)


def derive_scene_facts(
    narration_text: str,
    scenes: list[dict],
    kb: dict[str, dict] | None = None,
    *,
    label: str = "bible-kb derive",
) -> dict:
    """Ask the LLM (via agent-bridge) to propose the fact sheet. Returns the raw
    parsed dict {world_facts, scenes:[{id, facts}]}. Citations are hydrated by
    the caller (build_episode_facts)."""
    kb = kb or {}
    scene_brief = "\n".join(
        f"SCENE {s['id']} — {s['title']}\n  subject: {s['subject_block']}"
        for s in scenes
    )
    user = (
        "## KNOWN ENTITIES (reuse where they apply)\n"
        f"{_kb_digest(kb)}\n\n"
        "## NARRATION (the witness's account — the source of truth for what each scene depicts)\n"
        f"{narration_text}\n\n"
        "## SCENES TO ANNOTATE\n"
        f"{scene_brief}\n\n"
        "Produce the fact sheet JSON now."
    )
    from pipeline import engine as text_engine  # local import: avoid a hard dep at module load
    raw = agent_bridge.call_text(role=_DERIVE_ROLE, user=user, model=config.MODEL, label=label)
    return text_engine._extract_json(raw)


def build_episode_facts(
    episode: str,
    narration_path: Path,
    scene_plan_path: Path,
    *,
    scene_ids: list[int] | None = None,
) -> EpisodeFacts:
    """Full derivation: load narration + scenes + KB, derive facts, hydrate
    citations deterministically. `scene_ids` limits to a subset (POC)."""
    narration_text = Path(narration_path).read_text(encoding="utf-8").strip()
    scenes = load_scene_list(scene_plan_path)
    if scene_ids:
        wanted = set(scene_ids)
        scenes = [s for s in scenes if s["id"] in wanted]
    kb = load_kb()

    parsed = derive_scene_facts(narration_text, scenes, kb)

    world_facts = hydrate_citations(
        [FactCard.from_json(f) for f in (parsed.get("world_facts") or [])]
    )
    by_id = {int(x.get("id")): x for x in (parsed.get("scenes") or []) if x.get("id") is not None}
    scene_facts: list[SceneFacts] = []
    for s in scenes:
        raw_facts = (by_id.get(s["id"]) or {}).get("facts") or []
        facts = hydrate_citations([FactCard.from_json(f) for f in raw_facts])
        scene_facts.append(SceneFacts(
            sid=s["id"], title=s["title"], subject_block=s["subject_block"], facts=facts,
        ))

    return EpisodeFacts(
        episode=episode,
        source_narration=str(narration_path),
        source_scene_plan=str(scene_plan_path),
        world_facts=world_facts,
        scenes=scene_facts,
    )


# ---------------------------------------------------------------------------
# Vision accuracy audit — image vs the SPECIFIED + CONSTRAINED facts
# ---------------------------------------------------------------------------
_AUDIT_ROLE = (
    "You are an INDEPENDENT biblical-accuracy auditor. A painting was made for a "
    "scene; below is a fact sheet of Scripture-cited facts it must honour. Judge "
    "ONLY against these facts — not your general taste.\n\n"
    "Each fact is bucketed:\n"
    "  - SPECIFIED  = the Bible states it. The image MUST show it. A clear "
    "contradiction or omission of a specified visual = HARD FAIL.\n"
    "  - CONSTRAINED = the image must not CONTRADICT it (e.g. a stone temple when "
    "the text says a tent). Fail ONLY on an actual contradiction.\n"
    "Anything NOT in the fact sheet is artistic licence — do NOT fail on it. The "
    "Bible is silent about most of any painting; do not invent requirements.\n\n"
    "Return ONLY a JSON object (optionally fenced):\n"
    "{\n"
    '  "passed": true | false,                 // false if ANY specified fact is violated\n'
    '  "specified_violations": [{"claim": "<fact>", "actual": "<what you see>"}, ...],\n'
    '  "constrained_violations": [{"claim": "<fact>", "actual": "<contradiction seen>"}, ...],\n'
    '  "notes": "<brief overall read>"\n'
    "}\n"
    "passed=false ONLY when a SPECIFIED fact is clearly violated, or a CONSTRAINED "
    "fact is clearly contradicted. When the image is silent/ambiguous on a fact "
    "(neither shows nor contradicts it), that is NOT a violation."
)


@dataclass
class BiblicalAudit:
    passed: bool
    specified_violations: list[dict] = field(default_factory=list)
    constrained_violations: list[dict] = field(default_factory=list)
    notes: str = ""
    skipped: bool = False

    @classmethod
    def from_json(cls, d: dict) -> "BiblicalAudit":
        def vlist(key):
            return [
                {"claim": str(i.get("claim", "")).strip(), "actual": str(i.get("actual", "")).strip()}
                for i in (d.get(key) or []) if i
            ]
        return cls(
            passed=bool(d.get("passed", False)),
            specified_violations=vlist("specified_violations"),
            constrained_violations=vlist("constrained_violations"),
            notes=str(d.get("notes", "")).strip(),
        )


def _fact_lines(facts: list[FactCard]) -> str:
    out = []
    for f in facts:
        if f.bucket == "free":
            continue
        refs = ", ".join(f.scripture)
        tag = "SPECIFIED" if f.bucket == "specified" else "CONSTRAINED"
        out.append(f"- [{tag}] {f.claim}  (Scripture: {refs})")
        if f.kjv_text:
            out.append(f"    KJV: {f.kjv_text}")
        if f.banned_anachronisms:
            out.append(f"    MUST NOT show: {'; '.join(f.banned_anachronisms)}")
    return "\n".join(out) or "(no specified/constrained facts for this scene)"


def verify_biblical_accuracy(
    scene_title: str,
    subject_block: str,
    facts: list[FactCard],
    world_facts: list[FactCard],
    png_bytes: bytes,
) -> BiblicalAudit:
    """Claude-Vision audit of a rendered still against its cited facts. Routes
    through agent-bridge (no metered API). Fail-closed: on an audit ERROR the
    image is flagged needs-review (passed False, skipped True) rather than
    silently passing — a wrong still must never slip through."""
    all_checkable = [f for f in (world_facts + facts) if f.bucket in ("specified", "constrained")]
    user = (
        f"SCENE: {scene_title}\n"
        f"WHAT THE PAINTING DEPICTS (subject): {subject_block}\n\n"
        "FACT SHEET (judge the image ONLY against these):\n"
        f"{_fact_lines(all_checkable)}\n\n"
        "Audit the attached image against the SPECIFIED and CONSTRAINED facts above."
    )
    media = "image/png"
    try:
        from pipeline import engine as text_engine
        raw = agent_bridge.call_vision(
            role=_AUDIT_ROLE, user=user, image_bytes=png_bytes, media=media,
            model=config.MODEL, label=f"bible-audit:{scene_title[:40]}",
        )
        return BiblicalAudit.from_json(text_engine._extract_json(raw))
    except Exception as e:
        return BiblicalAudit(
            passed=False, skipped=True,
            notes=f"AUDIT ERROR — review by eye: {str(e)[:160]}",
        )


# ---------------------------------------------------------------------------
# Prompt enrichment — fold the visual directives + bans into the still prompt
# ---------------------------------------------------------------------------
def enrich_subject_block(subject_block: str, facts: list[FactCard], world_facts: list[FactCard]) -> str:
    """Append the SPECIFIED/CONSTRAINED visual directives so the render is
    biblically driven. Returns the enriched subject_block."""
    directives = []
    for f in (world_facts + facts):
        if f.bucket == "free":
            continue
        if f.visual_directive:
            directives.append(f.visual_directive)
    if not directives:
        return subject_block
    # de-dup while preserving order
    seen, uniq = set(), []
    for d in directives:
        k = d.lower().strip()
        if k not in seen:
            seen.add(k)
            uniq.append(d.strip().rstrip(".,"))
    return subject_block.rstrip() + " Biblically faithful detail: " + "; ".join(uniq) + "."


def collect_banned(facts: list[FactCard], world_facts: list[FactCard]) -> list[str]:
    seen, out = set(), []
    for f in (world_facts + facts):
        for b in f.banned_anachronisms:
            k = b.lower().strip()
            if k and k not in seen:
                seen.add(k)
                out.append(b.strip())
    return out


def enrich_for_scene(v1: Path, scene_id: int, subject_block: str,
                     *, max_directives: int = 8) -> tuple[str, list[str]]:
    """Fold this scene's cited biblical visual directives into its subject_block so
    the render is BIBLICALLY DRIVEN (not just checked). Returns (enriched_subject,
    banned_list). No-op (returns the input unchanged) if no fact sheet exists for
    the episode or the scene has no facts — so it is safe + going-forward.

    Folds the SCENE's own checkable directives + the SPECIFIED world directives
    (the must-match ones), capped + de-duped to keep the prompt clean — dense
    subject_blocks make image models morph (feedback-animation-clean-stills)."""
    facts_path = Path(v1) / "_bible_check" / "scene_facts.json"
    if not facts_path.exists():
        return subject_block, []
    try:
        ep = EpisodeFacts.from_json(json.loads(facts_path.read_text(encoding="utf-8")))
    except json.JSONDecodeError:
        return subject_block, []
    scene = next((s for s in ep.scenes if s.sid == scene_id), None)
    if scene is None:
        return subject_block, []
    world_spec = [w for w in ep.world_facts if w.bucket == "specified"]
    directives: list[str] = []
    seen = set()
    for f in scene.facts + world_spec:           # scene-specific first, then world musts
        if f.bucket == "free" or not f.visual_directive:
            continue
        d = f.visual_directive.strip().rstrip(".,")
        k = d.lower()
        if k not in seen:
            seen.add(k)
            directives.append(d)
        if len(directives) >= max_directives:
            break
    banned = collect_banned(scene.facts, ep.world_facts)
    if not directives:
        return subject_block, banned
    enriched = subject_block.rstrip() + " Biblically faithful detail: " + "; ".join(directives) + "."
    return enriched, banned


# ---------------------------------------------------------------------------
# KB promotion — grow the reusable KB from VERIFIED derivations only
# ---------------------------------------------------------------------------
_SLUG_RE = re.compile(r"[^a-z0-9]+")


def _slugify(s: str) -> str:
    return _SLUG_RE.sub("-", s.lower()).strip("-") or "entity"


def promote_to_kb(ep: EpisodeFacts, *, category_default: str = "customs") -> list[str]:
    """Write VERIFIED facts that carry an `entity` tag into bible_kb/<cat>/.
    Only verified facts are promoted — the KB grows from proven output, not
    guesses. Returns the list of entity files written/updated."""
    by_entity: dict[str, list[FactCard]] = {}
    for f in ep.world_facts + [fc for s in ep.scenes for fc in s.facts]:
        if not f.verified or not f.entity:
            continue
        by_entity.setdefault(f.entity, []).append(f)

    written: list[str] = []
    for entity, facts in by_entity.items():
        slug = _slugify(entity)
        # find existing file across categories, else default category
        existing = None
        for cat in KB_CATEGORIES:
            p = KB_DIR / cat / f"{slug}.json"
            if p.exists():
                existing = p
                break
        path = existing or (KB_DIR / category_default / f"{slug}.json")
        path.parent.mkdir(parents=True, exist_ok=True)
        ent = {}
        if path.exists():
            try:
                ent = json.loads(path.read_text(encoding="utf-8"))
            except json.JSONDecodeError:
                ent = {}
        ent.setdefault("slug", slug)
        ent.setdefault("name", entity)
        merged = {self_key(f): f for f in [FactCard.from_json(x) for x in ent.get("facts", [])]}
        for f in facts:
            merged[self_key(f)] = f
        ent["facts"] = [asdict(f) for f in merged.values()]
        path.write_text(json.dumps(ent, indent=2, ensure_ascii=False), encoding="utf-8")
        written.append(str(path))
    return written


def self_key(f: FactCard) -> str:
    """Dedup key for a fact within an entity (claim + sorted refs)."""
    return (f.claim.split("  [")[0].strip().lower() + "|" + ",".join(sorted(f.scripture))).strip()


# ===========================================================================
# LAYER 1 — deterministic over-reach scan ($0, no LLM)
# ===========================================================================
# A `specified` fact asserts "the Bible STATES this". The single most common way
# that goes wrong (proven on EW01: "white linen", "gold-set ephod") is a claim
# that names a COLOUR, NUMBER or MATERIAL the cited verse never uses. We catch
# that deterministically: if a high-risk descriptor in a specified claim is not
# present in its fetched KJV text, flag it. No LLM, no network — pure teeth.

_COLOURS = {
    "white", "black", "red", "blue", "purple", "scarlet", "crimson", "green",
    "gold", "silver", "bronze", "brass", "grey", "gray", "brown", "yellow",
    "azure", "vermilion",
}
_MATERIALS = {
    "gold", "silver", "bronze", "brass", "iron", "linen", "wool", "wood",
    "stone", "marble", "leather", "ivory", "cedar", "acacia", "shittim",
}
_NUMBERS = {
    "one": "1", "two": "2", "three": "3", "four": "4", "five": "5", "six": "6",
    "seven": "7", "eight": "8", "nine": "9", "ten": "10", "eleven": "11",
    "twelve": "12",
}
# normalize a claim descriptor to the root form the KJV is likely to use
_SYNONYM = {
    "golden": "gold", "brazen": "brass", "wooden": "wood", "woollen": "wool",
    "woolen": "wool", "silvern": "silver", "stony": "stone", "leathern": "leather",
}
_HIGH_RISK = _COLOURS | _MATERIALS | set(_NUMBERS)
_WORD_RE = re.compile(r"[a-z0-9]+")


def _kjv_word_set(kjv_text: str) -> set[str]:
    return set(_WORD_RE.findall(kjv_text.lower()))


def _norm_descriptor(tok: str) -> str:
    tok = tok.lower()
    tok = _SYNONYM.get(tok, tok)
    if tok.endswith("s") and tok[:-1] in _HIGH_RISK:   # depluralize stones->stone
        tok = tok[:-1]
    return tok


def over_reach_scan(facts: list[FactCard]) -> list[dict]:
    """Return a flag per SPECIFIED fact whose claim names a colour/number/material
    that does NOT appear in its cited KJV text. Each flag = a binding defect:
    cite a verse that contains the word, or re-bucket the fact to constrained/free.

    Facts with no kjv_text are skipped here (that is the hydration gate's job)."""
    flags: list[dict] = []
    negations = {"not", "no", "never", "without", "nor", "neither"}
    for f in facts:
        if f.bucket != "specified" or not f.kjv_text:
            continue
        kjv_words = _kjv_word_set(f.kjv_text)
        words = _WORD_RE.findall(f.claim.lower())
        for i, raw in enumerate(words):
            if raw not in _HIGH_RISK and _norm_descriptor(raw) not in _HIGH_RISK:
                continue
            # skip a NEGATED descriptor ("not plain white", "no gold") — it is a
            # guard against the colour/material, not a claim that it is present.
            if negations & set(words[max(0, i - 3):i]):
                continue
            tok = _norm_descriptor(raw)
            forms = {tok, raw}
            if tok in _NUMBERS:
                forms.add(_NUMBERS[tok])
            # also accept the gold<->golden direction
            forms |= {k for k, v in _SYNONYM.items() if v == tok}
            if forms & kjv_words:
                continue
            cat = ("colour" if tok in _COLOURS else
                   "material" if tok in _MATERIALS else "number")
            flags.append({
                "claim": f.claim,
                "scripture": list(f.scripture),
                "descriptor": raw,
                "category": cat,
                "why": f"'{raw}' ({cat}) is in a SPECIFIED claim but does not appear "
                       f"in the cited KJV; cite a verse that contains it or re-bucket "
                       f"to constrained/free.",
            })
    return flags


# ===========================================================================
# LAYER 3 — fail-closed chokepoint ("did the check run AND pass here?")
# ===========================================================================
@dataclass
class CheckStatus:
    ok: bool
    reasons: list[str] = field(default_factory=list)
    covered: list[int] = field(default_factory=list)
    missing_facts: list[int] = field(default_factory=list)
    missing_audit: list[int] = field(default_factory=list)
    failed_audit: list[int] = field(default_factory=list)
    over_reach: list[dict] = field(default_factory=list)
    unverified_specified: int = 0
    stale: bool = False
    stale_audit: list[int] = field(default_factory=list)


def _locate(v1: Path) -> dict:
    v1 = Path(v1)
    facts = v1 / "_bible_check" / "scene_facts.json"
    scene_plan = None
    for c in (v1 / "visual_16x9" / "scene_plan.json",
              v1 / "visual" / "scene_plan.json", v1 / "scene_plan.json"):
        if c.exists():
            scene_plan = c
            break
    images_dir = scene_plan.parent if scene_plan else v1
    return {"facts": facts, "scene_plan": scene_plan, "images_dir": images_dir}


def _rendered_scene_ids(images_dir: Path) -> list[int]:
    ids: list[int] = []
    for p in sorted(Path(images_dir).glob("[0-9][0-9]_*.png")):
        try:
            ids.append(int(p.stem[:2]))
        except ValueError:
            pass
    return ids


def sha_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def sha_file(p: Path) -> str:
    return sha_bytes(Path(p).read_bytes())


def scene_facts_sha(scene: SceneFacts) -> str:
    """Content hash of a scene's checkable facts — so a sidecar can be BOUND to the
    exact fact set it was audited against (an edit to the facts invalidates it)."""
    canon = [
        {"claim": f.claim, "bucket": f.bucket, "scripture": sorted(f.scripture)}
        for f in scene.facts if f.bucket in ("specified", "constrained")
    ]
    return sha_bytes(json.dumps(canon, sort_keys=True, ensure_ascii=False).encode("utf-8"))


def check_status(v1: Path, *, rendered_only: bool = True) -> CheckStatus:
    """Fail-closed status for the bible-check on one episode. Also writes
    <v1>/_bible_check/bible_check.status.json as the machine-checkable record.

    GREEN requires ALL of:
      - scene_facts.json exists and is CURRENT (scene_plan not newer than it),
      - every rendered still has a SceneFacts entry (coverage),
      - every rendered still has a .bib_audit.json with passed=true (not skipped),
      - no SPECIFIED fact is unverified (citation didn't resolve),
      - the deterministic over_reach_scan is clean.
    (The 5-CLI panel result is recorded as evidence in the manifest but is not a
    hard gate here — its verdict oscillates; the binding bar is the deterministic
    set above plus the recorded operator decision. See bible-kb-panel-calibration.)"""
    v1 = Path(v1)
    loc = _locate(v1)
    st = CheckStatus(ok=False)

    if not loc["facts"].exists():
        st.reasons.append("no _bible_check/scene_facts.json — run bib_validate first")
        _write_status(v1, st)
        return st

    raw = json.loads(loc["facts"].read_text(encoding="utf-8"))
    ep = EpisodeFacts.from_json(raw)
    all_facts = list(ep.world_facts) + [f for s in ep.scenes for f in s.facts]

    # staleness via CONTENT HASH, not mtime (git/copy rewrite mtimes; mtime is
    # forgeable). scene_facts.json must carry the sha256 of the scene_plan it was
    # built from; if the live scene_plan differs, the facts are stale.
    if loc["scene_plan"] and loc["scene_plan"].exists():
        stored = raw.get("scene_plan_sha256")
        if not stored:
            st.stale = True
            st.reasons.append("scene_facts.json is not bound to a scene_plan hash "
                              "(re-run bib_validate to bind it)")
        elif sha_file(loc["scene_plan"]) != stored:
            st.stale = True
            st.reasons.append("scene_plan.json changed since the facts were built "
                              "(hash mismatch) — re-derive/re-hydrate before locking")

    fact_ids = {s.sid for s in ep.scenes}
    scene_by_id = {s.sid: s for s in ep.scenes}
    st.covered = sorted(fact_ids)
    # rendered_only (default): check every rendered PNG. all-scenes: ALSO require every
    # PLANNED scene to be covered + audited (the strict superset, not a weaker subset).
    rendered = set(_rendered_scene_ids(loc["images_dir"]))
    if not rendered_only and loc["scene_plan"] and loc["scene_plan"].exists():
        try:
            plan = json.loads(loc["scene_plan"].read_text(encoding="utf-8"))
            for s in plan.get("scenes", []):
                sid = s.get("id", s.get("index"))
                if sid is not None:
                    rendered.add(int(sid))
        except (json.JSONDecodeError, ValueError, TypeError):
            pass
    rendered = sorted(rendered)

    for sid in rendered:
        if sid not in fact_ids:
            st.missing_facts.append(sid)
            continue
        png = next(iter(sorted(Path(loc["images_dir"]).glob(f"{sid:02d}_*.png"))), None)
        if png is None:
            continue
        sidecar = png.with_suffix(".bib_audit.json")
        if not sidecar.exists():
            st.missing_audit.append(sid)
            continue
        try:
            a = json.loads(sidecar.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            st.failed_audit.append(sid)
            continue
        if a.get("skipped") or not a.get("passed", False):
            st.failed_audit.append(sid)
            continue
        # the audit must be BOUND to the exact PNG bytes + the exact facts it ran
        # against — else a stale "passed" (audited before the facts changed) or a
        # hand-written sidecar would pass the gate.
        if (a.get("image_sha256") != sha_file(png)
                or a.get("facts_sha256") != scene_facts_sha(scene_by_id[sid])):
            st.stale_audit.append(sid)

    st.unverified_specified = sum(
        1 for f in all_facts if f.bucket == "specified" and f.scripture and not f.verified)
    st.over_reach = over_reach_scan(all_facts)

    if st.missing_facts:
        st.reasons.append(f"rendered scenes with NO derived facts: {st.missing_facts}")
    if st.missing_audit:
        st.reasons.append(f"rendered scenes with NO bible image-audit sidecar: {st.missing_audit}")
    if st.failed_audit:
        st.reasons.append(f"rendered scenes that FAILED or SKIPPED the image audit: {st.failed_audit}")
    if st.stale_audit:
        st.reasons.append(f"rendered scenes whose audit is STALE (PNG or facts changed "
                          f"since the audit ran; re-audit): {st.stale_audit}")
    if st.unverified_specified:
        st.reasons.append(f"{st.unverified_specified} SPECIFIED fact(s) with an unverified citation")
    if st.over_reach:
        st.reasons.append(f"{len(st.over_reach)} deterministic over-reach flag(s) "
                          f"(specified claim names a word not in its KJV)")

    st.ok = not st.reasons
    _write_status(v1, st)
    return st


def _write_status(v1: Path, st: CheckStatus) -> None:
    out = Path(v1) / "_bible_check"
    out.mkdir(parents=True, exist_ok=True)
    (out / "bible_check.status.json").write_text(
        json.dumps(asdict(st), indent=2, ensure_ascii=False), encoding="utf-8")


def assert_green(v1: Path, *, stage: str = "lock", rendered_only: bool = True) -> CheckStatus:
    """Fail-closed guard for callers (lock / animate). Raises RuntimeError listing
    the reasons if the bible-check is not green. Returns the status on success."""
    st = check_status(v1, rendered_only=rendered_only)
    if not st.ok:
        raise RuntimeError(
            f"BIBLE-CHECK GATE [{stage}] refused {Path(v1)}:\n  - "
            + "\n  - ".join(st.reasons)
            + "\nRun: .venv\\Scripts\\python.exe bib_validate.py \"<v1>\"  (fix + re-run)")
    return st


def gate(v1: Path, *, stage: str = "lock", rendered_only: bool = True) -> CheckStatus | None:
    """Policy wrapper drivers/skills call before spending. GOING-FORWARD ONLY:

      - env BIBLE_GATE=off            -> skip (global escape hatch)
      - <v1>/.bible_gate_exempt file  -> skip (explicitly grandfathered piece)
      - no <v1>/_bible_check/ dir AND mode != strict -> skip with notice
        (the piece predates the bible-check stage — grandfathered)
      - otherwise -> assert_green (raises RuntimeError if not green)
      - env BIBLE_GATE=warn           -> never raise, just warn
      - env BIBLE_GATE=strict         -> enforce even on pieces with no _bible_check

    Returns the CheckStatus when it ran, or None when skipped."""
    v1 = Path(v1)
    mode = os.getenv("BIBLE_GATE", "enforce").strip().lower()
    if mode in ("off", "0", "false", "skip"):
        print(f"[bible-gate] OFF — skipped {v1.name} ({stage}).")
        return None
    if (v1 / ".bible_gate_exempt").exists():
        print(f"[bible-gate] exempt marker — skipped {v1.name} ({stage}).")
        return None
    if not (v1 / "_bible_check").exists() and mode != "strict":
        print(f"[bible-gate] grandfathered (no _bible_check) — skipped {v1.name} ({stage}). "
              f"Set BIBLE_GATE=strict to enforce.")
        return None
    if mode == "warn":
        st = check_status(v1, rendered_only=rendered_only)
        if not st.ok:
            print(f"[bible-gate] WARN [{stage}] {v1.name} NOT green:\n  - " + "\n  - ".join(st.reasons))
        return st
    return assert_green(v1, stage=stage, rendered_only=rendered_only)
