from nes_ai.constants import ASSETS_DIR
from nes_ai.games.base import GameDefinition, TrainConfig


GAME = GameDefinition(
    slug="rush-n-attack",
    legacy_number="4",
    display_name="Rush'n Attack",
    retro_game="RushnAttack-Nes",
    default_state="1Player.Level1",
    wrapper_path="nes_ai.envs.rush_n_attack:RushNAttackWrapper",
    asset_dir=ASSETS_DIR / "RushnAttack-Nes",
    aliases=("rushnattack", "rush_n_attack"),
    train_config=TrainConfig(),
)

