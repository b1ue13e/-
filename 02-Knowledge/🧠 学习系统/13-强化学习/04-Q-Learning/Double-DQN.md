---
type: study
topic: "Double-DQN"
course: "强化学习"
created: 2026-04-18
status: completed
stage_moc: "[[🧭 阶段4-Q-Learning]]"
flow: knowledge
kind: concept
difficulty: intermediate
concept: ["Double-DQN", "Double DQN"]
upstream: ["[[DQN-目标网络]]", "[[QL-最大化偏差]]"]
tags: [学习, 强化学习]
---

# Double-DQN

> 所属模块：[[🗺️ 强化学习学习路径|强化学习学习路径]]
> 主教材：`《Reinforcement Learning》`
> 对应阶段：[[🧭 阶段4-Q-Learning|返回阶段页]]

## 动机
标准 DQN 的 max 在"选动作"和"评价值"上都用同一（目标）网络，放大最大化偏差、过估计 Q。Double DQN 把"选择"与"评估"解耦。

## 正式定义 / 公式
- 用在线网络 θ 选最优动作：a* = argmax_{a'} Q_θ(s', a')
- 用目标网络 θ^- 评估：y = r + γ Q_{θ^-}(s', a*)
即"在线网选、目标网评"，消除同一网络既选又评带来的正向偏差。

## 最小手算例子
<!-- NUMEX -->目标 y=r+γ·Q_target(s', argmaxₐ Q_online(s',a))。若 Q_online(s',·)=[0.9,0.4] 选中 a1，Q_target(s',a1)=0.8 ⇒ y=r+γ·0.8（动作选择与价值估计解耦，抑制 Q 过高估计）。

若目标网对某噪声动作估值虚高，标准 DQN 会既选它又高估它；DDQN 改用在线网选动作，避免被同一虚高值误导。

## 对比与常见错误
- 与 DQN：DDQN 几乎同成本，但显著降低过估计、提升稳定性。
- 常见错误：以为 DDQN 用"两个独立随机初始化网络"——实际上仍共享训练，只是选/评分离。

## 闭卷自测
1. Double DQN 如何缓解最大化偏差？
2. "选"与"评"分别用哪个网络？
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
