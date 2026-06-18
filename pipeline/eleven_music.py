"""ELEVEN MUSIC — a reusable RECIPE collection (Phase 2/0 of the fix-all plan).

Why recipes, not baked mp3s: the per-short Eleven scores are pivot-timed one-offs (their swell
lands on THAT short's CTA), so the audio can't be reused elsewhere. What IS reusable is the
RECIPE — {lens, mood, beat, prompt, mix directive, model_id} — REGENERATED on demand at the new
short's exact length via the Eleven API (the user-preferred automation). The baked mp3 stays as
per-render provenance, never the reuse source.

Design (round-2 review + user): a THIN Eleven schema in its own store (`eleven_music/recipes.json`),
sharing ONLY the doctrine gate (`BEAT_ALLOWED`) with the Suno `music_library/` so there is ONE
doctrine source of truth and no drift. Selection is its own lane (never mixes Suno + Eleven).

Lifecycle: ingest (proposed) -> human classifies lens->(mood,beat) + auditions by ear -> approve ->
find_for_beat returns only APPROVED + doctrine-allowed recipes -> regenerate_for(folder).

Run:
  .venv\\Scripts\\python.exe -m pipeline.eleven_music ingest      # seed proposals from music_designs.json
  .venv\\Scripts\\python.exe -m pipeline.eleven_music approve <slug> --mood lament --beat hook
  .venv\\Scripts\\python.exe -m pipeline.eleven_music find <beat> [--lens Minimalist-Ambient]
  .venv\\Scripts\\python.exe -m pipeline.eleven_music list
"""
from __future__ import annotations
import json
import re
import sys
from dataclasses import dataclass, field, asdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
STORE = ROOT / "eleven_music"
INDEX = STORE / "recipes.json"
DESIGNS = ROOT / "v2" / "coherence_audit" / "music_designs.json"

# The LOCKED mix directive (the standard for every Eleven score) — carried ON the recipe so it
# is data, not a hardcoded constant that can disagree across tools.
LOCKED_DIRECTIVE = {"gain_db": -8.0, "outro_s": 2.5, "duck_threshold": 0.12, "duck_ratio": 2.5,
                    "model_id": "music_v1"}


LENSES = ("Minimalist-Ambient", "Cinematic-Redemptive")


def _doctrine() -> tuple[dict, set]:
    """Import the SHARED doctrine tables from the Suno library's _specs (ONE source of truth)."""
    sys.path.insert(0, str(ROOT / "music_library"))
    import _specs  # noqa
    return dict(_specs.BEAT_ALLOWED), set(getattr(_specs, "LAYER_ONLY_MOODS", set()))


def beat_allowed() -> dict:
    """The raw shared BEAT_ALLOWED table (no second, drifting copy)."""
    return _doctrine()[0]


def allowed_primary(beat: str) -> set:
    """Moods that may lead a PRIMARY bed at this beat = BEAT_ALLOWED[beat] MINUS layer-only moods
    (full parity with music_library.find_for_beat, which also subtracts LAYER_ONLY_MOODS)."""
    ba, layer = _doctrine()
    return ba.get(beat, set()) - layer


@dataclass
class ElevenRecipe:
    slug: str
    title: str = ""
    lens: str = ""                      # Minimalist-Ambient | Cinematic-Redemptive
    mood: str = ""                      # from the shared _specs mood vocab (assigned at approval)
    beat: str = ""                      # hook|point|proof|conviction|landing (assigned at approval)
    prompt: str = ""                    # the Eleven /v1/music prompt (the reusable recipe core)
    gain_db: float = -8.0
    outro_s: float = 2.5
    duck_threshold: float = 0.12
    duck_ratio: float = 2.5
    model_id: str = "music_v1"
    status: str = "proposed"            # proposed | approved
    provenance: str = ""                # the short it was first generated for
    notes: str = ""

    def directive(self) -> dict:
        return {"gain_db": self.gain_db, "outro_s": self.outro_s,
                "duck_threshold": self.duck_threshold, "duck_ratio": self.duck_ratio,
                "model_id": self.model_id}


