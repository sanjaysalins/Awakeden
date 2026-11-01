# Independent review — gemini (OK, 117s)

Here is the independent review of the upload kit.

### Findings

**1. Ignored Red-Team Verdict on Title (Honesty/Doctrine)**
The in-engine red-team explicitly flagged the title `"God Hung Up a Snake. It Was the Cure."` with a `REVISE` verdict, noting that it overstates the text because the cure required the active step of *looking* at it. The red-team suggested using a question hook or changing it to `"God Hung Up a Snake. Looking at It Saved Them."` The generator completely ignored this mandatory feedback and retained the flagged title across all platforms.

**2. SEO Dishonesty / Tag Stuffing (Platform Fit)**
Under the **YouTube (Long-form 16:9)** section, the TAGS block includes `"bible shorts"`. Including a shorts-specific tag on a 16:9 long-form video is inaccurate tag-stuffing and violates SEO honesty. 

**3. Format Contradiction (Platform Fit)**
The metadata header explicitly states `Format: short`. However, the kit generates a full **YouTube (Long-form 16:9)** section. If this video is only a vertical short, the long-form section should not exist. If it is a dual-format release, the long-form description should be adapted for 16:9 audiences rather than being a 1:1 copy-paste of the Short description.

VERDICT: REVISE
TOP FIXES:
1. Change the title to respect the red-team's doctrinal precision flag (e.g., "God Hung Up a Snake. Looking at It Saved Them.").
2. Remove the "bible shorts" tag from the YouTube Long-form section.
3. Remove the YouTube Long-form section entirely if this asset is strictly a Short, as the header indicates.
