"""Shared episode resolver for the long-form 16:9 pipeline.

Makes the long-form drivers EPISODE-GENERIC. Before this, every driver hardcoded
`01_Isaiah_53_Suffering_Servant` plus per-scene tables (MOTION / BANK / JESUS /
DIRECTIONAL). Now the per-episode data lives in that episode's
`visual_16x9/scene_plan.json` and the drivers resolve the episode from argv.

scene_plan.json schema (per-episode config):
  top level:  format · episode (title) · audio · image_provider · animation ·
              style_base · style_tail · film_name · rule · scenes[]
  per scene:  id · mvt · t:[start,end] · title · subject_block ·
              camera (the move) · atmos (atmosphere drift) · sfx ·
              jesus_variant (null|passion|resurrection|...) · directional (bool) ·
              bank ({slug,scope,tags}|null — central image_library banking)

Usage in a driver:
    import sys
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from _episode import resolve
    ep = resolve(sys.argv)            # bare = Isaiah (back-compat); else pass a slug/dir
    for s in ep.scenes: ...
"""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LONGFORM = ROOT / "longform"
DEFAULT_SLUG = "01_Isaiah_53_Suffering_Servant"


def slugof(t):
    return re.sub(r"[^a-z0-9]+", "_", str(t).lower()).strip("_")[:40]


class Episode:
    def __init__(self, v1: Path):
        self.v1 = Path(v1)
        self.slug = self.v1.parent.name           # e.g. 02_Psalm_22_Song_From_The_Cross
        self.out = self.v1 / "visual_16x9"
        self.scene_plan_path = self.out / "scene_plan.json"
        self._plan = None

    # ---- plan / scenes -------------------------------------------------------
    @property
    def plan(self):
        if self._plan is None:
            if not self.scene_plan_path.is_file():
                raise SystemExit(
                    f"no scene_plan.json for episode {self.slug}:\n  {self.scene_plan_path}\n"
                    f"author the 16:9 scene plan first (see the Isaiah 53 plan as the template).")
            self._plan = json.loads(self.scene_plan_path.read_text(encoding="utf-8"))
        return self._plan

    @property
    def scenes(self):
        return self.plan["scenes"]

    @property
    def title(self):
        # don't REQUIRE a plan; ignore a placeholder that's just the folder slug
        ep = self.plan.get("episode") if self.scene_plan_path.is_file() else None
        if ep and ep != self.slug:
            return ep
        return re.sub(r"^\d+_", "", self.slug).replace("_", " ")

    def save_plan(self):
        self.scene_plan_path.write_text(
            json.dumps(self.plan, ensure_ascii=False, indent=2), encoding="utf-8")

    # ---- per-scene artifact paths -------------------------------------------
    def stem(self, s):
        return f"{s['id']:02d}_{slugof(s['title'])}"

    def png(self, s):
        return self.out / f"{self.stem(s)}.png"

    def mp4(self, s):
        return self.out / f"{self.stem(s)}.mp4"

    # ---- audio / film output -------------------------------------------------
    def audio(self, prefer_immersive=True):
        imm = self.v1 / "narration.immersive.mp3"
        if prefer_immersive and imm.exists():
            return imm
        return self.v1 / "narration.mp3"

    @property
    def film_out(self):
        # prefer an explicit film_name from the plan, but don't REQUIRE a plan to exist
        # (so the output path is knowable before the scene plan is authored)
        name = None
        if self.scene_plan_path.is_file():
            name = self.plan.get("film_name")
        if not name:
            base = re.sub(r"^\d+_", "", self.slug)   # drop leading NN_ ordinal
            name = f"{base}_16x9.mp4"
        return self.out / name

    # ---- style ---------------------------------------------------------------
    @property
    def style_base(self):
        return self.plan.get("style_base", "")

    @property
    def style_tail(self):
        return self.plan.get("style_tail",
                             "no text, no modern elements, cinematic 16:9 widescreen composition")


def resolve(argv, default_slug=DEFAULT_SLUG) -> Episode:
    """Resolve an Episode from argv. Accepts (first non-flag arg):
       a v1 dir · an episode dir/slug · or nothing (defaults to Isaiah for back-compat)."""
    arg = next((a for a in argv[1:] if not a.startswith("-")), None)
    if arg is None:
        return Episode(LONGFORM / default_slug / "v1")
    p = Path(arg)
    if not p.is_absolute() and not p.exists():
        cand = LONGFORM / arg                       # treat as a slug under longform/
        if cand.exists():
            p = cand
    if p.name == "v1":
        return Episode(p)
    if (p / "v1").exists():
        return Episode(p / "v1")
    return Episode(p)                               # assume it already points at a v1-like dir
