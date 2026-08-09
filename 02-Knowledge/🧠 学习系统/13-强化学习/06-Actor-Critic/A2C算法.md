---
title: "A2C 算法（同步优势 Actor-Critic）"
type: study
topic: "A2C 算法"
course: "强化学习"
created: 2026-08-07
status: learning
stage_moc: "[[🧭 阶段6-Actor-Critic]]"
flow: knowledge
kind: concept
upstream: ["[[Actor-Critic架构]]", "[[Actor网络]]", "[[Critic网络]]", "[[优势估计]]", "[[GAE广义优势估计]]"]
tags: [学习, 强化学习, A2C, Actor-Critic]
---
> 所属模块：[[🗺️ 强化学习学习路径|强化学习学习路径]]
> 主教材：`《Reinforcement Learning》`
> 对应阶段：[[🧭 阶段6-Actor-Critic|返回阶段页]]

# A2C 算法 (Advantage Actor-Critic，同步优势 Actor-Critic)

---

## 0. 学习边界

- **类别**：**A 类（核心概念，必须深挖）**
- **判断理由**：A2C 是 AC 的同步并行实用版，是 PPO/A3C 的共同祖先；理解它的"同步收集 + 批量 GAE + 联合损失"才能读懂现代 on-policy 训练循环。

---

## 1. A2C 是什么（家族定位）

A2C（Advantage Actor-Critic）是 Actor-Critic 的**同步并行**实用版：多个环境同步收集、同步更新。

- 多 worker **同步**执行，收集一批轨迹后用 GAE 估计优势，统一更新 Actor/Critic。
- 同步意味着所有 worker 用同一套参数、步调一致。

**最小手算例子**：4 个并行环境各跑一段，收集后合并，用 GAE 算优势，一次梯度更新全局参数。

- **与 A3C 对比**：A2C 同步、实现简单、易在 GPU 批量；A3C 异步。
- **常见错误**：把 A2C 当"单环境 AC"——它强调多环境并行批量。

---

## 2. 同步机制（Barrier 同步）

A2C 的"同步"指：等所有 worker 完成本轮收集，再统一更新，再广播新参数。

> Barrier 同步：workers 收集 → 汇总梯度/优势 → 中心更新 → 广播参数 → workers 继续。

避免异步带来的陈旧梯度（stale gradients）。

**最小手算例子**：4 worker 各跑 20 步后齐步等待，中心合并更新，再同时拿到新参数。

- **与 A3C 异步**：同步无陈旧梯度但需等最慢 worker；异步更快但梯度可能旧。
- **常见错误**：以为同步一定慢——GPU 批量下同步常更高效。

---

## 3. 批量优势估计

A2C 的优势估计常在"一批轨迹"上做（常用 GAE），更稳定。对一批 $(s,a,r,s')$ 用 GAE 算 $A_t^{\text{GAE}}$，再批量做 Actor/Critic 更新（MSE + 策略梯度）。批量降低单样本噪声。

**最小手算例子**：收集 4 worker × 20 步 = 80 个 transition，GAE 得 80 个优势，批量反向传播。

- **与逐样本更新对比**：批量估计优势方差更低、GPU 利用率高。
- **常见错误**：批次过大拖慢反馈——需调批量与回报周期。

---

## 4. A2C 的总损失

总损失 = Actor 损失 + Critic 损失（常加熵项）：

$$L = -\mathbb{E}\big[\log\pi_\theta(a|s)\cdot A\big] + c_v\,\mathbb{E}\big[(V_\phi(s)-y)^2\big] - c_e\,H(\pi_\theta)$$

三项：策略梯度（带优势）、价值 MSE、熵正则（鼓励探索）。

**最小手算例子（单样本）**：Actor 项 $-\log\pi(a_1)\cdot 1.05$；Critic 项 $(V(s)-1.45)^2$；熵项 $-c_e H$。三项加权求和反传。

- **与单纯 PG 对比**：多了 Critic MSE 与熵项。
- **常见错误**：漏掉熵项导致探索不足，或熵系数过大扰训练。

---

## 5. 最简 A2C 循环

最简 A2C：单（或少量）环境的 AC 在线循环。流程：用当前策略交互若干步 → 用优势更新 Actor/Critic → 重复。即 [[Actor-Critic架构]] 的基本在线版。

**最小手算例子（手算优势）**：某步回报 $G=5$、价值 $V(s)=3$ ⇒ $A=+2$（正向，应增强该动作）；若 $V(s)=5$ ⇒ $A=0$（与平均持平，不应调整）。每收集 $T$ 步：$(s,a,r,s')$ 算 TD/GAE 优势，更新 $\theta,\phi$，继续。

- **与完整 A2C 对比**：简单版不一定多 worker 批量；完整版强调并行批量。
- **常见错误**：以为简单版不用优势——AC 核心仍是优势更新。

---

## 6. 合并要点与误区

| 维度 | 要点 |
| :--- | :--- |
| 同步 | Barrier 等最慢 worker，无陈旧梯度 |
| 批量 | 多环境合并 + GAE，低方差 |
| 损失 | 策略梯度 + 值 MSE + 熵 |
| 误区 | 别当单环境 AC；熵项别漏别过大 |

---

## 闭卷自测
1. A2C 是什么？与 A3C 的关键区别？
2. A2C 的"同步"具体指什么？代价与收益？
3. A2C 如何批量估计优势？写成总损失构成。
4. 熵项在 A2C 损失中起什么作用？

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
