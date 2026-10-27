# Implementation Plan

Roadmap to a credible validation process, an open-source release, and a submittable paper.

**Scope decision (2026-10-27): this package is Canada only.** The experimental Indian
recognizers were removed from the package and the repository (`git log` before
2026-10-27 has them); India is to become a *separate* package, `pii-detector-in`,
with its own benchmark, when that work is funded. Phase 4 below is kept as the
specification for that future package and nothing in it is scheduled.

**Upstream change that reframes the paper (2026-10-27):** Presidio 2.2.363
(2026-06-28) added a Luhn-validated `CA_SIN` recognizer and 2.2.365 (2026-10-25) a
`CA_POSTAL_CODE` recognizer, both `enabled: false` by default. The package's
contribution is therefore the provincial health-card layer, the street-address
recognizer and the benchmark/evaluation methodology — not SIN/postal-code
detection. `run_eval.py` now reports a "Presidio + CA builtins" baseline.

Each item is a checkbox so this file doubles as a progress tracker.

---

## Phase 1 — Correctness fixes (COMPLETE)

**Status: COMPLETE (2026-07-02).** All items done; 42 tests pass, ruff clean, full
eval re-run. Post-fix headline numbers: stock Presidio FN rate 11.5% (CA) / 22.2% (IN)
→ pack 1.3% / 4.1% on gold splits; all identifier types at 1.000 pack recall; residual
misses are PERSON names only. Extra fix discovered during 1.4: Presidio's lemma-based
context enhancer matches single tokens only, so multi-word context phrases
("health card") never fired for the ULI recognizer — added single-token context words
("health", "card", "uli"), restoring ULI recall to 1.000 under honest gating.

- [x] **1.1 Fix context-gating bypass for checksumless identifiers** — plausibility
  validators (`ca_ab_uli_plausible`, `in_abha_plausible`) now return None/False (never
  True), so matches keep their pattern score and context gating governs; three-state
  contract documented in `base.py`; regression tests added.
- [x] **1.2 Remove dead `boost_score` parameter** — removed; docstring fixed.
- [x] **1.3 Fix `gen_ca_sin` first-digit typo** — leading digit drawn uniformly from
  "12345679"; redundant retry loop removed.
- [x] **1.4 Re-run full evaluation** — corpus regenerated, `results.md` and
  `error_analysis.json` updated.
- [x] **1.5 Reconcile paper numbers with results files** — abstract, §4 entity count
  (11,605), §5.1 split-agreement claim, §5.2 tables, precision figures, §5.3 error
  analysis (stale RAMQ paragraph replaced with gating design lesson), conclusion
  factors (8.8× CA, 5.4× IN).

## Phase 2 — Shared validation infrastructure (locale-agnostic, do once)

Applies to both locales; build before deepening either track.

- [x] **2.1 Eval regression gate in CI** — done (2026-07-02). `run_eval.py` now also
  writes machine-readable `results/results.json` (with env metadata + corpus
  checksums); new `evaluation/thresholds.json` pins per-entity recall floors
  (identifiers 1.0; PERSON/DATE/ADDRESS floors below measured values to absorb spaCy
  drift; TOTAL + span-precision floors) and `evaluation/check_thresholds.py` enforces
  them (missing entity = failure). New `eval` CI job: install → regenerate corpus →
  determinism check → eval → gate. Gate verified to fail (exit 1) on an injected
  recall drop and on a dropped entity; 44 checks pass on current results.
- [x] **2.2 Corpus determinism check** — done (2026-07-02). New
  `benchmark/check_determinism.py` compares sha256 of all four corpus JSONL files
  against committed `benchmark/data/checksums.json` (`--update` to refresh after
  intentional generator changes); verified corpus regenerates bit-identically.
  Version metadata (presidio-analyzer 2.2.363, spacy 3.8.13, en_core_web_sm 3.8.0,
  Python) now recorded in the `results.md` header and `results.json`.
