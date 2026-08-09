---
title: "Critic 网络（价值网络）"
type: study
topic: "Critic 网络"
course: "强化学习"
created: 2026-08-07
status: learning
stage_moc: "[[🧭 阶段6-Actor-Critic]]"
flow: knowledge
kind: concept
upstream: ["[[Actor-Critic架构]]", "[[V函数（状态价值函数）]]", "[[优势估计]]"]
tags: [学习, 强化学习, Actor-Critic, 价值网络]
---
> 所属模块：[[🗺️ 强化学习学习路径|强化学习学习路径]]
> 主教材：`《Reinforcement Learning》`
> 对应阶段：[[🧭 阶段6-Actor-Critic|返回阶段页]]

# Critic 网络 (Critic Network / 价值网络)

---

## 0. 学习边界

- **类别**：**A 类（核心概念，必须深挖）**
- **判断理由**：Critic 提供"状态相关基线/优势"，是 Actor-Critic 把 REINFORCE 的方差降下来的关键；不理解它的结构、目标与更新，就看不懂 AC 损失里的 MSE 项与优势信号来源。

---

## 1. Critic 的职责

Critic 是"评论家"：估计价值函数，给 Actor 提供低方差的优势信号。

$$\text{Critic 近似 } V_\phi(s)\ (\text{或 } Q)\text{ 作为基线/优势：}\quad A(s,a)\approx r+\gamma V_\phi(s')-V_\phi(s)$$

它把"回报"换成"一步自举优势"，降低 Actor 更新方差。

- **与 Actor 的区别**：Critic 不直接出动作，只评价值。
- **常见错误**：把 Critic 当"真值"——$V_\phi$ 是估计，有误差，故优势有偏。

---

## 2. Critic 的网络结构

Critic 通常也是神经网络：输入状态、输出标量价值 $V$。

- $V_\phi(s)\in\mathbb{R}$，一个回归头；也可估 $Q$（QAC 用 $Q$，见第 5 节）。
- 结构常比 Actor 简单（只需标量输出）。

**最小手算例子**：CartPole 中 Critic 为 MLP，输入 4 维状态，输出 1 个 $V$ 值。

- **常见错误**：让 Critic 输出"动作维度"却当 $V$ 用——需明确是 $V$ 还是 $Q$。

---

## 3. Critic 的损失与更新

Critic 自身也要训练——用 TD 误差最小化价值预测误差：

$$L(\phi)=\mathbb{E}\big[(V_\phi(s)-y)^2\big],\qquad y=r+\gamma V_\phi(s')\ (\text{bootstrap 目标})$$
$$\phi \leftarrow \phi - \beta \nabla_\phi L(\phi)$$

即 Critic 用 TD(0) 回归训练（见 [[TD-误差]]、[[值迭代]]）。

**最小手算例子**：$(s,r,s')=(s,+1,s'),\ V(s)=0.4,\ V(s')=0.5,\ \gamma=0.9$：$y=1+0.9\times 0.5=1.45$；Critic 朝 $y$ 把 $V(s)$ 由 $0.4$ 调向更靠近 $1.45$。

- **与 Actor 更新的本质不同**：Critic 做监督回归（MSE），Actor 做策略梯度（似然比）。
- **常见错误**：用 Actor 的 $\nabla\log\pi$ 更新 Critic——Critic 用自己的 MSE 梯度。

---

## 4. Critic 的核心产物：优势

Critic 把轨迹信息压缩成每步优势，喂给 Actor：

- 一步优势：$A(s,a)\approx r+\gamma V(s')-V(s)$（Critic 的 TD 误差 $\delta$）。
- 多步/GAE 形式见 [[优势估计]]。

**最小手算例子**：Critic 估 $V$ 或 $Q$。离散例：$V=0.5$，两动作 $Q=[0.7,0.3]$ ⇒ $A=[+0.2,-0.2]$（相对平均的优劣方向）。

- **与固定基线对比**：Critic 提供"状态相关"基线，比常数更优（见 [[基线-状态价值]]）。
- **常见错误**：把 Critic 输出的 $V$ 直接当优势——需做 $A=\dots-V$ 的差值。

---

## 5. Q-Critic 变体（QAC）

多数 AC 用 V-Critic；也可用 Q-Critic：Critic 估 $Q_\phi(s,a)$，优势 $A=Q_\phi(s,a)-V_\phi(s)$ 或仅用 $Q$。

- 离散动作：Critic 输出 $|A|$ 个 $Q$；离散例：$A(a_1)=Q(a_1)-\text{mean}(Q)$。
- 连续动作下 Q-Critic 难（需 $\max_a Q$ 或积分），故 V-Critic 更常见。

- **与 V-Critic 对比**：Q-Critic 直接给动作价值但连续动作不便；V-Critic 更通用。
- **常见错误**：连续动作硬上 Q-Critic——需处理 $\max_a Q$，回到回归值方法的老问题。

---

## 6. 合并手算示例

$(s,a,r,s')=(s,a_1,+1,s'),\ V(s)=0.4,\ V(s')=0.5,\ \gamma=0.9$：

1. Critic 一步优势（TD 误差）：$A=r+\gamma V(s')-V(s)=1+0.45-0.4=1.05$。
2. Critic 回归目标：$y=1.45$，把 $V(s)$ 朝 $1.45$ 调。
3. Actor 用 $A=1.05$ 提升 $\pi(a_1|s)$。

---

## 闭卷自测
1. Critic 在 AC 中负责什么？它如何帮 Actor 降方差？
2. Critic 网络输入/输出分别是什么？V-Critic 与 Q-Critic 结构差异？
3. 写出 Critic 的损失与更新式，并说明与 Actor 更新的本质区别。
4. 为何不能把 Critic 输出的 $V$ 直接当优势？

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
