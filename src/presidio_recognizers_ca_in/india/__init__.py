from .aadhaar import AadhaarRecognizer
from .abha import AbhaRecognizer
from .misc import (
    InMobileRecognizer,
    InPassportRecognizer,
    InPinCodeRecognizer,
    InVoterIdRecognizer,
)
from .pan import PanRecognizer
from .uhid import UhidRecognizer

__all__ = [
    "AadhaarRecognizer",
    "AbhaRecognizer",
    "PanRecognizer",
    "UhidRecognizer",
    "InMobileRecognizer",
    "InPinCodeRecognizer",
    "InVoterIdRecognizer",
    "InPassportRecognizer",
]


def get_india_recognizers() -> list:
    return [
        AadhaarRecognizer(),
        AbhaRecognizer(),
        PanRecognizer(),
        UhidRecognizer(),
        InMobileRecognizer(),
        InPinCodeRecognizer(),
        InVoterIdRecognizer(),
        InPassportRecognizer(),
    ]
