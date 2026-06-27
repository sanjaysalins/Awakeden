"""Build the long-form 16:9 scene_plan.json for EW01 Two Goats (Aaron / Day of
Atonement -> Christ). Period-documentary look, each scene tagged with a vetted
green-palette camera move. Runs the deterministic gates inline. Paper-only ($0)."""
import json, math
from pathlib import Path

V1 = Path(__file__).resolve().parent.parent / "longform" / "EW01_Two_Goats" / "v1"
OUT = V1 / "visual_16x9"
OUT.mkdir(exist_ok=True)

# Vetted green-palette camera moves (from the camera-palette test).
GREEN = {"pull_back", "zoomed_in", "dolly_shot", "dolly_in", "smooth_cinematic",
         "tracking_drone_view"}
RED = {"pan", "orbit", "360", "aerial_view", "top_down", "worms_eye_view",
       "pov_shot", "eye_level"}

STYLE = ("Baroque oil painting, dramatic chiaroscuro, Caravaggio and Rembrandt lighting, "
    "deep shadow and warm golden light, reverent sacred art, muted earth tones, fine "
    "visible brushwork, ancient biblical-period Near-Eastern setting, no text, no modern "
    "elements, cinematic 16:9 widescreen.")

# id, mvt, [start,end], title, framing, type, camera, atmos, sfx, directional, face_nbp, subject
S = [
 (1,"M1",[0.0,19.5],"Once a year, only once","wide","single","pull_back",
  "dawn incense smoke, dust haze","low crowd murmur, wind",False,False,
  "The high priest Aaron, small in golden vestments, stands alone before the towering "
  "curtained Tabernacle court at first light; behind and below him a vast hushed multitude "
  "of Israelites kept in shadow; immense pale sky; the sacred tent dominant and severe."),
 (2,"M1",[19.5,39.0],"I laid aside gold and glory","close","single","zoomed_in",
  "dust motes in a light shaft, faint smoke","cloth rustle",True,False,
  "Still-life: a golden breastplate, ephod and priestly garments laid upon a worn stone "
  "bench in a single shaft of light; two weathered hands releasing the gold; plain folded "
  "white linen waiting beside it. No face, hands only."),
 (3,"M1",[39.0,58.5],"Plain white linen, like a servant","medium-wide","single","dolly_shot",
  "oil-lamp flame flicker, smoke drift","footsteps, lamp hiss",False,False,
  "Aaron, now in plain white linen, seen from behind, walking down a dim colonnaded "
  "passage toward a great heavy veil lit by hanging oil lamps; his back fully to us."),
 (4,"M1",[58.5,78.0],"I went in alone","wide","single","dolly_in",
  "smoke and cloud drift, pulsing golden glow","deep silence, low tone",False,False,
  "Aaron's small linen-robed silhouette before an immense temple veil; through a narrow "
  "gap, thick darkness and a single faint golden glow of the mercy seat; the curtain "
  "towering and swallowing him."),
 (5,"M2",[78.0,99.0],"That he die not — the cloud upon the mercy seat","wide","ot_echo","smooth_cinematic",
  "luminous cloud billow, light shimmer","sustained holy drone",False,False,
  "The Holy of Holies: the golden ark and mercy seat between two great cherubim, a "
  "luminous cloud of divine presence above filling the dark chamber; one tiny prostrate "
  "linen-robed form at the lower edge, awed and small."),
 (6,"M2",[99.0,120.8],"I buried two of my own sons","medium","unified","smooth_cinematic",
  "smoke, ember glow","low grief tone, distant fire",False,False,
  "A unified memory tableau, soft-edged like remembrance. Foreground: Aaron's bowed "
  "grieving head and shoulders. Background memories dissolving softly into the dark: two "
  "fallen young priests amid strange-fire smoke; a shrouded body carried on a bier; an "
  "altar with a basin of blood and rising flame; the distant veil. Five soft vignettes, "
  "no panels or frames, all bleeding into one dim canvas."),
 (7,"M3",[120.8,144.0],"They brought me two goats, and I cast lots","close","ot_echo","zoomed_in",
  "drifting dust, altar smoke","goats, stone clack",True,False,
  "Two goats standing close together before the altar; a priest's weathered hands casting "
  "two small marked lot-stones over a bronze vessel; the markings only illegible scratches, "
  "not readable text; tabernacle court behind in shadow."),
 (8,"M3",[144.0,167.2],"The first goat I killed — blood within the vail","medium","single","dolly_in",
  "smoke, golden glow","drip, low tone",False,False,
  "Aaron in white linen carrying a shallow bronze basin of blood through thick darkness "
  "toward the faint golden glow of the mercy seat, his arm raised to sprinkle; seen from "
  "behind and side, the blood catching the light."),
 (9,"M3",[167.2,190.6],"Both my hands upon the live goat","medium","single","smooth_cinematic",
  "dust, heat haze","confessing murmur, wind",False,False,
  "Aaron laying both hands upon the head of a living goat, his own head bowed low in "
  "confession; a robed 'fit man' waits at the edge; beyond the camp gate the open "
  "wilderness opens pale and vast. Aaron in profile, half-shadowed."),
 (10,"M3",[190.6,213.9],"I watched it go — a land not inhabited","wide","single","dolly_shot",
  "drifting desert dust, heat-haze shimmer","wind, faint hooves",False,False,
  "A vast bleached desert wadi to a hazy horizon; a single small goat walking away down "
  "the cracked valley floor, reduced near to a dark speck; at the near edge, seen from "
  "behind, a lone robed man watches it go, dwarfed by the emptiness. (Reuse the approved "
  "test_hero.png.)"),
 (11,"M4",[213.9,239.5],"One offering — yet it took two goats","medium-wide","unified","smooth_cinematic",
  "smoke one side, dust and pale light the other","low wondering tone",False,False,
  "One frame holding the riddle: on the left, the slain goat in blood-red altar light "
  "and smoke (the price); on the right, the live goat facing an open pale road into the "
  "waste (the guilt carried off); the altar standing dark between them. A single unified "
  "canvas, soft transition, no hard divider."),
 (12,"M4",[239.5,265.0],"Why two? — two things at once","medium","single","dolly_in",
  "low smoke, dusk haze","quiet wind, embers",False,False,
  "Aaron alone in the emptying court at dusk, turning the question over; behind him one "
  "altar still smoking and one empty road running out into the darkening waste; his face "
  "lined and contemplative, lit by a single low flame."),
 (13,"M5",[265.0,289.3],"The people went home clean","wide","single","pull_back",
  "dusk haze, rising dust","relieved crowd murmur",False,False,
  "A great multitude of Israel departing at evening, faces lifted and unburdened, walking "
  "away from the tabernacle into golden dusk; the crowd kept soft and in shadow, a sense "
  "of relief over the whole field."),
 (14,"M5",[289.3,313.6],"Every year I came back and did it again","medium","unified","smooth_cinematic",
  "smoke, slow drifting motes","cyclical low tone",False,False,
  "A unified tableau of weary repetition: Aaron at the altar repeated as soft ghosted "
  "echoes receding into the dark, the same act year upon year; the same two goats faintly "
  "doubled; turning seasons hinted in the sky; the same basin of blood; the worn altar "
  "stone. Five soft vignettes melting into one dim recurring canvas."),
 (15,"M5",[313.6,338.0],"I was only ever pointing — a sign","medium","single","dolly_in",
  "lamp flicker, faint distant glow","held breath, low drone",False,False,
  "Aged Aaron, older and weary, alone before the veil at night, looking up toward a faint "
  "far light he cannot reach; deep shadow all around; his upturned face caught in a thin "
  "edge of light, full of unspoken longing."),
 (16,"M6",[338.0,360.6],"A shadow waits for the body — the body came","wide","jesus_link","smooth_cinematic",
  "shifting light, low smoke","tone lifts, dawn swell",False,False,
  "The long shadow of a cross falls across the old altar and the two goats, cast by an "
  "unseen figure of light off-frame; the shadow lengthens toward a luminous open doorway "
  "in the far dark; the old order dim, the coming light pale and growing. No gold cross, "
  "only shadow and a doorway of light."),
 (17,"M6",[360.6,383.2],"By his own blood he entered in once","medium-wide","jesus_link","dolly_in",
  "radiant light, cloud","glory swell",False,True,
  "Christ as the true High Priest, robed, seen from behind and side, passing through a "
  "torn radiant veil into holy light; he bears his own wounds rather than a basin of "
  "blood; darkness behind him, glory opening ahead. The fulfillment of the lone priest at "
  "the veil."),
 (18,"M6",[383.2,405.8],"The LORD laid on him the iniquity of us all","medium","unified","smooth_cinematic",
  "soft light, drifting dust","resolving chord",False,True,
  "A unified fulfillment canvas: the figure of Christ central; soft-edged to the left, the "
  "slain goat and its blood (the price paid); soft-edged to the right, the scapegoat "
  "vanishing into the wilderness (the guilt carried off); the two dissolving and resolving "
  "into the one Priest. Five soft vignettes on one canvas: Christ-centre, slain-goat, "
  "scapegoat-road, the-two-becoming-one, a faint cross of light."),
 (19,"M6",[405.8,428.4],"He suffered without the gate","wide","jesus_link","dolly_shot",
  "dust, heat haze, low cloud","lonely wind",False,False,
  "Christ led outside the city gate: a lonely robed figure on a road beyond the walls, "
  "moving toward a barren hill, deliberately echoing the scapegoat's road into the waste; "
  "the city walls behind, the wilderness ahead; seen from a distance, his back to us."),
 (20,"M6",[428.4,451.0],"He sat down — the veil rent from the top","medium-wide","jesus_link","pull_back",
  "pouring light, falling dust, faint fabric stir","deep resonant strike",True,True,
  "Two truths in one frame: the seated High-Priest Christ at rest in glory at the right "
  "hand (the chair Aaron never had), and the great temple veil torn from the top downward "
  "by no human hand, light pouring through the painted rip. The tear is painted, still, "
  "not actively ripping."),
 (21,"M7",[451.0,477.7],"Do not come to me, or a goat, or an altar","medium","single","pull_back",
  "fading smoke, growing light","gentle turn, soft tone",False,False,
  "Aged Aaron in linen steps back and gestures away from himself and from the old altar "
  "and goats, turning the viewer's eye past him toward a distant growing light; he "
  "diminishes into shadow as the light beyond him grows."),
 (22,"M7",[477.7,504.4],"Come to Jesus — carried as far as east from west","medium-wide","jesus_link","dolly_in",
  "dawn light, dust drifting away","warm rising swell",False,True,
  "A lone everyman figure walks free toward the risen Christ, who waits with open hands in "
  "dawn light; behind the walking figure a dark burden is being carried off small to the "
  "far horizon, never to return; the road ahead bright and open."),
 (23,"M7",[504.4,531.1],"The way is thrown wide open","wide","single","dolly_in",
  "pouring light, dust motes","light pour, airy tone",True,False,
  "The torn temple veil now fully open, brilliant light flooding out into the once-dark "
  "holy place; the path through it clear and inviting; no guard, no priest barring the "
  "way; the great curtain hanging painted and still, the opening ablaze."),
 (24,"M7",[531.1,557.8],"Boldness to enter into the holiest","medium-wide","unified","smooth_cinematic",
  "light, drifting dust","many footsteps, hush of awe",False,False,
  "Ordinary people of every kind draw near and step through the opened veil into the "
  "light, unafraid, where once only one man one day a year could go; kept soft and in "
  "gentle shadow so no single face dominates; a quiet procession into glory."),
 (25,"M7",[557.8,584.5],"Will you come in? — be carried clean","medium","jesus_link","dolly_in",
  "radiant light, gentle dust drift","final tender swell",False,True,
  "HERO CLOSE: the risen Christ stands in the full open doorway of light, the torn veil "
  "framing him, one hand extended toward the viewer in welcome; the way wide open behind "
  "him; warm, reverent, the whole frame resolving on his face and open hand. The landing."),
]

