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
class SuperMarioBros(gym.Wrapper):
    def __init__(self, env, reset_round=True, rendering=False):
        super(SuperMarioBros, self).__init__(env)
        self.env = env

        # Use a deque to store the last 9 frames
        self.num_frames = 9
        self.frame_stack = collections.deque(maxlen=self.num_frames)

        self.num_step_frames = 6

        self.reward_coeff = 3.0

        self.last_xscrollLo = 999

        self.last_x_pos = 999

        self.last_time = -1

        self.last_score = 0
        self.observation_space = gym.spaces.Box(low=0, high=255, shape=(112, 120, 3), dtype=np.uint8)
        self.reset_round = reset_round
        self.rendering = rendering
    def _stack_observation(self):
        return np.stack([self.frame_stack[i * 3 + 2][:, :, i] for i in range(3)], axis=-1)
    def reset(self):
        self.last_xscrollLo = 999
        self.last_x_pos = 999
        self.last_time = -1
        self.last_score = 0
        observation = self.env.reset()
        
        self.frame_stack.clear()
        for _ in range(self.num_frames):
            self.frame_stack.append(observation[::2, ::2, :])
        return self._stack_observation()

    def step(self, action):
        custom_done = False

        obs, _reward, _done, info = self.env.step(action)
        self.frame_stack.append(obs[::2, ::2, :])
        for _ in range(self.num_step_frames - 1):
            obs, _reward, _done, info = self.env.step(action)
            self.frame_stack.append(obs[::2, ::2, :])
            # Render the game if rendering flag is set to True.
            if self.rendering:
                self.env.render()
                ti.sleep(0.01)
        self.xscrollLo = info['xscrollLo']
        lives = info['lives']
        time = info['time']
        score = info['score']
        is_get_flag = False
        death_penalty = 0.0
        x_roll_reward = 0.0
        x_pos_reward = 0.0
        flag_reward = 0.0
        time_reward = 0.0
        score_reward = 0.0
        score = 0.0
        is_stage_over = False

        if info['enemy_pos_1'] == 49 or info['enemy_pos_2'] == 49 or info['enemy_pos_3'] == 49 or info['enemy_pos_4'] == 49 or info['enemy_pos_5'] == 49 or info['enemy_pos_6'] == 49 or info['enemy_pos_7'] == 49 :
            if info['is_stage_over'] == 3:
                is_stage_over = True
        if info['is_world_over'] == 2 or is_stage_over:
            is_get_flag = True
        x_pos = info['x_pos_a'] * 256 + info['x_pos_b']

        if info['player_state'] ==11 or info['y_viewport']>1 or info['player_state']==6:
            death_penalty= -25.0
            custom_done = True

        if self.xscrollLo - self.last_xscrollLo > 0:
            x_roll_reward =self.xscrollLo - self.last_xscrollLo
        if x_pos - self.last_x_pos > -5 and x_pos - self.last_x_pos < 5:
            x_pos_reward = (x_pos - self.last_x_pos) * 2
        if not self.reset_round:
            custom_done = False
        if is_get_flag:
            flag_reward = 50.0
            custom_done = True

        if time - self.last_time < 0:
            time_reward = ( time-self.last_time ) * 0.01
        if score - self.last_score > 0:
            score_reward = (score - self.last_score)* 0.001
        if lives < 1:
            custom_done = True
        self.last_xscrollLo = self.xscrollLo
        self.last_x_pos = x_pos
        self.last_time = time
        self.last_score = score
        r = time_reward+x_roll_reward+x_pos_reward+flag_reward+death_penalty
        return self._stack_observation(),r, custom_done, info 
    