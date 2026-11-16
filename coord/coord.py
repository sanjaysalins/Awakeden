"""coord.py - the ONE way lanes touch the board. $0, no network.
  coord.py status
  coord.py add <piece> <lane> [stage]         (coordinator adds a piece)
  coord.py claim <piece> <lane> <session>     (fails if another lane/session holds it)
  coord.py stage <piece> <lane> <stage> [msg] (owner only)
  coord.py ready <piece> <lane> <final_path>  (owner only; hands to coordinator)
  coord.py release <piece> <lane>
  coord.py note <lane> <text>                 (append to coord/notes/<lane>.md)
  coord.py check <lane> <path>                (is this path allowed for this lane?)
Run:  .venv/Scripts/python.exe coord/coord.py <command>"""
import json, os, sys, time
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent; B = ROOT / "coord" / "BOARD.json"; LOCK = ROOT / "coord" / ".lock"
STAGES = ["idea", "words_locked", "recorded", "visuals", "film", "sound", "packaging", "ready", "uploaded"]

def locked(fn):
    def w(*a):
        t0 = time.time()
        while True:
            try: fd = os.open(LOCK, os.O_CREAT | os.O_EXCL | os.O_WRONLY); break
            except FileExistsError:
                if time.time() - t0 > 15: sys.exit("board busy (stale coord/.lock? delete it if no one is writing)")
                time.sleep(0.2)
        try: return fn(*a)
        finally: os.close(fd); os.unlink(LOCK)
    return w

def load(): return json.loads(B.read_text(encoding="utf-8"))
def save(d): B.write_text(json.dumps(d, indent=1), encoding="utf-8")
def now(): return time.strftime("%Y-%m-%d %H:%M")

def status():
    d = load()
    for pid, p in d["pieces"].items():
        print("%-34s lane=%-7s stage=%-12s owner=%s  %s" % (pid, p["lane"], p["stage"], p.get("owner") or "-", p.get("msg", "")))
    if not d["pieces"]: print("(no pieces yet)")

@locked
def add(pid, lane, stage="idea"):
    d = load()
    if lane not in d["lanes"]: sys.exit("unknown lane")
    if pid in d["pieces"]: sys.exit("exists")
    d["pieces"][pid] = dict(lane=lane, stage=stage, owner=None, updated=now()); save(d); print("added", pid)

@locked
def claim(pid, lane, session):
    d = load(); p = d["pieces"].get(pid) or sys.exit("no such piece")
    if p["lane"] != lane: sys.exit("piece belongs to lane %s" % p["lane"])
    if p.get("owner") and p["owner"] != session: sys.exit("already claimed by " + p["owner"])
    p["owner"] = session; p["updated"] = now(); save(d); print("claimed", pid)

def _own(d, pid, lane):
    p = d["pieces"].get(pid) or sys.exit("no such piece")
    if p["lane"] != lane: sys.exit("not your lane")
    if not p.get("owner"): sys.exit("claim it first")
    return p

@locked
def stage(pid, lane, st, msg=""):
    d = load(); p = _own(d, pid, lane)
    if st not in STAGES: sys.exit("stage must be one of %s" % STAGES)
    p["stage"] = st; p["msg"] = msg; p["updated"] = now(); save(d); print(pid, "->", st)

@locked
def ready(pid, lane, final):
    d = load(); p = _own(d, pid, lane)
    if not (ROOT / final).is_file(): sys.exit("final file not found: " + final)
    p.update(stage="ready", final=final, owner=None, updated=now(), msg="handed to coordinator"); save(d); print(pid, "READY for coordinator")

@locked
def release(pid, lane):
    d = load(); p = _own(d, pid, lane); p["owner"] = None; save(d); print("released", pid)

def note(lane, text):
    d = load(); f = ROOT / d["lanes"][lane]["note_file"]; f.parent.mkdir(exist_ok=True)
    with open(f, "a", encoding="utf-8") as fh: fh.write("- %s  %s\n" % (now(), text))
    print("noted")

def check(lane, path):
    d = load(); rel = str(Path(path).resolve().relative_to(ROOT)).replace("\\", "/")
    for c in d["coordinator_only"]:
        if rel == c.rstrip("/") or rel.startswith(c if c.endswith("/") else c + "/"): print("NO: coordinator-only ->", c); sys.exit(1)
    for o in d["lanes"][lane]["owns"]:
        if rel.startswith(o): print("OK: lane", lane, "owns", o); return
    print("NO: not in lane %s areas %s (ask the coordinator)" % (lane, d["lanes"][lane]["owns"])); sys.exit(1)

if __name__ == "__main__":
    a = sys.argv[1:]
    cmd = {"status": status, "add": add, "claim": claim, "stage": stage, "ready": ready, "release": release, "note": note, "check": check}.get(a[0] if a else "")
    if not cmd: sys.exit(__doc__)
    cmd(*a[1:])
