from __future__ import annotations

from pathlib import Path

from nes_ai.envs.factory import create_retro_env
from nes_ai.games.base import GameDefinition
from nes_ai.training.model_store import ModelStore


def run_episodes(env, choose_action, episodes: int) -> list[float]:
    """Run full episodes with ``choose_action(observation)`` and return total rewards."""
    totals = []
    for _ in range(episodes):
        observation = env.reset()
        done = False
        total = 0.0
        while not done:
            observation, reward, done, _info = env.step(choose_action(observation))
            total += reward
        totals.append(total)
    return totals


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

    store = ModelStore(game)
    model_path = store.resolve_model_path(model_ref)
    env = create_retro_env(game, state=state, render=render, reset_round=reset_round)
    model = PPO.load(str(model_path), env=env)

    rewards = run_episodes(env, lambda observation: model.predict(observation)[0], episodes)
    env.close()
    return _write_evaluation_summary(store.evaluation_dir / "latest_run.txt", model_path, rewards)


def check_reward(
    game: GameDefinition,
    *,
    episodes: int = 30,
    render: bool = True,
    state: str | None = None,
    reset_round: bool = True,
):
    env = create_retro_env(game, state=state, render=render, reset_round=reset_round)
    rewards = run_episodes(env, lambda _observation: env.action_space.sample(), episodes)
    env.close()

    store = ModelStore(game)
    store.ensure_dirs()
    return _write_evaluation_summary(store.evaluation_dir / "random_policy.txt", None, rewards)


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
