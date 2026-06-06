"""SINGLE SOURCE OF TRUTH for the music catalogue.

CATALOGUE.md is GENERATED from this file (`python _gen_catalogue.py`) so prompts/tags
can never drift. ingest.py also reads this to tag each Suno download.

Post-panel revisions (2026-06-06):
  * tempo as musical terms, not bare BPM (Suno ignores numeric BPM) — bpm kept as a hint
  * added a NEUTRAL/exposition mood (the Point beat + long-form teaching stretches) — gap
    flagged by the panel; removed 2 redundant beds (kingdom-brass, dawn-hope) to stay ~20
  * doctrine is now DATA (BEAT_ALLOWED) the selector enforces, not prose
"""

# ---- doctrine: which moods may underscore each Gospel-Five-Beat beat ----------
# LOCKED rule: grace-anchored conviction — NO fear / pressure / unresolved-ache on the
# Conviction or Landing. So tension/urgent/lonely/lament are NARRATIVE-ONLY (the story's
# villainy/suffering), never the turn or the CTA.
# PRIMARY-bed moods per beat (glory is NOT here — it is a layer, see LAYER_ONLY_MOODS).
BEAT_ALLOWED = {
    "hook":       {"lonely", "tension", "urgent", "awe", "lament", "neutral"},
    "point":      {"neutral", "tender", "sacred", "pastoral", "awe"},
    "proof":      {"awe", "sacred", "tender", "neutral", "triumphant"},
    "conviction": {"sacred", "tender", "pastoral", "neutral"},
    "landing":    {"sacred", "tender", "pastoral", "neutral", "triumphant"},
}
# moods that may be the PRIMARY bed under the Conviction/Landing (the CTA) — convenience set
CTA_SAFE_MOODS = BEAT_ALLOWED["conviction"] | BEAT_ALLOWED["landing"]

# glory_* beds are melody-free / rhythm-free → LAYER-ONLY: they never serve as the primary
# bed (find_for_beat excludes them); they may sit UNDER a primary melodic bed via find_layer()
# without the "two music" clash. Rule: ONE primary melodic bed per clip, + optional glory pad.
LAYER_ONLY_MOODS = {"glory"}

# energy fitness per beat — find_for_beat prefers a bed whose energy matches the beat's job
# (e.g. exposition Point wants a flat/low bed, not a grace swell; Landing wants the climax).
BEAT_PREFERRED_ENERGY = {
    "hook":       {"low", "build"},
    "point":      {"low"},
    "proof":      {"build", "swell-and-rest"},
    "conviction": {"low"},
    "landing":    {"build", "climax"},
}

