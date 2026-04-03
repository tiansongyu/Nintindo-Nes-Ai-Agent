from pathlib import Path


REQUIRED_ASSET_FILES = (
    "rom.nes",
    "rom.sha",
    "data.json",
    "metadata.json",
    "scenario.json",
)


def validate_asset_dir(asset_dir: Path) -> None:
    if not asset_dir.exists():
        raise FileNotFoundError(f"Missing asset directory: {asset_dir}")
    for file_name in REQUIRED_ASSET_FILES:
        file_path = asset_dir / file_name
        if not file_path.exists():
            raise FileNotFoundError(f"Missing required asset file: {file_path}")
    state_files = list(asset_dir.glob("*.state"))
    if not state_files:
        raise FileNotFoundError(f"Missing required state file in asset directory: {asset_dir}")

