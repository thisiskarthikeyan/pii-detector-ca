# Evaluation results

Generated: 2026-07-03T18:57:01+00:00 | Python 3.12.13 | presidio-analyzer 2.2.363 | spacy 3.8.13 | en_core_web_lg 3.8.0

### Stock Presidio — locale=ca, split=gold

| Entity | Gold | Detected (overlap) | Recall | Strict recall | FN rate | Typed exact recall |
|---|---|---|---|---|---|---|
| ADDRESS | 62 | 61 | 0.984 | 0.000 | 0.016 | 0.000 |
| CA_AB_ULI | 25 | 8 | 0.320 | 0.320 | 0.680 | 0.000 |
| CA_BC_PHN | 25 | 25 | 1.000 | 1.000 | 0.000 | 0.000 |
| CA_OHIP | 26 | 19 | 0.731 | 0.231 | 0.269 | 0.000 |
| CA_RAMQ | 24 | 11 | 0.458 | 0.125 | 0.542 | 0.000 |
| CA_SIN | 32 | 0 | 0.000 | 0.000 | 1.000 | 0.000 |
| DATE | 141 | 141 | 1.000 | 0.957 | 0.000 | 0.957 |
| PERSON | 169 | 165 | 0.976 | 0.976 | 0.024 | 0.858 |
| **TOTAL** | 504 | 430 | 0.853 | 0.679 | 0.147 | 0.556 |

Span precision (predicted spans overlapping any gold PII): 0.705 (526/746)
Bootstrap 95% CI (1000 note-resamples): leak recall [0.828, 0.880], strict recall [0.644, 0.716], precision [0.684, 0.729]

### Presidio + pack — locale=ca, split=gold

| Entity | Gold | Detected (overlap) | Recall | Strict recall | FN rate | Typed exact recall |
|---|---|---|---|---|---|---|
| ADDRESS | 62 | 62 | 1.000 | 0.000 | 0.000 | 0.000 |
| CA_AB_ULI | 25 | 25 | 1.000 | 1.000 | 0.000 | 1.000 |
| CA_BC_PHN | 25 | 25 | 1.000 | 1.000 | 0.000 | 1.000 |
| CA_OHIP | 26 | 26 | 1.000 | 1.000 | 0.000 | 1.000 |
| CA_RAMQ | 24 | 24 | 1.000 | 1.000 | 0.000 | 1.000 |
| CA_SIN | 32 | 32 | 1.000 | 1.000 | 0.000 | 1.000 |
| DATE | 141 | 141 | 1.000 | 0.957 | 0.000 | 0.957 |
| PERSON | 169 | 165 | 0.976 | 0.976 | 0.024 | 0.858 |
| **TOTAL** | 504 | 500 | 0.992 | 0.857 | 0.008 | 0.817 |

Span precision (predicted spans overlapping any gold PII): 0.769 (734/954)
Bootstrap 95% CI (1000 note-resamples): leak recall [0.984, 0.998], strict recall [0.840, 0.876], precision [0.751, 0.789]

### Stock Presidio — locale=ca, split=generated

| Entity | Gold | Detected (overlap) | Recall | Strict recall | FN rate | Typed exact recall |
|---|---|---|---|---|---|---|
| ADDRESS | 605 | 597 | 0.987 | 0.000 | 0.013 | 0.000 |
| CA_AB_ULI | 222 | 80 | 0.360 | 0.351 | 0.640 | 0.000 |
| CA_BC_PHN | 213 | 213 | 1.000 | 1.000 | 0.000 | 0.000 |
| CA_OHIP | 261 | 163 | 0.625 | 0.207 | 0.375 | 0.000 |
| CA_RAMQ | 204 | 59 | 0.289 | 0.064 | 0.711 | 0.000 |
| CA_SIN | 302 | 12 | 0.040 | 0.033 | 0.960 | 0.000 |
| DATE | 1197 | 1197 | 1.000 | 0.942 | 0.000 | 0.933 |
| PERSON | 1505 | 1456 | 0.967 | 0.960 | 0.033 | 0.860 |
| **TOTAL** | 4509 | 3777 | 0.838 | 0.652 | 0.162 | 0.535 |

