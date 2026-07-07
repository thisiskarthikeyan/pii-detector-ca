"""Canadian postal code recognizer (address context)."""

from ..adapters.presidio import SpecRecognizer


class CaPostalCodeRecognizer(SpecRecognizer):
    entity_id = "CA_POSTAL_CODE"
