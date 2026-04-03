from nes_ai.constants import ASSETS_DIR
from nes_ai.games.base import GameDefinition, TrainConfig


GAME = GameDefinition(
    slug="final-mission",
    legacy_number="3",
    display_name="Final Mission",
    retro_game="SCATSpecialCyberneticAttackTeam-Nes",
    default_state="Level1-1",
    wrapper_path="nes_ai.envs.final_mission:FinalMissionWrapper",
    asset_dir=ASSETS_DIR / "SCATSpecialCyberneticAttackTeam-Nes",
    aliases=("scat", "scat-special-cybernetic-attack-team"),
    train_config=TrainConfig(),
)
