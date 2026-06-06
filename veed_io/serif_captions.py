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
import os
import subprocess
from dataclasses import dataclass, field, replace
from pathlib import Path

# ---- style knobs (tuned to the VEED reference) -----------------------------

FONT_NAME = "Inter"            # matches the VEED reference (sans)
CREAM = "&H00D8F0F4"           # ASS = AABBGGRR for #F4F0D8 (muted warm ivory) [LOCKED]
SMALL_FS = 90                  # small words (bigger)
ITALIC_FS = 112                # italic connector words — larger, to stand out
BIG_FS = 236                   # the enlarged key word (static mode, fixed size)

# DYNAMIC mode: the big word's size breathes with how hard the voice hits it.
BIG_FS_MIN = 184               # a mild stress
BIG_FS_MAX = 250               # a hard, landed stress
OUTLINE = 0                    # no outline
SHADOW = 1                     # whisper-subtle shadow (not a border) [LOCKED]
LINE_STEP_FACTOR = 0.70        # vertical step per line as a fraction of its font
                               # size (smaller = tighter; ~0.70 = lines hug)
MARGIN_L = 60                  # left inset (portrait reference)
MARGIN_V = 460                 # up from the bottom (portrait reference)

# All px above are tuned at this PORTRAIT reference frame; build_layout() scales
# them to whatever resolution / aspect the actual clip is (9:16 OR 16:9).
REF_H = 1920

# --- YouTube Shorts safe area / NO-GO zones (px @ 1080x1920 portrait) ---------
# Captions are clamped to the SAFE band between these zones and you can render
# them as a translucent overlay with --guides.
#   bottom = title / handle / caption / progress bar / CTA
#   right  = like / comment / share / remix / sound / subscribe column
#   left   = small inset margin   ·   top = search / sound-pill strip
NOGO_BOTTOM = 420
NOGO_RIGHT = 190
NOGO_LEFT = 40
NOGO_TOP = 150

# Static-mode drift slots, as "up-from-bottom" offsets (portrait reference).
STATIC_SLOTS_MV = [500, 630]


@dataclass
class Layout:
    """Resolution- and aspect-aware geometry for one clip.

    Built from the probed (w, h): portrait 9:16 keeps the YouTube-Shorts no-go
    zones; landscape 16:9 (long-form deep-dives) drops the Shorts chrome and
    uses calm lower-third margins. Every font/margin is scaled by h/REF_H so a
    word is the same FRACTION of frame height in either orientation.
    """
    w: int
    h: int
    portrait: bool
    small_fs: int
    italic_fs: int
    big_fs: int
    big_fs_min: int
    big_fs_max: int
    line_step: float
    margin_l: int
    margin_v: int
    nogo_top: int
    nogo_bottom: int
    nogo_left: int
    nogo_right: int
    big_max_w: int
    big_anchor_y: int          # fixed Y for the big word's baseline (stable focal)
    static_slots_mv: list[int]


def build_layout(w: int, h: int) -> Layout:
    portrait = h >= w
    scale = h / REF_H

    def s(v: float) -> int:
        return max(1, int(round(v * scale)))

    small, italic = s(SMALL_FS), s(ITALIC_FS)
    big, bmin, bmax = s(BIG_FS), s(BIG_FS_MIN), s(BIG_FS_MAX)

    if portrait:                                   # 9:16 — keep Shorts safe zones
        nogo_top, nogo_bottom = s(NOGO_TOP), s(NOGO_BOTTOM)
        nogo_left, nogo_right = s(NOGO_LEFT), s(NOGO_RIGHT)
        margin_l = s(MARGIN_L)
        slots = [s(mv) for mv in STATIC_SLOTS_MV]
    else:                                          # 16:9 — calm lower-third frame
        nogo_top, nogo_bottom = int(h * 0.06), int(h * 0.10)
        nogo_left = nogo_right = int(w * 0.06)
        margin_l = nogo_left + s(20)
        slots = [int(h * 0.30), int(h * 0.42)]

    big_max_w = w - margin_l - nogo_right - s(20)
    safe_bottom = h - nogo_bottom
    after_reserve = int(2.0 * small * LINE_STEP_FACTOR)   # room for ~2 tail lines
    big_anchor_y = safe_bottom - after_reserve            # eye rests here, always

    return Layout(w, h, portrait, small, italic, big, bmin, bmax,
                  LINE_STEP_FACTOR, margin_l, s(MARGIN_V), nogo_top, nogo_bottom,
                  nogo_left, nogo_right, big_max_w, big_anchor_y, slots)


