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
import sys
from common import get_game_info

import retro
from stable_baselines3 import PPO
from stable_baselines3.common.monitor import Monitor
from stable_baselines3.common.callbacks import CheckpointCallback
from stable_baselines3.common.vec_env import SubprocVecEnv
import argparse

NUM_ENV = 10

# Linear scheduler
def linear_schedule(initial_value, final_value=0.0):

    if isinstance(initial_value, str):
        initial_value = float(initial_value)
        final_value = float(final_value)
        assert (initial_value > 0.0)

    def scheduler(progress):
        return final_value + progress * (initial_value - final_value)

    return scheduler


parser = argparse.ArgumentParser(description='Training parameters')
parser.add_argument('game_number', help='The number of the game to train.')
parser.add_argument('--IsRender', type=bool, default=False, help='Whether to render the environment')

args = parser.parse_args()
IsRender = args.IsRender

game_info = get_game_info(args.game_number)

if game_info is None:
    print(f"Invalid game number. Please choose from {', '.join(game_mapping.keys())}.")
else:
    GameWrapper = game_info["wrapper"]
    game = game_info["game"]
    state = game_info["state"]

LOG_DIR = 'logs'
os.makedirs(LOG_DIR + "/" + game, exist_ok=True)

def make_env(game, state, seed=0):
    def _init():
        env = retro.make(
            game=game, 
            state=state, 
            use_restricted_actions=retro.Actions.FILTERED, 
            obs_type=retro.Observations.IMAGE    
        )
        env = GameWrapper(env,True,IsRender)
        env = Monitor(env)
        env.seed(seed)
        return env
    return _init

   
def main():
    env = SubprocVecEnv([make_env(game, state, seed=i) for i in range(NUM_ENV)])
    lr_schedule = linear_schedule(2.5e-4, 2.5e-6)

    clip_range_schedule = linear_schedule(0.15, 0.025)

    model = PPO(
        "CnnPolicy", 
        env,
        device="cuda", 
        verbose=1,
        n_steps=512,
        batch_size=512,
        n_epochs=4,
        gamma=0.94,
        learning_rate=lr_schedule,
        clip_range=clip_range_schedule,
        tensorboard_log=LOG_DIR + "/" + game
    )

    # Set the save directory
    save_dir = "trained_models"
    os.makedirs(save_dir, exist_ok=True)

    checkpoint_interval = 15000 # checkpoint_interval * num_envs = total_steps_per_checkpoint
    checkpoint_callback = CheckpointCallback(save_freq=checkpoint_interval, save_path=save_dir, name_prefix="ppo_"+game)

    # Writing the training logs from stdout to a file
    original_stdout = sys.stdout
    log_file_path = os.path.join(save_dir, "training_log.txt")
    with open(log_file_path, 'w') as log_file:
        sys.stdout = log_file
    
        model.learn(
            total_timesteps=int(50000000), # total_timesteps = stage_interval * num_envs * num_stages (1120 rounds)
            callback=[checkpoint_callback]#, stage_increase_callback]
        )
        env.close()

    # Restore stdout
    sys.stdout = original_stdout

    # Save the final model
    model.save(os.path.join(save_dir, "ppo_" + game + ".zip"))

if __name__ == "__main__":
    main()
