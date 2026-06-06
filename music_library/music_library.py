"""music_library — a central, reusable pool of MUSIC beds (Suno-generated).

Sibling to sound_library (SFX/ambience) and image_library (stills). Music is the
MOST reusable asset of all: a "reverent build" or "somber lament" bed is not story-
specific, so one good track serves many clips across shorts AND long-form.

Cost model: tracks are generated on the user's flat-rate Suno subscription (NOT
metered ElevenLabs credits). Generate a curated catalogue ONCE, tag it, reuse forever.

Layout:
  music_library/
    _inbox/                  drop raw Suno downloads here, named <slug>.mp3 (or <slug>_a/_b)
    clips/<slug>.mp3         the ingested, registered track
    index.json               manifest (one entry per track)
    CATALOGUE.md             the 20-track design spec (AI-panel reviewed)

Selection discipline: pick by emotional ARC, not just genre. Each clip's narration is
forced-aligned, so the chosen track's natural build can be timed (in-point) to land on
the gospel pivot, then trimmed + ducked under the voice downstream.

API:
  lib = MusicLibrary()
  hit = lib.find(tags=["reverent","build"], mood="sacred")   # -> entry or None
  path = lib.clip_path(slug)
  lib.register(MusicEntry(...))
  lib.import_file(src_mp3, slug=..., ...)
"""
from __future__ import annotations

import json
import shutil
from dataclasses import dataclass, asdict, field
from pathlib import Path

LIB_ROOT = Path(__file__).resolve().parent
CLIPS_DIR = LIB_ROOT / "clips"
INBOX_DIR = LIB_ROOT / "_inbox"
INDEX = LIB_ROOT / "index.json"


@dataclass
class MusicEntry:
    slug: str
    mood: str                       # sacred|lonely|tender|awe|triumphant|lament|tension|glory|pastoral|urgent|neutral
    energy: str                     # "low" | "build" | "climax" | "swell-and-rest"
    tags: list[str]
    prompt: str                     # the Suno prompt used
    duration_s: float
    tempo_bpm: int | None = None
    instrumentation: str = ""        # e.g. "strings, piano, duduk"
    has_vocals: bool = False         # wordless pads ok; lyric vocals = True (avoid for beds)
    use_cases: list[str] = field(default_factory=list)  # which beats/episode types
    raw_mean_db: float | None = None  # dBFS (ffmpeg volumedetect), NOT LUFS
    raw_max_db: float | None = None   # dBFS
    lufs_i: float | None = None       # integrated loudness (EBU R128) for narration-safe gain
    swell_s: float | None = None      # the track's climax/swell time (s), logged at approval;
                                      # the placer aligns this to the CTA timestamp (arc beds)
    # --- QC: a track is NOT selectable until a human audition marks it approved -------
    status: str = "pending"           # "pending" | "approved" | "rejected"
    qc_notes: str = ""                # e.g. "stealth vocals", "drum kit", "muddy midrange"
    # --- license provenance (commercial use != copyright protection) ------------------
    source: str = "suno"
    license: str = "suno-paid-commercial"
    suno_url: str = ""                # export/share URL for provenance
    reuse_scope: str = "neutral"      # music is almost always neutral
    created: str = ""                 # YYYY-MM-DD (pass in; no Date.now in this env)
    used_in: list[str] = field(default_factory=list)