# ---- caption STYLE presets (all offline, $0) -------------------------------
# Palette (reverent gospel: ivory + warm gold, never neon).
GOLD = "#F2C24C"        # warm amber — the emphasis colour
CREAMC = "#F4F0D8"      # the locked ivory
WHITE = "#FFFFFF"
SOFTGOLD = "#E9C877"
INK = "#141210"         # near-black outline


@dataclass
class Style:
    """A caption LOOK. Themes colour/outline/animation on top of the dynamic
    stable-focal layout — the emphasis stays voice-driven, the skin changes."""
    name: str
    base_hex: str = CREAMC      # small words
    accent_hex: str = CREAMC    # the big / active word
    outline: int = 0            # border px @ portrait ref (scaled per clip)
    outline_hex: str = INK
    shadow: int = 1
    bounce: bool = False        # big word scale-pops in
    glow: bool = False          # soft halo behind the big word
    uppercase: bool = False
    karaoke: bool = False        # each word fills to accent exactly as spoken


STYLES: dict[str, Style] = {
    # the current locked look (cream, big key word, italic connectors)
    "ivory":   Style("ivory"),
    # cream words, gold key word with a soft halo + gentle pop — refined viral
    "glow":    Style("glow", accent_hex=GOLD, glow=True, bounce=True),
    # white + thick dark outline (reads on ANY image), gold key word, pop
    "pop":     Style("pop", base_hex=WHITE, accent_hex=GOLD, outline=6, shadow=2,
                     bounce=True),
    # ALL-CAPS, heavy outline, gold key word — loud / bold
    "impact":  Style("impact", base_hex=WHITE, accent_hex=GOLD, outline=5,
                     shadow=2, uppercase=True),
    # each word lights up GOLD as it is spoken (uses the exact timings)
    "karaoke": Style("karaoke", base_hex=WHITE, accent_hex=GOLD, outline=3,
                     shadow=1, karaoke=True),
    # quiet, premium lower-third — the calm/cinematic alternative
    "minimal": Style("minimal", base_hex="#ECE7D2", accent_hex=SOFTGOLD,
                     outline=0, shadow=0),
}
DEFAULT_STYLE = "ivory"


@dataclass
class Tok:
    """One word with its size/role/timing — the unit the style renderer themes."""
    text: str
    fs: int
    role: str          # 'before' | 'big' | 'after'
    big: bool
    italic: bool
    start: float
    end: float

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
    rms: float = 0.0    # vocal loudness in this word's window (prosody.py); 0 = unknown
    peak: float = 0.0


@dataclass
class Phrase:
    words: list[Word]
    emphasis: int = 0    # index into words of the ENLARGED key word
    italic: int = -1     # index of the moving italic word (-1 = none / use connectors)
    strength: float = 0.5  # 0..1 emphasis strength -> big-word size (dynamic mode)
    start: float = field(init=False)
    end: float = field(init=False)

    def __post_init__(self) -> None:
        self.start = self.words[0].start
        self.end = max(self.words[-1].end, self.start + MIN_PHRASE_DUR)


def load_words(path: str | Path) -> list[Word]:
    raw = json.load(open(path, encoding="utf-8"))
    return [Word(d["w"], float(d["start"]), float(d["end"]),
                 float(d.get("rms", 0.0)), float(d.get("peak", 0.0)))
            for d in raw if d["w"]]


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


def _zscores(vals: list[float]) -> list[float]:
    """Standard-score a small list (pure python; emphasis is LOCAL contrast)."""
    n = len(vals)
    if n == 0:
        return []
    mean = sum(vals) / n
    var = sum((v - mean) ** 2 for v in vals) / n
    sd = var ** 0.5
    if sd < 1e-9:
        return [0.0] * n
    return [(v - mean) / sd for v in vals]


def _is_stop(word: str) -> bool:
    return word.strip(".,!?;:'\"").lower() in STOPWORDS