- [x] **2.3 Property-based tests (Hypothesis)** — done (2026-07-02). New
  `tests/test_properties.py`: exactly-one-check-digit property for Luhn and Verhoeff;
  single-digit-substitution detection for both checksums; all nine
  generator/validator pairs agree across random seeds (checksum validators must
  return True, plausibility validators must not return False); normalize round-trip
  for SIN. `hypothesis` added to dev deps.
- [x] **2.4 Negative unit-test suite** — done (2026-07-02). New
  `tests/test_negatives.py`: credit cards (Luhn-valid, all formats), invoice numbers,
  US SSN/phone formats, checksum-reject cases (SIN/OHIP/Aadhaar/BC PHN), cross-locale
  collision (Indian mobile vs BC PHN), and realistic clinical numerics (ICD-10, labs,
  vitals, accession numbers) — all asserted below reporting threshold across the whole
  pack. **Found and fixed a real precision bug:** Presidio compiles patterns with
  IGNORECASE by default, so the RAMQ pattern matched lowercase words + digits
  ("card 4111 1111" in a credit-card sentence) and the structural validator boosted it
  to 1.0. Added a `case_sensitive` option to `ValidatedPatternRecognizer` and enabled
  it for RAMQ, PAN, Voter ID, and Passport (all printed uppercase). Full suite: 66
  tests pass; determinism + eval + threshold gate all re-verified green (recall
  unchanged — benchmark values are uppercase).
- [x] **2.5 Fully-covered leak metric** — done (2026-07-03). `metrics.py` gains
  `fully_covered` (gold span ⊆ union of predictions) and a "Strict recall" column in
  all tables/JSON. Findings: pack identifiers stay 1.000 strict; the gap between leak
  and strict recall is real and locale-shaped — CA pack 0.987 leak vs 0.809 strict on
  gold (driven by ADDRESS 0.000 strict: spaCy LOCATION covers addresses only
  partially, and PERSON 0.818 strict), IN pack 0.959 vs 0.900. Strong paper material:
  the strict metric exposes partial-masking leaks that overlap recall hides.
- [x] **2.6 Statistical reporting** — done (2026-07-03). Percentile bootstrap 95% CIs
  (1000 note-level resamples, deterministic seed) for leak recall, strict recall, and
  precision in every table and in results.json. New `evaluation/seed_variance.py`
  generates in-memory corpora at alternate seeds (committed corpus/manifest untouched)
  → `results/seed_variance.md`: across seeds 42/101/202, spread ≤ 0.010 on all
  metrics, both locales — fixed-seed results are representative.
- [x] **2.7 Stronger stock-Presidio baseline** — done (2026-07-03). `run_eval.py
  --model` flag; non-default models write `results_<model>.*` so the canonical gated
  results are untouched. `en_core_web_lg` 3.8.0 installed and evaluated: stock leak
  recall is *lower* with lg (CA 0.851 vs 0.885; IN 0.745 vs 0.778 on gold) — the
  bigger model does not close the identifier gap — while pack+lg improves overall
  (CA 0.987/0.990, IN 1.000/0.999 leak recall) via better PERSON NER. Strengthens the
  paper's claim: the gap is a coverage problem, not a model-size problem. spaCy
  transformer engine deferred (optional).
- [x] **2.8 Pin the eval environment** — done (2026-07-03). `uv.lock` refreshed (now
  includes hypothesis); CI eval job installs with `uv sync --locked` + pinned spaCy
  model from new `evaluation/requirements-eval.txt` (model URLs kept out of pyproject
  so PyPI publishing isn't blocked; `uv run --no-sync` prevents the implicit sync from
  pruning the model). Test-matrix job intentionally stays on loose resolution — that's
  what consumers get. Validated by simulating the CI install in a throwaway env:
  66 tests pass, corpus regenerates bit-identically, eval reproduces the gated numbers
  exactly, all 44 threshold checks pass. Versions were already recorded in results
  metadata (2.2).
