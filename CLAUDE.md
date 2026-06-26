# CLAUDE.md

Guidance for working in this repository.

## Tooling

- **Always use `uv` / `uvx`. Never use `pip`, `pip install`, `python -m pip`, `pipx`, `poetry`, or `virtualenv` directly.**
  - Run one-off tools with `uvx` (e.g. `uvx pip-audit`, `uvx ruff`).
  - Manage environments and dependencies with `uv` (e.g. `uv venv`, `uv pip install`, `uv run`, `uv sync`).

## Project

- Python package: `ambra_sdk` (distributed as `ambra-sdk-brainkey`).
- Build backend: Hatchling (migrated from Poetry).
- Lockfile: `uv.lock` (regenerate with `uv lock`). The old `poetry.lock` has been removed.
- Supports Python >= 3.10.
- Audit dependencies with `uvx pip-audit -r <(uv export --all-extras --no-hashes --no-emit-project)`.
