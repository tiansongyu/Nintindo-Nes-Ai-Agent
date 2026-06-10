from nes_ai.games.registry import get_game


def get_game_info(game_number):
    game = get_game(game_number)
    return {
        "wrapper": game.wrapper,
        "game": game.retro_game,
        "state": game.default_state,
        "slug": game.slug,
        "asset_dir": game.asset_dir,
        "train_config": game.train_config,
    }
