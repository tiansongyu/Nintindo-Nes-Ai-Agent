"""Translation layer for the legacy script entry points (train.py / run.py)."""

from __future__ import annotations

import argparse

from nes_ai.cli import main as cli_main
from nes_ai.games.registry import get_game
from nes_ai.utils.naming import parse_bool


def forward_legacy_command(command: str, *, default_render: bool, argv=None) -> int:
    """Translate ``<script> <game_number> --IsRender ...`` into a ``nes_ai`` CLI call."""
    parser = argparse.ArgumentParser(description=f"Legacy {command} entry point.")
    parser.add_argument("game_number", help="Legacy game number.")
    parser.add_argument("--IsRender", default=default_render, help="Legacy render flag.")
    args, extras = parser.parse_known_args(argv)

    forwarded = [command, get_game(args.game_number).slug]
    if "--render" not in extras and "--no-render" not in extras:
        forwarded.append("--render" if parse_bool(args.IsRender) else "--no-render")
    forwarded.extend(extras)
    return cli_main(forwarded)
