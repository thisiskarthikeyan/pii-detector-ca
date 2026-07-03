# Implementation Plan

Roadmap to a credible validation process, an open-source release, and a submittable paper.

**Strategy: locale-split, Canada first. India is OUT OF SCOPE for the initial pass.**
Canada has a bounded identifier landscape (one federal ID, ~5 well-specified provincial
schemes) and can be driven to publication-quality depth quickly. India has far more
variation (per-facility UHIDs, state-level differences, multi-script text, diverse
mobile/ID formats) and gets its own track (Phase 4) only after the Canada work is done.

**India freeze policy for the initial pass:**
- Existing India recognizers/tests/gates stay in the repo and must keep passing at
  their current level (freeze = regression protection, not endorsement of depth).
- No new India recognizers, benchmark content, docs, or evaluation work until Phase 4.
- India-touching artifacts added by the shared-infra phase (thresholds.json entries,
  property/negative tests, corpus checksums for `in_*` files) are **provisional** and
  are re-validated/expanded as the first task of Phase 4 (item 4.0).
- Locale-agnostic work (metrics, CI, release plumbing) is done once, in the shared
  phases, and reused by both tracks.

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

- [ ] **3.1 CA false-positive stress corpus**
  - Canadian clinical notes with confusable non-PII numerics: accession numbers, lab
    values, credit-card numbers (Luhn-valid — must NOT match SIN/OHIP), US SSNs,
    ICD-10 codes, bare 9/10-digit quantities without context.
- [ ] **3.2 CA adversarial / hard split**
  - Identifiers without adjacent context words, unusual separators, line-wrapped
    values, OCR noise, dictation artifacts. Separate "hard" results table.
- [ ] **3.3 CA benchmark diversity**
  - Expand templates beyond 3 note types; expand name pools using Statistics Canada
    name-frequency lists (English- and French-Canadian, accented forms); more clinical
    filler variety. Addresses the circularity critique for the CA claims.
- [ ] **3.4 CA gold-split human review** — execute documented protocol on the CA gold
  split; record outcome in `docs/gold_review.md`.

### 3B. Coverage & correctness depth

- [ ] **3.5 Remaining provinces/territories**
  - Per-province recognizers (or documented format profiles) for SK, MB, NS, NB, NL,
    PE, YT, NT, NU — replacing/augmenting the generic context-gated fallback. Verify
    each format against official sources.
- [ ] **3.6 RAMQ realism** — generator: 3 surname letters + 1 first-name letter;
  verify structural rules (sex-offset month, day ranges) against RAMQ documentation.
- [ ] **3.7 French-language Quebec notes**
  - French clinical note templates + French context-word evaluation (currently the
    French context terms are implemented but never exercised). Requires a French
    spaCy model in the eval matrix.
- [ ] **3.8 CA identifier spec provenance docs**
  - `docs/identifiers/ca_*.md`: authoritative source (Service Canada, RAMQ, BC HIBC,
    Alberta Health, provincial ministries), exact rule implemented, known gaps.

## Phase 4 — India track (after Canada track is solid)

- [ ] **4.0 Revisit provisional India coverage from the shared-infra phase**
  - Re-validate and deepen everything India-related that was added while India was
    frozen: thresholds.json `in` floors (set from a shallow benchmark), India entries
    in the property/negative test suites, India corpus checksums, and the India
    results in results.md. Treat all current India numbers as provisional until this
    item completes.
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

- [ ] **5.1 README scope disclaimer** — not a compliance guarantee (PIPEDA/PHIPA/DPDP);
  synthetic-benchmark caveat; recommend locale-scoped registration
  (`get_recognizers(["ca"])`) to avoid cross-locale false positives.
- [ ] **5.2 CONTRIBUTING.md** — extension recipe: validator → recognizer → generator →
  template slot → eval threshold → spec doc.
- [ ] **5.3 SECURITY.md** — private disclosure channel for recall/leak findings.
- [ ] **5.4 Housekeeping** — fix placeholder repo URL/author in `pyproject.toml`;
  ensure `__pycache__`/`.pyc` untracked; document generated-data policy.
- [ ] **5.5 PyPI release** — 0.1.0 via trusted publishing; tag-triggered workflow.
- [ ] **5.6 CHANGELOG.md** + semver tags.
- [ ] **5.7 CITATION.cff + Zenodo DOI** archived at the paper's evaluated version.

## Phase 6 — Paper finalization

Note: the paper currently covers both locales. With the Canada-first split, either
(a) keep the two-locale paper and let India results reflect current depth while Canada
gets the hardened evaluation, or (b) narrow the first submission to Canada and make
India a follow-up. Decide at 6.1 based on how far Phase 4 has progressed by the
submission deadline.

- [ ] **6.1 Regenerate all §5 tables** from post-Phase-2/3 results; add CIs, strict
  leak metric, FP-rate table, `en_core_web_lg` baseline column. Decide single- vs
  two-locale scope.
- [ ] **6.2 Acknowledge benchmark circularity** in §4/§6; position the stock-Presidio
  gap as the robust finding; use FP/hard splits as non-circular evidence.
- [ ] **6.3 Ethics / broader-impact statement** — synthetic data only, checksum-valid
  collision caveat, dual-use note, not compliance certification.
- [ ] **6.4 Datasheet for the benchmark** (Gebru-style).
- [ ] **6.5 Complete references** — verify EMNLP 2025 / Communications Medicine 2026
  anchors; add identifier spec citations; Presidio, i2b2/n2c2, Verhoeff.
- [ ] **6.6 Fix §3.2 PAN notation** — explicit pattern
  `[A-Z]{3}[PCFHATBLJG][A-Z][0-9]{4}[A-Z]`.
- [ ] **6.7 Soften untested claims** — Hindi context words untested until 4.5; French
  untested until 3.7.
- [ ] **6.8 Venue mechanics** — target venue, template, page limit, anonymity rules,
  reproducibility appendix (single script from clean checkout to all tables).

---

## Suggested execution order

1. ~~Phase 1~~ (done).
2. Phase 2 (shared infra — locks in correctness; start PhysioNet application for 2.10
   immediately since approval takes days–weeks).
3. Phase 3 (Canada track, 3A before 3B; 3A items are the paper-critical ones).
4. Decision point: if a submission deadline is near, do Phase 6 with Canada-only or
   Canada-deep/India-current scope; otherwise proceed to Phase 4.
5. Phase 4 (India track), then Phase 5, then Phase 6.
