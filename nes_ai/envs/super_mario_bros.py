from nes_ai.envs.base import BaseRetroWrapper


class SuperMarioBrosWrapper(BaseRetroWrapper):
    def reset_state(self):
        self.last_xscroll_lo = 999
        self.last_x_pos = 999
        self.last_time = -1
        self.last_score = 0
        self._death = False
        self._got_flag = False

    def compute_reward(self, info):
        self._death = info.get("player_state") in {6, 11} or info.get("y_viewport", 0) > 1
        self._got_flag = self._did_get_flag(info)

        xscroll_lo = info.get("xscrollLo", 0)
        time_left = info.get("time", self.last_time)
        x_pos = info.get("x_pos_a", 0) * 256 + info.get("x_pos_b", 0)

        death_penalty = -25.0 if self._death else 0.0
        xscroll_reward = 0.0
        x_pos_reward = 0.0
        flag_reward = 50.0 if self._got_flag else 0.0
        time_reward = 0.0

        if xscroll_lo - self.last_xscroll_lo > 0:
            xscroll_reward = xscroll_lo - self.last_xscroll_lo
        if -5 < x_pos - self.last_x_pos < 5:
            x_pos_reward = (x_pos - self.last_x_pos) * 2
        if time_left - self.last_time < 0:
            time_reward = (time_left - self.last_time) * 0.01

        return time_reward + xscroll_reward + x_pos_reward + flag_reward + death_penalty

    def is_done(self, info):
        return self._death or self._got_flag or info.get("lives", 0) < 1

    def update_state(self, info):
        self.last_xscroll_lo = info.get("xscrollLo", self.last_xscroll_lo)
        self.last_x_pos = info.get("x_pos_a", 0) * 256 + info.get("x_pos_b", 0)
        self.last_time = info.get("time", self.last_time)
        self.last_score = info.get("score", self.last_score)

    def _did_get_flag(self, info):
        enemy_positions = [info.get(f"enemy_pos_{index}", 0) for index in range(1, 8)]
        is_stage_over = any(position == 49 for position in enemy_positions) and info.get("is_stage_over") == 3
        return info.get("is_world_over") == 2 or is_stage_over

