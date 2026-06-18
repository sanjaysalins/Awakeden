import json
from collections import Counter
from pathlib import Path

def S(index, slug, title, st, arc, fr, purpose, rat, vis, tone, subj, mood, jv, macros, vign, pacing, role, kind, prio=0):
    return {"index":index,"slug":slug,"title":title,"scene_type":st,"arc_position":arc,"framing":fr,
            "purpose":purpose,"rationale":rat,"visible_elements":vis,"emotional_tone":tone,
            "subject_block":subj,"mood_block":mood,"jesus_variant":jv,"priority":prio,
            "macro_elements":macros,"vignettes":vign,"pacing":pacing,"viral_role":role,"shot_kind":kind}

scenes = [
 S(1,"the-wound-that-wont-close","The Wound That Won't Close","single","opening-hook","close",
   "Make the hook's felt ache visible.",
   "Not a literal gory wound (horror) but the inner ache made reverent.",
   "a bowed first-century man, hand over his heart, a faint dark mark beneath worn cloth, deep shadow.",
   "quiet, unhealed ache",
   "a weathered first-century Judean man seen close, head bowed low and turned away, one calloused hand pressed flat over his own chest above the heart, the rough undyed tunic worn thin where the hand rests and faintly darkened beneath it, the knuckles tight, the eyes lost in shadow, the whole figure sunk in a brown-black ground with one low shaft of light on the bowed brow",
   "atmosphere of a guilt that will not close",
   None,["the hand pressed to the chest","the tight knuckles","the bowed brow in light","the worn cloth"],[],
   "slower","hook-open","standard",2),

 S(2,"isaiah-sees-the-suffering","Isaiah Sees It Coming","single","ot-echo","wide",
   "The point beat: 700 years early Isaiah foresaw healing through another's wounds.",
   "Show the prophet SEEING, not writing (no scroll, Kling garbles text); a vision in shadow.",
   "an aged prophet, eyes lifted, gazing toward a dim distant suffering figure; no text anywhere.",
   "ancient foresight, holy distance",
   "an aged first-century Hebrew prophet seen from the side in a coarse mantle, his lined face lifted and his eyes wide upon a dim far-off rise where a single suffering figure stands bound and small against a pale bruised sky, his weathered hand half-raised in awe, the foreground rocks dark, the distance hazed in dust and prophetic light, no writing or scroll present",
   "atmosphere of ancient foresight reaching across centuries",
   None,["the prophet's lifted eyes","the half-raised hand","the dim distant figure","the fold of the mantle"],[],
   "slower","build","standard"),

 S(3,"wounded-for-our-transgressions","Wounded For Our Transgressions","single","theological-centre","mid",
   "The proof's heart: He was wounded and bruised for us.",
   "The scourged Christ bound to the post, marked but reverent (Old-Master restraint, no gore-horror).",
   "Christ bound to a low post, back marked with welts, head bowed, modest cloth, no lurid blood.",
   "borne suffering, holy stillness",
   "the figure of Christ seen from behind and the side, bound by the wrists to a short rough stone post, the bare back and shoulder marked with the dark raised welts of a flogging held in solemn Old-Master restraint, the thorn-shadowed head bowed low to the chest, a modest cloth at the waist, the muscles slack and spent, warm low light raking across the marked shoulder against a deep shadowed ground",
   "atmosphere of suffering borne for another",
   "passion",["the marked shoulder","the bound wrists","the bowed head","the rough post"],[],
   "slower","build","standard",3),

 S(4,"as-a-lamb-to-the-slaughter","As A Lamb, Silent","single","ot-echo","close",
   "OT echo (Isa 53:7, cited Acts 8:32): the silent lamb led to slaughter.",
   "A single bound lamb, silent — the cited type, not a stretch.",
   "a single young lamb lying bound and still on dark stone, eyes calm, a faint cross-shaped shadow.",
   "silent, willing, set apart",
   "a single young lamb lying bound at the feet on a slab of dark stone, its wool pale and catching a low warm light, its eyes calm and unresisting, a thin cord at the folded legs, a faint cross-shaped shadow falling across the pale wool, the surrounding ground sunk in brown-black shadow",
   "atmosphere of silent, willing sacrifice",
   None,["the calm eye of the lamb","the bound legs","the cross-shaped shadow","the pale wool in light"],[],
   "slower","build","standard"),

 S(5,"by-whose-stripes","By Whose Stripes","single","symbolic-support","close",
   "Macro of the stripes themselves — the lever word made visible.",
   "Extreme close on the welt-lines, reverent and abstract, not a horror crop.",
   "an extreme close of a marked shoulder and back, welt-lines raised in raking light, reverent.",
   "the cost, held close",
   "an extreme close view of a marked shoulder and upper back, the raised welt-lines of a flogging rendered in restrained Old-Master paint catching a low raking light, the skin warm and living, a single strand of dark hair fallen across, the lower edge dissolving into deep shadow, no lurid colour",
   "atmosphere of a cost counted stripe by stripe",
   "passion",["the raised welt-lines","the curve of the shoulder","the fallen strand of hair","the shadowed edge"],[],
   "slower","build","standard"),

 S(6,"in-his-own-body-on-the-tree","In His Own Body, On The Tree","single","nt-gospel-link","low-angle",
   "THE HERO — the gospel-pivot: Christ on the cross, the wounds that heal, the CTA landing.",
   "Iconic, near-still, reverent crucifixion — bookends open and close so the Short lands on Christ.",
   "the crucified Christ on a rough cross, body marked with stripes, head bowed, faint light behind.",
   "finished, sovereign stillness",
   "the crucified Christ lifted on a rough wooden cross seen from a low reverent angle against a darkening sky, the body stretched and marked with the dark stripes of the flogging, the thorn-crowned head bowed in completion, a modest cloth at the waist, the arms taut along the beam, a faint pale light breaking behind the dark hill, the small forms of onlookers dim at the foot",
   "atmosphere of the finished work, sovereign and still",
   "passion",["the bowed thorn-crowned head","a nailed open hand","the marked side","the grain of the cross beam"],[],
   "slower","climax","hero",1),

 S(7,"the-apostle-lays-it-on-christ","The Apostle Lays It On Christ","unified","nt-gospel-link","mid",
   "Proof: the apostle takes Isaiah's word and applies it to the crucified Christ.",
   "Show the apostle GESTURING toward the cross (no scroll/text); the connection carried in vignettes.",
   "an aged apostle, hand opened toward a dim crucified Christ beyond, soft background vignettes of the echo.",
   "proclamation, recognition",
   "an aged first-century apostle robed in coarse cloth seen in three-quarter, his lined face grave and certain, one open hand turned toward a dim crucified figure on a far rise beyond him, the other hand at his breast, warm light on his brow against deep shadow, subtle background vignettes fading into shadow suggesting a marked and bound back, the dark stripes of a scourge, a rough cross on a far hill, and a gathered company of the healed",
   "atmosphere of an old promise landing on Christ",
   None,["the open hand toward the cross","the apostle's grave face","a fold of coarse robe","the dim far cross"],
   ["a marked and bound back","the dark stripes of a scourge","a rough cross on a far hill","a gathered company of the healed"],
   "controlled","build","standard"),

 S(8,"all-we-like-sheep","All We Like Sheep","unified","ot-echo","wide",
   "OT echo (Isa 53:6): we all strayed; the LORD laid the iniquity on Him.",
   "Scattered sheep on a darkening hill + one laden burdened figure — the pericope's own line.",
   "scattered sheep on a darkening hillside, one shadowed figure bowed under a great weight, a far cross.",
   "wandering, then laid on Him",
   "a darkening hillside seen wide, a scattering of pale sheep wandered apart across the slope each turned its own way, and at the centre a single shadowed figure bowed low under a great unseen weight on his shoulders, the light failing to a bruised gold at the horizon, subtle background vignettes fading into shadow suggesting a strayed lamb at a cliff edge, an empty fold gate, a shepherd's dropped staff, and a far rough cross on the crest",
   "atmosphere of the strayed flock and the weight laid on one",
   None,["the bowed laden figure","a single strayed sheep","the failing gold horizon","the dark slope"],
   ["a strayed lamb at a cliff edge","an empty fold gate","a shepherd's dropped staff","a far rough cross on the crest"],
   "slower","build","standard"),

 S(9,"he-bare-our-sins","He Bare Our Sins","unified","theological-centre","mid",
   "Proof / theological centre: He bore OUR sins in His body.",
   "Crucified Christ central, the things He bore as vignettes (no written record — abstract).",
   "the crucified Christ central and dominant, soft vignettes of broken chains, a lifted yoke, bowed sinners.",
   "the great exchange",
   "the crucified Christ at the centre and clearly dominant, the marked body bowed in completion against a dark noon sky, and faint and half-dissolved in the surrounding shadow the burdens laid on him, subtle background vignettes fading into shadow suggesting broken iron chains falling away, a heavy wooden yoke lifted from a bent back, a crowd of bowed and ashamed figures, and a dark stain washed pale",
   "atmosphere of the great exchange borne in one body",
   "passion",["the bowed marked body","broken chains falling","a lifted yoke","the dark noon sky"],
   ["broken iron chains falling away","a heavy wooden yoke lifted from a bent back","a crowd of bowed and ashamed figures","a dark stain washed pale"],
   "slower","pivot","standard"),

 S(10,"the-healed-believer","The Healed Believer","single","human-response","mid",
   "Conviction: the one who receives — the old wound now closed.",
   "Bookend echo of scene 1: the same kind of man, eased, the scar closed, light on the face.",
   "a weathered man kneeling, face lifted in eased relief, an open hand at his chest where a scar has closed.",
   "relief, undeserved healing",
   "a weathered first-century man kneeling low with his face lifted into a warm break of light, the lines of his face eased from grief to wonder, one open hand resting at his chest where a pale closed scar now sits quiet, the other hand open and empty at his side, the dark room falling away behind him into shadow",
   "atmosphere of an undeserved healing received",
   None,["the eased lifted face","the open empty hand","the closed pale scar","the break of warm light"],[],
   "slower","build","standard",6),

 S(11,"aimed-at-you","Aimed At You","single","revelation","close",
   "Conviction: 'ye' — the promise turned straight at the viewer.",
   "Christ's eyes turned gently toward the viewer — the pronoun made a gaze.",
   "a close reverent view of the crucified Christ's face, eyes turned gently toward the viewer.",
   "personal, tender address",
   "a close reverent view of the crucified Christ's face inclined toward the viewer, the eyes lowered yet turned with a tender willing address as if meeting one set of eyes, a thorn-marked brow, warm light catching one cheek against deep shadow, the grain of the dark beam just behind",
   "atmosphere of a promise aimed at one listener",
   "passion",["the turned eyes","the thorn-marked brow","light on one cheek","the dark beam behind"],[],
   "slower","pivot","standard",4),

 S(12,"finished-at-the-cross","Finished At The Cross","unified","nt-gospel-link","wide",
   "Landing: it was finished — the cross against a widening dawn.",
   "The cross at dawn with the finished-work echoes as vignettes; gospel-frame close.",
   "the cross against a widening gold dawn, the marked body still, soft vignettes of the finished work.",
   "completion, breaking light",
   "the rough cross standing against a widening gold dawn, the marked body of Christ still and bowed in completion, warm light breaking from behind the upright beam across a quiet land, the hill's crest in soft shadow, subtle background vignettes fading into shadow suggesting a torn temple veil, a sealed stone, a kneeling centurion, and a far gathered church in dawn light",
   "atmosphere of a finished work and breaking dawn",
   "passion",["the lit upright beam","the bowed still body","the gold dawn horizon","the soft hill crest"],
   ["a torn temple veil","a sealed stone","a kneeling centurion","a far gathered church in dawn light"],
   "slower","close","standard",5),

 S(13,"come-and-receive","Come And Receive","single","closing-devotional","mid",
   "Landing CTA: the wounded hands open in invitation — come and receive.",
   "Open scarred hands extended toward the viewer — the invitation made gesture.",
   "the open scarred hands of Christ extended toward the viewer, palms up, nail-marks healed, warm light.",
   "open, grace-filled invitation",
   "the two open hands of Christ extended toward the viewer with the palms turned up in welcome, the healed nail-marks clear in each palm, the wrists emerging from a clean robe, warm dawn light spilling across the open hands against a soft shadowed ground, the figure beyond held gentle and out of focus",
   "atmosphere of an open, unforced invitation",
   "passion",["the open scarred palms","the healed nail-marks","the spilling warm light","the clean robe cuff"],[],
   "slower","close","standard",7),

 S(14,"the-wound-he-closed","The Wound He Closed","single","closing-devotional","close",
   "Closing devotional: the ache of scene 1 now at rest — He closed it.",
   "Direct bookend to the hook — the same man, hand fallen from a closed scar, at peace.",
   "the same weathered man from the opening, now at rest, the hand fallen from a closed pale scar, soft light.",
   "settled peace, healed",
   "the same weathered first-century man from the opening seen close, the head no longer bowed but lifted and still, the hand fallen open from the chest where a pale closed scar now rests untroubled, the worn cloth smooth, a soft steady light resting on the calmed face against a quiet shadowed ground",
   "atmosphere of an old wound finally closed",
   None,["the lifted calm face","the open fallen hand","the closed pale scar","the steady soft light"],[],
   "slower","close","standard",8),
]

