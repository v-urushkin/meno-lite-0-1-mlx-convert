"""Convert bond005/meno-lite-0.1 to MLX with mxfp8 quantization."""

import sys
from pathlib import Path
from typing import Any

import yaml
from mlx_lm.convert import convert

CONFIG_PATH = Path(__file__).with_suffix(".yaml")


def load_config(path: Path) -> dict[str, Any]:
    """Load the conversion configuration from a YAML file.

    Args:
        path: Path to the YAML config file.

    Returns:
        Parsed configuration mapping.

    Raises:
        FileNotFoundError: If the config file does not exist.
    """
    if not path.is_file():
        raise FileNotFoundError(f"Config file not found: {path}")
    with path.open(encoding="utf-8") as file:
        return yaml.safe_load(file)


def ensure_target_free(mlx_path: Path) -> None:
    """Ensure the target model path is not already occupied.

    Args:
        mlx_path: Destination directory for the converted model.

    Exits:
        The process with code 1 if the path already exists.
    """
    if mlx_path.exists():
        sys.exit(f"[ERROR] Target path already exists: {mlx_path}")


def main() -> None:
    """Convert the model using settings from the adjacent YAML config."""
    config = load_config(CONFIG_PATH)
    ensure_target_free(Path(config["mlx_path"]))
    print(f"Converting with config {CONFIG_PATH}")
    convert(**config)


if __name__ == "__main__":
    main()
