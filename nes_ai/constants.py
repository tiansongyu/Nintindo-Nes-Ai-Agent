from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent
ASSETS_DIR = PROJECT_ROOT / "assets" / "games"
ARTIFACTS_DIR = PROJECT_ROOT / "artifacts"
MODELS_DIR = ARTIFACTS_DIR / "models"
TENSORBOARD_DIR = ARTIFACTS_DIR / "tensorboard"
EVALUATIONS_DIR = ARTIFACTS_DIR / "evaluations"
LEGACY_MODEL_DIR = PROJECT_ROOT / "trained_models"

