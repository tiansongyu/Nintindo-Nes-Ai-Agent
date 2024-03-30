# Copyright 2023 invoker__qq. All Rights Reserved.
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#     http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================

import sys
import os

for root, dirs, files in os.walk('.'):
    sys.path.append(root)

from FinalMissionWrapper import FinalMission
from RushnAttackWrapper import RushnAttack
from SuperMarioBrosWrapper import SuperMarioBros
from ninja_turtles_fight_wrapper import TeenageMutantNinjaTurtlesTournamentFighters

game_mapping = {
    "3": {"wrapper": FinalMission, "game": "SCATSpecialCyberneticAttackTeam-Nes", "state": "1Player.Level1"},
    "1": {"wrapper": SuperMarioBros, "game": "SuperMarioBros-Nes", "state": "Level1-1"},
    "4": {"wrapper": RushnAttack, "game": "RushnAttack-Nes", "state": "1Player.Level1"},
    "2": {"wrapper": TeenageMutantNinjaTurtlesTournamentFighters, "game": "TeenageMutantNinjaTurtlesTournamentFighters-Nes", "state": "Level1.LeoVsRaph.Tournament"}
}

def get_game_info(game_number):
    game_info = game_mapping.get(game_number)

    if game_info is None:
        print(f"Invalid game number. Please choose from {', '.join(game_mapping.keys())}.")
        sys.exit(1)

    return game_info