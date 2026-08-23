"""$0 validation (no HF render spend) for swirls_assemble.py + swirls_verify.py
against BOTH real shipped episodes.

1. Express both episodes as EpisodeManifests, content sliced from the real
   assemble_book_v2.py / assemble_ashes.py modules (imported, not retyped).
2. plan_units() parity: computed slots must match the real shipped scripts'
   own numbers.
3. sw_f1_freeze_budget() must apply ONLY to freeze units -- proves episode
   1's own boomerang units (F02/F04/F07/back) are exempted, not spuriously
   failed (the red-team catch, 2026-08-23).
4. Command/filter-string diff for episode 1: construct the EXACT ffmpeg
   filter_complex + output args swirls_assemble would use, and diff against
   assemble_book_v2.py's own construction -- byte-identical, proving a
   refactor bug that preserves the arithmetic but changes the constructed
   command would NOT be silently missed by arithmetic-only parity.
5. A REAL re-assemble of BOTH episodes from their existing (already-rendered,
   $0 to re-encode) inputs, into an ISOLATED SCRATCH directory -- never the
   manifest's live production `out=` path. FIXED 2026-08-23 (independent-
   review CRITICAL catch, claude): the original version pointed straight at
   `assemble_ashes.py`'s real output path and silently overwrote the actual
   shipped `THE_ASHES_BOOK_final.mp4` with a reproduction of the (currently
   still-defective) inputs on every validator run. Confirms SW-A1/A2/A3 for
   both episodes -- episode 1's real re-assemble is what actually PROVES the
   SW-A2 mode-aware fix (codex's catch: front/F05/F06 have native > slot and
   are never trimmed by design; a naive `held == slot` check would have
   spuriously failed the north star's own approved units).

Run:
  .venv\\Scripts\\python.exe poc_living_water_ink_style_test\\_validate_swirls_assemble.py
"""
from __future__ import annotations

import dataclasses
import shutil
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE / "swirls_pilot_01_jacobs_ladder"))
sys.path.insert(0, str(HERE / "swirls_episode_02_ashes_that_made_clean"))

import swirls_assemble as sa  # noqa: E402
import swirls_verify as sv  # noqa: E402
from swirls_assemble import DuckProfile, EpisodeManifest, ScoreVariant, Unit  # noqa: E402
import assemble_book_v2 as ab2  # noqa: E402
import assemble_ashes as aa  # noqa: E402
from pipeline import score_mix  # noqa: E402

FAILS = []


def check(label: str, cond: bool, detail: str = "") -> None:
    status = "PASS" if cond else "FAIL"
    print(f"[{status}] {label}" + (f" -- {detail}" if detail and not cond else ""))
    if not cond:
        FAILS.append(label)


# ============================================================ MANIFESTS ===
manifest_ep1 = EpisodeManifest(
    episode_dir=ab2.HERE, narration=ab2.NARRATION,
    units=[Unit(tag, src, words, mode) for tag, src, words, mode in ab2.UNITS],
    scores={"default": ScoreVariant(
        score=ab2.SCORE,
        duck=DuckProfile(ab2.MUSIC_GAIN_DB, ab2.DUCK_THRESHOLD, ab2.DUCK_RATIO, ab2.DUCK_RELEASE),
        out=ab2.OUT)},
    panel_style="ink_wash", outro_hold=ab2.OUTRO_HOLD, w=ab2.W, h=ab2.H, fps=ab2.FPS,
)

manifest_ep2 = EpisodeManifest(
    episode_dir=aa.HERE, narration=aa.NARRATION,
    units=[Unit(tag, src, words, mode) for tag, src, words, mode in aa.UNITS],
    scores={name: ScoreVariant(
        score=v["score"],
        duck=DuckProfile(v["gain"], v["threshold"], v["ratio"], v["release"]),
        out=v["out"]) for name, v in aa.SCORE_VARIANTS.items()},
    panel_style="ink_wash",  # episode 2's CURRENT shipped state -- defective, rebuild pending
    outro_hold=aa.OUTRO_HOLD, w=aa.W, h=aa.H, fps=aa.FPS,
)

# real per-page model tiers, sliced from the real PAGES dicts (not retyped)
import render_jacobs_ladder as jl  # noqa: E402
import render_ashes as ra  # noqa: E402

model_tier_ep1 = {pid: p.model_tier for pid, p in jl.PAGES.items()}
model_tier_ep1["front"] = model_tier_ep1["back"] = "veo3_1_lite"  # covers, locked
model_tier_ep2 = {pid: p.model_tier for pid, p in ra.PAGES.items()}
model_tier_ep2["front"] = model_tier_ep2["back"] = "veo3_1_lite"

# ==================================================== 2. PLAN PARITY ===
print("\n=== plan_units() parity ===")
plan1 = sa.plan_units(manifest_ep1)
plan2 = sa.plan_units(manifest_ep2)

