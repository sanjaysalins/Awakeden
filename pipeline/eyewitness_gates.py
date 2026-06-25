"""Deterministic, fail-closed gates for the Awakeden eyewitness format (EW-G1..EW-G6).

The binding contract is `v2/EYEWITNESS_SPEC.md` — §2.1 (the narration.md format these gates
parse), §3 (EW-INV-1..10), §4 (the gate registry), §9 (the lock). These are PURE-CODE checks
($0, no LLM); the 5-CLI panel (EW-G7..G10) is the separate outside review.

  EW-G1 KJV-strict   — every **"..."** quote is verbatim vs the cached KJV corpus (reuses kjv_check).
  EW-G2 Spine        — `## Beat N — name` headers present & ordered (LONG = 7, SHORT >= hook/act/reveal/invitation).
  EW-G3 Word budget  — spoken words within the form's range (SHORT 220-320, LONG 1300-1650).
  EW-G4 CTA-on-Jesus — the LAST beat names Jesus/Christ + an invitation verb + no banned bare-CTA template.
  EW-G5 First-person — first-person witness markers (I/my/me/mine...) above the form's floor.
  EW-G6 Cast present — >=2 voice roles implied (witness + scripture when KJV quotes exist + named speakers).

Each EW-Gn returns a GateResult; `run_gates(...)` returns the ordered list. A gate with
ok=False and blocking=True must block the LOCK (cli_witness_lock.py).
"""
from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from pathlib import Path

from pipeline import kjv_check

_REPO = Path(__file__).resolve().parent.parent
_RULES_PATH = _REPO / "data" / "eyewitness_rules.json"
_KJV_CACHE = _REPO / "data" / "kjv_cache.json"


# ---------------------------------------------------------------- rules
def load_rules() -> dict:
    return json.loads(_RULES_PATH.read_text(encoding="utf-8"))


# ---------------------------------------------------------------- result type
@dataclass
class GateResult:
    gate: str            # "EW-G1"
    name: str            # short human name
    ok: bool             # passed?
    blocking: bool       # a failing blocking gate must block the LOCK
    detail: str          # one-line summary
    findings: list[str] = field(default_factory=list)

    def __str__(self) -> str:
        tag = "PASS" if self.ok else ("FAIL" if self.blocking else "WARN")
        return f"[{tag}] {self.gate} {self.name}: {self.detail}"


# ---------------------------------------------------------------- parsing (§2.1)
_BEAT_RE = re.compile(r"^##\s+Beat\s+(\d+)\s*[—–-]\s*(.*)$")
_KJV_QUOTE_RE = re.compile(r'\*\*"([^"]+)"\*\*')          # a bold double-quote = a KJV quote
_SPEAKER_TAG_RE = re.compile(r"^\s*\*\*\[([^\]]+)\]\*\*")  # **[Speaker]** at line start


@dataclass
class Beat:
    n: int
    name: str
    spoken: str          # spoken words of this beat (tags/notes stripped)


@dataclass
class ParsedWitness:
    title: str
    form_hint: str | None
    header: str
    body: str
    beats: list[Beat]
    spoken_text: str
    kjv_quotes: list[str]
    speaker_tags: list[str]
    has_witness_prose: bool
    dialogue_lines: list[tuple[str, str]]   # (speaker_lower, raw_line) for each **[Speaker]** line


def _clean_spoken_line(raw: str) -> str:
    """Strip a single body line down to its spoken words: remove the **[Speaker]** tag,
    drop bracketed delivery notes, strip markdown emphasis. Returns '' for header/rule lines."""
    s = raw.strip()
    if not s or s == "---" or _BEAT_RE.match(s):
        return ""
    s = _SPEAKER_TAG_RE.sub("", s)            # drop the voice tag, keep the spoken line
    s = re.sub(r"\[[^\]]*\]", " ", s)         # drop [delivery notes]
    s = re.sub(r'[*_`>#"]', " ", s)           # strip emphasis / quote / heading markers
    return re.sub(r"\s+", " ", s).strip()


