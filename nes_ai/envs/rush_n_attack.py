from nes_ai.envs.base import BaseRetroWrapper


class RushNAttackWrapper(BaseRetroWrapper):
    def reset_state(self):
        self.last_scores = 0
        self.last_lives = 0
        self.last_xscroll = 0
        self.last_x_pos = 0
        self._out_of_lives = False

    def compute_reward(self, info):
        lives = info.get("lives", 0)
        scores = info.get("score", 0)
        xscroll = info.get("xscrollLo", 0) + info.get("xscrollHi", 0) * 256
        x_pos_in_screen = info.get("x_pos_in_screen", 0)

        reward_scores = 0
        reward_lives = 0
        reward_xscroll = 0
        reward_x_pos = 0

        if self.last_scores < scores:
            reward_scores = (scores - self.last_scores) * 4
        if self.last_lives > lives:
            reward_lives = -200
        if self.last_xscroll < xscroll:
            reward_xscroll = xscroll - self.last_xscroll
        reward_x_pos = (x_pos_in_screen - self.last_x_pos) * 0.1

        self._out_of_lives = lives < 1
        return 0.01 * (reward_lives + reward_scores + reward_xscroll + reward_x_pos)

    def is_done(self, info):
        return self._out_of_lives

    def update_state(self, info):
        self.last_scores = info.get("score", self.last_scores)
        self.last_lives = info.get("lives", self.last_lives)
        self.last_xscroll = info.get("xscrollLo", 0) + info.get("xscrollHi", 0) * 256
        self.last_x_pos = info.get("x_pos_in_screen", self.last_x_pos)