- [x] **2.9 Type checking in CI** — done (2026-07-03). mypy added to dev deps and
  configured in pyproject (`check_untyped_defs`, covers src/evaluation/benchmark/
  tests; `ignore_missing_imports` for stub-less presidio/spacy). Two findings fixed:
  `context` param typed `list[str] | None` vs Presidio's `list[str]` signature, and a
  stale `type: ignore`. "Type check" step added to the CI test job; mypy clean on all
  25 source files; `uv.lock` refreshed.
- [ ] **2.10 Real-data false-positive evaluation (MIMIC notes)**
  - Real de-identified clinical prose as FP stress test (PhysioNet credentialing
    required — **start the application now**; DUA prohibits redistribution: script in
    repo, numbers in paper only). Exercises both locales' recognizers at once.

## Phase 3 — Canada track (primary focus)

### 3A. Evaluation rigor

- [x] **3.1 CA false-positive stress corpus** — DONE
  - Canadian clinical notes with confusable non-PII numerics: accession numbers, lab
    values, credit-card numbers (Luhn-valid — must NOT match SIN/OHIP), US SSNs,
    ICD-10 codes, bare 9/10-digit quantities without context.
  - Done: `benchmark/generate_negatives.py` emits 300 deterministic PII-free notes
    (billing / lab report / admin templates) with Luhn-valid credit cards, US SSNs,
    9/10-digit serials and order numbers, ICD-10, labs/vitals, facility phones, and
    "context traps" (identifier context words with no identifier).
    `evaluation/run_negatives.py` measures pack-entity FPs for two configs.
  - Measured (seed 42): full pack 43.67 FP/100 notes — dominated by `IN_MOBILE` (85)
    and `IN_AADHAAR` (8) firing on Canadian order numbers / credit cards, a strong
    argument for locale-scoped registration. CA-only registration: 12.67 FP/100
    notes, all irreducible checksum collisions (`CA_SIN` 19, `CA_OHIP` 16,
    `CA_BC_PHN` 3 on random 9/10-digit serials, ~matching the expected ~10% Luhn
    base rate). Zero FPs from credit cards (4-4-4-4 grouping doesn't match SIN/OHIP
    separators), US SSNs (3-2-4 shape), or context traps.
  - Gated in CI: corpus covered by the determinism manifest; FP ceilings (55 and
    20 per 100 notes) enforced via `thresholds.json` + `check_thresholds.py`.
  - Paper input: report both FP rates and recommend `locales=["ca"]` for Canadian
    deployments.
- [x] **3.2 CA adversarial / hard split** — DONE
  - Identifiers without adjacent context words, unusual separators, line-wrapped
    values, OCR noise, dictation artifacts. Separate "hard" results table.
  - Done: `benchmark/generate_hard.py` — 300 single-identifier notes, 5 CA entities
    x 6 variants x 10 (control / no_context / unusual_separator / line_wrap /
    ocr_confusable / dictation), checksum-valid values, exact spans, deterministic,
    in the manifest. `evaluation/run_hard.py` writes the entity-x-variant
    leak/strict recall matrix to `results/hard_ca.{md,json}`.
  - Measured (pack, leak recall by variant): control 1.00, no_context 0.96,
    unusual_separator 0.56, line_wrap 0.38, ocr_confusable 0.38, dictation 0.50.
    This is the honest, non-circular recall number: the pack's patterns only handle
    the separator conventions the generators emit, and much of the residual "recall"
    on degraded variants is incidental overlap from built-in DATE_TIME /
    PHONE_NUMBER recognizers (pack rows equal stock rows there; strict recall on
    line_wrap/ocr is 0.02). Notable cells: SIN misses dot/slash-separated and
    dictation forms entirely; RAMQ drops to 0.10 on unusual separators; BC PHN
    survives dictation (compact 10-digit re-match) but not line wraps.
  - Gated in CI as regression floors at measured values (thresholds.json
    `hard_min_recall`) — floors document current robustness, they are not targets.
  - Paper input (6.1/6.2): present the variant matrix alongside the main-benchmark
    1.000 recall as the circularity acknowledgment; frames main-benchmark results
    as in-distribution upper bound. Closing the gaps (e.g. separator-tolerant
    patterns, wrap-tolerant matching) is future recognizer work — improving the
    numbers before the paper is optional, reporting them honestly is not.
