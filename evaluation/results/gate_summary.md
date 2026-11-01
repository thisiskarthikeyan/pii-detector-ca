# Threshold gate summary

System: Presidio + pack. Generated: 2026-10-29T05:16:15+00:00. Measured values are from the committed results files; bounds from evaluation/thresholds.json.

| Group | Check | Measured | Bound | Status |
|---|---|---|---|---|
| pack recall heldout | CA_SIN | 1.000 | >= 1.000 | OK |
| pack recall heldout | CA_OHIP | 1.000 | >= 1.000 | OK |
| pack recall heldout | CA_BC_PHN | 1.000 | >= 1.000 | OK |
| pack recall heldout | CA_AB_ULI | 1.000 | >= 1.000 | OK |
| pack recall heldout | CA_POSTAL_CODE | 1.000 | >= 1.000 | OK |
| pack recall heldout | CA_RAMQ | 1.000 | >= 0.900 | OK |
| pack recall heldout | CA_HEALTH_CARD | 0.810 | >= 0.700 | OK |
| pack recall heldout | ADDRESS | 0.714 | >= 0.650 | OK |
| leak recall heldout | PERSON | 0.964 | >= 0.900 | OK |
| leak recall heldout | DATE | 0.993 | >= 0.970 | OK |
| leak recall heldout | TOTAL | 0.982 | >= 0.950 | OK |
| precision heldout | pack | 1.000 | >= 0.990 | OK |
| precision heldout | pipeline | 0.660 | >= 0.600 | OK |
| over-redaction heldout | chars/note | 40.650 | <= 60.000 | OK |
| pack recall generated | CA_SIN | 1.000 | >= 1.000 | OK |
| pack recall generated | CA_OHIP | 1.000 | >= 1.000 | OK |
| pack recall generated | CA_BC_PHN | 1.000 | >= 1.000 | OK |
| pack recall generated | CA_AB_ULI | 1.000 | >= 1.000 | OK |
| pack recall generated | CA_POSTAL_CODE | 1.000 | >= 1.000 | OK |
| pack recall generated | CA_RAMQ | 0.950 | >= 0.900 | OK |
| pack recall generated | CA_HEALTH_CARD | 0.822 | >= 0.700 | OK |
| pack recall generated | ADDRESS | 0.857 | >= 0.650 | OK |
| leak recall generated | PERSON | 0.942 | >= 0.900 | OK |
| leak recall generated | DATE | 0.987 | >= 0.970 | OK |
| leak recall generated | TOTAL | 0.975 | >= 0.950 | OK |
| precision generated | pack | 1.000 | >= 0.990 | OK |
| precision generated | pipeline | 0.646 | >= 0.600 | OK |
| over-redaction generated | chars/note | 42.114 | <= 60.000 | OK |
| recognizer presence | CA_SIN | 290.000 | >= 50.000 | OK |
| recognizer presence | CA_OHIP | 192.000 | >= 50.000 | OK |
| recognizer presence | CA_RAMQ | 153.000 | >= 50.000 | OK |
| recognizer presence | CA_BC_PHN | 159.000 | >= 50.000 | OK |
| recognizer presence | CA_AB_ULI | 100.000 | >= 50.000 | OK |
| recognizer presence | CA_HEALTH_CARD | 665.000 | >= 50.000 | OK |
| recognizer presence | CA_POSTAL_CODE | 629.000 | >= 50.000 | OK |
| recognizer presence | CA_STREET_ADDRESS | 312.000 | >= 50.000 | OK |
| hard split pack recall | control | 1.000 | >= 1.000 | OK |
| hard split pack recall | no_context | 0.800 | >= 0.750 | OK |
| hard split pack recall | unusual_separator | 0.700 | >= 0.600 | OK |
| hard split pack recall | line_wrap | 0.000 | >= 0.000 | OK |
| hard split pack recall | ocr_confusable | 0.000 | >= 0.000 | OK |
| hard split pack recall | dictation | 0.000 | >= 0.000 | OK |
| address strict recall | one_line | 0.967 | >= 0.900 | OK |
| negatives FP rate | accession | 0.000 | <= 0.000 | OK |
| negatives FP rate | credit_card | 0.000 | <= 0.000 | OK |
| negatives FP rate | us_ssn | 0.000 | <= 0.000 | OK |
| negatives FP rate | phone_facility | 0.000 | <= 0.000 | OK |
| negatives FP rate | serial9 | 0.094 | <= 0.150 | OK |
| negatives FP rate | order10 | 0.083 | <= 0.150 | OK |
| negatives FP rate | mrn10 | 0.200 | <= 0.300 | OK |
| negatives FP rate | encounter10 | 0.100 | <= 0.200 | OK |
| negatives FP rate | phone_compact | 0.100 | <= 0.200 | OK |
| negatives FP rate | fax_compact | 0.133 | <= 0.200 | OK |
| negatives FP rate | trap_near | 0.683 | <= 0.800 | OK |
| negatives FP rate | trap_alberta | 1.433 | <= 1.600 | OK |
| negatives FP rate | trap_french | 1.133 | <= 1.300 | OK |
| negatives FP | unplanted | 0.000 | <= 0.000 | OK |

57 checks, 0 failure(s).
