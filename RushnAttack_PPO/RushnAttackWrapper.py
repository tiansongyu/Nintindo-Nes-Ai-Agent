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

import time as ti
import gym
import numpy as np
import collections
class RushnAttack(gym.Wrapper):
    def __init__(self, env, reset_round=True, rendering=False):
        super(RushnAttack, self).__init__(env)
        self.env = env

        # Use a deque to store the last 9 frames
        self.num_frames = 9
        self.frame_stack = collections.deque(maxlen=self.num_frames)

        self.num_step_frames = 6

        self.reward_coeff = 3.0

        self.last_lives = 6
        self.last_scores = 0
        self.last_xscoll = 0
        self.last_x_pos = 0
        self.observation_space = gym.spaces.Box(low=0, high=255, shape=(112, 120, 3), dtype=np.uint8)
        self.reset_round = reset_round
        self.rendering = rendering
    def _stack_observation(self):
        return np.stack([self.frame_stack[i * 3 + 2][:, :, i] for i in range(3)], axis=-1)
    def reset(self):
        self.last_score = 0
        self.last_lives = 0
        self.last_xscoll = 0
        self.last_x_pos = 0
        observation = self.env.reset()
        
        self.frame_stack.clear()
        for _ in range(self.num_frames):
            self.frame_stack.append(observation[::2, ::2, :])
        return self._stack_observation()

    def step(self, action):
        custom_done = False

        reward_scores = 0
        reward_lives = 0
        reward_xscroll = 0
        reward_x_pos = 0
        obs, _reward, _done, info = self.env.step(action)
        self.frame_stack.append(obs[::2, ::2, :])
        for _ in range(self.num_step_frames - 1):
            obs, _reward, _done, info = self.env.step(action)
            self.frame_stack.append(obs[::2, ::2, :])
            # Render the game if rendering flag is set to True.
            if self.rendering:
                self.env.render()
                ti.sleep(0.01)
        lives = info['lives']
        scores = info['score']
        xscollLo = info['xscrollLo']
        xscrollHi = info['xscrollHi']
        x_pos_in_screen = info['x_pos_in_screen']
        xscroll =(xscollLo + xscrollHi * 256) 
        if(self.last_scores < scores):
            reward_scores = (scores - self.last_scores) * 4
        if(self.last_lives > lives):
            reward_lives = -200
        if(self.last_xscoll < xscroll):
            reward_xscroll = (xscroll - self.last_xscoll)
        reward_x_pos = (x_pos_in_screen - self.last_x_pos) * 0.1
        if(lives < 1):
            custom_done = True
        self.last_scores = scores
        self.last_lives = lives
        self.last_xscoll = xscroll
        self.last_x_pos = x_pos_in_screen
        r = 0.01 * (reward_lives + reward_scores + reward_xscroll + reward_x_pos)
        # print("Reward: ", r, "Scores: ", scores, "Lives: ", lives, "Xscroll: ", xscroll, "X_pos: ", x_pos_in_screen)
        # print("Reward Scores: ", reward_scores, "Reward Lives: ", reward_lives, "Reward Xscroll: ", reward_xscroll, "Reward X_pos: ", reward_x_pos)
        return self._stack_observation(),r, custom_done, info 
    