obj = {
  "visual_reading": ("The arc opens on the felt ache (a guilt that will not close), lifts to Isaiah "
    "foreseeing healing through another's wounds, descends into the proof (the wounded, bruised, scourged "
    "Christ and the cross where it was borne 'in his own body'), then rises to the turn: the promise aimed "
    "at YOU, the believer healed, the cross finished at dawn, the open scarred hands, and the opening ache "
    "now closed. The cross (scene 6) is the hero bookending open and close so the Short lands on Christ."),
  "red_team_notes": ("Jaded Viewer risks: the stripes/scourge scenes (3,5) could blur or tip toward horror "
    "- held in Old-Master restraint, distinct framings. The 'Isaiah wrote' and 'apostle' beats are the trap "
    "(a scroll of text = Kling garbles letters) - solved by a VISION (2) and a GESTURE toward the cross (7), "
    "no writing anywhere. Scenes 1/14 are an intentional bookend; 6/9/11/12 are crucified-Christ frames in "
    "the back half - acceptable since the passage IS the cross, with varied framings (low-angle/mid/close/wide)."),
  "candidates": [
    {"title":"The Wound That Won't Close","scene_type":"single","arc_position":"opening-hook","framing":"close","purpose":"hook ache","rationale":"inner guilt made reverent, not gore","visible_elements":"bowed man, hand on chest","emotional_tone":"unhealed ache"},
    {"title":"Isaiah Sees It Coming","scene_type":"single","arc_position":"ot-echo","framing":"wide","purpose":"prophecy 700 yrs early","rationale":"prophet SEEING not writing","visible_elements":"aged prophet, lifted eyes, dim far figure","emotional_tone":"foresight"},
    {"title":"As A Lamb, Silent","scene_type":"single","arc_position":"ot-echo","framing":"close","purpose":"Isa 53:7 cited Acts 8:32","rationale":"the cited type, not a stretch","visible_elements":"a bound silent lamb, cross-shadow","emotional_tone":"willing sacrifice"},
    {"title":"In His Own Body, On The Tree","scene_type":"single","arc_position":"nt-gospel-link","framing":"low-angle","purpose":"the gospel-pivot hero","rationale":"the cross is where 1 Pet 2:24 lands","visible_elements":"crucified Christ, stripes, bowed head","emotional_tone":"finished"},
    {"title":"The Apostle Lays It On Christ","scene_type":"unified","arc_position":"nt-gospel-link","framing":"mid","purpose":"apostle applies Isaiah to Christ","rationale":"gesture toward cross, no scroll","visible_elements":"apostle, open hand toward dim cross","emotional_tone":"recognition"},
    {"title":"All We Like Sheep","scene_type":"unified","arc_position":"ot-echo","framing":"wide","purpose":"Isa 53:6 iniquity laid on Him","rationale":"the pericope's own next line","visible_elements":"strayed sheep, a laden figure, far cross","emotional_tone":"laid on Him"},
    {"title":"He Bare Our Sins","scene_type":"unified","arc_position":"theological-centre","framing":"mid","purpose":"the great exchange","rationale":"burdens as vignettes, no written record","visible_elements":"central Christ, broken chains, lifted yoke","emotional_tone":"exchange"},
    {"title":"Aimed At You","scene_type":"single","arc_position":"revelation","framing":"close","purpose":"the we->ye turn","rationale":"the pronoun made a gaze","visible_elements":"Christ's eyes turned to viewer","emotional_tone":"personal"},
  ],
  "scenes": scenes,
  "short_priority": [6,1,3,11,13,5,10,14],
  "hero_candidate": 6,
  "rationale": ("Hero = the cross (6): 1 Peter 2:24 lands the healing 'in his own body on the tree', so the "
    "gospel-pivot is the cross, not the most emotional frame. Kept 4 unified scenes (7,8,9,12) carrying the "
    "NT-link and the two OT echoes (Isa 53:6 sheep, Isa 53:7 lamb) so it reads as a study, not a slideshow. "
    "Rejected every scroll/written-text scene (Kling garbles letters) for a vision (2) and a gesture (7). "
    "Bookended the felt ache (1) with its healing (14)."),
  "beat_coverage": {"hook":[1],"point":[2,8],"proof":[3,4,5,6,7,9],"conviction":[10,11],"landing":[12,13,14]},
}
Path(".agent_bridge/responses/0001_7ab01b.txt").write_text(json.dumps(obj, ensure_ascii=False), encoding="utf-8")
print("wrote scene-plan response:", len(scenes), "scenes")
print("types:", dict(Counter(s["scene_type"] for s in scenes)))
print("nt-link:", [s["index"] for s in scenes if s["arc_position"]=="nt-gospel-link"])
print("ot-echo:", [s["index"] for s in scenes if s["arc_position"]=="ot-echo"])
print("framings:", dict(Counter(s["framing"] for s in scenes)))
