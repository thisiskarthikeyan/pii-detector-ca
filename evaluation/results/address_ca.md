# Street-address evaluation — ODA holdout (Canada)

300 single-address notes from the ODA eval holdout (street names never used by the main benchmark generator). `one_line` is the rendering the CA_STREET_ADDRESS regex was written against; the other forms are out-of-distribution. Strict recall requires the full address span to be fully covered; pack recall requires CA_STREET_ADDRESS itself to overlap it.

### Stock Presidio

ADDRESS leak recall: **0.977** (293/300); strict recall: **0.000** (0/300); pack recall: **0.000**
Pipeline precision: 0.328; pack precision: 0.000; over-redaction 39.4 chars/note
Bootstrap 95% CI strict recall (all forms): [0.0, 0.0]

| Form | Gold | Leak recall | Strict recall | Pack recall |
|---|---|---|---|---|
| apt_suite | 21 | 1.000 | 0.000 | 0.000 |
| no_comma_province | 21 | 0.905 | 0.000 | 0.000 |
| no_postal | 22 | 1.000 | 0.000 | 0.000 |
| one_line (in-distribution, gated) | 150 | 0.967 | 0.000 | 0.000 |
| postal_own_line | 21 | 1.000 | 0.000 | 0.000 |
| province_spelled | 22 | 1.000 | 0.000 | 0.000 |
| rural_route | 21 | 1.000 | 0.000 | 0.000 |
| two_line | 22 | 1.000 | 0.000 | 0.000 |

### Presidio + pack

ADDRESS leak recall: **1.000** (300/300); strict recall: **0.553** (166/300); pack recall: **0.617**
Pipeline precision: 0.333; pack precision: 1.000; over-redaction 39.4 chars/note
Bootstrap 95% CI strict recall (all forms): [0.4967, 0.61]

| Form | Gold | Leak recall | Strict recall | Pack recall |
|---|---|---|---|---|
| apt_suite | 21 | 1.000 | 0.000 | 0.667 |
| no_comma_province | 21 | 1.000 | 0.000 | 0.000 |
| no_postal | 22 | 1.000 | 0.000 | 0.000 |
| one_line (in-distribution, gated) | 150 | 1.000 | 0.967 | 1.000 |
| postal_own_line | 21 | 1.000 | 1.000 | 1.000 |
| province_spelled | 22 | 1.000 | 0.000 | 0.000 |
| rural_route | 21 | 1.000 | 0.000 | 0.000 |
| two_line | 22 | 1.000 | 0.000 | 0.000 |
