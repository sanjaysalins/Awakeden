"""swirls_short_run.py -- the Swirls SHORT commands behind swirls_episode.py (design v3.2 section 3).

Every command is a plain function (`cmd_*`) over an episode folder. Anything that could cost money goes
through swirls_guard (OpenArt: guard_context + the guarded bridge; ElevenLabs: the three fixed
commands voice / align / score). Anything outside the repo (the speech tools, the score script, a
local transcriber, the ElevenLabs aligner) is reached through the small `HOOKS` dict so the $0
dry run (T12) can swap them for fakes without touching the commands.
"""
from __future__ import annotations

import datetime
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import uuid
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE / "test_the_cross"))
sys.path.insert(0, str(ROOT))

import swirls_assemble as sa  # noqa: E402
import swirls_guard as guard  # noqa: E402
import swirls_short as ss  # noqa: E402
import swirls_verify as sv  # noqa: E402

PY = sys.executable
SCORE_NAME = "piano"


# ------------------------------------------------------------------ hooks (real by default) ---
def _run_cmd(cmd: list[str], env: dict | None = None, cwd: Path | None = None) -> int:
    return subprocess.run(cmd, env={**os.environ, **(env or {})}, cwd=cwd).returncode


def _eleven_align(d: Path) -> list[dict]:
    """ElevenLabs forced alignment of narration.mp3 against the tagged transcript (PAID)."""
    from pipeline import assembly_align as aa
    doc = aa._call_elevenlabs(d / "narration.mp3", aa.transcript(d))
    (d / "narration.alignment.json").write_text(json.dumps(doc, ensure_ascii=False, indent=2), encoding="utf-8")
    return [w for w in (doc.get("words") or [])]


def _whisper_text(mp3: Path) -> str:
    """Local, free: what a speech transcriber hears in the audio (no network if the model is cached)."""
    from faster_whisper import WhisperModel
    model = WhisperModel(os.getenv("ASSEMBLY_WHISPER_MODEL", "base"), device="cpu", compute_type="int8")
    segs, _ = model.transcribe(str(mp3), language="en")
    return " ".join(s.text for s in segs)


def _vision_ok() -> bool:
    import config
    return bool(config.agent_mode())


HOOKS = {"run": _run_cmd, "eleven_align": _eleven_align, "whisper": _whisper_text, "vision_ok": _vision_ok,
         "tracker": None}


# --------------------------------------------------------------------------- common helpers ---
def say(msg: str = "") -> None:
    print(msg)


def _report(gates: list, d: Path, unit: str | None = None, file: Path | None = None, source: str = "") -> bool:
    gates = sv.apply_overrides_bound(gates, d, unit, file) if unit else gates
    ok = True
    for g in gates:
        say(f"[{g.verdict:11}] {g.gate}: {g.evidence}" + (f"  FIX: {g.fix}" if g.fix else ""))
        ok = ok and g.verdict != "FAIL"
    if source:
        ss.record_warns(d, source, gates)
    return ok


def require_marker(d: Path) -> bool:
    import openart_bridge as ob
    hit = ob.find_marker(d)
    if hit is None or hit[0].resolve() != Path(d).resolve() or not hit[1].get("episode_id"):
        say("REFUSED: a trim (Swirls short) episode needs its .swirls_short marker (run `init`); "
            "every paid command refuses without it")
        return False
    return True


def cmd_init(d: Path) -> bool:
    """Step 0: folder + marker (random episode_id), the sub-folders, a status line."""
    d = Path(d)
    d.mkdir(parents=True, exist_ok=True)
    m = d / ".swirls_short"
    if not m.exists():
        m.write_text(json.dumps({"episode_id": uuid.uuid4().hex, "created": datetime.date.today().isoformat()}),
                     encoding="utf-8")
    for sub in ("words", "refs", "_qc", "_quotes"):
        (d / sub).mkdir(exist_ok=True)
    say(f"marker ready: {m}")
    return True


def _units(d: Path) -> dict[str, str]:
    return json.loads((d / "units.json").read_text(encoding="utf-8"))


def _doc(d: Path) -> dict:
    return json.loads((d / "unit_timing.json").read_text(encoding="utf-8"))


def _ids(ep) -> list[str]:
    return [u.tag for u in ep.MANIFEST.units]


def _spec(ep, id_: str):
    return ep.PAGES.get(id_) or ep.COVERS.get(id_)


def _plan_unit(d: Path, id_: str) -> dict | None:
    plan, _ = ss.load_page_plan(d)
    return (plan or {}).get("units", {}).get(id_)


def _sha_file(p: Path) -> str | None:
    return guard.sha256_of(p) if Path(p).is_file() else None


# ================================================================================= WORDS ===
def words_gates(d: Path) -> list:
    units = _units(d)
    info = ss.derive_speakers(d, units)
    gates = ss.lint_words(units, {t: v["voiced"] for t, v in info.items()})
    gates += ss.lint_speakers(info)
    spans = json.loads((d / "kjv_spans.json").read_text(encoding="utf-8")) if (d / "kjv_spans.json").exists() else None
    if spans is None:
        gates.append(ss._g("SWS-G1k", "FAIL", "kjv_spans.json missing: every quote needs a {ref, speaker, text} span"))
    else:
        from pipeline.assembly_timing import _parse_tagged_chunks
        gates += ss.lint_kjv(spans, (d / "narration.md").read_text(encoding="utf-8"),
                             _parse_tagged_chunks(d / "narration-tagged.md"))
    try:
        tagged = ss.tagged_transcript_tokens(d)
    except SystemExit as e:
        tagged = None
        gates.append(ss._g("SWS-G1s", "FAIL", str(e)))
    if tagged is not None:
        gates += ss.lint_sequence(units, (d / "narration.md").read_text(encoding="utf-8"), tagged)
    if os.environ.get("SWS_SKIP_NARRATION_GATE") != "1":
        gates += ss.run_narration_gate(d / "narration.md")
    return gates


