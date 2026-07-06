# Seed variance (Presidio + pack)

1000 notes per locale per seed; seeds: [42, 101, 202].

| Locale | Seed | Gold entities | Leak recall | Strict recall | Precision |
|---|---|---|---|---|---|
| ca | 42 | 5015 | 0.983 | 0.967 | 0.778 |
| ca | 101 | 5037 | 0.986 | 0.971 | 0.776 |
| ca | 202 | 4986 | 0.985 | 0.968 | 0.776 |
| in | 42 | 6264 | 0.968 | 0.914 | 0.796 |
| in | 101 | 6348 | 0.969 | 0.908 | 0.793 |
| in | 202 | 6414 | 0.967 | 0.905 | 0.795 |

- ca recall: min 0.983, max 0.986, spread 0.003
- ca strict_recall: min 0.967, max 0.971, spread 0.004
- ca precision: min 0.776, max 0.778, spread 0.002
- in recall: min 0.967, max 0.969, spread 0.003
- in strict_recall: min 0.905, max 0.914, spread 0.010
- in precision: min 0.793, max 0.796, spread 0.003
