"""swirls_guard.py -- SWS-G0, the spend guard for the Swirls SHORT pipeline (design v3.2 section 5).
$0 module: it reads/writes only files inside the episode folder (and the runtime bridge folders
under .agent_bridge\\) and never calls a paid API.

What it is, honestly: it stops MISTAKES (no recorded yes, over the cap the owner saw, wrong
settings, twice, late, a second session). It does NOT prove the owner said yes (the session types
`approve`), and it cannot see a direct MCP generate call (only `reconcile`, afterwards).

Files per episode: approvals.json (append-only grants), gates.json (append-only `ok` looks),
spend_log.jsonl (append-only rows, latest row per id wins), _quotes\\<step>.json, .spend.lock.
Row states: requested, UNRESOLVED, LATE_PENDING, CANCELLED_UNCLAIMED (all OPEN) -> confirmed | voided.
"""
from __future__ import annotations

import contextlib
import datetime
import hashlib
import json
import math
import os
import re
import shutil
import sys
import threading
import time
import uuid
from dataclasses import dataclass
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE / "test_the_cross"))
import openart_bridge as ob  # noqa: E402

# ------------------------------------------------------------------ constants ---
KLING_CR_PER_SECOND = 35            # kling-3-omni, pro, sound off, per whole second (design s0, measured)
STILL_CR = 40                       # nano-banana-pro 2K 9:16 (measured)
USD_PER_CR = 0.002
CONFIRM_TOLERANCE = 1.10
RENDERS_PER_UNIT = 3                # first render + 2 rerolls
KLING_MIN_S, KLING_MAX_S = 3, 15
# ElevenLabs rates are typed from the owner's invoice and UNVERIFIED until the first receipt (probe R3).
ELEVEN_USD_PER_CHAR = 0.0003
ELEVEN_ALIGN_USD = 0.05
ELEVEN_SCORE_USD_PER_SECOND = 0.0222
ELEVEN_RATES_VERIFIED = False
ELEVEN_COMMANDS = ("voice", "align", "score")       # the only paid ElevenLabs commands
OPEN = ("requested", "UNRESOLVED", "LATE_PENDING", "CANCELLED_UNCLAIMED")

# step -> currency, gate that opens it, first-item hard-stop gate, gate that closes it
STEPS = {
    "voice":    {"cur": "usd", "opens": "words",           "stop": None,              "closed": "voice_ear"},
    "pictures": {"cur": "cr",  "opens": "voice_ear",       "stop": "northstar_look",  "closed": "stills_animatic"},
    "clips":    {"cur": "cr",  "opens": "stills_animatic", "stop": "clip_test_look",  "closed": "draft_cut"},
    "score":    {"cur": "usd", "opens": "draft_cut",       "stop": None,              "closed": "film_final"},
    "poster":   {"cur": "cr",  "opens": "film_final",      "stop": None,              "closed": None},
}
ELEVEN_STEP = {"voice": "voice", "align": "voice", "score": "score"}
OK_GATES = ("words", "voice_ear", "northstar_look", "stills_animatic", "clip_test_look",
            "draft_cut", "film_final")


class SpendRefused(RuntimeError):
    """A paid request was refused. Fail closed."""


# --------------------------------------------------------------------- helpers ---
def sha256_of(data) -> str:
    if isinstance(data, Path):
        data = data.read_bytes()
    if isinstance(data, str):
        data = data.encode("utf-8")
    return hashlib.sha256(data).hexdigest()


def _file_sha(p: Path) -> str | None:
    p = Path(p)
    return sha256_of(p) if p.is_file() else None


def _write_json(p: Path, obj) -> None:
    tmp = p.with_name(p.name + ".tmp")
    tmp.write_text(json.dumps(obj, indent=2, ensure_ascii=False), encoding="utf-8")
    os.replace(tmp, p)


def _read_json(p: Path, default):
    if not Path(p).exists():
        return default
    try:
        return json.loads(Path(p).read_text(encoding="utf-8"))
    except Exception as e:
        raise SpendRefused(f"{Path(p).name} is broken ({e}) -- fix it by hand")


def _num(x) -> bool:
    return isinstance(x, (int, float)) and not isinstance(x, bool)


def png_path(ep_dir: Path, id_: str) -> Path:
    d = Path(ep_dir)
    return d / (f"{id_}_cover.png" if id_ in ("front", "back") else f"{d.name}_{id_}_9x16.png")


