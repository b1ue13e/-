---
type: study
topic: "PER"
course: "强化学习"
created: 2026-04-18
status: completed
stage_moc: "[[🧭 阶段4-Q-Learning]]"
flow: knowledge
kind: concept
difficulty: intermediate
concept: ["PER", "Prioritized Experience Replay"]
upstream: ["[[DQN-经验回放]]"]
tags: [学习, 强化学习]
---

# PER

> 所属模块：[[🗺️ 强化学习学习路径|强化学习学习路径]]
> 主教材：`《Reinforcement Learning》`
> 对应阶段：[[🧭 阶段4-Q-Learning|返回阶段页]]

## 动机
均匀回放对所有经验一视同仁，但"TD 误差大"的经验通常更值得学。优先经验回放（PER）按 TD 误差大小加权采样。

## 正式定义 / 公式
样本 i 优先级 p_i = |δ_i| + ε；采样概率 P(i) ∝ p_i^α。
为纠正"偏向高误差样本"带来的偏差，用重要性采样权重 w_i = (N·P(i))^{-β} 乘到梯度上，β 训练末趋 1。

## 最小手算例子
<!-- NUMEX -->优先级 p_i=|δ_i|^α，α=0.6。两轮 TD 误差 δ=[0.1,0.9] ⇒ p=[0.1^0.6,0.9^0.6]≈[0.25,0.94] ⇒ 归一后采样概率 P≈[0.21,0.79]（大误差样本被更频繁重放）。

某转移 TD 误差很大（学错了）→ 高优先级，被多次重放直至误差变小；已学会的环境样本渐少被抽。

## 对比与常见错误
- 与均匀回放：PER 收敛更快、数据效率更高，但实现更复杂（常配合 sum-tree 高效采样）。
- 常见错误：不做重要性采样校正——会导致梯度被高优先级样本带偏、训练不稳。

## 闭卷自测
1. PER 按什么优先级采样？
2. 为什么需要重要性采样权重？
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
