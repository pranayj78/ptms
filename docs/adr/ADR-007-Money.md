# ADR-007: Money Value Object

## Status

Accepted

## Context

PTMS performs tax and portfolio calculations where numeric correctness is mandatory.
Using binary floating-point (`float`) can introduce rounding drift (for example, `0.1 + 0.2 != 0.3`),
which is unacceptable for financial domain logic.

We are introducing a core `Money` value object under `ptms.core.value_objects` and need a clear,
project-wide rule for how monetary amounts are represented and operated on.

## Decision

PTMS will represent money with:

1. `Decimal` for amount storage and arithmetic.
2. `CurrencyCode` enum for currency identity.
3. Immutable value-object semantics for `Money`.
4. Domain calculations preserve precision. Rounding occurs only at external boundaries such as reporting, exports, or user-facing presentation.
5. Validation that prevents money-to-money arithmetic between different currencies unless explicitly converted.
6. Scalar arithmetic support for multiplication and division by `int` and `Decimal`.
7. Division by `Money` returns a dimensionless `Decimal` ratio.
8. `Money * Money` is intentionally unsupported.

## Alternatives Considered

### 1. `float`

- Pros: fast and simple.
- Cons: binary precision errors; unsafe for financial correctness.

Decision: Rejected.

### 2. Integer minor units (for example paise/cents)

- Pros: exact arithmetic; high performance.
- Cons: more boilerplate for scaling, formatting, and mixed-currency support.

Decision: Not selected as the default for PTMS at this stage.

### 3. `Decimal` (selected)

- Pros: exact decimal arithmetic, clear intent, Python standard library support.
- Cons: slower than `float`; requires disciplined quantization/rounding rules.

Decision: Accepted.

## Consequences

### Positive

- Financial calculations remain deterministic and audit-friendly.
- Domain code communicates intent clearly (`Money(amount, currency)` vs raw numbers).
- Currency mismatch bugs are caught early via validation.

### Negative

- Slight runtime overhead compared with `float`.
- Developers must avoid accidental `float` conversion and enforce decimal-safe inputs.
- Team must consistently apply rounding policy in I/O boundaries.

## Implementation Notes

1. `Money` should accept `Decimal | str | int` and normalize to `Decimal` internally.
2. Money constructors MUST reject float values to prevent accidental precision loss.
3. Define and document rounding mode (for example `ROUND_HALF_UP`) in one place.
4. Arithmetic rules:
    - `Money + Money` and `Money - Money`: only when currencies match.
    - `Money * scalar` and `Money / scalar`: allowed for `int` and `Decimal`.
    - `Money / Money`: allowed only when currencies match and returns `Decimal`.
    - `Money * Money`: unsupported.

### Operator Compatibility

> Public operator methods accept `object` and return `NotImplemented` for unsupported operand types. This follows Python's data model and allows reflected operations (`__radd__`, `__rsub__`, etc.) to participate before Python raises a `TypeError`.

Public interfaces should accurately model how the runtime interacts with the code, while internal validation should enforce domain invariants.

The domain model is permitted to be stricter than Python when doing so improves business correctness and readability.

5. Tests must cover:
    - precision behavior,
    - currency mismatch errors,
    - rounding/quantization behavior,
    - equality/hash semantics.

## Reference Implementation

```python
from decimal import Decimal

from ptms.core.enums import CurrencyCode
from ptms.core.value_objects import Money

grant = Money.of("6500.25", CurrencyCode.USD)
sale = Money.of("7200.75", CurrencyCode.USD)

gain = sale - grant
tax = gain * Decimal("0.30")
net = gain - tax
```


## Invariants

The following conditions must always hold true:

- A `Money` instance always has a valid `CurrencyCode`.
- Monetary amounts are represented using `Decimal`.
- `Money` instances are immutable.
- Money-to-money arithmetic operations require matching currencies.
- Operations never mutate existing instances.
- Precision is preserved; automatic rounding is not performed.

## Invalid Operations

The following operations are intentionally unsupported:

- Money + int
- Money + Decimal
- Money * Money
- Money + different currency

## Verification

The following behaviors must be verified through automated tests:

- [ ] Immutability
- [ ] Precision preserved
- [ ] Currency validated
- [ ] Equality semantics
- [ ] Hash semantics
- [ ] Invalid operations

## Scope

This ADR defines the core monetary abstraction used throughout PTMS.

It does not define:

- Tax calculations
- Exchange rates
- Currency conversion
- Reporting
- Localization
- Workbook formatting

Those concerns are addressed in separate components.

## Non-Goals

This ADR does not attempt to solve:

- Foreign exchange conversion
- Tax computation
- Currency formatting
- Jurisdiction-specific monetary rules
- Monetary allocation algorithms

## Future Evolution

This ADR intentionally limits the responsibilities of the `Money` value object.

The following concerns are out of scope and may be introduced through separate ADRs if required:

- Currency conversion and exchange rate management.
- Locale-aware formatting and display.
- Tax jurisdiction-specific rounding rules.
- Currency metadata (symbols, decimal precision, display names).
- Monetary allocation and distribution algorithms.
- Multi-currency portfolio calculations.

Future enhancements should preserve the Single Responsibility Principle.


## Approval

| Role | Status |
|------|--------|
| Author | Approved |
| Architecture Review | Approved |
| Implementation | Pending |
| Tests | Pending |