# Seed variance (Presidio + pack)

1000 notes per locale per seed; seeds: [42, 101, 202].

| Locale | Seed | Gold entities | Leak recall | Strict recall | Precision |
|---|---|---|---|---|---|
| ca | 42 | 5341 | 0.979 | 0.821 | 0.809 |
| ca | 101 | 5337 | 0.984 | 0.823 | 0.813 |
| ca | 202 | 5355 | 0.981 | 0.813 | 0.814 |
| in | 42 | 6264 | 0.968 | 0.914 | 0.796 |
| in | 101 | 6348 | 0.969 | 0.908 | 0.793 |
| in | 202 | 6414 | 0.967 | 0.905 | 0.795 |

- ca recall: min 0.979, max 0.984, spread 0.005
- ca strict_recall: min 0.813, max 0.823, spread 0.010
- ca precision: min 0.809, max 0.814, spread 0.005
- in recall: min 0.967, max 0.969, spread 0.003
- in strict_recall: min 0.905, max 0.914, spread 0.010
- in precision: min 0.793, max 0.796, spread 0.003
