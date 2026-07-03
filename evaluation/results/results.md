# Evaluation results

Generated: 2026-07-03T06:17:11+00:00 | Python 3.12.13 | presidio-analyzer 2.2.363 | spacy 3.8.13 | en_core_web_sm 3.8.0

### Stock Presidio — locale=ca, split=gold

| Entity | Gold | Detected (overlap) | Recall | Strict recall | FN rate | Typed exact recall |
|---|---|---|---|---|---|---|
| ADDRESS | 70 | 70 | 1.000 | 0.000 | 0.000 | 0.000 |
| CA_AB_ULI | 28 | 18 | 0.643 | 0.643 | 0.357 | 0.000 |
| CA_BC_PHN | 22 | 22 | 1.000 | 1.000 | 0.000 | 0.000 |
| CA_OHIP | 27 | 19 | 0.704 | 0.148 | 0.296 | 0.000 |
| CA_RAMQ | 23 | 13 | 0.565 | 0.043 | 0.435 | 0.000 |
| CA_SIN | 30 | 4 | 0.133 | 0.133 | 0.867 | 0.000 |
| DATE | 160 | 160 | 1.000 | 1.000 | 0.000 | 0.988 |
| PERSON | 170 | 163 | 0.959 | 0.818 | 0.041 | 0.559 |
| **TOTAL** | 530 | 469 | 0.885 | 0.657 | 0.115 | 0.477 |

Span precision (predicted spans overlapping any gold PII): 0.773 (610/789)
Bootstrap 95% CI (1000 note-resamples): leak recall [0.858, 0.912], strict recall [0.621, 0.691], precision [0.747, 0.798]

### Presidio + pack — locale=ca, split=gold

| Entity | Gold | Detected (overlap) | Recall | Strict recall | FN rate | Typed exact recall |
|---|---|---|---|---|---|---|
| ADDRESS | 70 | 70 | 1.000 | 0.000 | 0.000 | 0.000 |
| CA_AB_ULI | 28 | 28 | 1.000 | 1.000 | 0.000 | 1.000 |
| CA_BC_PHN | 22 | 22 | 1.000 | 1.000 | 0.000 | 1.000 |
| CA_OHIP | 27 | 27 | 1.000 | 1.000 | 0.000 | 1.000 |
| CA_RAMQ | 23 | 23 | 1.000 | 1.000 | 0.000 | 1.000 |
| CA_SIN | 30 | 30 | 1.000 | 1.000 | 0.000 | 1.000 |
| DATE | 160 | 160 | 1.000 | 1.000 | 0.000 | 0.988 |
| PERSON | 170 | 163 | 0.959 | 0.818 | 0.041 | 0.559 |
| **TOTAL** | 530 | 523 | 0.987 | 0.809 | 0.013 | 0.723 |

Span precision (predicted spans overlapping any gold PII): 0.821 (821/1000)
Bootstrap 95% CI (1000 note-resamples): leak recall [0.976, 0.996], strict recall [0.788, 0.830], precision [0.799, 0.841]

### Stock Presidio — locale=ca, split=generated

| Entity | Gold | Detected (overlap) | Recall | Strict recall | FN rate | Typed exact recall |
|---|---|---|---|---|---|---|
| ADDRESS | 591 | 589 | 0.997 | 0.000 | 0.003 | 0.000 |
| CA_AB_ULI | 216 | 137 | 0.634 | 0.597 | 0.366 | 0.000 |
| CA_BC_PHN | 226 | 226 | 1.000 | 1.000 | 0.000 | 0.000 |
| CA_OHIP | 220 | 147 | 0.668 | 0.150 | 0.332 | 0.000 |
| CA_RAMQ | 238 | 108 | 0.454 | 0.059 | 0.546 | 0.000 |
| CA_SIN | 311 | 71 | 0.228 | 0.219 | 0.772 | 0.000 |
| DATE | 1520 | 1520 | 1.000 | 0.986 | 0.000 | 0.965 |
| PERSON | 1489 | 1386 | 0.931 | 0.836 | 0.069 | 0.553 |
| **TOTAL** | 4811 | 4184 | 0.870 | 0.668 | 0.130 | 0.476 |

Span precision (predicted spans overlapping any gold PII): 0.756 (5394/7135)
Bootstrap 95% CI (1000 note-resamples): leak recall [0.862, 0.878], strict recall [0.657, 0.679], precision [0.748, 0.764]

### Presidio + pack — locale=ca, split=generated

| Entity | Gold | Detected (overlap) | Recall | Strict recall | FN rate | Typed exact recall |
|---|---|---|---|---|---|---|
| ADDRESS | 591 | 591 | 1.000 | 0.000 | 0.000 | 0.000 |
| CA_AB_ULI | 216 | 216 | 1.000 | 1.000 | 0.000 | 1.000 |
| CA_BC_PHN | 226 | 226 | 1.000 | 1.000 | 0.000 | 1.000 |
| CA_OHIP | 220 | 220 | 1.000 | 1.000 | 0.000 | 1.000 |
| CA_RAMQ | 238 | 238 | 1.000 | 1.000 | 0.000 | 1.000 |
| CA_SIN | 311 | 311 | 1.000 | 1.000 | 0.000 | 1.000 |
| DATE | 1520 | 1520 | 1.000 | 0.986 | 0.000 | 0.965 |
| PERSON | 1489 | 1386 | 0.931 | 0.836 | 0.069 | 0.553 |
| **TOTAL** | 4811 | 4708 | 0.979 | 0.822 | 0.021 | 0.728 |

Span precision (predicted spans overlapping any gold PII): 0.808 (7313/9054)
Bootstrap 95% CI (1000 note-resamples): leak recall [0.975, 0.983], strict recall [0.814, 0.829], precision [0.801, 0.814]

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
