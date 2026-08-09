---
type: project
project_type: homework
course: "强化学习"
title: "强化学习-课后作业-ActorCritic优势与GAE"
assignment_id: "RL-HW05"
assignment_level: lesson
assignment_format: exercise
stage_id: "06"
source_type: local_integration_task
accessed: "2026-08-07"
license: "[待验证]"
source: "本课程（强化学习）自编形成性练习；非任何名校官方作业，不冒充官方。"
created: 2026-08-07
status: ongoing
flow: project
tags: [作业, 强化学习, 课后作业, Actor-Critic, GAE, 优势]
requires:
  - "[[Actor-Critic架构]]"
  - "[[GAE广义优势估计]]"
  - "[[优势估计]]"
  - "[[🧭 强化学习-前置知识]]"
  - "[[Critic网络]]"
  - "[[TRPO信任域优化]]"
  - "[[优势估计]]"
  - "[[A3C算法]]"
  - "[[TRPO与PPO对比]]"
  - "[[Actor网络]]"
  - "[[TRPO简介]]"
  - "[[TRPO与PPO对比]]"
  - "[[GAE-Lambda1]]"
  - "[[GAE广义优势估计]]"
  - "[[A3C算法]]"
  - "[[Actor-Critic 与 PPO]]"
  - "[[TRPO信任域优化]]"
  - "[[A2C算法]]"
  - "[[优势函数]]"
  - "[[A2C算法]]"
  - "[[优势估计]]"
  - "[[Critic网络]]"
  - "[[PPOvsTRPO-实现]]"
  - "[[优势估计]]"
  - "[[GAE-单步]]"
  - "[[A2C算法]]"
  - "[[优势-估计]]"
  - "[[TRPO信任域优化]]"
  - "[[SAC软Actor-Critic]]"
  - "[[TRPO信任域优化]]"
  - "[[策略评估]]"
  - "[[GAE-公式]]"
  - "[[A3C算法]]"
  - "[[GAE-Lambda0]]"
  - "[[Critic网络]]"
  - "[[优势函数]]"
  - "[[优势估计]]"
  - "[[PPOvsTRPO-效果]]"
  - "[[Actor网络]]"
  - "[[A3C算法]]"
  - "[[Actor网络]]"
  - "[[TRPO与PPO对比]]"
  - "[[Critic网络]]"
  - "[[A2C算法]]"
  - "[[GAE-Lambda]]"
  - "[[A3C算法]]"
  - "[[TRPO信任域优化]]"
  - "[[GAE-Lambda95]]"
  - "[[Actor网络]]"
  - "[[TRPO与PPO对比]]"
  - "[[PPOvsTRPO-效率]]"
  - "[[PPOvsTRPO-约束]]"
  - "[[A2C算法]]"
  - "[[优势-方差]]"
---

# 强化学习-课后作业-ActorCritic优势与GAE

> 🎯 **作业目标**：把「策略梯度 + 值函数」合流为 Actor-Critic——手算优势函数 `A=Q−V`、A2C 的 actor/critic 更新、以及 GAE 的偏差—方差权衡，再用 ≤50 行实现 A2C 并与 REINFORCE 对比样本效率。对应阶段 6（Actor-Critic），是连接阶段 5（策略梯度）与阶段 7（PPO）的桥梁。

---

## 1. 身份与边界

- **身份**：强化学习课程课后作业（lesson 级），对应阶段 6（Actor-Critic）。
- **对应知识**：`[[Actor-Critic架构]]`、`[[GAE广义优势估计]]`、`[[优势估计]]`、`[[🧭 强化学习-前置知识]]`。
- **边界（允许 / 禁止）**：
  - ✅ 允许：纸笔推导 + 自写 A2C（actor + critic，numpy/torch）。
  - ❌ 禁止：直接调用 `sb3.A2C/PPO` 黑盒；禁止在 actor 损失里用 `Q` 而非 `A`（优势）导致尺度失衡。
  - ⚠️ 本题练**优势估计与双头更新**，不要求大规模调参。

---

## 2. 环境与最小依赖

- **环境**：纯 Python + `numpy`/`torch`。无需 gym。
- **单步 TD 骨架（题目内给出）**：

