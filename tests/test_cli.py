import io
import unittest
from unittest import mock

from nes_ai.cli import build_parser, main


class CliTests(unittest.TestCase):
    def test_train_parser_accepts_game_slug(self):
        parser = build_parser()
        args = parser.parse_args(["train", "super-mario-bros"])
        self.assertEqual(args.command, "train")
        self.assertEqual(args.game, "super-mario-bros")

    def test_list_games_parser(self):
        parser = build_parser()
        args = parser.parse_args(["list-games"])
        self.assertEqual(args.command, "list-games")

    def test_runtime_errors_are_reported_without_traceback(self):
        stderr = io.StringIO()
        with mock.patch("nes_ai.cli.install_roms", side_effect=RuntimeError("gym-retro is required")):
            with mock.patch("sys.stderr", stderr):
                exit_code = main(["install-roms"])
        self.assertEqual(exit_code, 1)
        self.assertIn("gym-retro is required", stderr.getvalue())


if __name__ == "__main__":
    unittest.main()
