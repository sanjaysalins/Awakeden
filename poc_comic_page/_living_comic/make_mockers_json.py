"""Builds episode_mockers.json (Piece 2 'The Mockers' Words', Psalm 22:7-8 + Matt 27) from the locked narration timings.
Panel map only: stills/clips are TODO (nothing rendered, nothing spent)."""
import json
OUT = r"F:\slk\PycharmProjects\JesusInTheBible\poc_comic_page\_living_comic\episode_mockers.json"
AUDIO = "batches/cluster_01_cross/mockers_words_ps227/audio/narration.mp3"
DUR = 78.0

# id, t0, t1, narration beat, still prompt idea, tier, flags
P = [
 ("m01_crowd_script",   0.0,  4.4, "The crowd ... was reading from a script",           "dark crowd silhouette mass, three faces lit, one holds a blank scroll (Witness Edge, foreground silhouette)", "kling", dict(role="first", ink_wake=True)),
 ("m02_david_writes",   4.4, 10.1, "A thousand years before, Psalm 22 ...",              "aged King David writing by lamp, harp on wall", "seedance", {}),
 ("m03_psalm_scroll",  10.1, 16.9, "David's words: they shake the head ...",             "open psalm scroll by clay lamp, close", "seedance", {}),
 ("m04_wagging_heads", 16.9, 19.7, "At the cross ... passers-by wagging their heads",    "three passers-by on the road below the cross, heads mid-shake (Witness Edge)", "kling", {}),
 ("m05_rulers_sneer",  19.7, 23.8, "the rulers sneering nearly line for line",           "chief priests and scribes apart, faces twisted in scorn", "kling", {}),
 ("m06_mocker_speaks", 23.8, 32.4, "He trusted in God ... I am the Son of God (Matt 27:43)", "single mocker close, mouth open, pointing up, level eye height", "kling", {}),
 ("m07_crowd_reciting",32.4, 36.4, "They thought they were inventing the cruelty",    "same crowd from behind, silhouettes, cross small in the distance", "seedance", {}),
 ("m08_scroll_glows",  36.4, 39.7, "They were reciting prophecy - unwilling witnesses", "psalm scroll again, one line catches lamplight (lamp = gold)", "seedance", {}),
 ("m09_cross_taunt",   39.7, 47.2, "save thyself ... come down from the cross (Matt 27:40)", "the cross at dusk, level camera, Jesus calm, mockers' hands pointing up from below", "kling", dict(role="jesus", ink_wake=True, sacred=True)),
 ("m10_stays",         47.2, 55.6, "But He could have come down ... staying on it",   "Jesus on the cross close, calm, nailed hand in frame, no glow", "seedance", dict(sacred=True)),
 ("m11_song_whole",    55.6, 62.3, "The man they mocked is the One the whole song was about", "psalm scroll lit, cross shadow falls across it", "seedance", {}),
 ("m12_scorners",      62.3, 68.5, "He stayed under scorn - theirs, and ours",         "crowd from behind, cross above them, one face turning", "seedance", dict(sacred=True)),
 ("m13_ends_of_world", 68.5, 75.0, "the song ends with the ends of the world turning to Him", "many figures from every direction walking toward a hill at dawn", "kling", {}),
 ("m14_landing",       75.0, 78.0, "Turn, and come to the One who would not come down", "cross at dawn, Jesus calm, one human figure turning toward Him (landing: locked face, no glow)", "seedance", dict(sacred=True)),
]
panels = []
for pid, a, b, beat, still, tier, fl in P:
    d = dict(id=pid, t=[a, b], beat=beat, still_prompt=still, clip_tier=tier, status="TODO still + clip", ink_wake=False, role="listener")
    d.update(fl); panels.append(d)

def bl(speaker, ref, text, a, b, tabs=None):
    d = dict(speaker=speaker, kjv_ref=ref, text=text, t=[a, b])
    if tabs: d["tabs"] = tabs
    return d

B = [
 # David (Psalm 22:7-8, excerpt exactly as narrated)
 bl("david", "Psalm 22:7-8", "they shake the head, saying,", 10.1, 16.9, [["DAVID", 90], ["PSALM 22:7-8", 760]]),
 bl("david", "Psalm 22:7-8", "He trusted on the LORD", 11.4, 16.9),
 bl("david", "Psalm 22:7-8", "that he would deliver him:", 13.0, 16.9),
 bl("david", "Psalm 22:7-8", "let him deliver him...", 14.6, 16.9),
 # mocker (Matt 27:43)
 bl("mocker", "Matthew 27:43", "He trusted in God;", 23.8, 32.4, [["A MOCKER", 90], ["MATT 27:43", 790]]),
 bl("mocker", "Matthew 27:43", "let him deliver him now,", 25.2, 32.4),
 bl("mocker", "Matthew 27:43", "if he will have him:", 27.2, 32.4),
 bl("mocker", "Matthew 27:43", "for he said,", 28.8, 32.4),
 bl("mocker", "Matthew 27:43", "I am the Son of God.", 29.6, 32.4),
 # mocker (Matt 27:40)
 bl("mocker", "Matthew 27:40", "save thyself.", 41.0, 47.2, [["A MOCKER", 90], ["MATT 27:40", 790]]),
 bl("mocker", "Matthew 27:40", "If thou be the Son of God,", 43.3, 47.2),
 bl("mocker", "Matthew 27:40", "come down from the cross.", 44.6, 47.2),
]
ep = dict(
    episode="the_mockers_ps22_7",
    status="PANEL MAP ONLY - no stills, no clips, no spend",
    format=dict(w=1080, h=1920, fps=30), first_episode=False,
    audio=dict(file=AUDIO, t0=0.0, dur=DUR, note="locked narration, 78.0s. Add >=3.0s landing hold (INV-26) at assembly; pad audio+video together."),
    panels=panels,
    kjv={},  # only Jesus' own words are chain-checked by LC-3. Jesus never speaks in this piece (no invented lines).
    balloons=B,
    cards=[
        dict(kind="hook", lines=["WHO SCRIPTED", "THE MOCKERY?"], t=[0.2, 2.8], decodes=[]),
        dict(kind="decode", lines=["DELIVER", "= RESCUE"], t=[17.0, 19.2], decodes=["deliver"]),
    ],
    decode_words=["deliver"],
    sfx=[],
    sketch_dir="poc_comic_page/_piece1/stills_v2/_sketch",
    output="poc_comic_page/_living_comic/out/the_mockers.mp4",
    cost_estimate=dict(
        stills="~12 unique stills, about $4-5 (rate to be re-quoted from the real invoice)",
        clips="4-5 Kling (action/crowd) about $1.13 each + 8-9 Seedance about $0.72 each = about $10-11; reuse-first check of existing mockers clips could cut this",
        voice="$0 (locked audio exists)", total="about $15, inside the ~$22 reserved. ESTIMATE ONLY. Each paid step needs its own yes + quoted price."),
)
json.dump(ep, open(OUT, "w", encoding="utf-8"), indent=1)
print("wrote", OUT)
