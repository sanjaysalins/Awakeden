"""The swirls-of-life series' own lightweight upload tracker -- separate from
the main engine's upload_tracker.py/production_board.py, which are wired to
the 76-episode catalogue (_website/manifest.yaml) that swirls episodes are
NOT part of (user's own call, 2026-08-25, asked for rather than assumed).

AUTOMATED (2026-08-25, user: "why dont you update it for swirl life episodes"
-> confirmed they meant "wire it into the pipeline, not a manual step"):
episodes are auto-discovered by scanning for an `episode.py` (the unified
production-file convention swirls_episode.py itself already uses) and
importing its own MANIFEST for the canonical final-video path + FRONT_COVER
for the real title -- no hardcoded per-episode registry to maintain for any
episode built this way. swirls_episode.py's own cmd_assemble() calls
build_srt.build() + this module's build() automatically after a clean
assemble, so a newly-locked episode's .srt and tracker entry appear with no
separate manual step.

The ONE pre-episode.py legacy piece (the pilot, built before this convention
existed) is kept in a small hardcoded LEGACY list since it has no MANIFEST to
introspect -- new episodes never need an entry added here by hand.

Scans each episode folder for its real deliverables (final video, the
SFX-mixed version, the timestamped .srt -- see feedback_swirls_no_burned_captions:
no burned-caption file is expected here by design) and renders one simple
HTML board. Posted-URL status is the one thing that can't be detected from
disk, so it's tracked in a small JSON ledger next to this script, written
only via --set (mirrors upload_tracker.py's own "one write path" rule).

Run:
  .venv\\Scripts\\python.exe poc_living_water_ink_style_test\\swirls_upload_tracker.py
  .venv\\Scripts\\python.exe poc_living_water_ink_style_test\\swirls_upload_tracker.py --set <folder_name> youtube https://...
"""
from __future__ import annotations

import importlib.util
import json
import sys
from datetime import date
from pathlib import Path

HERE = Path(__file__).resolve().parent
LEDGER = HERE / "_swirls_release_ledger.json"
BOARD = HERE / "_SWIRLS_UPLOAD_TRACKER.html"

# Pre-episode.py legacy pieces only -- built via one-off scripts
# (assemble_pilot.py) before the unified episode.py/swirls_episode.py
# convention existed. Every episode built the modern way is auto-discovered
# below and never needs an entry here.
LEGACY = [
    ("Jacob's Ladder (pilot)", "swirls_pilot_01_jacobs_ladder", "THE_LADDER_BOOK_final.mp4"),
]


