# ADR-009: AssessmentYear Parsing

## Status

Proposed

## Context

Assessment Year values will enter PTMS through user input, imports, and external integrations.

Without a consistent parsing policy, multiple incompatible AY text formats will appear across modules and increase validation defects.

RFC-001 identifies parsing as a key risk and calls for incremental hardening.

## Decision

PTMS parsing for `AssessmentYear` will be strict in v1 while supporting a small set of explicit formats.

### Accepted Inputs

The parser accepts:

- `2026`
- `AY 2026-27`
- `2026-2027`

### Strictness Policy

- Parsing is strict, not permissive.
- Input must match one of the accepted formats exactly after trimming leading/trailing whitespace.
- Invalid tokens (for example `A.Y. 2026-27`, `26-27`, `AY2026-27`) are rejected.
- Year continuity is validated (`end_year == start_year + 1`).

### Canonicalization

- Parsed output normalizes to a single canonical object (`AssessmentYear(start_year=2026)`).
- String rendering from the value object should be canonical and deterministic.

## Alternatives Considered

### 1. Permissive parsing

Rejected.

Reason:

- Encourages ambiguous input handling.
- Makes validation behavior harder to reason about.

### 2. Single-format parsing only

Rejected.

Reason:

- Too restrictive for realistic ingress paths.
- Forces avoidable normalization work onto every caller.

## Invariants

- Accepted formats normalize to the same canonical `AssessmentYear` value.
- Invalid formats are rejected deterministically.
- Parsing never changes the canonical internal representation.

## Consequences

### Positive

- Predictable and testable parser behavior.
- Lower ambiguity between FY and AY.
- Better data quality at entry points.

### Negative

- Some real-world variants are intentionally rejected.
- Integrations may need pre-normalization before PTMS parse.

## Future Evolution

- Additional human formats may be added only via new ADR or ADR amendment decision.
- Any expansion must preserve backward compatibility of existing accepted formats.

## Out of Scope

- User-interface-specific formatting beyond canonical domain parsing.
- Historical tax-law interpretation tied to specific year labels.
- Fuzzy or heuristic parsing of malformed inputs.

## Validation

This ADR is considered implemented when:

- [ ] Unit tests exist
- [ ] Documentation updated
- [ ] MyPy passes
- [ ] Ruff passes
- [ ] Public API documented

## Related

- ADR-001 Clean Architecture
- ADR-008 AssessmentYear Value Object.
- ADR-010 AssessmentYear and FinancialYear Relationship.
- RFC-001 Assessment Year Domain Model.