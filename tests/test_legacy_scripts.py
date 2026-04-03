import sys
import unittest
from unittest import mock

import run as legacy_run


class LegacyScriptTests(unittest.TestCase):
    def test_run_script_allows_no_render_override(self):
        with mock.patch.object(sys, "argv", ["run.py", "1", "--episodes", "1", "--no-render"]):
            with mock.patch.object(legacy_run, "cli_main", return_value=0) as cli_main:
                exit_code = legacy_run.main()
        self.assertEqual(exit_code, 0)
        cli_main.assert_called_once_with(
            ["play", "super-mario-bros", "--episodes", "1", "--no-render"]
        )


if __name__ == "__main__":
    unittest.main()
