# ADR-008: AssessmentYear Value Object

## Status

Proposed

## Context

PTMS requires a stable and explicit representation of the Indian Assessment Year across tax computation, validation, and reporting workflows.

Using primitives (`int` or `str`) would scatter validation and formatting logic and make domain rules harder to reason about.

RFC-001 defines `AssessmentYear` as a foundational domain primitive and positions it alongside existing value objects such as `Money`.

## Decision

PTMS will introduce `AssessmentYear` as an immutable value object.

### Immutability

- Instances are immutable after construction.
- Any transformation (for example `next()` or `previous()`) returns a new instance.

### Internal Representation

- Canonical internal representation is `start_year: int`.
- `end_year` is derived as `start_year + 1`.
- Construction validates Indian AY shape (consecutive years).

### Canonical Representation

The canonical string representation of an AssessmentYear is:

`AY 2026-27`

### Equality

- Two `AssessmentYear` values are equal when `start_year` matches.
- Equality is value-based, not identity-based.

### Comparison

- Ordering reflects chronological ordering of Assessment Years.
- `AssessmentYear(2026) > AssessmentYear(2025)` is valid and meaningful.

### Hashing

- Hash is derived from immutable value state (`start_year`).
- Equal objects must produce equal hashes.

## Invariants

AssessmentYear

- `start_year` is immutable
- `end_year == start_year + 1`
- equality uses `start_year`
- ordering uses chronological order

## Consequences

### Positive

- Clear domain semantics for AY.
- Reusable primitive across modules.
- Safer APIs with centralized validation.

### Negative

- Requires migration away from primitive integers/strings.
- Adds one more core object to maintain and document.

## Out of Scope

- Tax slab computation.
- Deduction rule enforcement.
- Historical tax-law interpretation.

## Alternatives Considered

Primitive int

- No domain semantics
- No centralized validation

Primitive str

- Parsing required everywhere
- Easy to create invalid values

## Validation

This ADR is considered implemented when:

- [ ] Unit tests exist
- [ ] Documentation updated
- [ ] MyPy passes
- [ ] Ruff passes
- [ ] Public API documented

## Related

- ADR-001 Clean Architecture
- ADR-009 AssessmentYear Parsing
- ADR-010 AssessmentYear and FinancialYear Relationship
- RFC-001 Assessment Year Domain Model.