scenes = []
for (sid,mvt,t,title,framing,stype,cam,atmos,sfx,direc,face,subj) in S:
    scenes.append({
        "id": sid, "mvt": mvt, "t": t, "title": title,
        "framing": framing, "scene_type": stype,
        "camera": cam, "atmos": atmos, "sfx": sfx,
        "directional": direc, "face_nbp": face,
        "subject_block": subj, "style_base": STYLE,
    })

plan = {
    "episode": "EW01_Two_Goats", "aspect": "16:9", "look": "period-documentary",
    "audio_seconds": 584.5, "hero_id": 25,
    "camera_palette_green": sorted(GREEN), "camera_palette_avoid": sorted(RED),
    "scenes": scenes,
}
(OUT / "scene_plan.json").write_text(json.dumps(plan, indent=2), encoding="utf-8")

# ---------------- deterministic gates ----------------
fails = []
movements = {f"M{i}" for i in range(1,8)}
counts = {m: sum(1 for s in scenes if s["mvt"]==m) for m in sorted(movements)}
for m in sorted(movements):
    if counts[m] < 2: fails.append(f"LF-SP-G2 movement {m} has {counts[m]} (<2)")
# framing spread
from collections import Counter
fr = Counter(s["framing"] for s in scenes)
if len(fr) < 3: fails.append(f"LF-SP-G8 only {len(fr)} framings (<3)")
top = max(fr.values())/len(scenes)
if top > 0.40: fails.append(f"LF-SP-G8 a framing is {top:.0%} (>40%)")
# binding mix
nun = sum(1 for s in scenes if s["scene_type"]=="unified")
njl = sum(1 for s in scenes if s["scene_type"]=="jesus_link")
not_ = sum(1 for s in scenes if s["scene_type"]=="ot_echo")
if nun < 2: fails.append(f"LF-SP-G9 unified={nun} (<2)")
if njl < 1: fails.append("LF-SP-G9 no jesus_link")
if not_ < 1: fails.append("LF-SP-G9 no ot_echo")
if scenes[-1]["scene_type"] != "jesus_link": fails.append("hero close is not Christ/jesus_link")
# camera palette
for s in scenes:
    if s["camera"] not in GREEN: fails.append(f"scene {s['id']} camera '{s['camera']}' not green")
    if s["camera"] in RED: fails.append(f"scene {s['id']} uses RED camera '{s['camera']}'")
# every scene has an atmospheric element
for s in scenes:
    if not s["atmos"].strip(): fails.append(f"scene {s['id']} missing atmos")
# window length sanity
longest = max(s["t"][1]-s["t"][0] for s in scenes)

print(f"Wrote {OUT/'scene_plan.json'}  ({len(scenes)} scenes)")
print(f"Movement coverage: {counts}")
print(f"Framings: {dict(fr)}   top={top:.0%}")
print(f"Mix: unified={nun}  jesus_link={njl}  ot_echo={not_}  hero=#{plan['hero_id']}")
print(f"NBP-face scenes (need Nano Banana Pro): {[s['id'] for s in scenes if s['face_nbp']]}")
print(f"Directional (minimal-move / veil) scenes: {[s['id'] for s in scenes if s['directional']]}")
print(f"Longest window: {longest:.1f}s")
print("\nGATES: " + ("ALL PASS ✓" if not fails else "FAILS:\n  - " + "\n  - ".join(fails)))
