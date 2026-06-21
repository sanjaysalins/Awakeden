"""Regenerate C:/Users/sanjay/V2_STATUS.html from disk truth — the living 'what's left
for the v2 treatment' tracker. Run after finishing/advancing any episode:

    .venv\\Scripts\\python.exe v2\\scan_v2_status.py

State per FIX-ALL target is detected from its narration folder, NOT hand-maintained:
  done   = assembly/viral_cut_sfx_music_captioned.mp4 exists (full v2 finish)
  finish = a viral_cut*.mp4 exists but no captioned final (cut done, needs SFX+score+caption)
  visuals= narration.mp3 exists but no cut (audio done, needs the visual build + assembly)
  audio  = no narration.mp3 (text only, needs audio first)
"""
from __future__ import annotations
from pathlib import Path
import html

NARR = Path(r"C:\Users\sanjay\PycharmProjects\PythonProject1\jesus\narration")
OUT = Path(r"C:\Users\sanjay\V2_STATUS.html")
HOME = Path(r"C:\Users\sanjay")

# --- the FIX-ALL v2 scope (folder, label, passage) ---
TARGETS = [
    ("08 The Well That Never Runs Dry", "08 The Well That Never Runs Dry", "John 4"),
    ("16 The Fire Jesus Built",         "16 The Fire Jesus Built",         "John 21"),
    ("32_The_Door_Was_a_Body",          "32 The Door Was a Body",          "John 10"),
    ("25 The Question on the Gaza Road", "25 The Question on the Gaza Road","Acts 8 / Isa 53"),
    ("27 A List of Dead Men",           "27 A List of Dead Men",           "Matt 16"),
    ("09 The Father Who Ran",           "09 The Father Who Ran",           "Luke 15"),
    ("19 The Cliff of Rival Gods",      "19 The Cliff of Rival Gods",      "Matt 16"),
    ("24 The Answer Was a Gift",        "24 The Answer Was a Gift",        "Matt 16"),
    ("26 Jesus Walked Past the Pool",   "26 Jesus Walked Past the Pool",   "John 5"),
    ("28 What Manner of Man",           "28 What Manner of Man",           "storm stilled"),
    ("29 The Race He Could Never Win",  "29 The Race He Could Never Win",  "John 5"),
    ("31 The Light You Can Stand In",   "31 The Light You Can Stand In",   "John 8"),
    ("23 The Prepared Belly",           "23 The Prepared Belly",           "Jonah"),
    ("34_The_Hunger_Bread_Cant_Fill",  "34 The Hunger Bread Can't Fill",  "John 6"),
    ("35_Manna_Fulfilled",             "35 Manna Fulfilled",              "John 6"),
    ("36_In_No_Wise_Cast_Out",         "36 In No Wise Cast Out",          "John 6"),
]
RETIRED = [
    ("Who Do You Say I Am", "Matt 16 · modern-English; #27 covers it", "drop"),
    ("21 The Pronouns That Preached the Gospel", "Isaiah 53 · never produced", "skip"),
]
# stable already-done cluster (outside the FIX-ALL back-catalogue numbering)
DONE_EXTRA = [
    ("Psalm 22 shorts #01-#08", "full series + publish packs"),
    ("Isaiah 53:5 - With His Stripes", "v2 pilot"),
    ("Mockers' Words (Ps 22)", "v2 pilot"),
    ("Zechariah 12:10 - Pierced", "v2 pilot"),
]
# clickable finals that live at C:/Users/sanjay/*_FINAL.mp4 (by folder)
FINAL_LINK = {
    "08 The Well That Never Runs Dry": "WELL_FINAL.mp4",
    "16 The Fire Jesus Built": "FIRE_FINAL.mp4",
    "32_The_Door_Was_a_Body": "DOOR_FINAL.mp4",
    "25 The Question on the Gaza Road": "GAZA_FINAL.mp4",
    "27 A List of Dead Men": "27_A_List_Of_Dead_Men_FINAL.mp4",
}


def state(folder: str) -> str:
    a = NARR / folder / "v1" / "assembly"
    if (a / "viral_cut_sfx_music_captioned.mp4").exists():
        return "done"
    if list(a.glob("viral_cut*.mp4")):
        return "finish"
    if (NARR / folder / "v1" / "narration.mp3").exists():
        return "visuals"
    return "audio"


