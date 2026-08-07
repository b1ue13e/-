---
type: study
topic: "QL-收敛"
course: "强化学习"
created: 2026-04-18
status: completed
stage_moc: "[[🧭 阶段4-Q-Learning]]"
flow: knowledge
kind: concept
difficulty: intermediate
concept: ["QL-收敛", "Q-Learning 收敛性"]
upstream: ["[[QL-更新]]", "[[贝尔曼-收缩性]]"]
tags: [学习, 强化学习]
---

# QL-收敛

> 所属模块：[[🗺️ 强化学习学习路径|强化学习学习路径]]
> 主教材：`《Reinforcement Learning》`
> 对应阶段：[[🧭 阶段4-Q-Learning|返回阶段页]]

## 动机
Q-learning 为什么最终能学到 Q*？因为它本质上是在迭代应用最优贝尔曼算子 T*，而 T* 是 γ-收缩的。

## 正式定义 / 公式
Q ← T* Q，其中 (T* Q)(s,a) = E[ r + γ max_{a'} Q(s',a') ]。
由收缩映射定理（阶段3「贝尔曼-收缩性」），迭代收敛到唯一不动点 Q*。
（需满足：α 满足随机近似条件、所有 (s,a) 被无限次访问。）

## 最小手算例子
表格 Q 反复用上述更新扫描，Q(A,right) 在多次更新后趋近真实最优 1。

## 对比与常见错误
- 常见错误：认为"只要更新就能收敛"——还需步长与覆盖条件（GLIE 类），否则可能不收敛或到次优。

## 闭卷自测
1. Q-learning 收敛到什么？依据哪条定理？
2. 收敛需要哪些条件？
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
