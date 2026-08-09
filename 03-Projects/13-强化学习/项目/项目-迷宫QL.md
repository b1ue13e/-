---
type: project
project_type: capstone
assignment_id: "RL-PROJ-迷宫QL"
assignment_level: capstone
stage_id: "04"
source_type: local_integration_task
flow: project
course: "13-强化学习"
title: "项目-迷宫求解器 (Q-Learning)"
stage_moc: "[[02-Knowledge/🧠 学习系统/13-强化学习/04-Q-Learning/🧭 阶段4-Q-Learning]]"
assignment_format: capstone
status: planned
created: 2026-08-07
tags: [项目, Q-Learning, 表格方法]
requires:
  - "[[02-Knowledge/🧠 学习系统/13-强化学习/04-Q-Learning/Q-Learning算法]]"
  - "[[02-Knowledge/🧠 学习系统/13-强化学习/02-马尔可夫决策过程/轨迹定义]]"
---

# 项目：迷宫求解器（Q-Learning）

## 身份与目标
用表格 Q-Learning 在一个网格迷宫中学到从起点到终点的策略。验证 off-policy 表格控制在稀疏奖励下的收敛行为。

## 环境与建模
- 网格世界（如 10×10），状态 = 格子坐标，动作 = {上,下,左,右}。
- 奖励：到达终点 +10，撞墙 -1，每步 -0.01。
- 终止：到达终点或步数上限。

## 交付产物
1. Q 表训练代码（ε-greedy 探索）。
2. 学习曲线（回合回报 vs 训练回合）。
3. 收敛后策略可视化（箭头网格）。

## Rubric
| 维度 | 要求 |
|:---|:---|
| 正确性 | Q 更新与 Bellman 一致，能收敛 |
| 探索 | ε 衰减策略合理 |
| 评估 | 至少 3 个随机种子的平均曲线 + 方差带 |
| 报告 | 说明步数惩罚对路径长度的影响 |

## 引导与自检
- 先跑通 [[02-Knowledge/🧠 学习系统/13-强化学习/04-Q-Learning/课后作业/强化学习-课后作业-Q学习单步更新与最小实现|Q学习单步更新最小实现]]。
- 自检：固定随机种子结果可复现；增大惩罚后路径是否变短。

## 后续入口
- [[02-Knowledge/🧠 学习系统/13-强化学习/04-Q-Learning/SARSA-名称|SARSA 对比]] · [[03-Projects/13-强化学习/项目/项目-悬崖对比|悬崖对比实验]]
