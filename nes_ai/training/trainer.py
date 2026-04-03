from __future__ import annotations

import contextlib
import sys

from nes_ai.envs.factory import make_retro_env_factory
from nes_ai.games.base import GameDefinition
from nes_ai.training.model_store import ModelStore
from nes_ai.training.schedules import linear_schedule


def _resolve_device(requested_device: str) -> str:
    if requested_device != "cuda":
        return requested_device
    try:
        import torch  # type: ignore
    except ModuleNotFoundError:
        return "cpu"
    return "cuda" if torch.cuda.is_available() else "cpu"


def train_game(
    game: GameDefinition,
    *,
    total_timesteps: int | None = None,
    num_envs: int | None = None,
    device: str | None = None,
    render: bool = False,
    state: str | None = None,
    reset_round: bool = True,
):
    try:
        from stable_baselines3 import PPO  # type: ignore
        from stable_baselines3.common.callbacks import CheckpointCallback  # type: ignore
        from stable_baselines3.common.monitor import Monitor  # type: ignore
        from stable_baselines3.common.vec_env import DummyVecEnv, SubprocVecEnv  # type: ignore
    except ModuleNotFoundError as exc:
        raise RuntimeError("stable-baselines3 is required for training.") from exc

    config = game.train_config
    total_timesteps = total_timesteps or config.total_timesteps
    num_envs = num_envs or config.num_envs
    device = _resolve_device(device or config.device)

    store = ModelStore.for_game(game)
    store.ensure_dirs()

    env_factory = [
        make_retro_env_factory(
            game,
            state=state,
            render=render,
            reset_round=reset_round,
            monitor_cls=Monitor,
        )
        for _ in range(num_envs)
    ]
    env = DummyVecEnv(env_factory) if num_envs == 1 else SubprocVecEnv(env_factory)

    model = PPO(
        "CnnPolicy",
        env,
        device=device,
        verbose=1,
        n_steps=config.n_steps,
        batch_size=config.batch_size,
        n_epochs=config.n_epochs,
        gamma=config.gamma,
        learning_rate=linear_schedule(config.learning_rate_start, config.learning_rate_end),
        clip_range=linear_schedule(config.clip_range_start, config.clip_range_end),
        tensorboard_log=str(store.tensorboard_dir),
    )

    checkpoint_callback = CheckpointCallback(
        save_freq=config.checkpoint_interval,
        save_path=str(store.checkpoints_dir),
        name_prefix="checkpoint",
    )

    with store.training_log_path.open("w", encoding="utf-8") as log_file:
        with contextlib.redirect_stdout(log_file):
            model.learn(total_timesteps=int(total_timesteps), callback=[checkpoint_callback])

    env.close()
    model.save(str(store.latest_model_path))
    sys.stdout.write(f"Saved model to {store.latest_model_path}\n")
    return store.latest_model_path
