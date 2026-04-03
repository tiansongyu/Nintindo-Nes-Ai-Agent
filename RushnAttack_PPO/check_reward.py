import sys

from nes_ai.cli import main as cli_main


def main():
    return cli_main(["check-reward", "rush-n-attack", "--render", *sys.argv[1:]])


if __name__ == "__main__":
    raise SystemExit(main())

