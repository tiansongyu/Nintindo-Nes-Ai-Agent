"""Single source of truth for every supported game.

Adding a game means adding one ``GameDefinition`` entry to ``GAMES``.
"""

from __future__ import annotations

from nes_ai.envs.final_mission import FinalMissionWrapper
from nes_ai.envs.rush_n_attack import RushNAttackWrapper
from nes_ai.envs.super_mario_bros import SuperMarioBrosWrapper
from nes_ai.envs.tmnt_tournament_fighters import TMNTTournamentFightersWrapper
from nes_ai.games.base import GameDefinition
from nes_ai.utils.naming import normalize_identifier


GAMES = (
    GameDefinition(
        slug="super-mario-bros",
        legacy_number="1",
        display_name="Super Mario Bros",
        retro_game="SuperMarioBros-Nes",
        default_state="Level1-1",
        wrapper=SuperMarioBrosWrapper,
        aliases=("supermariobros", "super_mario_bros"),
    ),
    GameDefinition(
        slug="tmnt-tournament-fighters",
        legacy_number="2",
        display_name="Teenage Mutant Ninja Turtles Tournament Fighters",
        retro_game="TeenageMutantNinjaTurtlesTournamentFighters-Nes",
        default_state="Level1.LeoVsRaph.Tournament",
        wrapper=TMNTTournamentFightersWrapper,
        aliases=(
            "teenagemutantninjaturtlestournamentfighters",
            "tmnt",
            "ninja-turtles",
        ),
    ),
    GameDefinition(
        slug="final-mission",
        legacy_number="3",
        display_name="Final Mission",
        retro_game="SCATSpecialCyberneticAttackTeam-Nes",
        default_state="Level1-1",
        wrapper=FinalMissionWrapper,
        aliases=("scat", "scat-special-cybernetic-attack-team"),
    ),
    GameDefinition(
        slug="rush-n-attack",
        legacy_number="4",
        display_name="Rush'n Attack",
        retro_game="RushnAttack-Nes",
        default_state="1Player.Level1",
        wrapper=RushNAttackWrapper,
        aliases=("rushnattack", "rush_n_attack"),
    ),
)

_BY_IDENTIFIER = {
    normalize_identifier(identifier): game
    for game in GAMES
    for identifier in game.identifiers()
}


def list_games() -> list[GameDefinition]:
    return list(GAMES)


def get_game(identifier: str) -> GameDefinition:
    game = _BY_IDENTIFIER.get(normalize_identifier(identifier))
    if game is None:
        available = ", ".join(entry.slug for entry in GAMES)
        raise KeyError(f"Unknown game '{identifier}'. Available games: {available}")
    return game
