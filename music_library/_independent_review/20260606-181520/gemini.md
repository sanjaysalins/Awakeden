# Independent review — gemini (OK, 49s)

This revision is much more honest about what is actually built and enforces strong discipline with the test-gate, successfully addressing the Round 1 complaints. However, it still contains fatal logical gaps in how the audio engine will actually operate on these files.

Here are the concrete findings:

**1. The "Swell Alignment" Magic Trick (Missing Metadata)**
*   **Citation:** *"align a track's swell to the CTA timestamp"* (Under NOT built yet)
*   **Critique:** How exactly does an automated python/FFmpeg pipeline magically find the "swell" in an un-stemmed, opaque Suno MP3? It can't. If the Phase-1 pilot is supposed to align a swell to a CTA, the exact timestamp of that swell must be logged in the library. Yet, neither `ingest.py` nor `approve.py` mentions adding `swell_ms` or `climax_ms` metadata. Without this data point, the placer is unbuildable. 

**2. Broken Layering Logic in `find_for_beat`**
*   **Citation:** *"Layering: only `glory_*` beds (melody-free, rhythm-free) may sit UNDER a melodic bed... [Matrix:] conviction | glory, neutral, pastoral, sacred, tender"*
*   **Critique:** The plan says `glory` tracks are layers, but maps them into the exact same doctrine matrix array as the primary beds (`neutral, pastoral`, etc). If `find_for_beat` just returns a random approved track for `conviction`, it might return ONLY a `glory` pad (leaving you with no primary bed), or it might return a `sacred` bed but the pipeline has no instructions on how/when to simultaneously fetch a `glory` bed for layering. The code logic for dual-track selection vs single-track selection is missing.

**3. Naive Generation Assumptions (Suno Realities)**
*   **Citation:** *"Count: 20 prompts × 2 takes = 40 raw files → audition → keep the best (≤20 final beds)."*
*   **Critique:** This assumes a 50% hit rate for Suno v5.5. Every prompt explicitly asks for "no drums" or "no percussion". Suno notoriously ignores negative prompts and forces rhythm into tracks. Expecting to get a usable, completely drum-free orchestral bed from exactly two takes is practically guaranteed to fail. You need a workflow that allows for dropping in takes `c, d, e, f` when `a` and `b` inevitably have ghost snares.

**4. The "Placer" is Handwaved, Not Planned**
*   **Citation:** *"Build + prove the generate→trim→align→duck loop on one real short"*
*   **Critique:** You accurately identified that `enhance.py` doesn't do this, but you didn't actually write a plan for how to build it. You just listed the verbs. Does the ducking use FFmpeg's `sidechaincompress`? How do you trim from the end without abrupt cutoffs (fade-outs)? A plan to "figure it out later" isn't a technical design.

VERDICT: REVISE
TOP FIXES:
1. Add a mandatory `swell_time_ms` (or similar) metadata field to `approve.py` and the library index, otherwise the "align to CTA" feature is impossible.
2. Update the `find_for_beat` logic/matrix to explicitly handle layer/pad selection as distinct from primary melodic bed selection. 
3. Explicitly define the technical architecture for the Phase-1 placer (FFmpeg sidechaining, fade-out logic, timeline math) rather than just stating the goal to "build + prove" it.
