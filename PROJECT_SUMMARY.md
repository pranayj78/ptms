# PTMS — Project Summary

## Personal Tax Management System

PTMS is an engineering-first Python platform for managing Indian personal taxation,
investments, and financial reporting. It is being designed for taxpayers with domestic and
foreign assets, with a particular focus on transparency, reproducibility, auditability, and
explainable calculations.

The long-term product vision includes capital-gains computation, RSU and foreign-asset
tracking, FIFO-based lot accounting, Schedule FA working papers, tax-regime comparison, and
Excel/PDF reporting. PTMS is deliberately not intended to replace the Income Tax portal; it
aims to produce reliable, inspectable working papers that support tax filing.

## Current State

The repository currently represents the architecture and domain-foundation phase rather than
a finished end-user product. Implemented foundations include:

- Immutable, type-safe `Money`, `AssessmentYear`, and `FinancialYear` value objects.
- Decimal-based monetary arithmetic that rejects binary floating-point input, preserves
  precision, and prevents accidental cross-currency calculations.
- Strict parsing and validation for Indian Assessment Year and Financial Year concepts.
- Explicit, reversible AY/FY conversion without duplicated state.
- ISO-based currency and country codes and strongly typed enums for assets, events, documents,
  and tax regimes.
- A planned Clean Architecture boundary between domain logic, application services,
  persistence, imports, CLI, and reporting/presentation adapters.

## Engineering and Architecture Highlights

PTMS applies practices normally expected in a professionally maintained software product:

- **Domain-driven design:** Financial concepts are represented as first-class value objects
  rather than primitive strings and numbers. Domain invariants are enforced at construction
  boundaries.
- **Clean Architecture:** Business and tax rules are kept independent of Excel, CLI, database,
  and future web/API interfaces, allowing presentation and infrastructure to evolve without
  rewriting the core model.
- **Financial correctness:** `Decimal` is used instead of `float`; rounding is reserved for
  explicit presentation boundaries; money is immutable and currency-safe.
- **Strict Python quality controls:** Python 3.12, comprehensive type annotations, strict MyPy
  settings, Ruff formatting/linting, Pytest, pre-commit hooks, and a deterministic `uv.lock`.
- **Automated CI:** Every push and pull request checks formatting, linting, static types, tests,
  and semantic-version syntax.
- **Architecture governance:** Important choices are documented through RFCs and Architecture
  Decision Records, including alternatives, trade-offs, invariants, non-goals, and validation
  criteria.
- **Automated ADR review:** A custom Python static-analysis tool scans the implementation and
  generates an ADR/RFC compliance report in GitHub Actions, including pull-request feedback.
- **Traceable delivery process:** Work is decomposed into GitHub issues and small stories, then
  connected to focused branches, conventional commits, pull requests, tests, and documentation.
- **Review discipline:** The pull-request template explicitly covers motivation, design,
  testing, documentation, ADR impact, type safety, compatibility, and performance.

## Project Evidence

At the time of this summary, the repository contains:

- 44 commits and 10 merged pull requests.
- More than 30 GitHub issues used to capture architecture work, features, tests, and
  story-level tasks.
- 148 passing Pytest cases across the current domain foundation, including parameterized edge
  cases and invariant checks.
- More than 30 Markdown documentation files.
- Nine Architecture Decision Records and one reviewed RFC, supported by an ADR template and
  index.
- Three GitHub Actions workflows covering code quality, semantic versioning, and ADR/RFC
  compliance.
- A tagged `Moneyv1.0` domain milestone.

Examples of delivered work include foundational enums, the `Money` value object and its
arithmetic behavior, an `AssessmentYear` RFC followed by ADRs and implementation, AY/FY domain
conversion, canonical representations, and the automated architecture-compliance workflow.

## Development Approach and Use of AI

I built PTMS as a Java engineer deliberately applying architecture and delivery disciplines to
Python. AI tools, primarily ChatGPT during the work represented here, accelerated design
exploration, implementation, documentation, and review. I retained responsibility for domain
framing, decomposition, architectural direction, engineering standards, validation, and the
final decisions recorded in the repository.

The project demonstrates that I can use AI as an engineering multiplier while still following
a rigorous development lifecycle: define the problem, document decisions, model the domain,
implement in small increments, test invariants and edge cases, automate quality gates, and
maintain traceability from issue to pull request.

## Why This Project Is Relevant to a Python Architecture Role

PTMS shows transferable architecture skills beyond language syntax: careful domain modeling,
separation of concerns, immutable value semantics, explicit invariants, API design, strict type
safety, test-driven validation, CI automation, decision documentation, and incremental delivery.
It also shows an ability to learn the Python ecosystem quickly and use its idioms—dataclasses,
`Decimal`, `StrEnum`, Python's operator protocol, Pytest, MyPy, Ruff, and `uv`—rather than simply
translating Java patterns mechanically.

Repository: <https://github.com/pranayj78/ptms>
