import json
p = r"F:\slk\PycharmProjects\JesusInTheBible\poc_comic_page\_living_comic\episode_proof.json"
e = json.load(open(p, encoding="utf-8-sig"))
sk = {"p2a_man": "p2a_sketch.png", "p2b_jesus": "p2b_sketch.png"}
src = ["_piece1/clips/p2a.mp4", "_piece1/clips/p2b.mp4", "_piece1/clips/p2a.mp4"]
for x, s in zip(e["panels"], src):
    x["sketch"] = sk.get(x["id"]); x["clip_src"] = s
e["sketch_dir"] = "_piece1/stills_v2/_sketch"
e["output"] = "poc_comic_page/_living_comic/out/in_no_wise_proof.mp4"
e["balloons"][0]["tabs"] = [["JESUS", 90], ["JOHN 6:37", 800]]
json.dump(e, open(p, "w", encoding="utf-8"), indent=1)
print("patched")
