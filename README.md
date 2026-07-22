# cookiecutter-databricks-ml-pipeline

A general Cookiecutter template for Databricks ML pipeline projects. It scaffolds
the standard structure used across our projects:

```
<project_slug>/
├── .azure-pipelines/          # CI (pre-commit + tests) and CD (acc → prd deploy)
├── .pre-commit-config.yaml    # ruff lint/format + hygiene hooks
├── databricks.yml             # Databricks Asset Bundle (dev / test / acc / prd targets)
├── project_config.yml         # Single source of truth for all pipeline parameters
├── pyproject.toml             # uv-managed dependencies, ruff, pytest config
├── version.txt                # Wheel version (setuptools dynamic version)
├── libs/                      # Private wheel dependencies (optional)
├── notebooks/                 # Exploration notebooks (excluded from pre-commit)
├── resources/                 # Extra bundle job/alert definitions (*.yml)
├── scripts/                   # Numbered job entry points (01 → 05)
├── src/<package_name>/        # Python package built into a wheel
└── tests/                     # pytest (local pyspark, no databricks-connect)
```

## Usage

```bash
# With uv (no install needed)
uvx cookiecutter path/to/cookiecutter-databricks-ml-pipeline

# Or with pip
pip install cookiecutter
cookiecutter path/to/cookiecutter-databricks-ml-pipeline
```

You will be prompted for:

| Variable | Meaning | Example |
|----------|---------|---------|
| `project_name` | Human-readable name | `Activity Model Warehouse` |
| `project_slug` | Folder + bundle name (auto-derived) | `activity_model_warehouse` |
| `package_name` | Python package under `src/` (auto-derived) | `activity_model_warehouse` |
| `project_description` | One-line description | |
| `databricks_host` | Workspace URL used in `databricks.yml` | |
| `notification_email` | Job email notifications + dev permissions | |
| `dev_catalog` / `acc_catalog` / `prd_catalog` | Unity Catalog per environment | |
| `schema_name` | UC schema for pipeline tables | |
| `python_version` | Python version for CI and pyproject | `3.12` |

## After generation

```bash
cd <project_slug>
git init
uv sync --extra dev --link-mode=copy   # --link-mode=copy avoids symlink issues on Windows/OneDrive
pre-commit install
databricks bundle validate --target dev
```

Then:

1. Fill in `project_config.yml` (source tables, model configs, processor parameters)
   and extend `ProjectConfig` in `src/<package>/config.py` to validate them.
2. Flesh out the skeleton classes in `src/<package>/` — the scripts in `scripts/`
   already wire them together in the right order.
3. Drop any private wheels into `libs/` and register them under `[tool.uv.sources]`
   in `pyproject.toml` plus the `libraries:` sections in `databricks.yml`.
4. In Azure DevOps, create the `databricks-acc-vars` / `databricks-prod-vars`
   variable groups (containing `DATABRICKS_HOST`), the `MLOPS_acc` / `MLOPS_prd`
   service connections, and a `Production` environment with manual approval.
