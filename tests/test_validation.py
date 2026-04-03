import tempfile
import unittest
from pathlib import Path

from nes_ai.games.registry import list_games
from nes_ai.utils.validation import validate_asset_dir


class ValidationTests(unittest.TestCase):
    def test_missing_rom_file_raises_clear_error(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            with self.assertRaisesRegex(FileNotFoundError, "rom.nes"):
                validate_asset_dir(Path(tmp_dir))

    def test_registered_games_point_to_real_assets_and_default_states(self):
        for game in list_games():
            validate_asset_dir(game.asset_dir)
            self.assertTrue((game.asset_dir / f"{game.default_state}.state").exists())


if __name__ == "__main__":
    unittest.main()
