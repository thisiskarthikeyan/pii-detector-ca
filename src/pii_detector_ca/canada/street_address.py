"""Canadian civic street address recognizer (plan item 3.9)."""

from ..adapters.presidio import SpecRecognizer


class CaStreetAddressRecognizer(SpecRecognizer):
    entity_id = "CA_STREET_ADDRESS"
