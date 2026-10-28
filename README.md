# pii-detector-ca

Checksum-validated [Microsoft Presidio](https://microsoft.github.io/presidio/) recognizers for **Canadian** health and government identifiers, plus a synthetic clinical-text benchmark and evaluation harness.

Most clinical de-identification tooling is built and tested on US identifier formats. Stock Presidio has no concept of an Ontario health card, a Quebec RAMQ number, or a Social Insurance Number, so these pass through a de-identification pipeline silently. This package closes that gap with deterministic, checksum-backed recognizers that plug into any Presidio `AnalyzerEngine`, or run standalone with no Presidio/spaCy dependency at runtime.

> **Scope and status.** Canada is the supported, evaluated locale for 0.1.0. Indian identifier recognizers ship in the package as **experimental** (see [Proposed: India](#proposed-india-experimental)) and have not been through the same evaluation.

## Supported entities (Canada)

| Entity | Identifier | Validation | Spec |
|---|---|---|---|
| `CA_SIN` | Social Insurance Number | Luhn checksum | [doc](docs/identifiers/ca_sin.md) |
| `CA_OHIP` | Ontario health card (10 digits + version code) | Luhn (mod-10) | [doc](docs/identifiers/ca_ohip.md) |
| `CA_RAMQ` | Quebec health insurance number | Structural (name/DOB encoding) | [doc](docs/identifiers/ca_ramq.md) |
| `CA_BC_PHN` | British Columbia Personal Health Number | Mod-11 weighted checksum | [doc](docs/identifiers/ca_bc_phn.md) |
| `CA_AB_ULI` | Alberta Unique Lifetime Identifier | Pattern + context gated | [doc](docs/identifiers/ca_ab_uli.md) |
| `CA_HEALTH_CARD` | Other provinces/territories (generic) | Context gated only | [doc](docs/identifiers/ca_health_card_generic.md) |
| `CA_POSTAL_CODE` | Canadian postal code | Structural (letter-class rules) | [doc](docs/identifiers/ca_postal_code.md) |
| `CA_STREET_ADDRESS` | Full civic/mailing address | Structural (postal + province anchor) | [doc](docs/identifiers/ca_street_address.md) |

## Install

Not yet on PyPI. Install from source:

```bash
git clone https://github.com/thisiskarthikeyan/pii-detector.git
cd pii-detector
pip install -e .
```

The Presidio integration also needs a spaCy model: `python -m spacy download en_core_web_sm` (see the snippet below for why `sm` is configured explicitly). The standalone `scan()` API needs neither.

## Usage

### Standalone detection (no Presidio required at runtime)

```python
from presidio_recognizers_ca_in import scan

matches = scan(
    "Patient health card 7577 752 616 AB, SIN 123-456-782.",
    locales=["ca"],
    threshold=0.35,
)
for hit in matches:
    print(hit.entity, hit.start, hit.end, hit.text, hit.score)
```

Entity rules live in `presidio_recognizers_ca_in.core` (validators, specs, scanner); the Presidio recognizers are thin adapters over the same specs. See [docs/architecture/core_contract.md](docs/architecture/core_contract.md).

### Presidio integration

```python
from presidio_analyzer import AnalyzerEngine
from presidio_analyzer.nlp_engine import NlpEngineProvider
from presidio_recognizers_ca_in import add_recognizers

# Same NLP engine as the published evaluation. A bare AnalyzerEngine()
# defaults to en_core_web_lg (~400 MB) and downloads it on first use.
nlp_engine = NlpEngineProvider(nlp_configuration={
    "nlp_engine_name": "spacy",
    "models": [{"lang_code": "en", "model_name": "en_core_web_sm"}],
}).create_engine()

analyzer = AnalyzerEngine(nlp_engine=nlp_engine, supported_languages=["en"])
add_recognizers(analyzer.registry, locales=["ca"])

results = analyzer.analyze(
    text="Patient health card 7577 752 616 AB, SIN 123-456-782.",
    language="en",
)
for r in results:
    print(r.entity_type, r.start, r.end, round(r.score, 2))
```

**Always pass `locales=["ca"]` for Canadian text.** The default (`locales=None`) currently registers the experimental Indian recognizers too, which adds false positives on Canadian documents (e.g. 10-digit numbers that look like Indian mobile numbers). The default is kept for 0.1.0 so the published evaluation stays reproducible; it may change to Canada-only in a later release.

A non-technical walkthrough is in [docs/user_manual.md](docs/user_manual.md).

## What this is not

- **Not a compliance guarantee.** Using this package does not by itself satisfy PIPEDA, PHIPA, provincial health-information acts, or any other regulation. It is one detection layer; keep human review and your organization's privacy process in the loop.
- **Not a full de-identifier.** It detects identifiers. Person names, dates, and free-text clues come from Presidio's underlying NLP engine (spaCy), which this package does not improve. Most remaining misses on the benchmark are non-Anglophone person names.
- **Not validated on real clinical text.** All reported numbers come from a synthetic benchmark (below). Real notes carry OCR noise, dictation artifacts, and formats a template generator cannot anticipate.
- **Checksum-valid ≠ real.** A string that passes Luhn or mod-11 is likely an identifier, not certainly one, and checksumless types (Alberta ULI, generic health cards) rely on nearby context words.

## Benchmark

`benchmark/` contains a seeded, deterministic generator for synthetic clinical notes (radiology reports, discharge summaries, referral letters, and more) with span-labeled PII injection. It also has a false-positive negatives corpus, an adversarial hard split, and a street-address holdout built from the StatCan Open Database of Addresses. `evaluation/` compares stock Presidio against Presidio + this pack; results are committed under `evaluation/results/`.

```bash
pip install -e ".[dev]" && pip install -r evaluation/requirements-eval.txt
python benchmark/generate_corpus.py --locale ca --n 1000
python benchmark/generate_negatives.py --locale ca --n 300
python benchmark/generate_hard.py --per-cell 10
python benchmark/generate_address_eval.py --n 300
python benchmark/check_determinism.py
python evaluation/run_eval.py --all
python evaluation/run_negatives.py
python evaluation/run_hard.py
python evaluation/run_address_eval.py
python evaluation/check_thresholds.py
```

CI runs this exact sequence in a locked environment (`uv.lock` + pinned spaCy model) and fails on any regression below `evaluation/thresholds.json`.

**Benchmark caveat:** the corpus is generated by the same project that wrote the recognizers, so in-distribution recall is partly circular. The robust findings are the stock-Presidio gap and the results on the negatives, hard, and address-holdout splits. Synthetic data only. No real patient data is used or included.

## Proposed: India (experimental)

The package also contains recognizers for Indian identifiers: `IN_AADHAAR` (Verhoeff), `IN_ABHA`, `IN_PAN`, `IN_UHID` (configurable per facility), `IN_MOBILE`, `IN_PIN_CODE`, `IN_VOTER_ID`, `IN_PASSPORT`. They are usable via `locales=["in"]`, but they are **proposed future work, not a supported feature**: there is no India false-positive corpus, no adversarial split, no gold-split review, and no provenance documentation yet, and India benchmark numbers should be treated as provisional. The validation roadmap is Phase 4 of [IMPLEMENTATION_PLAN.md](IMPLEMENTATION_PLAN.md). Contributions from people with Indian clinical-data expertise are welcome; see [CONTRIBUTING.md](CONTRIBUTING.md).

## Contributing, security, citation

- [CONTRIBUTING.md](CONTRIBUTING.md): dev setup and the recipe for adding an identifier.
- [SECURITY.md](SECURITY.md): report missed identifiers (leaks) privately, never with real data.
- [CITATION.cff](CITATION.cff): how to cite this software.
- [CHANGELOG.md](CHANGELOG.md).

## License

MIT. Benchmark data derived from Statistics Canada sources is used under the Open Government Licence – Canada; see the READMEs in `benchmark/data/oda/` and `benchmark/data/statcan_names/`.