class MusicLibrary:
    def __init__(self) -> None:
        CLIPS_DIR.mkdir(parents=True, exist_ok=True)
        INBOX_DIR.mkdir(parents=True, exist_ok=True)
        self.entries: list[MusicEntry] = []
        if INDEX.exists():
            for d in json.loads(INDEX.read_text(encoding="utf-8")):
                self.entries.append(MusicEntry(**d))

    # ---- lookup ----------------------------------------------------------
    def by_slug(self, slug: str) -> MusicEntry | None:
        return next((e for e in self.entries if e.slug == slug), None)

    def clip_path(self, slug: str) -> Path:
        return CLIPS_DIR / f"{slug}.mp3"

    def find(self, tags: list[str] | None = None, mood: str | None = None,
             energy: str | None = None, require_all: bool = False,
             include_pending: bool = False) -> MusicEntry | None:
        """Best match by mood (hard filter if given) then tag-overlap.
        Only APPROVED tracks are selectable unless include_pending=True (audition gate)."""
        want = {t.lower() for t in (tags or [])}
        best, best_score = None, -1
        for e in self.entries:
            if not include_pending and e.status != "approved":
                continue
            if mood and e.mood != mood:
                continue
            if energy and e.energy != energy:
                continue
            have = {t.lower() for t in e.tags} | {e.mood, e.energy}
            if require_all and not want.issubset(have):
                continue
            score = len(want & have)
            if score > best_score:
                best, best_score = e, score
        return best if best is not None else None

    def find_for_beat(self, beat: str, tags: list[str] | None = None) -> MusicEntry | None:
        """Doctrine-safe PRIMARY-bed selection for a Gospel-Five-Beat beat.
        - hard-filters to BEAT_ALLOWED moods (no tension/urgent/lonely/lament on conviction/landing)
        - excludes LAYER_ONLY_MOODS (glory pads are layers, never the primary bed)
        - prefers a bed whose energy fits the beat (BEAT_PREFERRED_ENERGY)
        - only approved tracks are selectable."""
        from _specs import BEAT_ALLOWED, LAYER_ONLY_MOODS, BEAT_PREFERRED_ENERGY
        allowed = BEAT_ALLOWED.get(beat)
        if allowed is None:
            raise ValueError(f"unknown beat {beat!r}; expected one of {list(BEAT_ALLOWED)}")
        allowed = allowed - LAYER_ONLY_MOODS
        pref_energy = BEAT_PREFERRED_ENERGY.get(beat, set())
        want = {t.lower() for t in (tags or [])}
        best, best_score = None, -1.0
        for e in self.entries:
            if e.status != "approved" or e.mood not in allowed:
                continue
            score = len({t.lower() for t in e.tags} & want)
            if e.energy in pref_energy:      # energy-fit bonus (claude flag)
                score += 1.5
            if score > best_score:
                best, best_score = e, score
        return best

    def find_layer(self, tags: list[str] | None = None) -> MusicEntry | None:
        """Pick an approved LAYER pad (glory_*) to sit UNDER a primary melodic bed.
        The only safe way to add a second musical element without the 'two music' clash."""
        from _specs import LAYER_ONLY_MOODS
        want = {t.lower() for t in (tags or [])}
        best, best_score = None, -1
        for e in self.entries:
            if e.status != "approved" or e.mood not in LAYER_ONLY_MOODS:
                continue
            score = len({t.lower() for t in e.tags} & want)
            if score > best_score:
                best, best_score = e, score
        return best

    def base_slug(self, slug: str) -> str:
        """sacred_grace_rise_a -> sacred_grace_rise (strip the take suffix)."""
        import re
        return re.sub(r"_[a-z]$", "", slug)

    def approved_sibling(self, slug: str) -> "MusicEntry | None":
        """An already-approved take of the SAME base (enforces one primary per base slug)."""
        base = self.base_slug(slug)
        return next((e for e in self.entries
                     if e.slug != slug and e.status == "approved"
                     and self.base_slug(e.slug) == base), None)

    def all_by_mood(self, mood: str) -> list[MusicEntry]:
        return [e for e in self.entries if e.mood == mood]

    def approve(self, slug: str, suno_url: str = "", notes: str = "",
                swell_s: float | None = None) -> None:
        e = self.by_slug(slug)
        if e:
            e.status = "approved"
            if suno_url:
                e.suno_url = suno_url
            if notes:
                e.qc_notes = notes
            if swell_s is not None:
                e.swell_s = swell_s
            self._save()

    def reject(self, slug: str, notes: str = "") -> None:
        e = self.by_slug(slug)
        if e:
            e.status, e.qc_notes = "rejected", notes
            self._save()

    # ---- write -----------------------------------------------------------
    def register(self, entry: MusicEntry) -> MusicEntry:
        existing = self.by_slug(entry.slug)
        if existing:
            self.entries.remove(existing)
        self.entries.append(entry)
        self._save()
        return entry

    def import_file(self, src: Path, **kw) -> MusicEntry:
        entry = MusicEntry(**kw)
        dst = self.clip_path(entry.slug)
        if Path(src).resolve() != dst.resolve():
            shutil.copy2(src, dst)
        return self.register(entry)

    def note_use(self, slug: str, episode: str) -> None:
        e = self.by_slug(slug)
        if e and episode not in e.used_in:
            e.used_in.append(episode)
            self._save()

    def _save(self) -> None:
        INDEX.write_text(
            json.dumps([asdict(e) for e in self.entries], indent=2, ensure_ascii=False),
            encoding="utf-8")


if __name__ == "__main__":
    lib = MusicLibrary()
    print(f"music library: {len(lib.entries)} track(s) at {LIB_ROOT}")
    for e in sorted(lib.entries, key=lambda x: x.mood):
        v = "VOX" if e.has_vocals else "inst"
        print(f"  {e.slug:<26} {e.mood:<10} {e.energy:<14} {v}  {e.duration_s:>5.0f}s  [{','.join(e.tags)}]")
