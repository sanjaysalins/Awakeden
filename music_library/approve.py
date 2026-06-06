"""Audition gate: mark an ingested take selectable (approved) or drop it (rejected).
Tracks stay status=pending — and thus unselectable — until you approve them here.

  python approve.py sacred_grace_rise_a --url https://suno.com/song/xxxx
  python approve.py sacred_grace_rise_b --reject --notes "stealth aah vocals"
  python approve.py --list            # show all tracks + status
"""
import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from music_library import MusicLibrary  # noqa: E402


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("slug", nargs="?", help="track slug, e.g. sacred_grace_rise_a")
    ap.add_argument("--url", default="", help="Suno export/share URL (provenance)")
    ap.add_argument("--swell", type=float, default=None,
                    help="climax/swell time in seconds (the placer aligns this to the CTA)")
    ap.add_argument("--reject", action="store_true")
    ap.add_argument("--notes", default="")
    ap.add_argument("--force", action="store_true", help="approve even if a sibling take is approved")
    ap.add_argument("--list", action="store_true")
    args = ap.parse_args()

    lib = MusicLibrary()
    if args.list or not args.slug:
        for e in sorted(lib.entries, key=lambda x: (x.mood, x.slug)):
            print(f"  {e.status:<9} {e.slug:<30} {e.mood:<10} "
                  f"{(str(e.lufs_i) + ' LUFS') if e.lufs_i is not None else '':<12} {e.qc_notes}")
        if not lib.entries:
            print("  (library empty — ingest some Suno takes first)")
        return

    e = lib.by_slug(args.slug)
    if not e:
        sys.exit(f"no such track: {args.slug} (run --list)")
    if args.reject:
        lib.reject(args.slug, notes=args.notes)
        print(f"[reject ] {args.slug}  {args.notes}")
        return

    # one primary approved take per base slug (codex flag)
    sib = lib.approved_sibling(args.slug)
    if sib and not args.force:
        sys.exit(f"[blocked] sibling take '{sib.slug}' already approved for this bed. "
                 f"Reject it first, or pass --force to keep both.")
    # swell timestamp is required for arc beds (build/climax) — the placer needs it
    if args.swell is None and e.energy in ("build", "climax", "swell-and-rest"):
        print("  QC checklist before approving an ARC bed: no lyric vocals · no stray drums "
              "(unless tension/urgent/triumphant) · midrange not muddy under voice.")
        sys.exit(f"[need-swell] '{args.slug}' is an arc bed (energy={e.energy}); pass "
                 f"--swell <seconds> (the climax time) so the placer can align it to the CTA.")
    lib.approve(args.slug, suno_url=args.url, notes=args.notes, swell_s=args.swell)
    sw = f"swell={args.swell}s" if args.swell is not None else ""
    print(f"[approve] {args.slug}  now SELECTABLE  {sw}  {('url=' + args.url) if args.url else ''}")


if __name__ == "__main__":
    main()
