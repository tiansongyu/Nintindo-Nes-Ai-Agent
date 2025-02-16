import os
import time 

import retro
from stable_baselines3.common.monitor import Monitor

from RushnAttackWrapper import RushnAttack  # 导入自定义的环境包装器

# 定义日志目录
LOG_DIR = 'logs/'
os.makedirs(LOG_DIR, exist_ok=True)  # 创建日志目录，如果不存在则创建

# 设置重置回合和渲染选项
RESET_ROUND = True  # 是否在战斗结束时重置回合
RENDERING = True    # 是否渲染游戏画面

# 创建环境的工厂函数
def make_env(game, state):
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
        return env
    return _init

# 定义游戏和状态
game = "RushnAttack-Nes"
state = "1Player.Level1"

# 创建环境
env = make_env(game, state)()
env = Monitor(env, LOG_DIR)  # 监控环境并记录日志

# 运行多个回合
num_episodes = 30
episode_reward_sum = 0  # 初始化总奖励
for _ in range(num_episodes):
    done = False
    obs = env.reset()  # 重置环境
    total_reward = 0  # 初始化每个回合的总奖励
    while not done:
        timestamp = time.time()  # 获取当前时间戳
        obs, reward, done, info = env.step(env.action_space.sample())  # 随机选择动作并执行
        if reward != 0:  # 如果奖励不为零
            total_reward += reward  # 累加奖励
            print("Total reward: {}".format(total_reward))  # 打印当前总奖励

    print("Total reward: {}".format(total_reward))  # 打印每个回合的总奖励
    episode_reward_sum += total_reward  # 累加回合奖励

env.close()  # 关闭环境
print("Average reward for random strategy: {}".format(episode_reward_sum / num_episodes))  # 打印平均奖励