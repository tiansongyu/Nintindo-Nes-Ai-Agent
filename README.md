# Nintindo-Nes-Ai-Agent
[English](https://github.com/tiansongyu/Nintindo-Nes-Ai-Agent/blob/main/README_en.md)|[中文](https://github.com/tiansongyu/Nintindo-Nes-Ai-Agent/blob/main/README.md)

本项目目的使用深度强化学习训练任天堂nes游戏，包括完整环境配置，训练过程，查看学习曲线，提供rom。

## List of Games

| 序号 | 游戏名称 |
| --- | --- |
| 1 | SuperMarioBros |
| 2 | TeenageMutantNinjaTurtlesTournamentFighters |
| 3 | FinalMission(SCATSpecialCyberneticAttackTeam) |
| 4 | RushnAttack |

## 环境配置(windows linux mac),所有命令一行一行执行

```bash
# 安装nvidia驱动
https://www.nvidia.cn/geforce/drivers/
# 安装cuda + cuDNN(注意版本对应关系）cuda 使用的是11.8
https://developer.nvidia.com/cuda-toolkit-archive # cuda 使用的是11.8
https://developer.nvidia.com/rdp/cudnn-archive
# 查看pytorch 和 cuda对应的版本
https://pytorch.org/get-started/previous-versions/

# 安装conda
https://www.anaconda.com/download/success#miniconda
# 下载代码
git clone git@github.com:tiansongyu/Nintindo-Nes-Ai-Agent.git
# 创建 conda 环境，将其命名为 Nintindo-Nes-Ai-Agent，Python 版本 3.8.10
conda create -n Nintindo-Nes-Ai-Agent python=3.8.10
conda activate Nintindo-Nes-Ai-Agent

cd Nintindo-Nes-Ai-Agent
# 安装 Python 代码库
python -m pip install --upgrade pip==24.0 -i https://pypi.tuna.tsinghua.edu.cn/simple
pip install setuptools==65.5.0 wheel==0.38.4 -i https://pypi.tuna.tsinghua.edu.cn/simple
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
# 卸载原有的cpu版本torch
pip uninstall torch
# 安装cuda版本torch
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
# 如果下载速度很慢
# 直接去下载wheel文件 https://download.pytorch.org/whl/cu118/torch-2.4.1%2Bcu118-cp38-cp38-win_amd64.whl
# pip instlal torch-2.4.1+cu118-cp38-cp38-win_amd64.whl
# 运行程序脚本定位 gym-retro 游戏文件夹位置
python set_up.py
```

### 查看训练结果

```bash
python run.py 1 
```

### 训练模型

```bash
python train.py 1
```

### 查看曲线
```bash
tensorboard --logdir=logs/
```
在浏览器中打开 Tensorboard 服务默认地址 `http://localhost:6006/`，即可查看训练过程的交互式曲线图。

### 示例图片

![SuperMarioBros](https://github.com/tiansongyu/Nintindo-Nes-Ai-Agent/raw/main/img/supermaiobros_nes.gif)
![NinjaTurtles](https://github.com/tiansongyu/Nintindo-Nes-Ai-Agent/raw/main/img/nijia_turtles_nes.gif)
![FinalMission](https://github.com/tiansongyu/Nintindo-Nes-Ai-Agent/raw/main/img/final_mission_nes.gif)


### tips
项目的集成度比较高，将环境配置高度封装，开包即用，由于gym retro最高支持python3.8，某些工具需要使用固定版本，本文在环境配置部分已经详细说明，请严格按照环境配置指示，否则大概率出现版本不匹配问题。

接下来详细介绍该项目的具体实现逻辑，该项目主要面向想要熟悉python语法、想直观了解强化学习等基础学习者，代码结构较为简单清晰，希望这个分享让大家一起交流起来，后续有兴趣做类似小东西的开发者可以随时交流。请注意，ROM 不包含在内，您必须自行获取。
### 
- 什么是gym retro？
本项目使用了Gym Retro,它可让您将经典视频游戏转变为Gym环境以进行强化学习，并集成了约 1000 款游戏。它使用支持Libretro API的各种模拟器，因此可以相当轻松地添加新的模拟器。
每个游戏集成都有文件列出游戏内变量的内存位置、基于这些变量的奖励函数、情节结束条件、关卡开始时的保存状态以及包含与这些文件一起使用的 ROM 哈希值的文件。
核心原理是通过读取游戏内存，获取游戏人物状态、环境等信息，传递給强化学习agent，使用某种强化学习算法，并输出操作，写入游戏内存，累积奖励，获取奖励最高的策略，如此反复，可以让游戏人物“看起来在玩游戏”。
- 什么是强化学习？
强化学习（RL）是一种机器学习（ML）技术，可以训练软件做出决策，以实现最佳结果。它模仿了人类为实现目标所采取的反复试验的学习过程。有助于实现目标的软件操作会得到加强，而偏离目标的操作将被忽略。 
在强化学习中，需要熟悉几个关键概念：
代理是 ML 算法（或自治系统）
环境是具有变量、边界值、规则和有效操作等属性的自适应问题空间
操作是 RL 代理在环境中导航时采取的步骤
状态是给定时间点的环境
奖励是执行操作的正值、负值或零值，换句话说就是奖励或惩罚
累积奖励是所有奖励的总和或最终值

### 已经实现的游戏
1. SuperMarioBros  (超级马里奥)
2. TeenageMutantNinjaTurtlesTournamentFighters(神龟对打 ps:小时候这么称呼)
3. FinalMission(SCATSpecialCyberneticAttackTeam)(最终任务 or 空中魂斗罗ps:盗版厂商乱起的名字)
4. RushnAttack (绿色兵团 or 红色警戒 or 捅刀子的 原因同上2)

### 代码结构，以超级马里奥为例
超级马里奥目录为SuperMarioBros_PPO
#### - common.py 封装了一个总的wrapper，如果要添加新游戏，需要修改这个文件，需要添加单个游戏的类。
#### set_up.py
set_up.py文件是负责初始化gym retro文件结构的工具，本文件将游戏的rom文件、state文件、scenario.json、rom.sha、data.json放置到gym retro中对应的位置，读者需要研读https://retro.readthedocs.io/en/latest/getting_started.html 可以理解为何需要这样做，
#### rom文件夹
- data.json存放该游戏的游戏人物内存信息、环境信息，需要手动通过cheat engine或gym自带工具获取人物以及环境信息，这里我已经给出地址，如果是新游戏需要大家手动进行hack，获取这些这些训练需要的关键信息，内存hack方法我可以单独出一期教程，有需要可以回复~~~
- rom.nes是游戏文件，需要自己获取
- rom.sha是游戏rom文件sha码，它必须对应gym中自带的rom.sha
- state后缀文件游戏关卡，gym导入它可以直接进行某一个关卡的训练
- metadata.json 和scenario.json存放gym自带强化学习参数，效果并不好，本项目没有使用，不赘述
#### SuperMarioBrosWrapper.py 
 类中有一个基类继承自gym.Wrapper，它是gym的一部分，我们需要实现step和reset函数
step是每一帧执行内容，开启后gym会自动执行，reset是初始化函数
step和reset是代码的核心内容，下面阐述整个程序基本运行逻辑：
1. 程序不断获取gym整个屏幕的色彩空间，转为一个112x120的RGB矩阵，代表此时的状态传入强化学习的环境部分observation_space。
2. 通过读取内存内容，包括使用info['lives']、info['time']、info['score']、['x_pos_b']、info['x_pos_a']、info['player_state']等函数获取人物的生命、此时时间、此时分数、人物坐标、人物生死状态等信息，再使用不同权重，相加得到reward，其中所有的权重需要不断测试根据经验给出，才能让游戏所有数据处于收敛状态。
3. reset函数负责初始化每次游戏重新开始时的值。
#### run.py
本文件读取trained_models下的目录的训练好的模型，进行模型回放操作。
#### train.py
本文件主要是强化学习参数的配置，使用了PPO算法，核心参数每个游戏可能并不相同，需要读者根据不同游戏不同电脑性能进行细节调整，参数为PPO算法的基本参数，没有特殊需要使用项目的即可。
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
修改 这部分内容可以控制训练次数
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
存放路径为
```
    model.save(os.path.join(save_dir, "ppo_" + game + ".zip"))
```
## 致谢

本项目使用了 
- [OpenAI Gym Retro](https://retro.readthedocs.io/en/latest/getting_started.html)
- [Stable-Baselines3](https://stable-baselines3.readthedocs.io/en/master/) 
- [linyi street fight ai](https://github.com/linyiLYi/street-fighter-ai)