def clip_path(ep_dir: Path, id_: str) -> Path:
    return png_path(ep_dir, id_).with_suffix(".mp4")


def unit_tags(ep_dir: Path) -> list[str]:
    d = Path(ep_dir)
    for name, key in (("unit_timing.json", "units"), ("units.json", None)):
        if (d / name).exists():
            try:
                data = json.loads((d / name).read_text(encoding="utf-8"))
                return list(data[key] if key else data)
            except Exception:
                return []
    return []


def north_star(ep_dir: Path) -> str | None:
    try:
        return json.loads((Path(ep_dir) / "page_plan.json").read_text(encoding="utf-8")).get("north_star")
    except Exception:
        return None


# ---------------------------------------------------------------- file lock ---
@contextlib.contextmanager
def _lock(ep_dir: Path, timeout: float = 15.0):
    p = Path(ep_dir) / ".spend.lock"
    t0 = time.time()
    while True:
        try:
            fd = os.open(str(p), os.O_CREAT | os.O_EXCL | os.O_WRONLY)
            os.write(fd, str(os.getpid()).encode())
            os.close(fd)
            break
        except FileExistsError:
            try:
                if time.time() - os.path.getmtime(p) > 60:      # a dead holder
                    os.unlink(p)
                    continue
            except OSError:
                pass
            if time.time() - t0 > timeout:
                raise SpendRefused("spend lock busy -- another command is checking the spend log")
            time.sleep(0.01)
    try:
        yield
    finally:
        with contextlib.suppress(OSError):
            os.unlink(p)


# ---------------------------------------------------------------------- log ---
def read_log(ep_dir: Path) -> dict[str, dict]:
    p = Path(ep_dir) / "spend_log.jsonl"
    state: dict[str, dict] = {}
    if not p.exists():
        return state
    for line in p.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        try:
            row = json.loads(line)
        except Exception:
            raise SpendRefused("spend_log.jsonl has a broken line -- fix it by hand")
        state[row["id"]] = {**state.get(row["id"], {}), **row}
    return state


def _append(ep_dir: Path, row: dict) -> None:
    with open(Path(ep_dir) / "spend_log.jsonl", "a", encoding="utf-8") as f:
        f.write(json.dumps(row, ensure_ascii=False) + "\n")


def mark(ep_dir: Path, rid: str, status: str | None = None, **fields) -> None:
    row = {"id": rid, "ts_update": time.time(), **fields}
    if status:
        row["status"] = status
    with _lock(ep_dir):
        _append(ep_dir, row)


def open_rows(ep_dir: Path) -> list[dict]:
    return [r for r in read_log(ep_dir).values() if r.get("status") in OPEN]


def _credits(r: dict) -> float:
    return float(r.get("credits_spent") or 0) if r["status"] == "confirmed" else 0.0


def spent(ep_dir: Path, step: str) -> float:
    return sum(_credits(r) for r in read_log(ep_dir).values() if r.get("step") == step)


def confirmed_row(ep_dir: Path, kind: str, unit: str) -> dict | None:
    rows = [r for r in read_log(ep_dir).values()
            if r.get("kind") == kind and r.get("unit") == unit and r.get("status") == "confirmed"]
    return max(rows, key=lambda r: r.get("ts", ""), default=None) if rows else None


# ------------------------------------------------------------------- gates (ok) ---
def bindings_for(ep_dir: Path, gate: str) -> dict:
    """The files a look/ok is bound to. A None hash = the file is missing = the gate cannot hold."""
    d = Path(ep_dir)
    tags = unit_tags(d)
    ns = north_star(d)
    if gate == "words":
        files = ["narration.md", "narration-tagged.md", "units.json"]
    elif gate == "voice_ear":
        files = ["narration.mp3"]
    elif gate == "northstar_look":
        files = [png_path(d, ns).name] if ns else []
    elif gate == "stills_animatic":
        files = [png_path(d, t).name for t in tags] + ["unit_timing.json"]
    elif gate == "clip_test_look":
        files = [clip_path(d, t).name for t in (ns, "back") if t]
    elif gate == "draft_cut":
        files = ["assembly_receipt.json"]
    elif gate == "film_final":
        fv = d / "FINAL_VIDEO.txt"
        target = None
        if fv.exists():
            for line in fv.read_text(encoding="utf-8").splitlines():
                line = line.strip()
                if line and Path(line).is_file():
                    target = Path(line)
                    break
                if line and (d / line).is_file():
                    target = d / line
                    break
        return {"FINAL_VIDEO": _file_sha(target) if target else None}
    else:
        raise SpendRefused(f"unknown gate {gate!r} (known: {OK_GATES})")
    out = {f: _file_sha(d / f) for f in files}
    return out or {"(nothing to bind)": None}