def _is_witness_prose_line(raw: str) -> bool:
    s = raw.strip()
    if not s or s == "---" or _BEAT_RE.match(s):
        return False
    if _SPEAKER_TAG_RE.match(s):              # a tagged dialogue line is NOT witness prose
        return False
    return bool(_clean_spoken_line(s))


def parse_witness(md: str) -> ParsedWitness:
    """Parse an eyewitness narration.md per §2.1. Everything after the FIRST '---' is spoken."""
    title = ""
    form_hint = None
    for line in md.splitlines():
        if line.startswith("# "):
            title = line[2:].strip()
            m = re.search(r"\((short|long)\)", title, re.I)
            if m:
                form_hint = m.group(1).lower()
            break

    parts = md.split("\n---", 1)
    if len(parts) == 2:
        header, body = parts[0], parts[1].lstrip("-\n")
    else:                                     # no front-matter rule: treat all as body
        header, body = "", md

    # split the body into beats by the `## Beat N — name` headers
    beats: list[Beat] = []
    cur_n: int | None = None
    cur_name = ""
    cur_lines: list[str] = []

    def _flush():
        if cur_n is not None:
            spoken = " ".join(_clean_spoken_line(l) for l in cur_lines).strip()
            spoken = re.sub(r"\s+", " ", spoken)
            beats.append(Beat(n=cur_n, name=cur_name, spoken=spoken))

    for line in body.splitlines():
        m = _BEAT_RE.match(line.strip())
        if m:
            _flush()
            cur_n = int(m.group(1))
            cur_name = m.group(2).strip()
            cur_lines = []
        elif cur_n is not None:
            cur_lines.append(line)
    _flush()

    spoken_text = re.sub(
        r"\s+", " ",
        " ".join(_clean_spoken_line(l) for l in body.splitlines())
    ).strip()
    kjv_quotes = _KJV_QUOTE_RE.findall(body)
    speaker_tags: list[str] = []
    dialogue_lines: list[tuple[str, str]] = []
    for l in body.splitlines():
        m = _SPEAKER_TAG_RE.match(l.strip())
        if m:
            spk = m.group(1).strip()
            speaker_tags.append(spk)
            dialogue_lines.append((spk.lower(), l.strip()))
    has_witness_prose = any(_is_witness_prose_line(l) for l in body.splitlines())

    return ParsedWitness(
        title=title, form_hint=form_hint, header=header, body=body, beats=beats,
        spoken_text=spoken_text, kjv_quotes=kjv_quotes,
        speaker_tags=speaker_tags, has_witness_prose=has_witness_prose,
        dialogue_lines=dialogue_lines,
    )


# ---------------------------------------------------------------- passage loading (EW-G1)
def load_passage(folder: Path) -> str | None:
    """The KJV source text to verbatim-check quotes against. STRICT: a folder-local
    `passage.txt` (the episode's NARROW pericope + its named NT cross-refs) is REQUIRED —
    no whole-cache fallback (that fallback let a verbatim quote from the WRONG book pass as
    'attributed', per the red-team). No passage.txt -> None -> EW-G1 fail-closed."""
    p = folder / "passage.txt"
    if p.is_file():
        return p.read_text(encoding="utf-8")
    return None


def _word_count(text: str) -> int:
    return len(text.split())


def _norm_kjv(s: str) -> str:
    """Normalize for a strict verbatim substring test: lowercase, smart-quote/dagger fold,
    strip everything but letters/apostrophes, collapse whitespace."""
    s = s.replace("’", "'").replace("�", "'")
    s = re.sub(r"\[\d+:\d+\]", " ", s).lower()
    s = re.sub(r"[^a-z' ]+", " ", s)
    return re.sub(r"\s+", " ", s).strip()


