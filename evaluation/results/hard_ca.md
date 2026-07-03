# Adversarial / hard split — Canada

300 single-identifier notes; checksum-valid values rendered in out-of-distribution surface forms. `control` is the in-distribution baseline; degradation from control is the honest robustness number.

Interpretation caveat: leak recall counts overlap by ANY recognizer, so on degraded variants part of the remaining recall is *incidental* masking by built-in recognizers (DATE_TIME / PHONE_NUMBER happening to overlap), not identifier recognition — where the pack and stock rows are identical, the pack's own patterns contributed nothing. Strict recall (in parentheses) shows whether the value was fully covered.

### Stock Presidio — leak recall (strict recall) per entity x variant

| Entity | control | no_context | unusual_separator | line_wrap | ocr_confusable | dictation |
|---|---|---|---|---|---|---|
| CA_AB_ULI | 0.80 (0.70) | 0.80 (0.60) | 0.50 (0.30) | 0.60 (0.00) | 0.60 (0.10) | 0.10 (0.00) |
| CA_BC_PHN | 1.00 (1.00) | 1.00 (1.00) | 1.00 (1.00) | 0.20 (0.00) | 0.10 (0.00) | 1.00 (1.00) |
| CA_OHIP | 0.80 (0.80) | 0.90 (0.90) | 1.00 (1.00) | 0.30 (0.00) | 0.50 (0.00) | 0.90 (0.90) |
| CA_RAMQ | 0.60 (0.10) | 0.90 (0.10) | 0.00 (0.00) | 0.80 (0.10) | 0.70 (0.00) | 0.30 (0.00) |
| CA_SIN | 0.00 (0.00) | 0.00 (0.00) | 0.20 (0.00) | 0.00 (0.00) | 0.00 (0.00) | 0.20 (0.00) |
| **ALL** | **0.64 (0.52)** | **0.72 (0.52)** | **0.54 (0.46)** | **0.38 (0.02)** | **0.38 (0.02)** | **0.50 (0.38)** |

### Presidio + pack — leak recall (strict recall) per entity x variant

| Entity | control | no_context | unusual_separator | line_wrap | ocr_confusable | dictation |
|---|---|---|---|---|---|---|
| CA_AB_ULI | 1.00 (1.00) | 0.80 (0.60) | 0.50 (0.30) | 0.60 (0.00) | 0.60 (0.10) | 0.10 (0.00) |
| CA_BC_PHN | 1.00 (1.00) | 1.00 (1.00) | 1.00 (1.00) | 0.20 (0.00) | 0.10 (0.00) | 1.00 (1.00) |
| CA_OHIP | 1.00 (1.00) | 1.00 (1.00) | 1.00 (1.00) | 0.30 (0.00) | 0.50 (0.00) | 0.90 (0.90) |
| CA_RAMQ | 1.00 (1.00) | 1.00 (1.00) | 0.10 (0.00) | 0.80 (0.10) | 0.70 (0.00) | 0.30 (0.00) |
| CA_SIN | 1.00 (1.00) | 1.00 (1.00) | 0.20 (0.00) | 0.00 (0.00) | 0.00 (0.00) | 0.20 (0.00) |
| **ALL** | **1.00 (1.00)** | **0.96 (0.92)** | **0.56 (0.46)** | **0.38 (0.02)** | **0.38 (0.02)** | **0.50 (0.38)** |
