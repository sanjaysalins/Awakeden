#!/usr/bin/env python
"""build_livingpage_16x9.py — the LIVING PAGE cut (v3 test): the comic as a master animator
would stage it, not as a template compositor fills it.

The language (all deterministic, $0 beyond the Kling clips):
  SLAM      panels do not sit in a grid — they arrive ON the narration's words: slide in
            over ~4 frames with a white impact flash in the panel and a decaying page shake.
  ALIVE     every panel is a moving source (Kling hero or $0 dynamic_cam) — never static.
  TAKEOVER  at the end of a beat the camera can dive INTO a chosen panel (zoompan toward
            its centre), so the cut lands inside the art, not on a wall of boxes.
  CONTRAST  sacred red-letter beats stay perfectly still — the stillness reads BECAUSE the
            rest of the page is alive.
  CRAFT     hand-wobbled ink borders + soft panel drop-shadows + halftone printing dots on
            the paper, so the page reads printed-and-inked, not vector-perfect.
  SOUND     each slam lands with a low boom (nail strike on "nailed", thunder on the storm)
            mixed UNDER the narration from the $0 sound_library.

Reuses the v2 machinery (caption tier solver + renderers, panel_fit crops, dynamic_cam,
frame-exact segments) via build_dyncomic_16x9; only the page compositor is new.

  .venv\\Scripts\\python.exe longform/02_Psalm_22_Song_From_The_Cross/build_livingpage_16x9.py --spec livingpage_m1.spec.json --clips
"""
import argparse, json, math, statistics, subprocess
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter

import build_dyncomic_16x9 as base
import caption_layout as cl
import panel_fit as pf

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
POOL = HERE / "v1" / "visual_16x9_inked"
WORK = POOL / "_livingpage_work"; WORK.mkdir(parents=True, exist_ok=True)
base.WORK = WORK                                  # caption states land in our work dir
ce = base.ce
PAGE = (1920, 1080)
SOUND = ROOT / "sound_library" / "clips"
PAPER = (252, 249, 241)
INK = (18, 14, 8, 255)
# Motion profiles (2026-07-14, user decision): the slam/shake feel is PER-PIECE via the spec's
# "motion" field, not global. "classic" = the original punchy look every already-approved piece
# was built with (default). "smooth" = the motion-sensitivity variant (no page shake, shorter
# slower slides, softer flash) the user asked for on women_first_witnesses.
MOTION_PROFILES = {
    "classic": dict(slide_h=60, slide_v=50, slide_dur=0.13, flash_a=0.6, flash_d=0.07,
                    shake_x=10.0, shake_y=7.0, shake_freq=70, shake_win=0.20),
    "smooth":  dict(slide_h=38, slide_v=32, slide_dur=0.22, flash_a=0.4, flash_d=0.05,
                    shake_x=0.0, shake_y=0.0, shake_freq=38, shake_win=0.16),
}


def set_motion_profile(name):
    global SLIDE_OFF, SLIDE_DUR, FLASH_ALPHA, FLASH_DUR
    global SHAKE_AMP_X, SHAKE_AMP_Y, SHAKE_FREQ, SHAKE_WIN
    p = MOTION_PROFILES[name]
    SLIDE_OFF = {"left": (p["slide_h"], 0), "right": (-p["slide_h"], 0),
                 "up": (0, p["slide_v"]), "down": (0, -p["slide_v"])}
    SLIDE_DUR, FLASH_ALPHA, FLASH_DUR = p["slide_dur"], p["flash_a"], p["flash_d"]
    SHAKE_AMP_X, SHAKE_AMP_Y = p["shake_x"], p["shake_y"]
    SHAKE_FREQ, SHAKE_WIN = p["shake_freq"], p["shake_win"]


set_motion_profile("classic")
run = base.run


_DIMS_CACHE = {}


def _dims(path):
    """Real (w,h) of a video source, ffprobed once and cached. REUSE FIX
    (backported 2026-07-19 from longform/04_The_Bronze_Serpent's 2026-07-16
    fix -- this copy never got it): panel-fit used to assume every source was
    PAGE-shaped (true for this episode's own 16:9 stills/Kling clips), which
    mis-solves the crop for a REUSED 9:16 clip_library clip dropped into a
    two_v/triptych_v column. Probing the actual file is backward-compatible
    (own sources ARE page-shaped, so this returns PAGE for them)."""
    p = str(path)
    if p not in _DIMS_CACHE:
        r = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0",
                            "-show_entries", "stream=width,height", "-of", "csv=p=0", p],
                            capture_output=True, text=True)
        try:
            w, h = r.stdout.strip().split(",")
            _DIMS_CACHE[p] = (int(w), int(h))
        except Exception:
            _DIMS_CACHE[p] = PAGE
    return _DIMS_CACHE[p]


