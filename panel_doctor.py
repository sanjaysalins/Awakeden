"""panel_doctor.py — health check for the independent-review AI panel.

A "doctor" for the local-CLI reviewer panel used by independent_review.py.
Three checks, each independent:

  1) INSTALL   — is each reviewer CLI reachable + does it answer --version?
  2) HISTORY   — scan every _independent_review/*/INDEX.md: per-reviewer OK/FAIL
                 rate, runs that ran on a DEGRADED panel (<min healthy voices),
                 and garbled/echoed verdict strings.
  3) SMOKE     — (opt-in, --smoke) send a 1-line review through each live CLI and
                 confirm a clean VERDICT comes back, with a hard per-CLI timeout.

Read-only except for an optional report file. No metered API (mirrors the panel:
strips API keys so each CLI uses its free subscription login).

Usage:
  .venv\\Scripts\\python.exe panel_doctor.py                 # install + history
  .venv\\Scripts\\python.exe panel_doctor.py --smoke         # + live smoke test
  .venv\\Scripts\\python.exe panel_doctor.py --root .        # scan a subtree
  .venv\\Scripts\\python.exe panel_doctor.py --json out.json # machine-readable
"""
from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import time
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

# Reuse the SAME provider table the real panel uses, so the doctor checks exactly
# what runs in production. If that import ever breaks, the panel is broken too.
try:
    from independent_review import PROVIDERS, build_cmd, resolve
except Exception as e:  # pragma: no cover
    print(f"[doctor] cannot import independent_review: {e}", file=sys.stderr)
    sys.exit(2)

VALID_VERDICTS = {"PASS", "REVISE", "FAIL"}
MIN_HEALTHY = 4  # a panel run with fewer than this many OK reviewers is "degraded"

# A tiny artifact the live smoke test reviews — clean, should come back PASS-ish.
SMOKE_PROMPT = (
    "You are a reviewer. Reply with one short sentence, then EXACTLY this block:\n"
    "VERDICT: PASS | REVISE | FAIL\nTOP FIXES:\n1. <fix>\n\n"
    "----- ARTIFACT START -----\n"
    "For God so loved the world, that he gave his only begotten Son.\n"
    "----- ARTIFACT END -----\n"
)

GREEN, YELLOW, RED, DIM, BOLD, RESET = (
    "\033[32m", "\033[33m", "\033[31m", "\033[2m", "\033[1m", "\033[0m"
)


def dot(state: str) -> str:
    return {"ok": GREEN + "GREEN " + RESET,
            "warn": YELLOW + "YELLOW" + RESET,
            "bad": RED + "RED   " + RESET}.get(state, state)


# ---------------------------------------------------------------- 1) INSTALL ---
def check_install(names: list[str], timeout: int = 25) -> dict:
    out = {}
    for n in names:
        cfg = PROVIDERS[n]
        exe = resolve(cfg["command"])
        if not exe:
            out[n] = {"installed": False, "path": None, "version": None,
                      "state": "bad", "note": "not on PATH"}
            continue
        ver, note = None, ""
        try:
            r = subprocess.run(build_cmd(exe, ["--version"]), capture_output=True,
                               text=True, timeout=timeout, encoding="utf-8",
                               errors="replace", stdin=subprocess.DEVNULL)
            ver = (r.stdout or r.stderr or "").strip().splitlines()
            ver = ver[0] if ver else ""
        except subprocess.TimeoutExpired:
            note = "version check hung"
        except Exception as e:
            note = f"version error: {e}"
        out[n] = {"installed": True, "path": exe, "version": ver,
                  "state": "ok" if not note else "warn", "note": note}
    return out


# ---------------------------------------------------------------- 2) HISTORY ---
def parse_index(p: Path) -> dict | None:
    """Parse an INDEX.md into {artifact, kind, stamp, rows:[{name,ok,secs,verdict}]}."""
    txt = p.read_text(encoding="utf-8", errors="replace")
    head = re.search(r"#\s*Independent review index\s*[—-]\s*(.+?)\s*\((\w+)\)", txt)
    rows = []
    for m in re.finditer(
        r"-\s*\*\*(\w+)\*\*\s*[—-]\s*(OK|FAILED)\s*\((\d+)s\)\s*[—-]\s*verdict:\s*(.*?)\s*[—-]\s*`",
        txt,
    ):
        name, status, secs, verdict = m.groups()
        rows.append({"name": name, "ok": status == "OK",
                     "secs": int(secs), "verdict": verdict.strip()})
    if not rows:
        return None
    return {"artifact": head.group(1) if head else p.parent.parent.name,
            "kind": head.group(2) if head else "?",
            "stamp": p.parent.name, "path": str(p), "rows": rows}


