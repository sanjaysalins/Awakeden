# COMIC STYLE BAKE-OFF — BRIEF (Fable, 2026-07-27)

$0 planning doc. No renders run. Sonnet executes after user OK.
Test spend if approved: **$1.50** (5 stills). Baseline comparison is free — it already exists.

---

## 1. What the current style actually is (baseline, from looking at the real files)

Viewed at full res: `C:\Users\sanjay\PycharmProjects\JesusInTheBible\poc_comic_page\rung2\stills\p5a_the_welcome.png`, `p1a_night_door.png`, `p2b_jesus_speaks.v1_TWINPORTRAIT.png`, plus both char sheets.

The current look is a **serious, moody inked graphic novel**: heavy black ink with dense
cross-hatching, halftone dot screening in the shadows, near-realistic faces and anatomy,
and a two-temperature palette — cool slate-blue stone against ONE warm amber light source —
mounted on aged cream paper. Night dominates; warmth only arrives as lamplight. It reads
**adult, solemn, cinematic** — prestige graphic novel, NOT the warm daylight illustrated-Bible
strip the user is describing. That gap is exactly what this bake-off measures.

---

## 2. Rules EVERY candidate must obey (from the DNA — not optional)

- **No baked text ever.** Every prompt ends with the validated block:
  *"GLOBAL TEXTUAL CONSTRAINT: NO text of any kind anywhere — no speech bubbles, no caption boxes, no lettering. Pure artwork only."*
  (Style-level negation is the one kind proven to work on this model. Never negate a concrete noun anywhere else in the prompt — describe the wanted end-state instead.)
- **Period-accurate**: first-century Judea dress, stone, sandals. No anachronisms.
- **Christ dignified**, never cartoon-cute, never superhero-built. This test scene is not a passion beat, so the wounds rule doesn't bite here — but see §7: the winner must pass a passion-beat still BEFORE adoption.
- No speech bubbles (user-locked). Captions are added later by code, never by the model.

---

## 3. One shared test scene — same for all 5 candidates

**The Welcome at the Door** (reuse — we already have this exact beat in baseline style, so the control render costs $0).

- Characters: the existing **Jesus + Seeker**, chained via
  `C:\Users\sanjay\PycharmProjects\JesusInTheBible\poc_comic_page\rung2\_charsheet_jesus.png` and
  `C:\Users\sanjay\PycharmProjects\JesusInTheBible\poc_comic_page\rung2\_charsheet_seeker.png`
  as `--image` refs on every render.
- Why this beat: two recurring faces (identity test) + warm light vs cool stone (palette test) + emotion (face test) + arch/door/scroll (period-detail test) + a free baseline control:
  file:///C:/Users/sanjay/PycharmProjects/JesusInTheBible/poc_comic_page/rung2/stills/p5a_the_welcome.png

**Shared SCENE BLOCK** (verbatim in every render, placed AFTER the style block):

> SCENE: A weary grey-haired traveler in a rough, ragged hooded cloak steps through a heavy
> arched wooden door, clutching a rolled parchment scroll. Jesus — long dark hair, short dark
> beard, simple cream first-century robe with a cloth sash and sandals — stands just inside,
> one hand resting on the traveler's shoulder, his face open and glad, welcoming him in.
> Ancient stone archway and flagstone floor, first-century Judea. Warm light fills the space
> beyond the door; the outer wall sits in cool evening shadow. Both faces clearly visible.
> The two men match the reference images exactly: same faces, same builds, same dress.

**Known risk, stated up front:** the char sheets are drawn in the baseline inked style, and a
chained ref can pull the render's STYLE back toward baseline, not just the faces. Mitigation
(from the validated spec): put the style block FIRST and restate it in one closing line.
Judge each render on how far it moves the style WHILE holding the faces.

---

## 4. The candidates (5 — genuinely distinct, not variations)

All 5 test renders go on **NBP `nano_banana_pro` (HF-billed, ~$0.30/still)** — it is the only
proven identity-hold path and this scene has both recurring characters in it. The per-candidate
provider note is about PRODUCTION plates if that style wins.

