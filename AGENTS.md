# AGENTS.md

Guidelines for AI coding agents working in this repository.

## Project Overview

Python 3.14 application that scrapes Untappd beer data, tracks consumption stats
among friends ("Pivni valka"), monitors pub tap lists, and archives check-ins via
RSS. Outputs a static HTML dashboard published to GitHub Pages.

Package manager: **uv** (Astral). No virtual environment activation needed -- use
`uv run` for all commands.

## Build & Run Commands

| Command                  | Description                                   |
|--------------------------|-----------------------------------------------|
| `make test`              | Run full test suite (`uv run --dev -m pytest`) |
| `make lint`              | Lint with ruff (`uvx ruff check`)             |
| `make lint-fix`          | Auto-fix lint issues (`uvx ruff check --fix`) |
| `make format`            | Format code (`uvx ruff format`)               |
| `make mypy`              | Type-check (strict on src, relaxed on tests)  |
| `make ty`                | Experimental type-check (`uvx ty check`)      |
| `make coverage`          | Run tests with coverage report                |
| `make before-commit`     | format + test + lint-fix + mypy (run before committing) |

### Running a Single Test

```sh
# Single test file
uv run --dev -m pytest tests/pivni_valka/test_pivni_valka.py

# Single test function
uv run --dev -m pytest tests/pivni_valka/test_pivni_valka.py::test_parse_unique_beers_count

# Single test directory / module
uv run --dev -m pytest tests/notifier/

# With verbose output
uv run --dev -m pytest -v tests/pivni_valka/test_pivni_valka.py::test_parse_unique_beers_count
```

### Running the Application

```sh
make run-pivni-valka                 # Full run (scrapes + notifies)
make run-pivni-valka-notificationless # No push notifications
make run-pivni-valka-local           # Skip downloading, use cached data
make run-notifier                    # Run pub tap notifier
make run-archivist                   # Run RSS archiver
```

## CI Pipeline

On every push (`.github/workflows/tests.yml`), CI runs in parallel:
- `make test` (pytest)
- `make mypy` (type checking)
- `make lint` (ruff)
- Smoke tests for pivni-valka and notifier pipelines

All checks must pass before merging.

## Code Style

### Formatting & Linting

- **Ruff** with `lint.select = ["ALL"]` -- nearly every rule is enabled
- **Line length:** 120 characters
- **Target version:** py314
- Run `before-commit` before committing
- Use `# noqa: XXXX` sparingly and only with a specific rule code

### Imports

- Standard library first, third-party second, local third (enforced by ruff `I` rules)
- Use **absolute imports**: `from database.models import PivniValka`, not relative imports
- Unused imports are only allowed in `__init__.py` files (re-exports)

### Type Annotations

- **Full type annotations on all function signatures** in source code (mypy `--strict`)
- Tests do **not** require type annotations
- Use modern Python syntax: `dict[str, int]`, `list[str]`, `str | None`, `tuple[str, ...]`
- Use `Literal` for constrained string types
- Use SQLAlchemy `Mapped[...]` for ORM column types

### Naming Conventions

- `snake_case` for functions, variables, modules, file names
- `PascalCase` for classes: `PivniValka`, `BaseRobot`, `OrmRobot`
- `UPPER_SNAKE_CASE` for module-level constants: `ENCODING`, `BASE_URL`, `TIMEOUT`
- Prefix private methods/attributes with `_`: `_main()`, `_args`

### Error Handling

- Raise specific exceptions with clear messages: `raise ValueError("Cannot parse user profile.")`
- Define custom exception classes when appropriate: `class UserNotFoundError(Exception)`
- Use exception chaining: `raise ... from e`
- Use `r.raise_for_status()` after HTTP requests
- Check required env vars early and raise `OSError` with a descriptive message

### Data Classes & Patterns

- Use `@dataclass` extensively for structured data (`frozen=True`, `kw_only=True` where appropriate)
- Use `pathlib.Path` consistently -- never `os.path`
- Use `httpx` with HTTP/2 for HTTP requests -- not `requests`
- Use context managers for DB sessions and file I/O
- Template Method pattern: `BaseRobot.run()` calls `_main()` (override in subclasses)

### Test Conventions

- Framework: **pytest** (plain functions, no test classes)
- Test files mirror source structure: `tests/pivni_valka/test_pivni_valka.py`
- Every test gets a fresh in-memory SQLite DB (autouse fixture in `conftest.py`)
- Use `unittest.mock` for mocking (`mock.patch`, `MagicMock`)
- Use `pytest.raises` for exception assertions, check message via `excinfo.value`
- Magic values and `assert` are permitted in tests (ruff rules relaxed)
- Private member access is permitted in tests

### What NOT to Do

- Do not add docstrings -- all `D1xx` rules are intentionally disabled
- Do not use `os.path` -- use `pathlib.Path`
- Do not use `requests` -- use `httpx`
- Do not use relative imports
- Do not add type annotations to test functions

## Project Structure

```
untappd/
  archivist/         # RSS feed check-in archiver
  data/              # SQLite dumps (data_dump.sql, test_dump.sql)
  database/          # SQLAlchemy ORM models and DB utilities
  maintenance/       # One-off maintenance scripts
  notifier/          # Pub tap monitoring & push notifications
  pivni_valka/       # Main stats tracking module
    stats/           # Chart data and tile computations
  robot/             # Base runner abstractions (BaseRobot, OrmRobot)
  templates/         # Jinja2 HTML templates
  tests/             # pytest test suite (mirrors source layout)
  utils/             # Shared utilities (HTTP, templates, users)
  web/               # Generated static output (GitHub Pages)
  run_*.py           # Entry point scripts
  Makefile           # All dev commands
  pyproject.toml     # Project config (uv-managed)
  ruff.toml          # Linter/formatter config
```

## Database

- In-memory SQLite via SQLAlchemy ORM
- Persistence via SQL dump files in `data/`
- Production data: `data/data_dump.sql`
- Test fixture data: `data/test_dump.sql`
- Test detection: `"pytest" in sys.modules` switches to test DB automatically