def cmd_words(d: Path) -> bool:
    return _report(words_gates(d), d)


# ================================================================================= QUOTES ===
def _tagged_chunks(d: Path):
    from pipeline.assembly_timing import _parse_tagged_chunks
    return _parse_tagged_chunks(d / "narration-tagged.md")


def prepare_turns(d: Path) -> bool:
    """If `_turns\\.text_sha256` differs from the current narration-tagged.md hash, DELETE `_turns\\`
    and write the new hash (no prose rule to remember). Returns True when it deleted."""
    d = Path(d)
    sha = guard.sha256_of(d / "narration-tagged.md")
    turns = d / "_turns"
    marker = turns / ".text_sha256"
    deleted = False
    if turns.exists() and (not marker.exists() or marker.read_text(encoding="utf-8").strip() != sha):
        shutil.rmtree(turns)
        deleted = True
    turns.mkdir(exist_ok=True)
    marker.write_text(sha, encoding="utf-8")
    return deleted


def _turn_file(d: Path, idx: int, speaker: str) -> Path:
    return d / "_turns" / f"{idx:02d}_{speaker}.mp3"


def voice_chars(d: Path) -> tuple[int, int]:
    """Characters of the turns that will ACTUALLY be rendered (cached turns cost 0): (narrator, character)."""
    d = Path(d)
    sha = guard.sha256_of(d / "narration-tagged.md")
    marker = d / "_turns" / ".text_sha256"
    stale = not (marker.exists() and marker.read_text(encoding="utf-8").strip() == sha)
    n_narr = n_char = 0
    for i, (sp, text) in enumerate(_tagged_chunks(d)):
        if not stale and _turn_file(d, i, sp).exists():
            continue
        if sp == "narrator":
            n_narr += len(text)
        else:
            n_char += len(text)
    return n_narr, n_char


def cmd_quote(d: Path, step: str, ep=None) -> bool:
    d = Path(d)
    try:
        if step == "voice":
            n, c = voice_chars(d)
            about = round(guard.eleven_price_voice(n, c) + guard.ELEVEN_ALIGN_USD, 4)
            q = guard.write_quote(d, step, about, round(c * guard.ELEVEN_USD_PER_CHAR, 4),
                                  {"narrator_chars": n, "character_chars": c, "passes": "narrator x2, characters x2 takes",
                                   "align_usd": guard.ELEVEN_ALIGN_USD, "rate": guard.ELEVEN_USD_PER_CHAR})
        elif step == "pictures":
            q = guard.write_quote(d, step, **_q(ss.quote_pictures(_doc(d))))
        elif step == "clips":
            q = guard.write_quote(d, step, **_q(ss.quote_clips(_doc(d))))
        elif step == "score":
            secs = float(_doc(d)["narration_seconds"]) + ss.OUTRO_HOLD
            about = round(secs * guard.ELEVEN_SCORE_USD_PER_SECOND, 4)
            q = guard.write_quote(d, step, about, round(about / 2, 4), {"seconds": secs, "parts": 2,
                                                                      "rate": guard.ELEVEN_SCORE_USD_PER_SECOND})
        else:
            say(f"REFUSED: no quote for step {step!r}")
            return False
    except (guard.SpendRefused, FileNotFoundError, KeyError) as e:
        say(f"REFUSED: {e}")
        return False
    sign = "$" if q["cur"] == "usd" else ""
    unit = "" if q["cur"] == "usd" else " cr"
    say(f"{step}: about {sign}{q['about']:g}{unit}, at most {sign}{q['at_most']:g}{unit} -- yes?")
    if q["cur"] == "usd" and not guard.ELEVEN_RATES_VERIFIED:
        say("  (ElevenLabs rates are typed from the invoice and UNVERIFIED until the first receipt)")
    return True


def _q(x: dict) -> dict:
    return {"about": x["about"], "planned_rerolls": x["planned_rerolls"], "items": x["items"]}


def cmd_approve(d: Path, step: str, cap, unit: str, balance, note, unit_id=None, renders=None, price=None) -> bool:
    try:
        g = guard.approve(Path(d), step, cap, unit, note or "", balance, unit_id, renders, price)
    except guard.SpendRefused as e:
        say(f"REFUSED: {e}")
        return False
    say(f"approved {step}: cap {g['cap']:g} {unit}" + (f", unit {unit_id} +{renders} render(s)" if unit_id else ""))
    return True


