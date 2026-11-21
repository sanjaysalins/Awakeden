# Film scan brief (2026-11-21, owner-approved, $0 - NO paid calls of any kind)
Goal: find every finished film with (1) backward/boomerang/ping-pong/freeze/zoom FILL, (2) AI slop, (3) words on screen that are not spoken, (4) a missing landing hold / abrupt end. Report only - change nothing.

Repo: F:\slk\PycharmProjects\JesusInTheBible (read CLAUDE.md "Locked decisions" for the owner's rules on fills, hero images, landing hold, captions).
Work ONLY in temp/scratch or this folder. Never edit any project file, never open files/browsers, never commit, never call any paid API/CLI (no hf.exe generate, no OpenArt, no ElevenLabs).

For EACH film you are given (video path + source folder):
1. FILL check: find the film's build/assemble script (in its source folder or the style engine it uses, e.g. poc_living_sketchbook/<film>/_*assemble*.py / retime*.py, livingpage spec + spec_report.json, Swirls _assembly). Find any slot where a clip is shorter than its slot and is reversed/boomeranged/ping-ponged/frozen/stretched (slow-mo >1.15x) or a Ken Burns push on a still. Also check by eye: extract frames at 2 fps over each suspicious slot and look for motion that reverses.
2. SLOP check: make 1-fps contact sheets of the whole film (ffmpeg fps=1, tile) and Read them; zoom (Read a full-size frame) on anything odd. Look for: morphing/changing people, extra or missing people, wrong anatomy (hands, long limbs, big heads), invented objects/light rays/streaks/blobs, text garbage, anachronisms (non-1st-century items), modesty problems, one character looking like another (e.g. a thief wearing a crown of thorns), style breaks.
3. TEXT check: any on-screen text (hook cards, gloss cards like "X = Y", quote cards, baked handwritten labels) whose words are NOT spoken at about that time. Burned captions that don't match the voice (transcribe with faster-whisper if available: `.venv\Scripts\python.exe -c "from faster_whisper import WhisperModel"`; small model, CPU).
4. END check: last spoken word time vs film end (need >= 3.0 s hold) and whether the last 0.25 s is near silent (ffmpeg astats or numpy on the audio).

Write ONE file per film: F:\slk\PycharmProjects\JesusInTheBible\_roadmap\film_scan_2026-11-21\<slug>.md with EXACTLY:
SLUG: <slug>
STATUS: POSTED|READY
VERDICT: CLEAN | MINOR | FIX | PULL
  (CLEAN = nothing a viewer would notice; MINOR = small, ok to post; FIX = must fix before posting / worth fixing if posted; PULL = Bible error or very visible slop)
FILLS: <list "time - clip - reverse/freeze/slowmo x/kenburns" or NONE>
SLOP: <list "time - what - low/med/high" or NONE>
TEXT: <list "time - on-screen words - not spoken/mismatch" or NONE>
END: hold=<s> silent_end=<yes/no>
FIX_IDEA: <one line: cheapest honest fix, and $0 or paid (how many new clips/stills)>

Then reply with a 1-line-per-film table only.
