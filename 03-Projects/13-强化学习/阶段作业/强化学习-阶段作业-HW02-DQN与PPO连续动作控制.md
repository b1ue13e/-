---
type: project
project_type: homework
course: "强化学习"
title: "强化学习-阶段作业-HW02-DQN与PPO连续动作控制"
assignment_id: "HW02"
assignment_level: stage
assignment_format: lab
stage_id: "07"
requires:
  - "[[动态规划：策略与值迭代]]"
  - "[[值函数近似与 DQN]]"
  - "[[经验回放与目标网络]]"
  - "[[PPO近端策略优化]]"
  - "[[GAE-公式]]"
  - "[[🧭 强化学习-前置知识]]"
source_type: official_assignment
source_url: "https://github.com/berkeleydeeprlcourse/homework_fall2023"
created: 2026-08-06
updated: 2026-08-06
status: ongoing
flow: project
tags: [作业, 强化学习, 阶段作业, 深度RL]
---

# 强化学习-阶段作业-HW02-DQN与PPO连续动作控制

> 🎯 **作业目标**：从表格法动态规划热身，到手写带 Replay Buffer 的 DQN，再到连续动作空间下的 PPO（Clipped Surrogate + GAE）。本作业改编自 UC Berkeley CS285（Deep RL）2023 秋作业 HW1/HW2，按本课程阶段重排，是阶段 7（PPO）的综合动手训练。

---

## 1. 身份与边界

- **身份**：强化学习课程阶段作业（stage 级），核心落在阶段 7（PPO），含阶段 2/3/4 的算法热身。
- **对应知识**：`[[动态规划：策略与值迭代]]`、`[[值函数近似与 DQN]]`、`[[经验回放与目标网络]]`、`[[PPO近端策略优化]]`、`[[GAE-公式]]`。
- **边界（允许 / 禁止）**：
  - ✅ 允许：用 `torch` / `gymnasium` 自行实现 VI/PI、DQN 核心循环、PPO 核心循环（含网络）。
  - ❌ 禁止：直接调用 `stable_baselines3.PPO` / `DQN` 等黑盒完成核心算法（仅允许用 `sb3` 做对照基线）；禁止修改给定评测脚本的判定逻辑。
  - ⚠️ 提交需固定随机种子，保证可复现。

---

## 2. 环境与 Starter Code

- **官方来源**：UC Berkeley CS285 *Deep RL* — homework_fall2023（`HW1` 表格法 + `HW2` DQN/PPO）。
- **获取方式**：
  ```bash
  git clone https://github.com/berkeleydeeprlcourse/homework_fall2023
  ```
  将本作业需要的两个 notebook 下载/拷贝到本地：
  `03-Projects/13-强化学习/阶段作业/hw02_dqn_ppo.ipynb`（若使用单文件整合版）。
- **核心依赖**：`gymnasium`（或 `gym`）、`torch`、`pytest`、`numpy`。
- **运行方式**：
  ```bash
  pytest tests/test_dqn.py tests/test_ppo.py -q   # 自带单元测试
  python train_dqn.py --env CartPole-v1           # 自实现训练脚本
  ```

> 注：原始仓库按HW1/HW2分册；本作业把它们合并为「表格热身 → DQN → PPO」三个阶段，题号与仓库一致，未改动公式与提交语义。原 `03-Projects/projects-rl/hw02_dqn_ppo.ipynb` 路径已失效，以本文件指定的仓库为准。

---

## 3. 题目详述（自包含）

### A 阶段 — 表格法动态规划（热身，对应阶段 2/3）
在 Gym 表格型环境中实现：
- **Value Iteration**：同步 Bellman 最优备份至收敛，`getPolicy` 给出最优动作。
- **Policy Iteration**：策略评估（解 `V^π`）+ 贪心改进至稳定。
- 验收：离散 GridWorld/CartPole 上收敛步数 < 50，策略与参考最优一致。

### B 阶段 — Deep Q-Network（对应阶段 4/7）
实现 DQN 核心：
- 卷积/MLP 近似 `Q_θ(s,a)`；**经验回放（Replay Buffer）** 打破样本相关；**目标网络（Target Network）** 稳定 TD 目标。
- ε-greedy 探索；TD 目标 `y = r + γ·max_a' Q_{θ^-}(s',a')`。
- 验收：`CartPole-v1` 上 Reward ≥ 200；进阶在 `LunarLander-v2` 上 Reward ≥ 200+。
- 必含消融：去掉经验回放 / 去掉目标网络，量化性能衰减。

### C 阶段 — PPO 连续控制（对应阶段 7）
实现 PPO 核心：
- **Clipped Surrogate Objective**：对策略比率 `r_t(θ)=π_θ(a_t|s_t)/π_{θ_old}(a_t|s_t)` 施加 `clip(r_t, 1−ε, 1+ε)` 限制，防止单步更新过大。
- **GAE**（广义优势估计）：`A_t^GAE = Σ_l (γλ)^l δ_{t+l}`，`δ_t = r_t + γV(s_{t+1}) − V(s_t)`。
- 多 epoch 更新、连续动作用高斯策略 `π_θ(a|s)=N(μ_θ(s), σ)`。
- 验收：`LunarLander-v2`（连续）或 `HalfCheetah` 上稳定收敛；报告 KL 散度与裁剪命中率。

