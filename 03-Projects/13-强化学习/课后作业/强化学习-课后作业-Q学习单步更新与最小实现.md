---
type: project
project_type: homework
course: "强化学习"
title: "强化学习-课后作业-Q学习单步更新与最小实现"
assignment_id: "RL-HW03"
assignment_level: lesson
assignment_format: exercise
stage_id: "04"
source_type: local_integration_task
accessed: "2026-08-07"
license: "[待验证]"
source: "本课程（强化学习）自编形成性练习；非任何名校官方作业，不冒充官方。"
created: 2026-08-07
status: ongoing
flow: project
tags: [作业, 强化学习, 课后作业, Q-Learning, SARSA, TD]
requires:
  - "[[时序差分与 Q-Learning]]"
  - "[[SARSA-更新]]"
  - "[[探索与利用]]"
  - "[[🧭 强化学习-前置知识]]"
  - "[[TD-0]]"
  - "[[QLvsSARSA-策略]]"
  - "[[QLvsSARSA-目标]]"
  - "[[QL-更新]]"
  - "[[局限-连续动作]]"
  - "[[SARSA-同策略]]"
  - "[[TD-自举]]"
  - "[[QL-收敛]]"
  - "[[局限-连续状态]]"
  - "[[TD-采样]]"
  - "[[QL-异策略]]"
  - "[[QLvsSARSA-风险]]"
  - "[[SARSA-名称]]"
  - "[[QL-最大化偏差]]"
  - "[[局限-离散限制]]"
  - "[[局限-维度灾难]]"
  - "[[TD-误差]]"
  - "[[TD0对比]]"
  - "[[MC方法]]"
  - "[[SARSA-收敛]]"
  - "[[QLvsSARSA-应用]]"
  - "[[DP方法]]"
---

# 强化学习-课后作业-Q学习单步更新与最小实现

> 🎯 **作业目标**：把时序差分（TD）的两大更新式——**Q-Learning（off-policy）**与 **SARSA（on-policy）**——从公式落到实处：手算单步更新、对比二者差异、再用 ≤30 行表格法在迷你网格上验证。对应阶段 4（Q-Learning），与阶段作业 P3 的「Pacman 综合实现」互补：本作业只练**单步更新与最小实现**。

---

## 1. 身份与边界

- **身份**：强化学习课程课后作业（lesson 级），对应阶段 4（Q-Learning）。
- **对应知识**：`[[时序差分与 Q-Learning]]`、`[[SARSA-更新]]`、`[[探索与利用]]`、`[[🧭 强化学习-前置知识]]`。
- **边界（允许 / 禁止）**：
  - ✅ 允许：纸笔推导 + 自写迷你网格表格 Q-Learning / SARSA。
  - ❌ 禁止：直接调用 `sb3` 的 DQN/Q-learning 黑盒；禁止在 Q-Learning 目标里用 `s'` 的实际（ε-greedy）动作代替 `max`。
  - ⚠️ Q-Learning 目标是 `max_a' Q(s',a')`（off-policy）；SARSA 目标是 `Q(s', a')`（a' 是 `s'` 处**实际**采取的动作，on-policy）。

---

## 2. 环境与最小依赖

- **环境**：纯 Python（dict 存 Q 表），或 numpy。无需 gym。
- **迷你网格**（题目内给出）：

```
3×1 格子：X → Y → Z（Z 终止）。
动作 Right：X→Y→Z（各 1.0）；Left 反向。
奖励：每步 −1；到达 Z 额外 +10（R(Y,Right,Z)=+10）。折扣 γ=0.9，α=0.5，ε=0.1。
```

**表格 Q-Learning / SARSA Starter（可直接运行，存为 `rl_hw03_td.py`）**：

```python
import numpy as np, random

gamma, alpha, eps = 0.9, 0.5, 0.1

def reward(s, a):
    # 每步 -1；从 Y 经 Right 到达 Z 额外 +10
    return 10.0 if (a == 0 and s == 1) else -1.0

def nxt(s, a):
    # Right: X->Y->Z(终止)；Left 反向
    return min(s + 1, 2) if a == 0 else max(s - 1, 0)

def act(Q, s):
    return random.randint(0, 1) if random.random() < eps else int(np.argmax(Q[s]))

def run(algo):
    Q = np.zeros((3, 2)); rets = []
    for _ in range(500):
        s, G = 0, 0.0
        while s != 2:                       # Z(state 2) 终止
            a = act(Q, s); ns = nxt(s, a); r = reward(s, a)
            if algo == 'ql':
                tgt = r + gamma * Q[ns].max() if ns != 2 else r          # off-policy
            else:
                na = act(Q, ns) if ns != 2 else 0
                tgt = r + gamma * Q[ns, na] if ns != 2 else r            # on-policy
            Q[s, a] += alpha * (tgt - Q[s, a]); G += r; s = ns
        rets.append(G)
    return Q, rets

for algo in ['ql', 'sarsa']:
    Q, rets = run(algo)
    print(algo, "平均回报(last100) =", round(float(np.mean(rets[-100:])), 2))
