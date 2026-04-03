from __future__ import annotations

from pathlib import Path

from nes_ai.envs.factory import create_retro_env
from nes_ai.games.base import GameDefinition
from nes_ai.training.model_store import ModelStore


def play_game(
    game: GameDefinition,
    *,
    model_ref: str = "latest",
    episodes: int = 30,
    render: bool = True,
    state: str | None = None,
    reset_round: bool = True,
):
    try:
        from stable_baselines3 import PPO  # type: ignore
    except ModuleNotFoundError as exc:
        raise RuntimeError("stable-baselines3 is required for playback.") from exc

    store = ModelStore.for_game(game)
    model_path = store.resolve_model_path(model_ref)
    env = create_retro_env(game, state=state, render=render, reset_round=reset_round)
    model = PPO.load(str(model_path), env=env)

    total_rewards = []
    for _ in range(episodes):
        observation = env.reset()
        done = False
        total_reward = 0.0
        while not done:
            action, _states = model.predict(observation)
            observation, reward, done, info = env.step(action)
            if reward != 0:
                total_reward += reward
        total_rewards.append(total_reward)

    env.close()
    summary_path = _write_evaluation_summary(store.evaluation_dir / "latest_run.txt", model_path, total_rewards)
    return summary_path


def check_reward(
    game: GameDefinition,
    *,
    episodes: int = 30,
    render: bool = True,
    state: str | None = None,
    reset_round: bool = True,
):
    env = create_retro_env(game, state=state, render=render, reset_round=reset_round)
    total_rewards = []
    for _ in range(episodes):
        observation = env.reset()
        done = False
        total_reward = 0.0
        while not done:
            observation, reward, done, info = env.step(env.action_space.sample())
            if reward != 0:
                total_reward += reward
        total_rewards.append(total_reward)

    env.close()
    store = ModelStore.for_game(game)
    store.ensure_dirs()
    return _write_evaluation_summary(store.evaluation_dir / "random_policy.txt", None, total_rewards)


def _write_evaluation_summary(target: Path, model_path: Path | None, rewards: list[float]) -> Path:
    target.parent.mkdir(parents=True, exist_ok=True)
    average = sum(rewards) / len(rewards) if rewards else 0.0
    with target.open("w", encoding="utf-8") as handle:
        if model_path is not None:
            handle.write(f"model={model_path}\n")
        handle.write(f"episodes={len(rewards)}\n")
        handle.write(f"average_reward={average}\n")
        handle.write("rewards=" + ",".join(str(reward) for reward in rewards) + "\n")
    return target
