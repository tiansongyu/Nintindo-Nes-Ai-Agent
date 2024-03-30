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

import os
import shutil
import retro

retro_directory = os.path.dirname(retro.__file__)
game_dirs_mapping = {
    "FinalMission_PPO": "SCATSpecialCyberneticAttackTeam-Nes",
    "SuperMarioBros_PPO": "SuperMarioBros-Nes",
    "RushnAttack_PPO": "RushnAttack-Nes",
    "TeenageMutantNinjaTurtlesTournamentFighters": "TeenageMutantNinjaTurtlesTournamentFighters-Nes"
}

for target_game_dir, game_dir in game_dirs_mapping.items():
    rom_directory = os.path.join(os.getcwd(), target_game_dir, 'rom')
    rom_files = os.listdir(rom_directory)
    for file in rom_files:
        shutil.copy(os.path.join(rom_directory, file), os.path.join(retro_directory, 'data', 'stable', game_dir))

    print(os.path.join(retro_directory, 'data', 'stable', game_dir))
    print(rom_directory)
    print(target_game_dir)
print("finish set up environment")