def verdict_clean(v: str) -> str | None:
    """Return the single clean verdict, or None if garbled/echoed/missing."""
    v = (v or "").strip().strip("*").strip()
    if not v or v == "—":
        return None
    token = v.split()[0].strip("*").upper()
    # echoed template ("PASS | REVISE | FAIL") => more than one valid token present
    present = [w for w in VALID_VERDICTS if re.search(rf"\b{w}\b", v.upper())]
    if len(present) > 1:
        return None
    return token if token in VALID_VERDICTS else None


def check_history(root: Path) -> dict:
    indexes = sorted(root.rglob("_independent_review/*/INDEX.md"))
    runs = [r for r in (parse_index(p) for p in indexes) if r]
    per = defaultdict(lambda: {"ok": 0, "fail": 0, "garbled": 0, "secs": []})
    degraded, garbled_rows = [], []
    for run in runs:
        healthy = sum(1 for r in run["rows"] if r["ok"])
        if healthy < MIN_HEALTHY:
            degraded.append({"artifact": run["artifact"], "stamp": run["stamp"],
                             "healthy": healthy, "total": len(run["rows"]),
                             "path": run["path"]})
        for r in run["rows"]:
            s = per[r["name"]]
            if r["ok"]:
                s["ok"] += 1
                s["secs"].append(r["secs"])
                if r["verdict"] and verdict_clean(r["verdict"]) is None:
                    s["garbled"] += 1
                    garbled_rows.append({"name": r["name"], "artifact": run["artifact"],
                                         "stamp": run["stamp"], "verdict": r["verdict"]})
            else:
                s["fail"] += 1
    # grade each reviewer
    for n, s in per.items():
        total = s["ok"] + s["fail"]
        rate = s["ok"] / total if total else 0
        s["total"] = total
        s["ok_rate"] = round(rate, 3)
        s["avg_secs"] = round(sum(s["secs"]) / len(s["secs"])) if s["secs"] else 0
        s["state"] = "ok" if rate >= 0.9 and not s["garbled"] else (
            "bad" if rate < 0.75 else "warn")
    return {"n_runs": len(runs), "per": dict(per),
            "degraded": degraded, "garbled": garbled_rows}


# ------------------------------------------------------------------ 3) SMOKE ---
def smoke_one(name: str) -> dict:
    cfg = PROVIDERS[name]
    exe = resolve(cfg["command"])
    if not exe:
        return {"name": name, "state": "bad", "note": "not installed", "secs": 0}
    args = list(cfg["args"])
    payload = (cfg.get("prefix", "") + "\n\n" + SMOKE_PROMPT).strip()
    tmp = None
    if cfg["mode"] == "file":
        tmp = Path(os.environ.get("TEMP", ".")) / f"_doctor_{name}.txt"
        tmp.write_text(payload, encoding="utf-8")
        args = [a.replace("{prompt_file}", str(tmp)) for a in args]
        stdin_payload = None
    else:
        stdin_payload = payload
    env = dict(os.environ)
    if os.getenv("JITB_PANEL_USE_API", "0") not in ("1", "true", "yes"):
        for k in ("ANTHROPIC_API_KEY", "GEMINI_API_KEY", "GOOGLE_API_KEY", "OPENAI_API_KEY"):
            env.pop(k, None)
    t = time.monotonic()
    try:
        r = subprocess.run(build_cmd(exe, args), input=stdin_payload, env=env,
                           capture_output=True, text=True, encoding="utf-8",
                           errors="replace", timeout=cfg["timeout"],
                           stdin=None if stdin_payload is not None else subprocess.DEVNULL)
        secs = round(time.monotonic() - t)
        out = (r.stdout or "").strip()
        v = verdict_clean(out.split("VERDICT:")[-1]) if "VERDICT:" in out else None
        if r.returncode == 0 and v:
            return {"name": name, "state": "ok", "secs": secs, "verdict": v}
        return {"name": name, "state": "warn" if out else "bad", "secs": secs,
                "note": f"no clean verdict (exit {r.returncode}, {len(out)} chars)"}
    except subprocess.TimeoutExpired:
        return {"name": name, "state": "bad", "secs": round(time.monotonic() - t),
                "note": f"HUNG > {cfg['timeout']}s"}
    finally:
        if tmp:
            tmp.unlink(missing_ok=True)


