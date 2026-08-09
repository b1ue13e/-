---
type: project
project_type: homework
course: "强化学习"
title: "强化学习-课后作业-策略梯度REINFORCE"
assignment_id: "RL-HW04"
assignment_level: lesson
assignment_format: exercise
stage_id: "05"
source_type: local_integration_task
accessed: "2026-08-07"
license: "[待验证]"
source: "本课程（强化学习）自编形成性练习；非任何名校官方作业，不冒充官方。"
created: 2026-08-07
status: ongoing
flow: project
tags: [作业, 强化学习, 课后作业, 策略梯度, REINFORCE]
requires:
  - "[[策略梯度定理与REINFORCE]]"
  - "[[基线-自适应]]"
  - "[[🧭 强化学习-前置知识]]"
  - "[[TRPO信任域优化]]"
  - "[[优势估计]]"
  - "[[PG-梯度]]"
  - "[[TRPO与PPO对比]]"
  - "[[Actor网络]]"
  - "[[TRPO简介]]"
  - "[[TRPO与PPO对比]]"
  - "[[REINFORCE-不稳定]]"
  - "[[REINFORCE-回报]]"
  - "[[GAE广义优势估计]]"
  - "[[参数化-神经网络]]"
  - "[[演进-随机策略]]"
  - "[[TRPO信任域优化]]"
  - "[[AC简介]]"
  - "[[优势函数]]"
  - "[[演进-端到端]]"
  - "[[基线-常数]]"
  - "[[折扣-回报]]"
  - "[[优势估计]]"
  - "[[Critic网络]]"
  - "[[PPOvsTRPO-实现]]"
  - "[[优势估计]]"
  - "[[参数化-连续]]"
  - "[[优势-估计]]"
  - "[[TRPO信任域优化]]"
  - "[[SAC软Actor-Critic]]"
  - "[[PG-似然比]]"
  - "[[TRPO信任域优化]]"
  - "[[优势估计]]"
  - "[[REINFORCE-高方差]]"
  - "[[折扣-Gamma]]"
  - "[[PG-目标函数]]"
  - "[[优势函数]]"
  - "[[优势估计]]"
  - "[[PPOvsTRPO-效果]]"
  - "[[Actor-Critic架构]]"
  - "[[Actor网络]]"
  - "[[参数化-可微]]"
  - "[[Actor网络]]"
  - "[[TRPO与PPO对比]]"
  - "[[折扣-修正]]"
  - "[[策略-参数化]]"
  - "[[REINFORCE-更新]]"
  - "[[PolicyGradient策略梯度]]"
  - "[[REINFORCE-信用]]"
  - "[[基线-状态价值]]"
  - "[[REINFORCE-无偏]]"
  - "[[TRPO信任域优化]]"
  - "[[REINFORCE-Baseline]]"
  - "[[演进-连续优化]]"
  - "[[REINFORCE-MC]]"
  - "[[演进-连续动作]]"
  - "[[Actor网络]]"
  - "[[PG-直观]]"
  - "[[MDP-折扣因子]]"
  - "[[TRPO与PPO对比]]"
  - "[[DDPG深度确定性策略梯度(DDPG)]]"
  - "[[PPOvsTRPO-效率]]"
  - "[[PPOvsTRPO-约束]]"
  - "[[优势-方差]]"
  - "[[参数化-离散]]"
  - "[[NPG]]"

---

# 强化学习-课后作业-策略梯度REINFORCE

> 🎯 **作业目标**：把策略梯度定理从公式落到实处——手算 softmax 策略的梯度方向，推导 REINFORCE 与 baseline 的方差缩减原理，再用 ≤40 行实现 REINFORCE（带/不带 baseline）对比回报方差。对应阶段 5（策略梯度），是「直接对策略参数求导」范式的第一份动手练习。

---

## 1. 身份与边界

