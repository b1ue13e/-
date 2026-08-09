---
created: 2026-08-07
type: study
course: "强化学习"
title: "基于信息的探索 VIME (Information-theoretic Exploration)"
topic: "基于信息的探索 VIME (Information-theoretic Exploration)"
stage_moc: "[[🧭 阶段9-模仿学习与探索]]"
flow: knowledge
kind: algorithm
status: learning
importance: "C"
tags: [学习, 强化学习, 探索, 信息论]
upstream: ["[[探索与利用基础]]", "[[模型不确定性与贝叶斯模型]]"]
concept: ["VIME", "信息增益", "贝叶斯", "熵减"]
sources:
  - "Houthooft et al. 2016 (VIME)"
---
# 基于信息的探索 VIME (Information-theoretic Exploration)

> 所属模块：[[🗺️ 强化学习学习路径|强化学习学习路径]]
> 对应阶段：[[🧭 阶段9-模仿学习与探索|返回阶段页]]

## 动机
从信息论角度，好的探索应当**最大化"关于环境动力学后验"的信息增益**。每走一步，如果这次经验能大幅更新我们对世界模型的信念，就值得去——这正是 VIME 的思想。它把好奇心写成"后验熵的减少量"，是模型基探索与信息论的美妙结合。

## 正式定义 / 公式
智能体维护一个动力学模型的贝叶斯后验 p(θ|D)。VIME 的内在奖励 = 执行 a_t 后后验熵的减少：

  r_int(s_t,a_t) = D_KL[ p(θ | D ∪ {(s_t,a_t)}) ‖ p(θ | D) ]

即"这一步让模型信念变了多少"。同时，外部策略优化的目标被加一个熵项以鼓励信息增益。实践中用变分近似（网络输出分布参数），把 KL 当奖励。

## 最小手算例子
机械臂不知道某关节阻尼多大。试一个动作后，后验从"阻尼∈[0,1]"收窄到"[0.2,0.3]"→信息增益大→VIME 奖励高，继续探；等阻尼已估准，再试同类动作后验几乎不变→奖励趋零，转向未知维度。类似主动学习（active learning）的"该问哪个问题"。

## 对比与常见错误
- 与 RND/ICM：VIME 显式基于**模型后验的信息增益**，理论更优雅；RND/ICM 是近似的误差信号。
- 与计数法：VIME 是连续、贝叶斯化的"访问价值"，不依赖离散计数。
- **常见错误**：变分近似太差→信息增益估计偏；奖励尺度未归一→压过外部奖励。

## 闭卷自测
1. VIME 的内在奖励等于什么量？它衡量"探索"的什么性质？
2. 它与主动学习（active learning）有何相似之处？

## 学完后可以完成

```dataview
LIST FROM "03-Projects" WHERE contains(requires, this.file.link)
```

## 相关下游知识

```dataview
LIST FROM "02-Knowledge/🧠 学习系统" WHERE contains(upstream, this.file.link)
```
