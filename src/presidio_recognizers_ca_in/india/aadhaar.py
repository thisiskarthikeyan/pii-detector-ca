"""Aadhaar number recognizer (Verhoeff-validated)."""

from ..adapters.presidio import SpecRecognizer


class AadhaarRecognizer(SpecRecognizer):
    entity_id = "IN_AADHAAR"
