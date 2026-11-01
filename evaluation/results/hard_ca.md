# Adversarial / hard split — Canada

1500 single-identifier notes (50 per entity x variant cell); checksum-valid values rendered in out-of-distribution surface forms. `control` is the in-distribution baseline.

Each cell shows **pack recall** (gold overlapped by a prediction of its own type: the recognizer actually fired) followed by [leak recall / strict recall]. Leak recall counts overlap by ANY recognizer, so on degraded variants it includes incidental masking by DATE_TIME or PHONE_NUMBER; where pack recall is 0.00 the pack's own patterns contributed nothing. CI gates pack recall only.

### Stock Presidio — pack recall [leak recall / strict recall] per entity x variant

| Entity | control | no_context | unusual_separator | line_wrap | ocr_confusable | dictation |
|---|---|---|---|---|---|---|
| CA_AB_ULI | **0.00** [0.86 / 0.76] | **0.00** [0.80 / 0.74] | **0.00** [0.36 / 0.16] | **0.00** [0.48 / 0.00] | **0.00** [0.66 / 0.28] | **0.00** [0.22 / 0.08] |
| CA_BC_PHN | **0.00** [1.00 / 1.00] | **0.00** [1.00 / 1.00] | **0.00** [1.00 / 1.00] | **0.00** [0.34 / 0.00] | **0.00** [0.46 / 0.04] | **0.00** [1.00 / 1.00] |
| CA_OHIP | **0.00** [0.96 / 0.94] | **0.00** [0.88 / 0.84] | **0.00** [0.90 / 0.84] | **0.00** [0.34 / 0.00] | **0.00** [0.40 / 0.00] | **0.00** [0.92 / 0.90] |
| CA_RAMQ | **0.00** [0.74 / 0.16] | **0.00** [0.78 / 0.22] | **0.00** [0.28 / 0.06] | **0.00** [0.76 / 0.04] | **0.00** [0.80 / 0.02] | **0.00** [0.16 / 0.04] |
| CA_SIN | **0.00** [0.04 / 0.02] | **0.00** [0.00 / 0.00] | **0.00** [0.18 / 0.04] | **0.00** [0.04 / 0.00] | **0.00** [0.06 / 0.00] | **0.00** [0.14 / 0.00] |
| **ALL** | **0.00** [0.72 / 0.58] | **0.00** [0.69 / 0.56] | **0.00** [0.54 / 0.42] | **0.00** [0.39 / 0.01] | **0.00** [0.48 / 0.07] | **0.00** [0.49 / 0.40] |

### Presidio + pack — pack recall [leak recall / strict recall] per entity x variant

| Entity | control | no_context | unusual_separator | line_wrap | ocr_confusable | dictation |
|---|---|---|---|---|---|---|
| CA_AB_ULI | **1.00** [1.00 / 1.00] | **0.00** [0.80 / 0.74] | **0.64** [0.98 / 0.74] | **0.00** [0.48 / 0.00] | **0.00** [0.66 / 0.28] | **0.00** [0.22 / 0.08] |
| CA_BC_PHN | **1.00** [1.00 / 1.00] | **1.00** [1.00 / 1.00] | **0.80** [1.00 / 1.00] | **0.00** [1.00 / 0.00] | **0.00** [0.80 / 0.08] | **0.00** [1.00 / 1.00] |
| CA_OHIP | **1.00** [1.00 / 1.00] | **1.00** [1.00 / 1.00] | **0.74** [1.00 / 0.94] | **0.00** [0.34 / 0.00] | **0.00** [0.40 / 0.00] | **0.00** [0.92 / 0.90] |
| CA_RAMQ | **1.00** [1.00 / 1.00] | **1.00** [1.00 / 1.00] | **0.58** [0.88 / 0.64] | **0.00** [0.76 / 0.04] | **0.00** [0.80 / 0.02] | **0.00** [0.16 / 0.04] |
| CA_SIN | **1.00** [1.00 / 1.00] | **1.00** [1.00 / 1.00] | **0.74** [0.90 / 0.78] | **0.00** [0.04 / 0.00] | **0.00** [0.06 / 0.00] | **0.00** [0.14 / 0.00] |
| **ALL** | **1.00** [1.00 / 1.00] | **0.80** [0.96 / 0.95] | **0.70** [0.95 / 0.82] | **0.00** [0.52 / 0.01] | **0.00** [0.54 / 0.08] | **0.00** [0.49 / 0.40] |