- **身份**：强化学习课程课后作业（lesson 级），对应阶段 5（策略梯度）。
- **对应知识**：`[[策略梯度定理与REINFORCE]]`、`[[基线-自适应]]`、`[[🧭 强化学习-前置知识]]`。
- **边界（允许 / 禁止）**：
  - ✅ 允许：纸笔推导 + 自写短视界 REINFORCE（numpy/torch 均可）。
  - ❌ 禁止：直接调用 `sb3.PPO/A2C` 等黑盒完成核心；禁止在 baseline 里引入依赖动作 `a` 的项（会引入偏差）。
  - ⚠️ 本题练**梯度方向与方差**，不要求大规模调参。

---

## 2. 环境与最小依赖

- **环境**：纯 Python + `numpy`（手算用），或 `torch`（实现用）。无需 gym。
- **单步 MDP（bandit）骨架（题目内给出）**：

```python
import numpy as np

r_true = np.array([1.0, 0.0])      # 2 臂真实奖励
theta = np.zeros(2); alpha = 0.1; baseline = 0.0

def softmax(t):
    e = np.exp(t - t.max()); return e / e.sum()   # 减 max 防溢出

for ep in range(1000):
    pi = softmax(theta)
    a = np.random.choice(2, p=pi)                 # 按策略采样一臂
    G = r_true[a] + np.random.normal(0, 0.01)     # 带噪声回报（单步轨迹）
    baseline = 0.9 * baseline + 0.1 * G           # 自适应基线 b←0.9b+0.1G
    grad = (G - baseline) * (np.eye(2)[a] - pi)   # (G-b)·∇log π
    theta += alpha * grad                         # REINFORCE 上升
print("学到 π =", np.round(softmax(theta), 3), "（应趋近 [1,0]）")
# 进阶：把 baseline 改成常数 0，对比方差；或换成多步轨迹 REINFORCE。
```

---

## 3. 题目详述（自包含）

### Q1 — 策略梯度方向手算
- 设 `θ=[0,0]`（均匀策略 `π=[0.5,0.5]`），奖励 `r=[1,0]`。策略梯度
  `∇_θ J(θ) = Σ_a π_a · ∇_θ log π_a · r_a`，其中 `∂log π_i / ∂θ_j = (1{i=j} − π_j)`。
- 手算 `∇_θ J`（两个分量），并说明梯度把概率推向哪个动作。

### Q2 — REINFORCE 与 baseline 方差缩减
- (a) 写出带 baseline 的 REINFORCE 梯度估计
  `g = ∇_θ log π(a_t|s_t) · (G_t − b)`；说明为何 `b`（不依赖动作 `a`）不改变梯度期望、但能减方差。
- (b) 给定两条轨迹回报 `G=[10, 2]`，对应 `∇logπ` 相同为 `d`。分别用 `b=0` 与 `b=6`（=均值）算梯度项，展示「居中」后方差下降（从 `[10d, 2d]` 变为 `[4d, −4d]`，均值同为 `12d` 不变）。

### Q3 — 最小实现
用 ≤40 行实现 REINFORCE（短视界环境，如离散 CartPole 小回合或 2 状态 bandit 序列）：
- 版本 A：无 baseline（`G_t` 直接）；版本 B：减去状态/回合均值 baseline `b`。
- 跑 ≥5 个随机种子，报告**回报的均值±标准差**，证明 B 的方差更低。
- 评测：两版最终均值相近，但 B 的 std 明显更小（方差缩减）。

---

## 4. 提交产物

- 代码：`rl_hw04_pg.py` 或 notebook（含 Q1 手算对照）。
- 说明：`README` ≤150 字，给出 Q1 的 `∇_θ J`、Q2(b) 两种基线下的梯度项、Q3 的均值±std 对比。

---

## 5. 评分 Rubric（满分 100）

| 维度 | 分值 | 标准 |
| :--- | :---: | :--- |
| 策略梯度手算（Q1） | 30 | 两个分量数值正确；方向解释正确 |
| baseline 推导（Q2） | 30 | 公式正确；居中方差缩减数值正确 |
| 最小实现（Q3） | 30 | REINFORCE 正确；baseline 版 std 更低 |
| 代码与说明 | 10 | 简洁、可复现、README 清晰 |

