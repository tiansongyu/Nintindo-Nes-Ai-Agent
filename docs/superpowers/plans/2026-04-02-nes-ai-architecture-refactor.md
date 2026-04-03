# NES AI Architecture Refactor Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Rebuild the repository around a modular `nes_ai` package so training, playback, ROM installation, and adding games all share one typed, testable architecture.

**Architecture:** Create a registry-driven package with lazy optional dependencies, a shared retro wrapper base, centralized training/model storage modules, and compatibility shims for the old scripts. Keep game-specific reward logic isolated while unifying environment creation, artifact paths, and CLI behavior.

**Tech Stack:** Python 3, `argparse`, `dataclasses`, Gym Retro, Stable-Baselines3, `unittest`, `compileall`

---

### Task 1: Package Scaffold, Registry, and Path Model

**Files:**
- Create: `nes_ai/__init__.py`
- Create: `nes_ai/__main__.py`
- Create: `nes_ai/constants.py`
- Create: `nes_ai/games/__init__.py`
- Create: `nes_ai/games/base.py`
- Create: `nes_ai/games/registry.py`
- Create: `nes_ai/games/super_mario_bros.py`
- Create: `nes_ai/games/rush_n_attack.py`
- Create: `nes_ai/games/final_mission.py`
- Create: `nes_ai/games/tmnt_tournament_fighters.py`
- Create: `nes_ai/utils/__init__.py`
- Create: `nes_ai/utils/naming.py`
- Create: `nes_ai/utils/validation.py`
- Test: `tests/test_registry.py`

- [ ] **Step 1: Write the failing registry and path tests**

```python
import unittest

from nes_ai.games.registry import get_game, list_games
from nes_ai.constants import PROJECT_ROOT


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

    def test_project_root_points_to_repository(self):
        self.assertTrue((PROJECT_ROOT / "README.md").exists())
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python -m unittest tests.test_registry -v`
Expected: FAIL with `ModuleNotFoundError: No module named 'nes_ai'`

- [ ] **Step 3: Write the minimal package scaffold and registry**

```python
@dataclass(frozen=True)
class GameDefinition:
    slug: str
    legacy_number: str
    retro_game: str
    default_state: str
    wrapper_path: str
    asset_dir: Path
    train_config: TrainConfig


def get_game(identifier: str) -> GameDefinition:
    normalized = normalize_identifier(identifier)
    ...
```

- [ ] **Step 4: Run test to verify it passes**

Run: `python -m unittest tests.test_registry -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add nes_ai tests/test_registry.py docs/superpowers/plans/2026-04-02-nes-ai-architecture-refactor.md
git commit -m "refactor: add package scaffold and game registry"
```

### Task 2: Shared Wrapper Base and Environment Tests

**Files:**
- Create: `nes_ai/envs/__init__.py`
- Create: `nes_ai/envs/gym_compat.py`
- Create: `nes_ai/envs/base.py`
- Create: `nes_ai/envs/factory.py`
- Create: `nes_ai/envs/super_mario_bros.py`
- Create: `nes_ai/envs/rush_n_attack.py`
- Create: `nes_ai/envs/final_mission.py`
- Create: `nes_ai/envs/tmnt_tournament_fighters.py`
- Test: `tests/test_env_base.py`

- [ ] **Step 1: Write the failing wrapper tests**

```python
import unittest
import numpy as np

from nes_ai.envs.base import BaseRetroWrapper, WrapperConfig


class FakeEnv:
    def __init__(self):
        self.action_space = type("ActionSpace", (), {"sample": lambda self: 0})()
        self.reset_calls = 0
        self.step_calls = 0

    def reset(self):
        self.reset_calls += 1
        return np.zeros((224, 240, 3), dtype=np.uint8)

    def step(self, action):
        self.step_calls += 1
        obs = np.full((224, 240, 3), self.step_calls, dtype=np.uint8)
        info = {"score": self.step_calls}
        return obs, 0.0, False, info


class DemoWrapper(BaseRetroWrapper):
    def reset_state(self):
        self.last_score = 0

    def compute_reward(self, info):
        return float(info["score"] - self.last_score)

    def is_done(self, info):
        return False

    def update_state(self, info):
        self.last_score = info["score"]


class BaseWrapperTests(unittest.TestCase):
    def test_reset_builds_stacked_observation(self):
        env = DemoWrapper(FakeEnv(), WrapperConfig())
        obs = env.reset()
        self.assertEqual(obs.shape, (112, 120, 3))

    def test_step_repeats_action_and_uses_reward_hooks(self):
        env = DemoWrapper(FakeEnv(), WrapperConfig(action_repeat=4))
        env.reset()
        _, reward, done, info = env.step(0)
        self.assertEqual(reward, 4.0)
        self.assertFalse(done)
        self.assertEqual(info["score"], 4)
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python -m unittest tests.test_env_base -v`
Expected: FAIL because `BaseRetroWrapper` and `WrapperConfig` are missing

- [ ] **Step 3: Write the shared wrapper base and game wrappers**

