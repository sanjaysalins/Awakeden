# mapengine — $0 deterministic animated Bible-map clips

Turn a Bible journey (Exodus, Abraham's call, Paul's voyages…) into a 16:9
animated map clip: an inked parchment base map + a progressively-drawn route
with a **walking caravan** marker, place-label pop-ins, a gentle push-in camera,
and an optional **sea-parting** beat — all deterministic ($0, no morphing).

## Why this shape (locked lessons)

- **Keep ALL text OFF the seedream image.** Labels are drawn deterministically by
  `mapengine.py`. Any baked-in map text would be garbled by Kling and is hard for
  seedream too. (Same rule as `feedback-never-animate-writing`.)
- **The route is drawn deterministically, not by Kling.** A generative model morphs
  lines/coastlines/labels. PIL+ffmpeg draw a crisp, pin-perfect route. (Bake-off
  proved pure-Kling can only give a *living map texture*, never the route itself.)
- **Sea-parting is masked to real water.** A teal water-mask built from the base map
  confines the parted corridor to the actual channel so it never spills onto desert.

## Files

- `render_base_map.py` — seedream_v4_5 ink base map (`--prompt` = the region). No text.
- `mapengine.py` — the engine: route + labels + caravan + sea-parting + camera → mp4.
- `caravan.py` — the hand-inked walking-caravan sprite (camel + rider + followers).
- `route.example.json` — the Exodus route (Egypt → Canaan) with a sea-parting event.

## Run

```
# 1. base map (edit --prompt for a different region)
<venv>\python.exe mapengine\render_base_map.py --out work\base_map.png

# 2. plot waypoints: open base_map.png, read off normalized coords into a route.json
#    (copy route.example.json and edit)

# 3. animate
<venv>\python.exe mapengine\mapengine.py --base work\base_map.png \
      --route work\route.json --out work\journey.mp4
```

## route.json schema

```json
{
  "title": "THE EXODUS",
  "subtitle": "from Egypt  to  the Promised Land",
  "config": {
    "caravan_scale": 1.5, "travel_s": 8.0, "camera_zoom": 0.05,
    "camera": {
      "lead_frames": 10,
      "keyframes": [
        { "at": 0.0,         "zoom": 1.0, "cx": 0.5, "cy": 0.5, "hold_s": 0.5 },
        { "at": "RAMESES",   "zoom": 1.6, "hold_s": 0.8 },
        { "at": 1.0,         "zoom": 1.0, "cx": 0.5, "cy": 0.5 }
      ]
    }
  },
  "waypoints": [
    { "name": "RAMESES", "x": 0.30, "y": 0.82, "label_dx": 0, "label_dy": 0.055 },
    { "name": "RED SEA CROSSING", "x": 0.60, "y": 0.72, "label_dy": -0.055,
      "sea_parting": { "cx": 0.645, "cy": 0.79, "length": 0.40, "gap": 0.045 } },
    { "name": "CANAAN", "x": 0.76, "y": 0.30, "label_dx": 0.03 }
  ]
}
```

- `x,y,label_dx,label_dy` are fractions of the frame (0..1).
- `config` is optional (see `DEFAULTS` in `mapengine.py`): `fps`, `travel_s`,
  `dwell_s`, `intro_s`, `outro_s`, `caravan_scale`, `marker` ("caravan" or "boat" —
  boat is a small bobbing ink hull+sail for a sea crossing, no legs to animate),
  `camera_zoom`, `camera`.
- `sea_parting` on any waypoint opens a dry corridor through the water on the leg
  to the NEXT waypoint: `cx,cy` = centre on the water, `gap` = corridor width,
  `length` = how far it runs (all fractions of frame height; masked to real water).
- `camera` (optional — the "Voyage Camera") replaces the flat `camera_zoom`
  single-centroid push-in with a traveling keyframe camera: wide establishing ->
  push to a waypoint -> hold -> glide to the next -> ... -> wide outro. Log-space
  zoom interpolation + the engine's shared smootherstep `ease()` + each keyframe
  arriving `lead_frames` early (camera parks at the payoff before the route/marker
  gets there). `at` = a waypoint name or a bare 0..1 progress fraction; the first
  and last keyframes are always the clip's literal first/last frame (bookends).
  Omit `camera` entirely and the old behaviour runs unchanged — see `.claude/skills/map/SKILL.md`
  for the full field reference.