# ---------------- craft assets (PIL, cached) ----------------
def halftone_bg():
    p = WORK / "_bg_halftone.png"
    if p.exists():
        return p
    img = Image.new("RGB", PAGE, PAPER)
    d = ImageDraw.Draw(img, "RGBA")
    for gy in range(0, PAGE[1], 7):
        for gx in range(0, PAGE[0], 7):
            if (gx // 7 + gy // 7) % 2 == 0:
                d.ellipse([gx, gy, gx + 1.6, gy + 1.6], fill=(120, 105, 85, 16))
    img.save(p)
    return p


def wobble_border(rect, tag):
    """Hand-inked border + soft drop shadow for one panel. Canvas has a margin so the
    shadow lives outside the panel; overlay at (x-M, y-M)."""
    M = 22
    x, y, w, h = rect
    p = WORK / f"_brd_{tag}_{w}x{h}.png"
    if p.exists():
        return p, M
    img = Image.new("RGBA", (w + 2 * M, h + 2 * M), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.rounded_rectangle([M + 9, M + 13, M + w + 9, M + h + 13], radius=8, fill=(20, 15, 10, 70))
    d.rectangle([M, M, M + w, M + h], fill=(0, 0, 0, 0))          # punch panel interior clear
    def edge(x0, y0, x1, y1, seed):
        n = max(2, int(math.hypot(x1 - x0, y1 - y0) / 36))
        pts = []
        for i in range(n + 1):
            t = i / n
            jx = math.sin(seed + i * 1.7) * 2.6
            jy = math.cos(seed * 1.3 + i * 2.1) * 2.6
            pts.append((x0 + (x1 - x0) * t + jx, y0 + (y1 - y0) * t + jy))
        d.line(pts, fill=INK, width=9, joint="curve")
    s = (w * 7 + h) % 97
    edge(M, M, M + w, M, s); edge(M + w, M, M + w, M + h, s + 11)
    edge(M + w, M + h, M, M + h, s + 23); edge(M, M + h, M, M, s + 37)
    img.save(p)
    return p, M


# ---------------- the living-page compositor ----------------
def compose_page(out, dur, panels, work):
    """panels: [{path, motion, bias, zoom, rect, at(rel), slide, flash, anchors?}] —
    overlays slam in at their `at` with slide + white flash; borders ride along."""
    feed, parts, chain = [], [], []
    for k, pn in enumerate(panels):
        feed.append(pn["path"])
    fc_in = len(feed)
    bg = halftone_bg()
    parts.append(f"[{fc_in}:v]setsar=1[bg]")
    prev = "bg"
    for k, pn in enumerate(panels):
        x, y, w, h = pn["rect"]
        clen = ce._clip_len(pn["path"])
        parts.append(ce._temporal(k, dur, pn["motion"], clen, f"t{k}"))
        if pn.get("anchors"):                       # fracture: crop this split at its anchor
            z, bx, by = pn["anchors"]
            parts.append(ce._panel_fill(f"t{k}", f"p{k}", w, h, z, bx, by))
        else:
            parts.append(ce._panel_fill(f"t{k}", f"p{k}", w, h, pn["zoom"], *pn["bias"]))
        at = pn.get("at", 0.0)
        brd, M = wobble_border(pn["rect"], f"p{k}")
        bi = len(feed) + 1 + k                      # borders appended after bg
        parts.append(f"[{bi}:v]format=rgba[b{k}]")
        if at <= 0.01:                              # present from frame 0
            parts.append(f"[{prev}][p{k}]overlay={x}:{y}[o{k}]")
            parts.append(f"[o{k}][b{k}]overlay={x - M}:{y - M}[w{k}]")
            prev = f"w{k}"
        else:
            offx, offy = SLIDE_OFF.get(pn.get("slide", "left"), SLIDE_OFF["left"])
            ex = f"{x}-{offx}*(1-min((t-{at:.3f})/{SLIDE_DUR},1))" if offx else str(x)
            ey = f"{y}-{offy}*(1-min((t-{at:.3f})/{SLIDE_DUR},1))" if offy else str(y)
            en = f"gte(t,{at:.3f})"
            parts.append(f"[{prev}][p{k}]overlay=x='{ex}':y='{ey}':enable='{en}'[o{k}]")
            exb = f"{x - M}-{offx}*(1-min((t-{at:.3f})/{SLIDE_DUR},1))" if offx else str(x - M)
            eyb = f"{y - M}-{offy}*(1-min((t-{at:.3f})/{SLIDE_DUR},1))" if offy else str(y - M)
            parts.append(f"[o{k}][b{k}]overlay=x='{exb}':y='{eyb}':enable='{en}'[w{k}]")
            prev = f"w{k}"
            if pn.get("flash", True):
                parts.append(f"color=c=white@{FLASH_ALPHA}:s={w}x{h}:r=30:d={dur},format=yuva420p[f{k}]")
                parts.append(f"[{prev}][f{k}]overlay={x}:{y}:enable='between(t,{at:.3f},{at + FLASH_DUR:.3f})'[fl{k}]")
                prev = f"fl{k}"
    parts.append(f"[{prev}]format=yuv420p[outv]")
    cmd = ["ffmpeg", "-y", "-loglevel", "error"]
    for pth in feed:
        cmd += ["-i", str(pth)]
    cmd += ["-loop", "1", "-framerate", "30", "-t", f"{dur}", "-i", str(bg)]
    for k, pn in enumerate(panels):
        brd, _ = wobble_border(pn["rect"], f"p{k}")
        cmd += ["-loop", "1", "-framerate", "30", "-t", f"{dur}", "-i", str(brd)]
    cmd += ["-filter_complex", ";".join(parts), "-map", "[outv]", "-r", "30",
            "-c:v", "libx264", "-crf", "18", "-preset", "medium", str(out)]
    run(cmd, f"compose {out.name}")
    return out


def apply_shake(seg, slams, dur):
    """Decaying page shake at each slam. Page pre-scaled 3% so the jitter never shows edges.
    Shake shape comes from the piece's motion profile; the "smooth" profile zeroes the amps
    (the panel slam-in carries the impact instead) — skip the re-encode entirely then."""
    if SHAKE_AMP_X == 0 and SHAKE_AMP_Y == 0:
        return
    def expr(amp):
        terms = [f"if(between(t,{a:.3f},{a + SHAKE_WIN:.3f}),{amp}*sin((t-{a:.3f})*{SHAKE_FREQ})*(1-(t-{a:.3f})/{SHAKE_WIN}),0)"
                 for a in slams]
        return "+".join(terms)
    W, H = PAGE
    sw, sh = round(W * 1.03 / 2) * 2, round(H * 1.03 / 2) * 2
    vf = (f"scale={sw}:{sh},crop={W}:{H}:"
          f"x='(iw-{W})/2+{expr(SHAKE_AMP_X)}':y='(ih-{H})/2+{expr(SHAKE_AMP_Y)}',setsar=1")
    tmp = seg.with_name(seg.stem + "_sh.mp4")
    run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(seg), "-vf", vf, "-r", "30",
         "-c:v", "libx264", "-crf", "18", "-preset", "veryfast", "-pix_fmt", "yuv420p", str(tmp)],
        f"shake {seg.name}")
    tmp.replace(seg)


