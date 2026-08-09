---
created: 2026-08-07
type: study
course: "强化学习"
title: "MCTS与模型基规划 (MCTS for Model-based Planning)"
topic: "MCTS与模型基规划 (MCTS for Model-based Planning)"
stage_moc: "[[🧭 阶段8-模型基与规划]]"
flow: knowledge
kind: algorithm
status: learning
importance: "A"
tags: [学习, 强化学习, 模型基, 搜索]
upstream: ["[[模型基RL概述]]", "[[MuZero]]", "[[模型预测控制MPC]]"]
concept: ["MCTS", "UCB", "AlphaZero", "MuZero", "搜索树"]
sources:
  - "Silver et al. 2016/2017/2020 (AlphaGo Zero, AlphaZero, MuZero)"
---
# MCTS与模型基规划 (MCTS for Model-based Planning)

> 所属模块：[[🗺️ 强化学习学习路径|强化学习学习路径]]
> 对应阶段：[[🧭 阶段8-模型基与规划|返回阶段页]]

## 动机
模型基 RL 的"规划"在 Atari/围棋这类离散大状态空间里，常由**蒙特卡洛树搜索（MCTS）**承担。AlphaZero 用已知规则模型 + MCTS 横扫棋类；MuZero 更进一步，用**学得的潜空间模型**做 MCTS，无需环境规则。MCTS 把"想象搜索"和"策略/价值提升"耦合起来。

## 正式定义 / 公式
MCTS 四步循环（在模型 f 上）：
1. **选择**：从根沿 UCB 选子节点，a = argmax Q(s,a) + c·P(s,a)·√(ΣN)/(1+N(s,a))，直到未展开节点。
2. **扩展**：用模型展开该节点，得到子状态与初始价值。
3. **仿真/评估**：用学到的价值网络 v_θ 或 rollout 估计叶子价值 G。
4. **回溯**：沿路径更新 N（访问次数）与 Q（价值均值）。
最终选访问次数最高的动作。AlphaZero 用 (p_θ 策略先验, v_θ 价值) 监督；MuZero 的模型还预测 reward 与 value，在 latent 里搜索。

## 最小手算例子
井字棋/围棋：根节点是当前局面，MCTS 在"想象"的对弈树里反复模拟，越常导致胜利的分支 N 越大；落子时直接选 N 最高的那步。模型 f 若是真实规则（AlphaZero）则零样本泛化到未见局面；若是学得的（MuZero）则靠表示/动力学网络生成 latent 转移。

## 对比与常见错误
- 与 MPC/CEM：MCTS 是树搜索、非均匀展开；CEM 是轨迹采样优化。
- 与背景规划 Dyna：MCTS 是**决策时、针对当前状态的搜索**；Dyna 离线更新值表。
- **常见错误**：模型 f 有偏导致搜索在错误树上自我强化（MuZero 用 value 正则缓解）；温度/探索常数 c 设错导致过早收敛或发散。

## 闭卷自测
1. MCTS 四步是什么？UCB 项分别鼓励什么？
2. MuZero 用 MCTS 与 AlphaZero 的根本区别（模型来源）？

## 学完后可以完成

```dataview
LIST FROM "03-Projects" WHERE contains(requires, this.file.link)
```

## 相关下游知识

```dataview
LIST FROM "02-Knowledge/🧠 学习系统" WHERE contains(upstream, this.file.link)
```
