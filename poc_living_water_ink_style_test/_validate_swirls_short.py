"""$0 offline tests for the Swirls SHORT pipeline (design v3.2 section 9.3: T1 .. T14). Synthetic data
only (tiny ffmpeg-generated clips and images in a temp dir), a temp bridge folder, a FAKE servicer
thread and mocks under every outside tool (speech tools, aligner, whisper, Vision, score). No paid API,
no OpenArt MCP call, no ElevenLabs call, no real episode file written: requests.post is patched to RAISE
for the whole run, so nothing here can bill.

Run:
  .venv\\Scripts\\python.exe poc_living_water_ink_style_test\\_validate_swirls_short.py
"""
from __future__ import annotations

import contextlib
import dataclasses
import hashlib
import io
import json
import math
import os
import shutil
import subprocess
import sys
import tempfile
import threading
import time
import uuid
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE / "test_the_cross"))
sys.path.insert(0, str(REPO))

# ---- NOTHING here may bill: any network POST is a hard error ---------------------------------
import requests  # noqa: E402


def _no_post(*a, **k):
    raise AssertionError("a network POST was attempted in a $0 test")


requests.post = _no_post
requests.Session.post = _no_post

import openart_bridge as ob  # noqa: E402
import swirls_assemble as sa  # noqa: E402
import swirls_guard as guard  # noqa: E402
import swirls_short as ss  # noqa: E402
import swirls_short_run as run  # noqa: E402
import swirls_verify as sv  # noqa: E402
import build_srt  # noqa: E402
from swirls_assemble import DuckProfile, EpisodeManifest, ScoreVariant, Unit  # noqa: E402
from swirls_cover import CoverSpec  # noqa: E402
from swirls_page import Panel, PageSpec  # noqa: E402

FAILS: list[str] = []
SKIPS: list[str] = []
NAMES: dict[str, list[str]] = {}
CURRENT = ["?"]


def check(label: str, cond: bool, detail: str = "") -> None:
    print(f"[{'PASS' if cond else 'FAIL'}] {label}" + (f" -- {detail}" if detail and not cond else ""))
    NAMES.setdefault(CURRENT[0], []).append(label)
    if not cond:
        FAILS.append(label)


def skip(label: str, why: str) -> None:
    print(f"[SKIP] {label} -- {why}")
    SKIPS.append(f"{label}: {why}")


def section(t: str, title: str) -> None:
    CURRENT[0] = t
    print(f"\n== {t}: {title} ==")


def raises(exc, fn, *a, **k) -> bool:
    try:
        fn(*a, **k)
    except exc:
        return True
    except Exception as e:  # wrong exception type
        print(f"      (raised {type(e).__name__}: {e})")
        return False
    return False


def verdicts(gates, gate=None):
    return [g.verdict for g in gates if gate is None or g.gate == gate or g.gate.startswith(gate + "[")]


def has_fail(gates, gate=None) -> bool:
    return "FAIL" in verdicts(gates, gate)


def ff(*args: str) -> None:
    subprocess.run(["ffmpeg", "-y", "-v", "error", *args], check=True)


def mk_clip(path: Path, seconds: float, size: str = "108x192", moving: bool = True, fps: int = 30) -> Path:
    src = f"testsrc2=s={size}:r={fps}:d={seconds}" if moving else f"color=c=0x884422:s={size}:r={fps}:d={seconds}"
    ff("-f", "lavfi", "-i", src, "-c:v", "libx264", "-preset", "ultrafast", "-pix_fmt", "yuv420p", "-an", str(path))
    return path


def mk_audio(path: Path, seconds: float, freq: int = 300) -> Path:
    ff("-f", "lavfi", "-i", f"sine=frequency={freq}:duration={seconds}", "-c:a", "libmp3lame", str(path))
    return path


def dur(p: Path) -> float:
    return sa.dur(p)


def sha(p) -> str:
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def frame_diffs(mp4: Path, times: list[float]) -> list[float]:
    import numpy as np
    frames = []
    for t in times:
        raw = subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{t:.3f}", "-i", str(mp4), "-frames:v", "1",
                              "-vf", "scale=54:96,format=gray", "-f", "rawvideo", "-"], capture_output=True, check=True).stdout
        frames.append(np.frombuffer(raw, dtype=np.uint8).astype(float))
    return [float(np.abs(a - b).mean()) for a, b in zip(frames, frames[1:])]


def probe_wh(p: Path) -> tuple[int, int, float]:
    pr = ss.probe_output(p)
    return pr["w"], pr["h"], pr["fps"]


# =====================================================================================
tmp = Path(tempfile.mkdtemp(prefix="swirls_short_test_"))
BRIDGE = tmp / "bridge"
ob.configure(BRIDGE)
ob.POLL_SECONDS = 0.03
ob.HEARTBEAT_SECONDS = 0.1
ob.TIMEOUT_SECONDS = 30.0
ob.HEARTBEAT_STALE_SECONDS = 60.0
import config  # noqa: E402
config.LLM_PROVIDER = "agent"      # the Vision READ goes through a mock below, never through the metered API

