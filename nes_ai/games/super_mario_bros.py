from nes_ai.constants import ASSETS_DIR
from nes_ai.games.base import GameDefinition, TrainConfig


GAME = GameDefinition(
    slug="super-mario-bros",
    legacy_number="1",
    display_name="Super Mario Bros",
    retro_game="SuperMarioBros-Nes",
    default_state="Level1-1",
    wrapper_path="nes_ai.envs.super_mario_bros:SuperMarioBrosWrapper",
    asset_dir=ASSETS_DIR / "SuperMarioBros-Nes",
    aliases=("supermariobros", "super_mario_bros"),
    train_config=TrainConfig(),
)

