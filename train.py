# Copyright 2023 invoker__qq. All Rights Reserved.
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#     http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================

import os
import sys
from common import get_game_info
import time

import retro
from stable_baselines3 import PPO
from stable_baselines3.common.monitor import Monitor
from stable_baselines3.common.callbacks import CheckpointCallback
from stable_baselines3.common.vec_env import SubprocVecEnv
import argparse

from RushnAttackWrapper import RushnAttack  # 导入自定义的环境包装器

NUM_ENV = 40  # 定义并行环境的数量

# 线性调度函数，用于动态调整学习率和剪切范围
def linear_schedule(initial_value, final_value=0.0):
    if isinstance(initial_value, str):
        initial_value = float(initial_value)
        final_value = float(final_value)
        assert (initial_value > 0.0)

    def scheduler(progress):
        return final_value + progress * (initial_value - final_value)

    return scheduler

# 解析命令行参数
parser = argparse.ArgumentParser(description='Training parameters')
parser.add_argument('game_number', help='The number of the game to train.')
parser.add_argument('--IsRender', type=bool, default=False, help='Whether to render the environment')

args = parser.parse_args()
IsRender = args.IsRender  # 获取渲染选项

# 获取游戏信息
game_info = get_game_info(args.game_number)

if game_info is None:
    print(f"Invalid game number. Please choose from {', '.join(game_mapping.keys())}.")
else:
    GameWrapper = game_info["wrapper"]  # 获取游戏包装器
    game = game_info["game"]  # 获取游戏名称
    state = game_info["state"]  # 获取游戏状态

LOG_DIR = 'logs'  # 定义日志目录
os.makedirs(LOG_DIR + "/" + game, exist_ok=True)  # 创建日志目录

# 设置重置回合和渲染选项
RESET_ROUND = True  # 是否在战斗结束时重置回合
RENDERING = True    # 是否渲染游戏画面

# 创建环境的工厂函数
def make_env(game, state, seed=0):
    def _init():
        # 创建 retro 环境
        env = retro.make(
            game=game, 
            state=state, 
            use_restricted_actions=retro.Actions.FILTERED, 
            obs_type=retro.Observations.IMAGE
        )
        # 使用 RushnAttack 包装环境
        env = RushnAttack(env, RESET_ROUND, RENDERING)
        env = Monitor(env)  # 监控环境
        env.seed(seed)  # 设置随机种子
        return env
    return _init

# 主训练函数
def main():
    # 创建多个并行环境
    env = SubprocVecEnv([make_env(game, state, seed=i) for i in range(NUM_ENV)])
    lr_schedule = linear_schedule(2.5e-4, 2.5e-6)  # 学习率调度

    clip_range_schedule = linear_schedule(0.15, 0.025)  # 剪切范围调度

    # 创建 PPO 模型
    model = PPO(
        "CnnPolicy", 
        env,
        device="cuda",  # 使用 GPU
        verbose=1,  # 输出详细信息
        n_steps=512,  # 每个更新的步数
        batch_size=512,  # 批量大小
        n_epochs=4,  # 训练的轮数
        gamma=0.94,  # 折扣因子
        learning_rate=lr_schedule,  # 学习率
        clip_range=clip_range_schedule,  # 剪切范围
        tensorboard_log=LOG_DIR + "/" + game  # TensorBoard 日志
    )
    save_dir = "trained_models"  # 定义模型保存目录
    os.makedirs(save_dir, exist_ok=True)  # 创建保存目录

    checkpoint_interval = 15000  # 检查点间隔
    checkpoint_callback = CheckpointCallback(save_freq=checkpoint_interval, save_path=save_dir, name_prefix="ppo_"+game)  # 创建检查点回调

    original_stdout = sys.stdout  # 保存原始标准输出
    log_file_path = os.path.join(save_dir, "training_log.txt")  # 定义日志文件路径
    with open(log_file_path, 'w') as log_file:
        sys.stdout = log_file  # 重定向标准输出到日志文件
        
        # 开始训练
        model.learn(
            total_timesteps=int(50000000),  # 总训练步数
            callback=[checkpoint_callback]  # 添加回调
        )
        env.close()  # 关闭环境

    sys.stdout = original_stdout  # 恢复标准输出
    model.save(os.path.join(save_dir, "ppo_" + game + ".zip"))  # 保存模型

if __name__ == "__main__":
    main()  # 运行主函数