### A. STORYBOOK BIBLE STRIP — the user's named direction
- **Look:** warm mid-century illustrated-Bible comic — clean even ink outlines, flat warm color, sunny daylight, friendly readable faces. The Picture-Bible tradition.
- **Style block:**
  > Classic mid-century illustrated Bible storybook comic art: confident clean black ink
  > outlines of even weight, warm flat color fills with simple two-tone shading, a sunny
  > honeyed daylight palette of warm tan, terracotta, olive and sky blue, friendly naturalistic
  > faces with clear readable expressions, minimal hatching, open uncluttered composition,
  > smooth matte paper finish.
- **Provider:** NBP for all character scenes; `nano_banana_2` fine for neutral plates — flat clean styles are easy for it.

### B. ACTION PAINTERLY — the strongest challenger
- **Look:** modern painted Bible-comic — loose ink over full painted color, dramatic angles, rich light. The Action-Bible tradition; keeps drama where A risks going flat.
- **Style block:**
  > Modern dynamic painted comic-book art: energetic loose ink drawing over fully painted
  > color, a rich saturated palette with dramatic painted light and atmospheric depth,
  > a sweeping cinematic camera angle, expressive lifelike faces, visible painterly brushwork
  > in cloth and sky.
- **Provider:** NBP everywhere — painted faces drift fastest without a ref.

### C. CLEAN-LINE EUROPEAN (bande dessinée)
- **Look:** Tintin-tradition album art — uniform line weight, perfectly flat color, zero hatching, maximum clarity. The most different-at-a-glance of the five.
- **Style block:**
  > European clean-line comic album art: uniform-weight crisp black outlines around every
  > form, perfectly flat color fills with zero gradients and zero hatching, a bright clear
  > daylight palette, simplified accurately-proportioned figures against a precise detailed
  > architectural background, calm balanced composition, smooth flat matte finish.
- **Provider:** NBP for characters; `nano_banana_2` strong candidate for plates — flat + architectural is its comfort zone.

### D. WATERCOLOR STORYBOOK
- **Look:** soft watercolor washes over light ink — the hand-painted children's-Bible plate. Gentlest, most devotional of the five.
- **Style block:**
  > Gentle watercolor storybook illustration: soft transparent watercolor washes over a fine
  > light-brown ink drawing, a luminous warm palette that pools and blooms softly at the
  > edges, generous pale paper breathing room, tender naturalistic faces, soft-edged shadows,
  > the feel of a hand-painted Bible storybook plate.
- **Provider:** NBP everywhere — soft styles lose face identity fastest; always chain the ref.

### E. MODERN FLAT WEBCOMIC — the dark horse
- **Look:** crisp flat cel-shaded digital comic — bold shapes, big readable faces, built for a phone screen. Most legible at Shorts size; also the cleanest to animate (big flat shapes = least invention surface).
- **Style block:**
  > Contemporary flat-color digital webcomic art: crisp dark-brown line art, bold simple
  > shapes, flat cel shading in two clean tones per surface, a warm modern palette of amber,
  > teal and cream, strong silhouette-first composition, large readable faces, generous
  > negative space, clean smooth finish.
- **Provider:** NBP for characters; `nano_banana_2` viable for plates.

**Deliberately NOT included** (locked decisions, not re-litigated here):
golden-age four-color retro + Baroque oil painted-comic — both deprecated 2026-07-25;
superhero style — fails the body-gate by construction; gritty adult noir — that's the baseline's own family, no contrast gained.

---

## 5. Cost

| Item | Count | Unit | Total |
|---|---|---|---|
| Test stills, one per candidate (NBP `nano_banana_pro`) | 5 | $0.30 | **$1.50** |
| Baseline control (`p5a_the_welcome.png`, already rendered) | 1 | $0 | $0 |
| Optional round 2: passion-beat still, top 2 styles only (§7) | 2 | $0.30 | +$0.60 |
| **Max total** | | | **≤ $2.10** |

Per the ask-before-spending rule: get the explicit OK on $1.50 before Sonnet renders anything.

---

## 6. How to judge (side-by-side gallery, 6 quick checks per still)