def _gates(ep_dir: Path) -> dict:
    return _read_json(Path(ep_dir) / "gates.json", {"history": []})


def gate_record(ep_dir: Path, gate: str) -> dict | None:
    hist = [h for h in _gates(ep_dir)["history"] if h["gate"] == gate]
    return hist[-1] if hist else None


def gate_valid(ep_dir: Path, gate: str) -> bool:
    rec = gate_record(ep_dir, gate)
    if not rec:
        return False
    cur = bindings_for(ep_dir, gate)
    return all(v is not None for v in cur.values()) and cur == rec["bindings"]


def record_gate(ep_dir: Path, gate: str, note: str, extra: dict | None = None) -> dict:
    if gate not in OK_GATES:
        raise SpendRefused(f"unknown gate {gate!r}")
    if not (note or "").strip():
        raise SpendRefused("ok needs --note with the owner's words and the date")
    b = bindings_for(ep_dir, gate)
    missing = [k for k, v in b.items() if v is None]
    if missing:
        raise SpendRefused(f"gate {gate!r} cannot be recorded, missing: {missing}")
    rec = {"gate": gate, "note": note.strip(), "date": datetime.date.today().isoformat(),
           "ts": time.time(), "bindings": b, **(extra or {})}
    with _lock(ep_dir):
        g = _gates(ep_dir)
        g["history"].append(rec)
        _write_json(Path(ep_dir) / "gates.json", g)
    return rec


def ok_notes(ep_dir: Path) -> list[str]:
    return [h["note"].strip() for h in _gates(ep_dir)["history"]]


# ----------------------------------------------------------- quotes and grants ---
def at_most(about: float, planned_rerolls: float, cur: str) -> float:
    raw = (about + planned_rerolls) * CONFIRM_TOLERANCE
    return float(math.ceil(raw - 1e-9)) if cur == "cr" else math.ceil(raw * 100 - 1e-9) / 100


def quote_bound_sha(ep_dir: Path, step: str) -> str | None:
    d = Path(ep_dir)
    f = {"voice": "narration-tagged.md"}.get(step, "unit_timing.json")
    return _file_sha(d / f)


def write_quote(ep_dir: Path, step: str, about: float, planned_rerolls: float, items: dict) -> dict:
    cur = STEPS[step]["cur"]
    q = {"step": step, "cur": cur, "about": about, "planned_rerolls": planned_rerolls,
         "at_most": at_most(about, planned_rerolls, cur), "items": items,
         "timing_sha256": quote_bound_sha(ep_dir, step),
         "rates_verified": bool(ELEVEN_RATES_VERIFIED) if cur == "usd" else True}
    (Path(ep_dir) / "_quotes").mkdir(exist_ok=True)
    _write_json(Path(ep_dir) / "_quotes" / f"{step}.json", q)
    return q


def read_quote(ep_dir: Path, step: str) -> dict:
    p = Path(ep_dir) / "_quotes" / f"{step}.json"
    if not p.exists():
        raise SpendRefused(f"no quote for {step!r}: run `quote {step}` first")
    return _read_json(p, {})


def step_open(ep_dir: Path, step: str, allow_closed: bool = False) -> str | None:
    """None if the step is open, else the reason."""
    spec = STEPS[step]
    if not gate_valid(ep_dir, spec["opens"]):
        return f"step {step!r} opens only after a valid {spec['opens']!r} look"
    if not allow_closed and spec["closed"] and gate_valid(ep_dir, spec["closed"]):
        return f"step {step!r} is closed ({spec['closed']!r} is recorded)"
    return None


def _approvals(ep_dir: Path) -> dict:
    data = _read_json(Path(ep_dir) / "approvals.json", {"grants": []})
    if not isinstance(data.get("grants"), list):
        raise SpendRefused("approvals.json is broken (no 'grants' list)")
    return data


def grants(ep_dir: Path) -> list[dict]:
    return _approvals(ep_dir)["grants"]


