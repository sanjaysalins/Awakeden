"""Serif "VEED-style" caption renderer — pure ffmpeg/libass, no API calls.

Replicates the cream high-contrast-serif look (small words + one enlarged bold
key word, left-aligned lower third, soft pop/fade) by generating an ASS subtitle
file from word-level timings and burning it in with ffmpeg.

Pipeline (all local):
    word timings (faster_whisper, offline)  ->  phrases  ->  .ass  ->  ffmpeg burn

LOCKED DEFAULT RECIPE (a plain run produces this — flags only override):
    * Font Inter, colour #F4F0D8 (muted warm ivory)
    * one big bold key word on its own line; small words around it
    * mid-phrase connector words italic AND a touch larger (ITALIC_FS)
    * trailing word indent-tucked under the key word (quote lockup)
    * near-zero line gap (LINE_STEP_FACTOR ~0.70) so lines read as one block
    * whisper-subtle shadow (1), no border
    * gentle fade in/out, NO zoom pop
    * two close left-aligned positions (gentle drift, not dizzy)
    * clamped inside the YouTube Shorts safe area (top/bottom/right/left no-go)

Usage:
    python -m veed_io.serif_captions --video clip.mp4 --words words.json --out out.mp4
    # overrides:  --color #RRGGBB   --shadow 0   --no-indent   --guides
"""

from __future__ import annotations

import argparse
import json
import subprocess
from dataclasses import dataclass, field
from pathlib import Path

# ---- style knobs (tuned to the VEED reference) -----------------------------

FONT_NAME = "Inter"            # matches the VEED reference (sans)
CREAM = "&H00D8F0F4"           # ASS = AABBGGRR for #F4F0D8 (muted warm ivory) [LOCKED]
SMALL_FS = 90                  # small words (bigger)
ITALIC_FS = 112                # italic connector words — larger, to stand out
BIG_FS = 236                   # the enlarged key word (bigger)
OUTLINE = 0                    # no outline
SHADOW = 1                     # whisper-subtle shadow (not a border) [LOCKED]
LINE_STEP_FACTOR = 0.70        # vertical step per line as a fraction of its font
                               # size (smaller = tighter; ~0.70 = lines hug)
MARGIN_L = 60                  # left inset (fallback)
MARGIN_V = 460                 # up from the bottom (fallback)

# --- YouTube Shorts safe area / NO-GO zones (px, for a 1080x1920 short) -------
# Captions are clamped to the SAFE band between these zones (see clamp in
# _phrase_events) and you can render them as a translucent overlay with --guides.
#   bottom = title / handle / caption / progress bar / CTA
#   right  = like / comment / share / remix / sound / subscribe column
#   left   = small inset margin
#   top    = search / sound-pill strip
NOGO_BOTTOM = 420
NOGO_RIGHT = 190
NOGO_LEFT = 40
NOGO_TOP = 150
BIG_MAX_W = 1080 - MARGIN_L - NOGO_RIGHT - 20   # width budget for the key word

# Two close vertical positions, left-aligned in the safe band — a gentle drift,
# not a jump (keeps it from feeling static OR dizzy).
POSITION_SLOTS = [
    {"an": 1, "ml": MARGIN_L, "mr": NOGO_RIGHT, "mv": 500},   # left, lower-mid
    {"an": 1, "ml": MARGIN_L, "mr": NOGO_RIGHT, "mv": 630},   # left, slightly up
]

# phrasing
MAX_WORDS = 5                  # words per on-screen phrase (VEED groups ~4-6)
PAUSE_BREAK = 0.45             # gap (s) that forces a new phrase
MIN_PHRASE_DUR = 0.6           # don't let a phrase flash too fast

# function/connector words that VEED renders ITALIC when mid-phrase
FUNCTION_WORDS = {
    "a", "an", "the", "that", "this", "of", "to", "in", "on", "is", "are",
    "was", "were", "be", "as", "at", "by", "from", "with", "and", "or", "but",
    "for", "it", "its", "your", "you", "so", "if", "than", "then", "into",
}

STOPWORDS = {
    "the", "a", "an", "and", "or", "but", "to", "of", "in", "on", "is", "are",
    "was", "were", "be", "been", "you", "your", "i", "it", "its", "he", "she",
    "they", "we", "him", "her", "them", "that", "this", "with", "for", "as",
    "at", "by", "from", "not", "no", "can", "will", "still", "so", "if",
}


@dataclass
class Word:
    w: str
    start: float
    end: float


@dataclass
class Phrase:
    words: list[Word]
    emphasis: int = 0  # index into words of the enlarged key word
    start: float = field(init=False)
    end: float = field(init=False)

    def __post_init__(self) -> None:
        self.start = self.words[0].start
        self.end = max(self.words[-1].end, self.start + MIN_PHRASE_DUR)


def load_words(path: str | Path) -> list[Word]:
    raw = json.load(open(path, encoding="utf-8"))
    return [Word(d["w"], float(d["start"]), float(d["end"])) for d in raw if d["w"]]


