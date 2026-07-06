# Evaluation results

Generated: 2026-07-03T22:03:55+00:00 | Python 3.12.13 | presidio-analyzer 2.2.363 | spacy 3.8.13 | en_core_web_lg 3.8.0

### Stock Presidio — locale=ca, split=gold

| Entity | Gold | Detected (overlap) | Recall | Strict recall | FN rate | Typed exact recall |
|---|---|---|---|---|---|---|
| ADDRESS | 68 | 68 | 1.000 | 0.000 | 0.000 | 0.000 |
| CA_AB_ULI | 27 | 9 | 0.333 | 0.333 | 0.667 | 0.000 |
| CA_BC_PHN | 27 | 27 | 1.000 | 1.000 | 0.000 | 0.000 |
| CA_OHIP | 25 | 17 | 0.680 | 0.160 | 0.320 | 0.000 |
| CA_RAMQ | 21 | 5 | 0.238 | 0.095 | 0.762 | 0.000 |
| CA_SIN | 30 | 1 | 0.033 | 0.033 | 0.967 | 0.000 |
| DATE | 134 | 134 | 1.000 | 0.963 | 0.000 | 0.955 |
| PERSON | 167 | 166 | 0.994 | 0.976 | 0.006 | 0.886 |
| **TOTAL** | 499 | 427 | 0.856 | 0.671 | 0.144 | 0.553 |

Span precision (predicted spans overlapping any gold PII): 0.700 (523/747)
Bootstrap 95% CI (1000 note-resamples): leak recall [0.833, 0.879], strict recall [0.642, 0.702], precision [0.680, 0.722]

### Presidio + pack — locale=ca, split=gold

| Entity | Gold | Detected (overlap) | Recall | Strict recall | FN rate | Typed exact recall |
|---|---|---|---|---|---|---|
| ADDRESS | 68 | 68 | 1.000 | 0.971 | 0.000 | 0.971 |
| CA_AB_ULI | 27 | 27 | 1.000 | 1.000 | 0.000 | 1.000 |
| CA_BC_PHN | 27 | 27 | 1.000 | 1.000 | 0.000 | 1.000 |
| CA_OHIP | 25 | 25 | 1.000 | 1.000 | 0.000 | 1.000 |
| CA_RAMQ | 21 | 21 | 1.000 | 1.000 | 0.000 | 1.000 |
| CA_SIN | 30 | 30 | 1.000 | 1.000 | 0.000 | 1.000 |
| DATE | 134 | 134 | 1.000 | 0.963 | 0.000 | 0.955 |
| PERSON | 167 | 166 | 0.994 | 0.976 | 0.006 | 0.886 |
| **TOTAL** | 499 | 498 | 0.998 | 0.978 | 0.002 | 0.946 |

Span precision (predicted spans overlapping any gold PII): 0.782 (804/1028)
Bootstrap 95% CI (1000 note-resamples): leak recall [0.994, 1.000], strict recall [0.965, 0.990], precision [0.766, 0.800]

### Stock Presidio — locale=ca, split=generated

| Entity | Gold | Detected (overlap) | Recall | Strict recall | FN rate | Typed exact recall |
|---|---|---|---|---|---|---|
| ADDRESS | 594 | 588 | 0.990 | 0.000 | 0.010 | 0.000 |
| CA_AB_ULI | 231 | 76 | 0.329 | 0.316 | 0.671 | 0.000 |
| CA_BC_PHN | 228 | 228 | 1.000 | 1.000 | 0.000 | 0.000 |
| CA_OHIP | 207 | 137 | 0.662 | 0.213 | 0.338 | 0.000 |
| CA_RAMQ | 234 | 72 | 0.308 | 0.085 | 0.692 | 0.000 |
| CA_SIN | 307 | 8 | 0.026 | 0.023 | 0.974 | 0.000 |
| DATE | 1221 | 1221 | 1.000 | 0.933 | 0.000 | 0.923 |
| PERSON | 1494 | 1464 | 0.980 | 0.977 | 0.020 | 0.891 |
| **TOTAL** | 4516 | 3794 | 0.840 | 0.658 | 0.160 | 0.544 |

Span precision (predicted spans overlapping any gold PII): 0.705 (4712/6682)
Bootstrap 95% CI (1000 note-resamples): leak recall [0.832, 0.849], strict recall [0.646, 0.669], precision [0.698, 0.712]

### Presidio + pack — locale=ca, split=generated

| Entity | Gold | Detected (overlap) | Recall | Strict recall | FN rate | Typed exact recall |
|---|---|---|---|---|---|---|
| ADDRESS | 594 | 594 | 1.000 | 0.946 | 0.000 | 0.943 |
| CA_AB_ULI | 231 | 231 | 1.000 | 1.000 | 0.000 | 1.000 |
| CA_BC_PHN | 228 | 228 | 1.000 | 1.000 | 0.000 | 1.000 |
| CA_OHIP | 207 | 207 | 1.000 | 1.000 | 0.000 | 1.000 |
| CA_RAMQ | 234 | 234 | 1.000 | 1.000 | 0.000 | 1.000 |
| CA_SIN | 307 | 307 | 1.000 | 1.000 | 0.000 | 1.000 |
| DATE | 1221 | 1221 | 1.000 | 0.933 | 0.000 | 0.923 |
| PERSON | 1494 | 1464 | 0.980 | 0.977 | 0.020 | 0.891 |
| **TOTAL** | 4516 | 4486 | 0.993 | 0.967 | 0.007 | 0.936 |

Span precision (predicted spans overlapping any gold PII): 0.786 (7241/9211)
Bootstrap 95% CI (1000 note-resamples): leak recall [0.991, 0.996], strict recall [0.962, 0.972], precision [0.781, 0.792]

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