def grant_alive(ep_dir: Path, g: dict, allow_closed: bool = False) -> bool:
    if g.get("quote_step") and quote_bound_sha(ep_dir, g["quote_step"]) != g.get("timing_sha256"):
        return False
    spec = STEPS[g["step"]]
    if not allow_closed and spec["closed"] and gate_valid(ep_dir, spec["closed"]):
        return False
    return True


def approve(ep_dir: Path, step: str, cap: float, cur: str, note: str, balance: float | None = None,
            unit_id: str | None = None, renders: int | None = None, price: float | None = None) -> dict:
    """Append a grant (append-only). Refused unless --cap equals the quote's at_most (base grant),
    the note carries that number and a date, the note is not an `ok` note, and (cr) balance >= cap."""
    if step not in STEPS:
        raise SpendRefused(f"unknown step {step!r}")
    if STEPS[step]["cur"] != cur:
        raise SpendRefused(f"step {step!r} is priced in {STEPS[step]['cur']}, not {cur}")
    if not _num(cap) or cap <= 0:
        raise SpendRefused("cap must be a positive number")
    note = (note or "").strip()
    if not re.search(r"\d{4}-\d{2}-\d{2}", note):
        raise SpendRefused("--note must quote the owner's words and carry a date (YYYY-MM-DD)")
    nums = {f"{cap:g}", f"{cap:.2f}", f"{int(cap)}" if float(cap).is_integer() else f"{cap}"}
    if not any(re.search(rf"(?<![\d.]){re.escape(n)}(?![\d])", note) for n in nums):
        raise SpendRefused(f"--note must contain the cap number the owner saw ({cap:g})")
    if note in ok_notes(ep_dir):
        raise SpendRefused("this note is the same text as a look (`ok`) note: a look is not a spend order")
    if cur == "cr":
        if not _num(balance):
            raise SpendRefused("balance unknown -- read it from openart_account_get and pass --balance")
        if balance < cap:
            raise SpendRefused(f"balance {balance} < cap {cap}")
    why = step_open(ep_dir, step)
    if why:
        raise SpendRefused(why)
    grant = {"grant_id": uuid.uuid4().hex[:10], "step": step, "unit_id": unit_id, "cap": cap, "cur": cur,
             "renders_allowed": None, "note": note, "date": datetime.date.today().isoformat(),
             "ts": time.time(), "price": price}
    if unit_id is None:
        q = read_quote(ep_dir, step)
        if cap != q["at_most"]:
            raise SpendRefused(f"--cap {cap:g} must equal the quote's 'at most' {q['at_most']:g} "
                               "(the number the owner was shown)")
        if q.get("timing_sha256") != quote_bound_sha(ep_dir, step):
            raise SpendRefused("the quote is stale (timing / text changed): run `quote` again")
        grant.update(quote_step=step, timing_sha256=q["timing_sha256"],
                     quote_sha256=sha256_of(Path(ep_dir) / "_quotes" / f"{step}.json"))
    else:
        if not renders or renders < 1:
            raise SpendRefused("a unit grant needs --renders >= 1")
        if not any(g["step"] == step and g["unit_id"] is None and grant_alive(ep_dir, g)
                   for g in grants(ep_dir)):
            raise SpendRefused(f"a unit grant adds to an approved step; {step!r} has no live base grant")
        grant["renders_allowed"] = int(renders)
    with _lock(ep_dir):
        data = _approvals(ep_dir)
        data["grants"].append(grant)
        _write_json(Path(ep_dir) / "approvals.json", data)
    return grant


# ------------------------------------------------------------------- pricing ---
def price_of(payload: dict, grant_price: float | None = None) -> tuple[float, str]:
    """Price FROM THE PAYLOAD. Unknown row -> the grant's --price, else refuse."""
    kind = payload.get("kind")
    if (kind == "anim" and payload.get("model") == "kling-3-omni" and payload.get("mode") == "image2video"
            and payload.get("resolution") == "pro" and payload.get("generate_sound") is False):
        d = payload.get("duration")
        if isinstance(d, int) and not isinstance(d, bool) and KLING_MIN_S <= d <= KLING_MAX_S:
            return float(KLING_CR_PER_SECOND * d), "cr"
    if (kind == "still" and payload.get("model") == "nano-banana-pro"
            and payload.get("mode") in ("image2image", "text2image")
            and payload.get("resolution") == "2K" and payload.get("aspect_ratio") == "9:16"):
        return float(STILL_CR), "cr"
    if _num(grant_price) and grant_price > 0:
        return float(grant_price), "cr"
    raise SpendRefused(f"unknown price row for {kind!r} {payload.get('model')!r} "
                       f"(mode/resolution/aspect/sound/duration do not match a known row) and no --price grant")


