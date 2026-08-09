---
title: "SARSA 算法"
type: study
topic: "SARSA 算法"
course: "强化学习"
created: 2026-08-07
status: learning
stage_moc: "[[🧭 阶段4-Q-Learning]]"
flow: knowledge
kind: concept
upstream: ["[[Q-Learning算法]]", "[[时序差分与 Q-Learning]]"]
tags: [强化学习, SARSA, 时序差分, On-Policy, 无模型RL]
concept: ["SARSA", "On-Policy", "TD 控制", "同策略"]
---

# SARSA 算法

## 1. SARSA 的定义与核心思想

**SARSA** 是一种**同策略（On-Policy）**的时序差分（TD）控制算法，直接学习行为策略（用于与环境交互的策略）下的动作价值函数 $Q^\pi(s,a)$。它由 Rummery 与 Niranjan 于 1994 年提出，名字来自一次转移中依次出现的五个量：**S**tate、**A**ction、**R**eward、**S**tate、**A**ction —— 即 $(S_t, A_t, R_{t+1}, S_{t+1}, A_{t+1})$。

**基本性质**：SARSA 的"学习策略"与"行为策略"是同一个（例如同一个 ε-greedy）。更新目标用"行为策略实际选出的下一动作 $A_{t+1}$"构造，因此学到的是"在该探索策略下的价值"，而非理论最优 $Q^*$。

---

## 2. 更新式与 TD 目标

**SARSA 更新（On-Policy TD 控制）**：

$$Q(S_t,A_t)\leftarrow Q(S_t,A_t)+\alpha\big[R_{t+1}+\gamma\,Q(S_{t+1},A_{t+1})-Q(S_t,A_t)\big]$$

其中 $A_{t+1}$ 由**当前行为策略**在 $S_{t+1}$ 选出（如 ε-greedy）。对比 Q-Learning 目标用 $\max_{a'}Q(S',a')$（贪心最优），SARSA 用行为策略选出的 $Q(S',A')$，这是两者数学上的根本差异。

**TD 误差**：$\delta_t = R_{t+1}+\gamma Q(S_{t+1},A_{t+1})-Q(S_t,A_t)$，更新即 $Q\leftarrow Q+\alpha\delta_t$。

---

## 3. 同策略（On-Policy）的含义

"On-Policy" 指用来"学习/更新"的策略与用来"与环境交互"的策略是同一个（$\pi_b = \pi$）。例如都用同一个 ε-greedy：

- SARSA 评估的是"带噪声的探索策略"的价值——它知道有时会因探索而走错，于是学到的 Q 反映了"真实会怎么走"。
- 常见错误：以为 on-policy 就"不能用探索"——行为策略本身可以带探索（ε-greedy），只是学与用同一策略。
- 对比 Q-Learning（off-policy）：Q-learning 学的是贪心最优 $Q^*$，不关心行为策略的探索；SARSA 把探索噪声直接纳入学习目标。

---

## 4. 收敛条件：GLIE

SARSA 在什么条件下收敛到"该策略下"的最优？答案是满足 **GLIE（Greedy in the Limit with Infinite Exploration）**：

- **所有状态-动作对被无限次访问**；
- **行为策略随时间趋近贪心**。

在此条件下，SARSA 收敛到最优动作价值（对所用的渐进贪心策略而言）。

- 例：ε-greedy 取 $\epsilon_t=1/t$：保证无限探索（GLIE 第一点）且最终趋近贪心（第二点）→ SARSA 收敛到最优。
- 常见错误：固定 ε（如恒 0.1）也期望收敛到最优——固定 ε 不满足"极限贪心"，通常只收敛到 ε-贪心策略下的次优值。

---

## 5. 最小手算例子

**2 状态链**（A→B 终止）：right→B(R=+1)，left→A(R=0)。γ=0.9, α=0.5, Q 初 0。
在 (A,right) 得 r=+1, s'=B；行为策略在 B 无动作（终止）则 $Q(B,\cdot)=0$。
目标 $= 1 + 0.9\cdot 0 = 1$，误差 $= 1-0 = 1$，$Q(A,right) \leftarrow 0 + 0.5\cdot 1 = 0.5$。

**五元组**：在 s1 用 ε-greedy 选 a=right，得 r=+1, s2；再用同策略选 a'=right。五元组 (s1,right,+1,s2,right) 即 SARSA 所用。名字强调"同一策略选 $A_{t+1}$"，正是 on-policy 的体现。

---

## 6. 对比与常见错误

| 维度 | SARSA（同策略） | Q-Learning（异策略） |
| :--- | :--- | :--- |
| 更新目标 | $r+\gamma Q(S',A')$，A' 由行为策略选 | $r+\gamma\max_{a'}Q(S',a')$ |
| 学到的值 | 行为策略（含探索）下的价值 | 贪心最优 $Q^*$ |
| 风险偏好 | 保守（计入探索风险） | 乐观（只看最优） |

- 常见错误：把 SARSA 目标写成 max——那是 Q-Learning 标志。
- 常见错误：把 SARSA 名字当成某人缩写——它直接来自五元组顺序 (S,A,R,S,A)。

---

## 7. 闭卷自测

1. 写出 SARSA 更新式，并说明 $A_{t+1}$ 从哪来。
2. 什么是 on-policy？SARSA 如何体现？
3. SARSA 收敛需要什么条件？为什么固定 ε 通常只收敛到次优？
4. SARSA 与 Q-Learning 更新目标的区别是什么？
5. 为什么 SARSA 面对危险（如悬崖）时更保守？

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
