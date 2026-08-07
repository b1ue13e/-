---
type: study
topic: "连续MDP"
course: "强化学习"
created: 2026-04-18
status: completed
stage_moc: "[[🧭 阶段2-马尔可夫决策过程]]"
flow: knowledge
kind: concept
difficulty: advanced
concept: ["连续MDP", "函数近似"]
upstream: ["[[MDP-状态空间]]", "[[MDP-动作空间]]"]
tags: [学习, 强化学习]
---

# 连续MDP

> 所属模块：[[🧭 阶段2-马尔可夫决策过程]] · 主线：MDP 扩展
> 前置：[[MDP-状态空间]] · [[MDP-动作空间]]

## 动机

机器人、自动驾驶的状态与动作是连续的；离散表格法失效，必须函数近似。这是 DQN/PPO/SAC 的现实舞台。

## 正式定义 / 公式

- **连续 MDP**：$\mathcal{S}\subset\mathbb{R}^n$、$\mathcal{A}\subset\mathbb{R}^m$ 连续。
- 价值/策略用神经网络等参数化：$v_\theta(s)$、$a_\mu(s)$；梯度类算法主导。

## 最小手算例子

倒立摆：$\mathcal{S}=(角度,角速度)\in\mathbb{R}^2$，$\mathcal{A}=力矩\in\mathbb{R}$；PPO/SAC 直接输出连续动作。

## 对比与常见错误

- **直接套表格法**：连续空间无法枚举状态。
- **忽略采样/归一化**：连续动作需合适探索（高斯噪声）与尺度归一。

## 闭卷自测
- 连续 MDP 为何不能用 Q 表？
- 常见处理函数近似方法？

## 学完后可以完成

```dataview
LIST
FROM "03-Projects"
WHERE contains(requires, this.file.link)
SORT assignment_level ASC, file.name ASC
```

## 相关下游知识

```dataview
LIST
FROM "02-Knowledge/🧠 学习系统"
WHERE contains(upstream, this.file.link)
SORT file.name ASC
```