def priced_fields(payload: dict) -> dict:
    keys = (["model", "mode", "resolution", "generate_sound", "duration"] if payload.get("kind") == "anim"
            else ["model", "mode", "resolution", "aspect_ratio"])
    return {k: payload.get(k) for k in keys}


def payload_hashes(payload: dict) -> dict:
    out = {"refs": {}, "start_image": None}
    for r in payload.get("refs") or []:
        out["refs"][r.get("subject", r.get("path"))] = _file_sha(Path(r["path"]))
    if payload.get("start_image_path"):
        out["start_image"] = _file_sha(Path(payload["start_image_path"]))
    return out


# ------------------------------------------------------------------ the guard ---
@dataclass
class GuardCtx:
    episode_dir: Path
    step: str
    unit: str
    kind: str                # still | anim
    prompt_sha256: str = ""


_local = threading.local()


@contextlib.contextmanager
def guard_context(episode_dir, step: str, unit: str, kind: str, prompt: str = ""):
    prev = getattr(_local, "ctx", None)
    _local.ctx = GuardCtx(Path(episode_dir), step, unit, kind, sha256_of(prompt) if prompt else "")
    try:
        yield _local.ctx
    finally:
        _local.ctx = prev


def current_context() -> GuardCtx | None:
    return getattr(_local, "ctx", None)


def _unit_renders(log: dict, kind: str, unit: str) -> int:
    return sum(1 for r in log.values() if r.get("kind") == kind and r.get("unit") == unit
               and r.get("status") != "voided")


def _over_price_lock(ep_dir: Path, step: str) -> bool:
    """A confirmed row above its price locks the step until a grant newer than that row."""
    log = read_log(ep_dir)
    over = [r["ts_update"] for r in log.values()
            if r.get("step") == step and r.get("over_price") and r.get("status") == "confirmed"]
    if not over:
        return False
    newest = max((g["ts"] for g in grants(ep_dir) if g["step"] == step), default=0)
    return newest < max(over)


def _check_common(ep_dir: Path, step: str, unit: str | None, kind: str, price: float,
                  allow_closed: bool = False) -> list[str]:
    """Shared by OpenArt before() and ElevenLabs eleven_before(). Returns the grant ids used."""
    why = step_open(ep_dir, step, allow_closed=allow_closed)
    if why:
        raise SpendRefused(why)
    live = [g for g in grants(ep_dir) if g["step"] == step and grant_alive(ep_dir, g, allow_closed)]
    base = [g for g in live if g["unit_id"] is None]
    if not base:
        raise SpendRefused(f"no live grant for step {step!r}: ask the owner (quote -> approve)")
    if _over_price_lock(ep_dir, step):
        raise SpendRefused(f"step {step!r} is locked: a confirmed row was above its price; needs a new grant")
    log = read_log(ep_dir)
    op = [r for r in log.values() if r.get("status") in OPEN]
    if op:
        raise SpendRefused("an open spend row blocks every paid command: "
                           + ", ".join(f"{r['id'][:8]}={r['status']}" for r in op)
                           + " (settle with fetch / confirm)")
    cap = sum(g["cap"] for g in live)
    already = spent(ep_dir, step)
    if already + price * CONFIRM_TOLERANCE > cap + 1e-9:
        raise SpendRefused(f"step {step!r}: spent {already:g} + {price:g} x1.10 would pass the cap {cap:g}")
    return [g["grant_id"] for g in live]


