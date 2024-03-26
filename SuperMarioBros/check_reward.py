import os
import time 

import retro
from stable_baselines3.common.monitor import Monitor

from SuperMarioBrosWrapper import SuperMarioBros  # Assuming you have this wrapper

LOG_DIR = 'logs/'
os.makedirs(LOG_DIR, exist_ok=True)

# actions for more complex movement
COMPLEX_MOVEMENT = [
    ['NOOP'],
    # ['right'],
    # ['right', 'A'],
    # ['right', 'B'],
    # ['right', 'A', 'B'],
    # ['A'],
    # ['left'],
    # ['left', 'A'],
    # ['left', 'B'],
    # ['left', 'A', 'B'],
    # ['down'],
    # ['up'],
]
def make_env(game, state):
    def _init():
        env = retro.make(
            game=game, 
            state=state, 
            use_restricted_actions=retro.Actions.DISCRETE, 
            obs_type=retro.Observations.IMAGE
        )
        env = SuperMarioBros(env)
        env.button = COMPLEX_MOVEMENT
        return env
    return _init

game = "SuperMarioBros-Nes"
state = "Level1-1"

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
        print(env.action_space.sample())
        obs, reward, done, info = env.step(env.action_space.sample())
        total_reward += reward
        print("Total reward: {}".format(total_reward))
        env.render()
        time.sleep(0.01)
    episode_reward_sum += total_reward

env.close()
print("Average reward for random strategy: {}".format(episode_reward_sum/num_episodes))