# Phase 1C — Stylized "teen+ reach" stills bake-off (PLAN)

Goal: test the popular animation style-families the LLMs recommended, to see if any
gives Awakeden a *fresh, broad-reach* look without becoming AI slop OR becoming
irreverent. Slots directly into the existing FACES.html bake-off (same subjects,
same model) so it is apples-to-apples with the 6 looks already tested.

## The 5 looks (DESCRIPTIVE strings — no studio/IP names, per cross-LLM warning)

| Key | Lane it targets | Prompt string (style prefix) |
|-----|-----------------|------------------------------|
| **S** | Comic-3D hybrid (Spider-Verse) | stylized 3D comic-book animation, bold black ink outlines, halftone dot shading, subtle chromatic-aberration offset, graphic flat color blocks, dynamic cinematic comic framing, non-photoreal CGI |
| **A** | Painterly 2.5D (Arcane/Fortiche) | painterly 2.5D animated-series style, visible textured brushwork over sculpted 3D forms, rich hand-painted surfaces, dramatic volumetric side light, gritty cinematic fantasy-drama mood |
| **P** | Painterly stylized 3D (DreamWorks/Puss) | painterly stylized 3D animated film still, soft hand-painted textures and visible brush strokes, expressive stylized features, warm cinematic lighting, storybook depth, never plastic-smooth |
| **N** | Cinematic modern anime (Ufotable) | modern high-quality 2D cinematic anime film still, clean sharp character art, dramatic cinematic lighting, detailed painted background, fluid expressive face, serious mature tone |
| **C** | Folk-art 2D (Cartoon Saloon/Wolfwalkers) | hand-drawn 2D folk-art animation, flat geometric stylization, decorative medieval-illumination patterning, muted earthy palette, reverent storybook composition |

## Anti-slop + anti-childish + reverence tail (every prompt)
"mature reverent dignified tone, period-accurate ancient Near East and Egypt, no
modern objects; NOT childish, NOT a cute mascot, NOT preschool cartoon, no plastic
toy sheen, no goofy expression, emotionally truthful face"

## Subjects (reuse 2 of the 3 — the decisive ones)
- `joseph_pit`  — emotion + morph stress test (tears, open mouth, wide eyes)
- `christ_face` — THE reverence gate; if a look makes Christ read cartoonish/cute, that look is OUT

(joseph_weep dropped for this round — weeping already reads well across every medium.)

## Cost
5 looks x 2 subjects = 10 stills x ~7 cr = **~70 cr**.
Budget after motion (~75 cr spent): ~143 cr left -> ~73 cr reserve kept for motion on winners.
(Add joseph_weep back = +5 stills = +~35 cr if wanted.)

## Adversarial reflection
1. **Reverence is the real risk** (not slop). Anime/comic/3D-cartoon can trivialize a
   sacred subject. Mitigation: hard anti-childish + reverent guard; Christ-face is the
   gate — cool Joseph + cute Christ = look rejected.
2. **IP-token drift** (cross-LLM flag): descriptive strings only, no brand names. Done.
3. **Strategic fork** (the dissenting LLM, correct): these ride the *popular teen* lane,
   the opposite of the premium Baroque/charcoal lane that already makes Awakeden stand
   out in apologetics. The stills inform the bet; the USER owns which bet to make.
4. **Motion morph**: flatter/graphic looks (comic, folk-art, anime) may actually survive
   Kling BETTER than photoreal (less realism to break). The charcoal/ink/clay motion
   clips rendering now are the leading indicator before we spend motion credits here.
5. **Budget honesty**: ~70 cr, no fabricated multipliers; keeps a motion reserve.

## Execute
`python render_styles2.py`  (idempotent; writes to faces/ as S_*/A_*/P_*/N_*/C_*__<subject>.png
so the existing build_gallery_faces.py picks them up once its LOOKS list is extended).
