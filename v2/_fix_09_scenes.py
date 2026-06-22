import json
from pathlib import Path

p = Path(r"C:/Users/sanjay/PycharmProjects/PythonProject1/jesus/narration/09 The Father Who Ran/v1/visual/scene_plan.json")
d = json.loads(p.read_text(encoding="utf-8"))

for s in d["plan"]["scenes"]:
    if s["index"] == 8:
        s["subject_block"] = (
            "the father's arms locked around his returned son in a quiet tearful homecoming, "
            "his bearded face pressed gently to the son's neck in welcome, the son fully clothed "
            "in a coarse ragged brown tunic that covers his chest and shoulders, an aged hand at "
            "rest on the son's clothed shoulder, the son's worn rags against the father's fine robe, "
            "both faces close and reverent"
        )
        s["visible_elements"] = (
            "the father embracing his fully-clothed son, bearded face to the son's neck, an aged "
            "hand on the clothed shoulder, ragged tunic against a fine robe; NO bare torso"
        )
        s["mood_block"] = "atmosphere of a reverent, tearful homecoming"
    if s["index"] == 10:
        s["subject_block"] = (
            "the running father centred with both arms opened wide and his weathered face lit with "
            "joy, his hands natural and anatomically correct, and behind him only a vague dark "
            "half-dissolved shadow-mass where a stern folded-arms figure is barely suggested, "
            "coming apart into cloud at its edges, subtle background vignettes fading into shadow "
            "suggesting a barred gate swinging inward, an abandoned empty judge's seat, and a raised "
            "hand lowering from a blow it never strikes"
        )
        s["visible_elements"] = (
            "the running father with both arms wide and natural, anatomically-correct hands; a vague "
            "dissolving shadow-form behind (not a defined figure); a barred gate; an empty seat"
        )

p.write_text(json.dumps(d, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print("updated subject_blocks for scenes 8 and 10")