def _emphasis_index(words: list[Word]) -> int:
    """Pick the key word to enlarge.

    Prefer a mid-phrase proper noun (Capitalised, like "Jesus"/"Christ"); else
    the longest non-stopword. Ties -> later word.
    """
    best, best_score = 0, -1
    for i, wd in enumerate(words):
        raw = wd.w.strip(".,!?;:'\"")
        token = raw.lower()
        score = len(token) + (3 if token not in STOPWORDS else 0)
        if i > 0 and raw[:1].isupper():   # proper noun mid-phrase -> strong boost
            score += 8
        if score >= best_score:
            best, best_score = i, score
    return best


def build_phrases(words: list[Word]) -> list[Phrase]:
    phrases: list[Phrase] = []
    cur: list[Word] = []
    for i, wd in enumerate(words):
        cur.append(wd)
        gap_next = (words[i + 1].start - wd.end) if i + 1 < len(words) else 99
        ends_sentence = wd.w.endswith((".", "!", "?", ",", ";", ":"))
        if len(cur) >= MAX_WORDS or gap_next >= PAUSE_BREAK or ends_sentence:
            phrases.append(Phrase(cur, _emphasis_index(cur)))
            cur = []
    if cur:
        phrases.append(Phrase(cur, _emphasis_index(cur)))
    return phrases


def _ass_time(t: float) -> str:
    h = int(t // 3600); t -= h * 3600
    m = int(t // 60); t -= m * 60
    s = int(t); cs = int(round((t - s) * 100))
    if cs == 100:
        s += 1; cs = 0
    return f"{h}:{m:02d}:{s:02d}.{cs:02d}"


def _big_fs(key: str) -> int:
    """Key-word size, shrunk if it would overflow the safe width."""
    approx_w = len(key) * BIG_FS * 0.58
    if approx_w <= BIG_MAX_W:
        return BIG_FS
    return max(SMALL_FS + 30, int(BIG_MAX_W / (len(key) * 0.58)))


def _phrase_lines(p: Phrase) -> list[tuple[str, int, str]]:
    """Phrase as visual lines top->bottom: (markup, line_font_size, role).

    role is 'before' | 'big' | 'after'. A line's font size (for tight stacking)
    is the largest run on it.
    """
    def word_markup(i: int, wd: Word) -> tuple[str, int]:
        token = wd.w.strip(".,!?;:'\"").lower()
        if i > 0 and token in FUNCTION_WORDS:
            return rf"{{\i1\fs{ITALIC_FS}}}{wd.w}{{\i0\fs{SMALL_FS}}}", ITALIC_FS
        return wd.w, SMALL_FS

    e = p.emphasis
    lines: list[tuple[str, int, str]] = []

    before = [word_markup(i, p.words[i]) for i in range(e)]
    if before:
        lines.append((" ".join(m for m, _ in before),
                      max(fs for _, fs in before), "before"))

    key = p.words[e].w
    bfs = _big_fs(key)
    lines.append((rf"{{\b1\i0\fs{bfs}}}{key}", bfs, "big"))

    after = [word_markup(i, p.words[i]) for i in range(e + 1, len(p.words))]
    if after:
        lines.append((" ".join(m for m, _ in after),
                      max(fs for _, fs in after), "after"))

    return lines


def _phrase_events(p: Phrase, slot: dict, height: int,
                   indent_after: bool = False) -> list[str]:
    """One positioned Dialogue per visual line, stacked tight, left-aligned.

    Anchored bottom-left (\\an1) at the slot; lines stack upward with a gap
    controlled by LINE_STEP_FACTOR. If ``indent_after`` the trailing small line
    is tucked under the right half of the key word (ChatGPT 'quote lockup' look).
    """
    lines = _phrase_lines(p)
    base_x = slot["ml"]
    start, end = _ass_time(p.start), _ass_time(p.end)

    # width of the key word, to compute the asymmetric indent of the after line
    big_markup = next((m for m, _, r in lines if r == "big"), "")
    big_fs = next((fs for _, fs, r in lines if r == "big"), BIG_FS)
    key_len = len(big_markup.split("}")[-1]) or 4
    big_w = key_len * big_fs * 0.58

    # 1) lay out bottom -> top: each entry = [x, y_bottom, fs, markup]
    placed: list[list] = []
    y = float(height - slot["mv"])
    for markup, fs, role in reversed(lines):
        x = base_x
        if role == "after" and indent_after:
            x = int(base_x + big_w * 0.42)
        placed.append([x, y, fs, markup])
        y -= fs * LINE_STEP_FACTOR

    # 2) clamp the whole block into the Shorts SAFE band (never enter no-go)
    safe_bottom = height - NOGO_BOTTOM
    safe_top = NOGO_TOP
    block_bottom = placed[0][1]
    block_top = placed[-1][1] - placed[-1][2]
    shift = 0.0
    if block_bottom > safe_bottom:
        shift = safe_bottom - block_bottom            # move up
    if (block_top + shift) < safe_top:                # too tall -> nudge down
        down = safe_top - (block_top + shift)
        headroom = safe_bottom - (block_bottom + shift)
        shift += min(down, max(0.0, headroom))

    # 3) emit (gentle fade only — no scale/zoom pop, avoids the "dizzy" feel)
    events: list[str] = []
    for x, yb, _fs, markup in placed:
        intro = rf"{{\an1\pos({x},{int(yb + shift)})\fs{SMALL_FS}\fad(180,120)}}"
        events.append(f"Dialogue: 0,{start},{end},Serif,,0,0,0,,{intro}{markup}")
    return events


def hex_to_ass(hex_colour: str) -> str:
    """#RRGGBB -> ASS &H00BBGGRR."""
    h = hex_colour.lstrip("#")
    r, g, b = h[0:2], h[2:4], h[4:6]
    return f"&H00{b}{g}{r}".upper()


def build_ass(phrases: list[Phrase], width: int, height: int, *,
              colour: str = CREAM, shadow: int = SHADOW,
              indent_after: bool = True) -> str:    # quote-lockup indent [LOCKED]
    header = f"""[Script Info]
ScriptType: v4.00+
PlayResX: {width}
PlayResY: {height}
WrapStyle: 2
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Serif,{FONT_NAME},{SMALL_FS},{colour},{colour},{colour},&H64000000,0,0,0,0,100,100,0,0,1,{OUTLINE},{shadow},1,{MARGIN_L},40,{MARGIN_V},1
"""
    lines = ["[Events]",
             "Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text"]
    for idx, p in enumerate(phrases):
        slot = POSITION_SLOTS[idx % len(POSITION_SLOTS)]
        lines.extend(_phrase_events(p, slot, height, indent_after=indent_after))
    return header + "\n".join(lines) + "\n"


def _probe_size(video: str) -> tuple[int, int]:
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-select_streams", "v:0",
         "-show_entries", "stream=width,height",
         "-of", "csv=s=x:p=0", video],
        capture_output=True, text=True,
    ).stdout.strip()
    w, h = out.split("x")
    return int(w), int(h)


