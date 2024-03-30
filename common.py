# common.py
import sys
import os

for root, dirs, files in os.walk('.'):
    sys.path.append(root)

from FinalMissionWrapper import FinalMission
from RushnAttackWrapper import RushnAttack
from SuperMarioBrosWrapper import SuperMarioBros
from ninja_turtles_fight_wrapper import TeenageMutantNinjaTurtlesTournamentFighters

game_mapping = {
    "1": {"wrapper": FinalMission, "game": "SCATSpecialCyberneticAttackTeam-Nes", "state": "1Player.Level1"},
    "2": {"wrapper": SuperMarioBros, "game": "SuperMarioBros-Nes", "state": "Level1-1"},
    "3": {"wrapper": RushnAttack, "game": "RushnAttack-Nes", "state": "1Player.Level1"},
    "4": {"wrapper": TeenageMutantNinjaTurtlesTournamentFighters, "game": "TeenageMutantNinjaTurtlesTournamentFighters-Nes", "state": "Level1.LeoVsRaph.Tournament"}
}

def get_game_info(game_number):
    game_info = game_mapping.get(game_number)

    if game_info is None:
        print(f"Invalid game number. Please choose from {', '.join(game_mapping.keys())}.")
        sys.exit(1)

    return game_info