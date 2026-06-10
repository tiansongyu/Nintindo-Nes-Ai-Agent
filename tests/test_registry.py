import unittest

from nes_ai.constants import PROJECT_ROOT
from nes_ai.envs.base import BaseRetroWrapper
from nes_ai.games.registry import get_game, list_games


class RegistryTests(unittest.TestCase):
    def test_lookup_by_slug_and_legacy_number(self):
        self.assertEqual(get_game("super-mario-bros").retro_game, "SuperMarioBros-Nes")
        self.assertEqual(get_game("1").slug, "super-mario-bros")

    def test_list_games_contains_all_current_titles(self):
        slugs = [game.slug for game in list_games()]
        self.assertEqual(
            slugs,
            [
                "super-mario-bros",
                "tmnt-tournament-fighters",
                "final-mission",
                "rush-n-attack",
            ],
        )

    def test_every_game_uses_a_retro_wrapper(self):
        for game in list_games():
            self.assertTrue(issubclass(game.wrapper, BaseRetroWrapper))

    def test_project_root_points_to_repository(self):
        self.assertTrue((PROJECT_ROOT / "README.md").exists())


if __name__ == "__main__":
    unittest.main()

