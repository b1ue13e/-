---
type: study
topic: "RLHF-RM"
course: "强化学习"
created: 2026-04-18
status: completed
stage_moc: "[[🧭 阶段7-PPO]]"
flow: knowledge
kind: concept
difficulty: intermediate
concept: ["RLHF-RM", "奖励模型训练"]
upstream: ["[[RLHF-背景]]", "[[RLHF-SFT]]"]
tags: [学习, 强化学习]
---

# RLHF-RM

> 所属模块：[[🗺️ 强化学习学习路径|强化学习学习路径]]
> 主教材：`《Reinforcement Learning》`
> 对应阶段：[[🧭 阶段7-PPO|返回阶段页]]

## 动机
人类不能实时给每条回答打分，需要训练一个能代替人类打分的模型。

## 正式定义 / 公式
用成对偏好数据 (x, y_w, y_l)（人类对同一 prompt x 的两个回答 y_w≻y_l）训练 RM，采用 Bradley-Terry 模型：
P(y_w≻y_l) = σ(r_φ(x,y_w) − r_φ(x,y_l))
最大化该似然即训练 RM 输出标量奖励 r_φ。

## 最小手算例子
<!-- NUMEX2 -->奖励模型 RM：用偏好对 (x,y_w,y_l) 训练，损失 −log σ(RM(y_w)−RM(y_l))。例收集数万偏好对，RM 在 7B 策略上打分层奖励。

prompt=“解释黑洞”，y_w 准确、y_l 错误 → RM 学到给 y_w 更高 r。

## 对比与常见错误
- 与 RLHF-奖励模型：本卡偏训练过程，后者偏 RM 的用途。
- 常见错误：把 RM 当绝对真值——它只是人类偏好的有噪代理。

## 闭卷自测
1. 奖励模型用什么数据训练？
2. Bradley-Terry 模型起什么作用？
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
