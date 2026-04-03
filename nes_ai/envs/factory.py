from __future__ import annotations

from nes_ai.envs.base import WrapperConfig
from nes_ai.games.base import GameDefinition
from nes_ai.utils.naming import load_attr


def create_retro_env(
    game: GameDefinition,
    *,
    state: str | None = None,
    render: bool = False,
    reset_round: bool = True,
):
    try:
        import retro  # type: ignore
    except ModuleNotFoundError as exc:
        raise RuntimeError("gym-retro is required for environment creation.") from exc

    wrapper_cls = load_attr(game.wrapper_path)
    env = retro.make(
        game=game.retro_game,
        state=state or game.default_state,
        use_restricted_actions=retro.Actions.FILTERED,
        obs_type=retro.Observations.IMAGE,
    )
    return wrapper_cls(
        env,
        WrapperConfig(render=render, reset_round=reset_round),
    )


def make_retro_env_factory(
    game: GameDefinition,
    *,
    state: str | None = None,
    render: bool = False,
    reset_round: bool = True,
    monitor_cls=None,
):
    def _init():
        env = create_retro_env(
            game,
            state=state,
            render=render,
            reset_round=reset_round,
        )
        if monitor_cls is not None:
            env = monitor_cls(env)
        return env

    return _init
