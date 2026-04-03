from __future__ import annotations

import shutil

from nes_ai.games.base import GameDefinition
from nes_ai.games.registry import get_game, list_games
from nes_ai.retro.paths import get_retro_stable_dir
from nes_ai.utils.validation import validate_asset_dir


def install_roms(game_identifier: str | None = None) -> list[str]:
    games = [get_game(game_identifier)] if game_identifier else list_games()
    retro_stable_dir = get_retro_stable_dir()
    installed = []

    for game in games:
        validate_asset_dir(game.asset_dir)
        target_dir = retro_stable_dir / game.retro_game
        target_dir.mkdir(parents=True, exist_ok=True)
        for asset in game.asset_dir.iterdir():
            if asset.is_file():
                shutil.copy2(asset, target_dir / asset.name)
        installed.append(str(target_dir))

    return installed
