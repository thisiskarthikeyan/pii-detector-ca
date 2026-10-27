# Provincial health-card numbers are the Canadian de-identification gap: checksum-validated recognizers and a reproducible benchmark

**Karthikeyan Murugaiah**

Draft v0.2 (2026-10-27). Target: JAMIA Open, *Research and Applications* (≤ 4,000 words, structured abstract ≤ 250 words, 4 tables, 6 figures); fallback arXiv (cs.CL) + ClinicalNLP 2027. Every number below is produced by `evaluation/*.py` from a clean checkout (see Reproducibility) and matches `evaluation/results/` at the commit this draft is attached to.

## Abstract

**Objective.** Clinical de-identification tooling is built around United States identifier formats. We measure how much Canadian identifying information passes through a widely used open-source de-identification engine, and close the gap with deterministic recognizers whose every decision can be audited by reading the code.

**Materials and Methods.** We release `pii-detector-ca`, eight recognizers for Canadian identifiers — Social Insurance Number (SIN), Ontario health number (OHIP), Quebec *numéro d'assurance maladie* (RAMQ), British Columbia Personal Health Number (PHN), Alberta Unique Lifetime Identifier (ULI), a context-gated generic health-card recognizer for the remaining nine jurisdictions, postal codes and civic addresses — each combining a permissive surface pattern with a checksum (Luhn, weighted mod-11) or published structural rule, and running standalone or inside Microsoft Presidio. We also release a seeded, span-labelled synthetic benchmark: 1,000 clinical notes across six note types (5,005 labelled spans) built from Statistics Canada census first names and Open Database of Addresses civic addresses, plus a 300-note false-positive corpus of confusable numerics, a 300-note adversarial split of out-of-distribution surface forms, and a 300-address holdout. Metrics are leak-oriented recall (any overlap), strict recall (full coverage) and span precision with note-level bootstrap 95% CIs.

**Results.** Stock Presidio leaks 13.0% of labelled spans on the held-out split (recall 0.870, 95% CI 0.841–0.897); enabling Presidio's own, default-disabled Canadian SIN and postal-code recognizers reduces this to 8.7%, leaving OHIP (0.692), RAMQ (0.429) and Alberta ULI (0.591) recall unchanged. With the pack, leak rate falls to 1.8% (recall 0.982, CI 0.969–0.992; strict 0.963) and every identifier type reaches 1.000; residual misses are person names. On the false-positive corpus the pack adds 12.3 false positives per 100 notes, all checksum collisions on random digit strings — a floor we quantify at 7.85% (SIN) and 10.29% (OHIP) of random strings. On the adversarial split, recall degrades to 0.60 (unusual separators), 0.54 (line wraps) and 0.48 (OCR confusion, dictation).

**Discussion and Conclusion.** The Canadian gap is a *provincial health-card* gap, not a federal-identifier gap, and checksum validation closes it on well-formed text at a quantifiable precision cost. Results on the adversarial split bound what regex-plus-checksum can do on degraded text. Code, generator, corpus and harness are MIT-licensed.

## Background and significance

De-identification research has produced strong systems for United States clinical text, evaluated on i2b2/n2c2 and oriented to HIPAA's eighteen identifier categories [1,2]. Recent LLM-based systems report near-perfect scores on those benchmarks while also removing clinically necessary content [3]. The identifier layer of protected health information, however, is jurisdiction-specific. A system that recognizes a Social Security Number and a US medical record number has no concept of an Ontario health number with its version code, a Quebec RAMQ number that encodes the holder's surname, birth date and sex, or a British Columbia PHN with its weighted mod-11 check digit.

This failure is silent. A pipeline with no rule for a RAMQ number does not flag its absence; the number passes into downstream systems, cloud APIs and research extracts. Under Ontario's PHIPA, information counts as de-identified only when re-identification risk is "low enough for the circumstances"; a leaked health number is a direct identifier and fails that test outright.

