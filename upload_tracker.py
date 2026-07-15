#!/usr/bin/env python
"""upload_tracker.py — THE one write path for "this video is posted".

You paste the URL after each upload; this records a DATED entry per platform in
`data/release_ledger.json` (url + posted date + the sha of the final that went
up), and for YouTube also writes `youtube_id` + `public_status: live` into
`_website/manifest.yaml` and rebuilds the read pages (the piece's page gains the
red "Watch the film" button). It NEVER uploads or deploys — after a batch of
--set calls, publish the _website folder the usual way, then run
release_check.py (the SYNC gate reads this ledger).

  .venv\\Scripts\\python.exe upload_tracker.py --list
  .venv\\Scripts\\python.exe upload_tracker.py --set sign-of-jonah youtube https://youtube.com/shorts/AbCdEf12345
  .venv\\Scripts\\python.exe upload_tracker.py --set sign-of-jonah tiktok https://www.tiktok.com/@awakeden/video/123...
  .venv\\Scripts\\python.exe upload_tracker.py --set it-is-finished https://youtu.be/XyZ...   (platform omitted = youtube)
"""
from __future__ import annotations

import datetime as _dt
import re
import subprocess
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
MANIFEST = ROOT / "_website" / "manifest.yaml"

from pipeline import finality, release_state  # noqa: E402

PLATFORMS = release_state.PLATFORMS  # youtube, tiktok, facebook, instagram


def video_id(url: str) -> str:
    """Accept full watch URLs, youtu.be, shorts links, or a bare 11-char id."""
    u = url.strip()
    if re.fullmatch(r"[A-Za-z0-9_-]{11}", u):
        return u
    for pat in (r"[?&]v=([A-Za-z0-9_-]{11})",
                r"youtu\.be/([A-Za-z0-9_-]{11})",
                r"/shorts/([A-Za-z0-9_-]{11})",
                r"/live/([A-Za-z0-9_-]{11})",
                r"/embed/([A-Za-z0-9_-]{11})"):
        m = re.search(pat, u)
        if m:
            return m.group(1)
    raise SystemExit(f"could not parse a YouTube video id from: {url}")


def _set(slug: str, platform: str, url: str, *, repost: bool) -> None:
    # re-read the manifest at the last moment — the user co-edits it live, and a
    # stale in-memory copy would clobber his edits on the dump (red-team M1)
    m = yaml.safe_load(MANIFEST.read_text(encoding="utf-8"))
    items = m["items"]
    hits = [it for it in items if it["slug"] == slug]
    if not hits:
        near = [it["slug"] for it in items if slug.split("-")[0] in it["slug"]]
        raise SystemExit(f"unknown slug '{slug}'. Close matches: {near}")
    if platform not in PLATFORMS:
        raise SystemExit(f"unknown platform '{platform}'. One of: {PLATFORMS}")
    if not url.strip().lower().startswith("http") and not (
            platform == "youtube" and re.fullmatch(r"[A-Za-z0-9_-]{11}", url.strip())):
        raise SystemExit(f"'{url}' does not look like a URL - paste the full link")
    it = hits[0]

    entry = {"url": url.strip(), "posted": _dt.date.today().isoformat()}
    src, _join = release_state.resolve_source(it)
    if src:
        _status, video = finality.final_video(src)
        if video:
            entry["final_sha"] = finality.content_sha(video)
            entry["video_file"] = video.name
    if "final_sha" not in entry:
        print(f"  WARN: no final video found for {slug} - recording WITHOUT a sha "
              "(divergence will be undetectable for this post)")
    if platform == "youtube":
        entry["video_id"] = video_id(url)

    ledger = release_state.load_ledger()
    old = ledger.setdefault(slug, {}).get(platform)
    if old:
        same = (old.get("url") == entry["url"]
                and old.get("final_sha") == entry.get("final_sha"))
        if same:
            entry["posted"] = old.get("posted", entry["posted"])  # idempotent re-paste
        elif not repost:
            # replacing a differing entry silently would launder the SYNC-G6
            # posted-sha FAIL without any re-post (red-team M2/C4)
            raise SystemExit(
                f"{slug} · {platform} is already recorded: {old.get('url')} "
                f"({old.get('posted')}).\nIf you really re-posted the video, re-run "
                "with --repost. The gate FAIL you may be seeing means the FILE "
                "changed after posting - pasting the same URL again does not fix that.")
    ledger[slug][platform] = entry
    release_state.save_ledger(ledger)
    print(f"{slug} · {platform}: {entry['url']} ({entry['posted']})"
          + (f"  [replaced {old.get('url', '?')}]" if old and not old.get("url") == entry["url"] else ""))

    if platform == "youtube":
        was = it.get("youtube_id")
        it["youtube_id"] = entry["video_id"]
        it["public_status"] = "live"
        release_state.atomic_write(
            MANIFEST, yaml.safe_dump(m, sort_keys=False, allow_unicode=True))
        print(f"  manifest: youtube_id = {entry['video_id']}"
              + (f" (was {was})" if was else "") + " · status -> live")
        print("  rebuilding read pages ...")
        try:
            subprocess.run([sys.executable, str(ROOT / "_website" / "build_readpage.py"),
                            "--html-only"], check=True)
        except subprocess.CalledProcessError as e:
            raise SystemExit(
                "  ledger + manifest are SAVED, but the read-page rebuild FAILED "
                f"(exit {e.returncode}).\n  Re-run: .venv\\Scripts\\python.exe "
                "_website\\build_readpage.py --html-only BEFORE deploying _website.")
        print("  done - deploy _website when the batch is finished, then run release_check.py")


def main() -> int:
    argv = [a for a in sys.argv[1:] if a != "--repost"]
    repost = "--repost" in sys.argv

    if "--set" in argv:
        i = argv.index("--set")
        rest = argv[i + 1:]
        if len(rest) == 2 and rest[1].lower() in PLATFORMS:
            raise SystemExit(f"missing the URL: --set {rest[0]} {rest[1]} <url>")
        if len(rest) == 2:                      # back-compat: --set <slug> <yt-url>
            slug, platform, url = rest[0], "youtube", rest[1]
        elif len(rest) == 3:
            slug, platform, url = rest[0], rest[1].lower(), rest[2]
        else:
            raise SystemExit("usage: --set <slug> [youtube|tiktok|facebook|instagram] <url> [--repost]")
        _set(slug, platform, url, repost=repost)

    m = yaml.safe_load(MANIFEST.read_text(encoding="utf-8"))
    items = m["items"]

    ledger = release_state.load_ledger()
    live = [it for it in items if it.get("youtube_id")]
    ready = [it for it in items if not it.get("youtube_id")
             and it.get("public_status") == "studio_complete"]

    def row(it: dict) -> str:
        cells = []
        for p in PLATFORMS:
            e = ledger.get(it["slug"], {}).get(p)
            cells.append(f"{p[:2].upper()} {e['posted']}" if e else f"{p[:2].lower()} -")
        return "  ".join(cells)

    print(f"\nPUBLISHED ({len(live)}):")
    for it in live:
        print(f"  {it['slug']:36} https://youtu.be/{it['youtube_id']}")
        print(f"  {'':36} {row(it)}")
    print(f"READY, NOT YET UPLOADED ({len(ready)}):")
    for it in ready:
        print(f"  {it['slug']:36} {row(it)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
