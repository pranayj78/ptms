Welcome

Thank you for contributing to PTMS.

PTMS is more than a tax calculator.

It is an engineering-first financial platform designed around transparency, auditability, explainability, and long-term maintainability.

We believe software quality comes from thoughtful design, disciplined engineering practices, and respectful collaboration.

Whether you're fixing a typo or implementing a new feature, your contribution helps make PTMS better.


Before opening a Pull Request ask yourself:

✓ Does this solve a real problem?

✓ Is the design simple?

✓ Can another engineer understand this in six months?

✓ Have I documented why I made this decision?

✓ Is this feature testable?

✓ Can the result be explained to a user?


## Workflow

1. Create an issue
2. Discuss the design
3. Implement
4. Test
5. Document
6. Review
7. Merge

## Branch Naming
feature/PTMS-004-core-enums

feature/PTMS-010-rsu-grant

fix/PTMS-024-fifo-bug

docs/PTMS-001-manifesto

refactor/PTMS-031-money

chore/github-actions

## Commit Messages
feat(core): add CountryCode enum

feat(domain): implement Employee aggregate

fix(rsu): correct FIFO allocation

docs(architecture): add event model

test(core): improve Money tests

ci(github): add MyPy workflow


## Definition of Done

A feature is not done until:

 Code completed
 Unit tests written
 Integration tests updated (if applicable)
 Ruff passes
 MyPy passes
 Documentation updated
 Public API documented
 ADR updated (if needed)
 Review completed
 CI passes


## Pull Request Checklist

Correctness

Readability

Naming

Architecture

Documentation

Tests

Future Extensibility

Performance

Security

## ADR Compliance Checklist

- [ ] Immutable
- [ ] Type-safe
- [ ] No hidden side effects
- [ ] Tested
- [ ] Documented
- [ ] Matches ADR



The project wins.

PTMS values ideas over opinions and evidence over ego.

Good engineering is collaborative.

The goal of every discussion is to improve the product, not to prove who is right.

Every review is an opportunity to learn.

Every contribution should leave the codebase better than it was found.


## Engineering Values

Transparency
Simplicity
Respect
Curiosity
Craftsmanship
Ownership
Automation
Continuous Learning


## Architecture
When in doubt,

choose the solution that is

easiest to understand,
easiest to test,
easiest to explain,
and easiest to maintain.