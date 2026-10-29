# pii-detector-ca

Checksum-validated detectors for **Canadian** health and government identifiers, usable standalone or as [Microsoft Presidio](https://microsoft.github.io/presidio/) recognizers, plus a synthetic clinical-text benchmark and evaluation harness.

Most clinical de-identification tooling is built and tested on US identifier formats. Presidio's default registry has no provincial health-card recognizers: an Ontario health number, a Quebec RAMQ number or a BC PHN passes through a stock de-identification pipeline silently. This package closes that gap with deterministic, checksum-backed recognizers that plug into any Presidio `AnalyzerEngine`, or run standalone with no Presidio/spaCy dependency at runtime.

> **Scope.** Canada only. An Indian identifier pack is planned as a separate package (`pii-detector-in`); it is not part of this one.

## Supported entities

| Entity | Identifier | Validation | Benchmark pack recall (generated split) | Spec |
|---|---|---|---|---|
| `CA_SIN` | Social Insurance Number | Luhn checksum; leading digit not 0/8 | 1.000 | [doc](docs/identifiers/ca_sin.md) |
| `CA_OHIP` | Ontario health number (10 digits + version code) | Luhn (mod-10); leading digit 1–9 | 1.000 (lowercase version codes not covered) | [doc](docs/identifiers/ca_ohip.md) |
| `CA_RAMQ` | Quebec health insurance number (NAM) | Structural (name/DOB encoding) | 0.950 (lowercase letter blocks miss by design) | [doc](docs/identifiers/ca_ramq.md) |
| `CA_BC_PHN` | British Columbia Personal Health Number | Mod-11 weighted checksum | 1.000 | [doc](docs/identifiers/ca_bc_phn.md) |
| `CA_AB_ULI` | Alberta Unique Lifetime Identifier | Pattern + Alberta context gated | 1.000 under Alberta wording; 0 without it | [doc](docs/identifiers/ca_ab_uli.md) |
| `CA_HEALTH_CARD` | Other provinces/territories (generic) | Context gated only | 0.822 (no context within 5 tokens → miss) | [doc](docs/identifiers/ca_health_card_generic.md) |
| `CA_POSTAL_CODE` | Canadian postal code | Structural (letter-class rules) | 1.000 | [doc](docs/identifiers/ca_postal_code.md) |
| `CA_STREET_ADDRESS` | Full civic/mailing address | Structural (postal + province anchor) | 0.857 (one-line form 0.99; other renderings mostly 0) | [doc](docs/identifiers/ca_street_address.md) |

"Pack recall" means the recognizer that owns the entity fired on the gold span; it is the number CI gates. Full tables, including leak recall (masked by any recognizer), strict recall, per-surface-form breakdowns, and the false-positive rates per confusable source, are in `evaluation/results/`.

**Relationship to Presidio's own Canadian recognizers.** Presidio ≥ 2.2.363 ships a `CA_SIN` recognizer and ≥ 2.2.365 a `CA_POSTAL_CODE` recognizer, both **disabled by default** in `default_recognizers.yaml`. The six health-card and address entities above have no upstream equivalent. If you enable Presidio's built-ins, skip ours to avoid duplicate detections: `add_recognizers(registry, exclude=["CA_SIN", "CA_POSTAL_CODE"])`. The evaluation reports a "Presidio + CA builtins" baseline so the health-card contribution is measured against the strongest no-pack configuration.

## Install

```bash
pip install pii-detector-ca              # standalone scan(): no dependencies
pip install "pii-detector-ca[presidio]"  # + Presidio recognizers
```

The Presidio integration also needs a spaCy model: `python -m spacy download en_core_web_sm` (see the snippet below for why `sm` is configured explicitly). The standalone `scan()` API needs neither.

From source: `git clone https://github.com/thisiskarthikeyan/pii-detector-ca.git && cd pii-detector-ca && pip install -e ".[presidio]"`.

## Usage

### Standalone detection (no Presidio required at runtime)

```python
from pii_detector_ca import scan

matches = scan("Patient health card 7577 752 616 AB, SIN 123-456-782.", threshold=0.35)
for hit in matches:
    print(hit.entity, hit.start, hit.end, hit.text, hit.score)
```

`scan()` is pattern + validator only — it applies **no context-word boosting**. Checksum/structure-backed entities (`CA_SIN`, `CA_OHIP`, `CA_RAMQ`, `CA_BC_PHN`, `CA_POSTAL_CODE`, `CA_STREET_ADDRESS`) work fully; the context-gated `CA_AB_ULI` and `CA_HEALTH_CARD` never reach the default threshold standalone and need the Presidio integration. Entity rules live in `pii_detector_ca.core` (validators, specs, scanner); the Presidio recognizers are thin adapters over the same specs. See [docs/architecture/core_contract.md](docs/architecture/core_contract.md).

### Presidio integration

```python
from presidio_analyzer import AnalyzerEngine
from presidio_analyzer.nlp_engine import NlpEngineProvider
from pii_detector_ca import add_recognizers

# Same NLP engine as the published evaluation. A bare AnalyzerEngine()
# defaults to en_core_web_lg (~400 MB) and downloads it on first use.
nlp_engine = NlpEngineProvider(nlp_configuration={
    "nlp_engine_name": "spacy",
    "models": [{"lang_code": "en", "model_name": "en_core_web_sm"}],
}).create_engine()

analyzer = AnalyzerEngine(nlp_engine=nlp_engine, supported_languages=["en"])
add_recognizers(analyzer.registry)

results = analyzer.analyze(
    text="Patient health card 7577 752 616 AB, SIN 123-456-782.",
    language="en",
)
for r in results:
    print(r.entity_type, r.start, r.end, round(r.score, 2))
```

A non-technical walkthrough is in [docs/user_manual.md](docs/user_manual.md).

## What this is not

- **Not a compliance guarantee.** Using this package does not by itself satisfy PIPEDA, PHIPA, provincial health-information acts, or any other regulation. It is one detection layer; keep human review and your organization's privacy process in the loop.
- **Not a full de-identifier.** It detects identifiers. Person names, dates, and free-text clues come from Presidio's underlying NLP engine (spaCy), which this package does not improve. Most remaining misses on the benchmark are non-Anglophone person names.
- **Not validated on real clinical text.** All reported numbers come from a synthetic benchmark (below). Real notes carry OCR noise, dictation artifacts, and formats a template generator cannot anticipate.
- **Checksum-valid ≠ real, and the collision floor is not small.** About 8% of random 9-digit strings pass the SIN check and about 9% of random 10-digit strings pass the OHIP check, with no context required. Measured on the negatives corpus: 10% of random 10-digit MRNs, encounter numbers and compact phone numbers are flagged `CA_OHIP` at score 1.0 with no health context (`evaluation/results/negatives_ca.md`, sources `mrn10`, `encounter10`, `phone_compact`). Whether compact 10-digit matches should require context is an open design question, tracked as expected-failure tests in `tests/test_negatives.py`.
- **Context gating has a measured false-positive cost.** Checksumless types (Alberta ULI, generic health cards) rely on context words within Presidio's 5-token window. An innocent 9-digit number inside that window of "health card", "Alberta" or "assurance maladie" is flagged in roughly 70–140% of cases (two recognizers often fire on one span); see the `trap_*` rows in `negatives_ca.md`.
- **No robustness to line wraps, OCR confusables, dictation spacing or digit regrouping.** Pack recall on those hard-split variants is 0.00 (`evaluation/results/hard_ca.md`). Dot and slash separators are matched.
- **French prose is out of scope.** French context words are implemented (and exercised in tests) but the benchmark is English-language clinical prose only.

## Benchmark

`benchmark/` contains a seeded, deterministic generator for synthetic clinical notes (ten note types, from radiology reports to tab-separated registration extracts and unlabelled nursing notes) with span-labeled PII injection. Identifier values are built from independent reference checksums (`benchmark/checksums_ref.py`, pinned to the package validators by `tests/test_oracle.py`), rendered in several surface forms (compact, spaced, dashed, dotted, slashed, mixed, glued or lowercase version codes) and tagged with the form so recall is reported per rendering. It also has a false-positive negatives corpus whose planted numbers are tagged by source (MRNs, encounter numbers, compact phones, context traps inside the enhancer window, and more), an adversarial hard split (50 notes per entity × variant), and a street-address holdout built from the StatCan Open Database of Addresses rendered half in-distribution and half in forms the recognizer was not written against. `evaluation/` compares stock Presidio, Presidio with its own Canadian built-ins enabled, and Presidio + this pack; results are committed under `evaluation/results/`, and `gate_summary.md` there lists every CI floor beside its measured value.

```bash
pip install -e ".[dev]" && pip install -r evaluation/requirements-eval.txt
python benchmark/generate_corpus.py --n 1000
python benchmark/generate_negatives.py --n 300
python benchmark/generate_hard.py --per-cell 50
python benchmark/generate_address_eval.py --n 300
python benchmark/check_determinism.py
python evaluation/run_eval.py --all
python evaluation/run_negatives.py
python evaluation/run_hard.py
python evaluation/run_address_eval.py
python evaluation/check_thresholds.py
```

CI runs this exact sequence in a locked environment (`uv.lock` + pinned spaCy model) and fails on any regression below `evaluation/thresholds.json`. The gate uses **pack recall** (the owning recognizer fired), a per-recognizer prediction-count presence check, deduplicated pack and pipeline precision, an over-redaction ceiling, per-variant pack recall on the hard split, strict recall on the in-distribution address form, and a false-positive ceiling per confusable source. Leak recall is reported but never gated, because it stays at 1.0 even when a recognizer is removed (`tests/test_gate.py` proves this).

**Benchmark caveat:** the templates are written by the same project that wrote the recognizers, so in-distribution recall is still partly circular even with independent checksums and varied renderings. The robust findings are the stock-Presidio gap, the per-form and per-source breakdowns, and the hard, negatives and address-holdout results, most of which are unflattering and are reported as such. The `heldout` split is the first 100 notes of the same generator stream, not an independently annotated set, and has not been human-reviewed. Synthetic data only; no real patient data is used or included. A false-positive run on real de-identified clinical prose is still outstanding (plan item 2.10).

## Contributing, security, citation

- [CONTRIBUTING.md](CONTRIBUTING.md): dev setup and the recipe for adding an identifier.
- [SECURITY.md](SECURITY.md): report missed identifiers (leaks) privately, never with real data.
- [CITATION.cff](CITATION.cff): how to cite this software.
- [CHANGELOG.md](CHANGELOG.md).

## License

MIT. Benchmark data derived from Statistics Canada sources is used under the Open Government Licence – Canada; see the READMEs in `benchmark/data/oda/` and `benchmark/data/statcan_names/`.
