# SOUNDSTAGE_SPEC.md — Long-form Immersive Audio (design doc)

> ## ⚠️ RED-TEAM VERDICT (2026-06-04): DON'T BUILD THIS YET — REVISE FIRST
> An independent red-team (verified against the code) found the plan builds heavy
> machinery on a broken timing source, ignores a free precision tool the repo already
> owns, and bakes two doctrinal/tone judgments into "locked" rules. **Pilot the experience
> by hand before building any tooling.** Must-fix list before this spec is buildable:
>
> 1. **CRITICAL — timing source is unusable.** §2/§3 anchor sounds to `narration.meta.json`,
>    but its `final_seconds` is index-misaligned with `turns` once silence pads exist
>    (verified: meta turn 3 `the_LORD` 6.48s read shows `final_seconds:0.4` = the pad).
>    CLAUDE.md already calls it "the scrambled meta." → Use `pipeline/assembly_timing.build_timeline`
>    or `pipeline/assembly_align.py`, NOT the meta.
> 2. **CRITICAL — the precision tool already exists.** §3's "char-position × duration" cue
>    placement is reinvented and ±2–4s off (non-uniform read, `[slow]` tags, 64s turns).
>    `pipeline/assembly_align.py` (local faster_whisper) gives exact per-word times, free.
>    Use it in BUILD, not just validation.
> 3. **HIGH — casting re-opens a locked, panel-approved script.** `narration-tagged.md:1-4`
>    deliberately keeps Isaiah's lines narrator-voiced. Re-casting 14 spans to an `isaiah`
>    voice must re-enter the panel/finalize gate, not just `kjv_check`.
> 4. **HIGH — doctrinal mis-cast.** §8 routes "for the transgression of my people was he
>    stricken" to God's voice; it is THIRD person (`narration-tagged.md:72`) — the prophet's
>    report, not God's first-person speech. WHO speaks v.4–6 ("Surely *he* hath borne *our*
>    griefs" = the redeemed "we") has no simple rule. → Casting OT scripture voice goes to
>    the PANEL, not a deterministic B1 heuristic.
> 5. **HIGH — verbatim gate has a hole.** `kjv_check` only inspects quoted spans ≥3 words;
>    words moved into prose during re-tagging are invisible. → Add a byte-identity partition
>    check around B1 (concatenation of all spans == original, normalized).
> 6. **MED — SFX beds.** ElevenLabs Sound-FX hard cap = 30s; loop only on
>    `eleven_text_to_sound_v2` (40 credits/s). An 8-min bed needs a seamless tiled loop, not
>    "cross-fade to length." Pin the model + `loop=true`. Drop `philip` (no line in Isa 53).
> 7. **MED — mix.** Single-pass `loudnorm` will PUMP the bed up in speech gaps (and in
>    `sacred_clean_windows`). → Two-pass loudnorm / static bed gain + a bus limiter.
> 8. **MED — validation overclaims.** The agent "reverence review" reads JSON+transcript, it
>    never HEARS the mix; and whisper STT recovery is a weak proxy for human intelligibility
>    (noise-robust → false PASS). → Make per-verse-window RMS/SNR the intelligibility gate;
>    add a real HUMAN LISTEN gate; demote STT to a smoke test.
>
> **Recommended path:** hand-craft ONE Isaiah 53 immersive mix (manual ffmpeg, ~6 cues placed
> with the existing free aligner, prophet cast by hand), ship it, USER LISTENS. Only if it
> clearly beats narrator+silence do we build the tooling — and the working filtergraph
> becomes the real spec. The sections below are the ORIGINAL (pre-red-team) design; read them
> through the lens of the fixes above.

