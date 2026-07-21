# ADR-010: AssessmentYear and FinancialYear Relationship

## Status

Proposed

## Context

Indian tax logic uses both Financial Year (FY) and Assessment Year (AY), and they are offset by one year.

Confusion between AY and FY is a known domain risk from RFC-001, so the relationship must be explicit and deterministic.

## Decision

PTMS will model `FinancialYear` as a separate value object and compute AY/FY conversion, not duplicate stored state.

### Storage Strategy

- `AssessmentYear` stores only AY canonical state (`start_year`).
- `FinancialYear` stores only FY canonical state (`start_year`).

### Conversion Strategy

- `AssessmentYear.financial_year` is computed from AY (`FY.start_year = AY.start_year - 1`).
- `FinancialYear.assessment_year` is computed from FY (`AY.start_year = FY.start_year + 1`).

### Eager vs Lazy

- Conversion may be implemented as a computed property (lazy by access).
- No cached duplicate field is stored in either object in v1.
- Conversion is O(1), so caching provides negligible benefit while introducing consistency risks.
- Conversion methods never mutate either value object.

## Alternatives Considered

### 1. Store both AY and FY on each object

Rejected.

Reason:

- Duplicates derived state.
- Introduces consistency and synchronization risk.

### 2. Model only AssessmentYear and use raw integers for FY

Rejected.

Reason:

- Weakens domain clarity.
- Loses type safety for a distinct business concept.

## Invariants

- AY and FY conversion is deterministic and reversible.
- Conversion never mutates either value object.
- No cached duplicate year state is stored in v1.

## Rationale

- Keeps each value object single-purpose and immutable.
- Prevents drift from duplicated AY/FY state.
- Maintains explicit ubiquitous language in domain APIs.

## Consequences

### Positive

- Clear separation of concepts.
- Simple and reliable conversion rules.
- Safer type-level modeling in services and validation.

### Negative

- Requires an additional value object (`FinancialYear`) in foundation scope.
- Existing code using raw integers will need migration.

## Out of Scope

- Tax law rate tables.
- Year-specific legal rule activation.
- Localization and presentation formatting.

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
- ADR-009 AssessmentYear Parsing.
- RFC-001 Assessment Year Domain Model.