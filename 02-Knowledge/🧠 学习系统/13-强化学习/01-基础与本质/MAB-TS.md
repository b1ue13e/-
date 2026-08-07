---
type: study
topic: "MAB-TS"
course: "强化学习"
created: 2026-04-18
status: completed
stage_moc: "[[🧭 阶段1-基础与本质]]"
flow: knowledge
kind: concept
difficulty: intermediate
concept: ["MAB", "汤普森采样"]
upstream: ["[[MAB-问题定义]]", "[[汤普森采样]]"]
tags: [学习, 强化学习]
---

# MAB-TS

> 所属模块：[[🧭 阶段1-基础与本质]] · 主线：多臂老虎机
> 前置：[[MAB-问题定义]] · [[汤普森采样]]

## 动机

把汤普森采样落到老虎机：在 MAB 框架下用贝叶斯后验做动作选择。

## 正式定义 / 公式

1. 初始化每臂后验（如 Beta(1,1)）。
2. 每步从各臂后验抽样，选最大者拉取。
3. 用观测奖励更新对应臂后验。

## 最小手算例子

两臂后验：臂1 α=2,β=3；臂2 α=5,β=4。一步抽样 θ1~Beta(2,3) 抽到 0.31，θ2~Beta(5,4) 抽到 0.61 → 拉臂2。
观测 R=0 → 更新臂2：β 由 4 变 5，后验成 (5,5)，均值由 5/9≈0.556 降到 5/10=0.5。

- UCB 是频率派、确定性、靠置信半径。
- TS 是贝叶斯派、随机性、靠后验抽样；通常样本效率更高、实现更简单。

## 对比与常见错误

- **把 TS 当确定性策略**：它本身是随机的（抽样）。
- **后验不更新**：漏掉一步更新会让探索停滞。

## 闭卷自测
- 简述 MAB-TS 与 MAB-UCB1 的两点区别。
- 为何 TS 实践中常优于 UCB？

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
