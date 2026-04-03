import argparse

from nes_ai.cli import main as cli_main
from nes_ai.games.registry import get_game
from nes_ai.utils.naming import parse_bool


def main():
    parser = argparse.ArgumentParser(description="Legacy training entry point.")
    parser.add_argument("game_number", help="Legacy game number.")
    parser.add_argument("--IsRender", default=False, help="Legacy render flag.")
    args, extras = parser.parse_known_args()

    argv = ["train", get_game(args.game_number).slug]
    has_render_override = "--render" in extras or "--no-render" in extras
    if parse_bool(args.IsRender) and not has_render_override:
        argv.append("--render")
    argv.extend(extras)
    return cli_main(argv)


if __name__ == "__main__":
    raise SystemExit(main())