- [x] **3.3 CA benchmark diversity** — DONE
  - Expand templates beyond 3 note types; expand name pools; more clinical filler
    variety. Addresses the circularity critique for the CA claims.
  - Done — addresses: `benchmark/curate_oda.py` reservoir-samples 2,000 usable
    rows per province from raw StatCan **ODA** CSVs (AB/ON/QC, OGL – Canada,
    supplied under gitignored `benchmark/data/external/oda/`) into committed
    `benchmark/data/oda/ca_addresses_sample.csv` (6,000 real civic addresses,
    204 KB) with provenance README (raw-file sha256, seed, filter). CA `gen_address`
    now draws real ODA addresses with format variety: French street-type ordering
    ("88, rue Lacaune"), unit prefixes ("910-766 John Counter Blvd" / "Unit 4, ..."),
    PO boxes, directions (NW/SE). The sample is a committed source artifact (CI
    cannot regenerate it), deliberately NOT in the determinism manifest.
  - Postal codes stay **synthetic**: the recognizer is purely structural so real
    codes add no coverage, and Canada Post claims rights over the postal-code
    database — real codes must not be committed. ODA `postal_code` column dropped
    at curation.
  - Done — names: CA pools widened from 16/16 to 38/43 reflecting census diversity
    (Franco accented, Punjabi, Chinese, Vietnamese, Filipino, Arabic, Eastern
    European, Irish/Scottish, Indigenous surnames). Templates: 3 new CA note types
    (ED triage, internal-medicine consult with PII in running prose, outpatient lab
    requisition) — 6 CA templates total. CA-only clinical-history additions kept in
    `CLINICAL_HISTORIES_CA` so the frozen India corpus regenerates bit-identically
    (verified: `in_*` hashes unchanged).
  - Re-measured (sm, gold): pack leak recall 0.994 / strict 0.861; identifiers all
    still 1.000/1.000; PERSON 0.982 leak (diverse names did NOT degrade spaCy on
    these templates); ADDRESS strict still 0.000 on real ODA addresses — confirms
    3.9 motivation with non-synthetic evidence. Span-precision floor re-pinned
    0.78 → 0.75 (measured 0.761–0.770 CA): richer templates give spaCy's built-ins
    more to mislabel (ORGANIZATION on hospital headers, DATE_TIME on durations);
    pack entities contribute zero benchmark FPs (gated separately via negatives
    ceilings). lg + seed-variance evidence regenerated (spread ≤ 0.009).
  - Paper impact (for 6.1): corpus is now 11,321 entities (CA 5,013 / IN 6,308);
    all §5 CA numbers change; stock CA FN rate now 9.9% (gold).
  - Names upgraded from hand-curated pools to census data (2026-07-03):
    `benchmark/curate_statcan_names.py` cleans StatCan **First names in Canada,
    2021 Census** (cat. 98-505-X2021007, StatCan Open Licence; raw CSV gitignored
    under `benchmark/data/external/statcan_names/`) into committed
    `benchmark/data/statcan_names/ca_first_names.csv` (9,152 names + counts,
    112 KB, attribution README). CA `gen_person` now samples first names
    frequency-weighted from the census distribution, plus a 15% accented
    supplement (census publishes names unaccented, count < 250 excluded, counts
    randomly rounded — documented in the README). Surnames remain hand-curated
    (census product covers first names only). India generator untouched
    (`in_*` hashes verified unchanged).
  - Re-measured with census names (sm, gold): pack 0.984 leak / 0.840 strict;
    PERSON 0.952 leak / 0.928 strict — realistic-frequency names cost spaCy ~3
    points of PERSON leak recall vs the hand-picked pool (0.982). Identifiers
    unaffected (1.000). All 52 gate checks pass; lg + seed-variance regenerated
    (spread ≤ 0.005).
