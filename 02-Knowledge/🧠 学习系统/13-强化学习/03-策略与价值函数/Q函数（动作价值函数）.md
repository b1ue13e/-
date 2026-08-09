---
type: study
topic: "Q函数（动作价值函数）"
course: "强化学习"
created: 2026-08-07
status: completed
stage_moc: "[[🧭 阶段3-策略与价值函数]]"
flow: knowledge
kind: concept
difficulty: intermediate
concept: ["动作价值函数 Q^π(s,a)", "最优动作价值 Q*(s,a)", "状态-动作价值"]
upstream: ["[[V函数（状态价值函数）]]", "[[回报定义]]"]
tags: [学习, 强化学习]
---

# Q函数（动作价值函数）

> 所属模块：[[🗺️ 强化学习学习路径|强化学习学习路径]]
> 主教材：`《Reinforcement Learning》`
> 对应阶段：[[🧭 阶段3-策略与价值函数|返回阶段页]]

## 动机
有时我们不仅关心"这个状态好不好"，还关心"在这个状态**做某个动作**好不好"。这引出了**动作价值函数 Q^π(s,a)**。它把"状态-动作对"映射成标量评分，比 V 多了一维——正因为如此，Q 能直接给出"每状态该选哪个动作"，是 Q-learning、DQN 等算法的直接学习目标。

## 正式定义 / 公式

### 1. 定义：动作价值函数 Q^π(s,a)
$$
Q^\pi(s,a) = \mathbb{E}_\pi\!\left[\,G_t \mid S_t = s,\; A_t = a\,\right]
$$
即在 $s$ 执行 $a$、之后遵循 $\pi$ 的条件下，回报的期望。

### 2. 期望展开（两种等价形式）
$$
Q^\pi(s,a) = \mathbb{E}_\pi\!\left[\,\sum_{k=0}^\infty \gamma^k R_{t+k+1} \mid S_t=s,\;A_t=a\,\right]
$$
递归形式（注意第一步固定了 $a$，其后动作由 $\pi$ 决定，所以是 $Q$ 的自举）：
$$
Q^\pi(s,a) = \mathbb{E}_\pi\!\left[\,R_{t+1} + \gamma Q^\pi(S_{t+1}, A_{t+1}) \mid S_t=s,\;A_t=a\,\right]
$$

### 3. 直觉："在某状态试某动作"的性价比评分
- $Q^\pi(s,a)$ 高 → 在 $s$ 做 $a$ 是个好选择。
- 最优 $Q^*$：$\displaystyle Q^*(s,a)=\max_\pi Q^\pi(s,a)$；取 $a^*=\arg\max_a Q^*(s,a)$ 即得最优动作。
- 很多算法（Q-learning、DQN）学的就是 $Q^*$，再贪心出策略。

### 4. 最优动作价值 Q*(s,a)
$$
Q^*(s,a) = \max_\pi Q^\pi(s,a)
$$
满足**贝尔曼最优方程**：
$$
Q^*(s,a) = \mathbb{E}\!\left[\,R + \gamma \max_{a'} Q^*(S',a')\,\right]
$$
（见「贝尔曼方程」）。

## 最小手算例子
沿用 2 状态 MDP：$s_1$ 只有动作 step，奖励 +1，$s_2$ 终止故 $Q=0$。
$$
Q^\pi(s_1,\text{step}) = \mathbb{E}[\,R + \gamma Q(s_2,\cdot)\,] = 1 + 0.9\cdot 0 = 1 = V^\pi(s_1)
$$
两动作情形：$s_1$ 下 step 给 +1、stay 给 0，则 $Q^*(s_1,\text{step})=1 > Q^*(s_1,\text{stay})=0$，最优动作 = step。

## 对比与常见错误
- **与 V**：V 对"状态"打分；Q 对"状态-动作"打分。给定策略时 $V(s)=\sum_a \pi(a|s)Q(s,a)$（见「V与Q的关系」）。
- **把 Q(s,a) 当成"在 s 之后全程都做 a"**：实际只在第一步做 $a$，之后回到策略 $\pi$。
- **递归式里第二步仍写 V 而非 Q**：严格递归应回到 $Q$（因第一步固定了 $a$，其后动作由 $\pi$ 决定，是 $Q$ 的自举）。
- **混淆 Q*(s,a) 与 V*(s)**：关系为 $V^*(s)=\max_a Q^*(s,a)$（见「V与Q的关系」）。

## 闭卷自测
1. $Q^\pi(s,a)$ 的定义？Q 与 V 的核心区别？
2. 写出 $Q^\pi(s,a)$ 的两种公式；递归形式里为什么回到 $Q$ 而不是 $V$？
3. $Q^*(s,a)$ 的定义与最优方程？如何用 $Q^*$ 得到 $V^*$ 与 $\pi^*$？

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
