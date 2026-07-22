# {{ cookiecutter.project_name }}

{{ cookiecutter.project_description }}

## Setup

```bash
# Install all dependencies (use --link-mode=copy on Windows to avoid symlink issues)
uv sync --extra dev --link-mode=copy

# For running tests
uv sync --extra test

# Install pre-commit hooks
pre-commit install
```

## Code quality

```bash
uv run ruff check src/
uv run ruff format src/
uv run pre-commit run --all-files
```

## Testing

```bash
uv run pytest
uv run pytest --cov={{ cookiecutter.package_name }}
```

## Build & deploy

```bash
# Build Python wheel
uv build

# Validate the Databricks bundle
databricks bundle validate --target dev

# Deploy to a target environment (dev, test, acc, prd)
databricks bundle deploy --target dev

# Run the main deployment job
databricks bundle run deployment --target dev
```

## Architecture

Pipeline stages (each is a task in the `deployment` job in `databricks.yml`):

All pipeline parameters live in `project_config.yml`, loaded and validated by
`ProjectConfig` in `src/{{ cookiecutter.package_name }}/config.py`.

## CI/CD

- `.azure-pipelines/ci.yml` — pre-commit checks and tests on every push
- `.azure-pipelines/cd.yml` — deploys to `acc` then `prd` (manual approval) on merge to the `prd` branch