def _dynamic_emphasis(words: list[Word]) -> tuple[int, int, float]:
    """Pick (big_idx, italic_idx, strength) from REAL vocal emphasis.

    Combines the loudness (RMS) and length the voice actually gave each word
    with a light text prior (content words over stopwords), all as phrase-local
    z-scores, so the enlarged word lands wherever the narrator leans in — early,
    middle or late in the phrase. The runner-up becomes the moving italic.
    """
    n = len(words)
    if n == 1:
        return 0, -1, 0.6

    z_rms = _zscores([w.rms for w in words])
    z_dur = _zscores([max(1e-3, w.end - w.start) for w in words])

    def prior(i: int) -> float:
        raw = words[i].w.strip(".,!?;:'\"")
        s = float(len(raw))
        if _is_stop(words[i].w):
            s -= 6.0
        if i > 0 and raw[:1].isupper():      # proper noun mid-phrase
            s += 8.0
        return s

    z_txt = _zscores([prior(i) for i in range(n)])

    score = [0.0] * n
    for i in range(n):
        s = 1.00 * z_rms[i] + 0.55 * z_dur[i] + 0.45 * z_txt[i]
        if _is_stop(words[i].w):             # a stopword wins only if REALLY hit
            s -= 2.0
        score[i] = s

    order = sorted(range(n), key=lambda i: score[i], reverse=True)
    big = order[0]
    italic = next((i for i in order[1:]), -1)

    # strength: how acoustically prominent the winner is (loudness+length only),
    # squashed to 0..1 so the big-word size breathes without going wild.
    ac = z_rms[big] + 0.5 * z_dur[big]
    strength = max(0.0, min(1.0, (ac + 0.4) / 2.2))
    return big, italic, strength


def build_phrases(words: list[Word], dynamic: bool = False) -> list[Phrase]:
    phrases: list[Phrase] = []
    cur: list[Word] = []

    def flush(group: list[Word]) -> None:
        if dynamic:
            big, ital, strength = _dynamic_emphasis(group)
            phrases.append(Phrase(group, big, ital, strength))
        else:
            phrases.append(Phrase(group, _emphasis_index(group)))

    for i, wd in enumerate(words):
        cur.append(wd)
        gap_next = (words[i + 1].start - wd.end) if i + 1 < len(words) else 99
        ends_sentence = wd.w.endswith((".", "!", "?", ",", ";", ":"))
        if len(cur) >= MAX_WORDS or gap_next >= PAUSE_BREAK or ends_sentence:
            flush(cur)
            cur = []
    if cur:
        flush(cur)
    return phrases


