# ADR-006: ISO Standards

## Status

Accepted

## Context

PTMS processes tax and portfolio data across multiple jurisdictions and data sources.

Without standardized identifiers and formats, the platform risks inconsistent parsing, duplicate mappings, and ambiguous reporting outputs.

To keep core domain behavior deterministic, PTMS needs explicit standards for country codes, currency codes, and date representations.

## Decision

PTMS adopts the following ISO standards as canonical defaults in domain and persistence-facing boundaries.

### 1. Country Codes

- Standard: ISO 3166-1 alpha-2.
- Representation: two-letter uppercase country code.
- PTMS domain type: `CountryCode` enum.

Examples:

- `IN`, `US`, `GB`, `SG`.

### 2. Currency Codes

- Standard: ISO 4217 alphabetic currency codes.
- Representation: three-letter uppercase currency code.
- PTMS domain type: `CurrencyCode` enum.

Examples:

- `INR`, `USD`, `GBP`, `SGD`.

### 3. Dates and Period Strings

- Standard: ISO 8601 for machine-readable dates and date-like strings.
- Canonical date format: `YYYY-MM-DD`.
- Canonical year format (where applicable): `YYYY`.

### 4. Casing and Normalization

- Inputs may be normalized at ingress boundaries.
- Internal domain values must remain canonical uppercase ISO codes.

## Scope

This ADR governs:

- Domain primitives and enums for country and currency identity.
- API/request/response contracts that carry these identifiers.
- Storage and export layers that require stable machine-readable formats.

This ADR does not govern:

- Human-friendly localized display text.
- Exchange rate sourcing.
- Country- or currency-specific legal calculations.

## Rationale

- ISO standards reduce ambiguity in integrations.
- Standards-aligned enums improve type safety and validation.
- Canonical formats simplify joins, lookups, and long-term maintenance.

## Consequences

### Positive

- Consistent identifiers across modules and services.
- Fewer data-quality defects from free-form strings.
- Cleaner interoperability with external datasets and tools.

### Negative

- Legacy or non-ISO inputs require normalization/adapters.
- Some edge-case external naming conventions may be rejected until mapped.

## Alternatives Considered

### 1. Free-form strings everywhere

Rejected.

Reason:

- No canonical validation.
- High risk of drift and typo defects.

### 2. Vendor-specific codes only

Rejected.

Reason:

- Locks PTMS to specific data providers.
- Reduces portability and transparency.

## Implementation Notes

- `CountryCode` and `CurrencyCode` enums are authoritative in the domain layer.
- Unknown inbound identifiers must fail fast or be mapped explicitly in adapters.
- Future extensions should preserve ISO compatibility and avoid introducing parallel code systems.

## Related

- ADR-007 Money Value Object.
- RFC-001 Assessment Year Domain Model.