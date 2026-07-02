# Evaluation results

### Stock Presidio — locale=ca, split=gold

| Entity | Gold | Detected (overlap) | Recall | FN rate | Typed exact recall |
|---|---|---|---|---|---|
| ADDRESS | 63 | 63 | 1.000 | 0.000 | 0.000 |
| CA_AB_ULI | 20 | 16 | 0.800 | 0.200 | 0.000 |
| CA_BC_PHN | 20 | 20 | 1.000 | 0.000 | 0.000 |
| CA_OHIP | 30 | 19 | 0.633 | 0.367 | 0.000 |
| CA_RAMQ | 30 | 12 | 0.400 | 0.600 | 0.000 |
| CA_SIN | 35 | 7 | 0.200 | 0.800 | 0.000 |
| DATE | 172 | 172 | 1.000 | 0.000 | 0.959 |
| PERSON | 165 | 155 | 0.939 | 0.061 | 0.521 |
| **TOTAL** | 535 | 464 | 0.867 | 0.133 | 0.469 |

Span precision (predicted spans overlapping any gold PII): 0.748 (590/789)

### Presidio + pack — locale=ca, split=gold

| Entity | Gold | Detected (overlap) | Recall | FN rate | Typed exact recall |
|---|---|---|---|---|---|
| ADDRESS | 63 | 63 | 1.000 | 0.000 | 0.000 |
| CA_AB_ULI | 20 | 20 | 1.000 | 0.000 | 1.000 |
| CA_BC_PHN | 20 | 20 | 1.000 | 0.000 | 1.000 |
| CA_OHIP | 30 | 30 | 1.000 | 0.000 | 1.000 |
| CA_RAMQ | 30 | 30 | 1.000 | 0.000 | 1.000 |
| CA_SIN | 35 | 35 | 1.000 | 0.000 | 1.000 |
| DATE | 172 | 172 | 1.000 | 0.000 | 0.959 |
| PERSON | 165 | 155 | 0.939 | 0.061 | 0.521 |
| **TOTAL** | 535 | 525 | 0.981 | 0.019 | 0.721 |

Span precision (predicted spans overlapping any gold PII): 0.802 (806/1005)

### Stock Presidio — locale=ca, split=generated

| Entity | Gold | Detected (overlap) | Recall | FN rate | Typed exact recall |
|---|---|---|---|---|---|
| ADDRESS | 609 | 607 | 0.997 | 0.003 | 0.000 |
| CA_AB_ULI | 218 | 154 | 0.706 | 0.294 | 0.000 |
| CA_BC_PHN | 240 | 240 | 1.000 | 0.000 | 0.000 |
| CA_OHIP | 215 | 142 | 0.660 | 0.340 | 0.000 |
| CA_RAMQ | 227 | 104 | 0.458 | 0.542 | 0.000 |
| CA_SIN | 331 | 65 | 0.196 | 0.804 | 0.000 |
| DATE | 1522 | 1522 | 1.000 | 0.000 | 0.961 |
| PERSON | 1469 | 1384 | 0.942 | 0.058 | 0.526 |
| **TOTAL** | 4831 | 4218 | 0.873 | 0.127 | 0.463 |

Span precision (predicted spans overlapping any gold PII): 0.754 (5470/7255)

### Presidio + pack — locale=ca, split=generated

| Entity | Gold | Detected (overlap) | Recall | FN rate | Typed exact recall |
|---|---|---|---|---|---|
| ADDRESS | 609 | 609 | 1.000 | 0.000 | 0.000 |
| CA_AB_ULI | 218 | 218 | 1.000 | 0.000 | 1.000 |
| CA_BC_PHN | 240 | 240 | 1.000 | 0.000 | 1.000 |
| CA_OHIP | 215 | 215 | 1.000 | 0.000 | 1.000 |
| CA_RAMQ | 227 | 227 | 1.000 | 0.000 | 1.000 |
| CA_SIN | 331 | 331 | 1.000 | 0.000 | 1.000 |
| DATE | 1522 | 1522 | 1.000 | 0.000 | 0.961 |
| PERSON | 1469 | 1384 | 0.942 | 0.058 | 0.526 |
| **TOTAL** | 4831 | 4746 | 0.982 | 0.018 | 0.717 |

Span precision (predicted spans overlapping any gold PII): 0.809 (7542/9327)

### Stock Presidio — locale=in, split=gold

