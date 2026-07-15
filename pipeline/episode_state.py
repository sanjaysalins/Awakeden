"""pipeline/episode_state.py — the EPISODE: a long + its derived shorts, tracked
as ONE unit of work (the Furgiven pattern the user asked for, 2026-07-15).

An episode's identity IS the long's own manifest slug — no new id to invent or
keep in sync. A short belongs to an episode by carrying `parent: <long-slug>`
(the hard link from v2/RELEASE_SYNC.md). Episodes are DETECTED, never
hand-declared: a long becomes visible as an episode the moment its first short
sets `parent:` to it — "Isaiah 53 becomes an episode as it grows shorts" (the
user's own framing), never before. Standalone shorts with no `parent:` (I AM
Sayings, Parables, Miracles, Questions Jesus Asked, ...) are NOT episodes and
are not forced into this shape — they keep their existing per-piece tracking.

Consumed by production_board.py (the roll-up section) and
build_upload_tracker.py (grouping a release as one campaign: the long, then
its shorts, together — matching the release-calendar cadence memory)."""
from __future__ import annotations

from dataclasses import dataclass, field

from pipeline.release_state import PieceState

_SHIPPED = {"studio_complete", "live"}


@dataclass
class EpisodeState:
    slug: str                       # = the long's manifest slug
    long: PieceState
    shorts: list = field(default_factory=list)   # list[PieceState], by cluster_order

    @property
    def title(self) -> str:
        return self.long.title

    @property
    def shorts_total(self) -> int:
        return len(self.shorts)

    @property
    def shorts_built(self) -> int:
        return sum(1 for s in self.shorts if s.finality.startswith("FINAL"))

    @property
    def shorts_started(self) -> int:
        """Not built yet, but not sitting untouched either (status has moved
        off 'planned') — the signal 'shorts building' needs to be honest:
        without this, a short nobody has queued reads the same as one
        mid-pipeline (red-team 2026-07-15)."""
        return sum(1 for s in self.shorts
                   if s.status != "planned" and not s.finality.startswith("FINAL"))

    @property
    def shorts_posted(self) -> int:
        """Fully posted = live on every platform a short targets."""
        return sum(1 for s in self.shorts
                   if s.ledger and all(p in s.ledger for p in s.post_platforms))

    @property
    def shorts_posted_any(self) -> int:
        """At least one platform live — real progress the 24-48h cross-post
        lag (the CANON in build_upload_tracker.py) would otherwise hide behind
        a 0% bar for days after a genuine YouTube post."""
        return sum(1 for s in self.shorts if s.ledger)

    @property
    def long_posted(self) -> bool:
        return bool(self.long.youtube_id)

    @property
    def long_ready(self) -> bool:
        """Built + catalogue-approved (status studio_complete/live) — the human
        gate that decides a piece may go out, not just that ffmpeg finished."""
        return self.long.status in _SHIPPED and self.long.finality.startswith("FINAL")

    @property
    def status(self) -> str:
        """One word for the roll-up: where this unit of work stands. Must agree
        with `long_ready` (production_board.py and build_upload_tracker.py both
        read this episode's state and must never contradict each other — a
        confirmed live bug, 2026-07-15: the board said "ready to release" while
        the tracker correctly said "not yet marked ready" for the SAME episode,
        because status here checked bare `finality` instead of `long_ready`)."""
        if self.long_posted and not self.long.finality.startswith("FINAL"):
            # posted once, then the final vanished/regressed (a wave-rebuild
            # clobber) — never silently downgrade a LIVE piece to "in production"
            return "long LIVE but its final video is missing/changed — investigate"
        if not self.long_ready:
            if self.long.finality.startswith("FINAL"):
                return "long built, awaiting catalogue approval"
            return "long in production"
        if not self.shorts_total:
            return "long done, no shorts yet"
        if self.shorts_built < self.shorts_total:
            if self.shorts_started:
                return f"shorts building ({self.shorts_built}/{self.shorts_total})"
            return f"shorts planned, none started ({self.shorts_built}/{self.shorts_total})"
        if not self.long_posted and not self.shorts_posted_any:
            return "built, ready to release"
        if self.long_posted and self.shorts_posted == self.shorts_total:
            return "COMPLETE — fully released"
        return (f"releasing ({self.shorts_posted}/{self.shorts_total} shorts fully posted, "
                f"{self.shorts_posted_any}/{self.shorts_total} posted somewhere)")

    @property
    def is_complete(self) -> bool:
        return self.status.startswith("COMPLETE")


def gather_episodes(states: list[PieceState]) -> list[EpisodeState]:
    """Every long that has at least one parent-linked short — detected, not declared."""
    by_slug = {s.slug: s for s in states}
    shorts_by_parent: dict[str, list[PieceState]] = {}
    for s in states:
        if s.kind == "short" and s.parent:
            shorts_by_parent.setdefault(s.parent, []).append(s)

    episodes = []
    for parent_slug, shorts in shorts_by_parent.items():
        long = by_slug.get(parent_slug)
        if long is None or long.kind != "long":
            continue  # SYNC-G7 already flags this as a real defect elsewhere
        shorts.sort(key=lambda s: (s.cluster_order if s.cluster_order is not None else 99, s.slug))
        episodes.append(EpisodeState(slug=parent_slug, long=long, shorts=shorts))
    episodes.sort(key=lambda e: e.title)
    return episodes


def standalone_shorts(states: list[PieceState]) -> list[PieceState]:
    """Shorts with no parent long — not episodes, kept as their existing series-grouped view."""
    return [s for s in states if s.kind == "short" and not s.parent]
