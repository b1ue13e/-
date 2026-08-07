---
type: study
topic: "优势-n步"
course: "强化学习"
created: 2026-04-18
status: completed
stage_moc: "[[🧭 阶段6-Actor-Critic]]"
flow: knowledge
kind: concept
difficulty: intermediate
concept: ["优势-n步", "n 步优势"]
upstream: ["[[优势-TD]]", "[[折扣-回报]]"]
tags: [学习, 强化学习]
---

# 优势-n步

> 所属模块：[[🗺️ 强化学习学习路径|强化学习学习路径]]
> 主教材：`《Reinforcement Learning》`
> 对应阶段：[[🧭 阶段6-Actor-Critic|返回阶段页]]

## 动机
单步优势偏估计、信息少；多步（n-step）优势在偏差与方差间折中。

## 正式定义 / 公式
n 步优势：
A_t^{(n)} = Σ_{k=0}^{n-1} γ^k r_{t+k+1} + γ^n V(s_{t+n}) − V(s_t)
n=1 退化为 TD 优势；n→∞ 退化为 MC 优势（G_t−V）。

## 最小手算例子
n=3：(r_t+γr_{t+1}+γ²r_{t+2}) + γ³V(s_{t+3}) − V(s_t)。比单步多看两步真实奖励。

## 对比与常见错误
- 与 GAE：n-step 是固定窗；GAE 是其指数加权组合（见「优势-GAE」）。
- 常见错误：n 取太大又回到高方差——需按任务调。

## 闭卷自测
1. 写出 n 步优势公式。
2. n=1 与 n→∞ 分别退化成什么？
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
