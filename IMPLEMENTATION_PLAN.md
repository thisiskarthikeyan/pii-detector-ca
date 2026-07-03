# Implementation Plan

Roadmap to a credible validation process, an open-source release, and a submittable paper.
Phases are ordered by dependency: correctness fixes first, then evaluation rigor, then
automation, then release and paper polish. Each item is a checkbox so this file doubles
as a progress tracker.

---

## Phase 1 — Correctness fixes (must-fix, blocks everything downstream)

- [ ] **1.1 Fix context-gating bypass for checksumless identifiers**
  - Problem: Presidio's `PatternRecognizer` sets score to `MAX_SCORE` (1.0) when
    `validate_result` returns `True`. The plausibility validators
    (`ca_ab_uli_plausible`, `in_abha_plausible`) return `True` for nearly any 9/14-digit
    string, so any bare number is flagged at score 1.0 and the low pattern score +
    context-word gate is bypassed entirely.
  - Fix: in `ValidatedPatternRecognizer`, distinguish *checksum* validators
    (True → boost, False → reject) from *plausibility* validators
    (None → keep pattern score, False → reject). Plausibility validators should never
    return `True`.
  - Files: `src/presidio_recognizers_ca_in/base.py`, `validators.py`,
    `canada/health_cards.py` (Alberta ULI), `india/abha.py`.
  - Add regression tests: bare 9-digit / 14-digit numbers with **no context** must not
    surface above the reporting threshold; with context words they must.

- [ ] **1.2 Remove dead `boost_score` parameter or make it functional**
  - `ValidatedPatternRecognizer.boost_score` is stored but never used; the docstring
    ("raises the score to boost_score") is wrong. Either implement it by overriding the
    score assignment or delete the parameter and fix the docstring.

- [ ] **1.3 Fix `gen_ca_sin` first-digit typo**
  - `rng.choice("123456579")` duplicates 5 and was presumably meant to be digits 1-9
    excluding 0/8 (`"12345679"`, or include 9 explicitly: `"123456799"` is wrong too —
    use `"12345679"` + `"9"` as valid leading digits per spec decision). Remove the
    now-redundant `while True` / `if base[0] not in "08"` loop.
  - File: `benchmark/pii_generators.py`.

- [ ] **1.4 Re-run the full evaluation after 1.1–1.3 and regenerate results**
  - `python benchmark/generate_corpus.py --locale ca --n 1000`
  - `python benchmark/generate_corpus.py --locale in --n 1000`
  - `python evaluation/run_eval.py --all`
  - Commit updated `evaluation/results/results.md` and `error_analysis.json`.

- [ ] **1.5 Reconcile paper numbers with results files**
  - Paper §5.2 says CA_RAMQ pack recall 0.967 and §5.3 discusses a 3.3% RAMQ miss;
    `results.md` shows 1.000. §5.3 also claims "100% on all eight validated types",
    contradicting the table two paragraphs earlier. After 1.4, regenerate every number
    in §5 from the results files and delete or rewrite the stale RAMQ error-analysis
    paragraph.
  - File: `paper/paper.md`.

## Phase 2 — Evaluation rigor (what reviewers will judge)

