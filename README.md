# Nintindo-Nes-Ai-Agent
本项目目的使用深度强化学习训练任天堂nes游戏，包括完整环境配置，训练过程，查看学习曲线，提供rom。

## list 
- SuperMarioBros
- TeenageMutantNinjaTurtlesTournamentFighters
- FinalMission(SCATSpecialCyberneticAttackTeam)
- RushnAttack

## 环境配置

```bash
# 创建 conda 环境，将其命名为 Nintindo-Nes-Ai-Agent，Python 版本 3.8.10
conda create -n Nintindo-Nes-Ai-Agent python=3.8.10
conda activate Nintindo-Nes-Ai-Agent

# 安装 Python 代码库
pip install setuptools==65.5.0 wheel==0.38.4
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

# 运行程序脚本定位 gym-retro 游戏文件夹位置
python set_up.py
```
### 训练模型

```bash
cd [game_dir]
python train.py
```

### 查看曲线
```bash
cd [game_dir]/main
tensorboard --logdir=logs/
```
在浏览器中打开 Tensorboard 服务默认地址 `http://localhost:6006/`，即可查看训练过程的交互式曲线图。


## 致谢

本项目使用了 
- [OpenAI Gym Retro](https://retro.readthedocs.io/en/latest/getting_started.html)
- [Stable-Baselines3](https://stable-baselines3.readthedocs.io/en/master/) 
- [linyi street fight ai](https://github.com/linyiLYi/street-fighter-ai)