Span precision (predicted spans overlapping any gold PII): 0.701 (4697/6697)
Bootstrap 95% CI (1000 note-resamples): leak recall [0.829, 0.846], strict recall [0.640, 0.663], precision [0.694, 0.709]

### Presidio + pack — locale=ca, split=generated

| Entity | Gold | Detected (overlap) | Recall | Strict recall | FN rate | Typed exact recall |
|---|---|---|---|---|---|---|
| ADDRESS | 605 | 605 | 1.000 | 0.000 | 0.000 | 0.000 |
| CA_AB_ULI | 222 | 222 | 1.000 | 1.000 | 0.000 | 1.000 |
| CA_BC_PHN | 213 | 213 | 1.000 | 1.000 | 0.000 | 1.000 |
| CA_OHIP | 261 | 261 | 1.000 | 1.000 | 0.000 | 1.000 |
| CA_RAMQ | 204 | 204 | 1.000 | 1.000 | 0.000 | 1.000 |
| CA_SIN | 302 | 302 | 1.000 | 1.000 | 0.000 | 1.000 |
| DATE | 1197 | 1197 | 1.000 | 0.942 | 0.000 | 0.933 |
| PERSON | 1505 | 1456 | 0.967 | 0.960 | 0.033 | 0.860 |
| **TOTAL** | 4509 | 4460 | 0.989 | 0.837 | 0.011 | 0.801 |

Span precision (predicted spans overlapping any gold PII): 0.768 (6614/8614)
Bootstrap 95% CI (1000 note-resamples): leak recall [0.986, 0.992], strict recall [0.830, 0.844], precision [0.762, 0.774]

### Stock Presidio — locale=in, split=gold

| Entity | Gold | Detected (overlap) | Recall | Strict recall | FN rate | Typed exact recall |
|---|---|---|---|---|---|---|
| ADDRESS | 33 | 33 | 1.000 | 0.000 | 0.000 | 0.000 |
| DATE | 133 | 133 | 1.000 | 0.940 | 0.000 | 0.865 |
| IN_AADHAAR | 41 | 14 | 0.341 | 0.293 | 0.659 | 0.000 |
| IN_ABHA | 67 | 16 | 0.239 | 0.164 | 0.761 | 0.000 |
| IN_MOBILE | 74 | 74 | 1.000 | 1.000 | 0.000 | 1.000 |
| IN_PAN | 41 | 3 | 0.073 | 0.073 | 0.927 | 0.000 |
| IN_PASSPORT | 12 | 0 | 0.000 | 0.000 | 1.000 | 0.000 |
| IN_UHID | 59 | 34 | 0.576 | 0.186 | 0.424 | 0.000 |
| IN_VOTER_ID | 13 | 3 | 0.231 | 0.154 | 0.769 | 0.000 |
| PERSON | 167 | 167 | 1.000 | 1.000 | 0.000 | 0.826 |
| **TOTAL** | 640 | 477 | 0.745 | 0.633 | 0.255 | 0.511 |

Span precision (predicted spans overlapping any gold PII): 0.701 (588/839)
Bootstrap 95% CI (1000 note-resamples): leak recall [0.727, 0.765], strict recall [0.611, 0.654], precision [0.686, 0.715]

### Presidio + pack — locale=in, split=gold

| Entity | Gold | Detected (overlap) | Recall | Strict recall | FN rate | Typed exact recall |
|---|---|---|---|---|---|---|
| ADDRESS | 33 | 33 | 1.000 | 0.000 | 0.000 | 0.000 |
| DATE | 133 | 133 | 1.000 | 0.940 | 0.000 | 0.865 |
| IN_AADHAAR | 41 | 41 | 1.000 | 1.000 | 0.000 | 1.000 |
| IN_ABHA | 67 | 67 | 1.000 | 1.000 | 0.000 | 1.000 |
| IN_MOBILE | 74 | 74 | 1.000 | 1.000 | 0.000 | 1.000 |
| IN_PAN | 41 | 41 | 1.000 | 1.000 | 0.000 | 1.000 |
| IN_PASSPORT | 12 | 12 | 1.000 | 1.000 | 0.000 | 1.000 |
| IN_UHID | 59 | 59 | 1.000 | 1.000 | 0.000 | 1.000 |
| IN_VOTER_ID | 13 | 13 | 1.000 | 1.000 | 0.000 | 1.000 |
| PERSON | 167 | 167 | 1.000 | 1.000 | 0.000 | 0.826 |
| **TOTAL** | 640 | 640 | 1.000 | 0.936 | 0.000 | 0.875 |

