from pii_detector_ca.validators import (
    ca_bc_phn_valid,
    ca_ohip_valid,
    ca_ramq_valid,
    ca_sin_valid,
    luhn_check_digit,
    luhn_valid,
)


class TestChecksumPrimitives:
    def test_luhn_known_valid(self):
        # Canonical Luhn test number
        assert luhn_valid("79927398713")

    def test_luhn_known_invalid(self):
        assert not luhn_valid("79927398710")

    def test_luhn_check_digit_roundtrip(self):
        for base in ["7992739871", "12345678", "998765432"]:
            assert luhn_valid(base + luhn_check_digit(base))


class TestCanadianValidators:
    def test_sin_valid(self):
        base = "12345678"
        sin = base + luhn_check_digit(base)
        assert ca_sin_valid(sin)
        assert ca_sin_valid(f"{sin[:3]}-{sin[3:6]}-{sin[6:]}")
        assert ca_sin_valid(f"{sin[:3]} {sin[3:6]} {sin[6:]}")

    def test_sin_rejects_bad_checksum(self):
        assert not ca_sin_valid("123456789")

    def test_sin_rejects_unissued_leading_digit(self):
        # Leading 0 and 8 are not issued
        base0, base8 = "04645428", "81234567"
        assert not ca_sin_valid(base0 + luhn_check_digit(base0))
        assert not ca_sin_valid(base8 + luhn_check_digit(base8))

    def test_ohip_valid_with_version_code(self):
        base = "123456789"
        num = base + luhn_check_digit(base)
        assert ca_ohip_valid(num)
        assert ca_ohip_valid(f"{num[:4]}-{num[4:7]}-{num[7:]}-AB")

    def test_ohip_rejects_bad_checksum(self):
        assert not ca_ohip_valid("1234567890")

    def test_ohip_rejects_leading_zero(self):
        # MOH HCV schema: health number is [1-9]\d{9}
        base = "023456789"
        assert not ca_ohip_valid(base + luhn_check_digit(base))

    def test_ohip_rejects_lowercase_version_code(self):
        # Version codes are uppercase on every card issue; lowercase trailing
        # letters are English words, not part of the identifier.
        base = "123456789"
        num = base + luhn_check_digit(base)
        assert not ca_ohip_valid(f"{num} on")

    def test_ramq_valid_male_and_female_months(self):
        assert ca_ramq_valid("BOUC 6501 2301")  # male: month 01
        assert ca_ramq_valid("BOUC 6551 2301")  # female: month 51
        assert ca_ramq_valid("TREM65122801")
        assert ca_ramq_valid("TREM 0501 2301")  # born 2005

    def test_ramq_rejects_impossible_month_or_day(self):
        assert not ca_ramq_valid("BOUC 6513 2301")  # month 13
        assert not ca_ramq_valid("BOUC 6501 3301")  # day 33
        assert not ca_ramq_valid("BO1C 6501 2301")  # digit in name part

    def test_bc_phn_roundtrip(self):
        # Some digit bases have no valid check digit (checksum 10/11 is never
        # issued), so search across bases until one validates.
        found = None
        for mid in range(100):
            base = f"9234567{mid:02d}"
            for last in "0123456789":
                if ca_bc_phn_valid(base + last):
                    found = base + last
                    break
            if found:
                break
        assert found is not None
        assert not ca_bc_phn_valid(found[:9] + str((int(found[9]) + 1) % 10))

    def test_bc_phn_must_start_with_9(self):
        assert not ca_bc_phn_valid("1123456789")
