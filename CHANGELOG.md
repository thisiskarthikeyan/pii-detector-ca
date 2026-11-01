# Changelog

All notable changes to this project are documented here. The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and the project uses [Semantic Versioning](https://semver.org/).

## [Unreleased]

### Changed

- Evaluation gate now enforces **pack recall** (the owning recognizer overlapped the gold span) for identifier entities instead of leak recall, plus a per-recognizer prediction-count presence check; removing a recognizer fails CI (`tests/test_gate.py`). Previously `CA_BC_PHN` and `CA_AB_ULI` passed with their recognizers deleted because built-in recognizers masked the same spans.
- Precision is reported as deduplicated pipeline precision and pack-only precision (CA_* predictions), with duplicate counts and an over-redaction metric (characters masked outside gold spans). The old any-overlap precision counted several predictions on one gold span as several true positives.
- Hard split: 50 notes per entity × variant (was 10); CI gates per-variant pack recall, with measured zeros for line-wrap, OCR and dictation kept as explicit floors of 0.
- Separator class for grouped identifier patterns (SIN, OHIP, BC PHN, Alberta ULI, RAMQ, generic health card) widened from `[- ]` to `[-. /]`.
- Benchmark: identifiers are built from independent reference checksums (`benchmark/checksums_ref.py`) rather than the package validators, pinned by `tests/test_oracle.py`; values are rendered in weighted surface forms (dot, slash, mixed separators, glued/lowercase version codes, lowercase RAMQ) and tagged with `form`; four templates added (Alberta registration, out-of-province intake, unlabelled nursing note, tab-separated registration extract); standalone `CA_POSTAL_CODE`, Alberta-labelled `CA_AB_ULI` and other-province `CA_HEALTH_CARD` gold spans; a ULI-shaped number under generic wording is gold `CA_HEALTH_CARD`; ~20% of benchmark addresses use out-of-distribution renderings. The "gold" split is reported as `heldout` (same file path).
- Negatives corpus: planted numbers are tagged by source (MRN, encounter, compact phone/fax, context traps inside the 5-token window, Alberta and French traps); FP rate is gated per source. Measured: 10% of random 10-digit MRNs are flagged `CA_OHIP`; context traps fire in 68–143% of cases.
- Address holdout: half the notes use forms the recognizer was not written against (two-line, province spelled out, no postal code, Apt/Suite, rural route, no comma before province); strict recall is reported per form and only the one-line form is gated. Measured out-of-distribution strict recall is 0.000 except postal-code-on-own-line.
- `check_thresholds.py` prints measured values beside every floor and writes `evaluation/results/gate_summary.md`.

## [0.1.0] - unreleased

First public release, Canada only. (Pre-release history: the package was developed as `presidio-recognizers-ca-in` with experimental Indian recognizers; those were removed before 0.1.0 and will return as a separate `pii-detector-in` package once they have their own benchmark.)

### Added

- Canadian recognizers: `CA_SIN` (Luhn), `CA_OHIP` (Luhn + version code), `CA_RAMQ` (structural), `CA_BC_PHN` (mod-11), `CA_AB_ULI` (context gated), `CA_HEALTH_CARD` (generic, context gated), `CA_POSTAL_CODE`, `CA_STREET_ADDRESS`.
- `presidio-analyzer` is an optional extra (`pip install pii-detector-ca[presidio]`); the base install has no dependencies.
- Framework-neutral core (`pii_detector_ca.core`): stdlib-only validators, entity specs, and a `scan()` API that runs without Presidio or spaCy. Presidio recognizers are thin adapters over the same specs.
- `add_recognizers(registry, exclude=[...])` / `get_recognizers(exclude=[...])` to skip entities that Presidio's own (default-disabled) `CA_SIN` / `CA_POSTAL_CODE` recognizers already cover.
- Synthetic clinical-note benchmark: a seeded, deterministic generator with a determinism manifest, a false-positive negatives corpus, an adversarial hard split, and a street-address holdout derived from the StatCan Open Database of Addresses.
- Evaluation harness: leak-oriented and strict recall, bootstrap 95% CIs, three baselines (stock Presidio, Presidio with its CA built-ins enabled, Presidio + pack), and a CI threshold gate in a locked environment.
- Provenance docs for every identifier (`docs/identifiers/`), a core contract doc, and a non-technical user manual.

### Changed (pre-release)

- `CA_AB_ULI` now requires Alberta-specific context ("alberta", "uli", "ahcip", "netcare"). A 9-digit number under generic "health card" wording is reported as `CA_HEALTH_CARD` only; the generic recognizer gained separated-form patterns (5-4, 3-3-3, 4-3-3) so those renderings are still covered. ULI typed-exact recall on the benchmark is 0 by design (values are labelled under generic headers); leak recall stays 1.0.
- "card" is not a context token: it boosted credit-card chunks ("payment card on file") by +200 FPs/300 notes on the negatives corpus.
- `evaluation/run_eval.py` reports a third system, "Presidio + CA builtins", and `results_en_core_web_lg.*` are regenerated for the Canada-only corpus.

### Fixed (pre-release)

- `CA_OHIP`: the separated pattern was compiled case-insensitively, so a lowercase English word following the number ("… 897 on file") was absorbed into the span as a bogus version code at score 1.0. Version codes are now matched case-sensitively, and the validator enforces the MOH HCV schema's non-zero first digit.
- `CA_HEALTH_CARD` and the French context terms never fired through Presidio: its lemma context enhancer matches single tokens, and the context lists were multi-word phrases. Single-token context words ("health", "card", "maladie", "msp", "hsn", …) added.
- Core-scanner evaluation counted correct `CA_STREET_ADDRESS` / `CA_POSTAL_CODE` predictions as false positives because `ADDRESS` gold was filtered out; predictions are now type-mapped and `ADDRESS` kept.
- Benchmark realism: dates of birth were drawn from the encounter-date range (including future dates); RAMQ letter blocks did not match the patient named in the note; RAMQ birth years stopped at 1999.

[Unreleased]: https://github.com/thisiskarthikeyan/pii-detector-ca/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/thisiskarthikeyan/pii-detector-ca/releases/tag/v0.1.0