p1_by_tag = {p["tag"]: p for p in plan1}
p2_by_tag = {p["tag"]: p for p in plan2}

# known-good numbers, independently recomputed by the red-team from the real
# files (2026-08-23) -- pin them so a future regression is caught
check("ep1 F03 static ratio ~32.5%",
      abs((max(p1_by_tag["f03"]["slot"] - p1_by_tag["f03"]["native"], 0) / p1_by_tag["f03"]["slot"]) - 0.325) < 0.02,
      f"got {p1_by_tag['f03']}")
check("ep2 F01 static ratio ~55.6%",
      abs((max(p2_by_tag["f01"]["slot"] - p2_by_tag["f01"]["native"], 0) / p2_by_tag["f01"]["slot"]) - 0.556) < 0.02,
      f"got {p2_by_tag['f01']}")
check("ep2 F04 static ratio ~50.3%",
      abs((max(p2_by_tag["f04"]["slot"] - p2_by_tag["f04"]["native"], 0) / p2_by_tag["f04"]["slot"]) - 0.503) < 0.02,
      f"got {p2_by_tag['f04']}")

# =========================================== 3. FREEZE-ONLY GATE SCOPE ===
print("\n=== SW-F1 freeze-only scope (the red-team's required fix) ===")
gates1 = sv.sw_f1_freeze_budget(plan1, model_tier_ep1)
gates2 = sv.sw_f1_freeze_budget(plan2, model_tier_ep2)
gates1_tags = {g.gate for g in gates1}
gates2_tags = {g.gate for g in gates2}

# episode 1 has 4 freeze units (front/f03/f05/f06); front/f05/f06 trivially PASS at
# 0% ratio because their native clip duration already exceeds the slot -- only f03's
# slot exceeds its native duration, landing right at the top of the accepted band
# (CONDITIONAL, not a clean PASS -- 32.5% sits between the 25% warn line and the 35%
# fail line, the exact boundary the fail line was set just above).
check("ep1: exactly its 4 freeze units got a gate result (boomerang units exempted)",
      gates1_tags == {"SW-F1[front]", "SW-F1[f03]", "SW-F1[f05]", "SW-F1[f06]"},
      f"got {sorted(gates1_tags)}")
by_tag1 = {g.gate: g for g in gates1}
check("ep1: front/f05/f06 PASS (native already exceeds slot, 0% static)",
      all(by_tag1[f"SW-F1[{t}]"].verdict == "PASS" for t in ("front", "f05", "f06")),
      str([by_tag1[f"SW-F1[{t}]"] for t in ("front", "f05", "f06")]))
check("ep1: f03 is CONDITIONAL at ~32.5% (not FAIL, not a clean PASS either)",
      by_tag1["SW-F1[f03]"].verdict == "CONDITIONAL", by_tag1["SW-F1[f03]"].evidence)
check("ep2: F01 and F04 (its two freeze units) both got gate results",
      gates2_tags == {"SW-F1[f01]", "SW-F1[f04]"}, f"got {sorted(gates2_tags)}")
f01_g = next(g for g in gates2 if g.gate == "SW-F1[f01]")
f04_g = next(g for g in gates2 if g.gate == "SW-F1[f04]")
check("ep2: F01 gate is FAIL (the known defect)", f01_g.verdict == "FAIL", f01_g.evidence)
check("ep2: F04 gate is FAIL (the known defect)", f04_g.verdict == "FAIL", f04_g.evidence)
print(f"  F01 fix suggestion: {f01_g.fix}")
print(f"  F04 fix suggestion: {f04_g.fix}")

# ===================================== 4. COMMAND/FILTER STRING DIFF (EP1) ===
print("\n=== ffmpeg filter/command string diff, episode 1 (no re-encode) ===")
narration_len_ep1 = sa.dur(ab2.NARRATION)
total_ep1 = narration_len_ep1 + ab2.OUTRO_HOLD

# what assemble_book_v2.py's own main() would build:
original_filt = (
    f"[1:a]{ab2.AFMT},volume={ab2.MUSIC_GAIN_DB}dB[mus];"
    f"[0:a]{ab2.AFMT},apad=whole_dur={total_ep1},asplit=2[main][key];"
    f"[mus][key]sidechaincompress=threshold={ab2.DUCK_THRESHOLD}:ratio={ab2.DUCK_RATIO}:"
    f"attack=20:release={ab2.DUCK_RELEASE}[musd];"
    f"[main][musd]amix=inputs=2:normalize=0,alimiter=limit=0.97,aresample=44100[mix];"
    f"[0:v]tpad=stop_mode=clone:stop_duration={ab2.OUTRO_HOLD}[vout]"
)
original_out_args = ["-map", "[vout]", "-map", "[mix]",
                      "-c:v", "libx264", "-crf", "18", "-preset", "medium", "-pix_fmt", "yuv420p",
                      "-movflags", "+faststart", "-c:a", "aac", "-b:a", "192k",
                      "-t", f"{total_ep1:.3f}", str(ab2.OUT)]

