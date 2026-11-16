# Fix round after the red team (2026-11-16)

OWNER APPROVAL: "yes" to fixing the red-team mistakes, total Swirls+fix spend limit $42 (already spent $32.31). Your own cap is in your prompt; never exceed it.

## What to fix
Red-team reports (blind Fable): `_quality_uplift_20261116\redteam_films_A.md` (ep08, ep13, Jacob's Ladder, ep07) and `redteam_films_B.md` (ep10, ep11, Woman Behold). Owner page: `_REDTEAM_FILMS.html`. Fix the defects listed there for your films, most severe first. Owner decision on the blue/gold ink swirl: small movement is ACCEPTED as part of the look; only fix swirl movement where it is easy to see (ep10 end F09B, ep11 end F10/F10B) or where the shot is being redone anyway.

Priority defects (verified by the orchestrator by eye):
- ep11 F03 ~21.5 s: Jesus touches a leper. Luke 17:12 "stood afar off" - the lepers must stay at a distance; Jesus speaks from apart. BIBLE ERROR - top priority.
- ep11 F10 redraw: Samaritan became old/grey; must match his face on F06/F08/F09 (middle-aged, dark beard, balding as on F09).
- ep13 F09B ~92 s: offered hand deformed into a claw.
- ep07 F03B ~34-40 s: lone wrapped head-shaped bundle on an empty bier (no body).
- ep08 F05B ~39.7-44.7 s: Jesus "holding a balloon on a string"; Nathanael must match his reference (no red vest).
- Jacob's Ladder 43.6-50.2 s: borrowed ep08 page with header "SEQ: CAN ANY GOOD THING" + angel popping in beside Jesus -> replace with a JL-own page (spec's JL F08 option) or a clean alternative; drop the underline on words not spoken.
- ep10 F09B end: woman walks out of frame, ribbon flies off page; F08B bloom vanishes; Simon must look the same on F06 and F06B.
- Woman Behold (comic, $0): move the BEHOLD=HERE IS card off John's face; caption box off Jesus' mouth; gaze line must not start on Jesus' face; gold thread off John's throat; fix the 2 s half-empty page at 31.9-33.9 s; John consistency where possible.

## How (same recipe and rules as before)
- Swirls: follow `_quality_uplift_20261116\design_swirls\ROLLOUT_BRIEF.md` (spend control, OpenArt only, quote before every job, ledger, look at every still before animating, no fill, audio bit-identical, no "no bubble" negative clauses). Reuse each film's existing `uplift\` scripts (cut_uplift.py, marks_overlay.py, check_uplift.py, make_review.py) - re-cut with the replacement clips.
- Comic: the builder's tools are in `poc_comic_page\_ELEVATE\uplift\` and `...\woman_behold_john1926\visual\uplift_v1\`; $0 only.

## DISK - CRITICAL
Drive F: has under 1 GB free. Two corrupt files were already produced when it ran low.
- Put ALL intermediate files (frames, base cuts, temp renders, downloads before checking) under C: in `%TEMP%\uplift_fix\<film>\`, not on F:.
- Write only the final fixed film to F: as `<film uplift folder>\<name>_fix1.mp4` (do NOT overwrite the v1 uplift file), plus new/changed stills and kept clips.
- Before writing to F:, check free space; if under 400 MB, write the final to `%TEMP%\uplift_fix\<film>\` instead and say so.
- After writing, run a full decode check: `ffmpeg -v error -i <file> -f null -` must print nothing.

## Never
Touch FINAL_VIDEO.txt, publish\, ledgers other than spend_ledger rows, other films, or commit. Never auto-open files.

## Finish
Per film: gates (incl. audio MD5 = shipped, decode clean), frames you looked at for each fixed defect (first/last frame of new clips), update that film's `_REVIEW.html` (or write `_FIX1_REVIEW.html`) showing v1 vs fix1 side by side for each fixed moment, $ spent. Reply with per-film: fixed / not fixed (why), $ spent, file:/// links.