- [ ] **3.4 CA gold-split human review** — execute documented protocol on the CA gold
  split; record outcome in `docs/gold_review.md`. Until done, the paper must not
  call the split "gold": it is the first 100 notes of the same generator stream.
- [x] **3.4a Pre-release bug sweep** — DONE (2026-10-27). Found by probing outside
  the benchmark's distribution: (a) OHIP separated pattern absorbed trailing 1-2
  letter English words into a 1.0-score span (IGNORECASE + optional version
  code) — now case-sensitive, validator enforces HCV `[1-9]\d{9}`;
  (b) `CA_HEALTH_CARD` and all French context never fired through Presidio
  (multi-word phrases vs single-token lemma enhancer) — single tokens added,
  engine-level regression tests in `tests/test_recognizers.py::TestEngineContext`;
  (c) `run_core_eval.py` counted correct address predictions as FPs;
  (d) corpus: future DOBs, RAMQ letters unrelated to the patient, RAMQ births
  capped at 1999. Measured checksum collision floors: 7.85% (SIN, 9-digit),
  10.29% (OHIP, 10-digit) on 20k random strings — to be reported in the paper.

### 3B. Coverage & correctness depth

- [ ] **3.5 Remaining provinces/territories**
  - Per-province recognizers (or documented format profiles) for SK, MB, NS, NB, NL,
    PE, YT, NT, NU — replacing/augmenting the generic context-gated fallback. Verify
    each format against official sources.