def check_smoke(names: list[str]) -> list[dict]:
    with ThreadPoolExecutor(max_workers=len(names)) as ex:
        return list(ex.map(smoke_one, names))


# -------------------------------------------------------------------- report ---
def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--root", default=".", help="subtree to scan for review history")
    ap.add_argument("--providers", default=",".join(PROVIDERS))
    ap.add_argument("--smoke", action="store_true", help="run a live 1-line review per CLI")
    ap.add_argument("--json", dest="json_out", default="", help="write machine-readable report")
    args = ap.parse_args()
    names = [n.strip() for n in args.providers.split(",") if n.strip() in PROVIDERS]

    print(f"{BOLD}=== AI panel doctor ==={RESET}")
    report: dict = {}

    print(f"\n{BOLD}1) INSTALL{RESET}  (is each reviewer reachable?)")
    inst = check_install(names)
    report["install"] = inst
    for n in names:
        d = inst[n]
        loc = d["path"] or "—"
        extra = (d["version"] or "") + (f"  {RED}{d['note']}{RESET}" if d["note"] else "")
        print(f"  {dot(d['state'])} {n:<8} {DIM}{loc}{RESET}  {extra}")

    print(f"\n{BOLD}2) HISTORY{RESET}  (scanning {args.root} for past runs)")
    hist = check_history(Path(args.root))
    report["history"] = hist
    print(f"  {hist['n_runs']} review runs found\n")
    print(f"  {'reviewer':<8} {'OK rate':>9} {'runs':>5} {'avg s':>6} {'garbled':>8}  status")
    for n in names:
        s = hist["per"].get(n)
        if not s:
            print(f"  {n:<8} {DIM}(no history){RESET}")
            continue
        print(f"  {n:<8} {s['ok_rate']*100:7.0f}% {s['total']:5d} {s['avg_secs']:6d} "
              f"{s['garbled']:8d}  {dot(s['state'])}")
    if hist["degraded"]:
        print(f"\n  {RED}DEGRADED runs (< {MIN_HEALTHY} healthy voices):{RESET}")
        for d in hist["degraded"]:
            print(f"    - {d['artifact']} @ {d['stamp']}: only {d['healthy']}/{d['total']} OK")
            print(f"      {DIM}{d['path']}{RESET}")
    if hist["garbled"]:
        print(f"\n  {YELLOW}Garbled/echoed verdicts:{RESET}")
        for g in hist["garbled"]:
            print(f"    - {g['name']} on {g['artifact']} @ {g['stamp']}: "
                  f"\"{g['verdict'][:40]}\"")

    if args.smoke:
        print(f"\n{BOLD}3) SMOKE{RESET}  (live 1-line review through each CLI — may take a few min)")
        sm = check_smoke(names)
        report["smoke"] = sm
        for d in sorted(sm, key=lambda x: x["name"]):
            note = f"verdict={d.get('verdict')}" if d["state"] == "ok" else d.get("note", "")
            print(f"  {dot(d['state'])} {d['name']:<8} {d['secs']:4d}s  {note}")

    # overall
    bad = [n for n in names if inst[n]["state"] == "bad"
           or hist["per"].get(n, {}).get("state") == "bad"]
    warn = [n for n in names if n not in bad and (inst[n]["state"] == "warn"
            or hist["per"].get(n, {}).get("state") == "warn")]
    print(f"\n{BOLD}=== diagnosis ==={RESET}")
    if bad:
        print(f"  {RED}UNHEALTHY:{RESET} {', '.join(bad)}")
    if warn:
        print(f"  {YELLOW}WATCH:{RESET}     {', '.join(warn)}")
    healthy = [n for n in names if n not in bad and n not in warn]
    if healthy:
        print(f"  {GREEN}HEALTHY:{RESET}   {', '.join(healthy)}")
    if hist["degraded"]:
        print(f"  {RED}{len(hist['degraded'])} past run(s) ran on a degraded panel — "
              f"consider re-reviewing those.{RESET}")

    if args.json_out:
        Path(args.json_out).write_text(json.dumps(report, indent=2), encoding="utf-8")
        print(f"\n[doctor] json -> {Path(args.json_out).resolve()}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
