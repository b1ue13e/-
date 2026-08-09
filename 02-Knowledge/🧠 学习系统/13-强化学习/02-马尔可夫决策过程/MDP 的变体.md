---
type: study
topic: "MDP 的变体"
course: "强化学习"
created: 2026-08-07
status: completed
stage_moc: "[[🧭 阶段2-马尔可夫决策过程]]"
flow: knowledge
kind: concept
difficulty: intermediate
concept: ["确定性 MDP", "随机性 MDP", "连续 MDP", "多智能体 MDP"]
upstream: ["[[MDP 与贝尔曼方程]]", "[[MDP-转移概率]]", "[[POMDP]]"]
tags: [学习, 强化学习]
---

# MDP 的变体

> 所属模块：[[🧭 阶段2-马尔可夫决策过程]] · 主线：MDP 五元组
> 前置：[[MDP 与贝尔曼方程]] · [[MDP-转移概率]] · [[POMDP]]

## 动机
标准 MDP 是随机、离散、单智能体的抽象。现实任务常以不同变体出现：确定性、随机性、连续、多智能体。本卡把四类常见 MDP 变体收口，说明各自对算法选型的影响。

## 正式定义 / 公式

### 1. 确定性 MDP
- 对每个 $(s,a)$，存在唯一 $s'$ 使 $P(s'\mid s,a)=1$；转移可写成函数 $s'=f(s,a)$，奖励 $r=R(s,a,s')$。是随机 MDP 的特例（退化分布）。
- 例：状态 s∈{1,2,3}，动作"右"：f(1,右)=2, f(2,右)=3, f(3,右)=3（撞墙不动）。自底向上：V(3)=0, V(2)=2+0.9·0=2, V(1)=1+0.9·2=2.8。

### 2. 随机性 MDP
- 对 $(s,a)$，$P(s'\mid s,a)$ 是非退化分布，下一状态按概率采样；价值是期望 $v_\pi(s)=\mathbb{E}[G_t\mid s]$，同动作不同结果。
- 例：掷骰子走格，同样"前进 3"可能因骰子结果落到不同格；规划须用期望。随机下需多次采样估计价值，更需探索。

### 3. 连续 MDP
- $\mathcal{S}\subset\mathbb{R}^n$、$\mathcal{A}\subset\mathbb{R}^m$ 连续；价值/策略用神经网络等参数化 $v_\theta(s)$、$a_\mu(s)$，梯度类算法主导。
- 例：倒立摆 $\mathcal{S}=(角度,角速度)\in\mathbb{R}^2$，$\mathcal{A}=力矩\in\mathbb{R}$；PPO/SAC 直接输出连续动作。表格法失效，需函数近似与合适探索（高斯噪声）、尺度归一。

### 4. 多智能体 MDP（MMDP / Dec-POMDP）
- 状态转移依赖**联合动作** $a=(a_1,\dots,a_n)$；关系可分**合作**（共享回报）、**竞争**（零和）、**混合**。
- 对单个 Agent，他人即环境的一部分，问题变成随机 MDP；足球 AI：11 个 Agent 联合动作决定球权转移。
- 注意：假设他人静止会失败；对手策略在变（非平稳性），经验可能过期。

## 最小手算例子
- 确定性 MDP 见上 V 计算。
- 随机性：掷骰子走格。
- 连续：倒立摆 PPO/SAC。
- 多智能体：足球 AI 合作进球、竞争抢断。

## 对比与常见错误
- **假设一切确定**：真实/仿真常含噪声，需随机建模；把随机当确定会忽略方差、规划过于乐观。
- **用单次结果当期望**：随机下需多次采样估计价值。
- **直接套表格法**：连续空间无法枚举状态。
- **忽略采样/归一化**：连续动作需合适探索与尺度归一。
- **假设他人静止 / 忽略非平稳性**：多智能体下对手策略在变，经验可能过期。

## 闭卷自测
1. 确定性 MDP 的转移如何表示？它与随机 MDP 的关系？
2. 随机 MDP 的价值为何是期望？与确定性 MDP 训练差异？
3. 连续 MDP 为何不能用 Q 表？常见处理函数近似方法？
4. 多智能体 MDP 的转移依赖什么？对单个 Agent 它表现为哪类 MDP？

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
