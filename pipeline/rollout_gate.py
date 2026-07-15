"""GOLD-MASTER ROLLOUT GATE (2026-07-14) - deterministic, $0, fail-closed.

Blocks a living-page short from the corpus rollout "done" state until its spec +
piece.json hit the gold-master bar set by women_first_witnesses_luke245 (user-approved
2026-07-13/14). Run at spec-authoring time - needs no build artifacts.

Usage:
  .venv\\Scripts\\python.exe -m pipeline.rollout_gate <piece_dir> [<piece_dir> ...]
Exit 0 = every piece PASS; exit 1 = any FAIL (each printed).
"""
import json
import sys
from collections import Counter
from pathlib import Path

FULLBLEED_MAX_PCT = 60        # gold master = 56%; "most beats grids, few full heroes"
MIN_TEMPLATES = 3             # template variety (quad/frac3/band3/stack_h/... + full)
MAX_STILL_USES = 2            # no still on more than 2 beats
MAX_FB_PAIRS = 2              # same-still full-bleed twice: only as an ADJACENT deliberate
                              # two-shot (gold master: women_bowed 10+11, landing 17+18)
FX_MIN_PCT = 50               # grade/rays arc on at least half the beats (gold = 83%)
MIN_LIVING_LIGHT = 2          # pinned by panel review 2026-07-14: default 2/piece, 3 by exception
ARC_COOL_MIN_K = 7000         # the arc needs a real cool pole...
ARC_LANDING_MAX_K = 5500      # ...and a landing that is genuinely warm (gold: 7900 -> 4900)
SLOP_TOKENS = (" - ", "...", "…", "—", "–", "â€")


