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