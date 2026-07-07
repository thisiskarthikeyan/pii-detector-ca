# Phase 2 Implementation Plan

Plan for evolving the current Presidio-first recognizer pack into a reusable,
framework-neutral local de-identification system.

The current `IMPLEMENTATION_PLAN.md` remains the Phase 1 / paper plan: Canada
depth, benchmark rigor, Presidio integration, release readiness, and manuscript
work. This Phase 2 plan starts from that foundation and separates the durable
assets (identifier specs, validators, benchmark, provenance) from Presidio so
they can be reused by high-throughput local services while still supporting
Presidio as an optional adapter.

---

## Guiding Principles

- **Local-first privacy boundary:** raw customer text must be processed in the
  customer's environment before any external LLM or third-party service sees it.
- **Framework-neutral core:** identifier rules, validators, context policies,
  transformation policies, and audit schemas must not depend on Presidio, spaCy,
  or any single NLP framework.
- **Presidio remains supported:** Presidio is still the first public adapter and
  paper vehicle, but it becomes a wrapper around the reusable core rather than
  the source of truth.
- **Auditable by construction:** every detection and transformation run records
  engine version, policy version, entities found, actions taken, and retention
  behavior without storing raw PII by default.
- **Secure lifecycle:** raw input is retained only long enough to scan and
  transform, with explicit destruction semantics and no accidental temp-file or
  debug-log persistence.
- **Benchmark as contract:** any implementation (Python core, Presidio adapter,
  Rust service, future ONNX-backed full mode) must pass the same deterministic
  corpus, negatives, hard splits, and thresholds.

---

## Phase 2A — Extract Framework-Neutral Identifier Core

Goal: make the deterministic identifier logic reusable without importing
Presidio.

- [x] **2A.1 Define machine-readable entity specs** — DONE (2026-07-06).
  Python specs in `core/specs.py` (16 entities; YAML export deferred). Each
  entry includes patterns, scores, context, validator binding, locale, and
  provenance doc path.
- [x] **2A.2 Move validators into a core module** — DONE (2026-07-06).
  `core/validators.py` is stdlib-only; top-level `validators.py` re-exports for
  backwards compatibility.
- [x] **2A.3 Add a generic Python scan API** — DONE (2026-07-06).
  `core.scan()` returns `Match` spans without Presidio/spaCy. Tests in
  `tests/test_core_scanner.py`; eval harness `evaluation/run_core_eval.py`.
- [x] **2A.4 Make Presidio recognizers thin adapters** — DONE (2026-07-06).
  All recognizer classes now subclass `adapters.presidio.SpecRecognizer` and
  load from `core/specs.py`. Public Presidio APIs unchanged.
- [x] **2A.5 Document engine-neutral contract** — DONE (2026-07-06).
  `docs/architecture/core_contract.md`.

---

## Phase 2B — Transformation Layer

Goal: move from detection-only to local de-identification actions.

- [ ] **2B.1 Define transformation policy schema**
  - Add a policy format such as `policies/clinical_default.yaml`.
  - Policy should specify per-entity action:
    - `block`;
    - `replace` (`<CA_SIN>`);
    - `redact` (remove span);
    - `mask` (preserve limited suffix/prefix);
    - `hash` (one-way pseudonymization);
    - `tokenize` (reversible vault-backed token, optional / future).
  - Include default policy behavior for unknown entity types.

- [ ] **2B.2 Implement deterministic text transformation**
  - Add a transform engine that accepts text + spans + policy and returns:
    - transformed text;
    - action records;
    - blocked/released decision;
    - transformation warnings.
  - Apply replacements from right to left to preserve offsets.
  - Preserve an offset map where practical so downstream systems can explain
    transformations.

- [ ] **2B.3 Add safe defaults**
  - Default customer-facing behavior should be `block` or `replace`, not
    flag-only.
  - Do not log raw values by default.
  - Provide explicit debug mode for development, disabled in production config.

