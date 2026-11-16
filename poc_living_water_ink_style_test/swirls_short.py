"""swirls_short.py -- the gates and arithmetic for the Swirls SHORT pipeline (45 s, 8 units: front
cover + 6 storyboard pages + back cover). Design: _swirls_short_design\\SWIRLS_SHORT_PIPELINE_DESIGN_v3.md
(v3.2, binding). $0 module: it reads files, runs ffmpeg/ffprobe and does arithmetic; it never
calls a paid API. The spend guard lives in swirls_guard.py (re-exported here: SpendRefused,
sha256_of, price helpers).

  timing   build_timing / lint_timing (SWS-G2, G3)      real ElevenLabs alignment + meta, no fallback
  words    lint_words (G1, G1e), lint_sequence (G1s), lint_kjv (G1k), lint_speakers (G1v)
  page     lint_baked_text (G4), lint_still_prose (G5), lint_clip_prose (G5a), validate_page_plan,
           lint_dosage (G6), lint_refs_* (G7a/b/c), lint_motion_carrier (G8), lint_order (G8t)
  clips    clip_tech (G11), lint_clip_provenance / lint_still_provenance (G14 / G14s),
           moving_hold (G15h), still_stretch (G12), make_strips + judge_eyes (G13)
  stills   edge_scan (G10)
  film     lint_assembly (G15), score_gate (G17), final chain (G16), film_panel_pass
  owner    status
"""
from __future__ import annotations

import datetime
import json
import math
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(HERE))
from pipeline.models import GateResult  # noqa: E402
import swirls_guard as guard  # noqa: E402
from swirls_guard import SpendRefused, sha256_of  # noqa: E402,F401

# ------------------------------------------------------------------ constants ---
OUTRO_HOLD = 3.0
FPS = 30
WORDS_PER_SECOND = 2.2           # measured on ep13 / ep16
TURN_PAUSE_SECONDS = 0.4         # counted only before a voiced quote (all the synth adds)
FRONT_SLOT = (2.0, 3.0)          # PASS; WARN to 3.5; FAIL under 1.8 / over 3.5
FRONT_SLOT_FAIL = (1.8, 3.5)
PAGE_SLOT = (5.0, 7.0)
PAGE_SLOT_FAIL = (4.5, 7.5)
BACK_SLOT = (6.0, 8.5)
BACK_SLOT_FAIL = (4.0, 9.0)
FILM_PASS = (42.0, 48.0)
FILM_FAIL = (40.0, 50.0)
VOICE_PASS = (39.0, 45.0)
VOICE_FAIL = (37.0, 47.0)
HOOK_WORDS = (4, 5)
PAGE_WORDS = (11, 14)            # 10 or 15 = WARN
LAST_LINE_MAX_WORDS = 10
TOTAL_WORDS = (80, 88)
EST_FILM = (38.0, 42.0)
MAX_VOICED_QUOTES = 5
FIRST_WORD_MAX_START = 0.40
KLING_MIN_S, KLING_MAX_S = guard.KLING_MIN_S, guard.KLING_MAX_S
MIN_CLIP_SIZE = (1072, 1900)
OUT_SIZE = (1080, 1920)
KLING_CR_PER_SECOND = guard.KLING_CR_PER_SECOND
STILL_CR = guard.STILL_CR
USD_PER_CR = guard.USD_PER_CR
MOTIF_STAGE = {"front": 0, "f01": 0, "f02": 1, "f03": 1, "f04": 2, "f05": 2, "f06": 3, "back": 3}
TAGS = ["front", "f01", "f02", "f03", "f04", "f05", "f06", "back"]
# G15h tuning (set by test T8 on real back covers vs frozen copies)
HOLD_K = 3.0
HOLD_ABS_FLOOR = 0.5     # T8 (real ep10/ep13/ep16 back covers): real windows >= 1.26, frozen / frame-0 / stops-at-1.5 copies <= 0.10 / 0.0
# T9: the pixel edge scan did NOT separate the shipped ep2/ep5/ep7/ep8 covers from ep10/ep13 (ep10 and ep13
# 'good' covers trip it; ep2 back and ep13 back pass), so on covers it can only WARN until a better
# detector exists. The design wants FAIL on covers; flip this to "FAIL" once T9 separates.
EDGE_COVER_LEVEL = "CONDITIONAL"
EDGE_PAGE_LEVEL = "CONDITIONAL"
NEVER_OVERRIDABLE = ("SWS-G0", "SWS-G1k", "SWS-G1s", "SWS-G14", "SWS-G14s", "SWS-G16")


def _g(gate, verdict, evidence, fix=""):
    return GateResult(gate, verdict, evidence, fix)


def is_pass(gates) -> bool:
    """WARN never counts as pass: only PASS verdicts are a pass."""
    return all(g.verdict == "PASS" for g in gates)


def no_fail(gates) -> bool:
    return not any(g.verdict == "FAIL" for g in gates)


# ============================================================== TOKENS / TIMING ===
class TimingError(RuntimeError):
    """Alignment / counts are missing or wrong. There is no fallback (fail closed)."""


_TOK = re.compile(r"[A-Za-z0-9]+(?:['’-][A-Za-z0-9]+)*")


def norm_tokens(text: str) -> list[str]:
    """Lower-cased word tokens; punctuation ignored. The unit of every sequence comparison."""
    return [t.lower().replace("’", "'") for t in _TOK.findall(str(text))]


def spoken_tokens(text: str) -> list[str]:
    return norm_tokens(text)


def _ffprobe_duration(p: Path) -> float:
    out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                          "-of", "default=nw=1:nk=1", str(p)],
                         capture_output=True, text=True, check=True).stdout.strip()
    return float(out)


def expected_clip_duration(index: int, n_units: int, slot: float) -> int:
    """front max(3, ceil(slot+0.5)); pages ceil(slot+0.5); back min(15, ceil(slot+2.0))."""
    if index == n_units - 1:
        return min(KLING_MAX_S, math.ceil(slot + 2.0 - 1e-9))
    if index == 0:
        return max(KLING_MIN_S, math.ceil(slot + 0.5 - 1e-9))
    return math.ceil(slot + 0.5 - 1e-9)


def md_tokens(md_text: str) -> list[str]:
    body = "\n".join(ln for ln in md_text.splitlines() if not ln.lstrip().startswith("#"))
    body = re.sub(r"<!--.*?-->", " ", body, flags=re.S)
    return norm_tokens(body)


def tagged_transcript_tokens(folder: Path) -> list[str]:
    from pipeline.assembly_align import transcript
    return norm_tokens(transcript(Path(folder)))


def lint_sequence(units: dict[str, str], md_text: str, tagged_tokens: list[str] | None,
                  align_tokens: list[str] | None = None) -> list[GateResult]:
    """SWS-G1s: the identical ordered token list in units.json (joined), narration.md (comments
    stripped), the narration-tagged.md transcript and (when given) the alignment words.
    Counts alone are not enough: two swapped words or one changed word FAIL. Never overridable."""
    lists = {"units.json": [t for txt in units.values() for t in norm_tokens(txt)],
             "narration.md": md_tokens(md_text)}
    if tagged_tokens is not None:
        lists["narration-tagged.md"] = tagged_tokens
    if align_tokens is not None:
        lists["alignment"] = align_tokens
    ref_name, ref = next(iter(lists.items()))
    bad = []
    for name, lst in list(lists.items())[1:]:
        if lst != ref:
            i = next((k for k, (a, b) in enumerate(zip(ref, lst)) if a != b), min(len(ref), len(lst)))
            bad.append(f"{name} differs from {ref_name} at word {i + 1}: "
                       f"{ref[i] if i < len(ref) else '(end)'!r} vs {lst[i] if i < len(lst) else '(end)'!r} "
                       f"(lengths {len(ref)} / {len(lst)})")
    if bad:
        return [_g("SWS-G1s", "FAIL", "; ".join(bad), "make every text file say the same words in the same order")]
    return [_g("SWS-G1s", "PASS", f"{len(lists)} lists, {len(ref)} identical ordered words")]


def read_alignment(folder: Path) -> tuple[list[dict], dict]:
    """Words + meta of a trim episode. The meta must name ElevenLabs and THIS audio file."""
    d = Path(folder)
    af, mf, mp3 = d / "narration.alignment.json", d / "narration.alignment.meta.json", d / "narration.mp3"
    if not af.exists() or not mf.exists() or not mp3.exists():
        raise TimingError(f"missing alignment / alignment meta / narration.mp3 in {d}")
    meta = json.loads(mf.read_text(encoding="utf-8"))
    if meta.get("backend") != "elevenlabs":
        raise TimingError(f"alignment backend is {meta.get('backend')!r}: only ElevenLabs forced alignment "
                          "may set timing (no whisper fallback)")
    if meta.get("audio_sha256") != sha256_of(mp3):
        raise TimingError("alignment meta audio_sha256 does not match narration.mp3 (stale alignment)")
    words = [w for w in (json.loads(af.read_text(encoding="utf-8")).get("words") or [])
             if re.search(r"[A-Za-z0-9]", str(w.get("text", "")))]
    if not words:
        raise TimingError("narration.alignment.json has no words")
    if meta.get("word_count") != len(words):
        raise TimingError(f"alignment meta word_count {meta.get('word_count')} != {len(words)} words")
    return words, meta


