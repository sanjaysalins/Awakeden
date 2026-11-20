"""Apply convergent red-team r2 fixes (Fable, Sonnet, Claude, Codex; Grok out of credit)."""
from pathlib import Path

P = Path(__file__).resolve().parents[2]
pub = P / "publish"


def edit(path, pairs):
    t = path.read_text(encoding="utf-8")
    for a, b in pairs:
        assert t.count(a) == 1, (path.name, a)
        t = t.replace(a, b)
    path.write_text(t, encoding="utf-8")
    print("fixed", path.name)


PLAIN = ("Job did not name Jesus. He described what only God does. "
         "In the film, Job's two lines are said in plain English; the KJV words are quoted here. "
         "The picture of Job by the sea is an illustration: he was not there.")
long_pairs = [
    ('"Lo, he goeth by me, and I see him not." (Job 9:11, KJV)',
     '"Lo, he goeth by me, and I see him not." (Job 9:11, KJV: He goes past me, and I do not see Him.)'),
    ("Job did not name Jesus. He described what only God does.\n", PLAIN + "\n"),
    (": He feels our weakness.", ': He feels our weakness. He "suffered being tempted" (Hebrews 2:18, KJV).'),
    ("1 Timothy 2:5; Hebrews 4:15.\n\nFind Jesus", "1 Timothy 2:5; Hebrews 2:18; Hebrews 4:15.\n\nFind Jesus"),
]
edit(pub / "youtube_short.md", long_pairs + [
    ("Read it: Job 9:8-11, 9:32-33; Mark 6:45-51; 1 Timothy 2:5; Hebrews 4:15.",
     "Read it: Job 9:8; Job 9:11; Job 9:32-33; Mark 6:45-51; 1 Timothy 2:5; Hebrews 2:18; Hebrews 4:15."),
])
edit(pub / "facebook.md", long_pairs)
for f in ["tiktok.md", "instagram.md"]:
    edit(pub / f, [("1 Timothy 2:5; Hebrews 4:15 (KJV).", "1 Timothy 2:5; Hebrews 2:18; Hebrews 4:15 (KJV).")])
ig = pub / "instagram.md"
t = ig.read_text(encoding="utf-8")
if "## ALT_TEXT" not in t:
    ig.write_text(t.rstrip("\n") + "\n\n## ALT_TEXT\nSepia comic-book short: Job on a rock by a stormy sea, then Jesus walking on the water toward His followers in a boat (Job 9:8; Mark 6:45-51).\n", encoding="utf-8")

