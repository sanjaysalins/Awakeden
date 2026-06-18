import json
from collections import Counter
from pathlib import Path

def S(i,slug,title,st,arc,fr,purpose,rat,vis,tone,subj,mood,jv,macros,vign,pacing,role,kind,prio=0):
    return {"index":i,"slug":slug,"title":title,"scene_type":st,"arc_position":arc,"framing":fr,
            "purpose":purpose,"rationale":rat,"visible_elements":vis,"emotional_tone":tone,
            "subject_block":subj,"mood_block":mood,"jesus_variant":jv,"priority":prio,
            "macro_elements":macros,"vignettes":vign,"pacing":pacing,"viral_role":role,"shot_kind":kind}

scenes=[
 S(1,"the-shaking-heads","The Shaking Heads","single","opening-hook","close",
   "Hook: the mockery made visible.","Jeering faces at the cross's foot — the arresting scorn.",
   "jeering first-century faces shaking their heads at the foot of a cross, lips curled.","cold scorn",
   "a tight cluster of jeering first-century Judean faces at the foot of a rough wooden upright, the heads tilted and shaken mid-scorn, lips curled and shot out in derision, eyes narrowed upward in contempt, weathered ancient skin and coarse dust-toned robes, the whole sunk in a brown-black ground with hard low light on the nearest sneer",
   "atmosphere of a crowd's scorn","passion",["a curled sneering lip","a shaken head","a pointing weathered hand","the dim cross upright"],[],
   "controlled","hook-open","standard",2),
 S(2,"a-script-a-thousand-years-old","A Script, A Thousand Years Old","single","ot-echo","wide",
   "Point: the mockery was foretold in Psalm 22.","Show the psalmist SEEING it, not a scroll (no garbled text).",
   "an aged psalmist gazing toward a dim distant mocked figure on a far rise; no text.","ancient foresight",
   "an aged first-century Hebrew psalmist seen from the side in a coarse mantle, his lined face lifted and his eyes wide toward a dim far-off rise where a single bound figure stands surrounded by tiny shadowed mockers, his weathered hand pressed to his breast, the foreground rocks dark, the distance hazed in dust and prophetic light, no writing or scroll present anywhere",
   "atmosphere of foresight reaching across centuries","passion",["the psalmist's lifted eyes","the hand at the breast","the dim mocked figure","the fold of the mantle"],[],
   "slower","build","standard"),
 S(3,"they-shoot-out-the-lip","They Shoot Out The Lip","single","central-conflict","close",
   "Proof (Ps 22:7): the curled lip of scorn.","A single mocking face, restrained not cartoonish.",
   "a single mocking first-century face filling the view, lower lip thrust out and curled.","derision, close",
   "a single mocking first-century Judean face filling the view, the lower lip thrust out and curled in derision, teeth just bared, the eyes lifted in cold scorn, weathered sun-worn skin in hard raking light, the rest of the head sunk in deep shadow",
   "atmosphere of a face set in scorn","passion",["the curled thrust lip","the cold lifted eyes","the raking light on skin","the shadowed edge"],[],
   "controlled","build","standard"),
 S(4,"the-passers-by-wag-their-heads","The Passers-By Wag Their Heads","unified","public-misunderstanding","wide",
   "Proof (Matt 27:39): the wagging heads.","The crowd at the cross + the echoing vignettes.",
   "a knot of passers-by at the cross wagging their heads; the dim crucified Christ above; vignettes.","mob scorn",
   "a wide view at the foot of a tall wooden cross, a knot of passers-by with heads wagged in scorn and dust-toned robes, the crucified Christ robed at the waist dim and small above them against a darkening sky, subtle background vignettes fading into shadow suggesting more wagging heads, a jabbing finger, a turned scornful back, and an aged psalmist's hand half-dissolved in the dark",
   "atmosphere of a passing crowd's contempt","passion",["the wagged heads","a jabbing finger","the small dim cross","the dust-toned robes"],
   ["more wagging heads","a jabbing finger","a turned scornful back","an aged psalmist's hand"],
   "controlled","build","standard"),
 S(5,"the-rulers-sneer","The Rulers Sneer","single","central-conflict","mid",
   "Proof (Matt 27:41): the chief priests mocking.","The rich-robed rulers in smug contempt.",
   "robed rulers in rich layered robes, faces lifted in smug contempt, a finger jabbed up.","smug contempt",
   "two robed first-century religious rulers in rich layered robes and prayer fringes seen close, their faces lifted in smug contempt toward an unseen cross above, one with a finger extended upward in accusation, the other's lip curled, dim onlookers half-dissolved behind them, warm low light on the smug brow against deep shadow",
   "atmosphere of smug religious contempt","passion",["the smug lifted face","the jabbing finger","the prayer fringes","the rich layered robe"],[],
   "controlled","build","standard"),
 S(6,"he-trusted-in-god","He Trusted In God","single","theological-centre","mid",
   "Proof: the crucified Christ enduring the recorded taunt.","Christ on the cross, bowed, enduring, reverent.",
   "the crucified Christ enduring on the cross, head bowed, against a dark sky.","borne scorn",
   "the crucified Christ on a rough wooden cross seen at mid distance against a darkened noon sky, the thorn-crowned head bowed low in endurance, the body robed at the waist, the arms taut along the beam, a faint sorrowful stillness on the face, the small dim forms of jeering figures at the foot",
   "atmosphere of scorn silently borne","passion",["the bowed thorn-crowned head","a nailed hand","the dark noon sky","the taut arm"],[],
   "slower","build","standard",3),
 S(7,"the-king-who-would-not-come-down","The King Who Would Not Come Down","single","nt-gospel-link","low-angle",
   "THE HERO — the gospel-pivot: the King who stayed on the cross.","Iconic reverent crucifixion; bookends the cut.",
   "the crucified Christ on the cross, head bowed in sovereign stillness, faint light behind.","finished, sovereign",
   "the crucified Christ lifted on a rough wooden cross seen from a low reverent angle against a darkening sky, the thorn-crowned head bowed in sovereign stillness, the body robed at the waist, the arms taut along the beam, a faint pale light breaking behind the dark hill, the small forms of mockers dim and turned away at the foot, the very top of the cross bare and plain with no inscription board and no lettering",
   "atmosphere of a King who stays, sovereign and still","passion",["the bowed thorn-crowned head","a nailed open hand","the still robed body","the grain of the beam"],[],
   "slower","climax","hero",1),
 S(8,"unwilling-witnesses","Unwilling Witnesses","unified","ot-echo","wide",
   "Proof: the scorners unknowingly reciting the prophecy.","Mockers foreground dark, the luminous Christ beyond.",
   "the dark backs of jeering mockers in front; the luminous crucified Christ beyond; vignettes.","unwitting testimony",
   "the dark backs and raised arms of a jeering crowd filling the foreground, and beyond them the crucified Christ small and luminous on the cross under a pale dusk sky, the mockers unknowingly framing him, subtle background vignettes fading into shadow suggesting an open scornful mouth, a raised fist, a far rough cross, and an aged psalmist's lifted hand half-dissolved in the dark",
   "atmosphere of enemies who testify without knowing","passion",["the dark jeering backs","a raised fist","the luminous distant cross","the pale dusk sky"],
   ["an open scornful mouth","a raised fist","a far rough cross","an aged psalmist's lifted hand"],
   "controlled","pivot","standard"),
 S(9,"if-thou-be-the-son-of-god","If Thou Be The Son Of God","single","personal-confrontation","low-angle",
   "Conviction: the 'come down' taunt hurled up.","A mocker jeering up at the cross; Christ silent above.",
   "a mocker's open-mouthed jeer hurled upward, the cross looming above.","the taunt, hurled",
   "a single first-century mocker seen from a low angle, the head thrown back and the mouth open mid-jeer toward a rough cross looming dark above against a bruised sky, one arm flung upward in derision, the dim crucified figure small and still at the top of the beam, hard light on the jeering throat and jaw against deep shadow",
   "atmosphere of a taunt flung at the silent cross","passion",["the open jeering mouth","the flung-up arm","the looming dark cross","the small still figure above"],[],
   "faster","build","standard"),
 S(10,"he-could-have-come-down","He Could Have Come Down","unified","nt-gospel-link","mid",
   "Conviction: restrained power — He chose to stay.","Christ central + restrained-power vignettes (half-dissolved).",
   "the crucified Christ central and dominant; dim restrained power vignettes around.","held power",
   "the crucified Christ at the centre and clearly dominant on the cross, calm and unbroken against a dark sky, and faint and barely-there in the surrounding shadow the power he holds back, subtle background vignettes fading into shadow suggesting dim ranks of restrained angelic figures, a held and unfallen bolt of light, the unbroken iron nails, and a steady unshaken face",
   "atmosphere of sovereign power willingly restrained","passion",["the calm unbroken face","a nailed hand","the dark sky","dim restrained ranks"],
   ["dim ranks of restrained angelic figures","a held unfallen bolt of light","the unbroken iron nails","a steady unshaken face"],
   "slower","pivot","standard"),
 S(11,"bearing-the-scorn","Bearing The Scorn","single","emotional-turning","close",
   "Conviction: Christ bears the scorn with willing love.","Christ's face close, enduring with love not pain.",
   "a close reverent view of the crucified Christ's face, eyes lowered in willing endurance.","willing endurance",
   "a close reverent view of the crucified Christ's face inclined and the eyes lowered in willing endurance rather than pain, a thorn-marked brow, the jaw set in quiet resolve, warm light catching one cheek against deep shadow, the grain of the dark beam just behind",
   "atmosphere of scorn borne in willing love","passion",["the lowered willing eyes","the thorn-marked brow","the set jaw","light on one cheek"],[],
   "slower","build","standard",4),
 S(12,"the-king-they-told-to-come-down","The King They Told To Come Down","single","revelation","mid",
   "Landing: the King who stayed.","The crucified Christ as King, a faint regal light, still on the cross.",
   "the crucified Christ on the cross with a faint regal stillness, the scorn quieting around.","the King who stays",
   "the crucified Christ on the cross seen at mid distance, the thorn-crowned head lifted slightly in a faint regal stillness, the body robed at the waist, a warm break of light beginning behind the dark hill, the jeering figures at the foot now small and falling into shadow, the cross reading like a throne",
   "atmosphere of a mocked King revealed as King","passion",["the lifted thorn-crowned head","the warm break of light","the throne-like cross","the dim falling mockers"],[],
   "slower","close","standard",5),
 S(13,"for-the-very-people-throwing-it","For The Very People Throwing It","unified","human-response","wide",
   "Landing: He bore it FOR the mockers.","Christ above looking down on the upturned faces; vignettes of a softening.",
   "the crucified Christ above looking down on upturned scornful faces; a softening; dawn.","mercy for scorners",
   "the crucified Christ on the cross above looking down with mercy on a field of upturned first-century faces below, some still scornful and one beginning to soften and lower its eyes, warm dawn light beginning across the quiet ground, subtle background vignettes fading into shadow suggesting a clenched fist loosening, a bowed shamed head, an open empty hand, and a far gathered company in dawn light",
   "atmosphere of mercy poured on the mockers","passion",["the merciful downward gaze","a softening upturned face","the warm dawn ground","a loosening fist"],
   ["a clenched fist loosening","a bowed shamed head","an open empty hand","a far gathered company in dawn light"],
   "slower","close","standard",6),
 S(14,"come-to-the-one-who-would-not-come-down","Come To The One Who Would Not Come Down","single","closing-devotional","wide",
   "Landing CTA: the cross at dawn, the King who stayed.","The cross against a widening dawn — the invitation.",
   "the cross against a widening gold dawn, the still King upon it, an open invitation.","open invitation",
   "the rough cross standing against a widening gold dawn, the thorn-crowned Christ still and reverent upon it, warm light breaking from behind the upright beam across a quiet land, the hill's crest in soft shadow, the jeering crowd gone, the scene hushed and open in dawn light",
   "atmosphere of an open invitation to the King who stayed","passion",["the lit upright beam","the still reverent figure","the gold dawn horizon","the hushed empty ground"],[],
   "slower","close","standard",7),
]
obj={
 "visual_reading":("The arc opens on the crowd's scorn (the shaking heads), lifts to the psalmist who foresaw "
   "it, descends through the curled lip / wagging passers-by / sneering rulers into the enduring Christ, "
   "turns on 'He could have come down' (held power) and the scorn borne in love, and lands on the mocked "
   "King who stayed — the cross at dawn, an open invitation. Hero #7 (the cross) bookends so it lands on Christ."),
 "red_team_notes":("Jaded Viewer risks: many jeering-face scenes (1,3,5,9) could blur into one angry crowd — "
   "varied framings (close/mid/low-angle/wide) and the turn to mercy (13) offset it. The 'script/psalm' beat "
   "is the writing trap — solved by a VISION (2), no scroll/text. Back half is crucifixion-heavy (6,7,10,11,12,14) "
   "but that is the passage; framings vary and the mocker scenes anchor the front half."),
 "candidates":[
   {"title":"The Shaking Heads","scene_type":"single","arc_position":"opening-hook","framing":"close","purpose":"hook scorn","rationale":"the arresting mockery","visible_elements":"jeering faces, shaken heads","emotional_tone":"scorn"},
   {"title":"A Script A Thousand Years Old","scene_type":"single","arc_position":"ot-echo","framing":"wide","purpose":"the prophecy","rationale":"psalmist SEEING not writing","visible_elements":"aged psalmist, dim mocked figure","emotional_tone":"foresight"},
   {"title":"The Rulers Sneer","scene_type":"single","arc_position":"central-conflict","framing":"mid","purpose":"Matt 27:41","rationale":"the religious contempt","visible_elements":"robed rulers, jabbing finger","emotional_tone":"smug"},
   {"title":"The King Who Would Not Come Down","scene_type":"single","arc_position":"nt-gospel-link","framing":"low-angle","purpose":"the hero cross","rationale":"the King who stayed = gospel-pivot","visible_elements":"crucified Christ, bowed head","emotional_tone":"sovereign"},
   {"title":"Unwilling Witnesses","scene_type":"unified","arc_position":"ot-echo","framing":"wide","purpose":"scorners recite prophecy","rationale":"enemies testify unknowing","visible_elements":"dark mockers, luminous Christ","emotional_tone":"testimony"},
   {"title":"He Could Have Come Down","scene_type":"unified","arc_position":"nt-gospel-link","framing":"mid","purpose":"held power","rationale":"He chose to stay","visible_elements":"Christ + restrained ranks","emotional_tone":"held power"},
   {"title":"For The Very People Throwing It","scene_type":"unified","arc_position":"human-response","framing":"wide","purpose":"mercy for mockers","rationale":"He bore it for them","visible_elements":"upturned faces, a softening","emotional_tone":"mercy"},
 ],
 "scenes":scenes,
 "short_priority":[7,1,6,11,14,3,5,13],
 "hero_candidate":7,
 "rationale":("Hero = the cross (7): the mocked King who would not come down is the gospel-pivot. Kept 4 unified "
   "scenes (4,8,10,13) carrying the NT-link and the two OT echoes (the psalmist #2, the unwilling-witnesses #8 "
   "reciting Ps 22). Rejected any scroll/written-script scene (Kling garbles letters) for a vision (#2). "
   "Front-loaded the mocker faces; the back half is the enduring/merciful King."),
 "beat_coverage":{"hook":[1],"point":[2],"proof":[3,4,5,6,8],"conviction":[9,10,11],"landing":[12,13,14]},
}
Path(".agent_bridge/responses/0001_c5184c.txt").write_text(json.dumps(obj,ensure_ascii=False),encoding="utf-8")
print("wrote",len(scenes),"scenes")
print("types:",dict(Counter(s["scene_type"] for s in scenes)))
print("nt-link:",[s["index"] for s in scenes if s["arc_position"]=="nt-gospel-link"])
print("ot-echo:",[s["index"] for s in scenes if s["arc_position"]=="ot-echo"])
print("framings:",dict(Counter(s["framing"] for s in scenes)))
