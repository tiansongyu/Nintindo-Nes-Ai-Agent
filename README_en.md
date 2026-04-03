# Nintindo-Nes-Ai-Agent
[English](https://github.com/tiansongyu/Nintindo-Nes-Ai-Agent/blob/main/README_en.md)|[中文](https://github.com/tiansongyu/Nintindo-Nes-Ai-Agent/blob/main/README.md)|

The purpose of this project is to use deep reinforcement learning to train Nintendo NES games, including complete environment setup, training process, viewing learning curves, and providing ROMs.
## List of Games

| order | game name |
| --- | --- |
| 1 | SuperMarioBros |
| 2 | TeenageMutantNinjaTurtlesTournamentFighters |
| 3 | FinalMission(SCATSpecialCyberneticAttackTeam) |
| 4 | RushnAttack |

## environment(windows linux)

```bash
# install conda
https://docs.anaconda.com/miniconda/
# downlaod code
git clone git@github.com:tiansongyu/Nintindo-Nes-Ai-Agent.git
# create conda environment,change name to Nintindo-Nes-Ai-Agent，Python version 3.8.10
conda create -n Nintindo-Nes-Ai-Agent python=3.8.10
conda activate Nintindo-Nes-Ai-Agent

# install Python requirements
python  -m pip install pip==24.0.0
pip install setuptools==65.5.0 wheel==0.38.4 -i https://pypi.tuna.tsinghua.edu.cn/simple
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

# Install ROM / state / data files into gym-retro
python -m nes_ai install-roms
```
### train model

```bash
python -m nes_ai train super-mario-bros
```

### view curves
```bash
tensorboard --logdir=artifacts/tensorboard/
```
Open the default address of the Tensorboard service http://localhost:6006/ in your browser to view the interactive training curves.

### view the result of training.

```bash
python -m nes_ai play super-mario-bros
```

### legacy commands

```bash
python set_up.py
python train.py 1
python run.py 1
```

These scripts still work, but now they only forward into the new `nes_ai` package entry point.

### display pictures

![SuperMarioBros](https://github.com/tiansongyu/Nintindo-Nes-Ai-Agent/raw/main/img/supermaiobros_nes.gif)
![NinjaTurtles](https://github.com/tiansongyu/Nintindo-Nes-Ai-Agent/raw/main/img/nijia_turtles_nes.gif)
![FinalMission](https://github.com/tiansongyu/Nintindo-Nes-Ai-Agent/raw/main/img/final_mission_nes.gif)


### tips
The project is highly integrated, with the environment configuration highly encapsulated, ready to use out of the box. Since gym retro supports up to Python 3.8, some tools need to use fixed versions. This is detailed in the environment configuration section. Please strictly follow the environment configuration instructions to avoid version mismatch issues.

Next, we will introduce the specific implementation logic of this project in detail. This project is mainly aimed at beginners who want to familiarize themselves with Python syntax and gain an intuitive understanding of reinforcement learning. The code structure is relatively simple and clear. We hope this sharing will encourage everyone to communicate and exchange ideas. Developers interested in creating similar small projects in the future are welcome to reach out at any time. Please note that ROMs are not included; you must obtain them yourself.
###  What is Gym Retro?
This project uses Gym Retro, which allows you to turn classic video games into Gym environments for reinforcement learning and integrates about 1000 games. It uses various emulators that support the Libretro API, making it relatively easy to add new emulators.

Each game integration includes files that list the memory locations of in-game variables, reward functions based on these variables, episode end conditions, save states at the start of levels, and files containing the ROM hashes used with these files.

The core principle is to read the game memory to obtain the status of game characters, environment, and other information, pass it to the reinforcement learning agent, use a certain reinforcement learning algorithm, output actions, write them back into the game memory, accumulate rewards, and obtain the strategy with the highest reward. Repeating this process can make the game characters "appear to be playing the game."

### What is Reinforcement Learning?
Reinforcement Learning (RL) is a machine learning (ML) technique that trains software to make decisions to achieve optimal outcomes. It mimics the trial-and-error learning process humans use to achieve goals. Actions that help achieve the goal are reinforced, while actions that deviate from the goal are ignored.

In reinforcement learning, several key concepts need to be familiarized with:

- Agent: The ML algorithm (or autonomous system)
- Environment: The adaptive problem space with attributes such as variables, boundary values, rules, and valid actions
- Action: The steps taken by the RL agent while navigating the environment
- State: The environment at a given point in time
- Reward: The positive, negative, or zero value for performing an action, in other words, the reward or punishment
- Cumulative Reward: The sum or final value of all rewards

### Implemented Games
1. SuperMarioBros  (Super Mario)
2. TeenageMutantNinjaTurtlesTournamentFighters (Ninja Turtles Fighting, as we called it in childhood)
3. FinalMission (SCAT Special Cybernetic Attack Team) (Final Mission or Air Contra, names given by bootleg manufacturers)
4. RushnAttack (Red Alert or Stabbing Game, for the same reason as above)

### Code Structure

The project now uses one modular package layout:

```text
nes_ai/
  games/        # game registry, default state, training config
  envs/         # shared Retro wrapper base + per-game reward logic
  training/     # PPO training, model loading, evaluation, checkpoints
  retro/        # gym-retro asset installation
  utils/        # shared helpers

assets/games/   # ROM, state, and memory metadata for each game
artifacts/      # models, tensorboard logs, evaluation summaries
```

Adding a new game now mainly means:

1. Put the new game's `rom.nes`, `rom.sha`, `data.json`, `metadata.json`, `scenario.json`, and `.state` files into `assets/games/<Retro game name>/`
2. Add one game definition module in `nes_ai/games/`
3. Add one wrapper module in `nes_ai/envs/` that only contains the reward and done logic for that game

This removes the previous need to edit multiple top-level scripts for every new title.

### Training Parameters

Training still uses PPO. Default hyperparameters now live in the `TrainConfig` attached to each game definition inside `nes_ai/games/*.py`.
```
    model = PPO(
        "CnnPolicy", 
        env,
        device="cuda", 
        verbose=1,
        n_steps=512,
        batch_size=512,
        n_epochs=4,
        gamma=0.94,
        learning_rate=lr_schedule,
        clip_range=clip_range_schedule,
        tensorboard_log=LOG_DIR + "/" + game
    )
```
You can override the main runtime settings from the CLI, for example:

```bash
python -m nes_ai train super-mario-bros --timesteps 50000000 --num-envs 10 --device cuda
```

Artifacts are now stored under:

```text
artifacts/models/<game-slug>/
artifacts/tensorboard/<game-slug>/
artifacts/evaluations/<game-slug>/
```
## THANKS

- [OpenAI Gym Retro](https://retro.readthedocs.io/en/latest/getting_started.html)
- [Stable-Baselines3](https://stable-baselines3.readthedocs.io/en/master/) 
- [linyi street fight ai](https://github.com/linyiLYi/street-fighter-ai)
