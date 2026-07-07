"""Indian mobile numbers, PIN codes, Voter ID (EPIC), and passport numbers."""

from ..adapters.presidio import SpecRecognizer


class InMobileRecognizer(SpecRecognizer):
    entity_id = "IN_MOBILE"


class InPinCodeRecognizer(SpecRecognizer):
    entity_id = "IN_PIN_CODE"


class InVoterIdRecognizer(SpecRecognizer):
    entity_id = "IN_VOTER_ID"


class InPassportRecognizer(SpecRecognizer):
    entity_id = "IN_PASSPORT"
