# Core detection contract

Framework-neutral identifier detection lives in `presidio_recognizers_ca_in.core`.
Presidio integration is optional and implemented in `presidio_recognizers_ca_in.adapters.presidio`.

## Components

| Module | Role |
|---|---|
| `core/validators.py` | Checksum and structural validation (stdlib only) |
| `core/specs.py` | Entity definitions: patterns, context words, validator binding |
| `core/scanner.py` | `scan()` API — regex + validator, no Presidio/spaCy |
| `adapters/presidio.py` | Builds Presidio `PatternRecognizer` instances from specs |

## Span output (`Match`)

Each detection returns:

- `entity` — e.g. `CA_SIN`, `IN_AADHAAR`
- `start`, `end` — character offsets in the input text
- `text` — matched substring
- `score` — confidence after validator semantics
- `pattern_name` — which regex fired

## Validator semantics

Three-state contract (mirrors Presidio adapter behavior):

| Return | Meaning |
|---|---|
| `True` | Checksum/structure passed → score becomes `MAX_SCORE` (1.0) |
| `False` | Rejected → match discarded |
| `None` | Plausibility-only → keep pattern score (context gating may be required) |

Plausibility validators (`CA_AB_ULI`, `IN_ABHA`) must never return `True`.

## Context words

Context lists are stored on each entity spec for documentation and for future
context-aware scoring. The generic `scan()` API currently performs pattern +
validator detection only (equivalent to Presidio `PatternRecognizer.analyze()`
with `nlp_artifacts=None`). Presidio's engine-level context boosting is not
applied in the core scanner.

## Benchmark contract

Any engine implementing these rules must pass the same deterministic corpora and
threshold gates. Use:

- `python evaluation/run_core_eval.py --all` for core-only identifier metrics
- `python evaluation/run_eval.py --all` for full Presidio + spaCy pipeline

## Adding an entity

1. Add validator (if needed) to `core/validators.py`
2. Add `EntitySpec` entry to `core/specs.py`
3. Add provenance doc under `docs/identifiers/`
4. Add recognizer class as `SpecRecognizer` subclass (Presidio adapter)
5. Extend tests in `tests/test_core_scanner.py` and `tests/test_recognizers.py`
