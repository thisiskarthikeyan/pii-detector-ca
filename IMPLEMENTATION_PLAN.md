# Implementation Plan

Roadmap to a credible validation process, an open-source release, and a submittable paper.

**Strategy: locale-split, Canada first.** Canada has a bounded identifier landscape
(one federal ID, ~5 well-specified provincial schemes) and can be driven to
publication-quality depth quickly. India has far more variation (per-facility UHIDs,
state-level differences, multi-script text, diverse mobile/ID formats) and gets its own
track once the Canada track and the shared infrastructure are solid. Locale-agnostic
work (metrics, CI, release plumbing) is done once, in the shared phases, and reused.

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

- [ ] **2.1 Eval regression gate in CI**
  - CI job: install spaCy model(s), regenerate corpus from fixed seed, run
    `run_eval.py`, fail if per-entity recall drops below pinned thresholds or FP rate
    rises above tolerance. Thresholds in a checked-in config
    (e.g. `evaluation/thresholds.yaml`).
- [ ] **2.2 Corpus determinism check**
  - CI hashes regenerated JSONL against committed checksums; record checksum + package
    versions in `results.md` header.
- [ ] **2.3 Property-based tests (Hypothesis)**
  - Base-rate validation of random strings (~1/10 Luhn, ~1/10 Verhoeff); generator
    outputs always pass validators; single-digit corruptions always fail;
    normalize/format round-trips. New `tests/test_properties.py`.
- [ ] **2.4 Negative unit-test suite**
  - Non-detection asserts: credit cards vs SIN/OHIP (shared Luhn!), US SSN, phone
    numbers vs BC PHN, bad-Verhoeff Aadhaar shapes, cross-locale collisions
    (Luhn-valid ULI vs SIN, Indian mobile vs BC PHN). New `tests/test_negatives.py`.
- [ ] **2.5 Fully-covered leak metric**
  - Strict variant: gold span fully covered by union of predicted spans. Report both.
    `evaluation/metrics.py`, `run_eval.py`.
- [ ] **2.6 Statistical reporting**
  - Bootstrap 95% CIs over notes; 3–5 corpus seeds; flag small-n cells.
- [ ] **2.7 Stronger stock-Presidio baseline**
  - `en_core_web_lg` (Presidio default) alongside `en_core_web_sm`; NLP config as CLI
    flag; optionally spaCy transformer.
- [ ] **2.8 Pin the eval environment** — use `uv.lock` in eval CI; pin spaCy model
  versions; record versions in results output.
- [ ] **2.9 Type checking in CI** (mypy or pyright).
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