def before(ctx: GuardCtx, payload: dict, provider: str = "openart") -> dict:
    """Call BEFORE every OpenArt request. Writes the `requested` row (under the lock) and returns it."""
    if provider != "openart":
        raise SpendRefused(f"provider {provider!r}: a marked Swirls short spends on OpenArt only")
    ep = Path(ctx.episode_dir).resolve()
    found = ob.find_marker(ep)
    if found is None or found[0].resolve() != ep:
        raise SpendRefused("no .swirls_short marker in the episode folder")
    out = payload.get("out_path")
    if not out:
        raise SpendRefused("payload has no out_path")
    try:
        Path(out).resolve().relative_to(ep)
    except ValueError:
        raise SpendRefused("out_path is outside this episode")
    if ctx.step not in STEPS or STEPS[ctx.step]["cur"] != "cr":
        raise SpendRefused(f"step {ctx.step!r} cannot spend OpenArt credits")
    if payload.get("kind") != ctx.kind:
        raise SpendRefused("payload kind does not match the guard context")
    gp = max((g["price"] for g in grants(ep) if g["step"] == ctx.step and g.get("price")), default=None)
    price, cur = price_of(payload, gp)
    with _lock(ep):
        spec = STEPS[ctx.step]
        ids = _check_common(ep, ctx.step, ctx.unit, ctx.kind, price)
        ns = north_star(ep)
        if spec["stop"] and not gate_valid(ep, spec["stop"]):
            allowed = {"pictures": {ns}, "clips": {ns, "back"}}.get(ctx.step, {ns})
            if ctx.unit not in allowed:
                raise SpendRefused(f"until {spec['stop']!r} is recorded only {sorted(a for a in allowed if a)} "
                                   f"may be bought, not {ctx.unit!r}")
        log = read_log(ep)
        extra = sum(g["renders_allowed"] or 0 for g in grants(ep)
                    if g["step"] == ctx.step and g["unit_id"] == ctx.unit and grant_alive(ep, g))
        n = _unit_renders(log, ctx.kind, ctx.unit)
        if n >= RENDERS_PER_UNIT + extra:
            raise SpendRefused(f"{ctx.kind} {ctx.unit!r} already has {n} renders (first + 2 rerolls): "
                               "a 4th needs a unit grant and a changed lever")
        if str(ctx.unit).startswith("ref:"):
            refs_done = {r["unit"] for r in log.values() if str(r.get("unit", "")).startswith("ref:")
                         and r.get("status") != "voided"}
            if ctx.unit not in refs_done and len(refs_done) >= 3:
                raise SpendRefused("3 ref renders at most (`still ref:<name>`)")
        hashes = payload_hashes(payload)
        row = {"id": uuid.uuid4().hex, "ts": datetime.datetime.now().isoformat(timespec="milliseconds"),
               "ts_update": time.time(), "step": ctx.step, "unit": ctx.unit, "kind": ctx.kind,
               "provider": "openart", "price": price, "cur": cur, "status": "requested",
               "out_path": str(Path(out).resolve()), "grants": ids,
               "prompt_sha256": ctx.prompt_sha256 or sha256_of(payload.get("prompt", "")),
               "input_sha256": hashes["start_image"] if ctx.kind == "anim" else sha256_of(
                   payload.get("prompt", "") + json.dumps(hashes["refs"], sort_keys=True)),
               "ref_sha256": hashes["refs"], "priced": priced_fields(payload)}
        _append(ep, row)
    return row


def _find_staged(rid: str) -> Path | None:
    hits = sorted(ob.STAGING_DIR.glob(f"{rid}.*")) if ob.STAGING_DIR.exists() else []
    return hits[0] if hits else None


def _read_receipt(rid: str) -> dict | None:
    p = ob.RECEIPTS_DIR / f"{rid}.json"
    if not p.exists():
        return None
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except Exception:
        return None


def _same(a, b) -> bool:
    if isinstance(a, str) and isinstance(b, str):
        return a.strip().lower() == b.strip().lower()
    return a == b


def _settle(ep_dir: Path, rid: str, record: dict | None, allow_over: bool = False) -> tuple[bool, str]:
    """Confirm an OpenArt row ONLY from the creation record read back from OpenArt: right creation,
    sent_params equal the priced fields, credits a number <= 1.10 x price. Then move the staged file."""
    ep = Path(ep_dir)
    row = read_log(ep)[rid]
    cid = row.get("creation_id")
    if not cid:
        return False, "no creation_id"
    if not record:
        return False, "no creation record (openart_creation_show) saved for this request"
    if record.get("creation_id") not in (None, cid):
        return False, "the record is for a different creation"
    sp = record.get("sent_params")
    want = row.get("priced") or {}
    if not isinstance(sp, dict) or any(k not in sp or not _same(sp[k], v) for k, v in want.items()
                                      if v is not None):
        return False, f"sent_params in the record do not equal the priced fields {want}"
    credits = record.get("credits_spent")
    if not _num(credits):
        return False, "the record shows no numeric credits_spent"
    over = credits > row["price"] * CONFIRM_TOLERANCE + 1e-9
    if over and not allow_over:
        return False, f"record credits {credits} > 110% of the price {row['price']}"
    staged = _find_staged(rid)
    out = Path(row["out_path"])
    if staged is None and not out.exists():
        return False, "no staged download (use fetch to re-download)"
    if staged is not None:
        out.parent.mkdir(parents=True, exist_ok=True)
        tmp = out.with_name(out.name + ".part")
        shutil.copyfile(staged, tmp)
        os.replace(tmp, out)
        with contextlib.suppress(OSError):
            staged.unlink()
    mark(ep, rid, "confirmed", credits_spent=credits, output_sha256=_file_sha(out), over_price=bool(over),
         record_creation_id=cid)
    return True, "confirmed"


