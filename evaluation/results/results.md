# Evaluation results

Generated: 2026-07-06T21:31:07+00:00 | Python 3.12.13 | presidio-analyzer 2.2.363 | spacy 3.8.13 | en_core_web_sm 3.8.0

### Stock Presidio — locale=ca, split=gold

| Entity | Gold | Detected (overlap) | Recall | Strict recall | FN rate | Typed exact recall |
|---|---|---|---|---|---|---|
| ADDRESS | 70 | 66 | 0.943 | 0.000 | 0.057 | 0.000 |
| CA_AB_ULI | 21 | 16 | 0.762 | 0.714 | 0.238 | 0.000 |
| CA_BC_PHN | 23 | 23 | 1.000 | 1.000 | 0.000 | 0.000 |
| CA_OHIP | 24 | 14 | 0.583 | 0.125 | 0.417 | 0.000 |
| CA_RAMQ | 32 | 13 | 0.406 | 0.031 | 0.594 | 0.000 |
| CA_SIN | 35 | 11 | 0.314 | 0.314 | 0.686 | 0.000 |
| DATE | 134 | 134 | 1.000 | 0.985 | 0.000 | 0.940 |
| PERSON | 169 | 166 | 0.982 | 0.964 | 0.018 | 0.704 |
| **TOTAL** | 508 | 443 | 0.872 | 0.685 | 0.128 | 0.482 |

Span precision (predicted spans overlapping any gold PII): 0.702 (549/782)
Bootstrap 95% CI (1000 note-resamples): leak recall [0.844, 0.900], strict recall [0.654, 0.717], precision [0.677, 0.728]

### Presidio + pack — locale=ca, split=gold

| Entity | Gold | Detected (overlap) | Recall | Strict recall | FN rate | Typed exact recall |
|---|---|---|---|---|---|---|
| ADDRESS | 70 | 70 | 1.000 | 0.943 | 0.000 | 0.929 |
| CA_AB_ULI | 21 | 21 | 1.000 | 1.000 | 0.000 | 1.000 |
| CA_BC_PHN | 23 | 23 | 1.000 | 1.000 | 0.000 | 1.000 |
| CA_OHIP | 24 | 24 | 1.000 | 1.000 | 0.000 | 1.000 |
| CA_RAMQ | 32 | 32 | 1.000 | 1.000 | 0.000 | 1.000 |
| CA_SIN | 35 | 35 | 1.000 | 1.000 | 0.000 | 1.000 |
| DATE | 134 | 134 | 1.000 | 0.985 | 0.000 | 0.940 |
| PERSON | 169 | 166 | 0.982 | 0.964 | 0.018 | 0.704 |
| **TOTAL** | 508 | 505 | 0.994 | 0.976 | 0.006 | 0.876 |

Span precision (predicted spans overlapping any gold PII): 0.781 (833/1066)
Bootstrap 95% CI (1000 note-resamples): leak recall [0.986, 1.000], strict recall [0.964, 0.988], precision [0.761, 0.802]

### Stock Presidio — locale=ca, split=generated

| Entity | Gold | Detected (overlap) | Recall | Strict recall | FN rate | Typed exact recall |
|---|---|---|---|---|---|---|
| ADDRESS | 615 | 604 | 0.982 | 0.000 | 0.018 | 0.000 |
| CA_AB_ULI | 227 | 161 | 0.709 | 0.670 | 0.291 | 0.000 |
| CA_BC_PHN | 226 | 226 | 1.000 | 1.000 | 0.000 | 0.000 |
| CA_OHIP | 224 | 146 | 0.652 | 0.179 | 0.348 | 0.000 |
| CA_RAMQ | 223 | 115 | 0.516 | 0.049 | 0.484 | 0.000 |
| CA_SIN | 302 | 64 | 0.212 | 0.205 | 0.788 | 0.000 |
| DATE | 1201 | 1201 | 1.000 | 0.990 | 0.000 | 0.969 |
| PERSON | 1478 | 1421 | 0.961 | 0.948 | 0.039 | 0.679 |
| **TOTAL** | 4496 | 3938 | 0.876 | 0.685 | 0.124 | 0.482 |

