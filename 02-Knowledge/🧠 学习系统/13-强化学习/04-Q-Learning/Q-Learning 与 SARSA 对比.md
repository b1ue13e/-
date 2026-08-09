---
title: "Q-Learning 与 SARSA 对比"
type: study
topic: "Q-Learning 与 SARSA 对比"
course: "强化学习"
created: 2026-08-07
status: learning
stage_moc: "[[🧭 阶段4-Q-Learning]]"
flow: knowledge
kind: concept
upstream: ["[[Q-Learning算法]]", "[[SARSA 算法]]", "[[时序差分与 Q-Learning]]"]
tags: [强化学习, Q-Learning, SARSA, On-Policy, Off-Policy, 对比]
concept: ["Q-Learning", "SARSA", "Off-Policy", "On-Policy", "风险偏好"]
---

# Q-Learning 与 SARSA 对比

## 1. 更新目标的差异（根本不同）

| | Q-Learning（异策略） | SARSA（同策略） |
| :--- | :--- | :--- |
| 更新目标 | $r+\gamma\max_{a'}Q(S',a')$ | $r+\gamma Q(S',A')$，A' 由行为策略选出 |
| 策略属性 | Off-Policy，学贪心最优 $Q^*$ | On-Policy，学行为策略下的价值 |
| 风险偏好 | 乐观（只看最优） | 保守（计入探索风险） |

更新目标的差异是两者数学上的根本不同，也解释了风险偏好差异。常见错误：把 SARSA 目标写成 max——那是 Q-Learning 标志。

## 2. 策略类型：On-Policy vs Off-Policy

- Q-Learning：Off-Policy，学贪心最优 $\pi^*$（不依赖行为策略）。
- SARSA：On-Policy，学行为策略（如 ε-greedy）下的价值。

同一悬崖环境：Q-Learning 评估"最优路径"（贴边走，最短但危险）；SARSA 评估"ε-greedy 实际会走的路径"（略远离悬崖，更保守）。常见错误：认为"两者最终策略一样"——Q-Learning 收敛到真正贪心最优；SARSA 收敛到其行为策略下最优（若 ε 不趋 0 则偏保守）。

## 3. 风险偏好与悬崖行走

因为有/无探索的"目标"不同，两者面对危险（如悬崖）时表现迥异：

- Q-Learning（off-policy）：学最优 $Q^*$，目标恒取 max——"乐观"，可能选贴边的高回报高风险动作。
- SARSA（on-policy）：目标含行为策略的探索，会把"探索误入危险"的代价算进去——"保守"，主动绕开危险区。

悬崖行走（cliff-walk）12×4 网格：Q-Learning 学到贴边直走（最短、但一步踏空即死）；SARSA 学到离悬崖一格走（略长但稳）。在线（边学边用）时 SARSA 往往活得更久。常见错误：认为 Q-Learning "一定更好"——训练期就要实际执行（online）且有致命危险时，SARSA 更安全。

## 4. 最小手算例子（数值）

设 $Q(s,a)=0$，$\alpha=0.1$，$r=1.0$，$\gamma=0.9$。

- Q-Learning 取 $\max_{a'}Q(s',a')=0.5$ ⇒ $Q\leftarrow 0+0.1\times(1+0.9\times0.5-0)=0.145$。
- SARSA 用实际下一步动作 $Q(s',a')=0.3$ ⇒ $Q\leftarrow 0+0.1\times(1+0.9\times0.3-0)=0.127$（更保守）。

若 s' 处行为策略多半选"安全动作"（Q 较低），SARSA 目标偏低（保守）；Q-Learning 目标取 max（乐观）。

## 5. 各自适合的场景

- **Q-Learning（及 DQN）**：确定性/可仿真环境、追求最优策略、能离线先训好再部署贪心策略。
- **SARSA**：训练期就要在线执行、环境有危险/高代价（学到"含探索"的安全策略）。
- 现代深度版：DQN 即 Q-Learning 的神经网络版；多数 on-policy 深度算法（PPO/A2C）更接近 SARSA 思想。

迷宫寻路（无致命危险）→ 两者都行，Q-Learning 给最短路径；自动驾驶仿真（撞了代价大）→ 倾向 SARSA/保守策略。常见错误：把"Q-Learning 收敛到最优"直接等同于"实际部署最安全"——训练期在线执行时，学习到的策略要连同探索一起评估。

## 6. 闭卷自测

1. 写出两者更新目标并圈出关键差异。
2. 两者在 on/off-policy 上的区别？这导致学到的策略有何不同？
3. 为何 SARSA 更"保守"？何时 Q-Learning 的风险偏好反而是缺点？
4. 给出 Q-Learning 与 SARSA 各自更适合的场景；DQN 对应哪一个？
5. 用数值例子说明同一转移下两者的更新量差异。

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
