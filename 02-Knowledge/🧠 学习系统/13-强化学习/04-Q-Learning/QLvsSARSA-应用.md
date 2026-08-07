---
type: study
topic: "QLvsSARSA-应用"
course: "强化学习"
created: 2026-04-18
status: completed
stage_moc: "[[🧭 阶段4-Q-Learning]]"
flow: knowledge
kind: concept
difficulty: intermediate
concept: ["QLvsSARSA-应用", "Q-Learning vs SARSA：应用场景"]
upstream: ["[[QLvsSARSA-策略]]", "[[QLvsSARSA-目标]]", "[[QLvsSARSA-风险]]"]
tags: [学习, 强化学习]
---

# QLvsSARSA-应用

> 所属模块：[[🗺️ 强化学习学习路径|强化学习学习路径]]
> 主教材：`《Reinforcement Learning》`
> 对应阶段：[[🧭 阶段4-Q-Learning|返回阶段页]]

## 动机
选哪个，取决于"是否在训练期就要实际执行"以及"环境是否有致命风险"。

## 正式定义 / 公式
- 确定性/可仿真环境、追求最优策略、能离线先训好：Q-learning（如离线训练后部署贪心策略）。
- 训练期就要在线执行、环境有危险/高代价：SARSA（学到"含探索"的安全策略）。
- 现代深度版：DQN 即 Q-learning 的神经网络版；多数 on-policy 深度算法（PPO/A2C）则更接近 SARSA 思想。

## 最小手算例子
<!-- NUMEX2 -->悬崖游走(cliff-walk) 12×4 网格：Q-learning 学到贴边最优路径（对偶然成功乐观），SARSA 学到离悬崖更远的安全路径；SARSA 平均步数略多但坠落率更低。

迷宫寻路（无致命危险）→ 两者都行，Q-learning 给最短路径；自动驾驶仿真（撞了代价大）→ 倾向 SARSA/保守策略。

## 对比与常见错误
- 常见错误：把"Q-learning 收敛到最优"直接等同于"实际部署最安全"——训练期在线执行时，学习到的策略要连同探索一起评估。

## 闭卷自测
1. 给出 Q-learning 与 SARSA 各自更适合的场景。
2. DQN 对应两者中的哪一个？
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
