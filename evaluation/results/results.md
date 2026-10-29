# Evaluation results

Generated: 2026-10-29T05:16:15+00:00 | Python 3.13.17 | presidio-analyzer 2.2.363 | spacy 3.8.13 | en_core_web_sm 3.8.0

The `heldout` split is the first 100 notes of the fixed-seed generator stream; it is not human-reviewed. All data is synthetic.

### Stock Presidio — split=heldout

| Entity | Gold | Leak recall | Strict recall | Pack recall | Typed exact |
|---|---|---|---|---|---|
| ADDRESS | 42 | 0.952 | 0.000 | 0.000 | 0.000 |
| CA_AB_ULI | 9 | 0.444 | 0.444 | 0.000 | 0.000 |
| CA_BC_PHN | 21 | 1.000 | 1.000 | 0.000 | 0.000 |
| CA_HEALTH_CARD | 42 | 0.595 | 0.524 | 0.000 | 0.000 |
| CA_OHIP | 23 | 0.783 | 0.304 | 0.000 | 0.000 |
| CA_POSTAL_CODE | 34 | 0.206 | 0.059 | 0.000 | 0.000 |
| CA_RAMQ | 18 | 0.500 | 0.167 | 0.000 | 0.000 |
| CA_SIN | 30 | 0.133 | 0.133 | 0.000 | 0.000 |
| DATE | 143 | 0.993 | 0.930 | 0.993 | 0.909 |
| PERSON | 139 | 0.964 | 0.935 | 0.928 | 0.662 |
| **TOTAL** | 501 | 0.806 | 0.651 | 0.541 | 0.443 |

Pack recall = gold span overlapped by the recognizer that owns the entity type (CA_STREET_ADDRESS for ADDRESS, DATE_TIME for DATE); leak recall counts overlap by any recognizer.

Pipeline precision (all predictions, deduplicated): 0.613 (TP 401, FP 253, duplicates on claimed gold 84)
Pack precision (CA_* predictions only): 0.000 (TP 0, FP 0, duplicates 0)
Over-redaction: 40.6 chars/note masked outside gold spans
Bootstrap 95% CI (1000 note-resamples): leak recall [0.771, 0.843], strict recall [0.618, 0.684], pack recall [0.512, 0.573], pipeline precision [0.585, 0.639], pack precision n/a

| Predicted type | TP (overlaps gold) | FP (no gold overlap) |
|---|---|---|
| DATE_TIME | 219 | 28 |
| LOCATION | 35 | 3 |
| MEDICAL_LICENSE | 1 | 0 |
| NRP | 0 | 16 |
| ORGANIZATION | 28 | 178 |
| PERSON | 148 | 28 |
| PHONE_NUMBER | 51 | 0 |
| US_BANK_NUMBER | 2 | 0 |
| US_PASSPORT | 1 | 0 |

### Presidio + CA builtins — split=heldout

| Entity | Gold | Leak recall | Strict recall | Pack recall | Typed exact |
|---|---|---|---|---|---|
| ADDRESS | 42 | 0.952 | 0.000 | 0.000 | 0.000 |
| CA_AB_ULI | 9 | 0.444 | 0.444 | 0.000 | 0.000 |
| CA_BC_PHN | 21 | 1.000 | 1.000 | 0.000 | 0.000 |
| CA_HEALTH_CARD | 42 | 0.595 | 0.524 | 0.000 | 0.000 |
| CA_OHIP | 23 | 0.783 | 0.304 | 0.000 | 0.000 |
| CA_POSTAL_CODE | 34 | 0.206 | 0.059 | 0.000 | 0.000 |
| CA_RAMQ | 18 | 0.500 | 0.167 | 0.000 | 0.000 |
| CA_SIN | 30 | 0.767 | 0.767 | 0.700 | 0.700 |
| DATE | 143 | 0.993 | 0.930 | 0.993 | 0.909 |
| PERSON | 139 | 0.964 | 0.935 | 0.928 | 0.662 |
| **TOTAL** | 501 | 0.844 | 0.689 | 0.583 | 0.485 |

Pack recall = gold span overlapped by the recognizer that owns the entity type (CA_STREET_ADDRESS for ADDRESS, DATE_TIME for DATE); leak recall counts overlap by any recognizer.

Pipeline precision (all predictions, deduplicated): 0.624 (TP 420, FP 253, duplicates on claimed gold 86)
Pack precision (CA_* predictions only): 1.000 (TP 21, FP 0, duplicates 0)
Over-redaction: 40.6 chars/note masked outside gold spans
Bootstrap 95% CI (1000 note-resamples): leak recall [0.811, 0.875], strict recall [0.658, 0.719], pack recall [0.560, 0.607], pipeline precision [0.596, 0.650], pack precision [1.000, 1.000]

