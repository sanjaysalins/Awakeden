# -*- coding: utf-8 -*-
"""One-off: build a SAMPLE upload kit for short #06 (agent-authored generation),
run the deterministic gates, write upload_kit.{json,md}. No bridge/API needed."""
from pipeline import upload_engine as ue, upload_gates, upload_handoff
from pipeline.upload_runner import _sibling_titles

MEDIA = r"longform/02_Psalm_22_Song_From_The_Cross/v1/shorts/06_The_Ends_Of_The_Earth"

KJV = "All the ends of the world shall remember and turn unto the LORD: and all the kindreds of the nations shall worship before thee."

raw = {
    "title_candidates": [
        {"text": "A Dying Man's Song Foretold the Whole World Turning to God (Psalm 22)",
         "angle": "prophecy-from-the-cross: the forsaken sufferer's own song predicts a global turning"},
        {"text": "Psalm 22 Ends With a Promise No One Expects",
         "angle": "curiosity gap, honest: the despair psalm closes on worldwide worship"},
        {"text": "The Forsaken Cry That Reached Every Nation",
         "angle": "scope contrast: one man alone -> all the ends of the earth"},
        {"text": "Why the Saddest Psalm Doesn't End in Despair",
         "angle": "reframe: the arc from forsaken to the nations worshipping"},
    ],
    "platforms": {
        "youtube_short": {
            "title": "A Dying Man's Song Foretold the Whole World Turning to God (Psalm 22)",
            "description_body": (
                "Psalm 22 opens with a man forsaken and dying alone — and ends with every nation on earth turning to God. "
                "The same song that cried “My God, my God, why hast thou forsaken me?” closes on a promise of worldwide worship. "
                "From that cross and the empty tomb, the gospel did go out to nation after nation.\n\n"
                "“" + KJV + "” (Psalm 22:27, KJV)\n\n"
                "The ends of the world include wherever you are. There is still room to turn to Him."
            ),
            "tags": ["Psalm 22", "Psalm 22 explained", "Bible prophecy", "Jesus in the Old Testament",
                     "Psalm 22 Jesus", "gospel to the nations", "Bible shorts", "KJV", "Christian shorts",
                     "all the ends of the world", "messianic psalm"],
            "hashtags": ["#Psalm22", "#Bible", "#Jesus", "#Gospel", "#Scripture"],
        },
        "youtube_long": {
            "title": "Psalm 22: The Forsaken Cry That Foretold the Whole World Turning to God",
            "description_body": (
                "Psalm 22 begins with the cry of a man forsaken and dying alone, yet it does not end there. "
                "By verse 27 the same song looks out and sees every family of every nation turning to the LORD. "
                "In this study we trace the psalm's own arc — from the forsaken sufferer to the worship of the nations — "
                "and how, from the cross and the empty tomb, the gospel went out to the ends of the earth.\n\n"
                "“" + KJV + "” (Psalm 22:27, KJV)\n\n"
                "Wherever you are is one of the ends of the world this verse promised. There is still room to turn to Him."
            ),
            "tags": ["Psalm 22", "Psalm 22 explained", "Psalm 22 Bible study", "messianic psalm",
                     "Bible prophecy fulfilled", "Jesus in the Old Testament", "gospel to the nations",
                     "Great Commission", "KJV Bible", "Christian Bible study", "Old Testament Jesus",
                     "all the ends of the world shall remember"],
            "hashtags": ["#Psalm22", "#BibleStudy", "#Jesus", "#Gospel", "#Scripture"],
        },
        "tiktok": {
            "title": "",
            "description_body": (
                "Psalm 22 opens with a man dying alone, forsaken — and ends with every nation on earth turning to God. "
                "The saddest psalm closes on worldwide worship."
            ),
            "tags": [],
            "hashtags": ["#Psalm22", "#Bible", "#Jesus", "#Gospel", "#fyp"],
        },
        "facebook": {
            "title": "A Dying Man's Song Foretold the Whole World Turning to God",
            "description_body": (
                "Psalm 22 opens with a man forsaken and dying alone — and ends with every nation on earth turning to God. "
                "From the cross and the empty tomb, the gospel went out to the ends of the earth.\n\n"
                "“" + KJV + "” (Psalm 22:27, KJV)\n\n"
                "The ends of the world include wherever you are. There is still room to turn to Him."
            ),
            "tags": [],
            "hashtags": ["#Psalm22", "#Bible", "#Jesus", "#Gospel"],
        },
        "instagram": {
            "title": "",
            "description_body": (
                "Psalm 22 opens with a man dying alone, forsaken — and ends with every nation on earth turning to God. "
                "The saddest psalm closes on worldwide worship."
            ),
            "tags": [],
            "hashtags": ["#Psalm22", "#Bible", "#Jesus", "#Gospel", "#Scripture", "#Faith", "#Christian"],
        },
    },
}

brand = ue.load_brand()
facts = ue.harvest_facts(MEDIA)
kit = ue.assemble_kit(facts, raw, brand)
kit.gates = upload_gates.run_all(kit, brand, _sibling_titles(MEDIA))
kit.status = "SAMPLE (agent-authored, gates only — red-team + panel pending your OK)"
kit.redteam = "(not run for the sample — will run the in-engine hostile auditor + full external panel after you approve the format)"
paths = upload_handoff.write_kit(kit)
print("GATES:")
for g in kit.gates:
    print(("  OK " if g.passed else "  XX ") + f"{g.gate} {g.name}: {g.detail}")
print("\nALL PASS:", kit.all_gates_pass)
print("MD :", paths["md"])
print("JSON:", paths["json"])
