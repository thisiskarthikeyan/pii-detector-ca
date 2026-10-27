# Evaluation results

Generated: 2026-10-27T03:06:32+00:00 | Python 3.12.3 | presidio-analyzer 2.2.365 | spacy 3.8.18 | en_core_web_sm 3.8.0

### Stock Presidio — split=gold

| Entity | Gold | Detected (overlap) | Recall | Strict recall | FN rate | Typed exact recall |
|---|---|---|---|---|---|---|
| ADDRESS | 65 | 64 | 0.985 | 0.000 | 0.015 | 0.000 |
| CA_AB_ULI | 22 | 13 | 0.591 | 0.545 | 0.409 | 0.000 |
| CA_BC_PHN | 24 | 24 | 1.000 | 1.000 | 0.000 | 0.000 |
| CA_OHIP | 26 | 18 | 0.692 | 0.192 | 0.308 | 0.000 |
| CA_RAMQ | 28 | 12 | 0.429 | 0.036 | 0.571 | 0.000 |
| CA_SIN | 29 | 8 | 0.276 | 0.276 | 0.724 | 0.000 |
| DATE | 132 | 132 | 1.000 | 0.985 | 0.000 | 0.955 |
| PERSON | 167 | 158 | 0.946 | 0.934 | 0.054 | 0.707 |
| **TOTAL** | 493 | 429 | 0.870 | 0.682 | 0.130 | 0.495 |

Span precision (predicted spans overlapping any gold PII): 0.690 (549/796)
Bootstrap 95% CI (1000 note-resamples): leak recall [0.841, 0.897], strict recall [0.644, 0.716], precision [0.667, 0.713]

### Presidio + CA builtins — split=gold

| Entity | Gold | Detected (overlap) | Recall | Strict recall | FN rate | Typed exact recall |
|---|---|---|---|---|---|---|
| ADDRESS | 65 | 64 | 0.985 | 0.000 | 0.015 | 0.000 |
| CA_AB_ULI | 22 | 13 | 0.591 | 0.545 | 0.409 | 0.000 |
| CA_BC_PHN | 24 | 24 | 1.000 | 1.000 | 0.000 | 0.000 |
| CA_OHIP | 26 | 18 | 0.692 | 0.192 | 0.308 | 0.000 |
| CA_RAMQ | 28 | 12 | 0.429 | 0.036 | 0.571 | 0.000 |
| CA_SIN | 29 | 29 | 1.000 | 1.000 | 0.000 | 1.000 |
| DATE | 132 | 132 | 1.000 | 0.985 | 0.000 | 0.955 |
| PERSON | 167 | 158 | 0.946 | 0.934 | 0.054 | 0.707 |
| **TOTAL** | 493 | 450 | 0.913 | 0.724 | 0.087 | 0.554 |

Span precision (predicted spans overlapping any gold PII): 0.701 (578/825)
Bootstrap 95% CI (1000 note-resamples): leak recall [0.891, 0.935], strict recall [0.692, 0.755], precision [0.679, 0.724]

### Presidio + pack — split=gold

| Entity | Gold | Detected (overlap) | Recall | Strict recall | FN rate | Typed exact recall |
|---|---|---|---|---|---|---|
| ADDRESS | 65 | 65 | 1.000 | 0.923 | 0.000 | 0.908 |
| CA_AB_ULI | 22 | 22 | 1.000 | 1.000 | 0.000 | 1.000 |
| CA_BC_PHN | 24 | 24 | 1.000 | 1.000 | 0.000 | 1.000 |
| CA_OHIP | 26 | 26 | 1.000 | 1.000 | 0.000 | 1.000 |
| CA_RAMQ | 28 | 28 | 1.000 | 1.000 | 0.000 | 1.000 |
| CA_SIN | 29 | 29 | 1.000 | 1.000 | 0.000 | 1.000 |
| DATE | 132 | 132 | 1.000 | 0.985 | 0.000 | 0.955 |
| PERSON | 167 | 158 | 0.946 | 0.934 | 0.054 | 0.707 |
| **TOTAL** | 493 | 484 | 0.982 | 0.963 | 0.018 | 0.876 |

Span precision (predicted spans overlapping any gold PII): 0.770 (826/1073)
Bootstrap 95% CI (1000 note-resamples): leak recall [0.969, 0.992], strict recall [0.946, 0.978], precision [0.751, 0.789]

