---
created: 2026-08-07
type: study
course: "强化学习"
title: "QMIX (QMIX Value Factorization)"
topic: "QMIX (QMIX Value Factorization)"
stage_moc: "[[🧭 阶段10-多智能体与分层RL]]"
flow: knowledge
kind: algorithm
status: learning
importance: "A"
tags: [学习, 强化学习, 多智能体, 值分解]
upstream: ["[[值分解VDN]]", "[[CTDE范式]]"]
concept: ["QMIX", "单调混合", "超网络", "信用分配"]
sources:
  - "Rashid et al. 2018 (QMIX)"
---
# QMIX (QMIX Value Factorization)

> 所属模块：[[🗺️ 强化学习学习路径|强化学习学习路径]]
> 对应阶段：[[🧭 阶段10-多智能体与分层RL|返回阶段页]]

## 动机
VDN 的纯加性分解表达力太弱，很多合作任务需要**非线性**但又要保持"局部贪婪=全局最优"的性质。QMIX 用一个小技巧做到：通过一个**单调混合网络**把各 Agent 的 Q_i 非线性地组合成 Q_tot，同时用超网络（hypernetwork）让混合权重依赖全局状态——既比 VDN 强，又保证执行时各 Agent 可独立贪婪。

## 正式定义 / 公式
约束（单调性）：

  ∂Q_tot / ∂Q_i ≥ 0,  ∀i

混合网络：Q_tot = f_ψ(s)(Q₁..Qₙ)，其中 f 是单调的（权重非负），权重 ψ 由超网络从全局状态 s 生成。训练用 TD 误差更新 Q_i 与混合网络；因单调性，argmax_{a} Q_tot = (argmax_{a_i} Q_i) 逐 Agent 分解，故执行去中心。

## 最小手算例子
矩阵博弈/交通协同：某些合作需要"一个 Agent 牺牲自己让全局更优"的**非线性**信用分配（非纯加性）。VDN 学不好，QMIX 因单调非线性混合能捕捉这种依赖，性能显著更好；同时执行时每个车只看自己 Q_i 贪婪变道，无需全图通信。

## 对比与常见错误
- 与 VDN：QMIX 表达力更强（单调非线性 vs 纯加），训练也更稳。
- 与 MADDPG：QMIX 是**值分解/Q-learning 系**，执行完全去中心；MADDPG 是 actor-critic 系，每 Agent 独立策略但中心 Critic。
- **常见错误**：违反单调性（混合权重出现负值）→ 局部贪婪不再等于全局最优，执行崩；超网络输入错（用局部而非全局 s）。

## 闭卷自测
1. QMIX 的"单调性约束"具体是什么？它为何能保证去中心执行正确？
2. 相比 VDN，QMIX 凭什么更强、又凭什么仍受限（单调性的天花板）？

## 学完后可以完成

```dataview
LIST FROM "03-Projects" WHERE contains(requires, this.file.link)
```

## 相关下游知识

```dataview
LIST FROM "02-Knowledge/🧠 学习系统" WHERE contains(upstream, this.file.link)
```
