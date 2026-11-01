"""Property-based tests (Hypothesis) for the checksum validator and corpus generators.

Three families of properties:

1. Check-digit uniqueness: for any digit base, exactly one of the ten possible
   check digits validates (Luhn is permutation-complete).
2. Single-digit error detection: corrupting any one digit of a valid value
   must break validation (the design guarantee of the checksum).
3. Generator/validator agreement: every RAW value the corpus generators
   produce must pass (or at least not fail) the corresponding package
   validator. Rendered surface forms are covered separately: forms the
   recognizers are documented NOT to match (lowercase RAMQ letters,
   lowercase OHIP version codes) are emitted at a low rate on purpose and
   must be the only ones that fail.
"""

from __future__ import annotations

import random
import sys
from pathlib import Path

import pytest
from hypothesis import given, settings
from hypothesis import strategies as st

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "benchmark"))

from pii_generators import (  # noqa: E402
    raw_ca_ab_uli,
    raw_ca_bc_phn,
    raw_ca_ohip,
    raw_ca_ramq,
    raw_ca_sin,
    render_ca_ohip,
    render_ca_ramq,
)

from pii_detector_ca import scan  # noqa: E402
from pii_detector_ca.validators import (  # noqa: E402
    ca_ab_uli_plausible,
    ca_bc_phn_valid,
    ca_ohip_valid,
    ca_ramq_valid,
    ca_sin_valid,
    luhn_check_digit,
    luhn_valid,
    normalize,
)

digits_st = st.text(alphabet="0123456789", min_size=8, max_size=11)


class TestCheckDigitUniqueness:
    @given(base=digits_st)
    def test_luhn_exactly_one_check_digit_validates(self, base):
        valid = [d for d in "0123456789" if luhn_valid(base + d)]
        assert valid == [luhn_check_digit(base)]


class TestSingleDigitErrorDetection:
    @given(
        base=st.text(alphabet="0123456789", min_size=9, max_size=9),
        pos=st.integers(min_value=0, max_value=9),
        delta=st.integers(min_value=1, max_value=9),
    )
    def test_luhn_detects_any_single_digit_substitution(self, base, pos, delta):
        full = base + luhn_check_digit(base)
        corrupted = full[:pos] + str((int(full[pos]) + delta) % 10) + full[pos + 1 :]
        assert corrupted != full
        assert not luhn_valid(corrupted)


# (generator, validator, must_pass): plausibility validators return None for
# plausible values, so for those we only require "not False".
GENERATOR_VALIDATOR_PAIRS = [
    (raw_ca_sin, ca_sin_valid, True),
    (raw_ca_ohip, ca_ohip_valid, True),
    (raw_ca_ramq, ca_ramq_valid, True),
    (raw_ca_bc_phn, ca_bc_phn_valid, True),
    (raw_ca_ab_uli, ca_ab_uli_plausible, False),
]


class TestGeneratorValidatorAgreement:
    @pytest.mark.parametrize(
        "gen,validate,must_pass",
        GENERATOR_VALIDATOR_PAIRS,
        ids=[g.__name__ for g, _, _ in GENERATOR_VALIDATOR_PAIRS],
    )
    @given(seed=st.integers(min_value=0, max_value=2**32 - 1))
    @settings(max_examples=50)
    def test_generated_value_validates(self, gen, validate, must_pass, seed):
        value = gen(random.Random(seed))
        result = validate(value)
        if must_pass:
            assert result is True
        else:
            assert result is not False  # plausibility: None (plausible) expected

    @given(seed=st.integers(min_value=0, max_value=2**32 - 1))
    @settings(max_examples=50)
    def test_rendered_forms_fail_only_where_documented(self, seed):
        rng = random.Random(seed)
        value, form = render_ca_ohip(rng)
        assert ca_ohip_valid(value) == (not form.endswith("version_lower")), (value, form)
        value, form = render_ca_ramq(rng)
        # The RAMQ validator is case-insensitive; the case-sensitive PATTERN
        # is what rejects lowercase letter blocks, so check via scan().
        assert ca_ramq_valid(value)
        assert bool(scan(value, entities=["CA_RAMQ"])) == (form != "lowercase"), (value, form)

    @given(seed=st.integers(min_value=0, max_value=2**32 - 1))
    @settings(max_examples=50)
    def test_normalize_strips_generated_sin_to_nine_digits(self, seed):
        value = raw_ca_sin(random.Random(seed))
        cleaned = normalize(value)
        assert len(cleaned) == 9 and cleaned.isdigit()
        assert cleaned[0] not in "08"

    @given(seed=st.integers(min_value=0, max_value=2**32 - 1))
    @settings(max_examples=50)
    def test_ramq_letters_follow_patient_name(self, seed):
        rng = random.Random(seed)
        value = raw_ca_ramq(rng, surname="Tremblay", first_name="Émile")
        assert value[:4] == "TREÉ"
