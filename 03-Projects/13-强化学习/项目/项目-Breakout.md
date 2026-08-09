---
type: project
project_type: capstone
assignment_id: "RL-PROJ-Breakout"
assignment_level: capstone
stage_id: "04"
source_type: local_integration_task
flow: project
course: "13-强化学习"
title: "项目-Atari Breakout (DQN)"
stage_moc: "[[02-Knowledge/🧠 学习系统/13-强化学习/04-Q-Learning/🧭 阶段4-Q-Learning]]"
assignment_format: capstone
status: planned
created: 2026-08-07
tags: [项目, Atari, 图像输入, DQN]
requires:
  - "[[02-Knowledge/🧠 学习系统/13-强化学习/04-Q-Learning/DQN深度Q网络]]"
  - "[[02-Knowledge/🧠 学习系统/13-强化学习/04-Q-Learning/Double-DQN]]"
---

# 项目：Atari Breakout（DQN）

## 身份与目标
用 DQN 处理原始像素输入玩 Atari `Breakout`，掌握帧堆叠、图像预处理与从像素到价值的端到端训练。

## 环境与建模
- 输入：连续 4 帧灰度图（84×84）。
- 动作：离散（不动作/左/右/发射）。
- 奖励：消除砖块得分。

## 交付产物
1. 预处理 + 卷积 Q 网络实现。
2. 训练曲线（得分 vs 帧数）与若干对局录屏/帧采样。
3. 与 [[03-Projects/13-强化学习/项目/项目-CartPoleDQN|CartPole DQN]] 的对比说明（状态维度、样本效率差异）。

## Rubric
| 维度 | 要求 |
|:---|:---|
| 正确性 | 帧堆叠、经验回放、目标网络正确 |
| 工程 | 预处理管线可复现 |
| 评估 | 多种子 + 与基线对比 |
| 报告 | 解释像素输入下的探索与训练稳定性 |

## 后续入口
- [[02-Knowledge/🧠 学习系统/13-强化学习/07-PPO/PPO近端策略优化|PPO]]（可换成策略梯度方法重做）
