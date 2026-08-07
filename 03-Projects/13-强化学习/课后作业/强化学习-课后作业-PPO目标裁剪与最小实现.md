---
type: project
project_type: homework
course: "强化学习"
title: "强化学习-课后作业-PPO目标裁剪与最小实现"
assignment_id: "RL-HW07"
assignment_level: lesson
assignment_format: exercise
stage_id: "07"
requires:
  - "[[PPO近端策略优化]]"
  - "[[PPOClip-目标]]"
  - "[[GAE广义优势估计]]"
  - "[[优势-符号]]"
  - "[[IS-比率]]"
  - "[[Actor-Critic架构]]"
  - "[[🧭 强化学习-前置知识]]"
source_type: local_integration_task
created: 2026-08-07
status: ongoing
flow: project
tags: [作业, 强化学习, 课后作业, PPO, PPO-Clip, 重要性采样]
---

# 强化学习-课后作业-PPO目标裁剪与最小实现

> 🎯 **作业目标**：手算 PPO-Clip 的重要性采样比率 `r(θ)` 与裁剪目标 `L^CLIP`，弄清「裁剪为何能限制步长」，再用 ≤50 行实现 PPO-Clip 单步更新，并与阶段 6 的 A2C 对比。对应阶段 7（PPO），是课程压轴，串接 `[[强化学习-课后作业-ActorCritic优势与GAE|RL-HW05]]` 的 GAE 优势。

---

## 1. 身份与边界

- **身份**：强化学习课程课后作业（lesson 级），对应阶段 7（PPO）。
- **对应知识**：`[[PPO近端策略优化]]`、`[[PPOClip-目标]]`、`[[GAE广义优势估计]]`、`[[优势-符号]]`、`[[IS-比率]]`、`[[Actor-Critic架构]]`、`[[🧭 强化学习-前置知识]]`。
- **边界（允许 / 禁止）**：
  - ✅ 允许：纸笔推导比率 / 裁剪 + 自写 PPO-Clip（numpy/torch）。
  - ❌ 禁止：直接调用 `sb3.PPO` 黑盒；禁止把 ratio 写成 `π_old/π_new`（方向反）。
  - ⚠️ 本题练**裁剪目标的构造与步长限制**，不要求大规模调参。

---

## 2. 环境与最小依赖

- **环境**：纯 Python + `numpy`/`torch`。无需 gym。
- **单步 PPO-Clip 骨架（题目内给出）**：

```python
import numpy as np
np.set_printoptions(suppress=True, precision=3)

gamma, eps = 0.9, 0.2
# 迷你轨迹 (s, a, r, done)；s' 由 s+1 给出，终止态 V(s')=0
traj = [(0, 0, -1.0, False), (1, 0, 10.0, True)]
V = np.zeros(3)                                  # 表格 critic（给定）
logits = {0: np.array([0.0, 0.0]), 1: np.array([0.0, 0.0])}  # 2 动作 softmax

def soft(z):
    z = z - z.max(); e = np.exp(z); return e / e.sum()
def logp(z, a):
    return np.log(soft(z)[a])

# 1) TD 优势 A_t = r + gamma*V(s') - V(s)
A = np.array([r + gamma * (0.0 if d else V[min(s + 1, 2)]) - V[s]
              for (s, a, r, d) in traj])
print("TD 优势 A =", np.round(A, 3))

# 2) PPO-Clip 单步更新（不同学习率展示裁剪是否生效）
for lr in [0.5, 2.0]:
    new = {s: logits[s].copy() for s in logits}
    L_clip = L_plain = 0.0
    for i, (s, a, r, d) in enumerate(traj):
        new[s][a] += lr * A[i]                    # 沿 +A 提升该动作
        rold = logp(logits[s], a)
        rnew = logp(new[s], a)
        ratio = np.exp(rnew - rold)
        unclip = ratio * A[i]
        clipped = np.clip(ratio, 1 - eps, 1 + eps) * A[i]
        L_clip += min(unclip, clipped)
        L_plain += unclip
    p0 = soft(new[0])
    print(f"lr={lr}: 更新后 π[0]={np.round(p0, 3)}  L^CLIP={L_clip:.3f}  (无裁剪={L_plain:.3f})")
```

---

## 3. 题目详述（自包含）

### Q1 — 比率 r(θ) 手算
给定旧策略 `π_old(a|s)=[0.5, 0.5]`，新策略在已采取动作 `a1` 上 `π_new(a1|s)=0.8`（另一动作 0.2）。
- 计算 `r = π_new(a1)/π_old(a1) = 0.8/0.5 = 1.6`；说明 `r>1` 表示新策略比旧策略更「自信」于该动作。

### Q2 — 裁剪目标 L^CLIP 手算
取 `ε=0.2`，优势 `A=+0.5`。
- 算 `clip(r, 1−ε, 1+ε) = clip(1.6, 0.8, 1.2) = 1.2`。
- 未裁剪项 `r·A = 1.6·0.5 = 0.8`；裁剪项 `1.2·0.5 = 0.6`；`L^CLIP = min(0.8, 0.6) = 0.6 < 0.8`。
- 解释：当优势为正且 `r` 过大时，裁剪把目标「封顶」在 0.6，**限制单步更新幅度**（防止策略跑太快）。
- （选）若 `A=−0.5`：未裁剪 `= −0.8`，裁剪项 `= −0.6`，`min = −0.8` —— 此时裁剪不提供下限，说明 PPO 对「降低坏动作概率」一侧不封底（已知特性）。

