#!/usr/bin/env python
"""upload_tracker.py — record uploaded YouTube URLs and push them to the website.

You paste the URL after each upload; this writes the youtube_id into
`_website/manifest.yaml`, rebuilds the read pages (the piece's page gains a red
"Watch the film" button that opens the video in a modal popup), and shows the
running published/pending tally. It NEVER uploads or deploys — after a batch of
--set calls, publish the _website folder the usual way.

  .venv\\Scripts\\python.exe upload_tracker.py --list
  .venv\\Scripts\\python.exe upload_tracker.py --set sign-of-jonah https://youtube.com/shorts/AbCdEf12345
  .venv\\Scripts\\python.exe upload_tracker.py --set it-is-finished https://youtu.be/XyZ...
"""
from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent
MANIFEST = ROOT / "_website" / "manifest.yaml"


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


def main() -> int:
    m = yaml.safe_load(MANIFEST.read_text(encoding="utf-8"))
    items = m["items"]

    if "--set" in sys.argv:
        i = sys.argv.index("--set")
        slug, url = sys.argv[i + 1], sys.argv[i + 2]
        hits = [it for it in items if it["slug"] == slug]
        if not hits:
            near = [it["slug"] for it in items if slug.split("-")[0] in it["slug"]]
            raise SystemExit(f"unknown slug '{slug}'. Close matches: {near}")
        vid = video_id(url)
        old = hits[0].get("youtube_id")
        hits[0]["youtube_id"] = vid
        hits[0]["public_status"] = "live"
        yaml.safe_dump(m, MANIFEST.open("w", encoding="utf-8"),
                       sort_keys=False, allow_unicode=True)
        print(f"{slug}: youtube_id = {vid}" + (f" (was {old})" if old else "") + " · status -> live")
        print("rebuilding read pages ...")
        subprocess.run([sys.executable, str(ROOT / "_website" / "build_readpage.py"),
                        "--html-only"], check=True)
        print("done - deploy _website when the batch is finished.")

    live = [it for it in items if it.get("youtube_id")]
    ready = [it for it in items if not it.get("youtube_id")
             and it.get("public_status") == "studio_complete"]
    print(f"\nPUBLISHED ({len(live)}):")
    for it in live:
        print(f"  {it['slug']:36} https://youtu.be/{it['youtube_id']}")
    print(f"READY, NOT YET UPLOADED ({len(ready)}):")
    for it in ready:
        print(f"  {it['slug']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
