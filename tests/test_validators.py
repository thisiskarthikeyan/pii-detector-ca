from presidio_recognizers_ca_in.validators import (
    ca_bc_phn_valid,
    ca_ohip_valid,
    ca_ramq_valid,
    ca_sin_valid,
    in_aadhaar_valid,
    in_mobile_valid,
    in_pan_valid,
    luhn_check_digit,
    luhn_valid,
    verhoeff_check_digit,
    verhoeff_valid,
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

    def test_verhoeff_known_valid(self):
        # Wikipedia worked example: check digit of 236 is 3
        assert verhoeff_valid("2363")

    def test_verhoeff_known_invalid(self):
        assert not verhoeff_valid("2364")

    def test_verhoeff_check_digit_roundtrip(self):
        for base in ["236", "23456789012", "99887766554"]:
            assert verhoeff_valid(base + verhoeff_check_digit(base))


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

    def test_ramq_valid_male_and_female_months(self):
        assert ca_ramq_valid("BOUC 6501 2301")  # male: month 01
        assert ca_ramq_valid("BOUC 6551 2301")  # female: month 51
        assert ca_ramq_valid("TREM65122801")

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


class TestIndianValidators:
    def test_aadhaar_valid(self):
        base = "23456789012"
        aadhaar = base + verhoeff_check_digit(base)
        assert in_aadhaar_valid(aadhaar)
        assert in_aadhaar_valid(f"{aadhaar[:4]} {aadhaar[4:8]} {aadhaar[8:]}")

    def test_aadhaar_rejects_bad_checksum(self):
        base = "23456789012"
        good = base + verhoeff_check_digit(base)
        bad = good[:11] + str((int(good[11]) + 1) % 10)
        assert not in_aadhaar_valid(bad)

    def test_aadhaar_rejects_leading_0_or_1(self):
        base = "13456789012"
        assert not in_aadhaar_valid(base + verhoeff_check_digit(base))

    def test_pan_valid(self):
        assert in_pan_valid("ABCPE1234F")  # P = person
        assert in_pan_valid("XYZCA9876B")  # C = company

    def test_pan_rejects_bad_holder_type(self):
        assert not in_pan_valid("ABCXE1234F")  # X is not a holder type

    def test_pan_rejects_bad_shape(self):
        assert not in_pan_valid("AB1PE1234F")

    def test_mobile_valid(self):
        assert in_mobile_valid("+91 98765 43210")
        assert in_mobile_valid("9876543210")
        assert in_mobile_valid("09876543210")

    def test_mobile_rejects_bad_leading_digit(self):
        assert not in_mobile_valid("5876543210")
