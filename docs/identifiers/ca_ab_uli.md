# CA_AB_ULI — Alberta Unique Lifetime Identifier / Personal Health Number

## Authoritative sources

- Alberta Netcare Learning Centre, *Person Directory* —
  <https://www.albertanetcare.ca/LearningCentre/Person-Directory.htm>
  (accessed 2026-07-06): the ULI is a unique, permanent number assigned to
  every person receiving health services in Alberta; it is referred to as
  the Alberta Personal Health Number (PHN) once the person is covered by
  the Alberta Health Care Insurance Plan (AHCIP).
- Alberta Health Services, *Patient Identification Policy PS-06* and AHS
  Meditech registration guides: the ULI is entered as a **9-digit** numeric
  identifier.
- Canadian URI Registry (FHIR NamingSystem
  `ca-ab-patient-healthcare-id`): ULI documented as Alberta Health's
  internal person identifier, equivalent to PHN in other jurisdictions.

## Rule implemented

- No public checksum or structure beyond "9 digits" is documented, so this
  recognizer is **context-gated**: pattern scores are set below the 0.35
  reporting threshold and only context-word boosting can surface a match.
- Patterns (`core/specs.py`): 5-4 digit groups separated by space, dash, dot
  or slash (score 0.2) or 9 contiguous digits (score 0.1) — both above `CA_HEALTH_CARD`'s floor so the
  province-specific label scores higher when both fire.
- Validator (`ca_ab_uli_plausible`): returns `False` for wrong shape or a
  single repeated digit (e.g. 000000000), `None` otherwise — never `True`,
  so the match keeps its low pattern score and context gating governs
  (three-state validator contract, see `docs/architecture/core_contract.md`).
- Context is **Alberta-specific only**: "uli", "alberta", "ahcip",
  "netcare". Generic wording ("health card 574839216") cannot attribute a
  9-digit number to a province, so such matches are reported as
  `CA_HEALTH_CARD` and never as `CA_AB_ULI`. Under Alberta context both
  labels are emitted on the same span (ULI at the higher score); Presidio
  does not collapse same-span results of different types.

## Known gaps

- Without a checksum, a bare 9-digit number with nearby health-card context
  is indistinguishable from a coincidental quantity; recall on
  context-free ULIs is intentionally sacrificed for precision (measured in
  the hard split's `no_context` variant).
- Whether Alberta ULIs have internal structure (ranges, era prefixes) is
  not public; none is assumed.