```python
import numpy as np

gamma, lam = 0.9, 0.95
S = 4
# 短轨迹 (s, a, r, done)：X->Y->Z(到达 D 终止，奖励 +10)
traj = [(0, 1, -1, False), (1, 0, -1, False), (2, 0, 10, True)]

V = np.zeros(S); pi = np.ones((S, 2)) / 2        # 表格 critic / actor

# 1) TD 误差 δ_t = r_t + γV(s_{t+1}) − V(s_t)
deltas = []
for (s, a, r, done) in traj:
    ns = min(s + 1, S - 1); v_next = 0.0 if done else V[ns]
    deltas.append(r + gamma * v_next - V[s])

# 2) GAE: A_t = Σ_{l≥0} (γλ)^l δ_{t+l}
A = np.zeros(len(traj))
for t in range(len(traj)):
    g, p = 0.0, 1.0
    for l in range(t, len(traj)):
        g += p * deltas[l]; p *= gamma * lam
    A[t] = g

# 3) A2C 更新（示意）
actor_grad = sum(A[t] * (np.eye(2)[a] - pi[s]) for (t, (s, a, _, _)) in enumerate(traj))
critic_grad = sum(A[t] * A[t] for t in range(len(traj)))
pi += 0.1 * actor_grad                        # actor 沿优势上升
V  += 0.1 * np.array([sum(A[t] for t, (s, _, _, _) in enumerate(traj) if s == s0)
                       for s0 in range(S)])   # critic 向优势回归
print("δ =", np.round(deltas, 3), " GAE A =", np.round(A, 3))
print("更新后 π[0] =", np.round(pi[0], 3))
```

---

## 3. 题目详述（自包含）

### Q1 — 优势函数手算
给定 `V(s)=2`，`Q(s,a1)=5`，`Q(s,a2)=1`。
- 计算 `A(s,a1)=Q(s,a1)−V(s)`、`A(s,a2)`；说明优势为何以 0 为中心，以及 actor 用 `A` 而非 `Q` 的好处（尺度无关、只关心「相对好坏」）。

### Q2 — A2C 更新手算
给定 `V(s)=2`, `r=1`, `γ=0.9`, `V(s')=3`, actor 在 `(s,a)` 的对数概率 `log π=−0.5`。
- (a) 算 TD 目标 `r + γ·V(s')` 与 TD 误差 `δ = 3.7 − 2 = 1.7`。
- (b) critic 损失 = `δ²`（或 `0.5·δ²`）；actor 梯度 ∝ `−log π · A`，取 `A=δ`。手算 actor 更新方向（应增大 `log π`，即 `+0.5·1.7=+0.85` 方向），解释符号。

### Q3 — GAE 加权手算
给定三步 TD 误差 `δ_0=1.0, δ_1=0.5, δ_2=−0.2`，`γ=0.9, λ=0.9`。
- 算 `A_0^{GAE} = δ_0 + (γλ)·δ_1 + (γλ)²·δ_2`，展示数值。
- 解释：`λ→0` 退化为单步 TD 优势（低方差、高偏差）；`λ→1` 趋近蒙特卡洛回报（低偏差、高方差）。

### Q4 — 最小实现
用 ≤50 行实现 A2C（actor + critic 两网络，可共享底层）：
- 优势取单步 TD 误差（或 GAE）；在离散 CartPole 上训练，报告学习曲线。
- 对比阶段 5 的 REINFORCE：A2C 通常**每步即更新、样本效率更高**。

---

## 4. 提交产物

- 代码：`rl_hw05_ac.py` 或 notebook（含 Q1–Q3 手算对照）。
- 说明：`README` ≤150 字，给出 Q1 的 `A`、Q2 的 `δ` 与 actor 方向、Q3 的 `A_0`，以及 Q4 与 REINFORCE 的样本效率对比。

---

## 5. 评分 Rubric（满分 100）

| 维度 | 分值 | 标准 |
| :--- | :---: | :--- |
| 优势函数（Q1） | 20 | `A` 数值正确；0 中心解释正确 |
| A2C 更新（Q2） | 30 | TD 误差与 actor 方向数值正确、符号解释对 |
| GAE（Q3） | 25 | `A_0` 数值正确；偏差—方差权衡解释正确 |
| 最小实现（Q4） | 20 | A2C 正确；样本效率优于 REINFORCE |
| 代码与说明 | 5 | 简洁、可复现 |