def build_timing(episode_dir: Path, manifest_words: dict[str, int] | None = None, write: bool = True) -> dict:
    """Unit k spans [first word of k, first word of k+1); front starts at 0.0; back ends at
    narration + 3.0. Fail closed: missing files, a missing / stale / non-ElevenLabs alignment meta,
    or ANY difference in the ordered word list between units.json, narration.md, narration-tagged.md
    and the alignment (SWS-G1s) is an error -- never a fallback guess."""
    d = Path(episode_dir)
    need = ["units.json", "narration.md", "narration-tagged.md"]
    missing = [n for n in need if not (d / n).exists()]
    if missing:
        raise TimingError(f"missing {missing} in {d}")
    units = json.loads((d / "units.json").read_text(encoding="utf-8"))
    if not isinstance(units, dict) or not units:
        raise TimingError("units.json must be a non-empty {tag: exact text} object")
    words, _meta = read_alignment(d)
    try:
        tagged = tagged_transcript_tokens(d)
    except SystemExit as e:
        raise TimingError(str(e))
    g1s = lint_sequence(units, (d / "narration.md").read_text(encoding="utf-8"), tagged,
                        [t for w in words for t in norm_tokens(w["text"])])[0]
    if g1s.verdict != "PASS":
        raise TimingError(f"SWS-G1s: {g1s.evidence}")
    counts = {tag: len(norm_tokens(txt)) for tag, txt in units.items()}
    if manifest_words is not None:
        bad = {t: (manifest_words.get(t), c) for t, c in counts.items() if manifest_words.get(t) != c}
        if bad:
            raise TimingError(f"Unit.words in episode.py != units.json (tag: (episode.py, units.json)): {bad}")
    narration_s = _ffprobe_duration(d / "narration.mp3")
    last_end = float(words[-1]["end"])
    if narration_s - last_end > 2.0 or last_end > narration_s + 0.5:
        raise TimingError(f"alignment does not cover the audio: last word ends {last_end:.2f}s, "
                          f"narration.mp3 is {narration_s:.2f}s")
    tags = list(units)
    idx, starts = 0, []
    for tag in tags:
        starts.append(float(words[idx]["start"]))
        idx += counts[tag]
    out_units, prev_b = {}, 0
    for i, tag in enumerate(tags):
        start_s = 0.0 if i == 0 else starts[i]
        end_s = starts[i + 1] if i + 1 < len(tags) else round(narration_s + OUTRO_HOLD, 3)
        slot = end_s - start_s
        b = round(end_s * FPS)
        out_units[tag] = {"start_s": round(start_s, 3), "end_s": round(end_s, 3),
                          "clip_duration": expected_clip_duration(i, len(tags), slot),
                          "end_frame": b, "frames": b - prev_b}
        prev_b = b
    doc = {
        "schema": "swirls-of-life/unit_timing v2",
        "episode": d.name,
        "written": datetime.date.today().isoformat(),
        "source": "narration.alignment.json (real ElevenLabs per-word timestamps)",
        "boundary_rule": "unit k spans [start_s of unit k's first spoken word, start_s of unit k+1's "
                         "first spoken word); the last unit runs to narration_end + outro_hold; "
                         "frames: B(k) = round(end_s(k) x 30), unit k has B(k)-B(k-1) frames",
        "narration_seconds": round(narration_s, 3),
        "outro_hold_seconds": OUTRO_HOLD,
        "fps": FPS,
        "first_word_start_s": round(float(words[0]["start"]), 3),
        "units": out_units,
    }
    if write:
        (d / "unit_timing.json").write_text(json.dumps(doc, indent=2), encoding="utf-8")
    return doc


def slot_of(doc: dict, tag: str) -> float:
    u = doc["units"][tag]
    return float(u["end_s"]) - float(u["start_s"])


def _zone(x: float, ok: tuple, hard: tuple) -> str:
    if ok[0] <= x <= ok[1]:
        return "PASS"
    return "WARN" if hard[0] <= x <= hard[1] else "FAIL"


def lint_timing(doc: dict, spec_clip_durations: dict | None = None, tempo_factor: float | None = None,
                manifest_size: tuple[int, int] | None = None) -> list[GateResult]:
    """SWS-G2 (voice) + SWS-G3 (slots, film, clip lengths incl. back = ceil(slot + 2.0), 1080x1920)."""
    out = []
    bad = []
    if tempo_factor is not None and abs(tempo_factor - 1.0) > 1e-6:
        bad.append(f"tempo factor {tempo_factor} != 1.0 (no time-stretch)")
    if doc.get("first_word_start_s", 0.0) > FIRST_WORD_MAX_START:
        bad.append(f"first word starts at {doc['first_word_start_s']}s (> {FIRST_WORD_MAX_START}s)")
    voice = float(doc["narration_seconds"])
    z = _zone(voice, VOICE_PASS, VOICE_FAIL)
    if z == "FAIL":
        bad.append(f"voice {voice:.1f}s outside {VOICE_FAIL}")
    if bad:
        out.append(_g("SWS-G2", "FAIL", "; ".join(bad), "re-record / re-time the voice"))
    elif z == "WARN":
        out.append(_g("SWS-G2", "CONDITIONAL", f"voice {voice:.1f}s outside the {VOICE_PASS} target"))
    else:
        out.append(_g("SWS-G2", "PASS", f"voice {voice:.1f}s, first word {doc.get('first_word_start_s')}s"))
    tags = list(doc["units"])
    fails, warns = [], []
    total = 0.0
    for i, tag in enumerate(tags):
        u = doc["units"][tag]
        slot = slot_of(doc, tag)
        total += slot
        ok, hard = ((FRONT_SLOT, FRONT_SLOT_FAIL) if i == 0 else (BACK_SLOT, BACK_SLOT_FAIL)
                    if i == len(tags) - 1 else (PAGE_SLOT, PAGE_SLOT_FAIL))
        zz = _zone(slot, ok, hard)
        if zz == "FAIL":
            fails.append(f"{tag} slot {slot:.2f}s outside {hard}")
        elif zz == "WARN":
            warns.append(f"{tag} slot {slot:.2f}s outside {ok}")
        cd = u.get("clip_duration")
        if not isinstance(cd, int) or isinstance(cd, bool) or not KLING_MIN_S <= cd <= KLING_MAX_S:
            fails.append(f"{tag} clip_duration {cd!r} is not a legal Kling length (integer {KLING_MIN_S}..{KLING_MAX_S})")
        else:
            want = expected_clip_duration(i, len(tags), slot)
            if cd != want:
                fails.append(f"{tag} clip_duration {cd}s != {want}s "
                             f"({'back = ceil(slot + 2.0)' if i == len(tags) - 1 else 'ceil(slot + 0.5)'})")
            if cd < slot + 0.1:
                fails.append(f"{tag} clip_duration {cd}s < slot {slot:.2f}s + 0.1")
        if spec_clip_durations is not None and spec_clip_durations.get(tag) != cd:
            fails.append(f"{tag} spec clip_duration {spec_clip_durations.get(tag)!r} != unit_timing {cd!r}")
    zf = _zone(total, FILM_PASS, FILM_FAIL)
    if zf == "FAIL":
        fails.append(f"film {total:.1f}s outside {FILM_FAIL}")
    elif zf == "WARN":
        warns.append(f"film {total:.1f}s outside {FILM_PASS}")
    if manifest_size is not None and tuple(manifest_size) != OUT_SIZE:
        fails.append(f"manifest declares {manifest_size[0]}x{manifest_size[1]}, a trim episode must declare "
                     f"{OUT_SIZE[0]}x{OUT_SIZE[1]}")
    if fails:
        out.append(_g("SWS-G3", "FAIL", "; ".join(fails), "re-cut the words or fix clip_duration / manifest size"))
    elif warns:
        out.append(_g("SWS-G3", "CONDITIONAL", "; ".join(warns)))
    else:
        out.append(_g("SWS-G3", "PASS", f"{len(tags)} units, film {total:.1f}s, clip lengths legal, {OUT_SIZE[0]}x{OUT_SIZE[1]}"))
    return out


# ================================================================== WORDS (G1 family) ===
def derive_speakers(folder: Path, units: dict[str, str]) -> dict[str, dict]:
    """Speaker per unit DERIVED from narration-tagged.md (never typed): {tag: {speaker, voiced,
    cue_missing}} where voiced = number of character (non-narrator) lines heard in that unit."""
    from pipeline.assembly_timing import _parse_tagged_chunks
    tagged = Path(folder) / "narration-tagged.md"
    chunks = _parse_tagged_chunks(tagged)
    raw = tagged.read_text(encoding="utf-8")
    raw = re.sub(r"<!--.*?-->", " ", raw, flags=re.S)
    no_cue = []
    for m in re.finditer(r'<speaker name="([^"]+)">(.*?)</speaker>', raw, flags=re.S):
        if not re.search(r"\[[^\]]+\]", m.group(2)):
            no_cue.append(m.group(1))
    info = {t: {"speaker": "", "voiced": 0, "cue_missing": []} for t in units}
    tags = list(units)
    bounds, acc = [], 0
    for t in tags:
        acc += len(norm_tokens(units[t]))
        bounds.append(acc)
    pos = 0
    for sp, text in chunks:
        n = len(norm_tokens(text))
        if n and sp != "narrator":
            lo, hi = pos, pos + n - 1
            for ti, t in enumerate(tags):
                b0 = bounds[ti - 1] if ti else 0
                if lo < bounds[ti] and hi >= b0:
                    info[t]["voiced"] += 1
                    info[t]["speaker"] = sp
        pos += n
    for t in tags:
        info[t]["cue_missing"] = no_cue if info[t]["speaker"] else []
    return info


