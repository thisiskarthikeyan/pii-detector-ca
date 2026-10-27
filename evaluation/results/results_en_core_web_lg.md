# Evaluation results

Generated: 2026-10-27T03:25:15+00:00 | Python 3.12.3 | presidio-analyzer 2.2.365 | spacy 3.8.18 | en_core_web_lg 3.8.0

### Stock Presidio — split=gold

| Entity | Gold | Detected (overlap) | Recall | Strict recall | FN rate | Typed exact recall |
|---|---|---|---|---|---|---|
| ADDRESS | 65 | 63 | 0.969 | 0.000 | 0.031 | 0.000 |
| CA_AB_ULI | 22 | 7 | 0.318 | 0.318 | 0.682 | 0.000 |
| CA_BC_PHN | 24 | 24 | 1.000 | 1.000 | 0.000 | 0.000 |
| CA_OHIP | 26 | 18 | 0.692 | 0.269 | 0.308 | 0.000 |
| CA_RAMQ | 28 | 6 | 0.214 | 0.036 | 0.786 | 0.000 |
| CA_SIN | 29 | 1 | 0.034 | 0.034 | 0.966 | 0.000 |
| DATE | 132 | 132 | 1.000 | 0.947 | 0.000 | 0.939 |
| PERSON | 167 | 165 | 0.988 | 0.976 | 0.012 | 0.892 |
| **TOTAL** | 493 | 416 | 0.844 | 0.665 | 0.156 | 0.554 |

Span precision (predicted spans overlapping any gold PII): 0.703 (521/741)
Bootstrap 95% CI (1000 note-resamples): leak recall [0.817, 0.872], strict recall [0.632, 0.697], precision [0.679, 0.730]

### Presidio + CA builtins — split=gold

| Entity | Gold | Detected (overlap) | Recall | Strict recall | FN rate | Typed exact recall |
|---|---|---|---|---|---|---|
| ADDRESS | 65 | 63 | 0.969 | 0.000 | 0.031 | 0.000 |
| CA_AB_ULI | 22 | 7 | 0.318 | 0.318 | 0.682 | 0.000 |
| CA_BC_PHN | 24 | 24 | 1.000 | 1.000 | 0.000 | 0.000 |
| CA_OHIP | 26 | 18 | 0.692 | 0.269 | 0.308 | 0.000 |
| CA_RAMQ | 28 | 6 | 0.214 | 0.036 | 0.786 | 0.000 |
| CA_SIN | 29 | 29 | 1.000 | 1.000 | 0.000 | 1.000 |
| DATE | 132 | 132 | 1.000 | 0.947 | 0.000 | 0.939 |
| PERSON | 167 | 165 | 0.988 | 0.976 | 0.012 | 0.892 |
| **TOTAL** | 493 | 444 | 0.901 | 0.722 | 0.099 | 0.613 |

Span precision (predicted spans overlapping any gold PII): 0.714 (550/770)
Bootstrap 95% CI (1000 note-resamples): leak recall [0.878, 0.925], strict recall [0.695, 0.750], precision [0.692, 0.740]

### Presidio + pack — split=gold

| Entity | Gold | Detected (overlap) | Recall | Strict recall | FN rate | Typed exact recall |
|---|---|---|---|---|---|---|
| ADDRESS | 65 | 65 | 1.000 | 0.938 | 0.000 | 0.908 |
| CA_AB_ULI | 22 | 22 | 1.000 | 1.000 | 0.000 | 0.000 |
| CA_BC_PHN | 24 | 24 | 1.000 | 1.000 | 0.000 | 1.000 |
| CA_OHIP | 26 | 26 | 1.000 | 1.000 | 0.000 | 1.000 |
| CA_RAMQ | 28 | 28 | 1.000 | 1.000 | 0.000 | 1.000 |
| CA_SIN | 29 | 29 | 1.000 | 1.000 | 0.000 | 1.000 |
| DATE | 132 | 132 | 1.000 | 0.947 | 0.000 | 0.939 |
| PERSON | 167 | 165 | 0.988 | 0.976 | 0.012 | 0.892 |
| **TOTAL** | 493 | 491 | 0.996 | 0.970 | 0.004 | 0.890 |