| Predicted type | TP (overlaps gold) | FP (no gold overlap) |
|---|---|---|
| CA_SIN | 21 | 0 |
| DATE_TIME | 219 | 28 |
| LOCATION | 35 | 3 |
| MEDICAL_LICENSE | 1 | 0 |
| NRP | 0 | 16 |
| ORGANIZATION | 28 | 178 |
| PERSON | 148 | 28 |
| PHONE_NUMBER | 51 | 0 |
| US_BANK_NUMBER | 2 | 0 |
| US_PASSPORT | 1 | 0 |

### Presidio + pack — split=heldout

| Entity | Gold | Leak recall | Strict recall | Pack recall | Typed exact |
|---|---|---|---|---|---|
| ADDRESS | 42 | 0.976 | 0.667 | 0.714 | 0.667 |
| CA_AB_ULI | 9 | 1.000 | 1.000 | 1.000 | 1.000 |
| CA_BC_PHN | 21 | 1.000 | 1.000 | 1.000 | 1.000 |
| CA_HEALTH_CARD | 42 | 0.952 | 0.929 | 0.810 | 0.738 |
| CA_OHIP | 23 | 1.000 | 0.826 | 1.000 | 0.826 |
| CA_POSTAL_CODE | 34 | 1.000 | 1.000 | 1.000 | 1.000 |
| CA_RAMQ | 18 | 1.000 | 1.000 | 1.000 | 1.000 |
| CA_SIN | 30 | 1.000 | 1.000 | 1.000 | 1.000 |
| DATE | 143 | 0.993 | 0.930 | 0.993 | 0.909 |
| PERSON | 139 | 0.964 | 0.935 | 0.928 | 0.662 |
| **TOTAL** | 501 | 0.982 | 0.920 | 0.938 | 0.822 |

Pack recall = gold span overlapped by the recognizer that owns the entity type (CA_STREET_ADDRESS for ADDRESS, DATE_TIME for DATE); leak recall counts overlap by any recognizer.

Pipeline precision (all predictions, deduplicated): 0.660 (TP 491, FP 253, duplicates on claimed gold 279)
Pack precision (CA_* predictions only): 1.000 (TP 207, FP 0, duplicates 78)
Over-redaction: 40.6 chars/note masked outside gold spans
Bootstrap 95% CI (1000 note-resamples): leak recall [0.970, 0.992], strict recall [0.896, 0.943], pack recall [0.920, 0.957], pipeline precision [0.638, 0.683], pack precision [1.000, 1.000]

| Predicted type | TP (overlaps gold) | FP (no gold overlap) |
|---|---|---|
| CA_AB_ULI | 9 | 0 |
| CA_BC_PHN | 21 | 0 |
| CA_HEALTH_CARD | 81 | 0 |
| CA_OHIP | 23 | 0 |
| CA_POSTAL_CODE | 72 | 0 |
| CA_RAMQ | 18 | 0 |
| CA_SIN | 31 | 0 |
| CA_STREET_ADDRESS | 30 | 0 |
| DATE_TIME | 219 | 28 |
| LOCATION | 35 | 3 |
| MEDICAL_LICENSE | 1 | 0 |
| NRP | 0 | 16 |
| ORGANIZATION | 28 | 178 |
| PERSON | 148 | 28 |
| PHONE_NUMBER | 51 | 0 |
| US_BANK_NUMBER | 2 | 0 |
| US_PASSPORT | 1 | 0 |

Per surface form (pack system only): gold entities tagged with the rendering the generator used.