### D 阶段（可选进阶）— Model-Based / 采样效率
实现 MBPO 或 World Models，在 `BipedalWalker` / `HalfCheetah` 上对比「有模型」相对纯无模型的采样效率提升（目标 ≥ 5×）。

---

## 4. 提交产物

- 代码：`hw02_dqn_ppo.ipynb`（或 `train_dqn.py` + `train_ppo.py` + `models/`）+ `tests/`。
- 报告：`report.md` 含：三阶段回报曲线（mean±std，≥3 随机种子）、DQN 消融表、PPO 的 KL/裁剪命中率图、至少 1 个失败案例归因。
- 依赖：`requirements.txt` 或 `environment.yml`，固定 `torch` / `gymnasium` 版本。
- 禁止：用 `sb3` 黑盒替代核心实现（对照基线除外）。

---

## 5. 评分 Rubric（满分 100）

| 维度 | 分值 | 标准 |
| :--- | :---: | :--- |
| 表格法正确性（A） | 15 | VI/PI 收敛且策略最优，步数达标 |
| DQN 正确性（B） | 30 | Replay+Target+ε-greedy 齐全；CartPole≥200；消融量化 |
| PPO 正确性（C） | 35 | 裁剪目标 + GAE 实现正确；连续任务稳定收敛；KL/裁剪报告 |
| 实验严谨性 | 15 | 多种子、对照、消融、失败归因齐全 |
| 代码可复现 | 5 | 一键运行、种子固定、依赖清晰 |

---

## 6. 基础要求、必要提示与常见错误

- **必要提示**：PPO 的 `ratio` 用 `exp(log_prob_new − log_prob_old)` 数值更稳；GAE 从后向前递推；DQN 目标网络用 `θ^-` 软更新或定期复制。
- **常见错误**：① 把 `log_prob_old` 用新策略重算（ratio 恒为 1，失去约束）；② GAE 的 `γ` 与 PPO 更新用的 `γ` 不一致；③ DQN 在 `step()` 后未把 `done` 区分「终止/截断」导致 bootstrap 错误；④ 连续动作直接 `argmax`（应采样）；⑤ 忘记 `detach` 旧网络输出导致梯度泄漏。
- **本地断言（PPO 损失不 NaN）**：

```python
import torch
from rl_solvers import ppo_loss
log_probs_old = torch.tensor([-0.5, -0.5])
log_probs_new = torch.tensor([-0.4, -0.8])
advantages    = torch.tensor([1.0, -1.0])
loss = ppo_loss(log_probs_new, log_probs_old, advantages, clip_eps=0.2)
assert not torch.isnan(loss), "PPO Loss 不得计算为 NaN"
```

---

## 7. 可选进阶任务（非主任务前置）

- 在 `HalfCheetah` 上把 PPO 与 SAC 对照，比较样本效率。
- 给 DQN 加 `Double DQN` / `Dueling` 并量化收益。
- 用 MBPO 验证「有模型」相对无模型的 5× 采样效率提升。

---

## 8. 自检清单

- [ ] `pytest` 自带单测通过（DQN/PPO）
- [ ] CartPole-v1 Reward ≥ 200（DQN）
- [ ] PPO 在连续任务稳定收敛，报告含 KL / 裁剪命中率
- [ ] DQN 消融表、多种子曲线、失败归因均在 `report.md`

---

## 9. 来源与后续入口

- **来源**：改编自 UC Berkeley CS285 (Deep RL) 2023 秋作业 `HW1`（表格法 VI/PI）与 `HW2`（DQN/PPO），仓库 `github.com/berkeleydeeprlcourse/homework_fall2023`（MIT）。按本课程阶段重排并补中文题面，**未改动公式与提交语义**；VI/PI 子任务源自 HW1、DQN/PPO 源自 HW2，已如实标注。
- **后续入口**：完成本作业后挑战 `[[强化学习-大作业-从表格Q学习到深度策略梯度|大作业：从表格 Q 到深度策略梯度]]`，把四种范式在同一任务上横向对比。
- **复习卡**：`[[值函数近似与 DQN]]`、`[[经验回放与目标网络]]`、`[[PPO近端策略优化]]`、`[[GAE-公式]]`。

---

## 🃏 知识内化卡片

- Q：PPO 为何对策略比率 `r_t(θ)` 施加 `clip(r_t, 1−ε, 1+ε)`？
- A：剪切限制新旧策略之间的更新幅度，防止当优势 `A_t > 0` 或 `A_t < 0` 时新策略步长过大导致策略崩溃，保证近端单调改进。
- Q：GAE 的偏差—方差权衡是什么？
- A：λ 越接近 0，优势估计越偏（用单步 TD 误差，低方差）；λ 越接近 1，越接近 Monte Carlo 回报（低偏差、高方差）。GAE 用 `(γλ)^l` 加权折中。
- Q：经验回放与目标网络分别解决 DQN 的什么问题？
- A：经验回放打破时序相关、提升样本利用率；目标网络固定 TD 目标一段时间，避免「目标随自身移动」导致的发散。