Canadian work exists but is narrow. Tu et al. adapted the PhysioNet *deid* tool to Ontario primary-care records in 2010 [4]. pyDeid, from Unity Health Toronto [5], is the most recent open Canadian system: a rule-based de-identifier evaluated on 700 real admission notes, with regular expressions for SIN, OHIP and postal codes. Reading its source, those rules are pure regular expressions — any 4-3-3 digit group is an OHIP number, any 3-3-3 group a SIN — with no checksum validation and no coverage of Quebec, British Columbia, Alberta or the other provinces. Microsoft Presidio [6], the extensible engine many institutions build on, added a Luhn-validated `CA_SIN` recognizer in version 2.2.363 (June 2026) and a `CA_POSTAL_CODE` recognizer in 2.2.365 (October 2026), both disabled by default; it has no provincial health-card recognizers.

Our contributions:

1. **Eight recognizers for Canadian identifiers** with deterministic validation wherever a public checksum or structure exists, documented against the issuing authority's specification, usable standalone (no NLP dependency) or as Presidio recognizers.
2. **A reproducible synthetic benchmark** that is span-labelled by construction, drawn from real Canadian name and address distributions, and accompanied by three non-circular evaluations: a false-positive corpus, an adversarial surface-form split and an address holdout.
3. **A measurement** that locates the Canadian gap precisely — in provincial health-card numbers — against three baselines including Presidio with its own Canadian recognizers enabled, with bootstrap intervals, seed-variance evidence and a quantified checksum-collision floor.

## Materials and methods

### Identifier landscape and recognizer design

Table 1 lists the identifiers, their published structure and the validation implemented. Each recognizer is a pair of surface patterns (separated form such as `123-456-782`, and compact form) plus a validator. Patterns are deliberately permissive and score below the reporting threshold (0.35); the validator then returns one of three states: *reject* (match discarded), *confirm* (score raised to 1.0) or *abstain* (pattern score kept, context words may raise it). This inverts the usual precision/recall trade-off: the regex can tolerate formatting variation because the checksum restores precision.

**Table 1. Identifiers, structure and validation.**

| Entity | Issuer / source | Structure | Validation |
|---|---|---|---|
| `CA_SIN` | Service Canada | 9 digits | Luhn; first digit ∉ {0, 8} |
| `CA_OHIP` | Ontario MOH (HCV spec) | `[1-9]\d{9}` + 0–2 uppercase version letters | Luhn (mod-10) |
| `CA_RAMQ` | RAMQ | 4 letters (3 surname + initial) + YYMMDD + 2 digits; MM+50 for women | Structural: MM ∈ 01–12 ∪ 51–62, DD ∈ 01–31 |
| `CA_BC_PHN` | BC MoH (HL7 catalogue §3.2) | 10 digits, leading 9 | Weighted mod-11 (2,4,8,5,10,9,7,3) |
| `CA_AB_ULI` | Alberta Health / Netcare | 9 digits, no public check | Abstain; Alberta-specific context only |
| `CA_HEALTH_CARD` | SK, MB, NS, NB, NL, PE, YT, NT, NU | 6–12 digits, 0–2 letters | Abstain; health-card context only |
| `CA_POSTAL_CODE` | Canada Post | `ANA NAN`, letter-class exclusions | Structural (pattern) |
| `CA_STREET_ADDRESS` | Canada Post conventions | civic no. … , municipality, PROV postal | Province code + postal structure |

Two design decisions follow from the three-state validator. First, **identifiers without a public checksum are never confirmed**: the Alberta ULI and the generic health-card validators only reject implausible values (wrong length, a single repeated digit) and otherwise abstain, so a bare nine-digit number is reported only when a context word is nearby. Second, **context attribution is conservative**: a nine-digit number under generic wording ("health card 574839216") is reported as `CA_HEALTH_CARD`, not as an Alberta ULI; the ULI label requires Alberta-specific context ("Alberta", "ULI", "AHCIP", "Netcare"). The benchmark labels ULI values under generic headers, so ULI typed-exact recall is 0 by design while leak recall is 1.0 through the generic recognizer; we report both.

Two implementation details matter for anyone building on Presidio. Its default context enhancer matches context words *one token at a time*, so a context list of phrases ("health card", "numéro d'assurance maladie") never fires; every context list carries single tokens. And Presidio compiles patterns case-insensitively by default, which turned an optional uppercase version-code group into a span-boundary bug — "… 897 **on** file" was absorbed into the OHIP span — found only by probing outside the benchmark; the OHIP and RAMQ patterns are compiled case-sensitively.

