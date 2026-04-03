from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path


@dataclass(frozen=True)
class TrainConfig:
    num_envs: int = 10
    total_timesteps: int = 50_000_000
    n_steps: int = 512
    batch_size: int = 512
    n_epochs: int = 4
    gamma: float = 0.94
    learning_rate_start: float = 2.5e-4
    learning_rate_end: float = 2.5e-6
    clip_range_start: float = 0.15
    clip_range_end: float = 0.025
    checkpoint_interval: int = 15_000
    device: str = "cuda"


@dataclass(frozen=True)
class GameDefinition:
    slug: str
    legacy_number: str
    display_name: str
    retro_game: str
    default_state: str
    wrapper_path: str
    asset_dir: Path
    aliases: tuple[str, ...] = ()
    train_config: TrainConfig = field(default_factory=TrainConfig)

    def identifiers(self) -> tuple[str, ...]:
        return (
            self.slug,
            self.legacy_number,
            self.display_name,
            self.retro_game,
            *self.aliases,
        )
