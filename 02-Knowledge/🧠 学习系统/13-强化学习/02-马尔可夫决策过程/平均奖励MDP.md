---
type: study
topic: "平均奖励MDP"
course: "强化学习"
created: 2026-04-18
status: completed
stage_moc: "[[🧭 阶段2-马尔可夫决策过程]]"
flow: knowledge
kind: concept
difficulty: advanced
concept: ["平均奖励", " continuing"]
upstream: ["[[回报定义]]"]
tags: [学习, 强化学习]
---

# 平均奖励MDP

> 所属模块：[[🧭 阶段2-马尔可夫决策过程]] · 主线：MDP 扩展
> 前置：[[回报定义]]

## 动机

持续任务（无终止）除了折扣回报，还可优化**平均奖励**；这是另一种目标范式，理解它才能正确建模"永不结束"的任务。

## 正式定义 / 公式

- **平均奖励** $J(\pi)=\lim_{T\to\infty}\frac{1}{T}\mathbb{E}[\sum_{t=0}^{T-1}r_t]$。
- 适用于持续（continuing）任务，避免无限折扣的偏差。
- 折扣回报与平均奖励在 $\gamma\to1$ 时相关联（差一个常数偏移）。

## 最小手算例子

一条轨迹奖励 [1,3,2,4]，T=4：平均奖励 J=(1+3+2+4)/4=2.5。
同样奖励若按折扣 γ=0.9 求和：G=1+0.9·3+0.81·2+0.729·4=8.236（随 T 增大被早期项主导）。
持续任务里平均奖励更稳定，不受"越早越好"的折扣偏好影响。

## 对比与常见错误

- **与折扣回报混用**：目标不同，最优策略可能不同。
- **忽视偏差项**：二者最优值差常数，比较策略时需注意。

## 闭卷自测
- 平均奖励目标如何定义？
- 它与折扣回报的关系与区别？

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