# ---------------------------------------------------------------- EW-G1 KJV-strict
def ew_g1_kjv(parsed: ParsedWitness, passage: str | None) -> GateResult:
    quotes = [q for q in parsed.kjv_quotes if q.strip()]
    if not quotes:
        return GateResult("EW-G1", "KJV-strict", True, True,
                          "no bold KJV quotes to verify (eyewitness may carry none)")
    if not passage or not passage.strip():
        return GateResult("EW-G1", "KJV-strict", False, True,
                          f"{len(quotes)} KJV quote(s) but NO passage.txt to verify against "
                          "(fail-closed) — provide the episode's narrow pericope + NT cross-refs")
    # STRICT: every bold quote must be a verbatim substring of the supplied passage. We do NOT
    # use kjv_check's overlap-threshold (which IGNORES low-overlap = lets fabrications through).
    npassage = _norm_kjv(passage)
    bad = [q for q in quotes if _norm_kjv(q) not in npassage]
    if bad:
        return GateResult("EW-G1", "KJV-strict", False, True,
                          f"{len(bad)} bold quote(s) NOT verbatim in passage.txt "
                          "(fabricated, altered, or misattributed)",
                          findings=[f'not in passage: "{q[:70]}"' for q in bad])
    return GateResult("EW-G1", "KJV-strict", True, True,
                      f"all {len(quotes)} bold quote(s) verbatim in the episode passage")


# ---------------------------------------------------------------- EW-G2 Spine coverage
def _role_of(name: str, role_keywords: dict) -> str | None:
    low = name.lower()
    for role, kws in role_keywords.items():
        if any(kw in low for kw in kws):
            return role
    return None


def ew_g2_spine(parsed: ParsedWitness, form: str, rules: dict) -> GateResult:
    beats = parsed.beats
    if not beats:
        return GateResult("EW-G2", "Spine", False, True,
                          "no `## Beat N — name` headers found (the spine is missing)")
    nums = [b.n for b in beats]
    if nums != sorted(nums) or len(set(nums)) != len(nums):
        return GateResult("EW-G2", "Spine", False, True,
                          f"beats out of order / duplicated: {nums}")

    if form == "long":
        need = {b["n"] for b in rules["beats_long"]}
        have = set(nums)
        missing = sorted(need - have)
        if missing:
            return GateResult("EW-G2", "Spine", False, True,
                              f"LONG needs all 7 beats; missing beat number(s) {missing}",
                              findings=[f"present: {nums}"])
        return GateResult("EW-G2", "Spine", True, True,
                          f"all 7 beats present & ordered {nums}")

    # SHORT: hook -> act -> reveal -> invitation present & in order
    role_kw = rules["role_keywords"]
    required = rules["required_roles_short"]
    pos: dict[str, int] = {}
    for i, b in enumerate(beats):
        r = _role_of(b.name, role_kw)
        if r and r not in pos:
            pos[r] = i
    missing = [r for r in required if r not in pos]
    if missing:
        return GateResult("EW-G2", "Spine", False, True,
                          f"SHORT missing required beat role(s): {missing}",
                          findings=[f"beats: {[b.name for b in beats]}"])
    order = [pos[r] for r in required]
    if order != sorted(order):
        return GateResult("EW-G2", "Spine", False, True,
                          f"SHORT roles out of order (hook->act->reveal->invitation): {order}")
    return GateResult("EW-G2", "Spine", True, True,
                      f"SHORT spine present & ordered ({required})")


# ---------------------------------------------------------------- EW-G3 Word budget
def ew_g3_words(parsed: ParsedWitness, form: str, rules: dict) -> GateResult:
    lo = rules["forms"][form]["word_min"]
    hi = rules["forms"][form]["word_max"]
    n = _word_count(parsed.spoken_text)
    if n < lo:
        return GateResult("EW-G3", "Word budget", False, True,
                          f"{n} spoken words < {lo} ({form} floor) — too thin")
    if n > hi:
        return GateResult("EW-G3", "Word budget", False, True,
                          f"{n} spoken words > {hi} ({form} ceiling) — over budget")
    return GateResult("EW-G3", "Word budget", True, True,
                      f"{n} spoken words within {lo}-{hi} ({form})")