def _guides_filter(w: int, h: int) -> str:
    """Translucent boxes over the Shorts no-go zones, for visual QA (--guides)."""
    red = "red@0.28"
    return ",".join([
        f"drawbox=x=0:y={h - NOGO_BOTTOM}:w={w}:h={NOGO_BOTTOM}:color={red}:t=fill",
        f"drawbox=x={w - NOGO_RIGHT}:y=0:w={NOGO_RIGHT}:h={h}:color={red}:t=fill",
        f"drawbox=x=0:y=0:w={w}:h={NOGO_TOP}:color={red}:t=fill",
        f"drawbox=x=0:y=0:w={NOGO_LEFT}:h={h}:color={red}:t=fill",
    ])


def render(video: str, words_json: str, out: str, fonts_dir: str, *,
           colour_hex: str | None = None, shadow: int = SHADOW,
           indent_after: bool = True, guides: bool = False) -> str:
    w, h = _probe_size(video)
    phrases = build_phrases(load_words(words_json))
    colour = hex_to_ass(colour_hex) if colour_hex else CREAM
    ass_path = Path(out).with_suffix(".ass")
    ass_path.write_text(
        build_ass(phrases, w, h, colour=colour, shadow=shadow,
                  indent_after=indent_after),
        encoding="utf-8",
    )

    # ffmpeg subtitles filter wants an escaped path on Windows (drive colon).
    ass_arg = str(ass_path).replace("\\", "/").replace(":", "\\:")
    fonts_arg = str(Path(fonts_dir)).replace("\\", "/").replace(":", "\\:")
    chain = []
    if guides:
        chain.append(_guides_filter(w, h))      # zones UNDER the text
    chain.append(f"subtitles={ass_arg}:fontsdir={fonts_arg}")
    vf = ",".join(chain)

    cmd = ["ffmpeg", "-y", "-loglevel", "error", "-i", video,
           "-vf", vf, "-c:a", "copy", out]
    subprocess.run(cmd, check=True)
    return out


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Serif VEED-style captions (no API).")
    ap.add_argument("--video", required=True)
    ap.add_argument("--words", required=True, help="word-timings JSON (w,start,end)")
    ap.add_argument("--out", required=True)
    ap.add_argument("--fonts", default="veed_io/fonts")
    ap.add_argument("--color", help="override text colour hex (default #F4F0D8)")
    ap.add_argument("--shadow", type=int, default=SHADOW,
                    help=f"soft shadow depth (default {SHADOW}; 0 = none)")
    ap.add_argument("--no-indent", dest="indent_after", action="store_false",
                    help="disable the quote-lockup indent (on by default)")
    ap.add_argument("--guides", action="store_true",
                    help="overlay the Shorts no-go zones (red) for visual QA")
    ap.set_defaults(indent_after=True)
    args = ap.parse_args(argv)
    path = render(args.video, args.words, args.out, args.fonts,
                  colour_hex=args.color, shadow=args.shadow,
                  indent_after=args.indent_after, guides=args.guides)
    print(f"wrote {Path(path).resolve()}")
    print(f"ass:  {Path(path).with_suffix('.ass').resolve()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
