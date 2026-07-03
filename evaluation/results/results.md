# Evaluation results

Generated: 2026-07-03T18:54:16+00:00 | Python 3.12.13 | presidio-analyzer 2.2.363 | spacy 3.8.13 | en_core_web_sm 3.8.0

### Stock Presidio — locale=ca, split=gold

| Entity | Gold | Detected (overlap) | Recall | Strict recall | FN rate | Typed exact recall |
|---|---|---|---|---|---|---|
| ADDRESS | 62 | 62 | 1.000 | 0.000 | 0.000 | 0.000 |
| CA_AB_ULI | 25 | 19 | 0.760 | 0.680 | 0.240 | 0.000 |
| CA_BC_PHN | 25 | 25 | 1.000 | 1.000 | 0.000 | 0.000 |
| CA_OHIP | 26 | 18 | 0.692 | 0.192 | 0.308 | 0.000 |
| CA_RAMQ | 24 | 16 | 0.667 | 0.083 | 0.333 | 0.000 |
| CA_SIN | 32 | 7 | 0.219 | 0.219 | 0.781 | 0.000 |
| DATE | 141 | 141 | 1.000 | 0.993 | 0.000 | 0.972 |
| PERSON | 169 | 166 | 0.982 | 0.959 | 0.018 | 0.657 |
| **TOTAL** | 504 | 454 | 0.901 | 0.710 | 0.099 | 0.492 |

Span precision (predicted spans overlapping any gold PII): 0.709 (560/790)
Bootstrap 95% CI (1000 note-resamples): leak recall [0.879, 0.922], strict recall [0.677, 0.745], precision [0.684, 0.735]

### Presidio + pack — locale=ca, split=gold

| Entity | Gold | Detected (overlap) | Recall | Strict recall | FN rate | Typed exact recall |
|---|---|---|---|---|---|---|
| ADDRESS | 62 | 62 | 1.000 | 0.000 | 0.000 | 0.000 |
| CA_AB_ULI | 25 | 25 | 1.000 | 1.000 | 0.000 | 1.000 |
| CA_BC_PHN | 25 | 25 | 1.000 | 1.000 | 0.000 | 1.000 |
| CA_OHIP | 26 | 26 | 1.000 | 1.000 | 0.000 | 1.000 |
| CA_RAMQ | 24 | 24 | 1.000 | 1.000 | 0.000 | 1.000 |
| CA_SIN | 32 | 32 | 1.000 | 1.000 | 0.000 | 1.000 |
| DATE | 141 | 141 | 1.000 | 0.993 | 0.000 | 0.972 |
| PERSON | 169 | 166 | 0.982 | 0.959 | 0.018 | 0.657 |
| **TOTAL** | 504 | 501 | 0.994 | 0.861 | 0.006 | 0.754 |

Span precision (predicted spans overlapping any gold PII): 0.770 (768/998)
Bootstrap 95% CI (1000 note-resamples): leak recall [0.987, 1.000], strict recall [0.843, 0.880], precision [0.748, 0.792]

### Stock Presidio — locale=ca, split=generated

| Entity | Gold | Detected (overlap) | Recall | Strict recall | FN rate | Typed exact recall |
|---|---|---|---|---|---|---|
| ADDRESS | 605 | 589 | 0.974 | 0.000 | 0.026 | 0.000 |
| CA_AB_ULI | 222 | 166 | 0.748 | 0.721 | 0.252 | 0.000 |
| CA_BC_PHN | 213 | 213 | 1.000 | 1.000 | 0.000 | 0.000 |
| CA_OHIP | 261 | 165 | 0.632 | 0.188 | 0.368 | 0.000 |
| CA_RAMQ | 204 | 103 | 0.505 | 0.034 | 0.495 | 0.000 |
| CA_SIN | 302 | 68 | 0.225 | 0.222 | 0.775 | 0.000 |
| DATE | 1197 | 1197 | 1.000 | 0.982 | 0.000 | 0.964 |
| PERSON | 1505 | 1439 | 0.956 | 0.916 | 0.044 | 0.639 |
| **TOTAL** | 4509 | 3940 | 0.874 | 0.676 | 0.126 | 0.469 |

Span precision (predicted spans overlapping any gold PII): 0.698 (5024/7201)
Bootstrap 95% CI (1000 note-resamples): leak recall [0.866, 0.883], strict recall [0.664, 0.688], precision [0.690, 0.706]

### Presidio + pack — locale=ca, split=generated

| Entity | Gold | Detected (overlap) | Recall | Strict recall | FN rate | Typed exact recall |
|---|---|---|---|---|---|---|
| ADDRESS | 605 | 605 | 1.000 | 0.000 | 0.000 | 0.000 |
| CA_AB_ULI | 222 | 222 | 1.000 | 1.000 | 0.000 | 1.000 |
| CA_BC_PHN | 213 | 213 | 1.000 | 1.000 | 0.000 | 1.000 |
| CA_OHIP | 261 | 261 | 1.000 | 1.000 | 0.000 | 1.000 |
| CA_RAMQ | 204 | 204 | 1.000 | 1.000 | 0.000 | 1.000 |
| CA_SIN | 302 | 302 | 1.000 | 1.000 | 0.000 | 1.000 |
| DATE | 1197 | 1197 | 1.000 | 0.982 | 0.000 | 0.964 |
| PERSON | 1505 | 1439 | 0.956 | 0.916 | 0.044 | 0.639 |
| **TOTAL** | 4509 | 4443 | 0.985 | 0.833 | 0.015 | 0.736 |

Span precision (predicted spans overlapping any gold PII): 0.761 (6941/9118)
Bootstrap 95% CI (1000 note-resamples): leak recall [0.982, 0.989], strict recall [0.825, 0.840], precision [0.755, 0.768]

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