def check_piece(piece_dir: Path) -> list[str]:
    """Return the list of FAIL reasons (empty = PASS)."""
    fails = []
    spec_p = piece_dir / "visual" / "livingpage_short.spec.json"
    pj_p = piece_dir / "piece.json"
    if not spec_p.is_file():
        return [f"no livingpage_short.spec.json (older format? migrate first)"]
    spec = json.loads(spec_p.read_text(encoding="utf-8"))
    beats = spec["beats"]

    if spec.get("motion") != "smooth":
        fails.append(f'motion={spec.get("motion", "classic")!r} - gold master is "smooth"')

    tpls = Counter(b["tpl"] for b in beats)
    full_pct = round(100 * tpls.get("full", 0) / len(beats))
    if full_pct > FULLBLEED_MAX_PCT:
        fails.append(f"fullbleed {full_pct}% > {FULLBLEED_MAX_PCT}% - convert beats to grids")
    if len(tpls) < MIN_TEMPLATES:
        fails.append(f"only {len(tpls)} template(s) {sorted(tpls)} - need >= {MIN_TEMPLATES}")

    uses = Counter(c["slug"] for b in beats for c in b["clips"])
    over = {s: n for s, n in uses.items() if n > MAX_STILL_USES}
    if over:
        fails.append(f"stills used > {MAX_STILL_USES}x: {over}")
    fb_beats = {}
    for i, b in enumerate(beats, 1):
        if b["tpl"] == "full":
            fb_beats.setdefault(b["clips"][0]["slug"], []).append(i)
    fb_pairs = {s: ix for s, ix in fb_beats.items() if len(ix) > 1}
    if len(fb_pairs) > MAX_FB_PAIRS:
        fails.append(f"{len(fb_pairs)} stills full-bleed twice (max {MAX_FB_PAIRS}): {fb_pairs}")
    for s, ix in fb_pairs.items():
        if len(ix) > 2 or ix[1] - ix[0] != 1:
            fails.append(f"full-bleed repeat {s} at beats {ix} - only an ADJACENT two-shot is allowed")

    fx_pct = round(100 * sum(1 for b in beats if b.get("fx")) / len(beats))
    if fx_pct < FX_MIN_PCT:
        fails.append(f"fx on {fx_pct}% of beats < {FX_MIN_PCT}% - author the cold->warm grade arc")
    # arc DIRECTION (panel 2026-07-14): presence is not an arc - need a cool pole and a
    # landing that is the warmest beat of the piece (lowest Kelvin)
    temps = [b["fx"]["temp"] for b in beats if (b.get("fx") or {}).get("temp")]
    last_temp = (beats[-1].get("fx") or {}).get("temp")
    if not temps:
        # rays-only fx could satisfy the % check with NO grade at all (panel round-2 flag)
        fails.append("no temp grade anywhere - the fx arc must carry colortemperature beats")
    else:
        if max(temps) < ARC_COOL_MIN_K:
            fails.append(f"grade arc flat: no cool pole >= {ARC_COOL_MIN_K}K (max {max(temps)}K)")
        if last_temp is None or last_temp != min(temps) or last_temp > ARC_LANDING_MAX_K:
            fails.append(f"grade arc: landing temp {last_temp}K must be the piece's warmest "
                         f"(lowest K) and <= {ARC_LANDING_MAX_K}K")
    if spec.get("cut_ticks"):
        fails.append("cut_ticks true - the gold master ships without per-cut tick SFX")
    # the spend meter charges a FLAT 7.5cr per clip, which is only true at 5s (panel
    # round-5 claude: a 10s anti-melt hold would silently halve the meter)
    if pj_p.is_file():
        dur = ((json.loads(pj_p.read_text(encoding="utf-8")).get("animate") or {})
               .get("duration", 5))
        if dur != 5:
            fails.append(f"animate.duration {dur} != 5 - the stop-loss meter is pinned to "
                         f"7.5cr per 5s clip; re-pin KLING_CR_PER_CLIP before rendering")

    slop = [i for i, b in enumerate(beats, 1)
            if (cp := b.get("cap")) and any(t in cp.get("text", "") for t in SLOP_TOKENS)]
    if slop:
        fails.append(f"dash/ellipsis/mojibake captions on beats {slop}")

    # living-light: at least one Kling-native lit clip, and the LANDING must carry light
    # (spec fx rays or a living_light clip) - every cut closes on Christ, lit.
    ll = {}
    ll_exc = None
    if pj_p.is_file():
        pj = json.loads(pj_p.read_text(encoding="utf-8"))
        ll = (pj.get("animate") or {}).get("living_light") or {}
        ll_exc = (pj.get("animate") or {}).get("living_light_exception")
    # user-granted exception (2026-07-15, father_forgive_them): a piece may ship with 1
    # living-light clip ONLY with an explicit, auditable grant - user + date + reason
    # (e.g. no second wound-free still; Kling regenerates blood on wound-marked palms,
    # memory living-light-no-fresh-blood). Never silent: malformed grants don't count.
    min_ll = MIN_LIVING_LIGHT
    if isinstance(ll_exc, dict) and ll_exc.get("user") and ll_exc.get("date") and ll_exc.get("reason"):
        min_ll = 1
    if len(ll) < min_ll:
        fails.append(f"{len(ll)} animate.living_light clip(s) < {min_ll} "
                     f"(default 2/piece: a reveal + the landing)")
    # double-lighting (panel convergent flag): a beat played by a living-light clip must
    # not ALSO carry the PIL rays overlay - Kling IS the light there
    for i, b in enumerate(beats, 1):
        if (b.get("fx") or {}).get("rays") and {c["slug"] for c in b["clips"]} & set(ll):
            fails.append(f"beat {i} double-lit: living_light clip AND fx.rays - drop the rays")
    # a living-light slug is WASTED MONEY unless some beat actually plays the Kling clip:
    # a clip-def with "cam" makes the builder use $0 dyncam and silently ignore the mp4
    for slug in ll:
        plays = [c for b in beats for c in b["clips"] if c["slug"] == slug]
        if not plays:
            fails.append(f"living_light[{slug}] paid but NO beat uses that slug")
        elif all(c.get("cam") for c in plays):
            fails.append(f"living_light[{slug}] paid but every beat plays it via dyncam "
                         f"(\"cam\" set) - the Kling clip never appears")
    last = beats[-1]
    last_slugs = {c["slug"] for c in last["clips"]}
    if not ((last.get("fx") or {}).get("rays") or last_slugs & set(ll)):
        fails.append("landing beat carries no light (no fx.rays and no living_light clip)")
    return fails


def main(argv) -> int:
    bad = 0
    for arg in argv:
        piece = Path(arg).resolve()
        fails = check_piece(piece)
        if fails:
            bad += 1
            print(f"FAIL {piece.name}")
            for f in fails:
                print(f"  - {f}")
        else:
            print(f"PASS {piece.name}")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