```python
@dataclass(frozen=True)
class WrapperConfig:
    frame_stack_size: int = 9
    action_repeat: int = 6
    render: bool = False
    reset_round: bool = True
    render_sleep: float = 0.01


class BaseRetroWrapper(gym.Wrapper):
    def step(self, action):
        final_info = {}
        for _ in range(self.config.action_repeat):
            observation, _, _, info = self.env.step(action)
            ...
        reward = self.compute_reward(final_info)
        done = self.is_done(final_info)
        self.update_state(final_info)
        return self._stack_observation(), reward, done, final_info
```

- [ ] **Step 4: Run test to verify it passes**

Run: `python -m unittest tests.test_env_base -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add nes_ai/envs tests/test_env_base.py
git commit -m "refactor: add shared retro wrapper base"
```

### Task 3: Training, Model Storage, CLI, and Compatibility Shims

**Files:**
- Create: `nes_ai/training/__init__.py`
- Create: `nes_ai/training/schedules.py`
- Create: `nes_ai/training/model_store.py`
- Create: `nes_ai/training/trainer.py`
- Create: `nes_ai/training/evaluator.py`
- Create: `nes_ai/retro/__init__.py`
- Create: `nes_ai/retro/paths.py`
- Create: `nes_ai/retro/installer.py`
- Create: `nes_ai/cli.py`
- Modify: `train.py`
- Modify: `run.py`
- Modify: `set_up.py`
- Modify: `common.py`
- Test: `tests/test_cli.py`
- Test: `tests/test_model_store.py`

- [ ] **Step 1: Write the failing CLI and model store tests**

```python
import unittest

from nes_ai.cli import build_parser
from nes_ai.training.model_store import ModelStore
from nes_ai.games.registry import get_game


class CliTests(unittest.TestCase):
    def test_train_parser_accepts_game_slug(self):
        parser = build_parser()
        args = parser.parse_args(["train", "super-mario-bros"])
        self.assertEqual(args.command, "train")
        self.assertEqual(args.game, "super-mario-bros")


class ModelStoreTests(unittest.TestCase):
    def test_paths_are_namespaced_by_game(self):
        store = ModelStore.for_game(get_game("super-mario-bros"))
        self.assertEqual(store.latest_model_path.name, "latest.zip")
        self.assertIn("super-mario-bros", str(store.model_dir))
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python -m unittest tests.test_cli tests.test_model_store -v`
Expected: FAIL because parser and model store are missing

- [ ] **Step 3: Write the CLI, model store, lazy dependency loading, and shims**

```python
def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="nes_ai")
    subparsers = parser.add_subparsers(dest="command", required=True)
    ...
    return parser


class ModelStore:
    @classmethod
    def for_game(cls, game: GameDefinition) -> "ModelStore":
        model_dir = ARTIFACTS_DIR / "models" / game.slug
        return cls(model_dir=model_dir, ...)
```

- [ ] **Step 4: Run test to verify it passes**

Run: `python -m unittest tests.test_cli tests.test_model_store -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add nes_ai train.py run.py set_up.py common.py tests/test_cli.py tests/test_model_store.py
git commit -m "refactor: add unified cli and model storage"
```

### Task 4: Asset Migration, Reward Check Shims, and Documentation

**Files:**
- Create: `assets/games/`
- Modify: `FinalMission_PPO/check_reward.py`
- Modify: `RushnAttack_PPO/check_reward.py`
- Modify: `SuperMarioBros_PPO/check_reward.py`
- Modify: `TeenageMutantNinjaTurtlesTournamentFighters/check_reward.py`
- Modify: `README.md`
- Modify: `README_en.md`
- Test: `tests/test_validation.py`

- [ ] **Step 1: Write the failing asset validation test**

```python
import tempfile
import unittest
from pathlib import Path

from nes_ai.utils.validation import validate_asset_dir


class ValidationTests(unittest.TestCase):
    def test_missing_rom_file_raises_clear_error(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            with self.assertRaisesRegex(FileNotFoundError, "rom.nes"):
                validate_asset_dir(Path(tmp_dir))
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python -m unittest tests.test_validation -v`
Expected: FAIL because `validate_asset_dir` is missing or incomplete

- [ ] **Step 3: Implement validation, migrate assets, and update docs/shims**

```python
REQUIRED_ASSET_FILES = (
    "rom.nes",
    "rom.sha",
    "data.json",
    "metadata.json",
    "scenario.json",
)


def validate_asset_dir(asset_dir: Path) -> None:
    for file_name in REQUIRED_ASSET_FILES:
        path = asset_dir / file_name
        if not path.exists():
            raise FileNotFoundError(f"Missing required asset file: {path}")
```

- [ ] **Step 4: Run verification commands**

Run: `python -m unittest discover -s tests -v`
Expected: PASS

Run: `python -m compileall nes_ai train.py run.py set_up.py common.py`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add assets README.md README_en.md FinalMission_PPO/check_reward.py RushnAttack_PPO/check_reward.py SuperMarioBros_PPO/check_reward.py TeenageMutantNinjaTurtlesTournamentFighters/check_reward.py tests/test_validation.py
git commit -m "refactor: migrate assets and update documentation"
```
