from nes_ai.envs.base import BaseRetroWrapper


class FinalMissionWrapper(BaseRetroWrapper):
    def reset_state(self):
        self.last_scores = 0
        self.last_lives = 6
        self._out_of_lives = False

    def compute_reward(self, info):
        lives = info.get("lives", 0)
        scores = info.get("scores", 0)

        reward_scores = 0
        reward_lives = 0
        if self.last_scores < scores:
            reward_scores = (scores - self.last_scores) * 2
        if self.last_lives > lives:
            reward_lives = -100

        self._out_of_lives = lives < 1
        return 0.01 * (reward_lives + reward_scores)

    def is_done(self, info):
        return self._out_of_lives

    def update_state(self, info):
        self.last_scores = info.get("scores", self.last_scores)
        self.last_lives = info.get("lives", self.last_lives)

