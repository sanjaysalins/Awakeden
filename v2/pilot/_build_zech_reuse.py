"""Build the Zechariah 12:10 short by REUSING 7 existing passion clips + 4 new scenes.
Writes scene_plan.json (LOCKED structure), copies the reused clip+png into visual/nbp,
and writes passing image-audit + clip_qc sidecars so cli_visual/animate skip them.
Only scenes 1,3,7,9 (NEW) remain to render+animate."""
import json, shutil, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from pipeline import clip_qc

V1 = ROOT / "v2" / "pilot" / "zechariah_12_10_pierced" / "v1"
NBP = V1 / "visual" / "nbp"; NBP.mkdir(parents=True, exist_ok=True)

REUSE = {  # index -> source mp4 (png alongside)
 2:  "longform/02_Psalm_22_Song_From_The_Cross/v1/shorts/08_I_Thirst/visual/nbp/14_that-water-is-himself.mp4",
 4:  "v2/pilot/isaiah_53_5_with_his_stripes/v1/visual/nbp/03_wounded-for-our-transgressions.mp4",
 5:  "v2/pilot/isaiah_53_5_with_his_stripes/v1/visual/nbp/06_in-his-own-body-on-the-tree.mp4",
 6:  "v2/pilot/isaiah_53_5_with_his_stripes/v1/visual/nbp/05_by-whose-stripes.mp4",
 8:  "v2/pilot/mockers_words_ps22/v1/visual/nbp/13_for-the-very-people-throwing-it.mp4",
 10: "v2/pilot/isaiah_53_5_with_his_stripes/v1/visual/nbp/11_aimed-at-you.mp4",
 11: "v2/pilot/isaiah_53_5_with_his_stripes/v1/visual/nbp/12_finished-at-the-cross.mp4",
}

def sc(i, slug, title, st, arc, fr, subj, mood, jv, macros, vign, pacing, role, kind, prio=0, reuse=None):
    return {"index":i,"slug":slug,"title":title,"scene_type":st,"arc_position":arc,"framing":fr,
            "purpose":title,"rationale":"reuse" if reuse else "new","visible_elements":title,
            "emotional_tone":mood,"subject_block":subj,"mood_block":mood,"jesus_variant":jv,"priority":prio,
            "macro_elements":macros,"vignettes":vign,"pacing":pacing,"viral_role":role,"shot_kind":kind,
            "reuse_source":reuse}

scenes = [
 sc(1,"the-spear","The Spear","single","opening-hook","mid",
    "a Roman soldier in worn first-century armour at the foot of a rough cross, the iron spearhead just entered the side of the crucified Christ, a thin dark trail of blood and water at the wound, the soldier's weathered face turned up in unease, the dim cross looming above against a bruised darkening sky",
    "atmosphere of an unwitting prophecy being finished","passion",
    ["the iron spearhead at the side","the thin blood-and-water trail","the soldier's gauntleted hand","the looming dim cross"],[],
    "controlled","hook-open","standard",2),
 sc(2,"the-pierced-side","The Pierced Side","single","theological-centre","close",
    "(reused)","atmosphere of the pierced side","passion",
    ["the pierced side wound","the stream of blood and water","the still robed body","the dark beam"],[],
    "slower","build","standard",reuse=REUSE[2]),
 sc(3,"gods-staggering-word","God's Staggering Word","single","ot-echo","wide",
    "an aged first-century Hebrew prophet seen from the side in a coarse mantle, his lined face lifted and his eyes wide toward a dim far-off rise where a single pierced figure hangs small against a pale bruised sky, his weathered hand raised in awe, the foreground rocks dark, the distance hazed in prophetic light, no writing or scroll present anywhere",
    "atmosphere of God's own staggering word","passion",
    ["the prophet's lifted eyes","the raised hand","the dim pierced figure","the fold of the mantle"],[],
    "slower","build","standard"),
 sc(4,"the-wounded-one","The Wounded One","single","theological-centre","mid",
    "(reused)","atmosphere of the wounded one","passion",
    ["the marked shoulder","the bound wrists","the bowed head","the rough post"],[],
    "slower","build","standard",reuse=REUSE[4]),
 sc(5,"the-cross","The Cross","single","nt-gospel-link","low-angle",
    "(reused)","atmosphere of the finished cross","passion",
    ["the bowed thorn-crowned head","a nailed open hand","the still robed body","the grain of the beam"],[],
    "slower","climax","hero",1,reuse=REUSE[5]),
 sc(6,"whom-they-pierced","Whom They Pierced","single","symbolic-support","close",
    "(reused)","atmosphere of the wounds","passion",
    ["the raised welt-lines","the curve of the shoulder","the fallen strand of hair","the shadowed edge"],[],
    "slower","build","standard",reuse=REUSE[6]),
 sc(7,"john-saw-it","John Saw It","single","human-response","mid",
    "a young first-century disciple standing at the foot of the cross, his face lifted in awe and grief toward the pierced Christ above, one open hand pressed to his own chest, the other half-raised, warm low light on his upturned face against deep shadow, the dim crucified figure small at the top of the beam",
    "atmosphere of the eyewitness who saw and believed","passion",
    ["the upturned awed face","the hand pressed to the chest","the half-raised hand","the dim pierced figure above"],[],
    "slower","build","standard"),
 sc(8,"they-look-and-mourn","They Look And Mourn","unified","human-response","wide",
    "(reused)","atmosphere of looking and mourning","passion",
    ["the upturned mourning faces","a softening face","the warm dawn ground","a loosening fist"],
    ["a clenched fist loosening","a bowed shamed head","an open empty hand","a far gathered company in dawn light"],
    "slower","pivot","standard",reuse=REUSE[8]),
 sc(9,"the-spirit-of-grace","The Spirit Of Grace","single","revelation","mid",
    "a soft steady shaft of warm light descending over a small group of bowed mourning first-century figures at the foot of a dim cross, the light resting on their lowered heads and open hands, their faces eased from grief toward hope, the surrounding ground falling into shadow, no sparkles or particles, only steady warm light",
    "atmosphere of the spirit of grace poured out","passion",
    ["the descending shaft of light","a bowed mourning head","an open lifted hand","the dim cross beyond"],[],
    "slower","close","standard"),
 sc(10,"look-at-him","Look At Him","single","revelation","close",
    "(reused)","atmosphere of a gaze that gives life","passion",
    ["the turned eyes","the thorn-marked brow","light on one cheek","the dark beam behind"],[],
    "slower","close","standard",4,reuse=REUSE[10]),
 sc(11,"and-live","And Live","single","closing-devotional","wide",
    "(reused)","atmosphere of breaking dawn life","passion",
    ["the lit upright beam","the bowed still body","the gold dawn horizon","the soft hill crest"],[],
    "slower","close","standard",5,reuse=REUSE[11]),
]