Span precision (predicted spans overlapping any gold PII): 0.788 (935/1186)
Bootstrap 95% CI (1000 note-resamples): leak recall [1.000, 1.000], strict recall [0.922, 0.951], precision [0.778, 0.799]

### Stock Presidio — locale=in, split=generated

| Entity | Gold | Detected (overlap) | Recall | Strict recall | FN rate | Typed exact recall |
|---|---|---|---|---|---|---|
| ADDRESS | 266 | 266 | 1.000 | 0.000 | 0.000 | 0.000 |
| DATE | 1166 | 1166 | 1.000 | 0.955 | 0.000 | 0.881 |
| IN_AADHAAR | 345 | 122 | 0.354 | 0.255 | 0.646 | 0.000 |
| IN_ABHA | 634 | 135 | 0.213 | 0.156 | 0.787 | 0.000 |
| IN_MOBILE | 592 | 592 | 1.000 | 1.000 | 0.000 | 1.000 |
| IN_PAN | 326 | 30 | 0.092 | 0.092 | 0.908 | 0.000 |
| IN_PASSPORT | 97 | 1 | 0.010 | 0.010 | 0.990 | 0.000 |
| IN_UHID | 574 | 364 | 0.634 | 0.155 | 0.366 | 0.000 |
| IN_VOTER_ID | 90 | 28 | 0.311 | 0.222 | 0.689 | 0.000 |
| PERSON | 1534 | 1527 | 0.995 | 0.990 | 0.005 | 0.826 |
| **TOTAL** | 5624 | 4231 | 0.752 | 0.631 | 0.248 | 0.513 |

Span precision (predicted spans overlapping any gold PII): 0.698 (5142/7365)
Bootstrap 95% CI (1000 note-resamples): leak recall [0.746, 0.759], strict recall [0.624, 0.639], precision [0.693, 0.703]

### Presidio + pack — locale=in, split=generated

| Entity | Gold | Detected (overlap) | Recall | Strict recall | FN rate | Typed exact recall |
|---|---|---|---|---|---|---|
| ADDRESS | 266 | 266 | 1.000 | 0.000 | 0.000 | 0.000 |
| DATE | 1166 | 1166 | 1.000 | 0.955 | 0.000 | 0.881 |
| IN_AADHAAR | 345 | 345 | 1.000 | 1.000 | 0.000 | 1.000 |
| IN_ABHA | 634 | 634 | 1.000 | 1.000 | 0.000 | 1.000 |
| IN_MOBILE | 592 | 592 | 1.000 | 1.000 | 0.000 | 1.000 |
| IN_PAN | 326 | 326 | 1.000 | 1.000 | 0.000 | 1.000 |
| IN_PASSPORT | 97 | 97 | 1.000 | 1.000 | 0.000 | 1.000 |
| IN_UHID | 574 | 574 | 1.000 | 1.000 | 0.000 | 1.000 |
| IN_VOTER_ID | 90 | 90 | 1.000 | 1.000 | 0.000 | 1.000 |
| PERSON | 1534 | 1527 | 0.995 | 0.990 | 0.005 | 0.826 |
| **TOTAL** | 5624 | 5617 | 0.999 | 0.941 | 0.001 | 0.881 |

Span precision (predicted spans overlapping any gold PII): 0.789 (8306/10529)
Bootstrap 95% CI (1000 note-resamples): leak recall [0.998, 1.000], strict recall [0.936, 0.946], precision [0.785, 0.793]