def after(ctx: GuardCtx, rid: str, resp: dict) -> bool:
    ep = Path(ctx.episode_dir)
    cid = resp.get("creation_id")
    mark(ep, rid, creation_id=cid)
    if resp.get("status") != "ok":
        mark(ep, rid, "UNRESOLVED", error=str(resp.get("error")))
        return False
    ok, why = _settle(ep, rid, _read_receipt(rid))
    if not ok:
        mark(ep, rid, "UNRESOLVED", error=why)
    return ok


def sweep(ep_dir: Path) -> list[str]:
    """Start-up sweep: a `requested` row whose client heartbeat is stale was killed. Rename-or-late."""
    done = []
    for r in list(open_rows(ep_dir)):
        if r.get("status") != "requested":
            continue
        rid = r["id"]
        hb = ob.GUARDED_DIR / f"{rid}.heartbeat"
        stale = (time.time() - hb.stat().st_mtime) > ob.HEARTBEAT_STALE_SECONDS if hb.exists() else True
        if not stale:
            continue
        if (ob.CANCELLED_DIR / f"{rid}.request.json").exists():
            st = "CANCELLED_UNCLAIMED"
        elif (ob.GUARDED_DIR / f"{rid}.request.json").exists():
            st = ob.cancel_request(rid)
        else:
            st = "LATE_PENDING"
        mark(ep_dir, rid, st, cancel_ts=time.time())
        done.append(f"{rid[:8]}={st}")
    return done


def fetch(ep_dir: Path, rid: str) -> tuple[bool, str]:
    """Settle an open OpenArt row from the creation record and the staged download. No new charge,
    no generate call."""
    ep = Path(ep_dir)
    row = read_log(ep).get(rid)
    if not row or row.get("status") not in OPEN or row.get("provider") != "openart":
        return False, "not an open OpenArt row"
    if not row.get("creation_id"):
        sub = ob.CLAIMED_DIR / f"{rid}.submitted.json"
        if sub.exists():
            mark(ep, rid, creation_id=json.loads(sub.read_text(encoding="utf-8")).get("creation_id"))
    if not read_log(ep)[rid].get("creation_id"):
        return False, "no creation_id known (no submitted.json): cannot settle; the owner decides"
    ok, why = _settle(ep, rid, _read_receipt(rid))
    if not ok:
        mark(ep, rid, "UNRESOLVED", error=why)
    return ok, why


