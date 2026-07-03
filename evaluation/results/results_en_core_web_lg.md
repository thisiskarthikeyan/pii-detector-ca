# Evaluation results

Generated: 2026-07-03T06:05:57+00:00 | Python 3.12.13 | presidio-analyzer 2.2.363 | spacy 3.8.13 | en_core_web_lg 3.8.0

### Stock Presidio — locale=ca, split=gold

| Entity | Gold | Detected (overlap) | Recall | Strict recall | FN rate | Typed exact recall |
|---|---|---|---|---|---|---|
| ADDRESS | 70 | 70 | 1.000 | 0.000 | 0.000 | 0.000 |
| CA_AB_ULI | 28 | 11 | 0.393 | 0.393 | 0.607 | 0.000 |
| CA_BC_PHN | 22 | 22 | 1.000 | 1.000 | 0.000 | 0.000 |
| CA_OHIP | 27 | 18 | 0.667 | 0.185 | 0.333 | 0.000 |
| CA_RAMQ | 23 | 7 | 0.304 | 0.043 | 0.696 | 0.000 |
| CA_SIN | 30 | 0 | 0.000 | 0.000 | 1.000 | 0.000 |
| DATE | 160 | 160 | 1.000 | 0.938 | 0.000 | 0.912 |
| PERSON | 170 | 163 | 0.959 | 0.929 | 0.041 | 0.871 |
| **TOTAL** | 530 | 451 | 0.851 | 0.655 | 0.149 | 0.555 |

Span precision (predicted spans overlapping any gold PII): 0.757 (565/746)
Bootstrap 95% CI (1000 note-resamples): leak recall [0.823, 0.878], strict recall [0.616, 0.696], precision [0.734, 0.781]

### Presidio + pack — locale=ca, split=gold

| Entity | Gold | Detected (overlap) | Recall | Strict recall | FN rate | Typed exact recall |
|---|---|---|---|---|---|---|
| ADDRESS | 70 | 70 | 1.000 | 0.000 | 0.000 | 0.000 |
| CA_AB_ULI | 28 | 28 | 1.000 | 1.000 | 0.000 | 1.000 |
| CA_BC_PHN | 22 | 22 | 1.000 | 1.000 | 0.000 | 1.000 |
| CA_OHIP | 27 | 27 | 1.000 | 1.000 | 0.000 | 1.000 |
| CA_RAMQ | 23 | 23 | 1.000 | 1.000 | 0.000 | 1.000 |
| CA_SIN | 30 | 30 | 1.000 | 1.000 | 0.000 | 1.000 |
| DATE | 160 | 160 | 1.000 | 0.938 | 0.000 | 0.912 |
| PERSON | 170 | 163 | 0.959 | 0.929 | 0.041 | 0.871 |
| **TOTAL** | 530 | 523 | 0.987 | 0.826 | 0.013 | 0.800 |

Span precision (predicted spans overlapping any gold PII): 0.811 (776/957)
Bootstrap 95% CI (1000 note-resamples): leak recall [0.977, 0.994], strict recall [0.802, 0.849], precision [0.792, 0.830]

### Stock Presidio — locale=ca, split=generated

| Entity | Gold | Detected (overlap) | Recall | Strict recall | FN rate | Typed exact recall |
|---|---|---|---|---|---|---|
| ADDRESS | 591 | 591 | 1.000 | 0.000 | 0.000 | 0.000 |
| CA_AB_ULI | 216 | 64 | 0.296 | 0.282 | 0.704 | 0.000 |
| CA_BC_PHN | 226 | 226 | 1.000 | 1.000 | 0.000 | 0.000 |
| CA_OHIP | 220 | 148 | 0.673 | 0.168 | 0.327 | 0.000 |
| CA_RAMQ | 238 | 66 | 0.277 | 0.080 | 0.723 | 0.000 |
| CA_SIN | 311 | 7 | 0.023 | 0.023 | 0.977 | 0.000 |
| DATE | 1520 | 1520 | 1.000 | 0.950 | 0.000 | 0.930 |
| PERSON | 1489 | 1439 | 0.966 | 0.955 | 0.034 | 0.901 |
| **TOTAL** | 4811 | 4061 | 0.844 | 0.668 | 0.156 | 0.572 |

Span precision (predicted spans overlapping any gold PII): 0.743 (4949/6659)
Bootstrap 95% CI (1000 note-resamples): leak recall [0.836, 0.853], strict recall [0.658, 0.680], precision [0.736, 0.751]

### Presidio + pack — locale=ca, split=generated

| Entity | Gold | Detected (overlap) | Recall | Strict recall | FN rate | Typed exact recall |
|---|---|---|---|---|---|---|
| ADDRESS | 591 | 591 | 1.000 | 0.000 | 0.000 | 0.000 |
| CA_AB_ULI | 216 | 216 | 1.000 | 1.000 | 0.000 | 1.000 |
| CA_BC_PHN | 226 | 226 | 1.000 | 1.000 | 0.000 | 1.000 |
| CA_OHIP | 220 | 220 | 1.000 | 1.000 | 0.000 | 1.000 |
| CA_RAMQ | 238 | 238 | 1.000 | 1.000 | 0.000 | 1.000 |
| CA_SIN | 311 | 311 | 1.000 | 1.000 | 0.000 | 1.000 |
| DATE | 1520 | 1520 | 1.000 | 0.950 | 0.000 | 0.930 |
| PERSON | 1489 | 1439 | 0.966 | 0.955 | 0.034 | 0.901 |
| **TOTAL** | 4811 | 4761 | 0.990 | 0.847 | 0.010 | 0.824 |

Span precision (predicted spans overlapping any gold PII): 0.801 (6868/8578)
Bootstrap 95% CI (1000 note-resamples): leak recall [0.987, 0.992], strict recall [0.841, 0.854], precision [0.795, 0.807]

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
