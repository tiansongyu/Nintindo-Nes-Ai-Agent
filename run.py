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
import time 
import sys
import retro
import argparse
import re

from stable_baselines3 import PPO
from stable_baselines3.common.monitor import Monitor
from stable_baselines3.common.callbacks import CheckpointCallback
from stable_baselines3.common.vec_env import SubprocVecEnv

from common import get_game_info

parser = argparse.ArgumentParser(description='Training parameters')
parser.add_argument('game_number', help='The number of the game to train.')
parser.add_argument('--IsRender', type=bool, default=False, help='Whether to render the environment')

args = parser.parse_args()
game_info = get_game_info(args.game_number)

if game_info is None:
    print(f"Invalid game number. Please choose one")
else:
    GameWrapper = game_info["wrapper"]
    game = game_info["game"]
    state = game_info["state"]

RESET_ROUND = True  # Whether to reset the round when fight is over. 
RENDERING = True    # Whether to render the game screen.


RANDOM_ACTION = False
NUM_EPISODES = 30 # Make sure NUM_EPISODES >= 3 if you set RESET_ROUND to False to see the whole final stage game.
MODEL_DIR = r"trained_models/"
def get_max_number(game):
    max_number = -1
    pattern = re.compile(f"ppo_{game}_(\d+)_steps")

    for filename in os.listdir(MODEL_DIR):
        match = pattern.match(filename)
        if match:
            number = int(match.group(1))
            if number > max_number:
                max_number = number
    return max_number
# use your trained model !!!!!!!!!!!!!!!
MODEL_NAME = "ppo_"+ game + "_" + str(get_max_number(game)) +"_steps"
print(MODEL_NAME)
def make_env(game, state):
    def _init():
        env = retro.make(
            game=game, 
            state=state, 
            use_restricted_actions=retro.Actions.FILTERED,
            obs_type=retro.Observations.IMAGE
        )
        env = GameWrapper(env, reset_round=RESET_ROUND, rendering=RENDERING)
        return env
    return _init

env = make_env(game, state)()

if not RANDOM_ACTION:
    model = PPO.load(os.path.join(MODEL_DIR, MODEL_NAME), env=env)

obs = env.reset()
done = False

num_episodes = NUM_EPISODES
episode_reward_sum = 0
num_victory = 0

for _ in range(num_episodes):
    done = False
    
    if RESET_ROUND:
        obs = env.reset()

    total_reward = 0

    while not done:
        timestamp = time.time()

        if RANDOM_ACTION:
            obs, reward, done, info = env.step(env.action_space.sample())
        else:
            action, _states = model.predict(obs)
            obs, reward, done, info = env.step(action)

        if reward != 0:
            total_reward += reward
            print("Reward: {:.3f}".format(reward))
            print("Total reward: {}\n".format(total_reward))
        if done:
            num_victory += 1
    print("Total reward: {}\n".format(total_reward))
    episode_reward_sum += total_reward

env.close()
if RANDOM_ACTION:
    print("Average reward for random action: {}".format(episode_reward_sum/num_episodes))
else:
    print("Average reward for {}: {}".format(MODEL_NAME, episode_reward_sum/num_episodes))
