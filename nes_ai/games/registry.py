from __future__ import annotations

from nes_ai.games.base import GameDefinition
from nes_ai.games.final_mission import GAME as FINAL_MISSION
from nes_ai.games.rush_n_attack import GAME as RUSH_N_ATTACK
from nes_ai.games.super_mario_bros import GAME as SUPER_MARIO_BROS
from nes_ai.games.tmnt_tournament_fighters import GAME as TMNT_TOURNAMENT_FIGHTERS
from nes_ai.utils.naming import normalize_identifier


_GAMES = (
    SUPER_MARIO_BROS,
    TMNT_TOURNAMENT_FIGHTERS,
    FINAL_MISSION,
    RUSH_N_ATTACK,
)


def list_games() -> list[GameDefinition]:
    return list(_GAMES)


def get_game(identifier: str) -> GameDefinition:
    normalized = normalize_identifier(identifier)
    for game in _GAMES:
        identifiers = {normalize_identifier(value) for value in game.identifiers()}
        if normalized in identifiers:
            return game
    available = ", ".join(game.slug for game in _GAMES)
    raise KeyError(f"Unknown game '{identifier}'. Available games: {available}")
