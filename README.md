# Nintindo-Nes-Ai-Agent
Nintindo-Nes-Ai-Agent

## 环境配置

```bash
# 创建 conda 环境，将其命名为 StreetFighterAI，Python 版本 3.8.10
conda create -n Nintindo-Nes-Ai-Agent python=3.8.10
conda activate Nintindo-Nes-Ai-Agent

# 安装 Python 代码库
pip install setuptools==65.5.0 
pip install -r ./main/requirements.txt

# 运行程序脚本定位 gym-retro 游戏文件夹位置
python -m retro.import TeenageMutantNinjaTurtlesTournamentFighters-Nes .
```
### 训练模型

```bash
cd [game_dir]
python train.py
```

### 查看曲线
```bash
cd [项目上级文件夹]/street-fighter-ai/main
tensorboard --logdir=logs/
```
在浏览器中打开 Tensorboard 服务默认地址 `http://localhost:6006/`，即可查看训练过程的交互式曲线图。


## 致谢

本项目使用了 [OpenAI Gym Retro](https://retro.readthedocs.io/en/latest/getting_started.html)、[Stable-Baselines3](https://stable-baselines3.readthedocs.io/en/master/) 等开源代码库。感谢各位程序工作者对开源社区的贡献！
[linyi street fight ai](https://github.com/linyiLYi/street-fighter-ai)