# ---------------------------------------------------------------- EW-G4 CTA-on-Jesus
def ew_g4_cta(parsed: ParsedWitness, rules: dict) -> GateResult:
    if not parsed.beats:
        return GateResult("EW-G4", "CTA-on-Jesus", False, True,
                          "no beats — cannot locate the closing invitation")
    last = parsed.beats[-1]
    text = " ".join(re.findall(r"[a-z']+", last.spoken.lower()))
    findings: list[str] = []
    has_jesus = any(t in text for t in rules["jesus_tokens"])
    has_verb = any(re.search(rf"\b{re.escape(v)}\b", text) for v in rules["invitation_verbs"])
    banned = [b for b in rules["banned_cta_templates"] if b in text]
    fear = [p for p in rules.get("fear_gainloss_lexicon", []) if p in text]
    if not has_jesus:
        findings.append("the closing beat names neither 'Jesus' nor 'Christ'")
    if not has_verb:
        findings.append(f"no invitation verb ({'/'.join(rules['invitation_verbs'])}) in the close")
    if banned:
        findings.append(f"banned bare-CTA template: {banned}")
    if fear:
        findings.append(f"fear / gain-loss / manufactured-pressure framing (EW-INV-2 forbids): {fear}")
    if findings:
        return GateResult("EW-G4", "CTA-on-Jesus", False, True,
                          f"closing beat '{last.name}' fails the CTA-on-Jesus rule",
                          findings=findings)
    return GateResult("EW-G4", "CTA-on-Jesus", True, True,
                      f"closing beat '{last.name}' lands on Jesus with an invitation verb")


# ---------------------------------------------------------------- EW-G5 First-person
def ew_g5_first_person(parsed: ParsedWitness, form: str, rules: dict) -> GateResult:
    floor = rules["forms"][form]["first_person_floor"]
    density_min = rules["forms"][form].get("first_person_density_min", 0.0)
    low = parsed.spoken_text.lower()
    count = 0
    for m in rules["first_person_markers"]:
        count += len(re.findall(rf"(?<![\w']){re.escape(m)}(?![\w'])", low))
    words = max(1, _word_count(parsed.spoken_text))
    density = count / words * 100.0
    if count < floor:
        return GateResult("EW-G5", "First-person", False, True,
                          f"only {count} first-person marker(s) < floor {floor} ({form}) — "
                          "reads as third-person essay, not a witness")
    # DENSITY: an essay sprinkled with a few "I" tics clears a raw floor but has low density;
    # a true first-person witness monologue runs high (the pilot ~11.5 /100 spoken words).
    if density < density_min:
        return GateResult("EW-G5", "First-person", False, True,
                          f"first-person density {density:.1f}/100 < {density_min} — "
                          f"{count} markers in {words} words reads as essay-narrator-in-costume, "
                          "not a sustained first-person witness")
    return GateResult("EW-G5", "First-person", True, True,
                      f"{count} first-person marker(s), density {density:.1f}/100 >= {density_min}")


# ---------------------------------------------------------------- EW-G6 Cast present
def ew_g6_cast(parsed: ParsedWitness, rules: dict) -> GateResult:
    min_voices = rules["cast"]["min_voices"]
    voices: set[str] = set()
    if parsed.has_witness_prose:
        voices.add("witness")
    if parsed.kjv_quotes:
        voices.add("scripture")
    for tag in parsed.speaker_tags:
        voices.add(tag.lower())
    # the spec flag: KJV quotes exist but no scripture routing is possible
    if parsed.kjv_quotes and "scripture" not in voices:
        return GateResult("EW-G6", "Cast present", False, True,
                          "KJV quotes exist but no scripture voice can be routed")
    if len(voices) < min_voices:
        return GateResult("EW-G6", "Cast present", False, True,
                          f"only {len(voices)} voice role(s) {sorted(voices)} < {min_voices} — "
                          "single-voice; add the scripture reader / a named speaker")
    return GateResult("EW-G6", "Cast present", True, True,
                      f"{len(voices)} voice role(s): {sorted(voices)}")


