import sys
import unittest
from unittest import mock

import nes_ai.legacy as legacy
import run as legacy_run
import train as legacy_train


class LegacyScriptTests(unittest.TestCase):
    def test_run_script_allows_no_render_override(self):
        with mock.patch.object(sys, "argv", ["run.py", "1", "--episodes", "1", "--no-render"]):
            with mock.patch.object(legacy, "cli_main", return_value=0) as cli_main:
                exit_code = legacy_run.main()
        self.assertEqual(exit_code, 0)
        cli_main.assert_called_once_with(
            ["play", "super-mario-bros", "--episodes", "1", "--no-render"]
        )

    def test_run_script_renders_by_default(self):
        with mock.patch.object(sys, "argv", ["run.py", "1"]):
            with mock.patch.object(legacy, "cli_main", return_value=0) as cli_main:
                exit_code = legacy_run.main()
        self.assertEqual(exit_code, 0)
        cli_main.assert_called_once_with(["play", "super-mario-bros", "--render"])

    def test_train_script_translates_legacy_render_flag(self):
        with mock.patch.object(sys, "argv", ["train.py", "1", "--IsRender", "true"]):
            with mock.patch.object(legacy, "cli_main", return_value=0) as cli_main:
                exit_code = legacy_train.main()
        self.assertEqual(exit_code, 0)
        cli_main.assert_called_once_with(["train", "super-mario-bros", "--render"])


if __name__ == "__main__":
    unittest.main()
