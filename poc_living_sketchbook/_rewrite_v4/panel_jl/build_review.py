import html
t=open('candidates/jl_FINAL_PROPOSED.txt',encoding='utf8').read()
spoken=[l for l in t.splitlines() if not l.startswith('[')]
chars=sum(len(l) for l in spoken)
old=open('../../../poc_living_water_ink_style_test/swirls_pilot_01_jacobs_ladder/narration.md',encoding='utf8').read().strip()
def block(s): return ''.join(f'<p class="{"sil" if l.startswith("[") else ""}">{html.escape(l)}</p>' for l in s.splitlines() if l.strip())
page=f'''<!doctype html><meta charset="utf-8"><title>Jacob's Ladder words</title>
<style>body{{font:20px/1.5 Georgia,serif;max-width:760px;margin:24px auto;padding:0 16px;background:#faf6ee;color:#222}}
h1{{font-size:28px}}.c{{background:#fff;border:2px solid #c9b88a;border-radius:10px;padding:8px 18px;margin:14px 0}}
.sil{{color:#888;font-style:italic;font-size:16px}}.bad{{border-color:#c66}}.good{{border-color:#4a8}}
td,th{{border:1px solid #ccc;padding:6px 10px;font-size:17px}}table{{border-collapse:collapse}}</style>
<h1>Jacob's Ladder: new words</h1>
<p><b>Words only. Picking does NOT spend money.</b></p>
<h2>Before (old)</h2><div class="c bad">{block(old)}</div>
<h2>After (proposed, 142 words)</h2><div class="c good">{block(t)}</div>
<h2>What was fixed</h2><ul>
<li>Stock ending "Ready to stop running...?" gone. Now: "Jacob never climbed that ladder. God came to him first."</li>
<li>No more "..." inside quotes. All KJV, unbroken.</li>
<li>"Jesus said He is that ladder" gone. Now only Jesus' own words (John 1:51).</li>
<li>Now says WHY Jacob runs.</li>
<li>Guesses about Jacob's guilt removed.</li></ul>
<h2>Blind reader scores (3 readers, 2 rounds)</h2>
<table><tr><th></th><th>Hook</th><th>Payoff</th><th>Landing</th><th>Clarity</th></tr>
<tr><td>Round 1 best (Z)</td><td>6-8</td><td>9</td><td>8-10</td><td>7-9</td></tr>
<tr><td>Round 2 (fixed)</td><td>6-9</td><td>8</td><td>8-10</td><td>7-9</td></tr></table>
<h2>Still weak</h2><ul>
<li>"ye shall see heaven open" is old English. One reader tuned out.</li>
<li>Why Jesus' echo matters is left unsaid. Kept on purpose: John 1:51 is what He said.</li>
<li>"Blessing" is not explained for a newcomer.</li>
<li>Simulated readers are not real people. Real seed viewers still recommended.</li></ul>
<h2>Next costs money (not started)</h2>
<p>Re-record voice: about {chars} characters, roughly <b>$0.15 to $0.20</b> (ElevenLabs). Then the video timing is rebuilt ($0 CPU), then pack and thumbnails ($0).</p>
<p><b>Say "lock words" to lock. Say "record" separately to spend.</b></p>'''
open('REVIEW_JL_WORDS.html','w',encoding='utf8').write(page)
print(chars)
