# Core scanner evaluation

Generated: 2026-10-27T03:07:42+00:00 | engine=core.scan

### Core scanner — split=gold

Pack identifier entities + ADDRESS only (framework-neutral core; no spaCy PERSON/DATE). CA_AB_ULI is context-gated and expected ~0 here.

| Entity | Gold | Detected (overlap) | Recall | Strict recall | FN rate |
|---|---|---|---|---|---|
| ADDRESS | 65 | 65 | 1.000 | 0.908 | 0.000 |
| CA_AB_ULI | 22 | 0 | 0.000 | 0.000 | 1.000 |
| CA_BC_PHN | 24 | 24 | 1.000 | 1.000 | 0.000 |
| CA_OHIP | 26 | 26 | 1.000 | 1.000 | 0.000 |
| CA_RAMQ | 28 | 28 | 1.000 | 1.000 | 0.000 |
| CA_SIN | 29 | 29 | 1.000 | 1.000 | 0.000 |
| **TOTAL (pack ids)** | 194 | 172 | 0.887 | 0.856 | 0.113 |

Span precision (pack-id predictions only): 1.000 (238/238)
Bootstrap 95% CI (pack ids): leak recall [0.840, 0.927]

### Core scanner — split=generated

Pack identifier entities + ADDRESS only (framework-neutral core; no spaCy PERSON/DATE). CA_AB_ULI is context-gated and expected ~0 here.

| Entity | Gold | Detected (overlap) | Recall | Strict recall | FN rate |
|---|---|---|---|---|---|
| ADDRESS | 637 | 637 | 1.000 | 0.937 | 0.000 |
| CA_AB_ULI | 255 | 10 | 0.039 | 0.039 | 0.961 |
| CA_BC_PHN | 209 | 209 | 1.000 | 1.000 | 0.000 |
| CA_OHIP | 205 | 205 | 1.000 | 1.000 | 0.000 |
| CA_RAMQ | 231 | 231 | 1.000 | 1.000 | 0.000 |
| CA_SIN | 313 | 313 | 1.000 | 1.000 | 0.000 |
| **TOTAL (pack ids)** | 1850 | 1605 | 0.868 | 0.846 | 0.132 |

Span precision (pack-id predictions only): 1.000 (2252/2252)
Bootstrap 95% CI (pack ids): leak recall [0.854, 0.882]
