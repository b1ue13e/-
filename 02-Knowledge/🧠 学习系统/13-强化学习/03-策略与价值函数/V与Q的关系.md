---
type: study
topic: "V与Q的关系"
course: "强化学习"
created: 2026-08-07
status: completed
stage_moc: "[[🧭 阶段3-策略与价值函数]]"
flow: knowledge
kind: concept
difficulty: intermediate
concept: ["V^π(s)=Σ_a π(a|s)Q^π(s,a)", "Q^π(s,a)=E[R+γV^π(S')]", "V*=max_a Q*"]
upstream: ["[[V函数（状态价值函数）]]", "[[Q函数（动作价值函数）]]"]
tags: [学习, 强化学习]
---

# V与Q的关系

> 所属模块：[[🗺️ 强化学习学习路径|强化学习学习路径]]
> 主教材：`《Reinforcement Learning》`
> 对应阶段：[[🧭 阶段3-策略与价值函数|返回阶段页]]

## 动机
V 和 Q 描述的是同一策略的好坏，只是粒度不同（状态 vs 状态-动作）。它们之间如何换算？这一组关系是"值函数方法"统一框架的关键：由 Q 可求 V，由 V 也可求 Q；最优价值之间也有同样但更简洁的换算。

## 正式定义 / 公式

### 1. 由 Q 求 V（V 是 Q 在策略下的加权平均）
$$
V^\pi(s) = \sum_a \pi(a|s)\, Q^\pi(s,a)
$$
权重是策略 $\pi(a|s)$，**不一定均匀**。

### 2. 由 V 求 Q（走一步看转移）
$$
Q^\pi(s,a) = \sum_{s'} P(s'|s,a)\,\big[\,R(s,a,s') + \gamma\, V^\pi(s')\,\big]
$$
即在 $s$ 做 $a$ 后，对下一状态 $s'$ 求"奖励 + 折扣 V"的期望（若转移随机，必须对所有 $s'$ 加权）。

### 3. 最优价值之间的关系（用 max 而非加权）
$$
V^*(s) = \max_a Q^*(s,a),\qquad
Q^*(s,a) = \mathbb{E}\!\left[\,R + \gamma \max_{a'} Q^*(S',a')\,\right]
$$
最优下 V 是 Q 对动作取最大；Q 是"奖励 + 折扣后最优"。不再有策略加权，直接取 max。

## 最小手算例子
**由 Q 求 V**：$s_1$ 下 $\pi(\text{右})=0.6,\;\pi(\text{左})=0.4$，$Q(s_1,\text{右})=1,\;Q(s_1,\text{左})=0$：
$$
V(s_1)=0.6\cdot 1 + 0.4\cdot 0 = 0.6
$$
**由 V 求 Q**：2 状态 MDP，$s_1$ 做 step 必到 $s_2$，$R=+1$，$V(s_2)=0$，$\gamma=0.9$：
$$
Q(s_1,\text{step})=1\cdot[\,1+0.9\cdot 0\,]=1=V(s_1)\quad\checkmark
$$
**最优**：$s_1$ 两动作 $Q^*(s_1,\text{step})=1,\;Q^*(s_1,\text{stay})=0$ → $V^*(s_1)=\max(1,0)=1$。

## 对比与常见错误
- **把权重当成 $1/|A|$**：权重是策略 $\pi(a|s)$，均匀只是特例。
- **由 V 求 Q 漏掉期望号 $\sum_{s'}$**：转移随机时必须对所有可能 $s'$ 加权。
- **在最优关系里仍写 $\sum_a \pi(a|s)$**：最优时不再有策略加权，直接取 max。

## 闭卷自测
1. 由 Q 求 V 与由 V 求 Q 的公式各是什么？权重能否均匀？
2. 最优下 V 与 Q 的关系？为什么用 max 而非加权平均？

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
