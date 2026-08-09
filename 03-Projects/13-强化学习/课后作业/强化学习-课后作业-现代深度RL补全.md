---
type: project
project_type: homework
course: "强化学习"
title: "强化学习-课后作业-现代深度RL补全"
assignment_id: "RL-HW10"
assignment_level: lesson
assignment_format: exercise
stage_id: "07"
source_type: local_integration_task
accessed: "2026-08-07"
license: "[待验证]"
source: "本课程（强化学习）自编形成性练习，参考原始论文（见文末）；非任何名校官方作业，不冒充官方题面。"
created: 2026-08-07
status: ongoing
flow: project
tags: [作业, 强化学习, 课后作业, 广度补全]
requires:
  - "[[TD3 (Twin Delayed DDPG)]]"
  - "[[最大熵RL]]"
  - "[[CQL (Conservative Q-Learning)]]"
  - "[[BCQ (Batch-Constrained Q-learning)]]"
  - "[[TD3+BC]]"
  - "[[DPO (Direct Preference Optimization)]]"
---

# 强化学习-课后作业-现代深度RL补全

> 🎯 **作业目标**：把阶段7的"现代深度RL补全"四块——连续控制(TD3)、最大熵(SAC基础)、离线RL(CQL/BCQ/TD3+BC)、偏好优化(DPO)——从公式落到手算与最小实现。对应阶段7扩展，与 HW02(深度连续控制)、HW07(PPO)互补。

---

## 1. 身份与边界

- **身份**：课后作业(lesson级)，对应阶段7扩展（现代深度RL补全）。
- **对应知识**：TD3 / 最大熵RL / CQL / BCQ / TD3+BC / DPO。
- **边界**：✅ 允许纸笔推导 + 自写 ≤40 行 numpy 最小实现；❌ 禁止把本作业标榜为某名校官方作业。

---

## 2. 题目详述（自包含）

### Q1 — TD3 双Q目标手算
参数 γ=0.99, r=−1；Q_{θ1'}=3.0, Q_{θ2'}=1.0。
- 手算 y = r + γ·min(Q_{θ1'}, Q_{θ2'})。给出结果并说明"为何取 min 而非均值/最大值"。

### Q2 — 最大熵 softmax 策略
两动作 Q=[2, 1]，α=1。求 π(a1), π(a2) 与熵 H = −Σπ·lnπ。

### Q3 — CQL 正则直觉
简述 CQL 正则项 R(θ)=E_{a~μ}[Q] − E_{a~πβ}[Q] 的作用；为何它能抑制分布外(OOO)过估计？

### Q4 — DPO 损失手算
偏好对 (y_w 胜 y_l)：logπ_θ(y_w)=−1.0, logπ_ref(y_w)=−1.2；logπ_θ(y_l)=−2.0, logπ_ref(y_l)=−1.5；β=0.5。
- 手算 L_DPO 内部的 σ 自变量值与损失值（应 ≈ 0.534）。

### Q5 — 最小实现（TD3+BC actor 损失）
用 ≤40 行 numpy 实现 TD3+BC 的 actor 损失：loss = −Q(s, π(s)).mean() + λ·((π(s) − a_data)^2).mean()。
给定随机 (s, a_data) 小批量，验证 loss 随 λ 增大而偏向贴合数据。

---

## 3. 评分 Rubric（满分100）

| 维度 | 分值 | 标准 |
| :--- | :---: | :--- |
| Q1 双Q | 20 | y=−0.01，min 理由正确 |
| Q2 softmax | 20 | π, H 正确 |
| Q3 CQL | 20 | 正则作用正确 |
| Q4 DPO | 20 | 损失 ≈ 0.534 |
| Q5 实现 | 20 | 代码正确、λ 行为符合直觉 |

---

## 4. 参考论文（知识点来源，非官方作业）

Fujimoto 2018 (TD3); Haarnoja 2018 (SAC/最大熵); Kumar 2020 (CQL); Fujimoto 2019 (BCQ); Fujimoto & Gu 2021 (TD3+BC); Rafailov 2023 (DPO)。

---

## 5. 环境与 Starter（可直接运行）

> 纯标准库实现，无需安装任何依赖。把下面代码存为 `starter_hw10.py` 后 `python starter_hw10.py` 即可运行，
> 用它核对 Q1/Q2/Q4 的手算值，并以 Q5 的骨架检验你的 ≤40 行实现。

```python
import math, random
# Q1: TD3 双Q目标
gamma, r = 0.99, -1.0
q1p, q2p = 3.0, 1.0
y = r + gamma * min(q1p, q2p)
print("Q1 y =", round(y, 4), "(期望 -0.01)")
# Q2: 最大熵 softmax 策略
Q = [2.0, 1.0]; alpha = 1.0
m = max(q/alpha for q in Q)
exps = [math.exp(q/alpha - m) for q in Q]
Z = sum(exps); pi = [e/Z for e in exps]
H = -sum(p*math.log(p) for p in pi)
print("Q2 pi =", [round(x,4) for x in pi], "H =", round(H,4))
# Q4: DPO 损失
def logsig(x): return -math.log(1+math.exp(-x))
lw_t, lw_r = -1.0, -1.2; ll_t, ll_r = -2.0, -1.5; beta = 0.5
arg = beta*((lw_t-lw_r)-(ll_t-ll_r)); loss = -logsig(arg)
print("Q4 DPO arg =", round(arg,4), "loss =", round(loss,4), "(期望 ~0.534)")
# Q5 骨架: TD3+BC actor 损失
def td3bc_loss(Q_of, pi_s, a_data, lam):
    adv = sum(Q_of(pi_s[i], a) for i,a in enumerate(a_data)) / len(a_data)
    bc  = sum((pi_s[i]-a)**2 for i,a in enumerate(a_data)) / len(a_data)
    return -adv + lam*bc
random.seed(0); pi_s=[0.5,0.5,0.5]; a_data=[0.4,0.6,0.3]
def Q_of(a_pred, a_data_i): return a_pred - a_data_i
for lam in [0.0, 1.0, 5.0]:
    print(f"Q5 lambda={lam} loss={td3bc_loss(Q_of, pi_s, a_data, lam):.4f}")
```

---

## 6. 来源声明（诚实标注）

本作业 `source_type: local_integration_task`，为**本课程（强化学习）自编形成性练习**。
- 诚实说明：非任何名校官方作业，不冒充官方题面；题面与验收由本课程独立制定，参考下列原始论文作为知识点来源（论文引用不等于官方作业）。
- 许可：[待验证]；访问日期 2026-08-07。
