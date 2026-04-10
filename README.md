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
python -m pip install --upgrade pip==24.0 
pip install -r requirements.txt 
# 安装 ROM / state / data 到 gym-retro
python -m nes_ai install-roms
```
### 查看训练结果

```bash
python -m nes_ai play super-mario-bros
```

### 训练模型

```bash
python -m nes_ai train super-mario-bros
```

### 查看曲线
```bash
tensorboard --logdir=artifacts/tensorboard/
```
在浏览器中打开 Tensorboard 服务默认地址 `http://localhost:6006/`，即可查看训练过程的交互式曲线图。

### 兼容旧命令

```bash
python set_up.py
python train.py 1
python run.py 1
```

这些脚本仍然可用，但现在只是转发到新的 `nes_ai` 包入口。

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

### 代码结构

当前版本已经重构为统一包结构，核心目录如下：

```text
nes_ai/
  games/        # 游戏注册信息、默认 state、训练配置
  envs/         # 通用 Retro wrapper 基类 + 各游戏奖励逻辑
  training/     # PPO 训练、模型加载、评估、checkpoint 管理
  retro/        # gym-retro 资源安装
  utils/        # 命名、校验等公共工具

assets/games/   # 各游戏的 rom/state/data 资源
artifacts/      # 模型、tensorboard、评估输出
```

现在新增一个游戏，主要只需要做三件事：

1. 把该游戏的 `rom.nes`、`rom.sha`、`data.json`、`metadata.json`、`scenario.json` 和 `.state` 文件放到 `assets/games/<Retro游戏名>/`
2. 在 `nes_ai/games/` 下新增一个游戏定义模块，注册 slug、默认 state、资源目录和训练参数
3. 在 `nes_ai/envs/` 下新增一个 wrapper，只实现该游戏自己的 reward 和 done 逻辑

这样就不需要再去同时修改 `common.py`、`train.py`、`run.py`、`set_up.py` 等多个入口。

### 训练参数

训练仍然使用 PPO，默认参数集中在 `nes_ai/games/*.py` 的 `TrainConfig` 中。典型参数如下：
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
训练总步数、并行环境数量、设备等参数也可以通过命令行覆盖，例如：

```bash
python -m nes_ai train super-mario-bros --timesteps 50000000 --num-envs 10 --device cuda
```

模型和日志现在统一存放到：

```text
artifacts/models/<game-slug>/
artifacts/tensorboard/<game-slug>/
artifacts/evaluations/<game-slug>/
```
## 致谢

本项目使用了 
- [OpenAI Gym Retro](https://retro.readthedocs.io/en/latest/getting_started.html)
- [Stable-Baselines3](https://stable-baselines3.readthedocs.io/en/master/) 
- [linyi street fight ai](https://github.com/linyiLYi/street-fighter-ai)
