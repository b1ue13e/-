---
created: 2026-08-07
type: study
course: "强化学习"
title: "DAgger (Dataset Aggregation)"
topic: "DAgger (Dataset Aggregation)"
stage_moc: "[[🧭 阶段9-模仿学习与探索]]"
flow: knowledge
kind: concept
status: learning
importance: "B"
tags: [学习, 强化学习]
upstream: ["[[行为克隆BC]]"]
concept: ["DAgger", "分布偏移", "专家查询", "滚动聚合"]
sources:
  - "Ross et al., 2011, 'A Reduction of Imitation Learning'"
---
# DAgger (Dataset Aggregation)

> 所属模块：[[🗺️ 强化学习学习路径|强化学习学习路径]]
> 主教材：`Imitation Learning 教程`
> 对应阶段：[[🧭 阶段9-模仿学习与探索|返回阶段页]]

## 动机
BC 在训练分布外的状态会犯错并越陷越深。DAgger 让学习者边跑边请专家标注"当前状态"的正确动作，把新状态补进数据集，逐步纠正偏移。

## 正式定义 / 公式
循环：用 π_i 采轨迹；对每个访问状态 s 查询专家得 a*；把 (s,a*) 加入 D；用增大后的 D 重新训练 π_{i+1}。

## 最小手算例子
第 1 轮 BC 在 100 状态上训；第 2 轮 π_1 跑出 100 新状态（含 40 个 BC 会错的状态），专家标注后 D 变 200；
第 3 轮错误状态占比从 40% 降到 10%，随轮次收敛。

## 对比与常见错误
- 与 BC：DAgger 主动补新状态标签，打破错误累积；代价是需专家在线。
- 常见错误：只在初始分布采数据（退化为 BC）；专家不可在线时无法用。

## 闭卷自测
1. DAgger 如何缓解 BC 的分布偏移？
2. DAgger 的主要代价/限制？

## 直觉：边跑边让专家补标签
BC 只在专家演示分布上训，一旦策略跑到训练外状态就错、且错误累积越陷越深（distribution shift）。DAgger 让学习者自己跑、对每个访问到的状态再请专家标正确动作、补进数据集重训，逐步把策略“拉回”专家分布。代价：需要专家在线可用；若只能离线拿一批演示则退化为 BC，无法纠正分布偏移。

## 学完后可以完成

```dataview
LIST
FROM "03-Projects"
WHERE contains(requires, this.file.link)
SORT assignment_level ASC, file.name ASC
```

## 相关下游知识

```dataview
LIST FROM "02-Knowledge/🧠 学习系统"
WHERE contains(upstream, this.file.link)
```