Span precision (predicted spans overlapping any gold PII): 0.791 (834/1054)
Bootstrap 95% CI (1000 note-resamples): leak recall [0.990, 1.000], strict recall [0.955, 0.982], precision [0.774, 0.811]

### Stock Presidio — split=generated

| Entity | Gold | Detected (overlap) | Recall | Strict recall | FN rate | Typed exact recall |
|---|---|---|---|---|---|---|
| ADDRESS | 637 | 628 | 0.986 | 0.000 | 0.014 | 0.000 |
| CA_AB_ULI | 255 | 85 | 0.333 | 0.314 | 0.667 | 0.000 |
| CA_BC_PHN | 209 | 209 | 1.000 | 1.000 | 0.000 | 0.000 |
| CA_OHIP | 205 | 133 | 0.649 | 0.171 | 0.351 | 0.000 |
| CA_RAMQ | 231 | 77 | 0.333 | 0.095 | 0.667 | 0.000 |
| CA_SIN | 313 | 13 | 0.042 | 0.035 | 0.958 | 0.000 |
| DATE | 1178 | 1178 | 1.000 | 0.950 | 0.000 | 0.940 |
| PERSON | 1484 | 1454 | 0.980 | 0.975 | 0.020 | 0.869 |
| **TOTAL** | 4512 | 3777 | 0.837 | 0.648 | 0.163 | 0.531 |

Span precision (predicted spans overlapping any gold PII): 0.702 (4732/6740)
Bootstrap 95% CI (1000 note-resamples): leak recall [0.828, 0.846], strict recall [0.637, 0.659], precision [0.695, 0.709]

### Presidio + CA builtins — split=generated

| Entity | Gold | Detected (overlap) | Recall | Strict recall | FN rate | Typed exact recall |
|---|---|---|---|---|---|---|
| ADDRESS | 637 | 628 | 0.986 | 0.000 | 0.014 | 0.000 |
| CA_AB_ULI | 255 | 85 | 0.333 | 0.314 | 0.667 | 0.000 |
| CA_BC_PHN | 209 | 209 | 1.000 | 1.000 | 0.000 | 0.000 |
| CA_OHIP | 205 | 133 | 0.649 | 0.171 | 0.351 | 0.000 |
| CA_RAMQ | 231 | 77 | 0.333 | 0.095 | 0.667 | 0.000 |
| CA_SIN | 313 | 313 | 1.000 | 1.000 | 0.000 | 1.000 |
| DATE | 1178 | 1178 | 1.000 | 0.950 | 0.000 | 0.940 |
| PERSON | 1484 | 1454 | 0.980 | 0.975 | 0.020 | 0.869 |
| **TOTAL** | 4512 | 4077 | 0.904 | 0.715 | 0.096 | 0.600 |

Span precision (predicted spans overlapping any gold PII): 0.715 (5045/7053)
Bootstrap 95% CI (1000 note-resamples): leak recall [0.896, 0.910], strict recall [0.706, 0.723], precision [0.708, 0.722]

### Presidio + pack — split=generated

| Entity | Gold | Detected (overlap) | Recall | Strict recall | FN rate | Typed exact recall |
|---|---|---|---|---|---|---|
| ADDRESS | 637 | 637 | 1.000 | 0.948 | 0.000 | 0.937 |
| CA_AB_ULI | 255 | 255 | 1.000 | 1.000 | 0.000 | 0.016 |
| CA_BC_PHN | 209 | 209 | 1.000 | 1.000 | 0.000 | 1.000 |
| CA_OHIP | 205 | 205 | 1.000 | 1.000 | 0.000 | 1.000 |
| CA_RAMQ | 231 | 231 | 1.000 | 1.000 | 0.000 | 1.000 |
| CA_SIN | 313 | 313 | 1.000 | 1.000 | 0.000 | 1.000 |
| DATE | 1178 | 1178 | 1.000 | 0.950 | 0.000 | 0.940 |
| PERSON | 1484 | 1454 | 0.980 | 0.975 | 0.020 | 0.869 |
| **TOTAL** | 4512 | 4482 | 0.993 | 0.971 | 0.007 | 0.877 |

Span precision (predicted spans overlapping any gold PII): 0.794 (7728/9736)
Bootstrap 95% CI (1000 note-resamples): leak recall [0.991, 0.996], strict recall [0.967, 0.976], precision [0.788, 0.799]