def lint_speakers(info: dict[str, dict]) -> list[GateResult]:
    """SWS-G1v: speaker is derived; every character line carries an emotion cue."""
    miss = sorted({s for v in info.values() for s in v["cue_missing"]})
    if miss:
        return [_g("SWS-G1v", "FAIL", f"character line(s) with no [emotion] cue: {miss}", "add a cue to every character line")]
    return [_g("SWS-G1v", "PASS", "speakers derived from narration-tagged.md; every character line has a cue")]


def lint_words(units: dict[str, str], voiced: dict[str, int] | None = None) -> list[GateResult]:
    """SWS-G1 (shape) + SWS-G1e (estimate), FAIL level. `voiced` = voiced character quotes per unit."""
    voiced = voiced or {}
    tags = list(units)
    fails, warns = [], []
    if len(tags) != 8:
        fails.append(f"{len(tags)} units (need 8)")
    total_w, est_film = 0, 0.0
    efails = []
    for i, tag in enumerate(tags):
        n = len(norm_tokens(units[tag]))
        v = voiced.get(tag, 0)
        total_w += n
        if i == 0:
            if not HOOK_WORDS[0] <= n <= HOOK_WORDS[1]:
                fails.append(f"hook {n} words (need {HOOK_WORDS[0]}-{HOOK_WORDS[1]})")
            est = n / WORDS_PER_SECOND + 0.3
            if est > FRONT_SLOT[1] + 1e-9:
                efails.append(f"hook estimate {est:.1f}s > {FRONT_SLOT[1]}s")
        elif i == len(tags) - 1:
            if n > LAST_LINE_MAX_WORDS:
                fails.append(f"last line {n} words (max {LAST_LINE_MAX_WORDS})")
            est = n / WORDS_PER_SECOND + OUTRO_HOLD
            if est > 9.0 + 1e-9:
                efails.append(f"{tag} estimate {est:.1f}s > 9.0s")
        else:
            if n in (PAGE_WORDS[0] - 1, PAGE_WORDS[1] + 1):
                warns.append(f"{tag} {n} words (WARN at 10 or 15)")
            elif not PAGE_WORDS[0] <= n <= PAGE_WORDS[1]:
                fails.append(f"{tag} {n} words (need {PAGE_WORDS[0]}-{PAGE_WORDS[1]})")
            if v > 1:
                fails.append(f"{tag} has {v} voiced quotes (max 1 per page)")
            est = n / WORDS_PER_SECOND + TURN_PAUSE_SECONDS * v
            if not 4.5 <= est <= 7.5:
                efails.append(f"{tag} estimate {est:.1f}s outside 4.5-7.5")
        est_film += n / WORDS_PER_SECOND + TURN_PAUSE_SECONDS * v
    if not TOTAL_WORDS[0] <= total_w <= TOTAL_WORDS[1]:
        fails.append(f"{total_w} words in total (need {TOTAL_WORDS[0]}-{TOTAL_WORDS[1]})")
    if sum(voiced.values()) > MAX_VOICED_QUOTES:
        fails.append(f"{sum(voiced.values())} voiced character quotes (max {MAX_VOICED_QUOTES})")
    if not EST_FILM[0] <= est_film <= EST_FILM[1]:
        efails.append(f"film estimate {est_film:.1f}s outside {EST_FILM}")
    out = []
    out.append(_g("SWS-G1", "FAIL", "; ".join(fails), "cut or reshape the lines before any money") if fails
               else _g("SWS-G1", "CONDITIONAL" if warns else "PASS",
                       "; ".join(warns) if warns else f"8 units, {total_w} words, {sum(voiced.values())} voiced quotes"))
    out.append(_g("SWS-G1e", "FAIL", "; ".join(efails), "the words will not fit the slots") if efails
               else _g("SWS-G1e", "PASS", f"estimate {est_film:.1f}s"))
    return out


# ---- G1k: KJV wrapper (in lane; kjv_strict.verify_span alone passes "I am ... the Christ") ---
_ELLIPSIS = re.compile(r"\.\.\.|…")
_END_PUNCT = " .!?\"'”’"


def _words_core(text: str) -> list[tuple[str, str]]:
    """(core word, attached trailing punctuation) per whitespace word; leading punctuation dropped."""
    out = []
    for w in text.replace("’", "'").replace("‘", "'").split():
        m = re.match(r"^[^A-Za-z0-9]*(.*?[A-Za-z0-9])([^A-Za-z0-9]*)$", w)
        if m:
            out.append((m.group(1), m.group(2)))
    return out


def kjv_run_found(ref: str, span_text: str) -> tuple[bool, str]:
    from pipeline import kjv_strict
    verses = kjv_strict.verse_texts(ref)
    if not verses:
        return False, f"ref {ref!r} not found in the pinned KJV corpus"
    hay = _words_core(kjv_strict._strip_markers(" ".join(verses)))
    span = _words_core(span_text)
    if not span:
        return False, "empty span"
    n = len(span)
    for s in range(0, len(hay) - n + 1):
        win = hay[s:s + n]
        if any(a[0] != b[0] for a, b in zip(win, span)):
            continue
        if any(win[i][1] != span[i][1] for i in range(n - 1)):
            continue
        last_h, last_s = win[-1][1], span[-1][1]
        if last_s == last_h or last_s == "" or all(c in _END_PUNCT for c in last_s):
            return True, "ok"
    return False, "no continuous whole-word, case-sensitive run of the verse matches"


def lint_kjv(spans: list[dict], narration_text: str, tagged_chunks: list[tuple[str, str]]) -> list[GateResult]:
    """SWS-G1k. For every span {ref, speaker, text}: (1) no `...` / the ellipsis character; (2) one
    continuous whole-word run inside the verse (or across consecutive verses of the ref); (3)
    case-sensitive ("LORD" is not "Lord"); (4) interior punctuation matches AND kjv_strict.verify_span
    agrees; (5) the span appears word for word in the narration; (6) every character line of
    narration-tagged.md is covered by a span. Never overridable."""
    from pipeline import kjv_strict
    fails = []
    narr = [w for w, _ in _words_core(" ".join(ln for ln in narration_text.splitlines()
                                              if not ln.lstrip().startswith("#")))]
    for i, sp in enumerate(spans or []):
        t, ref = str(sp.get("text", "")), sp.get("ref")
        tag = f"span {i + 1} ({ref})"
        if _ELLIPSIS.search(t):
            fails.append(f"{tag}: ellipsis (...) is not allowed, quote one continuous run")
            continue
        try:
            found, why = kjv_run_found(str(ref), t)
        except Exception as e:
            fails.append(f"{tag}: KJV corpus unavailable ({e}) -- fail closed")
            continue
        if not found:
            fails.append(f"{tag}: {why}: {t[:60]!r}")
            continue
        status, why2 = kjv_strict.verify_span(ref, t)
        if status != "OK":
            fails.append(f"{tag}: verify_span {status}: {why2}")
        words = [w for w, _ in _words_core(t)]
        if not any(narr[s:s + len(words)] == words for s in range(len(narr) - len(words) + 1)):
            fails.append(f"{tag}: not found word for word in narration.md")
    span_words = [[w for w, _ in _words_core(str(s.get("text", "")))] for s in spans or []]
    for sp_name, text in tagged_chunks:
        if sp_name == "narrator":
            continue
        words = [w for w, _ in _words_core(text)]
        if not words:
            continue
        if not any(sw[k:k + len(words)] == words for sw in span_words for k in range(len(sw) - len(words) + 1)):
            fails.append(f"character line by {sp_name!r} is not covered by a KJV span: {text[:60]!r}")
    if fails:
        return [_g("SWS-G1k", "FAIL", "; ".join(fails), "quote one continuous KJV run, exactly (never overridable)")]
    return [_g("SWS-G1k", "PASS", f"{len(spans or [])} KJV span(s): continuous whole-word case-sensitive runs")]


def run_narration_gate(narration_md: Path) -> list[GateResult]:
    """SWS-G1g: REPO\\narration_gate.py (hook + landing)."""
    import io
    import contextlib
    import narration_gate
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        rc = narration_gate.gate(Path(narration_md))
    text = buf.getvalue().strip().replace("\n", " | ")[:300]
    return [_g("SWS-G1g", "FAIL" if rc else "PASS", text if rc else "hook + landing earned")]


# ============================================================ PAGE LINTS (G4..G8) ===
_PLAIN = re.compile(r"^[A-Za-z' ,.?!]+$")
_REFRE = re.compile(r"^(?:[1-3] )?[A-Za-z]+(?: [A-Za-z]+)* \d{1,3}:\d{1,3}(?:-\d{1,3})?$")


def _nwords(s: str) -> int:
    return len(str(s).split())


def _text_problems(s: str) -> list[str]:
    bad = []
    if not _PLAIN.match(s or ""):
        chars = sorted({c for c in (s or "") if not re.match(r"[A-Za-z' ,.?!]", c)})
        bad.append(f"banned characters {chars} in {s!r}")
    if ".." in (s or ""):
        bad.append(f"ellipsis in {s!r}")
    return bad


def _run_pos(unit_tokens: list[str], phrase_tokens: list[str], start: int = 0) -> int:
    n = len(phrase_tokens)
    if not n:
        return -1
    for s in range(start, len(unit_tokens) - n + 1):
        if unit_tokens[s:s + n] == phrase_tokens:
            return s
    return -1