1. Same two men as the char sheets? (identity hold)
2. Clearly different from baseline at arm's length? (a near-miss candidate is wasted spend)
3. Warmer / more inviting than baseline? (the user's actual itch)
4. Reverent + period-correct? (no cute-Jesus, no anachronism)
5. Zero baked text?
6. Would it animate clean? (big simple shapes beat fine hatching under video models)

Build one `_STYLE_BAKEOFF_REVIEW.html` with baseline + 5 candidates in a row, full-res
clickable — judge at full resolution, never thumbnails.

---

## 7. What happens after (before any adoption)

The doorway scene tests **warmth**; it cannot test **reverence under suffering**. A style
that is lovely at the door can go kitsch at the cross. So: the top 1-2 candidates each get
ONE passion-beat still (servant register, faint matted blood per DNA §5a, positive-only
wording) before any switch decision. ~$0.60. A style that fails the cross fails, full stop.

---

## Fable's call

**A (Storybook Bible Strip) is the one to beat** — it answers the user's instinct directly
and moves furthest on the axes that matter (daylight, clean line, approachable faces) while
staying doctrinally safe. **B (Action Painterly) is the real challenger** because it keeps
dramatic range for passion beats, where A is most at risk of going flat. C is the most
visually distinct but risks reading as "Tintin in Judea"; D may be too soft for Shorts
thumbnails; E is the sleeper for phone-screen legibility and animation cleanliness.

---

## Round 2 — widely-loved comic genres (Fable, 2026-07-27, after eye-review of round 1)

User's ask, verbatim: *"can we test more style, expand the typically loved graphic comic
genre"* — the big popular comic traditions the world actually reads, not more variations
on the Bible-storybook niche. $0 planning; Sonnet renders after user OK.

**Where round 1 landed (all 5 renders eye-reviewed at full res):** A is the leader — warmest,
cleanest, both faces held, genuinely the look the user described. B is the real challenger —
the painted dusk sky gives it drama A lacks. C's faces tip cartoon (Jesus's grin). D lost the
enclosing stone — the wash dissolves to bare white paper at the edges, so the radiant-doorway
warmth leaks away. E is boldest and most phone-legible but reads generic-webcomic, not Bible
art. Round 2 tests five genres A–E never touched.

**Same rules (§2), same shared scene block (§3), same char sheets chained, all test renders
NBP `nano_banana_pro` (~$0.30/still).** Style block FIRST, one closing restate line, then the
global textual-constraint block. **Heightened pullback risk:** F–J sit much further from the
char sheets' inked style than A–E did, so expect the refs to drag harder — judge
style-movement-while-holding-faces exactly as in §6. The two monochrome candidates (I, J)
open AND close on their monochrome wording, because the colored refs will try to pull color
back in.

### F. MANGA INK — the world's biggest comic tradition
- **Look:** Japanese manga — expressive eyes, screentone dot shading, dynamic varied-weight
  linework. The most-read comic grammar on earth; completely un-Western, so maximum contrast.
- **Style block:**
  > Japanese manga ink comic art: confident varied-weight black ink linework, expressive
  > finely drawn eyes full of feeling, screentone dot shading in the shadows and cloth folds,
  > dynamic diagonal composition with strong perspective, fine hatching in hair and stone,
  > a restrained warm wash of amber and slate color over the ink, naturalistic adult
  > proportions, dignified serious faces, crisp bright paper.
- **Provider:** NBP for characters; `nano_banana_2` plausible for plates (line + tone suits it).
- **Distinct from A–E:** the only Japanese-grammar candidate — screentone + manga eye language;
  all five round-1 styles are Western. *Risk:* expressive eyes can slide cute — the block pins
  "naturalistic adult proportions, dignified serious faces"; screentone is fine texture that
  can moiré under video models (judge on §6 check 6).

### G. MAINSTREAM INK — the superhero TECHNIQUE, not the genre
- **Look:** the pure inking energy of modern mainstream comics — tapering brush lines, deep
  spot blacks, feathered hatching, dramatic angles. **Genre content stays banned by the
  body-gate:** Jesus and the Seeker wear plain first-century dress, ordinary human builds,
  always. We are borrowing the linework, never the bodies.
