# Closing the Locale Gap: Checksum-Validated Recognizers and a Synthetic Benchmark for Canadian and Indian Clinical De-identification

**Draft v0.1 — target: clinical NLP workshop (ClinicalNLP / LOUHI / ML4H); fallback arXiv preprint**

## Abstract

Automated de-identification of clinical text is dominated by tools and models developed for United States identifier formats and HIPAA categories. When applied to clinical documents from other jurisdictions, these systems silently miss national and provincial identifiers — a privacy failure that is invisible precisely because the categories are absent from the tools' training data and rule sets. We present (1) an open-source pack of fifteen checksum-validated recognizers for Canadian and Indian identifiers that plugs into Microsoft Presidio, (2) a reproducible synthetic benchmark of span-labeled clinical notes for both locales, and (3) an evaluation showing that stock Presidio misses 11.5% of PII spans on Canadian clinical notes and 22.2% on Indian ones, which the recognizer pack reduces to 1.3% and 4.1% respectively — with the residual misses concentrated in person-name recognition for non-Anglophone names. Deterministic checksum validation (Luhn, Verhoeff, mod-11) recovers identifier recall to 100% on all covered entity types without machine-learned components, making the approach auditable — a property regulators and privacy officers can verify by reading the code. Code, corpus generator, and evaluation harness are released under the MIT license.

## 1. Introduction

Clinical de-identification research has produced strong results on US corpora (i2b2/n2c2), and modern LLM-based systems report near-perfect F1 on HIPAA's eighteen PHI categories. But the identifier layer of PHI is jurisdiction-specific: a system that recognizes SSNs and US medical record numbers has never seen an Ontario health card version code, a Quebec RAMQ number encoding the holder's name and birth date, or a Verhoeff-validated Aadhaar number. Privacy regulation outside the US — PIPEDA and provincial health information acts in Canada, the Digital Personal Data Protection (DPDP) Act in India — is tightening at the same time as clinical AI adoption accelerates in both countries.

The gap is asymmetric in a dangerous way: false negatives are silent. A de-identification pipeline that has no concept of an ABHA number does not flag its absence; the identifier simply passes through to downstream systems, cloud APIs, or research datasets.

Our contributions:

1. **Recognizer pack.** Fifteen recognizers for Canadian (SIN, OHIP, RAMQ, BC PHN, Alberta ULI, generic provincial health cards, postal codes) and Indian (Aadhaar, ABHA, PAN, UHID, mobile, PIN code, Voter ID/EPIC, passport) identifiers, each combining surface patterns, deterministic validation where a checksum exists, and context-word boosting including non-English context terms (Hindi, French).
2. **Benchmark.** A synthetic, span-labeled corpus of 1,000 clinical notes per locale across three note types (radiology report, discharge summary, referral letter), generated with checksum-valid identifiers in realistic formatting variants. Labels are exact by construction; no manual annotation noise.
3. **Evaluation.** A leak-oriented evaluation protocol and error analysis comparing stock Presidio to Presidio plus the pack, quantifying the locale gap and its closure.

## 2. Related work

De-identification systems span rule-based (MIST, Philter), feature-based ML, neural NER (Clinical-Longformer variants fine-tuned on i2b2/n2c2 and synthetic PII datasets), and recent LLM-based generative approaches with surrogate replacement. Evaluation increasingly attends to clinical information retention (CIRE) alongside recall. Locale-specific tooling exists for Indian *financial* PII (bharat-pii, indian-pii, Armos) with checksum validation of Aadhaar and PAN, but none integrates with a clinical de-identification pipeline or covers health-domain identifiers (ABHA, UHID); to our knowledge no equivalent exists for Canadian health identifiers at all. Microsoft Presidio provides the extensible recognizer architecture we build on; its built-in registry covers US and a small set of international entities but none of the identifiers studied here.

## 3. Identifier landscape and recognizer design

### 3.1 Canada

