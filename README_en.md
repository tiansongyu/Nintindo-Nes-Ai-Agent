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

# Run the script to locate the gym-retro game folder
python set_up.py
```
### train model

```bash
python train.py 1 
```

### view curves
```bash
tensorboard --logdir=logs/
```
Open the default address of the Tensorboard service http://localhost:6006/ in your browser to view the interactive training curves.

### view the result of training.

```bash
python run.py 1 
```

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

### Code Structure, Using Super Mario as an Example
The Super Mario directory is SuperMarioBros_PPO
#### - common.py Encapsulates a general wrapper. If you want to add a new game, you need to modify this file and add a class for the individual game.
#### set_up.py
The set_up.py file is a tool responsible for initializing the gym retro file structure. This file places the game's ROM file, state file, scenario.json, rom.sha, and data.json in the corresponding locations in gym retro. Readers need to study the [getting started guide](https://retro.readthedocs.io/en/latest/getting_started.html) to understand why this is necessary.
#### rom Folder
- data.json stores the memory information and environment information of the game characters. This information needs to be manually obtained using Cheat Engine or gym's built-in tools. The addresses are provided here. If it's a new game, you need to manually hack to obtain these key pieces of information required for training. I can provide a separate tutorial on memory hacking if needed.
- rom.nes is the SHA code of the game ROM file, which must correspond to the rom.sha included in gym.
- rom.sha is the SHA code of the game ROM file, which must correspond to the rom.sha included in gym.
- state files are game levels. Gym can import these to directly train on a specific level.
- metadata.json  and scenario.json store the reinforcement learning parameters provided by gym. They are not very effective, so this project does not use them and will not elaborate on them.  
This class has a base class that inherits from gym.Wrapper, which is part of gym. We needto implement the step and reset functions. step is executed every frame and will beautomatically executed by gym once started. reset is the initialization function.  
The step and reset functions are the core content of the code. Below is the basic running logic of the entire program:
1. The program continuously captures the color space of the entire gym screen, converts it into a 112x120 RGB matrix, and passes it to the observation space of the reinforcement learning environment as the current state.
2. By reading memory content, including using functions like info['lives'], info['time'], info['score'], info['x_pos_b'], info['x_pos_a'], and info['player_state'], it obtains information such as the character's lives, current time, current score, character coordinates, and character's life status. These are then combined with different weights to get the reward. All weights need to be continuously tested and adjusted based on experience to ensure that all game data converges.
3. The reset function is responsible for initializing values each time the game restarts.
#### run.py
本文件读取trained_models下的目录的训练好的模型，进行模型回放操作。
#### train.py
This file mainly configures the reinforcement learning parameters and uses the PPO algorithm. The core parameters may vary for each game, and readers need to adjust the details according to different games and computer performance. The parameters are the basic parameters of the PPO algorithm, and you can use the project's defaults unless there are special requirements.
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
Modify this section to control the number of training iterations.
```
    checkpoint_interval = 15000 # checkpoint_interval * num_envs = total_steps_per_checkpoint
    checkpoint_callback = CheckpointCallback(save_freq=checkpoint_interval, save_path=save_dir, name_prefix="ppo_"+game)

    original_stdout = sys.stdout
    log_file_path = os.path.join(save_dir, "training_log.txt")
    with open(log_file_path, 'w') as log_file:
        sys.stdout = log_file
    
        model.learn(
            total_timesteps=int(50000000),
            callback=[checkpoint_callback]
        )
```
the save path is 
```
    model.save(os.path.join(save_dir, "ppo_" + game + ".zip"))
```
## THANKS

- [OpenAI Gym Retro](https://retro.readthedocs.io/en/latest/getting_started.html)
- [Stable-Baselines3](https://stable-baselines3.readthedocs.io/en/master/) 
- [linyi street fight ai](https://github.com/linyiLYi/street-fighter-ai)