| Entity | Form | Gold | Leak recall | Strict recall | Pack recall |
|---|---|---|---|---|---|
| ADDRESS | apt_suite | 1 | 1.000 | 0.000 | 1.000 |
| ADDRESS | no_comma_province | 3 | 1.000 | 0.000 | 0.000 |
| ADDRESS | no_postal | 4 | 0.750 | 0.000 | 0.000 |
| ADDRESS | one_line | 28 | 1.000 | 0.964 | 1.000 |
| ADDRESS | postal_own_line | 1 | 1.000 | 1.000 | 1.000 |
| ADDRESS | province_spelled | 3 | 1.000 | 0.000 | 0.000 |
| ADDRESS | two_line | 2 | 1.000 | 0.000 | 0.000 |
| CA_AB_ULI | compact | 2 | 1.000 | 1.000 | 1.000 |
| CA_AB_ULI | dash | 3 | 1.000 | 1.000 | 1.000 |
| CA_AB_ULI | dot | 1 | 1.000 | 1.000 | 1.000 |
| CA_AB_ULI | space | 3 | 1.000 | 1.000 | 1.000 |
| CA_BC_PHN | compact | 2 | 1.000 | 1.000 | 1.000 |
| CA_BC_PHN | compact+repeat | 1 | 1.000 | 1.000 | 1.000 |
| CA_BC_PHN | dash | 4 | 1.000 | 1.000 | 1.000 |
| CA_BC_PHN | dot | 1 | 1.000 | 1.000 | 1.000 |
| CA_BC_PHN | slash | 3 | 1.000 | 1.000 | 1.000 |
| CA_BC_PHN | slash+repeat | 2 | 1.000 | 1.000 | 1.000 |
| CA_BC_PHN | space | 7 | 1.000 | 1.000 | 1.000 |
| CA_BC_PHN | space+repeat | 1 | 1.000 | 1.000 | 1.000 |
| CA_HEALTH_CARD | MB:mixed | 1 | 1.000 | 1.000 | 1.000 |
| CA_HEALTH_CARD | MB:space | 2 | 0.500 | 0.500 | 0.500 |
| CA_HEALTH_CARD | NB:dash | 3 | 1.000 | 1.000 | 1.000 |
| CA_HEALTH_CARD | NB:slash | 1 | 1.000 | 1.000 | 1.000 |
| CA_HEALTH_CARD | NB:space | 2 | 1.000 | 1.000 | 1.000 |
| CA_HEALTH_CARD | NL:compact | 1 | 1.000 | 1.000 | 1.000 |
| CA_HEALTH_CARD | NL:dash | 2 | 1.000 | 1.000 | 1.000 |
| CA_HEALTH_CARD | NL:space | 1 | 1.000 | 1.000 | 1.000 |
| CA_HEALTH_CARD | NS:dot | 2 | 1.000 | 1.000 | 1.000 |
| CA_HEALTH_CARD | NS:mixed | 1 | 1.000 | 1.000 | 1.000 |
| CA_HEALTH_CARD | NS:space | 5 | 1.000 | 1.000 | 1.000 |
| CA_HEALTH_CARD | PE:compact | 2 | 1.000 | 1.000 | 0.500 |
| CA_HEALTH_CARD | PE:dash | 1 | 1.000 | 1.000 | 1.000 |
| CA_HEALTH_CARD | PE:dot | 1 | 1.000 | 1.000 | 0.000 |
| CA_HEALTH_CARD | PE:space | 1 | 1.000 | 1.000 | 1.000 |
| CA_HEALTH_CARD | SK:space | 1 | 1.000 | 1.000 | 1.000 |
| CA_HEALTH_CARD | SK:space+repeat | 1 | 1.000 | 1.000 | 1.000 |
| CA_HEALTH_CARD | uli:compact | 6 | 0.833 | 0.833 | 0.667 |
| CA_HEALTH_CARD | uli:dash | 3 | 1.000 | 1.000 | 1.000 |
| CA_HEALTH_CARD | uli:space | 5 | 1.000 | 0.800 | 0.400 |
| CA_OHIP | compact | 1 | 1.000 | 1.000 | 1.000 |
| CA_OHIP | compact+version_sep | 3 | 1.000 | 0.000 | 1.000 |
| CA_OHIP | dash | 1 | 1.000 | 1.000 | 1.000 |
| CA_OHIP | dash+repeat | 1 | 1.000 | 1.000 | 1.000 |
| CA_OHIP | dash+version_glued | 1 | 1.000 | 1.000 | 1.000 |
| CA_OHIP | dash+version_sep | 2 | 1.000 | 1.000 | 1.000 |
| CA_OHIP | dot | 1 | 1.000 | 1.000 | 1.000 |
| CA_OHIP | dot+version_sep | 2 | 1.000 | 1.000 | 1.000 |
| CA_OHIP | dot+version_sep+repeat | 1 | 1.000 | 1.000 | 1.000 |
| CA_OHIP | mixed | 1 | 1.000 | 1.000 | 1.000 |
| CA_OHIP | mixed+repeat | 1 | 1.000 | 1.000 | 1.000 |
| CA_OHIP | mixed+version_sep | 1 | 1.000 | 1.000 | 1.000 |
| CA_OHIP | space | 2 | 1.000 | 1.000 | 1.000 |
| CA_OHIP | space+repeat | 1 | 1.000 | 1.000 | 1.000 |
| CA_OHIP | space+version_lower | 1 | 1.000 | 0.000 | 1.000 |
| CA_OHIP | space+version_sep | 3 | 1.000 | 1.000 | 1.000 |
| CA_POSTAL_CODE | compact | 1 | 1.000 | 1.000 | 1.000 |
| CA_POSTAL_CODE | lowercase | 5 | 1.000 | 1.000 | 1.000 |
| CA_POSTAL_CODE | space | 28 | 1.000 | 1.000 | 1.000 |
| CA_RAMQ | compact | 7 | 1.000 | 1.000 | 1.000 |
| CA_RAMQ | compact+repeat | 2 | 1.000 | 1.000 | 1.000 |
| CA_RAMQ | dash | 2 | 1.000 | 1.000 | 1.000 |
| CA_RAMQ | space | 5 | 1.000 | 1.000 | 1.000 |
| CA_RAMQ | space+repeat | 2 | 1.000 | 1.000 | 1.000 |
| CA_SIN | compact | 5 | 1.000 | 1.000 | 1.000 |
| CA_SIN | dash | 7 | 1.000 | 1.000 | 1.000 |
| CA_SIN | dot | 4 | 1.000 | 1.000 | 1.000 |
| CA_SIN | mixed | 2 | 1.000 | 1.000 | 1.000 |
| CA_SIN | space | 12 | 1.000 | 1.000 | 1.000 |

