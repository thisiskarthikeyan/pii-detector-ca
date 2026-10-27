# Changelog

All notable changes to this project are documented here. The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and the project uses [Semantic Versioning](https://semver.org/).

## [Unreleased]

## [0.1.0] - unreleased

First public release, Canada only. (Pre-release history: the package was developed as `presidio-recognizers-ca-in` with experimental Indian recognizers; those were removed before 0.1.0 and will return as a separate `pii-detector-in` package once they have their own benchmark.)

### Added

- Canadian recognizers: `CA_SIN` (Luhn), `CA_OHIP` (Luhn + version code), `CA_RAMQ` (structural), `CA_BC_PHN` (mod-11), `CA_AB_ULI` (context gated), `CA_HEALTH_CARD` (generic, context gated), `CA_POSTAL_CODE`, `CA_STREET_ADDRESS`.
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

[Unreleased]: https://github.com/thisiskarthikeyan/pii-detector/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/thisiskarthikeyan/pii-detector/releases/tag/v0.1.0
