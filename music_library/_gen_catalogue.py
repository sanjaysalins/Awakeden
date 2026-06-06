"""Generate CATALOGUE.md from _specs.py — the SINGLE SOURCE OF TRUTH.
Run after editing _specs.py so the human-readable catalogue can never drift.

  python _gen_catalogue.py
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from _specs import SPECS, BEAT_ALLOWED, PILOT_SLUGS, LAYER_ONLY_MOODS, beats_for_mood  # noqa: E402

MOOD_ORDER = ["sacred", "lonely", "tender", "neutral", "awe", "triumphant",
              "lament", "tension", "glory", "pastoral", "urgent"]
MOOD_BLURB = {
    "sacred": "devotional grace, melodic — the flagship beds",
    "lonely": "sparse, hollow, unresolved (hooks, outcasts) — narrative-only on the CTA",
    "tender": "warm human compassion, mercy, hope",
    "neutral": "unobtrusive exposition bed (the Point beat + long-form teaching stretches)",
    "awe": "mounting crescendo, revelation, wonder",
    "triumphant": "victory, resurrection, the King",
    "lament": "grief, suffering, the cross — narrative-only on the CTA",
    "tension": "dread, threat, chaos — NARRATIVE villainy ONLY, never conviction/landing",
    "glory": "holy stillness, PAD/DRONE (no melody → the only safe layer partner)",
    "pastoral": "peace, rest, the shepherd",
    "urgent": "forward motion, the call — narrative-only on the CTA",
}


def main():
    L = []
    w = L.append
    w("# Music Library Catalogue — instrumental beds (Suno v5.5)")
    w("")
    w("> AUTO-GENERATED from `_specs.py` (`python _gen_catalogue.py`). Do not hand-edit — "
      "edit `_specs.py` and regenerate, so prompts/tags never drift.")
    w("")
    w("Reusable **instrumental** music beds for the gospel engine (60s shorts + 6–8 min "
      "long-form). Generated on the user's flat-rate paid Suno plan (commercial rights), "
      "NOT metered ElevenLabs credits. Sibling to `sound_library` (SFX) / `image_library` (stills).")
    w("")
    w("**Suno settings (every track):** v5.5 · **Instrumental = ON** · save **both** takes as "
      "`<slug>_a.mp3` + `<slug>_b.mp3` → drop in `_inbox/` → `python ingest.py`.")
    w(f"**Count:** {len(SPECS)} prompts × 2 takes = **{len(SPECS) * 2} raw files** → audition → "
      f"approve **one primary take per base slug** (`_a`/`_b`/… are candidates; extra takes OK "
      f"if both have ghost drums/vocals). Not a guaranteed {len(SPECS)}.")
    w("")

    # ---- honesty / status -----------------------------------------------------
    w("## Status (honest)")
    w("- ✅ Built: library API, specs, ingest (LUFS + dBFS), audition/approve gate (`approve.py`: "
      "blocks a 2nd take per base unless `--force`; requires `--swell` on arc beds), doctrine-aware "
      "PRIMARY selection (`find_for_beat`; energy-fit is a ranking bonus, not a hard filter — a "
      "wrong-energy bed only loses if a better-fit one is approved), layer selection (`find_layer`, "
      "glory pads only).")
    w("- ✅ **`placer.py` is BUILT + PROVEN** on John 4 (4 pilot beds, 2026-06-06): lonely hook → "
      "sacred swell auto-aligned to the landing @ 47.8s → glory pad under the close, all ducked. "
      "**STT word-recovery 99.4%** (gate ≥98%), 59.0s, no clipping. Swell auto-detected via numpy "
      "RMS envelope. Generalizes the proven `enhance.py mix()`. See `PLACER.md`.")
    w("- 🔁 Eleven Music is the bespoke-per-clip fallback (key scope enabled 2026-06-06, so it "
      "works — but it's **metered**, so a reused Suno bed is preferred).")
    w("")

    # ---- architecture decision ------------------------------------------------
    w("## Shorts vs long-form architecture (resolves one-bed-vs-five-beats)")
    w("- **60s shorts = ONE primary melodic bed for the whole clip** (not per-beat swaps). "
      "Because it also covers the Landing it must be **CTA-safe** (picked via "
      "`find_for_beat('landing', …)`), + an optional `glory_*` pad layered under the landing.")
    w("- Music **ducks to near-silent under the verbatim KJV quote** (intelligibility — the "
      "aligner drops words under a music bed). Pilot gate = STT word-recovery ≥ 98%.")
    w("- **Long-form = one bed per movement**, crossfaded; pads looped; music off under "
      "scripture. **Phase 2** — out of the shorts pilot.")
    w("")

    # ---- staged plan (test-gate) ---------------------------------------------
    w("## Staged plan (test-gate discipline — don't batch all 20 first)")
    w(f"0. **Lock design (done):** `PLACER.md` + metadata/gates in code.")
    w(f"1. **Pilot ({len(PILOT_SLUGS)} beds):** generate `{', '.join(PILOT_SLUGS)}` "
      "(ingest is pilot-gated — `--all` to override). `placer.py` is built; **prove** it on "
      "John 4 against the acceptance gates in `PLACER.md` (`lonely_searching` = the hook open "
      "that crossfades into the CTA-safe `sacred_grace_rise` primary, + `glory` pad layer).")
    w("2. **Batch the rest** only after the loop passes and the look is locked.")
    w("3. Every track stays `status=pending` (unselectable) until a human audition approves it; "
      "arc beds require a `--swell` timestamp at approval.")
    w("")

    # ---- doctrine matrix ------------------------------------------------------
    w("## Beat → mood doctrine matrix (enforced in code by `find_for_beat`)")
    w("LOCKED: grace-anchored conviction — NO fear/pressure/unresolved-ache on the Conviction "
      "or Landing. `tension`/`urgent`/`lonely`/`lament` are narrative-only.")
    w("")
    w("| beat | allowed PRIMARY moods |")
    w("|---|---|")
    for beat, moods in BEAT_ALLOWED.items():
        w(f"| {beat} | {', '.join(sorted(moods))} |")
    w("")
    w(f"**Layer (not primary):** `{'/'.join(sorted(LAYER_ONLY_MOODS))}_*` beds are melody-free / "
      "rhythm-free — `find_for_beat` NEVER returns them; `find_layer()` does. They're the only "
      "safe second musical element under a primary bed. One primary melodic bed per clip.")
    w("")

    # ---- boundary + decision --------------------------------------------------
    w("## Boundaries")
    w("- **music_library vs sound_library:** music = melodic/score/atmosphere *beds*; "
      "sound_library = ambient SFX + one-shots (incl. the existing `heavenly_choir_soft` swell). "
      "Don't stack a `glory_*` pad AND the choir SFX on one landing — pick one.")
    w("- **Suno bed vs Eleven Music:** default to a reusable Suno bed ($0, flat plan). Use a "
      "bespoke Eleven Music score only when a clip needs a custom-timed climax and the spend is OK.")
    w("- **License:** Suno paid plan grants commercial USE but not copyright protection. `ingest.py` "
      "records `source/license/created`; add the Suno export URL via `approve.py --url`.")
    w("")

    # ---- the prompts ----------------------------------------------------------
    w("## The Suno v5.5 style prompts (instrumental)")
    w("> Paste each into Suno's **Style** box, Instrumental ON. Tempo is given as musical terms "
      "(Suno ignores numeric BPM).")
    w("")
    for mood in MOOD_ORDER:
        slugs = [s for s, sp in SPECS.items() if sp["mood"] == mood]
        if not slugs:
            continue
        w(f"### {mood.upper()} — {MOOD_BLURB.get(mood, '')}")
        for slug in slugs:
            sp = SPECS[slug]
            pilot = "  ⭐PILOT" if slug in PILOT_SLUGS else ""
            w(f"**`{slug}`**{pilot} → `{slug}_a.mp3`, `{slug}_b.mp3`  ·  beats: "
              f"{', '.join(beats_for_mood(mood)) or '(narrative-only)'}")
            w(f"`{sp['prompt']}`")
            w("")
    out = HERE / "CATALOGUE.md"
    out.write_text("\n".join(L), encoding="utf-8")
    print(f"wrote {out} ({len(SPECS)} beds, {len(SPECS)*2} takes)")


if __name__ == "__main__":
    main()
