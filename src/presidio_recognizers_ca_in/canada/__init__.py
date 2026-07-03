from .health_cards import (
    AlbertaUliRecognizer,
    BcPhnRecognizer,
    GenericCaHealthCardRecognizer,
    OhipRecognizer,
    RamqRecognizer,
)
from .postal_code import CaPostalCodeRecognizer
from .sin import CaSinRecognizer
from .street_address import CaStreetAddressRecognizer

__all__ = [
    "CaSinRecognizer",
    "OhipRecognizer",
    "RamqRecognizer",
    "BcPhnRecognizer",
    "AlbertaUliRecognizer",
    "GenericCaHealthCardRecognizer",
    "CaPostalCodeRecognizer",
    "CaStreetAddressRecognizer",
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
        CaStreetAddressRecognizer(),
    ]