### Stock Presidio — split=generated

| Entity | Gold | Leak recall | Strict recall | Pack recall | Typed exact |
|---|---|---|---|---|---|
| ADDRESS | 364 | 0.970 | 0.000 | 0.000 | 0.000 |
| CA_AB_ULI | 99 | 0.667 | 0.636 | 0.000 | 0.000 |
| CA_BC_PHN | 158 | 1.000 | 1.000 | 0.000 | 0.000 |
| CA_HEALTH_CARD | 409 | 0.597 | 0.557 | 0.000 | 0.000 |
| CA_OHIP | 169 | 0.846 | 0.379 | 0.000 | 0.000 |
| CA_POSTAL_CODE | 271 | 0.151 | 0.085 | 0.000 | 0.000 |
| CA_RAMQ | 161 | 0.522 | 0.112 | 0.000 | 0.000 |
| CA_SIN | 275 | 0.149 | 0.142 | 0.000 | 0.000 |
| DATE | 1262 | 0.987 | 0.918 | 0.986 | 0.900 |
| PERSON | 1263 | 0.942 | 0.924 | 0.899 | 0.683 |
| **TOTAL** | 4431 | 0.805 | 0.659 | 0.537 | 0.451 |

Pack recall = gold span overlapped by the recognizer that owns the entity type (CA_STREET_ADDRESS for ADDRESS, DATE_TIME for DATE); leak recall counts overlap by any recognizer.

Pipeline precision (all predictions, deduplicated): 0.601 (TP 3558, FP 2360, duplicates on claimed gold 700)
Pack precision (CA_* predictions only): 0.000 (TP 0, FP 0, duplicates 0)
Over-redaction: 42.1 chars/note masked outside gold spans
Bootstrap 95% CI (1000 note-resamples): leak recall [0.794, 0.816], strict recall [0.646, 0.671], pack recall [0.528, 0.546], pipeline precision [0.592, 0.611], pack precision n/a

| Predicted type | TP (overlaps gold) | FP (no gold overlap) |
|---|---|---|
| DATE_TIME | 1933 | 225 |
| LOCATION | 277 | 19 |
| MAC_ADDRESS | 8 | 0 |
| MEDICAL_LICENSE | 2 | 0 |
| NRP | 5 | 129 |
| ORGANIZATION | 293 | 1712 |
| PERSON | 1326 | 275 |
| PHONE_NUMBER | 391 | 0 |
| UK_NHS | 9 | 0 |
| US_BANK_NUMBER | 11 | 0 |
| US_ITIN | 1 | 0 |
| US_PASSPORT | 2 | 0 |

### Presidio + CA builtins — split=generated

| Entity | Gold | Leak recall | Strict recall | Pack recall | Typed exact |
|---|---|---|---|---|---|
| ADDRESS | 364 | 0.970 | 0.000 | 0.000 | 0.000 |
| CA_AB_ULI | 99 | 0.667 | 0.636 | 0.000 | 0.000 |
| CA_BC_PHN | 158 | 1.000 | 1.000 | 0.000 | 0.000 |
| CA_HEALTH_CARD | 409 | 0.609 | 0.570 | 0.000 | 0.000 |
| CA_OHIP | 169 | 0.846 | 0.379 | 0.000 | 0.000 |
| CA_POSTAL_CODE | 271 | 0.151 | 0.085 | 0.000 | 0.000 |
| CA_RAMQ | 161 | 0.522 | 0.112 | 0.000 | 0.000 |
| CA_SIN | 275 | 0.745 | 0.742 | 0.709 | 0.709 |
| DATE | 1262 | 0.987 | 0.918 | 0.986 | 0.900 |
| PERSON | 1263 | 0.942 | 0.924 | 0.899 | 0.683 |
| **TOTAL** | 4431 | 0.843 | 0.697 | 0.581 | 0.495 |

