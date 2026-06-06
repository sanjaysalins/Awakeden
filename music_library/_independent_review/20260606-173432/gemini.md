# Independent review — gemini (OK, 27s)

The plan is well-organized, doctrinally sound, and clearly integrated with the existing pipeline concepts. The adversarial red-team section correctly identifies several real-world AI music generation risks (vocals, drums, clash). However, the plan fundamentally misunderstands how music arcs map to short-form video and relies on a tool (`enhance.py`) to do something it likely cannot do.

**1. Fatal Flaw: Arbitrary trimming destroys the 60s emotional arc**
*Claim:* "Mitigation: we don't need the whole track — `enhance.py` trims to any window and picks the in-point, so a 2–3 min Suno track gives several usable 60s sections." (Red-Team #6)
*Critique:* This completely breaks your Gospel Five-Beat structure (Hook/Point/Proof/Conviction/Landing). A 60s short requires the music to build and climax *exactly* in sync with the script's Conviction and Landing. If you generate a 3-minute track that takes 90 seconds to reach its climax, and you arbitrarily slice out a 60-second window, the music will either have no climax or climax at the wrong time. You cannot just "pick an in-point"; the track's structural climax must be aligned to the timing of the spoken CTA.

**2. False Capability: `enhance.py` cannot intelligently edit music**
*Claim:* "`enhance.py` trims to any window and picks the in-point"
*Critique:* Based on the directory structure, `11labs-testing/enhance.py` is almost certainly a script for processing/enhancing ElevenLabs voice generation, not an intelligent music editor that can detect musical phrases, beats, or climaxes to find perfect "in-points". Relying on this for automated music editing is a massive false assumption.

**3. Tool limitation: Suno ignores exact BPM numbers**
*Claim:* Prompts include exact tempos like `~48 bpm`, `~62 bpm`, `~108 bpm`.
*Critique:* Suno's LLM prompt parser does not reliably comprehend or execute exact numerical BPMs. It interprets musical descriptors. Using "adagio", "largo", "allegro", "very slow", or "driving tempo" is much more reliable than "62 bpm". 

**4. Missing Verification: Stems / Bleed**
*Claim:* "Suno sometimes adds 'aah' vocal pads... reject vocal takes" (Red-Team #5)
*Critique:* Even with Instrumental toggled ON, Suno frequently bleeds vocal-like artifacts or heavy mix mud into the mid-range where the narration sits. The plan lacks a verification step to run the generated audio through a stem splitter (like UVR or Demucs) or an EQ analyzer to ensure the vocal frequencies (1kHz - 4kHz) aren't too crowded for the ElevenLabs voice to cut through.

VERDICT: REVISE
TOP FIXES:
1. Fix the 60s shorts music strategy: You must define a programmatic way to align the music's climax with the script's CTA beat (e.g., aligning the track's loudest LUFS peak to the timestamp of the Conviction beat), rather than arbitrarily slicing a 60s window.
2. Remove the reliance on `enhance.py` for music trimming and assign this logic to the actual assembly pipeline (e.g., `pipeline/assembly_timing.py` or a dedicated music editor script).
3. Replace exact numerical BPMs in the Suno prompts with standard musical tempo descriptors (Adagio, Moderato, Presto) to improve generation adherence.
