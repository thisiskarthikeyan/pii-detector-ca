# Adversarial / hard split — Canada

300 single-identifier notes; checksum-valid values rendered in out-of-distribution surface forms. `control` is the in-distribution baseline; degradation from control is the honest robustness number.

Interpretation caveat: leak recall counts overlap by ANY recognizer, so on degraded variants part of the remaining recall is *incidental* masking by built-in recognizers (DATE_TIME / PHONE_NUMBER happening to overlap), not identifier recognition — where the pack and stock rows are identical, the pack's own patterns contributed nothing. Strict recall (in parentheses) shows whether the value was fully covered.

### Stock Presidio — leak recall (strict recall) per entity x variant

| Entity | control | no_context | unusual_separator | line_wrap | ocr_confusable | dictation |
|---|---|---|---|---|---|---|
| CA_AB_ULI | 0.90 (0.70) | 0.80 (0.70) | 0.40 (0.20) | 0.50 (0.00) | 0.80 (0.00) | 0.20 (0.20) |
| CA_BC_PHN | 1.00 (1.00) | 1.00 (1.00) | 1.00 (1.00) | 0.30 (0.00) | 0.40 (0.00) | 1.00 (1.00) |
| CA_OHIP | 1.00 (1.00) | 1.00 (1.00) | 0.80 (0.70) | 0.30 (0.00) | 0.20 (0.00) | 0.90 (0.90) |
| CA_RAMQ | 0.50 (0.10) | 0.90 (0.20) | 0.30 (0.10) | 0.90 (0.00) | 0.60 (0.00) | 0.10 (0.00) |
| CA_SIN | 0.00 (0.00) | 0.00 (0.00) | 0.20 (0.00) | 0.00 (0.00) | 0.00 (0.00) | 0.20 (0.00) |
| **ALL** | **0.68 (0.56)** | **0.74 (0.58)** | **0.54 (0.40)** | **0.40 (0.00)** | **0.40 (0.00)** | **0.48 (0.42)** |

### Presidio + pack — leak recall (strict recall) per entity x variant

| Entity | control | no_context | unusual_separator | line_wrap | ocr_confusable | dictation |
|---|---|---|---|---|---|---|
| CA_AB_ULI | 1.00 (1.00) | 0.80 (0.70) | 0.50 (0.20) | 0.50 (0.00) | 0.80 (0.00) | 0.20 (0.20) |
| CA_BC_PHN | 1.00 (1.00) | 1.00 (1.00) | 1.00 (1.00) | 0.30 (0.00) | 0.40 (0.00) | 1.00 (1.00) |
| CA_OHIP | 1.00 (1.00) | 1.00 (1.00) | 0.80 (0.70) | 0.30 (0.00) | 0.20 (0.00) | 0.90 (0.90) |
| CA_RAMQ | 1.00 (1.00) | 1.00 (1.00) | 0.30 (0.10) | 0.90 (0.00) | 0.60 (0.00) | 0.10 (0.00) |
| CA_SIN | 1.00 (1.00) | 1.00 (1.00) | 0.20 (0.00) | 0.00 (0.00) | 0.00 (0.00) | 0.20 (0.00) |
| **ALL** | **1.00 (1.00)** | **0.96 (0.94)** | **0.56 (0.40)** | **0.40 (0.00)** | **0.40 (0.00)** | **0.48 (0.42)** |
