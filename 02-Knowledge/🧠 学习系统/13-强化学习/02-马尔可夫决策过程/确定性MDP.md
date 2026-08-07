---
type: study
topic: "确定性MDP"
course: "强化学习"
created: 2026-04-18
status: completed
stage_moc: "[[🧭 阶段2-马尔可夫决策过程]]"
flow: knowledge
kind: concept
difficulty: beginner
concept: ["确定性", "MDP"]
upstream: ["[[MDP-转移概率]]"]
tags: [学习, 强化学习]
---

# 确定性MDP

> 所属模块：[[🧭 阶段2-马尔可夫决策过程]] · 主线：转移概率
> 前置：[[MDP-转移概率]]

## 动机

确定性环境是最简单的一类 MDP；理解它，才能对比随机环境的额外挑战。

## 正式定义 / 公式

- **确定性 MDP**：对每个 $(s,a)$，存在唯一 $s'$ 使 $P(s'\mid s,a)=1$。
- 转移可写成函数 $s'=f(s,a)$；奖励 $r=R(s,a,s')$。
- 是随机 MDP 的特例（退化分布）。

## 最小手算例子

状态 s∈{1,2,3}，动作"右"：f(1,右)=2, f(2,右)=3, f(3,右)=3（撞墙不动），对应 P(s'|s,右)=1。
奖励 R(1,右,2)=+1, R(2,右,3)=+2，γ=0.9。自底向上：V(3)=0, V(2)=2+0.9·0=2, V(1)=1+0.9·2=2.8。
## 对比与常见错误

- **假设一切确定**：真实/仿真常含噪声，需随机建模。
- **把随机当确定**：忽略方差会导致规划过于乐观。

## 闭卷自测
- 确定性 MDP 的转移如何表示？
- 它与随机 MDP 的关系？

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
