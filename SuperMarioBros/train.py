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

import retro
from stable_baselines3 import DQN
from stable_baselines3.common.monitor import Monitor
from stable_baselines3.common.callbacks import CheckpointCallback
from stable_baselines3.common.vec_env import DummyVecEnv

from SuperMarioBrosWrapper import SuperMarioBros
import argparse

# Parse command line arguments
parser = argparse.ArgumentParser(description='Training parameters')
parser.add_argument('--IsRender', type=bool, default=False, help='Whether to render the environment')
args = parser.parse_args()

IsRender = args.IsRender

LOG_DIR = 'logs'
os.makedirs(LOG_DIR, exist_ok=True)

def make_env(game, state, seed=0):
    def _init():
        env = retro.make(
            game=game, 
            state=state, 
            use_restricted_actions=retro.Actions.DISCRETE, 
            obs_type=retro.Observations.IMAGE    
        )
        env = SuperMarioBros(env,True,IsRender)
        env = Monitor(env)
        env.seed(seed)
        return env
    return _init

def main():
    # Set up the environment and model
    game = "SuperMarioBros-Nes"
    env = DummyVecEnv([make_env(game, state="Level1-1", seed=0)])

    model = DQN(
        "CnnPolicy", 
        env,
        device="cuda", 
        verbose=1,
        learning_rate=2.5e-4,
        buffer_size=50000,
        exploration_fraction=0.1,
        exploration_final_eps=0.02,
        train_freq=4,
        gradient_steps=1,
        target_update_interval=1000,
        tensorboard_log="logs",
    )

    # Set the save directory
    save_dir = "trained_models"
    os.makedirs(save_dir, exist_ok=True)

    checkpoint_interval = 300000 # checkpoint_interval * num_envs = total_steps_per_checkpoint
    checkpoint_callback = CheckpointCallback(save_freq=checkpoint_interval, save_path=save_dir, name_prefix="dqn_super_mario_bros")

    # Writing the training logs from stdout to a file
    original_stdout = sys.stdout
    log_file_path = os.path.join(save_dir, "training_log.txt")
    with open(log_file_path, 'w') as log_file:
        sys.stdout = log_file
    
        model.learn(
            total_timesteps=int(30000000), # total_timesteps = stage_interval * num_envs * num_stages (1120 rounds)
            callback=[checkpoint_callback]#, stage_increase_callback]
        )
        env.close()

    # Restore stdout
    sys.stdout = original_stdout

    # Save the final model
    model.save(os.path.join(save_dir, "dqn_SuperMarioBros_final.zip"))

if __name__ == "__main__":
    main()