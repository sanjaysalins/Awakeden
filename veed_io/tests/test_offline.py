"""Offline tests — no FAL_KEY and no fal-client install required.

Run:  python -m veed_io.tests.test_offline
"""

from __future__ import annotations

from veed_io.models import (
    PresetCustomization,
    SubtitleRequest,
    SubtitleResult,
    TextCustomization,
)
from veed_io.pricing import estimate_cost
from veed_io.presets import is_dynamic_preset


def test_arguments_omit_none() -> None:
    req = SubtitleRequest(video_url="https://x/clip.mp4", preset="glass")
    assert req.to_arguments() == {
        "video_url": "https://x/clip.mp4",
        "preset": "glass",
    }


def test_arguments_full() -> None:
    req = SubtitleRequest(
        video_url="https://x/clip.mp4",
        preset="simple",
        language="en-US",
        customization=PresetCustomization(
            position="bottom",
            shadow="max",
            baseline=TextCustomization(font="Inter", weight=400, color="#fff"),
            highlighted=TextCustomization(weight=800),
        ),
    )
    args = req.to_arguments()
    assert args["language"] == "en-US"
    assert args["customization"]["position"] == "bottom"
    assert args["customization"]["shadow"] == "max"
    assert args["customization"]["text_customizations"]["baseline"]["font"] == "Inter"
    assert args["customization"]["text_customizations"]["highlighted"] == {"weight": 800}


def test_validation_errors() -> None:
    for bad in [
        SubtitleRequest(video_url="", preset="glass"),
        SubtitleRequest(video_url="x", preset="not-a-preset"),
        SubtitleRequest(video_url="x", preset="glass",
                        srt_file_url="a", srt_content="b"),
    ]:
        try:
            bad.to_arguments()
        except ValueError:
            continue
        raise AssertionError(f"expected ValueError for {bad}")


def test_weight_bounds() -> None:
    try:
        TextCustomization(weight=1200).to_dict()
    except ValueError:
        pass
    else:
        raise AssertionError("expected ValueError for weight 1200")


def test_pricing() -> None:
    assert is_dynamic_preset("glass") is True
    assert is_dynamic_preset("simple") is False
    # 60s basic = $0.10 ; 60s dynamic = $0.20
    assert estimate_cost(60, "simple").usd == 0.10
    assert estimate_cost(60, "glass").usd == 0.20


def test_result_parse() -> None:
    resp = {"video": {"url": "https://x/out.mp4", "content_type": "video/mp4",
                       "file_size": 123}}
    res = SubtitleResult.from_response(resp, request_id="abc")
    assert res.video_url == "https://x/out.mp4"
    assert res.file_size == 123
    assert res.request_id == "abc"


def main() -> int:
    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    for t in tests:
        t()
        print(f"ok  {t.__name__}")
    print(f"\n{len(tests)} passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
