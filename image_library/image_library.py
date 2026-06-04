"""image_library — a central, reusable pool of generated Baroque stills.

Same idea as sound_library (and a 16:9 sibling to the 9:16 hero-stills `_library`):
generate a still ONCE, tag it, and pull it into other narrations instead of re-paying.

Reuse discipline (the LOCKED topical-fit gate, memory `feedback-topical-fit-gate`):
- `reuse_scope:"neutral"` — thread-neutral plates (wilderness, dawn, tomb, lamb, sheep,
  storm sky, AND gospel images of Christ/cross/risen) → may be pulled into ANY narration.
- `reuse_scope:"specific"` — story-bound stills (a specific character's marred face, the
  Ethiopian's chariot, a named trial scene) → reuse ONLY within the same thread.

Layout:
  image_library/
    stills/<slug>.png      cached image
    index.json             manifest (one entry per still)

API mirrors sound_library:
  lib = ImageLibrary()
  hit = lib.find(tags=["wilderness","dawn"], aspect="16:9")   # -> entry or None
  lib.register(ImageEntry(...))      lib.import_file(src_png, slug=..., ...)
  lib.by_slug(slug)   lib.still_path(slug)   lib.note_use(slug, episode)
"""
from __future__ import annotations

import json
import shutil
from dataclasses import dataclass, asdict, field
from pathlib import Path

LIB_ROOT = Path(__file__).resolve().parent
STILLS_DIR = LIB_ROOT / "stills"
INDEX = LIB_ROOT / "index.json"


@dataclass
class ImageEntry:
    slug: str
    aspect: str                   # "16:9" | "9:16"
    tags: list[str]
    subject: str                  # the subject_block / description
    reuse_scope: str = "neutral"  # "neutral" (any narration) | "specific" (same thread only)
    jesus_variant: str | None = None   # ministry | passion | resurrection | None
    style: str = "baroque-oil"
    source: str = "nbp"           # nbp | hf | kling
    source_episode: str = ""
    created: str = ""             # YYYY-MM-DD (pass in)
    used_in: list[str] = field(default_factory=list)


class ImageLibrary:
    def __init__(self) -> None:
        STILLS_DIR.mkdir(parents=True, exist_ok=True)
        self.entries: list[ImageEntry] = []
        if INDEX.exists():
            for d in json.loads(INDEX.read_text(encoding="utf-8")):
                self.entries.append(ImageEntry(**d))

    def by_slug(self, slug: str) -> ImageEntry | None:
        return next((e for e in self.entries if e.slug == slug), None)

    def still_path(self, slug: str) -> Path:
        return STILLS_DIR / f"{slug}.png"

    def find(self, tags: list[str], aspect: str | None = None,
             scope: str | None = None, require_all: bool = False) -> ImageEntry | None:
        """Best tag-overlap match. scope=None returns any; pass 'neutral' to restrict
        to cross-narration-safe plates. require_all => every tag must be present."""
        want = {t.lower() for t in tags}
        best, best_score = None, 0
        for e in self.entries:
            if aspect and e.aspect != aspect:
                continue
            if scope and e.reuse_scope != scope:
                continue
            have = {t.lower() for t in e.tags}
            if require_all and not want.issubset(have):
                continue
            score = len(want & have)
            if score > best_score:
                best, best_score = e, score
        return best if best_score > 0 else None

    def register(self, entry: ImageEntry) -> ImageEntry:
        existing = self.by_slug(entry.slug)
        if existing:
            self.entries.remove(existing)
        self.entries.append(entry)
        self._save()
        return entry

    def import_file(self, src: Path, **kw) -> ImageEntry:
        entry = ImageEntry(**kw)
        dst = self.still_path(entry.slug)
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
    lib = ImageLibrary()
    print(f"image library: {len(lib.entries)} still(s) at {LIB_ROOT}")
    for e in lib.entries:
        print(f"  {e.slug:<34} {e.aspect:<5} {e.reuse_scope:<8} [{','.join(e.tags[:5])}]")
