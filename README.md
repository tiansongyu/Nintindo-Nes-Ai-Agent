# Nintindo-Nes-Ai-Agent
本项目目的使用深度强化学习训练任天堂nes游戏，包括完整环境配置，训练过程，查看学习曲线，提供rom。

## List of Games

| 序号 | 游戏名称 |
| --- | --- |
| 1 | SuperMarioBros |
| 2 | TeenageMutantNinjaTurtlesTournamentFighters |
| 3 | FinalMission(SCATSpecialCyberneticAttackTeam) |
| 4 | RushnAttack |

## 环境配置(windows or linux)

```bash
# 创建 conda 环境，将其命名为 Nintindo-Nes-Ai-Agent，Python 版本 3.8.10
conda create -n Nintindo-Nes-Ai-Agent python=3.8.10
conda activate Nintindo-Nes-Ai-Agent

# 安装 Python 代码库
python -m pip install pip==24.0.0
pip install setuptools==65.5.0 wheel==0.38.4 -i https://pypi.tuna.tsinghua.edu.cn/simple
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

# 运行程序脚本定位 gym-retro 游戏文件夹位置
python set_up.py
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

### 查看训练结果

```bash
python run.py 1 
```

### 示例图片

![SuperMarioBros](img/supermaiobros_nes.gif)
![NinjaTurtles](img/nijia_turtles_nes.gif)
![FinalMission](img/final_mission_nes.gif)

## 致谢

本项目使用了 
- [OpenAI Gym Retro](https://retro.readthedocs.io/en/latest/getting_started.html)
- [Stable-Baselines3](https://stable-baselines3.readthedocs.io/en/master/) 
- [linyi street fight ai](https://github.com/linyiLYi/street-fighter-ai)
