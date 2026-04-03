import unittest

import numpy as np

from nes_ai.envs.base import BaseRetroWrapper, WrapperConfig


class FakeActionSpace:
    def sample(self):
        return 0


class FakeEnv:
    def __init__(self):
        self.action_space = FakeActionSpace()
        self.reset_calls = 0
        self.step_calls = 0

    def reset(self):
        self.reset_calls += 1
        return np.zeros((224, 240, 3), dtype=np.uint8)

    def step(self, action):
        self.step_calls += 1
        obs = np.full((224, 240, 3), self.step_calls, dtype=np.uint8)
        info = {"score": self.step_calls}
        return obs, 0.0, False, info


class DemoWrapper(BaseRetroWrapper):
    def reset_state(self):
        self.last_score = 0

    def compute_reward(self, info):
        return float(info["score"] - self.last_score)

    def is_done(self, info):
        return False

    def update_state(self, info):
        self.last_score = info["score"]


class BaseWrapperTests(unittest.TestCase):
    def test_reset_builds_stacked_observation(self):
        env = DemoWrapper(FakeEnv(), WrapperConfig())
        obs = env.reset()
        self.assertEqual(obs.shape, (112, 120, 3))

    def test_step_repeats_action_and_uses_reward_hooks(self):
        env = DemoWrapper(FakeEnv(), WrapperConfig(action_repeat=4))
        env.reset()
        _, reward, done, info = env.step(0)
        self.assertEqual(reward, 4.0)
        self.assertFalse(done)
        self.assertEqual(info["score"], 4)


if __name__ == "__main__":
    unittest.main()