def lint_baked_text(pages: dict, covers: dict | None = None, units: dict[str, str] | None = None) -> list[GateResult]:
    """SWS-G4 (section 2). Per page: `SEQ:` title 2-3 words (same on all pages); F01..F06; 3 labels
    1-2 words (one may be 3), 6 words or fewer in total, each found in THIS unit's spoken line in
    spoken order, all different; ONE caption 2-5 words, 28 characters or fewer, a continuous run of
    this unit's spoken words; labels + caption 11 words or fewer; no string twice; no label equal to
    or inside the caption; no corner NOTE; letters, space, apostrophe, comma, full stop, ? ! only."""
    fails = []
    titles = {p.seq_title.strip().lower() for p in pages.values()}
    if len(titles) > 1:
        fails.append(f"the SEQ title must be the same on all pages: {sorted(titles)}")
    for pid, p in pages.items():
        t = f"[{pid}]"
        fails += [f"{t} title: {m}" for m in _text_problems(p.seq_title)]
        if not 2 <= _nwords(p.seq_title) <= 3:
            fails.append(f"{t} title {p.seq_title!r} must be 2-3 words")
        if not re.fullmatch(r"F0[1-6]", p.frame_label) or p.frame_label != pid.upper():
            fails.append(f"{t} frame label {p.frame_label!r} must be {pid.upper()}")
        labels = [x.label for x in p.panels]
        if len(labels) != 3:
            fails.append(f"{t} needs exactly 3 panel labels")
        for lab in labels:
            fails += [f"{t} label: {m}" for m in _text_problems(lab)]
            if not 1 <= _nwords(lab) <= 3:
                fails.append(f"{t} label {lab!r} must be 1-2 words (one may be 3)")
        if sum(1 for lab in labels if _nwords(lab) == 3) > 1:
            fails.append(f"{t} only one label may have 3 words")
        if sum(_nwords(lab) for lab in labels) > 6:
            fails.append(f"{t} the 3 labels have more than 6 words in total")
        if len({l.strip().lower() for l in labels}) != len(labels):
            fails.append(f"{t} the 3 panel labels must all be different: {labels}")
        if len(p.caption_lines) != 1:
            fails.append(f"{t} needs exactly ONE caption line, has {len(p.caption_lines)}")
        cap = p.caption_lines[0] if p.caption_lines else ""
        for c in p.caption_lines:
            fails += [f"{t} caption: {m}" for m in _text_problems(c)]
            if not 2 <= _nwords(c) <= 5:
                fails.append(f"{t} caption {c!r} must be 2-5 words")
            if len(c) > 28:
                fails.append(f"{t} caption {c!r} is {len(c)} characters (max 28, one line)")
        if sum(_nwords(lab) for lab in labels) + _nwords(cap) > 11:
            fails.append(f"{t} labels + caption have more than 11 words ({sum(_nwords(l) for l in labels) + _nwords(cap)})")
        strings = [s.strip().lower() for s in labels + [cap]]
        if len(set(strings)) != len(strings):
            fails.append(f"{t} a string appears twice on the page")
        ct = norm_tokens(cap)
        for lab in labels:
            lt = norm_tokens(lab)
            if lt and (lt == ct or _run_pos(ct, lt) >= 0):
                fails.append(f"{t} label {lab!r} equals or sits inside the caption")
        if p.corner_note:
            fails.append(f"{t} the corner NOTE is gone: corner_note must be empty")
        if units is not None:
            ut = norm_tokens(units.get(pid, ""))
            if not ut:
                fails.append(f"{t} has no spoken line in units.json")
            else:
                if ct and _run_pos(ut, ct) < 0:
                    fails.append(f"{t} caption {cap!r} is not a continuous run of this unit's spoken words")
                at = 0
                for lab in labels:
                    pos = _run_pos(ut, norm_tokens(lab), at)
                    if pos < 0:
                        fails.append(f"{t} label {lab!r} is not found in this unit's spoken line, in spoken order")
                        break
                    at = pos + 1
    hook = norm_tokens((units or {}).get("front", ""))
    for side, c in (covers or {}).items():
        t = f"[{side}]"
        fails += [f"{t} title: {m}" for m in _text_problems(c.title)]
        if not 2 <= _nwords(c.title) <= 3:
            fails.append(f"{t} title {c.title!r} must be 2-3 words")
        if side == "front" and hook and not ({w for w in norm_tokens(c.title) if len(w) >= 4} & set(hook)):
            fails.append(f"{t} title {c.title!r} must carry a key word of the hook")
        if not _REFRE.match((c.subtitle or "").strip()):
            fails.append(f"{t} subtitle {c.subtitle!r} must be ONE Scripture reference (e.g. John 1:19-29)")
    if fails:
        return [_g("SWS-G4", "FAIL", "; ".join(fails), "fix the authored text (design section 2)")]
    return [_g("SWS-G4", "PASS", f"{len(pages)} pages + {len(covers or {})} covers: baked text clean")]


_MOTIF_NOUNS = r"thread|cord|ribbon|drip|drop|bloom|flower|petal|ring|loop|pool|puddle|glow|sparkle"
_STILL_BANNED = [
    (r"\b[A-Z]{2,}\b", "ALL-CAPS word"),
    (r"\d", "digit"),
    (r"\b(check|confirm|ensure|verify)\w*\b|\bmake sure\b", "verification verb"),
    (r"\bStage\s*\d", "'Stage N'"),
    (rf"\b({_MOTIF_NOUNS})s?\b", "banned motif noun"),
]
_CLIP_MOTIF = r"\b(ink|blue|gold|golden|stain|stains|swirl|swirls|brushstroke|motif)\b"
_SPEECH = (r"\b(say|says|said|saying|speak|speaks|speaking|spoke|spoken|talk\w*|whisper\w*|shout\w*|"
           r"call|calls|called|calling|cry|cries|cried|crying|answer\w*|repl(?:y|ies|ied|ying)|preach\w*|"
           r"proclaim\w*|announc\w*|exclaim\w*|pray|prays|prayed|praying|murmur\w*|sing|sings|singing|sang|"
           r"lips?|mouths?|voices?|ask|asks|asked|asking|tell|tells|told)\b")
_NEGATIVES = r"\b(no|not|never|without|nothing|neither|nor|none)\b|n't\b"


def _page_still_fields(p) -> list[tuple[str, str]]:
    f = [("still_shot_type", p.still_shot_type), ("main_scene_still", p.main_scene_still),
         ("material_closer", p.material_closer)]
    f += [(f"panel{i + 1}.content", x.content) for i, x in enumerate(p.panels)]
    return f


def lint_still_prose(pages: dict, covers: dict | None = None) -> list[GateResult]:
    """SWS-G5: authored still fields only (the locked still text is exempt)."""
    fails = []
    items = [(pid, f) for pid, p in pages.items() for f in _page_still_fields(p)]
    items += [(side, f) for side, c in (covers or {}).items() for f in (("scene", c.scene), ("lighting", c.lighting))]
    for pid, (name, text) in items:
        for pat, what in _STILL_BANNED:
            m = re.search(pat, text or "")
            if m:
                fails.append(f"[{pid}].{name}: {what} ({m.group(0)!r})")
    if fails:
        return [_g("SWS-G5", "FAIL", "; ".join(fails), "reword the authored field")]
    return [_g("SWS-G5", "PASS", "authored still prose clean")]


def lint_clip_prose(pages: dict, covers: dict | None = None) -> list[GateResult]:
    """SWS-G5a: clip prose never names the motif / ink / blue / gold / stain, has no speech verb,
    at most 2 negatives, no fence, bubble clause off."""
    fails, items = [], []
    for pid, p in pages.items():
        if p.fence_kind != "none":
            fails.append(f"[{pid}] fence_kind must be 'none'")
        if p.include_no_bubble_clause:
            fails.append(f"[{pid}] include_no_bubble_clause must be False")
        items += [(pid, "anim_shot_desc", p.anim_shot_desc), (pid, "main_scene_animation", p.main_scene_animation)]
        items += [(pid, f"panel_motions[{i}]", m) for i, m in enumerate(p.panel_motions)]
    items += [(side, "animation", c.animation) for side, c in (covers or {}).items()]
    for pid, name, text in items:
        for pat, what in ((_CLIP_MOTIF, "motif/ink word"), (_SPEECH, "speech verb")):
            m = re.search(pat, text or "", re.I)
            if m:
                fails.append(f"[{pid}].{name}: {what} ({m.group(0)!r})")
    for pid in {i[0] for i in items}:
        joined = " ".join(t for p_, _, t in items if p_ == pid)
        n = len(re.findall(_NEGATIVES, joined, re.I))
        if n > 2:
            fails.append(f"[{pid}] {n} negatives in clip prose (max 2)")
    if fails:
        return [_g("SWS-G5a", "FAIL", "; ".join(fails), "reword the motion; remove, do not forbid")]
    return [_g("SWS-G5a", "PASS", "clip prose clean")]


# ---- page_plan.json: ONE schema, validated on load, any missing field = FAIL ---
PLAN_FIELDS = {"full_figures": int, "crowd": bool, "motion_carrier": str, "motif_stage": int, "subjects": list}


