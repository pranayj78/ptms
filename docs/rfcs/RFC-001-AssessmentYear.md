# RFC-001 — Assessment Year Domain Model

**Status:** Reviewed

**Authors:** Pranay Joshi

**Reviewers:** PTMS Architecture Review

**Target Release:** Foundation v2.0

---

# 1. Summary

Introduce a first-class `AssessmentYear` value object that models the assessment year used throughout the Indian Income Tax system.

The Assessment Year will become one of the core domain primitives and will be used by every tax computation, tax return, validation rule, and reporting feature within PTMS.

---

# 2. Motivation

Currently PTMS has a production-ready `Money` value object.

However, almost every business rule in Indian taxation is dependent on the applicable Assessment Year.

Examples include:

- Income tax slab rates
- Standard deduction
- Section deduction limits
- Capital gains rules
- Rebate calculations
- Surcharge thresholds
- Validation rules
- Supported ITR forms

Without a first-class Assessment Year object these rules would eventually become scattered across the codebase.

---

# 3. Goals

The Assessment Year should:

- represent a valid Indian Assessment Year
- be immutable
- support comparison
- support equality and hashing
- provide a canonical string representation
- support conversion to Financial Year
- become a reusable domain primitive

---

# 4. Non-Goals

The first version will **not**:

- calculate tax slabs
- validate deduction limits
- understand CBDT notifications
- support historical law changes

Those responsibilities belong to higher-level domain services.

---

# 5. Why a Value Object?

Assessment Year has no identity.

These represent the same concept:

```python
AssessmentYear(2026)
AssessmentYear.of(2026)
AssessmentYear.parse("AY 2026-27")
```

Therefore it satisfies the DDD definition of a Value Object.

---

# 6. Ubiquitous Language

| Term | Meaning |
|------|---------|
| Assessment Year | Year in which income is assessed |
| Financial Year | Year in which income is earned |
| AY | Assessment Year |
| FY | Financial Year |

---

# 7. Proposed Public API (Illustrative)

```python
AssessmentYear.of(2026)

AssessmentYear.parse("AY 2026-27")

str(ay)

repr(ay)

ay.start_year

ay.end_year

ay.financial_year

ay.next()

ay.previous()
```

This is illustrative only; the ADR will finalize the API.

---

# 8. Alternatives Considered

## Option A

Represent Assessment Year as an `int`.

Rejected.

Lacks expressiveness and validation.

---

## Option B

Represent Assessment Year as a `str`.

Rejected.

Allows invalid values and requires repeated parsing.

---

## Option C

Dedicated immutable Value Object.

**Chosen.**

Consistent with our Money implementation and DDD principles.

---

# 9. Risks

- Confusion between FY and AY.
- Supporting future tax law changes.
- Parsing multiple human-readable formats.

These will be addressed incrementally.

---

# 10. Success Criteria

The RFC will be considered successful when:

- Assessment Year is implemented as a Value Object.
- All tests pass.
- API is documented.
- ADR is approved.
- PTMS uses Assessment Year instead of primitive integers.

---

# 11. Related ADRs

- ADR-008 AssessmentYear Value Object
- ADR-009 AssessmentYear Parsing
- ADR-010 AssessmentYear and FinancialYear Relationship
