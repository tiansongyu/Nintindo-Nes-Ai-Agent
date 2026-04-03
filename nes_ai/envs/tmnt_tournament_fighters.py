import math

from nes_ai.envs.base import BaseRetroWrapper


class TMNTTournamentFightersWrapper(BaseRetroWrapper):
    def reset_state(self):
        self.reward_coeff = 3.0
        self.full_hp = 176
        self.prev_player_health = self.full_hp
        self.prev_opponent_health = self.full_hp
        self._terminal = False

    def compute_reward(self, info):
        current_player_health = info.get("health", self.prev_player_health)
        current_opponent_health = info.get("enemy_health", self.prev_opponent_health)

        if current_player_health < 1:
            self._terminal = True
            reward = -math.pow(self.full_hp, (current_opponent_health + 1) / (self.full_hp + 1))
        elif current_opponent_health < 1:
            self._terminal = True
            reward = math.pow(self.full_hp, (current_player_health + 1) / (self.full_hp + 1)) * self.reward_coeff
        else:
            self._terminal = False
            reward = (
                self.reward_coeff * (self.prev_opponent_health - current_opponent_health)
                - (self.prev_player_health - current_player_health)
            )

        return 0.001 * reward

    def is_done(self, info):
        return self._terminal

    def update_state(self, info):
        self.prev_player_health = info.get("health", self.prev_player_health)
        self.prev_opponent_health = info.get("enemy_health", self.prev_opponent_health)

