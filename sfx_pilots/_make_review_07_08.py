"""Build a full-res still-review gallery for Psalm 22 shorts #07 + #08, with my QC notes."""
import os, html

ROOT = r"C:\Users\sanjay\PycharmProjects\JesusInTheBible\longform\02_Psalm_22_Song_From_The_Cross\v1\shorts"
OUT = os.path.join(ROOT, "_REVIEW_07_08_stills.html")

# status: ok | watch | redo
NOTES = {
 "07_The_Body_Foretold": [
  ("01_out-of-joint.png","Out of Joint","ok","Crucified body, arms stretched along the beam, head bowed. Clean hook."),
  ("02_the-king-who-wrote-it.png","The King Who Wrote It","ok","David at his scroll by lamp, with vignettes (cross on the hill, the dead Christ, mourners). Strong."),
  ("03_poured-out-like-water.png","Poured Out Like Water","ok","Gaunt dying face, a tear and a blood trickle. Haunting, on-theme."),
  ("04_crushed-in-your-place.png","Crushed In Your Place (HERO)","ok","Velazquez-style crucifixion, INRI titulus. The hero that closes the cut - excellent."),
  ("05_i-may-tell-all-my-bones.png","I May Tell All My Bones","ok","Gaunt torso, ribs countable. Matches the verse. (faint painterly head-light)"),
  ("06_they-look-and-stare.png","They Look and Stare","ok","REDONE v2 (period fix): weathered ANCIENT Judean crowd in coarse robes/head-coverings, a Roman helmet + spear, ancient buildings - modern look fixed. (one central figure reads slightly Christ-like but is crowd-scale)"),
  ("07_hung-by-the-arms.png","Hung by the Arms","ok","REDONE v2 (period fix): weathered Old-Master Christ, the raised arm + distended shoulder dominant, reverent. Modern look fixed."),
  ("08_whom-they-pierced.png","Whom They Pierced","ok","REDONE: the pierced-side torso dominates, only a few upturned faces + a spear - much less cluttered."),
  ("09_a-thousand-years-apart.png","A Thousand Years Apart","watch","Diptych: David + vignettes (left) | light band | a floating Christ bust (right). Works, but the right side is a plain floating bust. Optional re-roll to a David-vs-distant-cross split (like #08's version)."),
  ("10_wounded-for-us.png","Wounded for Us","ok","Scourged back with the stripes of a flogging. Strong (Isa 53:5)."),
  ("11_the-marks-of-one.png","The Marks of One","ok","REDONE v2 (horror fix): a calm REVERENT Old-Master Christ + the nail-pierced hand on the beam, soft devotional light, less blood. Horror tone fixed."),
  ("12_crushed-in-your-place-unified.png","Crushed So Another Goes Free","ok","REDONE v2 (period fix): the freed man is now an AGED ancient labourer in a coarse tunic (clearly ordinary, not modern, not a 2nd Christ), broken shackles on the ground. Fixed."),
  ("13_to-bring-you-home.png","To Bring You Home","ok","A lit doorway at dusk, olive tree, the path home. Warm and inviting."),
  ("14_come-to-him.png","Come to Him","ok","Christ's face with the cross + a sunset glow. Calm CTA close."),
 ],
 "08_I_Thirst": [
  ("01_two-words-on-a-cross.png","Two Words on a Cross","ok","Parched thorn-crowned face, head on the beam. Strong hook. (faint head-light)"),
  ("02_the-king-who-wrote-it.png","The King Who Wrote It","ok","David over his scroll by lamp. Clean."),
  ("03_dried-like-a-potsherd.png","Dried Like a Potsherd","ok","Broken potsherd + a parched hand in cracked earth. Literal for the verse."),
  ("04_the-tongue-cleaveth.png","The Tongue Cleaveth","ok","REDONE v2 (NSFW fix): a solemn AGED Old-Master face, eyes closed, the dry parted mouth/tongue held in quiet reverent thirst. Modest, period-authentic."),
  ("05_the-dust-of-death.png","The Dust of Death","ok","REDONE: a man fallen face-down on cracked grey dust, cheek to the earth - clearer 'dust of death'."),
  ("06_the-cry-recorded.png","The Cry Recorded","ok","Crucified Christ, arms nailed wide, first light. (bowed head hides the parted lips - minor)"),
  ("07_a-thousand-years-apart.png","A Thousand Years Apart","ok","Strong diptych: David + light band + a distant cross + the potsherd. All vignettes present."),
  ("08_who-made-every-river.png","Who Made Every River","ok","REDONE: the central Christ now dominates; the waters are dim/half-dissolved in shadow as intended."),
  ("09_living-water-offered.png","Living Water Offered","ok","Jesus at the well, the woman, waterpot + cup/crowd/river vignettes. Good John 4 ground."),
  ("10_hanging-there-with-nothing.png","Hanging There With Nothing","ok","Full stripped crucifixion, empty open hands, dry hill. Clean."),
  ("11_water-from-the-rock.png","Water from the Rock","ok","Moses strikes the rock, thirsting people drink. Strong OT echo (1 Cor 10:4)."),
  ("12_every-one-that-thirsteth.png","Come, Every One That Thirsteth","ok","Open spring, thirsty figures with empty vessels. Warm Isaiah 55 echo."),
  ("13_drink-and-never-thirst.png","Drink and Never Thirst","ok","Man drinking at the spring, the cross mirrored in the water (border defect fixed on retry; now full-bleed)."),
  ("14_that-water-is-himself.png","That Water Is Himself (HERO)","ok","Crucified Christ, living water from the pierced side, dawn (John 19:34). The hero - perfect."),
 ],
}

