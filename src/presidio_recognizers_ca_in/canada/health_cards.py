"""Canadian provincial health card recognizers."""

from ..adapters.presidio import SpecRecognizer


class OhipRecognizer(SpecRecognizer):
    entity_id = "CA_OHIP"


class RamqRecognizer(SpecRecognizer):
    entity_id = "CA_RAMQ"


class BcPhnRecognizer(SpecRecognizer):
    entity_id = "CA_BC_PHN"


class AlbertaUliRecognizer(SpecRecognizer):
    entity_id = "CA_AB_ULI"


class GenericCaHealthCardRecognizer(SpecRecognizer):
    entity_id = "CA_HEALTH_CARD"
