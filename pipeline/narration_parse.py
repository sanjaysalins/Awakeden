"""Shared, fail-closed parser for narration.md (shorts AND long-form).

Both formats mark spoken text with block headers:

    **[narrator]**
    spoken line(s)...

    **[narrator — KJV, Psalm 22:18]**
    "They part my garments among them, and cast lots upon my vesture."

Long-form additionally has `## MOVEMENT N — ...` section headers; shorts have a
`# Title` + status front-matter and a trailing `## DEPTH & SOURCING` / `## VOICE
PLAN` ledger. None of those non-spoken parts carry a `**[speaker]**` header, so a
parser that captures ONLY text following a speaker header naturally excludes them.

This replaces `veed_io/_extract_spoken.py` (which kept text only inside
`## MOVEMENT` sections and therefore returned an EMPTY string on shorts — a
fail-OPEN bug that let every downstream verification pass on nothing).

FAIL-CLOSED CONTRACT: if a narration yields zero spoken blocks, `parse_blocks`
raises `EmptyNarrationError`. Callers MUST abort — never silently pass.
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field

# ---- block header: **[speaker]** or **[speaker — KJV, <ref>]** ---------------
_BLOCK_HEADER = re.compile(r"^\s*\*\*\[([^\]]+)\]\*\*\s*$")
# section heading (## MOVEMENT ..., ## DEPTH ..., etc.) and the --- rule
_HEADING = re.compile(r"^\s*#{1,6}\s")
_RULE = re.compile(r"^\s*-{3,}\s*$")
# inside a header, the ref tag after a dash: "narrator — KJV, Psalm 22:18"
# accept em-dash, en-dash, double-hyphen, or single hyphen as the separator.
_DASH = r"(?:—|–|--|-)"
_REF_IN_HEADER = re.compile(rf"{_DASH}\s*KJV\s*,\s*(.+?)\s*$", re.IGNORECASE)


class EmptyNarrationError(ValueError):
    """Raised when a narration.md yields no spoken blocks (fail-closed)."""


@dataclass
class Block:
    speaker: str
    ref: str | None          # KJV ref tagged on the header, else None
    text: str                # the spoken prose of this block


@dataclass
class Narration:
    blocks: list[Block] = field(default_factory=list)

    @property
    def spoken_text(self) -> str:
        return "\n".join(b.text for b in self.blocks if b.text).strip()

    @property
    def hook(self) -> str:
        """First sentence of the FIRST block (the scroll-stopper). Derived from the
        first block so a following quote can't bleed into it."""
        if not self.blocks:
            return ""
        s = sentences(self.blocks[0].text)
        return s[0] if s else ""

    @property
    def cta(self) -> str:
        """Last sentence of the LAST block (the close). Derived from the last block
        so a preceding KJV quote (which may lack end punctuation) can't merge in."""
        if not self.blocks:
            return ""
        s = sentences(self.blocks[-1].text)
        return s[-1] if s else ""


def _parse_header(inner: str) -> tuple[str, str | None]:
    """'narrator — KJV, Psalm 22:18' -> ('narrator', 'Psalm 22:18').

    Accepts em-dash, en-dash, double-hyphen, or single hyphen as the separator
    (a lost ref would silently bypass KJV verification, so be liberal here)."""
    ref = None
    m = _REF_IN_HEADER.search(inner)
    if m:
        ref = m.group(1).strip()
    speaker = re.split(_DASH, inner, 1)[0].strip().lower()
    return speaker, ref


# the RENDERED tagged file (narration-tagged.md) is XML, not markdown headers:
#   <speaker name="narrator">spoken text… "KJV quote"…</speaker>
_XML_SPEAKER = re.compile(r'<speaker\s+name="([^"]*)"\s*>(.*?)</speaker>',
                          re.IGNORECASE | re.DOTALL)


def _parse_xml_blocks(md: str) -> list[Block]:
    blocks: list[Block] = []
    for m in _XML_SPEAKER.finditer(md):
        text = re.sub(r"\s+", " ", m.group(2)).strip()
        if text:
            blocks.append(Block(speaker=m.group(1).strip().lower(), ref=None, text=text))
    return blocks


def _parse_prose_blocks(md: str) -> list[Block]:
    """Engine-generated narration.md is PLAIN PROSE (paragraphs = beats, no speaker
    markers). Treat each paragraph as a narrator block so the lock can verify/cluster
    it too. Skips headings, rules, front-matter bullets, and a trailing ledger."""
    # truncate at a non-spoken ledger heading so DEPTH/SOURCING/VOICE never leaks in
    cut = re.split(r"(?im)^\s*#{1,6}\s*(?:depth|sourcing|voice\b)", md, 1)[0]
    blocks: list[Block] = []
    for para in re.split(r"\n\s*\n", cut):
        lines = [l for l in para.splitlines()
                 if l.strip() and not _HEADING.match(l) and not _RULE.match(l)
                 and not l.lstrip().startswith(("- ", "* ", "**Status", "**Series"))]
        text = " ".join(l.strip() for l in lines).strip()
        # stop at a DEPTH/VOICE ledger if one appears
        if text and not text.lower().startswith(("depth", "voice plan", "sourcing")):
            blocks.append(Block(speaker="narrator", ref=None, text=text))
    return blocks


