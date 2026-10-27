# Changelog

All notable changes to this project are documented here. The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and the project uses [Semantic Versioning](https://semver.org/).

## [Unreleased]

## [0.1.0] - unreleased

First public release. Canada is the supported locale; India is experimental.

### Added

- Canadian recognizers: `CA_SIN` (Luhn), `CA_OHIP` (Luhn + version code), `CA_RAMQ` (structural), `CA_BC_PHN` (mod-11), `CA_AB_ULI` (context gated), `CA_HEALTH_CARD` (generic, context gated), `CA_POSTAL_CODE`, `CA_STREET_ADDRESS`.
- Experimental Indian recognizers: `IN_AADHAAR` (Verhoeff), `IN_ABHA`, `IN_PAN`, `IN_UHID` (configurable), `IN_MOBILE`, `IN_PIN_CODE`, `IN_VOTER_ID`, `IN_PASSPORT`. Not yet validated to the same standard as Canada.
- Framework-neutral core (`presidio_recognizers_ca_in.core`): stdlib-only validators, entity specs, and a `scan()` API that runs without Presidio or spaCy. Presidio recognizers are thin adapters over the same specs.
- Synthetic clinical-note benchmark: a seeded, deterministic generator with a determinism manifest, a Canadian false-positive negatives corpus, an adversarial hard split, and a street-address holdout derived from the StatCan Open Database of Addresses.
- Evaluation harness: leak-oriented and strict recall, bootstrap 95% CIs, a stock-Presidio baseline (`en_core_web_sm` and `en_core_web_lg`), and a CI threshold gate in a locked environment.
- Provenance docs for every Canadian identifier (`docs/identifiers/`), a core contract doc, and a non-technical user manual.

[Unreleased]: https://github.com/thisiskarthikeyan/pii-detector/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/thisiskarthikeyan/pii-detector/releases/tag/v0.1.0