Span precision (predicted spans overlapping any gold PII): 0.700 (4967/7100)
Bootstrap 95% CI (1000 note-resamples): leak recall [0.868, 0.884], strict recall [0.674, 0.695], precision [0.691, 0.708]

### Presidio + pack — locale=ca, split=generated

| Entity | Gold | Detected (overlap) | Recall | Strict recall | FN rate | Typed exact recall |
|---|---|---|---|---|---|---|
| ADDRESS | 615 | 615 | 1.000 | 0.943 | 0.000 | 0.937 |
| CA_AB_ULI | 227 | 227 | 1.000 | 1.000 | 0.000 | 1.000 |
| CA_BC_PHN | 226 | 226 | 1.000 | 1.000 | 0.000 | 1.000 |
| CA_OHIP | 224 | 224 | 1.000 | 1.000 | 0.000 | 1.000 |
| CA_RAMQ | 223 | 223 | 1.000 | 1.000 | 0.000 | 1.000 |
| CA_SIN | 302 | 302 | 1.000 | 1.000 | 0.000 | 1.000 |
| DATE | 1201 | 1201 | 1.000 | 0.990 | 0.000 | 0.969 |
| PERSON | 1478 | 1421 | 0.961 | 0.948 | 0.039 | 0.679 |
| **TOTAL** | 4496 | 4439 | 0.987 | 0.972 | 0.013 | 0.878 |

Span precision (predicted spans overlapping any gold PII): 0.779 (7509/9642)
Bootstrap 95% CI (1000 note-resamples): leak recall [0.984, 0.990], strict recall [0.968, 0.977], precision [0.772, 0.785]

### Stock Presidio — locale=in, split=gold

| Entity | Gold | Detected (overlap) | Recall | Strict recall | FN rate | Typed exact recall |
|---|---|---|---|---|---|---|
| ADDRESS | 33 | 33 | 1.000 | 0.000 | 0.000 | 0.000 |
| DATE | 133 | 133 | 1.000 | 0.977 | 0.000 | 0.887 |
| IN_AADHAAR | 41 | 28 | 0.683 | 0.561 | 0.317 | 0.000 |
| IN_ABHA | 67 | 48 | 0.716 | 0.627 | 0.284 | 0.000 |
| IN_MOBILE | 74 | 74 | 1.000 | 1.000 | 0.000 | 1.000 |
| IN_PAN | 41 | 2 | 0.049 | 0.049 | 0.951 | 0.000 |
| IN_PASSPORT | 12 | 1 | 0.083 | 0.083 | 0.917 | 0.000 |
| IN_UHID | 59 | 36 | 0.610 | 0.203 | 0.390 | 0.000 |
| IN_VOTER_ID | 13 | 2 | 0.154 | 0.077 | 0.846 | 0.000 |
| PERSON | 167 | 141 | 0.844 | 0.832 | 0.156 | 0.731 |
| **TOTAL** | 640 | 498 | 0.778 | 0.662 | 0.222 | 0.491 |

Span precision (predicted spans overlapping any gold PII): 0.721 (640/888)
Bootstrap 95% CI (1000 note-resamples): leak recall [0.750, 0.805], strict recall [0.635, 0.691], precision [0.702, 0.738]

### Presidio + pack — locale=in, split=gold

| Entity | Gold | Detected (overlap) | Recall | Strict recall | FN rate | Typed exact recall |
|---|---|---|---|---|---|---|
| ADDRESS | 33 | 33 | 1.000 | 0.000 | 0.000 | 0.000 |
| DATE | 133 | 133 | 1.000 | 0.977 | 0.000 | 0.887 |
| IN_AADHAAR | 41 | 41 | 1.000 | 1.000 | 0.000 | 1.000 |
| IN_ABHA | 67 | 67 | 1.000 | 1.000 | 0.000 | 1.000 |
| IN_MOBILE | 74 | 74 | 1.000 | 1.000 | 0.000 | 1.000 |
| IN_PAN | 41 | 41 | 1.000 | 1.000 | 0.000 | 1.000 |
| IN_PASSPORT | 12 | 12 | 1.000 | 1.000 | 0.000 | 1.000 |
| IN_UHID | 59 | 59 | 1.000 | 1.000 | 0.000 | 1.000 |
| IN_VOTER_ID | 13 | 13 | 1.000 | 1.000 | 0.000 | 1.000 |
| PERSON | 167 | 141 | 0.844 | 0.832 | 0.156 | 0.731 |
| **TOTAL** | 640 | 614 | 0.959 | 0.900 | 0.041 | 0.855 |

