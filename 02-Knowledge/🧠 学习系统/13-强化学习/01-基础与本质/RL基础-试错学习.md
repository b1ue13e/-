---
type: study
topic: "RL基础-试错学习"
course: "强化学习"
created: 2026-04-18
status: completed
stage_moc: "[[🧭 阶段1-基础与本质]]"
flow: knowledge
kind: concept
difficulty: beginner
concept: ["RL基础", "试错学习"]
upstream: ["[[Agent定义]]"]
tags: [学习, 强化学习]
---

# RL基础-试错学习

> 所属模块：[[🧭 阶段1-基础与本质]] · 主线：RL概览
> 前置：[[Agent定义]]

## 动机

"试错（Trial-and-Error）"是 RL 获取知识的唯一途径；理解它才能理解探索的必要性与反馈闭环。

## 正式定义 / 公式

- **试错学习**：Agent 通过尝试动作、观察结果（奖励/状态）来逐步改进策略，无需显式示范。
- 与**监督**区别：没有"标准答案"可直接比对，只有环境反馈。
- 与**规划**区别：试错在真实/仿真环境中交互，规划在模型内推演。

## 最小手算例子

学骑自行车：摔几次（负奖励）后调整平衡（动作），最终学会（策略改进）。没人逐帧告诉你"此时该用多大力"。

## 对比与常见错误

- **试错 $\neq$ 随机乱撞**：有效试错由策略与探索机制引导，并会利用已学知识。
- **忽略样本效率**：纯试错样本效率低，后期用经验回放、世界模型等提升。

## 闭卷自测
- 试错学习与监督学习在"知识来源"上有何不同？
- 为什么"有效试错"仍需探索机制？

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
