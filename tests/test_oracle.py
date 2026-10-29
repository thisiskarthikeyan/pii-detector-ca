"""Package validators vs. the independent reference checksums.

``benchmark/checksums_ref.py`` is written from the published algorithms
without importing the package; the corpus generators use it. These tests
pin the two implementations to each other on random input and on fixed
vectors, so a bug shared by generator and validator cannot hide as 1.0
recall.
"""

from __future__ import annotations

import random
import sys
from pathlib import Path

import pytest
from hypothesis import given, settings
from hypothesis import strategies as st

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "benchmark"))

from checksums_ref import (  # noqa: E402
    bc_phn_check,
    bc_phn_ok,
    luhn_append,
    luhn_ok,
    ohip_ok,
    ramq_ok,
    sin_ok,
)
from pii_generators import (  # noqa: E402
    raw_ca_bc_phn,
    raw_ca_ohip,
    raw_ca_ramq,
    raw_ca_sin,
)

from pii_detector_ca.validators import (  # noqa: E402
    ca_bc_phn_valid,
    ca_ohip_valid,
    ca_ramq_valid,
    ca_sin_valid,
    luhn_check_digit,
    luhn_valid,
)

digits = st.text(alphabet="0123456789", min_size=2, max_size=14)


class TestLuhnAgreement:
    @given(value=digits)
    def test_luhn_valid_agrees_with_reference(self, value):
        assert luhn_valid(value) == luhn_ok(value)

    @given(base=st.text(alphabet="0123456789", min_size=1, max_size=12))
    def test_check_digit_agrees_with_reference(self, base):
        assert base + luhn_check_digit(base) == luhn_append(base)

    def test_canonical_vector(self):
        # ISO/IEC 7812 worked example.
        assert luhn_ok("79927398713") and luhn_valid("79927398713")
        assert not luhn_ok("79927398710") and not luhn_valid("79927398710")


class TestSinAgreement:
    @given(value=st.text(alphabet="0123456789", min_size=9, max_size=9))
    def test_random_nine_digits(self, value):
        assert ca_sin_valid(value) == sin_ok(value)

    def test_widely_cited_example_rejected_on_leading_zero(self):
        # 046 454 286 is the SIN example reproduced in many references: it
        # is Luhn-valid but starts with 0, which is not issued.
        assert luhn_ok("046454286")
        assert not sin_ok("046454286") and not ca_sin_valid("046454286")

    def test_business_number_prefix_rejected(self):
        value = luhn_append("81234567")
        assert not sin_ok(value) and not ca_sin_valid(value)


class TestOhipAgreement:
    @given(value=st.text(alphabet="0123456789", min_size=10, max_size=10))
    def test_random_ten_digits(self, value):
        assert ca_ohip_valid(value) == ohip_ok(value)

    @given(seed=st.integers(min_value=0, max_value=2**32 - 1))
    @settings(max_examples=50)
    def test_generated_with_version_codes(self, seed):
        value = raw_ca_ohip(random.Random(seed))
        for version in ("", "A", "KD"):
            assert ohip_ok(value, version) and ca_ohip_valid(value + version)
        assert not ca_ohip_valid(value + "kd")


class TestBcPhnAgreement:
    @given(value=st.text(alphabet="0123456789", min_size=10, max_size=10))
    def test_random_ten_digits(self, value):
        assert ca_bc_phn_valid(value) == bc_phn_ok(value)

    @given(seed=st.integers(min_value=0, max_value=2**32 - 1))
    @settings(max_examples=50)
    def test_generated_value_and_single_digit_corruption(self, seed):
        value = raw_ca_bc_phn(random.Random(seed))
        assert bc_phn_ok(value) and ca_bc_phn_valid(value)
        for pos in range(1, 10):
            corrupted = value[:pos] + str((int(value[pos]) + 1) % 10) + value[pos + 1 :]
            assert bc_phn_ok(corrupted) == ca_bc_phn_valid(corrupted)

    def test_thirteen_digit_transport_form_documented_gap(self):
        # Volume 4 transmits PHNs as 13 digits with leading zeros. The
        # reference accepts it; the package pattern does not (documented in
        # docs/identifiers/ca_bc_phn.md).
        value = raw_ca_bc_phn(random.Random(7))
        assert bc_phn_ok("000" + value)
        assert not ca_bc_phn_valid("000" + value)

    def test_some_bases_have_no_check_digit(self):
        # The routine yields 10 or 11 for some bases; those numbers cannot
        # be issued and no check digit validates.
        found_invalid_base = False
        for n in range(100000, 100500):
            base = "9" + f"{n:08d}"
            if bc_phn_check(base) is None:
                found_invalid_base = True
                assert not any(ca_bc_phn_valid(base + d) for d in "0123456789")
                break
        assert found_invalid_base


class TestRamqAgreement:
    @given(seed=st.integers(min_value=0, max_value=2**32 - 1))
    @settings(max_examples=50)
    def test_generated_values_pass_both(self, seed):
        value = raw_ca_ramq(random.Random(seed))
        assert ramq_ok(value) and ca_ramq_valid(value)

    @pytest.mark.parametrize(
        "value", ["BOUC65132301", "BOUC65013301", "BO1C65012301", "BOUC6501230"]
    )
    def test_structural_rejects_agree(self, value):
        assert not ramq_ok(value) and not ca_ramq_valid(value)

    def test_package_day_rule_is_looser_than_calendar(self):
        # Documented gap: the package accepts day 01-31 for every month;
        # the reference checks the calendar. Keep the difference visible.
        assert ca_ramq_valid("BOUC65023001")  # Feb 30
        assert not ramq_ok("BOUC65023001")


class TestGeneratorsUseReference:
    @given(seed=st.integers(min_value=0, max_value=2**32 - 1))
    @settings(max_examples=50)
    def test_generated_sin_passes_reference(self, seed):
        assert sin_ok(raw_ca_sin(random.Random(seed)))
