"""Configuration file for the project."""

from typing import Any

import yaml
from pydantic import BaseModel


class ExampleModelConfig(BaseModel):
    """Validation of a single sub-model configuration."""

    num_cols: list[str] = []
    cat_cols: list[str] = []
    target: str
    model_type: str
    parameters: dict[str, Any] = {}


class ProjectConfig(BaseModel):
    """Represent project configuration parameters loaded from YAML.

    Handles feature specifications, catalog details, and experiment parameters.
    Supports environment-specific configuration overrides.
    Extend this class with stricter validation models as the project grows.
    """

    catalog_name: str
    schema_name: str
    experiment_name: str
    experiment_id: str
    models: dict[str, ExampleModelConfig]

    @classmethod
    def from_yaml(cls, config_path: str, env: str = "dev") -> "ProjectConfig":
        """Load and parse configuration settings from a YAML file.

        Args:
            config_path: Path to the YAML configuration file
            env: Environment name to load environment-specific settings

        Returns:
            ProjectConfig instance initialized with parsed configuration

        """
        if env not in ["prd", "acc", "dev"]:
            raise ValueError(f"Invalid environment: {env}. Expected 'prd', 'acc', or 'dev'")

        with open(config_path) as f:
            config_dict = yaml.safe_load(f)
            config_dict["catalog_name"] = config_dict[env]["catalog_name"]
            config_dict["schema_name"] = config_dict[env]["schema_name"]
            config_dict["experiment_name"] = config_dict[env]["experiment_name"]
            config_dict["experiment_id"] = config_dict[env]["experiment_id"]

            return cls(**config_dict)


class Tags(BaseModel):
    """Represents a set of tags for a git commit.

    Contains information about the git SHA, branch, and job run ID.
    """

    git_sha: str
    branch: str
    job_run_id: str | None = None
