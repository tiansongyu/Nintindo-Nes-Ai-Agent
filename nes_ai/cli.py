import argparse
import sys

from nes_ai.games.registry import get_game, list_games
from nes_ai.retro.installer import install_roms
from nes_ai.training.evaluator import check_reward, play_game
from nes_ai.training.trainer import train_game


def add_bool_flag(parser: argparse.ArgumentParser, name: str, default: bool, help_text: str) -> None:
    destination = name.replace("-", "_")
    group = parser.add_mutually_exclusive_group()
    group.add_argument(f"--{name}", dest=destination, action="store_true", help=help_text)
    group.add_argument(f"--no-{name}", dest=destination, action="store_false", help=f"Disable {help_text.lower()}")
    parser.set_defaults(**{destination: default})


def _add_env_options(parser: argparse.ArgumentParser, *, render_default: bool) -> None:
    parser.add_argument("game", help="Game slug or legacy number.")
    parser.add_argument("--state", default=None)
    add_bool_flag(parser, "reset-round", True, "Reset the round when an episode ends.")
    add_bool_flag(parser, "render", render_default, "Render the game window.")


def _run_list_games(args: argparse.Namespace) -> int:
    for game in list_games():
        print(f"{game.legacy_number}. {game.slug} -> {game.retro_game}")
    return 0


def _run_install_roms(args: argparse.Namespace) -> int:
    for path in install_roms(args.game):
        print(path)
    return 0


def _run_train(args: argparse.Namespace) -> int:
    train_game(
        get_game(args.game),
        total_timesteps=args.timesteps,
        num_envs=args.num_envs,
        device=args.device,
        render=args.render,
        state=args.state,
        reset_round=args.reset_round,
    )
    return 0


def _run_play(args: argparse.Namespace) -> int:
    summary = play_game(
        get_game(args.game),
        model_ref=args.model,
        episodes=args.episodes,
        render=args.render,
        state=args.state,
        reset_round=args.reset_round,
    )
    print(summary)
    return 0


def _run_check_reward(args: argparse.Namespace) -> int:
    summary = check_reward(
        get_game(args.game),
        episodes=args.episodes,
        render=args.render,
        state=args.state,
        reset_round=args.reset_round,
    )
    print(summary)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="nes_ai")
    subparsers = parser.add_subparsers(dest="command", required=True)

    list_parser = subparsers.add_parser("list-games", help="List all registered games.")
    list_parser.set_defaults(func=_run_list_games)

    install_parser = subparsers.add_parser("install-roms", help="Install ROM assets into Gym Retro.")
    install_parser.add_argument("game", nargs="?", help="Optional game slug.")
    install_parser.set_defaults(func=_run_install_roms)

    train_parser = subparsers.add_parser("train", help="Train a game agent.")
    _add_env_options(train_parser, render_default=False)
    train_parser.add_argument("--timesteps", type=int, default=None)
    train_parser.add_argument("--num-envs", type=int, default=None)
    train_parser.add_argument("--device", default=None)
    train_parser.set_defaults(func=_run_train)

    play_parser = subparsers.add_parser("play", help="Play using a trained model.")
    _add_env_options(play_parser, render_default=True)
    play_parser.add_argument("--model", default="latest")
    play_parser.add_argument("--episodes", type=int, default=30)
    play_parser.set_defaults(func=_run_play)

    reward_parser = subparsers.add_parser("check-reward", help="Run a random policy reward sanity check.")
    _add_env_options(reward_parser, render_default=True)
    reward_parser.add_argument("--episodes", type=int, default=30)
    reward_parser.set_defaults(func=_run_check_reward)

    return parser


def main(argv=None):
    args = build_parser().parse_args(argv)
    try:
        return args.func(args)
    except (FileNotFoundError, KeyError, RuntimeError, ValueError) as exc:
        sys.stderr.write(f"{exc}\n")
        return 1