- [ ] **2.1 Stronger stock-Presidio baseline**
  - Add `en_core_web_lg` (Presidio's default) alongside `en_core_web_sm`; optionally a
    spaCy transformer engine. Report both in the paper; attribute PERSON-name misses to
    the best available engine, not the weakest.
  - Files: `evaluation/run_eval.py` (make NLP config a CLI flag), `paper/paper.md` §5.1.

- [ ] **2.2 False-positive stress corpus ("negatives" split)**
  - New generator producing notes with confusable non-PII numerics: accession numbers,
    lab values, invoice/claim numbers, credit-card numbers (Luhn-valid, must NOT match
    SIN/OHIP), US SSNs, ICD-10 codes, 9/14-digit quantities without context.
  - Metric: false-positive rate per recognizer on this split; add to results tables.
  - Files: new `benchmark/negatives.py` (or extend templates), `evaluation/run_eval.py`,
    `evaluation/metrics.py`.

- [ ] **2.3 Adversarial / hard split**
  - Identifiers with no adjacent context word, unusual separators (dots, mixed),
    line-wrapped values, OCR-style noise injection (character substitutions), and
    dictation artifacts. Report as a separate "hard" table; do not blend into the main
    split.
  - Files: `benchmark/` (noise channel module), `paper/paper.md` §4–5.

- [ ] **2.4 Fully-covered leak metric**
  - Current leak recall counts any 1-character overlap as "detected". Add a strict
    variant: gold span must be fully covered by the union of predicted spans. Report
    both; the strict one matches the masking threat model the paper invokes.
  - Files: `evaluation/metrics.py`, `evaluation/run_eval.py`, `paper/paper.md` §5.1.

- [ ] **2.5 Statistical reporting**
  - Bootstrap 95% CIs over notes for headline recall/FN/precision; run corpus
    generation over 3–5 seeds and report variance. Flag small-n cells (e.g.
    IN_PASSPORT n=11 on gold).
  - Files: `evaluation/metrics.py`, `evaluation/run_eval.py`, `paper/paper.md`.

- [ ] **2.6 Acknowledge and mitigate benchmark circularity**
  - Generators import the package's own validators and always place identifiers after
    strong context words — pack recall is near-true-by-construction. State this
    explicitly in §6; position the stock-Presidio gap as the robust finding and use the
    2.2/2.3 splits as the non-circular evidence for the pack.
  - Files: `paper/paper.md` §4, §6.

- [ ] **2.7 Gold-split human review protocol**
  - Write the procedure (reviewers, error definition, adjudication), execute it on both
    gold splits, record the outcome (e.g. "2 reviewers × 200 notes, N span errors").
    Either make "gold" mean something or drop the term.
  - Files: new `docs/gold_review.md`, `paper/paper.md` §4.

- [ ] **2.8 Third-party baseline: run or remove**
  - `run_eval.py` supports bharat-pii but no numbers exist anywhere. Either install it,
    run it, and report; or remove the code path and the mention.

## Phase 3 — Validation automation (CI as the enforcement mechanism)

- [ ] **3.1 Eval regression gate in CI**
  - New CI job: install spaCy model(s), regenerate corpus from fixed seed, run
    `run_eval.py`, fail if per-entity recall drops below pinned thresholds or FP rate
    rises above tolerance. Thresholds live in a checked-in config
    (e.g. `evaluation/thresholds.yaml`).
  - Files: `.github/workflows/ci.yml`, new threshold config, small assert script.

- [ ] **3.2 Corpus determinism check**
  - CI hashes regenerated JSONL against committed checksums so seed/stdlib drift is
    caught immediately. Record checksum + package versions in `results.md` header.

- [ ] **3.3 Property-based tests (Hypothesis)**
  - Random digit strings validate at expected base rates (~1/10 Luhn, ~1/10 Verhoeff);
    every generator output passes its validator; every single-digit corruption of a
    valid checksum fails; normalize/format round-trips.
  - Files: new `tests/test_properties.py`, add `hypothesis` to dev deps.

- [ ] **3.4 Negative unit-test suite**
  - Assert non-detection: credit cards vs SIN/OHIP, US SSN, phone numbers vs BC PHN,
    Aadhaar-shaped numbers with bad Verhoeff, cross-locale collisions
    (Luhn-valid ULI ≠ SIN report at top score, Indian mobile vs BC PHN).
  - Files: new `tests/test_negatives.py`.

- [ ] **3.5 Pin the eval environment**
  - Use `uv.lock` in the eval CI job; pin the spaCy model versions; keep library deps
    loose for consumers. Document exact versions in results output.

- [ ] **3.6 Type checking in CI**
  - Add mypy or pyright job; codebase is small and mostly annotated already.

## Phase 4 — Documentation & auditability

- [ ] **4.1 Identifier spec provenance docs**
  - One page per identifier under `docs/identifiers/`: authoritative source (Service
    Canada, RAMQ, BC HIBC, UIDAI, Income Tax Dept, ECI, MEA), exact rule implemented,
    known gaps/assumptions. Link from validators' docstrings and from the paper.

- [ ] **4.2 README scope disclaimer**
  - Not a compliance guarantee under PIPEDA/PHIPA/DPDP; synthetic-benchmark caveat;
    recommend locale-scoped registration (`get_recognizers(["ca"])`) to avoid
    cross-locale false positives — advertise the existing `locales=` parameter.

- [ ] **4.3 CONTRIBUTING.md**
  - Focus on the extension recipe: how to add a locale/identifier
    (validator → recognizer → generator → template slot → eval threshold → spec doc).

- [ ] **4.4 SECURITY.md** — private disclosure channel for recall/leak findings.

- [ ] **4.5 Housekeeping**
  - Fix placeholder repo URL and author in `pyproject.toml`; ensure `__pycache__` /
    `.pyc` are gitignored and untracked; document that `benchmark/data/generated/` is
    regenerated, not committed; fix RAMQ generator realism (3 surname letters + 1
    first-name letter) or document the simplification.

## Phase 5 — Release engineering

- [ ] **5.1 PyPI release** — publish 0.1.0 via GitHub Actions trusted publishing;
  release workflow triggered on tags. (README already advertises `pip install`.)
- [ ] **5.2 CHANGELOG.md** and tagged releases (semver).
- [ ] **5.3 CITATION.cff** + Zenodo DOI archived at the paper's evaluated version;
  paper cites the DOI, not `main`.

## Phase 6 — Paper finalization

- [ ] **6.1 Regenerate all §5 tables** from post-fix results (depends on Phases 1–2);
  add CIs, strict leak metric, FP-rate table, `en_core_web_lg` baseline column.
- [ ] **6.2 Ethics / broader-impact statement** — synthetic data only, checksum-valid
  generated IDs may coincidentally collide with issued ones, dual-use note, not a
  compliance certification.
- [ ] **6.3 Datasheet for the benchmark** (Gebru-style) as appendix or supplementary.
- [ ] **6.4 Complete references** — verify the EMNLP 2025 and Communications Medicine
  2026 anchors; add identifier spec citations from 4.1; Presidio, i2b2/n2c2, Verhoeff.
- [ ] **6.5 Fix §3.2 PAN format notation** — replace "AAAHA9999A" with the explicit
  pattern `[A-Z]{3}[PCFHATBLJG][A-Z][0-9]{4}[A-Z]` and clarify hold-type letter.
- [ ] **6.6 Soften untested claims** — Hindi/French context words are implemented but
  never exercised by the English-only corpus; say so.
- [ ] **6.7 Venue mechanics** — pick target (ClinicalNLP / LOUHI / ML4H), apply its
  template and page limit, check anonymity-period rules, write the reproducibility
  appendix (`make reproduce` or single script from clean checkout to all tables).

---

## Suggested execution order

1. Phase 1 end-to-end (small diffs, unblocks everything).
2. Phase 3.1–3.4 (lock in correctness before touching the benchmark further).
3. Phase 2 (eval rigor; largest work item — 2.2/2.3 are the paper-critical additions).
4. Phase 4, then 5 (docs and release, mostly mechanical).
5. Phase 6 last, once numbers are final.
