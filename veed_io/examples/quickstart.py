"""Minimal end-to-end example for veed_io.

Run from the repo root with FAL_KEY set:

    python veed_io/examples/quickstart.py
"""

from veed_io import SubtitleRequest, VeedSubtitlesClient
from veed_io.models import PresetCustomization, TextCustomization

# fal's own public sample clip.
SAMPLE = (
    "https://v3b.fal.media/files/b/0a967ce5/"
    "iARc_J0kLN9OEmiXnxT3l_substyle-example-input.mp4"
)


def main() -> None:
    client = VeedSubtitlesClient()  # reads FAL_KEY from the environment

    request = SubtitleRequest(
        video_url=SAMPLE,
        preset="glass",                     # dynamic preset (2x price)
        language="en-US",                   # source-audio language
        customization=PresetCustomization(
            position="bottom",
            shadow="mid",
            highlighted=TextCustomization(color="#FFD400", weight=800),
        ),
    )

    # Show what it will roughly cost (assume the sample is ~12s).
    print(client.estimate(12, request.preset))

    result = client.subtitle(request, on_log=lambda m: print(f"  {m}"))
    print("output:", result.video_url)

    saved = client.download(result, "./veed_io/out/")
    print("saved :", saved.resolve())


if __name__ == "__main__":
    main()
