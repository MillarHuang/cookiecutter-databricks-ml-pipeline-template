"""Post-generation hook: print next steps."""

PROJECT = "{{ cookiecutter.project_slug }}"

print(
    f"""
Project '{PROJECT}' generated successfully!

Next steps (run inside the project folder):
  git init                    # skip if you generated into an existing cloned repo
  uv sync --extra dev --link-mode=copy
  pre-commit install
  databricks bundle validate --target dev

Then fill in project_config.yml and the skeleton classes in src/.
"""
)
