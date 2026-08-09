---
created: 2026-08-07
type: study
course: "强化学习"
title: "Dyna算法 (Dyna)"
topic: "Dyna算法 (Dyna)"
stage_moc: "[[🧭 阶段8-模型基与规划]]"
flow: knowledge
kind: concept
status: learning
importance: "A"
tags: [学习, 强化学习]
upstream: ["[[模型基RL概述]]", "[[Q-Learning算法]]"]
concept: ["Dyna", "想象", "模型训练", "Q学习"]
sources:
  - "Sutton & Barto Ch.8.2"
---
# Dyna算法 (Dyna)

> 所属模块：[[🗺️ 强化学习学习路径|强化学习学习路径]]
> 主教材：`Sutton & Barto Ch.8.2`
> 对应阶段：[[🧭 阶段8-模型基与规划|返回阶段页]]

## 动机
真实交互昂贵，能否"每走一步真实环境，就在脑子里用模型多走几步"？Dyna 把真实经验既用于更新 Q、又用于训练模型，再用模型生成仿真经验更新 Q。

## 正式定义 / 公式
每次真实转移 (s,a,r,s')：① Q 学习更新 Q；② 用 (s,a,r,s') 更新模型 f；③ 重复 k 次：从 replay 取样 s,a，用 f 生成 (r',s'')，再做 Q 学习更新。

## 最小手算例子
真实每步后 k=10 次仿真。若真实一步得 1 个 (s,a,r,s')，则本轮共 11 次 Q 更新（1 真实 + 10 仿真）。
k 越大模型利用越充分，但 k 过大模型误差累积、Q 被污染。

## 对比与常见错误
- 与纯 Q-Learning：多了对模型的训练与仿真更新，加速。
- 常见错误：k 太大引入模型误差；模型未先 warmed up 就用。

## 闭卷自测
1. Dyna 中真实经验有哪两个用途？
2. k 过大为何可能有害？

## 直觉：每走一步真实环境，就在脑子里走 k 步
真实交互贵。Dyna 的核心循环：用一步真实 (s,a,r,s') 既更新 Q、又训练模型 f；再用 f 在 replay 上“想象”出 k 步仿真继续更新 Q。所以真实一步 → (1+k) 次 Q 更新，样本效率随 k 提升。但 k 太大模型误差累积、污染 Q——k 与模型精度要匹配，且模型需先 warm-up 再用。

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