def _ass_time(t: float) -> str:
    h = int(t // 3600); t -= h * 3600
    m = int(t // 60); t -= m * 60
    s = int(t); cs = int(round((t - s) * 100))
    if cs == 100:
        s += 1; cs = 0
    return f"{h}:{m:02d}:{s:02d}.{cs:02d}"


def _big_fs(key: str, base: int, lay: Layout) -> int:
    """Key-word size, shrunk if it would overflow the safe width."""
    approx_w = len(key) * base * 0.58
    if approx_w <= lay.big_max_w:
        return base
    return max(lay.small_fs + int(30 * lay.h / REF_H),
               int(lay.big_max_w / (len(key) * 0.58)))


def _big_fs_strength(key: str, strength: float, lay: Layout) -> int:
    """Dynamic key-word size: breathe between MIN..MAX by stress, then clamp."""
    span = lay.big_fs_max - lay.big_fs_min
    base = int(round(lay.big_fs_min + span * max(0.0, min(1.0, strength))))
    return _big_fs(key, base, lay)


def _est_w(vis_len: int, fs: int) -> float:
    """Rough rendered width of ``vis_len`` glyphs at font size ``fs``."""
    return vis_len * fs * 0.58


def _wrap_run(tokens: list[tuple[str, int, int]], role: str, lay: Layout
              ) -> list[tuple[str, int, str]]:
    """Greedy-wrap a run of (markup, fs, visible_len) tokens to the safe width.

    Returns visual lines (markup, line_fs, role). Lets a long lead-in or tail
    span >1 line, so the big word can genuinely land on line 1, 2 or 3+.
    """
    lines: list[tuple[str, int, str]] = []
    cur: list[str] = []
    cur_fs = 0
    cur_w = 0.0
    for markup, fs, vis in tokens:
        space = _est_w(1, lay.small_fs) if cur else 0.0
        add = _est_w(vis, fs) + space
        if cur and cur_w + add > lay.big_max_w:
            lines.append((" ".join(cur), cur_fs, role))
            cur, cur_fs, cur_w = [], 0, 0.0
            add = _est_w(vis, fs)
        cur.append(markup)
        cur_fs = max(cur_fs, fs)
        cur_w += add
    if cur:
        lines.append((" ".join(cur), cur_fs, role))
    return lines


def _phrase_lines_dynamic(p: Phrase, lay: Layout) -> list[tuple[str, int, str]]:
    """Dynamic layout: big word at its NATURAL position (so it moves up/down),
    one moving italic on the runner-up word, lead-in/tail wrapped to width."""
    e = p.emphasis

    def small_tok(i: int) -> tuple[str, int, int]:
        wd = p.words[i]
        vis = len(wd.w)
        if i == p.italic:
            return (rf"{{\i1\b0\fs{lay.italic_fs}}}{wd.w}{{\i0\fs{lay.small_fs}}}",
                    lay.italic_fs, vis)
        return (wd.w, lay.small_fs, vis)

    lines: list[tuple[str, int, str]] = []
    lines += _wrap_run([small_tok(i) for i in range(e)], "before", lay)

    key = p.words[e].w
    bfs = _big_fs_strength(key, p.strength, lay)
    lines.append((rf"{{\b1\i0\fs{bfs}}}{key}", bfs, "big"))

    lines += _wrap_run([small_tok(i) for i in range(e + 1, len(p.words))], "after", lay)
    return lines


def _phrase_lines(p: Phrase, lay: Layout) -> list[tuple[str, int, str]]:
    """Phrase as visual lines top->bottom: (markup, line_font_size, role).

    role is 'before' | 'big' | 'after'. A line's font size (for tight stacking)
    is the largest run on it.
    """
    def word_markup(i: int, wd: Word) -> tuple[str, int]:
        token = wd.w.strip(".,!?;:'\"").lower()
        if i > 0 and token in FUNCTION_WORDS:
            return (rf"{{\i1\fs{lay.italic_fs}}}{wd.w}{{\i0\fs{lay.small_fs}}}",
                    lay.italic_fs)
        return wd.w, lay.small_fs

    e = p.emphasis
    lines: list[tuple[str, int, str]] = []

    before = [word_markup(i, p.words[i]) for i in range(e)]
    if before:
        lines.append((" ".join(m for m, _ in before),
                      max(fs for _, fs in before), "before"))

    key = p.words[e].w
    bfs = _big_fs(key, lay.big_fs, lay)
    lines.append((rf"{{\b1\i0\fs{bfs}}}{key}", bfs, "big"))

    after = [word_markup(i, p.words[i]) for i in range(e + 1, len(p.words))]
    if after:
        lines.append((" ".join(m for m, _ in after),
                      max(fs for _, fs in after), "after"))

    return lines


def _wrap_toks(toks: list[Tok], lay: Layout) -> list[list[Tok]]:
    """Greedy-wrap a run of word toks to the safe width (keeps the tok objects)."""
    lines: list[list[Tok]] = []
    cur: list[Tok] = []
    cur_w = 0.0
    for t in toks:
        space = _est_w(1, lay.small_fs) if cur else 0.0
        add = _est_w(len(t.text), t.fs) + space
        if cur and cur_w + add > lay.big_max_w:
            lines.append(cur)
            cur, cur_w = [], 0.0
            add = _est_w(len(t.text), t.fs)
        cur.append(t)
        cur_w += add
    if cur:
        lines.append(cur)
    return lines


def _phrase_toklines_dynamic(p: Phrase, lay: Layout) -> list[list[Tok]]:
    """Dynamic layout as word toks: big word on its own line at its natural
    position, lead-in/tail wrapped to width. Style-agnostic (themed later)."""
    e = p.emphasis

    def mk(i: int, role: str) -> Tok:
        wd = p.words[i]
        ital = (i == p.italic)
        return Tok(wd.w, lay.italic_fs if ital else lay.small_fs, role,
                   False, ital, wd.start, wd.end)

    before = [mk(i, "before") for i in range(e)]
    key = p.words[e]
    big = Tok(key.w, _big_fs_strength(key.w, p.strength, lay), "big",
              True, False, key.start, key.end)
    after = [mk(i, "after") for i in range(e + 1, len(p.words))]
    return _wrap_toks(before, lay) + [[big]] + _wrap_toks(after, lay)


def _txt(t: Tok, style: Style) -> str:
    return t.text.upper() if style.uppercase else t.text


def _tok_override(t: Tok, style: Style) -> str:
    """Inline ASS override for one word (size, italic, big colour/pop)."""
    o = [rf"\fs{t.fs}", r"\i1" if t.italic else r"\i0",
         r"\b1" if t.big else r"\b0"]
    if not style.karaoke:                                 # karaoke owns colour
        o.append(rf"\1c{hex_to_ass(style.accent_hex if t.big else style.base_hex)}")
    if t.big and style.bounce:
        o.append(r"\t(0,130,\fscx116\fscy116)\t(130,260,\fscx100\fscy100)")
    return "".join(o)


def _render_line(line: list[Tok], x: int, y: int, phrase_start: float,
                 start: str, end: str, lay: Layout, style: Style) -> list[str]:
    """Emit the ASS Dialogue event(s) for one stacked line, in the given style."""
    events: list[str] = []

    # soft gold halo behind the big word (glow styles); big lines hold one tok
    if style.glow and any(t.big for t in line):
        t = line[0]
        blur = max(4, int(14 * lay.h / REF_H))
        halo = (rf"{{\an1\pos({x},{y})\b1\fs{t.fs}\1c{hex_to_ass(style.accent_hex)}"
                rf"\bord0\shad0\blur{blur}\fad(160,160)}}{_txt(t, style)}")
        events.append(f"Dialogue: 0,{start},{end},Serif,,0,0,0,,{halo}")

    parts: list[str] = []
    if style.karaoke:
        gap = max(0.0, line[0].start - phrase_start)
        parts.append(rf"{{\kf{int(round(gap * 100))}}}")
    for i, t in enumerate(line):
        ov = _tok_override(t, style)
        if style.karaoke:
            ov = rf"\kf{max(5, int(round((t.end - t.start) * 100)))}" + ov
        parts.append((" " if i else "") + "{" + ov + "}" + _txt(t, style))

    intro = rf"{{\an1\pos({x},{y})\fad(180,120)}}"
    events.append(f"Dialogue: 1,{start},{end},Serif,,0,0,0,,{intro}{''.join(parts)}")
    return events


def _phrase_events_dynamic(p: Phrase, lay: Layout, style: Style,
                           indent_after: bool) -> list[str]:
    """Styled dynamic events: stable focal anchor + per-style skin/karaoke."""
    toklines = _phrase_toklines_dynamic(p, lay)
    start, end = _ass_time(p.start), _ass_time(p.end)
    base_x = lay.margin_l

    big_tok = next((t for ln in toklines for t in ln if t.big), None)
    big_w = (len(big_tok.text) * big_tok.fs * 0.58) if big_tok else 0.0

    # stack bottom -> top, y relative to 0
    placed: list[list] = []     # [x, y, line_fs, role, line]
    y = 0.0
    for line in reversed(toklines):
        lfs = max(t.fs for t in line)
        role = "big" if any(t.big for t in line) else line[0].role
        x = base_x + (int(big_w * 0.42) if role == "after" and indent_after else 0)
        placed.append([x, y, lfs, role, line])
        y -= lfs * lay.line_step

    rel_big = next((yy for _x, yy, _f, role, _l in placed if role == "big"), 0.0)
    shift = lay.big_anchor_y - rel_big

    safe_bottom = lay.h - lay.nogo_bottom
    safe_top = lay.nogo_top
    block_bottom = placed[0][1] + shift
    if block_bottom > safe_bottom:
        shift += safe_bottom - block_bottom
    block_top = placed[-1][1] - placed[-1][2] + shift
    if block_top < safe_top:
        headroom = safe_bottom - (placed[0][1] + shift)
        shift += min(safe_top - block_top, max(0.0, headroom))

    events: list[str] = []
    for x, yb, _lfs, _role, line in placed:
        events += _render_line(line, x, int(yb + shift), p.start,
                               start, end, lay, style)
    return events


def _phrase_events(p: Phrase, slot_mv: int, lay: Layout,
                   indent_after: bool = False, dynamic: bool = False) -> list[str]:
    """One positioned Dialogue per visual line, stacked tight, left-aligned.

    Anchored bottom-left (\\an1); lines stack upward with a gap controlled by
    LINE_STEP_FACTOR. DYNAMIC mode pins the BIG word's baseline to a single
    fixed Y (``lay.big_anchor_y``) every phrase, so the reader's eye rests in
    one place while the emphasis (which word, its size, the italic) moves.
    STATIC mode anchors the block bottom at ``slot_mv``. If ``indent_after`` the
    trailing line is tucked under the key word (quote-lockup look).
    """
    lines = _phrase_lines_dynamic(p, lay) if dynamic else _phrase_lines(p, lay)
    base_x = lay.margin_l
    start, end = _ass_time(p.start), _ass_time(p.end)

    # width of the key word, to compute the asymmetric indent of the after line
    big_markup = next((m for m, _, r in lines if r == "big"), "")
    big_fs = next((fs for _, fs, r in lines if r == "big"), lay.big_fs)
    key_len = len(big_markup.split("}")[-1]) or 4
    big_w = key_len * big_fs * 0.58

    # 1) lay out bottom -> top with y RELATIVE to 0 (bottom line at 0).
    placed: list[list] = []     # [x, y_baseline, fs, role, markup]
    y = 0.0
    for markup, fs, role in reversed(lines):
        x = base_x
        if role == "after" and indent_after:
            x = int(base_x + big_w * 0.42)
        placed.append([x, y, fs, role, markup])
        y -= fs * lay.line_step

    # 2) anchor: dynamic pins the BIG line to a constant Y; static pins block bottom.
    if dynamic:
        rel_big = next((yy for _, yy, _f, role, _m in placed if role == "big"), 0.0)
        shift = lay.big_anchor_y - rel_big
    else:
        shift = float(lay.h - slot_mv)                # block bottom -> slot

    # 3) clamp the whole block into the SAFE band (never enter no-go).
    safe_bottom = lay.h - lay.nogo_bottom
    safe_top = lay.nogo_top
    block_bottom = placed[0][1] + shift
    block_top = placed[-1][1] - placed[-1][2] + shift
    if block_bottom > safe_bottom:
        shift += safe_bottom - block_bottom
    block_top = placed[-1][1] - placed[-1][2] + shift
    if block_top < safe_top:                          # too tall -> nudge down
        headroom = safe_bottom - (placed[0][1] + shift)
        shift += min(safe_top - block_top, max(0.0, headroom))

    # 4) emit (gentle fade only — no scale/zoom pop, avoids the "dizzy" feel)
    events: list[str] = []
    for x, yb, _fs, _role, markup in placed:
        intro = rf"{{\an1\pos({x},{int(yb + shift)})\fs{lay.small_fs}\fad(180,120)}}"
        events.append(f"Dialogue: 0,{start},{end},Serif,,0,0,0,,{intro}{markup}")
    return events


def hex_to_ass(hex_colour: str) -> str:
    """#RRGGBB -> ASS &H00BBGGRR."""
    h = hex_colour.lstrip("#")
    r, g, b = h[0:2], h[2:4], h[4:6]
    return f"&H00{b}{g}{r}".upper()


def build_ass(phrases: list[Phrase], lay: Layout, style: Style, *,
              indent_after: bool = True,             # quote-lockup indent [LOCKED]
              dynamic: bool = False) -> str:
    primary = hex_to_ass(style.accent_hex if style.karaoke else style.base_hex)
    secondary = hex_to_ass(style.base_hex)            # karaoke pre-fill colour
    outline_c = hex_to_ass(style.outline_hex)
    bord = max(0, int(round(style.outline * lay.h / REF_H)))
    header = f"""[Script Info]
ScriptType: v4.00+
PlayResX: {lay.w}
PlayResY: {lay.h}
WrapStyle: 2
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Serif,{FONT_NAME},{lay.small_fs},{primary},{secondary},{outline_c},&H64000000,0,0,0,0,100,100,0,0,1,{bord},{style.shadow},1,{lay.margin_l},40,{lay.margin_v},1
"""
    lines = ["[Events]",
             "Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text"]
    for idx, p in enumerate(phrases):
        if dynamic:
            lines.extend(_phrase_events_dynamic(p, lay, style, indent_after))
        else:
            slot_mv = lay.static_slots_mv[idx % len(lay.static_slots_mv)]
            lines.extend(_phrase_events(p, slot_mv, lay,
                                        indent_after=indent_after, dynamic=False))
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


def _guides_filter(lay: Layout) -> str:
    """Translucent boxes over the (aspect-aware) no-go zones, for visual QA."""
    red = "red@0.28"
    w, h = lay.w, lay.h
    return ",".join([
        f"drawbox=x=0:y={h - lay.nogo_bottom}:w={w}:h={lay.nogo_bottom}:color={red}:t=fill",
        f"drawbox=x={w - lay.nogo_right}:y=0:w={lay.nogo_right}:h={h}:color={red}:t=fill",
        f"drawbox=x=0:y=0:w={w}:h={lay.nogo_top}:color={red}:t=fill",
        f"drawbox=x=0:y=0:w={lay.nogo_left}:h={h}:color={red}:t=fill",
    ])


def _resolve_style(style: str | Style, colour_hex: str | None,
                   shadow: int | None) -> Style:
    s = style if isinstance(style, Style) else STYLES.get(style, STYLES[DEFAULT_STYLE])
    s = replace(s)                                   # don't mutate the registry
    if colour_hex:                                   # --color overrides the base
        s.base_hex = colour_hex
        if not s.karaoke and s.accent_hex == STYLES[s.name].base_hex:
            s.accent_hex = colour_hex                # keep mono styles mono
    if shadow is not None:
        s.shadow = shadow
    return s


def render(video: str, words_json: str, out: str, fonts_dir: str, *,
           colour_hex: str | None = None, shadow: int | None = None,
           indent_after: bool = True, guides: bool = False,
           dynamic: bool = False, style: str | Style = DEFAULT_STYLE) -> str:
    w, h = _probe_size(video)
    lay = build_layout(w, h)
    sty = _resolve_style(style, colour_hex, shadow)
    print(f"  layout: {w}x{h} {'9:16 portrait' if lay.portrait else '16:9 landscape'} "
          f"(big {lay.big_fs_min}-{lay.big_fs_max}px, focal y={lay.big_anchor_y}) "
          f"style={sty.name}")
    phrases = build_phrases(load_words(words_json), dynamic=dynamic)
    ass_path = Path(out).with_suffix(".ass")
    ass_path.write_text(
        build_ass(phrases, lay, sty, indent_after=indent_after, dynamic=dynamic),
        encoding="utf-8",
    )

    # ffmpeg's subtitles filter mis-parses a Windows drive-colon in the path:
    # the filtergraph parser splits 'C:' as an option separator and NO escaping
    # (\: or quoting) survives reliably. Robust fix: run ffmpeg FROM the .ass
    # directory and pass relative, colon-free paths. video/out stay absolute —
    # they're plain -i/output args, not inside the filtergraph.
    work = ass_path.resolve().parent
    video_abs = str(Path(video).resolve())
    out_abs = str(Path(out).resolve())
    ass_arg = ass_path.name
    fonts_arg = os.path.relpath(str(Path(fonts_dir).resolve()), str(work)).replace("\\", "/")
    chain = []
    if guides:
        chain.append(_guides_filter(lay))       # zones UNDER the text
    chain.append(f"subtitles={ass_arg}:fontsdir={fonts_arg}")
    vf = ",".join(chain)

    cmd = ["ffmpeg", "-y", "-loglevel", "error", "-i", video_abs,
           "-vf", vf, "-c:a", "copy", out_abs]
    subprocess.run(cmd, check=True, cwd=str(work))
    return out


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Serif VEED-style captions (no API).")
    ap.add_argument("--video", required=True)
    ap.add_argument("--words", required=True, help="word-timings JSON (w,start,end)")
    ap.add_argument("--out", required=True)
    ap.add_argument("--fonts", default="veed_io/fonts")
    ap.add_argument("--style", choices=sorted(STYLES), default=DEFAULT_STYLE,
                    help="caption look (ivory/glow/pop/impact/karaoke/minimal)")
    ap.add_argument("--color", help="override the base text colour hex")
    ap.add_argument("--shadow", type=int, default=None,
                    help="soft shadow depth override (default: per style)")
    ap.add_argument("--no-indent", dest="indent_after", action="store_false",
                    help="disable the quote-lockup indent (on by default)")
    ap.add_argument("--guides", action="store_true",
                    help="overlay the Shorts no-go zones (red) for visual QA")
    ap.add_argument("--static", dest="dynamic", action="store_false",
                    help="locked static look (default = dynamic emphasis-driven)")
    ap.set_defaults(indent_after=True, dynamic=True)
    args = ap.parse_args(argv)
    path = render(args.video, args.words, args.out, args.fonts,
                  colour_hex=args.color, shadow=args.shadow,
                  indent_after=args.indent_after, guides=args.guides,
                  dynamic=args.dynamic, style=args.style)
    print(f"wrote {Path(path).resolve()}")
    print(f"ass:  {Path(path).with_suffix('.ass').resolve()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