ROOT = r"F:\slk\PycharmProjects\JesusInTheBible\batches\cluster_05_prophecy\job_sea_short"
c = P / "UPLOAD_CHECKLIST.md"
edit(c, [
    ("Paste ONLY from `publish/PUBLISH_INDEX.html` (every field has a copy button, including the YouTube pinned comment). No other file is a paste source.",
     "Paste ONLY from `publish/PUBLISH_INDEX.html` (every field has a copy button, including the YouTube PINNED_COMMENT and the Instagram ALT_TEXT). No other file is a paste source."),
    ("Use the SAME moment on all four platforms.",
     "Write it as local date + time + time zone + UTC (e.g. 2026-12-01 18:00 GMT = 18:00 UTC). Use the SAME moment on all four, and check each scheduler shows it.\n"
     "**Do not schedule anything until the release line AND the rights lines below are filled and signed.**"),
    ("## 1. Before uploading (all platforms)\n",
     "## 1. Before uploading (all platforms)\n"
     f"- [ ] Open PowerShell and go to the pack folder first: `cd {ROOT}`\n"
     "- [ ] Paste page fresh? Open `publish/PUBLISH_INDEX.html`: the YouTube TITLE must read exactly \"Jesus Walks on Water. Job Said Only God Does.\" and description line 1 must start \"Long ago, a man named Job\". If not, rebuild it (`.venv\\Scripts\\python.exe cli_publish.py <this folder> --index`) and STOP until it matches.\n"
     "- [ ] Accounts: logged in as **Salt and Light Kingdom** on all four (the YouTube channel is shared with other work). Facebook posts to the Page, not a personal profile.\n"),
    ("- [ ] Rights, record who checked and the date here: ______. Voice and score: ElevenLabs (paid plan with commercial use). Stills: OpenArt (paid plan). Animation: Grok Imagine. Poster art: Antigravity (Google). Sound effects: the project's own sound library. If any one is not cleared for all four platforms, STOP and ask the owner.",
     "- [ ] Rights (fill each; if any one is not cleared for all four platforms, STOP and ask the owner):\n"
     "  - Voice + score, ElevenLabs, plan + commercial terms checked by ______ on ______\n"
     "  - Stills, OpenArt, plan + commercial terms checked by ______ on ______\n"
     "  - Animation, Grok Imagine, plan + commercial terms checked by ______ on ______\n"
     "  - Poster art, Antigravity (Google image tool), terms checked by ______ on ______\n"
     "  - Sound effects, project sound library, licence checked by ______ on ______\n"
     "  - KJV text: Crown rights apply in the UK (short quotes are normally allowed); checked by ______\n"
     "  - Scrub every frame of the video AND the poster for any tool watermark or logo."),
    ("- [ ] Subtitles: upload `publish/captions_locked.srt` as English. Then play it once with CC ON and once with CC OFF: no line may hide the burned-in words badly.",
     "- [ ] Subtitles: upload `publish/captions_locked.srt` (UTF-8) as English. Caption certification: \"This content has never aired on TV in the U.S.\" Then play it once with CC ON and once with CC OFF. If CC ON doubles or hides the burned-in words badly, delete the uploaded track."),
    ("- [ ] Thumbnail: Shorts thumbnails are set in the YouTube phone app. Upload `publish/thumbs/thumb_9x16.jpg` if offered; if not, pick the opening frame (first 2 s). Never the end card. Check the saved result.",
     "- [ ] Thumbnail: a Short may not take an uploaded image. In the YouTube phone app, pick a frame from the first 2 s (Job on the rock). If the app offers an image upload, use `publish/thumbs/thumb_9x16.jpg` (under 2 MB). Never the end card. Check the saved result on the channel page before scheduling."),
    ("- [ ] Publish to subscriptions feed and notify: on. Allow embedding: on.",
     "- [ ] Publish to subscriptions feed and notify: on. Allow embedding: on.\n"
     "- [ ] Automatic dubbing / auto-translated voice: **OFF** unless the owner says otherwise (it would put new AI voices on Job and Jesus)."),
    ("- [ ] Upload from TikTok Studio on desktop if you can (it keeps full quality and can Schedule). On a phone, check the file is still 1080x1920 after transfer.",
     "- [ ] Upload the original MP4 (TikTok Studio on desktop can Schedule; on a phone turn \"Upload HD\" ON). Watch the processed result.\n"
     "- [ ] A scheduled post may not be editable: read the caption once more before you press Schedule. Schedule no more than 10 days ahead."),
    ("- [ ] Use Meta Business Suite (desktop) to Schedule, or Save as Draft on the phone.\n- [ ] CAPTION",
     "- [ ] Use Meta Business Suite (desktop) to Schedule, or Save as Draft on the phone. If the AI label switch is not shown in Business Suite, do not schedule there: post from the app.\n- [ ] CAPTION"),
    ("- [ ] Alt text, if the app offers it (Advanced settings): \"Sepia comic-book short: Job on a rock by a stormy sea, then Jesus walking on the water toward His followers in a boat (Job 9:8; Mark 6:45-51).\"",
     "- [ ] Alt text, if the app offers it (Advanced settings): the ALT_TEXT field from the paste page.\n"
     "- [ ] Remix / downloads: ON only if the rights lines are filled; otherwise OFF. Meta AI voice translation: OFF."),
    ("- [ ] Use Meta Business Suite to Schedule, or Save as Draft. Audience: Public.",
     "- [ ] Use Meta Business Suite to Schedule, or Save as Draft (same AI-label rule as Instagram). Audience: Public. Share to Instagram: OFF.\n"
     "- [ ] Remix / downloads: ON only if the rights lines are filled. Meta AI voice translation: OFF."),
    ("- [ ] Write the real publish time here: ______.",
     "- [ ] Write the real publish time here: ______.\n"
     "- [ ] Check the pinned comment is really pinned, and no platform changed the cover.\n"
     "- [ ] If an error is found after release: fix text in place. Never delete and re-upload without the owner."),
])
