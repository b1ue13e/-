---
created: 2026-08-07
type: study
course: "强化学习"
title: "内在好奇心模块 ICM (Intrinsic Curiosity Module)"
topic: "内在好奇心模块 ICM (Intrinsic Curiosity Module)"
stage_moc: "[[🧭 阶段9-模仿学习与探索]]"
flow: knowledge
kind: algorithm
status: learning
importance: "A"
tags: [学习, 强化学习, 探索, 好奇心]
upstream: ["[[内在奖励与好奇心]]", "[[探索与利用基础]]"]
concept: ["ICM", "前向动态", "逆动态", "特征空间"]
sources:
  - "Pathak et al. 2017 (ICM)"
---
# 内在好奇心模块 ICM (Intrinsic Curiosity Module)

> 所属模块：[[🗺️ 强化学习学习路径|强化学习学习路径]]
> 对应阶段：[[🧭 阶段9-模仿学习与探索|返回阶段页]]

## 动机
RND 用随机网络蒸馏测新奇。ICM 用**可学习的逆/前向动态**来定义"有趣"：如果某个状态转移你能预测（无聊）就无奖励，预测不了（新奇且可控）就给内在奖励。关键技巧：先学一个**特征编码器**，滤掉与动作无关、不可控的干扰（如飘动的树叶），只在"可控动态"上算好奇心。

## 正式定义 / 公式
ICM 三网络：
- **逆动态网络**：φ(s_t,a_t)→ŝ_{t+1}，用于学好的特征 φ（能由 (s,a) 推出 s' 的特征才是信息量大的）。
- **前向动态网络**：在 φ 空间预测 φ(s_{t+1}) 从 (φ(s_t), a_t)；内在奖励 = ‖φ̂(s_{t+1}) − φ(s_{t+1})‖²。
总奖励 r = r_ext + λ·r_int。

## 最小手算例子
智能体在风里走路。树叶乱飞（不可控、与动作无关）→ 逆动态网络学会把树叶信息压缩掉（φ 不含它）；只有"脚下地形变化"（可控）才会让前向预测出错→产生好奇心奖励，驱动智能体去探索可影响的地形，而非对着树叶发呆。

## 对比与常见错误
- 与 RND：ICM 用可控性筛选特征，减少"无效新奇"；RND 更简单、无需逆网络。
- 与计数法：ICM 是预测误差型，计数法是密度型。
- **常见错误**：λ 过大→智能体沉迷"制造预测误差"（如原地抖动让模型跟不上）；特征 φ 没过滤干扰→好奇心被无关噪声耗尽。

## 闭卷自测
1. ICM 的逆动态网络起到什么作用（为何要学它）？
2. 为什么"可控性筛选"能避免好奇心被无关噪声耗尽？

## 学完后可以完成

```dataview
LIST FROM "03-Projects" WHERE contains(requires, this.file.link)
```

## 相关下游知识

```dataview
LIST FROM "02-Knowledge/🧠 学习系统" WHERE contains(upstream, this.file.link)
```
