# PTMS

Personal Tax Management System.
PTMS is an engineering-first platform for managing personal finance, tax compliance, investment tracking, and financial reporting with complete transparency and auditability.

PTMS exists because financial software should be transparent, reproducible, and understandable. Users should never have to trust a calculation they cannot inspect.

## Development Setup

1. Install dependencies:

	```bash
	uv sync --all-groups
	```

2. Install git hooks:

	```bash
	uv run pre-commit install
	uv run pre-commit install --hook-type commit-msg
	```

3. Run checks locally:

	```bash
	uv run pre-commit run --all-files
	uv run pytest -q
	```

## Conventional Commits

Commit messages are enforced through a commit-msg hook. Allowed types:

- `feat:`
- `fix:`
- `docs:`
- `refactor:`

Examples:

- `feat: add RSU vesting calculator`
- `fix: correct FIFO lot selection`
- `docs: update schedule FA guidance`
- `refactor: split tax rules service`

## Semantic Versioning

The project follows Semantic Versioning (`MAJOR.MINOR.PATCH`), for example:

- `0.1.0`
- `0.2.0`
- `1.0.0`

Current version is stored in `pyproject.toml` under `project.version`.

## CI

GitHub Actions workflow in `.github/workflows/ci.yml` runs on every push and pull request:

- Formatting check (`ruff format --check`)
- Linting (`ruff check`)
- Type checking (`mypy`)
- Tests (`pytest`)