def make_rays(png, page, at, strength):
    """Gold god-ray streak-fan + soft core glow as a full-page RGBA overlay (PIL, cached).
    Deterministic (sin-hash per ray, no RNG) so re-runs are byte-stable."""
    W, H = page
    cx, cy = at[0] * W, at[1] * H
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    dr = ImageDraw.Draw(img)
    aim = math.atan2(H / 2 - cy, W / 2 - cx)     # fan opens toward the page centre
    reach = math.hypot(W, H)
    for k in range(24):
        ang = aim + (k / 23 - 0.5) * math.radians(150)
        ln = reach * (0.55 + 0.45 * abs(math.sin(k * 12.9898)))
        hw = 14 + 60 * abs(math.sin(k * 4.1273))
        al = int(strength * (26 + 34 * abs(math.sin(k * 7.331))))
        tip = (cx + ln * math.cos(ang), cy + ln * math.sin(ang))
        perp = (math.cos(ang + math.pi / 2), math.sin(ang + math.pi / 2))
        dr.polygon([(cx, cy), (tip[0] + hw * perp[0], tip[1] + hw * perp[1]),
                    (tip[0] - hw * perp[0], tip[1] - hw * perp[1])],
                   fill=(255, 219, 145, al))
    img = img.filter(ImageFilter.GaussianBlur(16))
    glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    r = 0.14 * max(W, H)
    ImageDraw.Draw(glow).ellipse([cx - r, cy - r, cx + r, cy + r],
                                 fill=(255, 231, 178, int(110 * strength)))
    img.alpha_composite(glow.filter(ImageFilter.GaussianBlur(60)))
    img.save(png)


def apply_fx(seg, dur, fx, rects=None):
    """Bake the beat's viral effects in ONE fast re-encode of the ~4s segment — never a
    whole-video post-pass (the 2026-07-13 post-pass was minutes + GB files; this is instant).
    fx = spec per-beat {"temp": K, "rays": {"at": [fx,fy], "strength": 0..1, "opacity": 0..1}}:
    temp <6500 = warm resurrection light, >6500 = cool death/dark (SUBTLE — inked art is
    already warm); god-rays are the visible part. Runs after motion, BEFORE captions.
    rects: panel rects for paged templates — the grade applies only INSIDE them, because
    the ivory paper must stay constant across beats (a cool beat would print the page blue)."""
    rays, temp = fx.get("rays"), fx.get("temp")
    if not rays and not temp:
        return
    cmd = ["ffmpeg", "-y", "-loglevel", "error", "-i", str(seg)]
    chain, last = [], "[0:v]"
    if rays:
        at = rays.get("at", [0.5, 0.12])
        strength = rays.get("strength", 0.5)
        png = WORK / f"_rays_{PAGE[0]}x{PAGE[1]}_{at[0]:.2f}_{at[1]:.2f}_{strength:.2f}.png"
        if not png.exists():
            make_rays(png, PAGE, at, strength)
        cmd += ["-loop", "1", "-framerate", "30", "-t", f"{dur}", "-i", str(png)]
        # format BOTH sides to rgba before screen-blending or the gold turns MAGENTA
        chain.append(f"[0:v]format=rgba[b];[1:v]format=rgba[r];"
                     f"[b][r]blend=all_mode=screen:all_opacity={rays.get('opacity', 0.6)}[v]")
        last = "[v]"
    if temp and rects:
        chain.append(f"{last}split=2[fb][fg];[fg]colortemperature=temperature={int(temp)}[gt]")
        chain.append(f"[gt]split={len(rects)}" + "".join(f"[t{k}]" for k in range(len(rects))))
        for k, (x, y, w, h) in enumerate(rects):
            chain.append(f"[t{k}]crop={w}:{h}:{x}:{y}[c{k}]")
            chain.append(f"{'[fb]' if k == 0 else f'[b{k - 1}]'}[c{k}]overlay={x}:{y}[b{k}]")
        last = f"[b{len(rects) - 1}]"
    elif temp:
        chain.append(f"{last}colortemperature=temperature={int(temp)}[g]")
        last = "[g]"
    chain.append(f"{last}format=yuv420p[outv]")
    tmp = seg.with_name(seg.stem + "_fx.mp4")
    run(cmd + ["-filter_complex", ";".join(chain), "-map", "[outv]", "-r", "30",
               "-c:v", "libx264", "-crf", "18", "-preset", "veryfast", str(tmp)],
        f"fx {seg.name}")
    tmp.replace(seg)


def apply_camera(seg, dur, px, py, z_to, start):
    """Dive INTO the page toward (px,py): zoom 1 -> z_to from `start` to the beat end."""
    z = f"if(lt(time,{start:.3f}),1,min(1+({z_to}-1)*(time-{start:.3f})/({max(dur - start, 0.01):.3f}),{z_to}))"
    vf = (f"zoompan=z='{z}':x='{px}*(1-1/zoom)':y='{py}*(1-1/zoom)':d=1:s={PAGE[0]}x{PAGE[1]}:fps=30")
    tmp = seg.with_name(seg.stem + "_cm.mp4")
    run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(seg), "-vf", vf, "-r", "30",
         "-c:v", "libx264", "-crf", "18", "-preset", "veryfast", "-pix_fmt", "yuv420p", str(tmp)],
        f"camera {seg.name}")
    tmp.replace(seg)


