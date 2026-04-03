from nes_ai.games.registry import get_game
from nes_ai.utils.naming import load_attr


def get_game_info(game_number):
    game = get_game(game_number)
    return {
        "wrapper": load_attr(game.wrapper_path),
        "game": game.retro_game,
        "state": game.default_state,
        "slug": game.slug,
        "asset_dir": game.asset_dir,
        "train_config": game.train_config,
    }

