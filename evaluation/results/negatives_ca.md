# False-positive evaluation — Canadian confusables corpus

300 PII-free notes; every CA_* prediction at threshold >= 0.35 is a false positive. Each FP is attributed to the planted confusable value it overlaps (`source`); `fp_rate` is FPs per planted value of that source.

### pack

Total pack-entity FPs: 254 (84.67 per 100 notes; 109/300 notes affected)

| Source | Planted | FPs | FP rate | FP / 100 notes | By entity | Examples |
|---|---|---|---|---|---|---|
| accession | 120 | 0 | 0.000 | 0.0 | - | - |
| credit_card | 60 | 0 | 0.000 | 0.0 | - | - |
| encounter10 | 60 | 6 | 0.100 | 2.0 | CA_OHIP 6 | `CA_OHIP: 3428565653`; `CA_OHIP: 4126068941`; `CA_OHIP: 1880163892`; `CA_OHIP: 5042613413` |
| fax_compact | 60 | 8 | 0.133 | 2.67 | CA_BC_PHN 2, CA_OHIP 6 | `CA_BC_PHN: 9025550173`; `CA_OHIP: 7095550161`; `CA_OHIP: 6135550116`; `CA_OHIP: 6045550164` |
| mrn10 | 60 | 12 | 0.200 | 4.0 | CA_BC_PHN 1, CA_OHIP 11 | `CA_OHIP: 3801312434`; `CA_BC_PHN: 9912373573`; `CA_OHIP: 2035969522`; `CA_OHIP: 9729941477` |
| order10 | 120 | 10 | 0.083 | 3.33 | CA_BC_PHN 2, CA_OHIP 8 | `CA_OHIP: 7952112105`; `CA_BC_PHN: 9142208961`; `CA_OHIP: 7419505214`; `CA_OHIP: 6201123400` |
| phone_compact | 60 | 6 | 0.100 | 2.0 | CA_OHIP 6 | `CA_OHIP: 3065550125`; `CA_OHIP: 3065550166`; `CA_OHIP: 9025550113`; `CA_OHIP: 6135550181` |
| phone_facility | 60 | 0 | 0.000 | 0.0 | - | - |
| serial9 | 180 | 17 | 0.094 | 5.67 | CA_SIN 17 | `CA_SIN: 422525832`; `CA_SIN: 495 870 685`; `CA_SIN: 684-672-207`; `CA_SIN: 289542557` |
| trap_alberta | 60 | 86 | 1.433 | 28.67 | CA_AB_ULI 60, CA_HEALTH_CARD 21, CA_SIN 5 | `CA_AB_ULI: 396451235`; `CA_AB_ULI: 807398882`; `CA_HEALTH_CARD: 807398882`; `CA_AB_ULI: 032373782` |
| trap_french | 60 | 68 | 1.133 | 22.67 | CA_HEALTH_CARD 60, CA_SIN 8 | `CA_HEALTH_CARD: 507000352`; `CA_HEALTH_CARD: 188284372`; `CA_HEALTH_CARD: 470920900`; `CA_HEALTH_CARD: 766945698` |
| trap_near | 60 | 41 | 0.683 | 13.67 | CA_HEALTH_CARD 36, CA_SIN 5 | `CA_SIN: 667922611`; `CA_HEALTH_CARD: 667922611`; `CA_HEALTH_CARD: 082553333`; `CA_HEALTH_CARD: 943-330-230` |
| us_ssn | 60 | 0 | 0.000 | 0.0 | - | - |
