from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

from nes_ai.constants import EVALUATIONS_DIR, LEGACY_MODEL_DIR, MODELS_DIR, TENSORBOARD_DIR
from nes_ai.games.base import GameDefinition


@dataclass(frozen=True)
class ModelStore:
    game: GameDefinition
    model_dir: Path
    checkpoints_dir: Path
    tensorboard_dir: Path
    evaluation_dir: Path
    latest_model_path: Path
    training_log_path: Path

    @classmethod
    def for_game(cls, game: GameDefinition) -> "ModelStore":
        model_dir = MODELS_DIR / game.slug
        return cls(
            game=game,
            model_dir=model_dir,
            checkpoints_dir=model_dir / "checkpoints",
            tensorboard_dir=TENSORBOARD_DIR / game.slug,
            evaluation_dir=EVALUATIONS_DIR / game.slug,
            latest_model_path=model_dir / "latest.zip",
            training_log_path=model_dir / "training.log",
        )

    def ensure_dirs(self) -> None:
        self.model_dir.mkdir(parents=True, exist_ok=True)
        self.checkpoints_dir.mkdir(parents=True, exist_ok=True)
        self.tensorboard_dir.mkdir(parents=True, exist_ok=True)
        self.evaluation_dir.mkdir(parents=True, exist_ok=True)

    def resolve_model_path(self, model_ref: str = "latest") -> Path:
        if model_ref in {"latest", ""}:
            if self.latest_model_path.exists():
                return self.latest_model_path
            legacy = self.find_latest_legacy_model()
            if legacy is not None:
                return legacy
            raise FileNotFoundError(f"No model found for {self.game.slug}.")

        candidate = Path(model_ref)
        if candidate.exists():
            return candidate

        checkpoint = self.checkpoints_dir / model_ref
        if checkpoint.exists():
            return checkpoint

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
            if not match:
                continue
            step = int(match.group(1))
            if step > best_step:
                best_step = step
                best_match = file_path
        return best_match
