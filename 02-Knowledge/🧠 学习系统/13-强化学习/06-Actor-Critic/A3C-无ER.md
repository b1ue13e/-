---
type: study
topic: "A3C-无ER"
course: "强化学习"
created: 2026-04-18
status: completed
stage_moc: "[[🧭 阶段6-Actor-Critic]]"
flow: knowledge
kind: concept
difficulty: intermediate
concept: ["A3C-无ER", "A3C 无需经验回放"]
upstream: ["[[A3C-异步]]", "[[DQN-经验回放]]"]
tags: [学习, 强化学习]
---

# A3C-无ER

> 所属模块：[[🗺️ 强化学习学习路径|强化学习学习路径]]
> 主教材：`《Reinforcement Learning》`
> 对应阶段：[[🧭 阶段6-Actor-Critic|返回阶段页]]

## 动机
正因为并行去相关，A3C 通常不使用经验回放缓冲。

## 正式定义 / 公式
A3C 直接在线用并行 worker 的最新样本更新，省去 DQN 的 replay buffer 与采样。
（对比「DQN-经验回放」：那是 off-policy 表格/NN Q-learning 的需求。）

## 最小手算例子
<!-- NUMEX2 -->A3C 并行多 worker（常 16 个）各自采样、梯度异步累加，无共享 replay buffer。例：16 worker 各跑 N=20 步 ⇒ 每轮约 320 步经验，省去回放内存与等待。

worker 边采边更新，无环形缓冲；样本寿命 = 当前一步。

## 对比与常见错误
- 与 DQN：DQN 需回放（off-policy、相关样本）；A3C 在线、并行已去相关。
- 常见错误：把"无 ER"当成缺陷——对 on-policy AC 是合理简化。

## 闭卷自测
1. A3C 为何不用经验回放？
2. 这相对 DQN 是简化还是缺陷？
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
