# False-positive evaluation — Canadian confusables corpus

300 PII-free notes; every CA_*/IN_* prediction at threshold >= 0.35 is a false positive.

### pack (all locales)

Total pack-entity FPs: 131 (43.67 per 100 notes; 107/300 notes affected)

| Entity | FPs | Example matches |
|---|---|---|
| CA_BC_PHN | 3 | `9466067701`; `9304275177`; `9007387844` |
| CA_OHIP | 16 | `6517396112`; `4543095923`; `7559439455`; `7174956008`; `3757340603` |
| CA_SIN | 19 | `422525832`; `721-441-525`; `690219647`; `167-007-335`; `674-646-294` |
| IN_AADHAAR | 8 | `4800 8495 5006`; `5294 0255 5543`; `5295 0310 5968`; `4751 4230 6924`; `4011 4689 6469` |
| IN_MOBILE | 85 | `7211755002`; `9792171419`; `7286459114`; `8849418478`; `7861973435` |

### pack (ca only)

Total pack-entity FPs: 38 (12.67 per 100 notes; 37/300 notes affected)

| Entity | FPs | Example matches |
|---|---|---|
| CA_BC_PHN | 3 | `9466067701`; `9304275177`; `9007387844` |
| CA_OHIP | 16 | `6517396112`; `4543095923`; `7559439455`; `7174956008`; `3757340603` |
| CA_SIN | 19 | `422525832`; `721-441-525`; `690219647`; `167-007-335`; `674-646-294` |