Every rule is documented in `docs/identifiers/` with the authoritative source consulted, the exact rule implemented and the gaps between the two (for example, RAMQ publishes no per-month day rule and no check-digit algorithm). Where no official specification is public (the SIN Luhn rule, ULI structure) the document says so.

### Benchmark construction

Notes are assembled from templates for six note types — radiology report, discharge summary, referral letter, emergency-department triage record, internal-medicine consultation (identifiers embedded in running prose) and outpatient laboratory requisition — with slots filled by generators. Spans are recorded at insertion, so labels are exact by construction and every record is integrity-checked (`text[start:end] == value`). Identifier generators emit checksum-valid values in rotating compact/spaced/dashed forms; RAMQ letter blocks are derived from the patient named in the note; dates of birth are drawn from 1930–2015 and encounter dates from 2018–2025.

Name and address distributions are real. First names are sampled frequency-weighted from Statistics Canada's *First names in Canada, 2021 Census* (9,152 names after cleaning, Open Licence), with a 15% accented-name supplement because the census publishes names unaccented. Civic addresses are reservoir-sampled from the Open Database of Addresses (6,000 rows across Alberta, Ontario and Quebec; Open Government Licence – Canada), rendered in English and French civic styles with unit, PO-box and directional variants; postal codes remain synthetic because Canada Post asserts database rights over the real list. Surnames are hand-curated across Anglo, Franco, South and East Asian, Middle Eastern, Eastern European and Indigenous names.

The corpus is 1,000 notes with 5,005 labelled spans (seed 42). The first 100 notes (493 spans) are the held-out *evaluation split*; the remaining 900 (4,512 spans) are the *generated split*. We stress that the evaluation split is the first 100 notes of the same generator stream, not an independently annotated set; a human-review protocol is specified but not yet executed. A SHA-256 manifest pins all corpora, and CI regenerates them from seed and fails on any drift.

Three further corpora are **not** circular with respect to the recognizers:

- **Negatives** (300 notes, zero PII): billing worksheets, laboratory reports and administrative logs dense with Luhn-valid credit cards, US SSNs, random 9- and 10-digit serial and order numbers, ICD-10 codes, laboratory values, vitals, facility telephone numbers and "context traps" — sentences containing identifier context words with no identifier present. Every pack prediction is a false positive.
- **Adversarial split** (300 notes): one checksum-valid identifier per note for each of the five province-specific types, rendered in six variants — control, no context words, unusual separators (dots, slashes, regrouping), line wrap mid-identifier, one OCR-confusable character (0→O, 1→l) and dictation-style character spacing.
- **Address holdout** (300 notes): addresses from a separate 600-row ODA sample never seen by the main generator.

### Evaluation protocol

