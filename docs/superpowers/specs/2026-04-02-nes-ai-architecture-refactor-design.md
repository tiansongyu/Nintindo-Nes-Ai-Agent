# NES AI Architecture Refactor Design

**Date:** 2026-04-02

## Goal

Refactor the repository into a modular Python package so that training, playback, ROM installation, and game extension all run through one consistent architecture. The refactor must preserve current behavior, while making it materially easier to add new NES games and tune reward logic without rewriting entry scripts.

## Current Problems

### Scattered responsibilities

- `train.py`, `run.py`, and `set_up.py` each reimplement parts of environment creation and path handling.
- `common.py` mixes game registration, wrapper imports, and process-level path mutation.
- Each game directory contains similar wrapper and reward-check logic, but there is no shared abstraction for common behavior.

### Weak extension story

- Adding a new game currently requires touching multiple top-level scripts.
- Game definitions are expressed as untyped dictionaries, so configuration is hard to validate and easy to break.
- Training hyperparameters, model naming, and asset paths are not centrally owned.

### Operational fragility

- `os.walk('.')` plus `sys.path.append(...)` creates import order risk and hides packaging mistakes.
- Model lookup relies on filename parsing instead of a proper model store.
- Error handling is inconsistent for missing games, missing assets, or unavailable dependencies.

## Chosen Approach

Use a registry-based package architecture.

This design keeps the system simple enough for the current repository size while centralizing all game-specific variation into small, well-bounded modules. It avoids the overhead of a full plugin system, but still makes adding a game mostly a matter of creating one game definition module and one reward wrapper module.

## Architecture

### Package layout

```text
nes_ai/
  __init__.py
  __main__.py
  cli.py
  constants.py

  games/
    __init__.py
    base.py
    registry.py
    super_mario_bros.py
    rush_n_attack.py
    final_mission.py
    tmnt_tournament_fighters.py

  envs/
    __init__.py
    base.py
    factory.py
    super_mario_bros.py
    rush_n_attack.py
    final_mission.py
    tmnt_tournament_fighters.py

  training/
    __init__.py
    config.py
    schedules.py
    trainer.py
    evaluator.py
    model_store.py

  retro/
    __init__.py
    installer.py
    paths.py

  utils/
    __init__.py
    naming.py
    validation.py

assets/
  games/
    SuperMarioBros-Nes/
    RushnAttack-Nes/
    SCATSpecialCyberneticAttackTeam-Nes/
    TeenageMutantNinjaTurtlesTournamentFighters-Nes/
```

### Module responsibilities

- `nes_ai.games`
  Owns typed game definitions. A game definition contains the slug, display name, Retro game id, default state, asset directory, wrapper class, and default training config.

- `nes_ai.envs`
  Owns environment wrappers. Shared frame stacking, frame skipping, rendering, and observation preprocessing live in the base wrapper. Each game wrapper only implements reward logic, internal state tracking, and custom termination conditions.

- `nes_ai.training`
  Owns PPO training, model playback, schedules, output paths, and model discovery.

- `nes_ai.retro`
  Owns ROM and metadata installation into the Gym Retro stable data directory.

- `nes_ai.cli`
  Owns the single public command surface for listing games, installing ROM assets, training, playback, and reward checks.

## Data Model

### Training configuration

Training defaults move into a dataclass instead of remaining scattered in scripts.

```python
@dataclass(frozen=True)
class TrainConfig:
    num_envs: int = 10
    total_timesteps: int = 50_000_000
    n_steps: int = 512
    batch_size: int = 512
    n_epochs: int = 4
    gamma: float = 0.94
    learning_rate_start: float = 2.5e-4
    learning_rate_end: float = 2.5e-6
    clip_range_start: float = 0.15
    clip_range_end: float = 0.025
    checkpoint_interval: int = 15_000
    device: str = "cuda"
```

### Game definition

Each game module returns one `GameDefinition`.

```python
@dataclass(frozen=True)
class GameDefinition:
    slug: str
    display_name: str
    retro_game: str
    default_state: str
    asset_dir: Path
    wrapper_cls: type
    train_config: TrainConfig
```

This gives one explicit object that every workflow can depend on.

## CLI Design

All operations move behind one command entry point:

```bash
python -m nes_ai list-games
python -m nes_ai install-roms
python -m nes_ai train super-mario-bros
python -m nes_ai play super-mario-bros
python -m nes_ai check-reward super-mario-bros
```