| Identifier | Format | Integrity check |
|---|---|---|
| SIN | 9 digits | Luhn; leading digit excludes 0/8 |
| Ontario OHIP | 10 digits + 1-2 letter version code | Luhn (mod-10) |
| Quebec RAMQ | 4 letters + 8 digits | Structural: letters from surname, digits encode YYMMDD with +50 month offset for female holders |
| BC PHN | 10 digits, leading 9 | Weighted mod-11 |
| Alberta ULI | 9 digits | None public; context-gated |
| Postal code | A1A 1A1 | Letter-class restrictions |

### 3.2 India

| Identifier | Format | Integrity check |
|---|---|---|
| Aadhaar | 12 digits, leading 2-9 | Verhoeff |
| ABHA | 14 digits | None public; context-gated |
| PAN | AAAHA9999A | Fourth letter encodes holder type |
| UHID | Facility-specific | Configurable pattern (per-facility profile) |
| Mobile | +91 prefix, leading 6-9 | Structural |
| PIN code | 6 digits, leading 1-9 | Context-gated |
| Voter ID (EPIC) | 3 letters + 7 digits | Structural |
| Passport | Letter + 7 digits | Structural |

### 3.3 Design principles

**Checksum as precision lever.** Bare digit patterns are weak evidence (a 9-digit number is usually not a SIN). Each recognizer assigns a low pattern score, then deterministic validation either boosts the match to near-certainty or discards it. This inverts the usual precision/recall tradeoff: patterns can be permissive (high recall across formatting variants — compact, spaced, dashed) because validation restores precision.

**Context gating for checksumless identifiers.** ABHA, Alberta ULI, and PIN codes have no public checksum. Their patterns score below the reporting threshold alone and surface only when context words ("ABHA", "health account", "UHID", "PIN") appear nearby, including Hindi ("आधार") and French ("numéro d'assurance maladie") context terms.

**Auditability.** Every accept/reject decision traces to a regex and an arithmetic check. For compliance review under PIPEDA/PHIPA or the DPDP Act, this is verifiable by code inspection — unlike a neural model's decision surface.

## 4. Benchmark construction

Notes are assembled from templates for three note types per locale, with slots filled by generators that produce checksum-valid identifiers, locale-plausible person names (Indian; English- and French-Canadian including accented characters), addresses, and dates. Spans are recorded at insertion time, so labels are exact by construction; every record is integrity-checked (`text[start:end] == value`). Identifier surface forms rotate across compact/spaced/dashed variants. Each locale yields 1,000 notes (100 held out as a manually reviewable gold split), totalling 11,605 labeled entities. Clinical content (findings, impressions, diagnoses, medications) is drawn from non-PII pools and is never labeled.

The corpus is synthetic by design: no real patient data is used, no data-use agreement is required, and the generator (seeded, deterministic) is released so the corpus can be regenerated, scaled, or extended to new locales.

## 5. Evaluation

### 5.1 Protocol