def load() -> list[dict]:
    if not INDEX.exists():
        return []
    try:
        return json.loads(INDEX.read_text(encoding="utf-8")).get("recipes", [])
    except (OSError, ValueError):
        return []


def save(recipes: list[dict]) -> None:
    STORE.mkdir(exist_ok=True)
    INDEX.write_text(json.dumps({"_README": "Reusable Eleven-Music RECIPES (regenerate-on-demand, "
                                 "not baked mp3s). Shared doctrine gate with music_library/_specs. "
                                 "Selectable only when status=approved AND mood allowed for the beat.",
                                 "recipes": recipes}, indent=2, ensure_ascii=False), encoding="utf-8")


def add_recipe(rec: ElevenRecipe) -> dict:
    recipes = load()
    d = asdict(rec)
    recipes = [r for r in recipes if r.get("slug") != rec.slug] + [d]   # upsert by slug
    save(recipes)
    return d


def approve(slug: str, mood: str, beat: str, notes: str = "") -> dict:
    """Human classification + approval: assign the doctrine-vocab mood + the beat, mark approved.
    Fail-closed: refuses an unknown beat, an out-of-doctrine mood (incl. layer-only), a bad lens,
    or an EMPTY prompt (the prompt is the entire reusable payload — never approve/spend on a blank)."""
    ba = beat_allowed()
    if beat not in ba:
        raise ValueError(f"unknown beat {beat!r}; one of {list(ba)}")
    prim = allowed_primary(beat)
    if mood not in prim:
        raise ValueError(f"mood {mood!r} not doctrine-allowed for a PRIMARY bed at beat {beat!r} "
                         f"(allowed: {sorted(prim)})")
    recipes = load()
    for r in recipes:
        if r.get("slug") == slug:
            if not (r.get("prompt") or "").strip():
                raise ValueError(f"recipe {slug!r} has an empty prompt — nothing to regenerate; refusing")
            if r.get("lens") and r["lens"] not in LENSES:
                raise ValueError(f"recipe {slug!r} has an unknown lens {r['lens']!r}; one of {LENSES}")
            r.update(mood=mood, beat=beat, status="approved", notes=notes or r.get("notes", ""))
            save(recipes)
            return r
    raise KeyError(f"no recipe {slug!r}")


def find_for_beat(beat: str, lens: str | None = None) -> dict | None:
    """Return the best APPROVED recipe whose mood is doctrine-allowed for this beat (and lens if
    given). Eleven lane only — never returns a Suno bed. None if no doctrine-clean match."""
    allowed = allowed_primary(beat)            # subtracts LAYER_ONLY_MOODS — full parity with the Suno lib
    cands = [r for r in load()
             if r.get("status") == "approved" and r.get("mood") in allowed
             and (lens is None or lens.lower() in (r.get("lens", "").lower()))]
    if not cands:
        return None
    # prefer a recipe authored for this very beat, then any approved match
    cands.sort(key=lambda r: (r.get("beat") != beat, r.get("title", "")))
    return cands[0]


def ingest_designs() -> list[str]:
    """Seed PROPOSED recipes from the briefs in music_designs.json (all 11 have a baked score on
    disk = provenance). mood/beat are left blank (the briefs carry only a lens + free-text why) —
    a human must classify + approve before they are selectable (the doctrine gate needs a real
    mood/beat). Slugs are made UNIQUE (the 48-char truncation can otherwise collide + upsert-drop)."""
    if not DESIGNS.exists():
        return []
    designs = json.loads(DESIGNS.read_text(encoding="utf-8"))
    out, used = [], set()
    for d in designs:
        title = d.get("title", "")
        folder = d.get("folder", "")
        has_mp3 = bool(folder) and (Path(folder) / "assembly" / "music.mp3").exists()
        lens = (d.get("winner_lens", "") or "").split("(")[0].strip()
        base = re.sub(r"[^a-z0-9]+", "-", f"{title}_{lens}".lower()).strip("-")[:48]
        slug = base
        i = 2
        while slug in used:                    # guarantee uniqueness despite truncation
            slug = f"{base[:45]}-{i}"
            i += 1
        used.add(slug)
        add_recipe(ElevenRecipe(slug=slug, title=title, lens=lens, prompt=d.get("best_prompt", ""),
                                provenance=title, status="proposed",
                                notes=("baked mp3 on disk (provenance)" if has_mp3 else "recipe only"),
                                **LOCKED_DIRECTIVE))
        out.append(slug)
    return out