def add_sfx(mp4, events, out):
    """Mix slam sounds UNDER the narration. events: (abs_t, name_or_path, gain_db[, dur, fade])."""
    cmd = ["ffmpeg", "-y", "-loglevel", "error", "-i", str(mp4)]
    parts = []
    for k, ev in enumerate(events, 1):
        t, src, g = ev[0], ev[1], ev[2]
        dur = ev[3] if len(ev) > 3 else 2.2
        fade = ev[4] if len(ev) > 4 else 0.6
        p = src if isinstance(src, Path) else SOUND / f"{src}.mp3"
        cmd += ["-i", str(p)]
        ms = round(t * 1000)
        parts.append(f"[{k}:a]atrim=0:{dur},afade=t=out:st={max(dur - fade, 0):.2f}:d={fade},"
                     f"volume={g}dB,adelay={ms}|{ms}[s{k}]")
    mix = "".join(f"[s{k}]" for k in range(1, len(events) + 1))
    parts.append(f"[0:a]{mix}amix=inputs={len(events) + 1}:duration=first:normalize=0,alimiter=limit=0.97[a]")
    cmd += ["-filter_complex", ";".join(parts), "-map", "0:v", "-map", "[a]",
            "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", str(out)]
    run(cmd, "sfx mix")
    return out


def make_heartbeat(dest: Path, dur: float, bpm: float = 66.0):
    """$0 synthesized heartbeat (lub-dub), crescendo over `dur`, built to STOP DEAD at the end."""
    import math, struct, wave
    sr = 44100
    period = 60.0 / bpm
    frames = bytearray()
    for i in range(int(dur * sr)):
        t = i / sr
        tc = t % period
        v = 0.0
        for off, f0, amp in ((0.0, 54.0, 1.0), (0.30 * period, 48.0, 0.7)):
            dt = tc - off
            if 0 <= dt < 0.14:
                v += amp * math.sin(2 * math.pi * f0 * dt) * math.exp(-dt * 34)
        gain = 0.35 + 0.65 * min(t / max(dur - 0.001, 0.001), 1.0)
        frames += struct.pack("<h", int(max(-1.0, min(1.0, v * gain)) * 32000))
    with wave.open(str(dest), "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(sr)
        w.writeframes(bytes(frames))
    return dest


def apply_ramp(seg: Path, dur: float, src_t: float = 0.8, speed: float = 2.5):
    """Viral speed ramp: the first `src_t`s of the beat's art plays at `speed`x, the rest
    stretches to refill the beat — fast-in, settle, cut. Duration is unchanged (frame-exact
    pass still runs last). NEVER on beats with mid-beat slams/border-break (their word-timed
    events would desync) — main() guards that."""
    if dur <= src_t + 0.4:
        return
    fast_out = src_t / speed
    slow = (dur - fast_out) / (dur - src_t)
    fc = (f"[0:v]trim=0:{src_t},setpts=PTS/{speed}[ra];"
          f"[0:v]trim={src_t},setpts=(PTS-STARTPTS)*{slow:.6f}[rb];"
          f"[ra][rb]concat=n=2:v=1:a=0,fps=30,setsar=1[v]")
    tmp = seg.with_name(seg.stem + "_rp.mp4")
    run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(seg), "-filter_complex", fc,
         "-map", "[v]", "-r", "30", "-c:v", "libx264", "-crf", "18", "-preset", "veryfast",
         "-pix_fmt", "yuv420p", str(tmp)], f"ramp {seg.name}")
    tmp.replace(seg)


def apply_whip(seg: Path):
    """Whip-cut INTO the beat: a horizontal motion-blur streak on the first ~3 frames, so the
    cut reads as camera energy instead of a hard splice. Pairs with a whoosh in the mix."""
    vf = "gblur=sigma=24:sigmaV=1:enable='lt(t,0.10)'"
    tmp = seg.with_name(seg.stem + "_wp.mp4")
    run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(seg), "-vf", vf, "-r", "30",
         "-c:v", "libx264", "-crf", "18", "-preset", "veryfast", "-pix_fmt", "yuv420p", str(tmp)],
        f"whip {seg.name}")
    tmp.replace(seg)


def apply_inserts(seg: Path, dur: float, t0: float, inserts: list):
    """FLASH-FRAME inserts: a full-bleed still stabbed in for ~4 frames (comic panel-burst).
    inserts: [{at(abs), slug, frames?}] — exempt from the reuse counters by design: a 3-frame
    recall of an already-seen image is the effect, not a reuse."""
    cmd = ["ffmpeg", "-y", "-loglevel", "error", "-i", str(seg)]
    parts, prev = [], "0:v"
    for k, ins in enumerate(inserts):
        cmd += ["-loop", "1", "-framerate", "30", "-t", f"{dur}", "-i",
                str(POOL / f"{ins['slug']}.png")]
        rel = max(0.0, ins["at"] - t0)
        end = rel + ins.get("frames", 4) / 30.0
        parts.append(f"[{k + 1}:v]scale={PAGE[0]}:{PAGE[1]}:force_original_aspect_ratio=increase,"
                     f"crop={PAGE[0]}:{PAGE[1]},setsar=1[i{k}]")
        parts.append(f"[{prev}][i{k}]overlay=0:0:enable='between(t,{rel:.3f},{end:.3f})'[v{k}]")
        prev = f"v{k}"
    parts.append(f"[{prev}]format=yuv420p[outv]")
    tmp = seg.with_name(seg.stem + "_in.mp4")
    cmd += ["-filter_complex", ";".join(parts), "-map", "[outv]", "-r", "30",
            "-c:v", "libx264", "-crf", "18", "-preset", "veryfast", "-pix_fmt", "yuv420p", str(tmp)]
    run(cmd, f"inserts {seg.name}")
    tmp.replace(seg)


