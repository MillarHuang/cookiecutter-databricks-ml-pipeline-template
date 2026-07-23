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

### New project (creates a fresh folder)

```bash
# With uv (no install needed)
uvx cookiecutter path/to/cookiecutter-databricks-ml-pipeline

# Or with pip
pip install cookiecutter
cookiecutter path/to/cookiecutter-databricks-ml-pipeline
```

### Into an existing (cloned) repo

Cookiecutter always generates a `<project_slug>/` folder — it cannot flatten its
output into the current directory. To fill an empty repo you just cloned from
Azure DevOps, generate into the **parent** directory with the slug set to the
repo folder's exact name, and `-f` to allow writing into the existing folder:

First install cookiecutter and go to the repo folder location:
```bash
pip install cookiecutter
cd path\to\my-repo
```
Then use cookiecutter to generate the template (replacing `my-repo` with your actual repo folder name.)
```bash
# - -o .. — tells cookiecutter to put its output one level above your repo, in the parent folder.
# - project_slug=my-repo — forces the generated folder's name to be identical to your repo folder's name.
# - -f — permits writing into a folder that already exists instead of erroring.
cookiecutter "https://github.com/MillarHuang/cookiecutter-databricks-ml-pipeline-template.git" -o .. -f project_slug=my-repo
```

or 

```bash
cd path/to/my-cloned-repo
uvx cookiecutter path/to/cookiecutter-databricks-ml-pipeline -o .. -f project_slug=my-cloned-repo
```

The generated files land directly inside `my-cloned-repo/` and your `.git`
folder is left untouched. Hyphens in the repo name are fine: `package_name` is
sanitized independently (`my-cloned-repo` → package `my_cloned_repo`), and the
places that use `project_slug` (pyproject name, bundle name, experiment names)
all accept hyphens. Skip `git init` in the post-generation steps.

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
git init   # skip if you generated into an existing cloned repo
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