### Stock Presidio — split=generated

| Entity | Gold | Detected (overlap) | Recall | Strict recall | FN rate | Typed exact recall |
|---|---|---|---|---|---|---|
| ADDRESS | 637 | 629 | 0.987 | 0.000 | 0.013 | 0.000 |
| CA_AB_ULI | 255 | 183 | 0.718 | 0.678 | 0.282 | 0.000 |
| CA_BC_PHN | 209 | 209 | 1.000 | 1.000 | 0.000 | 0.000 |
| CA_OHIP | 205 | 136 | 0.663 | 0.141 | 0.337 | 0.000 |
| CA_RAMQ | 231 | 131 | 0.567 | 0.061 | 0.433 | 0.000 |
| CA_SIN | 313 | 68 | 0.217 | 0.204 | 0.783 | 0.000 |
| DATE | 1178 | 1178 | 1.000 | 0.986 | 0.000 | 0.949 |
| PERSON | 1484 | 1403 | 0.945 | 0.928 | 0.055 | 0.683 |
| **TOTAL** | 4512 | 3937 | 0.873 | 0.671 | 0.127 | 0.472 |

Span precision (predicted spans overlapping any gold PII): 0.696 (4995/7181)
Bootstrap 95% CI (1000 note-resamples): leak recall [0.864, 0.881], strict recall [0.661, 0.682], precision [0.688, 0.704]

### Presidio + CA builtins — split=generated

| Entity | Gold | Detected (overlap) | Recall | Strict recall | FN rate | Typed exact recall |
|---|---|---|---|---|---|---|
| ADDRESS | 637 | 629 | 0.987 | 0.000 | 0.013 | 0.000 |
| CA_AB_ULI | 255 | 183 | 0.718 | 0.678 | 0.282 | 0.000 |
| CA_BC_PHN | 209 | 209 | 1.000 | 1.000 | 0.000 | 0.000 |
| CA_OHIP | 205 | 136 | 0.663 | 0.141 | 0.337 | 0.000 |
| CA_RAMQ | 231 | 131 | 0.567 | 0.061 | 0.433 | 0.000 |
| CA_SIN | 313 | 313 | 1.000 | 1.000 | 0.000 | 1.000 |
| DATE | 1178 | 1178 | 1.000 | 0.986 | 0.000 | 0.949 |
| PERSON | 1484 | 1403 | 0.945 | 0.928 | 0.055 | 0.683 |
| **TOTAL** | 4512 | 4182 | 0.927 | 0.726 | 0.073 | 0.542 |

Span precision (predicted spans overlapping any gold PII): 0.708 (5308/7494)
Bootstrap 95% CI (1000 note-resamples): leak recall [0.920, 0.934], strict recall [0.717, 0.735], precision [0.700, 0.716]

### Presidio + pack — split=generated

| Entity | Gold | Detected (overlap) | Recall | Strict recall | FN rate | Typed exact recall |
|---|---|---|---|---|---|---|
| ADDRESS | 637 | 637 | 1.000 | 0.945 | 0.000 | 0.937 |
| CA_AB_ULI | 255 | 255 | 1.000 | 1.000 | 0.000 | 1.000 |
| CA_BC_PHN | 209 | 209 | 1.000 | 1.000 | 0.000 | 1.000 |
| CA_OHIP | 205 | 205 | 1.000 | 1.000 | 0.000 | 1.000 |
| CA_RAMQ | 231 | 231 | 1.000 | 1.000 | 0.000 | 1.000 |
| CA_SIN | 313 | 313 | 1.000 | 1.000 | 0.000 | 1.000 |
| DATE | 1178 | 1178 | 1.000 | 0.986 | 0.000 | 0.949 |
| PERSON | 1484 | 1403 | 0.945 | 0.928 | 0.055 | 0.683 |
| **TOTAL** | 4512 | 4431 | 0.982 | 0.965 | 0.018 | 0.873 |

Span precision (predicted spans overlapping any gold PII): 0.778 (7673/9859)
Bootstrap 95% CI (1000 note-resamples): leak recall [0.978, 0.986], strict recall [0.960, 0.970], precision [0.772, 0.785]
