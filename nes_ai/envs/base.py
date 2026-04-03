from __future__ import annotations

import collections
import time
from dataclasses import dataclass

import numpy as np

from nes_ai.envs.gym_compat import gym


@dataclass(frozen=True)
class WrapperConfig:
    frame_stack_size: int = 9
    action_repeat: int = 6
    render: bool = False
    reset_round: bool = True
    render_sleep: float = 0.01
    observation_shape: tuple[int, int, int] = (112, 120, 3)


class BaseRetroWrapper(gym.Wrapper):
    def __init__(self, env, config: WrapperConfig | None = None):
        super().__init__(env)
        self.config = config or WrapperConfig()
        self.frame_stack = collections.deque(maxlen=self.config.frame_stack_size)
        self.observation_space = gym.spaces.Box(
            low=0,
            high=255,
            shape=self.config.observation_shape,
            dtype=np.uint8,
        )

    def preprocess_observation(self, observation):
        return observation[::2, ::2, :]

    def _normalize_reset(self, reset_result):
        if isinstance(reset_result, tuple):
            return reset_result[0]
        return reset_result

    def _normalize_step(self, step_result):
        if len(step_result) == 5:
            observation, reward, terminated, truncated, info = step_result
            return observation, reward, terminated or truncated, info
        observation, reward, done, info = step_result
        return observation, reward, done, info

    def _stack_observation(self):
        if len(self.frame_stack) < 3:
            raise RuntimeError("Frame stack does not contain enough frames.")
        frame_count = len(self.frame_stack)
        indices = [((channel + 1) * frame_count // 3) - 1 for channel in range(3)]
        return np.stack(
            [self.frame_stack[index][:, :, channel] for channel, index in enumerate(indices)],
            axis=-1,
        )

    def reset(self):
        self.reset_state()
        observation = self._normalize_reset(self.env.reset())
        processed = self.preprocess_observation(observation)
        self.frame_stack.clear()
        for _ in range(self.config.frame_stack_size):
            self.frame_stack.append(processed)
        return self._stack_observation()

    def step(self, action):
        final_info = {}
        env_done = False
        for _ in range(self.config.action_repeat):
            observation, _, step_done, info = self._normalize_step(self.env.step(action))
            final_info = info
            env_done = env_done or step_done
            self.frame_stack.append(self.preprocess_observation(observation))
            if self.config.render:
                self.render()
                time.sleep(self.config.render_sleep)
            if step_done:
                break

        reward = self.compute_reward(final_info)
        done = self.is_done(final_info) or env_done
        self.update_state(final_info)
        if not self.config.reset_round:
            done = False
        return self._stack_observation(), reward, done, final_info

    def reset_state(self):
        raise NotImplementedError

    def compute_reward(self, info):
        raise NotImplementedError

    def is_done(self, info):
        raise NotImplementedError

    def update_state(self, info):
        raise NotImplementedError
