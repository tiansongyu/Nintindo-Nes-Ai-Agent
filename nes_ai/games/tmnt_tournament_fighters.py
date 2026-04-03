from nes_ai.constants import ASSETS_DIR
from nes_ai.games.base import GameDefinition, TrainConfig


GAME = GameDefinition(
    slug="tmnt-tournament-fighters",
    legacy_number="2",
    display_name="Teenage Mutant Ninja Turtles Tournament Fighters",
    retro_game="TeenageMutantNinjaTurtlesTournamentFighters-Nes",
    default_state="Level1.LeoVsRaph.Tournament",
    wrapper_path="nes_ai.envs.tmnt_tournament_fighters:TMNTTournamentFightersWrapper",
    asset_dir=ASSETS_DIR / "TeenageMutantNinjaTurtlesTournamentFighters-Nes",
    aliases=(
        "teenagemutantninjaturtlestournamentfighters",
        "tmnt",
        "ninja-turtles",
    ),
    train_config=TrainConfig(),
)