# ---------------------------------------------------------------- EW-G11 Words-of-God
def ew_g11_words_of_god(parsed: ParsedWitness, rules: dict) -> GateResult:
    """DOCTRINE (EW-INV-11): God / the LORD / Jesus get NO invented dialogue. Any line tagged
    with a divine speaker MUST carry a bold **"..."** KJV quote span (which EW-G1 then verifies
    verbatim). A divine-tagged line of free prose = words put in God's mouth = BLOCK."""
    divine = {d.replace("_", " ") for d in rules.get("divine_speaker_roles", [])}
    offenders: list[str] = []
    for spk, raw in parsed.dialogue_lines:
        if spk.replace("_", " ") in divine and not _KJV_QUOTE_RE.search(raw):
            offenders.append(f'[{spk}] invented (no KJV quote): "{_clean_spoken_line(raw)[:60]}"')
    if offenders:
        return GateResult("EW-G11", "Words-of-God", False, True,
                          f"{len(offenders)} invented line(s) attributed to God/Jesus "
                          "(divine speech must be verbatim KJV only)", findings=offenders)
    return GateResult("EW-G11", "Words-of-God", True, True,
                      "no invented words placed in God's / Jesus' mouth")


# ---------------------------------------------------------------- EW-G12 Reveal sound
def _reveal_beat(parsed: ParsedWitness, rules: dict) -> Beat | None:
    for b in parsed.beats:                    # explicit long beat 6
        if b.n == 6:
            return b
    for b in parsed.beats:                    # else by role keyword
        if _role_of(b.name, rules["role_keywords"]) == "reveal":
            return b
    return None


def ew_g12_reveal(parsed: ParsedWitness, rules: dict) -> GateResult:
    """DOCTRINE: (a) ban the templated reveal stinger ('at last I understood' etc.) anywhere in
    the spoken text (EW-INV / anti-template); (b) the reveal beat must NAME Christ in its body
    (the type->fulfillment turn is explicit, EW-INV-3), not just in a header."""
    low = parsed.spoken_text.lower()
    findings: list[str] = []
    banned = [p for p in rules.get("banned_spoken_phrases", []) if p in low]
    if banned:
        findings.append(f"banned templated reveal phrase (vary it): {banned}")
    rb = _reveal_beat(parsed, rules)
    if rb is not None:
        rlow = rb.spoken.lower()
        if not any(t in rlow for t in rules["jesus_tokens"]):
            findings.append(f"reveal beat '{rb.name}' body never names Jesus/Christ "
                            "(the type->fulfillment turn must be explicit, not just a header)")
    if findings:
        return GateResult("EW-G12", "Reveal sound", False, True,
                          "reveal beat / templated-phrase problem", findings=findings)
    return GateResult("EW-G12", "Reveal sound", True, True,
                      "reveal names Christ explicitly; no templated reveal stinger")


# ---------------------------------------------------------------- run all
def run_gates(md: str, form: str, passage: str | None) -> list[GateResult]:
    rules = load_rules()
    if form not in rules["forms"]:
        raise ValueError(f"unknown form {form!r} (expected short|long)")
    parsed = parse_witness(md)
    return [
        ew_g1_kjv(parsed, passage),
        ew_g2_spine(parsed, form, rules),
        ew_g3_words(parsed, form, rules),
        ew_g4_cta(parsed, rules),
        ew_g5_first_person(parsed, form, rules),
        ew_g6_cast(parsed, rules),
        ew_g11_words_of_god(parsed, rules),
        ew_g12_reveal(parsed, rules),
    ]


def blocking_findings(results: list[GateResult]) -> list[str]:
    out: list[str] = []
    for r in results:
        if not r.ok and r.blocking:
            out.append(str(r))
            out.extend(f"    - {f}" for f in r.findings)
    return out
