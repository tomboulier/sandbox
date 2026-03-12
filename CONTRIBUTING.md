# Contributing

## Philosophy

- **KISS** — Keep It Simple. The simplest solution that works is the right one.
- **YAGNI** — Don't build what isn't needed yet.
- **SOLID** — Single responsibility, open/closed, Liskov substitution, interface segregation, dependency inversion.
- **Clean Code** — Code is read far more than it is written. Optimize for readability.
- **Small commits** — Each commit should represent one logical change. If you find yourself writing "and" in a commit message, split it.

## Commit messages — Conventional Commits

Format: `<type>(<scope>): <description>`

```
feat(cli): add `sandbox graduate` command
fix(config): resolve missing default path on first run
docs(readme): update installation instructions
refactor(core): extract path resolution to helper function
test(graduate): add edge case for missing target directory
chore(deps): bump ruff to 0.5.0
```

**Rules:**
- Description in English, imperative mood ("add", not "adds" or "added")
- Max 72 characters on the first line
- No period at the end
- Blank line between subject and body if body is present
- Body wrapped at 72 characters

**Types:** `feat` `fix` `docs` `style` `refactor` `test` `chore` `perf` `ci` `build`

Breaking changes: add `!` after the type (`feat!:`) and a `BREAKING CHANGE:` footer.

## Code style

- Type hints on every function signature
- Docstrings in numpydoc format on public functions and classes
- Functions do one thing (Single Responsibility)
- Prefer explicit over implicit
- No magic numbers — use named constants
- Tests before implementation (TDD)

## Workflow

1. Fork and create a branch: `git checkout -b feat/my-feature`
2. Write a failing test first
3. Implement until the test passes
4. `uv run ruff check . --fix && uv run ruff format .`
5. `uv run mypy src`
6. `uv run pytest`
7. Commit and open a PR