Primary metric is **leak-oriented recall**: a gold PII span counts as detected if any predicted span of any entity type overlaps it, reflecting the de-identification threat model where masking matters more than type labeling. The complement is the false-negative (leak) rate. Secondary metric is **typed exact match** (exact boundaries plus correct type after mapping Presidio's built-in types). We also report span precision (fraction of predicted spans overlapping any gold PII).

Systems: stock Presidio 2.x (spaCy `en_core_web_sm` NLP engine, score threshold 0.35) and the same engine with the recognizer pack registered. Numbers below are on the gold splits (100 notes/locale); generated-split results (900 notes/locale) agree within 3 points on all totals.

### 5.2 Results

**Canada (gold split, 530 entities):**

| Entity | Stock recall | Pack recall |
|---|---|---|
| CA_SIN | 0.133 | 1.000 |
| CA_OHIP | 0.704 | 1.000 |
| CA_RAMQ | 0.565 | 1.000 |
| CA_BC_PHN | 1.000 | 1.000 |
| CA_AB_ULI | 0.643 | 1.000 |
| PERSON | 0.959 | 0.959 |
| **Total (FN rate)** | **0.885 (11.5%)** | **0.987 (1.3%)** |

**India (gold split, 640 entities):**

| Entity | Stock recall | Pack recall |
|---|---|---|
| IN_AADHAAR | 0.683 | 1.000 |
| IN_ABHA | 0.716 | 1.000 |
| IN_PAN | 0.049 | 1.000 |
| IN_UHID | 0.610 | 1.000 |
| IN_VOTER_ID | 0.154 | 1.000 |
| IN_PASSPORT | 0.083 | 1.000 |
| PERSON | 0.844 | 0.844 |
| **Total (FN rate)** | **0.778 (22.2%)** | **0.959 (4.1%)** |

Where stock Presidio does detect locale identifiers, detection is incidental — a SIN caught because its formatting resembles a US phone number — and typed exact recall for those entities is 0.000 across the board, meaning downstream policies keyed to entity types (e.g., "redact but keep dates") cannot be applied. Span precision rises with the pack (CA 0.773 to 0.821; IN 0.721 to 0.799) because validated identifier matches displace no correct predictions.

### 5.3 Error analysis

Post-pack false negatives are concentrated almost entirely in **person names, which the pack deliberately does not address**: spaCy's NER misses 4.1% of Canadian names and 15.6% of Indian names on the gold splits — e.g., "Manoj Banerjee", "Swati Verma", "Émile Lavoie". The general-NER locale gap for names mirrors the identifier gap and motivates locale-tuned NER or name-gazetteer augmentation as future work. All identifier entity types reach 1.000 recall with the pack on both splits.

This delineates the boundary cleanly: formatted identifiers are the failure class that rule-plus-checksum methods solve completely on this benchmark, while non-Anglophone person names require learned components. One design lesson surfaced during development: identifiers *without* a public checksum (ABHA, Alberta ULI) must not be score-boosted on plausibility alone — validators for these types only reject implausible values and otherwise defer to context-word gating, trading a small amount of recall on context-free mentions for acceptable precision on bare digit strings.

## 6. Limitations

- **Synthetic corpus.** Templates cannot capture the full messiness of real clinical text (OCR noise, dictation artifacts, mixed-language notes). Validation on real, hand-de-identified Canadian and Indian clinical text is ongoing work; the JSONL schema and harness accept such data unchanged.
- **English-only clinical prose.** French-language Quebec notes and Indic-script text are out of scope for this iteration; only context words are multilingual.
- **Name recognition is inherited.** The pack deliberately does not attempt person-name NER; residual leak rate is dominated by the underlying NLP engine's name recognition on non-Anglophone names.
- **Coverage.** Remaining Canadian provinces use a context-gated generic recognizer without per-province validation; Indian UHIDs vary per hospital and require per-facility configuration.

## 7. Conclusion

Locale identifier coverage is a low-cost, high-leverage fix for clinical de-identification outside the US: fifteen deterministic recognizers reduced the PII leak rate by a factor of 8.8 (Canada) and 5.4 (India) on our benchmark, with fully auditable decision logic. We release the pack, the corpus generator, and the evaluation harness to make locale-gap measurement reproducible, and propose the benchmark as a template for extending coverage audits to further jurisdictions.

## Reproducibility

```
uv pip install -e ".[dev]" && python -m spacy download en_core_web_sm
python benchmark/generate_corpus.py --locale ca --n 1000
python benchmark/generate_corpus.py --locale in --n 1000
python evaluation/run_eval.py --all
```

All tables in Section 5 are produced by `evaluation/run_eval.py` (results.md, error_analysis.json).

## References

*To be completed for submission; key anchors:*

- Microsoft Presidio: data protection and de-identification SDK.
- i2b2/n2c2 de-identification challenges (Uzuner et al.; Stubbs et al.).
- "Not What the Doctor Ordered: Surveying LLM-based De-identification and Quantifying Clinical Information Loss" (EMNLP 2025) — CIRE metric.
- Generalizable multilingual medical text anonymization using generative instruction tuning, Communications Medicine (2026).
- bharat-pii, indian-pii: Indian financial PII detection libraries.
- Verhoeff, J. (1969). Error Detecting Decimal Codes.