def validate_page_plan(doc) -> list[str]:
    """{ "north_star": "f04", "units": { tag: {full_figures:int, crowd:bool, motion_carrier:str,
    motif_stage:0-3, subjects:[names]} } }. Returns the problems (empty = valid)."""
    if not isinstance(doc, dict):
        return ["page_plan.json is not an object"]
    bad = []
    units = doc.get("units")
    if not isinstance(doc.get("north_star"), str):
        bad.append("missing north_star")
    if not isinstance(units, dict) or not units:
        return bad + ["missing units"]
    if isinstance(doc.get("north_star"), str) and doc["north_star"] not in units:
        bad.append(f"north_star {doc['north_star']!r} is not a unit")
    for tag, u in units.items():
        if not isinstance(u, dict):
            bad.append(f"{tag}: not an object")
            continue
        for k, typ in PLAN_FIELDS.items():
            if k not in u:
                bad.append(f"{tag}: missing {k}")
            elif not isinstance(u[k], typ) or (typ is int and isinstance(u[k], bool)):
                bad.append(f"{tag}: {k} must be {typ.__name__}")
        if isinstance(u.get("motif_stage"), int) and not 0 <= u["motif_stage"] <= 3:
            bad.append(f"{tag}: motif_stage must be 0-3")
        if isinstance(u.get("subjects"), list) and not all(isinstance(s, str) for s in u["subjects"]):
            bad.append(f"{tag}: subjects must be names")
    return bad


def load_page_plan(episode_dir: Path) -> tuple[dict | None, list[GateResult]]:
    p = Path(episode_dir) / "page_plan.json"
    if not p.exists():
        return None, [_g("SWS-PLAN", "FAIL", "page_plan.json missing", "write page_plan.json")]
    try:
        doc = json.loads(p.read_text(encoding="utf-8"))
    except Exception as e:
        return None, [_g("SWS-PLAN", "FAIL", f"page_plan.json unreadable ({e})")]
    bad = validate_page_plan(doc)
    if bad:
        return None, [_g("SWS-PLAN", "FAIL", "; ".join(bad), "fix page_plan.json (one schema, design step 3)")]
    return doc, [_g("SWS-PLAN", "PASS", f"{len(doc['units'])} units, north star {doc['north_star']}")]


def lint_dosage(plan: dict | None, pages: dict | None = None) -> list[GateResult]:
    """SWS-G6: motif dosage 0,0,1,1,2,2,3,3 (front..back); wording matches stage 0 vs 1-3."""
    if not plan:
        return [_g("SWS-G6", "FAIL", "page plan missing or invalid", "write page_plan.json")]
    fails = []
    for tag, want in MOTIF_STAGE.items():
        got = (plan.get("units", {}).get(tag) or {}).get("motif_stage")
        if got != want:
            fails.append(f"{tag} motif_stage {got!r} != {want}")
    for pid, p in (pages or {}).items():
        stage, closer = MOTIF_STAGE.get(pid), p.material_closer.lower()
        if stage == 0 and "no unusual ink" not in closer:
            fails.append(f"[{pid}] stage 0 closer must say the page carries no unusual ink")
        if stage and "one brushstroke of blue ink" not in closer:
            fails.append(f"[{pid}] stage {stage} closer must name the one brushstroke of blue ink")
    if fails:
        return [_g("SWS-G6", "FAIL", "; ".join(fails), "fix motif_stage / material_closer")]
    return [_g("SWS-G6", "PASS", "dosage 0,0,1,1,2,2,3,3")]


def load_refs(refs_json: Path) -> list[dict]:
    if not Path(refs_json).exists():
        return []
    raw = json.loads(Path(refs_json).read_text(encoding="utf-8"))
    items = raw.get("refs", []) if isinstance(raw, dict) else raw
    return [i if isinstance(i, dict) else {"name": str(i)} for i in items]


def _ref_name(r: dict) -> str:
    return str(r.get("name") or r.get("subject") or "").strip().lower()


def lint_refs_declared(plan: dict | None, refs_json: Path) -> list[GateResult]:
    """SWS-G7a: every subject on 2+ units is declared in refs/refs.json."""
    if not plan:
        return [_g("SWS-G7a", "FAIL", "page plan missing or invalid")]
    declared = {_ref_name(r) for r in load_refs(refs_json)}
    seen: dict[str, int] = {}
    for u in plan["units"].values():
        for s in {str(x).strip().lower() for x in u["subjects"]}:
            seen[s] = seen.get(s, 0) + 1
    missing = sorted(s for s, n in seen.items() if n >= 2 and s not in declared)
    if missing:
        return [_g("SWS-G7a", "FAIL", f"subjects on 2+ units with no declared ref: {missing}", "add them to refs/refs.json")]
    return [_g("SWS-G7a", "PASS", f"{sum(1 for n in seen.values() if n >= 2)} recurring subject(s), all declared")]


def lint_refs_files(ep_dir: Path) -> list[GateResult]:
    """SWS-G7b: every declared ref file exists (and its sha256 matches when declared)."""
    d = Path(ep_dir)
    bad = []
    for r in load_refs(d / "refs" / "refs.json"):
        f = d / "refs" / str(r.get("file", "")) if r.get("file") else None
        if f is None or not f.is_file():
            bad.append(f"{r.get('name')}: file missing")
        elif r.get("sha256") and r["sha256"] != sha256_of(f):
            bad.append(f"{r.get('name')}: sha256 differs from refs.json")
    if bad:
        return [_g("SWS-G7b", "FAIL", "; ".join(bad), "re-crop the ref / fix refs.json")]
    return [_g("SWS-G7b", "PASS", "every declared ref file exists")]


def lint_refs_sent(ep_dir: Path, plan: dict | None) -> list[GateResult]:
    """SWS-G7c: each still's request carried the ref hashes for that unit's subjects."""
    if not plan:
        return [_g("SWS-G7c", "FAIL", "page plan missing or invalid")]
    all_refs = load_refs(Path(ep_dir) / "refs" / "refs.json")
    refs = {_ref_name(r): r.get("sha256") for r in all_refs}
    source = {_ref_name(r): r.get("from_still") for r in all_refs}      # the page a ref was cropped FROM
    bad = []
    for tag, u in plan["units"].items():
        row = guard.confirmed_row(ep_dir, "still", tag)
        if row is None:
            continue
        sent = {k.strip().lower(): v for k, v in (row.get("ref_sha256") or {}).items()}
        for s in u["subjects"]:
            want = refs.get(s.strip().lower())
            if source.get(s.strip().lower()) == tag:
                continue                         # the north-star page is where the ref comes from
            if want and sent.get(s.strip().lower()) != want:
                bad.append(f"{tag}: ref {s!r} was not sent (or a different file was sent)")
    if bad:
        return [_g("SWS-G7c", "FAIL", "; ".join(bad), "re-render the still with the declared ref attached")]
    return [_g("SWS-G7c", "PASS", "declared refs were sent with each still")]


def lint_motion_carrier(plan: dict | None, speakers: dict[str, str], north_star: str | None = None) -> list[GateResult]:
    """SWS-G8: the speaker (DERIVED from the tagged file) holds still, so something else must carry
    the motion. FAIL on the north-star page, FAIL if more than one page, else WARN."""
    if not plan:
        return [_g("SWS-G8", "FAIL", "page plan missing or invalid")]
    ns = north_star or plan.get("north_star")
    only = []
    for tag, u in plan["units"].items():
        sp = (speakers.get(tag) or "").strip().lower()
        if not sp:
            continue
        carrier = u["motion_carrier"].strip().lower()
        if carrier in ("", "speaker", sp):
            only.append(tag)
    if ns in only:
        return [_g("SWS-G8", "FAIL", f"the north-star page {ns} has only its speaker to move",
                   "give a second figure or a prop the motion")]
    if len(only) > 1:
        return [_g("SWS-G8", "FAIL", f"{len(only)} pages have only the speaker to move: {only}")]
    if only:
        return [_g("SWS-G8", "CONDITIONAL", f"page {only[0]} has only the speaker to move")]
    return [_g("SWS-G8", "PASS", "every speaking page has a motion carrier")]


def lint_order(lists: dict[str, list[str]]) -> list[GateResult]:
    """SWS-G8t: the same tags in the same order in MANIFEST.units, units.json, unit_timing.json,
    page_plan.json."""
    ref_name, ref = next(iter(lists.items()))
    bad = [f"{n}: {l}" for n, l in lists.items() if l != ref]
    if bad:
        return [_g("SWS-G8t", "FAIL", f"unit order/tags differ from {ref_name} {ref}: " + "; ".join(bad))]
    return [_g("SWS-G8t", "PASS", f"{len(lists)} files list the same {len(ref)} tags in the same order")]


# ================================================================== QUOTES ===
def quote_pictures(doc: dict) -> dict:
    """8 stills + ~2 ref renders (about) ; planned: 1 more ref + 8 rerolls."""
    n = len(doc["units"])
    return {"about": STILL_CR * (n + 2), "planned_rerolls": STILL_CR * (1 + n),
            "items": {"stills": n, "refs_expected": 2, "refs_max": 3, "rerolls_planned": n, "cr_each": STILL_CR}}


def quote_clips(doc: dict) -> dict:
    cds = {t: int(u["clip_duration"]) for t, u in doc["units"].items()}
    tags = list(cds)
    back = cds[tags[-1]]
    page_max = max(v for t, v in cds.items() if t != tags[-1])
    return {"about": KLING_CR_PER_SECOND * sum(cds.values()),
            "planned_rerolls": KLING_CR_PER_SECOND * (back + 2 * page_max),
            "items": {"clip_seconds": sum(cds.values()), "rerolls_planned": "back x1, pages x2",
                      "cr_per_second": KLING_CR_PER_SECOND}}


# ================================================================== CLIPS ===
def _probe(mp4: Path) -> dict:
    r = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries",
                        "stream=width,height,r_frame_rate,nb_frames", "-show_entries", "format=duration",
                        "-of", "json", str(mp4)], capture_output=True, text=True)
    if r.returncode != 0:
        raise RuntimeError(r.stderr.strip() or "ffprobe failed")
    d = json.loads(r.stdout)
    s = d["streams"][0]
    num, _, den = str(s.get("r_frame_rate", "0/1")).partition("/")
    fps = float(num) / float(den or 1) if float(den or 1) else 0.0
    nb = int(s["nb_frames"]) if str(s.get("nb_frames", "")).isdigit() else None
    return {"w": int(s["width"]), "h": int(s["height"]), "dur": float(d["format"]["duration"]),
            "fps": fps, "frames": nb}


