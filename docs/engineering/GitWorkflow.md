# Git Workflow

## Branch Naming

- Use lowercase, hyphenated branch names.
- Prefix by intent:
	- `feature/<ticket-or-scope>`
	- `fix/<ticket-or-scope>`
	- `refactor/<ticket-or-scope>`
	- `design/<ticket-or-scope>`
	- `docs/<ticket-or-scope>`
- Include the work item when available (example: `feature/PTMS-024-money-scalar-arithmetic`).

## Commit Message Format

- Follow Conventional Commits.
- Allowed types in this repository: `feat`, `fix`, `docs`, `refactor`.
- Format:

```text
<type>(<scope>): <short summary>
```

- Examples:
	- `feat(money): support money-to-money ratio division`
	- `docs(adr): add assessment year parsing decision`

## PR Expectations

- Open PRs against `main` unless explicitly planned otherwise.
- Use the PR template in `.github/pull_request_template.md`.
- Fill all sections: Why, What, How, Tests, Documentation, ADR, Review Checklist.
- Keep PRs focused and scoped to one concern where possible.
- Include evidence of validation (lint, type-check, tests).

## RFC Process

- Create an RFC in `docs/rfcs/` for new domain capabilities or major behavior changes.
- RFC status starts as `Draft`.
- RFC must define:
	- Summary
	- Motivation
	- Goals and Non-Goals
	- Alternatives
	- Risks
	- Success Criteria
- After review alignment, promote key decisions into ADRs.

## ADR Process

- Create ADRs in `docs/adr/` with incremental numbering.
- ADRs are historical records; do not rewrite accepted intent retroactively.
- Each ADR should include:
	- Status
	- Context
	- Decision
	- Consequences
	- Scope and Non-Goals (when applicable)
	- Related RFC/ADR links
- If a decision changes, write a new ADR that supersedes the prior one.

## Review Checklist

- Correctness
- Simplicity
- Readability
- Tests
- Documentation
- Type Safety
- Backward Compatibility
- Performance (when relevant)

## Release Process

- Merge approved PRs into `main` through the standard review flow.
- Ensure CI is green before merge.
- Use Conventional Commits to support semantic versioning and release notes.
- Tag releases following SemVer.
- Publish release notes summarizing user-visible changes and migration notes.
