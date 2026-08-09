---
type: project
project_type: capstone
assignment_id: "RL-PROJ-CartPoleDQN"
assignment_level: capstone
stage_id: "04"
source_type: local_integration_task
flow: project
course: "13-强化学习"
title: "项目-CartPole DQN"
stage_moc: "[[02-Knowledge/🧠 学习系统/13-强化学习/04-Q-Learning/🧭 阶段4-Q-Learning]]"
assignment_format: capstone
status: planned
created: 2026-08-07
tags: [项目, DQN, 深度RL]
requires:
  - "[[02-Knowledge/🧠 学习系统/13-强化学习/04-Q-Learning/DQN深度Q网络]]"
  - "[[02-Knowledge/🧠 学习系统/13-强化学习/04-Q-Learning/Double-DQN]]"
---

# 项目：CartPole DQN

## 身份与目标
用 Deep Q-Network 在 Gymnasium `CartPole-v1` 上学到平衡策略，掌握经验回放、目标网络与卷积/MLP 编码器的工程要点。

## 环境与建模
- 状态：4 维连续观测；动作：离散 2 维（左/右推）。
- 奖励：每步 +1，倒下或越界终止。

## 交付产物
1. DQN 实现（Q 网络 + 目标网络 + 经验回放）。
2. 训练曲线（滑动平均回报）。
3. 至少 5 个种子的方差带与超参说明。

## Rubric
| 维度 | 要求 |
|:---|:---|
| 正确性 | 损失、目标计算无误，能稳定收敛 |
| 工程 | 回放缓冲、目标网络软/硬更新 |
| 评估 | 多种子 + 消融（去掉回放/目标网络各跑一次） |
| 报告 | 说明奖励塑形与终止条件 |

## 引导与自检
- 先完成 [[02-Knowledge/🧠 学习系统/13-强化学习/04-Q-Learning/DQN深度Q网络|DQN 最小实现]]。
- 自检：去掉经验回放后方差是否显著上升。

## 后续入口
- [[03-Projects/13-强化学习/项目/项目-Breakout|Atari Breakout]] · [[03-Projects/13-强化学习/阶段作业/强化学习-阶段作业-HW02-DQN与PPO连续动作控制|连续控制阶段作业]]
