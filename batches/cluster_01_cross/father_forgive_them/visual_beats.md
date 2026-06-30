# Visual beat-sheet — "Father, forgive them" (Luke 23:34)
Style: inked graphic-novel motion-comic · 9:16 short · ref-locked to ref_library anchors
Audio: 57.15s, 8 narration turns. Panels follow the locked narration in order (LV-G7 reading order).

| # | beat (audio) | t | panel concept (inked still) | ref_library anchors | furniture | motion |
|---|--------------|---|-----------------------------|---------------------|-----------|--------|
| 1 | HOOK | 0–10.3 | WIDE Golgotha: the cross, nailed hands prominent; Roman soldiers crouched at the foot dividing a garment; black storm sky | JESUS(passion), CROSS, GOLGOTHA, ROMAN_SOLDIERS | caption box: "Nails through his hands. Soldiers gambling for his clothes." | slow push to the nailed hands |
| 2 | POINT | 10.3–17 | Jesus on the cross, head lifted, lips parted — about to speak; soldiers small below | JESUS(passion, on cross) | caption: "As they divide his clothing, Jesus prays for the very people putting him to death." | push to his face |
| 3 | [JESUS] prayer | 17–21.7 | CLOSE on Jesus' face, eyes toward heaven — the red-letter moment | JESUS(passion, close) | 🔴 red-letter speech bar: "Father, forgive them; for they know not what they do." | hold, faint light shift |
| 4 | Luke + Scripture | 21.7–26 | the dice/lots tumbling in the dust + a soldier's hand; the seamless garment heaped | ROMAN_SOLDIERS (hands), dice/lots | caption: "Luke records it as they gambled:" + 📖 Scripture bar: "And they parted his raiment, and cast lots." | dice tumble / hard-cut to hand |
| 5 | intercession | 26–31.6 | Jesus' open nail-pierced hand catching light — mercy, not a fist | JESUS(passion), ROMAN_NAIL (pierced hand) | caption: "It does not excuse the sin — it intercedes for the sinner." | light blooms on the open palm |
| 6 | CONVICTION | 31.6–42 | the cross seen from below with a kneeling figure (us) in shadow; one shaft of light | JESUS(passion), CROSS | caption: "The sin that put him there was ours too — and the One who prayed for his killers still lives to intercede." | push up the cross toward the light |
| 7 | LANDING (hero) | 42–57 | gospel-pivot HERO: the RISEN Christ in warm light, pierced hand reaching toward the viewer — mercy held out | JESUS(resurrection, hero) | caption: "While we were yet sinners, Christ died for us. Come, and receive it by faith." | hold on the risen face + reaching hand (linger close) |

## Asset audit (inked style)
- The banked Cross stills/clips are **baroque-oil** (NBP), so they do NOT match the chosen inked look — these 7 panels render **fresh inked**.
- All identity/world is **ref-locked** to existing `ref_library` anchors (JESUS, CROSS, GOLGOTHA, ROMAN_SOLDIERS, ROMAN_NAIL) — no new character design, just new scene stills.
- Panel 6 may reuse panel 2's still (cross) with a different crop/caption → possibly 6 unique stills, not 7.

## Gate pre-checks (LANDSCAPE_VALIDATION siblings for shorts)
- LV-G1 ≥1 animated per grid: every panel animated ✓
- LV-G3 no dup clip: 7 distinct panels (watch panel 6/2 reuse) ✓
- LV-G7 reading order = narration order ✓
- LV-G11 never animate writing: the Scripture/red-letter text lives in PIL furniture (never rendered into the still), and no scroll/titulus is generatively animated ✓
- Doctrine: God/Father never depicted (the prayer is TO the Father — show only Jesus + light); lands on the risen Christ ✓

## Pending (this stage)
1. Mechanics map (driver + spec + inked renderer + animate) — agent running.
2. Exact `hf generate cost` quote for N stills + N clips — BEFORE any render.
