# Agent Instructions for `cs_flickrgallery`

Welcome to the `cs_flickrgallery` repository. This is a Plone 6 add-on project designed to integrate Flickr galleries into a Plone CMS site.
Please follow these guidelines and conventions when assisting with this project.

## Project Architecture & Tech Stack

- **Framework:** Plone 6 (Classic UI & REST API compatible, depending on the specific implementation)
- **Language:** Python 3.10+
- **Package Manager:** `uv`
- **Build System:** `hatchling`
- **Testing:** `pytest`, `pytest-plone`, `plone.app.testing`
- **Linting & Formatting:** `ruff`, `zpretty` (for ZCML)
- **Release Management:** `towncrier` (for changelogs)

## Build, Lint, and Test Commands

This project uses a `Makefile` to simplify common tasks. Behind the scenes, it relies heavily on `uv` to run commands in isolated virtual environments.

### Testing

Tests are located in the `tests/` directory.

- **Run all tests:**
  ```bash
  make test
  # or directly:
  uv run pytest
  ```
- **Run a single test file:**
  ```bash
  uv run pytest tests/test_behavior_something.py
  ```
- **Run a single test function/method:**
  ```bash
  uv run pytest tests/test_behavior_something.py::test_my_specific_feature
  ```
- **Run tests with coverage:**
  ```bash
  make test-coverage
  # or directly:
  uv run pytest --cov=cs_flickrgallery --cov-report term-missing
  ```

### Linting and Formatting

We use `ruff` for fast Python linting and formatting, and `zpretty` for Plone `.zcml` files.

- **Check and fix formatting:**
  ```bash
  make format
  # This runs: ruff check --select I --fix, ruff format, and zpretty -i src
  ```
- **Run linters:**
  ```bash
  make lint
  # This runs: ruff check --fix, pyroma, check-python-versions, and zpretty --check
  ```
- **Run both formatting and linting:**
  ```bash
  make check
  ```

### Plone Instance Commands

- **Install dependencies and create configuration:** `make install`
- **Start the local Plone instance:** `make start`
- **Start a Python console connected to Plone:** `make console`

## Code Style and Conventions

### Python Formatting & Imports
- **Line Length:** 88 characters (`ruff` default).
- **Import Sorting:** `ruff` is configured to format imports using single lines (`force-single-line = true`) and without distinct sections (`no-sections = true`). Always run `make format` to let `ruff` handle imports automatically.
- **Strings:** Prefer double quotes `"` over single quotes `'` for strings.

### Typing
- Plone has a rich history of using `zope.interface` for typing and component registration. Use interfaces in `interfaces.py` to define schemas for behaviors, control panels, and content types.
- For standard Python functions and methods, modern type hints (`typing` module) are encouraged.

### Naming Conventions
- **Files & Modules:** `snake_case`
- **Classes:** `PascalCase`
- **Functions, Methods, & Variables:** `snake_case`
- **Constants:** `UPPER_SNAKE_CASE`
- **Interfaces:** Prefix with `I`, e.g., `IFlickrSettings`.

### Plone Specifics
- **ZCML:** Plone components (views, behaviors, indexers) must be registered via `.zcml` files. Always check existing `configure.zcml` files. Run `zpretty -i src` to format ZCML correctly (part of `make format`).
- **Dependencies:** If you need to add a Python dependency, update `pyproject.toml` (`[project]` -> `dependencies`).
- **Translations:** Wrap translatable strings in the Plone message factory, typically imported as:
  ```python
  from cs_flickrgallery import _
  ```

### Error Handling
- Use Python's built-in exceptions where applicable.
- For Plone-specific errors (e.g., unauthorized access, not found), use exceptions from `zExceptions` (e.g., `NotFound`, `Unauthorized`).
- Provide clear, descriptive error messages. Do not swallow exceptions implicitly; always handle them or allow them to bubble up appropriately.

## Changelog
When adding a feature or fixing a bug, you must add a news fragment for `towncrier` in the `news/` directory.
Example: `echo "Added Flickr synchronization view." > news/123.feature`
Valid types are: `feature`, `bugfix`, `documentation`, `tests`, `internal`, `breaking`.

## Role as an AI Agent
- Do not assume external libraries are present unless specified in `pyproject.toml`.
- When modifying code, always look at surrounding imports and patterns to ensure your changes are idiomatic to the `cs_flickrgallery` codebase.
- Avoid introducing inline comments unless the logic is complex or unintuitive; code should largely be self-documenting.
- If asked to create a new module, test, or Plone component, try to model it after an existing one in the repository to maintain structure.
- **Mandatory Final Step:** Whenever you modify code, always verify it compiles and conforms to standards by running the appropriate linting, formatting, or test commands before confirming completion with the user.