### Q3 — 最小实现
用 ≤50 行实现 PPO-Clip 单步更新（softmax 策略 + TD/GAE 优势），在给定迷你轨迹上：
- 打印 TD 优势 `A`、更新后 `π[0]`、以及 `L^CLIP` 与「无裁剪」目标之差，验证裁剪确实把目标从 ~19 降到 11.2。

---

## 4. 提交产物

- 代码：`rl_hw07_ppo.py` 或 notebook（含 Q1–Q2 手算对照）。
- 说明：`README` ≤150 字，给出 Q1 的 `r`、Q2 的 `L^CLIP`、Q3 的 `A` 与裁剪前后目标差，以及与 A2C 的区别。

---

## 5. 评分 Rubric（满分 100）

| 维度 | 分值 | 标准 |
| :--- | :---: | :--- |
| 比率 r（Q1） | 20 | `r` 数值正确；方向解释对 |
| 裁剪 L^CLIP（Q2） | 35 | `clip` 值、`min` 值正确；封顶解释正确 |
| 最小实现（Q3） | 30 | PPO-Clip 正确；打印 `A`/`L^CLIP`；裁剪前后差正确 |
| 对比 A2C | 10 | 说明 PPO 多 epoch + 裁剪 vs A2C 单步 |
| 代码与说明 | 5 | 简洁、可复现 |

---

## 6. 基础要求、必要提示与常见错误

- **必要提示**：ratio 必为 `π_new/π_old`（不是反过来）；裁剪区间对称 `[1−ε, 1+ε]`；`L^CLIP` 对每步取 `min` 再求平均 / 和。
- **常见错误**：① ratio 方向反（写成 `π_old/π_new`）→ 梯度符号错；② 只对正优势裁剪、负优势不处理（标准实现直接 `clip(r,·)` 即可，无需按 `A` 符号分支）；③ 用整条回报 `G` 当 `A` 却不减基线 / 不做 GAE，方差爆炸；④ 把 `ε` 当学习率；⑤ 多 epoch 时用同一批旧概率却忘了每 epoch 用当前 `θ` 重算 `π_new`（应实时算 `r`）。
- **本地断言（Q2 速验）**：

```python
import numpy as np
eps, r, A = 0.2, 1.6, 0.5
L_unc = r * A
L_clip = min(r * A, np.clip(r, 1 - eps, 1 + eps) * A)
assert abs(L_clip - 0.6) < 1e-9 and abs(L_unc - 0.8) < 1e-9
```

---

## 7. 可选进阶任务（非主任务前置）

- 用 GAE（接 `[[强化学习-课后作业-ActorCritic优势与GAE|RL-HW05]]`）替换单步 TD 优势，观察 PPO 更稳定。
- 实现多 epoch：同一批数据反复跑 `K` 次小更新，每 epoch 用当前 `θ` 重算 `ratio`。
- 与 `[[强化学习-阶段作业-HW02-DQN与PPO连续动作控制|阶段作业 HW02]]` 的官方 PPO 对照，说明连续动作下如何用高斯策略算 `logp`。

---

## 8. 自检清单

- [ ] Q1 `r = 1.6`
- [ ] Q2 `clip = 1.2`，`L^CLIP = 0.6`（`< 0.8`）
- [ ] Q3 `A = [-1, 10]`；`lr=0.5` 时 `π[0] = [0.378, 0.622]`，`lr=2.0` 时 `π[0] = [0.119, 0.881]`，`L^CLIP` 均为 `11.2`（无裁剪约 `19`）
- [ ] 未用 `sb3` 黑盒

---

## 9. 来源与后续入口

- **来源**：本作业为**课程自编形成性练习**（`source_type: local_integration_task`），非单一官方作业；题面与验收由本课程独立制定，参考 Sutton & Barto §13.7 与阶段 7 知识卡，未冒充官方作业。
- **后续入口**：完成即走完全部七阶段 lesson 练习；下一步进入 `[[强化学习-阶段作业-HW02-DQN与PPO连续动作控制|阶段作业 HW02：DQN 与 PPO]]`（阶段 7）或 `[[强化学习-大作业-从表格Q学习到深度策略梯度|大作业：从表格 Q 到深度策略梯度]]`。
- **复习卡**：`[[PPO近端策略优化]]`、`[[PPOClip-目标]]`、`[[GAE广义优势估计]]`、`[[优势-符号]]`。

---

## 🃏 知识内化卡片

- Q：PPO 为什么要「裁剪」？
- A：普通策略梯度用 `r(θ)·A` 当目标，`r` 过大会让单步更新过猛、训练崩溃。`L^CLIP = min(r·A, clip(r, 1−ε, 1+ε)·A)` 把 `r` 限制在 `[1−ε, 1+ε]` 内，超界就不再奖励更大的 ratio，等价于「保守策略迭代」的信任域近似。
- Q：PPO 与阶段 6 的 A2C 区别？
- A：A2C 每步用 `A` 做一次 on-policy 更新；PPO 在同一批数据上做多 epoch 小更新，并用裁剪防止偏离旧策略过远，样本效率更高、更稳定。