```

---

## 3. 题目详述（自包含）

### Q1 — Q-Learning 单步手算
参数 `α=0.5, γ=0.9`。当前 `Q(X,Right)=0`，采样 `(X,Right,r=−1,Y)`，且 `max_a' Q(Y,a')=2.0`。
- 手算 Q-Learning 更新：`Q(X,Right) ← Q + α[r + γ·max Q(Y,·) − Q]`。给出结果。

### Q2 — SARSA vs Q-Learning 对比
同一过渡，但给出 `s'` 处**实际下一步动作** `a'=Right`，且 `Q(Y,Right)=1.5`。
- (a) 手算 SARSA 更新：`Q(X,Right) ← Q + α[r + γ·Q(Y,a') − Q]`。
- (b) 对比 Q1 的 Q-Learning 结果，二者差多少？为什么？
- (c) 直觉：在「悬崖行走」中，为何 SARSA 通常比 Q-Learning 更保守（学到离悬崖更远的安全路径）？

### Q3 — 最小实现
用 ≤30 行实现表格 Q-Learning 与 SARSA（共用迷你网格）：
- ε-greedy 探索；每算法跑 500 episode，记录每 episode 总回报。
- 输出：两种算法平均回报曲线，并说明谁更快学到到达 Z 的高回报路径。
- 评测：Q-Learning 在已知模型下往往回报更高（学最优），SARSA 更稳但可能略保守。

---

## 4. 提交产物

- 代码：`rl_hw03_td.py` 或 notebook（含 Q1/Q2 手算的对照断言）。
- 说明：`README` ≤150 字，给出 Q1 结果、Q2(a) 结果与二者差值、Q3 的回报曲线结论。

---

## 5. 评分 Rubric（满分 100）

| 维度 | 分值 | 标准 |
| :--- | :---: | :--- |
| Q-Learning 手算（Q1） | 25 | 更新式正确，数值正确（应为 `0+0.5[−1+0.9·2−0]=0.4`） |
| SARSA 对比（Q2） | 35 | SARSA 数值正确；差异与 cliff 直觉正确 |
| 最小实现（Q3） | 30 | 两算法实现正确；回报曲线符合直觉 |
| 代码与说明 | 10 | 简洁、可复现、README 清晰 |

---

## 6. 基础要求、必要提示与常见错误

- **必要提示**：Q-Learning 的 TD 目标用 `max_a' Q(s',a')`（**不**依赖 `s'` 实际动作）；SARSA 用 `Q(s', a')` 中 `a'` 是 `s'` 处**真实执行的动作**（样本里的下一步）。
- **常见错误**：① Q-Learning 目标误用 `s'` 的 ε-greedy 动作（那会变成 SARSA 且失去 off-policy 性质）；② 更新式漏掉旧值项，写成 `Q ← α·target`；③ SARSA 把 `a'` 取成 `max` 而非样本中的实际动作；④ 终止态 `Z` 之后还去查 `Q(Z,·)`（应直接 `target=r`，无 `γ·V(s')` 项）。
- **本地断言（Q1 速验）**：

```python
alpha, gamma = 0.5, 0.9
Q = 0.0; r = -1.0; maxQ_next = 2.0
Q = Q + alpha * (r + gamma * maxQ_next - Q)
assert abs(Q - 0.4) < 1e-9   # Q-Learning 单步结果
```

---

## 7. 可选进阶任务（非主任务前置）

- 给迷你网格加随机转移（Right 0.8 成功），重跑并对比确定转移。
- 实现 **Expected SARSA**（目标取对 `π` 的期望而非单样本 a'），对比方差。
- 在更大网格上手算一次 Q-Learning 备份，验证与代码一致。

---

## 8. 自检清单

- [ ] Q1 结果 = 0.4（数值正确）
- [ ] Q2(a) SARSA 结果正确，且说明与 Q-Learning 的差异来源
- [ ] Q3 两种算法均学到到达 Z 的高回报路径
- [ ] 未用 sb3 黑盒；Q-Learning 目标确为 `max`

---

## 9. 来源与后续入口

- **来源**：本作业为**课程自编形成性练习**（`source_type: local_integration_task`），非单一官方作业；题面与验收由本课程独立制定，参考 Sutton & Barto §6.4–6.5 与阶段 4 知识卡，未冒充官方作业。
- **后续入口**：本作业后进入 `[[强化学习-阶段作业-CS188-P3-Q学习与近似Q学习|阶段作业 P3：Q-Learning 与近似 Q-Learning]]`（Gridworld/Pacman 综合实现），挑战 `[[强化学习-阶段作业-HW02-DQN与PPO连续动作控制|阶段作业 HW02：DQN 与 PPO]]`。
- **复习卡**：`[[时序差分与 Q-Learning]]`、`[[SARSA-更新]]`、`[[探索与利用]]`。

---

## 🃏 知识内化卡片

- Q：Q-Learning 与 SARSA 的更新目标有何不同？
- A：Q-Learning（off-policy）用 `max_a' Q(s',a')`；SARSA（on-policy）用样本里 `s'` 处**实际**动作 `a'` 的 `Q(s',a')`。仅这一处差异，决定二者行为不同。
- Q：为什么 SARSA 在悬崖行走中更保守？
- A：SARSA 的更新用**实际**会走的下一步动作，其中包含「踩到悬崖」的危险动作，于是把靠近悬崖的状态估值压低、学到远离悬崖的安全路径；Q-Learning 用 `max`，忽视该危险动作，路径更近但训练中可能真掉崖。
- Q：Q-Learning 为何是 off-policy？
- A：行为策略是 ε-greedy（用于采样），但学习目标是贪心 `max`，直接估计最优动作值；行为策略只影响采到的样本，不影响被学习的策略。


## 来源声明（诚实标注）

本作业 `source_type: local_integration_task`，为**本课程（强化学习）自编形成性练习**。
- 诚实说明：非任何名校官方作业，不冒充官方题面；题面与验收由本课程独立制定。
- 许可：[待验证]；访问日期 2026-08-07。
