"""ABHA (Ayushman Bharat Health Account) number recognizer."""

from ..adapters.presidio import SpecRecognizer


class AbhaRecognizer(SpecRecognizer):
    entity_id = "IN_ABHA"