# =================================================================================== OK ===
def cmd_ok(d: Path, gate: str, note: str, take: str | None = None, ep=None) -> bool:
    d = Path(d)
    extra = None
    try:
        if gate == "words":
            if not _report(words_gates(d), d):
                say("REFUSED: the word gates FAIL")
                return False
        elif gate == "voice_ear":
            if take not in ("A", "B"):
                say("REFUSED: `ok voice_ear --take A|B`")
                return False
            src = d / f"narration_take{take}.mp3"
            if not src.is_file():
                say(f"REFUSED: {src.name} does not exist (run `voice` first)")
                return False
            shutil.copyfile(src, d / "narration.mp3")
            extra = {"take": take}
        elif gate == "northstar_look":
            ns = guard.north_star(d)
            if not ns or not (d / "_qc" / f"hold_{ns}.mp4").is_file():
                say("REFUSED: run `hold <north star>` and look at it on a phone first")
                return False
        elif gate == "stills_animatic":
            if not (d / "_qc" / "animatic.mp4").is_file():
                say("REFUSED: run `animatic` first")
                return False
        elif gate == "clip_test_look":
            ns = guard.north_star(d)
            for t in (ns, "back"):
                q = Path(str(guard.clip_path(d, t)) + ".clipqc.json")
                if not q.is_file() or json.loads(q.read_text(encoding="utf-8")).get("fail"):
                    say(f"REFUSED: clip {t} has no clean clipqc")
                    return False
        elif gate == "draft_cut":
            rc = d / "assembly_receipt.json"
            if not rc.is_file() or json.loads(rc.read_text(encoding="utf-8")).get("kind") != "draft":
                say("REFUSED: no draft assembly receipt")
                return False
        elif gate == "film_final":
            if not _report(ss.check_chain(d), d):
                return False
            fp = d / "_qc" / "film_panel.json"
            if not fp.is_file():
                say("REFUSED: no film panel result (_qc\\film_panel.json)")
                return False
            ok, weak = ss.film_panel_pass(json.loads(fp.read_text(encoding="utf-8")).get("seats", []))
            if not ok:
                say("NOT PASSED. Still weak: " + "; ".join(weak))
                return False
        rec = guard.record_gate(d, gate, note, extra)
    except (guard.SpendRefused, OSError) as e:
        say(f"REFUSED: {e}")
        return False
    say(f"look recorded: {gate} ({len(rec['bindings'])} file hash(es) bound)")
    return True


# ================================================================================ VOICE ===
def _synth(d: Path, stability: float) -> int:
    import config
    return HOOKS["run"]([PY, str(config.PER_TURN_SYNTH_SCRIPT), str(d), "--target", "45", "--natural",
                         "--pre-quote-pause", "0.4", "--stability", str(stability)])


def _turn_files(d: Path, narrator: bool) -> list[Path]:
    out = []
    for f in (d / "_turns").glob("*.mp3"):
        m = re.match(r"^(\d+)_([a-zA-Z]+)(__atempo)?\.mp3$", f.name)
        if m and ((m.group(2).lower() == "narrator") == narrator):
            out.append(f)
    return out


def cmd_voice(d: Path) -> bool:
    """RUN voice: the runner builds the commands (no free-form command). Pass 1 at 0.3 renders all turns
    (characters = take A); narrator files removed and pass 2 at 0.65 (narrator; characters reused) gives the
    full take A; character files moved aside and pass 3 at 0.3 gives take B. Never --force."""
    d = Path(d)
    if not require_marker(d):
        return False
    n, c = voice_chars(d)
    price = round(guard.eleven_price_voice(n, c) + guard.ELEVEN_ALIGN_USD, 4)
    try:
        guard.sweep(d)
        row = guard.eleven_before(d, "voice", max(price, 0.0001), guard.sha256_of(d / "narration-tagged.md"))
    except guard.SpendRefused as e:
        say(f"REFUSED by SWS-G0: {e}")
        return False
    ok, detail = False, ""
    try:
        if prepare_turns(d):
            say("  _turns\\ deleted: the text changed since it was rendered")
        has_chars = any(sp != "narrator" for sp, _ in _tagged_chunks(d))
        if has_chars:
            rc = _synth(d, 0.3)
            if rc:
                raise RuntimeError(f"pass 1 failed ({rc})")
            keepA = d / "_turns" / "_takeA"
            keepA.mkdir(exist_ok=True)
            for f in _turn_files(d, False):
                shutil.copyfile(f, keepA / f.name)
        for f in _turn_files(d, True):
            f.unlink()
        rc = _synth(d, 0.65)
        if rc:
            raise RuntimeError(f"pass 2 failed ({rc})")
        shutil.copyfile(d / "narration.mp3", d / "narration_takeA.mp3")
        if has_chars:
            for f in _turn_files(d, False):
                f.unlink()
            rc = _synth(d, 0.3)
            if rc:
                raise RuntimeError(f"pass 3 failed ({rc})")
            shutil.copyfile(d / "narration.mp3", d / "narration_takeB.mp3")
        else:
            shutil.copyfile(d / "narration_takeA.mp3", d / "narration_takeB.mp3")
        ok = True
    except Exception as e:
        detail = str(e)
        say(f"FAILED: {e}")
    guard.eleven_finish(d, row["id"], ok, detail)
    say(f"voice row {row['id'][:8]} is OPEN until `confirm {row['id'][:8]} --amount <usd> --note ...` "
        "(no history receipt: probe R3 not run)")
    return ok


def cmd_align(d: Path) -> bool:
    """RUN align: once per narration.mp3 hash. ElevenLabs forced alignment -> alignment + meta. Then the
    local 'audio says the words' check (SWS-G2w). No whisper fallback for timing."""
    d = Path(d)
    if not require_marker(d):
        return False
    mp3 = d / "narration.mp3"
    if not mp3.is_file():
        say("REFUSED: no narration.mp3 (pick a take: `ok voice_ear --take A|B`)")
        return False
    try:
        guard.sweep(d)
        row = guard.eleven_before(d, "align", guard.ELEVEN_ALIGN_USD, guard.sha256_of(mp3))
    except guard.SpendRefused as e:
        say(f"REFUSED by SWS-G0: {e}")
        return False
    ok, detail = False, ""
    try:
        words = HOOKS["eleven_align"](d)
        real = [w for w in words if re.search(r"[A-Za-z0-9]", str(w.get("text", "")))]
        (d / "narration.alignment.meta.json").write_text(json.dumps(
            {"audio_sha256": guard.sha256_of(mp3), "backend": "elevenlabs", "word_count": len(real)}), encoding="utf-8")
        ok = True
    except Exception as e:
        detail = str(e)
        say(f"FAILED (stop; the owner decides; no silent whisper timing): {e}")
    guard.eleven_finish(d, row["id"], ok, detail)
    if not ok:
        return False
    heard = HOOKS["whisper"](mp3)
    g2w = ss.audio_says_words(_units(d), heard)
    return _report(g2w, d)


