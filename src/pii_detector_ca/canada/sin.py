"""Canadian Social Insurance Number (SIN) recognizer."""

from ..adapters.presidio import SpecRecognizer


class CaSinRecognizer(SpecRecognizer):
    entity_id = "CA_SIN"