---

## 6. 基础要求、必要提示与常见错误

- **必要提示**：REINFORCE 用**折扣回报** `G_t = Σ_{k≥t} γ^{k−t} r_k`（不是单步奖励）；baseline 可依赖状态 `s_t` 但**绝不能依赖动作** `a_t`，否则 `E[∇logπ·b] ≠ 0` 引入偏差。
- **常见错误**：① 把 baseline 写成依赖 `a` 的函数（偏差）；② 用 `r_t` 而非 `G_t` 当回报；③ 漏掉折扣 `γ`；④ 高斯策略里 log-prob 错写成 `(a−μ)/σ` 而非 `−(a−μ)²/(2σ²)`；⑤ 梯度上升却把 loss 符号搞反（policy gradient 是**最大化** J，实现时常用 `loss = −logπ·A` 再 SDG 下降）。
- **本地断言（Q1 速验）**：

```python
import numpy as np
theta = np.array([0., 0.]); r = np.array([1., 0.])
pi = np.exp(theta) / np.exp(theta).sum()
grad = sum(pi[a] * (np.eye(2)[a] - pi) * r[a] for a in range(2))
assert np.allclose(grad, np.array([0.25, -0.25])), grad   # 推向 action 0
```

---

## 7. 可选进阶任务（非主任务前置）

- 实现**自适应基线** `b ← β·b + (1−β)·G`（指数滑动平均），对比固定均值基线。
- 换成高斯连续策略，验证 `∇_θ log π` 含 `(a−μ)/σ²` 项。
- 对比 REINFORCE 与阶段 4 的 Q-Learning 在离散任务上的样本效率。

---

## 8. 自检清单

- [ ] Q1 梯度 = `[0.25, −0.25]`，方向指向高奖励臂
- [ ] Q2(b) 两种基线梯度项均值相同、居中后方差下降
- [ ] Q3 带 baseline 版 std 明显更小
- [ ] 未调用 sb3 黑盒；baseline 不依赖动作

---

## 9. 来源与后续入口

- **来源**：本作业为**课程自编形成性练习**（`source_type: local_integration_task`），非单一官方作业；题面与验收由本课程独立制定，参考 Sutton & Barto §13 与阶段 5 知识卡，未冒充官方作业。
- **后续入口**：完成后进入 `[[强化学习-课后作业-ActorCritic优势与GAE|课后作业 RL05：Actor-Critic 优势与 GAE]]`（阶段 6），把「策略梯度 + 值函数」合流为 actor-critic。
- **复习卡**：`[[策略梯度定理与REINFORCE]]`、`[[基线-自适应]]`。

---

## 🃏 知识内化卡片

- Q：策略梯度定理的核心形式？
- A：`∇_θ J(θ) = E_{τ∼π_θ}[ Σ_t ∇_θ log π_θ(a_t|s_t) · G_t ]`——对轨迹中每步的对数概率乘其回报求期望，沿此方向提升参数即提升期望回报。
- Q：baseline 为何不减期望却减方差？
- A：对任意不依赖 `a_t` 的 `b(s_t)`，有 `E[∇logπ(a_t|s_t)·b] = 0`（因 `E_a[∇logπ]=0`），故梯度期望不变；但 `G_t` 减去常数 `b` 后中心化，单次估计的方差下降。
- Q：REINFORCE 与 Q-Learning 的根本区别？
- A：REINFORCE 直接对**策略参数**求导（policy-based），可处理连续/随机策略；Q-Learning 学**动作值**再贪心出策略（value-based）。前者高方差、后者有偏（max 引入）。


## 来源声明（诚实标注）

本作业 `source_type: local_integration_task`，为**本课程（强化学习）自编形成性练习**。
- 诚实说明：非任何名校官方作业，不冒充官方题面；题面与验收由本课程独立制定。
- 许可：[待验证]；访问日期 2026-08-07。