try:
    # ===================================================================== T1 / T2 ===
    section("T1", "trim: frame-exact cuts, scale-and-crop, 1080x1920, no fill")
    ed = tmp / "ep_a"
    ed.mkdir()
    narr = mk_audio(ed / "narration.mp3", 6.0)
    # fractional slots: front 0-2.4, f01 2.4-4.7, back 4.7-9.0  (frames 72 / 69 / 129 = 270)
    timing = {"schema": "x", "units": {"front": {"start_s": 0.0, "end_s": 2.4}, "f01": {"start_s": 2.4, "end_s": 4.7},
                                       "back": {"start_s": 4.7, "end_s": 9.0}}}
    (ed / "unit_timing.json").write_text(json.dumps(timing), encoding="utf-8")
    # Kling-sized clips (1072x1928) with a CIRCLE drawn on the first one, to prove no stretch
    circ = ed / "front.mp4"
    ff("-f", "lavfi", "-i", "color=c=black:s=1072x1928:r=30:d=3.2", "-vf",
       "geq=lum='if(lt(hypot(X-536,Y-964),300),255,0)':cb=128:cr=128", "-c:v", "libx264", "-preset", "ultrafast",
       "-pix_fmt", "yuv420p", "-an", str(circ))
    clips = {"front": circ, "f01": mk_clip(ed / "f01.mp4", 3.2, "1072x1928"), "back": mk_clip(ed / "back.mp4", 6.0, "1072x1928")}
    score = mk_audio(ed / "score.mp3", 12.0, freq=220)
    duck = DuckProfile(-12.0, 0.12, 2.5, 250)
    man = EpisodeManifest(
        episode_dir=ed, narration=narr, units=[Unit(t, clips[t], 3, "trim") for t in ("front", "f01", "back")],
        scores={"s": ScoreVariant(score=score, duck=duck, out=ed / "scored.mp4")},
        panel_style="woodcut_hybrid", w=1080, h=1920)
    check("trim episode detected", sa.is_trim_episode(man))
    check("old-mode episode is not trim", not sa.is_trim_episode(EpisodeManifest(ed, narr, [Unit("a", clips["f01"], 1, "freeze")], {}, "ink_wash")))
    check("mixed trim + freeze is an error", raises(ValueError, sa.is_trim_episode, EpisodeManifest(
        ed, narr, [Unit("front", clips["front"], 1, "trim"), Unit("f01", clips["f01"], 1, "freeze")], {}, "ink_wash")))
    check("trim without unit_timing tag is an error", raises(ValueError, sa.is_trim_episode, EpisodeManifest(
        ed, narr, [Unit("zzz", clips["front"], 1, "trim")], {}, "ink_wash")))
    man720 = dataclasses.replace(man, w=720, h=1280)
    check("a 720x1280 trim manifest is REFUSED", raises(ValueError, sa.assemble, man720, None))
    short_man = dataclasses.replace(man, units=[Unit("front", mk_clip(tmp / "s1.mp4", 1.0, "1072x1928"), 3, "trim"),
                                                Unit("f01", clips["f01"], 3, "trim"), Unit("back", clips["back"], 3, "trim")])
    check("a clip shorter than its slot raises ShortClipError (never filled)", raises(sa.ShortClipError, sa.assemble, short_man, None))
    rd = sa.assemble(man, None)
    out_draft = rd["out"]
    w, h, fps = probe_wh(out_draft)
    check("output is exactly 1080x1920 at 30 fps", (w, h) == (1080, 1920) and abs(fps - 30) < 0.01, f"{w}x{h} {fps}")
    frames = [u["frames"] for u in rd["units"]]
    check("cuts at B(k) = round(end_s x 30), counted from the film start (72, 69, 129)", frames == [72, 69, 129], str(frames))
    rec = rd["receipt"]
    check("total frames = round(total x 30) within one frame", abs(rec["total_frames"] - 270) <= 1, str(rec["total_frames"]))
    r0 = ss.lint_assembly(rec, {"narration_seconds": 6.0, "first_word_start_s": 0.1, "units": timing["units"]}, out_draft)
    check("SWS-G15 passes the frame-exact cut", r0[0].verdict == "PASS", r0[0].evidence)
    # a circle stays a circle: measure the bright blob in the first frame of the output
    frm = tmp / "circ.png"
    ff("-i", str(out_draft), "-frames:v", "1", str(frm))
    from PIL import Image
    import numpy as np
    a = np.asarray(Image.open(frm).convert("L"))
    ys, xs = np.where(a > 128)
    ratio = (xs.max() - xs.min() + 1) / (ys.max() - ys.min() + 1)
    check("a circle stays a circle (scale-and-crop, no stretch)", abs(ratio - 1.0) < 0.03, f"w/h = {ratio:.3f}")

    section("T2", "scored trim through mix_tail + draft; legacy freeze untouched")
    r = sa.assemble(man, "s")
    f = r["out"]
    check("scored trim: total = voice + 3.0 s", abs(dur(f) - 9.0) < 0.1, f"{dur(f)}")
    import check_landing_hold
    ok, msg = check_landing_hold.check_parity(f)
    check("scored trim: picture and sound lengths match (<0.1 s)", ok, msg)
    pic, aud = check_landing_hold._durations(f)
    check("scored trim: picture = sound within one frame", pic is not None and aud is not None and abs(pic - aud) <= 1 / 30 + 1e-3, f"{pic} {aud}")
    frozen = tmp / "frozen.mp4"
    ff("-i", str(clips["back"]), "-vf", "trim=end=3,setpts=PTS-STARTPTS,tpad=stop_mode=clone:stop_duration=3",
       "-c:v", "libx264", "-pix_fmt", "yuv420p", "-an", str(frozen))
    frozen_diffs = frame_diffs(frozen, [3.2, 3.7, 4.2, 4.7, 5.2, 5.7])
    check("freeze control really reads as frozen (test has teeth)", max(frozen_diffs) < 0.5, f"{frozen_diffs}")
    check("scored trim: the last 3 s are NOT a frozen frame", min(frame_diffs(f, [6.2, 6.7, 7.2, 7.7, 8.2, 8.7])) > 1.0)
    check("scored trim: G15h moving hold PASSES on the final file", ss.moving_hold(f, 6.0, tmp / "_h1").verdict == "PASS")
    check("the same measure FAILS the frozen control (G15h has teeth)", ss.moving_hold(frozen, 3.0, tmp / "_h2").verdict == "FAIL")
    check("draft written as <episode>_draft.mp4 with assembly_receipt.json", rd["out"].name == "ep_a_draft.mp4" and (ed / "assembly_receipt.json").exists())
    check("scored receipt is separate and chains the draft's", (ed / "assembly_receipt_scored.json").exists() and
          json.loads((ed / "assembly_receipt_scored.json").read_text())["draft_receipt_sha256"] == sha(ed / "assembly_receipt.json"))
    check("draft on an old-mode episode is an error", raises(ValueError, sa.assemble, EpisodeManifest(
        ed, narr, [Unit("a", clips["f01"], 1, "freeze")], {}, "ink_wash"), None))
    # legacy freeze/boomerang: identical ffmpeg argument lists to HEAD (loaded from git, not retyped)
    try:
        head_src = subprocess.run(["git", "show", "HEAD:poc_living_water_ink_style_test/swirls_assemble.py"], cwd=str(REPO),
                                  capture_output=True, text=True, check=True).stdout
        import types
        head = types.ModuleType("swirls_assemble_head")
        head.__dict__["__file__"] = str(HERE / "swirls_assemble.py")
        sys.modules["swirls_assemble_head"] = head
        exec(compile(head_src, "swirls_assemble_HEAD.py", "exec"), head.__dict__)

        def record(mod):
            calls = []
            mod.run = lambda cmd: calls.append([str(x).replace(str(tmp), "<T>") for x in cmd])
            mod.dur = lambda p: 5.0
            lm = mod.EpisodeManifest(ed, narr, [], {}, "ink_wash", w=720, h=1280)
            wk = tmp / "legacy_work"
            wk.mkdir(exist_ok=True)
            mod.make_freeze(clips["f01"], tmp / "o.mp4", 7.0, 3.2, wk, "x", lm)
            mod.make_boomerang(clips["f01"], tmp / "o2.mp4", 7.0, 3.2, wk, "x", lm)
            mod.make_freeze_tail_loop(clips["f01"], tmp / "o3.mp4", 7.0, 3.2, wk, "x", lm)
            return calls
        keep_run, keep_dur = sa.run, sa.dur
        a_calls, b_calls = record(head), record(sa)
        sa.run, sa.dur = keep_run, keep_dur
        check("legacy freeze / boomerang / tail-loop ffmpeg argument lists are identical to HEAD",
              a_calls == b_calls and len(a_calls) > 5, f"{len(a_calls)} vs {len(b_calls)} calls")
    except Exception as e:
        skip("legacy ffmpeg argument-list comparison with HEAD", f"git show failed: {e}")

    # ==================================================================== T3 / T3b ===
    section("T3", "timing maths reproduce ep13's own unit_timing.json (11 units)")

    def write_meta(d: Path, backend="elevenlabs", words=None):
        al = json.loads((d / "narration.alignment.json").read_text(encoding="utf-8"))["words"]
        n = len([w for w in al if any(c.isalnum() for c in w["text"])]) if words is None else words
        (d / "narration.alignment.meta.json").write_text(json.dumps(
            {"audio_sha256": sha(d / "narration.mp3"), "backend": backend, "word_count": n}), encoding="utf-8")

    ep13 = HERE / "swirls_episode_13_the_cross_that_wasnt_his"
    if (ep13 / "narration.alignment.json").exists() and (ep13 / "unit_timing.json").exists():
        d13 = tmp / "ep13_copy"
        d13.mkdir()
        shutil.copy(ep13 / "narration.alignment.json", d13)
        shutil.copy(ep13 / "narration.mp3", d13)
        words13 = [w for w in json.loads((d13 / "narration.alignment.json").read_text(encoding="utf-8"))["words"]
                   if any(c.isalnum() for c in w["text"])]
        counts13 = [("front", 14), ("f01", 25), ("f02", 21), ("f03", 22), ("f04", 14), ("f05", 28),
                    ("f06", 28), ("f07", 17), ("f08", 13), ("f09", 21), ("back", 24)]
        units13, i = {}, 0
        for tag, n in counts13:
            units13[tag] = " ".join(w["text"] for w in words13[i:i + n])
            i += n
        (d13 / "units.json").write_text(json.dumps(units13), encoding="utf-8")
        (d13 / "narration.md").write_text("\n".join(units13.values()), encoding="utf-8")
        (d13 / "narration-tagged.md").write_text("\n\n".join(units13.values()), encoding="utf-8")
        write_meta(d13)
        mine = ss.build_timing(d13)["units"]
        real = json.loads((ep13 / "unit_timing.json").read_text(encoding="utf-8"))["units"]
        check("timing maths = ep13's own unit_timing.json (all 11 units)", len(real) == 11 and all(
            abs(mine[t]["start_s"] - real[t]["start_s"]) < 0.002 and abs(mine[t]["end_s"] - real[t]["end_s"]) < 0.002 for t in real))
    else:
        skip("ep13 timing reproduction", "ep13 files not present")

    section("T3b", "the 8-unit golden fixture (hand-computed) incl. back = ceil(slot + 2.0)")
    gdir = tmp / "golden"
    gdir.mkdir()
    fx = HERE / "fixtures" / "golden_8unit"
    shutil.copy(fx / "narration.alignment.json", gdir)
    shutil.copy(fx / "units.json", gdir)
    expect = json.loads((fx / "expected_unit_timing.json").read_text(encoding="utf-8"))
    mk_audio(gdir / "narration.mp3", expect["narration_seconds"])
    gunits = json.loads((gdir / "units.json").read_text(encoding="utf-8"))
    (gdir / "narration.md").write_text("\n".join(gunits.values()), encoding="utf-8")
    (gdir / "narration-tagged.md").write_text("\n\n".join(gunits.values()), encoding="utf-8")
    write_meta(gdir)
    gd = ss.build_timing(gdir)
    gu = gd["units"]
    check("golden: every start_s / end_s matches the hand-computed fixture", all(
        abs(gu[t]["start_s"] - e["start_s"]) < 0.002 and abs(gu[t]["end_s"] - e["end_s"]) < 0.01 for t, e in expect["units"].items()),
          str({t: (gu[t]["start_s"], gu[t]["end_s"]) for t in gu}))
    check("golden: clip_duration (front max(3,ceil(slot+.5)), pages ceil(slot+.5), back ceil(slot+2.0))",
          all(gu[t]["clip_duration"] == e["clip_duration"] for t, e in expect["units"].items()),
          str({t: gu[t]["clip_duration"] for t in gu}))
    check("golden: frames per unit are B(k)-B(k-1) and sum to round(total x 30) = 1359",
          all(gu[t]["frames"] == e["frames"] for t, e in expect["units"].items()) and sum(u["frames"] for u in gu.values()) == 1359)
    check("golden: the back clip is slot + 2.0 rounded up (10 s for a 7.2 s slot)", gu["back"]["clip_duration"] == 10)
    check("golden timing passes SWS-G2 / G3", not has_fail(ss.lint_timing(gd, None, None, (1080, 1920))))
    cd_bad = json.loads(json.dumps(gd))
    cd_bad["units"]["back"]["clip_duration"] = 8
    check("G3: a back clip of slot + 0.5 (the old rule) FAILs", has_fail(ss.lint_timing(cd_bad), "SWS-G3"))
    check("G3: a 720x1280 manifest FAILs", has_fail(ss.lint_timing(gd, None, None, (720, 1280)), "SWS-G3"))
    check("G3: spec clip_duration differing from unit_timing FAILs", has_fail(ss.lint_timing(gd, {"back": 9}), "SWS-G3"))
    for bad in (2, 16, 4.5, True, None):
        cd = json.loads(json.dumps(gd))
        cd["units"]["f01"]["clip_duration"] = bad
        check(f"G3 illegal clip_duration {bad!r} FAILs", has_fail(ss.lint_timing(cd), "SWS-G3"))
    check("G2 tempo != 1.0 FAILs", has_fail(ss.lint_timing(gd, None, 1.2), "SWS-G2"))
    check("G2 late first word FAILs", has_fail(ss.lint_timing(dict(gd, first_word_start_s=0.9)), "SWS-G2"))
    check("G2 voice 36 s FAILs; 38 s is a WARN", has_fail(ss.lint_timing(dict(gd, narration_seconds=36.0)), "SWS-G2")
          and verdicts(ss.lint_timing(dict(gd, narration_seconds=38.0)), "SWS-G2") == ["CONDITIONAL"])
    sl = json.loads(json.dumps(gd))
    sl["units"]["f01"]["end_s"] = sl["units"]["f01"]["start_s"] + 4.0
    check("G3: a 4.0 s page slot FAILs (under 4.5)", has_fail(ss.lint_timing(sl), "SWS-G3"))
    sl = json.loads(json.dumps(gd))
    sl["units"]["f01"]["end_s"] = sl["units"]["f01"]["start_s"] + 4.7
    check("G3: a 4.7 s page slot is a WARN, not a pass", "CONDITIONAL" in verdicts(ss.lint_timing(sl), "SWS-G3") or has_fail(ss.lint_timing(sl), "SWS-G3"))

    d4 = tmp / "t3_neg"
    d4.mkdir()
    for fn in ("narration.alignment.json", "units.json"):
        shutil.copy(gdir / fn, d4)
    shutil.copy(gdir / "narration.md", d4)
    shutil.copy(gdir / "narration-tagged.md", d4)
    mk_audio(d4 / "narration.mp3", 42.3)
    check("timing REFUSES with no alignment meta", raises(ss.TimingError, ss.build_timing, d4))
    write_meta(d4)
    m = json.loads((d4 / "narration.alignment.meta.json").read_text())
    (d4 / "narration.alignment.meta.json").write_text(json.dumps(dict(m, audio_sha256="0" * 64)), encoding="utf-8")
    check("timing REFUSES a meta for a different narration.mp3 (stale)", raises(ss.TimingError, ss.build_timing, d4))
    write_meta(d4, backend="whisper")
    check("timing REFUSES a whisper-backed alignment (no whisper timing)", raises(ss.TimingError, ss.build_timing, d4))
    write_meta(d4, words=83)
    check("timing REFUSES a meta word_count that does not match", raises(ss.TimingError, ss.build_timing, d4))

    section("T11", "_swirls_anchor_ref returns John 1:19-29")
    from pipeline.upload_engine import _swirls_anchor_ref
    brief = tmp / "_DESIGN_BRIEF.md"
    brief.write_text("John 1:19-29 (Isaiah 40:3 fulfilled; the voice and the Lamb)\n\nnotes", encoding="utf-8")
    check("_swirls_anchor_ref -> John 1:19-29", _swirls_anchor_ref(brief, "JOHN 1") == "John 1:19-29")

    # ======================================================================= T4 / T4b ===
    section("T4", "words + baked-text + prose lints (the design's FAIL cases)")
    UNIT_F02 = "He confessed and denied not I am not the Christ he said plainly"

    def mk_page(pid="f02", **over) -> PageSpec:
        base = dict(
            seq_title="The Desert Voice", frame_label=pid.upper(),
            panels=(Panel("confessed", "a lamp and a scroll on a table"), Panel("denied", "an open hand"),
                    Panel("Christ", "a wooden bowl")),
            still_shot_type="medium wide shot",
            main_scene_animation="the man shifts his weight, then the lamp flame leans.",
            anim_shot_desc="medium wide shot",
            main_scene_still="a lamplit table with two men; a brushstroke of blue ink runs left to right across the dry floor.",
            material_closer="the one brushstroke of blue ink is the only unusual ink on the page, and every figure and the paper beneath them are free of any ink.",
            panel_motions=("the light warms slowly", "haze drifts", "a lamp flame leans gently"),
            fence_kind="none", caption_lines=("he said plainly",), corner_note="",
            include_no_bubble_clause=False, panel_style="woodcut_hybrid", clip_duration=8)
        base.update(over)
        return PageSpec(**base)

    U = {"f02": UNIT_F02}
    good_page = mk_page()
    g4 = lambda **o: ss.lint_baked_text({"f02": mk_page(**o)}, None, U)  # noqa: E731
    check("G4 a clean page passes", g4()[0].verdict == "PASS", g4()[0].evidence)
    check("G4 'MEDIUM TWO-SHOT' (still prose, all caps) FAILs", has_fail(ss.lint_still_prose({"f02": mk_page(still_shot_type="MEDIUM TWO-SHOT")})))
    check("G4 dash caption FAILs", has_fail(g4(caption_lines=("he said - plainly",))))
    check("G4 em dash caption FAILs", has_fail(g4(caption_lines=("he said — plainly",))))
    check("G4 doubled labels FAIL", has_fail(g4(panels=(Panel("denied", "x"), Panel("Denied", "y"), Panel("Christ", "z")))))
    check("G4 label = caption FAILs", has_fail(g4(caption_lines=("denied",))))
    check("G4 label inside the caption FAILs", has_fail(g4(caption_lines=("he said plainly",), panels=(
        Panel("confessed", "x"), Panel("denied", "y"), Panel("said", "z")))))
    check("G4 two-line caption FAILs", has_fail(g4(caption_lines=("he said", "plainly"))))
    check("G4 quote marks FAIL", has_fail(g4(caption_lines=('he "said" plainly',))))
    check("G4 a corner note FAILs (the NOTE is gone)", has_fail(g4(corner_note="NOTE: warm lamp")))
    check("G4 12 reading words FAIL (labels 3+2+2, caption 5)", any("more than 11" in x.evidence for x in g4(
        panels=(Panel("he confessed and", "x"), Panel("denied not", "y"), Panel("the Christ", "z")),
        caption_lines=("not I am not the",))) and has_fail(g4(
        panels=(Panel("he confessed and", "x"), Panel("denied not", "y"), Panel("the Christ", "z")),
        caption_lines=("not I am not the",))))
    long_cap = ss.lint_baked_text({"f02": mk_page(caption_lines=("denied confessed plainly said",))}, None, {"f02": UNIT_F02})
    check("G4 a caption over 28 characters FAILs", has_fail(long_cap) and any("28" in x.evidence for x in long_cap))
    check("G4 a caption that is NOT a run of this unit's spoken words FAILs", has_fail(g4(caption_lines=("he walked home",))))
    check("G4 a label not spoken on its page FAILs", has_fail(g4(panels=(Panel("confessed", "x"), Panel("river", "y"), Panel("Christ", "z")))))
    check("G4 labels out of spoken order FAIL", has_fail(g4(panels=(Panel("Christ", "x"), Panel("denied", "y"), Panel("confessed", "z")))))
    check("G4 SEQ title that differs between pages FAILs", has_fail(ss.lint_baked_text(
        {"f02": good_page, "f03": mk_page("f03", seq_title="Another Name")}, None, {"f02": UNIT_F02, "f03": UNIT_F02})))
    check("G4 frame label not matching the unit FAILs", has_fail(g4(frame_label="F05")))
    cov = CoverSpec(side="front", scene="s", lighting="warm amber over cool grey", title="The Desert Voice", subtitle="John 1:19-29",
                    title_position="top", animation="a", clip_duration=4)
    HOOK = "Who answers the desert voice"
    check("G4 front cover with a Scripture ref and the hook's key word passes",
          ss.lint_baked_text({}, {"front": cov}, {"front": HOOK})[0].verdict == "PASS", ss.lint_baked_text({}, {"front": cov}, {"front": HOOK})[0].evidence)
    check("G4 cover title with a digit FAILs", has_fail(ss.lint_baked_text({}, {"front": dataclasses.replace(cov, title="Psalm 41 Now")}, {"front": HOOK})))
    check("G4 cover title that misses the hook's key word FAILs", has_fail(ss.lint_baked_text({}, {"front": dataclasses.replace(cov, title="Wild Bread")}, {"front": HOOK})))
    check("G4 cover subtitle that is not one reference FAILs", has_fail(ss.lint_baked_text({}, {"front": dataclasses.replace(cov, subtitle="John and Isaiah")}, {"front": HOOK})))
    check("G5 digit FAILs", has_fail(ss.lint_still_prose({"f02": mk_page(main_scene_still="three men, 2 lamps")})))
    check("G5 verification verb FAILs", has_fail(ss.lint_still_prose({"f02": mk_page(main_scene_still="make sure the hand is closed")})))
    for noun in ("thread", "cord", "ribbon", "drip", "bloom", "ring", "glow", "puddle"):
        check(f"G5 motif noun {noun!r} FAILs", has_fail(ss.lint_still_prose({"f02": mk_page(main_scene_still=f"a blue {noun} crosses the table")})))
    check("G5 clean prose passes", ss.lint_still_prose({"f02": good_page})[0].verdict == "PASS")
    check("G5a clean clip prose passes", ss.lint_clip_prose({"f02": good_page})[0].verdict == "PASS")
    check("G5a motif named in the clip FAILs", has_fail(ss.lint_clip_prose({"f02": mk_page(main_scene_animation="the blue ink moves")})))
    for verb in ("says", "speak", "whisper", "shouts", "calls out", "cries", "answers", "replied", "preach", "proclaims", "announces",
                 "exclaim", "prays", "murmurs", "sings", "his lips", "the mouth", "a voice"):
        check(f"G5a speech word {verb!r} FAILs", has_fail(ss.lint_clip_prose({"f02": mk_page(main_scene_animation=f"the man {verb} softly")})))
    check("G5a three negatives FAIL", has_fail(ss.lint_clip_prose({"f02": mk_page(main_scene_animation="no new figure, never a bubble, without a mark")})))
    check("G5a fence on FAILs", has_fail(ss.lint_clip_prose({"f02": mk_page(fence_kind="stain", fence_callout="x")})))
    check("G5a bubble clause on FAILs", has_fail(ss.lint_clip_prose({"f02": mk_page(include_no_bubble_clause=True)})))
    plan_ok = {"north_star": "f04", "units": {t: {"full_figures": 2, "crowd": False, "motion_carrier": "a lamp",
                                                   "motif_stage": s, "subjects": []} for t, s in ss.MOTIF_STAGE.items()}}
    check("G6 dosage 0,0,1,1,2,2,3,3 passes", ss.lint_dosage(plan_ok)[0].verdict == "PASS")
    bp = json.loads(json.dumps(plan_ok))
    bp["units"]["f04"]["motif_stage"] = 1
    check("G6 wrong dosage FAILs", has_fail(ss.lint_dosage(bp)))
    check("G6 missing plan FAILs", has_fail(ss.lint_dosage(None)))
    check("G6 stage-0 page with the stage-1 closer FAILs", has_fail(ss.lint_dosage(plan_ok, {"f01": good_page})))

    # ---- word shape G1 / G1e
    def mk_units(counts, extra=None):
        u = {}
        for tag, n in zip(ss.TAGS, counts):
            u[tag] = " ".join(f"x{i}" for i in range(n))
        return u

    base_counts = [5, 12, 12, 12, 12, 12, 12, 9]
    ok_voiced = {"f01": 1, "f02": 1, "f04": 1}
    gw = ss.lint_words(mk_units(base_counts), ok_voiced)
    check("G1 / G1e: a good 86-word film passes", all(g.verdict == "PASS" for g in gw), str([g.evidence for g in gw]))
    check("G1 a 6-word hook FAILs", has_fail(ss.lint_words(mk_units([6] + base_counts[1:]), ok_voiced), "SWS-G1"))
    check("G1 a 3-word hook FAILs", has_fail(ss.lint_words(mk_units([3] + base_counts[1:]), ok_voiced), "SWS-G1"))
    check("G1 94 words FAIL", has_fail(ss.lint_words(mk_units([5, 14, 14, 14, 14, 14, 14, 5]), ok_voiced), "SWS-G1"))
    check("G1 6 voiced quotes FAIL", has_fail(ss.lint_words(mk_units(base_counts), {f"f0{i}": 1 for i in range(1, 7)}), "SWS-G1"))
    check("G1 2 quotes on one page FAIL", has_fail(ss.lint_words(mk_units(base_counts), {"f02": 2}), "SWS-G1"))
    check("G1 a page of 10 words is a WARN (not a pass)", "CONDITIONAL" in verdicts(ss.lint_words(mk_units([5, 10, 12, 12, 12, 12, 14, 9]), ok_voiced), "SWS-G1"))
    check("G1 a page of 9 words FAILs", has_fail(ss.lint_words(mk_units([5, 9, 12, 12, 12, 12, 14, 9]), ok_voiced), "SWS-G1"))
    check("G1 an 11-word last line FAILs", has_fail(ss.lint_words(mk_units(base_counts[:-1] + [11]), ok_voiced), "SWS-G1"))
    check("G1 not 8 units FAILs", has_fail(ss.lint_words({"front": "hi there"}), "SWS-G1"))
    check("G1e a film that is too long by estimate FAILs", has_fail(ss.lint_words(mk_units([5, 14, 14, 14, 14, 14, 14, 10]), ok_voiced), "SWS-G1e")
          or has_fail(ss.lint_words(mk_units([5, 14, 14, 14, 14, 14, 14, 10]), ok_voiced), "SWS-G1"))
    check("G1v: a character line with no emotion cue FAILs", has_fail(ss.lint_speakers({"f02": {"speaker": "john", "voiced": 1, "cue_missing": ["john"]}})))

    section("T4b", "page_plan.json: one schema, validated on load")
    pd = tmp / "plan_ep"
    pd.mkdir()
    (pd / "page_plan.json").write_text(json.dumps(plan_ok), encoding="utf-8")
    pl, pg = ss.load_page_plan(pd)
    check("the design's example page_plan.json loads", pl is not None and pg[0].verdict == "PASS", pg[0].evidence)
    for field in ("full_figures", "crowd", "motion_carrier", "motif_stage", "subjects"):
        bad = json.loads(json.dumps(plan_ok))
        del bad["units"]["f03"][field]
        (pd / "page_plan.json").write_text(json.dumps(bad), encoding="utf-8")
        check(f"missing {field} = FAIL on load", ss.load_page_plan(pd)[0] is None and ss.load_page_plan(pd)[1][0].verdict == "FAIL")
    bad = json.loads(json.dumps(plan_ok))
    del bad["north_star"]
    (pd / "page_plan.json").write_text(json.dumps(bad), encoding="utf-8")
    check("missing north_star = FAIL on load", ss.load_page_plan(pd)[0] is None)
    old_shape = {"units": {"f01": {"heads": 2, "recurring": [], "turn": False, "motif_stage": 0}}}
    (pd / "page_plan.json").write_text(json.dumps(old_shape), encoding="utf-8")
    check("the OLD shape (heads / recurring / turn) is FAIL, not silently vacuous", ss.load_page_plan(pd)[0] is None)
    rj = tmp / "refs.json"
    plan_r = json.loads(json.dumps(plan_ok))
    for t in ("f01", "f02"):
        plan_r["units"][t]["subjects"] = ["John", "Priest"]
    rj.write_text(json.dumps({"refs": [{"name": "John", "file": "john.png"}]}), encoding="utf-8")
    check("G7a: an undeclared subject on 2+ units FAILs", has_fail(ss.lint_refs_declared(plan_r, rj)))
    rj.write_text(json.dumps({"refs": [{"name": "John", "file": "j.png"}, {"name": "Priest", "file": "p.png"}]}), encoding="utf-8")
    check("G7a: all declared passes", ss.lint_refs_declared(plan_r, rj)[0].verdict == "PASS")
    sp = {t: "" for t in ss.TAGS}
    sp["f04"] = "john"
    plan_g8 = json.loads(json.dumps(plan_ok))
    plan_g8["units"]["f04"]["motion_carrier"] = "john"
    check("G8: the north-star page with only its speaker to move FAILs", has_fail(ss.lint_motion_carrier(plan_g8, sp)))
    plan_g8["units"]["f04"]["motion_carrier"] = "a reed"
    check("G8: a carrier other than the speaker passes", ss.lint_motion_carrier(plan_g8, sp)[0].verdict == "PASS")
    sp2 = dict(sp, f01="priest", f02="john")
    plan_g8b = json.loads(json.dumps(plan_ok))
    for t in ("f01", "f02"):
        plan_g8b["units"][t]["motion_carrier"] = ""
    check("G8: two speaker-only pages FAIL", has_fail(ss.lint_motion_carrier(plan_g8b, sp2)))
    check("G8: one speaker-only page is a WARN", verdicts(ss.lint_motion_carrier(plan_g8b, dict(sp, f01="priest"))) == ["CONDITIONAL"])
    check("G8t: the same tags in the same order passes", ss.lint_order({"a": ss.TAGS, "b": list(ss.TAGS)})[0].verdict == "PASS")
    sw = list(ss.TAGS)
    sw[2], sw[3] = sw[3], sw[2]
    check("G8t: swapped unit order FAILs", has_fail(ss.lint_order({"MANIFEST": ss.TAGS, "page_plan": sw})))

    # ========================================================================== T5 / T5b ===
    section("T5", "KJV wrapper (in lane): continuous whole-word, case-sensitive, no ellipsis, no network")
    from pipeline import kjv_strict
    NARR = ("He said, I am the voice of one crying in the wilderness, Prepare ye the way of the LORD. "
            "Who art thou? And he confessed, and denied not. I am not the Christ. Art thou that prophet? Behold the Lamb of God, here he is.")
    chunks = [("narrator", "He said"), ("john", "I am the voice of one crying in the wilderness,")]

    def kj(ref, text, narr=NARR, ch=None):
        return ss.lint_kjv([{"ref": ref, "speaker": "narrator", "text": text}], narr, ch or [])
    check("KJV: the 10-word John 1:23 run PASSES", kj("John 1:23", "I am the voice of one crying in the wilderness,")[0].verdict == "PASS",
          kj("John 1:23", "I am the voice of one crying in the wilderness,")[0].evidence)
    check("KJV: 'Prepare ye the way of the LORD' PASSES", kj("Isaiah 40:3", "Prepare ye the way of the LORD")[0].verdict == "PASS")
    check("KJV: 'I am not the Christ.' (John 1:20) PASSES", kj("John 1:20", "I am not the Christ.")[0].verdict == "PASS")
    check("KJV: across two verses (John 1:19-20) a continuous run PASSES",
          kj("John 1:19-20", "Who art thou? And he confessed, and denied not")[0].verdict == "PASS",
          kj("John 1:19-20", "Who art thou? And he confessed, and denied not")[0].evidence)
    # the shared verifier is fooled by an ellipsis splice; the wrapper is not
    check("the shared kjv_strict.verify_span ACCEPTS 'I am ... the Christ' (why a wrapper exists)",
          kjv_strict.verify_span("John 1:20", "I am ... the Christ")[0] == "OK")
    check("KJV: 'I am ... the Christ' (John 1:20) FAILs", has_fail(kj("John 1:20", "I am ... the Christ")))
    check("KJV: 'I am … that prophet' FAILs", has_fail(kj("John 1:21", "I am … that prophet")))
    check("KJV: a match inside a word ('am not the Chr') FAILs", has_fail(kj("John 1:20", "am not the Chr")))
    check("KJV: wrong case ('Lord' for 'LORD') FAILs", has_fail(kj("Isaiah 40:3", "Prepare ye the way of the Lord")))
    check("KJV: a run that skips a word FAILs", has_fail(kj("Isaiah 40:3", "Prepare the way of the LORD")))
    check("KJV: words in the wrong order FAIL", has_fail(kj("John 1:20", "I am the not Christ")))
    check("KJV: an unknown reference FAILs (fail closed)", has_fail(kj("Hezekiah 9:9", "I am not the Christ")))
    check("KJV: a span that is not word for word in the narration FAILs", has_fail(kj("John 1:20", "I am not the Christ.", narr="He said no.")))
    check("KJV: a character line not covered by any span FAILs", has_fail(ss.lint_kjv(
        [{"ref": "John 1:20", "speaker": "john", "text": "I am not the Christ."}], NARR, [("john", "I am the voice of one")])))
    check("KJV: a covered character line passes", ss.lint_kjv(
        [{"ref": "John 1:20", "speaker": "john", "text": "I am not the Christ."}], NARR, [("john", "I am not the Christ.")])[0].verdict == "PASS")

    section("T5b", "sequence gate G1s: identical ordered word lists (counts alone are not enough)")
    units5 = {"front": "Who answers the desert voice", "f01": "Priests came to ask him"}
    md5 = "# a comment line\nWho answers the desert voice\nPriests came to ask him\n"
    tok = lambda s: ss.norm_tokens(s)  # noqa: E731
    check("G1s: identical lists PASS (comment lines ignored)", ss.lint_sequence(units5, md5, tok("Who answers the desert voice Priests came to ask him"))[0].verdict == "PASS")
    check("G1s: two words swapped between units FAIL", has_fail(ss.lint_sequence(
        units5, md5, tok("Who answers the desert voice Priests came ask to him"))))
    check("G1s: the tagged file differing by one word FAILs", has_fail(ss.lint_sequence(
        units5, md5, tok("Who answers the desert voices Priests came to ask him"))))
    check("G1s: narration.md differing by one word FAILs", has_fail(ss.lint_sequence(
        units5, md5.replace("answers", "answer"), tok("Who answers the desert voice Priests came to ask him"))))
    check("G1s: the alignment differing FAILs", has_fail(ss.lint_sequence(
        units5, md5, tok("Who answers the desert voice Priests came to ask him"), tok("Who answers the desert voice Priests came to ask them"))))
    check("G1s: a comment containing different words is ignored", ss.lint_sequence(
        units5, "# other words here\n" + md5, tok("Who answers the desert voice Priests came to ask him"))[0].verdict == "PASS")

    # ========================================================================= T7 / T7b / T7c ===
    section("T7", "strict still audit on the RAW strings; read; provenance")
    exp7 = ["SEQ: The Desert Voice", "F04", "reeds", "river", "the road", "I am the voice"]
    plan7 = {"full_figures": 2, "crowd": False, "motif_stage": 2}

    def raw7(**over):
        r = {"texts_seen": list(exp7), "full_figures": 2, "crowd": False, "speech_bubble": False,
             "motif_marks": [{"colour": "blue", "where": "ground"}], "motif_bad_shape": False, "drawn_border": False,
             "caption_bottom_pct": 60}
        r.update(over)
        return r
    j = lambda raw, plan=plan7: sv.judge_still_raw(exp7, raw, plan)  # noqa: E731
    check("judge: the exact text passes", j(raw7())[0].verdict == "PASS", str([g.evidence for g in j(raw7())]))
    seen_swap = lambda i, s: raw7(texts_seen=[s if k == i else t for k, t in enumerate(exp7)])  # noqa: E731
    check("judge: a dash ('I am — the voice') FAILs", has_fail(j(seen_swap(5, "I am — the voice"))))
    check("judge: quote marks ('\"I am the voice\"') FAIL", has_fail(j(seen_swap(5, '"I am the voice"'))))
    check("judge: 'MCU' (an unplanned token, 3 letters) FAILs", has_fail(j(raw7(texts_seen=exp7 + ["MCU"]))))
    check("judge: 'F05' for 'F04' FAILs", has_fail(j(seen_swap(1, "F05"))))
    check("judge: 'JOHN 1:28' for 'JOHN 1:23' FAILs", has_fail(sv.judge_still_raw(["JOHN 1:23"], {"texts_seen": ["JOHN 1:28"]}, {}, texts_only=True)))
    check("judge: 'Lamp' for 'Lamb' FAILs", has_fail(sv.judge_still_raw(["the Lamb"], {"texts_seen": ["the Lamp"]}, {}, texts_only=True)))
    check("judge: 'I am' for 'I am not' FAILs", has_fail(sv.judge_still_raw(["I am not"], {"texts_seen": ["I am"]}, {}, texts_only=True)))
    check("judge: a caption twice in one string FAILs", has_fail(sv.judge_still_raw(
        ["I am the voice"], {"texts_seen": ["I am the voice I am the voice"]}, {}, texts_only=True)))
    check("judge: a label drawn twice FAILs", has_fail(j(raw7(texts_seen=exp7 + ["reeds"]))))
    check("judge: an ellipsis FAILs", has_fail(j(seen_swap(5, "I am the voice..."))))
    check("judge: missing text FAILs", has_fail(j(raw7(texts_seen=exp7[:-1]))))
    check("judge: full_figures differing FAILs", has_fail(j(raw7(full_figures=3))))
    check("judge: a crowd when the plan says none FAILs", has_fail(j(raw7(crowd=True))))
    check("judge: a speech bubble FAILs", has_fail(j(raw7(speech_bubble=True))))
    check("judge: a motif drawn as a cord FAILs", has_fail(j(raw7(motif_bad_shape=True))))
    check("judge: a drawn border FAILs", has_fail(j(raw7(drawn_border=True))))
    check("judge: stage 0 with a motif mark FAILs", has_fail(j(raw7(), dict(plan7, motif_stage=0))))
    check("judge: stage 2 with no motif mark FAILs", has_fail(j(raw7(motif_marks=[]))))
    w_gates = j(raw7(caption_bottom_pct=82), plan7)
    check("judge: a caption below 75% is a WARN, never a PASS", verdicts(w_gates) == ["CONDITIONAL"] and not ss.is_pass(w_gates))
    w2 = sv.judge_still_raw(exp7, raw7(crowd=False), dict(plan7, crowd=True))
    check("judge: a crowd planned but not read is a WARN", "CONDITIONAL" in verdicts(w2) and not ss.is_pass(w2))
    check("ss.is_pass: WARN is not a pass", not ss.is_pass([ss._g("x", "CONDITIONAL", "")]) and ss.is_pass([ss._g("x", "PASS", "")]))

    # ---- the Vision READ is mocked by label; `read` clears a text FAIL for that file hash only
    VISION = {}

    def fake_vision(image_bytes, role, user_text, label):
        key = label.split(":", 1)[1] if ":" in label else label
        v = VISION.get(key)
        return v(image_bytes) if callable(v) else (v if v is not None else {})
    REAL_VISION_RAW = sv._vision_raw
    sv._vision_raw = fake_vision
    from PIL import Image
    import numpy as np
    rng = np.random.default_rng(7)

    def mk_png(path: Path, seed=0, size=(100, 178)):
        r = np.random.default_rng(seed)
        Image.fromarray(r.integers(90, 220, (size[1], size[0], 3)).astype("uint8")).save(path)
        return path
    png7 = mk_png(tmp / "page7.png", 1)
    VISION["page7"] = raw7(texts_seen=seen_swap(5, "I am - the voice")["texts_seen"])
    check("audit_still_v3: the misread FAILs", has_fail(sv.audit_still_v3(png7, exp7, plan7)))
    sv.record_read(png7, exp7, "zoomed 2x: no dash, 2026-11-15")
    check("a recorded read clears the text FAIL for that file", not has_fail(sv.audit_still_v3(png7, exp7, plan7)))
    check("the sidecar records png_sha256 + audit_version 3", (lambda d: d["png_sha256"] == sha(png7) and d["audit_version"] == 3)(
        json.loads(Path(str(png7) + ".audit3.json").read_text())))
    mk_png(png7, 99)
    VISION["page7"] = raw7(texts_seen=seen_swap(5, "I am - the voice")["texts_seen"])
    check("the read is VOID after the file changes (a new render)", has_fail(sv.audit_still_v3(png7, exp7, plan7)))
    other = mk_png(tmp / "page8.png", 5)
    VISION["page8"] = raw7(texts_seen=seen_swap(5, "I am - the voice")["texts_seen"])
    check("a read for one PNG does not clear another PNG", has_fail(sv.audit_still_v3(other, exp7, plan7)))
    config.LLM_PROVIDER = "api"
    try:
        check("metered Vision (API mode) is REFUSED by the Vision read", raises(RuntimeError, REAL_VISION_RAW, b"x", "r", "u", "l"))
        check("the runner refuses a trim episode while the metered API mode is on", run._vision_gate() is False)
    finally:
        config.LLM_PROVIDER = "agent"
    check("the runner accepts agent mode", run._vision_gate() is True)

    # ---- provenance: G14 over MANIFEST.units[*].src, G14s on stills
    pv = tmp / "prov_ep"
    pv.mkdir()
    (pv / ".swirls_short").write_text(json.dumps({"episode_id": "prov"}), encoding="utf-8")
    still_f01 = mk_png(guard.png_path(pv, "f01"), 11)
    clip_f01 = mk_clip(guard.clip_path(pv, "f01"), 1.0, "1072x1928")
    other_clip = mk_clip(pv / "elsewhere.mp4", 1.0, "1072x1928")

    def forge(kind, unit, out_sha, in_sha, status="confirmed"):
        guard._append(pv, {"id": uuid.uuid4().hex, "ts": f"2026-11-15T10:00:{len(guard.read_log(pv)):02d}.000", "ts_update": time.time(), "step": "x",
                           "unit": unit, "kind": kind, "provider": "openart", "price": 1, "cur": "cr", "status": status,
                           "output_sha256": out_sha, "input_sha256": in_sha, "credits_spent": 1})
    mu = [Unit("f01", clip_f01, 12, "trim")]
    check("G14: no confirmed row for the clip FAILs", has_fail(ss.lint_clip_provenance(pv, mu)))
    forge("still", "f01", sha(still_f01), "p")
    forge("anim", "f01", sha(clip_f01), sha(still_f01))
    check("G14: canonical path + receipt hash + current still PASSES", ss.lint_clip_provenance(pv, mu)[0].verdict == "PASS", ss.lint_clip_provenance(pv, mu)[0].evidence)
    check("G14s: the still has a receipt -> PASS", ss.lint_still_provenance(pv, ["f01"])[0].verdict == "PASS")
    check("G14: a Unit.src pointing at another file FAILs", has_fail(ss.lint_clip_provenance(pv, [Unit("f01", other_clip, 12, "trim")])))
    mk_png(still_f01, 12)
    check("G14: replacing the PNG makes the old mp4 stale (FAIL)", has_fail(ss.lint_clip_provenance(pv, mu)))
    check("G14s: a PNG with no receipt (copied in) FAILs", has_fail(ss.lint_still_provenance(pv, ["f01"])))
    pc = guard.clip_path(pv, "f01")
    check("run.clip_state: a clip whose still changed is STALE", run.clip_state(pv, "f01") == "stale")
    forge("still", "f01", sha(still_f01), "p2")
    forge("anim", "f01", sha(clip_f01) if False else sha(pc), sha(still_f01))
    check("run.clip_state: a clip bound to the current still is FRESH", run.clip_state(pv, "f01") == "fresh")
    sup = run._supersede(pc, "stale")
    check("a stale mp4 is renamed .SUPERSEDED_<why>, never 'skipped as done'", sup.name.endswith(".SUPERSEDED_stale") and not pc.exists() and run.clip_state(pv, "f01") == "none")

    section("T7b", "G13 eyes: hard flags FAIL, soft WARN, 540 px strips of 6")
    reads_ok = [{"frames": [{"texts_seen": list(exp7), "full_figures": 2}] * 6}]
    ge = lambda reads: ss.judge_eyes(reads, plan7, exp7)  # noqa: E731
    check("G13: a clean clip passes", ge(reads_ok)[0].verdict == "PASS", str([g.evidence for g in ge(reads_ok)]))
    check("G13: a speech bubble FAILs", has_fail(ge([dict(reads_ok[0], speech_bubble=True)])))
    last_changed = [{"frames": [{"texts_seen": list(exp7), "full_figures": 2}] * 5 + [{"texts_seen": exp7[:-1] + ["I am the voices"], "full_figures": 2}]}]
    check("G13: a changed caption on the LAST frame FAILs", has_fail(ge(last_changed)))
    check("G13: ink_changed FAILs", has_fail(ge([dict(reads_ok[0], ink_changed=True)])))
    check("G13: new legible text FAILs", has_fail(ge([dict(reads_ok[0], new_text=True)])))
    check("G13: a still thing that moves FAILs", has_fail(ge([dict(reads_ok[0], still_thing_moving=True)])))
    check("G13: bare-skin doubt FAILs", has_fail(ge([dict(reads_ok[0], bare_skin=True)])))
    check("G13: a full-figure count change FAILs", has_fail(ge([{"frames": [{"texts_seen": list(exp7), "full_figures": 2}] * 3 + [{"texts_seen": list(exp7), "full_figures": 3}] * 3}])))
    soft = ge([dict(reads_ok[0], mouth_changed=True, drift=True)])
    check("G13: a mouth / drift flag is a WARN, not a FAIL and not a pass", not has_fail(soft) and "CONDITIONAL" in verdicts(soft))
    mv = mk_clip(tmp / "strip_src.mp4", 6.5, "270x480")
    strips, times = ss.make_strips(mv, 6.0, tmp / "strips")
    ims = [Image.open(s) for s in strips]
    check("strips: frames at 2 per second of the span + the true last frame", times[0] == 0.0 and len(times) == 13 and times[-1] > 5.9, str(times))
    check("strips: 540 px tiles, 6 per strip image", ims[0].width == 540 * 6 and all(i.width in (540 * 6, 540 * 1) for i in ims), str([i.size for i in ims]))
    check("strips: 13 frames make 3 strip images", len(strips) == 3)

    section("T7c", "overrides: gate + unit + file hash + dated owner quote")
    ov = tmp / "ov_ep"
    ov.mkdir()
    f02p, f03p = mk_png(ov / "f02.png", 21), mk_png(ov / "f03.png", 22)
    (ov / "_overrides.json").write_text(json.dumps({"entries": [
        {"gate": "SWS-G13", "unit": "f02", "file_sha256": sha(f02p), "owner_quote": "ok, the mouth is fine", "date": "2026-11-15"},
        {"gate": "SWS-G14", "unit": "f02", "file_sha256": sha(f02p), "owner_quote": "skip it", "date": "2026-11-15"},
        {"gate": "SWS-G1k", "unit": "f02", "file_sha256": sha(f02p), "owner_quote": "skip it", "date": "2026-11-15"}]}), encoding="utf-8")
    fail13 = [ss._g("SWS-G13", "FAIL", "bubble")]
    check("an override for f02's file clears f02", sv.apply_overrides_bound(fail13, ov, "f02", f02p)[0].verdict == "CONDITIONAL")
    check("it does NOT clear f03", sv.apply_overrides_bound(fail13, ov, "f03", f03p)[0].verdict == "FAIL")
    mk_png(f02p, 23)
    check("it does NOT clear f02 after a reroll (new file hash)", sv.apply_overrides_bound(fail13, ov, "f02", f02p)[0].verdict == "FAIL")
    mk_png(f02p, 21)
    for g in ("SWS-G14", "SWS-G1k", "SWS-G14s", "SWS-G1s", "SWS-G16", "SWS-G0"):
        check(f"an override on {g} is ignored", sv.apply_overrides_bound([ss._g(g, "FAIL", "x")], ov, "f02", f02p)[0].verdict == "FAIL")

    # ======================================================================= T8 / T9 ===
    section("T8", "G15h moving hold on REAL back covers vs frozen / frame-0 / stops-at-1.5 copies")
    real_srcs = {}
    for nm, rel in (("ep10", "swirls_episode_10_she_loved_much/back_cover.mp4"), ("ep13", "swirls_episode_13_the_cross_that_wasnt_his/back_cover.mp4")):
        if (HERE / rel).exists():
            real_srcs[nm] = HERE / rel
    c16 = sorted((HERE / "swirls_episode_16_let_the_little_children" / "clips").glob("*.mp4")) if (HERE / "swirls_episode_16_let_the_little_children" / "clips").exists() else []
    if c16:
        real_srcs["ep16"] = c16[-1]
    if not real_srcs:
        skip("T8 real back covers", "no ep10/ep13/ep16 clips on disk")
    for nm, src in real_srcs.items():
        real = tmp / f"t8_{nm}_real.mp4"
        ff("-i", str(src), "-vf", "scale=360:-2,fps=30", "-c:v", "libx264", "-preset", "ultrafast", "-pix_fmt", "yuv420p", "-an", str(real))
        d_ = ss._ffprobe_duration(real)
        hs = d_ - 3.0
        variants = {}
        for lbl, vf in (("frozen", f"trim=end={hs:.3f},setpts=PTS-STARTPTS,tpad=stop_mode=clone:stop_duration=3"),
                        ("frame0", f"trim=end=0.04,setpts=PTS-STARTPTS,tpad=stop_mode=clone:stop_duration={d_ - 0.04:.3f}"),
                        ("stops-at-1.5s", f"trim=end={hs + 1.5:.3f},setpts=PTS-STARTPTS,tpad=stop_mode=clone:stop_duration=1.5")):
            v = tmp / f"t8_{nm}_{lbl}.mp4"
            ff("-i", str(real), "-vf", vf, "-c:v", "libx264", "-preset", "ultrafast", "-pix_fmt", "yuv420p", "-an", str(v))
            variants[lbl] = v
        gr = ss.moving_hold(real, hs, tmp / f"t8c_{nm}")
        check(f"G15h: the real {nm} back cover PASSES (k={ss.HOLD_K}, floor {ss.HOLD_ABS_FLOOR})", gr.verdict == "PASS", gr.evidence)
        for lbl, v in variants.items():
            gv = ss.moving_hold(v, hs, tmp / f"t8c_{nm}_{lbl}")
            check(f"G15h: the {lbl} copy of {nm} FAILs", gv.verdict == "FAIL", gv.evidence)

    section("T9", "edge scan: separates the shipped bad covers from the good ones?")
    bad_c, good_c = [], []
    for ep_, lst in (("02", bad_c), ("05", bad_c), ("07", bad_c), ("08", bad_c), ("10", good_c), ("13", good_c)):
        for dd in HERE.glob(f"swirls_episode_{ep_}_*"):
            for nm in ("front_cover.png", "back_cover.png"):
                if (dd / nm).exists():
                    lst.append((ep_, nm, ss.edge_scan(dd / nm).verdict))
    sep = bool(bad_c and good_c) and all(v == "FAIL" for _, _, v in bad_c) and all(v == "PASS" for _, _, v in good_c)
    print(f"      bad covers: {[(a, b[:5], c) for a, b, c in bad_c]}\n      good covers: {[(a, b[:5], c) for a, b, c in good_c]}")
    check("T9 outcome is recorded honestly: the pixel scan does " + ("" if sep else "NOT ") + "separate them; covers level is "
          + ss.EDGE_COVER_LEVEL, (sep and ss.EDGE_COVER_LEVEL == "FAIL") or (not sep and ss.EDGE_COVER_LEVEL == "CONDITIONAL"))
    paper = (np.random.default_rng(3).integers(150, 200, (356, 200))).astype("uint8")
    Image.fromarray(paper).save(tmp / "e_ok.png")
    check("G10 clean edges pass", ss.edge_scan(tmp / "e_ok.png").verdict == "PASS")
    ruled = paper.copy()
    ruled[2, :] = 10
    Image.fromarray(ruled).save(tmp / "e_rule.png")
    check("G10 a drawn rule FAILs at level FAIL", ss.edge_scan(tmp / "e_rule.png", "FAIL").verdict == "FAIL")
    check("G10 the same rule is only a WARN on a page (level CONDITIONAL)", ss.edge_scan(tmp / "e_rule.png", ss.EDGE_PAGE_LEVEL).verdict == "CONDITIONAL")
    band = paper.copy()
    band[:8, :] = 255
    Image.fromarray(band).save(tmp / "e_band.png")
    check("G10 a blank band FAILs at level FAIL", ss.edge_scan(tmp / "e_band.png", "FAIL").verdict == "FAIL")
    check("crop keeps the aspect ratio and is proportional", abs((lambda b: (b[2] - b[0]) / (b[3] - b[1]))(ss.crop_box(1536, 2752, 0.03)) - 1536 / 2752) < 0.002)

    # ============================================================================= T6 ===
    section("T6", "spend guard + bridge protocol: a FAKE servicer on real files, nothing can bill")
    GEN: list[str] = []          # every call the fake servicer makes to its 'generate tool'
    GEN_LOCK = threading.Lock()
    EXPECT = json.loads((HERE / "fixtures" / "golden_8unit" / "expected_unit_timing.json").read_text(encoding="utf-8"))

    def default_asset(payload: dict, path: Path, rid: str) -> None:
        if payload["kind"] == "still":
            r = np.random.default_rng(int(rid[:6], 16))
            Image.fromarray(r.integers(90, 220, (112, 64, 3)).astype("uint8")).save(path, format="PNG")
        else:
            path.write_bytes(b"FAKEMP4" + os.urandom(64))

    class Servicer(threading.Thread):
        """Follows POC\\SWIRLS_SHORT_SERVICER.md: claim by rename, refuse stale, generate once, write
        submitted.json at once, download to staging, receipt = the creation record, then reply."""
        def __init__(self, session="s1", mode="ok", hold=None, asset=default_asset):
            super().__init__(daemon=True)
            self.session, self.mode, self.hold, self.asset = session, mode, hold, asset
            self.stop_ev = threading.Event()

        def run(self):
            while not self.stop_ev.is_set():
                for req in sorted(ob.GUARDED_DIR.glob("*.request.json")) if ob.GUARDED_DIR.exists() else []:
                    try:
                        self.service(req)
                    except FileNotFoundError:
                        pass            # the client cancelled it between listing and claiming
                    except Exception as e:  # a test bug must be loud, not silent
                        import traceback
                        traceback.print_exc()
                        print("      servicer error:", repr(e))
                time.sleep(0.02)

        def service(self, req: Path):
            rid = req.name.split(".")[0]
            ob.CLAIMED_DIR.mkdir(parents=True, exist_ok=True)
            claim = ob.CLAIMED_DIR / f"{rid}.{self.session}.json"
            try:
                os.replace(req, claim)          # rule 0: claim first; a failed rename = someone else has it
            except OSError:
                return
            data = json.loads(claim.read_text(encoding="utf-8"))
            hb = Path(data["heartbeat"])
            stale = (not hb.exists()) or (time.time() - hb.stat().st_mtime) > ob.HEARTBEAT_STALE_SECONDS
            if time.time() > data["not_after"] or stale:       # rule 1: refuse
                ob.CANCELLED_DIR.mkdir(parents=True, exist_ok=True)
                os.replace(claim, ob.CANCELLED_DIR / f"{rid}.request.json")
                self.reply(rid, {"status": "error", "error": "expired or client gone"})
                return
            with GEN_LOCK:
                GEN.append(rid)                                  # THE generate call
            cid = f"cr_{rid[:8]}"
            (ob.CLAIMED_DIR / f"{rid}.submitted.json").write_text(json.dumps({"creation_id": cid}), encoding="utf-8")   # rule 3
            if self.hold is not None:
                self.hold.wait(30)
            payload = data["payload"]
            ob.STAGING_DIR.mkdir(parents=True, exist_ok=True)
            staged = ob.STAGING_DIR / f"{rid}{Path(payload['out_path']).suffix}"
            self.asset(payload, staged, rid)                     # rule 4: staging, never out_path
            price, _ = guard.price_of(payload)
            sent = dict(data["priced"])
            credits = price
            if self.mode == "sound_on":
                sent["generate_sound"] = True
            if self.mode == "over_price":
                credits = price * 1.5
            ob.RECEIPTS_DIR.mkdir(parents=True, exist_ok=True)
            if self.mode != "no_record":                         # rule 5: the receipt is the creation record
                (ob.RECEIPTS_DIR / f"{rid}.json").write_text(json.dumps(
                    {"creation_id": cid, "sent_params": sent, "credits_spent": credits}), encoding="utf-8")
            if self.mode == "error_after_submit":
                self.reply(rid, {"status": "error", "error": "download failed", "creation_id": cid})
            elif self.mode == "no_record":
                self.reply(rid, {"status": "ok", "creation_id": cid, "sent_params": sent, "credits_spent": price})
            else:
                self.reply(rid, {"status": "ok", "creation_id": cid})

        def reply(self, rid: str, body: dict):
            ob.RESPONSES_DIR.mkdir(parents=True, exist_ok=True)
            tmpf = ob.RESPONSES_DIR / f"{rid}.tmp"
            tmpf.write_text(json.dumps({"id": rid, **body}), encoding="utf-8")
            os.replace(tmpf, ob.RESPONSES_DIR / f"{rid}.response.json")

    @contextlib.contextmanager
    def servicers(*svs):
        for s_ in svs:
            s_.start()
        try:
            yield svs
        finally:
            for s_ in svs:
                s_.stop_ev.set()
            for s_ in svs:
                s_.join(timeout=3)

    def mk_guard_ep(name: str, voice_ear: bool = True) -> Path:
        d = tmp / name
        d.mkdir()
        (d / ".swirls_short").write_text(json.dumps({"episode_id": "ep-" + name}), encoding="utf-8")
        units = json.loads((HERE / "fixtures" / "golden_8unit" / "units.json").read_text(encoding="utf-8"))
        (d / "units.json").write_text(json.dumps(units), encoding="utf-8")
        (d / "narration.md").write_text("\n".join(units.values()), encoding="utf-8")
        (d / "narration-tagged.md").write_text("\n\n".join(units.values()), encoding="utf-8")
        mk_audio(d / "narration.mp3", 3.0)
        doc = {"narration_seconds": 42.3, "units": {t: dict(u) for t, u in EXPECT["units"].items()}}
        (d / "unit_timing.json").write_text(json.dumps(doc), encoding="utf-8")
        (d / "page_plan.json").write_text(json.dumps({"north_star": "f04", "units": {}}), encoding="utf-8")
        guard.record_gate(d, "words", "owner picked the words 2026-11-15")
        if voice_ear:
            guard.record_gate(d, "voice_ear", "take A 2026-11-15")
        return d

    def pay_still(d, unit, **o):
        p = {"kind": "still", "model": "nano-banana-pro", "mode": "text2image", "prompt": f"prompt {unit}", "aspect_ratio": "9:16",
             "resolution": "2K", "refs": [], "out_path": str(guard.png_path(d, unit))}
        p.update(o)
        return p

    def pay_anim(d, unit, dur_=7, **o):
        p = {"kind": "anim", "model": "kling-3-omni", "mode": "image2video", "prompt": f"motion {unit}", "start_image_path": str(guard.png_path(d, unit)),
             "duration": dur_, "resolution": "pro", "generate_sound": False, "out_path": str(guard.clip_path(d, unit))}
        p.update(o)
        return p

    def submit(d, step, unit, payload):
        with guard.guard_context(d, step, unit, payload["kind"], payload["prompt"]):
            return ob.submit(payload)

    def refused(d, step, unit, payload, why="", ctx=True):
        """A refusal writes NOTHING: no request file, no new log row."""
        n_req = len(list(ob.GUARDED_DIR.glob("*.request.json"))) if ob.GUARDED_DIR.exists() else 0
        n_log = len(guard.read_log(d))
        try:
            if ctx:
                submit(d, step, unit, payload)
            else:
                ob.submit(payload)
        except ob.OpenArtBridgeError as e:
            same = (len(list(ob.GUARDED_DIR.glob("*.request.json"))) if ob.GUARDED_DIR.exists() else 0) == n_req and len(guard.read_log(d)) == n_log
            if why and why not in str(e):
                print(f"      (refused for another reason: {e})")
                return False
            return same
        return False

    def grant(d, step, balance=10000, doc=None):
        doc = doc or json.loads((d / "unit_timing.json").read_text(encoding="utf-8"))
        q = guard.write_quote(d, step, **run._q(ss.quote_pictures(doc) if step == "pictures" else ss.quote_clips(doc)))
        return guard.approve(d, step, q["at_most"], "cr", f"owner: yes, about {q['about']:g}, at most {q['at_most']:g} cr, 2026-11-15", balance)

    g1 = mk_guard_ep("ep_g1")
    check("no guard context: a marked out_path is refused and nothing is written", refused(g1, "pictures", "f04", pay_still(g1, "f04"), "no guard context", ctx=False))
    check("no grant: refused, nothing written", refused(g1, "pictures", "f04", pay_still(g1, "f04"), "no live grant"))
    q = guard.write_quote(g1, "pictures", **run._q(ss.quote_pictures(json.loads((g1 / "unit_timing.json").read_text(encoding="utf-8")))))
    check("quote: about 400 cr, at most 836 cr (= ceil((400 + 360) x 1.10))", (q["about"], q["at_most"]) == (400, 836), str(q))
    n_ap = lambda: len(json.loads((g1 / "approvals.json").read_text())["grants"]) if (g1 / "approvals.json").exists() else 0  # noqa: E731
    check("approve --cap != the quote's 'at most' is refused", raises(guard.SpendRefused, guard.approve, g1, "pictures", 800, "cr", "yes 800 2026-11-15", 9999))
    check("approve with a note that lacks the cap number is refused", raises(guard.SpendRefused, guard.approve, g1, "pictures", 836, "cr", "owner said yes 2026-11-15", 9999))
    check("approve with a note that lacks a date is refused", raises(guard.SpendRefused, guard.approve, g1, "pictures", 836, "cr", "owner said yes 836", 9999))
    guard.record_gate(g1, "words", "owner: 836 cr yes 2026-11-15")
    check("approve with a note equal to an `ok` note is refused (a look is not a spend order)",
          raises(guard.SpendRefused, guard.approve, g1, "pictures", 836, "cr", "owner: 836 cr yes 2026-11-15", 9999))
    check("approve with balance < cap is refused", raises(guard.SpendRefused, guard.approve, g1, "pictures", 836, "cr", "yes 836 cr 2026-11-15", 500))
    check("none of those refusals wrote a grant", n_ap() == 0)
    check("approve on a step that is not open (score before draft_cut) is refused", raises(
        guard.SpendRefused, guard.approve, g1, "score", 1.0, "usd", "yes 1.0 2026-11-15"))
    gr = grant(g1, "pictures")
    check("approve with --cap = the quote's at-most, number and date in the note: ok", gr["cap"] == 836 and n_ap() == 1)
    ns_png = guard.png_path(g1, "f04")
    check("a request outside the first-item hard stop (f01 before northstar_look) is refused",
          refused(g1, "pictures", "f01", pay_still(g1, "f01"), "may be bought"))
    check("unknown price row (4K) is refused, nothing written", refused(g1, "pictures", "f04", pay_still(g1, "f04", resolution="4K"), "unknown price row"))
    check("sound ON is refused (not a known price row)", refused(g1, "pictures", "f04", pay_anim(g1, "f04", generate_sound=True), "unknown price row"))
    check("an illegal clip length (2 s) is refused", refused(g1, "pictures", "f04", pay_anim(g1, "f04", dur_=2), "unknown price row"))
    os.environ["SWIRLS_GEN_PROVIDER"] = "hf"
    check("provider != openart is refused", refused(g1, "pictures", "f04", pay_still(g1, "f04"), "OpenArt only"))
    del os.environ["SWIRLS_GEN_PROVIDER"]
    import swirls_page
    from swirls_page import render_still
    check("render_still(provider='hf') under a marker raises (the four render functions refuse)",
          raises(RuntimeError, render_still, mk_page(), g1 / "x_f02_9x16.png", "hf"))
    import swirls_cover
    check("render_cover_still(provider='hf') under a marker raises", raises(RuntimeError, swirls_cover.render_cover_still, cov, g1 / "front_cover.png", "hf"))
    check("render_animation / render_cover_animation refuse hf under a marker too",
          raises(RuntimeError, swirls_page.render_animation, mk_page(), ns_png, g1 / "x.mp4", "hf")
          and raises(RuntimeError, swirls_cover.render_cover_animation, cov, ns_png, g1 / "front_cover.mp4", "hf"))
    other = mk_guard_ep("ep_other")
    check("out_path outside this episode is refused", refused(g1, "pictures", "f04", pay_still(g1, "f04", out_path=str(guard.png_path(other, "f04"))), "outside this episode"))
    check("a missing/void look gate is refused (narration.mp3 changed after voice_ear)", (lambda: (
        (g1 / "narration.mp3").rename(g1 / "narration.mp3.bak"), mk_audio(g1 / "narration.mp3", 3.5),
        refused(g1, "pictures", "f04", pay_still(g1, "f04"), "voice_ear"))[2])())
    (g1 / "narration.mp3").unlink()
    (g1 / "narration.mp3.bak").rename(g1 / "narration.mp3")
    check("the look is valid again once the file is back", guard.gate_valid(g1, "voice_ear"))
    check("no marker on a trim episode: every paid command refuses", (lambda d: (d.mkdir(), run.require_marker(d) is False)[1])(tmp / "no_marker_ep"))

    with servicers(Servicer()):
        resp = submit(g1, "pictures", "f04", pay_still(g1, "f04"))
        check("north-star still: one generate call, creation_id in the reply", len(GEN) == 1 and resp["creation_id"].startswith("cr_"))
        row = guard.confirmed_row(g1, "still", "f04")
        check("the row is confirmed from the creation RECORD (credits 40, hash of the file)", row is not None and row["credits_spent"] == 40
              and row["output_sha256"] == sha(ns_png) and row["creation_id"] == resp["creation_id"])
        check("the file arrived via staging (out_path written only after the receipt checks)", ns_png.exists() and not list(ob.STAGING_DIR.glob(f"{row['id']}.*")))
        check("a request is a uuid4 rid and carried a heartbeat + not_after", len(row["id"]) == 32 and (ob.CLAIMED_DIR / f"{row['id']}.submitted.json").exists())
        claimed = json.loads(next(ob.CLAIMED_DIR.glob(f"{row['id']}.s1.json")).read_text())
        check("the request carried episode_id, not_after, heartbeat, priced fields and ref/start sha256", all(k in claimed for k in (
            "episode_id", "not_after", "heartbeat", "priced", "sha256", "servicer_rules")) and claimed["episode_id"] == "ep-ep_g1")
        check("the order of two guarded requests for one unit cannot be a 'second still before northstar_look'",
              refused(g1, "pictures", "f02", pay_still(g1, "f02"), "may be bought"))
        guard.record_gate(g1, "northstar_look", "looked on a phone 2026-11-15")
        check("after northstar_look the other units may be bought", submit(g1, "pictures", "f01", pay_still(g1, "f01"))["status"] == "ok")
        # reroll rule: first + 2 rerolls, a 4th needs a unit grant
        for _ in range(2):
            submit(g1, "pictures", "f02", pay_still(g1, "f02"))
        submit(g1, "pictures", "f02", pay_still(g1, "f02"))
        check("f02: three renders done (first + 2 rerolls)", guard._unit_renders(guard.read_log(g1), "still", "f02") == 3)
        check("a 4th render of one unit is refused", refused(g1, "pictures", "f02", pay_still(g1, "f02"), "4th"))
        check("a unit grant needs a live base grant and a number in the note", raises(guard.SpendRefused, guard.approve, g1, "pictures", 44, "cr", "one more 2026-11-15", 9999, "f02", 1))
        guard.approve(g1, "pictures", 44, "cr", "owner: one more f02, at most 44 cr, changed the lever, 2026-11-15", 9999, "f02", 1)
        check("the unit grant adds ONE render for that unit", submit(g1, "pictures", "f02", pay_still(g1, "f02"))["status"] == "ok"
              and refused(g1, "pictures", "f02", pay_still(g1, "f02"), "renders"))
        for _ in range(3):
            submit(g1, "pictures", "f03", pay_still(g1, "f03"))
        check("...and it does not help another unit (f03's 4th is still refused)", refused(g1, "pictures", "f03", pay_still(g1, "f03"), "4th"))
        check("grants are APPEND-ONLY (2 grants, the first untouched)", (lambda gs: len(gs) == 2 and gs[0]["cap"] == 836)(guard.grants(g1)))

        # an open row blocks everything; two before() calls race, one wins
        ctx = guard.GuardCtx(g1, "pictures", "f05", "still", guard.sha256_of("prompt f05"))
        wins, errs = [], []
        bar = threading.Barrier(2)

        def racer():
            bar.wait()
            try:
                wins.append(guard.before(ctx, pay_still(g1, "f05")))
            except guard.SpendRefused as e:
                errs.append(str(e))
        ts_ = [threading.Thread(target=racer) for _ in range(2)]
        [t.start() for t in ts_]
        [t.join() for t in ts_]
        check("two before() calls racing: exactly one wins (lock + one open row)", len(wins) == 1 and len(errs) == 1 and "open spend row" in errs[0], str(errs))
        check("an open row blocks every paid command (any step, any unit)", refused(g1, "pictures", "f06", pay_still(g1, "f06"), "open spend row"))
        guard.mark(g1, wins[0]["id"], "voided")
        check("a voided row unblocks", submit(g1, "pictures", "f05", pay_still(g1, "f05"))["status"] == "ok")
        # closing gate
        for t in ss.TAGS:
            if not guard.png_path(g1, t).exists():
                mk_png(guard.png_path(g1, t), 31)
        guard.record_gate(g1, "stills_animatic", "page 4 go 2026-11-15")
        check("a closed step (stills_animatic recorded) refuses and its grants die", refused(g1, "pictures", "f06", pay_still(g1, "f06"), "closed")
              and not any(guard.grant_alive(g1, g_) for g_ in guard.grants(g1)))

    # ---- cap sums fit their own planned rerolls (pictures: 8 stills + 3 refs + 8 rerolls; clips: all + back + 2 pages)
    g3 = mk_guard_ep("ep_g3")
    guard.write_quote(g3, "pictures", **run._q(ss.quote_pictures(json.loads((g3 / "unit_timing.json").read_text(encoding="utf-8")))))
    grant(g3, "pictures")
    mk_png(guard.png_path(g3, "f04"), 41)
    guard.record_gate(g3, "northstar_look", "look 2026-11-15")

    def book(d, step, unit, payload, kind=None):
        """before() + a confirmed row (what a clean receipt would do), without the servicer."""
        row = guard.before(guard.GuardCtx(d, step, unit, payload["kind"], "p"), payload)
        guard.mark(d, row["id"], "confirmed", credits_spent=row["price"], output_sha256="x")
        return row
    try:
        for t in ss.TAGS:
            book(g3, "pictures", t, pay_still(g3, t))
        for n_ in ("a", "b", "c"):
            book(g3, "pictures", f"ref:{n_}", pay_still(g3, "f04"))
        for t in ss.TAGS:
            book(g3, "pictures", t, pay_still(g3, t))
        pic_fit = True
    except guard.SpendRefused as e:
        pic_fit, pic_err = False, str(e)
    check("pictures: 8 stills + 3 refs + 8 rerolls all fit inside the cap the owner saw", pic_fit, "" if pic_fit else pic_err)
    check("pictures: a 4th ref render is refused (3 at most)", raises(guard.SpendRefused, book, g3, "pictures", "ref:d", pay_still(g3, "f04")))
    extra_ok = 0
    for t in ("f01", "f02", "f03", "f05"):
        try:
            book(g3, "pictures", t, pay_still(g3, t))
            extra_ok += 1
        except guard.SpendRefused:
            break
    check("pictures: only the 10% headroom is spare, then the cap refuses (it is not open-ended)", extra_ok <= 2 and
          guard.spent(g3, "pictures") <= 836, f"{extra_ok} extra renders, spent {guard.spent(g3, 'pictures')}")
    g4 = mk_guard_ep("ep_g4")
    doc4 = json.loads((g4 / "unit_timing.json").read_text(encoding="utf-8"))
    for t in ss.TAGS:
        mk_png(guard.png_path(g4, t), 51)
    guard.record_gate(g4, "stills_animatic", "page 4 go 2026-11-15")
    guard.write_quote(g4, "clips", **run._q(ss.quote_clips(doc4)))
    q4 = grant(g4, "clips", doc=doc4)
    cds = {t: u["clip_duration"] for t, u in doc4["units"].items()}
    try:
        for t in ("f04", "back"):
            book(g4, "clips", t, pay_anim(g4, t, cds[t]))
        for t in ("f04", "back"):
            guard.clip_path(g4, t).write_bytes(b"stub")
        guard.record_gate(g4, "clip_test_look", "clips look 2026-11-15")
        for t in ss.TAGS:
            if t not in ("f04", "back"):
                book(g4, "clips", t, pay_anim(g4, t, cds[t]))
        book(g4, "clips", "back", pay_anim(g4, "back", cds["back"]))
        pm = max(v for t, v in cds.items() if t != "back")
        for t in [t for t, v in cds.items() if v == pm][:1] + [t for t, v in cds.items() if v == pm][:1]:
            book(g4, "clips", t, pay_anim(g4, t, cds[t]))
        clip_fit = True
    except guard.SpendRefused as e:
        clip_fit, clip_err = False, str(e)
    check("clips: 8 clips + 1 back reroll + 2 page rerolls all fit inside the cap the owner saw", clip_fit, "" if clip_fit else clip_err)
    check("clips: the quote is 35 cr per whole second (1,890 cr for the golden 54 clip-seconds)", ss.quote_clips(doc4)["about"] == 35 * 54 == 1890)

    # ---- protocol failure modes (episode g2)
    g2 = mk_guard_ep("ep_g2")
    grant(g2, "pictures")
    ob.TIMEOUT_SECONDS = 0.5
    t0 = time.time()
    try:
        submit(g2, "pictures", "f04", pay_still(g2, "f04"))
        got = None
    except ob.OpenArtBridgeError as e:
        got = e
    rid_a = next(iter(guard.open_rows(g2)))["id"]
    check("timeout BEFORE a claim: the request is renamed into cancelled/ -> CANCELLED_UNCLAIMED",
          got is not None and guard.read_log(g2)[rid_a]["status"] == "CANCELLED_UNCLAIMED" and (ob.CANCELLED_DIR / f"{rid_a}.request.json").exists())
    check("...and it blocks every paid command until settled", refused(g2, "pictures", "f04", pay_still(g2, "f04"), "open spend row"))
    check("void without a list dump is refused", raises(guard.SpendRefused, guard.confirm, g2, rid_a, "n", None, None, True, None))
    row_a = guard.read_log(g2)[rid_a]
    dump = tmp / "list_dump.json"
    dump.write_text(json.dumps({"from_ts": time.time() - 60, "to_ts": time.time() + 60,
                                "creations": [{"creation_id": "x1", "prompt_sha256": row_a["prompt_sha256"]}]}), encoding="utf-8")
    check("a list dump that SHOWS a creation for it refuses the void", raises(guard.SpendRefused, guard.confirm, g2, rid_a, "n", None, None, True, dump))
    dump.write_text(json.dumps({"from_ts": time.time() + 5, "to_ts": time.time() + 60, "creations": []}), encoding="utf-8")
    check("a list dump that does not cover the request window refuses the void", raises(guard.SpendRefused, guard.confirm, g2, rid_a, "n", None, None, True, dump))
    dump.write_text(json.dumps({"from_ts": time.time() - 60, "to_ts": time.time() + 60, "creations": []}), encoding="utf-8")
    check("a covering list dump with no creation voids it", guard.confirm(g2, rid_a, "no creation 2026-11-15", None, None, True, dump)[1] == "voided")

    # timeout AFTER a claim: LATE_PENDING, not voidable, no new request; fetch settles with no 2nd generate
    gen_before = len(GEN)
    hold = threading.Event()
    sv_late = Servicer("late", hold=hold)
    ob.TIMEOUT_SECONDS = 0.6
    with servicers(sv_late):
        try:
            submit(g2, "pictures", "f04", pay_still(g2, "f04"))
        except ob.OpenArtBridgeError:
            pass
        rid_b = next(iter(guard.open_rows(g2)))["id"]
        check("timeout AFTER the claim: the rename fails -> LATE_PENDING", guard.read_log(g2)[rid_b]["status"] == "LATE_PENDING" and len(GEN) == gen_before + 1)
        check("a LATE_PENDING row can NOT be voided", raises(guard.SpendRefused, guard.confirm, g2, rid_b, "n", None, None, True, dump))
        check("no new request is allowed while it is open", refused(g2, "pictures", "f04", pay_still(g2, "f04"), "open spend row"))
        check("fetch before the render is ready stays open (no staged file / record yet)", guard.fetch(g2, rid_b)[0] is False)
        hold.set()
        t_end = time.time() + 5
        while time.time() < t_end and not (ob.RECEIPTS_DIR / f"{rid_b}.json").exists():
            time.sleep(0.05)
        time.sleep(0.1)
        ok_b, why_b = guard.fetch(g2, rid_b)
        check("fetch settles it from the staged file + the record, with NO second generate call", ok_b and len(GEN) == gen_before + 1, why_b)
        check("the fetched file landed at out_path with its hash stored", guard.png_path(g2, "f04").exists()
              and guard.read_log(g2)[rid_b]["output_sha256"] == sha(guard.png_path(g2, "f04")))
    ob.TIMEOUT_SECONDS = 30.0

    # killed client (no finally): swept by heartbeat
    ctx = guard.GuardCtx(g2, "pictures", "f01", "still", "p")
    guard.record_gate(g2, "northstar_look", "look 2026-11-15")
    row_c = guard.before(ctx, pay_still(g2, "f01"))
    ob.GUARDED_DIR.mkdir(parents=True, exist_ok=True)
    (ob.GUARDED_DIR / f"{row_c['id']}.request.json").write_text(json.dumps({"id": row_c["id"]}), encoding="utf-8")
    (ob.GUARDED_DIR / f"{row_c['id']}.heartbeat").write_text("x", encoding="utf-8")
    check("a live client's request is not swept", guard.sweep(g2) == [])
    ob.HEARTBEAT_STALE_SECONDS = 0.05
    time.sleep(0.2)
    sw = guard.sweep(g2)
    check("a killed client (stale heartbeat, never claimed) is swept to CANCELLED_UNCLAIMED", len(sw) == 1 and guard.read_log(g2)[row_c["id"]]["status"] == "CANCELLED_UNCLAIMED")
    guard.mark(g2, row_c["id"], "voided")
    row_d = guard.before(ctx, pay_still(g2, "f01"))
    (ob.GUARDED_DIR / f"{row_d['id']}.heartbeat").write_text("x", encoding="utf-8")
    time.sleep(0.2)                                  # no request file left = a servicer claimed it
    guard.sweep(g2)
    check("a killed client whose request was already claimed is swept to LATE_PENDING (not voidable)", guard.read_log(g2)[row_d["id"]]["status"] == "LATE_PENDING")
    guard.mark(g2, row_d["id"], "voided")
    ob.HEARTBEAT_STALE_SECONDS = 60.0

    # past not_after: the servicer refuses, no generate
    gen_before = len(GEN)
    ob.GUARDED_DIR.mkdir(parents=True, exist_ok=True)
    (ob.GUARDED_DIR / "deadbeef.heartbeat").write_text("x", encoding="utf-8")
    (ob.GUARDED_DIR / "deadbeef.request.json").write_text(json.dumps({"id": "deadbeef", "not_after": time.time() - 5,
                        "heartbeat": str(ob.GUARDED_DIR / "deadbeef.heartbeat"), "payload": pay_still(g2, "f01"), "priced": {}}), encoding="utf-8")
    with servicers(Servicer("late2")):
        time.sleep(0.4)
    rep = json.loads((ob.RESPONSES_DIR / "deadbeef.response.json").read_text())
    check("a request past not_after is refused by the servicer: no generate call, error reply, moved to cancelled/",
          len(GEN) == gen_before and rep["status"] == "error" and (ob.CANCELLED_DIR / "deadbeef.request.json").exists())

    # an error reply WITH a creation_id: settle by fetch, never by a new render
    gen_before = len(GEN)
    with servicers(Servicer("err", mode="error_after_submit")):
        try:
            submit(g2, "pictures", "f01", pay_still(g2, "f01"))
        except ob.OpenArtBridgeError:
            pass
    rid_e = next(iter(guard.open_rows(g2)))["id"]
    check("an error reply with a creation_id leaves the row UNRESOLVED, creation_id stored", guard.read_log(g2)[rid_e]["status"] == "UNRESOLVED"
          and guard.read_log(g2)[rid_e]["creation_id"].startswith("cr_"))
    ok_e, why_e = guard.fetch(g2, rid_e)
    check("fetch settles it: ONE generate call in total, the file lands", ok_e and len(GEN) == gen_before + 1 and guard.png_path(g2, "f01").exists(), why_e)

    # typed sent_params and no record dump: UNRESOLVED
    with servicers(Servicer("typed", mode="no_record")):
        try:
            submit(g2, "pictures", "f03", pay_still(g2, "f03"))
        except ob.OpenArtBridgeError:
            pass
    rid_f = next(iter(guard.open_rows(g2)))["id"]
    check("a reply with typed sent_params but no creation record is UNRESOLVED; the file stays in staging",
          guard.read_log(g2)[rid_f]["status"] == "UNRESOLVED" and not guard.png_path(g2, "f03").exists() and list(ob.STAGING_DIR.glob(f"{rid_f}.*")))
    check("confirm of an OpenArt row with a typed amount and no record dump is REFUSED", raises(guard.SpendRefused, guard.confirm, g2, rid_f, "typed 40 2026-11-15", None, 40.0))
    rec_dump = tmp / "rec_dump.json"
    rec_dump.write_text(json.dumps({"creation_id": guard.read_log(g2)[rid_f]["creation_id"], "sent_params": guard.read_log(g2)[rid_f]["priced"],
                                    "credits_spent": 40}), encoding="utf-8")
    ok_f, why_f = guard.confirm(g2, rid_f, "saved record dump 2026-11-15", rec_dump)
    check("confirm --receipt <saved record dump> settles it and moves the staged file", ok_f and guard.png_path(g2, "f03").exists(), why_f)

    # record shows sound ON: UNRESOLVED (a clip row; stills have no sound field)
    gc = mk_guard_ep("ep_gc")
    for t in ss.TAGS:
        mk_png(guard.png_path(gc, t), 61)
    guard.record_gate(gc, "stills_animatic", "page 4 go 2026-11-15")
    docc = json.loads((gc / "unit_timing.json").read_text(encoding="utf-8"))
    grant(gc, "clips", doc=docc)
    with servicers(Servicer("snd2", mode="sound_on")):
        try:
            submit(gc, "clips", "f04", pay_anim(gc, "f04", 7))
        except ob.OpenArtBridgeError:
            pass
    rid_h = next(iter(guard.open_rows(gc)))["id"]
    check("a creation record that shows sound ON is UNRESOLVED (never confirmed)", guard.read_log(gc)[rid_h]["status"] == "UNRESOLVED"
          and not guard.clip_path(gc, "f04").exists() and "sent_params" in guard.read_log(gc)[rid_h]["error"])
    guard.mark(gc, rid_h, "voided")
    with servicers(Servicer("over", mode="over_price")):
        try:
            submit(gc, "clips", "f04", pay_anim(gc, "f04", 7))
        except ob.OpenArtBridgeError:
            pass
    rid_i = next(iter(guard.open_rows(gc)))["id"]
    check("a record above 110% of the price is UNRESOLVED", guard.read_log(gc)[rid_i]["status"] == "UNRESOLVED")
    over_dump = tmp / "over_dump.json"
    over_dump.write_text(json.dumps({"creation_id": guard.read_log(gc)[rid_i]["creation_id"], "sent_params": guard.read_log(gc)[rid_i]["priced"],
                                     "credits_spent": 368}), encoding="utf-8")
    guard.confirm(gc, rid_i, "accepted the real figure 2026-11-15", over_dump)
    check("the real figure above the row price confirms it but LOCKS the step until a new grant",
          guard.read_log(gc)[rid_i]["over_price"] and raises(guard.SpendRefused, guard.before, guard.GuardCtx(gc, "clips", "f04", "anim", "p"), pay_anim(gc, "f04", 7)))
    guard.approve(gc, "clips", 280, "cr", "owner: one more, at most 280 cr, 2026-11-15", 9999, "f04", 1)
    check("a new grant lifts the lock", guard.before(guard.GuardCtx(gc, "clips", "f04", "anim", "p"), pay_anim(gc, "f04", 7))["status"] == "requested")

    # two servicers, one request -> exactly one generate call
    gen_before = len(GEN)
    gd = mk_guard_ep("ep_gd")
    grant(gd, "pictures")
    with servicers(Servicer("A"), Servicer("B")):
        submit(gd, "pictures", "f04", pay_still(gd, "f04"))
    check("two servicers, one request -> exactly one generate call", len(GEN) == gen_before + 1)

    # reconcile
    creations = [{"creation_id": "cr_unknown", "prompt_sha256": "abc"}, {"creation_id": "cr_logged", "prompt_sha256": "abc"},
                 {"creation_id": "cr_other", "prompt_sha256": "zzz"}]
    guard.mark(gd, next(iter(guard.read_log(gd))), creation_id="cr_logged")
    fl = guard.reconcile(gd, creations, {"abc"})
    check("reconcile flags a creation that matches an episode prompt but is not in the log", [c["creation_id"] for c in fl] == ["cr_unknown"])

    # ===================================================================== T6b / T10 / T10b ===
    section("T6b", "ElevenLabs boundary: fixed commands, char price, _turns, no free-form, no cached billing")
    ev = mk_guard_ep("ep_ev")
    (ev / "narration-tagged.md").write_text(
        'Narrator line one here. <speaker name="john">[plain] I am not the Christ.</speaker> Narrator line two.', encoding="utf-8")
    units_ev = ev / "_turns"
    units_ev.mkdir()
    (units_ev / ".text_sha256").write_text("OLD", encoding="utf-8")
    (units_ev / "00_narrator.mp3").write_bytes(b"x")
    check("prepare_turns DELETES _turns when the text hash changed", run.prepare_turns(ev) is True and not (units_ev / "00_narrator.mp3").exists())
    (units_ev / "00_narrator.mp3").write_bytes(b"x")
    check("...and keeps it when the hash is the same", run.prepare_turns(ev) is False and (units_ev / "00_narrator.mp3").exists())
    n_c, c_c = run.voice_chars(ev)
    chunks_ev = run._tagged_chunks(ev)
    full = sum(len(t) for sp_, t in chunks_ev if sp_ == "narrator")
    check("voice quote = characters of the UNCACHED turns only (cached narrator turn 0 costs nothing)",
          (n_c, c_c) == (full - len(chunks_ev[0][1]), len("I am not the Christ.")), f"{n_c} {c_c}")
    (units_ev / ".text_sha256").write_text("OLD", encoding="utf-8")
    check("a changed text means EVERYTHING is uncached again", run.voice_chars(ev) == (full, len("I am not the Christ.")))
    check("price = chars x 2 passes at the invoice rate (+ alignment)", abs(guard.eleven_price_voice(100, 50) - 300 * guard.ELEVEN_USD_PER_CHAR) < 1e-9)
    check("the ElevenLabs rates are flagged UNVERIFIED until a receipt", guard.ELEVEN_RATES_VERIFIED is False)
    gv_ = mk_guard_ep("ep_gv", voice_ear=False)
    qv = guard.write_quote(gv_, "voice", 0.6, 0.1, {})
    check("voice quote: at most = ceil((0.60 + 0.10) x 1.10 to the cent) = 0.77", qv["at_most"] == 0.77, str(qv))
    check("approve voice (usd) needs the cap number and a date in the note", raises(guard.SpendRefused, guard.approve, gv_, "voice", 0.77, "usd", "yes 2026-11-15")
          and guard.approve(gv_, "voice", 0.77, "usd", "owner: about 0.60, at most 0.77, yes 2026-11-15")["cap"] == 0.77)
    check("no free-form paid command: 'paid' / 'curl' are not whitelisted", raises(guard.SpendRefused, guard.eleven_before, gv_, "paid", 0.1)
          and raises(guard.SpendRefused, guard.eleven_before, gv_, "per_turn_synth", 0.1))
    check("the whitelist is exactly voice / align / score", guard.ELEVEN_COMMANDS == ("voice", "align", "score"))
    rv = guard.eleven_before(gv_, "voice", 0.1, guard.sha256_of(gv_ / "narration-tagged.md"))
    guard.eleven_finish(gv_, rv["id"], True)
    check("an ElevenLabs row stays OPEN until a typed confirm (one open row blocks the next command)",
          guard.read_log(gv_)[rv["id"]]["status"] == "UNRESOLVED" and raises(guard.SpendRefused, guard.eleven_before, gv_, "voice", 0.1))
    guard.confirm(gv_, rv["id"], "invoice line 2026-11-15", None, 0.1)
    check("align before the owner picked a take (voice_ear) is refused", raises(guard.SpendRefused, guard.eleven_before, gv_, "align", 0.05, guard.sha256_of(gv_ / "narration.mp3")))
    guard.record_gate(gv_, "voice_ear", "take A 2026-11-15")
    check("voice is closed once voice_ear is recorded", raises(guard.SpendRefused, guard.eleven_before, gv_, "voice", 0.1))
    ra = guard.eleven_before(gv_, "align", 0.05, guard.sha256_of(gv_ / "narration.mp3"))
    guard.eleven_finish(gv_, ra["id"], True)
    guard.confirm(gv_, ra["id"], "invoice line 2026-11-15", None, 0.05)
    check("align a second time for the SAME audio hash is refused", raises(guard.SpendRefused, guard.eleven_before, gv_, "align", 0.05, guard.sha256_of(gv_ / "narration.mp3")))
    check("an ElevenLabs request above the cap is refused", raises(guard.SpendRefused, guard.eleven_before, gv_, "voice", 5.0))
    check("build_srt.build() REFUSES a marked folder (no unlogged paid alignment)", raises(RuntimeError, build_srt.build, gv_))
    check("build_srt.build_from_cache raises when there is no cache (it never aligns)", raises(FileNotFoundError, build_srt.build_from_cache, gv_))
    import pipeline.assembly_align as aa
    real_align = aa.align
    aa.align = lambda *a, **k: (_ for _ in ()).throw(AssertionError("align() was called"))
    try:
        shutil.copy(gdir / "narration.alignment.json", gv_)
        out_srt = build_srt.build_from_cache(gv_)
        check("build_from_cache builds the .srt from the cached alignment and NEVER calls align", out_srt.exists() and "-->" in out_srt.read_text())
    finally:
        aa.align = real_align

    section("T10b", "G2w: the audio says the words (local, $0)")
    units_w = json.loads((fx / "units.json").read_text(encoding="utf-8"))
    heard_ok = " ".join(units_w.values())
    check("G2w: audio that says the words passes", ss.audio_says_words(units_w, heard_ok)[0].verdict == "PASS")
    bad_u = dict(units_w)
    heard_bad = " ".join(("totally different words about something else entirely here now" if t == "f03" else v) for t, v in units_w.items())
    check("G2w: a turn that says OTHER words FAILs (stale audio)", has_fail(ss.audio_says_words(units_w, heard_bad)))
    _w = heard_ok.split(); heard_small = " ".join(_w[:20] + _w[22:])
    check("G2w: two missing words inside one page still pass (10% film / 25% unit thresholds)", ss.audio_says_words(units_w, heard_small)[0].verdict == "PASS")
    try:
        from faster_whisper import WhisperModel
        wm = WhisperModel("base", device="cpu", compute_type="int8", local_files_only=True)
        e13 = HERE / "swirls_episode_13_the_cross_that_wasnt_his"
        ws = [w["text"] for w in json.loads((e13 / "narration.alignment.json").read_text(encoding="utf-8"))["words"] if any(c.isalnum() for c in w["text"])]
        u13, i = {}, 0
        for tag, n in [("front", 14), ("f01", 25), ("f02", 21), ("f03", 22), ("f04", 14), ("f05", 28), ("f06", 28), ("f07", 17), ("f08", 13), ("f09", 21), ("back", 24)]:
            u13[tag] = " ".join(ws[i:i + n])
            i += n
        segs, _ = wm.transcribe(str(e13 / "narration.mp3"), language="en")
        heard13 = " ".join(s.text for s in segs)
        gw13 = ss.audio_says_words(u13, heard13)
        check("G2w: the REAL ep13 audio against its own words passes (sets the thresholds)", gw13[0].verdict == "PASS", gw13[0].evidence)
        print("      (ep13 result:", gw13[0].evidence, ")")
    except Exception as e:  # model not cached / no whisper: never download in a $0 test
        skip("G2w on the real ep13 audio", f"local whisper model unavailable ({type(e).__name__}); thresholds unverified on real audio")

    # ============================================================================ T12 ===
    section("T12", "NO-SPEND DRY RUN: the real cmd_* in the guarded order, real bridge files, mocks underneath")
    import swirls_episode as se
    T12_BASE = Path(os.environ["SWIRLS_T12_DIR"]) if os.environ.get("SWIRLS_T12_DIR") else tmp
    T12_BASE.mkdir(parents=True, exist_ok=True)
    D12 = T12_BASE / "swirls_episode_99_dry_run"
    if D12.exists():
        shutil.rmtree(D12)
    BRIDGE12 = tmp / "bridge12"
    ob.configure(BRIDGE12)
    GEN.clear()

    LINES = {
        "front": "Who answers the desert voice",
        "f01": "Priests came from the city to ask the stranger, Who art thou?",
        "f02": "He confessed, and denied not. I am not the Christ, he said plainly",
        "f03": "They pressed him again, and he pointed to Isaiah the prophet",
        "f04": "He said, I am the voice of one crying in the wilderness",
        "f05": "Isaiah wrote of a voice: Prepare ye the way of the LORD",
        "f06": "The prophet pointed past himself to someone standing among the people",
        "back": "Behold the Lamb of God, here he is",
    }
    TAGGED = {
        "front": "[quiet] Who answers the desert voice",
        "f01": 'Priests came from the city to ask the stranger, <speaker name="priests">[curious] Who art thou?</speaker>',
        "f02": '[serious] He confessed, and denied not. <speaker name="john">[plain] I am not the Christ.</speaker> he said plainly',
        "f03": "[steady] They pressed him again, and he pointed to Isaiah the prophet",
        "f04": '[warm] He said, <speaker name="john">[steady] I am the voice of one crying in the wilderness</speaker>',
        "f05": "[reflective] Isaiah wrote of a voice: Prepare ye the way of the LORD",
        "f06": "[reflective] The prophet pointed past himself to someone standing among the people",
        "back": "[tender] Behold the Lamb of God, here he is",
    }
    DATA = {
        "f01": {"labels": ["priests", "city", "stranger"], "caption": "who art thou"},
        "f02": {"labels": ["confessed", "denied", "Christ"], "caption": "he said plainly"},
        "f03": {"labels": ["pressed", "pointed", "Isaiah"], "caption": "the prophet"},
        "f04": {"labels": ["said", "voice", "crying"], "caption": "in the wilderness"},
        "f05": {"labels": ["Isaiah", "voice", "way"], "caption": "of the lord"},
        "f06": {"labels": ["prophet", "himself", "someone"], "caption": "among the people"},
    }
    for t in DATA:
        DATA[t]["stage"] = ss.MOTIF_STAGE[t]
    WORDS12 = {t: len(ss.norm_tokens(v)) for t, v in LINES.items()}
    SPANS = [
        {"ref": "John 1:19", "speaker": "priests", "text": "Who art thou?"},
        {"ref": "John 1:20", "speaker": "john", "text": "I am not the Christ."},
        {"ref": "John 1:23", "speaker": "john", "text": "I am the voice of one crying in the wilderness,"},
        {"ref": "Isaiah 40:3", "speaker": "narrator", "text": "Prepare ye the way of the LORD"},
        {"ref": "John 1:29", "speaker": "narrator", "text": "Behold the Lamb of God"},
    ]
    PLAN12 = {"north_star": "f04", "units": {t: {"full_figures": 2, "crowd": False,
                                                   "motion_carrier": {"f01": "a lamp flame", "f02": "the river reeds"}.get(t, "a reed"),
                                                   "motif_stage": ss.MOTIF_STAGE[t], "subjects": ["John"] if t in ("f02", "f04") else []}
                                             for t in ss.TAGS}}
    EPISODE_PY = '''"""Synthetic dry-run episode (T12): plumbing and order only, nothing about film quality."""
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
POC = Path(r"@@POC@@")
sys.path.insert(0, str(POC))
sys.path.insert(0, str(POC / "test_the_cross"))
from swirls_assemble import DuckProfile, EpisodeManifest, ScoreVariant, Unit  # noqa: E402
from swirls_cover import CoverSpec  # noqa: E402
from swirls_page import PageSpec, Panel, Ref  # noqa: E402

NAME = HERE.name
TAGS = ["front", "f01", "f02", "f03", "f04", "f05", "f06", "back"]
_T = json.loads((HERE / "unit_timing.json").read_text(encoding="utf-8"))["units"] if (HERE / "unit_timing.json").exists() else {}


def _cd(tag, default):
    return _T.get(tag, {}).get("clip_duration", default)


DATA = @@DATA@@
WORDS = @@WORDS@@
CLOSER0 = "the page carries no unusual ink: every figure and the paper beneath them are free of any ink."
CLOSER1 = ("the one brushstroke of blue ink is the only unusual ink on the page, and every figure and the "
           "paper beneath them are free of any ink.")


def page(tag):
    d = DATA[tag]
    stage = d["stage"]
    still = ("a plain dusk riverbank; the priests stand apart." if stage == 0 else
             "a plain dusk riverbank with two men; a brushstroke of blue ink runs left to right across the dry ground.")
    refs = [Ref("John", str(HERE / "refs" / "john.png"))] if tag == "f02" else []
    return PageSpec(
        seq_title="The Desert Voice", frame_label=tag.upper(),
        panels=tuple(Panel(l, c) for l, c in zip(d["labels"], ("a reed in the wind", "a pair of sandals", "a flat stone"))),
        still_shot_type="medium wide shot", anim_shot_desc="medium wide shot",
        main_scene_still=still, material_closer=CLOSER0 if stage == 0 else CLOSER1,
        panel_motions=("the light warms slowly", "haze drifts", "a reed leans gently"),
        main_scene_animation="the reeds sway, then the lamp flame leans.",
        fence_kind="none", caption_lines=(d["caption"],), corner_note="", refs=refs,
        include_no_bubble_clause=False, panel_style="woodcut_hybrid", clip_duration=_cd(tag, 7))


def cover(side):
    return CoverSpec(side=side, scene="a lone figure on a dusk riverbank", lighting="warm amber light against a cool grey sky",
                     title="The Desert Voice", subtitle="John 1:19-29", title_position="top" if side == "front" else "bottom",
                     animation="wind moves the grass and the robe edge", clip_duration=_cd(side, 4))


PAGES = {t: page(t) for t in TAGS[1:-1]}
COVERS = {"front": cover("front"), "back": cover("back")}


def _src(tag):
    return HERE / (f"{tag}_cover.mp4" if tag in ("front", "back") else f"{NAME}_{tag}_9x16.mp4")


MANIFEST = EpisodeManifest(
    episode_dir=HERE, narration=HERE / "narration.mp3",
    units=[Unit(t, _src(t), WORDS[t], "trim") for t in TAGS],
    scores={"piano": ScoreVariant(score=HERE / "score_piano.mp3", duck=DuckProfile(-12.0, 0.12, 2.5, 250), out=HERE / f"{NAME}_piano.mp4")},
    panel_style="woodcut_hybrid", w=1080, h=1920)
'''.replace("@@POC@@", str(HERE)).replace("@@DATA@@", repr(DATA)).replace("@@WORDS@@", repr(WORDS12))

    # ---- mocks under the commands: speech tools, aligner, whisper, score, Vision ------------------
    SYNTH_PASSES: list[float] = []
    base_clip = tmp / "base15.mp4"
    mk_clip(base_clip, 15.0, "1072x1928")

    def asset12(payload: dict, path: Path, rid: str) -> None:
        if payload["kind"] == "still":
            r = np.random.default_rng(int(rid[:6], 16))
            Image.fromarray(r.integers(90, 220, (480, 270, 3)).astype("uint8")).save(path, format="PNG")
        else:
            ff("-i", str(base_clip), "-t", str(payload["duration"]), "-c", "copy", str(path))

    def fake_run(cmd, env=None, cwd=None):
        name = Path(cmd[1]).name
        if name == "per_turn_synth.py":
            stab = float(cmd[cmd.index("--stability") + 1])
            SYNTH_PASSES.append(stab)
            folder = Path(cmd[2])
            for i, (sp_, text) in enumerate(run._tagged_chunks(folder)):
                f_ = folder / "_turns" / f"{i:02d}_{sp_}.mp3"
                if not f_.exists():
                    mk_audio(f_, 0.5, freq=200 + int(stab * 100))
            mk_audio(folder / "narration.mp3", 42.3, freq=240 + 10 * len(SYNTH_PASSES))
            return 0
        if name == "generate_score_piano.py":
            assert env and env.get("SWIRLS_RUN_SCORE") == run.score_token(Path(cwd)), "the score script must get the runner's token"
            mk_audio(Path(cwd) / "score_piano.mp3", 50.0, freq=440)
            return 0
        if name == "build_sfx.py":
            return subprocess.run([sys.executable, cmd[1]], env={**os.environ, **(env or {}), "JITB_ROOT": str(REPO)}, cwd=cwd).returncode
        raise AssertionError(f"unexpected command {cmd}")

    def fake_align(d: Path):
        words, t = [], 0.1
        for tag in ss.TAGS:
            for w in LINES[tag].split():
                words.append({"text": w, "start": round(t, 3), "end": round(t + 0.45, 3)})
                t += 0.5
        (d / "narration.alignment.json").write_text(json.dumps({"words": words}), encoding="utf-8")
        return words

    run.HOOKS["run"] = fake_run
    run.HOOKS["eleven_align"] = fake_align
    run.HOOKS["whisper"] = lambda mp3: " ".join(LINES.values())
    run.HOOKS["vision_ok"] = lambda: True
    STEM_UNIT = {}

    def unit_of(stem: str) -> str:
        if stem.startswith("front_cover"):
            return "front"
        if stem.startswith("back_cover"):
            return "back"
        return next(t for t in ss.TAGS[1:-1] if f"_{t}_" in stem)

    def vision12(image_bytes, role, user_text, label):
        kind, _, stem = label.partition(":")
        unit = unit_of(stem)
        spec = (EP12.PAGES.get(unit) or EP12.COVERS.get(unit))
        exp = sv.expected_baked_texts(spec)
        pu = PLAN12["units"][unit]
        if kind == "swirls-still-v3":
            return {"texts_seen": list(exp), "full_figures": pu["full_figures"], "crowd": False, "speech_bubble": False,
                    "motif_marks": [{"colour": "blue", "where": "ground"}] if pu["motif_stage"] else [],
                    "motif_bad_shape": False, "drawn_border": False, "caption_bottom_pct": 55}
        return {"frames": [{"texts_seen": list(exp), "full_figures": pu["full_figures"]}] * 6, "speech_bubble": False, "new_text": False,
                "ink_changed": False, "still_thing_moving": False, "bare_skin": False, "mouth_changed": False, "drift": False}

    sv._vision_raw = vision12
    os.environ["SWS_SKIP_NARRATION_GATE"] = "1"   # the synthetic words are not prose; G1g is a repo tool, wired + checked on a real narration below
    _n16 = HERE / "swirls_episode_16_let_the_little_children" / "narration.md"
    if _n16.exists():
        check("T12 G1g (narration_gate.py) is wired and returns a SWS-G1g verdict on a real narration", ss.run_narration_gate(_n16)[0].gate == "SWS-G1g")
    say_buf = io.StringIO()

    def quiet(fn, *a, **k):
        """Run a real cmd_* but keep its console chatter out of the log (printed only if it returned False)."""
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            r_ = fn(*a, **k)
        if r_ is False:
            print(buf.getvalue()[-900:])
        say_buf.write(buf.getvalue())
        return r_

    def ok_step(label, fn, *a, **k):
        r_ = quiet(fn, *a, **k)
        check(f"T12 {label}", r_ is not False and r_ is not None or r_ is True)
        return r_

    def note_for(cap, cur="cr"):
        return f"owner: yes, about it, at most {cap:g}{' cr' if cur == 'cr' else ''}, 2026-11-15"

    # 0. folder + marker
    check("T12 init: folder + marker", quiet(run.cmd_init, D12) is True and (D12 / ".swirls_short").exists())
    (D12 / "_DESIGN_BRIEF.md").write_text("John 1:19-29 (Isaiah 40:3 fulfilled; the voice and the Lamb)\n", encoding="utf-8")
    (D12 / "units.json").write_text(json.dumps(LINES), encoding="utf-8")
    (D12 / "narration.md").write_text("# spoken words only\n" + "\n".join(LINES.values()) + "\n", encoding="utf-8")
    (D12 / "narration-tagged.md").write_text("\n\n".join(TAGGED.values()) + "\n", encoding="utf-8")
    (D12 / "kjv_spans.json").write_text(json.dumps(SPANS), encoding="utf-8")
    check("T12 a paid command refuses before init (no marker) and an un-inited folder has no spend files", run.require_marker(tmp / "nope") is False)

    # 1. words
    ok_step("words: G1 / G1e / G1s / G1k / G1v / G1g all pass", run.cmd_words, D12)
    check("T12 ok words (a look, bound to the 3 text files)", quiet(run.cmd_ok, D12, "words", "owner picked the words 2026-11-15") is True)
    check("T12 a changed word voids the words look", (lambda: ((D12 / "narration.md").write_text((D12 / "narration.md").read_text() + "\n", encoding="utf-8"),
                                                              not guard.gate_valid(D12, "words"))[1])())
    (D12 / "narration.md").write_text("# spoken words only\n" + "\n".join(LINES.values()) + "\n", encoding="utf-8")
    quiet(run.cmd_ok, D12, "words", "owner picked the words again 2026-11-15")

    # 2. voice (ask 1)
    check("T12 quote voice", quiet(run.cmd_quote, D12, "voice") is True)
    qv12 = guard.read_quote(D12, "voice")
    check("T12 approve voice with the cap the owner saw", quiet(run.cmd_approve, D12, "voice", qv12["at_most"], "usd", None, note_for(qv12["at_most"], "usd")) is True)
    check("T12 voice: three passes (0.3 all, 0.65 narrator, 0.3 take B) and two takes built", quiet(run.cmd_voice, D12) is True
          and SYNTH_PASSES == [0.3, 0.65, 0.3] and (D12 / "narration_takeA.mp3").exists() and (D12 / "narration_takeB.mp3").exists()
          and sha(D12 / "narration_takeA.mp3") != sha(D12 / "narration_takeB.mp3"), str(SYNTH_PASSES))
    open_v = guard.open_rows(D12)
    check("T12 the voice row is OPEN (no history receipt): nothing else paid can run", len(open_v) == 1 and not run.cmd_align(D12))
    check("T12 confirm the voice row with a typed invoice amount", quiet(run.cmd_confirm, D12, open_v[0]["id"][:8], qv12["about"], "invoice line 2026-11-15") is True)
    check("T12 ok voice_ear --take A builds narration.mp3 from take A", quiet(run.cmd_ok, D12, "voice_ear", "take A by ear 2026-11-15", "A") is True
          and sha(D12 / "narration.mp3") == sha(D12 / "narration_takeA.mp3"))
    check("T12 align (ElevenLabs forced alignment, mocked) + G2w passes", quiet(run.cmd_align, D12) is True
          and json.loads((D12 / "narration.alignment.meta.json").read_text())["backend"] == "elevenlabs")
    open_a = guard.open_rows(D12)
    check("T12 align a second time for the same audio is refused", len(open_a) == 1 and quiet(run.cmd_confirm, D12, open_a[0]["id"][:8], guard.ELEVEN_ALIGN_USD, "invoice 2026-11-15") is True
          and quiet(run.cmd_align, D12) is False)

    # 3. timing + plan
    check("T12 timing from the real alignment (frames, clip lengths, G2/G3)", quiet(run.cmd_timing, D12, None, None) is True)
    doc12 = json.loads((D12 / "unit_timing.json").read_text(encoding="utf-8"))
    check("T12 the timing is the golden timing (clips 4,7,7,6,7,7,6,10 = 54 s)", [u["clip_duration"] for u in doc12["units"].values()] == [4, 7, 7, 6, 7, 7, 6, 10])
    (D12 / "episode.py").write_text(EPISODE_PY, encoding="utf-8")
    (D12 / "page_plan.json").write_text(json.dumps(PLAN12), encoding="utf-8")
    (D12 / "refs").mkdir(exist_ok=True)
    (D12 / "refs" / "refs.json").write_text(json.dumps({"refs": [{"name": "John", "file": "john.png", "from_still": "f04"}]}), encoding="utf-8")
    EP12 = se._load_episode(D12)
    check("T12 timing again with the manifest: Unit.words and 1080x1920 agree", quiet(run.cmd_timing, D12, {u.tag: u.words for u in EP12.MANIFEST.units},
                                                                                        (EP12.MANIFEST.w, EP12.MANIFEST.h)) is True)
    check("T12 a paid still before `plan` has passed is refused", quiet(se.cmd_still, EP12, "f04") is False and not guard.png_path(D12, "f04").exists())
    check("T12 plan: every plan gate passes (G3 G4 G5 G5a plan G6 G7a G8 G8t)", quiet(se.cmd_plan, EP12) is True)

    # 4. pictures (ask 2) + north star
    check("T12 quote pictures", quiet(run.cmd_quote, D12, "pictures") is True)
    qp = guard.read_quote(D12, "pictures")
    check("T12 approve pictures needs the balance and the cap", quiet(run.cmd_approve, D12, "pictures", qp["at_most"], "cr", 9000, note_for(qp["at_most"])) is True)
    GEN.clear()
    with servicers(Servicer("s12", asset=asset12)):
        check("T12 a second still before northstar_look is refused", quiet(se.cmd_still, EP12, "f01") is False and not guard.png_path(D12, "f01").exists() and not GEN)
        check("T12 still f04 (the north star) through the guarded bridge", quiet(se.cmd_still, EP12, "f04") is True and len(GEN) == 1 and guard.png_path(D12, "f04").exists())
        check("T12 hold f04 on its real slot (+ the 390 px phone proof)", quiet(run.cmd_hold, EP12, "f04") is True and (D12 / "_qc" / "hold_f04.mp4").exists()
              and Image.open(D12 / "_qc" / "phone_f04.jpg").width == 390)
        check("T12 ok northstar_look", quiet(run.cmd_ok, D12, "northstar_look", "page 3 looks right on a phone 2026-11-15") is True)
        # the hand-cropped ref (from the north-star page), bound to its source still
        im = Image.open(guard.png_path(D12, "f04"))
        im.crop((20, 40, 200, 300)).save(D12 / "refs" / "john.png")
        (D12 / "refs" / "refs.json").write_text(json.dumps({"refs": [{"name": "John", "file": "john.png", "from_still": "f04",
                                                                     "sha256": sha(D12 / "refs" / "john.png")}]}), encoding="utf-8")
        for t in ("f01", "f02", "f03", "f05", "f06", "front", "back"):
            check(f"T12 still {t}", quiet(se.cmd_still, EP12, t) is True and guard.png_path(D12, t).exists())
        check("T12 8 stills = 8 generate calls = 320 cr logged (a ref crop costs nothing)", len(GEN) == 8 and guard.spent(D12, "pictures") == 320)
        check("T12 verify: G9 strict audit + G10 + G14s + G7b + G7c on all 8 stills", quiet(se.cmd_verify, EP12) is True)
        check("T12 G7c: f02's request carried the John ref hash", guard.confirmed_row(D12, "still", "f02")["ref_sha256"].get("John") == sha(D12 / "refs" / "john.png"))
        check("T12 animatic + the contact sheet", quiet(run.cmd_animatic, EP12) is True and (D12 / "_qc" / "animatic.mp4").exists()
              and (D12 / "_qc" / "contact_sheet.jpg").exists())
        check("T12 ok stills_animatic closes the pictures step", quiet(run.cmd_ok, D12, "stills_animatic", "page 4 go 2026-11-15") is True)
        png_before = sha(guard.png_path(D12, "f01"))
        check("T12 a reroll after the closing gate is refused (and the file is kept)", quiet(se.cmd_still, EP12, "f01", True) is False
              and guard.png_path(D12, "f01").exists() and sha(guard.png_path(D12, "f01")) == png_before and len(GEN) == 8)

        # 5. clips (ask 3)
        check("T12 quote clips (35 cr x 54 s = 1,890 cr about)", quiet(run.cmd_quote, D12, "clips") is True and guard.read_quote(D12, "clips")["about"] == 1890)
        qc = guard.read_quote(D12, "clips")
        check("T12 approve clips", quiet(run.cmd_approve, D12, "clips", qc["at_most"], "cr", 9000, note_for(qc["at_most"])) is True)
        check("T12 a clip for any page but the two test clips is refused before clip_test_look", quiet(se.cmd_animate, EP12, "f01") is False
              and not guard.clip_path(D12, "f01").exists())
        n_gen = len(GEN)
        for t in ("f04", "back"):
            check(f"T12 animate {t} (test clip)", quiet(se.cmd_animate, EP12, t) is True and guard.clip_path(D12, t).exists())
            check(f"T12 clipqc {t}: G11 G14 G12 G13 (+ G15h on the back cover's last 3 s)", quiet(se.cmd_clipqc, EP12, t) is True)
        check("T12 the two test clips = 2 generate calls", len(GEN) == n_gen + 2)
        check("T12 re-running animate on a fresh clip buys nothing", quiet(se.cmd_animate, EP12, "f04") is True and len(GEN) == n_gen + 2)
        check("T12 ok clip_test_look", quiet(run.cmd_ok, D12, "clip_test_look", "page 5 back cover played to its end 2026-11-15") is True)
        for t in ("front", "f01", "f02", "f03", "f05", "f06"):
            check(f"T12 animate {t} + clipqc", quiet(se.cmd_animate, EP12, t) is True and quiet(se.cmd_clipqc, EP12, t) is True)
        check("T12 8 clips = 8 generate calls (plus 8 stills); clips logged = 1,890 cr = the quote", len(GEN) == 16 and guard.spent(D12, "clips") == 1890)

        # 6. draft
        check("T12 assemble --draft: frame-exact trim, 1080x1920, G14 over the manifest, G15, G15h", quiet(se.cmd_assemble, EP12, None, True) is True)
        rec12 = json.loads((D12 / "assembly_receipt.json").read_text(encoding="utf-8"))
        check("T12 the draft receipt carries each clip's hash = its confirmed spend row's output hash", all(
            u["src_sha256"] == guard.confirmed_row(D12, "anim", u["tag"])["output_sha256"] for u in rec12["units"]))
        check("T12 total frames = round(total x 30) and frames per unit are the golden ones", abs(rec12["total_frames"] - 1359) <= 1
              and [u["frames"] for u in rec12["units"]] == [78, 180, 195, 165, 180, 180, 165, 216], str([u["frames"] for u in rec12["units"]]))
        check("T12 ok draft_cut stores the draft's receipt hash and closes the clips step", quiet(run.cmd_ok, D12, "draft_cut", "page 6 approve the cut 2026-11-15") is True)
        try:
            submit(D12, "clips", "f01", pay_anim(D12, "f01", 7))
            closed_refused = False
        except ob.OpenArtBridgeError as e:
            closed_refused = "closed" in str(e)
        check("T12 any spend after the closing gate (draft_cut) is refused", closed_refused and len(GEN) == 16)

    # 7. score (ask 4) - the real template copy is only DRY-RUN (T14); the paid script is mocked here
    check("T12 quote score", quiet(run.cmd_quote, D12, "score") is True)
    qs = guard.read_quote(D12, "score")
    check("T12 approve score (usd)", quiet(run.cmd_approve, D12, "score", qs["at_most"], "usd", None, note_for(qs["at_most"], "usd")) is True)
    check("T12 score (the fixed command, runner token) + typed confirm", quiet(run.cmd_score, D12) is True
          and quiet(run.cmd_confirm, D12, guard.open_rows(D12)[0]["id"][:8], qs["about"], "invoice 2026-11-15") is True and (D12 / "score_piano.mp3").exists())
    check("T12 assemble --score piano (requests.post patched to RAISE: it still succeeds, no alignment is bought)",
          quiet(se.cmd_assemble, EP12, "piano", False) is True and (D12 / "assembly_receipt_scored.json").exists())
    check("T12 the .srt was built from the CACHED alignment", (D12 / f"{D12.name}.srt").exists())
    check("T12 the scored receipt chains the draft's", json.loads((D12 / "assembly_receipt_scored.json").read_text())["draft_receipt_sha256"] == sha(D12 / "assembly_receipt.json"))

    # 8. SFX copy + final
    shutil.copy(HERE / "_short_templates" / "build_sfx.py", D12 / "build_sfx.py")
    check("T12 finalize: the episode's own build_sfx.py (reads the scored receipt) + cache SRT + FINAL_VIDEO + chain + landing hold + G15 + G15h",
          quiet(se.run.cmd_finalize, EP12) is True and (D12 / "final_receipt.json").exists())
    fr12 = json.loads((D12 / "final_receipt.json").read_text(encoding="utf-8"))
    sc12 = json.loads((D12 / "assembly_receipt_scored.json").read_text(encoding="utf-8"))
    final_path = Path((D12 / "FINAL_VIDEO.txt").read_text().strip())
    check("T12 receipts chain: clip rows -> draft receipt -> scored receipt -> final receipt -> FINAL_VIDEO.txt", fr12["input_sha256"] == sc12["output_sha256"]
          and fr12["output_sha256"] == sha(final_path) and ss.check_chain(D12)[0].verdict == "PASS")
    rows12, nxt12, spend12 = ss.status(D12)
    check("T12 status says step 10 (the film panel) is next", nxt12.startswith("NEXT: step 10"), nxt12)
    check("T12 logged spend: pictures 320 cr (<= quote 400), clips 1,890 cr (= quote); voice and score closed by typed confirms",
          spend12["pictures"]["spent"] == 320 and spend12["clips"]["spent"] == 1890 and spend12["voice"]["spent"] > 0 and spend12["score"]["spent"] > 0)
    check("T12 no open rows are left", not guard.open_rows(D12))
    check("T12 only the guarded bridge folders were used (the legacy gen_requests/ is untouched)", not (BRIDGE12 / "gen_requests").exists()
          or not list((BRIDGE12 / "gen_requests").glob("*")))
    # film panel + owner's last look
    check("T12 ok film_final is refused with no film panel result", quiet(run.cmd_ok, D12, "film_final", "owner: fine 2026-11-15") is False)
    (D12 / "_qc").mkdir(exist_ok=True)
    seats_bad = [{"who": True, "what": True, "why": False, "curiosity": 8}, {"who": True, "what": True, "why": True, "curiosity": 6}]
    (D12 / "_qc" / "film_panel.json").write_text(json.dumps({"seats": seats_bad}), encoding="utf-8")
    check("T12 a panel that misses a 'why' / has a median under 7 is NOT PASSED", quiet(run.cmd_ok, D12, "film_final", "owner: fine 2026-11-15") is False
          and ss.film_panel_pass(seats_bad)[0] is False)
    seats_ok = [{"who": True, "what": True, "why": True, "curiosity": 8}, {"who": True, "what": True, "why": True, "curiosity": 7},
                {"who": True, "what": True, "why": True, "curiosity": 7}]
    (D12 / "_qc" / "film_panel.json").write_text(json.dumps({"seats": seats_ok}), encoding="utf-8")
    check("T12 a passing panel + the chain lets the owner record film_final", quiet(run.cmd_ok, D12, "film_final", "owner: fine 2026-11-15") is True
          and ss.film_panel_pass(seats_ok)[0] is True)
    with contextlib.redirect_stdout(io.StringIO()) as sbuf:
        run.cmd_status(D12)
    check("T12 status prints the open WARNs in plain words (WARN never counts as pass)", "Open WARNs" in sbuf.getvalue() or not ss.open_warns(D12))

    # ====================================================================== reconcile on the walk ===
    cre = [{"creation_id": "cr_stray", "prompt_sha256": guard.sha256_of(__import__("swirls_page").assemble_still_prompt(EP12.PAGES["f03"]))}]
    dump12 = tmp / "list12.json"
    dump12.write_text(json.dumps({"creations": cre}), encoding="utf-8")
    with contextlib.redirect_stdout(io.StringIO()):
        flagged = run.cmd_reconcile(D12, dump12, EP12)
    check("T12 reconcile flags a creation that matches an episode prompt but is not in the log", flagged is False)

    # =============================================================================== T14 ===
    section("T14", "parameterised score / SFX copies + G17 score gate")
    shutil.copy(HERE / "_short_templates" / "generate_score_piano.py", D12 / "generate_score_piano.py")
    env14 = {**os.environ, "JITB_ROOT": str(REPO)}
    env14.pop("SWIRLS_RUN_SCORE", None)
    r14 = subprocess.run([sys.executable, str(D12 / "generate_score_piano.py"), "--dry-run"], capture_output=True, text=True, env=env14, cwd=D12)
    inp14 = json.loads(r14.stdout) if r14.returncode == 0 else {}
    check("T14 score copy --dry-run reads its inputs from assembly_receipt.json / unit_timing.json / page_plan.json",
          r14.returncode == 0 and inp14.get("cut") == json.loads((D12 / "assembly_receipt.json").read_text())["output"]
          and abs(inp14["split"] - doc12["units"]["f04"]["start_s"]) < 1e-6 and inp14["north_star"] == "f04", r14.stderr[-300:])
    srcs14 = (D12 / "generate_score_piano.py").read_text(encoding="utf-8") + (D12 / "build_sfx.py").read_text(encoding="utf-8")
    check("T14 neither copy names another episode's file (no swirls_episode_NN, EP16, back_cover.mp4)", not any(x in srcs14 for x in (
        "swirls_episode_1", "swirls_episode_0", "EP16", "back_cover.mp4", "_REMOTION")))
    r14b = subprocess.run([sys.executable, str(D12 / "generate_score_piano.py")], capture_output=True, text=True, env=env14, cwd=D12)
    check("T14 the score copy EXITS when run directly (no runner token): a bare run can never spend", r14b.returncode != 0 and "refused" in (r14b.stdout + r14b.stderr))
    r14c = subprocess.run([sys.executable, str(D12 / "generate_score_piano.py")], capture_output=True, text=True, cwd=D12,
                          env={**env14, "SWIRLS_RUN_SCORE": "wrong"})
    check("T14 ...and with a wrong token", r14c.returncode != 0 and "refused" in (r14c.stdout + r14c.stderr))
    r14d = subprocess.run([sys.executable, str(D12 / "build_sfx.py"), "--dry-run"], capture_output=True, text=True, env=env14, cwd=D12)
    check("T14 the SFX copy runs on the T12 episode (--dry-run) and finalize already ran it for real", r14d.returncode == 0 and final_path.exists(), r14d.stderr[-300:])
    tot = 45.3
    good_s = tmp / "score_good.mp3"
    mk_audio(good_s, 50.0, 440)
    check("G17: a good score passes (length, no dead window, music in the last 3 s, no clipping)",
          ss.score_gate(good_s, tot, D12 / f"{D12.name}_piano.mp4", D12 / "narration.mp3")[0].verdict == "PASS")
    dead_s = tmp / "score_dead.mp3"
    ff("-f", "lavfi", "-i", "anullsrc=r=44100:cl=stereo:d=5", "-f", "lavfi", "-i", "sine=frequency=440:duration=45", "-filter_complex", "[0:a][1:a]concat=n=2:v=0:a=1", "-c:a", "libmp3lame", str(dead_s))
    check("G17: a score with a 5 s dead start FAILs", has_fail(ss.score_gate(dead_s, tot)))
    short_s = tmp / "score_short.mp3"
    mk_audio(short_s, 30.0, 440)
    check("G17: a score shorter than the film FAILs", has_fail(ss.score_gate(short_s, tot)))
    gap_s = tmp / "score_gap.mp3"
    ff("-f", "lavfi", "-i", "sine=frequency=440:duration=20", "-f", "lavfi", "-i", "anullsrc=r=44100:cl=stereo:d=6", "-f", "lavfi", "-i", "sine=frequency=440:duration=25",
       "-filter_complex", "[0:a][1:a][2:a]concat=n=3:v=0:a=1", "-c:a", "libmp3lame", str(gap_s))
    check("G17: a dead join in the middle FAILs", has_fail(ss.score_gate(gap_s, tot)))
    silent_tail = tmp / "mix_silent_tail.mp4"
    ff("-f", "lavfi", "-i", "testsrc2=s=54x96:r=30:d=9", "-f", "lavfi", "-i", "sine=frequency=440:duration=6", "-filter_complex", "[1:a]apad=whole_dur=9[a]",
       "-map", "0:v", "-map", "[a]", "-c:v", "libx264", "-pix_fmt", "yuv420p", "-c:a", "aac", "-t", "9", str(silent_tail))
    check("G17: no music in the last 3 s of the MIX FAILs", has_fail(ss.score_gate(good_s, 9.0, silent_tail)))
    check("T14 the copied templates are pinned with their sources", (HERE / "_short_templates" / "SOURCE.md").exists())

    # leave the dry-run folder only when asked to (inspection), else it goes with tmp
    if os.environ.get("SWIRLS_T12_DIR"):
        print(f"\n      T12 dry-run episode kept at: {D12}")


finally:
    ob.configure(Path(os.environ.get("AGENT_BRIDGE_DIR", REPO / ".agent_bridge")))
    shutil.rmtree(tmp, ignore_errors=True)

print("\n(scratch dir removed)")
total_checks = sum(len(v) for v in NAMES.values())
print(f"\n{total_checks} checks, {len(SKIPS)} skipped")
for s_ in SKIPS:
    print("  SKIPPED:", s_)
print("\nALL PASS" if not FAILS else f"\nSOME FAILED -- {FAILS}")
sys.exit(1 if FAILS else 0)