COLOR = {"ok":"#2e7d32","watch":"#b8860b","redo":"#c62828"}
BADGE = {"ok":"KEEP","watch":"OPTIONAL","redo":"REDO"}

cards = []
for short, items in NOTES.items():
    title = short.replace("_"," ")
    cards.append(f'<h2 style="margin:32px 8px 8px;font-size:26px">{html.escape(title)}</h2>')
    cards.append('<div class="grid">')
    for fn,scene,st,note in items:
        rel = f"{short}/visual/nbp/{fn}"
        c = COLOR[st]
        cards.append(f'''
        <div class="card" style="border-color:{c}">
          <a href="{rel}" target="_blank"><img src="{rel}" loading="lazy"></a>
          <div class="meta">
            <div class="hd"><span class="num">{fn[:2]}</span> {html.escape(scene)}
              <span class="badge" style="background:{c}">{BADGE[st]}</span></div>
            <div class="note">{html.escape(note)}</div>
          </div>
        </div>''')
    cards.append('</div>')

doc = f'''<!doctype html><html><head><meta charset="utf-8">
<title>Psalm 22 #07 + #08 - still review</title>
<style>
 body{{background:#1a1a1a;color:#eee;font-family:Segoe UI,Arial,sans-serif;margin:0;padding:20px}}
 h1{{font-size:30px;margin:8px}}
 .lead{{color:#bbb;margin:8px;max-width:900px;line-height:1.5}}
 .grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:18px;padding:8px}}
 .card{{background:#222;border:3px solid;border-radius:10px;overflow:hidden;display:flex;flex-direction:column}}
 .card img{{width:100%;display:block;cursor:zoom-in}}
 .meta{{padding:10px 12px}}
 .hd{{font-size:15px;font-weight:600;margin-bottom:6px}}
 .num{{display:inline-block;background:#444;border-radius:5px;padding:1px 7px;margin-right:4px;font-size:13px}}
 .badge{{float:right;color:#fff;font-size:11px;font-weight:700;padding:2px 8px;border-radius:10px;letter-spacing:.5px}}
 .note{{font-size:13px;color:#ccc;line-height:1.45}}
</style></head><body>
<h1>Psalm 22 shorts - still review: #07 The Body Foretold &amp; #08 I Thirst</h1>
<p class="lead">Click any image to open it full-size in a new tab. Badge = my recommendation:
<b style="color:#2e7d32">KEEP</b> = good as-is &nbsp;
<b style="color:#b8860b">OPTIONAL</b> = works, could re-roll &nbsp;
<b style="color:#c62828">REDO</b> = clear defect, should re-render.
<br><b>My read: one clear REDO (#07 scene 06), two optional re-rolls (#07 scene 09 + 12). #08 is clean.</b>
Tell me which you want done and I'll re-render the still, re-animate that clip, and rebuild the cut (re-assemble + SFX + caption).</p>
{''.join(cards)}
</body></html>'''

open(OUT,"w",encoding="utf-8").write(doc)
print("wrote", OUT)
