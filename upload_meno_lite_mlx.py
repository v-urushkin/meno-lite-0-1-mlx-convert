"""Upload the converted MLX model to the Hugging Face Hub."""

import sys
from pathlib import Path
from typing import Any

import yaml
from huggingface_hub import HfApi, get_token

CONFIG_PATH = Path(__file__).with_suffix(".yaml")


def load_config(path: Path) -> dict[str, Any]:
    """Load the upload configuration from a YAML file.

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


def validate_repo_id(repo_id: str) -> None:
    """Ensure the repository identifier looks like '<namespace>/<repo-name>'.

    Args:
        repo_id: Repository identifier, e.g. "your-username/meno-lite-0.1-mlx-mxfp8".

    Exits:
        The process with code 1 if the identifier is a placeholder or malformed.
    """
    if repo_id.startswith("YOUR_USERNAME") or "/" not in repo_id:
        sys.exit(
            f"[ERROR] Invalid repo_id: {repo_id!r}. Expected '<namespace>/<repo-name>' "
            "(e.g. 'your-username/meno-lite-0.1-mlx-mxfp8'). "
            "Edit upload_meno_lite_mlx.yaml."
        )


def validate_local_model(local_path: Path) -> list[Path]:
    """Validate that the local model directory is ready for upload.

    Args:
        local_path: Directory with the converted model.

    Returns:
        Sorted list of files that will be uploaded.

    Exits:
        The process with code 1 if the directory is missing or incomplete.
    """
    if not local_path.is_dir():
        sys.exit(f"[ERROR] Model directory not found: {local_path}")
    files = sorted(p for p in local_path.rglob("*") if p.is_file())
    names = {p.name for p in files}
    if "config.json" not in names:
        sys.exit(f"[ERROR] 'config.json' not found in {local_path}")
    if not any(p.suffix == ".safetensors" for p in files):
        sys.exit(f"[ERROR] No .safetensors files found in {local_path}")
    return files


def main() -> None:
    """Create the target repo (if needed) and upload the model files."""
    config = load_config(CONFIG_PATH)
    local_path = Path(config["local_path"])
    repo_id = str(config["repo_id"])
    private = bool(config.get("private", False))

    validate_repo_id(repo_id)
    files = validate_local_model(local_path)

    if not get_token():
        sys.exit(
            "[ERROR] No Hugging Face token found. "
            "Set the HF_TOKEN environment variable or run 'hf auth login'."
        )

    api = HfApi()
    print(f"Files to upload ({len(files)}):")
    for file in files:
        print(f"  {file.relative_to(local_path)}")

    print(f"Creating repo {repo_id} (private={private}) ...")
    api.create_repo(repo_id=repo_id, repo_type="model", private=private, exist_ok=True)

    print(f"Uploading {local_path} -> {repo_id} ...")
    api.upload_folder(
        repo_id=repo_id,
        folder_path=local_path,
        repo_type="model",
        commit_message="Upload meno-lite-0.1-mlx-mxfp8 (MLX, mxfp8 8-bit)",
    )

    print(f"Done: https://huggingface.co/{repo_id}")


if __name__ == "__main__":
    main()
