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

def get_max_number(game, model_dir):
    """获取模型的最大编号"""
    max_number = -1
    pattern = re.compile(f"ppo_{game}_(\d+)_steps")

    for filename in os.listdir(model_dir):
        match = pattern.match(filename)
        if match:
            number = int(match.group(1))
            if number > max_number:
                max_number = number
    return max_number

def make_env(game_info, reset_round, rendering):
    """创建环境的工厂函数"""
    def _init():
        env = retro.make(
            game=game_info["game"], 
            state=game_info["state"], 
            use_restricted_actions=retro.Actions.FILTERED,
            obs_type=retro.Observations.IMAGE
        )
        env = game_info["wrapper"](env, reset_round, rendering)
        return env
    return _init

def main():
    parser = argparse.ArgumentParser(description='Run parameters')
    parser.add_argument('game_number', help='The number of the game to run.')
    parser.add_argument('--IsRender', type=bool, default=True, help='Whether to render the environment')

    args = parser.parse_args()
    game_info = get_game_info(args.game_number)

    if game_info is None:
        print(f"Invalid game number. Please choose one")
        sys.exit(1)

    RESET_ROUND = True  
    RENDERING = args.IsRender  # 使用命令行参数中的渲染选项

    MODEL_DIR = r"trained_models/"
    MODEL_NAME = "ppo_"+ game_info["game"] + "_" + str(get_max_number(game_info["game"], MODEL_DIR)) +"_steps"
    print(MODEL_NAME)

    env = make_env(game_info, RESET_ROUND, RENDERING)()

    model = PPO.load(os.path.join(MODEL_DIR, MODEL_NAME), env=env)

    obs = env.reset()
    done = False

    num_episodes = 30
    episode_reward_sum = 0
    num_victory = 0

    for _ in range(num_episodes):
        done = False
        
        if RESET_ROUND:
            obs = env.reset()

        total_reward = 0

        while not done:
            timestamp = time.time()
            action, _states = model.predict(obs)
            obs, reward, done, info = env.step(action)

            if reward != 0:
                total_reward += reward
                print("Reward: {:.3f}".format(reward))
                print("Total reward: {}".format(total_reward))

        print("Total reward: {}".format(total_reward))
        episode_reward_sum += total_reward

    env.close()
    print("Average reward for {}: {}".format(MODEL_NAME, episode_reward_sum/num_episodes))

if __name__ == "__main__":
    main()  # 运行主函数