- **Style block:**
  > Bold contemporary comic-book inking: confident tapering brush-and-pen lines, deep solid
  > spot blacks, crisp feathered hatching at the edges of forms, dramatic low-angle
  > composition with strong depth, rich saturated color with warm rim light, lean everyday
  > human figures in simple first-century robes, expressive lifelike faces, glossy
  > printed-comic finish.
- **Provider:** NBP for characters; `nano_banana_2` viable for plates.
- **Distinct from A–E:** B is *painted* color with loose ink; G is pure line discipline —
  spot blacks + punchy flat color. The energy of the shelf's best-sellers without one
  spandex thread. Animates clean (bold shapes, solid blacks).

### H. WEBTOON PAINTERLY — the most-loved LIVING comic genre
- **Look:** Korean manhwa/webtoon digital painting — soft luminous color, minimal delicate
  line, glowing light, polished finish. The fastest-growing comic audience on earth, and
  native to the exact phone screens Shorts play on.
- **Style block:**
  > Korean webtoon digital painting: soft painterly rendering with delicate minimal linework,
  > luminous glowing light and smooth gentle color gradients, a warm radiant palette,
  > lifelike faces with soft cinematic shading, atmospheric glow around the light source,
  > clean polished finish, composition built for a phone screen.
- **Provider:** NBP everywhere — soft styles lose face identity fastest (same warning as D).
- **Distinct from A–E:** the only soft-digital luminous candidate — D was paper watercolor,
  H is screen-glow paint. *Risk:* faces can drift "drama-handsome" — hold the Christ-dignity
  check hard.

### I. NOIR SPOT-COLOR — black, white, and ONE color
- **Look:** high-contrast noir comic — pure black-and-white chiaroscuro with a single spot
  color. For this test scene the one color IS the theology: the doorway's amber light is the
  only color in the frame.
- **Honest note on the §4 exclusion:** round 1 excluded *full-color gritty noir* as the
  baseline's own family. The spot-color mechanic is a different, instantly-recognizable look
  (total monochrome + one hue), and the user's round-2 ask named it — so it earns its slot.
  It moves AWAY from warmth, so it is a passion-beat/special-episode candidate, not a
  house-style candidate.
- **Style block:**
  > Stark monochrome noir comic art: high-contrast black-and-white ink, great pools of solid
  > black shadow, bold graphic silhouettes and hard-edged shapes of light, heavy dry-brush
  > texture, lifelike serious faces, dramatic composition — and one single spot color, the
  > warm amber glow of the doorway light, the only color in the frame, monochrome everywhere
  > else.
- **Provider:** NBP for characters; `nano_banana_2` strong for plates (graphic B/W shapes).
- **Distinct from A–E:** the only monochrome+spot-color candidate; different at ten paces.
  *Risk:* weak Shorts thumbnails next to color styles; at a cross scene the spot color must
  NEVER be blood-red (bright blood is gated) — amber light only.

### J. DORÉ ENGRAVING — historically THE Bible-illustration look
- **Look:** classical 19th-century engraved illustration in the Gustave Doré Bible tradition —
  monochrome steel-engraving cross-hatch, vast light shafts, epic reverent scale. The most
  iconic "Bible art" ever printed; instant scriptural gravitas.
- **Style block:**
  > Classical nineteenth-century engraved Bible illustration in the tradition of Gustave
  > Doré: fine parallel engraving lines and dense cross-hatching, a full monochrome tonal
  > range from deep velvet shadow to radiant white light, a great shaft of light breaking
  > over the scene, epic monumental composition, reverent naturalistic figures with lifelike
  > anatomy, the look of a steel engraving printed on cream paper, monochrome throughout.
- **Provider:** NBP everywhere — engraved faces drift fast without the ref.
- **Distinct from A–E:** zero overlap with anything tried; the one candidate that reads
  "Bible illustration" before it reads "comic." *Risk:* dense hatching shimmers under video
  models; monochrome thumbnails. Strongest candidate for passion beats regardless.

---

## Round 2b — the hard-scene test (the cross)

User's suggestion, verbatim: *"could I suggest doing one of jesus nailed to a cross, since
that is always problematic still."* He is right — §7 already flagged that the doorway only
tests warmth, never reverence-under-suffering, and the crucifixion is historically this
project's hardest render. This section engineers that test so it doesn't fail on first try.
Every rule below is a hard-won lesson (DNA §5a + the crucifixion fact card), not style:

