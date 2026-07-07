# Evaluation results

Generated: 2026-07-06T21:32:09+00:00 | Python 3.12.13 | presidio-analyzer 2.2.363 | spacy 3.8.13 | en_core_web_lg 3.8.0

### Stock Presidio — locale=ca, split=gold

| Entity | Gold | Detected (overlap) | Recall | Strict recall | FN rate | Typed exact recall |
|---|---|---|---|---|---|---|
| ADDRESS | 70 | 70 | 1.000 | 0.000 | 0.000 | 0.000 |
| CA_AB_ULI | 21 | 8 | 0.381 | 0.333 | 0.619 | 0.000 |
| CA_BC_PHN | 23 | 23 | 1.000 | 1.000 | 0.000 | 0.000 |
| CA_OHIP | 24 | 14 | 0.583 | 0.125 | 0.417 | 0.000 |
| CA_RAMQ | 32 | 10 | 0.312 | 0.125 | 0.688 | 0.000 |
| CA_SIN | 35 | 1 | 0.029 | 0.029 | 0.971 | 0.000 |
| DATE | 134 | 134 | 1.000 | 0.918 | 0.000 | 0.918 |
| PERSON | 169 | 168 | 0.994 | 0.988 | 0.006 | 0.840 |
| **TOTAL** | 508 | 428 | 0.843 | 0.646 | 0.157 | 0.522 |

Span precision (predicted spans overlapping any gold PII): 0.724 (528/729)
Bootstrap 95% CI (1000 note-resamples): leak recall [0.816, 0.868], strict recall [0.612, 0.679], precision [0.703, 0.747]

### Presidio + pack — locale=ca, split=gold

| Entity | Gold | Detected (overlap) | Recall | Strict recall | FN rate | Typed exact recall |
|---|---|---|---|---|---|---|
| ADDRESS | 70 | 70 | 1.000 | 0.929 | 0.000 | 0.929 |
| CA_AB_ULI | 21 | 21 | 1.000 | 1.000 | 0.000 | 1.000 |
| CA_BC_PHN | 23 | 23 | 1.000 | 1.000 | 0.000 | 1.000 |
| CA_OHIP | 24 | 24 | 1.000 | 1.000 | 0.000 | 1.000 |
| CA_RAMQ | 32 | 32 | 1.000 | 1.000 | 0.000 | 1.000 |
| CA_SIN | 35 | 35 | 1.000 | 1.000 | 0.000 | 1.000 |
| DATE | 134 | 134 | 1.000 | 0.918 | 0.000 | 0.918 |
| PERSON | 169 | 168 | 0.994 | 0.988 | 0.006 | 0.840 |
| **TOTAL** | 508 | 507 | 0.998 | 0.965 | 0.002 | 0.915 |

Span precision (predicted spans overlapping any gold PII): 0.802 (812/1013)
Bootstrap 95% CI (1000 note-resamples): leak recall [0.994, 1.000], strict recall [0.947, 0.980], precision [0.784, 0.818]

### Stock Presidio — locale=ca, split=generated

| Entity | Gold | Detected (overlap) | Recall | Strict recall | FN rate | Typed exact recall |
|---|---|---|---|---|---|---|
| ADDRESS | 615 | 610 | 0.992 | 0.000 | 0.008 | 0.000 |
| CA_AB_ULI | 227 | 82 | 0.361 | 0.335 | 0.639 | 0.000 |
| CA_BC_PHN | 226 | 226 | 1.000 | 1.000 | 0.000 | 0.000 |
| CA_OHIP | 224 | 144 | 0.643 | 0.201 | 0.357 | 0.000 |
| CA_RAMQ | 223 | 62 | 0.278 | 0.058 | 0.722 | 0.000 |
| CA_SIN | 302 | 12 | 0.040 | 0.036 | 0.960 | 0.000 |
| DATE | 1201 | 1201 | 1.000 | 0.954 | 0.000 | 0.946 |
| PERSON | 1478 | 1446 | 0.978 | 0.975 | 0.022 | 0.893 |
| **TOTAL** | 4496 | 3783 | 0.841 | 0.658 | 0.159 | 0.546 |

Span precision (predicted spans overlapping any gold PII): 0.702 (4703/6695)
Bootstrap 95% CI (1000 note-resamples): leak recall [0.833, 0.851], strict recall [0.647, 0.669], precision [0.695, 0.710]

### Presidio + pack — locale=ca, split=generated

| Entity | Gold | Detected (overlap) | Recall | Strict recall | FN rate | Typed exact recall |
|---|---|---|---|---|---|---|
| ADDRESS | 615 | 615 | 1.000 | 0.946 | 0.000 | 0.937 |
| CA_AB_ULI | 227 | 227 | 1.000 | 1.000 | 0.000 | 1.000 |
| CA_BC_PHN | 226 | 226 | 1.000 | 1.000 | 0.000 | 1.000 |
| CA_OHIP | 224 | 224 | 1.000 | 1.000 | 0.000 | 1.000 |
| CA_RAMQ | 223 | 223 | 1.000 | 1.000 | 0.000 | 1.000 |
| CA_SIN | 302 | 302 | 1.000 | 1.000 | 0.000 | 1.000 |
| DATE | 1201 | 1201 | 1.000 | 0.954 | 0.000 | 0.946 |
| PERSON | 1478 | 1446 | 0.978 | 0.975 | 0.022 | 0.893 |
| **TOTAL** | 4496 | 4464 | 0.993 | 0.972 | 0.007 | 0.942 |

Span precision (predicted spans overlapping any gold PII): 0.784 (7245/9237)
Bootstrap 95% CI (1000 note-resamples): leak recall [0.991, 0.995], strict recall [0.967, 0.977], precision [0.779, 0.790]

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
