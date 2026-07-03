# Evaluation results

Generated: 2026-07-03T19:23:51+00:00 | Python 3.12.13 | presidio-analyzer 2.2.363 | spacy 3.8.13 | en_core_web_sm 3.8.0

### Stock Presidio — locale=ca, split=gold

| Entity | Gold | Detected (overlap) | Recall | Strict recall | FN rate | Typed exact recall |
|---|---|---|---|---|---|---|
| ADDRESS | 68 | 65 | 0.956 | 0.000 | 0.044 | 0.000 |
| CA_AB_ULI | 27 | 21 | 0.778 | 0.704 | 0.222 | 0.000 |
| CA_BC_PHN | 27 | 27 | 1.000 | 1.000 | 0.000 | 0.000 |
| CA_OHIP | 25 | 17 | 0.680 | 0.160 | 0.320 | 0.000 |
| CA_RAMQ | 21 | 11 | 0.524 | 0.048 | 0.476 | 0.000 |
| CA_SIN | 30 | 9 | 0.300 | 0.300 | 0.700 | 0.000 |
| DATE | 134 | 134 | 1.000 | 1.000 | 0.000 | 0.948 |
| PERSON | 167 | 159 | 0.952 | 0.928 | 0.048 | 0.743 |
| **TOTAL** | 499 | 443 | 0.888 | 0.699 | 0.112 | 0.503 |

Span precision (predicted spans overlapping any gold PII): 0.694 (557/803)
Bootstrap 95% CI (1000 note-resamples): leak recall [0.861, 0.914], strict recall [0.670, 0.732], precision [0.669, 0.720]

### Presidio + pack — locale=ca, split=gold

| Entity | Gold | Detected (overlap) | Recall | Strict recall | FN rate | Typed exact recall |
|---|---|---|---|---|---|---|
| ADDRESS | 68 | 68 | 1.000 | 0.000 | 0.000 | 0.000 |
| CA_AB_ULI | 27 | 27 | 1.000 | 1.000 | 0.000 | 1.000 |
| CA_BC_PHN | 27 | 27 | 1.000 | 1.000 | 0.000 | 1.000 |
| CA_OHIP | 25 | 25 | 1.000 | 1.000 | 0.000 | 1.000 |
| CA_RAMQ | 21 | 21 | 1.000 | 1.000 | 0.000 | 1.000 |
| CA_SIN | 30 | 30 | 1.000 | 1.000 | 0.000 | 1.000 |
| DATE | 134 | 134 | 1.000 | 1.000 | 0.000 | 0.948 |
| PERSON | 167 | 159 | 0.952 | 0.928 | 0.048 | 0.743 |
| **TOTAL** | 499 | 491 | 0.984 | 0.840 | 0.016 | 0.764 |

Span precision (predicted spans overlapping any gold PII): 0.758 (770/1016)
Bootstrap 95% CI (1000 note-resamples): leak recall [0.972, 0.994], strict recall [0.819, 0.859], precision [0.737, 0.779]

### Stock Presidio — locale=ca, split=generated

| Entity | Gold | Detected (overlap) | Recall | Strict recall | FN rate | Typed exact recall |
|---|---|---|---|---|---|---|
| ADDRESS | 594 | 584 | 0.983 | 0.000 | 0.017 | 0.000 |
| CA_AB_ULI | 231 | 165 | 0.714 | 0.667 | 0.286 | 0.000 |
| CA_BC_PHN | 228 | 228 | 1.000 | 1.000 | 0.000 | 0.000 |
| CA_OHIP | 207 | 138 | 0.667 | 0.184 | 0.333 | 0.000 |
| CA_RAMQ | 234 | 122 | 0.521 | 0.038 | 0.479 | 0.000 |
| CA_SIN | 307 | 69 | 0.225 | 0.218 | 0.775 | 0.000 |
| DATE | 1221 | 1221 | 1.000 | 0.989 | 0.000 | 0.962 |
| PERSON | 1494 | 1418 | 0.949 | 0.930 | 0.051 | 0.679 |
| **TOTAL** | 4516 | 3945 | 0.874 | 0.685 | 0.126 | 0.485 |

Span precision (predicted spans overlapping any gold PII): 0.699 (4925/7047)
Bootstrap 95% CI (1000 note-resamples): leak recall [0.865, 0.882], strict recall [0.673, 0.696], precision [0.691, 0.707]

### Presidio + pack — locale=ca, split=generated

| Entity | Gold | Detected (overlap) | Recall | Strict recall | FN rate | Typed exact recall |
|---|---|---|---|---|---|---|
| ADDRESS | 594 | 594 | 1.000 | 0.000 | 0.000 | 0.000 |
| CA_AB_ULI | 231 | 231 | 1.000 | 1.000 | 0.000 | 1.000 |
| CA_BC_PHN | 228 | 228 | 1.000 | 1.000 | 0.000 | 1.000 |
| CA_OHIP | 207 | 207 | 1.000 | 1.000 | 0.000 | 1.000 |
| CA_RAMQ | 234 | 234 | 1.000 | 1.000 | 0.000 | 1.000 |
| CA_SIN | 307 | 307 | 1.000 | 1.000 | 0.000 | 1.000 |
| DATE | 1221 | 1221 | 1.000 | 0.989 | 0.000 | 0.962 |
| PERSON | 1494 | 1418 | 0.949 | 0.930 | 0.051 | 0.679 |
| **TOTAL** | 4516 | 4440 | 0.983 | 0.842 | 0.017 | 0.752 |

Span precision (predicted spans overlapping any gold PII): 0.764 (6864/8986)
Bootstrap 95% CI (1000 note-resamples): leak recall [0.980, 0.987], strict recall [0.834, 0.849], precision [0.757, 0.770]

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
