---
type: study
topic: "MAB-问题定义"
course: "强化学习"
created: 2026-04-18
status: completed
stage_moc: "[[🧭 阶段1-基础与本质]]"
flow: knowledge
kind: concept
difficulty: beginner
concept: ["多臂老虎机", "问题定义"]
upstream: ["[[探索与利用]]"]
tags: [学习, 强化学习]
---

# MAB-问题定义

> 所属模块：[[🧭 阶段1-基础与本质]] · 主线：多臂老虎机
> 前置：[[探索与利用]]

## 动机

多臂老虎机（Multi-Armed Bandit, MAB）是 RL 的"最小模型"：去掉状态转移，只剩"探索-利用"。吃透它，后面所有带探索的 RL 算法都更好懂。

## 正式定义 / 公式

- 有 $k$ 个臂（动作）$a\in\{1,\dots,k\}$，臂 $a$ 的真实价值 $q_*(a)=\mathbb{E}[R_t\mid A_t=a]$。
- 每步选臂 $A_t$，观测奖励 $R_t\sim\mathbb{P}(\cdot\mid a)$，目标最大化累计奖励 $\sum_t R_t$。
- **估值** $\hat Q_t(a)$ 逐步逼近 $q_*(a)$；**遗憾** $L_T=\sum_t(q_*(a^*)-q_*(A_t))$。

## 最小手算例子

3 台机器，真实均值 $[0.3,0.6,0.2]$。最优是臂 2。算法要在"多拉臂 2（利用）"与"试探臂 1/3（探索）"间权衡。

## 对比与常见错误

- **与完整 RL 混淆**：MAB 无状态、无转移；带状态后才是 MDP。
- **用均值硬判**：样本少时均值不可靠，必须考虑不确定性。

## 闭卷自测
- 写出 MAB 的目标与 regret 定义。
- MAB 相比完整 RL 少了什么？

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
