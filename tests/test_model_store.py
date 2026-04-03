import unittest

from nes_ai.games.registry import get_game
from nes_ai.training.model_store import ModelStore


class ModelStoreTests(unittest.TestCase):
    def test_paths_are_namespaced_by_game(self):
        store = ModelStore.for_game(get_game("super-mario-bros"))
        self.assertEqual(store.latest_model_path.name, "latest.zip")
        self.assertIn("super-mario-bros", str(store.model_dir))


if __name__ == "__main__":
    unittest.main()

