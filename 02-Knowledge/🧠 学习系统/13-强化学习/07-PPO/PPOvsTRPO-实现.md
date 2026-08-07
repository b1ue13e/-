---
type: study
topic: "PPOvsTRPO-实现"
course: "强化学习"
created: 2026-04-18
status: completed
stage_moc: "[[🧭 阶段7-PPO]]"
flow: knowledge
kind: concept
difficulty: intermediate
concept: ["PPOvsTRPO-实现", "PPO 与 TRPO 实现复杂度"]
upstream: ["[[PPOvsTRPO-约束]]"]
tags: [学习, 强化学习]
---

# PPOvsTRPO-实现

> 所属模块：[[🗺️ 强化学习学习路径|强化学习学习路径]]
> 主教材：`《Reinforcement Learning》`
> 对应阶段：[[🧭 阶段7-PPO|返回阶段页]]

## 动机
工程上 PPO 之所以普及，关键在于它实现简单。

## 正式定义 / 公式
- TRPO：需计算 Fisher 信息矩阵、Hessian-vector 乘积、共轭梯度、线搜索；
- PPO：只需普通 SGD/Adam 优化裁剪目标，复用标准深度学习栈。
复杂度从二阶降到一阶。

## 最小手算例子
<!-- NUMEX2 -->实现差异：PPO-Clip 仅 ratio=π_new/π_old 裁剪一行，无需 CG/线搜；TRPO 需 Fisher-vector product + 共轭梯度 + KL 线搜，代码量约 1/3。

同样一张策略网络，TRPO 要多写约百行线性代数工具；PPO 仅一个 clip 损失。

## 对比与常见错误
- 与 PPOvsTRPO-效率：实现简单直接带来效率优势。
- 常见错误：以为 PPO 精度不如 TRPO——实践中二者常相当。

## 闭卷自测
1. 为何 PPO 实现比 TRPO 简单？
2. 复杂度差异来自哪里？
## 学完后可以完成

```dataview
TABLE assignment_level, source_type FROM "03-Projects"
WHERE contains(requires, this.file.link)
```

## 相关下游知识

```dataview
LIST FROM "02-Knowledge/🧠 学习系统"
WHERE contains(upstream, this.file.link)
```
