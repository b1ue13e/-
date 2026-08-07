---
type: study
topic: "RL基础-延迟奖励"
course: "强化学习"
created: 2026-04-18
status: completed
stage_moc: "[[🧭 阶段1-基础与本质]]"
flow: knowledge
kind: concept
difficulty: beginner
concept: ["RL基础", "延迟奖励", "折扣因子"]
upstream: ["[[奖励函数]]"]
tags: [学习, 强化学习]
---

# RL基础-延迟奖励

> 所属模块：[[🧭 阶段1-基础与本质]] · 主线：RL概览
> 前置：[[奖励函数]]

## 动机

RL 的奖励常是延迟的（下棋终局才评分），"现在动作"与"未来奖励"的因果需要折扣与信用分配来连接。

## 正式定义 / 公式

- **延迟奖励**：即时奖励 $r_t$ 往往不能反映长期好坏，真正目标是回报 $G_t=\sum_{k=0}^{\infty}\gamma^k r_{t+k+1}$。
- **折扣因子** $\gamma$ 让远期奖励贬值，稳定学习与权衡长短。
- **信用分配**：把最终成败分摊到导致它的各步动作。

## 最小手算例子

走迷宫：每步 −1（怕拖沓），到终点 +10。靠近出口的路因折扣后仍获高 $G_t$，被优先学。

## 对比与常见错误

- **$\gamma$ 太接近 1**：回报方差大、学习慢、易发散。
- **忽视信用分配**：把失败全归咎最后一步，策略学偏。

## 闭卷自测
- 为何延迟奖励必须引入折扣 $\gamma$？
- 信用分配问题指什么？

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
