"""Indian mobile numbers, PIN codes, Voter ID (EPIC), and passport numbers."""

from presidio_analyzer import Pattern

from ..base import ValidatedPatternRecognizer
from ..validators import in_mobile_valid


class InMobileRecognizer(ValidatedPatternRecognizer):
    """Mobile: optional +91 / 0 prefix, 10 digits starting 6-9."""

    def __init__(self):
        super().__init__(
            supported_entity="IN_MOBILE",
            patterns=[
                Pattern(
                    name="in_mobile_prefixed",
                    regex=r"(?:\+91[- ]?|\b0)?[6-9]\d{4}[- ]?\d{5}\b",
                    score=0.4,
                ),
            ],
            context=["mobile", "phone", "contact", "whatsapp", "मोबाइल"],
            validator=in_mobile_valid,
        )


class InPinCodeRecognizer(ValidatedPatternRecognizer):
    """Postal PIN: 6 digits, first digit 1-9; context-gated (weak pattern)."""

    def __init__(self):
        super().__init__(
            supported_entity="IN_PIN_CODE",
            patterns=[
                Pattern(name="in_pin", regex=r"\b[1-9]\d{5}\b", score=0.05),
            ],
            context=["pin", "pincode", "pin code", "postal", "address", "पिन"],
            validator=None,
        )


class InVoterIdRecognizer(ValidatedPatternRecognizer):
    """Voter ID (EPIC): 3 letters + 7 digits."""

    def __init__(self):
        super().__init__(
            supported_entity="IN_VOTER_ID",
            patterns=[
                Pattern(name="in_voter_id", regex=r"\b[A-Z]{3}\d{7}\b", score=0.4),
            ],
            context=["voter", "epic", "election", "proof", "id proof", "मतदाता"],
            validator=None,
        )


class InPassportRecognizer(ValidatedPatternRecognizer):
    """Indian passport: one letter (no Q/X/Z) + 7 digits, first digit 1-9."""

    def __init__(self):
        super().__init__(
            supported_entity="IN_PASSPORT",
            patterns=[
                Pattern(
                    name="in_passport",
                    regex=r"\b[A-PR-WY][1-9]\d{6}\b",
                    score=0.4,
                ),
            ],
            context=["passport", "proof", "id proof", "पासपोर्ट"],
            validator=None,
        )
