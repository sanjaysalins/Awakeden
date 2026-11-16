# Doodle design: "Jesus Promised Paradise to a Criminal" (38 s short)

Design only. $0. Nothing built into the film yet. No project file changed.

## The call: ONE doodle, not two

I looked at all 14 shots. 11 are Jesus' face or a cross close-up (no-draw zone).
Only 3 shots are free: the storm light (shot 9), the two kneelers (shot 13), the garden (shot 14).
Only one of them passes every red-team rule. So this film gets **one** doodle. A second would be forced.

## The doodle: "He walks up to Him"

**In one line:** the man in the tan hood who knelt at the cross (shot 13) is inked in again, on the garden hill, walking up to Jesus (shot 14).

| Item | Value |
|---|---|
| Beat | The 3 s landing hold. No words. Last word "too." ends 34.66 s. |
| Shot | Shot 14, `paradise_dawn`, 35.00-38.00 s (t_in 0.0, cx .5, cy .5, z 1.05 to 1.25) |
| Draws | 35.60 to 36.85 s (1.25 s) |
| Holds | 36.85 to 38.00 s (1.15 s), fully still |
| Exit | None. The film ends on it. On loop it is gone again, which helps a re-watch. |
| Size | 0.075 of clip width x 0.092 of clip height (about 94 x 204 px on screen at 36.6 s) |
| Anchor (feet) | Source clip (x 0.457, y 0.426) at clip time 1.6 s. Sunlit grass, left of centre, below His feet. |
| Gap to Jesus | His feet are at about (0.50, 0.31). The doodle's head tops out at y 0.336. It never touches Him or His shadow at draw time. |

### What is drawn (stroke order)

Back view of a small hooded figure in a robe, mid-step, facing up the hill.

| # | Time (s) | Stroke | Width (px at 1080 wide) |
|---|---|---|---|
| 1 | 35.60-35.78 | Hood, one arc over the head | 6 |
| 2 | 35.78-36.05 | Left shoulder and back, down to the hem | 7 |
| 3 | 36.00-36.25 | Right shoulder and side, down to the hem | 6 |
| 4 | 36.25-36.40 | Wavy hem | 6 |
| 5 | 36.38-36.48 | Hood edge on the shoulders, short seam | 4 |
| 6 | 36.45-36.55 | Belt (the kneeler in shot 13 has the same belt) | 4 |
| 7 | 36.52-36.66 | Two robe folds, one sleeve line | 3 |
| 8 | 36.64-36.72 | Two heel marks under the hem | 5 |
| Fill | 36.30-36.70 | Flat tan wash rises from hem to hood | - |
| Shadow | 36.62-36.85 | One dry-brush shadow, down-left, same slant as the tree shadows | - |

- Speed: steady hand, linear. Each stroke eases out in its last 2 frames. No bounce, no pop.
- Ink: warm black `#14100C` (sampled from the art's own line).
- Fill: tan `#CDAC7C`, shade `#96703F`. This is the kneeler's robe colour (sampled (161,126,86) to (252,225,156)). It is darker than Jesus' white robe, so He stays the brightest thing.
- Shadow: `#14100A` at 45 percent.
- Line: uneven brush, 3 to 7 px, round caps. Match the cypress outlines, not a vector pen.
- No line-boil in the hold. The landing is still.
- The paths are in `doodle_mock.html` (SVG, origin 436,588 on the 1080x1920 frame at 36.6 s). The mock shape is a guide. For the real build, trace the hood and robe from the shot-13 kneeler so it is truly the same man.

### Why it earns its place

- The art already has it half-drawn. Shot 13 shows a man in a tan hood kneeling at the cross. Shot 14 shows Jesus alone in the garden. The doodle finishes the picture: "with me in paradise" (Luke 23:43).
- It pays off "With Him" and "you too" with no words on screen.
- It gives the 3 s hold a reason to stay. Today the hold is a still garden.
- It is doctrine from the verse itself. Nothing added: he asked, and he is with Him.

### Why it reads in any language

- Two pictures, same robe: a man kneels, then the same man walks to Jesus. No letters, no symbols, no clock.
- It reads by depth (near to far, up the hill), not left to right. Fine for RTL viewers.
- The hold has no subtitle cue (last cue ends by about 35.3 s), and the doodle sits at 31 to 41 percent of screen height. The lower third stays clear.

### Sticking to the picture (important finding)

`to_screen()` is not enough here. **The source clip moves on its own** (the hill grows, His shadow lengthens). Checked by frame compare at 0.0 / 1.5 / 2.95 s.

Build rule:
1. Track 2 points in the source clip, every frame: the foot of the inner-left cypress (about 0.432, 0.304) and the foot of the inner-right cypress (about 0.600, 0.302). OpenCV template match or LK flow. $0.
2. From the 2 points get move + scale against the reference frame (clip time 1.6 s). Apply to the anchor and the doodle size.
3. Then apply the push-in **per frame**, not the mean zoom that `to_screen()` uses:
   `z = z0 + (z1 - z0) * i / n`, `vx = clamp(cx - 0.5/z, 0, 1 - 1/z)`, same for `vy`,
   `screen = ((ax - vx) * z * 1080, (ay - vy) * z * 1920)`, doodle scale = `z` x tracked scale.
4. Gate: on 5 sampled frames the feet must sit within 4 px of the tracked grass point.

### Honest odds (my guess, not data)

- Reads as "the man who knelt is now with Jesus": about 70 percent (+/- 15).
- Feels forced to the owner: about 20 percent (+/- 10). Lower than v1-style symbols because it is a figure from the art, not a diagram.
- Known risk: some will read it as "a soul going to heaven". That is close to the verse, so I accept it.
- Known wart, not ours: in the clip His shadow grows long during the hold. It is in the shipped film already. By 38.0 s the shadow tip comes near the doodle. The tan fill keeps the figure readable.

Test it on 3 real people with the sound off before it ships.

## Rejected

| Idea | Shot | Why not |
|---|---|---|
| Empty kneeling outline, "a place for you" | 13, two kneelers | Best idea on paper. But the only free sand is in the subtitle zone, right when the "you too" cue is up. A version small enough to fit above it (about 240 px) is smaller than the far kneelers, so it reads as a child. |
| Tiny kneeling figure inside the far light shaft, "someday" | 9, storm light | A figure in a beam from the sky reads as a UFO abduction. Also the shaft drifts sideways in the clip. The far hills are in the bottom UI zone. |
| Hand-inked ray burst at "Today." | 11, Jesus profile | It is a crucifixion close-up. Rays by His head sit in the no-draw zone. |
| Footprints up the garden path | 14, garden | The path is in the bottom UI zone. Prints are too small on a phone. |
| Question mark, sun-as-clock, crown for "kingdom" | various | A glyph needs reading (and differs by script). A crown is a diagram, the kind that felt forced before. |
