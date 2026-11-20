"""Apply the convergent red-team r1 fixes (Fable/Claude/Codex; Grok out of credit) to the pack text."""
from pathlib import Path

P = Path(__file__).resolve().parents[2]
pub = P / "publish"

OLD_L1 = "Long before Jesus, Job said God alone walks on the sea. Then Jesus did it."
NEW_L1 = "Long ago, a man named Job said God alone walks on the sea. Then Jesus did it."
OLD_TAGS = "#Job #Jesus #Bible #JesusWalksOnWater #BibleStory"
NEW_TAGS = "#JesusWalksOnWater #BookOfJob #Jesus #Bible #BibleStory"

common = [
    (OLD_L1, NEW_L1),
    (OLD_TAGS, NEW_TAGS),
    ('says God alone "treadeth upon the waves of the sea."', 'says God alone "treadeth upon the waves of the sea" (walks on the waves).'),
]
long_only = [
    ('Job also said of God: "he passeth on also, but I perceive him not." (Job 9:11, KJV)',
     'Job also said of God: "Lo, he goeth by me, and I see him not." (Job 9:11, KJV)'),
    ("But this time they saw Him, and He spoke", "But unlike Job, they saw Him, and He spoke"),
    ('and says He is "touched with the feeling of our infirmities." (Hebrews 4:15, KJV) The film ends with an invitation to trust Jesus.',
     'and says He can be "touched with the feeling of our infirmities" (Hebrews 4:15, KJV): He feels our weakness.'),
]
short_only = [
    ('The Bible does not say why He "would have passed by them."',
     'The Bible does not say why He "would have passed by them." Job did not name Jesus. He described what only God does.'),
    ("Hebrews 4:15.\n\nFind Jesus", "Hebrews 4:15 (KJV).\n\nFind Jesus"),
]

for f, extra in [("youtube_short.md", long_only), ("facebook.md", long_only), ("tiktok.md", short_only), ("instagram.md", short_only)]:
    p = pub / f
    t = p.read_text(encoding="utf-8")
    for a, b in common + extra:
        assert t.count(a) == 1, (f, a)
        t = t.replace(a, b)
    p.write_text(t, encoding="utf-8")
    print("fixed", f)

PIN = ('Job 9:8 says God alone "treadeth upon the waves of the sea." Job also said, "Lo, he goeth by me, and I see him not" (Job 9:11). '
       'In Mark 6:48 Jesus comes "walking upon the sea," and "would have passed by them." The Bible does not say why. '
       'But unlike Job, they saw Him, and He spoke: "It is I; be not afraid" (Mark 6:50). Job did not name Jesus; he described what only God does. '
       'Have you ever felt God go past you? Read it: Job 9:8-11, 9:32-33; Mark 6:45-51; 1 Timothy 2:5; Hebrews 4:15.')

c = P / "UPLOAD_CHECKLIST.md"
t = c.read_text(encoding="utf-8")
for a, b in [
    ("upload checklist (2026-11-17, film t13_final)", "upload checklist (2026-11-19, film visual/job_sea_final.mp4)"),
    ("- [ ] Playlist: the Bible prophecy series playlist (same one as Bethlehem, Immanuel and Nazareth) (create it once).",
     "- [ ] Playlist: \"Jesus in the Bible\" (NOT the prophecy playlist: Job did not foretell Jesus). Create it once."),
    ("- [ ] Thumbnail: upload `thumbs/thumb_9x16.jpg` in YouTube Studio if offered. If not, use the opening hook frame (first 2 s). Never the end card.",
     "- [ ] Thumbnail: Shorts thumbnails are set in the YouTube phone app (desktop Studio may not offer it). Upload `thumbs/thumb_9x16.jpg` there if offered; if not, pick the opening hook frame (first 2 s). Never the end card. Preview the saved result."),
    ("- [ ] Shorts remixing: allow.", "- [ ] Publish to subscriptions feed and notify: on. Allow embedding: on.\n- [ ] Shorts remixing: allow."),
    ("- [ ] Captions: Instagram has no SRT upload.", "- [ ] Settings: \"Upload at highest quality\" ON. Trial reel OFF.\n- [ ] Captions: Instagram has no SRT upload."),
    ("post and pin this comment on YouTube:\n  > \n", f"post and pin this comment on YouTube:\n  > {PIN}\n"),
]:
    assert t.count(a) == 1, a
    t = t.replace(a, b)
c.write_text(t, encoding="utf-8")
print("fixed checklist")