Optional overrides remain available:

```bash
python -m nes_ai train super-mario-bros --timesteps 50000000 --num-envs 10 --device cuda
python -m nes_ai play rush-n-attack --model latest --render true
```

The CLI stays on `argparse` to avoid new dependencies.

## Environment Design

### Shared base wrapper

The base wrapper owns the common mechanics currently duplicated in each game wrapper:

- initialize frame stack
- preprocess observations to `(112, 120, 3)`
- repeat each action for multiple emulator frames
- render and sleep when requested
- return stacked observations in a consistent format

Its extension points are:

- `reset_state()`
- `compute_reward(info)`
- `is_done(info)`
- `update_state(info)`

### Game-specific wrappers

Each game wrapper is reduced to reward and termination logic only.

Examples:

- `SuperMarioBrosWrapper` keeps x-position, scrolling, flag, timer, and death logic.
- `RushnAttackWrapper` keeps score, lives, scrolling, and screen-position logic.
- `FinalMissionWrapper` keeps score and lives logic.
- `TeenageMutantNinjaTurtlesTournamentFightersWrapper` keeps player and enemy health logic.

This keeps future game additions focused on memory interpretation rather than pipeline wiring.

## Artifacts and Paths

Training outputs move into a normalized structure:

```text
artifacts/
  models/
    super-mario-bros/
      latest.zip
      training.log
      checkpoints/
        step_150000.zip
        step_300000.zip
  tensorboard/
    super-mario-bros/
  evaluations/
    super-mario-bros/
      latest_run.txt
      random_policy.txt
```

Benefits:

- one directory per game
- stable default model path via `latest.zip`
- no regex-based "largest checkpoint filename" lookup
- cleaner separation between checkpoints, logs, and final models

## ROM Asset Installation

The previous `set_up.py` behavior becomes `python -m nes_ai install-roms`.

The installer:

1. Reads all registered `GameDefinition` objects
2. Validates required files in each `asset_dir`
3. Locates Gym Retro's stable data directory
4. Copies the files into the matching Retro game directory

Required asset files are:

- `rom.nes`
- `rom.sha`
- `data.json`
- `metadata.json`
- `scenario.json`
- one or more `.state` files

## Backward Compatibility

The new structure becomes the primary workflow, but root-level compatibility shims remain:

- `train.py`
- `run.py`
- `set_up.py`

Each old entry script becomes a thin forwarder into `nes_ai.cli`. This preserves existing habits during migration while preventing business logic from living in two places.

Existing asset contents and trained model behavior remain supported. Model storage paths will change, but CLI behavior remains functionally equivalent.

## Error Handling

The refactor should explicitly handle:

- unknown game slug
- missing asset directory or required asset file
- missing model or checkpoint
- unavailable optional dependencies such as `retro` or `stable_baselines3`
- requested CUDA device when CUDA is not available

Errors should be actionable, naming the missing game, file, model, or dependency directly.

## Testing Strategy

### Unit tests

Add tests for:

- game registry lookup and listing
- artifact and model path resolution
- latest model selection
- asset validation
- CLI argument parsing and command routing

These tests should not require `retro` or `stable_baselines3`.

### Wrapper integration tests

Use a stub Gym environment to test the shared base wrapper:

- reset fills the frame stack correctly
- step repeats an action the configured number of frames
- output observation shape matches `(112, 120, 3)`
- reward and done hooks are invoked in the expected order

### Verification checks

At minimum, the refactor must support:

- `python -m compileall nes_ai train.py run.py set_up.py`
- unit tests that exercise the new package without optional runtime dependencies
- CLI help and command parsing on machines that do not have Retro installed

## Non-Goals

This refactor does not include:

- changing the PPO algorithm
- redesigning reward functions beyond what is needed to preserve current behavior
- introducing a plugin loading system
- changing ROM contents or memory-hacking workflow

## Implementation Direction

Implementation should proceed in three phases:

1. Build the package, registry, shared wrapper base, artifact store, and unified CLI.
2. Migrate all four existing games onto the new architecture and add compatibility shims.
3. Add tests, run compilation and test verification, then update documentation to point to the new commands.

## Expected Outcome

After the refactor, adding a new game should mostly require:

1. placing Retro assets into `assets/games/<retro-game>/`
2. writing one game definition module
3. writing one reward wrapper module

The training and playback pipeline should not require edits for each new title.