# base_slug: dict(mood, energy, tempo, tempo_bpm, instrumentation, tags, use_cases, prompt)
SPECS = {
    "sacred_grace_rise": dict(mood="sacred", energy="build", tempo="slow, adagio", tempo_bpm=60,
        instrumentation="strings, grand piano, duduk",
        tags=["sacred", "reverent", "grace", "build", "climax", "strings", "piano", "duduk"],
        use_cases=["landing", "cta", "grace-climax"],
        prompt="Cinematic neoclassical film score, sacred and tender; solo piano, warm strings, subtle duduk; starts intimate and sparse, one steady build to a warm redemptive climax near the end, then gentle resolve; clean film-score mix, instrumental only, no vocals, no choir, no drums"),
    "sacred_intimate_piano": dict(mood="sacred", energy="low", tempo="slow, adagio", tempo_bpm=55,
        instrumentation="solo piano, string pad",
        tags=["sacred", "intimate", "piano", "prayerful", "hushed", "devotional"],
        use_cases=["quiet-revelation", "devotional-close", "conviction"],
        prompt="intimate sacred solo piano with delicate string pad underneath, prayerful, hushed, tender devotional, lots of space and air, chamber, no percussion, slow adagio"),
    "lonely_searching": dict(mood="lonely", energy="low", tempo="very slow, largo", tempo_bpm=50,
        instrumentation="solo cello, duduk",
        tags=["lonely", "searching", "hollow", "cello", "duduk", "sparse", "unresolved"],
        use_cases=["hook", "outcast", "the-ache"],
        prompt="Sparse neoclassical cinematic, hollow and searching; lone cello and distant duduk over faint ambient strings; very slow, lots of space, unresolved; instrumental only, no vocals, no choir, no drums"),
    "lonely_windswept": dict(mood="lonely", energy="low", tempo="free, no pulse", tempo_bpm=None,
        instrumentation="drone, ney flute, dark strings",
        tags=["lonely", "desolate", "wilderness", "drone", "ney", "bleak", "isolation"],
        use_cases=["hook", "wilderness", "temptation", "desolation"],
        prompt="desolate ambient cinematic, low drone with a thin lonely ney flute, windswept wilderness, bleak and barren, sustained dark strings, sense of isolation, no rhythm, no drums"),
    "tender_compassion": dict(mood="tender", energy="low", tempo="gentle, andante", tempo_bpm=62,
        instrumentation="warm strings, harp",
        tags=["tender", "compassion", "warm", "harp", "mercy", "comforting", "hopeful", "healing", "hope"],
        use_cases=["jesus-speaks", "mercy", "conviction", "healing", "new-beginning"],
        prompt="tender cinematic, warm strings and soft harp, gentle and compassionate, comforting, mercy and kindness, hopeful glow, chamber orchestra, no drums, gentle andante"),
    "awe_revelation_build": dict(mood="awe", energy="build", tempo="moderate, moderato", tempo_bpm=70,
        instrumentation="strings, wordless choir pad",
        tags=["awe", "revelation", "crescendo", "wonder", "choir-pad", "rising", "epic"],
        use_cases=["proof", "ot-echo", "build"],
        prompt="cinematic crescendo, building orchestral strings layered with a soft wordless choir pad, mounting wonder and revelation, steadily rising to an awe-struck peak, epic but reverent, no drum beat, moderate moderato"),
    "awe_holy_mystery": dict(mood="awe", energy="swell-and-rest", tempo="slow swell", tempo_bpm=None,
        instrumentation="high strings, low cello, glassy bells",
        tags=["awe", "mystery", "sacred", "shimmering", "bells", "otherworldly", "divine"],
        use_cases=["divine-near", "wonder", "proof"],
        prompt="mysterious sacred ambient, shimmering high strings over deep low cello, glassy bells, sense of the divine drawing near, holy and otherworldly, slow swelling, no percussion"),
    "triumphant_resurrection": dict(mood="triumphant", energy="climax", tempo="lively, allegretto", tempo_bpm=80,
        instrumentation="full strings, soaring brass, timpani",
        tags=["triumphant", "resurrection", "victory", "brass", "radiant", "uplifting", "epic", "regal", "kingdom"],
        use_cases=["resurrection", "victory", "he-is-risen", "christ-the-king", "prophecy-fulfilled"],
        prompt="triumphant cinematic orchestral, bright full strings and soaring brass, radiant and victorious, redemptive resurrection swell, glorious and uplifting, majestic and kingly, epic finale, light timpani swells, lively allegretto"),
    "lament_suffering_cello": dict(mood="lament", energy="low", tempo="very slow, grave", tempo_bpm=48,
        instrumentation="solo cello, low strings",
        tags=["lament", "suffering", "cello", "mournful", "grief", "heavy", "sorrow"],
        use_cases=["isaiah-53", "suffering-servant", "the-cross"],
        prompt="mournful cinematic, grieving solo cello over low sustained strings, sorrowful and heavy, the weight of suffering, aching lament, dark chamber, no drums, very slow grave"),
    "lament_forsaken": dict(mood="lament", energy="low", tempo="extremely slow", tempo_bpm=None,
        instrumentation="sparse strings, lone violin",
        tags=["lament", "forsaken", "desolate", "violin", "anguish", "hollow", "ambient"],
        use_cases=["psalm-22", "gethsemane", "forsaken"],
        prompt="desolate sacred lament, near-silent sparse strings and a distant lone violin, abandonment and anguish, hollow grief, almost ambient, trembling, no percussion, extremely slow"),
    "tension_dread_pulse": dict(mood="tension", energy="build", tempo="driving moderate", tempo_bpm=90,
        instrumentation="low string ostinato, sub pulse",
        tags=["tension", "dread", "ostinato", "ominous", "threat", "dark", "narrative-only"],
        use_cases=["betrayal", "arrest", "judgment"],
        prompt="dark cinematic tension, low pulsing string ostinato, no melody, mounting dread and unease, ominous undertow, creeping threat, sparse low percussion pulse, driving moderate"),
    "tension_storm_unrest": dict(mood="tension", energy="climax", tempo="agitated", tempo_bpm=None,
        instrumentation="tremolo strings, low brass, percussion swells",
        tags=["tension", "storm", "chaos", "tremolo", "turmoil", "danger", "narrative-only"],
        use_cases=["storm-at-sea", "the-mob", "chaos"],
        prompt="agitated cinematic storm, frantic tremolo strings and swelling low brass, chaos and turmoil, rising percussion swells, danger and unrest, dramatic, intense"),
    "glory_holy_stillness": dict(mood="glory", energy="low", tempo="free, no pulse", tempo_bpm=None,
        instrumentation="ethereal pad, low strings",
        tags=["glory", "stillness", "drone", "pad", "weightless", "holy", "layerable", "no-melody"],
        use_cases=["heaven", "theophany", "layer-under-melodic"],
        prompt="Sacred ambient drone, weightless and holy; sustained ethereal pad with soft low strings; timeless, no melody, no rhythm, slow evolving texture; instrumental only, no vocals, no choir, no drums"),
    "glory_light_descending": dict(mood="glory", energy="swell-and-rest", tempo="slow swell", tempo_bpm=None,
        instrumentation="warm pad, glassy bells, high strings",
        tags=["glory", "light", "radiant", "pad", "bells", "divine", "swell", "layerable"],
        use_cases=["divine-breaking-in", "radiance"],
        prompt="radiant sacred ambient, slowly swelling warm pad with gentle glassy bells and soft high strings, the divine breaking in, light descending, glowing and holy, no beat, no drums"),
    "pastoral_still_waters": dict(mood="pastoral", energy="low", tempo="gentle, andante", tempo_bpm=64,
        instrumentation="flowing strings, harp, woodwind",
        tags=["pastoral", "peace", "rest", "harp", "serene", "still-waters", "calm"],
        use_cases=["psalm-23", "rest", "peace", "conviction"],
        prompt="peaceful pastoral cinematic, gentle flowing strings and soft harp with light woodwind, restful and serene, still waters, green pastures, calm reassuring, no drums, gentle andante"),
    "pastoral_shepherd_calm": dict(mood="pastoral", energy="low", tempo="moderate, andante", tempo_bpm=68,
        instrumentation="acoustic strings, soft flute",
        tags=["pastoral", "shepherd", "comfort", "flute", "homely", "gentle", "intimate"],
        use_cases=["the-shepherd", "the-flock", "comfort"],
        prompt="warm folk-orchestral, simple gentle acoustic strings and soft flute, comforting and homely, the good shepherd, pastoral calm, intimate, no drums, moderate andante"),
    "urgent_journey_drive": dict(mood="urgent", energy="build", tempo="driving, allegro", tempo_bpm=108,
        instrumentation="staccato strings, frame drum",
        tags=["urgent", "journey", "drive", "ostinato", "momentum", "travel", "propulsive", "narrative-only"],
        use_cases=["the-road", "journey", "pursuit"],
        prompt="driving cinematic strings, light rhythmic staccato ostinato, forward momentum and travel, a determined journey, propulsive but orchestral, taut frame-drum pulse, driving allegro"),
    "urgent_call_rising": dict(mood="urgent", energy="build", tempo="urgent, allegro", tempo_bpm=100,
        instrumentation="layered strings",
        tags=["urgent", "call", "rising", "decision", "insistent", "resolve", "summons", "narrative-only"],
        use_cases=["call-to-follow", "decision"],
        prompt="rising cinematic urgency, accelerating layered strings building insistently, a summons, a moment of decision, mounting resolve to a decisive hit, orchestral, urgent allegro"),
    # --- NEUTRAL / exposition (panel-flagged gap: the Point beat + long-form teaching) ---
    "neutral_teaching_warm": dict(mood="neutral", energy="low", tempo="gentle, andante", tempo_bpm=66,
        instrumentation="soft strings, light piano",
        tags=["neutral", "underscore", "exposition", "teaching", "calm", "understated", "point"],
        use_cases=["point", "exposition", "long-form-connective"],
        prompt="Understated cinematic underscore, calm and neutral; soft warm strings and gentle piano, low-key; steady and unobtrusive with room for a narrator, no big melody; instrumental only, no vocals, no choir, no drums"),
    "neutral_teaching_low": dict(mood="neutral", energy="low", tempo="larghetto", tempo_bpm=None,
        instrumentation="low pad, subtle strings",
        tags=["neutral", "underscore", "ambient", "teaching", "background", "minimal", "long-form"],
        use_cases=["long-form-teaching", "connective", "exposition"],
        prompt="minimal ambient underscore, soft low strings and a subtle warm pad, very understated background bed, neutral and calm, leaves space for a speaking voice, no melody hooks, no drums, larghetto"),
}

# pilot subset: prove the generate->trim->duck loop on these first (test-gate discipline)
PILOT_SLUGS = ["sacred_grace_rise", "lonely_searching", "neutral_teaching_warm", "glory_holy_stillness"]


def beats_for_mood(mood: str) -> list[str]:
    return [b for b, allowed in BEAT_ALLOWED.items() if mood in allowed]
