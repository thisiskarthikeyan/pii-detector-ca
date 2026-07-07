"""PAN (Permanent Account Number) recognizer."""

from ..adapters.presidio import SpecRecognizer


class PanRecognizer(SpecRecognizer):
    entity_id = "IN_PAN"