def parse_blocks(md: str) -> list[Block]:
    """Parse spoken blocks from a narration.md (markdown `**[speaker]**` blocks),
    a rendered narration-tagged.md (`<speaker name=...>` XML), OR engine plain prose.
    Fail-closed on empty."""
    low = md.lower()
    if "<speaker" in low:
        blocks = _parse_xml_blocks(md)
        # fail-closed: if there are <speaker tokens we couldn't all parse, refuse
        # (never hash/verify partial text from a malformed tag)
        if not blocks or len(blocks) != low.count("<speaker"):
            raise EmptyNarrationError("malformed / unparseable <speaker> tag(s) in tagged file")
        return blocks
    blocks: list[Block] = []
    cur: Block | None = None
    buf: list[str] = []

    def flush() -> None:
        nonlocal cur, buf
        if cur is not None:
            cur.text = " ".join(t.strip() for t in buf if t.strip()).strip()
            if cur.text:
                blocks.append(cur)
        cur, buf = None, []

    for raw in md.splitlines():
        line = raw.rstrip("\n")
        mh = _BLOCK_HEADER.match(line)
        if mh:
            flush()
            speaker, ref = _parse_header(mh.group(1))
            cur = Block(speaker=speaker, ref=ref, text="")
            continue
        # a section heading or horizontal rule ends the current spoken block
        if _HEADING.match(line) or _RULE.match(line):
            flush()
            continue
        if cur is not None:
            buf.append(line)
    flush()

    if not blocks:
        # no speaker markers at all → engine plain-prose narration.md
        blocks = _parse_prose_blocks(md)
    if not blocks:
        raise EmptyNarrationError(
            "no spoken text found (no **[speaker]** / <speaker> markers and no prose) "
            "— refusing to verify an empty extraction (fail-closed)."
        )
    return blocks


def parse(md: str) -> Narration:
    return Narration(blocks=parse_blocks(md))


# ---- quoted spans + KJV ref classification -----------------------------------
_QUOTE = re.compile(r"[\"“”]([^\"“”]+)[\"“”]")

# Spoken-but-not-KJV-claim rhetoric that appears inside narrator blocks: a quoted
# fragment that is an attribution/scripture-frame, not a claim to be verbatim KJV.
_RHETORIC = {
    "that the scripture might be fulfilled",
}


def quoted_spans_with_refs(md: str) -> list[dict]:
    """Each quoted span -> {text, ref, klass}.

    klass:
      'tagged_kjv'  — inside a **[... — KJV, <ref>]** block (MUST verify verbatim)
      'inline_kjv'  — a quoted span in an untagged block (best-effort ref; verify if resolvable)
      'rhetoric'    — an explicit scripture-frame/attribution phrase, NOT a KJV claim

    FAIL-CLOSED at the block level: a KJV-tagged block that yields NO quoted span
    still emits a tagged_kjv span over the whole block text — it is never silently
    skipped (that was the original fail-open bug, one level down).
    """
    out: list[dict] = []
    for b in parse_blocks(md):
        quotes = [q.strip() for q in _QUOTE.findall(b.text) if q.strip()]
        if b.ref:
            if quotes:
                for span in quotes:
                    out.append({"text": span, "ref": b.ref, "klass": "tagged_kjv"})
            else:
                # tagged KJV block with no quote marks — verify the whole block, don't skip
                out.append({"text": b.text.strip(), "ref": b.ref, "klass": "tagged_kjv"})
            continue
        for span in quotes:
            # untagged block: only an EXPLICIT scripture-frame is exempt; short spans
            # are NOT blanket-exempted (e.g. "I thirst." / "It is finished." must verify).
            klass = "rhetoric" if normalize(span) in _RHETORIC else "inline_kjv"
            out.append({"text": span, "ref": None, "klass": klass})
    return out


# ---- normalization + sentence segmentation -----------------------------------
def normalize(s: str) -> str:
    """Lowercase, fold smart quotes/dashes, strip markdown + punctuation, collapse ws.

    For fingerprinting/similarity ONLY — NOT for KJV verbatim comparison (that keeps
    punctuation; see the strict KJV check in Phase B). Punctuation is stripped so
    'Come to Him.' and 'come to him' fingerprint identically; apostrophes inside
    words are kept ('that's')."""
    s = s.replace("’", "'").replace("‘", "'").replace("“", '"').replace("”", '"')
    s = s.replace("—", " ").replace("–", " ").replace("--", " ")
    s = re.sub(r"[*_`]", "", s)                 # strip markdown emphasis
    s = s.lower()
    s = re.sub(r"[^a-z0-9'\s]", " ", s)          # strip punctuation (keep apostrophes)
    s = re.sub(r"'+(?=\s|$)", " ", s)            # drop trailing/dangling apostrophes
    s = re.sub(r"\s+", " ", s)
    return s.strip()


# Common abbreviations whose trailing period must NOT end a sentence.
_ABBREV = (
    "mr", "mrs", "ms", "dr", "st", "vs", "etc", "jr", "sr", "no",
    "gen", "ex", "lev", "num", "deut", "ps", "prov", "isa", "jer", "matt",
    "mk", "lk", "jn", "rom", "cor", "gal", "eph", "phil", "col", "heb", "rev", "v",
)
_ABBREV_RX = re.compile(r"(?:\b" + r"|\b".join(_ABBREV) + r")\.$", re.IGNORECASE)
# end of sentence: terminal . ! ? optionally followed by a closing quote/bracket.
_SENT_SPLIT = re.compile(r'(?<=[.!?])["”’\')\]]*\s+')


def sentences(text: str) -> list[str]:
    text = re.sub(r"\s+", " ", text).strip()
    if not text:
        return []
    raw = _SENT_SPLIT.split(text)
    # re-join fragments that were split right after a known abbreviation
    out: list[str] = []
    for frag in raw:
        frag = frag.strip()
        if not frag:
            continue
        if out and _ABBREV_RX.search(out[-1]):
            out[-1] = out[-1] + " " + frag
        else:
            out.append(frag)
    return out
