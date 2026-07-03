# presidio-recognizers-ca-in

Checksum-validated [Microsoft Presidio](https://microsoft.github.io/presidio/) recognizers for **Canadian** and **Indian** identifiers, plus a synthetic clinical-text benchmark and evaluation harness.

Most clinical de-identification tooling is trained and tested on US identifier formats. This package closes the locale gap for two underserved regions with deterministic, checksum-backed recognizers that plug directly into any Presidio `AnalyzerEngine`.

## Supported entities

### Canada

| Entity | Identifier | Validation |
|---|---|---|
| `CA_SIN` | Social Insurance Number | Luhn checksum |
| `CA_OHIP` | Ontario health card (10 digits + version code) | Luhn (mod-10) |
| `CA_RAMQ` | Quebec health insurance number | Structural (name/DOB encoding) |
| `CA_BC_PHN` | British Columbia Personal Health Number | Mod-11 weighted checksum |
| `CA_AB_ULI` | Alberta Unique Lifetime Identifier | Pattern + context gated |
| `CA_POSTAL_CODE` | Canadian postal code | Structural (letter-class rules) |
| `CA_STREET_ADDRESS` | Full civic/mailing address | Structural (postal + province anchor) |

### India

| Entity | Identifier | Validation |
|---|---|---|
| `IN_AADHAAR` | Aadhaar number | Verhoeff checksum |
| `IN_ABHA` | Ayushman Bharat Health Account | Pattern + context gated |
| `IN_PAN` | Permanent Account Number | Structural (holder-type letter) |
| `IN_UHID` | Hospital UHID (configurable) | Configurable pattern + context |
| `IN_MOBILE` | Indian mobile number | Structural (+91 / leading 6-9) |
| `IN_PIN_CODE` | Postal PIN code | Pattern + context gated |
| `IN_VOTER_ID` | Voter ID (EPIC) | Structural |
| `IN_PASSPORT` | Indian passport number | Structural |

## Install

```bash
pip install presidio-recognizers-ca-in
```

## Usage

```python
from presidio_analyzer import AnalyzerEngine
from presidio_recognizers_ca_in import add_recognizers

analyzer = AnalyzerEngine()
add_recognizers(analyzer.registry)

results = analyzer.analyze(
    text="Patient health card 9012 345 678 BD, Aadhaar 2345 6789 0123.",
    language="en",
)
```

Or get the recognizer instances directly:

```python
from presidio_recognizers_ca_in import get_recognizers

for rec in get_recognizers():
    print(rec.supported_entities)
```

Per-facility UHID formats (matching hospital-specific MRN schemes):

```python
from presidio_recognizers_ca_in.india import UhidRecognizer

rec = UhidRecognizer(pattern=r"\bAIIMS-\d{8}\b")
```

## Benchmark

`benchmark/` contains a synthetic clinical-note generator (radiology reports, discharge summaries, referral letters) with span-labeled PII injection for both locales, and `evaluation/` contains the harness that compares stock Presidio against Presidio + this pack.

```bash
python benchmark/generate_corpus.py --locale ca --n 1000
python benchmark/generate_corpus.py --locale in --n 1000
python evaluation/run_eval.py --all
```

All numbers in the accompanying paper are reproducible with the commands above. Synthetic data only — no real patient data is used or included.

## License

MIT