def clip_tech(mp4: Path, slot: float, min_size: tuple[int, int] = MIN_CLIP_SIZE) -> GateResult:
    """SWS-G11: decodes, at least slot + 0.10 s, at least 1072 x 1900; fps recorded (not 30 = WARN)."""
    try:
        pr = _probe(Path(mp4))
    except Exception as e:
        return _g("SWS-G11", "FAIL", f"{Path(mp4).name} does not decode: {e}")
    bad = []
    if pr["dur"] < slot + 0.1:
        bad.append(f"length {pr['dur']:.2f}s < slot {slot:.2f}s + 0.1")
    if pr["w"] < min_size[0] or pr["h"] < min_size[1]:
        bad.append(f"size {pr['w']}x{pr['h']} < {min_size[0]}x{min_size[1]}")
    if bad:
        return _g("SWS-G11", "FAIL", f"{Path(mp4).name}: " + "; ".join(bad), "re-render longer / at pro size")
    ev = f"{Path(mp4).name}: {pr['w']}x{pr['h']}, {pr['dur']:.2f}s, {pr['fps']:.2f} fps"
    if abs(pr["fps"] - FPS) > 0.01:
        return _g("SWS-G11", "CONDITIONAL", ev + f" (fps is not {FPS}: scaled to {FPS} in the cut)")
    return _g("SWS-G11", "PASS", ev)


def lint_clip_provenance(ep_dir: Path, manifest_units: list, ids: list[str] | None = None) -> list[GateResult]:
    """SWS-G14 (never overridable): for EACH MANIFEST.units[*].src: it is the canonical clip path,
    its sha256 = the confirmed spend row's output_sha256, and that row's input_sha256 = the current still."""
    d = Path(ep_dir)
    bad = []
    for u in manifest_units:
        tag = u.tag
        canon = guard.clip_path(d, tag)
        if Path(u.src).resolve() != canon.resolve():
            bad.append(f"{tag}: Unit.src {Path(u.src).name} is not the canonical clip {canon.name}")
            continue
        row = guard.confirmed_row(d, "anim", tag)
        still = guard.png_path(d, tag)
        if row is None:
            bad.append(f"{tag}: no confirmed spend row for this clip")
        elif not canon.is_file() or sha256_of(canon) != row.get("output_sha256"):
            bad.append(f"{tag}: the clip file is not the one the confirmed row produced")
        elif not still.is_file() or row.get("input_sha256") != sha256_of(still):
            bad.append(f"{tag}: the still changed since this clip was rendered (stale clip)")
    if bad:
        return [_g("SWS-G14", "FAIL", "; ".join(bad), "re-render the clip from the current still (never overridable)")]
    return [_g("SWS-G14", "PASS", f"{len(manifest_units)} clips: canonical path, receipt hash, current still")]


def lint_still_provenance(ep_dir: Path, ids: list[str], refs_json: Path | None = None) -> list[GateResult]:
    """SWS-G14s: every still PNG equals the output_sha256 of a confirmed spend row; a ref PNG is
    either such a render or a crop whose declared source still is. No file copied in from elsewhere."""
    d = Path(ep_dir)
    log = guard.read_log(d)
    outs = {r.get("output_sha256") for r in log.values() if r.get("status") == "confirmed"}
    bad = []
    for t in ids:
        p = guard.png_path(d, t)
        if p.is_file() and sha256_of(p) not in outs:
            bad.append(f"{t}: {p.name} has no confirmed spend receipt (copied in?)")
    for r in load_refs(refs_json or d / "refs" / "refs.json"):
        f = d / "refs" / str(r.get("file", ""))
        if not f.is_file():
            continue
        src = r.get("from_still")
        if src:
            sp = guard.png_path(d, src)
            if not (sp.is_file() and sha256_of(sp) in outs):
                bad.append(f"ref {r.get('name')}: its source still {src!r} has no receipt")
        elif sha256_of(f) not in outs:
            bad.append(f"ref {r.get('name')}: no confirmed receipt and no from_still")
    if bad:
        return [_g("SWS-G14s", "FAIL", "; ".join(bad), "reroll through the guarded bridge; no hand fixes (never overridable)")]
    return [_g("SWS-G14s", "PASS", "every still/ref has a spend receipt")]


# ---- G15h: the moving hold ---------------------------------------------------
def _gray_frames(mp4: Path, ss: float, dur: float, fps: float) -> list:
    import numpy as np
    r = subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{ss:.3f}", "-t", f"{dur:.3f}", "-i", str(mp4),
                        "-vf", f"fps={fps},scale=54:96,format=gray", "-f", "rawvideo", "-"],
                       capture_output=True, check=True)
    a = np.frombuffer(r.stdout, dtype=np.uint8).astype(float)
    n = a.size // (54 * 96)
    return [a[i * 5184:(i + 1) * 5184] for i in range(n)]


def hold_window_diffs(mp4: Path, hold_start: float, hold_len: float = 3.0) -> list[float]:
    """Mean frame difference (0-255) in each 1 s window of the hold: pairs 0.5 s apart."""
    import numpy as np
    fr = _gray_frames(mp4, hold_start, hold_len, 2)
    last = _gray_frames(mp4, max(hold_start + hold_len - 0.1, 0), 0.1, 10)
    if last:
        fr = fr[:int(hold_len * 2)] + [last[-1]]
    d = [float(np.abs(a - b).mean()) for a, b in zip(fr, fr[1:])]
    wins = []
    for w in range(int(round(hold_len))):
        seg = d[2 * w:2 * w + 2]
        wins.append(sum(seg) / len(seg) if seg else 0.0)
    return wins


def frozen_control(mp4: Path, hold_start: float, work: Path, hold_len: float = 3.0) -> Path:
    """Take the last used frame, hold it `hold_len` s, encode it through the same chain."""
    work = Path(work)
    work.mkdir(parents=True, exist_ok=True)
    frame = work / "_hold_last.png"
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-ss", f"{max(hold_start - 0.04, 0):.3f}", "-i", str(mp4),
                    "-frames:v", "1", str(frame)], check=True)
    out = work / "_hold_control.mp4"
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-loop", "1", "-framerate", str(FPS), "-i", str(frame),
                    "-t", f"{hold_len:.3f}", "-r", str(FPS), "-c:v", "libx264", "-crf", "18", "-preset", "medium",
                    "-pix_fmt", "yuv420p", str(out)], check=True)
    return out


def moving_hold(mp4: Path, hold_start: float, work: Path, k: float | None = None, hold_len: float = 3.0,
                abs_floor: float | None = None, gate: str = "SWS-G15h") -> GateResult:
    """SWS-G15h: noise floor N from a frozen control of the same last frame; every 1 s window of the
    hold must be at least max(k x N, absolute floor). One window under = FAIL (motion that stops half
    way fails; a clip frozen from frame 0 fails). Measured on the clip, the draft and the final file."""
    k = HOLD_K if k is None else k
    floor = HOLD_ABS_FLOOR if abs_floor is None else abs_floor
    ctl = frozen_control(mp4, hold_start, work, hold_len)
    n_floor = max(hold_window_diffs(ctl, 0.0, hold_len))
    need = max(k * n_floor, floor)
    wins = hold_window_diffs(mp4, hold_start, hold_len)
    low = [i for i, w in enumerate(wins) if w < need]
    ev = f"{Path(mp4).name}: windows {[round(w, 2) for w in wins]} vs floor {need:.2f} (N={n_floor:.2f}, k={k})"
    if low:
        return _g(gate, "FAIL", ev + f"; window(s) {low} under the floor: the hold stops moving",
                  "re-render the back clip with motion that runs to the last second")
    return _g(gate, "PASS", ev)


def still_stretch(mp4: Path, start: float, end: float, work: Path, is_north_star: bool = False) -> GateResult:
    """SWS-G12: the G15h floor applied to every 1 s window of a clip's used span: WARN (FAIL on the
    north-star page)."""
    ctl = frozen_control(mp4, end, work, 1.0)
    n_floor = max(hold_window_diffs(ctl, 0.0, 1.0)[:1] or [0.0])
    need = max(HOLD_K * n_floor, HOLD_ABS_FLOOR)
    low, t = [], start
    while t + 1.0 <= end + 1e-6:
        w = hold_window_diffs(mp4, t, 1.0)[0]
        if w < need:
            low.append(round(t, 1))
        t += 1.0
    if low:
        return _g("SWS-G12", "FAIL" if is_north_star else "CONDITIONAL",
                  f"{Path(mp4).name}: still stretch(es) starting at {low} s")
    return _g("SWS-G12", "PASS", f"{Path(mp4).name}: no still stretch")


# ---- G13: eyes -----------------------------------------------------------------
STRIP_TILE_W = 540
STRIP_TILES = 6


def strip_times(span_s: float, fps_samples: float = 2.0) -> list[float]:
    """2 frames per second of the used span, plus the true last frame."""
    n = int(math.floor(span_s * fps_samples + 1e-9))
    ts = [i / fps_samples for i in range(n + 1) if i / fps_samples < span_s - 1e-6]
    ts.append(max(span_s - 1.0 / FPS, 0.0))
    return ts