def cmd_score(d: Path, ep=None) -> bool:
    """RUN score: the fixed command; the episode's own score script exits unless this token is set."""
    d = Path(d)
    if not require_marker(d):
        return False
    secs = float(_doc(d)["narration_seconds"]) + ss.OUTRO_HOLD
    try:
        guard.sweep(d)
        row = guard.eleven_before(d, "score", round(secs * guard.ELEVEN_SCORE_USD_PER_SECOND, 4),
                                  guard.sha256_of(d / "assembly_receipt.json"))
    except (guard.SpendRefused, FileNotFoundError) as e:
        say(f"REFUSED by SWS-G0: {e}")
        return False
    token = score_token(d)
    rc = HOOKS["run"]([PY, str(d / "generate_score_piano.py")], env={"SWIRLS_RUN_SCORE": token}, cwd=d)
    guard.eleven_finish(d, row["id"], rc == 0, f"score script exit {rc}")
    say(f"score row {row['id'][:8]} is OPEN until `confirm {row['id'][:8]} --amount <usd> --note ...`")
    return rc == 0


def score_token(d: Path) -> str:
    import openart_bridge as ob
    return guard.sha256_of("score:" + str((ob.find_marker(d) or (None, {}))[1].get("episode_id")))[:16]


def cmd_confirm(d: Path, rid: str, amount=None, note=None, receipt=None, void=False, list_dump=None) -> bool:
    d = Path(d)
    full = next((k for k in guard.read_log(d) if k.startswith(rid)), None)
    if not full:
        say(f"REFUSED: unknown row {rid!r}")
        return False
    try:
        ok, why = guard.confirm(d, full, note or "", Path(receipt) if receipt else None, amount, void,
                                Path(list_dump) if list_dump else None)
    except guard.SpendRefused as e:
        say(f"REFUSED: {e}")
        return False
    say(f"{rid}: {why}")
    return ok


def cmd_fetch(d: Path, rid: str) -> bool:
    d = Path(d)
    full = next((k for k in guard.read_log(d) if k.startswith(rid)), None)
    if not full:
        say(f"REFUSED: unknown row {rid!r}")
        return False
    ok, why = guard.fetch(d, full)
    say(f"fetch {rid}: {why} (no new render was requested)")
    return ok


def cmd_reconcile(d: Path, dump: Path, ep) -> bool:
    """$0, detective: flag creations in a saved openart_creation_list dump that match an episode
    prompt but are not in the spend log."""
    from swirls_page import assemble_animation_prompt, assemble_still_prompt
    from swirls_cover import assemble_cover_animation_prompt, assemble_cover_still_prompt
    hashes = set()
    for pid, p in ep.PAGES.items():
        hashes |= {guard.sha256_of(assemble_still_prompt(p)), guard.sha256_of(assemble_animation_prompt(p))}
    for side, c in ep.COVERS.items():
        hashes |= {guard.sha256_of(assemble_cover_still_prompt(c)), guard.sha256_of(assemble_cover_animation_prompt(c))}
    data = json.loads(Path(dump).read_text(encoding="utf-8"))
    flagged = guard.reconcile(d, data.get("creations", []), hashes)
    for c in flagged:
        say(f"[FLAG] creation {c.get('creation_id')} matches an episode prompt but is not in spend_log.jsonl")
    say(f"reconcile: {len(flagged)} flagged")
    return not flagged


# ============================================================================== TIMING / PLAN ===
def cmd_timing(d: Path, manifest_words=None, manifest_size=None) -> bool:
    d = Path(d)
    try:
        doc = ss.build_timing(d, manifest_words)
    except ss.TimingError as e:
        say(f"FAILED (fail closed, no fallback): {e}")
        return False
    for tag, u in doc["units"].items():
        say(f"{tag:6} {u['start_s']:7.3f} -> {u['end_s']:7.3f}  slot {u['end_s'] - u['start_s']:5.2f}s  "
            f"clip {u['clip_duration']}s  frames {u['frames']}")
    return _report(ss.lint_timing(doc, None, None, manifest_size), d)


def plan_gates(ep, d: Path) -> list:
    d = Path(d)
    doc = _doc(d)
    units = _units(d)
    specs = {pid: p.clip_duration for pid, p in ep.PAGES.items()}
    specs.update({side: c.clip_duration for side, c in ep.COVERS.items()})
    meta = d / "narration.meta.json"
    tempo = json.loads(meta.read_text(encoding="utf-8")).get("narrator_atempo_factor") if meta.exists() else None
    gates = ss.lint_timing(doc, specs, tempo, (ep.MANIFEST.w, ep.MANIFEST.h))
    gates += ss.lint_baked_text(ep.PAGES, ep.COVERS, units)
    gates += ss.lint_still_prose(ep.PAGES, ep.COVERS)
    gates += ss.lint_clip_prose(ep.PAGES, ep.COVERS)
    plan, pg = ss.load_page_plan(d)
    gates += pg
    if plan:
        info = ss.derive_speakers(d, units)
        gates += ss.lint_dosage(plan, ep.PAGES)
        gates += ss.lint_refs_declared(plan, d / "refs" / "refs.json")
        gates += ss.lint_motion_carrier(plan, {t: v["speaker"] for t, v in info.items()}, plan.get("north_star"))
        gates += ss.lint_order({"MANIFEST.units": _ids(ep), "units.json": list(units),
                                "unit_timing.json": list(doc["units"]), "page_plan.json": list(plan["units"])})
    return gates