def main() -> None:
    rows = [(f, lbl, ps, state(f)) for f, lbl, ps in TARGETS]
    done   = [r for r in rows if r[3] == "done"]
    finish = [r for r in rows if r[3] == "finish"]
    visuals= [r for r in rows if r[3] == "visuals"]
    audio  = [r for r in rows if r[3] == "audio"]
    n_done = len(done) + len(DONE_EXTRA) + 4  # +Psalm22 counts as 1 card but 8 pieces; +pilots in DONE_EXTRA
    total_done_pieces = len(done) + 8 + 3
    remaining = len(finish) + len(visuals) + len(audio)

    def card(cls, tag, tagcol, label, ref, need="", link=""):
        a = f'<div class=need><a href="file:///{(HOME/link).as_posix()}">▶ final</a></div>' if link else (f'<div class=need>{html.escape(need)}</div>' if need else "")
        return (f'<div class="card {cls}"><span class=tag style="background:{tagcol}">{tag}</span>'
                f'<b>{html.escape(label)}</b><br><span class=ref>{html.escape(ref)}</span>{a}</div>')

    P = []
    P.append('<!doctype html><meta charset=utf-8><title>v2 Treatment — Status</title>')
    P.append('''<style>
body{font-family:system-ui,-apple-system,Segoe UI,Roboto,sans-serif;background:#f6f7f8;margin:0;padding:24px 20px 60px;color:#1d2125;line-height:1.45}
h1{font-size:22px;margin:0 0 4px}.as-of{color:#888;font-size:12px;margin-bottom:18px}
h2{font-size:15px;margin:26px 0 10px}.sub{font-size:13px;margin:14px 0 8px}
.bar{height:22px;border-radius:11px;overflow:hidden;display:flex;background:#e6e8ea;max-width:760px;margin:6px 0 4px;font-size:11px;font-weight:700;color:#fff}
.bar span{display:flex;align-items:center;justify-content:center;white-space:nowrap}
.legend{font-size:12px;color:#555;margin-bottom:6px}.dot{display:inline-block;width:10px;height:10px;border-radius:3px;margin:0 4px 0 12px;vertical-align:middle}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(250px,1fr));gap:10px;max-width:1100px}
.card{background:#fff;border-radius:9px;padding:11px 13px;border-left:6px solid #ccc;box-shadow:0 1px 2px rgba(0,0,0,.05)}
.card b{font-size:14px}.card .ref{color:#8a8f94;font-size:11px}.card .need{font-size:12px;color:#444;margin-top:5px}
.card a{color:#1565c0;text-decoration:none;font-size:12px;font-weight:600}.card a:hover{text-decoration:underline}
.done{border-left-color:#2e7d32}.finish{border-left-color:#b8860b}.visuals{border-left-color:#1565c0}.audio{border-left-color:#7e57c2}.retired{border-left-color:#9aa0a6;opacity:.7}
.tag{font-size:10px;font-weight:700;padding:2px 7px;border-radius:10px;color:#fff;float:right}
.note{max-width:760px;font-size:13px;color:#555;background:#fff;border-radius:9px;padding:12px 14px;margin-top:6px}
</style>''')
    P.append('<h1>JesusInTheBible — v2 Treatment Status</h1>')
    P.append('<div class=as-of>auto-generated from disk · "v2 treatment" = clip fixes + element-gated visuals + SFX + cinematic-orchestral score + caption</div>')

    tot = total_done_pieces + remaining
    def pct(n): return max(3, round(100 * n / tot))
    P.append('<div class=bar>'
             f'<span style="background:#2e7d32;width:{pct(total_done_pieces)}%">{total_done_pieces} done</span>'
             f'<span style="background:#b8860b;width:{pct(len(finish))}%">{len(finish)}</span>'
             f'<span style="background:#1565c0;width:{pct(len(visuals))}%">{len(visuals)}</span>'
             f'<span style="background:#7e57c2;width:{pct(len(audio))}%">{len(audio)}</span></div>')
    P.append('<div class=legend>'
             '<span class=dot style="background:#2e7d32"></span>done at v2 bar'
             '<span class=dot style="background:#b8860b"></span>cut exists → finish'
             '<span class=dot style="background:#1565c0"></span>audio done → needs visuals'
             '<span class=dot style="background:#7e57c2"></span>text only → needs audio'
             '<span class=dot style="background:#9aa0a6"></span>retired</div>')
    P.append(f'<div class=note><b>Bottom line: {remaining} left to check &amp; fix.</b> '
             f'{total_done_pieces} finished. Of the {remaining} — {len(finish)} have a cut and need a re-check + finish, '
             f'{len(visuals)} need the full visual build (audio done), and {len(audio)} need audio first.</div>')

    P.append(f'<h2>✅ Done at the v2 bar — {total_done_pieces}</h2><div class=grid>')
    for f, lbl, ps, _ in done:
        P.append(card("done", "done", "#2e7d32", lbl, f"{ps} · FIX-ALL", link=FINAL_LINK.get(f, "")))
    for lbl, ref in DONE_EXTRA:
        P.append(card("done", "done", "#2e7d32", lbl, ref))
    P.append('</div>')

    P.append(f'<h2>⏳ Remaining — {remaining}</h2>')
    if finish:
        P.append('<div class=sub style="color:#b8860b">Cut exists → re-check &amp; finish · ~$2–5 each</div><div class=grid>')
        for f, lbl, ps, _ in finish:
            P.append(card("finish", "finish", "#b8860b", lbl, f"{ps} · has a cut", "re-check cut → SFX + score + caption"))
        P.append('</div>')
    if visuals:
        P.append('<div class=sub style="color:#1565c0">Audio done → needs visual build + assembly + finish · ~$7–9 each</div><div class=grid>')
        for f, lbl, ps, _ in visuals:
            P.append(card("visuals", "visuals", "#1565c0", lbl, ps))
        P.append('</div>')
    if audio:
        P.append('<div class=sub style="color:#7e57c2">Text only → needs audio first, then everything · ~$8–10</div><div class=grid>')
        for f, lbl, ps, _ in audio:
            P.append(card("audio", "audio", "#7e57c2", lbl, f"{ps} · script ready, no audio yet", "synth audio → visuals → assembly → finish"))
        P.append('</div>')

    P.append('<h2 style="color:#9aa0a6">Retired — not in scope</h2><div class=grid>')
    for lbl, ref, tg in RETIRED:
        P.append(card("retired", tg, "#9aa0a6", lbl, ref))
    P.append('</div></html>')

    OUT.write_text("\n".join(P), encoding="utf-8")
    print(f"[v2-status] done={total_done_pieces}  finish={len(finish)}  visuals={len(visuals)}  audio={len(audio)}  -> {OUT}")


if __name__ == "__main__":
    main()