def make_strips(mp4: Path, span_s: float, out_dir: Path) -> tuple[list[Path], list[float]]:
    """Frames at 2 per second of the used span, each 540 px wide, 6 per strip image."""
    from PIL import Image
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    times = strip_times(span_s)
    tiles = []
    for i, t in enumerate(times):
        f = out_dir / f"_tile_{i:03d}.jpg"
        subprocess.run(["ffmpeg", "-y", "-v", "error", "-ss", f"{t:.3f}", "-i", str(mp4), "-frames:v", "1",
                        "-vf", f"scale={STRIP_TILE_W}:-2", "-q:v", "3", str(f)], check=True)
        tiles.append(f)
    strips = []
    for s in range(0, len(tiles), STRIP_TILES):
        grp = [Image.open(t) for t in tiles[s:s + STRIP_TILES]]
        w, h = STRIP_TILE_W * len(grp), max(i.height for i in grp)
        canvas = Image.new("RGB", (w, h), "white")
        for j, im in enumerate(grp):
            canvas.paste(im, (j * STRIP_TILE_W, 0))
        p = out_dir / f"{Path(mp4).stem}_strip{s // STRIP_TILES + 1}.jpg"
        canvas.save(p, quality=90)
        strips.append(p)
    for t in tiles:
        t.unlink()
    return strips, times


