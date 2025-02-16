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

# 定义 RushnAttack 类，继承自 gym.Wrapper
class RushnAttack(gym.Wrapper):
    def __init__(self, env, reset_round=True, rendering=False):
        # 初始化父类
        super(RushnAttack, self).__init__(env)
        self.env = env

        # 使用 deque 存储最近的 9 帧
        self.num_frames = 9
        self.frame_stack = collections.deque(maxlen=self.num_frames)

        # 每个步骤中执行的帧数
        self.num_step_frames = 6

        # 奖励系数
        self.reward_coeff = 3.0

        # 初始化状态变量
        self.last_lives = 6
        self.last_scores = 0
        self.last_xscoll = 0
        self.last_x_pos = 0

        # 定义观察空间
        self.observation_space = gym.spaces.Box(low=0, high=255, shape=(112, 120, 3), dtype=np.uint8)
        self.reset_round = reset_round
        self.rendering = rendering

    # 堆叠观察帧
    def _stack_observation(self):
        return np.stack([self.frame_stack[i * 3 + 2][:, :, i] for i in range(3)], axis=-1)

    # 重置环境
    def reset(self):
        # 重置状态变量
        self.last_score = 0
        self.last_lives = 0
        self.last_xscoll = 0
        self.last_x_pos = 0
        
        # 重置环境并获取初始观察
        observation = self.env.reset()
        
        # 清空帧堆栈并填充初始帧
        self.frame_stack.clear()
        for _ in range(self.num_frames):
            self.frame_stack.append(observation[::2, ::2, :])
        
        # 返回堆叠后的观察
        return self._stack_observation()

    # 执行动作
    def step(self, action):
        custom_done = False

        # 初始化奖励变量
        reward_scores = 0
        reward_lives = 0
        reward_xscroll = 0
        reward_x_pos = 0
        
        # 执行动作并获取观察和信息
        obs, _reward, _done, info = self.env.step(action)
        self.frame_stack.append(obs[::2, ::2, :])
        
        # 执行多个步骤以获取更多帧
        for _ in range(self.num_step_frames - 1):
            obs, _reward, _done, info = self.env.step(action)
            self.frame_stack.append(obs[::2, ::2, :])
            
            # 如果设置了渲染，则渲染游戏
            if self.rendering:
                self.env.render()
                ti.sleep(0.01)

        # 从信息中提取状态
        lives = info['lives']
        scores = info['score']
        xscollLo = info['xscrollLo']
        xscrollHi = info['xscrollHi']
        x_pos_in_screen = info['x_pos_in_screen']
        
        # 计算滚动位置
        xscroll = (xscollLo + xscrollHi * 256) 
        
        # 奖励计算
        if self.last_scores < scores:
            reward_scores = (scores - self.last_scores) * 4
        if self.last_lives > lives:
            reward_lives = -200
        if self.last_xscoll < xscroll:
            reward_xscroll = (xscroll - self.last_xscoll)
        reward_x_pos = (x_pos_in_screen - self.last_x_pos) * 0.1
        
        # 检查是否完成
        if lives < 1:
            custom_done = True
        
        # 更新状态变量
        self.last_scores = scores
        self.last_lives = lives
        self.last_xscoll = xscroll
        self.last_x_pos = x_pos_in_screen
        
        # 计算最终奖励
        r = 0.01 * (reward_lives + reward_scores + reward_xscroll + reward_x_pos)
        
        # 返回堆叠后的观察、奖励、完成标志和信息
        return self._stack_observation(), r, custom_done, info 
    