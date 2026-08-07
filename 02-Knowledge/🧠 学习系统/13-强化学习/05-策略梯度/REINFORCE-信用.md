---
type: study
topic: "REINFORCE-信用"
course: "强化学习"
created: 2026-04-18
status: completed
stage_moc: "[[🧭 阶段5-策略梯度]]"
flow: knowledge
kind: concept
difficulty: intermediate
concept: ["REINFORCE-信用", "信用分配与 REINFORCE"]
upstream: ["[[REINFORCE-高方差]]", "[[优势-定义]]"]
tags: [学习, 强化学习]
---

# REINFORCE-信用

> 所属模块：[[🗺️ 强化学习学习路径|强化学习学习路径]]
> 主教材：`《Reinforcement Learning》`
> 对应阶段：[[🧭 阶段5-策略梯度|返回阶段页]]

## 动机
一条长轨迹里，最终奖励该"归功于"哪一步动作？这是信用分配（credit assignment）问题，也是 REINFORCE 方差的来源之一。

## 正式定义 / 公式
原始 REINFORCE 用 G_t（含之后所有步）给第 t 步加权——把后续步的运气也算到当前动作头上。
基线/优势把权重改成"相对该状态平均"的部分，只奖励"比平均更好"的动作，缓解错配。

## 最小手算例子
<!-- NUMEX2 -->信用分配：轨迹 τ=(s0,a0,r1,s1,a1,r2)，回报 G0=r1+γr2。baseline b 下优势 ĝ0=G0−b。若 r1=1,r2=0,γ=0.9 ⇒ G0=1；b=0.5 ⇒ ĝ0=0.5（归因到 a0）。

第 t 步走对但后续走错导致 G_t 低：原始版误罚第 t 步；用优势 A_t=G_t−V(s_t) 可部分抵消后续影响。

## 对比与常见错误
- 常见错误：认为"用 G_t 就公平"——G_t 混入了与当前动作无关的未来随机性。

## 闭卷自测
1. 什么是信用分配问题？
2. 优势如何缓解它？
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
