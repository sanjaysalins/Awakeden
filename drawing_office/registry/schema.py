"""Drawing Office device registry -- plain-dict loader/validator.

No external deps beyond stdlib (json, pathlib). Every device in the registry
is a JSON "card" describing one $0-first visual device (a reusable mechanic
for turning one or two rendered plates into a full beat), proven or being
proven against the poc_bethesda_style_test/ galleries. See
drawing_office/registry/cards/*.json for the cards themselves.
"""
from __future__ import annotations

import json
from pathlib import Path

REQUIRED_FIELDS = [
    "name",
    "conceit",
    "shape_fit",
    "plate_bill",
    "derived_views",
    "motion_slots",
    "generation_alignment",
    "risk_flags",
    "accuracy_spec",
    "beat_template",
    "caption_lane",
    "lettering",
    "score_shape",
    "sfx_palette",
    "status",
    "evidence",
]

# Status rank, most-proven first. Higher-status cards should be reached for
# before lower-status ones when several cards fit the same shape.
_STATUS_RANK = [
    "proven-episode",
    "proven-poc",
    "stills-tested-clean",
    "stills-tested",
    "stills-tested-recovered",
    "stills-tested-flagged",
    "mechanics-proven",
    "concept",
    "retired",
]

CARDS_DIR = Path(__file__).resolve().parent / "cards"


def load_card(path: Path) -> dict:
    """Read and validate one JSON card. Raises ValueError naming any missing
    required field(s)."""
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    missing = [f for f in REQUIRED_FIELDS if f not in data]
    if missing:
        raise ValueError(
            f"{path}: card is missing required field(s): {', '.join(missing)}"
        )
    return data


def load_registry(dir: Path = None) -> dict:
    """Load every *.json file in drawing_office/registry/cards/ (or `dir` if
    given), keyed by each card's own "name" field. Raises ValueError on a
    duplicate name."""
    cards_dir = Path(dir) if dir is not None else CARDS_DIR
    registry: dict[str, dict] = {}
    for path in sorted(cards_dir.glob("*.json")):
        card = load_card(path)
        name = card["name"]
        if name in registry:
            raise ValueError(
                f"duplicate card name '{name}': already loaded from another "
                f"file before {path}"
            )
        registry[name] = card
    return registry


def query_by_shape(registry: dict, shape: str) -> list:
    """Return cards whose shape_fit.primary or shape_fit.secondary contains
    `shape`, sorted most-proven first (see _STATUS_RANK)."""
    matches = [
        card for card in registry.values()
        if shape in card["shape_fit"].get("primary", [])
        or shape in card["shape_fit"].get("secondary", [])
    ]

    def rank(card: dict) -> int:
        status = card["status"]
        try:
            return _STATUS_RANK.index(status)
        except ValueError:
            # Unknown status sorts last (least trusted).
            return len(_STATUS_RANK)

    return sorted(matches, key=rank)


def assert_no_alignment_risk(card: dict) -> None:
    """The strongest guardrail in the system: every card MUST declare
    generation_alignment == "forbidden" (no partial credit, no other value
    accepted). Raises ValueError otherwise."""
    value = card.get("generation_alignment")
    if value != "forbidden":
        raise ValueError(
            f"card '{card.get('name', '<unknown>')}' has "
            f"generation_alignment={value!r}, must be exactly 'forbidden'"
        )


if __name__ == "__main__":
    registry = load_registry()
    for card in registry.values():
        assert_no_alignment_risk(card)
    print(f"loaded {len(registry)} cards, all generation_alignment=forbidden OK\n")
    for name in sorted(registry):
        card = registry[name]
        print(f"{card['name']:<22} status={card['status']}")