def make_tick(dest: Path):
    """$0 cut-tick: a 60ms damped snap — texture on ordinary cuts so slams keep their rank."""
    import random, struct, wave
    sr = 44100
    rnd = random.Random(7)
    frames = bytearray()
    for i in range(int(0.06 * sr)):
        t = i / sr
        v = math.sin(2 * math.pi * 1900 * t) * math.exp(-t * 90) * 0.9
        v += (rnd.random() * 2 - 1) * math.exp(-t * 70) * 0.25
        frames += struct.pack("<h", int(max(-1.0, min(1.0, v)) * 32000))
    with wave.open(str(dest), "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(sr)
        w.writeframes(bytes(frames))
    return dest


def make_whoosh(dest: Path):
    """$0 whip whoosh: 0.35s dark filtered-noise swell, peaks ~40% in then dies."""
    import random, struct, wave
    sr = 44100
    rnd = random.Random(11)
    dur, prev = 0.35, 0.0
    frames = bytearray()
    for i in range(int(dur * sr)):
        x = (i / sr) / dur
        env = (x / 0.4) if x < 0.4 else max(0.0, 1.0 - (x - 0.4) / 0.6)
        prev = prev * 0.88 + (rnd.random() * 2 - 1) * 0.12          # one-pole lowpass = dark
        frames += struct.pack("<h", int(max(-1.0, min(1.0, prev * env * 3.2)) * 32000))
    with wave.open(str(dest), "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(sr)
        w.writeframes(bytes(frames))
    return dest


def border_frame_strips():
    """4 full-page transparent PNGs forming a hand-inked paper panel-frame (top/bottom/left/right).
    Used by the BORDER-BREAK move: the frame flies apart and the art bleeds off the page."""
    names = []
    T, S = 84, 128                       # top/bottom band height, side band width
    W, H = PAGE
    geo = {"bb_top": (0, 0, W, T), "bb_bottom": (0, H - T, W, T),
           "bb_left": (0, 0, S, H), "bb_right": (W - S, 0, S, H)}
    inner = {"bb_top": ("h", T), "bb_bottom": ("h", H - T), "bb_left": ("v", S), "bb_right": ("v", W - S)}
    for name, (x, y, w, h) in geo.items():
        p = WORK / f"_{name}.png"
        names.append(p)
        if p.exists():
            continue
        img = Image.new("RGBA", PAGE, (0, 0, 0, 0))
        d = ImageDraw.Draw(img)
        d.rectangle([x, y, x + w, y + h], fill=PAPER + (255,))
        axis, pos = inner[name]
        pts = []
        n = (W if axis == "h" else H) // 36
        for i in range(n + 1):
            t = i / n
            j = math.sin(7 + i * 1.7) * 2.6
            if axis == "h":
                pts.append((t * W, pos + j))
            else:
                pts.append((pos + j, t * H))
        d.line(pts, fill=INK, width=9, joint="curve")
        img.save(p)
    return names


def apply_border_break(seg: Path, dur: float, at: float):
    """The frame flies apart at `at` and the full-bleed art is released past the panel."""
    strips = border_frame_strips()
    off = f"3200*(t-{at:.3f})*(t-{at:.3f})+120*(t-{at:.3f})"
    move = {0: ("0", f"if(lt(t,{at:.3f}),0,-({off}))"),        # top -> up
            1: ("0", f"if(lt(t,{at:.3f}),0,({off}))"),         # bottom -> down
            2: (f"if(lt(t,{at:.3f}),0,-({off}))", "0"),        # left -> left
            3: (f"if(lt(t,{at:.3f}),0,({off}))", "0")}         # right -> right
    cmd = ["ffmpeg", "-y", "-loglevel", "error", "-i", str(seg)]
    for p in strips:
        cmd += ["-loop", "1", "-framerate", "30", "-t", f"{dur}", "-i", str(p)]
    parts, prev = [], "0:v"
    for k in range(4):
        ex, ey = move[k]
        parts.append(f"[{k + 1}:v]format=rgba[b{k}]")
        out = f"o{k}" if k < 3 else "vout"
        parts.append(f"[{prev}][b{k}]overlay=x='{ex}':y='{ey}'[{out}]")
        prev = out
    parts.append("[vout]format=yuv420p[outv]")
    tmp = seg.with_name(seg.stem + "_bb.mp4")
    cmd += ["-filter_complex", ";".join(parts), "-map", "[outv]", "-r", "30",
            "-c:v", "libx264", "-crf", "18", "-preset", "veryfast", "-pix_fmt", "yuv420p", str(tmp)]
    run(cmd, f"border break {seg.name}")
    tmp.replace(seg)


# ---------------- main ----------------
def main():
    import _polite; _polite.be_polite()
    ap = argparse.ArgumentParser()
    ap.add_argument("--spec", default="livingpage_m1.spec.json")
    ap.add_argument("--clips", action="store_true")
    ap.add_argument("--no-sfx", action="store_true")
    ap.add_argument("--lint", action="store_true", help="$0 plan check: crops/captions/reuse/DoD, no ffmpeg")
    ap.add_argument("--allow-slop", action="store_true",
                    help="override the fail-closed dash-slop caption block (user-approved only)")
    ap.add_argument("--only", default="", help="rebuild only these beat numbers (e.g. 3,17); others reuse existing segs")
    ap.add_argument("--pool", default="", help="visual pool dir (default: this episode's). Graduation seam: any piece can use the engine")
    ap.add_argument("--page", default="", help="WxH, e.g. 1080x1920 for a 9:16 short (default 1920x1080)")
    ap.add_argument("--no-ticks", action="store_true", help="drop the per-cut tick SFX (the 1900Hz snap); slams/whooshes/heartbeat stay")
    ap.add_argument("--skip-stills-gate", action="store_true", help="bypass the fail-closed stills human-gate (only when deliberately skipping review)")
    ap.add_argument("--skip-panel-variety", action="store_true", help="bypass the panel-variety/reuse-aspect gate (only for a deliberate, user-approved exception)")
    ap.add_argument("--skip-animated-gate", action="store_true", help="bypass the animated-pct gate (only for a deliberate, user-approved exception)")
    a = ap.parse_args()
    global POOL, WORK, DYN, PAGE
    if a.pool:
        POOL = Path(a.pool).resolve()
        WORK = POOL / "_livingpage_work"; WORK.mkdir(parents=True, exist_ok=True)
        DYN = POOL / "_dyncam_work"
        base.POOL, base.WORK, base.DYN = POOL, WORK, DYN
        base.WORK.mkdir(parents=True, exist_ok=True)
    if a.page:
        w, h = (int(x) for x in a.page.lower().split("x"))
        PAGE = (w, h)
        base.PAGE = PAGE
        ce.set_page(w, h)
        base.dc.OUT_W, base.dc.OUT_H = w, h  # dynamic_cam runtime seam (file untouched)
        if h > w:                            # portrait: caption furniture scaled to the shorts look
            cl.BASE_H = 1560                 # kinetic ~47px on a 1080-wide page (matches the locked short)
            cl.SHORTS_SAFE_BOT = 0.18        # keep captions out of the TikTok/Reels/Shorts bottom-UI band
    if not a.lint and not a.skip_stills_gate:      # #1 fail-closed STILLS HUMAN-GATE (grandfathered if no gate.json)
        import sys as _sys
        if str(ROOT) not in _sys.path:
            _sys.path.insert(0, str(ROOT))
        import stills_gate
        if stills_gate.check(POOL, stage="build") != 0:
            _sys.exit(3)
    spec = json.loads((POOL / a.spec).read_text(encoding="utf-8"))
    if not a.skip_panel_variety:      # #2 PANEL-VARIETY GATE (wired 2026-07-19 — was a
        import sys as _sys           # per-episode script nothing invoked; grandfathered
        if str(ROOT) not in _sys.path:   # (WARN+skip) for pools with no visual_tags.json)
            _sys.path.insert(0, str(ROOT))
        from pipeline import panel_variety as _pv
        if _pv.check(POOL, spec) != 0:
            _sys.exit(4)
    motion = spec.get("motion", "classic")
    assert motion in MOTION_PROFILES, f"unknown motion profile {motion!r} (pick: {sorted(MOTION_PROFILES)})"
    set_motion_profile(motion)
    print(f"[motion] profile = {motion}")
    for p, q in zip(spec["beats"], spec["beats"][1:]):
        assert p["t"][1] > p["t"][0] and abs(p["t"][1] - q["t"][0]) < 1e-6, f"beats not contiguous at {p['t']}"
    clips_dir = POOL / "clips"
    only = {int(x) for x in a.only.split(",") if x.strip()}
    segs, report, sfx_events = [], [], []
    crop_seen, reuse_all, fitwarn = {}, [], []
    TICK, WHOOSH = WORK / "_tick.wav", WORK / "_whoosh.wav"
    if not a.lint:
        if not TICK.exists():
            make_tick(TICK)
        if not WHOOSH.exists():
            make_whoosh(WHOOSH)

    def source(cdef):
        # Every-screen-animated rule (backported 2026-07-19 from Bronze Serpent's
        # 2026-07-17 fix -- this copy never got it): a real rendered clip always
        # wins when present -- `cam` is only a Ken-Burns fallback for slugs with
        # no clip. The old order checked `cam` FIRST, so any beat with a `cam`
        # hint set silently used Ken Burns even when a real animated clip existed.
        slug, cam = cdef["slug"], cdef.get("cam")
        live = clips_dir / f"{slug}.mp4"
        if a.clips and live.exists() and live.stat().st_size > 0:
            return live, "kling", None, cdef.get("motion", "pushin")
        if cam:
            return base.dyncam_clip(slug, cam) if not a.lint else live, "dyncam", cam, "pushin"
        return base.dyncam_clip(slug, "arc") if not a.lint else live, "dyncam", "arc", "pushin"

    reused_segs = []
    for i, b in enumerate(spec["beats"], 1):
        tpl = b["tpl"]
        f0, f1 = round(b["t"][0] * 30), round(b["t"][1] * 30)
        dur = round((f1 - f0) / 30.0, 6)
        t0 = b["t"][0]
        rects = ce.panels_for(tpl); mode = ce.template_mode(tpl)
        seg = WORK / f"seg_{i:02d}.mp4"
        panels_info, slams, moving = [], [], []
        skip_build = a.lint or (only and i not in only and seg.exists())
        if skip_build and not a.lint:
            reused_segs.append(i)

        if mode == "single":                        # full-bleed hero: the locked engine path
            cdef = b["clips"][0]
            clip, src, cam, motion = source(cdef)
            anc = pf.load_anchor(POOL, cdef["slug"]) or pf.default_anchor()
            sol = pf.solve_crop((rects[0][2], rects[0][3]), PAGE, anc, motion)
            z = round(sol["zoom"] * cdef.get("zoom", 1.0), 3)
            if not skip_build:
                ce.build_segment(seg, tpl, [{"kind": "clip", "path": str(clip), "motion": motion,
                                             "bias": list(sol["bias"]), "zoom": z}], dur, None, WORK)
            msc = cl.SRC_SCALE["kling" if src == "kling" else f"dyncam_{cam}"]
            panels_info.append(cl.panel_boxes(rects[0], PAGE, anc, sol["bias"], z, motion_scale=msc))
            moving.append(src)
            base._reuse_check(crop_seen, reuse_all, cdef["slug"], i,
                              (1.8, tuple(round(v, 1) for v in sol["bias"]), round(z, 1), motion))
        elif mode == "fracture":
            cdef = b["clips"][0]
            clip, src, cam, motion = source(cdef)
            anc = pf.load_anchor(POOL, cdef["slug"]) or pf.default_anchor()
            anchors = [tuple(x) for x in b["anchors"]]
            ats = b.get("panel_at", [t0] * len(rects))
            slides = b.get("panel_slide", ["left"] * len(rects))
            panels = []
            msc = cl.SRC_SCALE["kling" if src == "kling" else f"dyncam_{cam}"]
            for k, r in enumerate(rects):
                at_rel = max(0.0, round(ats[k % len(ats)] - t0, 3))
                panels.append({"path": str(clip), "motion": motion, "bias": (0.5, 0.5), "zoom": 1.0,
                               "rect": r, "at": at_rel, "slide": slides[k % len(slides)],
                               "flash": b.get("flash", True), "anchors": anchors[k % len(anchors)]})
                if at_rel > 0.01:
                    slams.append((at_rel, None))
                panels_info.append(cl.panel_boxes(r, PAGE, anc, anchors[k % len(anchors)][1:],
                                                  anchors[k % len(anchors)][0], motion_scale=msc))
            if not skip_build:
                compose_page(seg, dur, panels, WORK)
            moving.append(src)
            base._reuse_check(crop_seen, reuse_all, cdef["slug"], i, ("frac", tuple(anchors)))
        else:                                       # fill_each grids — the living page
            if len(b["clips"]) != len(rects):
                raise ValueError(f"beat {i} {tpl}: {len(b['clips'])} clips for {len(rects)} panels")
            panels = []
            for k, cdef in enumerate(b["clips"]):
                clip, src, cam, motion = source(cdef)
                anc = pf.load_anchor(POOL, cdef["slug"]) or pf.default_anchor()
                r = rects[k]
                sol = pf.solve_crop((r[2], r[3]), _dims(clip), anc, motion)
                z = round(sol["zoom"] * cdef.get("zoom", 1.0), 3)
                if not sol["fit"] and max(sol["lost"]) > 0.10:
                    fitwarn.append(f"  beat {i:>2} {tpl:10} panel {k} {cdef['slug']:24} {sol['reason']}")
                at_rel = max(0.0, round(cdef.get("at", t0) - t0, 3))
                panels.append({"path": str(clip), "motion": motion, "bias": sol["bias"],
                               "zoom": z, "rect": r, "at": at_rel,
                               "slide": cdef.get("slide", "left"), "flash": cdef.get("flash", True)})
                msc = cl.SRC_SCALE["kling" if src == "kling" else f"dyncam_{cam}"]
                panels_info.append(cl.panel_boxes(r, PAGE, anc, sol["bias"], z, motion_scale=msc))
                moving.append(src)
                if at_rel > 0.01:
                    slams.append((at_rel, cdef.get("sfx", "impact_low_boom") if cdef.get("flash", True) else None))
                base._reuse_check(crop_seen, reuse_all, cdef["slug"], i,
                                  (round(r[2] / r[3], 1), tuple(round(v, 1) for v in sol["bias"]),
                                   round(z, 1), motion))
            if not skip_build:
                compose_page(seg, dur, panels, WORK)

        bb = b.get("border_break")
        if b.get("ramp"):
            if slams or bb:
                print(f"  [!] beat {i}: ramp SKIPPED (mid-beat slams/border-break would desync)")
                b["ramp"] = False
            elif not skip_build:
                apply_ramp(seg, dur)
        if slams and not skip_build:
            apply_shake(seg, [s[0] for s in slams], dur)
        for at_rel, sname in slams:
            if sname:
                sfx_events.append((t0 + at_rel, sname, -8))
        if bb:
            at_rel = round(bb["at"] - t0, 3)
            if not skip_build:
                apply_border_break(seg, dur, at_rel)
                apply_shake(seg, [at_rel], dur)
            sfx_events.append((bb["at"], "veil_tearing", -10))
        tk = b.get("takeover")
        if tk and not skip_build:
            r = rects[tk["panel"]]
            apply_camera(seg, dur, r[0] + r[2] // 2, r[1] + r[3] // 2, tk.get("zoom", 1.3), tk["start"] - t0)
        if b.get("punch") and not skip_build:
            base.apply_punch(seg, dur)
        if b.get("whip"):
            if not skip_build:
                apply_whip(seg)
            sfx_events.append((max(0.0, t0 - 0.03), WHOOSH, -16, 0.4, 0.12))
        ins = b.get("inserts", [])
        if ins and not skip_build:
            apply_inserts(seg, dur, t0, ins)
        for e in ins:
            src = e["sfx"] if "sfx" in e else TICK
            sfx_events.append((e["at"], src, e.get("gain", -13), 0.25, 0.08))
        fxd = b.get("fx")
        if fxd and not skip_build:
            apply_fx(seg, dur, fxd, None if mode == "single" else rects)
        cp = b.get("cap")
        if (spec.get("cut_ticks") and not a.no_ticks and i > 1 and not bb
                and not (cp and cp["type"] == "redletter")):
            sfx_events.append((t0, TICK, spec.get("tick_gain", -19), 0.2, 0.06))
        for ev in b.get("sfx", []):
            sfx_events.append((ev[1], ev[0], ev[2] if len(ev) > 2 else -15))
        cap = b.get("cap"); csol = None
        if cap:
            csol = cl.solve(PAGE, panels_info, cap)
            if not skip_build:
                if csol["cls"] == "kinetic":
                    base.apply_kinetic(seg, cap, csol, dur, f"{i:02d}", delay=0.18 if b.get("punch") else 0.0)
                else:
                    base.apply_redletter(seg, cap, csol, dur, f"{i:02d}", at=b.get("cap_at", 0.35))
        if not skip_build:
            base.exact_frames(seg, dur)
        segs.append(seg)
        tag = f"T{csol['tier']}{'*FLAG' if csol and csol['flag'] else ''} {csol['style']}" if csol else "-"
        print(f"  [{i:2}] {tpl:10} {dur:5.2f}s {len(slams)} slam(s) {'BREAK ' if bb else ''}{'TAKEOVER ' if tk else ''}"
              f"{'PUNCH ' if b.get('punch') else ''}"
              f"{('FX(' + ('rays+' if fxd.get('rays') else '') + str(fxd.get('temp', '')) + 'K) ') if fxd else ''}"
              f"{'/'.join(moving):13} cap:{tag}", flush=True)
        report.append({"beat": i, "t": b["t"], "dur": dur, "tpl": tpl, "slams": len(slams),
                       "slugs": [c["slug"] for c in b["clips"]],
                       "sources": moving, "punch": bool(b.get("punch")),
                       "cap": None if not csol else {k: csol[k] for k in ("tier", "style", "flag")}})

    durs = [r["dur"] for r in report]
    held = sorted([round(d, 2) for d in durs if d > 6.0], reverse=True)
    flags = [r["beat"] for r in report if r["cap"] and r["cap"]["flag"]]
    tiers = [r["cap"]["tier"] for r in report if r["cap"]]
    # STANDARD §3b: machine-enforced richness + grammar (model-independent — a weaker
    # planner CANNOT silently ship the slideshow or slop text; these numbers block it)
    from collections import Counter
    cnt, fb, slop = Counter(), Counter(), []
    for idx, b in enumerate(spec["beats"], 1):
        for c in b["clips"]:
            cnt[c["slug"]] += 1
            if b["tpl"] == "full":
                fb[c["slug"]] += 1
        cp = b.get("cap")
        if cp and cp["type"] == "caption" and any(
                t in cp["text"] for t in (" - ", "...", "—", "–", "â€")):
            slop.append(idx)  # dash-joint "X - Y" template + ellipsis + mojibake = AI slop
        if cp and cp["type"] == "redletter" and "..." in cp["text"]:
            slop.append(idx)
    std = {"stills_over_2_uses": {s: n for s, n in cnt.items() if n > 2},
           "stills_fullbleed_twice": {s: n for s, n in fb.items() if n > 1},
           "fullbleed_beat_pct": round(100 * sum(1 for b in spec["beats"] if b["tpl"] == "full") / len(spec["beats"])),
           "slop_caption_beats": slop}
    dod = {"median_beat_s": round(statistics.median(durs), 2), "max_beat_s": round(max(durs), 2),
           "held_gt6s": held, "slams": sum(r["slams"] for r in report),
           "kling_or_punch_or_slam_pct": round(100 * sum(1 for r in report if "kling" in r["sources"]
                                               or r["punch"] or r["slams"]) / len(report)),
           "tier1_pct": round(100 * tiers.count(1) / max(1, len(tiers))),
           "reuse_violations": reuse_all, "tier3_or_flagged_beats": flags,
           "standard_3b": std,
           "ramps": sum(1 for b in spec["beats"] if b.get("ramp")),
           "whips": sum(1 for b in spec["beats"] if b.get("whip")),
           "flash_inserts": sum(len(b.get("inserts", [])) for b in spec["beats"]),
           "fx_beats": sum(1 for b in spec["beats"] if b.get("fx")),
           "cut_ticks": bool(spec.get("cut_ticks")),
           "beats": len(report)}
    if fitwarn:
        print(f"\n[fit-gate] {len(fitwarn)} over-cropped panel(s):\n" + "\n".join(fitwarn))
    if reused_segs and a.clips:       # red-team F2: reused segs keep the PIXELS they were
        print(f"[animated-gate] NOTE: --only reused {len(reused_segs)} existing seg(s) "
              f"{reused_segs} — the gate scores the CURRENT clips dir, not the pixels "
              f"inside reused segs (a seg rendered before its clip landed stays dyncam)")
    if a.lint:                        # DoD prints BEFORE the gate can exit — a failing
        print(f"\nLINT DoD: {json.dumps(dod, indent=1)}")   # lint must never swallow the
    if not a.skip_animated_gate:      # diagnostics needed to repair the piece (red-team
        import sys as _sys            # 2026-07-19). #3 ANIMATED-PCT GATE — the DoD number
        if str(ROOT) not in _sys.path:    # was advisory-only; --clips renders only,
            _sys.path.insert(0, str(ROOT))    # stills-only previews are all-dyncam by design
        from pipeline import animated_gate as _ag
        if _ag.check(report, clips=a.clips) != 0:
            _sys.exit(5)
    if a.lint:
        return

    # FAIL-CLOSED: dash-joint / ellipsis / mojibake captions are AI slop
    # (memory feedback-no-dash-caption-slop) — refuse to render them onto pixels.
    if slop and not a.allow_slop:
        print(f"\nSLOP BLOCK: beats {slop} carry dash-joint/ellipsis/mojibake captions. "
              f"Rewrite as plain sentences (or --allow-slop with user approval).")
        import sys as _s
        _s.exit(3)

    hb = spec.get("heartbeat")
    if hb and not a.no_sfx:
        dur_hb = round(hb["to"] - hb["from"], 3)
        hbw = WORK / "_heartbeat.wav"
        make_heartbeat(hbw, dur_hb, hb.get("bpm", 66))
        sfx_events.append((hb["from"], hbw, hb.get("gain", -9), dur_hb, 0.06))

    lst = WORK / "concat.txt"
    lst.write_text("".join(f"file '{s.as_posix()}'\n" for s in segs), encoding="utf-8")
    silent = WORK / "_silent.mp4"
    run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", str(lst),
         "-c:v", "libx264", "-crf", "18", "-preset", "veryfast", "-pix_fmt", "yuv420p", str(silent)], "concat")
    audio = (POOL / spec["audio"]).resolve()
    total = spec.get("total", spec["beats"][-1]["t"][1])
    muxed = WORK / "_muxed.mp4"
    run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(silent), "-i", str(audio),
         "-map", "0:v", "-map", "1:a", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k",
         "-t", f"{total:.2f}", str(muxed)], "mux")
    out = POOL / (Path(a.spec).stem + "_preview.mp4")
    if sfx_events and not a.no_sfx:
        add_sfx(muxed, sorted(sfx_events, key=lambda e: e[0]), out)
    else:
        out.write_bytes(muxed.read_bytes())

    (POOL / (Path(a.spec).stem + "_report.json")).write_text(
        json.dumps({"dod": dod, "clips_build": bool(a.clips), "beats": report},
                   indent=1), encoding="utf-8")
    print(f"\nDoD: {json.dumps(dod)}")
    print(f"\nDONE -> {out}\n  file:///{str(out).replace(chr(92), '/')}")


if __name__ == "__main__":
    main()
