# Core scanner evaluation

Generated: 2026-07-07T04:32:48+00:00 | engine=core.scan

### Core scanner — locale=ca, split=gold

Identifier entities only (framework-neutral core; no spaCy PERSON/DATE).

| Entity | Gold | Detected (overlap) | Recall | Strict recall | FN rate |
|---|---|---|---|---|---|
| CA_AB_ULI | 21 | 0 | 0.000 | 0.000 | 1.000 |
| CA_BC_PHN | 23 | 23 | 1.000 | 1.000 | 0.000 |
| CA_OHIP | 24 | 24 | 1.000 | 1.000 | 0.000 |
| CA_RAMQ | 32 | 32 | 1.000 | 1.000 | 0.000 |
| CA_SIN | 35 | 35 | 1.000 | 1.000 | 0.000 |
| **TOTAL (pack ids)** | 135 | 114 | 0.844 | 0.844 | 0.156 |

Span precision (pack-id predictions only): 0.449 (115/256)
Bootstrap 95% CI (pack ids): leak recall [0.782, 0.901]

### Core scanner — locale=ca, split=generated

Identifier entities only (framework-neutral core; no spaCy PERSON/DATE).

| Entity | Gold | Detected (overlap) | Recall | Strict recall | FN rate |
|---|---|---|---|---|---|
| CA_AB_ULI | 227 | 7 | 0.031 | 0.031 | 0.969 |
| CA_BC_PHN | 226 | 226 | 1.000 | 1.000 | 0.000 |
| CA_OHIP | 224 | 224 | 1.000 | 1.000 | 0.000 |
| CA_RAMQ | 223 | 223 | 1.000 | 1.000 | 0.000 |
| CA_SIN | 302 | 302 | 1.000 | 1.000 | 0.000 |
| **TOTAL (pack ids)** | 1202 | 982 | 0.817 | 0.817 | 0.183 |

Span precision (pack-id predictions only): 0.451 (1004/2228)
Bootstrap 95% CI (pack ids): leak recall [0.796, 0.838]

### Core scanner — locale=in, split=gold

Identifier entities only (framework-neutral core; no spaCy PERSON/DATE).

| Entity | Gold | Detected (overlap) | Recall | Strict recall | FN rate |
|---|---|---|---|---|---|
| IN_AADHAAR | 41 | 41 | 1.000 | 1.000 | 0.000 |
| IN_ABHA | 67 | 39 | 0.582 | 0.448 | 0.418 |
| IN_MOBILE | 74 | 74 | 1.000 | 1.000 | 0.000 |
| IN_PAN | 41 | 41 | 1.000 | 1.000 | 0.000 |
| IN_PASSPORT | 12 | 12 | 1.000 | 1.000 | 0.000 |
| IN_UHID | 59 | 24 | 0.407 | 0.000 | 0.593 |
| IN_VOTER_ID | 13 | 13 | 1.000 | 1.000 | 0.000 |
| **TOTAL (pack ids)** | 307 | 244 | 0.795 | 0.687 | 0.205 |

Span precision (pack-id predictions only): 1.000 (248/248)
Bootstrap 95% CI (pack ids): leak recall [0.751, 0.835]

### Core scanner — locale=in, split=generated

Identifier entities only (framework-neutral core; no spaCy PERSON/DATE).

| Entity | Gold | Detected (overlap) | Recall | Strict recall | FN rate |
|---|---|---|---|---|---|
| IN_AADHAAR | 345 | 345 | 1.000 | 1.000 | 0.000 |
| IN_ABHA | 634 | 445 | 0.702 | 0.479 | 0.298 |
| IN_MOBILE | 592 | 592 | 1.000 | 1.000 | 0.000 |
| IN_PAN | 326 | 326 | 1.000 | 1.000 | 0.000 |
| IN_PASSPORT | 97 | 97 | 1.000 | 1.000 | 0.000 |
| IN_UHID | 574 | 232 | 0.404 | 0.000 | 0.596 |
| IN_VOTER_ID | 90 | 90 | 1.000 | 1.000 | 0.000 |
| **TOTAL (pack ids)** | 2658 | 2127 | 0.800 | 0.660 | 0.200 |

Span precision (pack-id predictions only): 1.000 (2200/2200)
Bootstrap 95% CI (pack ids): leak recall [0.785, 0.815]