- **Pierced WOUND, never the hardware noun** — naming it at close range hallucinates
  decorative spikes/screws/gibberish signs. Wound-only wording is also fully faithful.
- **Arms stretched OUT along the crossbeam, wrists near the ENDS; whole figure framed** —
  a tight face+hands close-up forces an impossible slumped pose.
- **ONE cross, stated plainly** — models have drawn TWO crosses in one frame. No thieves in
  this test.
- **Supernatural darkness, not storm weather** (Luke 23:44-45) — sun blotted out, no
  thunderclouds/lightning.
- **Loincloth, garments parted** (John 19:23-24). DNA allows robed as a per-piece choice;
  the test uses the loincloth because it is the harder, more literal case — a style that
  renders a marred unrobed body reverently will certainly pass robed.
- **Crown of thorns may remain; blood always faint, dried, matted** — never bright droplets.
- **Servant register, end-state words only:** gaunt, sorrowful, marred, head bowed. None of
  the banned body tokens appear, and nothing is negated — positive description only.
- **No Seeker in this scene.** Chain `C:\Users\sanjay\PycharmProjects\JesusInTheBible\poc_comic_page\rung2\_charsheet_jesus.png`
  ONLY, for the face. (NSFW-block history on bare-torso crosses is an HF *video* issue; the
  marred NBP still is proven achievable —
  `C:\Users\sanjay\PycharmProjects\JesusInTheBible\longform\EW01_Two_Goats\_retro_dna\_prove_it\christ_cross_marred.png`.)

**Prompt assembly, per finalist:** [finalist's STYLE BLOCK] → [PASSION SCENE BLOCK below,
verbatim] → one-line style restate → the global textual-constraint block (§2).

**Shared PASSION SCENE BLOCK:**

> SCENE: One wooden cross stands alone on the rocky crest of Golgotha — a single upright,
> a single crossbeam. Jesus hangs on that one cross, the only figure in the frame, his arms
> stretched out along the crossbeam with his wrists near its ends. At each wrist and at his
> feet is a dark ragged pierced wound, the blood dried dark and matted. He wears only a rough
> cloth loincloth; his body is gaunt and wasted, ribs shadowed, his head bowed beneath the
> crown of thorns, his face sorrowful and marred with suffering — the same face as the
> reference image: long dark hair, short dark beard. The whole figure is visible from a quiet
> mid-distance below the cross. Supernatural darkness lies over the land — the sun blotted
> out, daylight failed to a deep still dusk, the far hills and city wall sunk in shadow.
> Still, silent, reverent.

**Eye-audit (from the logged two-crosses bug):** count the crosses and trace each arm to ITS
beam before passing; audit at full res; body-gate Vision check on every result.

**Finalists — run 3, not 10:** **A** (round-1 leader — must prove it doesn't go kitsch at the
cross before any adoption) **+ the top TWO round-2 standouts as judged at the doorway
gallery.** Pre-registered expectation: **H** (strongest new all-rounder) and **J** (the
reverence benchmark — the engraved tradition was built for Golgotha, and it frames the
judgment of the other two). If the doorway gallery flips the standout order, swap the
round-2 slots; the rule stays "leader + two standouts."

---

## Round 2 + 2b cost (updated)

| Item | Count | Unit | Total |
|---|---|---|---|
| Round 1 test stills A–E (DONE, user-reviewed) | 5 | $0.30 | $1.50 spent |
| Round 2 test stills F–J (NBP, doorway scene) | 5 | $0.30 | $1.50 |
| Round 2b passion still, 3 finalists | 3 | $0.30 | $0.90 |
| **New spend this round (needs explicit user OK)** | | | **$2.40** |
| **Whole bake-off, all rounds** | | | **$3.90** |

---

## Fable's updated pick (round 2)

**A still leads overall; among the new five, H (Webtoon Painterly) is the pick — the
most-loved living comic genre, phone-native and warm, exactly the user's itch — with G
(Mainstream Ink) close behind for drama and J (Doré) reserved as the passion-beat
specialist; nothing is adopted until it passes the Round 2b cross.**
