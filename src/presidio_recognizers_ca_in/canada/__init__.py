from .health_cards import (
    AlbertaUliRecognizer,
    BcPhnRecognizer,
    GenericCaHealthCardRecognizer,
    OhipRecognizer,
    RamqRecognizer,
)
from .postal_code import CaPostalCodeRecognizer
from .sin import CaSinRecognizer

__all__ = [
    "CaSinRecognizer",
    "OhipRecognizer",
    "RamqRecognizer",
    "BcPhnRecognizer",
    "AlbertaUliRecognizer",
    "GenericCaHealthCardRecognizer",
    "CaPostalCodeRecognizer",
]


def get_canada_recognizers() -> list:
    return [
        CaSinRecognizer(),
        OhipRecognizer(),
        RamqRecognizer(),
        BcPhnRecognizer(),
        AlbertaUliRecognizer(),
        GenericCaHealthCardRecognizer(),
        CaPostalCodeRecognizer(),
    ]
