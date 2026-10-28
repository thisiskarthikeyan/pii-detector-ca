# Contributing

Thanks for helping close the locale gap in clinical de-identification. This project's value is that every detection decision is **auditable and reproducible**, so contributions are held to that bar: sourced rules, deterministic tests, and no regressions on the evaluation gate.

## Ground rules

- **Never commit real patient, customer, or personal data.** That includes in tests, issues, PRs, and screenshots. Use synthetic values that pass the relevant checksum (the generators in `benchmark/pii_generators.py` produce them). `benchmark/data/real/` is gitignored for this reason.
- **Canada only.** Indian identifiers are planned as a separate package (`pii-detector-in`); PRs adding other jurisdictions to this package will be redirected.
- Missed-identifier (leak) findings with real-world impact go through [SECURITY.md](SECURITY.md), not public issues.

## Development setup

Requires Python ≥ 3.10 and [uv](https://docs.astral.sh/uv/).

```bash
uv sync --extra dev   # includes the presidio extra
uv pip install -r evaluation/requirements-eval.txt   # pinned spaCy model, for evaluation
```

Fast checks (run all three before opening a PR; CI runs them on 3.10 and 3.12):

```bash
uv run ruff check .
uv run mypy
uv run pytest -q
```

The full evaluation gate (CI's `eval` job) is the command sequence in the README's *Benchmark* section, ending with `python evaluation/check_thresholds.py`.

## Adding or changing an identifier

Work through these in order. A PR that skips a step will be asked to add it.

1. **Source the rule.** Find the authoritative format and checksum definition (government or issuing-authority publication). If no official source exists, say so explicitly.
2. **Validator.** Add a stdlib-only function to `src/pii_detector_ca/core/validators.py`. Checksumless identifiers must never *boost* a score on plausibility alone: return `False` to reject or `None` to defer to context, never `True` (see `tests/test_recognizers.py` for the regression tests that enforce this).
3. **Entity spec.** Add an `EntitySpec` in `core/specs.py` (patterns, base scores, context words, validator binding, provenance doc path). The core `scan()` API picks it up automatically. Context lists must include **single tokens**: Presidio's lemma context enhancer never matches a multi-word phrase.
4. **Presidio adapter.** Add a thin `SpecRecognizer` subclass in `canada/` and register it in `get_canada_recognizers()`.
5. **Tests.** Positive cases for every surface variant (compact / spaced / dashed), negatives for near-misses and checksum failures, and a property-based test where a checksum exists (`tests/test_properties.py`).
6. **Generator + template slot.** Add a `gen_*` function in `benchmark/pii_generators.py`, wire it into the slot filler in `benchmark/generate_corpus.py`, and place a `("SLOT", "<ENTITY>")` segment in the relevant templates in `benchmark/templates.py`. Generators must take the passed `random.Random` instance, never global `random`, or determinism breaks.
7. **Regenerate and re-pin.** Regenerate the corpora, then run `python benchmark/check_determinism.py --update` and commit the updated `benchmark/data/checksums.json` together with the generator change.
8. **Threshold.** Add a floor for the new entity in `evaluation/thresholds.json`. Checksum-backed identifiers are expected to hold 1.0 recall.
9. **Provenance doc.** Add `docs/identifiers/<entity>.md` (source, implemented rule, known gaps) and a row in `docs/identifiers/README.md`.
10. **Docs.** Update the entity table in `README.md` and `docs/user_manual.md`, and add a `CHANGELOG.md` entry.

## Changing evaluation results

Committed files under `evaluation/results/` back the paper's numbers (manuscript on the `paper` branch). If your change moves them, regenerate them in the locked environment (`uv sync --locked`), commit them in the same PR, and explain the delta in the PR description. Lowering a threshold needs a stated reason. "It failed" is not one.

## Pull requests

- Keep PRs focused; one identifier or one fix per PR.
- Describe *why*, and include before/after numbers when detection behavior changes.
- By contributing you agree your work is released under the project's MIT license.