def cmd_plan(ep) -> bool:
    d = Path(ep.MANIFEST.episode_dir)
    gates = plan_gates(ep, d)
    ok = _report(gates, d, source="plan")
    plan_ok = d / "_qc" / "plan_ok.json"
    plan_ok.parent.mkdir(exist_ok=True)
    if ok:
        plan_ok.write_text(json.dumps({"episode_py": _sha_file(d / "episode.py"),
                                       "page_plan": _sha_file(d / "page_plan.json")}), encoding="utf-8")
    elif plan_ok.exists():
        plan_ok.unlink()
    return ok


def plan_current(d: Path) -> bool:
    p = Path(d) / "_qc" / "plan_ok.json"
    if not p.is_file():
        return False
    try:
        rec = json.loads(p.read_text(encoding="utf-8"))
    except Exception:
        return False
    return rec == {"episode_py": _sha_file(d / "episode.py"), "page_plan": _sha_file(d / "page_plan.json")}


# ================================================================================ STILLS ===
def _supersede(p: Path, why: str) -> Path:
    n = p.with_name(f"{p.name}.SUPERSEDED_{why}")
    k = 1
    while n.exists():
        k += 1
        n = p.with_name(f"{p.name}.SUPERSEDED_{why}_{k}")
    p.rename(n)
    return n


def _trim_gate(ep, d: Path) -> bool:
    if not require_marker(d):
        return False
    if not plan_current(d):
        say("REFUSED: `plan` has not passed on the current episode.py + page_plan.json")
        return False
    return True


def cmd_still(ep, id_: str, reroll: bool = False) -> bool:
    import swirls_page
    d = Path(ep.MANIFEST.episode_dir)
    if not _trim_gate(ep, d):
        return False
    if swirls_page.GEN_PROVIDER != "openart":
        say("REFUSED: a marked Swirls short renders on OpenArt only (SWIRLS_GEN_PROVIDER must be openart)")
        return False
    guard.sweep(d)
    if id_.startswith("ref:"):
        return _still_ref(ep, d, id_)
    spec = _spec(ep, id_)
    if spec is None:
        say(f"FAILED: {id_!r} is not a page id or a cover side")
        return False
    png = guard.png_path(d, id_)
    gates = [sv.sw_l4_refs_exist([spec])]
    if id_ in ep.COVERS:
        gates += [sv.sw_l1_cover_lighting_contrast(spec), sv.sw_l2_cover_text_lock(spec)]
    if not _report(gates, d):
        return False
    why = guard.step_open(d, "pictures")
    if why:                                   # check BEFORE touching any file: a renamed PNG would void the closing look
        say(f"REFUSED by SWS-G0: {why}")
        return False
    row = guard.confirmed_row(d, "still", id_)
    sup = png
    if png.exists():
        if row and row.get("output_sha256") == _sha_file(png) and not reroll:
            say(f"  [skip] {png.name} is already rendered (receipt matches); `--reroll` buys a new one")
            return True
        if not reroll:
            say(f"REFUSED: {png.name} exists with no matching spend receipt (copied in?). Reroll it through the guard.")
            return False
        sup = _supersede(png, "rerolled")
        say(f"  superseded -> {sup.name}")
    if id_ in ep.PAGES:
        from swirls_page import assemble_still_prompt as pf
        render = lambda: swirls_page.render_still(spec, png)  # noqa: E731
    else:
        import swirls_cover
        from swirls_cover import assemble_cover_still_prompt as pf
        render = lambda: swirls_cover.render_cover_still(spec, png)  # noqa: E731
    with guard.guard_context(d, "pictures", id_, "still", pf(spec)):
        try:
            ok = render()
        except RuntimeError as e:
            say(f"REFUSED: {e}")
            ok = False
    if not ok and reroll and not png.exists() and sup.exists():
        sup.rename(png)                          # a refused reroll must not lose the file it superseded
        say(f"  {png.name} restored (the reroll was refused or failed; nothing was bought)")
    if ok:
        level = ss.EDGE_COVER_LEVEL if id_ in ep.COVERS else ss.EDGE_PAGE_LEVEL
        _report([ss.edge_scan(png, level)], d, source=f"edge:{id_}")
    return ok


def _still_ref(ep, d: Path, id_: str) -> bool:
    """`still ref:<name>`: a subject not on the north-star page, rendered through the same guard
    (3 at most). The episode's REF_PROMPTS[name] = {"prompt": str, "refs": [Ref...]}."""
    import openart_bridge as ob
    name = id_.split(":", 1)[1]
    spec = getattr(ep, "REF_PROMPTS", {}).get(name)
    if not spec:
        say(f"FAILED: episode.py has no REF_PROMPTS[{name!r}]")
        return False
    out = d / "refs" / f"{name}.png"
    out.parent.mkdir(exist_ok=True)
    payload = {"kind": "still", "model": "nano-banana-pro", "mode": "image2image" if spec.get("refs") else "text2image",
               "prompt": spec["prompt"], "aspect_ratio": "9:16", "resolution": "2K",
               "refs": [{"path": r.path, "subject": r.subject} for r in spec.get("refs", [])], "out_path": str(out)}
    with guard.guard_context(d, "pictures", id_, "still", spec["prompt"]):
        try:
            ob.submit(payload)
        except ob.OpenArtBridgeError as e:
            say(f"FAILED: {e}")
            return False
    say(f"  -> refs\\{out.name}: add it to refs\\refs.json (name, file, sha256)")
    return True