Span precision (predicted spans overlapping any gold PII): 0.799 (987/1235)
Bootstrap 95% CI (1000 note-resamples): leak recall [0.944, 0.972], strict recall [0.882, 0.919], precision [0.786, 0.812]

### Stock Presidio — locale=in, split=generated

| Entity | Gold | Detected (overlap) | Recall | Strict recall | FN rate | Typed exact recall |
|---|---|---|---|---|---|---|
| ADDRESS | 266 | 264 | 0.992 | 0.000 | 0.008 | 0.000 |
| DATE | 1166 | 1166 | 1.000 | 0.984 | 0.000 | 0.899 |
| IN_AADHAAR | 345 | 261 | 0.757 | 0.617 | 0.243 | 0.000 |
| IN_ABHA | 634 | 469 | 0.740 | 0.574 | 0.260 | 0.000 |
| IN_MOBILE | 592 | 592 | 1.000 | 1.000 | 0.000 | 1.000 |
| IN_PAN | 326 | 21 | 0.064 | 0.064 | 0.936 | 0.000 |
| IN_PASSPORT | 97 | 7 | 0.072 | 0.072 | 0.928 | 0.000 |
| IN_UHID | 574 | 364 | 0.634 | 0.181 | 0.366 | 0.000 |
| IN_VOTER_ID | 90 | 31 | 0.344 | 0.278 | 0.656 | 0.000 |
| PERSON | 1534 | 1364 | 0.889 | 0.878 | 0.111 | 0.730 |
| **TOTAL** | 5624 | 4539 | 0.807 | 0.679 | 0.193 | 0.491 |

Span precision (predicted spans overlapping any gold PII): 0.715 (5758/8055)
Bootstrap 95% CI (1000 note-resamples): leak recall [0.799, 0.815], strict recall [0.671, 0.688], precision [0.709, 0.721]

### Presidio + pack — locale=in, split=generated

| Entity | Gold | Detected (overlap) | Recall | Strict recall | FN rate | Typed exact recall |
|---|---|---|---|---|---|---|
| ADDRESS | 266 | 264 | 0.992 | 0.000 | 0.008 | 0.000 |
| DATE | 1166 | 1166 | 1.000 | 0.984 | 0.000 | 0.899 |
| IN_AADHAAR | 345 | 345 | 1.000 | 1.000 | 0.000 | 1.000 |
| IN_ABHA | 634 | 634 | 1.000 | 1.000 | 0.000 | 1.000 |
| IN_MOBILE | 592 | 592 | 1.000 | 1.000 | 0.000 | 1.000 |
| IN_PAN | 326 | 326 | 1.000 | 1.000 | 0.000 | 1.000 |
| IN_PASSPORT | 97 | 97 | 1.000 | 1.000 | 0.000 | 1.000 |
| IN_UHID | 574 | 574 | 1.000 | 1.000 | 0.000 | 1.000 |
| IN_VOTER_ID | 90 | 90 | 1.000 | 1.000 | 0.000 | 1.000 |
| PERSON | 1534 | 1364 | 0.889 | 0.878 | 0.111 | 0.730 |
| **TOTAL** | 5624 | 5452 | 0.969 | 0.916 | 0.031 | 0.858 |

Span precision (predicted spans overlapping any gold PII): 0.795 (8922/11219)
Bootstrap 95% CI (1000 note-resamples): leak recall [0.965, 0.974], strict recall [0.911, 0.922], precision [0.791, 0.800]
