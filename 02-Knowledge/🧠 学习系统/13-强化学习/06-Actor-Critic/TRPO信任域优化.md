---
title: "TRPO 信任域策略优化"
type: study
topic: "TRPO 信任域优化"
course: "强化学习"
created: 2026-08-07
status: learning
stage_moc: "[[🧭 阶段6-Actor-Critic]]"
flow: knowledge
kind: concept
upstream: ["[[Actor-Critic架构]]", "[[策略梯度]]", "[[优势估计]]", "[[TRPO与PPO对比]]"]
tags: [学习, 强化学习, TRPO, 信任域, 策略优化]
---
> 所属模块：[[🗺️ 强化学习学习路径|强化学习学习路径]]
> 主教材：`《Reinforcement Learning》`
> 对应阶段：[[🧭 阶段6-Actor-Critic|返回阶段页]]

# TRPO 信任域策略优化 (Trust Region Policy Optimization)

---

## 0. 学习边界

- **类别**：**A 类（核心概念，必须深挖）**
- **判断理由**：TRPO 是"限制单步策略变化以保稳定"的理论化代表，是 PPO 的直接祖先；理解信任域、KL 约束、共轭梯度与单调改进，才能看懂 PPO 为何用裁剪近似它。

---

## 1. TRPO 家族谱系

TRPO 是一族"信任域策略优化"方法的代表，理解谱系有助于衔接 PPO。

> 自然梯度(NPG) → TRPO(约束优化+CG) → PPO(clip 近似)

共同点：限制单步策略变化、用优势做更新。

**谱系要点**：原版 TRPO（CG+线搜）、PPO-Clip（裁剪替代约束）、PPO-Penalty（KL 惩罚）。同一任务可先试 TRPO，再换 PPO（实现更简单、效果相近）。

- **与 PPO 对比**：PPO 用裁剪目标近似 KL 约束，省去 CG/线搜。
- **常见错误**：把 TRPO 与 PPO 当完全不同路线——PPO 是 TRPO 的实用近似。

---

## 2. 信任域：把更新限制在"策略变化不大"的范围内

普通 PG 步长难设、易崩。TRPO 把更新限制在"策略分布变化不大"的信任域内，稳定改进。

> 每步在 $\mathrm{KL}(\pi_\theta\|\pi_{\theta+\Delta})\le\delta$ 的约束下，最大化带重要性权重的优势目标。

更新前算新旧策略 KL，若超阈值 $\delta$ 就缩小步长，避免策略剧变（呼应 [[REINFORCE-不稳定]]）。

- **与 NPG 对比**：TRPO 用约束近似 NPG 的自然梯度，避免求大 Fisher 逆。
- **常见错误**：把 TRPO 当无约束二阶——KL 约束正是其稳定关键。

---

## 3. KL 约束：用什么度量"策略变化大小"

信任域用策略间的 KL 散度度量"策略变化大小"。

$$\mathrm{KL}\big(\pi_{\theta_{old}}(\cdot|s)\,\|\,\pi_{\theta_{new}}(\cdot|s)\big)\le\delta\quad(\text{对每个 }s\text{ 或对状态平均})$$

KL 衡量"动作分布"偏移程度，比参数 $\Delta\theta$ 更贴合策略实际变化。

**最小手算例子（离散）**：$p=[0.5,0.5],\ q=[0.8,0.2]$，则
$\mathrm{KL}(p\|q)=0.5\ln(0.5/0.8)+0.5\ln(0.5/0.2)\approx 0.223$ nat。TRPO 约束 $\mathrm{KL}(\pi_{new}\|\pi_{old})\le\delta$，$\delta$ 常取 0.01。

- **常见错误**：用 $L_2(\Delta\theta)$ 当信任域——参数距离不等于策略分布距离。

---

## 4. 共轭梯度解自然梯度（TRPO-CG）

TRPO 需解"带 KL 约束的自然梯度"——用共轭梯度（CG）近似，避免显式求大 Fisher 逆。

> 用 CG 解 $F x=g$（$F$ 为 Fisher 矩阵，$g$ 为策略梯度），得自然梯度方向；再线搜满足 KL$\le\delta$ 的步长。$F$ 用 Hessian-vector product 近似，不显式构造矩阵。

**最小手算例子**：CG 解 $Ax=b$：$A=\begin{bmatrix}2&1\\1&2\end{bmatrix},\ b=[3,3]$，精确解 $x=[1,1]$（验证 $A\cdot[1,1]=[3,3]$）。CG 用步长 $\alpha=(r\cdot r)/(p\cdot Ap)$ 沿共轭方向迭代，$k$ 维问题至多 $k$ 步收敛。

- **与 NPG 对比**：NGP 显式 $F^{-1}$；TRPO 用 CG 近似，省内存更可行。
- **常见错误**：以为 TRPO 直接求 $F^{-1}$——它刻意避免以省开销。

---

## 5. 单调改进保证

TRPO 的理论底气：在信任域内更新能保证"性能单调不降"（近似）。

> 单调改进定理：若 KL 约束满足，则 $J(\theta_{new})\ge J(\theta_{old})-\text{常数}\cdot\mathrm{KL}$，保证每步不大幅变差。

**手算例子**：若 $\mathrm{KL}(\pi_{new}\|\pi_{old})\le\delta$，则 $\eta(\pi_{new})\ge\eta(\pi_{old})-C\cdot\delta^2$（带下界）。取 $\delta=0.01$ ⇒ 每步性能下降有上限，迭代近似单调上升。

- **与 REINFORCE 不稳定对比**：单调保证从机制上避免崩溃。
- **常见错误**：把"单调"当"每步必涨"——它保证不显著变差，非保证必涨。

---

## 6. 合并要点

| 维度 | 要点 |
| :--- | :--- |
| 谱系 | NPG → TRPO → PPO |
| 约束 | KL$\le\delta$，度量分布而非参数距离 |
| 求解 | CG + 线搜，避免 $F^{-1}$ |
| 保证 | 单调改进（不显著变差） |

---

## 闭卷自测
1. TRPO 家族包含哪些方法？TRPO 与 PPO 的关系？
2. TRPO 的"信任域"是什么？相对普通 PG 解决什么？
3. TRPO 用什么约束策略变化？为何用 KL 而非参数距离？
4. TRPO 用什么求自然梯度？为何避免显式 $F^{-1}$？
5. TRPO 的单调改进保证是什么？为何能避免崩溃？

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