# what swirls_assemble.assemble() would build for the same manifest+variant:
variant = manifest_ep1.scores["default"]
generated_music_chain = f"[1:a]{score_mix.AFMT},volume={variant.duck.gain_db}dB[mus];"
generated_tail = score_mix.mix_tail(total_ep1, manifest_ep1.outro_hold, fmt_narration=True,
                                     sidechain=variant.duck.sidechain())
generated_filt = generated_music_chain + generated_tail
generated_out_args = score_mix.output_args(variant.out, preset="medium", total=total_ep1)

check("filter_complex string is byte-identical", generated_filt == original_filt,
      f"\n  generated: {generated_filt}\n  original:  {original_filt}")
check("output args list is identical", generated_out_args == original_out_args,
      f"\n  generated: {generated_out_args}\n  original:  {original_out_args}")

# ============================ 5. REAL RE-ASSEMBLE, BOTH EPISODES, SCRATCH ===
# Never write to the manifest's real `out=` path -- redirect every score
# variant's output into an isolated scratch dir before calling assemble().
SCRATCH = HERE / "_validate_scratch"
if SCRATCH.exists():
    shutil.rmtree(SCRATCH)
SCRATCH.mkdir(parents=True)


def _scratchify(manifest: EpisodeManifest, label: str) -> EpisodeManifest:
    scratch_scores = {
        name: dataclasses.replace(variant, out=SCRATCH / f"{label}_{name}.mp4")
        for name, variant in manifest.scores.items()
    }
    return dataclasses.replace(manifest, scores=scratch_scores)


print("\n=== real re-assemble, episode 1 (existing inputs, scratch output, no HF spend) ===")
result1 = sa.assemble(_scratchify(manifest_ep1, "ep1"), "default", work_dirname="_assembly_validate")
check("episode 1 re-assembles to a plausible duration (>0s, matches its own narration+hold)",
      abs(result1["final_duration"] - (result1["narration_len"] + manifest_ep1.outro_hold)) < 0.5,
      f"got {result1['final_duration']:.2f}s")

a1_ep1 = sv.sw_a1_duration_parity(result1["out"])
check("ep1 SW-A1 duration parity", a1_ep1.verdict == "PASS", a1_ep1.evidence)

a2_ep1 = sv.sw_a2_unit_duration(result1["units"])
check("ep1 SW-A2 every unit matches its mode-aware expected duration "
      "(THE empirical proof the mode-aware fix is correct, not just arithmetic)",
      all(g.verdict == "PASS" for g in a2_ep1),
      "; ".join(g.evidence for g in a2_ep1 if g.verdict != "PASS"))
for g in a2_ep1:
    print(f"    {g.gate}: {g.evidence}")

a3_ep1 = sv.sw_a3_total_duration(result1["final_duration"], result1["narration_len"], manifest_ep1.outro_hold)
check("ep1 SW-A3 total duration matches narration+hold", a3_ep1.verdict == "PASS", a3_ep1.evidence)

print("\n=== real re-assemble, episode 2 (existing inputs, scratch output, no HF spend) ===")
result2 = sa.assemble(_scratchify(manifest_ep2, "ep2"), "original", work_dirname="_assembly_validate")
check("episode 2 re-assembles to ~62.00s", abs(result2["final_duration"] - 62.00) < 0.5,
      f"got {result2['final_duration']:.2f}s")

a1_ep2 = sv.sw_a1_duration_parity(result2["out"])
check("ep2 SW-A1 duration parity", a1_ep2.verdict == "PASS", a1_ep2.evidence)

a2_ep2 = sv.sw_a2_unit_duration(result2["units"])
check("ep2 SW-A2 every unit within tolerance of its expected duration",
      all(g.verdict == "PASS" for g in a2_ep2),
      "; ".join(g.evidence for g in a2_ep2 if g.verdict != "PASS"))

a3_ep2 = sv.sw_a3_total_duration(result2["final_duration"], result2["narration_len"], manifest_ep2.outro_hold)
check("ep2 SW-A3 total duration matches narration+hold", a3_ep2.verdict == "PASS", a3_ep2.evidence)

shutil.rmtree(SCRATCH, ignore_errors=True)
shutil.rmtree(manifest_ep1.episode_dir / "_assembly_validate", ignore_errors=True)
shutil.rmtree(manifest_ep2.episode_dir / "_assembly_validate", ignore_errors=True)
print(f"\n(scratch output + intermediate work dirs cleaned up -- nothing written to either "
      f"episode's real files)")

print("\n" + ("ALL PASS" if not FAILS else f"FAILED: {FAILS}"))
sys.exit(1 if FAILS else 0)