def cmd_hold(ep, id_: str) -> bool:
    """$0: the page held for its real slot under its real voice line (+ a 390 px phone proof)."""
    d = Path(ep.MANIFEST.episode_dir)
    png = guard.png_path(d, id_)
    if not png.is_file():
        say(f"FAILED: {png.name} is not rendered")
        return False
    doc = _doc(d)
    u = doc["units"][id_]
    slot = ss.slot_of(doc, id_)
    qc = d / "_qc"
    qc.mkdir(exist_ok=True)
    out = qc / f"hold_{id_}.mp4"
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-loop", "1", "-framerate", str(ss.FPS), "-t", f"{slot:.3f}", "-i", str(png),
                    "-ss", f"{u['start_s']:.3f}", "-t", f"{slot:.3f}", "-i", str(d / "narration.mp3"),
                    "-vf", "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,setsar=1,format=yuv420p",
                    "-c:v", "libx264", "-crf", "20", "-c:a", "aac", "-t", f"{slot:.3f}", str(out)], check=True)
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", str(png), "-vf", "scale=390:-2", "-frames:v", "1",
                    str(qc / f"phone_{id_}.jpg")], check=True)
    say(f"hold written: {out}\n  phone proof: {qc / f'phone_{id_}.jpg'}")
    return True


def cmd_verify(ep) -> bool:
    """G9 (the one still audit) + G10 edge scan + G14s + G7c over every rendered still."""
    d = Path(ep.MANIFEST.episode_dir)
    if not _vision_gate():
        return False
    ok = True
    ids = [i for i in _ids(ep) if guard.png_path(d, i).exists()]
    for id_ in ids:
        png = guard.png_path(d, id_)
        spec = _spec(ep, id_)
        gates = sv.audit_still_v3(png, sv.expected_baked_texts(spec), _plan_unit(d, id_))
        gates.append(ss.edge_scan(png, ss.EDGE_COVER_LEVEL if id_ in ep.COVERS else ss.EDGE_PAGE_LEVEL))
        say(f"-- {id_}")
        ok = _report(gates, d, id_, png, source=f"still:{id_}") and ok
    plan, _ = ss.load_page_plan(d)
    ok = _report(ss.lint_still_provenance(d, ids), d) and ok
    ok = _report(ss.lint_refs_files(d), d) and ok
    ok = _report(ss.lint_refs_sent(d, plan), d) and ok
    say("Human check, always: Read every PNG, zoom 2x on every baked string, count each named character, "
        "read _qc\\phone_<id>.jpg")
    return ok


def _vision_gate() -> bool:
    if not HOOKS["vision_ok"]():
        say("REFUSED: metered Vision (API) mode is on; a Swirls short reads through the in-chat agent bridge only")
        return False
    return True


def cmd_read(ep, id_: str, strings: list[str], note: str) -> bool:
    d = Path(ep.MANIFEST.episode_dir)
    png = guard.png_path(d, id_)
    try:
        sv.record_read(png, strings, note)
    except Exception as e:
        say(f"REFUSED: {e}")
        return False
    say(f"read recorded for {png.name} (this file hash only)")
    return cmd_verify_one(ep, id_)


def cmd_verify_one(ep, id_: str) -> bool:
    d = Path(ep.MANIFEST.episode_dir)
    png = guard.png_path(d, id_)
    return _report(sv.audit_still_v3(png, sv.expected_baked_texts(_spec(ep, id_)), _plan_unit(d, id_)), d, id_, png)


def _font() -> str | None:
    for f in (r"C:\Windows\Fonts\arial.ttf", r"C:\Windows\Fonts\segoeui.ttf"):
        if Path(f).is_file():
            return f.replace("\\", "/").replace(":", r"\:")
    return None


