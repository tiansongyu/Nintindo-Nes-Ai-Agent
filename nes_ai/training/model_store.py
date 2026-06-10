from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

from nes_ai.constants import EVALUATIONS_DIR, LEGACY_MODEL_DIR, MODELS_DIR, TENSORBOARD_DIR
from nes_ai.games.base import GameDefinition


@dataclass(frozen=True)
class ModelStore:
    """Filesystem layout for one game's models, logs and evaluations."""

    game: GameDefinition

    @property
    def model_dir(self) -> Path:
        return MODELS_DIR / self.game.slug

    @property
    def checkpoints_dir(self) -> Path:
        return self.model_dir / "checkpoints"

    @property
    def tensorboard_dir(self) -> Path:
        return TENSORBOARD_DIR / self.game.slug

    @property
    def evaluation_dir(self) -> Path:
        return EVALUATIONS_DIR / self.game.slug

    @property
    def latest_model_path(self) -> Path:
        return self.model_dir / "latest.zip"

    @property
    def training_log_path(self) -> Path:
        return self.model_dir / "training.log"

    def ensure_dirs(self) -> None:
        for directory in (self.checkpoints_dir, self.tensorboard_dir, self.evaluation_dir):
            directory.mkdir(parents=True, exist_ok=True)

    def resolve_model_path(self, model_ref: str = "latest") -> Path:
        if model_ref in {"latest", ""}:
            if self.latest_model_path.exists():
                return self.latest_model_path
            legacy = self.find_latest_legacy_model()
            if legacy is not None:
                return legacy
            raise FileNotFoundError(f"No model found for {self.game.slug}.")

        for candidate in (Path(model_ref), self.checkpoints_dir / model_ref):
            if candidate.exists():
                return candidate

        raise FileNotFoundError(f"Unknown model reference '{model_ref}' for {self.game.slug}.")

    def find_latest_legacy_model(self) -> Path | None:
        if not LEGACY_MODEL_DIR.exists():
            return None

        final_model = LEGACY_MODEL_DIR / f"ppo_{self.game.retro_game}.zip"
        if final_model.exists():
            return final_model

        pattern = re.compile(rf"ppo_{re.escape(self.game.retro_game)}_(\d+)_steps\.zip$")
        best_match = None
        best_step = -1
        for file_path in LEGACY_MODEL_DIR.glob("*.zip"):
            match = pattern.match(file_path.name)
            if match and int(match.group(1)) > best_step:
                best_step = int(match.group(1))
                best_match = file_path
        return best_match
