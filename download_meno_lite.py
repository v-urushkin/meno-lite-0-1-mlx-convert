"""Download the bond005/meno-lite-0.1 model from the Hugging Face Hub."""

from pathlib import Path

from huggingface_hub import snapshot_download

REPO_ID = "bond005/meno-lite-0.1"
TARGET_DIR = Path("original_models") / "meno-lite-0.1"


def download_model(repo_id: str, target_dir: Path) -> Path:
    """Download a full model snapshot from the Hugging Face Hub.

    Args:
        repo_id: Repository identifier, e.g. "bond005/meno-lite-0.1".
        target_dir: Local directory to store the downloaded snapshot.

    Returns:
        Path to the directory with the downloaded files.
    """
    return Path(snapshot_download(repo_id=repo_id, local_dir=target_dir))


def main() -> None:
    """Download the model into original_models/meno-lite-0.1."""
    print(f"Downloading {REPO_ID} -> {TARGET_DIR} ...")
    path = download_model(REPO_ID, TARGET_DIR)
    print(f"Done: {path}")


if __name__ == "__main__":
    main()