- [x] **3.6 RAMQ realism** — DONE (2026-07-06). `gen_ca_ramq` now builds the
  letter block per RAMQ's published composition: 3 surname letters (shared
  `_ramq_letters` helper; apostrophes/hyphens dropped, X-padded) + a
  first-name initial drawn from the census-weighted first-name distribution
  (new `gen_ca_first_name`, shared with `gen_person`). Hard-split `_raw_ramq`
  uses the same helper over the surname pool. Structural rules verified
  against RAMQ documentation (card-usage page + pharmacists' manual): 12-char
  NAM = 3 surname letters + first-name initial + YY + MM (+50 for women, so
  01-12/51-62) + DD + 2-digit administrative code — validator's month rule
  confirmed; day stays 01-31 (no per-month rule published); final two digits
  unvalidated (no public checksum; "chiffre-preuve" algorithm not public).
  Findings recorded in `docs/identifiers/ca_ramq.md`. CA corpus + hard split
  regenerated (IN hashes unchanged), manifest updated, full eval re-run: all
  identifiers still 1.000, all 53 gate checks pass (hard-split
  unusual_separator 0.64 and ocr_confusable 0.48 drifted up with the new
  letter blocks; floors unchanged).
- [ ] **3.7 French-language Quebec notes** — **DEFERRED (post-1.0 release)**
  - French clinical note templates + French context-word evaluation (currently the
    French context terms are implemented but never exercised). Requires a French
    spaCy model in the eval matrix. Moved out of the initial Canada release scope;
    revisit after Phase 5/6 or as a follow-up release.
- [x] **3.8 CA identifier spec provenance docs** — DONE (2026-07-06).
  `docs/identifiers/` (README index + 8 docs: SIN, OHIP, RAMQ, BC PHN, AB ULI,
  generic health card, postal code, street address), each recording the
  authoritative source (Service Canada, Ontario MOH HCV manual + technical
  spec, RAMQ, BC MoH Software Compliance Standards check-digit routine,
  Alberta Netcare/AHS, Canada Post), the exact rule implemented
  (pattern + validator), and known gaps. Where a rule has no official public
  spec (SIN Luhn, ULI structure, RAMQ short-name convention) the doc says so
  explicitly. Verification findings: OHIP HCV schema requires first digit
  non-zero (not enforced by our validator — noted as gap); BC PHN weights
  and 10/11-invalid rule match the published routine exactly.
- [x] **3.9 CA_STREET_ADDRESS recognizer + non-circular address evaluation** — DONE
  - Motivation: ADDRESS was the dominant leak (strict recall 0.000 on all CA gold
    addresses — spaCy masked the city, CA_POSTAL_CODE the code, civic + street
    leaked on every note).
  - Done: `CaStreetAddressRecognizer` — English + French full-line patterns
    anchored by province + structural postal code; validator in `validators.py`.
    Registered as the 8th Canada recognizer (16 total in pack).
  - ODA holdout: `benchmark/curate_oda_eval.py` (seed 1042, 200/province) →
    `benchmark/data/oda/ca_addresses_eval.csv` (600 rows, never used by main
    benchmark generator). `benchmark/generate_address_eval.py` → 300 single-address
    notes; `evaluation/run_address_eval.py` → `results/address_ca.{md,json}`.
  - Measured: ODA holdout strict recall 0.000 → **0.950** (pack); main CA gold
    ADDRESS strict **0.971** (was 0.000); overall CA gold strict **0.972** (was
    0.840). Gated in CI (`address_min_strict_recall` floor 0.90). TYPE_MAP maps
    CA_STREET_ADDRESS → ADDRESS for typed metrics.
  - Paper input (6.1): report holdout before/after table; recognizer count is now
    16 (paper still says 15 — update at table regeneration).

## Phase 4 — India track (future separate package `pii-detector-in`)

**Status (2026-10-27): removed from this package; unscheduled.** The India
recognizers, generators, templates, gold corpus and tests were deleted from the
repository on 2026-10-27 (recoverable from git history). When the India package
starts, extract `core/` into a shared dependency first (see PHASE2 plan 2A) so
the two packages share validators, the spec schema and the Presidio adapter.

- [ ] **4.0 Restore the India recognizers from git history into `pii-detector-in`**
  - Aadhaar (Verhoeff), ABHA, PAN, UHID, mobile, PIN, Voter ID, passport, plus the
    generators/templates. Re-validate every rule against an official source before
    re-publishing; the pre-removal numbers were provisional.
- [ ] **4.1 IN false-positive stress corpus** — Indian confusables: bare 12/14-digit
  quantities, invoice/GST numbers, IFSC-adjacent strings, lab values.
- [ ] **4.2 IN adversarial / hard split** — no-context identifiers, separator
  variants, OCR/dictation noise, code-mixed (Hinglish) snippets.
- [ ] **4.3 IN benchmark diversity** — expand name pools (regional diversity:
  North/South/East naming conventions, single-name patients), more templates,
  state-varied addresses.
- [ ] **4.4 UHID facility-profile system** — ship a small library of real hospital
  UHID format profiles (configurable per deployment); document the per-facility
  configuration story properly.
- [ ] **4.5 Indic-script and code-mixed text support** — evaluate Hindi context words
  for real (currently untested); decide scope for Devanagari/other-script notes.
- [ ] **4.6 bharat-pii baseline: run or remove** — the harness supports it but no
  numbers exist; install and report, or delete the code path.
- [ ] **4.7 IN gold-split human review** — same protocol as 3.4.
- [ ] **4.8 IN identifier spec provenance docs** — UIDAI, ABDM/NHA, Income Tax Dept,
  ECI, MEA sources.

## Phase 5 — Documentation, release engineering

- [x] **5.1 README scope disclaimer** — DONE (2026-10-27). *What this is not* section
  + benchmark-circularity caveat; examples use `locales=["ca"]`; doc snippets verified
  executable. Original item: not a compliance guarantee (PIPEDA/PHIPA/DPDP);
  synthetic-benchmark caveat; recommend locale-scoped registration
  (`get_recognizers(["ca"])`) to avoid cross-locale false positives.
- [x] **5.2 CONTRIBUTING.md** — DONE (2026-10-27). extension recipe: validator → recognizer → generator →
  template slot → eval threshold → spec doc.
- [x] **5.3 SECURITY.md** — DONE (2026-10-27); uses GitHub private vulnerability
  reporting, which must be enabled in repo settings once public. private disclosure channel for recall/leak findings.
- [x] **5.4 Housekeeping** — DONE (2026-10-27). Author "Karthikeyan Murugaiah" +
  email in `pyproject.toml`/`CITATION.cff`; ORCID still to add before the DOI.
- [x] **5.4a Rename to `pii-detector-ca`, remove India** — DONE (2026-10-27).
  Distribution `pii-detector-ca`, import `pii_detector_ca`; `locales=` removed
  from the API; `exclude=` added to `add_recognizers` for the Presidio built-in
  name collision.
- [ ] **5.5 PyPI release** — 0.1.0 via trusted publishing; tag-triggered workflow.
  Name `pii-detector-ca` verified free on PyPI 2026-10-27.
- [ ] **5.6 CHANGELOG.md** + semver tags. — CHANGELOG added (2026-10-27); `v0.1.0`
  tag pending release.
- [ ] **5.7 CITATION.cff + Zenodo DOI** — CITATION.cff added (2026-10-27); DOI pending; archive at the paper's evaluated version.

## Phase 6 — Paper finalization

Decision (2026-10-27): Canada-only paper. `paper/paper.md` is stale (two-locale,
pre-Phase-2/3 numbers, 15 recognizers / 3 note types) and must be rewritten, not
patched. Headline contribution: provincial health-card coverage + benchmark
methodology; SIN/postal are upstream now (see top of file).

- [x] **6.1 Regenerate all §5 tables** — DONE (2026-10-27). `paper/paper.md`
  rewritten (v0.2) from current results: three baselines incl. "Presidio + CA
  builtins", CIs, strict recall, negatives, adversarial, address holdout, lg,
  seed variance, collision floors. Structured for JAMIA Open *Research and
  Applications* (≤ 4,000 words).
- [ ] **6.1a pyDeid baseline run** — pyDeid (Sundrelingam et al., JAMIA Open
  2025; MIT; `GEMINI-Medicine/pyDeid`, `deid_string()` API) is regex-only for
  SIN/OHIP/postal with no checksum. Run it on the evaluation split, negatives
  and hard split and add a column; the paper currently characterises it from
  source only (Limitations). Not run in the sandboxed session (external code).
- [x] **6.2 Acknowledge benchmark circularity** — DONE in v0.2 (Discussion).
- [x] **6.3 Ethics / broader-impact statement** — DONE in v0.2.
- [ ] **6.4 Datasheet for the benchmark** (Gebru-style).
- [ ] **6.5 Complete references** — verify EMNLP 2025 / Communications Medicine 2026
  anchors; add identifier spec citations; Presidio, i2b2/n2c2, Verhoeff.
- [x] **6.6 Report checksum collision floors** — DONE in v0.2 (Results).
- [x] **6.7 Soften untested claims** — DONE in v0.2 (Limitations).
- [ ] **6.8 Venue mechanics** — Primary: JAMIA Open *Research and Applications*
  (4,000 words, structured abstract ≤ 250, 4 tables / 6 figures, APC ~US$3,625
  list — confirm; preprints allowed; pyDeid published there Jan 2025). Fallback:
  arXiv cs.CL now + ClinicalNLP 2027 (2026 deadline was 16 Feb; expect ~Feb 2027).
  JOSS is **not** eligible until the repo has 6 months of public history
  (~April 2027) and requires an AI-usage disclosure. Needs: ORCID, Zenodo DOI
  (5.7), v0.1.0 tag, figures (none yet — at minimum the Table 3 heatmap and a
  leak-vs-strict bar chart).

---

## Suggested execution order

1. ~~Phase 1~~ (done).
2. Phase 2 (shared infra — locks in correctness; start PhysioNet application for 2.10
   immediately since approval takes days–weeks).
3. Phase 3 (Canada track, 3A before 3B; 3A items are the paper-critical ones).
4. Decision point: if a submission deadline is near, do Phase 6 with Canada-only or
   Canada-deep/India-current scope; otherwise proceed to Phase 4.
5. Phase 5, then Phase 6. Phase 4 only as a separate package.
