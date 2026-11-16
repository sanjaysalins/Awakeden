# Independent review — gemini (OK, 147s)

Here are the adversarial findings based on your specified lens:

**Feasibility against the real codebase / tools:**
- The plan asks Sonnet to build "one template (episode words + timings in, film out)." This bypasses the repo's existing `cli_assemble.py` engine, which handles dynamic speed-first/trim-past-cap allocation. By forcing rigid "timings in" to a template, you are replacing an intelligent, cut-aware audio-jigsaw assembly with a brittle, static script.

**Hidden risks, false assumptions, single points of failure:**
- **FALSE ASSUMPTION:** The plan acknowledges "expect Spanish/German ~25% longer" but simultaneously relies on "a word-free master film." You cannot drop a 47-second German audio track onto a 38-second master film. The audio length must dictate the video cuts, or you will lose sync and run out of footage.
- **PLATFORM LIMITATION:** YouTube does not support "a separate swappable lettering layer per language." You can swap audio and SRTs on a single video, but any on-screen graphical layers or translated verse chips must be burned in. If you have on-screen text, you must render and upload entirely separate MP4s to separate channels.

**Over-engineering / premature building:**
- Option A proposes designing the doodle kit ("ink circle drawn around the thief's face as he speaks") before proving its technical viability. Generative AI clips have unpredictable framing. Automating spatial doodles requires either a Claude Vision pass to find the face coordinates or manual X/Y entry per clip. Building a fully automated template before solving this mapping is premature.

**Missing steps, edge cases, or verification gaps:**
- There is no step to reconcile the translated narrator script with the foreign Bible translation. The hook relies on mirroring exact text ("To day shalt thou..." -> "Not someday. Today."). If the Spanish Reina-Valera 1909 uses different vocabulary for "paradise" or "today," a direct translation of the narrator script will break the rhetorical contrast. 

**Reuse: does it duplicate tools that already exist?**
- The plan effectively forks the pipeline. The repo already contains "$0 deterministic devices" and an assembly engine. Proposing a standalone "template" to ingest words and output a film duplicates the assembly stage rather than integrating motion graphics as a reusable stage within the existing `cli_assemble.py` or Remotion structures.

**Cost / spend and whether it's justified:**
- The quoted cost ("clips ~$8-12") only accounts for generating the base clips. It completely ignores the rendering and compute costs of generating multiple localized MP4s, which will be mandatory because YouTube doesn't support dynamic visual layers.

***

### ADDITIONAL CONTEXT / BRIEF

**(1) What is missing:**
The physical reality of video distribution. The plan assumes you can have one global upload with swappable graphical text layers. Since this feature doesn't exist on YouTube, you must choose between completely text-free global visuals (relying strictly on SRTs) or rendering/uploading separate localized videos.

**(2) What would you do INSTEAD if you were designing this formula from scratch:**
I would pass each localized audio track through a dynamic assembly pipeline (like the existing engine or a dynamic Remotion equivalent) so that the cuts and doodle timings snap specifically to the foreign audio length. I would render hardcoded, localized MP4s for separate language channels rather than chasing a mythical global "master film."

**(3) Biggest risk the formula gets stale or repetitive:**
The rigid "two contrast pairs" paradox structure. Not every Bible passage naturally contains a clean binary contrast. Forcing this hook onto every episode will lead to artificial, stretched exegesis that violates the standing rule: "surprising about the text, never about the truth."

**(4) Multi-language/SRT pitfalls not covered:**
The English script's wordplay is deeply tied to the KJV. Translating the SRTs without completely rewriting the narrator's script around the target language's specific public-domain Bible phrasing will destroy the landing's impact. 

**(5) Doodle/motion-graphic pitfalls:**
Doodles anchored to the footage ("ink arrow from his cross to Jesus") require precise X/Y coordinate tracking. Because generative clips do not have standardized framing, a generic template cannot accurately place these doodles without manual spatial mapping per shot.

VERDICT: FAIL
TOP FIXES:
1. Abandon the "word-free master film" concept; you must re-time and render separate videos per language to account for the ~25% audio expansion.
2. Remove the "swappable lettering layer" assumption for a single global upload; YouTube does not support localized video layers, requiring hardcoded localized MP4s.
3. Add a verification step to ensure the localized narrator script's wordplay actually matches the vocabulary of the chosen public-domain foreign Bible translation.