**Status:** DESIGN DRAFTED, RED-TEAMED → REVISE. NOT built. Audio-only scope.
**Author:** drafted 2026-06-04 with the user. Pilot target = Isaiah 53.
**Folder it serves:** `C:\Users\sanjay\PycharmProjects\JesusInTheBible\longform\`

This spec turns long-form narration from *one documentary narrator + silence* into a
**soundstage**: the prophet reads his own words, God speaks God's words, named NT people
get their own voices, and a living-but-restrained sound bed (wind, sea, thunder, footsteps,
the nails) sits *under* the read — designed so the later 16:9 clips can match it.

Two new pipelines, exactly as the user asked: a **BUILD** pipeline that creates the
immersive track, and a **VALIDATION** pipeline that proves the design actually happened
and that no scripture word got buried.

---

## 0. Locked decisions (do not relitigate without the user)

1. **Casting = FULL author + character cast.**
   - `narrator` (teacher/documentary voice) reads ONLY the commentary/teaching prose.
   - The **prophet's own voice** reads his scripture. Isaiah reads Isaiah 53.
     (Jeremiah reads Jeremiah, David/Psalmist reads the Psalms, in later episodes.)
   - **God's voice** (`the_LORD`) reads God's *direct* speech only (e.g. Isa 52:13;
     "for the transgression of my people"; "Behold, my servant").
   - NT speakers get their own voices: `eunuch` (Ethiopian), `philip`, etc.
2. **SFX source = ElevenLabs Sound Effects API** (same vendor + key as the voices).
   Metered. Every sound is **cached** so it is paid for once. **Always quote exact spend
   and get explicit OK before any metered render** (standing rule, memory
   `feedback-ask-before-spending`).
3. **Intensity = RESTRAINED & REVERENT.** Subtle, prayerful bed. The nails are *felt* —
   a single weighty, distant strike — never graphic. Sound supports the text and gets out
   of the way. Narration is ALWAYS dominant. No sensationalism.
4. **This session = design doc only.** No code, no spend. (This file.)

---

## 1. Principles (binding)

- **Scripture is never obscured.** Beds duck under speech; nothing competes with a
  quoted verse. The intelligibility check (Validation B) is fail-closed.
- **Reverence on sacred moments.** God's direct speech plays *clean* — no SFX over it.
  The cross/nails are weighty, not gory.
- **The narrator never impersonates the prophet.** Teaching prose = narrator. Quoted
  scripture = the author. This keeps the doctrinal line clear (commentary vs the Word).
- **KJV verbatim survives casting.** Re-tagging who-speaks-what must NOT change a single
  quoted word. Re-checked by `kjv_check` after the cast pass.
- **One plan drives audio AND the future video.** `soundstage_plan.json` carries a
  `visual_cue` on every sound, so the later 16:9 clip stage reads the same file and the
  rain you HEAR is the rain you SEE.
- **Reuse downstream pipelines.** `per_turn_synth.py` renders the voices; `kjv_check`
  validates verbatim; `faster_whisper` (from `veed_io`) does the STT intelligibility
  read. We do NOT re-implement TTS or STT.

---

## 2. Architecture

```
                 narration.md  (locked long-form script)
                        │
   ┌────────────────────┴──────────────────────────────┐
   │   BUILD PIPELINE                                    │
   │   cli_soundstage.py "<v1>"                          │
   ├────────────────────────────────────────────────────┤
   │ B1 CAST design   (LLM, agent-mode)                  │ → narration-tagged.md (rich) + voices.json (cast)
   │ B2 SOUND design  (LLM, agent-mode)                  │ → soundstage_plan.json
   │ B3 VOICE render  per_turn_synth --natural  (REUSE)  │ → narration.voice.mp3 + narration.meta.json (grid)
   │ B4 SOUND fetch   ElevenLabs Sound-FX  [METERED]     │ → _sfx/<hash>.mp3 cache (idempotent)
   │ B5 MIX           ffmpeg sidechain duck + layer      │ → narration.immersive.mp3 + mix.log.json
   └────────────────────────────────────────────────────┘
                        │
   ┌────────────────────┴──────────────────────────────┐
   │   VALIDATION PIPELINE                               │
   │   cli_soundstage_audit.py "<v1>"                    │
   ├────────────────────────────────────────────────────┤
   │ A deterministic  cast/verbatim/coverage/levels      │ → soundstage.audit.json (PASS/FAIL gates)
   │ B perceptual     faster_whisper STT vs script       │ → intelligibility report (every verse word heard)
   │ C reverence      independent agent review            │ → soundstage.independent-review.md
   └────────────────────────────────────────────────────┘
