# Seed variance (Presidio + pack)

1000 notes per locale per seed; seeds: [42, 101, 202].

| Locale | Seed | Gold entities | Leak recall | Strict recall | Precision |
|---|---|---|---|---|---|
| ca | 42 | 5004 | 0.988 | 0.973 | 0.779 |
| ca | 101 | 5020 | 0.987 | 0.970 | 0.771 |
| ca | 202 | 4992 | 0.984 | 0.965 | 0.775 |
| in | 42 | 6264 | 0.968 | 0.914 | 0.796 |
| in | 101 | 6348 | 0.969 | 0.908 | 0.793 |
| in | 202 | 6414 | 0.967 | 0.905 | 0.795 |

- ca recall: min 0.984, max 0.988, spread 0.004
- ca strict_recall: min 0.965, max 0.973, spread 0.007
- ca precision: min 0.771, max 0.779, spread 0.008
- in recall: min 0.967, max 0.969, spread 0.003
- in strict_recall: min 0.905, max 0.914, spread 0.010
- in precision: min 0.793, max 0.796, spread 0.003