| Entity | Gold | Detected (overlap) | Recall | FN rate | Typed exact recall |
|---|---|---|---|---|---|
| ADDRESS | 37 | 37 | 1.000 | 0.000 | 0.000 |
| DATE | 137 | 137 | 1.000 | 0.000 | 0.920 |
| IN_AADHAAR | 46 | 36 | 0.783 | 0.217 | 0.000 |
| IN_ABHA | 63 | 37 | 0.587 | 0.413 | 0.000 |
| IN_MOBILE | 71 | 71 | 1.000 | 0.000 | 1.000 |
| IN_PAN | 34 | 3 | 0.088 | 0.912 | 0.000 |
| IN_PASSPORT | 11 | 2 | 0.182 | 0.818 | 0.000 |
| IN_UHID | 66 | 41 | 0.621 | 0.379 | 0.000 |
| IN_VOTER_ID | 17 | 7 | 0.412 | 0.588 | 0.000 |
| PERSON | 163 | 143 | 0.877 | 0.123 | 0.742 |
| **TOTAL** | 645 | 514 | 0.797 | 0.203 | 0.493 |

Span precision (predicted spans overlapping any gold PII): 0.711 (671/944)

### Presidio + pack — locale=in, split=gold

| Entity | Gold | Detected (overlap) | Recall | FN rate | Typed exact recall |
|---|---|---|---|---|---|
| ADDRESS | 37 | 37 | 1.000 | 0.000 | 0.000 |
| DATE | 137 | 137 | 1.000 | 0.000 | 0.920 |
| IN_AADHAAR | 46 | 46 | 1.000 | 0.000 | 1.000 |
| IN_ABHA | 63 | 63 | 1.000 | 0.000 | 1.000 |
| IN_MOBILE | 71 | 71 | 1.000 | 0.000 | 1.000 |
| IN_PAN | 34 | 34 | 1.000 | 0.000 | 1.000 |
| IN_PASSPORT | 11 | 11 | 1.000 | 0.000 | 1.000 |
| IN_UHID | 66 | 66 | 1.000 | 0.000 | 1.000 |
| IN_VOTER_ID | 17 | 17 | 1.000 | 0.000 | 1.000 |
| PERSON | 163 | 143 | 0.877 | 0.123 | 0.742 |
| **TOTAL** | 645 | 625 | 0.969 | 0.031 | 0.860 |

Span precision (predicted spans overlapping any gold PII): 0.790 (1028/1301)

### Stock Presidio — locale=in, split=generated

| Entity | Gold | Detected (overlap) | Recall | FN rate | Typed exact recall |
|---|---|---|---|---|---|
| ADDRESS | 300 | 299 | 0.997 | 0.003 | 0.000 |
| DATE | 1200 | 1200 | 1.000 | 0.000 | 0.889 |
| IN_AADHAAR | 404 | 312 | 0.772 | 0.228 | 0.000 |
| IN_ABHA | 600 | 442 | 0.737 | 0.263 | 0.000 |
| IN_MOBILE | 621 | 621 | 1.000 | 0.000 | 1.000 |
| IN_PAN | 321 | 13 | 0.040 | 0.960 | 0.000 |
| IN_PASSPORT | 101 | 8 | 0.079 | 0.921 | 0.000 |
| IN_UHID | 579 | 363 | 0.627 | 0.373 | 0.000 |
| IN_VOTER_ID | 95 | 31 | 0.326 | 0.674 | 0.000 |
| PERSON | 1500 | 1324 | 0.883 | 0.117 | 0.729 |
| **TOTAL** | 5721 | 4613 | 0.806 | 0.194 | 0.486 |

Span precision (predicted spans overlapping any gold PII): 0.713 (5906/8285)

### Presidio + pack — locale=in, split=generated

| Entity | Gold | Detected (overlap) | Recall | FN rate | Typed exact recall |
|---|---|---|---|---|---|
| ADDRESS | 300 | 299 | 0.997 | 0.003 | 0.000 |
| DATE | 1200 | 1200 | 1.000 | 0.000 | 0.889 |
| IN_AADHAAR | 404 | 404 | 1.000 | 0.000 | 1.000 |
| IN_ABHA | 600 | 600 | 1.000 | 0.000 | 1.000 |
| IN_MOBILE | 621 | 621 | 1.000 | 0.000 | 1.000 |
| IN_PAN | 321 | 321 | 1.000 | 0.000 | 1.000 |
| IN_PASSPORT | 101 | 101 | 1.000 | 0.000 | 1.000 |
| IN_UHID | 579 | 579 | 1.000 | 0.000 | 1.000 |
| IN_VOTER_ID | 95 | 95 | 1.000 | 0.000 | 1.000 |
| PERSON | 1500 | 1324 | 0.883 | 0.117 | 0.729 |
| **TOTAL** | 5721 | 5544 | 0.969 | 0.031 | 0.853 |

Span precision (predicted spans overlapping any gold PII): 0.794 (9156/11535)
