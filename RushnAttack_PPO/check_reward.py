import os
import time 

import retro
from stable_baselines3.common.monitor import Monitor

from RushnAttackWrapper import RushnAttack  # Assuming you have this wrapper

LOG_DIR = 'logs/'
os.makedirs(LOG_DIR, exist_ok=True)

RESET_ROUND = True  # Whether to reset the round when fight is over. 
RENDERING = True    # Whether to render the game screen.

def make_env(game, state):
    def _init():
        env = retro.make(
            game=game, 
            state=state, 
            use_restricted_actions=retro.Actions.FILTERED, 
            obs_type=retro.Observations.IMAGE
        )
        env = RushnAttack(env,RESET_ROUND,RENDERING)
        return env
    return _init

game = "RushnAttack-Nes"
state = "1Player.Level1"

env = make_env(game, state)()
env = Monitor(env, LOG_DIR)

num_episodes = 30
episode_reward_sum = 0
for _ in range(num_episodes):
    done = False
    obs = env.reset()
    total_reward = 0
    while not done:
        timestamp = time.time()
        obs, reward, done, info = env.step(env.action_space.sample())
        if reward != 0:
            total_reward += reward
            print("Total reward: {}".format(total_reward))

    print("Total reward: {}".format(total_reward))
    episode_reward_sum += total_reward

env.close()
print("Average reward for random strategy: {}".format(episode_reward_sum/num_episodes))