def _load_episode_module(folder: Path):
    spec = importlib.util.spec_from_file_location(f"episode_{folder.name}", folder / "episode.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def discover() -> list[tuple[str, str, Path | None]]:
    """(title, folder_name, final_video_path_or_None) for every episode.py-based
    episode found, by actually importing its own locked MANIFEST/FRONT_COVER --
    not by guessing filenames."""
    found = []
    for folder in sorted(HERE.glob("swirls_*")):
        if not (folder / "episode.py").is_file():
            continue
        try:
            mod = _load_episode_module(folder)
            title = getattr(mod, "FRONT_COVER", None)
            title = title.title if title is not None else folder.name
            variant = next(iter(mod.MANIFEST.scores.values()), None)
            final = variant.out if variant is not None else None
        except Exception as e:
            print(f"  !! could not introspect {folder.name}/episode.py: {e}")
            title, final = folder.name, None
        found.append((title, folder.name, final))
    return found


def load_ledger() -> dict:
    if LEDGER.exists():
        return json.loads(LEDGER.read_text(encoding="utf-8"))
    return {}


def save_ledger(d: dict) -> None:
    LEDGER.write_text(json.dumps(d, indent=2), encoding="utf-8")


def scan(folder: Path, final: Path | None) -> dict:
    sfx_path = None
    if final is not None:
        sfx_path = final.with_name(final.name.replace(".mp4", "_sfx.mp4"))
        sfx_path = sfx_path if sfx_path.is_file() else None
    # SRT filename isn't standardized across every episode (episode 1's own
    # first SRT predates the shared build_srt.py's folder-name convention) --
    # glob for any .srt at top level instead of assuming a fixed name.
    srt_matches = sorted(folder.glob("*.srt"))
    srt_path = srt_matches[0] if srt_matches else None
    return {
        "final": final if (final is not None and final.is_file()) else None,
        "sfx": sfx_path,
        "srt": srt_path,
    }


def esc(s: str) -> str:
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def build() -> None:
    ledger = load_ledger()
    episodes = [(title, slug, HERE / slug / final_name) for title, slug, final_name in LEGACY]
    episodes += discover()

    cards = []
    for title, slug, final in episodes:
        folder = HERE / slug
        info = scan(folder, final)
        posted = ledger.get(slug, {})

        def pill(ok, label):
            # only show what's actually there -- a missing SFX bed (etc.) on an
            # older episode isn't a defect to flag, just not done, so omit
            # rather than render a red "no" (user, 2026-08-25).
            if not ok:
                return ""
            return f'<span class="pill good">{label}</span>'

        links = []
        if info["final"]:
            links.append(f'<a href="file:///{info["final"].resolve().as_posix()}">final video</a>')
        if info["sfx"]:
            links.append(f'<a href="file:///{info["sfx"].resolve().as_posix()}">sfx version</a>')
        if info["srt"]:
            links.append(f'<a href="file:///{info["srt"].resolve().as_posix()}">captions.srt</a>')
        links_html = " &middot; ".join(links) if links else "<i>nothing rendered yet</i>"

        if posted:
            posted_html = "<br>".join(
                f'{esc(plat)}: <a href="{esc(url)}">{esc(url)}</a> ({when})'
                for plat, (url, when) in posted.items())
        else:
            posted_html = "<i>not posted anywhere yet</i>"

        cards.append(f"""
<div class="card">
  <h2>{esc(title)}</h2>
  <div class="pills">
    {pill(info['final'], 'final video')}
    {pill(info['sfx'], 'sfx bed')}
    {pill(info['srt'], 'timestamped captions')}
  </div>
  <div class="links">{links_html}</div>
  <div class="posted"><span class="label">Posted</span><br>{posted_html}</div>
</div>""")

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Swirls Upload Tracker</title>
<style>
  body {{ font-family: Verdana, Arial, sans-serif; background: #faf7f0; color: #222;
         max-width: 720px; margin: 40px auto; padding: 0 20px; line-height: 1.5; }}
  h1 {{ font-size: 26px; color: #7a4a12; margin-bottom: 4px; }}
  .sub {{ color: #666; font-size: 15px; margin-bottom: 24px; }}
  .card {{ background: #fff; border: 1px solid #e2d9c8; border-radius: 12px;
          padding: 18px 22px; margin-bottom: 16px; }}
  h2 {{ font-size: 18px; color: #7a4a12; margin: 0 0 10px; }}
  .pills {{ margin-bottom: 10px; }}
  .pill {{ display: inline-block; font-size: 12px; padding: 3px 9px; border-radius: 10px;
          font-weight: bold; margin-right: 6px; margin-bottom: 4px; }}
  .pill.good {{ background: #d9f0d9; color: #1a5c1a; }}
  .links {{ font-size: 14px; margin-bottom: 10px; }}
  .links a {{ color: #2a5aa0; }}
  .posted {{ font-size: 13px; color: #555; background: #f7f4ec; border-radius: 8px; padding: 8px 12px; }}
  .label {{ font-size: 11px; color: #888; text-transform: uppercase; letter-spacing: .04em; }}
</style>
</head>
<body>

<h1>Swirls of Life — Upload Tracker</h1>
<div class="sub">Separate from the main catalogue tracker &mdash; just this POC series' own episodes. Auto-refreshed after every clean assemble.</div>

{"".join(cards)}

</body>
</html>
"""
    BOARD.write_text(html, encoding="utf-8")
    print(f"[ok] {BOARD}")


def set_posted(slug: str, platform: str, url: str) -> None:
    ledger = load_ledger()
    ledger.setdefault(slug, {})[platform] = [url, date.today().isoformat()]
    save_ledger(ledger)
    print(f"[ok] recorded {slug} / {platform} -> {url}")


if __name__ == "__main__":
    if len(sys.argv) >= 2 and sys.argv[1] == "--set":
        _, _, slug, platform, url = sys.argv
        set_posted(slug, platform, url)
    build()
