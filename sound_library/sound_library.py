"""sound_library — a central, reusable pool of generated SFX / ambience clips.

Same idea as the hero-stills library: generate a sound ONCE, tag it, and reuse it
across episodes (long-form AND short-form) instead of re-paying ElevenLabs every time.

Layout:
  sound_library/
    clips/<slug>.mp3          the cached audio
    index.json                manifest (one entry per clip)

Reuse discipline (mirrors the topical-fit gate for stills): environmental sounds
(wind, thunder, sea, rain, crowd, footsteps, birds, road) are `reuse_scope:"neutral"`
and may be pulled into ANY episode. Story-specific cues are `reuse_scope:"specific"`
and should only be reused inside the same thread.

API:
  lib = SoundLibrary()
  hit = lib.find(tags=["wind","desert"], category="ambience")   # -> entry or None
  path = lib.clip_path(slug)                                     # -> Path
  lib.register(slug, prompt, duration_s, category, tags, ...)    # add an existing file
  lib.import_file(src_mp3, slug, ...)                            # copy a file in + register
"""
from __future__ import annotations

import json
import shutil
from dataclasses import dataclass, asdict, field
from pathlib import Path

LIB_ROOT = Path(__file__).resolve().parent
CLIPS_DIR = LIB_ROOT / "clips"
INDEX = LIB_ROOT / "index.json"


@dataclass
class SoundEntry:
    slug: str
    category: str                 # "ambience" | "oneshot"
    tags: list[str]
    prompt: str
    duration_s: float
    loopable: bool = False
    raw_mean_db: float | None = None
    raw_max_db: float | None = None
    source: str = "elevenlabs:sound-generation"
    credits_est: int = 0
    reuse_scope: str = "neutral"  # "neutral" (any episode) | "specific"
    created: str = ""             # YYYY-MM-DD (pass in; no Date.now in this env)
    used_in: list[str] = field(default_factory=list)


class SoundLibrary:
    def __init__(self) -> None:
        CLIPS_DIR.mkdir(parents=True, exist_ok=True)
        self.entries: list[SoundEntry] = []
        if INDEX.exists():
            for d in json.loads(INDEX.read_text(encoding="utf-8")):
                self.entries.append(SoundEntry(**d))

    # ---- lookup ----------------------------------------------------------
    def by_slug(self, slug: str) -> SoundEntry | None:
        return next((e for e in self.entries if e.slug == slug), None)

    def clip_path(self, slug: str) -> Path:
        return CLIPS_DIR / f"{slug}.mp3"

    def find(self, tags: list[str], category: str | None = None,
             require_all: bool = False) -> SoundEntry | None:
        """Best tag-overlap match. require_all => every tag must be present."""
        want = {t.lower() for t in tags}
        best, best_score = None, 0
        for e in self.entries:
            if category and e.category != category:
                continue
            have = {t.lower() for t in e.tags}
            if require_all and not want.issubset(have):
                continue
            score = len(want & have)
            if score > best_score:
                best, best_score = e, score
        return best if best_score > 0 else None

    # ---- write -----------------------------------------------------------
    def register(self, entry: SoundEntry) -> SoundEntry:
        existing = self.by_slug(entry.slug)
        if existing:
            self.entries.remove(existing)
        self.entries.append(entry)
        self._save()
        return entry

    def import_file(self, src: Path, **kw) -> SoundEntry:
        """Copy an existing mp3 into the library and register it. kw -> SoundEntry."""
        entry = SoundEntry(**kw)
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
    lib = SoundLibrary()
    print(f"sound library: {len(lib.entries)} clip(s) at {LIB_ROOT}")
    for e in lib.entries:
        print(f"  {e.slug:<28} {e.category:<9} [{','.join(e.tags)}]  {e.duration_s}s  scope={e.reuse_scope}")