---

## 6. 基础要求、必要提示与常见错误

- **必要提示**：优势 `A(s,a)=Q(s,a)−V(s)` 必须同一 `(s,a)`；终止态 `s'` 的 `V(s')=0` 不进入 bootstrap；GAE 从后向前递推 `A_t = δ_t + γλ·A_{t+1}`。
- **常见错误**：① actor 损失误用 `Q` 而非 `A`，导致梯度尺度被绝对价值带偏；② 终止时仍 `V(s')` bootstrap（应置 0）；③ critic 用整条回报而非 TD 误差训练（失去 online 优势）；④ 符号搞反：policy 是最大化，`loss=−logπ·A` 再下降；⑤ GAE 的 `γ` 与更新用的 `γ` 不一致。
- **本地断言（Q2 速验）**：

```python
V_s, r, gamma, V_sp, logpi = 2.0, 1.0, 0.9, 3.0, -0.5
delta = r + gamma * V_sp - V_s          # 1.0 + 0.9*3 - 2 = 1.7
actor_dir = -logpi * delta              # -(-0.5)*1.7 = +0.85  (增大 logπ)
assert abs(delta - 1.7) < 1e-9 and abs(actor_dir - 0.85) < 1e-9
```

---

## 7. 可选进阶任务（非主任务前置）

- 实现 **GAE** 版 A2C（替代单步 TD 优势），对比学习稳定性。
- 把 actor/critic 底层共享网络，观察表征复用收益。
- 与 `[[强化学习-阶段作业-HW02-DQN与PPO连续动作控制|阶段作业 HW02]]` 的 PPO 对照，说明 A2C→PPO 的改进点（截断、多 epoch）。

---

## 8. 自检清单

- [ ] Q1 `A(s,a1)=3, A(s,a2)=−1`
- [ ] Q2 `δ=1.7`，actor 方向 `+0.85`（增大 logπ）
- [ ] Q3 `A_0` 数值正确，且能解释 λ 的偏差—方差权衡
- [ ] Q4 A2C 样本效率优于 REINFORCE；未用 sb3 黑盒

---

## 9. 来源与后续入口

- **来源**：本作业为**课程自编形成性练习**（`source_type: local_integration_task`），非单一官方作业；题面与验收由本课程独立制定，参考 Sutton & Barto §13.5 与阶段 6 知识卡，未冒充官方作业。
- **后续入口**：完成本作业即走完「基础→MDP→值函数→Q-Learning→策略梯度→Actor-Critic」全范式；下一步进入 `[[强化学习-阶段作业-HW02-DQN与PPO连续动作控制|阶段作业 HW02：DQN 与 PPO]]`（阶段 7）或 `[[强化学习-大作业-从表格Q学习到深度策略梯度|大作业：从表格 Q 到深度策略梯度]]`。
- **复习卡**：`[[Actor-Critic架构]]`、`[[GAE广义优势估计]]`、`[[优势估计]]`。

---

## 🃏 知识内化卡片

- Q：Actor-Critic 与 REINFORCE 的核心区别？
- A：REINFORCE 用整条轨迹回报 `G_t` 当基线减后的「信用」；Actor-Critic 用一个**可学习的 critic `V(s)`** 估计优势 `A≈δ`，**每步即可更新**，方差更低、样本效率更高。
- Q：优势 `A=Q−V` 为何比直接用 `Q` 好？
- A：`A` 以 0 为中心，只表达「该动作相对平均水平的优劣」，消除状态绝对价值的尺度影响，梯度更稳定；且 `E_a[A]=0` 自带基线效果。
- Q：GAE 的 `λ` 控制什么？
- A：`A_t^{GAE}=Σ_l (γλ)^l δ_{t+l}`。`λ→0` 用单步 TD 优势（低方差、高偏差）；`λ→1` 趋近 Monte Carlo（低偏差、高方差）；`λ` 在二者间折中。


## 来源声明（诚实标注）

本作业 `source_type: local_integration_task`，为**本课程（强化学习）自编形成性练习**。
- 诚实说明：非任何名校官方作业，不冒充官方题面；题面与验收由本课程独立制定。
- 许可：[待验证]；访问日期 2026-08-07。
