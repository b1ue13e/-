---
type: study
topic: "MDP-转移概率"
course: "强化学习"
created: 2026-04-18
status: completed
stage_moc: "[[🧭 阶段2-马尔可夫决策过程]]"
flow: knowledge
kind: concept
difficulty: beginner
concept: ["MDP", "转移概率"]
upstream: ["[[MDP-状态空间]]", "[[MDP-动作空间]]"]
tags: [学习, 强化学习]
---

# MDP-转移概率

> 所属模块：[[🧭 阶段2-马尔可夫决策过程]] · 主线：MDP 五元组
> 前置：[[MDP-状态空间]] · [[MDP-动作空间]]

## 动机

转移概率 $P$ 是 MDP 的"物理规律"：给定状态与动作，下一状态与奖励如何随机产生。它是动态规划与模型基 RL 的核心。

## 正式定义 / 公式

- 联合形式：$P(s',r\mid s,a)=\Pr\{S_{t+1}=s',R_{t+1}=r\mid S_t=s,A_t=a\}$。
- 常拆分为转移 $P(s'\mid s,a)=\sum_r P(s',r\mid s,a)$ 与期望奖励 $R(s,a)=\mathbb{E}[R_{t+1}\mid s,a]$。
- 归一化：$\sum_{s',r}P(s',r\mid s,a)=1$。

## 最小手算例子

网格世界中"向上"：以 0.8 移到上格、0.1 左、0.1 右（随机滑动），则对应 $P$ 三处非零且和为 1。

## 对比与常见错误

- **写成 $P(s'\mid s)$**：漏掉动作 $a$，它不是马尔可夫决策而是普通链。
- **忘记归一化**：每行（对 $s',r$）必须和为 1。

## 闭卷自测
- 写出 $P(s',r\mid s,a)$ 含义与归一化约束。
- 为什么转移必须依赖动作 $a$？

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
