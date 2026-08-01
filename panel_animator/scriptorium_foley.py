#!/usr/bin/env python
"""Scriptorium Foley -- the page is heard being made. Every lettering/paper
device in this show already knows, to the frame, exactly WHEN it acts (blue
line's 0.9s ink-arrival front, wash-creep's advance window, paperRip's tear,
Ink Stamp's 0.18s pop, Scribed Ink's letter-by-letter reveal) -- none of it
makes a sound. This module gives each device's already-known schedule a
matching DIEGETIC sound from the existing sound_library: a sound the page
itself would make being physically drawn/stamped/scratched, never music,
never a UI effect.

Brief: poc_living_sketchbook/_FABLE_ROUND3_SERIES_SKILLS.md section 2
"Scriptorium Foley". Storm episode source of truth for cue timing:
poc_living_sketchbook/storm/_s4_assemble.py (SHOTS/TRANSITIONS/OVERLAYS --
read here, not re-parsed; see storm_cue_list()'s own docstring for the exact
line-by-line provenance of every timestamp below).

$0, deterministic: every cue is an existing sound_library/clips/*.mp3 asset,
trimmed + gained + held-breath-enveloped with plain numpy (ffmpeg used only to
decode/encode PCM, never to invent audio). No ElevenLabs, no new generation.

THE ONE FLAGGED CONFLICT (do not resolve silently): a nib-scratch under
Scribed Ink's letter-by-letter KJV verse reveal (Storm's s08, Matthew 8:26)
touches the project's own locked "near-silence + one low tone under quoted
Scripture" rule (SKILL.md sec.7). storm_cue_list(nib_scratch_on=...) is a
TOGGLE for exactly this reason -- build BOTH variants, A/B by ear, the user
decides. Every other device below is untouched by that rule.

Usage (library):
    from scriptorium_foley import storm_cue_list, build_foley_bus
    from held_breath import energy_envelope
    words = json.load(open("_storm_alignment.json"))
    energy = energy_envelope(words, total_duration=63.0)
    bus = build_foley_bus(storm_cue_list(nib_scratch_on=True), energy, total_duration=63.0)
    # bus is an (n_samples, 2) float32 array -- write it, mix it in as ONE
    # MORE additive SFX input in the caller's own filter graph (never a
    # replacement for narration/music/existing SFX branches).

Usage (CLI -- builds the Storm proof-of-concept test clips + prints the
measurable verification numbers; this project's standing rule is verify by
LISTENING before anything locks -- this CLI only proves what can be proven
without ears: correct cue placement/duration, real attenuation vs. the raw
asset, and a real held-breath dip across a real narration silence):
    .venv\\Scripts\\python.exe panel_animator\\scriptorium_foley.py --build-storm-tests
    .venv\\Scripts\\python.exe panel_animator\\scriptorium_foley.py --verify
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from held_breath import energy_envelope  # noqa -- THE one silence envelope; reused, not reimplemented

sys.path.insert(0, str(ROOT))
from pipeline.score_mix import AFMT, SIDECHAIN  # noqa -- reuse the repo's own duck constants, don't reinvent

SOUND_CLIPS = ROOT / "sound_library" / "clips"
SR = 44100

STORM_DIR = ROOT / "poc_living_sketchbook" / "storm"
STORM_ALIGN = STORM_DIR / "_storm_alignment.json"
STORM_NARRATION = Path(
    r"C:\Users\sanjay\PycharmProjects\PythonProject1\jesus\narration\20 He Was Asleep in the Storm\v1\narration.mp3"
)
STORM_TOTAL = 63.0  # matches _s4_assemble.py's own TOTAL -- the padded final
                     # length, not just the narration's last word (per
                     # held-breath's own guardrail: pass the padded total).

# ---------------------------------------------------------------------------
# device -> sound_library asset map
#
# sound_library/ was built entirely for BIBLE-SCENE foley (crowds, animals,
# weapons, water, fire, market) -- it has ZERO stationery/paper-craft
# recordings (no nib scratch, no brush drag, no felt tap). Every mapping
# below is therefore an honest SUBSTITUTE picked for the closest available
# physical contour (attack/decay shape, texture, brightness), not a real hit.
# See .claude/skills/scriptorium-foley/SKILL.md for the gap this leaves.
#
# gain_db is the cue's BASE ambience level before the held-breath envelope
# multiplies it further -- every value is <= -14dB per the repo's own
# audio-layer-stack rule (SFX always ducked/low, never louder/unducked).
# ---------------------------------------------------------------------------
DEVICE_SOUND_MAP = {
    "blue_line_stroke": dict(
        slug="sea_waves_shore", trim=None, gain_db=-16.0,
        match="substitute",
        note=("wanted: one single wet brush-drag under the ink-arrival front. "
              "No brush/liquid-drag foley exists in the library; one wave-lap "
              "onset+decay (a natural, single, smooth swish) is the closest "
              "available attack/release contour to a brush stroke."),
    ),
    "wash_creep_wash": dict(
        slug="river_well_water", trim=None, gain_db=-18.0,
        match="substitute",
        note=("wanted: a faint continuous water-wash under the advancing "
              "storm wash. The library's flowing spring/stream is the "
              "closest SUSTAINED liquid ambience (vs. sea_waves_shore's "
              "stop-start lapping, reserved for the blue-line one-shot)."),
    ),
    "nib_scratch": dict(
        slug="footsteps_dirt_approach", trim=None, gain_db=-22.0,
        pre_filt="highpass=f=500,treble=g=6:f=3000",
        match="substitute-weak (real gap -- see SKILL.md)",
        note=("wanted: a dry quill/nib scratch under Scribed Ink's letter-by-"
              "letter reveal. NO textural scratch asset exists in this "
              "library at all -- it is 100% scene-foley, nothing stationery. "
              "Dry gravel footsteps, high-passed to strip their low-end thud "
              "and brighten the grain, is the least-wrong stand-in available; "
              "this is a real gap, not a good match, flagged honestly."),
    ),
    "felt_press_tap": dict(
        slug="waterpot_drop_run", trim=(0.0, 0.35), gain_db=-14.0,
        match="substitute",
        note=("wanted: a felt stamp press-tap under Ink Stamp's 0.18s pop. "
              "The jar-set-down 'thunk' (trimmed to just its onset, before "
              "the running footsteps in the rest of that source) is the "
              "closest single soft-contact percussive one-shot in the "
              "library that isn't metal-on-metal (nail_strike_single) or a "
              "multi-step walk."),
    ),
    "paper_tear": dict(
        slug="bread_tearing", trim=(0.0, 0.6), gain_db=-14.0,
        match="substitute",
        note=("wanted: an actual paper tear under the paperRip transition. "
              "bread_tearing's crisp, brittle single-tear transient is "
              "closer in texture (paper is crisp, not cloth) than "
              "veil_tearing's longer, heavier fabric rip -- veil_tearing "
              "stays reserved for a real veil moment elsewhere. Reused "
              "unchanged (v6) for the s06->s07 Torn-Out Page rip -- same "
              "physical action, a page tearing, just a different boundary."),
    ),
    # ---- v6 additions (_STORM_V6_SCORE.md) -- same substitute-only honesty
    # as the block above; no new assets, just new device keys onto the same
    # library. ----
    "keeper_scratch": dict(
        slug="footsteps_dirt_approach", trim=None, gain_db=-26.0,
        pre_filt="highpass=f=500,treble=g=6:f=3000",
        match="substitute-weak (same real gap as nib_scratch, see SKILL.md)",
        note=("wanted: the Keeper's OWN hand scratching in the margin (s01 "
              "Field Header, s03 Bleeding Word entry, s08 keeper stub) -- "
              "not the Word's formal Scribed Ink. Same underlying substitute "
              "as nib_scratch (no stationery foley exists in this library at "
              "all), reused at the score's explicit '-4dB below Scribed Ink "
              "level' (nib_scratch's own -22dB base -> -26dB here) so the "
              "human hand always reads quieter than the Word's register."),
    ),
    "ink_drop": dict(
        slug="waterpot_drop_run", trim=(0.0, 0.30), gain_db=-14.0,
        match="substitute",
        note=("wanted: a single ink drop hitting the page (s03 Bleeding "
              "Word) and the inkwell re-dip splash (s05 Inkwell Runs Dry's "
              "blot). No ink/liquid-on-paper foley exists; the water-pot "
              "drop's own onset splash (a different trim of the same asset "
              "already reused for felt_press_tap's stamp thunk) is the "
              "closest single wet-impact transient in the library."),
    ),
}


@dataclass
class Cue:
    device: str      # key into DEVICE_SOUND_MAP
    start: float     # GLOBAL seconds, same timeline as the episode's own assembler
    duration: float
    label: str = ""


def storm_cue_list(nib_scratch_on: bool = True, v6_devices: bool = False) -> list[Cue]:
    """The Storm episode's (Matthew 8:23-27) cue list, read directly off
    poc_living_sketchbook/storm/_s4_assemble.py's OWN schedule constants --
    no separate alignment/parsing needed, the timing already exists there:

      - blue_line ink-arrival front: apply_paper_devices(), "s01_waves"
        branch, `if t < 0.9`.
      - wash_creep advance windows: SHOTS[0] s01_waves (0.00-2.10) and
        SHOTS[3] s04_asleep (6.67-10.84) -- both run `wash_creep.apply_wash_creep`.
      - paperRip transition: TRANSITIONS = {23.55: "paperRip"}, applied over
        a 0.4s cross-fade (`if tt <= t < tt + 0.4`).
      - Scribed Ink verse card: OVERLAYS (23.75, 27.10, verse_card, ...) --
        the ONE flagged conflict cue (SKILL.md sec.7 near-silence rule).
        TOGGLED by nib_scratch_on; every other cue here is unaffected by
        that rule.
      - Ink Stamp "EXACTLY.": OVERLAYS (35.05, 36.50, exactly_stamp, ...),
        0.18s pop-in ease -- the felt press-tap fires right on the pop.

    A generic pipeline would derive this list from each device's own
    scheduling call instead of a hardcoded literal (see SKILL.md "wiring a
    new episode" section) -- this function is the Storm-specific proof, not
    the universal extractor.

    v6_devices=True (_STORM_V6_SCORE.md, poc_living_sketchbook/storm/
    _s6_assemble.py) layers the full-coverage device pass's own cue windows
    on top, read off _s6_assemble.py's own as-built timing constants (see
    that file's header comment for the alignment provenance of each number):

      - s01 Field Header keeper-hand write-on (1.50-3.30s).
      - s03 Bleeding Word entry write-on (4.35-5.00s) + the drop-hit itself
        (5.032s, bound to "screaming" ending -- the fear-beat word).
      - s05 Inkwell Runs Dry: dry-scratch under the starved tail
        (13.346-14.146s) + the re-dip/blot splash (14.146-14.546s).
      - s06->s07 Torn-Out Page rip (21.60-21.95s, the rip-away phase only --
        the grab/lift itself is silent).
      - s08 keeper stub scratch, STOPS DEAD at the Word's instant whole
        arrival (22.756-23.545s) -- no cue at all under the verse card
        itself, near-silence per SKILL.md sec.7 stands unchanged.

    v6_devices=True SUPERSEDES nib_scratch_on: v6 replaces s08's old
    letter-by-letter Scribed Ink reveal with an instant complete arrival
    (LAW 1), so the old nib-scratch-under-reveal cue no longer has anything
    to scratch under and is dropped, not toggled.
    """
    cues = [
        Cue("blue_line_stroke", 0.00, 0.90, "s01 cold-open ink-arrival ident stroke"),
        Cue("wash_creep_wash", 0.00, 2.10, "s01 wash-creep advance"),
        Cue("wash_creep_wash", 6.67, 4.17, "s04 wash-creep advance"),
        Cue("paper_tear", 23.55, 0.40, "paperRip transition into s08 verse"),
        Cue("felt_press_tap", 35.05, 0.22, "s11 EXACTLY. Ink Stamp pop-in"),
    ]
    if v6_devices:
        cues += [
            Cue("keeper_scratch", 1.50, 1.80, "v6 s01 Field Header write-on"),
            Cue("keeper_scratch", 4.35, 0.65, "v6 s03 Bleeding Word entry write-on"),
            Cue("ink_drop", 5.032, 0.30, "v6 s03 Bleeding Word drop-hit"),
            Cue("nib_scratch", 13.346, 0.80, "v6 s05 Inkwell Runs Dry -- starve-tail dry scratch"),
            Cue("ink_drop", 14.146, 0.40, "v6 s05 Inkwell Runs Dry -- re-dip blot"),
            Cue("paper_tear", 21.60, 0.35, "v6 s06->s07 Torn-Out Page rip-away"),
            Cue("keeper_scratch", 22.756, 0.789, "v6 s08 keeper stub -- stops dead at the Word's arrival"),
        ]
    elif nib_scratch_on:
        cues.append(Cue("nib_scratch", 23.75, 27.10 - 23.75,
                         "s08 Scribed Ink verse reveal (TOGGLE, see SKILL.md sec.7 conflict)"))
    return cues


# ---------------------------------------------------------------------------
# PCM decode/encode via ffmpeg (no new deps -- soundfile/pydub not installed
# in this venv; the repo's own convention everywhere else is subprocess+ffmpeg)
# ---------------------------------------------------------------------------

def _ffmpeg_read_pcm(src: Path, trim: tuple[float, float] | None = None,
                      pre_filt: str | None = None, sr: int = SR) -> np.ndarray:
    """Decode an existing sound_library asset to float32 stereo. Returns
    (n_samples, 2). trim=(t0,t1) grabs only that slice of the SOURCE file
    (used when only part of a multi-event asset is wanted, e.g. just the
    jar-thunk onset before waterpot_drop_run's running footsteps)."""
    parts = []
    if pre_filt:
        parts.append(pre_filt)
    if trim:
        parts.append(f"atrim=start={trim[0]}:end={trim[1]}")
        parts.append("asetpts=PTS-STARTPTS")
    parts.append(f"aformat=sample_fmts=fltp:channel_layouts=stereo:sample_rates={sr}")
    af = ",".join(parts)
    cmd = ["ffmpeg", "-y", "-v", "error", "-i", str(src), "-af", af,
           "-f", "f32le", "-ac", "2", "-ar", str(sr), "pipe:1"]
    r = subprocess.run(cmd, capture_output=True, check=True)
    return np.frombuffer(r.stdout, dtype=np.float32).reshape(-1, 2).copy()


def _write_raw_f32(path: Path, arr: np.ndarray) -> None:
    np.asarray(arr, dtype=np.float32).tofile(path)


def rms_dbfs(x: np.ndarray) -> float:
    r = float(np.sqrt(np.mean(np.square(x)))) if x.size else 0.0
    return 20 * np.log10(r) if r > 1e-12 else -120.0


def peak_dbfs(x: np.ndarray) -> float:
    p = float(np.max(np.abs(x))) if x.size else 0.0
    return 20 * np.log10(p) if p > 1e-12 else -120.0


# ---------------------------------------------------------------------------
# cue rendering: trim + gain + held-breath envelope
# ---------------------------------------------------------------------------

def render_cue_samples(cue: Cue, energy) -> np.ndarray:
    """One cue's finished PCM segment: source asset -> gain (ambience-level,
    <= -14dB) -> held-breath energy(t) multiplier sampled at each output
    sample's GLOBAL timestamp (cue.start + local_t) -- the SAME energy(t)
    every visual paper device already multiplies its own amplitude by, so
    the desk goes quiet exactly where the narrator does."""
    spec = DEVICE_SOUND_MAP[cue.device]
    src = SOUND_CLIPS / f"{spec['slug']}.mp3"
    if not src.exists():
        raise SystemExit(f"missing sound_library asset: {src}")
    raw = _ffmpeg_read_pcm(src, trim=spec.get("trim"), pre_filt=spec.get("pre_filt"))

    n_needed = int(round(cue.duration * SR))
    if len(raw) >= n_needed:
        seg = raw[:n_needed].copy()
    else:
        reps = int(np.ceil(n_needed / max(1, len(raw))))
        seg = np.tile(raw, (reps, 1))[:n_needed].copy()

    gain_lin = 10 ** (spec["gain_db"] / 20.0)
    seg *= gain_lin

    # 5ms in/out fade so a cue's own trim boundary never clicks
    fade_n = max(1, min(int(0.005 * SR), len(seg) // 4))
    ramp = np.linspace(0.0, 1.0, fade_n, dtype=np.float32)
    seg[:fade_n] *= ramp[:, None]
    seg[-fade_n:] *= ramp[::-1][:, None]

    t_global = cue.start + np.arange(len(seg)) / SR
    env = np.fromiter((energy(t) for t in t_global), dtype=np.float32, count=len(t_global))
    seg *= env[:, None]
    return seg


def build_foley_bus(cues: list[Cue], energy, total_duration: float) -> np.ndarray:
    """Sum every cue into one additive SFX bus, full episode length. This IS
    the "new layer" -- it is handed to the caller's existing mix as ONE MORE
    input to amix, never as a replacement for narration/music/existing SFX."""
    n_total = int(round(total_duration * SR))
    bus = np.zeros((n_total, 2), dtype=np.float32)
    for cue in cues:
        seg = render_cue_samples(cue, energy)
        i0 = int(round(cue.start * SR))
        i1 = min(i0 + len(seg), n_total)
        if i0 >= n_total or i1 <= i0:
            continue
        bus[i0:i1] += seg[: i1 - i0]
    return bus


# ---------------------------------------------------------------------------
# standalone test-clip rendering (proof only -- never touches the shipped mp4)
# ---------------------------------------------------------------------------

def render_test_clip(name: str, still: Path, t0: float, t1: float, bus: np.ndarray,
                      narration_path: Path, outdir: Path) -> Path:
    """Still (looped) + [real narration slice] + [this cue bus's slice],
    narration-sidechain-ducked exactly like every other SFX layer in this
    repo (pipeline.score_mix's own SIDECHAIN constant). Additive-only: a
    brand new standalone file, the shipped STORM_living_sketchbook.mp4 is
    never opened for writing."""
    outdir.mkdir(parents=True, exist_ok=True)
    dur = t1 - t0
    i0, i1 = int(round(t0 * SR)), int(round(t1 * SR))
    local_bus = bus[i0:i1]
    raw_path = outdir / f"_{name}_foley.raw"
    _write_raw_f32(raw_path, local_bus)

    out = outdir / f"{name}.mp4"
    filt = (
        f"[1:a]{AFMT},asplit=2[nmain][nkey];"
        f"[2:a]{AFMT}[foley];"
        f"[foley][nkey]sidechaincompress={SIDECHAIN}[foleyd];"
        f"[nmain][foleyd]amix=inputs=2:normalize=0,alimiter=limit=0.97,aresample=44100[mix]"
    )
    cmd = [
        "ffmpeg", "-y", "-v", "error",
        "-loop", "1", "-t", f"{dur:.3f}", "-i", str(still),
        "-ss", f"{t0:.3f}", "-t", f"{dur:.3f}", "-i", str(narration_path),
        "-f", "f32le", "-ar", str(SR), "-ac", "2", "-i", str(raw_path),
        "-filter_complex", filt,
        "-vf", "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920",
        "-map", "0:v", "-map", "[mix]",
        "-c:v", "libx264", "-crf", "20", "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-b:a", "192k", "-t", f"{dur:.3f}", "-shortest",
        str(out),
    ]
    subprocess.run(cmd, check=True)
    raw_path.unlink(missing_ok=True)
    return out


def build_storm_tests(outdir: Path | None = None) -> list[Path]:
    outdir = outdir or (STORM_DIR / "_qc2")
    words = json.load(open(STORM_ALIGN, encoding="utf-8"))
    energy = energy_envelope(words, total_duration=STORM_TOTAL)

    bus_on = build_foley_bus(storm_cue_list(nib_scratch_on=True), energy, STORM_TOTAL)
    bus_off = build_foley_bus(storm_cue_list(nib_scratch_on=False), energy, STORM_TOTAL)

    stills = STORM_DIR / "stills"
    made = []
    made.append(render_test_clip("foley_test_s01_coldopen", stills / "s01_waves.png",
                                  0.0, 2.6, bus_on, STORM_NARRATION, outdir))
    made.append(render_test_clip("foley_test_s04_washcreep", stills / "s04_asleep.png",
                                  6.67, 10.9, bus_on, STORM_NARRATION, outdir))
    made.append(render_test_clip("foley_test_s08_verse_SCRATCH_ON", stills / "s08_verse.png",
                                  23.55, 27.9, bus_on, STORM_NARRATION, outdir))
    made.append(render_test_clip("foley_test_s08_verse_SCRATCH_OFF", stills / "s08_verse.png",
                                  23.55, 27.9, bus_off, STORM_NARRATION, outdir))
    made.append(render_test_clip("foley_test_s11_exactly", stills / "s11_exactly.png",
                                  34.5, 37.5, bus_on, STORM_NARRATION, outdir))
    return made


# ---------------------------------------------------------------------------
# measurable verification -- NOT an ear-check. Confirms placement/duration,
# real attenuation vs. the raw asset, and a real held-breath dip across a
# real narration silence. A human must still listen before this locks.
# ---------------------------------------------------------------------------

def verify() -> None:
    words = json.load(open(STORM_ALIGN, encoding="utf-8"))
    energy = energy_envelope(words, total_duration=STORM_TOTAL)
    cues = storm_cue_list(nib_scratch_on=True)
    bus = build_foley_bus(cues, energy, STORM_TOTAL)

    print("=== A: cue placement + duration (bus energy inside vs. just outside each window) ===")
    for cue in cues:
        i0, i1 = int(cue.start * SR), int((cue.start + cue.duration) * SR)
        inside = bus[i0:i1]
        pre = bus[max(0, i0 - int(0.15 * SR)):i0]
        post = bus[i1:i1 + int(0.15 * SR)]
        print(f"  {cue.device:<16} [{cue.start:6.2f}-{cue.start + cue.duration:6.2f}] "
              f"inside RMS={rms_dbfs(inside):7.1f}dBFS  "
              f"pre-window RMS={rms_dbfs(pre):7.1f}dBFS  post-window RMS={rms_dbfs(post):7.1f}dBFS")

    print("\n=== B: attenuation vs. the raw (undamped/ungained) asset ===")
    for cue in cues:
        spec = DEVICE_SOUND_MAP[cue.device]
        raw = _ffmpeg_read_pcm(SOUND_CLIPS / f"{spec['slug']}.mp3", trim=spec.get("trim"))
        seg = render_cue_samples(cue, energy)
        print(f"  {cue.device:<16} raw asset RMS={rms_dbfs(raw):7.1f}dBFS peak={peak_dbfs(raw):6.1f}dBFS  "
              f"-> cue RMS={rms_dbfs(seg):7.1f}dBFS peak={peak_dbfs(seg):6.1f}dBFS  "
              f"(delta {rms_dbfs(seg) - rms_dbfs(raw):+6.1f}dB, base gain spec'd {spec['gain_db']:+.1f}dB)")

    print("\n=== C: held-breath dip across a REAL narration silence gap ===")
    # s08 nib-scratch cue (23.75-27.10) contains the real gap 24.91-25.57
    # ("fearful," -> "O", from _storm_alignment.json / held_breath --demo).
    nib = next(c for c in cues if c.device == "nib_scratch")
    seg = render_cue_samples(nib, energy)
    t0 = nib.start
    def sub(a, b):
        return seg[int((a - t0) * SR):int((b - t0) * SR)]
    speech_win = sub(23.85, 24.45)      # inside the cue, no gap nearby -> energy ~1.0
    gap_win = sub(25.05, 25.40)         # inside the real 24.91-25.57 gap -> energy -> floor (0.25)
    print(f"  nib_scratch   speech-region RMS={rms_dbfs(speech_win):7.1f}dBFS   "
          f"gap-region RMS={rms_dbfs(gap_win):7.1f}dBFS   "
          f"measured drop={rms_dbfs(speech_win) - rms_dbfs(gap_win):5.1f}dB")
    print(f"  energy(t) itself: energy(24.10)={energy(24.10):.3f} (speech)  "
          f"energy(25.20)={energy(25.20):.3f} (gap floor, expect 0.25)  "
          f"predicted dB drop={20*np.log10(energy(24.10)/energy(25.20)):.1f}dB")

    # s04 wash-creep cue (6.67-10.84) contains two real gaps: 7.34-8.70, 9.21-10.84.
    wash = next(c for c in cues if c.device == "wash_creep_wash" and abs(c.start - 6.67) < 1e-6)
    seg2 = render_cue_samples(wash, energy)
    t0 = wash.start
    def sub2(a, b):
        return seg2[int((a - t0) * SR):int((b - t0) * SR)]
    speech_win2 = sub2(6.70, 7.10)       # right at the cue's start, energy ~1.0
    gap_win2 = sub2(7.90, 8.30)          # inside the real 7.34-8.70 gap
    print(f"\n  wash_creep_wash(s04) speech-region RMS={rms_dbfs(speech_win2):7.1f}dBFS   "
          f"gap-region RMS={rms_dbfs(gap_win2):7.1f}dBFS   "
          f"measured drop={rms_dbfs(speech_win2) - rms_dbfs(gap_win2):5.1f}dB")
    print(f"  energy(t) itself: energy(6.90)={energy(6.90):.3f} (speech)  "
          f"energy(8.10)={energy(8.10):.3f} (gap floor, expect 0.25)")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--build-storm-tests", action="store_true",
                     help="render the Storm proof-of-concept test clips into _qc2/")
    ap.add_argument("--verify", action="store_true",
                     help="print the measurable (non-ear) verification numbers")
    ap.add_argument("--outdir", default=None)
    a = ap.parse_args()

    if a.build_storm_tests:
        outdir = Path(a.outdir) if a.outdir else None
        paths = build_storm_tests(outdir)
        print("[ok] built:")
        for p in paths:
            print(f"  {p}")
    if a.verify:
        verify()
    if not a.build_storm_tests and not a.verify:
        ap.print_help()