- [ ] **2B.4 Add transformation tests**
  - Unit tests for overlapping spans, adjacent spans, multiline spans, masked
    suffixes, full redaction, replacement labels, and block-on-hit policy.
  - Golden tests showing an LLM-bound prompt after de-identification contains
    no detected identifier spans.

---

## Phase 2C — Local De-Identification Service

Goal: provide a private service that orchestrators and LLM tools can call before
any external model invocation.

- [ ] **2C.1 Define service API**
  - Initial endpoints:
    - `POST /v1/scan`;
    - `POST /v1/deidentify`;
    - `GET /v1/health`;
    - `GET /v1/version`.
  - `scan` returns spans and summary only.
  - `deidentify` returns sanitized text, block/release decision, audit id,
    policy version, engine version, and summary counts.

- [ ] **2C.2 Implement Python reference service**
  - Use the generic core scanner by default.
  - Allow optional Presidio-backed full mode when configured.
  - Bind to `127.0.0.1` by default.
  - Keep the service deployable as a local process or sidecar.

- [ ] **2C.3 Add orchestrator examples**
  - Example flow:
    - receive raw text;
    - call local `/v1/deidentify`;
    - if blocked, stop;
    - if released, send only sanitized text to the LLM;
    - store audit id with the downstream request.
  - Include examples for a plain Python client and a generic HTTP client.

- [ ] **2C.4 Add operational controls**
  - Request size limits.
  - Timeout limits.
  - Configurable locale/entity allowlists.
  - Configurable policy path.
  - Structured errors for blocked content, invalid policy, and unsupported
    entities.

---

## Phase 2D — Audit, Retention, and Secure Destruction

Goal: make every run explainable while minimizing sensitive data retention.

- [ ] **2D.1 Define audit event schema**
  - Fields:
    - `audit_id`;
    - timestamp;
    - caller identity;
    - policy version;
    - engine version;
    - locale/entity configuration;
    - input byte length and output byte length;
    - entity counts by type;
    - actions by type;
    - blocked/released decision;
    - duration;
    - retention mode.
  - Do not store raw input, raw output, or raw span values by default.

- [ ] **2D.2 Implement append-only audit writer**
  - Start with local JSONL for development.
  - Design interface so production deployments can write to WORM storage,
    customer SIEM, signed logs, or database-backed audit tables.
  - Include integrity metadata such as event hash and previous-event hash
    where feasible.

- [ ] **2D.3 Define retention modes**
  - `zero_retention`: raw input and raw output are never persisted.
  - `transient_debug`: raw values allowed only in local dev with explicit
    config and warning banners.
  - `token_vault`: optional future mode for reversible tokenization.

- [ ] **2D.4 Secure destruction practices**
  - Avoid temp files for raw input.
  - Avoid logging request bodies.
  - Minimize copies of raw strings in service code.
  - For native engines, use explicit zeroization for owned byte buffers.
  - For Python reference implementation, document limits of memory zeroization
    and rely on process isolation, zero retention, no temp files, and short
    object lifetimes.

- [ ] **2D.5 Add security documentation**
  - Add `docs/security/data_lifecycle.md`.
  - Include data-flow diagram, trust boundaries, default retention behavior,
    logging guarantees, known limitations, and deployment hardening checklist.

---

## Phase 2E — High-Throughput Native Engine

Goal: add a production-oriented implementation suitable for high-throughput
local deployments.

- [ ] **2E.1 Decide repository layout**
  - Option A: Rust crate inside this repo under `crates/pii_core/`.
  - Option B: separate repo generated from the shared specs.
  - Prefer in-repo initially so CI can run the same benchmark contract.

- [ ] **2E.2 Implement Rust identifier scanner**
  - Compile regexes from the machine-readable specs.
  - Port checksum and structural validators.
  - Implement context-window scoring for context-gated identifiers.
  - Return the same span schema as the Python core.

