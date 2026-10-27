"""Framework-neutral identifier detection core (stdlib only).

Use ``scan()`` for Presidio-free detection. Presidio integration lives in
``pii_detector_ca.adapters.presidio``.
"""

from .scanner import DEFAULT_THRESHOLD, MAX_SCORE, scan
from .specs import ENTITY_IDS, get_entity_spec, get_entity_specs
from .types import EntitySpec, Match, PatternSpec

__all__ = [
    "DEFAULT_THRESHOLD",
    "MAX_SCORE",
    "ENTITY_IDS",
    "EntitySpec",
    "Match",
    "PatternSpec",
    "get_entity_spec",
    "get_entity_specs",
    "scan",
]
