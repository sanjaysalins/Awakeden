# RESUME — Audio enhancement + Music library (paused 2026-06-06)

Pick up here tomorrow. Two related tracks ran today: (1) enhancing the **Well / John 4**
viral_cut with music+SFX, (2) building a reusable **Suno music library** with an AI-panel.

---

## ✅ What's DONE today

### 1. Well (John 4) clip — audio enhancement test (`11labs-testing/`)
Layered music + SFX UNDER the existing narration, ducked.
- **ElevenLabs-music version (you liked the music):**
  `C:\Users\sanjay\PycharmProjects\JesusInTheBible\11labs-testing\viral_cut_enhanced.mp4`
  (Eleven Music score + well-water + faint village + waterpot SFX, no choir, ducked)
- New SFX `waterpot_drop_run` registered into `sound_library` (now 30 clips incl. the
  Eleven score `score_reverent_grace`).
- ElevenLabs key scopes `music_generation` + `user_read` were enabled today (music works).

### 2. Music library (`music_library/`) — reusable Suno beds, panel-hardened
- **20-bed catalogue** (11 moods), `_specs.py` = single source of truth →
  `python _gen_catalogue.py` rebuilds `CATALOGUE.md`. Doctrine + audition gated.
- **3 AI-panel rounds** (`music_library/_independent_review/`): round 3 = claude PASS +
  3 REVISE converging on "build the placer". Built it.
- **`placer.py` BUILT + PROVEN** on John 4: lonely hook → sacred swell auto-aligned to the
  landing @47.8s → glory pad under the close, all ducked; **STT word-recovery 99.4%** (gate
  ≥98%). Swell auto-detected (numpy RMS). `--ambience` adds sound_library SFX (water) under music.
- **`qc.py`** auto-QC: reliable **vocal-leak** flag (Whisper ASR) + swell/LUFS. Drums are
  ear-checked (numpy beat heuristic was unreliable; librosa/Demucs not installed — cut it).
- **4 pilot beds generated + ingested + approved** (`_a` takes): sacred_grace_rise (swell 130.4s),
  lonely_searching, neutral_teaching_warm, glory_holy_stillness.
- Pilot outputs to compare:
  - Suno music + water: `C:\Users\sanjay\PycharmProjects\JesusInTheBible\music_library\pilot_well_water.mp4`
  - Suno music, no water: `C:\Users\sanjay\PycharmProjects\JesusInTheBible\music_library\pilot_well_placed.mp4`

---

## 🟡 OPEN — your verdict so far
- You felt the **bespoke ElevenLabs score sounded better** than the Suno pilot, and the Suno
  pilot was **missing the water** (fixed: placer now layers it). Diagnosis: **the Suno prompts
  need work** — fixed by rewriting to production-brief style + purity tags.

---

## ▶️ NEXT (do this first tomorrow)
1. **Regenerate the 4 pilot beds in Suno** with the IMPROVED prompts (in
   `C:\Users\sanjay\PycharmProjects\JesusInTheBible\music_library\CATALOGUE.md`,
   ⭐PILOT beds). They're now production-brief style + "instrumental only, no vocals, no choir,
   no drums". Suno: Custom · Instrumental ON · ~2–3 min · download both takes.
2. **A/B the flagship `sacred_grace_rise` 3 ways** to find the best prompt lever:
   the catalogue prompt · structure-tags in the lyrics box · composer-style (Max Richter /
   Ólafur Arnalds). Whichever wins, I bake it into all 20.
3. Save takes to `C:\Users\sanjay\PycharmProjects\JesusInTheBible\music_library\_inbox\`
   (name `<slug>_a.mp3`, `<slug>_b.mp3`; extra takes `_c` OK).
4. Tell me — I run: `ingest.py` → `qc.py` (vocal gate) → `approve.py` (with `--swell` for sacred)
   → `placer.py` on John 4 **with `--ambience river_well_water:-17`** so it's a fair A/B vs the
   Eleven version.
5. **Decision pending:** Suno library (flat cost, reusable) vs bespoke ElevenLabs (metered, you
   preferred the sound) — judge once the improved Suno prompts are in. Could also be hybrid
   (Eleven for hero clips, Suno for volume).

### Run commands (reminders)
```
cd C:\Users\sanjay\PycharmProjects\JesusInTheBible
.venv\Scripts\python.exe music_library\ingest.py            # pilot-gated; --all for full catalogue
.venv\Scripts\python.exe music_library\qc.py                # vocal-leak flag + swell/LUFS
.venv\Scripts\python.exe music_library\approve.py --list
.venv\Scripts\python.exe music_library\placer.py --help
```

---

## ⏭️ Later / backlog
- If Suno wins: **batch the other 16 beds** (`ingest.py --all`), approve, build out the library.
- Long-form music strategy (per-movement beds, crossfade) = Phase 2 (see `music_library/PLACER.md`).
- Optional: widen the KJV-quote duck to the full verse (the pilot's `--quote` only matched the
  first half of the John 4:14 quote).
- STANDING last step on any finished clip: captions via
  `.venv\Scripts\python.exe -m veed_io.caption --video "<clip>"`.
