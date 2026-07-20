# PTMS Engineering Manifesto
## Principle #0

The Project Wins

Who wins does not matter.

The project should win.

We all learn.

Prefer simplicity over cleverness.

A solution that is easy to understand, test, and maintain is usually the right solution.

## Our Mission

Build a transparent, trustworthy, and extensible financial platform that empowers professionals to understand and manage their taxes rather than simply calculate them.

---

## Engineering Principles

### 1. Truth Over Convenience

Every number must be traceable to its source.

No hidden calculations.

No unexplained assumptions.

---

### 2. Business Logic Is Independent

Business rules never belong in Excel, the CLI, or the UI.

They belong in the domain layer.

---

### 3. Explainability

Every calculation should answer:

Why?

How?

Where did this come from?

---

### 4. Test Everything

If a tax rule cannot be tested,
it should not exist.

---

### 5. Small Modules

Prefer many small components over one large one.

---

### 6. Documentation Is Code

If architecture changes,

documentation changes.

---

### 7. Backwards Compatibility

Opening last year's project
should always work.

---

### 8. Automation Before Manual Work

If something is repeated,

it should eventually become automated.

---

### 9. Security

Financial data belongs to the user.

Privacy is a first-class requirement.

---

### 10. Engineering Craftsmanship

Write code that you would be proud to maintain five years from now.

---

### 11. Preserve Data Fidelity

PTMS domain objects never silently:

- round,
- normalize,
- truncate,
- format,
- localize.

They preserve the exact business value.

Formatting belongs to the presentation layer.


Engineering Rules

I propose these become permanent.

The Project Wins.

Business Logic Before UI.

Everything is Tested.

Everything is Explainable.

Everything is Traceable.

Everything is Versioned.

Everything is Reproducible.

Leave the Code Better Than You Found It.