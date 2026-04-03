from pathlib import Path


def get_retro_stable_dir() -> Path:
    try:
        import retro  # type: ignore
    except ModuleNotFoundError as exc:
        raise RuntimeError("gym-retro is required for ROM installation.") from exc

    retro_directory = Path(retro.__file__).resolve().parent
    return retro_directory / "data" / "stable"