- [ ] **2E.3 Benchmark and parity tests**
  - Run the Rust engine against the same benchmark corpora.
  - Compare entity recall, negatives, and hard-split behavior with the Python
    core and Presidio adapter.
  - Add CI gates so Rust cannot drift below thresholds.

- [ ] **2E.4 Service packaging**
  - Expose Rust scanner as:
    - CLI;
    - local HTTP or gRPC service;
    - optional Python bindings via `pyo3` if useful.
  - Keep default deployment fully local with no outbound network dependency.

- [ ] **2E.5 Performance targets**
  - Define throughput and latency targets after baseline measurement.
  - Suggested initial targets:
    - identifiers-only p95 latency under 5 ms for typical clinical note size;
    - batch throughput suitable for thousands of short notes per second on a
      commodity VM;
    - memory footprint small enough for sidecar deployment.

---

## Phase 2F — Optional Full-Text NER Backends

Goal: support names, dates, and other contextual PII without making spaCy or
Presidio mandatory.

- [ ] **2F.1 Define NER backend interface**
  - `none`: identifiers only.
  - `presidio`: current behavior, useful for reference and compatibility.
  - `spacy`: direct spaCy backend if Presidio is unnecessary.
  - `onnx`: future local model runtime for high-throughput deployments.

- [ ] **2F.2 Separate identifier metrics from NER metrics**
  - Report deterministic identifier recall independently from PERSON/DATE
    performance.
  - Make it explicit that PERSON recall is backend-dependent.

- [ ] **2F.3 Add backend-specific evaluation**
  - Keep the existing Presidio/spaCy evaluation as the reference.
  - Add optional evaluation jobs for direct spaCy or ONNX backends when they
    exist.

---

## Phase 2G — Product Documentation

Goal: communicate the system as a local privacy-preserving de-identification
service, not only a Presidio recognizer package.

- [ ] **2G.1 Add architecture overview**
  - `docs/architecture/local_deid_service.md`.
  - Include:
    - local-only trust boundary;
    - orchestrator-before-LLM pattern;
    - detection vs transformation vs audit;
    - Presidio adapter role;
    - high-throughput native path.

- [ ] **2G.2 Add API documentation**
  - Request/response examples for `/scan` and `/deidentify`.
  - Policy examples.
  - Error examples.
  - Audit event examples without raw PII.

- [ ] **2G.3 Update README positioning**
  - Current README can keep Presidio-first quickstart.
  - Add a roadmap note: the project is moving toward reusable local
    de-identification components, with Presidio as the first adapter.

- [ ] **2G.4 Update paper framing later**
  - Keep the paper scoped to the Presidio-backed evaluation unless Phase 2 is
    complete and evaluated.
  - Mention framework-neutral specs and future high-throughput implementation
    only as future work unless measured.

---

## Suggested Execution Order

1. Finish current Phase 1 Canada/paper-critical work from
   `IMPLEMENTATION_PLAN.md`.
2. Start Phase 2A: specs + core validators + generic Python scanner.
3. Convert Presidio recognizers into thin adapters over the specs.
4. Add Phase 2B transformation policies and engine.
5. Add Phase 2C local service and orchestrator examples.
6. Add Phase 2D audit/retention/security lifecycle.
7. Begin Phase 2E Rust/native engine once the core spec contract is stable.
8. Add optional full-text NER backends only after deterministic identifier
   parity is locked.

---

## Phase 1 Plan Changes Implied by Phase 2

Keep `IMPLEMENTATION_PLAN.md` mostly intact for the paper and initial release,
but make these small positioning changes when convenient:

- State that Presidio is the **initial adapter**, not the long-term core.
- Avoid describing recognizers as the only product surface; describe the
  reusable identifier rules, validators, provenance docs, and benchmark as the
  durable project assets.
- Keep Canada-first and India-freeze policies unchanged.
- Keep all current evaluation gates unchanged; they become the compatibility
  contract for future non-Presidio engines.
- Add a short pointer from `IMPLEMENTATION_PLAN.md` to this Phase 2 plan after
  Phase 5 or in a new roadmap note.

