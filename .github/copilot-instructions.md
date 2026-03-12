# Copilot Instructions

## Project

Python CLI tool (`sandbox`) to manage the lifecycle of development experiments.
`src/` layout, Python 3.11+, uv, ruff, mypy strict, pytest.

## Code conventions

- Type hints on every function signature
- Docstrings in numpydoc format on public functions and classes
- KISS, YAGNI, SOLID, DRY
- Small functions with single responsibility (Clean Code / Bob Martin)
- No magic numbers — use named constants
- No comments that restate the code — only explain *why*, never *what*

## Commit messages — Conventional Commits

Format: `<type>(<scope>): <description>`
- Imperative mood, English
- Max 72 characters on the first line
- No trailing period
- Types: feat, fix, docs, style, refactor, test, chore, perf, ci, build

## Tests

- TDD: write the failing test before the implementation
- One assertion per test when possible
- Test names describe the behaviour: `test_new_creates_dated_directory`

## Do not

- Suggest features not asked for (YAGNI)
- Add defensive code for cases that cannot happen
- Refactor outside the scope of the current task