def regenerate_for(v1_folder, slug: str, script: str | None = None, yes: bool = False):
    """Reuse path: pull a recipe, regenerate a fresh score at THIS short's length via the Eleven
    API, mix at the recipe's locked directive. (METERED.) Delegates to sfx_pilots.add_music.build_one.

    PRECONDITION: <v1_folder>/assembly/viral_cut_sfx.mp4 MUST exist — build_one mixes the score
    UNDER that finished SFX cut and times the score to its duration. Without it build_one returns
    falsy; we check + raise here so the failure is loud, not a silent no-op."""
    rec = next((r for r in load() if r.get("slug") == slug), None)
    if not rec:
        raise KeyError(f"no recipe {slug!r}")
    if not (rec.get("prompt") or "").strip():
        raise ValueError(f"recipe {slug!r} has an empty prompt — refusing to call the metered API")
    cut = Path(v1_folder) / "assembly" / "viral_cut_sfx.mp4"
    if not cut.exists():
        raise FileNotFoundError(f"{cut} missing — build the SFX cut first (regenerate_for mixes the "
                                "score UNDER it + times the score to its length)")
    sys.path.insert(0, str(ROOT))
    from sfx_pilots.add_music import build_one  # noqa
    return build_one(str(v1_folder), rec["prompt"], gain=rec.get("gain_db", -8.0),
                     script=script, yes=yes, regen=True, outro=rec.get("outro_s", 2.5))


if __name__ == "__main__":
    a = [x for x in sys.argv[1:] if not x.startswith("--")]
    opt = {sys.argv[i]: sys.argv[i + 1] for i in range(len(sys.argv) - 1) if sys.argv[i].startswith("--")}
    if a and a[0] == "ingest":
        slugs = ingest_designs()
        print(f"ingested {len(slugs)} PROPOSED recipes (classify + approve before use):")
        for s in slugs:
            print(f"  {s}")
        raise SystemExit(0)
    if len(a) >= 2 and a[0] == "approve":
        r = approve(a[1], opt.get("--mood", ""), opt.get("--beat", ""), opt.get("--notes", ""))
        print(f"approved {r['slug']} -> mood={r['mood']} beat={r['beat']}")
        raise SystemExit(0)
    if len(a) >= 2 and a[0] == "find":
        r = find_for_beat(a[1], lens=opt.get("--lens"))
        print(f"best for beat '{a[1]}': {r['slug'] if r else 'NONE (no approved doctrine-clean recipe)'}")
        raise SystemExit(0)
    if a and a[0] == "list":
        for r in load():
            print(f"  [{r['status']:>8}] {r['slug']:46} lens={r.get('lens','?')[:20]:20} "
                  f"mood={r.get('mood') or '-':10} beat={r.get('beat') or '-'}")
        raise SystemExit(0)
    if len(a) >= 3 and a[0] == "regen":
        # METERED: regenerate a recipe's score at <folder>'s length + mix at the locked directive
        ok = regenerate_for(a[1], a[2], script=opt.get("--script"), yes="--yes" in sys.argv)
        print(f"regen {'ok' if ok else 'FAILED'} for {a[2]} -> {a[1]}")
        raise SystemExit(0 if ok else 1)
    print("usage: eleven_music ingest | approve <slug> --mood <m> --beat <b> | find <beat> [--lens L] "
          "| list | regen <v1 folder> <slug> [--script <spoken.txt>] --yes")