def cmd_animatic(ep) -> bool:
    """$0: the stills at their real slots with the real voice and a STILLS TEST mark, plus a contact sheet."""
    from PIL import Image
    d = Path(ep.MANIFEST.episode_dir)
    ids = _ids(ep)
    if any(not guard.png_path(d, i).exists() for i in ids):
        say("FAILED: not every still is rendered")
        return False
    doc = _doc(d)
    qc = d / "_qc"
    qc.mkdir(exist_ok=True)
    segs = []
    prev = 0
    for t in ids:
        b = doc["units"][t]["end_frame"]
        seg = qc / f"_an_{t}.mp4"
        subprocess.run(["ffmpeg", "-y", "-v", "error", "-loop", "1", "-framerate", str(ss.FPS), "-i", str(guard.png_path(d, t)),
                        "-vf", "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,setsar=1,format=yuv420p",
                        "-frames:v", str(b - prev), "-c:v", "libx264", "-crf", "22", str(seg)], check=True)
        prev = b
        segs.append(seg)
    lst = qc / "_an_list.txt"
    lst.write_text("\n".join(f"file '{s.resolve().as_posix()}'" for s in segs), encoding="utf-8")
    font = _font()
    mark = (f"drawtext=fontfile='{font}':text='STILLS TEST':fontcolor=white:fontsize=60:x=40:y=60:box=1:boxcolor=black@0.6"
            if font else "drawbox=x=0:y=0:w=iw:h=24:color=red@0.8:t=fill")
    out = qc / "animatic.mp4"
    total = doc["narration_seconds"] + ss.OUTRO_HOLD
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", str(lst), "-i", str(d / "narration.mp3"),
                    "-vf", mark, "-c:v", "libx264", "-crf", "22", "-pix_fmt", "yuv420p", "-c:a", "aac",
                    "-af", f"apad=whole_dur={total}", "-t", f"{total:.3f}", str(out)], check=True)
    for s in segs:
        s.unlink()
    lst.unlink()
    tiles = [Image.open(guard.png_path(d, t)).convert("RGB").resize((270, 480)) for t in ids]
    sheet = Image.new("RGB", (270 * 4, 480 * 2), "white")
    for i, im in enumerate(tiles):
        sheet.paste(im, ((i % 4) * 270, (i // 4) * 480))
    sheet.save(qc / "contact_sheet.jpg", quality=88)
    say(f"animatic: {out}\n  contact sheet (costume / face drift): {qc / 'contact_sheet.jpg'}")
    return True


# ================================================================================ CLIPS ===
def clip_state(d: Path, id_: str) -> str:
    """none (no mp4) | fresh (its confirmed row's output hash is the file AND its input hash is the current
    still) | stale. A stale mp4 is never 'skipped as done': the runner renames it before a new render."""
    mp4, png = guard.clip_path(d, id_), guard.png_path(d, id_)
    if not mp4.exists():
        return "none"
    row = guard.confirmed_row(d, "anim", id_)
    fresh = row and _sha_file(mp4) == row.get("output_sha256") and row.get("input_sha256") == _sha_file(png)
    return "fresh" if fresh else "stale"


def cmd_animate(ep, id_: str) -> bool:
    import swirls_page
    d = Path(ep.MANIFEST.episode_dir)
    if not _trim_gate(ep, d):
        return False
    if swirls_page.GEN_PROVIDER != "openart":
        say("REFUSED: a marked Swirls short renders on OpenArt only")
        return False
    if not _vision_gate():
        return False
    guard.sweep(d)
    spec = _spec(ep, id_)
    if spec is None:
        say(f"FAILED: {id_!r} is not a page id or a cover side")
        return False
    png = guard.png_path(d, id_)
    mp4 = guard.clip_path(d, id_)
    if not png.exists():
        say(f"BLOCKED: still {png.name} not rendered yet")
        return False
    specs = {pid: p.clip_duration for pid, p in ep.PAGES.items()}
    specs.update({side: c.clip_duration for side, c in ep.COVERS.items()})
    g3 = [g for g in ss.lint_timing(_doc(d), specs, None, (ep.MANIFEST.w, ep.MANIFEST.h)) if g.gate == "SWS-G3"]
    gates = g3 + sv.audit_still_v3(png, sv.expected_baked_texts(spec), _plan_unit(d, id_)) + ss.lint_still_provenance(d, [id_])
    gates += ss.lint_refs_files(d)
    if not _report(gates, d, id_, png):
        say("BLOCKED: SWS-G3 / SWS-G9 / SWS-G14s must pass before a clip is paid for")
        return False
    state = clip_state(d, id_)
    if state == "fresh":
        say(f"  {mp4.name} is fresh (receipt matches the current still): nothing to buy")
        return True
    if state == "stale":
        why = guard.step_open(d, "clips")
        if why:                               # check before renaming: a missing file would void the closing look
            say(f"REFUSED by SWS-G0: {why}")
            return False
        say(f"  stale clip -> {_supersede(mp4, 'stale').name}")
    if id_ in ep.PAGES:
        from swirls_page import assemble_animation_prompt as pf
        render = lambda: swirls_page.render_animation(spec, png, mp4)  # noqa: E731
    else:
        import swirls_cover
        from swirls_cover import assemble_cover_animation_prompt as pf
        render = lambda: swirls_cover.render_cover_animation(spec, png, mp4)  # noqa: E731
    with guard.guard_context(d, "clips", id_, "anim", pf(spec) + guard.sha256_of(png)):
        try:
            return render()
        except RuntimeError as e:
            say(f"REFUSED: {e}")
            return False


def cmd_clipqc(ep, id_: str | None) -> bool:
    d = Path(ep.MANIFEST.episode_dir)
    if not _vision_gate():
        return False
    doc = _doc(d)
    ns = guard.north_star(d)
    ok = True
    for tag in ([id_] if id_ else _ids(ep)):
        mp4, png = guard.clip_path(d, tag), guard.png_path(d, tag)
        if not mp4.exists():
            say(f"[SKIP] {tag}: no clip yet")
            continue
        slot = ss.slot_of(doc, tag)
        say(f"-- {tag}")
        gates = [ss.clip_tech(mp4, slot)]
        mu = [u for u in ep.MANIFEST.units if u.tag == tag]
        gates += ss.lint_clip_provenance(d, mu)
        work = d / "_qc" / f"_hold_{tag}"
        gates.append(ss.still_stretch(mp4, 0.0, slot, work, is_north_star=(tag == ns)))
        if tag == "back":
            gates.append(ss.moving_hold(mp4, max(slot - ss.OUTRO_HOLD, 0.0), work))
        strips, _times = ss.make_strips(mp4, slot, d / "_qc" / f"strips_{tag}")
        reads = sv.read_strips(strips)
        gates += ss.judge_eyes(reads, _plan_unit(d, tag) or {}, sv.expected_baked_texts(_spec(ep, tag)))
        one = _report(gates, d, tag, mp4, source=f"clip:{tag}")
        Path(str(mp4) + ".clipqc.json").write_text(json.dumps({
            "output_sha256": _sha_file(mp4), "still_sha256": _sha_file(png), "slot": slot, "fail": not one,
            "strips": [str(s) for s in strips]}, indent=2), encoding="utf-8")
        ok = one and ok
        spk = ss.derive_speakers(d, _units(d)).get(tag, {}).get("speaker")
        if spk:
            say(f"  PLAY THIS CLIP: a character line ({spk}) is heard here and a strip cannot show lips moving")
    return ok


# ================================================================================ ASSEMBLY ===
def _stream_durations(mp4: Path) -> tuple[float | None, float | None]:
    import check_landing_hold
    return check_landing_hold._durations(Path(mp4))


def cmd_assemble(ep, score_name: str | None, draft: bool = False) -> bool:
    d = Path(ep.MANIFEST.episode_dir)
    if not require_marker(d):
        return False
    if not _vision_gate():
        return False
    ids = _ids(ep)
    plan, _ = ss.load_page_plan(d)
    gates = []
    for id_ in ids:
        png = guard.png_path(d, id_)
        if not png.exists():
            gates.append(ss._g("SW-V2-gate", "FAIL", f"{id_} not rendered"))
            continue
        gates += [g for g in sv.audit_still_v3(png, sv.expected_baked_texts(_spec(ep, id_)), _plan_unit(d, id_))
                  if g.verdict == "FAIL"]
    gates += ss.lint_still_provenance(d, ids)
    gates += ss.lint_clip_provenance(d, ep.MANIFEST.units)
    if not _report(gates, d):
        return False
    try:
        result = sa.assemble(ep.MANIFEST, None if draft else score_name)
    except (sa.ShortClipError, ValueError) as e:
        say(f"FAILED: {e}")
        return False
    doc = _doc(d)
    gates = [sv.sw_a1_duration_parity(result["out"])]
    gates += sv.sw_a2_unit_duration(result["units"])
    gates.append(sv.sw_a3_total_duration(result["final_duration"], result["narration_len"], ep.MANIFEST.outro_hold))
    pic, aud = _stream_durations(result["out"])
    gates += ss.lint_assembly(result["receipt"], doc, result["out"], pic, aud)
    gates.append(ss.moving_hold(result["out"], result["total"] - ss.OUTRO_HOLD, d / "_qc" / "_hold_cut"))
    if not draft:
        variant = ep.MANIFEST.scores[score_name]
        gates += ss.score_gate(variant.score, result["total"], result["out"], ep.MANIFEST.narration)
    ok = _report(gates, d, source="draft" if draft else "scored")
    if ok and not draft:
        import build_srt
        try:
            build_srt.build_from_cache(d)
        except Exception as e:
            say(f"[warn] cached .srt not built (non-fatal; no alignment is ever bought here): {e}")
        if HOOKS["tracker"]:
            HOOKS["tracker"]()
    return ok


def cmd_finalize(ep) -> bool:
    """Step 9: the episode's own build_sfx.py (reads assembly_receipt_scored.json), cache-only SRT,
    FINAL_VIDEO.txt, final_receipt.json (SWS-G16), then the landing hold + G15 + G15h on the FINAL file."""
    import build_srt
    d = Path(ep.MANIFEST.episode_dir)
    if not require_marker(d):
        return False
    try:
        sc = json.loads((d / "assembly_receipt_scored.json").read_text(encoding="utf-8"))
    except Exception:
        say("FAILED: no scored assembly receipt (run `assemble --score piano`)")
        return False
    rc = HOOKS["run"]([PY, str(d / "build_sfx.py")], cwd=d)
    final = d / f"{d.name}_final_piano_sfx.mp4"
    if rc or not final.is_file():
        say("FAILED: build_sfx.py did not produce the final file")
        return False
    build_srt.build_from_cache(d)
    (d / "FINAL_VIDEO.txt").write_text(str(final) + "\n", encoding="utf-8")
    ss.write_final_receipt(d, Path(sc["output"]), final)
    doc = _doc(d)
    pic, aud = _stream_durations(final)
    gates = ss.check_chain(d)
    gates += ss.lint_assembly(sc, doc, final, pic, aud)
    gates.append(ss.moving_hold(final, float(sc["total"]) - ss.OUTRO_HOLD, d / "_qc" / "_hold_final"))
    import check_landing_hold
    ok_l, msg = check_landing_hold.check_parity(final)
    gates.append(ss._g("SWS-landing", "PASS" if ok_l else "FAIL", msg))
    return _report(gates, d, source="final")


def cmd_status(d: Path) -> bool:
    d = Path(d)
    if (d / ".swirls_short").exists():
        sw = guard.sweep(d)
        if sw:
            say("sweep: " + ", ".join(sw))
    rows, nxt, spend = ss.status(d)
    for name, done, _ in rows:
        say(f"[{'done' if done else '    '}] {name}")
    say(f"\n{nxt}")
    for step, v in spend.items():
        say(f"{step}: spent {v['spent']:g} of cap {v['cap']:g} {v['cur']}")
    op = guard.open_rows(d) if (d / "spend_log.jsonl").exists() else []
    for r in op:
        say(f"OPEN ROW {r['id'][:8]} {r['step']}/{r['unit']} = {r['status']}: settle it (fetch / confirm)")
    warns = ss.open_warns(d)
    if warns:
        say("Open WARNs (WARN never counts as pass):")
        for w in warns:
            say("  - " + w.replace("|", ": "))
    return True