The primary metric is **leak-oriented recall**: a gold span counts as detected if any predicted span of any type overlaps it, matching the masking threat model. Because a one-character overlap leaves most of an identifier exposed, we also report **strict recall** (the gold span is fully covered by the union of predictions), **typed exact recall** (exact boundaries and correct type after mapping Presidio's built-in labels) and **span precision** (fraction of predictions overlapping any gold PII). Confidence intervals are percentile bootstraps over 1,000 note-level resamples.

Three systems are compared, all with spaCy `en_core_web_sm` 3.8.0 and threshold 0.35: **Stock Presidio** (default registry); **Presidio + CA built-ins** (stock plus Presidio's own `CaSinRecognizer` and `CaPostalCodeRecognizer`, which ship disabled) — the strongest configuration available without this package; and **Presidio + pack**. We repeat the main comparison with `en_core_web_lg`, and report the standalone scanner (no NLP engine) separately. Presidio-analyzer 2.2.363 and all model versions are pinned in `uv.lock`; results files record them.

## Results

### Locale gap and closure

**Table 2. Evaluation split (100 notes, 493 spans), `en_core_web_sm`. Leak recall per entity; totals with 95% CI.**

| Entity | n | Stock Presidio | + CA built-ins | + pack |
|---|---|---|---|---|
| `CA_SIN` | 29 | 0.276 | **1.000** | 1.000 |
| `CA_OHIP` | 26 | 0.692 | 0.692 | **1.000** |
| `CA_RAMQ` | 28 | 0.429 | 0.429 | **1.000** |
| `CA_BC_PHN` | 24 | 1.000 | 1.000 | 1.000 |
| `CA_AB_ULI` | 22 | 0.591 | 0.591 | **1.000** |
| `ADDRESS` (leak / strict) | 65 | 0.985 / 0.000 | 0.985 / 0.000 | 1.000 / **0.923** |
| `PERSON` | 167 | 0.946 | 0.946 | 0.946 |
| `DATE` | 132 | 1.000 | 1.000 | 1.000 |
| **Total leak recall** | 493 | 0.870 [0.841, 0.897] | 0.913 [0.891, 0.935] | **0.982 [0.969, 0.992]** |
| **Total strict recall** | | 0.682 [0.644, 0.716] | 0.724 [0.692, 0.755] | **0.963 [0.946, 0.978]** |
| Leak rate | | 13.0% | 8.7% | **1.8%** |
| Typed exact recall | | 0.495 | 0.554 | 0.832 |
| Span precision | | 0.690 | 0.701 | 0.777 |

The generated split (900 notes, 4,512 spans) agrees: 0.873 → 0.927 → 0.982 leak recall, 0.965 strict with the pack. Across seeds 42, 101 and 202 the pack's leak recall spans 0.982–0.987 (spread 0.005), strict recall 0.965–0.971 and precision 0.780–0.784.

Three observations. First, **enabling Presidio's own Canadian recognizers closes the SIN gap completely and moves nothing else**: the remaining 8.7% leak is OHIP, RAMQ and ULI. The Canadian gap is a provincial health-card gap. Second, where stock Presidio does catch a health number, it is incidental — a RAMQ caught because its digits resemble a date, an OHIP caught as a phone number — and typed exact recall for every Canadian identifier is 0.000 under both baselines, so type-aware policies ("mask identifiers, keep dates") cannot be applied. Third, **strict recall exposes what leak recall hides**: stock Presidio overlaps 98.5% of addresses but fully covers none (spaCy's `LOCATION` masks the municipality; the civic number and street leak on every note), and OHIP strict recall is 0.192 against 0.692 leak.

### Stronger NLP engine

With `en_core_web_lg`, stock leak recall is *lower* (0.844 vs 0.870) because the larger model trades identifier-adjacent `PHONE_NUMBER`/`DATE_TIME` hits for better names; the built-ins baseline reaches 0.901 and the pack 0.996 (strict 0.970), with `PERSON` recall 0.988. Model size does not close the identifier gap; coverage does.

### False positives and the checksum floor

On the 300-note negatives corpus the pack produces 37 false positives (12.3 per 100 notes; 36 notes affected): `CA_SIN` 19, `CA_OHIP` 15, `CA_BC_PHN` 3, all on random 9- and 10-digit serial or order numbers that happen to pass a checksum. Zero false positives arise from Luhn-valid credit cards (the 4-4-4-4 grouping never matches), US SSNs, laboratory values or the context traps. We measured the floor directly: 7.85% of 20,000 random 9-digit strings pass the SIN validator and 10.29% of random 10-digit strings pass the OHIP validator, with no context required. A checksum is roughly 3.3 bits of evidence; compact telephone numbers, medical record numbers and accession numbers in real text will be flagged at about that rate. This is the price of the design and is reported as such.

An earlier iteration of the generic health-card recognizer used "card" as a single-token context word; the negatives corpus immediately exposed it ("Payment **card** on file: 4111 1111 …" → 200 extra false positives) and it was removed. The corpus does the job it was built for.

### Adversarial surface forms

**Table 3. Adversarial split: leak recall (strict recall) by variant, 50 notes per variant.**

| Variant | Stock Presidio | + pack |
|---|---|---|
| control | 0.68 (0.56) | **1.00 (1.00)** |
| no context words | 0.74 (0.58) | **0.96 (0.94)** |
| unusual separator | 0.54 (0.40) | 0.60 (0.40) |
| line wrap | 0.40 (0.00) | 0.54 (0.00) |
| OCR confusable | 0.40 (0.00) | 0.48 (0.02) |
| dictation spacing | 0.48 (0.42) | 0.48 (0.42) |

This is the honest recall number. Checksum-backed types survive the absence of context (SIN, OHIP, RAMQ, BC PHN all 1.00 with no context; ULI 0.80 because it is context-gated by design). Off the separator conventions the generator emits, the pack's own patterns contribute little: on line-wrapped, OCR-corrupted and dictated values the pack and stock rows are nearly identical, and strict recall is ≤ 0.02 — the residual leak recall is incidental overlap from built-in `DATE_TIME`/`PHONE_NUMBER` recognizers. SIN is the most brittle (0.20 on dotted/slashed forms, 0.00 on wraps and OCR); BC PHN the most robust (its compact 10-digit form re-matches after dictation spacing is removed). Closing these gaps is pattern work, not benchmark work.

### Address holdout and standalone scanner

On 300 never-seen ODA addresses, strict recall rises from 0.000 (stock) to 0.950 (pack; 95% CI 0.923–0.970); leak recall from 0.970 to 1.000. The standalone scanner — regex plus validator, no spaCy, no Presidio — reaches 1.000 recall on every checksum- or structure-backed identifier and on addresses (strict 0.908), with span precision 1.000 on the evaluation split; it reports no ULI (0.000) because it applies no context scoring, which is documented as a property of that API.

## Discussion

**Where the gap is.** Against the strongest no-pack baseline, 8.7% of labelled spans still leak, and all of it is OHIP, RAMQ and Alberta ULI. The same is true of pyDeid's coverage [5]: SIN, OHIP and postal codes only, by unvalidated regex. For the ~12 million residents of Quebec, British Columbia and Alberta, no open tool validated a health number before this work. The generic recognizer for the remaining nine jurisdictions is a context-gated net, kept deliberately weak until each province's format is verified against an official source.

**Checksum as evidence, not proof.** The validator design yields 1.000 recall on well-formed identifiers and a quantified false-positive floor. We argue this trade is correct for de-identification, where a false negative is a privacy breach and a false positive is an over-masked serial number, but it should be stated, not hidden: a deployment that processes many bare 9–10-digit quantities will see ~8–10% of them flagged.

**Auditability.** Every accept/reject decision is a regular expression plus an arithmetic check, traceable to a provenance document. For a privacy officer reviewing a pipeline under PHIPA or PIPEDA this is verifiable by inspection, which a neural model's decision surface is not. We do not claim it is sufficient: names, dates and free-text clues remain the NLP engine's problem, and on this benchmark the residual leak is almost entirely non-Anglophone person names.

**Circularity.** The main corpus is generated by the same project that wrote the recognizers; 1.000 in-distribution recall is close to tautological and should be read as an upper bound. The robust findings are (i) the baseline gap, which is independent of our patterns, (ii) the negatives corpus, (iii) the adversarial split, where recall falls to 0.48–0.60, and (iv) the address holdout. We publish the generator so the corpus can be regenerated, rescaled or extended, and the harness accepts any JSONL in the same schema, including real annotated text.

### Limitations

- **No real clinical text.** All numbers are synthetic. Real notes carry OCR noise, dictation artefacts and formats no template anticipates; the adversarial split is a proxy, not a substitute. The evaluation split is not independently annotated.
- **English prose only.** French context terms are implemented and exercised by engine-level tests, but no French-language note corpus exists; Quebec notes are out of scope for this version.
- **Coverage.** Nine jurisdictions share a generic recognizer; the Alberta ULI has no public checksum; RAMQ's final two digits and its day-of-month are unvalidated because RAMQ publishes no rule.
- **No comparison run against pyDeid.** We characterise it from its source; running it on this benchmark is straightforward (its `deid_string` API) and planned.
- **Upstream drift.** Presidio's Canadian coverage changed twice in four months; the built-ins baseline is pinned to 2.2.363 and will need re-running as upstream evolves.

## Conclusion

Measured against Presidio with its own Canadian recognizers enabled, the remaining Canadian de-identification gap is provincial health-card numbers. Eight checksum- and structure-validated recognizers reduce the leak rate on a reproducible synthetic benchmark from 8.7% to 1.8% (13.0% to 1.8% against stock), raise address strict recall from 0.000 to 0.923, and do so with fully inspectable logic and a false-positive floor we quantify rather than hide. The adversarial split shows the limit of the approach on degraded text. The recognizers, generator, corpora and harness are released under the MIT licence as `pii-detector-ca`.

## Reproducibility

From a clean checkout, with Python ≥ 3.10 and `uv`:

```
uv sync --locked --extra dev && uv pip install -r evaluation/requirements-eval.txt
python benchmark/generate_corpus.py --n 1000
python benchmark/generate_negatives.py --n 300
python benchmark/generate_hard.py --per-cell 10
python benchmark/generate_address_eval.py --n 300
python benchmark/check_determinism.py
python evaluation/run_eval.py --all          # Tables 2 (+ generated split)
python evaluation/run_eval.py --all --model en_core_web_lg
python evaluation/run_negatives.py            # false-positive corpus
python evaluation/run_hard.py                 # Table 3
python evaluation/run_address_eval.py         # address holdout
python evaluation/run_core_eval.py --all      # standalone scanner
python evaluation/seed_variance.py            # seeds 42/101/202
python evaluation/check_thresholds.py         # CI regression gate
```

CI runs this sequence on every push in a locked environment and fails on any regression below `evaluation/thresholds.json`.

## Ethics and data statement

No real patient data is used or included. Names and addresses come from Statistics Canada open products under their respective licences; addresses are public civic addresses with no personal association; postal codes are synthetic. Checksum-valid identifiers in the corpus are generated, not issued, and no attempt is made to verify them against any registry. The package is a detection aid and does not by itself satisfy PIPEDA, PHIPA or any provincial statute. Dual-use: the generators produce checksum-valid identifiers, which is also what a tester of a billing system would need; they produce nothing an attacker could not produce from the public checksum definitions.

## References

*Verified anchors; to be formatted for the venue.*

1. Stubbs A, Uzuner Ö. Annotating longitudinal clinical narratives for de-identification: the 2014 i2b2/UTHealth corpus. *J Biomed Inform.* 2015.
2. Norgeot B, et al. Protected Health Information filter (Philter): accurately and securely de-identifying free-text clinical notes. *npj Digit Med.* 2020.
3. Aghakasiri K, Zambare N, Thai J, Ye C, Mehta M, Mitchell JR, Abdalla M. Not What the Doctor Ordered: Surveying LLM-based De-identification and Quantifying Clinical Information Loss. *Proc. EMNLP 2025*, pp. 32187–32203. arXiv:2509.14464.
4. Tu K, et al. De-identification of primary care electronic medical records free-text data in Ontario, Canada. *BMC Med Inform Decis Mak.* 2010;10:35.
5. Sundrelingam V, Parimoo S, Pogacar F, Koppula R, Shin S, Pou-Prom C, Roberts SB, Verma AA, Razak F. pyDeid: an improved, fast, flexible, and generalizable rule-based approach for deidentification of free-text medical records. *JAMIA Open.* 2025;8(1):ooae152.
6. Microsoft Presidio: Data Protection and De-identification SDK. CHANGELOG entries 2.2.363 (2026-06-28, `CA_SIN`) and 2.2.365 (2026-10-25, `CA_POSTAL_CODE`).
7. Ontario Ministry of Health. *Technical Specification for Health Card Validation (HCV) Service via Electronic Business Services*, 2025-10-08; *Health Card Validation Reference Manual*, 2024-10-10.
8. BC Ministry of Health. *Software Compliance Standards, Volume 4 — HL7 Message Catalog*, §3.2 PHN Check Digit Routine.
9. Régie de l'assurance maladie du Québec. *Utilisation de la carte d'assurance maladie*; *Manuel des pharmaciens*, 2025.
10. Statistics Canada. *First names in Canada, 2021 Census* (98-505-X2021007); *Open Database of Addresses*.
11. Employment and Social Development Canada. *The Social Insurance Number Code of Practice*.
