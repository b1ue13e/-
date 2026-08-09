---
type: study
topic: "MDP 的状态、动作与奖励"
course: "强化学习"
created: 2026-08-07
status: completed
stage_moc: "[[🧭 阶段2-马尔可夫决策过程]]"
flow: knowledge
kind: concept
difficulty: beginner
concept: ["MDP 五元组 (S,A,P,R,γ)", "状态空间", "动作空间 A(s)", "奖励函数 R(s,a)"]
upstream: ["[[状态空间]]", "[[动作空间]]", "[[奖励函数]]"]
tags: [学习, 强化学习]
---

# MDP 的状态、动作与奖励

> 所属模块：[[🧭 阶段2-马尔可夫决策过程]] · 主线：MDP 五元组
> 前置：[[状态空间]] · [[动作空间]] · [[奖励函数]]

## 动机
MDP 用五元组 $(\mathcal{S},\mathcal{A},P,R,\gamma)$ 形式化一个序贯决策问题。本卡把"状态空间、动作空间、奖励函数"三个分量收口（转移概率 $P$ 与折扣 $\gamma$ 见「MDP-转移概率」「MDP-折扣因子」），建立从阶段 1 概念到 MDP 框架的精确落点。

## 正式定义 / 公式

### 1. 状态空间 $\mathcal{S}$
- $\mathcal{S}$：所有可能状态的集合；在 MDP 中状态必须满足**马尔可夫性**（足以预测未来，无需更早历史）。
- 离散 MDP：$\mathcal{S}$ 有限或可数（如 $4\times4$ 网格世界 $\mathcal{S}=\{1,\dots,16\}$）；连续 MDP：$\mathcal{S}\subset\mathbb{R}^n$。
- **状态 $\neq$ 观测**：POMDP 中观测 $o$ 不等于 $s$（见 [[POMDP]]）；状态不满足马尔可夫性时需把历史拼入状态（见 [[马尔可夫性质]]）。

### 2. 动作空间 $\mathcal{A}$
- $\mathcal{A}$：所有可能动作的集合；可依赖状态记为 $\mathcal{A}(s)$。
- **离散动作**：有限集，如网格世界 $\{上,下,左,右\}$（悬崖路中"下"会坠崖）。
- **连续动作**：$\mathcal{A}\subset\mathbb{R}^n$，如力矩向量（见 [[MDP 的变体|连续 MDP]]）。
- 规模对比：网格世界 $|A|=4$，max_a Q 只比 4 个数；连续控制如机械臂 $A\subset\mathbb{R}^2$ 乃至 $\mathbb{R}^6$，动作不可枚举，Q-learning 的 max 直接失效。

### 3. 奖励函数 $R$
- 期望形式：$R(s,a)=\mathbb{E}[R_{t+1}\mid S_t=s,A_t=a]$，或 $R(s,a,s')=\mathbb{E}[R_{t+1}\mid s,a,s']$。
- 与阶段 1 [[奖励函数]] 一致，只是现在明确处于 MDP 框架（依赖 $s,a$）；奖励塑造（reward shaping）常在此设计（见 [[奖励设计与环境工程]]）。
- 迷宫例：每步 −1（鼓励快），到达终点 +10，撞墙 −5。

## 最小手算例子
- $4\times4$ 网格世界：$\mathcal{S}=\{1,\dots,16\}$（含终止格），$\mathcal{A}=\{N,S,E,W\}$；悬崖路问题中"下"会坠崖（负奖励）。
- 连续控制：倒立摆 $\mathcal{S}=(角度,角速度)\in\mathbb{R}^2$，$\mathcal{A}=力矩\in\mathbb{R}$；PPO/SAC 直接输出连续动作。

## 对比与常见错误
- **状态 $\neq$ 观测**：POMDP 中二者不同。
- **忽略 $\mathcal{A}(s)$ 约束**：某些状态不可行动作需单独建模。
- **混淆动作与状态**：动作是干预，不是状态的一部分。
- **奖励 $\neq$ 回报**：奖励是单步，回报是折扣累积（见 [[回报定义]]）。
- **奖励黑客**：错误塑造会引出非预期最优行为。

## 闭卷自测
1. 写出 MDP 五元组；MDP 中状态必须满足什么性质？不满足会怎样？
2. MDP 动作空间与阶段 1 的"动作空间"概念有何异同？何为 $\mathcal{A}(s)$？为何需要它？
3. MDP 的 $R(s,a)$ 与阶段 1 的奖励函数是什么关系？为何设计奖励要小心"奖励黑客"？

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
