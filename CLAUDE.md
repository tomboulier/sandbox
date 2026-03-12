# sandbox — Instructions for Claude Code

## Project

CLI Python tool to manage the lifecycle of development experiments.
Commands: `new`, `ls`, `graduate`, `demote`, `find`.

## Stack

- Python 3.11+, `src/` layout
- `uv` for dependency management
- `ruff` for linting and formatting (replaces black + flake8 + isort)
- `mypy` in strict mode
- `pytest` with TDD approach

## Commands

```bash
uv sync                  # install dependencies
uv run pytest            # run tests
uv run ruff check .      # lint
uv run ruff format .     # format
uv run mypy src          # type check
```

## Conventions

See `CONTRIBUTING.md` for the full guide. Key points:

**Commits — Conventional Commits:**
- Format: `<type>(<scope>): <description>`
- Imperative mood, English, max 72 chars, no trailing period
- One logical change per commit — if you write "and", split the commit

**Code:**
- Type hints on every function
- Docstrings in numpydoc format on all public API
- KISS, YAGNI, SOLID, DRY
- Clean Code (Bob Martin): small functions, single responsibility, no magic numbers
- TDD: write the test first

**Do not:**
- Add features not explicitly requested (YAGNI)
- Add comments that just restate the code
- Refactor code outside the scope of the current task