Pack recall = gold span overlapped by the recognizer that owns the entity type (CA_STREET_ADDRESS for ADDRESS, DATE_TIME for DATE); leak recall counts overlap by any recognizer.

Pipeline precision (all predictions, deduplicated): 0.612 (TP 3727, FP 2360, duplicates on claimed gold 731)
Pack precision (CA_* predictions only): 1.000 (TP 200, FP 0, duplicates 0)
Over-redaction: 42.1 chars/note masked outside gold spans
Bootstrap 95% CI (1000 note-resamples): leak recall [0.833, 0.853], strict recall [0.685, 0.709], pack recall [0.573, 0.589], pipeline precision [0.603, 0.621], pack precision [1.000, 1.000]

| Predicted type | TP (overlaps gold) | FP (no gold overlap) |
|---|---|---|
| CA_SIN | 200 | 0 |
| DATE_TIME | 1933 | 225 |
| LOCATION | 277 | 19 |
| MAC_ADDRESS | 8 | 0 |
| MEDICAL_LICENSE | 2 | 0 |
| NRP | 5 | 129 |
| ORGANIZATION | 293 | 1712 |
| PERSON | 1326 | 275 |
| PHONE_NUMBER | 391 | 0 |
| UK_NHS | 9 | 0 |
| US_BANK_NUMBER | 11 | 0 |
| US_ITIN | 1 | 0 |
| US_PASSPORT | 2 | 0 |

### Presidio + pack — split=generated

| Entity | Gold | Leak recall | Strict recall | Pack recall | Typed exact |
|---|---|---|---|---|---|
| ADDRESS | 364 | 1.000 | 0.808 | 0.857 | 0.802 |
| CA_AB_ULI | 99 | 1.000 | 1.000 | 1.000 | 1.000 |
| CA_BC_PHN | 158 | 1.000 | 1.000 | 1.000 | 1.000 |
| CA_HEALTH_CARD | 409 | 0.951 | 0.939 | 0.822 | 0.748 |
| CA_OHIP | 169 | 1.000 | 0.864 | 1.000 | 0.852 |
| CA_POSTAL_CODE | 271 | 1.000 | 1.000 | 1.000 | 1.000 |
| CA_RAMQ | 161 | 1.000 | 0.957 | 0.950 | 0.950 |
| CA_SIN | 275 | 1.000 | 1.000 | 1.000 | 1.000 |
| DATE | 1262 | 0.987 | 0.918 | 0.986 | 0.900 |
| PERSON | 1263 | 0.942 | 0.924 | 0.899 | 0.683 |
| **TOTAL** | 4431 | 0.975 | 0.927 | 0.937 | 0.834 |

Pack recall = gold span overlapped by the recognizer that owns the entity type (CA_STREET_ADDRESS for ADDRESS, DATE_TIME for DATE); leak recall counts overlap by any recognizer.

Pipeline precision (all predictions, deduplicated): 0.646 (TP 4316, FP 2360, duplicates on claimed gold 2442)
Pack precision (CA_* predictions only): 1.000 (TP 1828, FP 0, duplicates 672)
Over-redaction: 42.1 chars/note masked outside gold spans
Bootstrap 95% CI (1000 note-resamples): leak recall [0.971, 0.980], strict recall [0.919, 0.934], pack recall [0.930, 0.944], pipeline precision [0.639, 0.654], pack precision [1.000, 1.000]

| Predicted type | TP (overlaps gold) | FP (no gold overlap) |
|---|---|---|
| CA_AB_ULI | 100 | 0 |
| CA_BC_PHN | 159 | 0 |
| CA_HEALTH_CARD | 665 | 0 |
| CA_OHIP | 192 | 0 |
| CA_POSTAL_CODE | 629 | 0 |
| CA_RAMQ | 153 | 0 |
| CA_SIN | 290 | 0 |
| CA_STREET_ADDRESS | 312 | 0 |
| DATE_TIME | 1933 | 225 |
| LOCATION | 277 | 19 |
| MAC_ADDRESS | 8 | 0 |
| MEDICAL_LICENSE | 2 | 0 |
| NRP | 5 | 129 |
| ORGANIZATION | 293 | 1712 |
| PERSON | 1326 | 275 |
| PHONE_NUMBER | 391 | 0 |
| UK_NHS | 9 | 0 |
| US_BANK_NUMBER | 11 | 0 |
| US_ITIN | 1 | 0 |
| US_PASSPORT | 2 | 0 |

Per surface form (pack system only): gold entities tagged with the rendering the generator used.

