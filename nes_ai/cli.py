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


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="nes_ai")
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("list-games", help="List all registered games.")

    install_parser = subparsers.add_parser("install-roms", help="Install ROM assets into Gym Retro.")
    install_parser.add_argument("game", nargs="?", help="Optional game slug.")

    train_parser = subparsers.add_parser("train", help="Train a game agent.")
    train_parser.add_argument("game", help="Game slug or legacy number.")
    train_parser.add_argument("--timesteps", type=int, default=None)
    train_parser.add_argument("--num-envs", type=int, default=None)
    train_parser.add_argument("--device", default=None)
    train_parser.add_argument("--state", default=None)
    add_bool_flag(train_parser, "reset-round", True, "Reset the round when an episode ends.")
    add_bool_flag(train_parser, "render", False, "Render the game window.")

    play_parser = subparsers.add_parser("play", help="Play using a trained model.")
    play_parser.add_argument("game", help="Game slug or legacy number.")
    play_parser.add_argument("--model", default="latest")
    play_parser.add_argument("--episodes", type=int, default=30)
    play_parser.add_argument("--state", default=None)
    add_bool_flag(play_parser, "reset-round", True, "Reset the round when an episode ends.")
    add_bool_flag(play_parser, "render", True, "Render the game window.")

    reward_parser = subparsers.add_parser("check-reward", help="Run a random policy reward sanity check.")
    reward_parser.add_argument("game", help="Game slug or legacy number.")
    reward_parser.add_argument("--episodes", type=int, default=30)
    reward_parser.add_argument("--state", default=None)
    add_bool_flag(reward_parser, "reset-round", True, "Reset the round when an episode ends.")
    add_bool_flag(reward_parser, "render", True, "Render the game window.")

    return parser


def main(argv=None):
    parser = build_parser()
    args = parser.parse_args(argv)

    try:
        if args.command == "list-games":
            for game in list_games():
                print(f"{game.legacy_number}. {game.slug} -> {game.retro_game}")
            return 0

        if args.command == "install-roms":
            installed = install_roms(args.game)
            for path in installed:
                print(path)
            return 0

        game = get_game(args.game)

        if args.command == "train":
            train_game(
                game,
                total_timesteps=args.timesteps,
                num_envs=args.num_envs,
                device=args.device,
                render=args.render,
                state=args.state,
                reset_round=args.reset_round,
            )
            return 0

        if args.command == "play":
            summary = play_game(
                game,
                model_ref=args.model,
                episodes=args.episodes,
                render=args.render,
                state=args.state,
                reset_round=args.reset_round,
            )
            print(summary)
            return 0

        if args.command == "check-reward":
            summary = check_reward(
                game,
                episodes=args.episodes,
                render=args.render,
                state=args.state,
                reset_round=args.reset_round,
            )
            print(summary)
            return 0
    except (FileNotFoundError, KeyError, RuntimeError, ValueError) as exc:
        sys.stderr.write(f"{exc}\n")
        return 1

    parser.error(f"Unknown command: {args.command}")
    return 2
