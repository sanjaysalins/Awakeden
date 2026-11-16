# Graphic-comic motion kit: build notes (Thief film test copy v1)

Output: `F:\slk\PycharmProjects\JesusInTheBible\poc_comic_page\_ELEVATE\arms\TP_S32_COMIC_v1.mp4` (1080x1920, 30 fps, 1140 frames = 38.000 s, shipped audio stream copied bit-for-bit).
Shipped film was only READ. Nothing committed. $0 (no paid tools). Headless render only.

## What was built
Kit (Remotion, typed, data-driven) in `F:\slk\PycharmProjects\JesusInTheBible\_remotion\src\comic_kit\`:
- `core.tsx` - shared values, easing (glide / settle / slam), seeded wobble, `ink_stroke`, `boil`, `anchor` data types, `guard` (violation check), episode types.
- `layouts.tsx` - `page` (paper + Ben-Day dots), `panel`, `inset_panel`, `splash_border`, panel state machine (panel_slam, panel_dive, pull_out_to_page, panel_join, page_settle, page_glide camera), `anchorScreen` (the `anchor` push maths), `ShotVideo`.
- `transitions.tsx` - whip_pan, slam_cut, speed_zoom, ink_slash_split (hook), halftone_dissolve (radial / rise), page_flip_up, border_fall, punch_cut, ink_bleed, iris, gutter_wipe. panel_shatter lives in `doodles.tsx` (`PanelShatter`).
- `doodles.tsx` - ink_splat, shock_lines, border_build, pill_edge (spiky / dashed), shout_fan, speed_lines (radial / focus / parallel), drops, motion_ticks, jolt, crosshatch_shade, halftone_vignette, rays (soft / burst), crack_lines.
- `pagemoves.tsx` - gutter_shift + the split page used by ink_slash_split. (panel_join and page_settle are Move kinds in `layouts.tsx`.)
- `ComicFilm.tsx` - generic renderer: episode.json -> scenes, transitions, doodles, pills. `index.ts` re-exports.
- `F:\slk\PycharmProjects\JesusInTheBible\_remotion\src\ThiefComic.tsx` - the film (thin wrapper). Root.tsx: one import + one `<Composition id="ThiefComic">` line added, nothing else touched.

Python helpers in `F:\slk\PycharmProjects\JesusInTheBible\poc_comic_page\_ELEVATE\formula\build\`:
`prep_assets.py` (pre-loops clips to 30 fps into `_remotion/public/comic_thief/`, exports pill + hook PNGs with the shipped code `build_w3.pill_tabs` / `build_tp.light_text`, hook moved to y 200), `geo.py` (same push maths as the kit), `build_thief.py` (writes `thief_episode.json`: beats, clips, devices, hand-keyed anchors), `gates_comic.py`, `contacts.py`, `sheet.py`, `gridview.py`, `frames.cjs` (headless still renders).

## Render a new episode
1. Put its clips in `_remotion/public/<assets>/` (30 fps, looped >= 13 s: see `prep_assets.clips`), pills/hook PNGs in `<assets>/pills/`.
2. Write an `episode.json` (copy `thief_episode.json`: scenes with panels/moves, transitions between scene ids, doodles with `at`/`until`/`pos`, `no_draw` masks, `pills`).
3. `cd F:\slk\PycharmProjects\JesusInTheBible\_remotion` then
   `npx remotion render src/index.ts ThiefComic out/X_silent.mp4 --props=<episode props json> --muted --concurrency=2 --crf=12 --jpeg-quality=95 --pixel-format=yuv420p`
   (props file = `{"episode": <episode.json>}`; add a new `<Composition>` with its own frame count if the length differs).
4. Mux: `ffmpeg -i X_silent.mp4 -i <shipped final> -map 0:v -map 1:a -c copy -t <len> out.mp4`.
5. Marks-only pass for gates: props `{"episode":..., "marks":true, "hideKinds":["pill_edge"]}` renders doodles + transition marks as white on black (no pictures, fast); then `gates_comic.py`.

## Owner decisions applied
- `answer_light_profile` (f796-882) kept, nothing drawn: punch_cut in, iris out with no ring (a ring would cross his face). Cards 12 and 13 (crack, shatter, bleed, burst) are NOT used; those devices exist in the kit.
- Jesus' line f674-796: borders fall (border_fall), then only the static splash border. The pixels of that window come from the shipped film itself (see gaps).
- Gutter wipe at 31.93 s replaced by a second page_flip_up: the wipe bar would sweep across the risen Jesus face panel.

## Gate results
Final run (`gates_result.json`, `gates_out.txt`):
```
PASS G1 duration - video 38.000 s (1140 frames) audio 38.000 s 1080,1920,30/1
PASS G2 audio identical - shipped MD5=dc03d5c2394dbfccddd36c96eb595d61 | comic MD5=dc03d5c2394dbfccddd36c96eb595d61
PASS G3a stillness vs shipped (f674-796) - mean abs diff 1.81 (max 2.01), limit 2.0, over 123 frames
PASS G5 variety - sequence: panel_slam > panel_slam > panel_slam > panel_dive > whip_pan > page_glide > slam_cut > speed_zoom > ink_slash_split > halftone_dissolve > page_flip_up > pull_out_to_page > border_fall > punch_cut > iris > page_flip_up > halftone_dissolve | repeats-in-a-row [] | >2 uses {}
PASS G8 word sync (never early) - 10 word-tied frames checked; early: none
PASS G9 anchor (mocker mouth, 5 frames) - max error 0.01 px vs hand-keyed shipped-film points (keys are by-eye, about +/-15 px)
PASS G3b stillness: no overlay f674-796 - max mark pixels 0
PASS G4 answer_light_profile clean f796-891 - max mark pixels 0 (comic transitions only into/out of it: punch_cut in, iris out with no ring)
PASS G6 pill zone free (pill_edge excluded = it IS the pill's edge) - max mark pixels in x70-1010,y974-1250 while a pill shows: 0 (frame 1058)
PASS G7 no-draw masks (Jesus faces / close-ups) - masks 5, violations none
ALL PASS
```
G3a passes at 1.81 only because the window's pixels are the shipped frames (re-encoded). G6 excludes pill_edge (it is the pill's own edge) and transition marks are clipped out of the pill zone in code.

Contact sheets: `contact_v1.jpg`, `old_vs_new.jpg` (same folder). Media in `_remotion/public/comic_thief/` and `_remotion/out/` must not be committed (no-media-to-GitHub rule); `shipped_ref.mp4` there is a read-only copy of the shipped film.

## Known gaps / not done
- 14 transitions drawn (spec 16): T13 panel_shatter and T14 ink_bleed dropped by the Option B decision; T16 gutter_wipe swapped out (face rule). All three are in the kit, unused.
- Stillness window uses shipped-film pixels (spliced inside Remotion): re-rendering the Jesus clip with CSS zoom differs from ffmpeg zoompan by about 6 mean grey levels (edge resampling), so the 2.0 limit cannot be met by re-rendering. The spec's own fallback was used.
- Anchors: mocker mouth/head are hand-keyed from shipped frames (OpenCV matchTemplate tracker is in `build_thief.track()` but lost the deforming mouth). Other anchors are analytic push maths (static picture points). Accuracy about +/-15 px by eye.
- Clip frame phase: 24 -> 30 fps duplication can differ by one frame from the shipped build.
- Boil on panel borders and marks is 2-set / 3-frame as spec; the motion feel is only judged from stills, not watched.
- panel_shatter, crack_lines, ink_bleed, rays burst, gutter_wipe, shock_lines variants are not exercised by this film (only compiled).
- Spec items not built: `guard` is a pixel gate (marks pass) plus a JS helper, not a live per-frame render blocker.

---
# v2: real comic PAGES (page system)

Output: `F:\slk\PycharmProjects\JesusInTheBible\poc_comic_page\_ELEVATE\arms\TP_S32_COMIC_v2.mp4` (same audio, 38.000 s). Data: `thief_episode_v2.json` (written by `build_thief_v2.py`). Contact sheet: `contact_v2.jpg`. v1 is untouched.

## Page system (comic_kit)
- `pages.ts` / `pages.py`: page layouts as data: `stack3`, `stack2`, `side2`, `big_2small`, `big_inset`, `splash`, `diag2` (diag2 = the `type:"split"` scene with `margin`). A scene may say `"layout":"stack2"` and leave panel boxes out; `normalizeEpisode()` fills them. The python mirror is needed because anchors need the boxes.
- Each panel is its own live clip with its own crop/push (`shot`: cx, cy, z0, z1). Bold-ink wobbled border + hard drop shadow + small tilt, on spec paper with dots.
- Reading moves (panel Move kinds in `layouts.tsx`): `panel_slam` (on a word frame), `panel_dive` (page panel grows to full-bleed), `panel_read` (dive in, hold, ease back to the page; kit only, not used in this film), `panel_join` (one panel hops onto another), `page_glide` (camera scroll), `pull_out_to_page`, `page_settle`. A growing panel is drawn on top of the others.
- Page turns are the scene transitions: whip_pan, slam_cut, speed_zoom, ink_slash_split, halftone_dissolve, page_flip_up, border_fall, punch_cut, iris.
- `SplitScene` got `margin` (diagonal-gutter page framed by paper, polygon borders). `halftone_vignette` got `rect` (dots only inside one panel). `shout_fan` got `inner`.

## How a new episode declares pages
In `episode.json` a scene is `{id, f0, f1, paper:true, layout:"stack2", panels:[{id, mount, shot:{clip,t_in,f_start,cx,cy,z0,z1,f_z0,f_z1}, tilt, filter}], moves:[{kind:"panel_slam", panel, at, shake}, {kind:"panel_dive", panel, at, frames}, ...]}`. `f0` = first frame the page is on screen; `mount` = first frame a panel is on screen (use a word frame = ceil(word_start*30) with a `panel_slam`). Link pages with `transitions:[{kind, from, to, at, frames}]` (the outgoing page stays alive to `at+frames`). Doodles anchor to a panel with `pos:{anchor:{scene,panel,pic:[x,y],track?}}`; `pic` is normalised picture coordinates, so marks follow the panel crop. Add `no_draw` boxes for every Jesus face panel. Render with `--props=out/thief_v2_props.json` (`{"episode": ...}`), no new Root line is needed.

## Page plan (v2)
A hook page, 4 panels (Jesus eyes, paradise, mocker, thief) then thief dives full-bleed on "Why?" (no marks) / B 2-stack: three crosses + a thief on his cross, dive into the crosses / C mocker big + penitent wide, shout fan, spiky pill / mocker face punch (speed_zoom, full-bleed) / D diagonal split page (ink slash, mocker fades out) / E prayer 2-stack: thief + Jesus listens, halftone hush on the thief panel only / F hope: kingdom rays + penitent + paradise slams on "Someday." / Jesus' line: single splash, still (shipped pixels) / answer_light_profile: clean splash / G Jesus + thief 2-stack, thief panel joins on "Him." / H "you": kneelers + the thief's prayer, dashed edge / dawn hold, border_build + page_settle.

## v2 fixes
- Thief-head spikes (shock crown at "Why?") removed. The mocker shout fan now points away from the head (arc -45..20 deg, inner 120 px).
- Tiny thief inset beside risen Jesus replaced by a proper 2-panel page (head-crop panel, joins on "Him.").

## Gates v2 (`gates_comic.py --v2`; G10 and G11 added)
See `gates_out_v2.txt`: G10 page coverage (2+ panels together) must be >= 60 % of runtime; G11 no duplicate clip on one page. Page-1 head panel and Jesus panels are in `no_draw`.

Known gaps v2: motion is judged from stills; Jesus' line window is still the shipped pixels; `panel_read` (in and back out) exists but is not used; three-panel stack (`stack3`) layout exists but no page uses it after the "nail" clip was dropped (it is a Jesus close-up, same subject as the centre cross).