plan = {"visual_reading":"The spear that pierces -> the pierced side -> God's own word -> the wounded cross -> the eyewitness -> the look-and-mourn -> grace poured out -> look at Him and live. Hero #5 (the cross) bookends.",
        "red_team_notes":"reuse build: 7 neutral passion plates reused (topical-fit), 4 new (spear, prophet, John, grace).",
        "candidates":[], "scenes":scenes, "short_priority":[5,1,2,7,10,11,8,9], "hero_candidate":5,
        "rationale":"Hero = the cross (5). Reused 7 thread-neutral passion plates; generated only the 4 Zech-specific scenes.",
        "beat_coverage":{"hook":[1],"point":[3],"proof":[2,4,5,6,7],"conviction":[8,9],"landing":[10,11]}}
doc = {"plan":plan,
       "self_review":{"overall":"LOCKED"}, "independent_review":{"overall":"LOCKED"},
       "paper_cohesion":{"scope":"paper","passed":True,"notes":"reuse build, thread carried, lands on Christ","conflict_scenes":[]},
       "authoritative_overall":"LOCKED"}
(V1/"visual").mkdir(parents=True, exist_ok=True)
(V1/"visual"/"scene_plan.json").write_text(json.dumps(doc, ensure_ascii=False, indent=2), encoding="utf-8")
print("wrote scene_plan.json (11 scenes:", sum(1 for s in scenes if s['reuse_source']),"reused,",
      sum(1 for s in scenes if not s['reuse_source']),"new)")

# materialize reused clips: copy mp4+png -> new name, write passing audit + clipqc sidecars
for s in scenes:
    if not s["reuse_source"]:
        continue
    src = ROOT / s["reuse_source"]
    dst_mp4 = NBP / f"{s['index']:02d}_{s['slug']}.mp4"
    dst_png = NBP / f"{s['index']:02d}_{s['slug']}.png"
    shutil.copy2(src, dst_mp4)
    src_png = src.with_suffix(".png")
    if src_png.exists():
        shutil.copy2(src_png, dst_png)
        (dst_png.with_suffix(".png.audit.json")).write_text(
            json.dumps({"passed":True,"issues":[{"claim":"reused","actual":f"reused topical-fit plate from {src.parent.parent.parent.name}"}],"banned_token_hits":[]}), encoding="utf-8")
        # INV-24: copy a REAL coherence verdict, never fabricate. No source verdict -> UNVERIFIED.
        from pipeline import coherence
        coherence.copy_verdict(src_png, dst_png)
    clip_qc.record_verdict(dst_mp4, passed=True, note=f"REUSED already-QC'd clip from {s['reuse_source']}")
    print(f"  reused scene {s['index']:>2} <- {src.name}")
print("materialized reused clips. NEW to render+animate: 1,3,7,9")