def judge_eyes(reads: list[dict], plan_unit: dict, expected: list[str]) -> list[GateResult]:
    """SWS-G13 judge over the Vision READS of the strips (one dict per strip: bubble, new_text,
    ink_changed, still_thing_moving, bare_skin, mouth_changed, drift, frames:[{texts_seen,
    full_figures}]). Hard flags FAIL: speech bubble; new legible text; a planned baked string
    missing or changed on the first, middle or last frame; figure count change; ink_changed; a
    figure/prop the plan says is still, moving; bare-skin doubt. Soft (WARN): mouth, drift."""
    import swirls_verify as sv
    hard, soft = [], []
    frames = [f for r in reads for f in r.get("frames", [])]
    for key, what in (("speech_bubble", "speech bubble"), ("new_text", "new legible text"),
                      ("ink_changed", "ink_changed (the motif grew, glowed or moved)"),
                      ("still_thing_moving", "a figure or prop the plan says is still, moves"),
                      ("bare_skin", "bare-skin doubt on a figure")):
        if any(r.get(key) for r in reads):
            hard.append(what)
    if frames:
        picks = {0: "first", len(frames) // 2: "middle", len(frames) - 1: "last"}
        for idx, name in picks.items():
            f = frames[idx]
            if expected and f.get("texts_seen") is not None:
                res = sv.judge_still_raw(expected, {"texts_seen": f["texts_seen"], "full_figures": f.get("full_figures"),
                                                    "crowd": False, "motif_marks": None}, plan_unit, texts_only=True)
                bad = [g for g in res if g.verdict == "FAIL"]
                if bad:
                    hard.append(f"baked text on the {name} frame: {bad[0].evidence}")
        figs = {f.get("full_figures") for f in frames if f.get("full_figures") is not None}
        if len(figs) > 1:
            hard.append(f"full-figure count changes during the clip: {sorted(figs)}")
    for key, what in (("mouth_changed", "a mouth looks different between frames"), ("drift", "drift")):
        if any(r.get(key) for r in reads):
            soft.append(what)
    out = []
    if hard:
        out.append(_g("SWS-G13", "FAIL", "; ".join(hard), "re-render or reword the motion"))
    if soft:
        out.append(_g("SWS-G13[soft]", "CONDITIONAL", "; ".join(soft), "look at the clip played"))
    if not out:
        out.append(_g("SWS-G13", "PASS", f"{len(reads)} strips read, no hard flag"))
    return out


# ================================================================== STILLS ===
def crop_box(w: int, h: int, frac: float) -> tuple[int, int, int, int]:
    dx, dy = round(w * frac), round(h * frac)
    return dx, dy, w - dx, h - dy


def crop_png(png: Path, frac: float, out: Path) -> Path:
    from PIL import Image
    im = Image.open(png)
    im.crop(crop_box(im.width, im.height, frac)).save(out)
    return out


def edge_scan(png: Path, level: str = "FAIL") -> GateResult:
    """SWS-G10: pixel scan of the four edges. A drawn rule or a blank band. FAIL on covers, WARN on
    pages (level="CONDITIONAL")."""
    import numpy as np
    from PIL import Image
    a = np.asarray(Image.open(png).convert("L"), dtype=float)
    h, w = a.shape
    k = max(4, int(min(h, w) * 0.02))
    sides = {"top": a[:k, :], "bottom": a[h - k:, :], "left": a[:, :k].T, "right": a[:, w - k:].T}
    bad = []
    for name, strip in sides.items():
        if strip.std() < 2.5:
            bad.append(f"{name}: blank band")
        if ((strip < 90).mean(axis=1) > 0.85).any():
            bad.append(f"{name}: drawn rule")
    if bad:
        return _g("SWS-G10", level, f"{Path(png).name}: " + "; ".join(bad),
                  "re-render (no hand crop in the pilot)")
    return _g("SWS-G10", "PASS", f"{Path(png).name}: edges clean")


# ============================================================ FILM (G15, G16, G17) ===
def probe_output(mp4: Path) -> dict:
    return _probe(Path(mp4))


def lint_assembly(receipt: dict, doc: dict, final_mp4: Path, picture_s: float | None = None,
                  audio_s: float | None = None) -> list[GateResult]:
    """SWS-G15: all `trim`; every cut at B(k) within one frame; total frames within one of
    round(total x 30); picture = sound within one frame; output 1080x1920 at 30 fps; no -shortest;
    first word by 0.40 s."""
    bad = []
    pr = _probe(Path(final_mp4))
    if (pr["w"], pr["h"]) != OUT_SIZE:
        bad.append(f"output {pr['w']}x{pr['h']} is not {OUT_SIZE[0]}x{OUT_SIZE[1]}")
    if abs(pr["fps"] - FPS) > 0.01:
        bad.append(f"output fps {pr['fps']:.2f} is not {FPS}")
    if receipt.get("uses_shortest"):
        bad.append("the cut used -shortest")
    if set(receipt.get("modes", ["trim"])) != {"trim"}:
        bad.append("not every unit is `trim`")
    total = float(doc["narration_seconds"]) + OUTRO_HOLD
    want_total = round(total * FPS)
    frames = {u["tag"]: u["frames"] for u in receipt.get("units", [])}
    prev = 0
    for tag, u in doc["units"].items():
        b = round(float(u["end_s"]) * FPS)
        want = b - prev
        prev = b
        if tag not in frames or abs(frames[tag] - want) > 1:
            bad.append(f"{tag}: {frames.get(tag)} frames, expected {want} (cut at B(k)={b})")
    if receipt.get("total_frames") is None or abs(receipt["total_frames"] - want_total) > 1:
        bad.append(f"total frames {receipt.get('total_frames')} vs round(total x 30) = {want_total}")
    if picture_s is not None and audio_s is not None and abs(picture_s - audio_s) > 1.0 / FPS + 1e-6:
        bad.append(f"picture {picture_s:.3f}s and sound {audio_s:.3f}s differ by more than one frame")
    if doc.get("first_word_start_s", 0) > FIRST_WORD_MAX_START:
        bad.append(f"first word at {doc['first_word_start_s']}s")
    if bad:
        return [_g("SWS-G15", "FAIL", "; ".join(bad), "fix the cut")]
    return [_g("SWS-G15", "PASS", f"trim cut: {want_total} frames, {OUT_SIZE[0]}x{OUT_SIZE[1]} at {FPS} fps, cuts on B(k)")]


def write_final_receipt(ep_dir: Path, input_mp4: Path, output_mp4: Path) -> dict:
    rec = {"input_sha256": sha256_of(Path(input_mp4)), "output_sha256": sha256_of(Path(output_mp4)),
           "output": str(output_mp4), "written": datetime.date.today().isoformat()}
    Path(ep_dir, "final_receipt.json").write_text(json.dumps(rec, indent=2), encoding="utf-8")
    return rec


def check_chain(ep_dir: Path) -> list[GateResult]:
    """SWS-G16: final_receipt.json input sha = the scored assembly's output sha; FINAL_VIDEO.txt names
    a file whose sha is the receipt's output sha. Never overridable."""
    d = Path(ep_dir)
    try:
        fr = json.loads((d / "final_receipt.json").read_text(encoding="utf-8"))
        sc = json.loads((d / "assembly_receipt_scored.json").read_text(encoding="utf-8"))
    except Exception as e:
        return [_g("SWS-G16", "FAIL", f"receipt missing/unreadable ({e})")]
    bad = []
    if fr.get("input_sha256") != sc.get("output_sha256"):
        bad.append("final_receipt input is not the scored assembly output")
    fv = d / "FINAL_VIDEO.txt"
    named = None
    if fv.exists():
        for line in fv.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            for cand in (Path(line), d / line):
                if line and cand.is_file():
                    named = cand
                    break
            if named:
                break
    if named is None:
        bad.append("FINAL_VIDEO.txt names no existing file")
    elif sha256_of(named) != fr.get("output_sha256"):
        bad.append("FINAL_VIDEO.txt names a file that is not the receipt's output")
    if bad:
        return [_g("SWS-G16", "FAIL", "; ".join(bad), "rebuild the SFX/final from the scored cut (never overridable)")]
    return [_g("SWS-G16", "PASS", "hash chain: scored assembly -> final -> FINAL_VIDEO.txt")]


def _rms_db_windows(path: Path, win: float = 1.0) -> list[float]:
    import numpy as np
    r = subprocess.run(["ffmpeg", "-v", "error", "-i", str(path), "-ac", "1", "-ar", "8000", "-f", "f32le", "-"],
                       capture_output=True, check=True)
    a = np.frombuffer(r.stdout, dtype=np.float32)
    n = int(8000 * win)
    out = []
    for i in range(0, len(a) - n + 1, n):
        rms = float(np.sqrt(np.mean(a[i:i + n] ** 2)))
        out.append(20 * math.log10(rms) if rms > 1e-9 else -120.0)
    return out


SCORE_FLOOR_DB = -55.0


def score_gate(score_mp3: Path, total: float, mix_mp4: Path | None = None,
               narration_mp3: Path | None = None) -> list[GateResult]:
    """SWS-G17: score length >= total; no 1 s window of the score below the floor from 0 to total
    (dead start / join / hold); music audible in the last 3 s of the MIX; no clipping. FAIL.
    Music 10-16 dB under the voice in speech = WARN (measured)."""
    import numpy as np
    bad = []
    dur = _ffprobe_duration(Path(score_mp3))
    if dur < total - 0.05:
        bad.append(f"score is {dur:.1f}s, shorter than the film {total:.1f}s")
    win = _rms_db_windows(Path(score_mp3))
    dead = [i for i, db in enumerate(win[:int(math.ceil(total))]) if db < SCORE_FLOOR_DB]
    if dead:
        bad.append(f"score is below {SCORE_FLOOR_DB:.0f} dB in 1 s window(s) {dead[:8]}")
    warn = []
    if mix_mp4 is not None:
        mw = _rms_db_windows(Path(mix_mp4))
        tail = mw[-3:] if len(mw) >= 3 else mw
        if any(db < SCORE_FLOOR_DB for db in tail):
            bad.append("no music audible in the last 3 s of the mix")
        r = subprocess.run(["ffmpeg", "-v", "error", "-i", str(mix_mp4), "-ac", "1", "-ar", "8000", "-f", "f32le", "-"],
                           capture_output=True, check=True)
        a = np.frombuffer(r.stdout, dtype=np.float32)
        if a.size and float((np.abs(a) >= 0.999).mean()) > 0.001:
            bad.append("the mix clips")
        if narration_mp3 is not None:
            nw = _rms_db_windows(Path(narration_mp3))
            sw_ = _rms_db_windows(Path(score_mp3))
            speech = [i for i, db in enumerate(nw) if db > -35 and i < len(sw_)]
            if speech:
                gap = sum(nw[i] - sw_[i] for i in speech) / len(speech)
                if not 10 <= gap <= 16:
                    warn.append(f"music is {gap:.0f} dB under the voice in speech (target 10-16)")
    out = []
    if bad:
        out.append(_g("SWS-G17", "FAIL", "; ".join(bad), "regenerate / re-join the score"))
    else:
        out.append(_g("SWS-G17", "PASS", f"score {dur:.1f}s, no dead window, music in the last 3 s of the mix"))
    if warn:
        out.append(_g("SWS-G17[ratio]", "CONDITIONAL", "; ".join(warn)))
    return out


def film_panel_pass(seats: list[dict]) -> tuple[bool, list[str]]:
    """Step 10 pass mark: every seat gets who, what and why right; no Bible-accuracy complaint is
    open; median curiosity score 7 or more. Else NOT PASSED with the 'still weak' list."""
    weak = []
    for i, s in enumerate(seats):
        for k in ("who", "what", "why"):
            if not s.get(k):
                weak.append(f"seat {i + 1} did not get {k}")
        if s.get("bible_complaint_open"):
            weak.append(f"seat {i + 1} has an open Bible-accuracy complaint")
    scores = sorted(float(s.get("curiosity", 0)) for s in seats)
    med = scores[len(scores) // 2] if len(scores) % 2 else (scores[len(scores) // 2 - 1] + scores[len(scores) // 2]) / 2 if scores else 0
    if not seats or med < 7:
        weak.append(f"median curiosity {med} (need 7 or more)")
    return (not weak), weak


# ================================================================== STATUS ===
def open_warns(ep_dir: Path) -> list[str]:
    p = Path(ep_dir) / "_qc" / "open_warns.json"
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except Exception:
        return []


def record_warns(ep_dir: Path, source: str, gates: list) -> None:
    """Open WARNs are listed in plain words on every owner page: WARN never counts as pass."""
    p = Path(ep_dir) / "_qc"
    p.mkdir(exist_ok=True)
    warns = {w.split("|", 1)[0]: w for w in open_warns(ep_dir)}
    for k in [k for k in warns if k == source]:
        del warns[k]
    for g in gates:
        if g.verdict == "CONDITIONAL":
            warns[f"{source}|{g.gate}"] = f"{source}|{g.gate}|{g.evidence}"
    (p / "open_warns.json").write_text(json.dumps(sorted(warns.values()), indent=2), encoding="utf-8")


def status(ep_dir: Path) -> tuple[list[tuple[str, bool, str]], str, dict]:
    """The 12-step file checklist (design section 3). Returns (rows, next_line, spend)."""
    d = Path(ep_dir)
    tags = guard.unit_tags(d) if (d / "unit_timing.json").exists() else []
    gv = lambda g: guard.gate_valid(d, g)  # noqa: E731
    stills = [t for t in tags if guard.png_path(d, t).exists()]
    clips = [t for t in tags if guard.clip_path(d, t).exists()]
    rows = [
        ("0 folder", (d / "_DESIGN_BRIEF.md").exists() and (d / ".swirls_short").exists(),
         "make the folder with _DESIGN_BRIEF.md (line 1 = exact verse range) and the .swirls_short marker"),
        ("1 words", gv("words"), "RUN words, owner page 1, then `ok words`"),
        ("2 voice", gv("voice_ear") and (d / "narration.alignment.meta.json").exists(),
         "ask 1 (voice): quote / approve / voice; owner picks a take (`ok voice_ear --take A|B`); then align"),
        ("3 timing + plan", (d / "unit_timing.json").exists() and (d / "page_plan.json").exists() and (d / "episode.py").exists(),
         "RUN timing, write episode.py + page_plan.json, RUN plan"),
        ("4 north star", gv("northstar_look"), "ask 2 (pictures): still the north-star page; hold; owner page 3; `ok northstar_look`"),
        ("5 stills", bool(tags) and len(stills) == len(tags) and gv("stills_animatic"),
         f"{len(stills)}/{len(tags) or 8} stills; verify, animatic, owner page 4; `ok stills_animatic`"),
        ("6 clips", bool(tags) and len(clips) == len(tags) and gv("clip_test_look"),
         f"{len(clips)}/{len(tags) or 8} clips; ask 3 (clips): 2 test clips, owner page 5, the other 6"),
        ("7 draft film", gv("draft_cut"), "RUN assemble --draft; owner page 6; `ok draft_cut`"),
        ("8 score", (d / "assembly_receipt_scored.json").exists(), "ask 4 (music): quote / approve / score; RUN assemble --score piano"),
        ("9 sfx/srt/final", (d / "final_receipt.json").exists() and (d / "FINAL_VIDEO.txt").exists(),
         "build_sfx.py (from the receipt), cache SRT, FINAL_VIDEO.txt, final receipt"),
        ("10 film panel", gv("film_final"), "film-only blind panel; owner page 7; `ok film_final`. The pilot ends here"),
        ("11 publish", (d / "publish").exists(), "only when the owner asks to post (outside the pilot)"),
    ]
    nxt = next((f"NEXT: step {r[0]} -- {r[2]}" for r in rows if not r[1]), "NEXT: all steps done")
    return rows, nxt, guard.spend_summary(d)


# ---- SWS-G2w: "the audio says the words" ($0, local) ------------------------------
G2W_UNIT_MAX_UNMATCHED = 0.25
G2W_FILM_MAX_UNMATCHED = 0.10


def audio_says_words(units: dict[str, str], heard_text: str) -> list[GateResult]:
    """Forced alignment only echoes the transcript, so it cannot notice STALE audio. Compare what a
    local speech transcriber heard in narration.mp3 with units.json, unit by unit: more than 25 % of
    a unit's words unmatched, or more than 10 % of the film = FAIL (listen, then re-synth that turn).
    KJV words lower a transcriber's score a little; thresholds are set in test T10b."""
    import difflib
    ref, owner = [], []
    for tag, txt in units.items():
        toks = norm_tokens(txt)
        ref += toks
        owner += [tag] * len(toks)
    heard = norm_tokens(heard_text)
    sm = difflib.SequenceMatcher(None, ref, heard, autojunk=False)
    matched = [False] * len(ref)
    for blk in sm.get_matching_blocks():
        for i in range(blk.a, blk.a + blk.size):
            matched[i] = True
    bad = []
    for tag in units:
        idx = [i for i, o in enumerate(owner) if o == tag]
        if idx:
            miss = sum(1 for i in idx if not matched[i]) / len(idx)
            if miss > G2W_UNIT_MAX_UNMATCHED:
                bad.append(f"{tag}: {miss:.0%} of its words not heard")
    film = (sum(1 for m in matched if not m) / len(ref)) if ref else 1.0
    if film > G2W_FILM_MAX_UNMATCHED:
        bad.append(f"film: {film:.0%} of the words not heard")
    if bad:
        return [_g("SWS-G2w", "FAIL", "; ".join(bad), "listen; re-synth that turn (delete _turns for it)")]
    return [_g("SWS-G2w", "PASS", f"audio says the words ({film:.0%} unmatched overall)")]