```

Build runs in order; **B3 must run before B5** because the mix needs the per-turn timing
grid (`narration.meta.json`) to place sounds. Validation runs after a full build.

---

## 3. Data model — `soundstage_plan.json`

One file per `<v1>` folder. Anchors every sound to the **turn grid** (turn index +
position), so it stays correct even if a re-render shifts absolute times slightly.

```jsonc
{
  "version": 1,
  "folder": "01_Isaiah_53_Suffering_Servant",
  "cast": {
    "narrator":  { "voice_id": "LSi9zNCeliLuhIGGS0By", "role": "teacher/commentary" },
    "isaiah":    { "voice_id": "<TBD>",                "role": "prophet — reads Isaiah 53 quotes" },
    "the_LORD":  { "voice_id": "UzI1NsMEV3ni5JRkRSls", "role": "God — direct speech only" },
    "eunuch":    { "voice_id": "puDRtQWF8NtQiPMJygTb", "role": "Ethiopian official (Acts 8:34)" },
    "philip":    { "voice_id": "<TBD>",                "role": "Philip (Acts 8)" }
  },

  "ambience": [                       // long beds, low under speech
    {
      "id": "amb_open_wind",
      "intent": "lonely Judean wind — the prophet alone with the vision",
      "sfx_prompt": "soft desolate desert wind, distant, low, seamless loop, no music",
      "start": { "turn": 0,  "pos": "start" },
      "end":   { "turn": 5,  "pos": "end"   },
      "gain_db": -26, "fade_in": 2.0, "fade_out": 2.5, "duck_under_speech": true,
      "visual_cue": "wide empty Judean wilderness, wind-moved dust"
    }
  ],

  "sfx": [                           // point one-shots
    {
      "id": "sfx_nail",
      "intent": "the cost made audible — a single weighty, distant strike (RESTRAINED)",
      "sfx_prompt": "one single distant heavy iron hammer strike on metal, deep, reverberant, solemn, no echo spam",
      "anchor": { "turn": 18, "pos": "word", "phrase": "wounded for our transgressions" },
      "lead_ms": -250, "gain_db": -14, "duck_under_speech": true, "reverence": true,
      "visual_cue": "the hammer/nail beat — do not show gore"
    }
  ],

  "mix": {
    "target_lufs": -16.0,            // integrated loudness of final mix
    "speech_floor_db": -3.0,         // voice stem normalization ceiling
    "bed_below_speech_db": 12.0,     // beds must sit >=12 dB under speech (validation gate)
    "sacred_clean_windows": [        // NO sfx/bed swell allowed inside these (God's words)
      { "turn": 6, "reason": "Behold my servant — God speaks" }
    ]
  }
}
```

**Anchor positions:** `start` | `end` of a turn, or `word` + `phrase` (the mixer finds
the phrase's fractional offset within the turn from char position × turn duration; good
enough at restrained levels — no forced alignment needed).

---

## 4. BUILD pipeline — stage detail

### B1 — Cast design  (`pipeline/soundstage_cast.py`, LLM agent-mode, free)
- Input: `narration.md` (+ existing `narration-tagged.md` if present).
- Read every quoted span. Decide its speaker by the casting rule (§0.1):
  scripture-by-this-author → that author's voice; God's direct words → `the_LORD`;
  NT person → that person; teaching prose → `narrator`.
- Output: a richer `narration-tagged.md` (more `<speaker>` spans) + `voices.json` cast.
- **Constraint:** never alter a quoted word; only wrap/route it. (Re-checked in Validation A.)
- New voice_ids (isaiah, philip, …) come from `config.VOICE_MAP` / a long-form cast roster;
  pick distinct, fitting ElevenLabs voices (prophet = weathered/gravitas; Philip = warm/clear).

### B2 — Sound design  (`pipeline/soundstage_sound.py`, LLM agent-mode, free)
- Input: `narration.md` + the turn list.
- Propose ambience beds + SFX one-shots under the **restrained-reverent** rule:
  beds for *place* (wilderness wind, road, crowd-from-a-distance, Golgotha hush),
  one-shots for *named events* in the text (chariot wheels on the Gaza road, a lamb,
  the single nail-strike, a low thunder at "it pleased the LORD").
- Each item gets: intent, `sfx_prompt` (for ElevenLabs), anchor, gain/fade, `visual_cue`.
- **Hard rules the designer must honor:** no sound inside `sacred_clean_windows`; nothing
  graphic; ≤ ~1 one-shot per ~20s so it never turns into a sound-effects reel; beds change
  only at movement boundaries (the 7-movement spine).
- Output: `soundstage_plan.json`.

### B3 — Voice render  (REUSE `per_turn_synth.py`, metered ElevenLabs voices)
- Run exactly the proven long-form recipe (natural pace, no stretch):
  ```
  per_turn_synth.py "<v1>" --target 600 --natural --no-gate \
      --pre-quote-pause 0.4 --post-quote-pause 0.35 --stability 0.65
  ```
- Produces the **voice-only stem** + `narration.meta.json` (per-turn durations = the grid).
- **Change needed:** today this writes `narration.mp3`. For the soundstage we want the
  voice stem kept separate so the mix doesn't clobber it. Options (decide at build time):
  (a) add a `--out-name narration.voice.mp3` flag to per_turn_synth (tiny, clean), or
  (b) copy `narration.mp3` → `narration.voice.mp3` right after B3. **Prefer (a).**

### B4 — Sound fetch  (`pipeline/soundstage_fetch.py`, METERED ElevenLabs Sound-FX)
- For each ambience/sfx item: POST `sfx_prompt` to ElevenLabs Sound Effects
  (`/v1/sound-generation`), request duration ≈ the window length (loops for beds).
- **Cache by hash of (prompt, duration):** `_sfx/<sha1>.mp3`. Idempotent — re-runs are free.
- Beds longer than the API max are tiled/cross-faded to length in B5.
- **GATE BEFORE SPEND:** print the full item list + estimated credit/$ cost and require a
  `--yes` flag (red banner, same discipline as `veed_io`, memory `feedback-veed-io-spend-control`).

### B5 — Mix  (`pipeline/soundstage_mix.py`, ffmpeg, free)
- Load voice stem + the grid; compute each sound's absolute start from its anchor.
- Build one ffmpeg `filter_complex`:
  - voice stem = lead, loudness-normalized to `speech_floor_db`;
  - each bed: `adelay` to its start, `afade` in/out, `volume=gain_db`, then
    **`sidechaincompress`** keyed off the voice so beds dip whenever the narrator speaks;
  - each one-shot: `adelay` + `volume`, also sidechain-ducked unless it's in a speech gap;
  - `amix` everything, then `loudnorm` to `target_lufs`.
- Output: `narration.immersive.mp3` + `mix.log.json` (every layer, its start/gain, the
  exact filtergraph) — the log is what Validation A reads.

---

## 5. VALIDATION pipeline — `cli_soundstage_audit.py`

### A — Deterministic gates (no LLM; fail-closed)
- **SS-G1 cast coverage:** every turn has a speaker present in `cast`; every `voice_id` non-empty.
- **SS-G2 verbatim survival:** run `kjv_check` on every quoted span in the (re-cast)
  `narration-tagged.md` against the cached wider pericope. Any altered word → FAIL.
- **SS-G3 sound coverage:** every item in `soundstage_plan.json` has a rendered file in
  `_sfx/` AND appears in `mix.log.json`. A planned sound that never made it into the mix → FAIL.
- **SS-G4 level discipline:** measured bed RMS sits ≥ `bed_below_speech_db` under the voice
  stem RMS in the same window (beds aren't drowning speech).
- **SS-G5 sacred clean:** no sound overlaps any `sacred_clean_windows` range.
- **SS-G6 density:** no more than N one-shots per minute (anti sound-reel guard).
- Output: `soundstage.audit.json` with per-gate PASS/FAIL. Any FAIL blocks "locked".

### B — Perceptual intelligibility (REUSE `faster_whisper`, free/local)
- STT the **final** `narration.immersive.mp3` → transcript with word timings.
- Diff transcript against the script. **Every scripture word must be recovered** (fuzzy
  match, tolerant of homophones). A verse word the STT can't hear = it's buried = FAIL.
- This is the real "is the immersion HELPING not HURTING the Word" test.
- Output: `intelligibility.json` (missing/low-confidence words + the second they occur).

### C — Independent reverence review (agent-mode, free; standing rule
`always-independent-red-team`)
- A fresh hostile reviewer reads `narration.md` + `soundstage_plan.json` (+ the
  intelligibility report) and asks: does any sound sensationalize, distract, undercut
  reverence, or compete with God's words? Authoritative on tone.
- Output: `soundstage.independent-review.md`.

---

## 6. Reuse map (CLAUDE.md: do not duplicate downstream pipelines)

| Need | Reuse | New code |
| --- | --- | --- |
| Multi-voice TTS | `per_turn_synth.py` (subprocess, `--natural`) | only a `--out-name` flag |
| KJV verbatim | `pipeline/kjv_check.py` | — |
| STT intelligibility | `veed_io` `faster_whisper` timings | thin wrapper |
| LLM calls | agent-bridge (`LLM_PROVIDER=agent`) | cast/sound design prompts |
| SFX generation | ElevenLabs Sound-FX API | `soundstage_fetch.py` + cache |
| Mix | ffmpeg | `soundstage_mix.py` filtergraph |

New files (all NEW, nothing duplicated):
`cli_soundstage.py`, `cli_soundstage_audit.py`,
`pipeline/soundstage_models.py` (Cast, Ambience, Sfx, SoundstagePlan, MixSpec, AuditResult),
`pipeline/soundstage_cast.py`, `pipeline/soundstage_sound.py`,
`pipeline/soundstage_fetch.py`, `pipeline/soundstage_mix.py`,
`pipeline/soundstage_audit.py`.

---

## 7. Cost model (audio-only)

- **Voices (B3):** already proven ≈ $1–2 (ElevenLabs eleven_v3, ~6.5k chars). Re-render
  only when the cast changes.
- **Sound-FX (B4):** ElevenLabs Sound Effects ≈ a few cents per generation; Isaiah 53
  ≈ 12–20 sounds → est. **~$2–5**, paid once (cached). **Exact list + cost quoted before run.**
- **Design (B1/B2), Validation (A/B/C):** agent-mode = $0; STT = local = $0.
- **Per long-form episode all-in: ~$4–8 audio.** (Video is separate, not in scope.)

---

## 8. Isaiah 53 — worked starting point (for when we build)

**Cast:** narrator (teacher) · `isaiah` (all the Isaiah 52–53 quotes — currently narrator-
voiced) · `the_LORD` (Isa 52:13 "Behold my servant"; "for the transgression of my people
was he stricken" — God's first-person) · `eunuch` (Acts 8:34) · `philip` (the "preached
unto him Jesus" line is *narration about* Philip, so it stays narrator — Philip has no
quoted line here; keep him in the roster for other episodes).

**Sound sketch (restrained):**
- bed: lonely Judean wind under the opening report (movements 1).
- low single thunder-roll under "Yet it pleased the LORD to bruise him" (movement 6) —
  weighty, distant, NOT a storm.
- a flock/lamb breath + distant shears under "as a sheep before her shearers is dumb".
- chariot wheels + open-road wind under the Gaza-road / eunuch movement (Acts 8).
- ONE distant nail-strike under "wounded for our transgressions" (the only "cross" SFX —
  reverent, singular).
- a soft dawn/birds-far-off lift under "toward morning … see his seed" (resurrection turn).
- `sacred_clean_windows`: God's two direct-speech turns play with bed ducked to near-silence.

---

## 9. Forward-compat: audio → video sync (later, not now)

Every ambience/sfx item carries `visual_cue`. When the 16:9 long-form visual stage is
built, its scene planner reads `soundstage_plan.json` so each sound has a matching shot
(the nail you hear = the hammer beat you see; the wind you hear = the wilderness you see).
This is why the sound plan is designed first and lives in one shared file.

---

## 10. Build order (when greenlit — each step its own approval)

1. `soundstage_models.py` + `cli_soundstage.py` skeleton (free).
2. B1 cast + B2 sound design on Isaiah 53 → human-review the `soundstage_plan.json` (free).
3. Add `per_turn_synth.py --out-name` (tiny) + B3 re-render with the full cast (~$1–2, quoted).
4. B4 fetch + B5 mix → first `narration.immersive.mp3` (~$2–5 SFX, quoted, gated `--yes`).
5. Validation A/B/C → fix → lock.
6. Generalize to the long-form catalogue; wire `visual_cue` into the future 16:9 stage.
