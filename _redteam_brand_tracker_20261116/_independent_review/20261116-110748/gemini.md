# Independent review — gemini (OK, 162s)

This plan introduces severe data corruption risks, breaks existing metadata, and fails to fully execute the owner's requirements. 

Here are the specific defects:

**1. Ledger Corruption via Broken JS Split (Data Loss Risk)**
In `build_upload_tracker.py`, the `all_cmds` function attempts to parse the slug and platform from the input ID:
`const [_, slug, plat] = i.id.split('_');`
Because almost all of your slugs contain underscores (e.g., `it_is_finished_john1930`, `episode_04_naaman`), this split is fundamentally broken. It will split into `["u", "it", "is", "finished", ...]`, assigning `slug="it"` and `plat="is"`. If the user clicks "COPY ALL", it will generate commands like `upload_tracker.py --set it is "..."`, writing garbage data to your ledger. 

**2. Hardcoded Script Path Breaks Swirls Ledger**
Also in `all_cmds` in `build_upload_tracker.py`, the generated command hardcodes the main tracker:
`lines.push('.venv\\\\Scripts\\\\python.exe upload_tracker.py --set ' + slug + ...)`
For Swirls cards, the individual "COPY command" button correctly routes to `poc_living_water_ink_style_test\swirls_upload_tracker.py`. But if a user uses the "COPY ALL" button, Swirls URLs will be routed to the *main* ledger using the wrong script, corrupting the main catalog with Swirls entries.

**3. Hashtag Formatting Destroyed by Regex**
In `tools_strip_awakeden.py`, the fallback regex is:
`t = re.sub(r"\b[Aa]wakeden\b", "Salt and Light Kingdom", t)`
Because `#` is a non-word character, the word boundary `\b` matches immediately before the `a` in `#awakeden`. This will blindly replace `#awakeden` with `#Salt and Light Kingdom`. Injecting spaces into a hashtag breaks it entirely across all historical publish packs.

**4. Verification Gap: Thumbnails Still Have the Old Logo**
The plan provides a "Video logo patch script" to strip the burned-in logo from 17 unposted videos, and `pipeline/channel_dress.py` was updated to return `0.0` to prevent future renders from drawing it. However, there is no step to regenerate the *existing* thumbnails for those 17 videos. Because `thumbnails.py` skips files that already exist on disk, those 17 unposted thumbnails still have the Awakeden logo burned into them, violating the owner's explicit rule to "remove at $0".

**5. Missing Cross-Platform Links in Old Packs**
In `tools_strip_awakeden.py`, the script surgically replaces the YouTube handle:
`t.replace("@awakeden (https://youtube.com/@awakeden)", f"{YT_H} ({YT_U})")`
However, it completely fails to inject the newly minted TikTok, Facebook, and Instagram handles into the `Follow:` block of existing `youtube_short.md` and `facebook.md` files. While newly generated packs will get all four links (via `upload_engine.py`), the historical unposted packs will only promote the YouTube channel, creating a fragmented brand presence.

VERDICT: FAIL
TOP FIXES:
1. Rewrite the JS in `build_upload_tracker.py` to extract the slug and platform safely (e.g., using `dataset` attributes instead of `split('_')`) and conditionally route Swirls inputs to `swirls_upload_tracker.py`.
2. Fix the regex in `tools_strip_awakeden.py` to explicitly handle `#awakeden` without injecting spaces (e.g., `#SaltAndLightKingdom`).
3. Add a mandatory step to delete and regenerate the thumbnails for the 17 patched videos so the old logo is actually removed from the image assets.
