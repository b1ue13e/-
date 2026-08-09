---
type: study
topic: "V函数（状态价值函数）"
course: "强化学习"
created: 2026-08-07
status: completed
stage_moc: "[[🧭 阶段3-策略与价值函数]]"
flow: knowledge
kind: concept
difficulty: intermediate
concept: ["状态价值函数 V^π(s)", "最优状态价值 V*(s)", "折扣回报期望"]
upstream: ["[[回报定义]]", "[[MDP 与贝尔曼方程]]"]
tags: [学习, 强化学习]
---

# V函数（状态价值函数）

> 所属模块：[[🗺️ 强化学习学习路径|强化学习学习路径]]
> 主教材：`《Reinforcement Learning》`
> 对应阶段：[[🧭 阶段3-策略与价值函数|返回阶段页]]

## 动机
我们怎么判断"某个状态好不好"？最直接的方式：从这一状态出发、按当前策略一直走，未来能拿到的（折扣）回报平均有多少。这个"长期期望值"就是**状态价值函数 V^π(s)**。它把"状态"直接映射成一个标量分数，是价值方法（value-based）与几乎所有 DP/TD 算法的基石。

## 正式定义 / 公式

### 1. 定义：状态价值函数 V^π(s)
$$
V^\pi(s) = \mathbb{E}_\pi\!\left[\,G_t \mid S_t = s\,\right]
$$
即在状态 $s$ 出发、之后始终遵循策略 $\pi$ 的条件下，回报 $G_t$ 的期望。

### 2. 期望展开（两种等价形式）
把 $G_t = \sum_{k=0}^\infty \gamma^k R_{t+k+1}$ 代入，可得"展开求和"形式：
$$
V^\pi(s) = \mathbb{E}_\pi\!\left[\,\sum_{k=0}^\infty \gamma^k R_{t+k+1} \mid S_t = s\,\right]
$$
或等价写成**递归一步 + 剩余**的"期望递归"形式（贝尔曼期望方程的雏形）：
$$
V^\pi(s) = \mathbb{E}_\pi\!\left[\,R_{t+1} + \gamma V^\pi(S_{t+1}) \mid S_t = s\,\right]
$$
两个式子等价：前者把整条轨迹展开，后者只往前看一步、把"剩余"用 $V^\pi$ 自身表示。

### 3. 直觉：状态的一张"分数表"
- $V^\pi(s)$ 越大 → 从 $s$ 出发长期收益越高（好状态、好策略）。
- 不同策略得到不同的 $V$：$V^{\pi_1}(s) > V^{\pi_2}(s)$ 表示在 $s$ 处策略 $\pi_1$ 比 $\pi_2$ 好。

### 4. 最优状态价值 V*(s)
$$
V^*(s) = \max_\pi V^\pi(s) = \max_\pi \mathbb{E}_\pi[\,G_t \mid S_t=s\,]
$$
即对所有策略取最大，是状态 $s$ 能达到的最高分。它满足**贝尔曼最优方程**（见「贝尔曼方程」）。

## 最小手算例子
2 状态 MDP：$s_1 \xrightarrow{\text{step}} s_2$（终止），转移概率 1，奖励 $R=+1$，$\gamma=0.9$；$s_2$ 终止故 $V(s_2)=0$。
$$
V^\pi(s_1) = \mathbb{E}[\,R + \gamma\cdot 0\,] = 1 + 0.9\cdot 0 = 1
$$
若 $s_1$ 还有动作"停留"拿 0，则最优仍取 step，$V^*(s_1)=1$。

两个策略对比：$\pi_a$ 从 $s_1$ 直接拿 +1 到终止；$\pi_b$ 绕路拿 0 再终止，则 $V^{\pi_a}(s_1)=1 > V^{\pi_b}(s_1)=0$。

## 对比与常见错误
- **与 Q 函数**：V 只看"状态"，Q 同时看"状态-动作对"。关系见「V与Q的关系」。
- **漏掉"条件于 π"**：$V$ 的值依赖所用策略，换策略值就变（记为 $V^\pi$）。
- **把 V(s) 当成"立即奖励"**：$V$ 是长期期望回报，不是单步奖励。
- **认为 V*(s) 依赖某个具体策略**：$V^*$ 是"跨所有策略"的最大值，本身不直接对应单一可执行策略（需配合 $Q^*$ 取贪心得到 $\pi^*$，见「贝尔曼方程」）。

## 闭卷自测
1. $V^\pi(s)$ 的定义与含义？为什么上标要标 $\pi$？
2. 写出 $V^\pi(s)$ 的两种等价公式；折扣因子 $\gamma$ 在公式里的作用是什么？
3. 怎么用直觉解释 $V^\pi(s)$？$V^*(s)$ 与 $V^\pi(s)$ 的关系？

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