| Entity | Form | Gold | Leak recall | Strict recall | Pack recall |
|---|---|---|---|---|---|
| ADDRESS | apt_suite | 9 | 1.000 | 0.111 | 0.444 |
| ADDRESS | no_comma_province | 6 | 1.000 | 0.000 | 0.000 |
| ADDRESS | no_postal | 6 | 1.000 | 0.000 | 0.000 |
| ADDRESS | one_line | 297 | 1.000 | 0.939 | 0.990 |
| ADDRESS | postal_own_line | 14 | 1.000 | 1.000 | 1.000 |
| ADDRESS | province_spelled | 17 | 1.000 | 0.000 | 0.000 |
| ADDRESS | rural_route | 8 | 1.000 | 0.000 | 0.000 |
| ADDRESS | two_line | 7 | 1.000 | 0.000 | 0.000 |
| CA_AB_ULI | compact | 25 | 1.000 | 1.000 | 1.000 |
| CA_AB_ULI | dash | 24 | 1.000 | 1.000 | 1.000 |
| CA_AB_ULI | dot | 13 | 1.000 | 1.000 | 1.000 |
| CA_AB_ULI | mixed | 4 | 1.000 | 1.000 | 1.000 |
| CA_AB_ULI | slash | 5 | 1.000 | 1.000 | 1.000 |
| CA_AB_ULI | space | 28 | 1.000 | 1.000 | 1.000 |
| CA_BC_PHN | compact | 27 | 1.000 | 1.000 | 1.000 |
| CA_BC_PHN | compact+repeat | 9 | 1.000 | 1.000 | 1.000 |
| CA_BC_PHN | dash | 39 | 1.000 | 1.000 | 1.000 |
| CA_BC_PHN | dash+repeat | 1 | 1.000 | 1.000 | 1.000 |
| CA_BC_PHN | dot | 19 | 1.000 | 1.000 | 1.000 |
| CA_BC_PHN | dot+repeat | 5 | 1.000 | 1.000 | 1.000 |
| CA_BC_PHN | mixed | 7 | 1.000 | 1.000 | 1.000 |
| CA_BC_PHN | mixed+repeat | 2 | 1.000 | 1.000 | 1.000 |
| CA_BC_PHN | slash | 5 | 1.000 | 1.000 | 1.000 |
| CA_BC_PHN | slash+repeat | 1 | 1.000 | 1.000 | 1.000 |
| CA_BC_PHN | space | 38 | 1.000 | 1.000 | 1.000 |
| CA_BC_PHN | space+repeat | 5 | 1.000 | 1.000 | 1.000 |
| CA_HEALTH_CARD | MB:compact | 5 | 1.000 | 1.000 | 0.800 |
| CA_HEALTH_CARD | MB:compact+repeat | 1 | 1.000 | 1.000 | 1.000 |
| CA_HEALTH_CARD | MB:dash | 20 | 0.700 | 0.700 | 0.700 |
| CA_HEALTH_CARD | MB:dash+repeat | 1 | 1.000 | 1.000 | 1.000 |
| CA_HEALTH_CARD | MB:dot | 4 | 1.000 | 1.000 | 0.750 |
| CA_HEALTH_CARD | MB:mixed | 2 | 1.000 | 1.000 | 1.000 |
| CA_HEALTH_CARD | MB:mixed+repeat | 1 | 1.000 | 1.000 | 1.000 |
| CA_HEALTH_CARD | MB:slash | 1 | 1.000 | 1.000 | 1.000 |
| CA_HEALTH_CARD | MB:space | 12 | 0.917 | 0.917 | 0.917 |
| CA_HEALTH_CARD | NB:compact | 5 | 1.000 | 1.000 | 1.000 |
| CA_HEALTH_CARD | NB:dash | 6 | 1.000 | 1.000 | 1.000 |
| CA_HEALTH_CARD | NB:dot | 5 | 1.000 | 1.000 | 1.000 |
| CA_HEALTH_CARD | NB:dot+repeat | 1 | 1.000 | 1.000 | 1.000 |
| CA_HEALTH_CARD | NB:mixed | 7 | 1.000 | 1.000 | 1.000 |
| CA_HEALTH_CARD | NB:mixed+repeat | 2 | 1.000 | 1.000 | 1.000 |
| CA_HEALTH_CARD | NB:slash | 1 | 1.000 | 1.000 | 1.000 |
| CA_HEALTH_CARD | NB:space | 11 | 0.727 | 0.727 | 0.636 |
| CA_HEALTH_CARD | NB:space+repeat | 1 | 1.000 | 1.000 | 1.000 |
| CA_HEALTH_CARD | NL:compact | 4 | 1.000 | 1.000 | 0.750 |
| CA_HEALTH_CARD | NL:dash | 8 | 1.000 | 1.000 | 1.000 |
| CA_HEALTH_CARD | NL:dot | 8 | 1.000 | 1.000 | 0.875 |
| CA_HEALTH_CARD | NL:mixed | 2 | 1.000 | 0.500 | 1.000 |
| CA_HEALTH_CARD | NL:mixed+repeat | 1 | 1.000 | 1.000 | 1.000 |
| CA_HEALTH_CARD | NL:slash | 6 | 0.833 | 0.333 | 0.667 |
| CA_HEALTH_CARD | NL:space | 8 | 1.000 | 1.000 | 0.875 |
| CA_HEALTH_CARD | NL:space+repeat | 1 | 1.000 | 1.000 | 1.000 |
| CA_HEALTH_CARD | NS:compact | 6 | 1.000 | 1.000 | 1.000 |
| CA_HEALTH_CARD | NS:compact+repeat | 3 | 1.000 | 1.000 | 1.000 |
| CA_HEALTH_CARD | NS:dash | 14 | 0.929 | 0.929 | 0.714 |
| CA_HEALTH_CARD | NS:dash+repeat | 1 | 1.000 | 1.000 | 1.000 |
| CA_HEALTH_CARD | NS:dot | 3 | 1.000 | 1.000 | 1.000 |
| CA_HEALTH_CARD | NS:mixed | 4 | 1.000 | 1.000 | 0.750 |
| CA_HEALTH_CARD | NS:mixed+repeat | 1 | 1.000 | 1.000 | 1.000 |
| CA_HEALTH_CARD | NS:slash | 1 | 1.000 | 1.000 | 1.000 |
| CA_HEALTH_CARD | NS:space | 11 | 1.000 | 1.000 | 0.818 |
| CA_HEALTH_CARD | PE:compact | 4 | 1.000 | 1.000 | 0.750 |
| CA_HEALTH_CARD | PE:dash | 14 | 1.000 | 1.000 | 0.786 |
| CA_HEALTH_CARD | PE:dash+repeat | 1 | 1.000 | 1.000 | 1.000 |
| CA_HEALTH_CARD | PE:dot | 4 | 1.000 | 1.000 | 1.000 |
| CA_HEALTH_CARD | PE:dot+repeat | 1 | 1.000 | 1.000 | 1.000 |
| CA_HEALTH_CARD | PE:mixed | 3 | 1.000 | 1.000 | 1.000 |
| CA_HEALTH_CARD | PE:slash | 3 | 1.000 | 1.000 | 1.000 |
| CA_HEALTH_CARD | PE:slash+repeat | 1 | 1.000 | 1.000 | 1.000 |
| CA_HEALTH_CARD | PE:space | 10 | 1.000 | 1.000 | 0.800 |
| CA_HEALTH_CARD | PE:space+repeat | 1 | 1.000 | 1.000 | 1.000 |
| CA_HEALTH_CARD | SK:compact | 8 | 1.000 | 1.000 | 0.750 |
| CA_HEALTH_CARD | SK:dash | 10 | 0.800 | 0.800 | 0.800 |
| CA_HEALTH_CARD | SK:dot | 3 | 1.000 | 1.000 | 1.000 |
| CA_HEALTH_CARD | SK:space | 8 | 1.000 | 1.000 | 1.000 |
| CA_HEALTH_CARD | SK:space+repeat | 2 | 1.000 | 1.000 | 1.000 |
| CA_HEALTH_CARD | uli:compact | 25 | 1.000 | 1.000 | 0.840 |
| CA_HEALTH_CARD | uli:compact+repeat | 5 | 1.000 | 1.000 | 1.000 |
| CA_HEALTH_CARD | uli:dash | 38 | 1.000 | 1.000 | 0.737 |
| CA_HEALTH_CARD | uli:dash+repeat | 6 | 1.000 | 1.000 | 1.000 |
| CA_HEALTH_CARD | uli:dot | 14 | 0.643 | 0.643 | 0.643 |
| CA_HEALTH_CARD | uli:mixed | 11 | 1.000 | 1.000 | 0.727 |
| CA_HEALTH_CARD | uli:slash | 9 | 1.000 | 1.000 | 1.000 |
| CA_HEALTH_CARD | uli:slash+repeat | 1 | 1.000 | 1.000 | 1.000 |
| CA_HEALTH_CARD | uli:space | 51 | 0.980 | 0.961 | 0.686 |
| CA_HEALTH_CARD | uli:space+repeat | 8 | 1.000 | 1.000 | 1.000 |
| CA_OHIP | compact | 16 | 1.000 | 1.000 | 1.000 |
| CA_OHIP | compact+repeat | 3 | 1.000 | 1.000 | 1.000 |
| CA_OHIP | compact+version_glued | 6 | 1.000 | 1.000 | 1.000 |
| CA_OHIP | compact+version_lower | 3 | 1.000 | 0.000 | 1.000 |
| CA_OHIP | compact+version_lower+repeat | 1 | 1.000 | 0.000 | 1.000 |
| CA_OHIP | compact+version_sep | 12 | 1.000 | 0.083 | 1.000 |
| CA_OHIP | compact+version_sep+repeat | 2 | 1.000 | 0.000 | 1.000 |
| CA_OHIP | dash | 12 | 1.000 | 1.000 | 1.000 |
| CA_OHIP | dash+repeat | 1 | 1.000 | 1.000 | 1.000 |
| CA_OHIP | dash+version_glued | 6 | 1.000 | 1.000 | 1.000 |
| CA_OHIP | dash+version_lower | 4 | 1.000 | 0.250 | 1.000 |
| CA_OHIP | dash+version_sep | 24 | 1.000 | 1.000 | 1.000 |
| CA_OHIP | dash+version_sep+repeat | 4 | 1.000 | 1.000 | 1.000 |
| CA_OHIP | dot | 7 | 1.000 | 1.000 | 1.000 |
| CA_OHIP | dot+repeat | 1 | 1.000 | 1.000 | 1.000 |
| CA_OHIP | dot+version_glued | 1 | 1.000 | 1.000 | 1.000 |
| CA_OHIP | dot+version_sep | 2 | 1.000 | 1.000 | 1.000 |
| CA_OHIP | mixed | 1 | 1.000 | 1.000 | 1.000 |
| CA_OHIP | mixed+version_glued | 1 | 1.000 | 1.000 | 1.000 |
| CA_OHIP | mixed+version_lower | 1 | 1.000 | 0.000 | 1.000 |
| CA_OHIP | mixed+version_sep | 1 | 1.000 | 1.000 | 1.000 |
| CA_OHIP | slash | 4 | 1.000 | 1.000 | 1.000 |
| CA_OHIP | slash+repeat | 1 | 1.000 | 1.000 | 1.000 |
| CA_OHIP | slash+version_lower | 1 | 1.000 | 0.000 | 1.000 |
| CA_OHIP | slash+version_sep | 4 | 1.000 | 1.000 | 1.000 |
| CA_OHIP | slash+version_sep+repeat | 2 | 1.000 | 1.000 | 1.000 |
| CA_OHIP | space | 24 | 1.000 | 1.000 | 1.000 |
| CA_OHIP | space+repeat | 2 | 1.000 | 1.000 | 1.000 |
| CA_OHIP | space+version_glued | 3 | 1.000 | 1.000 | 1.000 |
| CA_OHIP | space+version_glued+repeat | 1 | 1.000 | 1.000 | 1.000 |
| CA_OHIP | space+version_lower | 1 | 1.000 | 0.000 | 1.000 |
| CA_OHIP | space+version_sep | 16 | 1.000 | 1.000 | 1.000 |
| CA_OHIP | space+version_sep+repeat | 1 | 1.000 | 1.000 | 1.000 |
| CA_POSTAL_CODE | compact | 59 | 1.000 | 1.000 | 1.000 |
| CA_POSTAL_CODE | lowercase | 21 | 1.000 | 1.000 | 1.000 |
| CA_POSTAL_CODE | space | 191 | 1.000 | 1.000 | 1.000 |
| CA_RAMQ | compact | 63 | 1.000 | 1.000 | 1.000 |
| CA_RAMQ | compact+repeat | 4 | 1.000 | 1.000 | 1.000 |
| CA_RAMQ | dash | 20 | 1.000 | 1.000 | 1.000 |
| CA_RAMQ | dash+repeat | 2 | 1.000 | 1.000 | 1.000 |
| CA_RAMQ | lowercase | 8 | 1.000 | 0.125 | 0.000 |
| CA_RAMQ | space | 56 | 1.000 | 1.000 | 1.000 |
| CA_RAMQ | space+repeat | 8 | 1.000 | 1.000 | 1.000 |
| CA_SIN | compact | 61 | 1.000 | 1.000 | 1.000 |
| CA_SIN | dash | 83 | 1.000 | 1.000 | 1.000 |
| CA_SIN | dot | 26 | 1.000 | 1.000 | 1.000 |
| CA_SIN | mixed | 16 | 1.000 | 1.000 | 1.000 |
| CA_SIN | slash | 22 | 1.000 | 1.000 | 1.000 |
| CA_SIN | space | 67 | 1.000 | 1.000 | 1.000 |
