# Core scanner evaluation

Generated: 2026-11-01T00:37:43+00:00 | engine=core.scan

### Core scanner — split=heldout

Pack identifier entities + ADDRESS only (framework-neutral core; no spaCy PERSON/DATE). CA_AB_ULI is context-gated and expected ~0 here.

| Entity | Gold | Leak recall | Strict recall | Pack recall |
|---|---|---|---|---|
| ADDRESS | 42 | 0.905 | 0.667 | 0.714 |
| CA_AB_ULI | 9 | 0.000 | 0.000 | 0.000 |
| CA_BC_PHN | 21 | 1.000 | 1.000 | 1.000 |
| CA_HEALTH_CARD | 42 | 0.024 | 0.024 | 0.000 |
| CA_OHIP | 23 | 1.000 | 0.826 | 1.000 |
| CA_POSTAL_CODE | 34 | 1.000 | 1.000 | 1.000 |
| CA_RAMQ | 18 | 1.000 | 1.000 | 1.000 |
| CA_SIN | 30 | 1.000 | 1.000 | 1.000 |
| **TOTAL (pack ids)** | 219 | 0.753 | 0.689 | 0.712 |

Pack precision (deduplicated): 1.000 (TP 165, FP 0, duplicates 30); over-redaction 0.0 chars/note
Bootstrap 95% CI (pack ids): pack recall [0.652, 0.766]

### Core scanner — split=generated

Pack identifier entities + ADDRESS only (framework-neutral core; no spaCy PERSON/DATE). CA_AB_ULI is context-gated and expected ~0 here.

| Entity | Gold | Leak recall | Strict recall | Pack recall |
|---|---|---|---|---|
| ADDRESS | 364 | 0.984 | 0.802 | 0.857 |
| CA_AB_ULI | 99 | 0.000 | 0.000 | 0.000 |
| CA_BC_PHN | 158 | 1.000 | 1.000 | 1.000 |
| CA_HEALTH_CARD | 409 | 0.042 | 0.042 | 0.000 |
| CA_OHIP | 169 | 1.000 | 0.852 | 1.000 |
| CA_POSTAL_CODE | 271 | 1.000 | 1.000 | 1.000 |
| CA_RAMQ | 161 | 0.950 | 0.950 | 0.950 |
| CA_SIN | 275 | 1.000 | 1.000 | 1.000 |
| **TOTAL (pack ids)** | 1906 | 0.735 | 0.687 | 0.702 |

Pack precision (deduplicated): 1.000 (TP 1401, FP 0, duplicates 334); over-redaction 0.0 chars/note
Bootstrap 95% CI (pack ids): pack recall [0.682, 0.721]