def confirm(ep_dir: Path, rid: str, note: str, receipt: Path | None = None, amount: float | None = None,
            void: bool = False, list_dump: Path | None = None) -> tuple[bool, str]:
    ep = Path(ep_dir)
    row = read_log(ep).get(rid)
    if not row or row.get("status") not in OPEN:
        raise SpendRefused("not an open row")
    if not (note or "").strip():
        raise SpendRefused("confirm needs a --note")
    if void:
        if row["status"] != "CANCELLED_UNCLAIMED":
            raise SpendRefused("only CANCELLED_UNCLAIMED rows can be voided (a claimed request cannot be)")
        if not list_dump:
            raise SpendRefused("void needs --list-dump (a saved openart_creation_list for the request window)")
        dump = _read_json(Path(list_dump), None)
        start = time.mktime(datetime.datetime.fromisoformat(row["ts"]).timetuple())
        end = row.get("cancel_ts") or time.time()
        if not dump or not _num(dump.get("from_ts")) or not _num(dump.get("to_ts")) \
                or dump["from_ts"] > start or dump["to_ts"] < end:
            raise SpendRefused("the list dump does not cover the request's time window")
        if any(c.get("prompt_sha256") == row["prompt_sha256"] for c in dump.get("creations", [])):
            raise SpendRefused("the list dump shows a creation for this request: it was paid, use fetch")
        mark(ep, rid, "voided", void_note=note)
        return True, "voided"
    if row["provider"] == "openart":
        if not receipt:
            raise SpendRefused("an OpenArt row needs --receipt <saved creation record dump>; "
                               "a typed amount alone is refused")
        rec = _read_json(Path(receipt), None)
        if not isinstance(rec, dict) or not (rec.get("creation_id") or row.get("creation_id")):
            raise SpendRefused("the dump has no creation_id")
        if not row.get("creation_id"):
            mark(ep, rid, creation_id=rec["creation_id"])
        ob.RECEIPTS_DIR.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(receipt, ob.RECEIPTS_DIR / f"{rid}.json")
        ok, why = _settle(ep, rid, rec, allow_over=True)
        if not ok:
            mark(ep, rid, "UNRESOLVED", error=why)
        return ok, why
    if not _num(amount) or amount < 0:
        raise SpendRefused("an ElevenLabs row needs --amount (usd)")
    mark(ep, rid, "confirmed", credits_spent=float(amount), confirm_note=note,
         over_price=bool(amount > row["price"] * CONFIRM_TOLERANCE + 1e-9))
    return True, "confirmed"


def reconcile(ep_dir: Path, creations: list[dict], episode_prompt_hashes: set[str]) -> list[dict]:
    """Detective ($0): creations whose prompt matches an episode prompt but that are not in the log."""
    known = {r.get("creation_id") for r in read_log(ep_dir).values()}
    return [c for c in creations if c.get("prompt_sha256") in episode_prompt_hashes
            and c.get("creation_id") not in known]


# ------------------------------------------------------- ElevenLabs boundary ---
def eleven_price_voice(chars_narrator_uncached: int, chars_character_uncached: int) -> float:
    return round((chars_narrator_uncached * 2 + chars_character_uncached * 2) * ELEVEN_USD_PER_CHAR, 4)


def eleven_before(ep_dir: Path, command: str, price_usd: float, input_sha256: str = "") -> dict:
    """The fixed ElevenLabs commands only. One open row; `align` once per audio hash."""
    if command not in ELEVEN_COMMANDS:
        raise SpendRefused(f"{command!r} is not a whitelisted paid command {ELEVEN_COMMANDS}")
    ep = Path(ep_dir)
    step = ELEVEN_STEP[command]
    if not _num(price_usd) or price_usd <= 0:
        raise SpendRefused("price unknown")
    with _lock(ep):
        if command == "align":
            if not gate_valid(ep, "voice_ear"):
                raise SpendRefused("align runs only after a valid voice_ear (the chosen take)")
            if any(r.get("kind") == "align" and r.get("input_sha256") == input_sha256 and r.get("status") != "voided"
                   for r in read_log(ep).values()):
                raise SpendRefused("alignment was already bought for this narration.mp3 (once per audio hash)")
        _check_common(ep, step, command, command, price_usd, allow_closed=(command == "align"))
        row = {"id": uuid.uuid4().hex, "ts": datetime.datetime.now().isoformat(timespec="milliseconds"),
               "ts_update": time.time(), "step": step, "unit": command, "kind": command,
               "provider": "elevenlabs", "price": float(price_usd), "cur": "usd", "status": "requested",
               "input_sha256": input_sha256, "rate_verified": ELEVEN_RATES_VERIFIED}
        _append(ep, row)
    return row


def eleven_finish(ep_dir: Path, rid: str, ok: bool, detail: str = "") -> None:
    """The row stays OPEN until `confirm --amount` (or the history receipt, probe R3, unverified)."""
    mark(ep_dir, rid, "UNRESOLVED", error=None if ok else detail, awaiting="confirm --amount")


# --------------------------------------------------------------------- summary ---
def spend_summary(ep_dir: Path) -> dict:
    out = {}
    try:
        gs = grants(ep_dir)
    except SpendRefused:
        gs = []
    for step in STEPS:
        live = [g for g in gs if g["step"] == step]
        if live:
            out[step] = {"cap": sum(g["cap"] for g in live), "spent": spent(ep_dir, step),
                         "cur": STEPS[step]["cur"], "grants": len(live)}
    return out
